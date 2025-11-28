# Identity Service

## What is the AGNTCY Identity Service?

AGNTCY Identity Service serves as the central hub for managing and verifying digital identities for your Agentic Services. In today's interconnected digital landscape, secure and reliable identity management is paramount. AGNTCY Identity Service addresses this need by providing a streamlined service to:

- **Verify** the authenticity of existing identity badges.
- **Register** new Agentic Services, establishing their unique identities.

Whether you are integrating existing services or deploying new ones, AGNTCY Identity Service ensures that all your components—including MCP Servers, A2A Agents, and OASF—are properly identified and managed.

## Getting Started with AGNTCY Identity Service

To begin using AGNTCY Identity Service's features, you have two primary pathways:

1. **Verify Existing Identities**: If you already possess identity badges for your Agentic Services, you can use AGNTCY Identity Service to verify their authenticity and integrate them into the system.
2. **Register New Agentic Services**: For new deployments or services that require a fresh identity, AGNTCY Identity Service facilitates the registration process, allowing you to create and manage their digital presence.

### Get Started in 5 Minutes

This short guide allows you to setup the Identity Service `Frontend` as well as the Identity Service `Backend`.

#### Prerequisites

To run these steps successfully, you need to have the following installed:

- [Docker Desktop](https://docs.docker.com/get-docker/), or have both: [Docker Engine v27 or higher](https://docs.docker.com/engine/install/) and [Docker Compose v2.35 or higher](https://docs.docker.com/compose/install/)

#### Setup OIDC Provider

1. Setup OIDC Provider

   - Create an OIDC application in your OIDC provider.

     You can use any OIDC provider of your choice. For testing purposes, you can use [Ory](https://www.ory.sh/), [Keycloak](https://www.keycloak.org/) or [Auth0](https://auth0.com/).
     Configure the following variables in your shell environment:

     ```bash
     export OIDC_ISSUER_URL=<OIDC_ISSUER_URL>
     export OIDC_CLIENT_ID=<OIDC_CLIENT_ID>
     export OIDC_LOGIN_URL=<OIDC_LOGIN_URL>
     export OIDC_CLIENT_ID_CLAIM_NAME=<OIDC_CLIENT_ID_CLAIM_NAME>
     ```

     where:

     - `OIDC_ISSUER_URL` - The URL of your OIDC provider (e.g., `https://{INSTANCE_URL}/oauth2/{CLIENT_ID}/.well-known/openid-configuration`).
     - `OIDC_CLIENT_ID` - The client ID you created in your OIDC provider.
     - `OIDC_LOGIN_URL` - The login URL of your OIDC provider (e.g., `https://{INSTANCE_URL}/oauth2/{CLIENT_ID}/authorize`).
     - `OIDC_CLIENT_ID_CLAIM_NAME` - The claim name in the Access token that contains the client ID (default: `cid`).

       !!! note
           Make sure to add `http://localhost:5500` as a redirect URI for your OIDC client.

   - Or use our demo script to setup a local OIDC provider using [Ory Hydra](https://www.ory.sh/):

     ```bash
     . ./demo/scripts/setup_hydra_oidc
     ```

     This will setup a local OIDC provider using Ory and configure the necessary environment variables in your shell.

2. Start the Frontend and the Backend with Docker:

   ```bash
   ./deployments/scripts/launch.sh
   ```

   Or use `make` if available locally:

   ```bash
   make start
   ```

   !!! note
       You can also install the `Backend` and the `Frontend` using our [Helm charts](https://github.com/agntcy/identity-service/tree/main/charts).

3. Access the Frontend UI and the Backend APIs:

   - The Backend APIs will be available at: `http://localhost:4000` for REST and `http://localhost:4001` for gRPC.
   - The Frontend UI will be available at: `http://localhost:5500`.

## Key Functionalities

AGNTCY Identity Service is structured around two core functionalities to cater to different identity management needs:

### Verify Identities

This functionality is designed for users who need to confirm the legitimacy of pre-existing identities.

- **Purpose**: To validate and integrate identities for your deployed Agentic Services.
- **Scope**: Primarily focuses on verifying identities associated with:
  - **MCP Servers** (Model Context Protocol)
  - **A2A Agents** (Agent-to-Agent communication entities)
  - **OASF** ([Open Agentic Schema Framework](https://github.com/agntcy/oasf))
- **Action**: Initiate the verification process by clicking the "**Verify Identity**" button. This will guide you through the steps required to authenticate your existing identities.

### Create Identities

This functionality empowers developers to establish new identities for their AI Agents and MCP Servers and define their associated access controls.

- **Purpose**: To provision and manage new digital identities for Agentic Services.
- **Scope**: Allows you to add and configure identities for:
  - **MCP Servers**
  - **A2A Agents**
  - **OASF**
- **Management**: Beyond creation, this section enables you to:
  - **Manage identities**: Update, modify, or revoke existing identities.
  - **Define `TBAC` Rules and Policies**: Implement Task-Based Access Control rules to govern how your Agentic Services interact and access resources, ensuring secure and compliant operations.
- **Action**: To create new identities or manage existing ones, you will typically need to "**Log In**" to your AGNTCY Identity Service account. If you are a new user, you can "**Sign Up**" to create an account and begin leveraging these features.

## Accessing AGNTCY Identity Service

Access to AGNTCY Identity Service's full suite of features, particularly for creating and managing identities, requires user authentication.

- **Log In**: If you already have an account, use the "**Log In**" option to access your dashboard and manage your Agentic Service identities.
- **Sign Up**: If you are new to AGNTCY Identity Service, select "**Sign Up**" to create a new account and begin your journey with secure identity management.

For more in-depth instructions, tutorials, and advanced configurations, please navigate through the specific sections of our comprehensive documentation.
