# Identity in CoffeeAGNTCY

CoffeeAGNTCY uses [Ory Hydra](https://www.ory.sh/hydra) as its identity provider (IDP) within the Agent Identity Service. Ory Hydra is an open-source OAuth2 and OpenID Connect server, which aligns with AGNTCY’s commitment to open, collaborative development.

The identity flow shown below outlines how CoffeeAGNTCY’s agents authenticate and verify one another through the Agentic Identity Service. before proceeding with collaborative tasks.

```mermaid
sequenceDiagram
    participant U as User
    participant S as Supervisor Agent (A2A)
    participant I as AGNTCY Identity
    participant F as Farm Agent (A2A)

    %% Valid badge flow
    F->>I: Registers as Agentic Application
    U->>S: Sends order prompt
    S->>I: Get Farm's Badge Id
    S->>I: Verify farm's badge
    I-->>S: Badge is valid
    S->>F: Sends request to create order
    F-->>S: Responds with order details
    S-->>U: Forwards the order confirmation

    %% Separator
    Note over U,F: -----------------------------

    %% Invalid badge flow
    I-->>S: Badge is invalid
    S-->>U: Unable to proceed with this prompt
    
```

For more information on Identity in AGNTCY, see the [Identity documentation.](../identity/identity.md)
