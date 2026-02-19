# Testbed Deployment

The [dir-staging](https://github.com/agntcy/dir-staging) repository contains the deployment manifests for AGNTCY Directory project. It is designed to be used with Argo CD for GitOps-style continuous deployment.

The manifests are organized into two main sections:

- `projects/`: Contains Argo CD project definitions.
- `projectapps/`: Contains Argo CD application definitions.

The project will deploy the following components:

- `applications/dir` - AGNTCY Directory server with storage backend (v1.0.0).
- `applications/dir-admin` - AGNTCY Directory Admin CLI client (v1.0.0).
- `applications/spire*` - SPIRE stack for identity and federation.

!!! note
    This is not a production-ready deployment. It is provided as-is for demonstration and testing purposes.

## Onboarding

To onboard a new environment to Directory Public Staging Network, see the [onboarding guide](./directory-public-staging.md).

## Quick Starting a Development Environment

This guide sets up the development environment for local testing and development. It uses a local Kind cluster with NodePort services and simplified security. For production deployment with Ingress and TLS, see the [Production Setup](#production-setup) section below.

This guide demonstrates how to set up AGNTCY Directory project using Argo CD in Kubernetes [Kind](https://kind.sigs.k8s.io/) cluster.

1. Create Kind cluster

    ```bash
    kind create cluster --name dir-dev
    ```

2. Install Argo CD in the cluster.

    ```bash
    # Install Argo CD
    kubectl create namespace argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

    # Wait for Argo CD to be ready
    kubectl wait --namespace argocd --for=condition=available deployment --all --timeout=120s
    ```

3. Deploy Directory via Argo CD.

    ```bash
    # Add project
    kubectl apply -f https://raw.githubusercontent.com/agntcy/dir-staging/main/projects/dir/dev/dir-dev.yaml

    # Add application
    kubectl apply -f https://raw.githubusercontent.com/agntcy/dir-staging/main/projectapps/dir/dev/dir-dev-projectapp.yaml
    ```

4. Check results in Argo CD UI.

    ```bash
    # Retrieve password
    kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d; echo

    # Port forward the Argo CD API to localhost:8080
    kubectl port-forward svc/argocd-server -n argocd 8080:443
    ```

    Login to the UI at [https://localhost:8080](https://localhost:8080) with username `admin` and the password retrieved above.

    Verify deployment by checking the results of CronJobs in `dir-admin` application.

5. Clean up.

    ```bash
    kind delete cluster --name dir-dev
    ```

### Token-based Directory Client Authentication for Development Environment

In some cases, you may want to use Directory Client locally without SPIRE stack. In this case, you can use token-based authentication using SPIFFE X509 SVID tokens.

To generate a SPIFFE SVID token for authenticating local Directory Client with the Directory Server in the dev environment, follow the steps below:

1. Create a SPIFFE SVID for local Directory Client.

    ```bash
    kubectl exec spire-dir-dev-argoapp-server-0 -n dir-dev-spire -c spire-server -- \
    /opt/spire/bin/spire-server x509 mint \
    -dns dev.api.example.org \
    -spiffeID spiffe://example.org/local-client \
    -output json > spiffe-dev.json
    ```

2. Set SPIFFE Token variable for Directory Client.

    ```bash
    # Set authentication method to token
    export DIRECTORY_CLIENT_AUTH_MODE="token"
    export DIRECTORY_CLIENT_SPIFFE_TOKEN="spiffe-dev.json"

    # Set Directory Server address and skip TLS verification
    export DIRECTORY_CLIENT_SERVER_ADDRESS="127.0.0.1:8888"
    export DIRECTORY_CLIENT_TLS_SKIP_VERIFY="true"
    ```

3. Port-forward Directory Server API.

    ```bash
    kubectl port-forward svc/dir-dir-dev-argoapp-apiserver -n dir-dev-dir 8888:8888
    ```

4. Run Directory Client.

    ```bash
    dirctl info baeareiesad3lyuacjirp6gxudrzheltwbodtsg7ieqpox36w5j637rchwq
    ```

## Production Deployment

This example configuration uses simplified settings for local Kind/Minikube testing.
For production deployment, consider these enhancements:

| Feature | Kind/Minikube Deployment | Production Deployment |
|---------|---------------------|------------|
| **SPIFFE CSI Driver** | ✅ Enabled (v0.5.5+) | ✅ Enabled |
| **Storage** | emptyDir (ephemeral) | PVCs (persistent) |
| **Deployment Strategy** | Recreate (default) | Recreate (required with PVCs) |
| **Credentials** | Hardcoded in values.yaml | ExternalSecrets + Vault |
| **Resources** | 250m/512Mi | 500m-2000m / 1-4Gi |
| **Ingress** | NodePort (local) | Ingress + TLS |
| **Rate Limits** | 50 RPS | 500+ RPS |
| **Trust Domain** | example.org | your-domain.com |
| **Read-Only FS** | No (emptyDir) | Yes (with PVCs) |

!!! note
    This configuration is optimized for local testing. For production, enable the optional features documented below.

### Key Production Features

**SPIFFE CSI Driver** (v0.5.5+):

- Enabled by default via `spire.useCSIDriver: true`.
- Provides synchronous workload identity injection.
- Eliminates authentication race conditions ("certificate contains no URI SAN" errors).
- More secure than hostPath mounts in workload containers.

**Persistent Storage**:

- Enable PVCs for routing datastore and database (v0.5.2+).
- Prevents data loss across pod restarts.
- See `pvc.create` and `database.pvc.enabled` in values.yaml.

    !!! warning
        When using PVCs, set `strategy.type: Recreate` to prevent database lock conflicts.

**Secure Credential Management**:

- Use ExternalSecrets Operator with Vault instead of hardcoded secrets.
- See commented ExternalSecrets configuration in values.yaml.

**Resource Sizing**:

- Increase limits based on expected load (CPU: 500m-2000m, Memory: 1-4Gi).
- Monitor and adjust after observing production traffic.

**Ingress & TLS**:

- Configure Ingress for external access.
- Use cert-manager with Let's Encrypt for production certificates.
- Enable SSL passthrough for DIR API (SPIFFE mTLS).

### Minikube Production Simulation

If you wish to test production-like setup locally with Ingress and TLS, follow the steps below using Minikube.

!!! note
    We are using Minikube to simulate production setup, as it supports Ingress and TLS out of the box. Steps below marked as (local) are optional and intended for local testing purposes only.

!!! warning
    It is not recommended to deploy both dev and prod environments in the same cluster, as they may conflict with each other.

### Production Setup

1. Create Minikube cluster.

    ```bash
    minikube start -p dir-prod
    ```

2. (local) Enable Ingress and DNS addons in Minikube.

    The deployment uses `*.test` domain for Ingress resources. 

    For local testing purposes, Minikube Ingress controller is required to route traffic to our Ingress resources.

    Otherwise, if you are deploying to a cloud provider with its own Ingress controller,
    make sure that it supports SSL Passthrough.

    ```bash
    # Enable Ingress and Ingress-DNS addons
    minikube addons enable ingress -p dir-prod
    minikube addons enable ingress-dns -p dir-prod

    # Patch Ingress controller to enable SSL Passthrough
    kubectl patch deployment -n ingress-nginx ingress-nginx-controller --type='json' \
    -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value":"--enable-ssl-passthrough"}]'
    ```

3. (local) Enable Local DNS inside Minikube.

    The deployment uses `*.test` domain for Ingress resources. 

    For local testing purposes, we need to configure DNS resolution
    inside Minikube cluster to resolve `*.test` domain to Minikube IP address
    using [minikube/ingress-dns](https://minikube.sigs.k8s.io/docs/handbook/addons/ingress-dns) guide.

    Otherwise, if you are deploying to a cloud provider with its own Ingress controller,
    you can skip this step.

    ```bash
    # Get Minikube IP
    minikube ip -p dir-prod

    # Add DNS resolver entry for `*.test` domain
    # Follow guide at: https://minikube.sigs.k8s.io/docs/handbook/addons/ingress-dns

    # Update CoreDNS ConfigMap to forward `test` domain to Minikube IP
    kubectl edit configmap coredns -n kube-system
    ```

4. (local) Install [cert-manager](https://cert-manager.io) with Self-Signed Issuer.

    The deployment uses cert-manager `letsencrypt` issuer to issue TLS certificates for Ingress resources.

    For local testing purposes, we will create a self-signed root CA certificate
    and configure cert-manager to use it as `letsencrypt` issuer.

    Otherwise, if you are deploying to a cloud provider with its own cert-manager,
    you can skip this step, but ensure that `letsencrypt` issuer is available.

    ```bash
    # Install cert-manager
    kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.19.1/cert-manager.yaml

    # Wait for cert-manager to be ready
    kubectl wait --namespace cert-manager --for=condition=available deployment --all --timeout=120s

    # Create Self-Signed Issuer and Root CA Certificate
    kubectl apply -f - <<EOF
    apiVersion: cert-manager.io/v1
    kind: ClusterIssuer
    metadata:
      name: selfsigned-issuer
    spec:
      selfSigned: {}
    ---
    apiVersion: cert-manager.io/v1
    kind: Certificate
    metadata:
      name: my-selfsigned-ca
      namespace: cert-manager
    spec:
      isCA: true
      commonName: my-selfsigned-ca
      secretName: root-secret
      privateKey:
        algorithm: ECDSA
        size: 256
      issuerRef:
        name: selfsigned-issuer
        kind: ClusterIssuer
        group: cert-manager.io
    ---
    apiVersion: cert-manager.io/v1
    kind: ClusterIssuer
    metadata:
      name: letsencrypt
    spec:
      ca:
        secretName: root-secret
    EOF
    ```

5. Install Argo CD in the cluster.

    ```bash
    # Install Argo CD
    kubectl create namespace argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

    # Wait for Argo CD to be ready
    kubectl wait --namespace argocd --for=condition=available deployment --all --timeout=120s
    ```

6. Deploy Directory via Argo CD.

    ```bash
    # Add project
    kubectl apply -f https://raw.githubusercontent.com/agntcy/dir-staging/main/projects/dir/prod/dir-prod.yaml

    # Add application
    kubectl apply -f https://raw.githubusercontent.com/agntcy/dir-staging/main/projectapps/dir/prod/dir-prod-projectapp.yaml
    ```

7. Check results in Argo CD UI.

    ```bash
    # Retrieve password
    kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d; echo

    # Port forward the Argo CD API to localhost:8080
    kubectl port-forward svc/argocd-server -n argocd 8080:443
    ```

    Login to the UI at [https://localhost:8080](https://localhost:8080) with username `admin` and the password retrieved above.

    Verify deployment by checking the results of CronJobs in `dir-admin` application.

8. Clean up.

    ```bash
    minikube delete -p dir-prod
    ```

### Token-based Directory Client authentication

To generate a SPIFFE SVID token for authenticating local Directory Client
with the Directory Server, follow these steps:

1. Create a SPIFFE SVID for local Directory Client.

    ```bash
    kubectl exec spire-dir-prod-argoapp-server-0 -n dir-prod-spire -c spire-server -- \
    /opt/spire/bin/spire-server x509 mint \
    -dns prod.api.example.org \
    -spiffeID spiffe://example.org/local-client \
    -output json > spiffe-prod.json
    ```

2. Set SPIFFE Token variable for Directory Client.

    ```bash
    # Set authentication method to token
    export DIRECTORY_CLIENT_AUTH_MODE="token"
    export DIRECTORY_CLIENT_SPIFFE_TOKEN="spiffe-prod.json"

    # Set Directory Server address (via Ingress)
    export DIRECTORY_CLIENT_SERVER_ADDRESS="prod.api.example.org:443"

    # Or, set Directory Server address and skip TLS verification (via port-forwarding)
    export DIRECTORY_CLIENT_SERVER_ADDRESS="127.0.0.1:8888"
    export DIRECTORY_CLIENT_TLS_SKIP_VERIFY="true"
    ```

3. Port-forward Directory Server API.

    ```bash
    kubectl port-forward svc/dir-dir-prod-argoapp-apiserver -n dir-prod-dir 8888:8888
    ```

4. Run Directory Client.

    ```bash
    dirctl info baeareiesad3lyuacjirp6gxudrzheltwbodtsg7ieqpox36w5j637rchwq
    ```

## GitHub OAuth Authentication

The Directory server can be deployed with an optional Envoy gateway that provides GitHub OAuth authentication, allowing users to access the Directory API using their GitHub identity.

### Features

- Device Flow (default) — No OAuth App registration required.
- Casbin RBAC — Policy-driven, role-based authorization.
- Multi-Role Support — Define admin, reader, and custom roles.
- Per-Method Permissions — Fine-grained API access control
- User & Org Roles — Assign roles to individual users or entire GitHub orgs.
- Default Role — Automatic role for any authenticated user.
- Token Caching — Automatic credential management.
- CI/CD Support — Use GitHub PATs for automation.
- Helm Integration — Fully integrated as `envoy-authz` subchart.

### Quick Start

1. Enable in your deployment values:

    Edit `applications/dir/dev/values.yaml`:

    ```yaml
    apiserver:
      # Enable the Envoy auth gateway subchart
      envoyAuthz:
        enabled: true

      # Configure the subchart
      envoy-authz:
        envoy:
          replicaCount: 1  # Increase for production
          backend:
            address: "dir-dir-dev-argoapp-apiserver.dir-dev-dir.svc.cluster.local"
            port: 8888
          spiffe:
            enabled: true
            trustDomain: example.org
            className: dir-spire

        authServer:
          replicaCount: 1  # Increase for production

          # Casbin RBAC Configuration
          authorization:
            # Default role for any authenticated GitHub user
            defaultRole: "reader"

            # Role definitions
            roles:
              # Admin role - full access
              admin:
                allowedMethods:
                  - "*"  # Wildcard grants all methods
                users:
                  - "github:alice"
                  - "github:bob"
                orgs: []

              # Reader role - read-only access
              reader:
                allowedMethods:
                  - "/agntcy.dir.store.v1.StoreService/Pull"
                  - "/agntcy.dir.search.v1.SearchService/SearchCIDs"
                  - "/agntcy.dir.routing.v1.RoutingService/List"
                users: []  # Inherited by defaultRole
                orgs: []

          # GitHub provider configuration
          github:
            enabled: true
            cacheTTL: 5m

        ingress:
          enabled: true
          className: "nginx"
          host: "dev.gateway.example.org"
          annotations:
            # Required for gRPC over HTTPS
            nginx.ingress.kubernetes.io/backend-protocol: "GRPC"
            nginx.ingress.kubernetes.io/grpc-backend: "true"
    ```

2. Deploy GitHub OAuth authentication

    ArgoCD syncs automatically after git push.

3. Authenticate:

    ```bash
    # Device Flow (recommended - no OAuth App needed)
    export DIRECTORY_CLIENT_SERVER_ADDRESS="dev.gateway.example.org:443"
    export DIRECTORY_CLIENT_AUTH_MODE="github"

    # Login - opens browser for GitHub authorization
    dirctl auth login

    # Use dirctl normally after login
    dirctl routing list
    ```

    For CI/CD, use GitHub Personal Access Tokens or Actions' `GITHUB_TOKEN`:

    ```bash
    export DIRECTORY_CLIENT_AUTH_MODE="github"
    export DIRECTORY_CLIENT_GITHUB_TOKEN="${GITHUB_PAT}"
    # Or use GitHub Actions' automatic token:
    # export DIRECTORY_CLIENT_GITHUB_TOKEN="${GITHUB_TOKEN}"

    # Connect to Envoy gateway
    export DIRECTORY_CLIENT_SERVER_ADDRESS="dev.gateway.example.org:443"

    dirctl routing list
    ```

    !!! note
        For CI/CD, your GitHub user or bot account must be assigned a role (admin or reader) in the RBAC configuration.

### Configuration Options

#### Available API Methods

For a complete list of all 24 Directory API methods with their full gRPC paths and descriptions, see the [envoy-authz values.yaml reference](https://github.com/agntcy/dir/blob/main/install/charts/envoy-authz/values.yaml#L93-L151).

#### User-based roles

Specific users with specific permissions:

```yaml
authServer:
  authorization:
    defaultRole: ""  # No default role - explicit assignment required
    roles:
      admin:
        allowedMethods: ["*"]
        users:
          - "github:alice"
          - "github:bob"
        orgs: []
```

#### Organization-based roles

Entire GitHub org gets a role:

```yaml
authServer:
  authorization:
    defaultRole: "reader"  # All authenticated users get reader
    roles:
      admin:
        allowedMethods: ["*"]
        users: []
        orgs:
          - "your-org"  # All org members are admins
```

#### Combined roles

Users override org roles:

```yaml
authServer:
  authorization:
    defaultRole: "reader"
    userDenyList:
      - "github:suspended-user"  # Block specific users
    roles:
      admin:
        allowedMethods: ["*"]
        users:
          - "github:alice"  # Individual admin
        orgs:
          - "your-org"      # Org-wide admin
      reader:
        allowedMethods:
          - "/agntcy.dir.store.v1.StoreService/Pull"
          - "/agntcy.dir.search.v1.SearchService/SearchCIDs"
        users: []
        orgs: []
```

#### RBAC Precedence

Deny > User Role > Org Role > Default Role

See [Directory Helm Chart documentation](https://github.com/agntcy/dir/tree/main/install/charts/envoy-authz) for complete API method list and advanced configuration.
