# Data Plane

The AGP data plane implements an efficient message routing and delivery system between agents.

## Message Format

AGP messages use a channel-based addressing scheme for content routing:

```protobuf
message AgpMessage {
    string channel_id = 1;
    string message_id = 2;
    bytes payload = 3;
    MessageMetadata metadata = 4;
}
```

## Connection Table

The connection table maintains agent connectivity information:
- Maps channel IDs to connected agents
- Tracks connection state and capabilities

## Forwarding Table

The forwarding table implements intelligent message routing:
- Maps message patterns to delivery strategies
- Supports content-based routing
- Maintains routing metrics and preferences
- Handles multicast and anycast delivery

## Message Buffer

The message buffer provides temporary storage:
- Caches messages for reliable delivery
- Implements store-and-forward when needed
- Supports message deduplication
- Handles out-of-order delivery