# Semantic Router Agent (Coming soon)

When defining a multi-agent application workflow, it is often necessary to make decisions based on the output of invoked agents.

In a graph-based agentic applications (for example, LangGraph), this corresponds to decideing which node in the graph to execute based on the current state of the graph.

There is a large set of common decisions that are based on semantic similarity, even if some of these decisions can be trivially implemented by a simple `if` condition and others can be so complex that they require a dedicated agent to be processed.

This is where the Semantic Router Agent comes in. The Semantic Router Agent is a component, modelled as a node in the graph, that takes an input in the form of natural language and decides where to go next. Here next means following an edge in the graph that is associated to the semantically closest reference natural language text. In other words: the Semantic Router Agent chooses the next node based on a semantic routing table.

**Example**:

> An assistant agent receives a prompt from a user during a conversation and based on the content, it needs to perform different actions:
> - If the user is posting a new request, start the request handling flow.
> - If the user is satisfied with the conversation, terminate it and direct the flow to the auditing agent.
> - If the user is not satisfied, involve a human.
>
> The above can be implemented with a semantic router agent with three possible routes, with each route associated with a text describing what is the expected content of the user prompt.
