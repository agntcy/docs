# SLIM Group Creation

One of the key features of [SLIM](slim-core.md) is its support for secure group communication.
In SLIM, a group consists of multiple clients that communicate through a shared
channel. Each channel is identified by a unique name, as described in the [SLIM
Messaging Layer](slim-data-plane.md). When MLS is enabled, group
communication benefits from end-to-end encryption.

This guide provides all the information you need to create and manage groups within a
SLIM network.

## Creating Groups with the Python Bindings


This section shows how to use the SLIM Python bindings to create a group.
This requires a [multicast session](./slim-session.md#multicast). A multicast
session is a channel shared among multiple participants and used to
send messages to everyone. When a new participant wants to join the channel,
they must be invited by the channel creator.

The channel creator can be part of a Python application and can either
actively participate in the communication process (possibly implementing some
of the application logic) or serve solely as a channel moderator. For a complete
example of how to use the moderator, see the [SLIM Group
Communication Tutorial](slim-group-tutorial.md).

This section provides the basic
steps to follow, along with Python code snippets, for setting up a multicast session.
A complete [example](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/examples/src/slim_bindings_examples/multicast.py) of group communication can be found in the SLIM repo, in addition
to a related [README](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/examples/src/slim_bindings_examples/README_multicast.md) with explanations on how to run it.

### Create the Channel

The channel can be created by instantiating a Multicast session,
which initializes the corresponding state in the SLIM session layer.
In this example, communication between participants will be encrypted
end-to-end, as MLS is enabled.

```python
created_session = await local_app.create_session(
    slim_bindings.PySessionConfiguration.Multicast(  # type: ignore  # Build multicast session configuration
        channel_name=chat_channel,  # Logical multicast channel (PyName) all participants join; acts as group/topic identifier.
        max_retries=5,  # Max per-message resend attempts upon missing ack before reporting a delivery failure.
        timeout=datetime.timedelta(
            seconds=5
        ),  # Ack / delivery wait window; after this duration a retry is triggered (until max_retries).
        mls_enabled=enable_mls,  # Enable Messaging Layer Security for end-to-end encrypted & authenticated group communication.
    )
)
```

### Invite Participants to the Channel

Once the multicast session is created, new participants can be invited
to join. Not all participants need to be
added initially; you can add them later, even after communication
has already started.

```python
# Invite each provided participant. Route is set before inviting to ensure
# outbound control messages can reach them. For more info see
# https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/SESSION.md#invite-a-new-participant
for invite in invites:
    invite_name = split_id(invite)
    await local_app.set_route(invite_name)
    await created_session.invite(invite_name)
    print(f"{local} -> add {invite_name} to the group")
```

### Listen for Invitations and Messages

Participants that need to join the group start without a session and wait to be
invited. To wait for an invitation, the application calls `listen_for_session`.
When an invite message is received, a new session is created at the SLIM session layer,
and `listen_for_session` returns the metadata for the newly created session.

```python
format_message_print(local, "-> Waiting for session...")
session = await local_app.listen_for_session()
```


At this point, when a session is available, the participant can start listening for messages:

```python
while True:
    try:
        # Await next inbound message from the multicast session.
        # The returned parameters are a message context and the raw payload bytes.
        # Check session.py for details on PyMessageContext contents.
        ctx, payload = await session.get_message()
        format_message_print(
            local,
            f"-> Received message from {ctx.source_name}: {payload.decode()}",
        )
    except asyncio.CancelledError:
        # Graceful shutdown path (ctrl-c or program exit).
        break
    except Exception as e:
        # Non-cancellation error; surface and exit the loop.
        format_message_print(local, f"-> Error receiving message: {e}")
        break
```

The next section describes how to register the newly created group
with the SLIM Controller and configure routes between nodes.

## Creating Groups with the SLIM Controller

The controller API exposes operations to manage SLIM groups. You can use this API in client
applications to create and manage SLIM groups, add clients to
groups, and set routes between SLIM nodes.

You can generate gRPC API SDKs from the [schema
registry](https://buf.build/agntcy/slim/sdks/main:protobuf).

The following sections show example Python code fragments:

### Creating a SLIM Channel

```python
import grpc
from controlplane.v1 import controlplane_pb2_grpc as controlplane_api
from controlplane.v1 import controlplane_pb2

# Create gRPC connection
channel = grpc.insecure_channel("localhost:50051")
client = controlplane_api.ControlPlaneServiceStub(channel)

# Create channel request
create_channel_request = controlplane_pb2.CreateChannelRequest(
    moderators=["agntcy/namespace/moderator"]  # Name of the moderator
)

try:
    response = client.CreateChannel(create_channel_request)
    channel_id = response.channel_id

    if not response:
        print("\nNo channels found")
        return

    print(f"Channel created with ID: {channel_id}")

except grpc.RpcError as e:
    print(f"Request failed: {e}")
finally:
    channel.close()
```

### Adding Participants to a SLIM Group

```python
import grpc
from controlplane.v1 import controlplane_pb2_grpc as controlplane_api
from controlplane.v1 import controlplane_pb2

# Create gRPC connection
channel = grpc.insecure_channel("localhost:50051")
client = controlplane_api.ControlPlaneServiceStub(channel)

# Add participant request
add_participant_request = controlplane_pb2.AddParticipantRequest(
    participant_id="agntcy/namespace/participant_1",
    channel_id="agntcy/namespace/group_channel"
)

try:
    ack = client.AddParticipant(add_participant_request)

    print(f"ACK received for {ack.original_message_id}: success={ack.success}")

except grpc.RpcError as e:
    print(f"Request failed: {e}")
finally:
    channel.close()
```

### Setting Routes Between SLIM Nodes

```python
import grpc
from controlplane.v1 import controlplane_pb2_grpc as controlplane_api
from controlplane.v1 import controlplane_pb2
from grpc_api import grpc_api_pb2 as grpcapi

# Create gRPC connection
channel = grpc.insecure_channel("localhost:50051")
client = controlplane_api.ControlPlaneServiceStub(channel)

try:
    # Create connection to the target node
    connection = grpcapi.Connection(
        connection_id="http://127.0.0.1:46357",
        config_data='{"endpoint": "http://127.0.0.1:46357"}'
    )

    create_connection_request = controlplane_pb2.CreateConnectionRequest(
        connection=connection,
        node_id="slim/0"
    )

    create_connection_response = client.CreateConnection(create_connection_request)

    if not create_connection_response.success:
        raise Exception("Failed to create connection")

    connection_id = create_connection_response.connection_id
    print(f"Connection created successfully with ID: {connection_id}")

    # Add subscription for a group to a SLIM node
    subscription = grpcapi.Subscription(
        component_0="agntcy",
        component_1="namespace",
        component_2="group_channel",
        connection_id=connection_id
    )

    create_subscription_request = controlplane_pb2.CreateSubscriptionRequest(
        node_id="slim/0",
        subscription=subscription
    )

    create_subscription_response = client.CreateSubscription(create_subscription_request)

    if not create_subscription_response.success:
        raise Exception("Failed to create subscription")

    print(f"Subscription created successfully with ID: {create_subscription_response.subscription_id}")

except grpc.RpcError as e:
    print(f"gRPC error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    channel.close()
```

## Identity Management

To set up an MLS group, each client needs to have a valid identity. In the [SLIM
Group Communication Tutorial](slim-group-tutorial.md), we used a simple shared
secret to quickly set up identities for the clients. In a real-world scenario,
you would typically use a more secure method, such as tokens or certificates, to
authenticate clients and establish their identities.

SLIM supports JWT (JSON Web Tokens) for identity management. Tokens can come
from an external identity provider or can be generated by the SLIM nodes
directly if you provide the necessary private key for signing the tokens and
public key for verification. Check the [Identity
Test](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/tests/test_identity.py)
for an example of how to use JWT tokens with SLIM if you have your own keys.

If you are running your SLIM clients in a Kubernetes environment, a very common
approach to give an identity to each client is to use SPIRE
(https://spiffe.io/). SPIRE provides a way to issue [SPIFFE
IDs](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/#spiffe-id) to
workloads, in the form of JWT tokens, which SLIM can then use to
authenticate clients. This allows for secure and scalable identity management in
distributed systems.

### Using SPIRE with SLIM

SLIM integrates well with SPIRE, as it allows you to use the JWT tokens
generated by SPIRE as client identities, and at the same time it can verify
these tokens using the key bundle provided by SPIRE. This section shows how to
use SPIRE with SLIM to manage client identities in a group communication
scenario.

#### Installing SPIRE and Creating a ClusterSPIFFEID CRD

To use SPIRE with SLIM, you need to have a SPIRE server and agent running in
your environment. You can follow the [SPIRE installation
guide](https://artifacthub.io/packages/helm/spiffe/spire#install-instructions)
to install SPIRE using Helm in a Kubernetes cluster, and to assign a SPIFFE ID
to each of your workloads.

#### The SPIFFE Helper

The [SPIFFE Helper](https://github.com/spiffe/spiffe-helper) is a simple utility
for fetching X.509 SVID certificates and JWT tokens from the SPIFFE Workload
API. You can use it to obtain the JWT tokens for SLIM clients, which can then be
used to authenticate clients and establish their identities in the SLIM network.

Since tokens are normally short-lived, the SPIFFE Helper can be used to
automatically refresh the tokens when they expire, ensuring that clients always
have a valid identity.

You can run SPIFFE Helper as a sidecar container in the SLIM client pods,
ensuring that the client can always access a valid JWT token. The SLIM clients
can then use the token to authenticate themselves with the SLIM network.

#### Running SPIFFE Helper as a Sidecar Container

To run the SPIFFE Helper as a sidecar container, you can add it to your SLIM
client's pod definition. First you need to create a ConfigMap with the SPIFFE
Helper configuration, which will be mounted as a volume in the pod. Here is an
example of how to create the ConfigMap:

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: spiffe-helper-config
  labels:
    app: slim-client
data:
  helper.conf: |
    agent_address =  "/run/spire/agent-sockets/api.sock"
    cmd = ""
    cmd_args = ""
    cert_dir = "/svids"
    renew_signal = ""
    svid_file_name = "tls.crt"
    svid_key_file_name = "tls.key"
    svid_bundle_file_name = "svid_bundle.pem"
    jwt_bundle_file_name = "key.jwt"
    cert_file_mode = 0600
    key_file_mode = 0600
    jwt_svid_file_mode = 0600
    jwt_bundle_file_mode = 0600
    jwt_svids = [{jwt_audience="slim-demo", jwt_svid_file_name="jwt_svid.token"}]
    daemon_mode = true
EOF
```

Here we create a ConfigMap named `spiffe-helper-config` with the SPIFFE Helper
configuration. The configuration specifies the SPIFFE Workload API socket
address, the directory where the SVIDs will be stored, and the JWT audience for
the JWT SVIDs. The `daemon_mode` is set to `true`, which means the SPIFFE Helper
will run in the background and automatically refresh the SVIDs when they expire.

Next, you can add the SPIFFE Helper as a sidecar container in your SLIM client
pod definition. Here is an example of how to do that:

```yaml
apiVersion: v1
kind: Pod
metadata:
    name: slim-client
spec:
  containers:
  - name: slim-client
    image: ghcr.io/agntcy/slim:latest
    volumeMounts:
    - name: svids
        mountPath: /run/spiffe/svids
    - name: spiffe-helper-config
        mountPath: /etc/spiffe-helper
  - name: spiffe-helper
    image: ghcr.io/spiffe/spiffe-helper:latest
    imagePullPolicy: IfNotPresent
    args: [ "-config", "config/helper.conf" ]
    volumeMounts:
    - name: spiffe-helper-config
      mountPath: /config/helper.conf
      subPath: helper.conf
    - name: spire-agent-socket
      mountPath: /run/spire/agent-sockets
      readOnly: false
    - name: svids-volume
      mountPath: /svids
      readOnly: false
    volumes:
    - name: svids
      emptyDir: {}
    - name: spiffe-helper-config
      configMap:
        name: spiffe-helper-config
    - name: spire-agent-socket
      hostPath:
        path: /run/spire/agent-sockets
```

Notice that here we are using the SLIM node image as the main container, and the
SPIFFE Helper as a sidecar container. Normally the main container will be your
SLIM client application, which will use the JWT tokens generated by the SPIFFE
Helper to authenticate itself with the SLIM network.

#### Using the JWT SVID in Your SLIM Client

Once the SPIFFE Helper is running as a sidecar container, it will generate the
JWT SVIDs and store them in the `/svids` directory.

```
ls /svids/
jwt_svid.token  key.jwt  svid_bundle.pem  tls.crt  tls.key
```

You can then use the JWT SVID in your SLIM client application to authenticate
itself with the SLIM network. Here is how you can create a SLIM
PyIdentityProvider and PyIdentityVerifier using the JWT SVID:

```python
def jwt_identity(
    jwt_path: str = "/svids/jwt_svid.token",
    jwk_path: str = "/svids/key.jwt",
    iss: str = None,
    sub: str = None,
    aud: list = None,
):
    """
    Parse the JWK and JWT from the provided strings.
    """

    print(f"Using JWk file: {jwk_path}")

    with open(jwk_path) as jwk_file:
        jwk_string = jwk_file.read()

    # The JWK is normally encoded as base64, so we need to decode it
    spire_jwks = json.loads(jwk_string)

    for _, v in spire_jwks.items():
        # Decode first item from base64
        spire_jwks = base64.b64decode(v)
        break

    provider = slim_bindings.PyIdentityProvider.StaticJwt(
        path=jwt_path,
    )

    pykey = slim_bindings.PyKey(
        algorithm=slim_bindings.PyAlgorithm.RS256,
        format=slim_bindings.PyKeyFormat.Jwks,
        key=slim_bindings.PyKeyData.Content(content=spire_jwks.decode("utf-8")),
    )

    verifier = slim_bindings.PyIdentityVerifier.Jwt(
        public_key=pykey,
        issuer=iss,
        audience=aud,
        subject=sub,
    )

    return provider, verifier
```

A complete example of how to use the JWT SVID in a SLIM client can be found in
the examples in the [SLIM Python
Bindings](https://github.com/agntcy/slim/tree/slim-v0.4.0/data-plane/python-bindings/examples/src/slim_bindings_examples/common.py#L71-L112).

You can then use the provider and verifier to create a SLIM application exactly
as described in the [SLIM Group Tutorial](slim-group-tutorial.md#identity). In
the future we will provide even more provider and verifier implementations to
facilitate integrations with SLIM. We will also give developers the ability to
create their own providers and verifiers, so that they can use any identity
management system they want.
