# Getting Started with SLIM

SLIM is a secure, scalable, and user-friendly communication framework that unifies state-of-the-art capabilities from all mentioned frameworks into a single implementation.

For more information on SLIM, see the [detailed documentation](../messaging/slim-core.md).

## Prerequisites

To build the project and work with the code, you need the following
installed components in your system:

### Taskfile

Taskfile is required to run all the build operations. Follow the
[installation instructions](https://taskfile.dev/installation/) in the Taskfile
documentation to find the best installation method for your system.

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

## Artifacts distribution

### Crates

For more information, see [crates.io](https://crates.io/users/artifacts-agntcy).

```bash
cargo install slim-gw
```

### Container Images

```bash
docker pull ghcr.io/agntcy/slim/gw:latest
```

### Helm Charts

```bash
helm pull ghcr.io/agntcy/slim/helm/slim:latest
```

### PyPI Packages

```bash
pip install slim-bindings
```