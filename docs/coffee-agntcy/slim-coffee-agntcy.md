# SLIM v0.4.0 in CoffeeAGNTCY

CoffeeAGNTCY uses [SLIM](../messaging/slim-core.md) as its default transport layer for all inter-agent communication. SLIM supports request-reply, unicast (fire-and-forget), publisher/subscriber, and group communication (1-to-many) messaging patterns, making it well-suited for CoffeeAGNTCY's dynamic multi-agent workflows.

The **AGNTCY App SDK** abstracts the underlying SLIM protocol behind a unified factory API. This allows developers to instantiate SLIM-based A2A (agent-to-agent) clients and servers without dealing directly with low-level transport details. Learn more about the App SDK [here](https://github.com/agntcy/app-sdk).

Note: Publisher/subscriber support is available using **NATS transport**, which can be used instead of SLIM transport for Lungo Publisher/Subscriber pattern.

## Instantiating the Factory and SLIM Transport

```python
factory = AgntcyFactory("name_of_agent", enable_tracing=True)
transport = factory.create_transport("SLIM", endpoint=SLIM_ENDPOINT, name="default/default/graph")
```

Here:  
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

Used when the supervisor agent sends the same request to multiple farm agents and waits for all the responses:

```python
responses = await client.broadcast_message(request, broadcast_topic=BROADCAST_TOPIC, recipients=recipients)
```

Here the `broadcast_topic` is the topic to which the message is broadcasted and the `recipients` is the list of agents to which the message is sent.

- **Group Communication Pattern**
Used when multiple agents participate in a group chat session, where all agents can send messages and listen to communications from other agents in the group:

```python
responses = await client.broadcast_message(
        request,
        broadcast_topic=f"{uuid4()}",
        recipients=recipients,
        end_message="DELIVERED",
        group_chat=True,
        timeout=60,
      )
```

Here `broadcast_topic` is the topic to which the message is broadcast, `recipients` is the list of agents to which the message is sent, `end_message` is the message that is sent to all agents when the group chat is closed, `group_chat` is a boolean that indicates whether we want to send a message as a group chat or not, and `timeout` is the timeout for the group chat session.

## Example Implementations  

You can explore the CoffeeAGNTCY code to see these concepts in context:  

Publisher/Subscriber pattern:

- **Client implementation** (message sending logic):
  [coffee_agents/lungo/agents/supervisors/auction/graph/tools.py](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/agents/supervisors/auction/graph/tools.py)

- **Server implementation** (message handling logic):
  [coffee_agents/lungo/agents/farms/brazil/farm_server.py](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/agents/farms/brazil/farm_server.py)

Group Communication pattern:

- **Client implementation** (message sending logic):
  [coffee_agents/lungo/agents/supervisors/logistic/graph/tools.py](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/agents/supervisors/logistic/graph/tools.py)

- **Server implementation** (message handling logic):
  [coffee_agents/lungo/agents/logistics/accountant/server.py](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/agents/logistics/accountant/server.py)
