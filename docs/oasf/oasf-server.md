# Open Agentic Schema Framework Server

The server/directory contains the Open Agents Schema Framework (OASF) Schema Server source code.
The schema server is an HTTP server that provides a convenient way to browse and use the OASF schema.
The server provides also schema validation capabilities to be used during development.

You can access the OASF schema server, which is running the latest released schema, at [schema.oasf.agntcy.org](https://schema.oasf.agntcy.org).

The schema server can also be used locally.

## Prerequisites

- [Taskfile](https://taskfile.dev/)
- [Docker](https://www.docker.com/)

Make sure Docker is installed with Buildx.

## Development

Use `Taskfile` for all related development operations such as testing, validating, deploying, and working with the project.

### Clone the repository

```shell
git clone https://github.com/agntcy/oasf.git
```

### Build artifacts

This step fetches all project dependencies and
subsequently build all project artifacts such as
Helm charts and Docker images.

```shell
task deps
task build
```

### Deploy locally

This step creates an ephemeral Kind cluster
and deploy OASF services through Helm chart.
It also sets up port forwarding
so that the services can be accessed locally.

```shell
task up
```

To access the schema server, open [`localhost:8080`](http://localhost:8080) in your browser.

**Note**: Any changes made to the schema or server backend itself requires running `task up` again.

### Hot reload

In order to run the server in hot-reload mode, you must first deploy
the services, and run another command to signal that the schema will be actively updated.

This can be achieved by starting an interactive reload session through:

```shell
task reload
```

Note that this only performs hot-reload for schema changes.
Reloading backend changes still requires re-running `task build && task up`.

### Cleanup

This step handles cleanup procedure by
removing resources from previous steps,
including ephemeral Kind clusters and Docker containers.

```shell
task down
```

## Artifacts distribution

For more information, see https://github.com/orgs/agntcy/packages?repo_name=oasf.
