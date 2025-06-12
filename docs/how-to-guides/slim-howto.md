# Getting Started with SLIM

Secure Low-Latency Interactive Messaging (SLIM) aims to provide a secure, scalable, and user-friendly communication framework that unifies state-of-the-art capabilities from all mentioned frameworks into a single implementation.

For more information on SLIM, see the [detailed documentation](../tools/slim-core.md).

## Prerequisites

To build the project and work with the code, you need the following
installed components in your system:

### Taskfile

Taskfile is required to run all the build operations. Follow the
[installation instructions](https://taskfile.dev/installation/) in the Taskfile
documentations to find the best installation method for your system.

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

The data-plane components are implemented in rust. Install with rustup:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

For more information, see [Rust](https://rustup.rs/).

### Golang

The control-plane components are implemented in Golang. Follow the installation
instructions in the golang website.

## Artifacts distribution

### Crates

For more information, see (https://crates.io/users/artifacts-agntcy).

```bash
cargo install agp-gw
```

### Container Images

```bash
docker pull ghcr.io/agntcy/agp/gw:latest
```

### Helm Charts

```bash
helm pull ghcr.io/agntcy/agp/helm/agp:latest
```

### Pypi Packages

```bash
pip install agp-bindings
```