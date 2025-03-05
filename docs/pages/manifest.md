# Agent Manifest

## Introduction

An Agent Manifest is a document that describes in detail the following:
* What the agent is capable of.
* How the agent can be consumed if provided as-a-service.
* How the agent can be deployed if provided as a deployable artifact.
* What are the dependencies of the agent, that is, which other agents it relies on.

The manifest is designed to be used by [Agent Connect Protocol](connect.md) and the Workflow Server and stored in the Agent Directory with the corresponding OASF extensions.

This document describes the principles of the Agent Manifest definition.

## Agent Manifest Structure

Agent Manifest includes the following sections:
* [Agent Identification and Metadata](#agent-identification-and-metadataidentification)
* [Agent Interface Data Structure Specification](#agent-interface-data-structure-specification)
* [Agent Deployment and Consumption](#agent-deployment-and-consumption)
* [Agent Dependencies](#agent-dependencies)

<a id="agent-identification-and-metadataidentification"></a>
### Agent Identification and Metadata

Agent Manifest must uniquely identify an agent within the namespace it is part of. This is done through a unique name and a version.

Agent Manifest must include a natural language description that describes what the agent is capable of doing. This allows user and potentially other agents to select the agent that best fits a given task.

Agent Manifest can include metadata that provides additional information about the agent, such as ownership, timestamps, tags, and so on.

<a id="agent-interface-data-structure-specification"></a>
### Agent Interface Data Structure Specification
Agents willing to interoperate with other agents expose an interface that allow for invocation and configuration.

Agent Connect Protocol specifies a standard for this interface. However, it specifies methods to configure and invoke agents, but it does not specify the format of the data structures that an agent expects and produces for such configurations and invocations.

The specification of these data structures is included in what we call the Agent ACP descriptor, which can be provided by ACP itself, but it is also defined as part of the Agent Manifest.

Agent ACP descriptor must include an interface data structure specification section that provides schema definitions for the following data structures:
* **Configuration**: The data structure used to provide agent configuration.
* **Input**: The data structures used to provide agent input.
* **Output**: The data structure used to retrieve agent output.

If an agent supports interrupts, meaning its execution can be interrupted to request additional input and then resumed, the Agent Manifest needs to define the types of interrupts that can possibly occur.

For each of the interrupts it must define the following:
* **Interrupt Output**: The format of the output provided by the specific interrupt.
* **Resume Input**: The input expected by the agent to resume its execution when this specific interrupt occurs.

All schema definitions must include natural language description of the data structure, natural language description of each data structure element, and valid examples of correctly populated data structures.

<a id="agent-deployment-and-consumption"></a>
### Agent Deployment and Consumption

Agents can be provided in two different forms, which we call deployment modes:

* **As a service**: a network endpoint that exposes an interface to the agent (for example, Agent Connect Protocol).
* **As a deployable artifact**, for example:
   * A docker image, which once deployed exposes an interface to the agent (for example, Agent Connect Protocol).
   * A source code bundle, which can be executed within the specific runtime and framework it is built on.

The same agent can support one or more deployment modes.

The Agent Manifest must include a list of all the possible deployment modes supported by the agent. For each mode, it needs to provide all the information needed to consume the agent service or to deploy and then consume it, including authentication details when applicable.

<a id="agent-dependencies"></a>
### Agent Dependencies

An agent may depend on other agents, which means that at some point of its execution it needs to invoke them to accomplish its tasks. We refer to these other agents as **sub-agents**.  A user who wants to use the agent, needs to know this information and check that the dependencies are satisfied, that is, make sure that the sub-agents are available.
This may imply simply checking that sub-agents are reachable or deploying them, according to the deployment modes they support.

The Agent Manifest must include a list of all sub-agents in the form of a list of references to their manifests.

Note the recursive nature of Agent Manifests that can point in turn to other Agent Manifests as dependencies.
