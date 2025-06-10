# Introduction

The AGNTCY is an open source collective building the infrastructure for The Internet of Agents (IoA): an open, interoperable internet for agent to agent collaboration.

The IoA represents a transformative initiative in the field
of artificial intelligence designed to create a standardized ecosystem for AI
agent discovery, interconnection, and collaboration. This comprehensive
framework addresses the growing need for interoperability and secure
communication between AI agents developed across different frameworks and
platforms.

## Vision

Agentic AI will accelerate all of human work. Enterprises need to create agentic workflows and applications combining internal and third-party agents to fully leverage the power of AI, accelerate their business, and achieve significant productivity gains.
We believe that an open, interoperable Internet of Agents is the key to enabling the best possible path forward to accelerate innovation and create the most value for all participants, from builders to operators, developers to consumers across all industries and businesses.

## Mission

We are an open source collective commited to build the Internet of Agents to be accessible to all. Our mission is to build a diverse, collaborative space to innovate, develop, and maintain software components and services that solve key problems in the domain of agentic workflows and multi-agent applications.

## Capabilities

Based on advanced protocols, frameworks, and components, the goal of IoA software infrastructure is to enable and simplify the creation of multi-agent applications through the following steps:

1. **DISCOVER**: Find and evaluate the best agents for the job.
1. **COMPOSE**: Connect agents into effective workflows across any framework or vendor.
1. **DEPLOY**: Run multi-agent systems at scale, securely.
1. **EVALUATE**: Monitor performance and improve efficiency and efficacy over time.

## Technical Objectives

1. **Interoperability**: Establish a common protocol that enables AI agents from different vendors and platforms to communicate and work together efficiently.
2. **Security**: Ensure secure interactions between agents through robust authentication, authorization, and encryption mechanisms.
3. **Scalability**: Design a scalable architecture that leverages the cloud-native stack optiomally, supporting a growing number of agents and interactions without compromising performance.
4. **Standardization**: Develop standardized data models and schemas to ensure consistent data representation and validation across the ecosystem.

## Core Components

The initial set of IoA components and architecture is outlined below. This is a starting point - as new members join and bring their contributions, the collective will continue to evolve and expand the IoA architecture, components, and interfaces.

![IoA Stack](assets/ioa_stack.png)

1. **Agent Identity**: A system that leverages decentralized technologies to manage and verify the identities of Agents issued by any organization, ensuring secure and trustworthy interactions.
1. **Open Agent Schema Framework (OASF)**: An OCI based extensible data model allowing to describe agents' attributes and ensuring unique identification of agents. Current OASF repo can be found [here](https://github.com/agntcy/oasf), OASF schema documentation can be found [here](https://schema.oasf.agntcy.org).
1. **Agent Directory**: Allows to announce and discover agents or multi-agent applications. Any organization can run its directory and keep it in sync with others, forming the Internet of Agents inventory.
1. **Agent Manifest**: A standard format to describes agents, their capabilities, their dependencies, and how to deploy or consume them. The manifest is designed to be used by ACP and the Workflow Server and stored in the Agent Directory with the corresponding OASF extensions.
1. **Semantic SDK**: 
    * **I/O Mapper Agent**: Handles semantic data adaptations between agents that need to communicate with each other.
    * **Semantic Router**: Directs workflows via semantic matches. (coming soon)
1. **Syntactic SDK**:
    * **Agent Connect Protocol (ACP)**: A standard interface to invoke agents (or agentic applications), provide input, retrieve output, retrieve supported schemas, graph topology and other useful information. Current ACP spec can be found [here](https://spec.acp.agntcy.org/).
    * **API-bridge Agent** to connect an Agent with any API end-point (tools or data sources)
    * **Human in the Loop Agent** to interface with human input/output seamlessly. (coming soon)
1. **Messaging SDK**:
    * **Agent Gateway Protocol (AGP)**: A protocol that defines the standards and guidelines for secure and efficient network-level communication between AI agents. AGP ensures interoperability and seamless data exchange by specifying message formats, transport mechanisms, and interaction patterns.
    * **Agent Gateway**: Offers handy secure (MLS and quantum safe) network-level communication services to a group of agents (typically those of a given multi-agent application) through SDK/Libraries. It extends gRPC to support  pub/sub interactions in addition to request/reply, streaming, fire & forget and more.
1. **Agent Workflow Server**: Deploys and supervises agent workflows written in various frameworks and makes them available through the Agent Connect Protocol. Such workflows could be multi-agent applications including a mix of toolkit agents, local and remote agents. 
1. **Agentic Ensemble Observability & Evaluation**: Telemetry collectors, tools and services to enable multi-agent application observability and evaluation
1. **Agentic Ensemble Security**: Tools and services to trust and  protect multi-agent applications.


The following diagram shows a simplified architecture of the core components described above.


![IoA Arch](assets/ioa_arch.png)

## Benefits

* **Enhanced Collaboration**: By enabling seamless communication and data exchange, IoA fosters collaboration between AI agents, leading to more sophisticated and integrated solutions.
* **Improved Efficiency**: Standardized protocols and frameworks reduce the complexity of integrating diverse AI agents, resulting in faster development and deployment of AI-driven applications.
* **Increased Security**: Robust security mechanisms ensure that interactions between agents are secure, protecting sensitive data, and preventing unauthorized access.
* **Future-Proof Architecture**: The scalable and flexible design of IoA ensures that the ecosystem can grow and adapt to future advancements in AI technology.
