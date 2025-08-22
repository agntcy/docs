#SLIM in CoffeeAGNTCY

CoffeeAGNTCY uses [SLIM](../messaging/slim-core.md) as its default transport layer for all inter-agent communication. SLIM supports both **unicast** (1-to-1) and **broadcast** (1-to-many) messaging patterns, making it well-suited for CoffeeAGNTCY’s dynamic multi-agent workflows.  

The **AGNTCY App SDK** abstracts the underlying SLIM protocol behind a unified factory API. This allows developers to instantiate SLIM-based A2A (agent-to-agent) clients and servers without dealing directly with low-level transport details. Learn more about the App SDK [here](https://github.com/agntcy/app-sdk).

## Instantiating the Factory and SLIM Transport  

```python
factory = AgntcyFactory("name_of_agent", enable_tracing=True)
transport = factory.create_transport("SLIM", endpoint=SLIM_ENDPOINT)
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

- **Broadcast Message**  

Used when the supervisor agent sends the same request to multiple farm agents and waits for all (or a subset) of responses:  

```python
responses = await client.broadcast_message(request, expected_responses=3)
```

The `expected_responses` parameter defines how many replies the caller waits for before proceeding.  

## Example Implementations  

You can explore the CoffeeAGNTCY code to see these concepts in context:  

- **Client implementation** (message sending logic):  
  [coffee_agents/lungo/exchange/graph/tools.py](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/exchange/graph/tools.py)  

- **Server implementation** (message handling logic):  
  [coffee_agents/lungo/farms/brazil/farm_server.py](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/farms/brazil/farm_server.py)  





