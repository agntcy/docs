# Agent Workflow Server Introduction

A workflow server is essential for building Multi-Agent Applications (MAAs) as it ensures execution and deployment of agents and sub-agents in both development and production environments. It also guarantees consistent exposure of the Agent Connect Protocol (ACP), enabling smooth interoperability and communication within the application.

The Agent Workflow Server (AgWS) enables participation in the IoA. It accommodates agents from diverse frameworks, ensuring their dependencies are met and that they can be invoked through ACP, regardless of their underlying implementation.

The server operates through a command-line interface that inputs an agent, ensuring it runs and is accessible through ACP.

Agents are made available to the AgWS through a manifest, which details the agent's source, whether it be raw source code, a Docker image, or a remote endpoint. The manifest also includes a list of dependencies.

The AgWS can create running agents as local processes, Docker containers, or containers within a remote Kubernetes cluster. 

Additionally, it offers mechanisms for state preservation across multiple instances, through in-memory solutions or stable storage options.