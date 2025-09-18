# Getting Started

This guide will help you get started with the Directory project, including setting up your development environment, building the project, running tests, and deploying the services.

## Prerequisites

To build the project and work with the code, you need the following components installed in your system:

- [Taskfile](https://taskfile.dev/)
- [Docker](https://www.docker.com/)
- [Golang](https://go.dev/doc/devel/release#go1.24.0)

!!! note
    
    Make sure Docker is installed with Buildx.

## Quick Start

To quickly get started with the Directory project, you need two components:

- **Directory API Server**: The main service that manages agent directory records and handles API requests. Check [Deployment](#deployment) section for deployment options.
- **Directory Client**: A command-line or SDK tool to interact with the Directory API Server. Check [Artifacts distribution](#artifacts-distribution) section for installation instructions.

## Development

Use `Taskfile` for all related development operations such as testing, validating, deploying, and working with the project.

### Clone the repository

```bash
git clone https://github.com/agntcy/dir
cd dir
```

### Initialize the project

This step fetches all project dependencies and prepares the environment for development.

```bash
task deps
```

### Make changes

Make the changes to the source code and rebuild for later testing.

```bash
task build
```

### Test changes

The local testing pipeline relies on Golang to perform unit tests, and Docker to perform E2E tests in an isolated Kubernetes environment using Kind.

```bash
task test:unit
task test:e2e
```

## Artifacts distribution

All artifacts are tagged using the [Semantic Versioning](https://semver.org/) and follow the checked-out source code tags. It is not advised to use artifacts with mismatched versions.

### Container images

All container images are distributed via [GitHub Packages](https://github.com/orgs/agntcy/packages?repo_name=dir).

```bash
docker pull ghcr.io/agntcy/dir-ctl:v0.3.0
docker pull ghcr.io/agntcy/dir-apiserver:v0.3.0
```

### Helm charts

All helm charts are distributed as OCI artifacts via [GitHub Packages](https://github.com/agntcy/dir/pkgs/container/dir%2Fhelm-charts%2Fdir).

```bash
helm pull oci://ghcr.io/agntcy/dir/helm-charts/dir --version v0.3.0
```

### Binaries

All release binaries are distributed via [GitHub Releases](https://github.com/agntcy/dir/releases)
and [Homebrew](https://brew.sh/) `agntcy/dir` tap.

Check [CLI References](directory-cli.md) for detailed installation instructions.

### SDKs

- [**Golang**](directory-sdk.md#golang-sdk)
- [**Python**](directory-sdk.md#python-sdk)
- [**Javascript**](directory-sdk.md#javascript-sdk)

## Deployment

Directory API services can be deployed either using the `Taskfile` or directly via the released Helm chart.

### Using Taskfile

This starts the necessary components such as storage and API services.

```bash
task server:start
```

### Using Helm chart

This deploys Directory services into an existing Kubernetes cluster.

```bash
helm pull oci://ghcr.io/agntcy/dir/helm-charts/dir --version v0.3.0
helm upgrade --install dir oci://ghcr.io/agntcy/dir/helm-charts/dir --version v0.3.0
```

### Using Docker Compose

This deploys Directory services using Docker Compose:

```bash
cd install/docker
docker compose up -d
```
