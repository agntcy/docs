# Agent Connect Protocol

## Introduction

Existing Multi-Agent Systems (MAS) provide convenient ways to build Multi-Agent Applications (MAAs) that combine various agents and enable them to communicate with each other. Such communication occurs within the MAS using internal mechanisms and APIs.

Building the Internet of Agents (IoA) requires agents built by different parties, potentially for different MAS and potentially running in different locations to interact.

While interaction between co-located agents implemented through the same MAS is trivial, it is harder in case the agents are not natively compatible or in case they run in different locations.

We propose a solution where all agents are able to communicate over the network using a standard protocol to interoperate. We call it the **Agent Connect Protocol** (**ACP**).

This document describes the main requirements and design principles of the ACP.

The current specification of the ACP can be found [here](https://spec.acp.agntcy.org/).

## ACP Requirements

Agent Connect Protocol needs to formally specify the network interactions needed to address the following:

* **Authentication**: Define how caller authenticates with an agent and what its permissions are.
* **Configuration**: Define how to configure a remote agent.
* **Invocation**: Define how to invoke a remote agent providing input for its execution.
* **Output retrieval and interrupt Handling**: Define how to retrieve the result of an agent invocation. Different interaction modes should be supported:
    * Synchronous
    * Asynchronous
    * Streaming

    This should include interrupt handling. That is, how agents notify the caller about execution suspension to ask for additional input.
* **Capabilities and Schema definitions**: Retrieve details about the agent supported capabilities and the data structures definitions for configuration, input, and output.
* **Error definitions**: Receive error notifications with meaningful error codes and explanations.


### Authentication and Authorization
Agents invoked remotely need to authenticate the caller and make sure they have the proper authorization to perform the invocation.

Authorization mechanisms are outside the scope of the ACP specification.

ACP does not enforce a single authentication scheme to be used by all agents. Instead, it defines a list of allowed authentication schemes and lets agents declare which one is adopted.

For the reason above, ACP must define an endpoint that does not require authentication and returns the specific authentication scheme that is supported by the agent.

<a id="configuration"></a>
### Configuration

Agents may support configuration.

Configuration is meant to provide parameters needed by the agent to function and to flavor their behavior.

Configurations are typically valid for multiple invocations.

ACP needs to define an endpoint to provide agent configuration.

This endpoint must be distinct by the invocation endpoint, in this case it must return an identifier of the configured instance of the agent that can be used in multiple subsequent invocations.

Invocation endpoint should also provide an option to specify the configuration. In this case the configuration is valid only for the specific invocation.

Format of the configuration data structure is specified through a schema. For more information, see [Schema Definitions](#schemas).

Configuration endpoint may return an error. For more information, see [Error Definitions](#errors).

<a id="invocation"></a>
### Invocation

ACP must define an invocation endpoint that triggers the execution of an agent or resume a previously interrupted execution of an agent.

The invocation endpoint must accept the following parameters:

* **Input**

    An input provides specific information and contexts for the agent to operate. Format of the input data structure is specified through a schema. For more information, see [Schema Definitions](#schemas).

* **Optional configuration**

    When provided, this configuration is valid only for this invocation. Alternatively, the invocation endpoint must accept the identifier of a previously configured instance of an agent. For more information, see [Configuration](#configuration).

* **Optional callback**

    When provided, the output of the invocation is provided asynchronously through the provided callback. For more information, see [Output Retrieval and Interrupt Handling](#output).

* **Optional execution identifier**

    In this case, the agent is requested to resume a previously interrupted execution, identified by the execution identifier.

The invocation endpoint must return the following:

* The **output** of the execution, in case it is provided synchronously.
* An **execution identifier**, which is then used to receive asynchronous output and to resume an interrupted execution.

Invocation endpoint may return an error. For more information, see [Error Definitions](#errors).

<a id="output"></a>
### Output Retrieval

Once an agent is invoked, it can provide output as a result of its operations.

Output can be provided to the caller synchronously (as a response of the invocation endpoint) or asynchronously (through a callback provided as input of the invocation endpoint).

Output can be provided when the following conditions occur:
* The agent has terminated its execution and provides the final result of the execution.
* The agent has interrupted its execution because it needs additional input. For example approval or chat interaction.
* The agent is still running but it provides partial results, that is, streaming.

Output must carry information about which condition occurred.

Format of the output data structure is specified through a schema. For more information, see [Schema Definitions](#schemas).

<a id="schemas"></a>
### Capabilities and Schema Definitions

The ACP does not mandate the format of the data structures used to carry information to and from an agent but it allows agents to provide definitions of those formats through the ACP.
The ACP must define an endpoint that provides schema definitions for configuration, input, and output.

Different agents may implement different parts of the protocol. For example: an agent may support streaming, while another may only support full responses. An agent may support threads while another may not.

The ACP must define an endpoint that provides details about the specific capabilities that the agent supports.

Schemas, agent capabilities, and other essential information that describe an agent are also needed in what we call the [Agent Manifest](manifest.md). 

<a id="errors"></a>
### Error Definitions

Each of the operations offered by the ACP can produce an error.

Errors can be provided synchronously by each of the invoked endpoints or asynchronously when they occur during an execution that supports asynchronous output.

The ACP must define errors for the most common error conditions.

Each definition must include the following details:
* Error code.
* Description of the error condition.
* A flag that says if the error is transient or permanent.
* An optional schema definition of additional information that the error can be associated with.

The ACP also allows agents to provide definitions of errors specific for that agent. For this purpose, the ACP must define an endpoint that provides schema definitions for all agent specific errors that are not included in the ACP specification.
