# Flow Diagrams

## Agntcy - User Flows

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

Additional flow diagrams can be found in the [`Identity Spec`](https://spec.identity.agntcy.org/docs/category/sequence-flows).

