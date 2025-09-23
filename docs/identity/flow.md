# Sequence Flows

## Identity Flows

### Initial Identity Setup

```mermaid
sequenceDiagram
autonumber

Agent Creator->>Identity CLI: Connect to wallet
activate Identity CLI
Identity CLI->>Wallet: Connect
activate Wallet
Wallet-->>Identity CLI: Connected
deactivate Wallet
Identity CLI-->>Agent Creator: Connected
deactivate Identity CLI

Agent Creator->>Identity CLI: Create and store public and private keys
activate Identity CLI
Identity CLI->>Identity CLI: Create public and private keys
Identity CLI->>Wallet: Store keys
activate Wallet
Wallet-->>Identity CLI: Stored
deactivate Wallet
Identity CLI-->>Agent Creator: Keys created and stored
deactivate Identity CLI

Agent Creator->>Identity CLI: Connect to Identity Node
activate Identity CLI
Identity CLI->>Identity Node: Connect to Identity Node
activate Identity Node
Identity Node-->>Identity CLI: Connected
deactivate Identity Node
Identity CLI->>Agent Creator: Connected
deactivate Identity CLI

Agent Creator->>Identity CLI: Request to publish public key as well known
activate Identity CLI
Identity CLI->>Wallet: Get public key
activate Wallet
Wallet-->>Identity CLI: Public key
deactivate Wallet
Identity CLI->>Identity Node: Request to publish public key as well known
activate Identity Node
Identity Node-->>Identity CLI: Respond with verification uri action<br/>to complete publishing
Identity CLI-->>Agent Creator: Respond with verification uri action to complete publishing
deactivate Identity CLI
Agent Creator->>Identity Node: Complete verification uri action (e.g., via browser)
Identity Node-->>Identity Node: Publish public key as well known
Identity Node-->>Agent Creator: Published public key as well known
deactivate Identity Node
```

## User Flows

### Create a New Agent

This sequence diagram illustrates the process of creating, publishing, and registering an Agent's metadata and identity information within the Agntcy ecosystem.

```mermaid
sequenceDiagram
autonumber

Agent Creator->>e.g. Github: Publish agent source<br/>code and ACP manifest

Agent Creator->>Identity CLI: Create and publish ResolverMetadata with an Agent ID

Agent Creator->>Directory CLI: Create Agent OASF with Agent ID in identity extension

Agent Creator->>Directory CLI: Publish OASF

Agent Creator->>Identity CLI: Issue and Publish an Agent Badge (Verifiable Credential) with OASF
```

### Update an Agent

This sequence diagram illustrates the process of updating an existing Agent along with its associated metadata and identity information within the Agntcy ecosystem.

```mermaid
sequenceDiagram
autonumber

Agent Creator->>e.g. Github: Update and publish agent source<br/>code and ACP manifest

Agent Creator->>Directory CLI: Update Agent OASF keeping the same<br/>Agent ID in identity extension

Agent Creator->>Directory CLI: Publish OASF

Agent Creator->>Identity CLI: Issue and Publish a new Agent Badge (Verifiable Credential) with OASF
```

### Verify an Agent Locally

This sequence diagram illustrates the local verification process of an Agent's authenticity, including its associated identity credentials, within the Agntcy ecosystem.

```mermaid
sequenceDiagram
autonumber

Agent Consumer->>Directory CLI: Discover and download the agent OASF

Agent Consumer->>Agent Consumer: Extract the Agent ID from<br/>the OASF identity extension

Agent Consumer->>Identity CLI: Resolve the Agent ID to get the Agent Badges

Agent Consumer->>Agent Consumer: Find the Agent Badge<br/>that matches the OASF

Agent Consumer->>Identity CLI: Verify the Agent Badge
```

### Verify an Agent Using Search Endpoint

This sequence diagram illustrates the process of verifying an Agent's authenticity using a search endpoint within the Agntcy ecosystem. This approach allows the Agent Verifier to locate and validate the correct Agent Badge by querying directly with both the Agent ID and OASF.

```mermaid
sequenceDiagram
autonumber

Agent Consumer->>Directory CLI: Discover and download the agent OASF

Agent Consumer->>Agent Consumer: Extract the Agent ID from<br/>the OASF identity extension

Agent Consumer->>Identity CLI: Search for the Agent Badge<br/>for the Agent ID + OASF

Agent Consumer->>Identity CLI: Verify the Agent Badge
```

## Detailed Flows

### Create a New Agent

```mermaid
sequenceDiagram
autonumber

Agent Creator->>e.g. Github: Publish agent source<br/>code and ACP manifest
activate e.g. Github
e.g. Github-->>Agent Creator: Published
deactivate e.g. Github

Agent Creator->>Identity CLI: Create and publish ResolverMetadata with an Agent ID
activate Identity CLI
Identity CLI->>Wallet: Get Public Key
activate Wallet
Wallet-->>Identity CLI: Public Key
deactivate Wallet
Identity CLI->>Identity Node: Create and publish ResolverMetadata with an Agent ID
activate Identity Node
Identity Node->>Identity Node: Generate a globally unique ID
Identity Node->>Identity Node: Create ResolverMetadata with Agent ID
Identity Node-->>Identity CLI: Created and published
deactivate Identity Node
Identity CLI-->>Agent Creator: Created and published
deactivate Identity CLI

Agent Creator->>Directory CLI: Create Agent OASF with Agent ID in identity extension
activate Directory CLI
Directory CLI-->>Agent Creator: OASF
deactivate Directory CLI

Agent Creator->>Directory CLI: Publish OASF
activate Directory CLI
Directory CLI->>Directory: Publish OASF
activate Directory
Directory-->>Directory CLI: Published OASF with<br/>Catalogue ID (Digest)
deactivate Directory
Directory CLI-->>Agent Creator: Published OASF with Catalogue ID (Digest)
deactivate Directory CLI

Agent Creator->>Identity CLI: Issue and Publish an Agent Badge<br/>(Verifiable Credential) with OASF
activate Identity CLI
Identity CLI->>Identity CLI: Issue an Agent Badge (Verifiable Credential) with OASF
Identity CLI->>Wallet: Get Private Key
activate Wallet
Wallet-->>Identity CLI: Private Key
deactivate Wallet
Identity CLI->>Identity CLI: Generate Data Integrity proof and add to Agent Badge
Identity CLI->>Identity Node: Publish the Agent Badge<br/>(/v1alpha1/vc/publish)
activate Identity Node
Identity Node-->>Identity CLI: Published
deactivate Identity Node
Identity CLI-->>Agent Creator: Issued and Published
deactivate Identity CLI

```

### Update an Agent

```mermaid
sequenceDiagram
autonumber

Agent Creator->>e.g. Github: Update and publish agent source<br/>code and ACP manifest
activate e.g. Github
e.g. Github-->>Agent Creator: Published
deactivate e.g. Github

Agent Creator->>Directory CLI: Update Agent OASF keeping the same<br/>Agent ID in identity extension
activate Directory CLI
Directory CLI-->>Agent Creator: OASF
deactivate Directory CLI

Agent Creator->>Directory CLI: Publish OASF
activate Directory CLI
Directory CLI->>Directory: Publish OASF
activate Directory
Directory-->>Directory CLI: Published OASF with<br/>Catalogue ID (Digest)
deactivate Directory
Directory CLI-->>Agent Creator: Published OASF with Catalogue ID (Digest)
deactivate Directory CLI

Agent Creator->>Identity CLI: Issue and Publish a new Agent Badge (Verifiable Credential) with OASF
activate Identity CLI
Identity CLI->>Identity CLI: Issue a new Agent Badge (Verifiable Credential) with OASF
Identity CLI->>Wallet: Get Private Key
activate Wallet
Wallet-->>Identity CLI: Private Key
deactivate Wallet
Identity CLI->>Identity CLI: Generate Data Integrity proof
Identity CLI->>Identity Node: Publish the Agent Badge<br/>(/v1alpha1/vc/publish)
activate Identity Node
Identity Node-->>Identity CLI: Published
deactivate Identity Node
Identity CLI-->>Agent Creator: Issued and Published
deactivate Identity CLI
```

### Verify an Agent Locally

```mermaid
sequenceDiagram
autonumber

Agent Consumer->>Directory CLI: Discover and download the agent OASF
activate Directory CLI
Directory CLI->>Directory: Discover and download the agent OASF
activate Directory
Directory-->>Directory CLI: Downloaded OASF
deactivate Directory
Directory CLI->>Agent Consumer: Downloaded OASF
deactivate Directory CLI

Agent Consumer->>Agent Consumer: Extract the Agent ID from<br/>the OASF identity extension

Agent Consumer->>Identity CLI: Resolve the Agent ID to get the Agent Badges
activate Identity CLI
Identity CLI->>Identity Node: Resolve the Agent ID to get the Agent Badges
activate Identity Node
Identity Node-->>Identity CLI: Agent Badges
deactivate Identity Node
Identity CLI-->>Agent Consumer: Agent Badges
deactivate Identity CLI

Agent Consumer->>Agent Consumer: Find the Agent Badge<br/>that matches the OASF

Agent Consumer->>Identity CLI: Verify the Agent Badge
activate Identity CLI
Identity CLI->>Identity Node: Resolve the Agent ID to get the ResolverMetadata
activate Identity Node
Identity Node-->>Identity CLI: ResolverMetadata
deactivate Identity Node
Identity CLI->>Identity CLI: Verify the Agent Badge Data Integrity proof<br/>using the ResolverMetadata public key
Identity CLI-->>Agent Consumer: Verified
deactivate Identity CLI
```

### Verify an Agent Using Search Endpoint

```mermaid
sequenceDiagram
autonumber

Agent Consumer->>Directory CLI: Discover and download the agent OASF
activate Directory CLI
Directory CLI->>Directory: Discover and download the agent OASF
activate Directory
Directory-->>Directory CLI: Downloaded OASF
deactivate Directory
Directory CLI->>Agent Consumer: Downloaded OASF
deactivate Directory CLI

Agent Consumer->>Agent Consumer: Extract the Agent ID from<br/>the OASF identity extension

Agent Consumer->>Identity CLI: Search for the Agent Badge<br/>for the Agent ID + OASF
activate Identity CLI
Identity CLI->>Identity Node: Search for the Agent Badge<br/>for the Agent ID + OASF<br/>(/v1alpha1/vc/search)
activate Identity Node
Identity Node-->>Identity CLI: Agent Badge
deactivate Identity Node
Identity CLI-->>Agent Consumer: Agent Badge
deactivate Identity CLI

Agent Consumer->>Identity CLI: Verify the Agent Badge
activate Identity CLI
Identity CLI->>Identity Node: Resolve the Agent ID to get the ResolverMetadata
activate Identity Node
Identity Node-->>Identity CLI: ResolverMetadata
deactivate Identity Node
Identity CLI->>Identity CLI: Verify the Agent Badge Data Integrity proof<br/>using the ResolverMetadata public key
Identity CLI-->>Agent Consumer: Verified
deactivate Identity CLI
```
