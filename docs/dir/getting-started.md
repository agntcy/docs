# Getting Started

Deploy Directory with SPIRE in a Kind cluster for development and testing. Uses `example.org` as the trust domain (local only—cannot federate with the public network).

**Prerequisites:** [Docker](https://www.docker.com/), [Kind](https://kind.sigs.k8s.io/), [kubectl](https://kubernetes.io/docs/tasks/tools/), [Helm](https://helm.sh/) 3.x

!!! note
    Ensure Docker has Buildx enabled.

---

## Helm install (recommended)

Deploy Directory using Helm only—no Argo CD. Uses the same charts and configuration patterns as [dir-staging](https://github.com/agntcy/dir-staging).

#### Step 1: Create Kind cluster

```bash
kind create cluster --name dir-dev
```

#### Step 2: Add Helm repositories

```bash
helm repo add spiffe https://spiffe.github.io/helm-charts-hardened
helm repo update
```

#### Step 3: Deploy SPIRE CRDs

```bash
helm install spire-crds spiffe/spire-crds \
  --version 0.5.0 \
  --namespace dir-dev-spire-crds \
  --create-namespace
```

#### Step 4: Deploy SPIRE server and agent

```bash
helm install spire spiffe/spire \
  --version 0.27.0 \
  --namespace dir-dev-spire \
  --create-namespace \
  --set global.spire.trustDomain=example.org \
  --set global.installAndUpgradeHooks.enabled=false \
  --set global.deleteHooks.enabled=false \
  --set spire-server.federation.enabled=true \
  --set spire-server.controllerManager.className=dir-spire
```

Wait for SPIRE to be ready:

```bash
kubectl wait --for=condition=ready pod -n dir-dev-spire -l app.kubernetes.io/name=server --timeout=240s
kubectl wait --for=condition=ready pod -n dir-dev-spire -l app.kubernetes.io/name=agent --timeout=240s
```

#### Step 5: Deploy Directory (API server, Zot, PostgreSQL)

The Directory chart includes the API server, Zot registry, and PostgreSQL. Pipe values from stdin using `-f -`:

```bash
helm install dir oci://ghcr.io/agntcy/dir/helm-charts/dir \
  --version v1.0.0 \
  --namespace dir-dev-dir \
  --create-namespace \
  -f - <<'EOF'
# Minimal values for Kind - based on dir-staging applications/dir/dev/values.yaml
# Release name: dir. Service names: dir-apiserver, dir-zot (chart.oci.registryAddress uses Release.Name-zot)
apiserver:
  image:
    repository: ghcr.io/agntcy/dir-apiserver
    tag: v1.0.0
    pullPolicy: IfNotPresent
  service:
    type: NodePort
  metrics:
    enabled: false
  routingService:
    type: NodePort
    nodePort: 30555
  spire:
    enabled: true
    className: dir-spire
    trustDomain: example.org
    useCSIDriver: true
  config:
    listen_address: "0.0.0.0:8888"
    oasf_api_validation:
      disable: true
    authn:
      enabled: true
      mode: "x509"
      socket_path: "unix:///run/spire/agent-sockets/api.sock"
      audiences:
        - "spiffe://example.org/spire/server"
    authz:
      enabled: true
      enforcer_policy_file_path: "/etc/agntcy/dir/authz_policies.csv"
    ratelimit:
      enabled: false
    store:
      provider: "oci"
      oci:
        registry_address: "dir-zot.dir-dev-dir.svc.cluster.local:5000"
        auth_config:
          insecure: "true"
          username: "admin"
          password: "admin"
    routing:
      listen_address: "/ip4/0.0.0.0/tcp/5555"
      datastore_dir: /etc/routing/datastore
      directory_api_address: "dir-apiserver.dir-dev-dir.svc.cluster.local:8888"
      gossipsub:
        enabled: false
    sync:
      auth_config:
        username: "user"
        password: "user"
    publication:
      scheduler_interval: "1h"
      worker_count: 0
      worker_timeout: "30m"
    database:
      type: "postgres"
      postgres:
        host: ""
        port: 5432
        database: "dir"
        ssl_mode: "disable"
  authz_policies_csv: |
    p,example.org,*
    p,*,/agntcy.dir.store.v1.StoreService/Pull
    p,*,/agntcy.dir.store.v1.StoreService/PullReferrer
    p,*,/agntcy.dir.store.v1.StoreService/Lookup
    p,*,/agntcy.dir.store.v1.SyncService/RequestRegistryCredentials
  secrets:
    ociAuth:
      username: "admin"
      password: "admin"
  reconciler:
    config:
      regsync:
        enabled: false
      indexer:
        enabled: false
  postgresql:
    enabled: true
    auth:
      username: "dir"
      password: "dir"
      database: "dir"
  strategy:
    type: Recreate
  extraVolumeMounts:
    - name: dir-routing-storage
      mountPath: /etc/routing
  extraVolumes:
    - name: dir-routing-storage
      emptyDir: {}
  zot:
    resources: {}
    mountSecret: true
    authHeader: "admin:admin"
    secretFiles:
      htpasswd: |-
        admin:$2y$05$vmiurPmJvHylk78HHFWuruFFVePlit9rZWGA/FbZfTEmNRneGJtha
        user:$2y$05$L86zqQDfH5y445dcMlwu6uHv.oXFgT6AiJCwpv3ehr7idc0rI3S2G
    mountConfig: true
    configFiles:
      config.json: |-
        {
          "distSpecVersion": "1.1.1",
          "storage": {"rootDirectory": "/var/lib/registry"},
          "http": {
            "address": "0.0.0.0",
            "port": "5000",
            "auth": {"htpasswd": {"path": "/secret/htpasswd"}},
            "accessControl": {
              "adminPolicy": {"users": ["admin"], "actions": ["read", "create", "update", "delete"]},
              "repositories": {"**": {"anonymousPolicy": [], "defaultPolicy": ["read"]}}
            }
          },
          "log": {"level": "info"},
          "extensions": {"search": {"enable": true}, "trust": {"enable": true, "cosign": true, "notation": false}}
        }
EOF
```

Wait for the API server to be ready:

```bash
kubectl wait --for=condition=ready pod -n dir-dev-dir -l app.kubernetes.io/name=apiserver --timeout=240s
```

#### Step 6: Port-forward and verify

```bash
kubectl port-forward svc/dir-apiserver -n dir-dev-dir 8888:8888
```

In another terminal, verify with token-based auth:

```bash
# Install dirctl (if needed)
brew tap agntcy/dir https://github.com/agntcy/dir
brew install dirctl

# Create SPIFFE SVID for local client
SPIRE_POD=$(kubectl get pods -n dir-dev-spire -l app.kubernetes.io/name=server -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n dir-dev-spire "$SPIRE_POD" -c spire-server -- \
  /opt/spire/bin/spire-server x509 mint \
  -dns dev.api.example.org \
  -spiffeID spiffe://example.org/local-client \
  -output json > spiffe-dev.json

# Configure and verify
export DIRECTORY_CLIENT_AUTH_MODE="token"
export DIRECTORY_CLIENT_SPIFFE_TOKEN="spiffe-dev.json"
export DIRECTORY_CLIENT_SERVER_ADDRESS="127.0.0.1:8888"
export DIRECTORY_CLIENT_TLS_SKIP_VERIFY="true"

dirctl info bafytest123
# Expected: Error: record not found (proves API is reachable)
```

**Push and pull a record:**

```bash
# Push via pipe
cat <<'EOF' | dirctl push --stdin --output raw
{"name":"burger_seller_agent","schema_version":"1.0.0","version":"1.0.0","description":"Helps with creating burger orders","authors":["Example Organization"],"created_at":"2025-01-01T00:00:00Z","skills":[{"name":"natural_language_processing/natural_language_understanding/contextual_comprehension","id":10101}],"locators":[{"type":"container_image","urls":["https://ghcr.io/agntcy/burger-seller-agent"]}],"modules":[{"name":"integration/mcp","data":{"name":"github-mcp-server","connections":[{"type":"stdio","command":"docker","args":["run","-i","--rm","-e","GITHUB_PERSONAL_ACCESS_TOKEN","ghcr.io/github/github-mcp-server"],"env_vars":[{"name":"GITHUB_PERSONAL_ACCESS_TOKEN","default_value":"","description":"Secret value for GITHUB_PERSONAL_ACCESS_TOKEN"}]}]}},{"name":"integration/a2a","data":{"card_data":{"protocolVersions":["0.2.6"],"name":"burger_seller_agent","description":"Helps with creating burger orders","supportedInterfaces":[{"url":"https://burger-agent-109790610330.us-central1.run.app","protocolBinding":"HTTP+JSON"}],"provider":{"url":"https://example.com","organization":"Example Organization"},"version":"1.0.0","capabilities":{"streaming":true},"defaultInputModes":["text","text/plain"],"defaultOutputModes":["text","text/plain"],"skills":[{"id":"create_burger_order","name":"Burger Order Creation Tool","description":"Helps with creating burger orders","tags":["burger order creation"],"examples":["I want to order 2 classic cheeseburgers"]}]},"card_schema_version":"v1.0.0"}}]}
EOF

# Pull by name (JSON output)
dirctl pull burger_seller_agent -o json
```

#### Step 7: Clean up

```bash
helm uninstall dir -n dir-dev-dir
helm uninstall spire -n dir-dev-spire
helm uninstall spire-crds -n dir-dev-spire-crds
kind delete cluster --name dir-dev
```

### Chart reference

| Component | Chart | Version |
|-----------|-------|---------|
| **SPIRE CRDs** | `spiffe/spire-crds` | 0.5.0 |
| **SPIRE** | `spiffe/spire` | 0.27.0 |
| **Directory** | `oci://ghcr.io/agntcy/dir/helm-charts/dir` | v1.0.0 |

Full configuration examples: [dir-staging applications](https://github.com/agntcy/dir-staging/tree/main/applications).

---

## Alternative: GitOps / Argo CD

For teams already using Argo CD, Directory can be deployed from a GitOps repository. [dir-staging](https://github.com/agntcy/dir-staging) is an example you can fork or clone to maintain your own GitOps repo.

1. Create a Kind cluster and install Argo CD.
2. Apply the dir-staging project and application manifests (or your forked repo).
3. Argo CD syncs SPIRE CRDs, SPIRE, and Directory from the repo.

```bash
kind create cluster --name dir-dev
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl wait --namespace argocd --for=condition=available deployment --all --timeout=120s

kubectl apply -f https://raw.githubusercontent.com/agntcy/dir-staging/main/projects/dir/dev/dir-dev.yaml
kubectl apply -f https://raw.githubusercontent.com/agntcy/dir-staging/main/projectapps/dir/dev/dir-dev-projectapp.yaml

kubectl wait --for=condition=ready pod -n dir-dev-spire -l app.kubernetes.io/name=server --timeout=240s
kubectl wait --for=condition=ready pod -n dir-dev-spire -l app.kubernetes.io/name=agent --timeout=240s
kubectl wait --for=condition=ready pod -n dir-dev-dir -l app.kubernetes.io/name=apiserver --timeout=240s
```

Port-forward: `kubectl port-forward svc/dir-dir-dev-argoapp-apiserver -n dir-dev-dir 8888:8888`

See [dir-staging](https://github.com/agntcy/dir-staging) for full configuration and customization options.

!!! important "Trust domain"
    This Quick Start uses `example.org` for local testing only. To federate with the public Directory network, you need a unique trust domain. See [Production Deployment](deployment.md) and [Connect to the Public Directory](federation.md).

---

## For Developers

To build and develop the Directory project from source:

### Prerequisites

- [Taskfile](https://taskfile.dev/)
- [Docker](https://www.docker.com/)
- [Golang](https://go.dev/doc/devel/release#go1.24.0)

### Clone and build

```bash
git clone https://github.com/agntcy/dir
cd dir
task deps
task build
```

### Run tests

```bash
task test:unit
task test:e2e
```

### Deploy for development

Directory can be run via Taskfile, Helm, or Docker Compose:

| Method | Command |
|--------|---------|
| **Taskfile** | `DIRECTORY_SERVER_OASF_API_VALIDATION_SCHEMA_URL=https://schema.oasf.outshift.com task server:start` |
| **Helm** | `helm upgrade --install dir oci://ghcr.io/agntcy/dir/helm-charts/dir --version v1.0.0` |
| **Docker Compose** | `cd install/docker && docker compose up -d` |

For configuration options, see [Validation](validation.md).

```bash
docker pull ghcr.io/agntcy/dir-ctl:v1.0.0
docker pull ghcr.io/agntcy/dir-apiserver:v1.0.0
```

- **Container images:** [GitHub Packages](https://github.com/orgs/agntcy/packages?repo_name=dir)
- **Helm charts:** `oci://ghcr.io/agntcy/dir/helm-charts/dir`
- **CLI:** [directory-cli.md](directory-cli.md)
- **SDKs:** [directory-sdk.md](directory-sdk.md) (Go, Python, JavaScript)

All helm charts are distributed as OCI artifacts via [GitHub Packages](https://github.com/agntcy/dir/pkgs/container/dir%2Fhelm-charts%2Fdir).

```bash
helm pull oci://ghcr.io/agntcy/dir/helm-charts/dir --version v1.0.0
```

### Binaries

All release binaries are distributed via [GitHub Releases](https://github.com/agntcy/dir/releases)
and [Homebrew](https://brew.sh/) `agntcy/dir` tap.

Check [CLI References](directory-cli.md) for detailed installation instructions.

### SDKs

- [**Golang**](directory-sdk.md#golang-sdk)
- [**Python**](directory-sdk.md#python-sdk)
- [**Javascript**](directory-sdk.md#javascript-sdk)

## Directory MCP Server

The Directory services are also accessible through the Directory MCP Server. It provides a standardized interface for AI assistants and tools to interact with the Directory system and work with OASF agent records. See the [Directory CLI Reference](directory-cli.md#directory-mcp-server) for more information.

## Deployment

Directory API services can be deployed either using the `Taskfile` or directly via the released Helm chart.

### Using Taskfile

This starts the necessary components such as storage and API services.

```bash
DIRECTORY_SERVER_OASF_API_VALIDATION_SCHEMA_URL=https://schema.oasf.outshift.com task server:start
```

!!! note

    MacOS users may encounter a "port 5000 already in use" error. This is likely caused by the AirPlay Receiver feature. You can disable it in your System Settings.

### Using Helm chart

This deploys Directory services into an existing Kubernetes cluster.

```bash
helm pull oci://ghcr.io/agntcy/dir/helm-charts/dir --version v1.0.0
helm upgrade --install dir oci://ghcr.io/agntcy/dir/helm-charts/dir --version v1.0.0
```

Alternatively, you can configure the OASF schema URL explicitly:

```bash
helm upgrade --install dir oci://ghcr.io/agntcy/dir/helm-charts/dir --version v1.0.0 \
  --set apiserver.config.oasf_api_validation.schema_url=https://schema.oasf.outshift.com
```

Or create a `values.yaml` file:

```yaml
apiserver:
  config:
    oasf_api_validation:
      schema_url: "https://schema.oasf.outshift.com"
```

Then deploy:

```bash
helm upgrade --install dir oci://ghcr.io/agntcy/dir/helm-charts/dir --version v1.0.0 -f values.yaml
```

For more configuration options, see the [Validation](validation.md) documentation.

### Using Docker Compose

This deploys Directory services using Docker Compose.
  
 While the Directory server has a default OASF schema URL, Docker Compose deployments may require explicitly setting the `DIRECTORY_SERVER_OASF_API_VALIDATION_SCHEMA_URL` environment variable:

```bash
cd install/docker
export DIRECTORY_SERVER_OASF_API_VALIDATION_SCHEMA_URL=https://schema.oasf.outshift.com
docker compose up -d
```

Alternatively, you can disable API validation (not recommended for production):

```bash
cd install/docker
export DIRECTORY_SERVER_OASF_API_VALIDATION_DISABLE=true
docker compose up -d
```

For more configuration options, see the [Validation](validation.md) documentation.

## Next Steps

- **Connect to the public Directory** — Federate with `prod.api.ads.outshift.io` to discover and publish agents. See [Connect to the Public Directory](federation.md).
- Use the [Directory CLI](directory-cli.md) to create and query records.
- Explore [Features and Usage Scenarios](scenarios.md): build, store, sign, discover, search.
