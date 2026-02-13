# SLIM A2A

SLIM A2A is a native integration of A2A built on top of SLIM. It utilizes SLIMRPC (SLIM Remote Procedure Call) and the SLIMRPC compiler to compile A2A protobuf file and generate the necessary code to enable A2A functionality on SLIM.

## What is SLIMRPC and SLIMRPC compiler

SLIMRPC is a framework that enables Protocol Buffers (protobuf) Remote Procedure Calls (RPC) over SLIM. This is similar to gRPC, which uses HTTP/2 as its transport layer for protobuf-based RPC. More information can be found [here](./slim-rpc.md)

To compile a protobuf file and generate the clients and service stub you can use the [SLIMRPC compiler](./slim-slimrpc-compiler.md). This works in a similar way to the protoc compiler.

For SLIM A2A we compiled the [a2a.proto](https://github.com/a2aproject/A2A/blob/v0.3.0/specification/grpc/a2a.proto) file using the SLIMRPC compiler. The generated code is in [a2a_pb2_slimrpc.py](https://github.com/agntcy/slim-a2a-python/blob/main/slima2a/types/a2a_pb2_slimrpc.py).

## How to use SLIMA2A

Using SLIMA2A is very similar to using the standard A2A implementation. As a reference example here we use the [echo agent](https://github.com/agntcy/slim-a2a-python/tree/main/examples/echo_agent) available in the SLIM A2A Python repository. In the following sections, we highlight and explain the key differences between the standard and SLIM A2A implementations.

### Server Implementation

SLIMA2A provides two approaches for setting up an A2A server: a quick start method using helper functions, and an advanced method for more control.

#### Quick Start (Recommended)

The quick start approach uses the `setup_slim_client` helper function to simplify SLIM initialization:

```python
import asyncio
import slim_bindings
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from slima2a import setup_slim_client
from slima2a.handler import SRPCHandler
from slima2a.types.a2a_pb2_slimrpc import add_A2AServiceServicer_to_server

# Initialize and connect to SLIM (simplified helper)
service, local_app, local_name, conn_id = await setup_slim_client(
    namespace="agntcy",
    group="demo",
    name="echo_agent",
)

# Create request handler
agent_executor = MyAgentExecutor()
task_store = InMemoryTaskStore()
request_handler = DefaultRequestHandler(
    agent_executor=agent_executor,
    task_store=task_store,
)

# Create servicer
servicer = SRPCHandler(agent_card, request_handler)

# Create server
server = slim_bindings.Server.new_with_connection(local_app, local_name, conn_id)

add_A2AServiceServicer_to_server(servicer, server)

# Run server
await server.serve_async()
```

#### Advanced Setup (Manual Configuration)

??? note "Advanced Setup - Click to expand"

    For more control over the SLIM configuration, you can manually initialize all components:

    ```python
    import asyncio
    import slim_bindings
    from a2a.server.request_handlers import DefaultRequestHandler
    from a2a.server.tasks import InMemoryTaskStore
    from slima2a.handler import SRPCHandler
    from slima2a.types.a2a_pb2_slimrpc import add_A2AServiceServicer_to_server

    # Set the event loop for slim_bindings
    slim_bindings.slim_bindings.uniffi_set_event_loop(asyncio.get_running_loop())

    # Initialize slim_bindings service
    tracing_config = slim_bindings.new_tracing_config()
    runtime_config = slim_bindings.new_runtime_config()
    service_config = slim_bindings.new_service_config()
    tracing_config.log_level = "info"

    slim_bindings.initialize_with_configs(
        tracing_config=tracing_config,
        runtime_config=runtime_config,
        service_config=[service_config],
    )

    service = slim_bindings.get_global_service()

    # Create local name
    local_name = slim_bindings.Name("agntcy", "demo", "echo_agent")

    # Connect to SLIM
    client_config = slim_bindings.new_insecure_client_config("http://localhost:46357")
    conn_id = await service.connect_async(client_config)

    # Create app with shared secret
    local_app = service.create_app_with_secret(
        local_name, "secretsecretsecretsecretsecretsecret"
    )

    # Subscribe to local name
    await local_app.subscribe_async(local_name, conn_id)

    # Create request handler
    agent_executor = MyAgentExecutor()
    task_store = InMemoryTaskStore()
    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor,
        task_store=task_store,
    )

    # Create servicer
    servicer = SRPCHandler(agent_card, request_handler)

    # Create server
    server = slim_bindings.Server.new_with_connection(local_app, local_name, conn_id)

    add_A2AServiceServicer_to_server(servicer, server)

    # Run server
    await server.serve_async()
    ```

    Key differences from the standard A2A implementation:
    
    1. **SLIM Bindings Initialization**: Set up the event loop and initialize `slim_bindings` with tracing and runtime configurations.
    2. **SLIM Name Creation**: Create a `slim_bindings.Name` object with namespace, group, and name components.
    3. **Connection Setup**: Connect to the SLIM server and create an app with a shared secret for MLS (Message Layer Security).
    4. **Server Creation**: Use `slim_bindings.Server.new_with_connection()` instead of a standard HTTP server.
    5. **Service Registration**: Register the servicer using `add_A2AServiceServicer_to_server()` from the generated SLIMRPC code.

### Client Implementation

Similar to the server, SLIMA2A provides both quick start and advanced client setup options.

#### Quick Start (Recommended)

```python
import asyncio
import httpx
from a2a.client import ClientFactory, minimal_agent_card
from a2a.types import Message, Part, Role, TextPart
from slima2a import setup_slim_client
from slima2a.client_transport import ClientConfig, SRPCTransport, slimrpc_channel_factory

# Initialize and connect to SLIM (simplified helper)
service, slim_local_app, local_name, conn_id = await setup_slim_client(
    namespace="agntcy",
    group="demo",
    name="client",
)

# Create client config
httpx_client = httpx.AsyncClient()
client_config = ClientConfig(
    supported_transports=["JSONRPC", "slimrpc"],
    streaming=True,
    httpx_client=httpx_client,
    slimrpc_channel_factory=slimrpc_channel_factory(slim_local_app, conn_id),
)

# Create client factory and register transport
client_factory = ClientFactory(client_config)
client_factory.register("slimrpc", SRPCTransport.create)

# Create client with minimal agent card
agent_card = minimal_agent_card("agntcy/demo/echo_agent", ["slimrpc"])
client = client_factory.create(card=agent_card)

# Send message
request = Message(
    role=Role.user,
    message_id="request-id",
    parts=[Part(root=TextPart(text="Hello, world!"))],
)

async for event in client.send_message(request=request):
    if isinstance(event, Message):
        for part in event.parts:
            if isinstance(part.root, TextPart):
                print(part.root.text)
```

#### Advanced Setup (Manual Configuration)

??? note "Advanced Setup - Click to expand"

    ```python
    import asyncio
    import httpx
    import slim_bindings
    from a2a.client import ClientFactory, minimal_agent_card
    from a2a.types import Message, Part, Role, TextPart
    from slima2a.client_transport import ClientConfig, SRPCTransport, slimrpc_channel_factory

    # Set the event loop for slim_bindings
    slim_bindings.slim_bindings.uniffi_set_event_loop(asyncio.get_running_loop())

    # Initialize slim_bindings service
    tracing_config = slim_bindings.new_tracing_config()
    runtime_config = slim_bindings.new_runtime_config()
    service_config = slim_bindings.new_service_config()
    tracing_config.log_level = "info"

    slim_bindings.initialize_with_configs(
        tracing_config=tracing_config,
        runtime_config=runtime_config,
        service_config=[service_config],
    )

    service = slim_bindings.get_global_service()

    # Create local name
    local_name = slim_bindings.Name("agntcy", "demo", "client")

    # Connect to SLIM
    client_config_slim = slim_bindings.new_insecure_client_config("http://localhost:46357")
    conn_id = await service.connect_async(client_config_slim)

    # Create app with shared secret
    slim_local_app = service.create_app_with_secret(
        local_name, "secretsecretsecretsecretsecretsecret"
    )

    # Subscribe to local name
    await slim_local_app.subscribe_async(local_name, conn_id)

    # Create client config
    httpx_client = httpx.AsyncClient()
    client_config = ClientConfig(
        supported_transports=["JSONRPC", "slimrpc"],
        streaming=True,
        httpx_client=httpx_client,
        slimrpc_channel_factory=slimrpc_channel_factory(slim_local_app, conn_id),
    )

    # Create client factory and register transport
    client_factory = ClientFactory(client_config)
    client_factory.register("slimrpc", SRPCTransport.create)

    # Create client with minimal agent card
    agent_card = minimal_agent_card("agntcy/demo/echo_agent", ["slimrpc"])
    client = client_factory.create(card=agent_card)

    # Send message
    request = Message(
        role=Role.user,
        message_id="request-id",
        parts=[Part(root=TextPart(text="Hello, world!"))],
    )

    async for event in client.send_message(request=request):
        if isinstance(event, Message):
            for part in event.parts:
                if isinstance(part.root, TextPart):
                    print(part.root.text)
    ```

    Key differences from the standard A2A client:
    
    1. **Channel Factory**: Use `slimrpc_channel_factory` instead of manually creating channels, which handles the SLIM connection details.
    2. **Transport Registration**: Register the `SRPCTransport` as the "slimrpc" transport in the client factory.
    3. **Agent Card Configuration**: Specify "slimrpc" as the transport protocol in the agent card.
    4. **Supported Transports**: Add "slimrpc" to the list of supported transports alongside "JSONRPC".

### Helper Functions

The `slima2a` package provides convenient helper functions to simplify SLIM setup:

- **`setup_slim_client(namespace, group, name, slim_url="http://localhost:46357", secret="...", log_level="info")`** - Complete SLIM client setup in one call. Returns `(service, local_app, local_name, conn_id)`.
- **`initialize_slim_service(log_level="info")`** - Initialize SLIM service with default configuration.
- **`connect_and_subscribe(service, local_name, slim_url="http://localhost:46357", secret="...")`** - Connect to SLIM server and subscribe to a local name.
- **`slimrpc_channel_factory(local_app, conn_id)`** - Creates a channel factory function for use with A2A client configuration.

## Configuration Parameters

### SLIM Connection

- **`namespace`**: The namespace component of the SLIM name (e.g., "agntcy")
- **`group`**: The group component of the SLIM name (e.g., "demo")
- **`name`**: The name component of the SLIM name (e.g., "echo_agent")
- **`slim_url`**: The endpoint URL for the SLIM server (default: "http://localhost:46357")
- **`shared_secret`**: A secret string used for MLS (Message Layer Security). Must be at least 32 characters.

### Logging

Set the log level through `tracing_config.log_level` with values like "info", "debug", "warn", or "error".

## Running the Example

See the [echo agent example](https://github.com/agntcy/slim-a2a-python/tree/main/examples/echo_agent) in the SLIM A2A Python repository for a complete working implementation.
