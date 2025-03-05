## Introduction

The AGNTCY is an open source collective building the infrastructure for The Internet of Agents: an open, interoperable internet for agent to agent collaboration. 

### Vision

Agentic AI will accelerate all of human work. Enterprises must create agentic workflows and applications combining internal and 3rd party agents to fully leverage the power of AI, accelerate their business and unlock new step-change in productivity.
We believe that an open, interoperable Internet of Agents is the key to enabling the best possible path forward to accelerate innovation and create the most value for all participants, from builders to operators, developers to consumers across all industries and businesses. 

### Mission

We are an open source collective that will build the Internet of Agents to be accessible for all: A diverse, collaborative space to innovate, develop, and maintain software components and services that solve key problems in the domain of agentic workflows and multi-agent applications. 

### Capabilities

Based on advanced protocols, frameworks and components, the goal of IoA software infrastructure enables and simplify the creation of multi-agent applications through the following steps:
	1	DISCOVER: Find and evaluate the best agents for the job 
	2	COMPOSE: Connect agents into effective workflows across any framework or vendor 
	3	DEPLOY: Run multi-agent systems at scale, securely 
	4	EVALUATE: Monitor performance and improve efficiency and efficacy over time 

### Technical Objectives

1. **Interoperability**: Establish a common protocol that enables AI agents from different vendors and platforms to communicate and work together efficiently.
2. **Security**: Ensure secure interactions between agents by implementing robust authentication, authorization, and encryption mechanisms.
3. **Scalability**: Design a scalable architecture that optimally leverages the underlying cloud-native stack and can support a growing number of agents and interactions without compromising performance.
4. **Standardization**: Develop standardized data models and schemas to ensure consistent data representation and validation across the ecosystem.

### Core Components

The initial set of IoA components and architecture is described below. As a very first step, we are sharing 2 important specifications: OASF and ACP. In a few weeks the collective will release code and documentation for most of the components. This is a starting point - as new members join and bring their contributions, the collective will continue to evolve and expand the IoA architecture, components and interfaces.   

```{image} ../_static/ioa_stack.png
:alt: Simplified Internet of Agent Stack
:width: 100%
:align: center
```

1. **Open Agent Schema Framework (OASF)**: A framework that provides standardized data models and schemas for representing and validating data exchanged between agents. OASF ensures data integrity and consistency across the Internet of Agents ecosystem.
1. **Agent Directory**: A centralized service that stores and manages OASF metadata about AI agents, including their capabilities, attributes, and constraints. This service enables agents to discover and connect with each other based on their advertised capabilities.
1. **Decentralized Agent Identity**: A system that leverages decentralized technologies to manage and verify the identities of Agents issued by any organization, ensuring secure and trustworthy interactions.
1. **Agent Connect Protocol (ACP)**: A protocol that defines a standard interface to invoke agents, configure them, provide input, and retrieve output.
1. **Multi-Agent Application Toolkit**: A set of agents and software libraries that support seamless creation of Multi-Agent workflows.
1. **Agent Workflow Server**: A server that leverages ACP to manage and executes workflows involving multiple AI agents, ensuring coordinated and efficient task execution.
1. **Agent Manifest**: A standard format to describes agents, their capabilities, their dependencies, and how to deploy or consume them. The manifest is designed to be used by ACP and the Workflow Server and stored in the Agent Directory with the corresponding OASF extensions.  
1. **Agent Gateway Protocol (AGP)**: A protocol that defines the standards and guidelines for secure and efficient network-level communication between AI agents. AGP ensures interoperability and seamless data exchange by specifying message formats, transport mechanisms, and interaction patterns.
1. **Agent Observability**: Tools and techniques for monitoring and analyzing the behavior and performance of AI agents, providing insights into their operations and interactions.

The following diagram shows a simplified architecture of the core components described above.


```{image} ../_static/ioa_arch.png
:alt: Simplified Internet of Agent Stack
:width: 100%
:align: center
```

### Benefits

1. **Enhanced Collaboration**: By enabling seamless communication and data exchange, IoA fosters collaboration between AI agents, leading to more sophisticated and integrated solutions.
2. **Improved Efficiency**: Standardized protocols and frameworks reduce the complexity of integrating diverse AI agents, resulting in faster development and deployment of AI-driven applications.
3. **Increased Security**: Robust security mechanisms ensure that interactions between agents are secure, protecting sensitive data and preventing unauthorized access.
4. **Future-Proof Architecture**: The scalable and flexible design of IoA ensures that the ecosystem can grow and adapt to future advancements in AI technology.

