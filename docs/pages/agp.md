# Core Concepts

Multi-agent software incorporates complex design patterns inherited from various
established frameworks:

- Machine learning
- Cloud-native computing
- Interactive real-time applications
- Big data processing

LLMs (Large Language Models) and agent frameworks serve as middleware that
automates processes traditionally requiring human intervention. This integration
layer connects diverse systems and enables new automation capabilities through:

- Natural language processing
- Contextual understanding
- Task decomposition
- Autonomous decision making

By integrating these technologies, multi-agent systems can manage complex
workflows while ensuring:

- Cloud-native scalability
- Real-time responsiveness
- Large-scale data processing
- Seamless ML model integration

## Main Components

Interconnecting these systems at scale requires meeting strict latency and
response time requirements. AGP aims to provide a secure, scalable, and
user-friendly communication framework that unifies state-of-the-art capabilities
from all mentioned frameworks into a single implementation.

The main components of AGP are:

- Data plane
- Session layer
- Control plane
- Security layer.

```mermaid
graph TB
    %% Services
    AS[Authentication Service]
    DS[Delivery Service]

    %% Clients and Members
    Client1[Client 1]:::client
    Client2[Client 2]:::client
    Client3[Client 3]:::client

    %% Group Definition
    subgraph MLSGroup[MLS Group]
        Member1[Member 1]:::member
        Member2[Member 2]:::member
    end

    %% Client Authentication
    Client1 --> AS
    Client2 --> AS
    Client3 --> AS

    %% Client-DS Connections
    Client1 -.-> DS
    Client2 --> DS
    Client3 --> DS

    %% Member Associations
    Client2 === Member1
    Client3 === Member2

    %% Styles
    classDef service fill:#f9f,stroke:#333,stroke-width:2px
    classDef client fill:#bbf,stroke:#333,stroke-width:2px
    classDef member fill:#fbb,stroke:#333,stroke-width:2px

    class AS,DS service
    class Client1,Client2,Client3 client
    class Member1,Member2 member
```