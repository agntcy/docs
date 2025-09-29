# SLIM Group Communication Tutorial

This tutorial shows how to set up secure group communication using
SLIM. The group is created by defining a multicast session and inviting
participants. Messages are sent to a shared channel where every member can read
and write. All messages are end-to-end encrypted using the
[MLS protocol](https://datatracker.ietf.org/doc/html/rfc9420). This tutorial is
based on the
[multicast.py](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/examples/src/slim_bindings_examples/multicast.py)
example in the SLIM repo. A companion
[README](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/examples/src/slim_bindings_examples/README_multicast.md)
explains the example step by step.

## Key Features

- **Name-based Addressing**: In SLIM, all endpoints (channels and clients) have
  a name, and messages use a name-based addressing scheme for content routing.
- **Session Management**: Allows for the creation and management of sessions.
- **Broadcast Messaging**: Facilitates broadcast messaging to multiple
  subscribers.
- **End-to-End Encryption**: Ensures secure communication using the [MLS
  protocol](https://datatracker.ietf.org/doc/html/rfc9420).


## Configure Client Identity and Implement the SLIM App

Each member of the group runs a local SLIM app instance to
communicate with the SLIM network. Each member also has a unique identity used
for authentication and by the MLS protocol.

### Identity

Each member must have a unique identity. This is required to
set up end-to-end encryption using the MLS protocol. The identity can be a JWT
or a shared secret. For simplicity in this example we use a shared secret. A 
[tutorial](https://github.com/agntcy/slim/tree/main/data-plane/python/bindings/examples#running-in-kubernetes-spire--jwt)
on generating a JWT token using SPIRE and using it with SLIM is available in the
SLIM repo.

The python objects managing the identity are called `PyIdentityProvider` and
`PyIdentityVerifier`. The `PyIdentityProvider` is responsible for providing the
identity, while the `PyIdentityVerifier` is responsible for verifying the
identity. 

```python
def shared_secret_identity(identity: str, secret: str):
    """
    Create a provider & verifier pair for shared-secret (symmetric) authentication.

    Args:
        identity: Logical identity string (often same as PyName string form).
        secret: Shared secret used to sign / verify tokens (not for production).

    Returns:
        (provider, verifier): Tuple of PyIdentityProvider & PyIdentityVerifier.
    """
    provider = slim_bindings.PyIdentityProvider.SharedSecret(  # type: ignore
        identity=identity, shared_secret=secret
    )
    verifier = slim_bindings.PyIdentityVerifier.SharedSecret(  # type: ignore
        identity=identity, shared_secret=secret
    )
    return provider, verifier
```

This is a helper function defined in
[common.py](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/examples/src/slim_bindings_examples/common.py#L85) 
that can be used to create a `PyIdentityProvider` and `PyIdentityVerifier` from two input strings.

### SLIM App

The provider and verifier are used to create a local SLIM app that can
exchange messages with other apps via the SLIM network. To create
the SLIM app we leverage another helper function defined in
[common.py](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/examples/src/slim_bindings_examples/common.py#L289)

```python
async def create_local_app(
    local: str,
    slim: dict,
    remote: str | None = None,
    enable_opentelemetry: bool = False,
    shared_secret: str = "secret",
    jwt: str | None = None,
    spire_trust_bundle: str | None = None,
    audience: list[str] | None = None,
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
    else:
        print(
            "Warning: Falling back to shared-secret authentication. Don't use this in production!"
        )
        # Fall back to shared secret (dev-friendly default).
        provider, verifier = shared_secret_identity(
            identity=local,
            secret=shared_secret,
        )

    # Convert local identifier to a strongly typed PyName.
    local_name = split_id(local)

    # Instantiate Slim (async constructor prepares underlying PyService).
    local_app = await slim_bindings.Slim.new(local_name, provider, verifier)

    # Provide feedback to user (instance numeric id).
    format_message_print(f"{local_app.id_str}", "Created app")

    # Establish outbound connection using provided parameters.
    _ = await local_app.connect(slim)

    # Confirm endpoint connectivity.
    format_message_print(f"{local_app.id_str}", f"Connected to {slim['endpoint']}")

    return local_app
```

This function takes several parameters as input:

- `local` (str): The SLIM name of the local application in the form
    `org/ns/service` (required).
- `slim` (dict): Configuration to connect to the remote SLIM node. Example:
    ```python
    {
            "endpoint": "http://127.0.0.1:46357",
            "tls": {"insecure": True},
    }
    ```
    (required)
- `enable_opentelemetry` (bool, default: `False`): Enable OpenTelemetry
    tracing. If `True`, traces are sent to `http://localhost:4317` by default.
- `shared_secret` (str | None, default: `None`): Shared secret for identity and
    authentication. Required if JWT, bundle and audience are not provided.
- `jwt` (str | None, default: `None`): JWT token for identity. Used with
    `spire_trust_bundle` and `audience` for JWT-based authentication.
- `spire_trust_bundle` (str | None, default: `None`): JWT trust bundle (CA certificates or
    JWKS). It is expected in JSON format such as
    ```json
    {
        "trust-domain-1.org": "base-64-encoded-jwks",
        "trust-domain-2.org": "base-64-encoded-jwks",
        ...
    }
    ```
- `audience` (list[str] | None, default: `None`): List of allowed audiences for
    JWT authentication.

If `jwt`, `spire_trust_bundle`, and `audience` are not provided, `shared_secret` must be set (only
recommended for local testing or examples, not production). In this example we
use the shared secret option, but the same function supports all authentication flows.

## Create the Multicast Session (Group Communication)

One application acts as moderator: it creates the multicast session and invites
participants by sending invitation control messages. A detailed description of
multicast sessions and the invitation process is available
[here](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/SESSION.md).

### Creating the Multicast Session and Inviting Members

The creator of the multicast session invites other members to join the group. The
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
    )

    # Parse the remote channel/topic if provided; else None triggers passive mode.
    chat_channel = split_id(remote) if remote else None

    # Track background tasks (receiver loop + optional keyboard loop).
    tasks: list[asyncio.Task] = []

    # Session object only exists immediately if we are moderator.
    created_session = None
    if chat_channel and invites:
        # We are the moderator; create the multicast session now.
        format_message_print(
            f"Creating new multicast session (moderator)... {split_id(local)}"
        )
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

        # Small delay so underlying routing / session creation stabilizes.
        await asyncio.sleep(1)

        # Invite each provided participant. Route is set before inviting to ensure
        # outbound control messages can reach them. For more info see
        # https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/SESSION.md#invite-a-new-participant
        for invite in invites:
            invite_name = split_id(invite)
            await local_app.set_route(invite_name)
            await created_session.invite(invite_name)
            print(f"{local} -> add {invite_name} to the group")
```

This code comes from the
[multicast.py](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/examples/src/slim_bindings_examples/multicast.py)
example. The local application is created using the helper function shown earlier.
The channel name (the logical multicast topic) is produced via the
[split_id](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/examples/src/slim_bindings_examples/common.py#L63)
helper by parsing the `remote` parameter. A new multicast session is then created
using `local_app.create_session(...)` with a
`slim_bindings.PySessionConfiguration.Multicast` configuration. The key parameters are:

- `channel_name`: Logical channel/topic used to exchange messages among participants.
- `max_retries`: Maximum number of retransmission attempts (upon missing ack) before
    notifying the application of delivery failure.
- `timeout`: Duration to wait for an acknowledgment; if the ack is not received in time a retry is triggered. If
    omitted / None, the session is unreliable (no retry/ack flow).
- `mls_enabled`: Set to `True` to enable MLS for end-to-end encryption.

After the session creation, the moderator invites participants via `created_session.invite`.
Before sending each invitation it must call `local_app.set_route(invite_name)` so
SLIM knows how to deliver the control messages.

### Implement Participants and Receive Messages

The group participants will be implemented in a similar way, but they
will not create the session. They will create the SLIM service instance and wait
for invites. Once they receive the invite, they can read and write on the shared channel.

```python
    async def receive_loop():
        """
        Receive messages for the bound session.

        Behavior:
          * If not moderator: wait for a new multicast session (listen_for_session()).
          * If moderator: reuse the created_session reference.
          * Loop forever until cancellation or an error occurs.
        """
        if created_session is None:
            format_message_print(local, "-> Waiting for session...")
            session = await local_app.listen_for_session()
        else:
            session = created_session

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

Each non-moderator participant listens for an incoming session using
`local_app.listen_for_session()`. This returns a
[PySession](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/slim_bindings/session.py)
object containing metadata such as session ID, type, source name, and destination name.
The moderator already holds this information and therefore reuses the existing
`created_session` (see `session = created_session`).

Participants then call `ctx, payload = await session.get_message()` to receive
messages. `payload` contains the raw message bytes and `ctx` is a
[PyMessageContext](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/slim_bindings/_slim_bindings.pyi#L22)
with source, destination, message type, and metadata.

### Publish Messages to the Session

All participants can publish messages on the shared channel

```python
    while True:
        # Run blocking input() in a worker thread so we do not block the event loop.
        user_input = await asyncio.to_thread(input, "\033[1mmessage>\033[0m ")
        if user_input.strip().lower() in ("exit", "quit"):
            break
        try:
            # Send message to the channel_name specified when creating the session.
            # As the session is multicast, all participants will receive it.
            # calling publish_with_destination on a multicast session will raise an error.
            await created_session.publish(user_input.encode())
        except Exception as e:
            format_message_print(local, f"-> Error sending message: {e}")
```
Messages are sent using `created_session.publish(user_input.encode())`.
Only the payload is provided and there is no explicit destination, because the
multicast channel was fixed at session creation and delivery fan-outs to all
participants.

In the
[multicast.py](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/examples/src/slim_bindings_examples/multicast.py)
example only the moderator sends messages. In practice any participant can call
`publish()`.

## How to Run the Example

In this toturial we presented step by step how to create a new multicast session and 
how to enable group communication on top of SLIM. The full code can be found in 
[multicast.py](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/examples/src/slim_bindings_examples/multicast.py)
in the SLIM repo. To run the example, follow the step listed here.

### Run SLIM
As all members of the group will be communicating via a SLIM network, we can set
up a SLIM instance representing the SLIM network. We will use the pre-built
docker image for this purpose.

First execute this command to create the SLIM configuration file. Details about
the [configuration](https://github.com/agntcy/slim/tree/main/data-plane/config) 
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

This configuration will start a SLIM instance with a server listening on port
46357, without TLS encryption for simplicity. Messages are still encrypted
using the MLS protocol, but the connections between SLIM nodes do not use TLS.
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

Another way to run SLIM is to use the
[Taskfile](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/Taskfile.yaml)
available in the Python bindings example. From `data-plane/python/bindings/` run:

```bash
task python:example:server
```

The outcome of this command will be the same.

### Start the Participants
In this example we use two participants: `agntcy/ns/client-1` and `agntcy/ns/client-2`.
Authentication uses a shared secret. From the same folder run these commands in
two different terminals:

```bash
uv run --package slim-bindings-examples multicast                               \
    --local agntcy/ns/client-1                                                  \
    --slim '{"endpoint": "http://localhost:46357", "tls": {"insecure": true}}'  \
    --shared-secret "secret"
```
```bash
uv run --package slim-bindings-examples multicast                               \
    --local agntcy/ns/client-2                                                  \
    --slim '{"endpoint": "http://localhost:46357", "tls": {"insecure": true}}'  \
    --shared-secret "secret"

```

Or use the commands in the Taskfile:

```bash
task python:example:multicast:client-1
```
```bash
task python:example:multicast:client-2
```

The outcome of these commands should look like:

```bash
$ task python:example:multicast:client-1
Uninstalled 1 package in 0.66ms
Installed 1 package in 1ms
Warning: Falling back to shared-secret authentication. Don't use this in production!
Agntcy/ns/client-1/6642107279451824449       Created app
Agntcy/ns/client-1/6642107279451824449       Connected to http://localhost:46357
Agntcy/ns/client-1                           -> Waiting for session...
```

### Create the Group

Run the moderator application to create the session and invite the two
participants. In another terminal run:

```bash
uv run --package slim-bindings-examples multicast                             \
    --local agntcy/ns/moderator                                                 \
    --slim '{"endpoint": "http://localhost:46357", "tls": {"insecure": true}}'  \
    --shared-secret "secret"                                                    \
    --remote agntcy/ns/chat                                                     \
    --invites agntcy/ns/client-1                                                \
    --invites agntcy/ns/client-2                                                \
    --enable-mls
```

Or use the command in the Taskfile:

```bash
task python:example:multicast:moderator
```

The result should look like:

```bash
$ task python:example:multicast:moderator
Warning: Falling back to shared-secret authentication. Don't use this in production!
Agntcy/ns/moderator/7425710098087306743      Created app
Agntcy/ns/moderator/7425710098087306743      Connected to http://localhost:46357
Creating new multicast session (moderator)... 169ca82eb17d6bc2/eef9769a4c6990d1/fc9bbc406957794b/ffffffffffffffff (agntcy/ns/moderator/ffffffffffffffff)
agntcy/ns/moderator -> add 169ca82eb17d6bc2/eef9769a4c6990d1/58ec40d7c837e0b9/ffffffffffffffff (agntcy/ns/client-1/ffffffffffffffff) to the group
agntcy/ns/moderator -> add 169ca82eb17d6bc2/eef9769a4c6990d1/b521a3788f1267a8/ffffffffffffffff (agntcy/ns/client-2/ffffffffffffffff) to the group
message>
```

### Send Messages

Now you can write a message from the moderator terminal:

```bash
message> hello
```

The message will be received by the two other participants:
```
Agntcy/ns/client-1                           -> Waiting for session...
Agntcy/ns/client-1                           -> Received message from 169ca82eb17d6bc2/eef9769a4c6990d1/fc9bbc406957794b/8658189cd0ac748 (agntcy/ns/moderator/8658189cd0ac748): hello
```


## Additional Example: Point-to-Point Communication

The SLIM repository also includes examples of point-to-point sessions. Using
the SLIM SDK for point‑to‑point sessions is similar to the multicast approach.
See
[point_to_point.py](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/examples/src/slim_bindings_examples/point_to_point.py)
and its accompanying
[README](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/examples/src/slim_bindings_examples/README_point_to_point.md).

Point-to-point communication is useful when you want SLIM as a transport for
protocols that are inherently unicast (e.g., MCP or A2A). You typically
communicate with a single server but still benefit from SLIM's routing,
security, and session management.

For a detailed guide on using MCP over SLIM see
[SLIM and MCP Integration](slim-mcp.md). For A2A over SLIM see
[SLIM A2A](./slim-a2a.md) integration.
