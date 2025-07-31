# Getting Started with SLIM

SLIM is a secure, scalable, and user-friendly communication framework that
unifies state-of-the-art capabilities from all mentioned frameworks into a
single implementation.

For more information on SLIM, see the [detailed
documentation](../messaging/slim-core.md).

## Installation

SLIM is composed of multiple components, each with its own installation
instructions. Below are the main components and how to install them.

### SLIM Node

The SLIM Node is the core component that handles messaging operations. It can be
installed either using the provided container image, with
[cargo](https://github.com/rust-lang/cargo) or with [Helm](https://helm.sh/).

#### Using Docker

```bash
docker pull ghcr.io/agntcy/slim:latest

cat << EOF > ./config.yaml
tracing:
  log_level: info
  display_thread_names: true
  display_thread_ids: true

runtime:
  n_cores: 0
  thread_name: "slim-data-plane"
  drain_timeout: 10s

services:
  slim/0:
    pubsub:
      servers:
        - endpoint: "0.0.0.0:46357"
          tls:
            insecure: true

      clients: []
EOF

docker run -it \
    -v ./config.yaml:/config.yaml -p 46357:46357 \
    ghcr.io/agntcy/slim:latest /slim --config /config.yaml
```

#### Using Cargo

```bash
cargo install agntcy-slim

cat << EOF > ./config.yaml
tracing:
  log_level: info
  display_thread_names: true
  display_thread_ids: true

runtime:
  n_cores: 0
  thread_name: "slim-data-plane"
  drain_timeout: 10s

services:
  slim/0:
    pubsub:
      servers:
        - endpoint: "0.0.0.0:46357"
          tls:
            insecure: true

      clients: []
EOF

~/.cargo/bin/slim --config ./config.yaml
```

#### Using Helm

We also provide a Helm chart for deploying SLIM in Kubernetes environments.

```bash
helm pull oci://ghcr.io/agntcy/slim/helm/slim --version v0.1.8
```

For information about how to use the Helm chart, see the
[values.yaml](https://github.com/agntcy/slim/blob/main/charts/slim/values.yaml)

### SLIM Controller

The SLIM Controller is responsible for managing SLIM Nodes and providing a
user-friendly interface for configuration. It can be installed using the
provided container image or with [Helm](https://helm.sh/).

### Using Docker

```bash
docker pull ghcr.io/agntcy/slim/controller:latest

cat << EOF > ./slim-controller.yaml
northbound:
  httpHost: localhost
  httpPort: 50051
  logging:
    level: DEBUG

southbound:
  httpHost: localhost
  httpPort: 50052
  logging:
    level: DEBUG
EOF

docker run -it \
    -v ./slim-controller.yaml:/config.yaml -p 50051:50051 -p 50052:50052 \
    ghcr.io/agntcy/slim/controller:latest -config /config.yaml
```

### Using Helm

```bash
helm pull oci://ghcr.io/agntcy/slim/helm/slim-controller --version v0.1.3
```

### SLIM Python Bindings

SLIM provides Python bindings for easy integration with Python applications. You
can install the bindings using pip, or you can include them into your app's
pyproject.toml:

```bash
pip install slim-bindings
```

```toml
[project]
...
dependencies = ["slim-bindings>=0.3.6"]
```

### Slimctl

`slimctl` is a command-line tool for managing SLIM Nodes and Controllers. It can
be installed downloaded from the [releases
page](https://github.com/agntcy/slim/releases/tag/slimctl-v0.1.4).

```bash
curl -LO https://github.com/agntcy/slim/releases/download/slimctl-v0.1.4/slimctl-linux-amd64
sudo mv slimctl-linux-amd64 /usr/local/bin/slimctl
```

## Build the code

To build the project and work with the code, you need the following installed
components in your system:

### Taskfile

Taskfile is required to run all the build operations. Follow the [installation
instructions](https://taskfile.dev/installation/) in the Taskfile documentation
to find the best installation method for your system.

<details>
  <summary>with brew</summary>

```bash
brew install go-task
```

</details>
<details>
  <summary>with curl</summary>

```bash
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin
```

</details>

For more information, see [Taskfile](https://taskfile.dev/).

### Rust

The data-plane components are implemented in Rust. Install with rustup:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

For more information, see [Rust](https://rustup.rs/).

### Go

The control-plane components are implemented in Go. Follow the installation
instructions in the Go website.
