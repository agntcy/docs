# Using the Agent Directory

The Agent Directory (dir) allows publication, exchange and discovery of information about AI agents over a distributed peer-to-peer network.

For detailed information in the Agent Directory Service, see the [Agent Directory Service documentation](../dir/overview.md).

## Prerequisites

To build the project and work with the code, you need the following components installed:

- [Taskfile](https://taskfile.dev/)
- [Docker](https://www.docker.com/)
- [Golang](https://go.dev/doc/devel/release#go1.24.0)

!!! note
    Make sure Docker is installed with Buildx.

## Development Workflow

Use `Taskfile` for all related development operations such as testing, validating, deploying, and working with the project.

### Clone the repository

```bash
git clone https://github.com/agntcy/dir
cd dir
```

### Initialize the project

This step will fetch all project dependencies and prepare the environment for development.

```bash
task deps
```

### Make changes

Make the changes to the source code and rebuild for later testing.

```bash
task build
```

### Test changes

The local testing pipeline relies on Golang to perform unit tests, and
Docker to perform E2E tests in an isolated Kubernetes environment using Kind.

```bash
task test:unit
task test:e2e
```

## Artifacts distribution

All artifacts are tagged using the [Semantic Versioning](https://semver.org/) and follow the checked out source code tags.
It is not advised to use artifacts with mismatching versions.

### Container images

All container images are distributed via [GitHub Packages](https://github.com/orgs/agntcy/packages?repo_name=dir).

```bash
docker pull ghcr.io/agntcy/dir-ctl:v0.2.0
docker pull ghcr.io/agntcy/dir-apiserver:v0.2.0
```

### Helm charts

All helm charts are distributed as OCI artifacts via [GitHub Packages](https://github.com/agntcy/dir/pkgs/container/dir%2Fhelm-charts%2Fdir).

```bash
helm pull oci://ghcr.io/agntcy/dir/helm-charts/dir --version v0.2.0
```

### Binaries

All release binaries are distributed via [GitHub Releases](https://github.com/agntcy/dir/releases).

### SDKs

- **Golang** - [github.com/agntcy/dir/api](https://pkg.go.dev/github.com/agntcy/dir/api), [github.com/agntcy/dir/cli](https://pkg.go.dev/github.com/agntcy/dir/cli), [github.com/agntcy/dir/server](https://pkg.go.dev/github.com/agntcy/dir/server)

## Deployment

Directory API services can be deployed either using the `Taskfile` or directly via released Helm chart.

### Using Taskfile

This will start the necessary components such as storage and API services.

```bash
task server:start
```

### Using Helm chart

This will deploy Directory services into an existing Kubernetes cluster.

```bash
helm pull oci://ghcr.io/agntcy/dir/helm-charts/dir --version v0.2.0
helm upgrade --install dir oci://ghcr.io/agntcy/dir/helm-charts/dir --version v0.2.0
```
