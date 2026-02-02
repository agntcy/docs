# Getting Started with SLIM

!!! info "What is SLIM?"
    SLIM is a secure, scalable, and user-friendly communication framework that unifies state-of-the-art capabilities from all mentioned frameworks into a single implementation.
    
    📚 For more information, see the [detailed documentation](./overview.md).

---

## Installation

SLIM is composed of multiple components, each with its own installation instructions. Choose the components you need based on your use case.

---

### :material-server: SLIM Node

The SLIM Node is the core component that handles messaging operations.

!!! tip "Installation Methods"
    You can install the SLIM Node using Docker, Cargo, Helm, or the CLI binary. Choose the method that best fits your infrastructure.

=== "Docker"

    Pull the SLIM container image and run it with a configuration file:

    ```bash
    docker pull ghcr.io/agntcy/slim:1.0.0
    ```

    Create a configuration file:

    ```yaml
    # config.yaml
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
    ```

    Run the container:

    ```bash
    docker run -it \
        -v ./config.yaml:/config.yaml -p 46357:46357 \
        ghcr.io/agntcy/slim:1.0.0 /slim --config /config.yaml
    ```

=== "Cargo"

    Install SLIM using Rust's package manager:

    ```bash
    cargo install agntcy-slim
    ```

    Create a configuration file:

    ```yaml
    # config.yaml
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
    ```

    Run SLIM:

    ```bash
    ~/.cargo/bin/slim --config ./config.yaml
    ```

=== "Helm"

    For Kubernetes deployments, use the official Helm chart:

    ```bash
    helm pull oci://ghcr.io/agntcy/slim/helm/slim --version v1.0.0
    ```

    !!! note "Configuration"
        For detailed configuration options, see the [values.yaml](https://github.com/agntcy/slim/blob/slim-v1.0.0/charts/slim/values.yaml) in the repository.

=== "CLI Binary"

    For local development and testing, use the `slimctl` binary.

    !!! info "Installation"
        Install the slimctl binary following the [instructions below](#slimctl).

    === "Default Configuration"

        Run with default settings:

        ```bash
        slimctl slim start
        ```

    === "Custom Configuration"

        Create a configuration file:

        ```yaml
        # config.yaml
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
        ```

        Start SLIM with the configuration:

        ```bash
        slimctl slim start --config ./config.yaml
        ```


!!! tip "Advanced Usage"
    For more configuration options, see the [SLIM Configuration reference](./slim-data-plane-config.md)

---

### :material-console: SLIM Controller

The SLIM Controller manages SLIM Nodes and provides a user-friendly interface for configuration.

=== "Docker"

    Pull the controller image:

    ```bash
    docker pull ghcr.io/agntcy/slim/control-plane:1.0.0
    ```

    Create a configuration file:

    ```yaml
    # slim-control-plane.yaml
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
    ```

    Run the controller:

    ```bash
    docker run -it \
        -v ./slim-control-plane.yaml:/config.yaml -v .:/db \
        -p 50051:50051 -p 50052:50052                      \
        ghcr.io/agntcy/slim/control-plane:1.0.0           \
        -config /config.yaml
    ```

=== "Helm"

    For Kubernetes deployments:

    ```bash
    helm pull oci://ghcr.io/agntcy/slim/helm/slim-control-plane --version v1.0.0
    ```

---

### :material-code-braces: SLIM Bindings

Language bindings allow you to integrate SLIM with your applications.

=== "Python"

    Install using pip:

    ```bash
    pip install slim-bindings
    ```

    Or add to your `pyproject.toml`:

    ```toml
    [project]
    # ...
    dependencies = ["slim-bindings~=1.0"]
    ```

    !!! example "Learn More"
        - 📖 [Messaging Layer Tutorial](./slim-data-plane.md)
        - 💻 [Python Examples](https://github.com/agntcy/slim/tree/slim-v1.0.0/data-plane/bindings/python/examples)

=== "Go"

    Install the Go bindings:

    ```bash
    go get github.com/agntcy/slim-bindings-go@v1.0.0
    ```

    Run the setup tool to install native libraries:

    ```bash
    go run github.com/agntcy/slim-bindings-go/cmd/slim-bindings-setup
    ```

    Add to your `go.mod`:

    ```go
    require github.com/agntcy/slim-bindings-go v1.0.0
    ```

    !!! warning "C Compiler Required"
        The Go bindings use native libraries via [CGO](https://pkg.go.dev/cmd/cgo), so you'll need a C compiler installed on your system.

    !!! example "Examples"
        Check out the [Go examples](https://github.com/agntcy/slim/tree/slim-v1.0.0/data-plane/bindings/go/examples) in the repository.

---

### :material-hammer-wrench: Slimctl

`slimctl` is a command-line tool for managing SLIM Nodes and Controllers.

#### Installation

Choose your platform:

=== "macOS (Apple Silicon)"

    ```bash
    curl -LO https://github.com/agntcy/slim/releases/download/slimctl-v1.0.0/slimctl_1.0.0_darwin_arm64.tar.gz
    tar -xzf slimctl_1.0.0_darwin_arm64.tar.gz
    sudo mv slimctl /usr/local/bin/slimctl
    sudo chmod +x /usr/local/bin/slimctl
    ```

    !!! warning "macOS Security"
        You may need to allow the binary to run if blocked by Gatekeeper:

        ```bash
        sudo xattr -rd com.apple.quarantine /usr/local/bin/slimctl
        ```

        Alternatively, go to **System Settings > Privacy & Security** and allow the application when prompted.

=== "macOS (Intel)"

    ```bash
    curl -LO https://github.com/agntcy/slim/releases/download/slimctl-v1.0.0/slimctl_1.0.0_darwin_amd64.tar.gz
    tar -xzf slimctl_1.0.0_darwin_amd64.tar.gz
    sudo mv slimctl /usr/local/bin/slimctl
    sudo chmod +x /usr/local/bin/slimctl
    ```

=== "Linux (AMD64)"

    ```bash
    curl -LO https://github.com/agntcy/slim/releases/download/slimctl-v1.0.0/slimctl_1.0.0_linux_amd64.tar.gz
    tar -xzf slimctl_1.0.0_linux_amd64.tar.gz
    sudo mv slimctl /usr/local/bin/slimctl
    sudo chmod +x /usr/local/bin/slimctl
    ```

=== "Windows (AMD64)"

    Download and extract the Windows binary:

    ```powershell
    # Using PowerShell
    Invoke-WebRequest -Uri "https://github.com/agntcy/slim/releases/download/slimctl-v1.0.0/slimctl_1.0.0_windows_amd64.zip" -OutFile "slimctl.zip"
    Expand-Archive -Path "slimctl.zip" -DestinationPath "."
    
    # Move to a directory in your PATH (e.g., C:\Program Files\slimctl\)
    # Or add the current directory to your PATH
    ```

    Alternatively, download directly from the [releases page](https://github.com/agntcy/slim/releases/download/slimctl-v1.0.0/slimctl_1.0.0_windows_amd64.zip).

!!! tip "Other Installation Methods"
    Check the [slimctl documentation](https://github.com/agntcy/slim/tree/slim-v1.0.0/control-plane/slimctl/README.md) for additional installation methods.

#### Verification

Verify the installation:

```bash
slimctl help
```

This should display help information and available commands.

---

## :material-wrench: Building from Source

To build SLIM from source, you'll need the following tools installed.

### Prerequisites

#### Taskfile

Taskfile is required for running build operations.

=== "Homebrew"

    ```bash
    brew install go-task
    ```

=== "curl"

    ```bash
    sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin
    ```

=== "Other Methods"

    See the [Taskfile installation guide](https://taskfile.dev/installation/) for more options.

#### Rust

The data-plane components are written in Rust:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

!!! info
    Learn more at [rustup.rs](https://rustup.rs/)

#### Go

The control-plane components are written in Go. Follow the [official installation guide](https://go.dev/doc/install).

---

## :material-rocket: Next Steps

!!! success "Ready to Go!"
    You've installed SLIM! Here's what to do next:

    1. :material-book-open-page-variant: Read the [messaging layer documentation](./slim-data-plane.md)
    2. :material-code-tags: Explore the [example applications](https://github.com/agntcy/slim/tree/slim-v1.0.0/data-plane/bindings/)
    3. :material-cog: Learn about [configuration options](./overview.md)
    4. :material-forum: Join the community and ask questions

---

## :material-help-circle: Need Help?

!!! question "Getting Stuck?"
    - 📖 Check the [detailed documentation](./overview.md)
    - 💬 Ask questions in our community forums
    - 🐛 Report issues on [GitHub](https://github.com/agntcy/slim)
