# Multi-Agent Application Toolkit

The Multi-Agent Application Toolkit is a comprehensive suite of agents designed to tackle the prevalent challenges encountered in developing applications that require effective coordination among agents originating from diverse sources, APIs, and humans.

In the following we list and describes the agents that compose this toolkit.

## I/O Mapper Agent

In multi-agent applications, ensuring seamless communication between two agents requires that the output of the first agent is compatible with the input of the second agent. This compatibility must be achieved across three distinct levels:
	1.	Transport Level: Both agents must utilize the same transport protocol to exchange data.
	2.	Format Level: Both agents should convey information using the same format, such as identical JSON data structures, or in case of natural language, same semantic structure.
	3.	Semantic Level: Both agents must "discuss the same subject", meaning the information expected by the second agent should be included in the output of the first agent.

Discrepancies at any of these levels can hinder effective communication between agents.

Assuming semantic compatibility among agents, where the first agent's output inherently contains the necessary information for the second agent, the I/O Mapper Agent is designed to address compatibility at the format and semantic levels. Implemented as an agent itself, it leverages a large language model (LLM) to ensure that the output from one agent is transformed to be compatible with the input of another. This transformation can encompass various processes, such as:
	•	JSON Structure Transcoding: Re-mapping a JSON dictionary into another format.
	•	Text Summarization: Condensing text or removing extraneous information.
	•	Text Translation: Converting text from one language to another.
	•	Text Manipulation: Reformulating parts of one text into another form.
	•	A combination of the above


The I/O Mapper Agent operates using schema definitions of input and output as specified by the Agent Connect Protocol, which should include natural language descriptions of data structures and, preferably, numerous examples to facilitate accurate LLM inference.

## API Bridge Agent

In the realm of agentic applications, seamless connectivity to APIs is a fundamental requirement. The process of interfacing with an API should be as straightforward as engaging with a remote agent. This is where the API Bridge Agent comes into play. Its primary function is to ensure that APIs can be accessed and utilized through the Agent Connect Protocol (ACP), akin to how agents are made accessible through ACP by the agent workflow server.

The API Bridge Agent is built as an API gateway plugin, which can be easily configured using any OpenAPI specification. Its core capabilities include:
* Transforming natural language requests received via ACP into REST API calls.
* Converting API responses back into natural language to be communicated through ACP.

Additionally, the API Bridge Agent offers advanced features for automatically selecting the most appropriate API from a set of available options in response to a given natural language request.

Moreover, the API Bridge Agent is designed to support a wide array of pre-configured API services, providing extensive "out-of-the-box" functionality.


## Semantic Router Agent

When defining a multi-agent application workflow, it is often needed to make decisions based on the output of invoked agents. 

In a graph-based agentic application (e.g., Langgraph), this corresponds to decide which node in the graph to execute based on the current state of the graph.  

While some of these decisions can be trivially implemented by a simple if condition, and while others can be so complex to require a dedicated agent to be processed, there is a large set of common decisions that are based on semantic similarity.  

This is where the Semantic Router Agent comes in. The semantic router agent is a component, modelled as a node in the graph, that takes an input in the form of natural language and decides where to go next.  Here next means following an edge in the graph that is associated to the semantically closest reference natural language text.  In other words: the semantic router agent chooses the next node based on a semantic routing table.  

**An example**:


> An assistant agent receives a prompt from a user during a conversation and based on the content of such prompt, it needs to perform different actions:
> - if the user is posting a new request, start the request handling flow;
> - if the user is satisfied with the conversation, terminate it and direct the flow to the auditing agent;
> - if the user is not satisfied, involve a human;
>
> The above can be implemented with a semantic router agent with three 
> possible routes, with each route  associated with a text describing what  is the expected content of the user prompt.

## Human in the Loop Agent

In many cases, agentic applications require human input.  

Involving the human requires two things:
* Interrupt a multi-application flow to wait for such human input. This is provided by the different frameworks in different ways, but  corresponds to pausing the application and resuming it when input is available.
* Engage with the human to collect the input. This can happen in many ways and each application will have its own preferences.

The Human in the Loop (HIL) Agent is an agent that implements most common methods to engage with humans. 

Few examples below:
- Webhook: the agent calls a provided webhook to request for input and receive it through OpenAPI/REST.
- Email engagement: the agent sends an email and offers a web interface to provide input.
- Webex/slack/… engagement: the agent uses a webex/slack/… channel to request input.
- etc.