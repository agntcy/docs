# Getting Started

The Agent Directory Service supports multiple deployment modes depending on
your use case. Choose the approach that best fits your environment and goals.

## Deployment Options

| Mode | Components | Best for |
|------|-----------|----------|
| [**dirctl daemon**](dir-deployment-local.md#dirctl-daemon-recommended-local-mode) | Single process (apiserver + reconciler + SQLite + local OCI store) | Quick local setup, single-user development, lightweight testing |
| [**Docker Compose**](dir-deployment-local.md#docker-compose-deployment) | Separate containers (apiserver, reconciler, Zot registry, PostgreSQL) | Multi-service local development, closer to production topology |
| [**Helm / Kubernetes**](dir-deployment-kubernetes.md) | Full Kubernetes deployment with SPIRE identity | Dev/staging clusters, team environments, pre-production |

### Start locally in seconds

The fastest way to get a Directory running is the built-in daemon, which
requires only the `dirctl` binary:

```bash
brew tap agntcy/dir https://github.com/agntcy/dir
brew install dirctl

dirctl daemon start
```

The daemon listens on `localhost:8888` with all state stored under
`~/.agntcy/dir/`. See [Local Deployment](dir-deployment-local.md) for the full
guide, platform support matrix, and configuration options.

### Deploy on Kubernetes

For team environments or when you need SPIFFE/SPIRE workload identity, deploy
Directory into a Kubernetes cluster using Helm or GitOps. See
[Kubernetes Deployment](dir-deployment-kubernetes.md) for the full walkthrough.

## Directory MCP Server

The Directory services are also accessible through the Directory MCP Server. It
provides a standardized interface for AI assistants and tools to interact with
the Directory system and work with OASF agent records. See the
[MCP Server documentation](directory-mcp.md) for more information.

## Next Steps

- Connect to the public Directory: federate with the public Directory network
  at `prod.api.ads.outshift.io` to discover and publish agents. See
  [Running a Federated Directory Instance](partner-prod-federation.md).
- Use the [Directory CLI](directory-cli.md) to create and query records.
- Explore [Features and Usage Scenarios](scenarios.md): build, store, sign,
  discover, search.
