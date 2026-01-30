# SLIM Group Communication Tutorial

This tutorial shows how to set up secure group communication using
SLIM. The group is created by defining a group session and inviting
participants. Messages are sent to a shared channel where every member can read
and write. All messages are end-to-end encrypted using the
[MLS protocol](https://datatracker.ietf.org/doc/html/rfc9420). This tutorial is
based on the
[group.py](https://github.com/agntcy/slim/blob/slim-v1.0.0/data-plane/python/bindings/examples/src/slim_bindings_examples/group.py)
example in the SLIM repo.

## Key Features

- **Name-based Addressing**: In SLIM, all endpoints (channels and clients) have
  a name, and messages use a name-based addressing scheme for content routing.
- **Session Management**: Allows for the creation and management of sessions using
    both the SLIM Python Bindings and the SLIM Controller.
- **Broadcast Messaging**: Facilitates broadcast messaging to multiple
  subscribers.
- **End-to-End Encryption**: Ensures secure communication using the [MLS
  protocol](https://datatracker.ietf.org/doc/html/rfc9420).

## Configure Client Identity and Implement the SLIM App

Every participant in a group requires a unique identity for authentication and for use by the MLS protocol. This section explains how to set up identity and create a SLIM application instance.

### Identity

Each participant must have a unique identity. This is required to set up end-to-end encryption using the MLS protocol. The identity can be a JWT or shared secret. For simplicity, this example uses a shared secret. For JWT-based identity, see the [tutorial](https://github.com/agntcy/slim/tree/slim-v1.0.0/data-plane/python/bindings/examples#running-in-kubernetes-spire--jwt) in the SLIM repository.

The Python objects managing the identity are called `IdentityProvider` and `IdentityVerifier`. The `IdentityProvider` provides the identity, while the `IdentityVerifier` verifies it:

```python
def shared_secret_identity(identity: str, secret: str):
    """
    Create a provider & verifier pair for shared-secret (symmetric) authentication.
    """
    provider = slim_bindings.IdentityProvider.SharedSecret(
        identity=identity, shared_secret=secret
    )
    verifier = slim_bindings.IdentityVerifier.SharedSecret(
        identity=identity, shared_secret=secret
    )
    return provider, verifier
```

This is a helper function defined in
[common.py](https://github.com/agntcy/slim/blob/slim-v1.0.0/data-plane/python/bindings/examples/src/slim_bindings_examples/common.py#L85)
that can be used to create a `IdentityProvider` and `IdentityVerifier` from two input strings.

### SLIM App

The provider and verifier are used to create a local SLIM application that can exchange messages with other participants via the SLIM network. To create the SLIM app, use the helper function defined in [common.py](https://github.com/agntcy/slim/blob/slim-v1.0.0/data-plane/python/bindings/examples/src/slim_bindings_examples/common.py#L289):

```python
async def create_local_app(
    local: str,
    slim: dict,
    remote: str | None = None,
    enable_opentelemetry: bool = False,
    shared_secret: str = "abcde-12345-fedcb-67890-deadc",
    jwt: str | None = None,
    spire_trust_bundle: str | None = None,
    audience: list[str] | None = None,
    spire_socket_path: str | None = None,
    spire_target_spiffe_id: str | None = None,
    spire_jwt_audience: list[str] | None = None,
):
    """
    Build and connect a Slim application instance given user CLI parameters.

    Resolution precedence for auth:
      1. If jwt + bundle + audience provided -> JWT/JWKS flow.
      2. Else -> shared secret (must be provided, raises if missing).

    Args:
        local: Local identity string (org/ns/app).
        slim: Dict of connection parameters (endpoint, tls flags, etc.).
        remote: Optional remote identity (unused here, reserved for future).
        enable_opentelemetry: Enable OTEL tracing export.
        shared_secret: Symmetric secret for shared-secret mode.
        jwt: Path to static JWT token (for StaticJwt provider).
        spire_trust_bundle: Path to a spire trust bundle file (containing the JWKs for each trust domain).
        audience: Audience list for JWT verification.

    Returns:
        Slim: Connected high-level Slim instance.
    """
    # Initialize tracing (synchronous init; not awaited as binding returns immediately).
    slim_bindings.init_tracing(
        {
            "log_level": "info",
            "opentelemetry": {
                "enabled": enable_opentelemetry,
                "grpc": {
                    "endpoint": "http://localhost:4317",
                },
            },
        }
    )

    # Derive identity provider & verifier using JWT/JWKS if all pieces supplied.
    if jwt and spire_trust_bundle and audience:
        print("Using JWT + JWKS authentication.")
        provider, verifier = jwt_identity(
            jwt,
            spire_trust_bundle,
            aud=audience,
        )
    elif spire_socket_path or spire_target_spiffe_id or spire_jwt_audience:
        print("Using SPIRE dynamic identity authentication.")
        provider, verifier = spire_identity(
            socket_path=spire_socket_path,
            target_spiffe_id=spire_target_spiffe_id,
            jwt_audiences=spire_jwt_audience,
        )
    else:
        print("Using shared-secret authentication.")
        # Fall back to shared secret.
        provider, verifier = shared_secret_identity(
            identity=local,
            secret=shared_secret,
        )

    # Convert local identifier to a strongly typed Name.
    local_name = split_id(local)

    # Instantiate Slim (async constructor prepares underlying Service).
    local_app = slim_bindings.Slim(local_name, provider, verifier)

    # Provide feedback to user (instance numeric id).
    format_message_print(f"{local_app.id_str}", "Created app")

    # Establish outbound connection using provided parameters.
    _ = await local_app.connect(slim)

    # Confirm endpoint connectivity.
    format_message_print(f"{local_app.id_str}", f"Connected to {slim['endpoint']}")

    return local_app
```

This function takes several parameters as input:

- `local` (required, str): The SLIM name of the local application in the form
    `org/ns/service`.
- `slim` (required, dict): Configuration to connect to the remote SLIM node. For example:

```python
    {
        "endpoint": "http://127.0.0.1:46357",
        "tls": {"insecure": True},
    }
  ```

- `enable_opentelemetry` (bool, default: `False`): Enable OpenTelemetry
    tracing. If `True`, traces are sent to `http://localhost:4317` by default.
- `shared_secret` (str | None, default: `None`): Shared secret for identity and
    authentication. Required if JWT, bundle and audience are not provided.
- `jwt` (str | None, default: `None`): JWT token for identity. Used with
    `spire_trust_bundle` and `audience` for JWT-based authentication.
- `spire_trust_bundle` (str | None, default: `None`): JWT trust bundle
  (list of JWKs, one for each trust domain). Expected in JSON format such as:

  ```json
    {
        "trust-domain-1.org": "base-64-encoded-jwks",
        "trust-domain-2.org": "base-64-encoded-jwks",
        ...
    }
  ```

- `audience` (list[str] | None, default: `None`): List of allowed audiences for
    JWT authentication.
- `spire_socket_path` (str | None, default: `None`): Path to the SPIRE agent
    socket for dynamic identity authentication. When provided along with
    `spire_target_spiffe_id` and `spire_jwt_audience`, enables SPIRE-based
    authentication.
- `spire_target_spiffe_id` (str | None, default: `None`): The SPIFFE ID of the
    target service for SPIRE authentication. Used in conjunction with
    `spire_socket_path` and `spire_jwt_audience`.
- `spire_jwt_audience` (list[str] | None, default: `None`): List of audiences
    for SPIRE JWT authentication. Required when using SPIRE dynamic identity
    authentication along with `spire_socket_path` and `spire_target_spiffe_id`.

The function supports three authentication flows with the following precedence:

1. JWT/JWKS authentication (if `jwt`, `spire_trust_bundle`, and `audience` are provided)
2. SPIRE dynamic identity (if `spire_socket_path`, `spire_target_spiffe_id`, and `spire_jwt_audience` are provided)
3. Shared secret authentication (fallback, only recommended for local testing or examples, not production)

In this example, we use the shared secret option.

## Group Communication Using the Python Bindings

Now that you know how to set up a SLIM application, we can see how to create a group where multiple participants can exchange messages. We start by showing how to create a group session using the Python bindings.

In this setting, one participant acts as moderator: it creates the group session and invites participants by sending invitation control messages. A detailed description of group sessions and the invitation process is available [here](https://github.com/agntcy/slim/blob/slim-v1.0.0/data-plane/python/bindings/SESSION.md).

### Creating the Group Session and Inviting Members

The creator of the group session invites other members to join the group. The
session will be identified by a unique session ID, and the group communication
will take place over a specific channel name. The session creator is responsible
for managing the session lifecycle, including creating, updating, and
terminating the session as needed.

As each participant is provided with an identity, setting up MLS for end-to-end
encryption is straightforward: the session is created with the
`mls_enabled` flag set to `True`, which will enable the MLS protocol for the
session. This ensures that all messages exchanged within the session are
end-to-end encrypted, providing confidentiality and integrity for the group
communication.

```python
# Create & connect the local Slim instance (auth derived from args).
local_app = await create_local_app(
    local,
    slim,
    enable_opentelemetry=enable_opentelemetry,
    shared_secret=shared_secret,
    jwt=jwt,
    spire_trust_bundle=spire_trust_bundle,
    audience=audience,
    spire_socket_path=spire_socket_path,
    spire_target_spiffe_id=spire_target_spiffe_id,
    spire_jwt_audience=spire_jwt_audience,
)

# Parse the remote channel/topic if provided; else None triggers passive mode.
chat_channel = split_id(remote) if remote else None

# Track background tasks (receiver loop + optional keyboard loop).
tasks: list[asyncio.Task] = []

# Session sharing between tasks
session_ready = asyncio.Event()
shared_session_container = [None]  # Use list to make it mutable across functions

# Session object only exists immediately if we are moderator.
created_session = None
if chat_channel and invites:
    # We are the moderator; create the group session now.
    format_message_print(
        f"Creating new group session (moderator)... {split_id(local)}"
    )
    config = slim_bindings.SessionConfiguration.Group(
        max_retries=5,  # Max per-message resend attempts upon missing ack before reporting a delivery failure.
        timeout=datetime.timedelta(
            seconds=5
        ),  # Ack / delivery wait window; after this duration a retry is triggered (until max_retries).
        mls_enabled=enable_mls,  # Enable Messaging Layer Security for end-to-end encrypted & authenticated group communication.
    )

    created_session, handle = await local_app.create_session(
        chat_channel,  # Logical group channel (Name) all participants join; acts as group/topic identifier.
        config,  # session configuration
    )

    await handle

    # Invite each provided participant. Route is set before inviting to ensure
    # outbound control messages can reach them. For more info, see
    # https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/SESSION.md#invite-a-new-participant
    for invite in invites:
        invite_name = split_id(invite)
        await local_app.set_route(invite_name)
        handle = await created_session.invite(invite_name)
        await handle
        print(f"{local} -> add {invite_name} to the group")
```

This code comes from the
[group.py](https://github.com/agntcy/slim/blob/slim-v1.0.0/data-plane/python/bindings/examples/src/slim_bindings_examples/group.py)
example. The local application is created using the helper function shown earlier.
The channel name (the logical group topic) is produced via the
[split_id](https://github.com/agntcy/slim/blob/slim-v1.0.0/data-plane/python/bindings/examples/src/slim_bindings_examples/common.py#L63)
helper by parsing the `remote` parameter.

A new group session is created by calling `local_app.create_session(...)` with two parameters:
the channel name and a `slim_bindings.SessionConfiguration.Group` configuration object.
The `create_session` call returns a tuple containing the session object and a handle that must be awaited.
The key configuration parameters to setup the `SessionConfiguration` are:

- `max_retries`: Maximum number of retransmission attempts (upon missing ack) before
    notifying the application of delivery failure.
- `timeout`: Duration to wait for an acknowledgment; if the ack is not received in time, a retry is triggered. If
    omitted / None, the session is unreliable (no retry/ack flow).
- `mls_enabled`: Set to `True` to enable MLS for end-to-end encryption.

After the session creation, the moderator invites participants via `created_session.invite(invite_name)`.
Each `invite` call returns a handle that should be awaited to ensure the invitation completes.

### Implement Participants and Receive Messages

The group participants are implemented in a similar way, but they
do not create the session. They create the SLIM service instance and wait
for invites. Once they receive the invite, they can read and write on the shared channel.

```python
async def receive_loop(
    local_app, created_session, session_ready, shared_session_container
):
    """
    Receive messages for the bound session.

    Behavior:
      * If not moderator: wait for a new group session (listen_for_session()).
      * If moderator: reuse the created_session reference.
      * Loop forever until cancellation or an error occurs.
    """
    if created_session is None:
        print_formatted_text("Waiting for session...", style=custom_style)
        session = await local_app.listen_for_session()
    else:
        session = created_session

    # Make session available to other tasks
    shared_session_container[0] = session
    session_ready.set()

    while True:
        try:
            # Await next inbound message from the group session.
            # The returned parameters are a message context and the raw payload bytes.
            # Check session.py for details on MessageContext contents.
            ctx, payload = await session.get_message()
            print_formatted_text(
                f"{ctx.source_name} > {payload.decode()}",
                style=custom_style,
            )
        except asyncio.CancelledError:
            # Graceful shutdown path (ctrl-c or program exit).
            break
        except Exception as e:
            # Non-cancellation error; surface and exit the loop.
            print_formatted_text(f"-> Error receiving message: {e}")
            break
```

Each non-moderator participant listens for an incoming session using
`local_app.listen_for_session()`. This returns a session object containing metadata
such as session ID, type, source name, and destination name.
The moderator already holds this information and therefore reuses the existing
`created_session` (see `session = created_session`).

Participants (including the moderator) then call `ctx, payload = await session.get_message()` to receive
messages. `payload` contains the raw message bytes and `ctx` is a
[MessageContext](https://github.com/agntcy/slim/blob/slim-v1.0.0/data-plane/python/bindings/slim_bindings/session.py)
with source, destination, message type, and metadata.

### Publish Messages to the Session

All participants can publish messages on the shared channel:

```python
async def keyboard_loop(session_ready, shared_session_container, local_app):
    """
    Interactive loop allowing participants to publish messages.

    Typing 'exit' or 'quit' (case-insensitive) terminates the loop.
    Each line is published to the group channel as UTF-8 bytes.
    """
    try:
        # 1. Initialize an async session
        prompt_session = PromptSession(style=custom_style)

        # Wait for the session to be established
        await session_ready.wait()

        print_formatted_text(
            f"Welcome to the group {shared_session_container[0].dst}!\nSend a message to the group, or type 'exit' or 'quit' to quit.",
            style=custom_style,
        )

        while True:
            # Run blocking input() in a worker thread so we do not block the event loop.
            user_input = await prompt_session.prompt_async(
                f"{shared_session_container[0].src} > "
            )

            if user_input.lower() in ("exit", "quit"):
                # Also terminate the receive loop.
                handle = await local_app.delete_session(shared_session_container[0])
                await handle
                break

            # Send message to the channel_name specified when creating the session.
            # As the session is group, all participants will receive it.
            await shared_session_container[0].publish(user_input.encode())
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        pass
    except asyncio.CancelledError:
        # Handle task cancellation gracefully
        pass
    except Exception as e:
        print_formatted_text(f"-> Error sending message: {e}")
```

Messages are sent using `shared_session_container[0].publish(user_input.encode())`.
Only the payload is provided and there is no explicit destination, because the
group channel was fixed at session creation and delivery fans out to all
participants.

When a user types 'exit' or 'quit', the application calls `local_app.delete_session()`
which returns a handle that must be awaited to ensure proper session cleanup before
terminating the loop. When the moderator closes the session,
all other participants are automatically notified, causing their receive loops to terminate
and their sessions to close gracefully. If the session closure is initiated by a participant,
only its local session is closed.

### Run the Group Communication Example

Now we will show how to run a new group session and
how to enable group communication on top of SLIM. The full code can be found in
[group.py](https://github.com/agntcy/slim/blob/slim-v1.0.0/data-plane/python/bindings/examples/src/slim_bindings_examples/group.py)
in the SLIM repo. To run the example, follow the steps listed here:

#### Run SLIM

As all members of the group are communicating via a SLIM network, we can set
up a SLIM instance representing the SLIM network. We use the pre-built
docker image for this purpose.

First execute this command to create the SLIM configuration file. Details about
the [configuration](https://github.com/agntcy/slim/tree/slim-v1.0.0/data-plane/config)
can be found in the SLIM repo.

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
    dataplane:
      servers:
        - endpoint: "0.0.0.0:46357"
          tls:
            insecure: true

      clients: []
    controller:
      servers: []
EOF
```

This configuration starts a SLIM instance with a server listening on port
46357, without TLS encryption for simplicity. Messages are still encrypted
using the MLS protocol, but the connections between SLIM nodes do not use TLS.
In a production environment, it is recommended to always use TLS and configure
proper authentication and authorization mechanisms.

You can run the SLIM instance using Docker:

```bash
docker run -it \
    -v ./config.yaml:/config.yaml -p 46357:46357 \
    ghcr.io/agntcy/slim:1.0.0 /slim --config /config.yaml
```

If everything goes fine, you should see an output like this one:

```bash
2025-10-06T08:22:54.529981Z  INFO main ThreadId(01) application_lifecycle: slim: Runtime started
2025-10-06T08:22:54.530116Z  INFO main ThreadId(01) application_lifecycle: slim: Starting service: slim/0
2025-10-06T08:22:54.530157Z  INFO main ThreadId(01) application_lifecycle: slim_service::service: starting service
2025-10-06T08:22:54.530193Z  INFO main ThreadId(01) application_lifecycle: slim_service::service: starting server 0.0.0.0:46357
...
```

#### Start the Participants

In this example, we use two participants: `agntcy/ns/client-1` and `agntcy/ns/client-2`.
Authentication uses a shared secret. In the SLIM repository, go to the folder
`slim/data-plane/python/bindings/examples` and run these commands in two different terminals:

```bash
uv run --package slim-bindings-examples group                               \
    --local agntcy/ns/client-1                                                  \
    --slim '{"endpoint": "http://localhost:46357", "tls": {"insecure": true}}'  \
    --shared-secret "very-long-shared-secret-value-0123456789abcdef"
```

```bash
uv run --package slim-bindings-examples group                               \
    --local agntcy/ns/client-2                                                  \
    --slim '{"endpoint": "http://localhost:46357", "tls": {"insecure": true}}'  \
    --shared-secret "very-long-shared-secret-value-0123456789abcdef"

```

This starts two participants authenticated with a shared secret.
The output of these commands should look like this:

```bash
Warning: Falling back to shared-secret authentication. Don't use this in production!
Agntcy/ns/client-1/456243414154990054        Created app
Agntcy/ns/client-1/456243414154990054        Connected to http://localhost:46357
Waiting for session...
```

#### Create the Group

Run the moderator application to create the session and invite the two
participants. In another terminal run:

```bash
uv run --package slim-bindings-examples group                               \
    --local agntcy/ns/moderator                                                 \
    --slim '{"endpoint": "http://localhost:46357", "tls": {"insecure": true}}'  \
    --shared-secret "very-long-shared-secret-value-0123456789abcdef"            \
    --remote agntcy/ns/chat                                                     \
    --invites agntcy/ns/client-1                                                \
    --invites agntcy/ns/client-2                                                \
    --enable-mls
```

The result should look like:

```bash
Agntcy/ns/moderator/16858445264489265394     Created app
Agntcy/ns/moderator/16858445264489265394     Connected to http://localhost:46357
Creating new group session (moderator)... 169ca82eb17d6bc2/eef9769a4c6990d1/fc9bbc406957794b/ffffffffffffffff (agntcy/ns/moderator/ffffffffffffffff)
agntcy/ns/moderator -> add 169ca82eb17d6bc2/eef9769a4c6990d1/58ec40d7c837e0b9/ffffffffffffffff (agntcy/ns/client-1/ffffffffffffffff) to the group
agntcy/ns/moderator -> add 169ca82eb17d6bc2/eef9769a4c6990d1/b521a3788f1267a8/ffffffffffffffff (agntcy/ns/client-2/ffffffffffffffff) to the group
Welcome to the group 169ca82eb17d6bc2/eef9769a4c6990d1/4abb367236cabc2a/ffffffffffffffff (agntcy/ns/chat/ffffffffffffffff)!
Send a message to the group, or type 'exit' or 'quit' to quit.
169ca82eb17d6bc2/eef9769a4c6990d1/fc9bbc406957794b/e9f53aa5ef3fb8f2 (agntcy/ns/moderator/e9f53aa5ef3fb8f2) >
```

Now `client-1` and `client-2` are invited to the group, so on both of their terminals you should
be able to see a welcome message such as:

```bash
Welcome to the group 169ca82eb17d6bc2/eef9769a4c6990d1/4abb367236cabc2a/ffffffffffffffff (agntcy/ns/chat/ffffffffffffffff)!
Send a message to the group, or type 'exit' or 'quit' to quit.
169ca82eb17d6bc2/eef9769a4c6990d1/58ec40d7c837e0b9/6a34b65ebc955471 (agntcy/ns/client-1/6a34b65ebc955471) >
```

At this point, you can write messages from any terminal and they will be received by all other group participants.

Writing 'exit' or 'quit' from the moderator will close all the applications.

## Group Communication Using the SLIM Controller

Previously, we saw how to run group communication using the Python bindings with an in-application moderator.
This participant creates the group session and invites all other participants.
In this section, we describe how to create and orchestrate a group using the SLIM Controller, and we show how all
these functions can be delegated to the controller. We reuse the same group example code in this section as well.

Identity handling is unchanged between the two approaches; refer back to [SLIM Identity](#configure-client-identity-and-implement-the-slim-app). Below are the steps to run the controller-managed version.

### Application Differences

With the controller, you do not need to set up a moderator in your application. All participants can be run as we did for `client-1` and `client-2` in the previous examples. In code, this means you can avoid creating a new group session (using `local_app.create_session`) and the invitation loop. You only need to implement the `receive_loop` where the application waits for new sessions. This greatly simplifies your code.

### Run the Group Communication Example

Now we will show how to set up a group using the SLIM Controller. The reference code for the
application is still [group.py](https://github.com/agntcy/slim/blob/slim-v1.0.0/data-plane/python/bindings/examples/src/slim_bindings_examples/group.py). To run this example, follow the steps listed here.

#### Run the SLIM Controller

First, start the SLIM Controller. Full details are in the [Controller](./slim-controller.md) documentation; here we reproduce the minimal setup. Create a configuration file:

```bash
cat << EOF > ./config-controller.yaml
northbound:
  httpHost: 0.0.0.0
  httpPort: 50051
  logging:
    level: INFO

southbound:
  httpHost: 0.0.0.0
  httpPort: 50052
  logging:
    level: INFO

reconciler:
  maxRequeues: 15
  maxNumOfParallelReconciles: 1000

logging:
  level: INFO

database:
  filePath: /db/controlplane.db
EOF
```

This config defines two APIs exposed by the controller:

- Northbound API: used by an operator (e.g. via slimctl) to configure channels and participants, as well as the SLIM network.
- Southbound API: used by SLIM nodes to synchronize with the controller.

Start the controller with Docker:

```bash
docker run -it \
    -v ./config-controller.yaml:/config.yaml -v .:/db -p 50051:50051 -p 50052:50052 \
    ghcr.io/agntcy/slim/control-plane:1.0.0 --config /config.yaml
```

If everything goes fine, you should see an output like this:

```bash
2025-10-06T08:06:06Z INF Starting route reconcilers
2025-10-06T08:06:06Z INF Starting Route Reconciler thread_name=reconciler-1
2025-10-06T08:06:06Z INF Starting Route Reconciler thread_name=reconciler-0
2025-10-06T08:06:06Z INF Starting Route Reconciler thread_name=reconciler-2
2025-10-06T08:06:06Z INF Southbound API Service is Listening on [::]:50052
2025-10-06T08:06:06Z INF Northbound API Service is listening on [::]:50051
```

#### Run the SLIM Node

With the controller running, start a SLIM node configured to talk to it over the Southbound API. This node config includes two additional settings compared to the file from the previous section:

- A controller client used to connect to the Southbound API running on port 50052.
- A shared secret token provider that will be used by the SLIM node to send messages over the SLIM network. As with the normal application, you can use a shared secret or a proper JWT.

Create the `config-slim.yaml` for the node using the command below. We use the `host.docker.internal` endpoint to reach the controller from inside the Docker container via the host.

```bash
cat << EOF > ./config-slim.yaml
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
    dataplane:
      servers:
        - endpoint: "0.0.0.0:46357"
          tls:
            insecure: true

      clients: []
    controller:
      servers: []
      clients:
        - endpoint: "http://host.docker.internal:50052"
          tls:
            insecure: true
      token_provider:
        type: shared_secret
        data: "very-long-shared-secret-value-0123456789abcdef"
EOF
```

This starts a SLIM node that connects to the controller:

```bash
docker run -it \
    -v ./config-slim.yaml:/config.yaml -p 46357:46357 \
    ghcr.io/agntcy/slim:1.0.0 /slim --config /config.yaml
```

If everything goes fine, you should see an output like this one:

```bash
2025-10-06T08:22:54.529981Z  INFO main ThreadId(01) application_lifecycle: slim: Runtime started
2025-10-06T08:22:54.530116Z  INFO main ThreadId(01) application_lifecycle: slim: Starting service: slim/0
2025-10-06T08:22:54.530157Z  INFO main ThreadId(01) application_lifecycle: slim_service::service: starting service
2025-10-06T08:22:54.530193Z  INFO main ThreadId(01) application_lifecycle: slim_service::service: starting server 0.0.0.0:46357
...
```

On the Controller side, you can see that the new node registers with the controller. The
output should be similar to this:

```bash
2025-10-06T11:47:14+02:00 INF Registering node with ID: slim/0 svc=southbound
2025-10-06T11:47:14+02:00 INF Connection details: [endpoint: 127.0.0.1:46357] svc=southbound
2025-10-06T11:47:14+02:00 INF Create generic routes for node node_id=slim/0 service=RouteService
2025-10-06T11:47:14+02:00 INF Sending routes to registered node slim/0 node_id=slim/0
2025-10-06T11:47:14+02:00 INF Sending configuration command to registered node connections_count=0 message_id=8e9d311a-0012-4fb2-93dc-cda2cb0dd2ef node_id=slim/0 subscriptions_count=0 subscriptions_to_delete_count=0
2025-10-06T11:47:14+02:00 INF Sending routes completed successfully ack_messages=[] node_id=slim/0 original_message_id=8e9d311a-0012-4fb2-93dc-cda2cb0dd2ef
```

#### Run the Participants

Because the controller manages the group lifecycle, no participant needs to be designated as moderator in code. Every application instance just waits for a session invite. In three separate terminals, from the folder
`slim/data-plane/python/bindings/examples` run:

```bash
uv run --package slim-bindings-examples group                               \
    --local agntcy/ns/client-1                                                  \
    --slim '{"endpoint": "http://localhost:46357", "tls": {"insecure": true}}'  \
    --shared-secret "very-long-shared-secret-value-0123456789abcdef"
```

```bash
uv run --package slim-bindings-examples group                               \
    --local agntcy/ns/client-2                                                  \
    --slim '{"endpoint": "http://localhost:46357", "tls": {"insecure": true}}'  \
    --shared-secret "very-long-shared-secret-value-0123456789abcdef"
```

```bash
uv run --package slim-bindings-examples group                               \
    --local agntcy/ns/client-3                                                  \
    --slim '{"endpoint": "http://localhost:46357", "tls": {"insecure": true}}'  \
    --shared-secret "very-long-shared-secret-value-0123456789abcdef"
```

Each terminal should show output similar to:

```bash
Warning: Falling back to shared-secret authentication. Don't use this in production!
Agntcy/ns/client-1/9494657801285491688       Created app
Agntcy/ns/client-1/9494657801285491688       Connected to http://localhost:46357
Waiting for session...
```

At this point all applications are waiting for a new session.

#### Manage the Group with slimctl

Use `slimctl` (see [slim-controller](./slim-controller.md)) to send administrative commands to the controller.

First, you need to run `slimctl`. You can download it from the slim repo using this script:

```bash
#!/bin/bash
set -e

# This script automatically detects your OS and architecture,
# then downloads the appropriate slimctl binary.

# Detect OS and architecture
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

# Map architecture to the format used in release asset names
case "$ARCH" in
  x86_64)
    ARCH="amd64"
    ;;
  aarch64 | arm64)
    ARCH="arm64"
    ;;
  *)
    echo "Unsupported architecture: $ARCH" >&2
    exit 1
    ;;
esac

# Check for supported OS
if [ "$OS" != "linux" ] && [ "$OS" != "darwin" ]; then
  echo "Unsupported OS: $OS" >&2
  exit 1
fi

# Construct the download URL
VERSION="v1.0.0"
COMMIT_HASH="35c37ab"
ARCHIVE_NAME="slimctl_slimctl-${VERSION}-SNAPSHOT-${COMMIT_HASH}_${OS}_${ARCH}.tar.gz"
DOWNLOAD_URL="https://github.com/agntcy/slim/releases/download/slimctl-${VERSION}/${ARCHIVE_NAME}"

# Download and extract the binary
echo "Downloading slimctl for ${OS}-${ARCH}..."
curl -L "${DOWNLOAD_URL}" -o "${ARCHIVE_NAME}"
tar -xzf "${ARCHIVE_NAME}"
rm "${ARCHIVE_NAME}"

# Make it executable
chmod +x slimctl
```

To verify that `slimctl` was downloaded successfully, run the following command:

```bash
./slimctl version
```

##### Create the Group

Select any running participant to be the initial member of the group. This participant acts as the logical
moderator of the channel, similar to the Python bindings example. However, you don't
need to handle this explicitly in the code. Run the following command to create the channel:

```bash
./slimctl controller channel create moderators=agntcy/ns/client-1/9494657801285491688
```

The full name of the application can be taken from the output in the console. The value
`9494657801285491688` is the actual id of the `client-1` application returned by
SLIM. In your case, this value will be different.

Expected response from `slimctl`:

```bash
Received response: agntcy/ns/xyIGhc2igNGmkeBDlZ
```

The value `agntcy/ns/xyIGhc2igNGmkeBDlZ` is the channel (or group) identifier (name) that must be used in subsequent commands.

On the application side, `client-1` was added to the session, so you should see
something like this:

```bash
Welcome to the group 169ca82eb17d6bc2/eef9769a4c6990d1/e8ab33f6d6111780/ffffffffffffffff (agntcy/ns/xyIGhc2igNGmkeBDlZ/ffffffffffffffff)!
Send a message to the group, or type 'exit' or 'quit' to quit.
169ca82eb17d6bc2/eef9769a4c6990d1/58ec40d7c837e0b9/83c3ccf725835be8 (agntcy/ns/client-1/83c3ccf725835be8) >
```

##### Add Participants

Now that the new group is created, add the additional participants `client-2` and `client-3` using the following `slimctl` commands:

```bash
./slimctl controller participant add -c agntcy/ns/xyIGhc2igNGmkeBDlZ agntcy/ns/client-2
./slimctl controller participant add -c agntcy/ns/xyIGhc2igNGmkeBDlZ agntcy/ns/client-3
```

The expected `slimctl` output is:

```bash
Adding participant to channel ID agntcy/ns/xyIGhc2igNGmkeBDlZ: agntcy/ns/client-2
Participant added successfully to channel ID agntcy/ns/xyIGhc2igNGmkeBDlZ: agntcy/ns/client-2
```

Now all the participants are part of the same group, and so each client log should show that the join was successful:

```bash
Welcome to the group 169ca82eb17d6bc2/eef9769a4c6990d1/e8ab33f6d6111780/ffffffffffffffff (agntcy/ns/xyIGhc2igNGmkeBDlZ/ffffffffffffffff)!
Send a message to the group, or type 'exit' or 'quit' to quit.
169ca82eb17d6bc2/eef9769a4c6990d1/b521a3788f1267a8/e4011f7be5222a24 (agntcy/ns/client-2/e4011f7be5222a24) >
```

At this point, every member can send messages, and they will be received by all the other participants.

##### Remove a Participant

To remove one of the participants from the channel, run the following command:

```bash
./slimctl c participant delete -c agntcy/ns/xyIGhc2igNGmkeBDlZ agntcy/ns/client-3
```

The `slimctl` expected output is this:

```bash
Deleting participant from channel ID agntcy/ns/xyIGhc2igNGmkeBDlZ: agntcy/ns/client-3
Participant deleted successfully from channel ID agntcy/ns/xyIGhc2igNGmkeBDlZ: agntcy/ns/client-3
```

The application on `client-3` exits because the session related to the group was closed, which breaks the
receive loop in the Python code. Notice that this command does not work
for `client-1`, which was added as the first participant. In fact, removing `client-1` is
equivalent to deleting the channel itself.

##### Delete channel

To delete the channel, run the following command:

```bash
./slimctl controller channel delete agntcy/ns/xyIGhc2igNGmkeBDlZ
```

The `slimctl` output is this:

```bash
Channel deleted successfully with ID: agntcy/ns/xyIGhc2igNGmkeBDlZ
```

All applications connected to the group stop as their receive loops terminate.
