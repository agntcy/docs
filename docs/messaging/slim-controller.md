# SLIM Controller

The [SLIM](slim-core.md) Controller is a central management component that
orchestrates and manages SLIM nodes in a distributed messaging system. It
provides a unified interface for configuring routes, managing node registration,
and coordinating communication between nodes.

The Controller serves as the central coordination point for SLIM infrastructure,
offering both northbound and southbound interfaces. The northbound interface
allows external systems and administrators to configure and manage the SLIM
network. The southbound interface enables SLIM nodes to register and receive
configuration updates.

## Key Features

- **Centralized Node Management**: Register and manage multiple SLIM nodes from a single control point.
- **Route Configuration**: Set up message routing between nodes through the Controller.
- **Bidirectional Communication**: Supports both northbound and southbound gRPC interfaces.
- **Connection Orchestration**: Manages connections and subscriptions between SLIM nodes.

## Architecture

The Controller implements northbound and southbound gRPC interfaces.

The northbound interface provides management capabilities for external systems
and administrators, such as [slimctl](#slimctl). It includes:

- **Route Management**: Create, list, and manage message routes between nodes.
- **Connection Management**: Set up and monitor connections between SLIM nodes.
- **Node Discovery**: List registered nodes and their status.

The southbound interface allows SLIM nodes to register with the Controller and
receive configuration updates. It includes:

- **Node Registration**: Nodes can register themselves with the Controller.
- **Node De-registration**: Nodes can unregister when shutting down.
- **Configuration Distribution**: The Controller can push configuration updates to registered nodes.
- **Bidirectional Communication**: Supports real-time communication between the Controller and nodes.

### Control Plane Architecture

```mermaid
graph TB
    %% User and CLI
    User[👤 User/Administrator]
    CLI[slimctl CLI Tool]

    %% Control Plane Components
    subgraph "Control Plane"
        Controller[SLIM Controller<br/>- Northbound API<br/>- Southbound API<br/>- Node Registry]
        Config[Configuration<br/>Store]
    end

    %% Data Plane Nodes
    subgraph "Data Plane"
        Node1[SLIM Node 1<br/>- Message Routing<br/>- Client Connections]
        Node2[SLIM Node 2<br/>- Message Routing<br/>- Client Connections]
        Node3[SLIM Node 3<br/>- Message Routing<br/>- Client Connections]
    end

    %% Client Applications
    subgraph "Applications"
        App1[Client App 1]
        App2[Client App 2]
        App3[Client App 3]
    end

    %% User interactions
    User -->|Commands| CLI
    CLI -->|gRPC Northbound<br/>Port 50051| Controller

    %% Control plane interactions
    Controller <-->|Store/Retrieve<br/>Configuration| Config

    %% Southbound connections
    Controller <-->|gRPC Southbound<br/>Port 50052<br/>Registration & Config| Node1
    Controller <-->|gRPC Southbound<br/>Port 50052<br/>Registration & Config| Node2
    Controller <-->|gRPC Southbound<br/>Port 50052<br/>Registration & Config| Node3

    %% Inter-node communication
    Node1 <-->|Message Routing| Node2
    Node2 <-->|Message Routing| Node3
    Node1 <-->|Message Routing| Node3

    %% Application connections
    App1 -->|SLIM Protocol| Node1
    App2 -->|SLIM Protocol| Node2
    App3 -->|SLIM Protocol| Node3

    %% Styling for light/dark mode compatibility
    classDef user fill:#4A90E2,stroke:#2E5D8A,stroke-width:2px,color:#FFFFFF
    classDef control fill:#9B59B6,stroke:#6A3A7C,stroke-width:2px,color:#FFFFFF
    classDef data fill:#27AE60,stroke:#1E8449,stroke-width:2px,color:#FFFFFF
    classDef app fill:#F39C12,stroke:#D68910,stroke-width:2px,color:#FFFFFF

    class User,CLI user
    class Controller,Config control
    class Node1,Node2,Node3 data
    class App1,App2,App3 app
```

### Control Flow Sequence

```mermaid
sequenceDiagram
    participant User
    participant CLI as slimctl CLI
    participant Controller as SLIM Controller
    participant Node as SLIM Node
    participant App as Client App

    %% Node Registration
    Note over Node,Controller: Node Startup & Registration
    Node->>Controller: Register Node (Southbound)
    Controller->>Node: Registration Ack
    Controller->>Controller: Store Node Info

    %% Route Management via CLI
    Note over User,Controller: Route Management
    User->>CLI: slimctl route add org/ns/agent via config.json
    CLI->>Controller: CreateRoute Request (Northbound)
    Controller->>Controller: Validate & Store Route
    Controller->>Node: Push Route Configuration (Southbound)
    Node->>Controller: Configuration Ack
    Controller->>CLI: Route Created Response
    CLI->>User: Success Message

    %% Connection Management
    Note over User,Controller: Connection Management
    User->>CLI: slimctl connection list --node-id=slim/1
    CLI->>Controller: ListConnections Request (Northbound)
    Controller->>Controller: Retrieve Connection Info
    Controller->>CLI: Connections List Response
    CLI->>User: Display Connections

    %% Application Communication
    Note over App,Node: Application Messaging
    App->>Node: Connect & Subscribe
    Node->>App: Connection Established
    App->>Node: Publish Message
    Node->>Node: Route Message via Controller Config

    %% Node Status Updates
    Note over Node,Controller: Status Monitoring
    Node->>Controller: Status Update (Southbound)
    Controller->>Controller: Update Node Status
```

### Configuring the SLIM Controller

The Controller can be configured through the `config.yaml` file.

An example of a minimal configuration:

```yaml
northbound:
  httpHost: localhost
  httpPort: 50051
  logging:
    level: DEBUG

southbound:
  httpHost: localhost
  httpPort: 50052
  # number of node reconciler threads
  reconciler:
    threads: 3

logging:
  level: DEBUG
```

Example config to enable MTLS on Southbound endpoint using [Spire](https://spiffe.io/docs/latest/spire-about/spire-concepts/).

```yaml
  northbound:
    httpHost: 0.0.0.0
    httpPort: 50051

  southbound:
    httpHost: 0.0.0.0
    httpPort: 50052
      tls:
        useSpiffe: true
      spire:
        socketPath: "unix:///run/spire/agent-sockets/api.sock"

  logging:
    level: DEBUG

  reconciler:
    # Max number of times a failed reconcile will be retried
    maxRequeues: 15
    # Max number of reconciles that can be run in parallel for different nodes
    maxNumOfParallelReconciles: 1000

  # Specifies the SQLite database file path for storing control plane data
  database:
    filePath: controlplane.db

  spire:
    enabled: false
    # Slim Controller SVIDs will be federated with these trust domains
    trustedDomains: []
      # - cluster-a.example.org
      # - cluster-b.example.org
```

## Usage

## Prerequisites

Go 1.24 or later is required for running the SLIM Controller.

Task runner is recommended for Taskfile commands.

### Building the Controller

The Controller can be built by running the following task:

```
# Build all Controller components
task control-plane:build

# Or build just the Controller binary
task control-plane:control-plane:build
```

### Starting the Controller

The Controller can be started by running the following task:

```bash
# Start the Controller service
task control-plane:control-plane:run
```

Alternatively, start the Controller with the Docker image:

```
docker run ghcr.io/agntcy/slim/control-plane:0.0.1
```

Or use the following to also add a configuration file:

```
docker run -v ./config.yaml:/config.yaml  ghcr.io/agntcy/slim/control-plane:0.0.1 -c /config.yaml
```

### Managing Nodes

Nodes can register themselves with the Controller upon startup. Once registered, the controller can communicate with nodes using the same connection.

To enable self-registration, configure the nodes with the Controller address:

```yaml
  tracing:
    log_level: info
    display_thread_names: true
    display_thread_ids: true

  runtime:
    n_cores: 0
    thread_name: "slim-data-plane"
    drain_timeout: 10s

  services:
    slim/1:
      dataplane:
        servers: []
        clients: []
      controller:
        servers: []
        clients:
          - endpoint: "http://<controller-address>:50052"
            tls:
              insecure: true
```

Routes between SLIM nodes are automatically created by Controller upon receiving new subscriptions from clients.

Nodes can be managed through slimctl. Although routes are automatically created for client subscription you can still add/remove routes manually.

For more information, see the [slimctl](#slimctl).

## slimctl

`slimctl` is the command-line interface for the SLIM controller.

### Installing slimctl

Slimctl is available for multiple operating systems and architectures. 

To install slimctl, download the appropriate release asset from GitHub or, if you are on macOS, by using Homebrew.

#### Downloading Slimctl from Github

1. Go to the slimctl [GitHub releases page](https://github.com/agntcy/slim/releases).
2. Download the asset matching your operating system and architecture -- for example, Linux, macOS, Windows.
3. Extract the downloaded archive and then move the `slimctl` binary to a directory in your `PATH`.

#### Installing Slimctl via Homebrew (MacOS)

If you are using macOS, you can install slimctl via Homebrew:

```
brew tap agntcy/slim git@github.com:agntcy/slim.git
brew install slimctl
```

This automatically downloads and installs the latest version of slimctl for your system.


### Configuring slimctl

`slimctl` supports configuration through a configuration file, environment variables, or command-line flags.

By default, `slimctl` looks for a configuration file at `$HOME/.slimctl/config.yaml` or in the current working directory.

An example `config.yaml`:

```yaml
server: "127.0.0.1:50001"
timeout: "10s"
tls:
  insecure: false
  ca_file: "/path/to/ca.pem"
  cert_file: "/path/to/client.pem"
  key_file: "/path/to/client.key"
```

The `server` endpoint should point to a [SLIM Control](https://github.com/agntcy/slim/tree/slim-v0.7.0/control-plane/control-plane) endpoint which is a central service managing SLIM node configurations.

### Commands

List nodes:

`slimctl controller node list`

List connections on a SLIM instance:

`slimctl controller connection list --node-id=<slim_node_id>`

List routes on a SLIM instance:

`slimctl controller route list --node-id=<slim_node_id>`

Add a route to the SLIM instance:

`slimctl controller route add <organization/namespace/agentName/agentId> via <slim-node-id or path_to_config_file> --node-id=<slim_node_id>`

Delete a route from the SLIM instance:

`slimctl controller route del <organization/namespace/agentName/agentId> via <slim-node-id or path_to_config_file> --node-id=<slim_node_id>`

Print version information:

`slimctl version`

Run `slimctl <command> --help` for more details on flags and usage.

### Example 1: Create, Delete Route using node-id

Add route for node `slim/a` to forward messages for `org/default/alice/0` to node `slim/b`.
```bash
slimctl controller node list

Node ID: slim/b status: CONNECTED
  Connection details:
  - Endpoint: 127.0.0.1:46457
    MtlsRequired: false
    ExternalEndpoint: test-slim.default.svc.cluster.local:46457
Node ID: slim/a status: CONNECTED
  Connection details:
  - Endpoint: 127.0.0.1:46357
    MtlsRequired: false
    ExternalEndpoint: test-slim.default.svc.cluster.local:46357

slimctl controller route add org/default/alice/0 via slim/b --node-id slim/a


# Delete an existing route
slimctl controller route del org/default/alice/0 via slim/b --node-id slim/a
```

### Example 2: Create, Delete Route Using `connection_config.json`


```bash
# Add a new route
cat > connection_config.json <<EOF
{
"endpoint": "http://127.0.0.1:46357"
}
EOF
slimctl controller route add org/default/alice/0 via connection_config.json


# Delete an existing route
slimctl controller route del org/default/alice/0 via http://localhost:46367
```

For full reference of connection_config.json, see the [client-config-schema.json](https://github.com/agntcy/slim/blob/slim-v0.7.0/data-plane/core/config/src/grpc/schema/client-config.schema.json).

### Managing SLIM Nodes Directly

SLIM nodes can be configured to expose a Controller endpoint of a SLIM instance, slimctl can connect to this endpoint to manage the SLIM instance directly by using slimctl `node` sub-command. In this case, in the configuration file, the server should point to the SLIM instance endpoint.

To enable this, configure the node to host a server allowing the client to connect:

```yaml
  tracing:
    log_level: info
    display_thread_names: true
    display_thread_ids: true

  runtime:
    n_cores: 0
    thread_name: "slim-data-plane"
    drain_timeout: 10s

  services:
    slim/1:
      dataplane:
        servers: []
        clients: []
      controller:
        servers:
            - endpoint: "0.0.0.0:46358"
              tls:
                insecure: true # Or specify tls cert and key
        clients: []
```

List connections on a SLIM instance:
`slimctl node connection list --server=<node_control_endpoint>`

List routes on a SLIM instance:
`slimctl node route list --server=<node_control_endpoint>`

Add a route to the SLIM instance:
`slimctl node route add <organization/namespace/agentName/agentId> via <config_file> --server=<node_control_endpoint>`

Delete a route from the SLIM instance:
`slimctl node route del <organization/namespace/agentName/agentId> via <host:port> --server=<node_control_endpoint>`
