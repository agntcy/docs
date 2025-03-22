# Core Concepts

Agentic applications

<<<<<<< HEAD
=======
 **Security**: Employs authentication, authorization, and end-to-end encryption to protect data privacy and integrity.

## Source tree

Main software components:

- [data-plane](./data-plane): client and cloud components for efficient message
  forwarding among agents
- [control-plane](./control-plane): cloud services to manage control-plane ops
  carried out by agents

## Prerequisites

To build the project and work with the code, you will need the following
installed in your system:

### [Taskfile](https://taskfile.dev/)

Taskfile is required to run all the build operations. Follow the
[installation](https://taskfile.dev/installation/) instructions in the Taskfile
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


### [Rust](https://rustup.rs/)

The data-plane components are implemented in rust. Install with rustup:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### [Golang](https://go.dev/doc/install)

The control-plane components are implemented in golang. Follow the installation
instructions in the golang website.

## Artifacts distribution

### [Crates](./data-plane/gateway)

See https://crates.io/users/artifacts-agntcy

```bash
cargo install agp-gw
```

### [Container images](./data-plane/Dockerfile)

```bash
docker pull ghcr.io/agntcy/agp/gw:latest
```

### [Helm charts](./deploy/charts/agp)

```bash
helm pull ghcr.io/agntcy/agp/helm/agp:latest
```

### [Pypi packages](./data-plane/python-bindings)

```bash
pip install agp-bindings
```
>>>>>>> 6f254564eaf1ce71d7fb21be2a4b204121fd19c7
