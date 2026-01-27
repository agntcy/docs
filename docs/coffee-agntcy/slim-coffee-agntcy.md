# SLIM v0.6.0 in CoffeeAGNTCY

CoffeeAGNTCY works with both NATS and [SLIM](../slim/overview.md) transports and illustrates multiple messaging patterns including request-reply, unicast (fire-and-forget), publisher/subscriber, and group communication, making them well-suited for CoffeeAGNTCY's dynamic multi-agent workflows.

**Default Transport Usage:**

- **NATS**: Default for publisher/subscriber patterns.
- **SLIM**: Default for group communication patterns.

You can find the transport configuration [here](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/config/config.py#L9-L10).

The **AGNTCY App SDK** abstracts the underlying SLIM protocol behind a unified factory API. This allows developers to instantiate SLIM-based A2A (agent-to-agent) clients and servers without dealing directly with low-level transport details. Learn more about the App SDK [here](https://github.com/agntcy/app-sdk).

!!! note
    Publisher/subscriber support is available using **NATS transport**, which can be used instead of SLIM transport for Lungo Publisher/Subscriber pattern.

## Instantiating the Factory and SLIM Transport

```python
factory = AgntcyFactory("name_of_agent", enable_tracing=True)
transport = factory.create_transport("SLIM", endpoint=SLIM_ENDPOINT, name="default/default/graph")
```

Where:

- `AgntcyFactory` initializes the factory for the agent.
- `create_transport("SLIM", ...)` provisions a SLIM transport instance connected to the configured endpoint.

## Sending Messages

SLIM accommodates both targeted and broadcast messaging within the same API:

- **1-to-1 Message**

    Used when the supervisor agent needs to send a request to a single farm agent:

    ```python
    response = await client.send_message(request)
    ```

- **Publisher/Subscriber Pattern**

    Used when the auction supervisor sends the same request to multiple farm agents and waits for all the responses:

    ```python
    responses = await client.broadcast_message(
        request,
        broadcast_topic=BROADCAST_TOPIC,
        recipients=recipients
    )
    ```

    Where:

    - `broadcast_topic` is the topic to which the message is broadcasted.
    - `recipients` is the list of agents to which the message is sent.

  ### Streaming Publisher/Subscriber

    For real-time responses as farms reply, use the streaming variant:

    ```python
    response_stream = client.broadcast_message_streaming(
        request,
        broadcast_topic=BROADCAST_TOPIC,
        recipients=recipients
    )
    ```

    This returns a stream of data from the farms.

- **Group Communication Pattern**

    Used when multiple agents participate in a group chat session, where all agents can send messages and listen to communications from other agents in the group:

    ```python
    responses = await client.start_groupchat(
        init_message=request,
        group_channel=f"{uuid4()}",
        participants=recipients,
        end_message="DELIVERED",
        timeout=60,
    )
    ```

    Where:

    - `init_message` is the initial message to start the group chat.
    - `group_channel` is the unique channel ID for the group chat session.
    - `participants` is the list of agent topics participating in the group chat.
    - `end_message` is the message that signals the end of the group chat.
    - `timeout` is the timeout for the group chat session in seconds.

  ### Streaming Group Communication

    For real-time order state transitions as each agent processes the order:

    ```python
    response_stream = client.start_streaming_groupchat(
        init_message=request,
        group_channel=f"{uuid4()}",
        participants=recipients,
        end_message="DELIVERED",
        timeout=60,
    )
    ```

    This returns a stream of data as agents process the order.

## Example Implementations

You can explore the CoffeeAGNTCY code to see these concepts in context:

Publisher/Subscriber pattern:

- [**Client implementation** (message sending logic)](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/agents/supervisors/auction/graph/tools.py)

- [**Server implementation** (message handling logic)](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/agents/farms/brazil/farm_server.py)

Group Communication pattern:

- [**Client implementation** (message sending logic)](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/agents/supervisors/logistics/graph/tools.py)

- [**Server implementation** (message handling logic)](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/agents/logistics/accountant/server.py)
