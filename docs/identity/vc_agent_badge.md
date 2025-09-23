# Agent Badge Examples

## OASF Agent Badge

The example below shows an [Agent Badge](./credentials.md#agent-badge) as a VC, represented as a JSON-LD object that contains information about the Agent, including the issuing organization, its [ID](identifiers.md#definitions), a schema definition, which in this case is an [OASF Definition](../oasf/open-agentic-schema-framework.md). Such definitions may encompass additional metadata, including locators, authentication methods, hashing methods, etc. The VC below also includes a data integrity proof within an envelope.

```json
CREDENTIAL
{
  @context: ["https://www.w3.org/ns/credentials/v2", "https://www.w3.org/ns/credentials/examples/v2"],
  id: uuid(),
  type: ["VerifiableCredential", "AgentBadge"],
  issuer: ORG,
  validFrom: date(),
  credentialSubject: {
    id: "ID",
    badge: OASF_JSON,
  },
  credentialSchema: [{
    id: "https://schema.oasf.agntcy.org/schema/objects/agent",
    type: "JsonSchema"
  }],
  proof: {
    type: "DataIntegrityProof",
    proofPurpose: "assertionMethod",
    proofValue: "z58DAdFfa9SkqZMVPxAQp...jQCrfFPP2oumHKtz"
  }
}

```

Where:

- `credentialSubject.id`: represents the [ID](./identifiers.md#definitions) of the Agent subject.
- `credentialSubject.badge`: adheres to the [OASF Definition](../oasf/open-agentic-schema-framework.md) schema.

## A2A Agent Badge

Similarly, the example below shows a second Agent Badge, using in this case another definition, that is, an [A2A Agent Card](https://github.com/google/A2A/blob/main/specification/json/a2a.json#AgentCard) schema.

```json
CREDENTIAL
{
  @context: ["https://www.w3.org/ns/credentials/v2", "https://www.w3.org/ns/credentials/examples/v2"],
  id: uuid(),
  type: ["VerifiableCredential", "AgentBadge"],
  issuer: ORG,
  validFrom: date(),
  credentialSubject: {
    id: "ID",
    badge: AGENT_CARD_JSON,
  },
  credentialSchema: [{
    id: "https://github.com/google/A2A/blob/main/specification/json/a2a.json#AgentCard",
    type: "JsonSchema"
  }],
  proof: {
    type: "DataIntegrityProof",
    proofPurpose: "assertionMethod",
    proofValue: "y58DA4DS42D35455A32Qp...jQCrfFPP2oumHKtz"
  }
}

```

Where:

- `credentialSubject.id`: represents the [ID](identifiers.md#definitions) of the Agent subject.
- `credentialSubject.badge`: adheres to the [A2A Agent Card](https://github.com/google/A2A/blob/main/specification/json/a2a.json#AgentCard) schema.

The `proof` in an Agent Badge can be verified using the `assertionMethod` defined in the `ResolverMetadata` object (various `ResolverMetadata` examples are available [here](./identifier_examples.md)).

!!! note
    Multiple envelopes are supported in AGNTCY, including JSON Object Signing and Encryption (JOSE).

## Agent Badges Accessible through a "Well-Known" Endpoint

The Agent Badges of an agent subject can be accessed using the following well-known URL: [https://api.NODE/ID/.well-known/vcs.json](https://api.NODE/ID/.well-known/vcs.json)

Where:

- `ID`: represents the [ID](identifiers.md#definitions) of the Agent subject.
- `NODE`: represents a **trust anchor**, that is, an Identity Node within the AGNTCY identity system.

!!! note
    Under the well-known URL above, there could be several agents badges available from the same issuer.
