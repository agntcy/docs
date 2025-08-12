# Verifiable Credentials

AGNTCY supports various types of Verifiable Credentials (VCs). A verifiable credential is a structured and cryptographically verifiable way to express claims made by an issuer. These claims can pertain to:

- Agent definitions (for example, an [OASF definition](../oasf/open-agentic-schema-framework.md) or an [A2A Agent Card](https://google.github.io/A2A/specification/agent-card/))
- Deployment configurations
- Authorization assertions used in processes such as Multi-Factor Authentication (MFA)

## Key VCs

The identity framework conceived by AGNTCY allows not only to cryptographically bind an agent ID to an issuer, a public key and a proof of provenance but also the binding of the same agent ID to different definitions of the core agent, including different schemas, versions, locators, etc., as well as additional VCs that may be used during Multi-Factor authentication and authorization (MFA) processes. The same approach applies to MCP Servers.

Among some of the key VCs within AGNTCY are the following:

### Agent Badge

An Agent Badge is an enveloped VC captured in the form of a JSON-LD object that represents a specific definition of an agent subject in the IoA.

The definition follows a given schema (for example, an OASF definition or an A2A Agent Card schema). An agent subject can have multiple Agent Badges, each representing a different definition of the same core agent or agent subject. For instance, different software versions and/or patched releases of an agent will have different Agent Badges.

The same applies if the agent's code is available in different forms (for example, if it can be used and composed using different types of artifacts, such as a Docker container image or a Python package), or if the source code can be reached at different sites or routing locators (through GitHub or sites like Hugging Face), and so on.

Examples of an Agent Badge can be found [here](./vc_agent_badge.md).

### MCP Server Badge

An MCP Server Badge is an enveloped VC, captured in the form of a JSON-LD object, that represents a specific definition of an MCP Server subject in the IoA. The definition should follow a given schema (that is, a json specification following a similar approach to A2A's card but for MCP Servers). 

Like in the case of an agent subject, an MCP Server can have multiple MCP Server Badges, each representing a different definition of the same core MCP Server subject. For instance, different software versions and/or patched releases of an MCP Server will have different MCP Server Badges. 

A example of an MCP Server Badge can be found [here](./vc_mcp.md).

## Use Cases

The combined use of Badges (VCs) and ResolverMetadata enables automated and trustworthy validation of:

- Issuer public keys, via assertion methods.
- Authenticity and integrity of credentials (Agent or MCP Server Badges).
- Entity provenance and update lineage (especially critical for secure versioning).

## Benefits of this Model

- Prevents impersonation of Agents, and MCP Server resources and tools by ensuring provenance can be verified.
- Enables secure versioning and traceability, supporting safe upgrades and patching.
- Facilitates advanced authentication and authorization workflows, including those involving:
    - Dynamic trust establishment
    - Machine-to-machine negotiation (with or without human input)
    - Pre-connection credential validation

These capabilities apply equally to Agents and MCP Servers, supporting trust-aware composition and interaction across the IoA.
