# Open Agentic Schema Framework Server

The `server/` directory contains the Open Agentic Schema Framework (OASF) Schema
Server source code.
The schema server is an HTTP server that provides a convenient way to browse and
use the OASF schema.
The server provides also schema validation capabilities to be used during
development.

You can access the OASF schema server, which is running the latest released
schema, at [schema.oasf.outshift.com](https://schema.oasf.outshift.com).

The schema server can also be used locally.

## Development

Use `Taskfile` for all related development operations such as testing,
validating, deploying, and working with the project.

Check the
[example.env](https://github.com/agntcy/oasf/blob/main/server/.env.sample) to
see the configuration for the operations below.

### Prerequisites

- [Taskfile](https://taskfile.dev/)
- [Docker](https://www.docker.com/)
- [Go](https://go.dev/)
- [yq](https://github.com/mikefarah/yq)
- [curl](https://curl.se/)
- [tar](https://www.gnu.org/software/tar/)

Make sure Docker is installed with Buildx.

### Clone the Repository

```shell
git clone https://github.com/agntcy/oasf.git
```

### Build Artifacts

This step will fetch all project dependencies and subsequently build all project
artifacts such as helm charts and Docker images.

```shell
task deps
task build
```

### Deploy Locally

This step will create an ephemeral Kind cluster and deploy OASF services via
Helm chart.
It also sets up port forwarding so that the services can be accessed locally.

```shell
IMAGE_TAG=latest task build:images
task up
```

To access the schema server, open [`localhost:8080`](http://localhost:8080) in
your browser.

**Note:** Any changes made to the server backend itself will require running
`task up` again.

To set your own local OASF server using Elixir tooling, follow
[these instructions](https://github.com/agntcy/oasf/blob/main/server/README.md).

### Hot Reload

In order to run the server in hot-reload mode, you must first deploy the
services, and run another command to signal that the schema will be actively
updated.

This can be achieved by starting an interactive reload session via:

```shell
task reload
```

**Note:** This will only perform hot-reload for schema changes.
Reloading backend changes still requires re-running `task build && task up`.

### Deploy Locally with Multiple Versions

Trying out OASF locally with multiple versions is also possible, with updating
the `install/charts/oasf/values-test-versions.yaml` file with the required
versions and deploying OASF services on the ephemeral Kind cluster with those
values.

```
HELM_VALUES_PATH=./install/charts/oasf/values-test-versions.yaml task up
```

### Cleanup

This step will handle cleanup procedure by removing resources from previous
steps, including ephemeral Kind clusters and Docker containers.

```shell
task down
```

## Distribution

### Artifacts

See
[AGNTCY Github Registry](https://github.com/orgs/agntcy/packages?repo_name=oasf).

### Protocol Buffer Definitions

The `proto` directory contains the Protocol Buffer (`.proto`) files defining our
data objects and APIs.
The full proto module, generated language stubs and it's versions are hosted at
the Buf Schema Registry:
[https://buf.build/agntcy/oasf](https://buf.build/agntcy/oasf)
