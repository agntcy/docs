# Identity Quick Start Guide

## Get Started

This short guide allows you to setup the Identity `Issuer CLI` as well as the Identity `Node Backend`.
The `Issuer CLI` allows to generate, register, search for, and verify badges for Agents and MCP Servers. The CLI includes a library enabling storage and retrieval of the keys required to sign the badges, both on local storage or using a 3rd party wallet or vault.
The `Node Backend` comprises the APIs and the backend core. It stores, maintains, and binds org:sub-org IDs, PubKeys, Subject IDs and metadata, including badges, ResolverMetadata and Verifiable Credentials (VCs).

For detailed information in the Agent Directory Service, see the [Identity documentation](../identity/identity.md).

### Prerequisites

To run these steps successfully, you need to have the following installed:

- [Docker Desktop](https://docs.docker.com/get-docker/), or have both: [Docker Engine v27 or higher](https://docs.docker.com/engine/install/) and [Docker Compose v2.35 or higher](https://docs.docker.com/compose/install/)

### Step 1: Install the Issuer CLI

Use the following command to install the `Issuer CLI`:

using `curl`:

```bash
sh -c "$(curl -sSL https://raw.githubusercontent.com/agntcy/identity/refs/heads/main/deployments/scripts/identity/install_issuer.sh)"
```

or using `wget`:

```bash
sh -c "$(wget -qO- https://raw.githubusercontent.com/agntcy/identity/refs/heads/main/deployments/scripts/identity/install_issuer.sh)"
```

```{NOTE}
> You can also download the `Issuer CLI` binary corresponding to your platform from the [latest releases](https://github.com/agntcy/identity/releases).
>
> On some platforms you might need to add execution permissions and/or approve the binary in `System Security Settings`.
>
> For easier use, consider moving the binary to your `$PATH` or to the `/usr/local/bin` folder.
```

If you have `Golang` set up locally, you could also use the `go install command`:

```bash
go install github.com/agntcy/identity/cmd/issuer@latest && \
  ln -s $(go env GOPATH)/bin/issuer $(go env GOPATH)/bin/identity
```

### Step 2: Start the Node Backend with Docker

1. Clone the repository:

   ```bash
   git clone https://github.com/agntcy/identity.git
   ```

2. Start the Node Backend with Docker:

   ```bash
   ./deployments/scripts/identity/launch_node.sh
   ```

   Or use `make` if available locally:

   ```bash
   make start_node
   ```

### Step 3: Verify the Installation

You can verify the installation by running the command below to see the [different commands available](#core-commands-to-use-the-cli):

```bash
identity -h
```

## Core commands to use the CLI

Here are the core commands you can use with the CLI

- **vault**: Manage cryptographic vaults and keys
- **issuer**: Register and manage issuer configurations
- **metadata**: Generate and manage metadata for identities
- **badge**: Issue and publish badges for identities
- **verify**: Verify identity badges
- **config**: Display the current configuration context

## Run the demo

This demo scenario will allow you to see how to use the AGNTCY Identity components can be used in a real environment.
You will be able to perform the following:

- Register as an Issuer
- Generate metadata for an MCP Server
- Issue and publish a badge for the MCP Server
- Verify the published badge

### Prerequisites

First, follow the steps in the [Get Started](#get-started) section above to install the `Issuer CLI` and run the `Node Backend`, and generate a local vault and keys.

To run this demo setup locally, you need to have the following installed:

- [Docker Desktop](https://docs.docker.com/get-docker/), or have both: [Docker Engine v27 or higher](https://docs.docker.com/engine/install/) and [Docker Compose v2.35 or higher](https://docs.docker.com/compose/install/)
- [Ollama CLI](https://ollama.com/download)
- [Okta CLI](https://cli.okta.com/manual/#installation)

### Step 1: Run the Samples with Ollama and Docker

The agents in the samples rely on a local instance of the Llama 3.2 LLM to power the agent's capabilities.
With Ollama installed, you can download and run the model (which is approximately 2GB, so ensure you have enough disk space) using the following command:

1. Run the Llama 3.2 model:

   ```bash
   ollama run llama3.2
   ```

2. From the root of the repository, navigate to the `samples` directory and run the following command to deploy the `Currency Exchange A2A Agent` leveraging the `Currency Exchange MCP Server`:

   ```bash
   cd samples && docker compose up -d
   ```

3. [Optional] Test the samples using the provided [test clients](https://github.com/agntcy/identity/tree/main/samples/README.md#testing-the-samples).

### Step 2: Use the CLI to create a local Vault and generate keys

1. Create a local vault to store generated cryptographic keys:

   ```bash
   identity vault connect file -f ~/.identity/vault.json -v "My Vault"
   ```

2. Generate a new key pair and store it in the vault:

   ```bash
   identity vault key generate
   ```

### Step 3: Register as an Issuer

For this demo we will use Okta as an IdP to create an application for the Issuer.
The quickly create a trial account and application, we have provided a script to automate the process using the Okta CLI.

```{IMPORTANT}
> If you already have an Okta account, you can use the `okta login` command to log in to your existing organization.
>
> If registering a new Okta developer account fails, proceed with manual trial signup and then use the `okta login` command,
> as instructed by the Okta CLI.
```

1. Run the following command from the root repository to create a new Okta application:

   ```bash
   . ./demo/scripts/create_okta_app
   ```

2. In the interactive prompt, choose the following options:

   `> 4: Service (Machine-to-Machine)`, `> 5: Other`

3. Register the Issuer using the `Issuer CLI` and the environment variables from the previous step:

   ```bash
   identity issuer register -o "My Organization" \
       -c "$OKTA_OAUTH2_CLIENT_ID" -s "$OKTA_OAUTH2_CLIENT_SECRET" -u "$OKTA_OAUTH2_ISSUER"
   ```

```{NOTE}
> You can now access the `Issuer's Well-Known Public Key` at [`http://localhost:4000/v1alpha1/issuer/{common_name}/.well-known/jwks.json`](http://localhost:4000/v1alpha1/issuer/{common_name}/.well-known/jwks.json),
> where `{common_name}` is the common name you provided during registration.
```

### Step 4: Generate metadata for an MCP Server

Create a second application for the MCP Server metadata using Okta, similar to the previous step:

1. Run the following command from the root repository to create a new Okta application:

   ```bash
   . ./demo/scripts/create_okta_app
   ```

2. In the interactive prompt, choose the following options:

   `> 4: Service (Machine-to-Machine)`, `> 5: Other`

3. Generate metadata for the MCP Server using the `Issuer CLI` and the environment variables from the previous step:

   ```bash
   identity metadata generate -c "$OKTA_OAUTH2_CLIENT_ID" \
       -s "$OKTA_OAUTH2_CLIENT_SECRET" -u "$OKTA_OAUTH2_ISSUER"
   ```

> [!NOTE]
> When successful, this command will print the metadata ID, which you will need in the next step to view published badges that are linked to this metadata.

### Step 5: Issue and Publish a Badge for the MCP Server

1. Issue a badge for the MCP Server:

   ```bash
   identity badge issue mcp -u http://localhost:9090 -n "My MCP Server"
   ```

2. Publish the badge:

   ```bash
   identity badge publish
   ```

```{NOTE}
> You can now access the `VCs as a Well-Known` at [`http://localhost:4000/v1alpha1/vc/{metadata_id}/.well-known/vcs.json`](http://localhost:4000/v1alpha1/vc/{client_id}/.well-known/vcs.json),
> where `{metadata_id}` is the metadata ID you generated in the previous step.
```

### (Optional) Step 6: Verify a Published Badge

You can use the `Issuer CLI` to verify a published badge any published badge, not just those that you issued yourself.
This allows others to verify the Agent and MCP badges you publish.

1. Download the badge that you created in the previous step, replacing {metadata_id} with the metadata ID from step 4:

   ```bash
   curl -o vcs.json http://localhost:4000/v1alpha1/vc/{metadata_id}/.well-known/vcs.json
   ```

2. Verify the badges using the `Issuer CLI`:

   ```bash
   identity verify -f vcs.json
   ```

## Development

For more detailed development instructions please refer to the following sections:

- [Node Backend](https://github.com/agntcy/identity/tree/main/cmd/node/README.md)
- [Issuer CLI](https://github.com/agntcy/identity/tree/main/cmd/issuer/README.md)
- [Samples](https://github.com/agntcy/identity/tree/main/samples/README.md)
- [Api Spec](https://github.com/agntcy/identity/tree/main/api/spec/README.md)
- [Node Client SDK](https://github.com/agntcy/identity/tree/main/api/client/README.md)
