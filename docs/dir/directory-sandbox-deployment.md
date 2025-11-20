# Sandbox Deployment

This repository contains the deployment manifests for AGNTCY Directory project.
It is designed to be used with Argo CD for GitOps-style continuous deployment.

The manifests are organized into two main sections:

- `projects/`: Contains Argo CD project definitions.
- `projectapps/`: Contains Argo CD application definitions.

The project will deploy the following components:

- `applications/dir` - AGNTCY Directory server with storage backend.
- `applications/dir-admin` - AGNTCY Directory Admin CLI client.
- `applications/spire*` - SPIRE stack for identity and federation.

!!! note
    This is not a production-ready deployment. It is provided as-is for demonstration and testing purposes.

## Onboarding

To onboard a new environment to **Directory Public Staging Network**, check the [onboarding guide](./directory-public-staging.md).

## Quick Start

This guide sets up the development environment for local testing and development. It uses a local Kind cluster with NodePort services and simplified security. For production deployment with Ingress and TLS, see the [Production Setup](#production-setup) section below.

This guide demonstrates how to set up AGNTCY Directory project using Argo CD in Kubernetes [Kind](https://kind.sigs.k8s.io/) cluster.

1. Create Kind cluster

    ```bash
    kind create cluster --name dir-dev
    ```

2. Install Argo CD in the cluster.

    ```bash
    # Install ArgoCD
    kubectl create namespace argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

    # Wait for ArgoCD to be ready
    kubectl wait --namespace argocd --for=condition=available deployment --all --timeout=120s
    ```

3. Deploy Directory via ArgoCD.

    ```bash
    # Add project
    kubectl apply -f https://raw.githubusercontent.com/agntcy/dir-staging/main/projects/dir/dev/dir-dev.yaml

    # Add application
    kubectl apply -f https://raw.githubusercontent.com/agntcy/dir-staging/main/projectapps/dir/dev/dir-dev-projectapp.yaml
    ```

4. Check results in ArgoCD UI.

    ```bash
    # Retrieve password
    kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d; echo

    # Port forward the ArgoCD API to localhost:8080
    kubectl port-forward svc/argocd-server -n argocd 8080:443
    ```

    Login to the UI at [https://localhost:8080](https://localhost:8080) with username `admin` and the password retrieved above.

    Verify deployment by checking the results of CronJobs in `dir-admin` application.

5. Clean up.

    ```bash
    kind delete cluster --name dir-dev
    ```

### Token-based Directory Client Authentication (Dev)

In some cases, you may want to use Directory Client locally without SPIRE stack. In this case, you can use token-based authentication using SPIFFE X509 SVID tokens.

To generate a SPIFFE SVID token for authenticating local Directory Client with the Directory Server in the dev environment, follow the steps below:

1. Create a SPIFFE SVID for local Directory Client.

    ```bash
    kubectl exec spire-dir-dev-argoapp-server-0 -n dir-dev-spire -c spire-server -- \
    /opt/spire/bin/spire-server x509 mint \
    -dns dev.api.directory.outshift.test \
    -spiffeID spiffe://dev.directory.outshift/local-client \
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

## Production Setup

If you wish to deploy production-grade setup with your own domains and Ingress capabilities on top, follow the steps below.

!!! note
    We are using Minikube to simulate production setup, as it supports Ingress and TLS out of the box. Steps below marked as (local) are optional and intended for local testing purposes only.

!!! warning
    It is not recommended to deploy both dev and prod environments in the same cluster, as they may conflict with each other.

<details>
<summary><strong>View Production Setup</strong></summary>

<br/>

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

4. (local) Install CertManager with Self-Signed Issuer.

    The deployment uses CertManager `letsencrypt` issuer to issue TLS certificates for Ingress resources.

    For local testing purposes, we will create a self-signed root CA certificate
    and configure CertManager to use it as `letsencrypt` issuer.

    Otherwise, if you are deploying to a cloud provider with its own CertManager,
    you can skip this step, but ensure that `letsencrypt` issuer is available.

    ```bash
    # Install Cert-Manager
    kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.19.1/cert-manager.yaml

    # Wait for Cert-Manager to be ready
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
    # Install ArgoCD
    kubectl create namespace argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

    # Wait for ArgoCD to be ready
    kubectl wait --namespace argocd --for=condition=available deployment --all --timeout=120s
    ```

6. Deploy Directory via ArgoCD.

    ```bash
    # Add project
    kubectl apply -f https://raw.githubusercontent.com/agntcy/dir-staging/main/projects/dir/prod/dir-prod.yaml

    # Add application
    kubectl apply -f https://raw.githubusercontent.com/agntcy/dir-staging/main/projectapps/dir/prod/dir-prod-projectapp.yaml
    ```

7. Check results in ArgoCD UI.

    ```bash
    # Retrieve password
    kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d; echo

    # Port forward the ArgoCD API to localhost:8080
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
    -dns prod.api.directory.outshift.test \
    -spiffeID spiffe://prod.directory.outshift/local-client \
    -output json > spiffe-prod.json
    ```

2. Set SPIFFE Token variable for Directory Client.

    ```bash
    # Set authentication method to token
    export DIRECTORY_CLIENT_AUTH_MODE="token"
    export DIRECTORY_CLIENT_SPIFFE_TOKEN="spiffe-prod.json"

    # Set Directory Server address (via Ingress)
    export DIRECTORY_CLIENT_SERVER_ADDRESS="prod.api.directory.outshift.test:443"

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

</details>
