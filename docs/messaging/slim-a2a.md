# SLIM A2A

SLIM A2A is a native integration of A2A built on top of SLIM. It utilizes SLIMRPC (SLIM Remote Procedure Call) and the SLIMRPC compiler to compile A2A protobuf file and generate the necessary code to enable A2A functionality on SLIM.

## What is SLIMRPC and SLIMRCP compiler

SLIMRPC is a framework that enables Protocol Buffers (protobuf) Remote Procedure Calls (RPC) over SLIM. This is similar to gRPC, which uses HTTP/2 as its transport layer for protobuf-based RPC. More information can be found [here](./slim-rpc.md)

To compile a protobuf file and generate the clients and service stub you can use the [SLIMRPC compiler](./slim-slimrpc-compiler.md). This works in a similar way to the protoc compiler.

For SLIM A2A we compiled the [a2a.proto](https://github.com/a2aproject/A2A/blob/main/specification/grpc/a2a.proto) file using the SLIM RPC compiler. The generated code is in [a2a_pb2_slimrpc.py](https://github.com/agntcy/slim/blob/main/data-plane/python/integrations/slima2a/slima2a/types/a2a_pb2_slimrpc.py).

## How to use SLIMA2A

Using SLIMA2A is very similar to using the standard A2A implementation. As a reference example here we use the [travel planner agent](https://github.com/a2aproject/a2a-samples/tree/main/samples/python/agents/travel_planner_agent) available on the A2A samples repository. The version adapted to use SLIM A2A can be found in [travel_planner_agent](https://github.com/agntcy/slim/tree/main/data-plane/python/integrations/slima2a/examples/travel_planner_agent) folder. In the following section, we highlight and explain the key difference between the standard and SLIM A2A implementations.

### Travel Planner: Server

In this section we highlight the main differences between the SLIM A2A [server](https://github.com/agntcy/slim/blob/main/data-plane/python/integrations/slima2a/examples/travel_planner_agent/server.py) implementation with respect to the original implementation in the A2A repository.

1. Import the SLIMRPC package.
    ```python
    import slimrpc
    ```
2. Create the SLIMRPCHandler. Notice that the definitions for `AgentCard` and `DefaultRequestHandler` remain unchanged from the original A2A example.
    ```python
    agent_card = AgentCard(
        name="travel planner Agent",
        description="travel planner",
        url="http://localhost:10001/",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )
    request_handler = DefaultRequestHandler(
        agent_executor=TravelPlannerAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )
    servicer = SLIMRPCHandler(agent_card, request_handler)
    ```
3. Setup the `slimrpc.Server`. This is the only place where you need to setup few parameters that are specific to SLIM.

    ```python
    server = slimrpc.Server(
        local="agntcy/demo/travel_planner_agent",
        slim={
            "endpoint": "http://localhost:46357",
            "tls": {
                "insecure": True,
            },
        },
        shared_secret="secret",
    )
    ```

    Where:

    - `local`: Name of the local application.
    - `slim`: Dictionary specifying how to connect to the SLIM node.
    - `shared_secret`: Used to set up MLS (Message Layer Security).

    For more information about these settings, see the [SLIMRPC](./slim-rpc.md).

4. Register the Service.

    ```python
    add_A2AServiceServicer_to_server(
        servicer,
        server,
    )
    ```

Your A2A server is now ready to run on SLIM.

### Travel Planner: Client

These are the main differences between the [client](https://github.com/agntcy/slim/blob/main/data-plane/python/integrations/slima2a/examples/travel_planner_agent/client.py) using SLIM A2A and the standard one.

1. Create a channel. This requires a configuration that is similar to the server
    ```python
    def channel_factory(topic: str) -> slimrpc.Channel:
        channel = slimrpc.Channel(
            local="agntcy/demo/client",
            remote=topic,
            slim={
                "endpoint": "http://localhost:46357",
                "tls": {
                    "insecure": True,
                },
            },
            shared_secret="secret",
        )
        return channel
    ```
2. Add SLIM RPC in the supported transports.
    ```python
    client_config = ClientConfig(
        supported_transports=["JSONRPC", "slimrpc"],
        streaming=True,
        httpx_client=httpx_client,
        slimrpc_channel_factory=channel_factory,
    )
    client_factory = ClientFactory(client_config)
    client_factory.register("slimrpc", SLIMRPCTransport.create)
    agent_card = minimal_agent_card("agntcy/demo/travel_planner_agent", ["slimrpc"])
    client = client_factory.create(card=agent_card)
    ```
