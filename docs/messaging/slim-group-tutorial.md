# SLIM Group Communication Tutorial

This tutorial will show how to set up a secure group communication system using
SLIM. The group will be created by defining a pub-sub session with a moderator,
which will invite the other members. Messages will be sent to the shared
channel, where every member can read and write. Messages are end-to-end
encrypted using the [MLS
protocol](https://datatracker.ietf.org/doc/html/rfc9420).

### Key Features

- **Name-based Addressing**: In SLIM, all endpoints (channels and clients) have
  a name, and messages use a name-based addressing scheme for content routing.
- **Session Management**: Allows for the creation and management of sessions
  with moderators.
- **Broadcast Messaging**: Facilitates broadcast messaging to multiple
  subscribers.
- **End-to-End Encryption**: Ensures secure communication using the [MLS
  protocol](https://datatracker.ietf.org/doc/html/rfc9420).

### Setting up the SLIM Instance

As all members of the group will be communicating via a SLIM network, we can set
up a SLIM instance representing the SLIM network. We will use the pre-built
docker image for this purpose.

First execute this command to create the SLIM configuration file. Details about
the configuration can be found in the [SLIM
Repo](https://github.com/agntcy/slim/tree/main/data-plane/config).

```bash
cat << EOF > ./config.yaml
tracing:
  log_level: info
  display_thread_names: true
  display_thread_ids: true

runtime:
  n_cores: 0
  thread_name: "slim-data-plane"
  drain_timeout: 10s

services:
  slim/0:
    pubsub:
      servers:
        - endpoint: "0.0.0.0:46357"
          tls:
            insecure: true

      clients: []
EOF
```

This configuration will start a SLIM instance with a server listening on port
46357, without TLS encryption for simplicity. Messages will be still encrypted
using the MLS protocol, but the connections between SLIM nodes will not use TLS.
In a production environment, it is recommended to always use TLS and configure
proper authentication and authorization mechanisms.

You can run the SLIM instance using Docker:

```bash
docker run -it \
    -v ./config.yaml:/config.yaml -p 46357:46357 \
    ghcr.io/agntcy/slim:latest /slim --config /config.yaml
```

If everything goes fine, you should see an output like this one:

```
2025-07-31T09:07:45.859161Z  INFO main ThreadId(01) application_lifecycle: slim: Runtime started
2025-07-31T09:07:45.859213Z  INFO main ThreadId(01) application_lifecycle: slim: Starting service: slim/0
2025-07-31T09:07:45.859624Z  INFO main ThreadId(01) application_lifecycle: slim_service: starting service
2025-07-31T09:07:45.859683Z  INFO main ThreadId(01) application_lifecycle: slim_service: starting server 0.0.0.0:46357
2025-07-31T09:07:45.859793Z  INFO main ThreadId(01) application_lifecycle: slim_service: server configured: setting it up config=ServerConfig { endpoint: 0.0.0.0:46357, tls_setting: TlsServerConfig { config: Config { ca_file: None, ca_pem: None, include_system_ca_certs_pool: false, cert_file: None, cert_pem: None, key_file: None, key_pem: None, tls_version: "tls1.3", reload_interval: None }, insecure: true, client_ca_file: None, client_ca_pem: None, reload_client_ca_file: false }, http2_only: true, max_frame_size: None, max_concurrent_streams: None, max_header_list_size: None, read_buffer_size: None, write_buffer_size: None, keepalive: KeepaliveServerParameters { max_connection_idle: 3600s, max_connection_age: 7200s, max_connection_age_grace: 300s, time: 120s, timeout: 20s }, auth: None }
2025-07-31T09:07:45.861393Z  INFO slim-data-plane ThreadId(11) slim_service: running service
```

### Configure Client Identity and Implementing the SLIM App

Each member of the group will run a local slim app instance that will be used to
communicate with the SLIM network. Also each member will have a unique identity
that will be used to authenticate the member in the SLIM network.

#### Identity

Each member of the group must have a unique identity. This is a requirement to
setup the end-to-end encryption using the MLS protocol. The identity can be
represented by a JWT, or a shared secret. For simplicity, we will use a shared
secret. You can find examples using JWT in the [SLIM
Repo](https://github.com/agntcy/slim/blob/main/data-plane/python-bindings/examples/src/slim_bindings_examples/common.py#L71-L112).

The python objects managing the identity are called `PyIdentityProvider` and
`PyIdentityVerifier`. The `PyIdentityProvider` is responsible for providing the
identity, while the `PyIdentityVerifier` is responsible for verifying the
identity.

```python
def shared_secret_identity(
    identity: str, secret: str
) -> tuple[PyIdentityProvider, PyIdentityVerifier]:
    """
    Create a provider and verifier using a shared secret.

    :param identity: A unique string, identifier of the app.
    :param secret: A shared secret used for authentication.
    :return: A tuple of (provider, verifier).
    """
    provider: PyIdentityProvider = PyIdentityProvider.SharedSecret(
        identity=identity, shared_secret=secret
    )
    verifier: PyIdentityVerifier = PyIdentityVerifier.SharedSecret(
        identity=identity, shared_secret=secret
    )

    return provider, verifier
```

#### SLIM App

The provider and the verifier will be used to create a local SLIM app, that can
be used to exchange messages with other apps via the SLIM network.

```python
async def create_slim_app(secret: str, local_name: PyName) -> PyService:
    """
    Create a SLIM app instance with the given shared secret.
    This app will be used to communicate with other SLIM nodes in the network.

    :param secret: A shared secret used for authentication.
    :param local_name: A unique name for the SLIM app instance.
                       It will be used to identify the app in the SLIM network.
    :return: A SLIM app instance.
    """

    # Create the provider and verifier using the shared secret.
    provider, verifier = shared_secret_identity(
        identity=f"{local_name}",
        secret=secret,
    )

    # Create the SLIM app. This is a in-process SLIM client that can be used to
    # exchange messages with other SLIM nodes in the network.
    slim_app = await Slim.new(local_name, provider, verifier)

    # Connect the SLIM app to the SLIM network.
    _ = await slim_app.connect(
        {"endpoint": "http://127.0.0.1:46357", "tls": {"insecure": True}}
    )

    # Return the SLIM app instance.
    return slim_app
```

### Implementing the Moderator

The moderator will be responsible for creating the group and inviting other
members. The moderator will create a session and send an invitation message to
the other members. The invitation will contain the session ID and the channel
name for the group communication.

The moderator can be implemented as a Python service using the SLIM SDK.

#### Creating the Session and Inviting Members

The moderator creates a session and invites other members to join the group. The
session will be identified by a unique session ID, and the group communication
will take place over a specific channel name. The moderator will be responsible
for managing the session lifecycle, including creating, updating, and
terminating the session as needed.

As each participant is provided with an identity, setting up MLS for end-to-end
encryption is straightforward. The moderator will create a session with the
`mls_enabled` flag set to `True`, which will enable the MLS protocol for the
session. This ensures that all messages exchanged within the session are
end-to-end encrypted, providing confidentiality and integrity for the group
communication.

```python
async def create_session_and_invite_members(
    slim_app: PyService, invitees: list[PyName]
):
    """
    Create a session with the given session ID and channel ID.

    :param slim_app: The SLIM app instance.
    :return: The created session.
    """

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

    print(f"Session created: {session_info}")

    # Invite other members to the session.
    for invitee in invitees:
        print(f"Inviting {invitee}")
        await slim_app.set_route(invitee)  # Allow messages to be sent to the invitee.
        await slim_app.invite(
            session_info, invitee
        )  # Send an invitation to the invitee.

    # Return the created session.
    return session_info

async def run_moderator(secret: str):
    local_name = PyName("agntcy", "namespace", "moderator")

    # Create the moderator SLIM app instance.
    moderator_slim_app = await create_slim_app(secret, local_name)

    # Define the invitees for the group session.
    invitees = [
        PyName("agntcy", "namespace", "participant1"),
    ]

    async with moderator_slim_app:
        # Create a session and invite the members.
        session_info = await create_session_and_invite_members(moderator_slim_app, invitees)

        # Wait for a bit to ensure all participants are ready.
        await asyncio.sleep(1)

        # Send a message to the group channel.
        await send_message(moderator_slim_app, session_info, "Hello group!")

        # Wait for a message from a participant
        _, msg = await moderator_slim_app.receive(session=session_info.id)

        # Print message
        print(f"Received message from participant: {msg.decode()}")
```

### Implementing the Group Participants

The group participants will be implemented similarly to the moderator, but they
will not create the session. They will create the SLIM service instance and wait
for invites sent by the moderator. Once they receive the invite, they can read
and write on the shared channel.

```python
async def run_participant(secret: str):
    local_name = PyName("agntcy", "namespace", "participant1")

    participant_slim_app = await create_slim_app(secret, local_name)

    print(f"Listening for sessions - locator: {local_name}")

    async with participant_slim_app:
        # Listen for new sessions opened by moderators
        recv_session, _ = await participant_slim_app.receive()

        # Session is received, now we can read and write on the shared channel.
        print(f"Received session: {recv_session.id}")

        # Receive messages from the session
        recv_session, msg_rcv = await participant_slim_app.receive(session=recv_session.id)

        # Print the message
        print(f"Received: {msg_rcv.decode()}")

        # Reply with a message
        await participant_slim_app.publish(
            recv_session,
            f"{msg_rcv.decode()} from participant".encode(),
            recv_session.destination_name,
        )

        # Wait to ensure message is sent
        await asyncio.sleep(1)
```

### Putting All Together

Here is the complete code to run the moderator and the participants in a single
script. You can run this script to see how the group communication works using
SLIM.

The same example can be found in the [SLIM examples
folder](https://github.com/agntcy/slim/tree/main/data-plane/python-bindings/examples).
In particular this tutorial is based on the
[pubsub.py](https://github.com/agntcy/slim/blob/main/data-plane/python-bindings/examples/src/slim_bindings_examples/pubsub.py)
example

#### moderator.py

```python
import asyncio
import datetime

from slim_bindings import (
    Slim,
    PyName,
    PyService,
    PyIdentityProvider,
    PyIdentityVerifier,
    PySessionConfiguration,
    PySessionDirection,
    init_tracing,
)


def shared_secret_identity(
    identity: str, secret: str
) -> tuple[PyIdentityProvider, PyIdentityVerifier]:
    """
    Create a provider and verifier using a shared secret.

    :param identity: A unique string, identifier of the app.
    :param secret: A shared secret used for authentication.
    :return: A tuple of (provider, verifier).
    """
    provider: PyIdentityProvider = PyIdentityProvider.SharedSecret(
        identity=identity, shared_secret=secret
    )
    verifier: PyIdentityVerifier = PyIdentityVerifier.SharedSecret(
        identity=identity, shared_secret=secret
    )

    return provider, verifier


async def create_slim_app(secret: str, local_name: PyName) -> PyService:
    """
    Create a SLIM app instance with the given shared secret.
    This app will be used to communicate with other SLIM nodes in the network.

    :param secret: A shared secret used for authentication.
    :param local_name: A unique name for the SLIM app instance.
                       It will be used to identify the app in the SLIM network.
    :return: A SLIM app instance.
    """

    # Create the provider and verifier using the shared secret.
    provider, verifier = shared_secret_identity(
        identity=f"{local_name}",
        secret=secret,
    )

    # Create the SLIM app. This is a in-process SLIM client that can be used to
    # exchange messages with other SLIM nodes in the network.
    slim_app = await Slim.new(local_name, provider, verifier)

    # Connect the SLIM app to the SLIM network.
    _ = await slim_app.connect(
        {"endpoint": "http://127.0.0.1:46357", "tls": {"insecure": True}}
    )

    # Return the SLIM app instance.
    return slim_app


async def create_session_and_invite_members(
    slim_app: PyService, invitees: list[PyName]
):
    """
    Create a session with the given session ID and channel ID.

    :param slim_app: The SLIM app instance.
    :return: The created session.
    """

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

    print(f"Session created: {session_info}")

    # Invite other members to the session.
    for invitee in invitees:
        print(f"Inviting {invitee}")
        await slim_app.set_route(invitee)  # Allow messages to be sent to the invitee.
        await slim_app.invite(
            session_info, invitee
        )  # Send an invitation to the invitee.

    # Return the created session.
    return session_info


async def send_message(slim_app: PyService, session_info, message: str):
    """
    Send a message to the group channel.

    :param slim_app: The SLIM app instance.
    :param session_info: The session information.
    :param message: The message to send.
    """

    # Send the message to the shared channel.
    await slim_app.publish(
        session_info,
        message.encode(),
        PyName("agntcy", "namespace", "group_channel"),
    )


async def run_moderator(secret: str):
    local_name = PyName("agntcy", "namespace", "moderator")

    # Create the moderator SLIM app instance.
    moderator_slim_app = await create_slim_app(secret, local_name)

    # Define the invitees for the group session.
    invitees = [
        PyName("agntcy", "namespace", "participant1"),
    ]

    async with moderator_slim_app:
        # Create a session and invite the members.
        session_info = await create_session_and_invite_members(
            moderator_slim_app, invitees
        )

        # Wait for a bit to ensure all participants are ready.
        await asyncio.sleep(1)

        # Send a message to the group channel.
        await send_message(moderator_slim_app, session_info, "Hello group!")

        # Wait for a message from a participant
        _, msg = await moderator_slim_app.receive(session=session_info.id)

        # Print message
        print(f"Received message from participant: {msg.decode()}")


def main():
    try:
        asyncio.run(run_moderator("shared_secret"))
    except KeyboardInterrupt:
        print("Client interrupted by user.")

```

#### participant.py

```python
import asyncio
import datetime

from slim_bindings import (
    Slim,
    PyName,
    PyService,
    PyIdentityProvider,
    PyIdentityVerifier,
    PySessionConfiguration,
    PySessionDirection,
    PySessionInfo,
    init_tracing,
)


def shared_secret_identity(
    identity: str, secret: str
) -> tuple[PyIdentityProvider, PyIdentityVerifier]:
    """
    Create a provider and verifier using a shared secret.

    :param identity: A unique string, identifier of the app.
    :param secret: A shared secret used for authentication.
    :return: A tuple of (provider, verifier).
    """
    provider: PyIdentityProvider = PyIdentityProvider.SharedSecret(
        identity=identity, shared_secret=secret
    )
    verifier: PyIdentityVerifier = PyIdentityVerifier.SharedSecret(
        identity=identity, shared_secret=secret
    )

    return provider, verifier


async def create_slim_app(secret: str, local_name: PyName) -> PyService:
    """
    Create a SLIM app instance with the given shared secret.
    This app will be used to communicate with other SLIM nodes in the network.

    :param secret: A shared secret used for authentication.
    :param local_name: A unique name for the SLIM app instance.
                       It will be used to identify the app in the SLIM network.
    :return: A SLIM app instance.
    """

    # Create the provider and verifier using the shared secret.
    provider, verifier = shared_secret_identity(
        identity=f"{local_name}",
        secret=secret,
    )

    # Create the SLIM app. This is a in-process SLIM client that can be used to
    # exchange messages with other SLIM nodes in the network.
    slim_app = await Slim.new(local_name, provider, verifier)

    # Connect the SLIM app to the SLIM network.
    _ = await slim_app.connect(
        {"endpoint": "http://127.0.0.1:46357", "tls": {"insecure": True}}
    )

    # Return the SLIM app instance.
    return slim_app


async def run_participant(secret: str):
    local_name = PyName("agntcy", "namespace", "participant1")

    participant_slim_app = await create_slim_app(secret, local_name)

    print(f"Listening for sessions - locator: {local_name}")

    async with participant_slim_app:
        # Listen for new sessions opened by moderators
        recv_session, _ = await participant_slim_app.receive()

        # Session is received, now we can read and write on the shared channel.
        print(f"Received session: {recv_session.id}")

        # Receive messages from the session
        recv_session, msg_rcv = await participant_slim_app.receive(
            session=recv_session.id
        )

        # Print the message
        print(f"Received: {msg_rcv.decode()}")

        # Reply with a message
        await participant_slim_app.publish(
            recv_session,
            f"{msg_rcv.decode()} from participant".encode(),
            recv_session.destination_name,
        )

        # Wait to ensure message is sent
        await asyncio.sleep(1)


def main():
    try:
        asyncio.run(run_participant("shared_secret"))
    except KeyboardInterrupt:
        print("Client interrupted by user.")
```

## Example: 1:1 Communication

The slim repository also includes examples of 1:1 communication sessions. Using
the SLIM SDK for 1:1 sessions is very similar to the approach demonstrated in
the group communication example. For reference, see the
[fire_and_forget.py](https://github.com/agntcy/slim/blob/main/data-plane/python-bindings/examples/src/slim_bindings_examples/fire_and_forget.py)
and
[request_reply.py](https://github.com/agntcy/slim/blob/main/data-plane/python-bindings/examples/src/slim_bindings_examples/request_reply.py)
files.

1:1 communication is particularly useful when you want to use SLIM as a
transport layer for protocols that are inherently point-to-point, such as MCP or
A2A. In these cases, you typically need to communicate with a single server, but
you can still benefit from the simplicity and security that the SLIM messaging
layer provides.

For a detailed guide on using MCP on top of SLIM, please refer to the [SLIM and
MCP Integration](slim-mcp.md) page.
