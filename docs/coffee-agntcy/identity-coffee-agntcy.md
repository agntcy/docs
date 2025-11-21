# Identity in CoffeeAGNTCY

!!! info "Setup Guide"
    For setup instructions and testing details, see the [Identity Integration Documentation](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/docs/identity_integration.md).

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

## TBAC (Tool-Based Access Control)

CoffeeAGNTCY demonstrates TBAC implementation at both agent and tool levels, controlling access across different communication patterns.

### Agent-Level TBAC (Broadcasting)

This flow shows how TBAC controls agent-to-agent communication when broadcasting to multiple farms:

```mermaid
sequenceDiagram
    User->>Supervisor Agent (A2A): Sends list inventories prompt
    Supervisor Agent (A2A)->>AGNTCY Identity: Get the access token for TBAC
    AGNTCY Identity->>Supervisor Agent (A2A): Badge verified, return access token
    Supervisor Agent (A2A)->>Colombia Farm Agent (A2A): Broadcast list inventory with access token
    Supervisor Agent (A2A)->>Vietnam Farm Agent (A2A): Broadcast list inventory with access token
    Supervisor Agent (A2A)->>Brazil Farm Agent (A2A): Broadcast list inventory with access token
    Colombia Farm Agent (A2A)->>Supervisor Agent (A2A): Auth-enabled, verified access token, return inventory
    Vietnam Farm Agent (A2A)->>Supervisor Agent (A2A): Auth-enabled, verified access token, return inventory
    Brazil Farm Agent (A2A)->>Supervisor Agent (A2A): Auth not enabled, return inventory without token verification
    Supervisor Agent (A2A)->>User: Collected all inventories, return aggregated results
```

### Tool-Level TBAC (Point-to-Point)

This flow demonstrates TBAC enforcement for MCP tool invocations:

```mermaid
sequenceDiagram
    User->>Supervisor Agent (A2A): Sends create order prompt
    Supervisor Agent (A2A)->>Colombia Farm Agent (A2A): Sends request to create order
    Colombia Farm Agent (A2A)->>AGNTCY Identity: Get access token for TBAC
    AGNTCY Identity->>Colombia Farm Agent (A2A): Badge verified, return access token
    Colombia Farm Agent (A2A)->>Payment Service (MCP): Make list transactions MCP tool call with access token
    Payment Service (MCP)->>Colombia Farm Agent (A2A): Verified access token, return list of transactions
    Colombia Farm Agent (A2A)->>AGNTCY Identity: Get access token for TBAC
    AGNTCY Identity->>Colombia Farm Agent (A2A): Badge verified, return access token
    Colombia Farm Agent (A2A)->>Payment Service (MCP): Make create payment MCP tool call with access token
    Payment Service (MCP)->>Colombia Farm Agent (A2A): Verified access token, payment created
    Colombia Farm Agent (A2A)->>Supervisor Agent (A2A): Order created successfully
    Supervisor Agent (A2A)->>User: Return order details
```

For more information on Identity in AGNTCY, see the [Identity documentation.](../identity/identity.md)
