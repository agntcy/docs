# MCP Server Badge Example

## MCP Server Badge

The example below shows an [MCP Server Badge](./credentials.md) as a VC, represented as a JSON-LD object that contains information about the MCP Server, including the issuing organization, its [ID](identifiers.md), and schema definition (e.g. an [MCP Server Definition](https://spec.identity.agntcy.org/jsonschema/agntcy/identity/core/v1alpha1/McpServer#source-) in JSON). Such a definition may encompass additional metadata, including locators, authentication methods, hashing methods, etc. The VC below also includes a data integrity proof as an embedded proof within an envelope.

```json
CREDENTIAL
{
  @context: ["https://www.w3.org/ns/credentials/v2", "https://www.w3.org/ns/credentials/examples/v2"],
  id: uuid(),
  type: ["VerifiableCredential", "MCPServerBadge"],
  issuer: ORG,
  validFrom: date(),
  credentialSubject: {
    id: "ID",
    badge: MCP_SERVER_JSON,
  },
  credentialSchema: [{
    id: "https://spec.identity.agntcy.org/jsonschema/agntcy/identity/core/v1alpha1/McpServer#source-",
    type: "JsonSchema"
  }],
  proof: {
    type: "DataIntegrityProof",
    proofPurpose: "assertionMethod",
    proofValue: "x36BAcFde8KkqYABCyBCq...jQCrfFPP2oumHKtz"
  }
}

```

Where:

- `credentialSubject.id`: represents the [ID](identifiers.md#definitions) of the MCP Server subject.
- `credentialSubject.badge`: adheres to the [MCP Server Definition](https://spec.identity.agntcy.org/jsonschema/agntcy/identity/core/v1alpha1/McpServer#source-) schema.

The `proof` in an MCP Server Badge can be verified using the `assertionMethod` defined in the `ResolverMetadata` object (various `ResolverMetadata` examples are available [here](./identifier_examples.md)).

Multiple envelopes are supported in AGNTCY, including JSON Object Signing and Encryption (JOSE).

## MCP Server Badges accessible through a "well-known" endpoint

The MCP Server Badges can be accessed using the following well-known URL: [https://api.NODE/ID/.well-known/vcs.json](https://api.NODE/ID/.well-known/vcs.json)

Where:

- `ID`: represents the [ID](identifiers.md#definitions) of the MCP Server subject.
- `NODE`: represents a **trust anchor**, that is, an Identity Node within the AGNTCY identity system.

!!! note
    Under the well-known URL above, there could be several MCP Server badges available from the same issuer.
