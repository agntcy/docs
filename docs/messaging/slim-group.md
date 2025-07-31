# SLIM Group Managment

One of the key features of SLIM is its support for secure group communication.
In SLIM, a group consists of multiple clients that communicate through a shared
channel. Each channel is identified by a unique name, as described in the [SLIM
Messaging Layer](slim-data-plane.md). Additionally, when MLS is enabled, group
communication benefits from end-to-end encryption.

This document provides all the information you need to create a group within a
SLIM network.

## Group Creation Using a Moderator

As described in the [SLIM Messaging Layer](slim-data-plane.md), a group is
managed by a moderator. A moderator is a specific client with the ability to
create a channel, add or remove clients, and perform the functions that are
generly delegated to the Delivery Service in the MLS protocol.

The moderator uses the SLIM Python bindings to set up a group session and
configure all the required state to enable secure communication between
participants. The moderator is part of a Python application and can either
participate activelly in the communication process -possibly implementing some
of the application logic- or serve solely as a channel moderator. A complete
example on how to use the moderator can be found in the [SLIM Group
Communication Tutorial](slim-group-tutorila.md). Here, we provide the basic
steps to follow, along with Python code snippets, for setting up a group.

- **Step 1: Create the Moderator** The moderator is created by instantiating a
  streaming bidirectional session, which initializes the corresponding state in
  the SLIM session layer. In this example, communication between participants
  will be encrypted end-to-end, as MLS is enabled.

```python
    # Define the shared channel for group communication.
    # This channel will be used by all members of the group to exchange messages.
    shared_channel = PyName("agntcy", "namespace", "group_channel")

    # Create a new session. The group session is a bidirectional streaming session.
    # Here is where we enable the MLS protocol for end-to-end encryption.
    session_info = await slim_app.create_session(
        PySessionConfiguration.Streaming(
            PySessionDirection.BIDIRECTIONAL,
            topic=shared_channel,  # The channel ID for group communication.
            moderator=True,  # This session is created by the moderator.
            max_retries=5,  # Maximum number of retries for reliability.
            timeout=datetime.timedelta(seconds=5),  # Timeout for message delivery.
            mls_enabled=True,  # Enable MLS for end-to-end encryption.
        )
    )
```

- **Step 2: Invite Clients to the Channel** The moderator now needs to invite
  other participants to the channel. Note that not all participants need to be
  added at the beginning; they can also be added later, even after communication
  on the channel has already started.

```python
    # Invite other members to the session.
    for invitee in invitees:
        print(f"Inviting {invitee}")
        await slim_app.set_route(invitee)  # Allow messages to be sent to the invitee.
        await slim_app.invite(
            session_info, invitee
        )  # Send an invitation to the invitee.
```

- **Step 3: Listen from invites** To receive an invitation to the channel, each
  participant must listen for incoming messages The moderator will send the
  invite directly to the participant’s name, not via the channel, since the
  participant does not yet know the channel name.

```python
    async with participant_slim_app:
        # Listen for new sessions opened by moderators
        recv_session, _ = await participant_slim_app.receive()

        # Session is received, now we can read and write on the shared channel.
        print(f"Received session: {recv_session.id}")

        # Receive messages from the session
        recv_session, msg_rcv = await participant_slim_app.receive(session=recv_session.id)

        # Print the message
        print(f"Received: {msg_rcv.decode()}")
```

At this point, the group is set up and clients can start exchanging messages.
However, this configuration is not automatically reflected in the [SLIM
Controller](slim-controller.md) and must be reported manually. In particular, if
the SLIM network is composed of multiple nodes, registration with the control
plane is mandatory to properly set up routes between nodes. In the future, we
will automate this process to make it easier for developers. The group setup by
the moderator will work out of the box only if a single SLIM node is present in
the network.

In the next section, we will describe how to register the newly created group
with the SLIM Controller and how to properly configure routes between nodes.

## Group Creation Using SLIM Controller

The controller API exposes operations to manage SLIM groups. Client
applications can use this API to create and manage SLIM groups, add clients to
groups, and set routes between SLIM nodes.

GRPC API SDKs can be generated from the [schema
registry](https://buf.build/agntcy/slim/sdks/main:protobuf)

Example golang code fragments:

### Create a SLIM channel

```go
	conn, err := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	client := controlplaneApi.NewControlPlaneServiceClient(conn)

	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	createChannelRequest := &controlplaneApi.CreateChannelRequest{
		Moderators: []string{"agncty/namespace/moderator"}, // This is the name of the moderator
	}
	resp, err := client.CreateChannel(context.Background(), createChannelRequest)
	if err != nil {
		fmt.Printf("send request: %v", err.Error())
	}
	channelId := resp.GetChannelId()
	if resp == nil {
		fmt.Println("\nNo channels found")
		return
	}
	fmt.Printf("Received response: %v\n", channelId)
```

### Add clients to a SLIM group

```go
	conn, err := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	client := controlplaneApi.NewControlPlaneServiceClient(conn)

	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	addParticipantRequest := &controlplaneApi.AddParticipantRequest{
		ParticipantId: "agncty/namespace/participant_1",
		ChannelId:     "agncty/namespace/group_channel",
	}
	ack, err := client.AddParticipant(context.Background(), addParticipantRequest)
	if err != nil {
		fmt.Printf("send request: %v", err.Error())
	}

	fmt.Printf(
		"ACK received for %s: success=%t\n",
		ack.OriginalMessageId,
		ack.Success,
	)
```

### Set routes for the group name between slim nodes

```go
	conn, err := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	client := controlplaneApi.NewControlPlaneServiceClient(conn)

	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	createConnectionResponse, err := client.CreateConnection(context.Background(),
		&controlplaneApi.CreateConnectionRequest{
			Connection: &grpcapi.Connection{
				ConnectionId: "http://127.0.0.1:46357",
				ConfigData:   "{\"endpoint\": \"http://127.0.0.1:46357\"}",
			},
			NodeId: "slim/0",
		})
	if err != nil {
		log.Fatalf("failed to create connection: %w", err)
	}

	connectionID := createConnectionResponse.ConnectionId
	if !createConnectionResponse.Success {
		log.Fatal("failed to create connection")
	}
	fmt.Printf("Connection created successfully with ID: %v\n", connectionID)

    // add subscription for a group a SLIM node
	subscription := &grpcapi.Subscription{
		Component_0:  "agncty",
		Component_1:  "namespace",
		Component_2:  "group_channel",
		ConnectionId: connectionID,
	}

	createSubscriptionResponse, err := client.CreateSubscription(context.Background(), &controlplaneApi.CreateSubscriptionRequest{
		NodeId:       "slim/0",
		Subscription: subscription,
	})
	if err != nil {
		log.Fatalf("failed to create subscription: %w", err)
	}
	if !createSubscriptionResponse.Success {
		log.Fatalf("failed to create subscription")
	}
	fmt.Printf("Subscrption created successfully with ID: %v\n", createSubscriptionResponse.SubscriptionId)

```

## Identity management

To be able to setup a MLS group, each client needs to have a valid identity. In
the Group Communication Tutorial, we used a simple shared secret to quickly
setup identities for the clients. In a real-world scenario, you would typically
use a more secure method, such tokens or certificates, to authenticate clients
and establish their identities.

SLIM supports JWT (JSON Web Tokens) for identity management. Tokens can come
from an external identity provider or can be generated by the SLIM nodes
directly if we provide the necessary private key for signing the tokens and
public key for verification. Check the [Identity
Test](https://github.com/agntcy/slim/blob/main/data-plane/python-bindings/tests/test_identity.py)
for an example of how to use JWT tokens with SLIM if you have your own keys.

If you are running your SLIM clients in a k8s environment, a very common
approach to give an identity to each client is to use SPIRE
(https://spiffe.io/). SPIRE provides a way to issue [SPIFFE
IDs](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/#spiffe-id) to
workloads, in the form of JWT tokens, which can then be used by SLIM to
authenticate clients. This allows for secure and scalable identity management in
distributed systems.

### Using SPIRE with SLIM

SLIM integrates very well with SPIRE, as it allows to use the JWT tokens
generated by SPIRE as client identities, and at the same time it can verify
these tokens using key bundle provided by SPIRE. Here we will show how to use
SPIRE with SLIM to manage client identities in a group communication scenario.

#### Install SPIRE and create a ClusterSPIFFEID CRD

To use SPIRE with SLIM, you need to have a SPIRE server and agent running in
your environment. You can follow the [SPIRE installation
guide](https://artifacthub.io/packages/helm/spiffe/spire#install-instructions)
to install SPIRE using Helm in a Kubernetes cluster, and to assign a spiffe ID
to each one of your workloads.

Here is a quick example of how to install SPIRE and create a ClusterSPIFFEID
CRD:

```bash
helm upgrade --install -n spire-server spire-crds spire-crds --repo https://spiffe.github.io/helm-charts-hardened/ --create-namespace
helm upgrade --install -n spire-server spire spire --repo https://spiffe.github.io/helm-charts-hardened/

kubectl apply -f - <<EOF
apiVersion: spire.spiffe.io/v1alpha1
kind: ClusterSPIFFEID
metadata:
  name: slim-workloads
labels:
    app: slim-client
spec:
  spiffeIDTemplate: "spiffe://domain.test/ns/{{ .PodMeta.Namespace }}/sa/{{ .PodSpec.ServiceAccountName }}"
EOF

```

#### The SPIFFE Helper

The [SPIFFE Helper](https://github.com/spiffe/spiffe-helper) is a simple utility
for fetching X.509 SVID certificates and JWT tokens from the SPIFFE Workload
API. It can be used to obtain the JWT tokens for SLIM clients, which can then be
used to authenticate clients and establish their identities in the SLIM network.

As tokens are normally short-lived, the SPIFFE Helper can be used to
automatically refresh the tokens when they expire, ensuring that clients always
have a valid identity.

SPIFFE Helper can be run as a sidecar container in the SLIM client pods,
ensuring that the client can always access a valid JWT token. The SLIM clients
can then use the token to authenticate itself with the SLIM network.

#### Run SPIFFE Helper as sidecar container

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

Notice that here we are using the slim node image as the main container, and the
SPIFFE Helper as a sidecar container. Normally the main container will be your
SLIM client application, which will use the JWT tokens generated by the SPIFFE
Helper to authenticate itself with the SLIM network.

#### Use the JWT SVID in your SLIM client

Once the SPIFFE Helper is running as a sidecar container, it will generate the
JWT SVIDs and store them in the `/svids` directory.

```
ls /svids/
jwt_svid.token	key.jwt  svid_bundle.pem  tls.crt  tls.key
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
Bindings](https://github.com/agntcy/slim/blob/main/data-plane/python-bindings/examples/src/slim_bindings_examples/common.py#L71-L112).

The provider and verifier can then be used to create a SLIM application exactly
as described in the [SLIM Group Tutorial](slim-group-tutorial.md#identity). In
the future we will provide even more provider and verifier implementations to
facilitate integrations with SLIM. Also we will give developers the ability to
create their own providers and verifiers, so that they can use any identity
management system they want.
