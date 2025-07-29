# Data Plane

The [SLIM](slim-core.md) Data Plane implements an efficient message routing and delivery system between agents.

## Message Format

SLIM messages use a channel-based addressing scheme for content routing:

```protobuf
message SLIMMessage {
    string channel_id = 1;
    string message_id = 2;
    bytes payload = 3;
    MessageMetadata metadata = 4;
}
```

## Connection Table

The connection table maintains agent connectivity information by mapping channel IDs to connected agents and tracking connection state and capabilities.

## Forwarding Table

The forwarding table implements intelligent message routing by providing the following:

- Maps message patterns to delivery strategies.
- Supports content-based routing.
- Maintains routing metrics and preferences.
- Handles multicast and anycast delivery.

## Message Buffer

The message buffer provides temporary storage by implementing the following:

- Caches messages for reliable delivery.
- Implements store-and-forward when needed.
- Supports message deduplication.
- Handles out-of-order delivery.

## Data Plane Flow

```mermaid
graph LR
    A([Input]) --> B[Buffer]
    B --> C{Forwarding}
    C --> D[Connection]
    D -->|Direct| E([Output])
    D -->|Multicast| E
    D -->|Anycast| E

    style B fill:#ffffff,stroke:#000000,stroke-width:2px
    style C fill:#f0f0f0,stroke:#000000,stroke-width:2px
    style D fill:#e0e0e0,stroke:#000000,stroke-width:2px
```

The diagram shows the message flow through the SLIM data plane components:

1. Messages enter the system and are processed by the Message Buffer.
2. The Message Buffer handles deduplication and store-and-forward.
3. The Forwarding Table determines routing strategy.
4. The Connection Table manages delivery to connected agents.
5. Messages are delivered through direct, multicast, or anycast methods.

## Group Management and Encryption

Agents can be grouped together to form a group. To create a group, create a session as moderator.

The following needs to be defined:

- `remote_organization`
- `remote_namespace`
- `broadcast_topic`

Encryption can be enabled through a JSON Web Token (JWT) in the session creation request by setting `mls_enable` to `true`.

To enable group encryption:

1. Define 'jwt_identity'
2. Define shared secret
3. Set `mls_enable` to `true`

The group is created by sending a message to the broadcast topic.

## Authentication

Authentication can be configured when running `create_pyservice`. The following needs to be defined through `shared_secret_identity`:

- `PyIdentityProvider`
- `PyIdentityVerifier`

The provider is JWT and the verifier is a public key.
