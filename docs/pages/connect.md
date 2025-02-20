# Agent Connect Protocol 

## Introduction

Existing Multi-Agent Systems (MAS) provide convenient ways to build Multi-Agent applications that combine various agents and enable them to communicate with each other.

Such communication occurs within the MAS using internal mechanisms and APIs.

Building the Internet of Agents requires agents built by different parties, potentially for different MAS and potentially running in different locations to interact. 

While interaction between co-located agents implemented through the same MAS is trivial, it is harder in case the agents are not natively compatible or in case they run in different locations.

We propose a solution where all agents are able to communicate over the network using a standard protocol to interoperate. We call it the **Agent Connect Protocol**, we also interchangeably use the acronym **ACP** to refer to it.

This document describes the main requirements and design principles of ACP.

The current specification of ACP can be found [here](https://agntcy.github.io/acp-spec), ACP Software Development Kit can be found [here](https://agntcy.github.io/acp-sdk).

## ACP Requirements

Agent Connect Protocol needs to formally specify the network interactions needed to address the following:

* **Authentication**: Define how caller authenticates with an agent and what its permissions are.
* **Configuration**: Define how to configure a remote agent.
* **Invocation**: Define how to invoke a remote agent providing input for its execution.
* **Output retrieval and interrupt Handling**: Define how to retrieve the result of an agent invocation. Different interaction modes should be supported: synchronous, asynchronous, and streaming. This should include interrupt handling, i.e. how agents notify the caller about execution suspension to ask for additional input.
* **Capabilities and Schema definitions**: Retrieve details about the agent supported capabilities and the data structures definitions for configuration, input, and output.
* **Error definitions**: receive error notifications with meaningful error codes and explanations.


### Authentication and Authorization
Agents invoked remotely need to authenticate the caller and make sure they have the proper authorization to perform the invocation.

Authorization mechanisms are outside the scope of the ACP specification.

ACP does not enforce a single authentication scheme to be used by all agents. Instead, it defines a list of allowed authentication schemes and lets agents declare which one is adopted.

For the reason above, ACP must define an endpoint that does not require authentication and returns the specific authentication scheme that is supported by the agent.

<a id="configuration"></a>
### Configuration
Agents may support configuration. 

Configuration is meant to provide parameters needed by the agent to function and/or to flavor their behavior. 

Configurations are typically valid for multiple invocations. 

ACP needs to define an endpoint to provide agent configuration. 

This endpoint must be distinct by the invocation endpoint, in this case it must return an identifier of the configured instance of the agent that can be used in multiple subsequent invocations.

Invocation endpoint should also provide an option to specify the configuration. In this case the configuration is valid only for the specific invocation.

Format of the configuration data structure is specified through a schema, see [Schema Definitions](#schemas)

Configuration endpoint may return an error. See [Error Definitions](#errors)

<a id="invocation"></a>
### Invocation
ACP must define an invocation endpoint that triggers one execution of an agent or resume a previously interrupted execution of an agent.

Invocation endpoint must accept input as parameter. An input provides specific information and contexts for the agent to operate. Format of the input data structure is specified through a schema, see [Schema Definitions](#schemas).

Invocation endpoint must accept an optional configuration as parameter. When provided, this configuration is valid only for this invocation. In alternative, invocation endpoint must accept the identifier of a previously configured instance of an agent (See [Configuration](#configuration)).

Invocation endpoint must accept an optional callback as parameter. When provided, the output of the invocation is provided asynchronously through the provided callback (See [Output Retrieval and Interrupt Handling](#output)).

Invocation endpoint must accept an optional execution identifier as parameter. In this case, the agent is requested to resume a previously interrupted execution, identified by the execution identifier.

Invocation endpoint must return the output of the execution, in case it is provided synchronously.

Invocation endpoint must return an execution identifier, which is then used to receive asynchronous output and to resume an interrupted execution.

Invocation endpoint may return an error. See [Error Definitions](#errors)

<a id="output"></a>
### Output Retrieval
Once an agent is invoked, it can provide output as a result of its operations.

Output can be provided to the caller synchronously, i.e. as a response of the invocation endpoint, or asynchronously, i.e. through a callback, provided as input of the invocation endpoint.

Output can be provided when different conditions occur:
1. The agent has terminated its execution and provides the final result of the execution.
2. The agent has interrupted its execution because it needs additional input, e.g. approval, chat interaction etc.
3. The agent is still running but it provides partial results, i.e. streaming

Output must carry information about which condition occurred.

Format of the output data structure is specified through a schema, see [Schema Definitions](#schemas).

<a id="schemas"></a>
### Capabilities and Schema definitions

ACP does not mandate the format of the data structures used to carry information to and from an agent, but it allows agents to provide definitions of those formats through ACP.
ACP must define an endpoint that provides schema definitions for configuration, input, and output.

Different agents may implement different parts of the protocol, for example: an agent may support streaming, while another may only support full responses; an agent may support threads while another may not.

ACP must define and endpoint that provides details about the specific capabilities that the agent supports.

Schemas, agent capabilities and other essential information that describe an agent are also needed in what we call the [Agent Manifest](manifest.md). For this reason, ACP exposes an endpoint that serves the Agent Manifest. 

<a id="errors"></a>
### Error Definitions
Each of the operations offered by ACP can produce an error. 

Errors can be provided synchronously by each of the invoked endpoints, or asynchronously when they occur during an execution that supports asynchronous output.

ACP must define errors for the most common error conditions. Each definition must include:
* Error code
* Description of the error condition
* A flag that says if the error is transient or permanent
* An optional schema definition of additional information that the error can be associated with.

ACP also allows agents to provide definitions of errors specific for that agent. For this purpose, ACP must define an endpoint that provides schema definitions for all agent specific error that are not included in the ACP specification.


