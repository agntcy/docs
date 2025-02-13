# Agent Manifest

## Introduction

An Agent Manifest is a document that describes in detail:
* what an agent is capable of
* how an agent can be consumed if provided as-a-service
* how an agent can be deployed if provided as a deployable artifact
* what are the dependencies of an agent, i.e. what other agents it relies on

Agent Manifest specification, which is part of the [Agent Connect Protocol](connect.md) specification, defines a standard format for Agent Manifests.

This document describes the main requirements of the Agent Manifest definition.

## Agent Manifest Structure

Agent Manifest needs to include the following sections.

### Agent Indentification and Metadata
Agent Manifest must uniquely identify an agent within the namespace it is part of, this is done through a unique name and a version. 

Agent Manifest must include a natural language description that illustrates what the agent is capable of doing. This allows user and potentially other agents to select an agent that best fit a given task.

Agent Manifest could include metadata that provide additional information about the agent, such as ownership, timestamps, tags etc.

### Agent Interface Data Structure Specification
Agents willing to interoperate with other agents, expose an interface that allow for invocation and configuration. For example Agent Connect Protocol specifies a standard for this interface. 

This interface however specifies methods to configure, invoke agents, but it does not specify the format of the data structures that an agent expects and produces for such configurations, invocation and results.

The specification of these data structure is included in the Agent Manifest.

Agent Manifest must include an interface specification section that provides schema definitions for the following data structures:
* Configuration: The data structure used to provide agent configuration 
* Input: The data structures used to provide agent input
* Output: The data structure used to retrieve agent output

If an agent supports interrupts, meaning its execution can be interrupted to request additional input and then resumed, the Agent Manifest needs to define the types of interrupts that can possibly occur. For each of them:
   * Interrupt Output: The format of the output provided by the specific interrupt
   * Resume Input: The input expected by the agent to resume its execution when this specific interrupt occurs.

All schema definitions must include natural language description of the data structure, natural language description of each data structure element, and valid examples of correctly populated data structures. 

### Agent Deployment and Consumption
Agents can be provided in two different forms, which we call deployment modes:

* **As a service**: a network endpoint that exposes an interface to the agent (e.g Agent Connect Protocol)
* **As a deployable artifact**, in particular:
   * A docker image, which once deployed exposes an interface to the agent (e.g. Agent Connect Protocol)
   * A source code bundle, which can be executed within the specific runtime and framework it is built.

The same agent can support one or more of the forms described above.

The Agent Manifest must include a list of all the possible deployment modes supported by the agent. For each mode it needs to provide all the information needed to consume the agent service or to deploy and then consume it, including authentication details when applicable.

### Agent Dependencies
An agent may depend on other agents, which means that at some point of its execution it needs to invoke them to accomplish its tasks. We refer to these other agents as sub-agents.  A user that wants to use the agent needs to know this information and check that the dependencies are satisfied, i.e. make sure that the sub-agents are available. 
This may imply simply check that sub-agents are available or deploy them, according to the deployment modes they support.

The Agent Manifest must include a list of all sub-agent in the form of a list of references to their manifests.

Note that recursive nature of Agent Manifests that can point in turn to other Agent Manifests as dependencies.

## How Agent Manifest relates to Agent Connect Protocol 
Agent Manifest is part of the specification of Agent Connect Protocol. 

A potential user of an agent needs to access the agent manifest to get all the needed information to interact with the agent.

The manifest is available as an "offline" document, e.g. a json file or it can be retrieved directly from a running agent through the Agent Connect Protocol.

## How Agent Manifest relates to Agent Directory and Open Agent Schema Framework
