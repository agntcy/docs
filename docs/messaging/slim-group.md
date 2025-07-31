# SLIM Group Managment

One of the most important caracteristics of SLIM is that it allows secure group communincation.
A gruop in SLIM is a set of clients that can communicate together using a shared channel. The channel is
identified by a name, as described in [SLIM Messaging Layer](slim-data-plane.md). In addition, when MLS is
enable, the group communincation is protected by end-to-end encryption.

Here you will find all the information required to create a gruop
in a SLIM network.

 ## Gruop Creation Using a Moderator

 As descibe in [SLIM Messaging Layer](slim-data-plane.md), a gruop is managed by a moderator.
 A moderator is a particular client that is able to create a Channel, add and remove clients and performs the 
 functions delegeated to the delivery service by the MLS protocol.

 The moderator uses the SLIM python bindings in order to setup a group session and configure all the 
 required state to allow secure communication between participants. The moderator is part of a python application
 and it can be part of the communincation process implementing some logic, or it can be just used to moderate 
 the channel. A full example on how to use the moderator
 can be found in the [SLIM Group Communication Tutorial](slim-group-tutorila.md). Here we report the basic steps to follow
 with snipets of python code to setup a group.

- **Create the moderator**:  The moderator is created by creating a Streaming bidirectional session that
will create the corresponding state in the SLIM session layer. In this example the communication between 
partcipants will be encrypted end-to-end as MLS is enabled.

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

-  **Invite Client to the Channel**:  Now the moderator needs to invite other partcipants to the 
channel. Notice that not all particpants needs to be added at the beginning but they can be add also later.

```python
    # Invite other members to the session.
    for invitee in invitees:
        print(f"Inviting {invitee}")
        await slim_app.set_route(invitee)  # Allow messages to be sent to the invitee.
        await slim_app.invite(
            session_info, invitee
        )  # Send an invitation to the invitee.
```

-  **The participants need to listen**: In other to receive the invitation to the channel each participant 
needs to listen for incoming messages. Notice the the invite message will be sent on the name of the particpant
and not on the channel as the partcipant doesn't know the channel yet

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

At this point the group it set and the clients can start to exchange messages.
However this configuration is not reflected the SLIM Controller automatically and so it as to be reported manually
into the controller. In particular, if the SLIM network is composed by multiple nodes the registration to
the control plane is mandatory in order to properly setup the routes between nodes as the goup setup 
by the moderator itself can work out of the box only is a singlo SLIM node is present in the network.

In the next session we will describe out to register the new created group in the SLIM controller and 
how to properly set the routes between the nodes

## How to use the north bound control plane API

Laszlo - add commands for this part

- 1 create the group
- 2 add clients to the group
- 3 set the routes for the group name between slim nodes

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

#### [The SPIFFE Helper](https://github.com/spiffe/spiffe-helper)

The [SPIFFE Helper](https://github.com/spiffe/spiffe-helper) is a simple utility
for fetching X.509 SVID certificates and JWT tokens from the SPIFFE Workload API.
It can be used to obtain the JWT tokens for SLIM clients, which can then be used
to authenticate clients and establish their identities in the SLIM network.

As tokens are normally short-lived, the SPIFFE Helper can be used to
automatically refresh the tokens when they expire, ensuring that clients always
have a valid identity.

SPIFFE Helper can be run as a sidecar container in the SLIM client pods, ensuring
that the client can always access a valid JWT token. The SLIM clients can then
use the token to authenticate itself with the SLIM network.

#### Run SPIFFE Helper as sidecar container

To run the SPIFFE Helper as a sidecar container, you can add it to your SLIM
client's pod definition. First you need to create a ConfigMap with the SPIFFE Helper
configuration, which will be mounted as a volume in the pod. Here is an example
of how to create the ConfigMap:

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