# Public Staging Instance Deployment

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

This guide demonstrates how to set up AGNTCY Directory project using Argo CD in Kubernetes Kind cluster.

1. Create Kind cluster:

    ```bash
    kind create cluster --name argo-dev
    ```

2. Install Argo CD in the cluster:

    ```bash
    kubectl create namespace argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
    ```

3. Deploy Directory via ArgoCD:

    ```bash
    # Add project
    kubectl apply -f https://raw.githubusercontent.com/agntcy/dir-staging/main/projects/dir/project.yaml

    # Add application
    kubectl apply -f https://raw.githubusercontent.com/agntcy/dir-staging/main/projectapps/dir/application.yaml
    ```


4. Check results in ArgoCD UI:

    ```bash
    # Retrieve password
    kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d; echo

    # Port forward the ArgoCD API to localhost:8080
    kubectl port-forward svc/argocd-server -n argocd 8080:443
    ```

    Login to the UI at [https://localhost:8080](https://localhost:8080) with username `admin` and the password retrieved above.

5. Clean up

    ```bash
    kind delete cluster --name argo-dev
    ```
