# Getting Started


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

### [Golang]

The control-plane components are implemented in golang. Follow the installation
instructions in the golang website.

## Artifacts distribution

### [Crates]

See https://crates.io/users/artifacts-agntcy

```bash
cargo install agp-gw
```

### [Container images]

```bash
docker pull ghcr.io/agntcy/agp/gw:latest
```

### [Helm charts]

```bash
helm pull ghcr.io/agntcy/agp/helm/agp:latest
```

### [Pypi packages]

```bash
pip install agp-bindings
```
