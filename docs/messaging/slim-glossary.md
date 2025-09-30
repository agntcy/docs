# SLIM Messaging Glossary

This glossary defines technical terms referenced across the SLIM messaging documentation: core concepts, naming, sessions, routing, configuration, security, integrations (SLIMRPC, A2A, MCP), and deployment tooling. Terms are alphabetized.

---

## A

### Ack (Acknowledgment)
A confirmation—explicit or implicit—that a sent message was delivered or processed. In reliable modes, missing acks trigger retries until `max_retries` is reached or a timeout fires.

### Anycast
Session/routing mode where a message addressed to a 3‑component name (`org/namespace/service`) is delivered to exactly one currently reachable instance. Each message may choose a different instance. Useful for stateless load distribution and discovery.

---

## C

### Channel (Multicast Channel)
Logical grouping identifier (the SLIM name without a unique client hash) for many-to-many communication. All participants receive every multicast message.

### Channel Moderator (Moderator)
Creator and privileged manager of a multicast channel. Invites/removes participants and coordinates MLS group state distribution where applicable.

### Channel Name Pattern
Uses SLIM naming structure up to the service level: `org/namespace/service` (no client hash). Serves as a shared multicast identifier.

### Client (Application Client)
Runtime endpoint connected to a SLIM node. Identified by full four-component name: `org/namespace/service/clientHash`.

### Client Configuration
Configuration branch describing outbound (client) connections: endpoint, TLS, timeouts, headers, auth, proxy, metadata.

### Client Instance ID (Hash Component)
Fourth name component, typically derived from identity material (e.g., a hash of a public key). Ensures unique and routable unicast identity per instance.

### Configuration Distribution
Process by which the Controller transmits updated routing, connection, or subscription data to registered nodes via the southbound interface.

### Configuration Substitution
Mechanisms to replace placeholders with environment variable values or file content at load time (e.g., injecting secrets, certificates).

### Connection (Routing Connection)
Configured link (endpoint + parameters) enabling a SLIM node to route traffic to another SLIM node.

### Connection Management
Administrative operations (list/create/delete) over connections, typically via Controller APIs or `slimctl`.

### Connection Retry / Keepalive
Transport mechanisms and parameters ensuring persistent liveness and timely detection of failed peers (idle timeout, heartbeat intervals).

### Control Plane
Management layer (Controller + `slimctl` + gRPC APIs) orchestrating routes, connections, channels, subscriptions, and identity — not the direct payload flow.

### Controller (SLIM Controller)
Central orchestration service offering northbound (administrative) and southbound (node) gRPC interfaces for configuration, topology, and group/channel operations.

---

## D

### Data Plane (Messaging Layer)
Operational pipeline for message routing, delivery, encryption (MLS), and session state, implemented in SLIM nodes. It can be used synonymously with "SLIM Node".

### Discovery (Service Discovery via Anycast)
Initial interaction where Anycast picks any available instance; if persistent affinity is needed, Unicast (sticky) binds subsequent messages to a chosen instance.

### Drain Timeout
Grace period during node shutdown to finish in-flight operations before forceful termination.

---

## E

### Endpoint
Host:port (and scheme) on which a server listens or a client connects (e.g., `http://localhost:46357` or `https://localhost:46357` for clients, `0.0.0.0:46357` for servers).

### Environment Variable Substitution
Injecting dynamic environment values into config fields at runtime.

---

## F

### File Content Substitution
Populating configuration entries with the contents of external files (certificates, keys, tokens) at load time.

---

## G

### Group (Multicast Group)
Set of participants joined to a multicast channel sharing message distribution and, when enabled, an MLS security context.

### Group Communication
Many-to-many pattern where each channel message is broadcast to all current participants.

### Group Session
Programmatic session object (in bindings) representing a multicast channel, its members, invitations, and MLS state.

---

## H

### Hash-Based Client Identifier
Deterministic identity-derived value forming the fourth component of a client name, ensuring unique unicast addressing.

---

## I

### Identity
Cryptographic or token-based representation of a workload (shared secret, JWT, SPIFFE SVID) determining trust and naming uniqueness.

### Invitation (Group Invitation)
Control message enabling a client to join an existing multicast group; processed by a listener via `listen_for_session`.

---

## L

### Local Name
The fully qualified SLIM name representing the current application endpoint.

---

## M

### Max Retries (Session Config)
Upper limit on retransmission attempts for a single message lacking timely acknowledgment.

### Metadata (Session/Message Metadata)
Custom key-value tags (role, replicas, environment, region) used for observability, routing hints, or policy.

### MLS (Message Layer Security)
End-to-end group key agreement and encryption protocol (RFC 9420) providing confidentiality and integrity beyond hop-level TLS termination.

### Moderator (Channel Moderator)
See Channel Moderator.

### Multicast
Session type enabling many-to-many distribution; every message is delivered to all participants in the channel.

---

## N

### Name (SLIM Name)
Structured routing identifier: `organization/namespace/service/clientHash` (full) or first three components for anycast/channel addressing.

### Namespace
Second component of a SLIM name; often encodes environment, region, or an organizational partition.

### Node (SLIM Node)
Runtime process implementing the data plane: message routing, session handling, MLS operations, optional control endpoints.

### Node ID
Configured identifier (e.g., `slim/0`) for referencing a node in Controller operations (connections, subscriptions).

### Node Registration
Southbound action where a node registers with the Controller to receive configuration updates and provide status.

### Northbound Interface
Controller administrative API consumed by operators/tools (`slimctl`) for route, connection, and subscription management.

---

## O

### Observed Timeout (Session Timeout)
Elapsed interval before a message is considered undelivered (triggering retry or failure) if no acknowledgment is received.

### Organization
First component of a SLIM name representing the top-level administrative or tenant boundary.

---

## P

### Participant (Group Participant)
Client that has accepted an invitation and joined a multicast group, receiving all channel traffic.

---

## R

### Reload Interval (TLS / Identity Rotation)
Polling period for reloading certificates or keys (notably with SPIRE dynamic rotation).

### Retry
Re-attempt of sending a message after a timeout window, capped by `max_retries`.

### Route (Routing Entry)
Controller-managed mapping directing messages for a particular name (or prefix) through a specific connection.

### Route Management
Administrative operations manipulating routing entries (list/add/delete) to shape message forwarding paths.

### Routing Configuration
Aggregate of connections plus subscriptions establishing effective pathways across nodes in the SLIM network.

---

## S

### Server (Inbound Endpoint)
Configured listener receiving connections/messages (with optional TLS/auth).

### Session (SLIM Session)
Abstraction for interaction context: Anycast (distributed), Unicast (affinity), Multicast (group). Manages encryption (MLS), retries, and message sequencing.

### Session Layer
Middleware that abstracts encryption, invitations, routing resolution, and reliability, offering simple send/receive primitives.

### Shared Secret Identity
Simplest identity bootstrap (common secret) used for demos or tests before deploying stronger mechanisms.

### Slimctl
Command-line tool managing routes, connections, subscriptions, and nodes via Controller or direct node endpoints.

### SLIM (Secure Low-Latency Interactive Messaging)
Framework delivering secure, scalable, low-latency messaging with unified naming, session semantics, encryption, and extensibility.

### SLIMA2A
Integration of A2A agent protocol over SLIM using SLIMRPC-generated stubs.

### SLIM Controller
See Controller.

### SLIM Data Plane
See Data Plane (Messaging Layer).

### SLIM Group
Multicast channel plus participant set and associated MLS group state.

### SLIM Node
See Node.

### SLIM Session
See Session.

### SLIM Specification
Formal protocol and architecture definition (naming, routing, session, security semantics).

### SLIMRPC
Protobuf-based RPC framework operating over SLIM transport (unary and streaming patterns). Analogous to gRPC but using SLIM naming and channels.

### SLIMRPC Channel
Client-side abstraction binding local identity and remote SLIM name for RPC invocation.

### SLIMRPC Compiler (protoc-slimrpc-plugin)
Protoc plugin generating Python stubs and servicers for SLIMRPC services defined in `.proto` files.

### Southbound Interface
Controller API for node registration, de-registration, configuration push, and status updates.

### Subscription
Binding between a routed name/prefix and a connection so messages destined to that name traverse the appropriate path.

### Timeout (Request / Session Timeout)
Upper bound for waiting on acknowledgments or RPC responses before retry/failure escalation.

---

## U

### Unicast
Session mode binding communication to a specific discovered instance after an initial discovery. Ensures message affinity to a single endpoint.

### User (Administrator)
Operator employing `slimctl` or client SDKs to configure and monitor SLIM infrastructure components.
