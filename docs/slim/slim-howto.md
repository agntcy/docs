# Getting Started with SLIM

SLIM is a secure, scalable, and user-friendly communication framework that
unifies state-of-the-art capabilities from all mentioned frameworks into a
single implementation.

For more information on SLIM, see the [detailed
documentation](./overview.md).

## Installation

SLIM is composed of multiple components, each with its own installation
instructions. Below are the main components and how to install them.

### SLIM Node

The SLIM Node is the core component that handles messaging operations. It can be
installed using the provided container image, with
[cargo](https://github.com/rust-lang/cargo) or with [Helm](https://helm.sh/).

#### Using Docker

```bash
docker pull ghcr.io/agntcy/slim:v0.7.0

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
    dataplane:
      servers:
        - endpoint: "0.0.0.0:46357"
          tls:
            insecure: true

      clients: []
EOF

docker run -it \
    -v ./config.yaml:/config.yaml -p 46357:46357 \
    ghcr.io/agntcy/slim:v0.7.0 /slim --config /config.yaml
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
    dataplane:
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
helm pull oci://ghcr.io/agntcy/slim/helm/slim --version v0.7.0
```

For information about how to use the Helm chart, see the
[values.yaml](https://github.com/agntcy/slim/blob/slim-v0.7.0/charts/slim/values.yaml)

### SLIM Controller

The SLIM Controller is responsible for managing SLIM Nodes and providing a
user-friendly interface for configuration. It can be installed using the
provided container image or with [Helm](https://helm.sh/).

### Using Docker

```bash
docker pull ghcr.io/agntcy/slim/control-plane:v0.7.0

cat << EOF > ./slim-control-plane.yaml
northbound:
  httpHost: 0.0.0.0
  httpPort: 50051
  logging:
    level: INFO

southbound:
  httpHost: 0.0.0.0
  httpPort: 50052
  logging:
    level: INFO

reconciler:
  maxRequeues: 15
  maxNumOfParallelReconciles: 1000

logging:
  level: INFO

database:
  filePath: /db/controlplane.db
EOF

docker run -it \
    -v ./slim-control-plane.yaml:/config.yaml -v .:/db \
    -p 50051:50051 -p 50052:50052                      \
    ghcr.io/agntcy/slim/control-plane:v0.7.0           \
    -config /config.yaml
```

### Using Helm

```bash
helm pull oci://ghcr.io/agntcy/slim/helm/slim-control-plane --version v0.7.0
```

### SLIM Bindings

#### Python

SLIM provides Python bindings for easy integration with Python applications. You
can install the bindings using pip, or you can include them into your app's
pyproject.toml:

```bash
pip install slim-bindings
```

```toml
[project]
...
dependencies = ["slim-bindings>=0.7.0"]
```

A tutorial on how to use the bindings in an application can be found in the [messaging layer
documentation](./slim-data-plane.md). Otherwise examples are available in the
[SLIM Repository](https://github.com/agntcy/slim/tree/slim-v0.7.0/data-plane/python/bindings/examples/src/slim_bindings_examples).

### Slimctl

`slimctl` is a command-line tool for managing SLIM Nodes and Controllers. It can
be downloaded from the [releases
page](https://github.com/agntcy/slim/releases/tag/slimctl-v0.7.0) in the SLIM repo.

#### Installation

Choose the appropriate installation method for your operating system:

=== "macOS (Apple Silicon)"

    ```bash
    curl -LO https://github.com/agntcy/slim/releases/download/slimctl-v0.7.0/slimctl_slimctl-v0.7.0-SNAPSHOT-35c37ab_darwin_arm64.tar.gz
    sudo mv slimctl-darwin-arm64 /usr/local/bin/slimctl
    sudo chmod +x /usr/local/bin/slimctl
    ```

    !!! note "macOS Security"
        You may need to allow the binary to run if it's blocked by Gatekeeper:

        ```bash
        sudo xattr -rd com.apple.quarantine /usr/local/bin/slimctl
        ```

        Alternatively, you can go to **System Settings > Privacy & Security** and allow the application to run when prompted.

=== "Linux (AMD64)"

    ```bash
    curl -LO https://github.com/agntcy/slim/releases/download/slimctl-v0.7.0/slimctl_slimctl-v0.7.0-SNAPSHOT-35c37ab_linux_amd64.tar.gz
    sudo mv slimctl-linux-amd64 /usr/local/bin/slimctl
    sudo chmod +x /usr/local/bin/slimctl
    ```

#### Verification

After installation, verify that `slimctl` is working correctly:

```bash
slimctl help
```

This should display the help information and available commands for `slimctl`.

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
