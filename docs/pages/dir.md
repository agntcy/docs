# Core Concepts

The Agent Directory Service (ADS) is a distributed directory service designed to
store metadata for AI agent applications. This metadata, stored as directory
records, enables the discovery of agent applications with specific skills for
solving various problems.
The implementation features distributed directories that interconnect through a
content-routing protocol. This protocol maps agent skills to directory record
identifiers and maintains a list of directory servers currently hosting those
records.
Directory records are identified by globally unique names that are routable
within a DHT (Distributed Hash Table) to locate peer directory servers.
Similarly, the skill taxonomy is routable in the DHT to map skillsets to records
that announce those skills.

Each directory record must include skills from a defined taxonomy, as specified
in the [Taxonomy of AI Agent Skills](oasf-taxonomy.md) from [OASF](oasf.md).
While all record data is modeled using [OASF](oasf.md), only skills are
leveraged for content routing in the distributed network of directory servers.
The ADS specification is under active development and is published as an
Internet Draft at [ADS Spec](https://spec.dir.agntcy.org). The source code is
available in the [ADS Spec sources](https://github.com/agntcy).
The current reference implementation, written in Go, provides server and client
nodes with gRPC and protocol buffer interfaces. The directory record storage is
built on [ORAS](https://oras.land) (OCI Registry As Storage), while data
distribution uses the [zot](https://zotregistry.dev) OCI server implementation.

## Naming

In distributed systems, having a reliable and collision-resistant naming scheme
is crucial. The agent directory uses cryptographic hashes to generate globally
unique identifiers for data records.
ADS leverages OCI as object storage and therefore identifiers are made available
as described in [OCI digest](https://github.com/opencontainers/image-spec/blob/main/descriptor.md#digests).

## Content Routing

ADS implements capability-based record discovery through a hierarchical skill
taxonomy. This architecture enables:

1. Capability Announcement:
   1. Multi-agent systems can publish their capabilities by encoding them as
      skill taxonomies.
   2. Each record contains metadata describing the agent's functional abilities.
   3. Skills are structured in a hierarchical format for efficient matching.
2. Discovery Process: The system performs a two-phase discovery operation:
   1. Matches queried capabilities against the skill taxonomy to determine
      records by their identifier.
   2. Identifies the server nodes storing relevant records.
3. Distributed Resolution: Local nodes execute targeted retrievals based on:
   1. Skill matching results: Evaluates capability requirements.
   2. Server location information: Determines optimal data sources.

ADS uses libp2p [Kad-DHT](https://docs.libp2p.io/concepts/discovery-routing/kaddht/)
for server and content discovery.

## Distributed Object Storage

ADS differs from block storage systems like
[IPFS](https://ipfs.tech/) in its approach to distributed object storage.
The differences are described in the following sections.

### Simplified Content Retrieval

1. ADS directly stores complete records rather than splitting them into blocks.
2. No special optimizations needed for retrieving content from multiple sources.
3. Records are retrieved as complete units using standard OCI protocols.

### OCI Integration

ADS leverages the OCI distribution specification for content storage and retrieval:

1. Records are stored and transferred using OCI artifacts.
2. Any OCI distribution-compliant server can participate in the network.
3. Servers retrieve records directly from each other using standard OCI protocols.

While ADS uses zot as its reference OCI server implementation, the system works
with any server that implements the OCI distribution specification.

## Flow Diagrams

```mermaid
sequenceDiagram
    participant User
    participant DHT
    participant ServerA
    participant ServerB
    participant ServerC

    Note over ServerA,ServerC: Publication Phase
    ServerA->>ServerA: Generate record digest
    ServerA->>ServerA: Extract skills from record
    ServerA->>ServerA: Store record locally
    ServerA->>DHT: Announce digest + skills
    ServerB->>ServerB: Generate record digest
    ServerB->>ServerB: Extract skills from record
    ServerB->>ServerB: Store record locally
    ServerB->>DHT: Announce digest + skills
    DHT->>DHT: Update routing tables<br/>(skills→digests→servers)

    Note over User,ServerC: Discovery Phase
    User->>DHT: Query by skills
    DHT->>DHT: Search routing tables
    DHT->>User: Return matching digests<br/>+ server addresses
    User->>User: Select records
    User->>ServerA: Download record 1
    User->>ServerB: Download record 2
```


# Agent Directory Records Example

## Skill Tags (Taxonomy)
```yaml
skills:
  language:
    - text-generation
    - text-completion
    - text-summarization
    - text-translation
  vision:
    - image-generation
    - image-classification
    - object-detection
  audio:
    - speech-to-text
    - text-to-speech
  reasoning:
    - task-planning
    - decision-making
    - problem-solving
```

## Record Examples with Digests

### Text Generation Agent
```json
{
  "digest": "sha256:4e8c72f126b2e4a318911ba11b39432978d0611a56d53a2cfb6fdb42853df0e2",
  "skills": [
    "language/text-generation",
    "language/text-completion"
  ],
  "metadata": {
    "name": "gpt4-agent",
    "version": "1.0.0",
    "locator": {
      "type": "github",
      "url": "github.com/agntcy/agents/gpt4-agent"
    }
  }
}
```

### Vision Processing Agent
```json
{
  "digest": "sha256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
  "skills": [
    "vision/image-generation",
    "vision/image-classification"
  ],
  "metadata": {
    "name": "dall-e-agent",
    "version": "2.0.0",
    "locator": {
      "type": "github",
      "url": "github.com/agntcy/agents/dalle-agent"
    }
  }
}
```

### Multi-Modal Agent
```json
{
  "digest": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "skills": [
    "language/text-generation",
    "vision/image-generation",
    "reasoning/task-planning"
  ],
  "metadata": {
    "name": "multi-modal-agent",
    "version": "1.0.0",
    "locator": {
      "type": "github",
      "url": "github.com/agntcy/agents/multimodal-agent"
    }
  }
}
```

The digests are SHA-256 hashes of the record content, making them:
- Globally unique
- Content-addressable
- Collision-resistant
- Immutable