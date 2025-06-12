# Identifiers

## Definitions

The [`AGNTCY`](https://agntcy.org/) supports various types of identities, referred to as IDs, which serve as universally unique identifiers for the main entities or subjects operated by the [`AGNTCY`](https://agntcy.org/), including Agents and Multi-Agent Systems (MAS).

### Key Identifiers

Each ID is associated 1:1 with ResolverMetadata, which contains the necessary information to establish trust while trying to use or interact with an Agent or a MAS ID.
ID: A universally unique identifier that represents the identity of a subject (e.g., an Agent or MAS).
ResolverMetadata: Metadata, represented in the form of a JSON-LD object, containing cryptographic material and verification methods to resolve and establish trust with the associated ID (e.g., an Agent or MAS).

Concrete examples with various IDs and associated ResolverMetadata can be found [`here`](https://spec.identity.agntcy.org/docs/id/examples)