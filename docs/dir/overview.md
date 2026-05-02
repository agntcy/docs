## The missing layer

Agents can't collaborate if they can't find each other. The agentic web needs an open, distributed, federated discovery layer — one that no single vendor controls, that works across every protocol and platform, and that any agent can participate in regardless of where or how it was built.

ADS is that layer. It is the discovery and collaboration infrastructure for the Internet of Agents: a federated registry where agents are found by what they *can do*, not what they are named. You publish your agent once; any node in the network can find it. No re-registration on individual platforms. No platform lock-in.

---

## 3 things that distinguish ADS

### 1. Capability-based discovery across organizational boundaries

Traditional service discovery — DNS, service meshes, container registries — works when you already know what you're looking for. Agents are different. You often know *what you need* before you know *which agent to call*.

ADS routes queries on a standardized, hierarchical skill taxonomy. A query for "find agents with image analysis capabilities" resolves across all federated nodes — crossing clouds, frameworks, and organizational boundaries — without knowing in advance which agents exist or where they're deployed. The DHT-based routing (libp2p Kad-DHT) scales to thousands of nodes and millions of records with no central authority required.

### 2. Protocol-agnostic interoperability

OASF records support protocol-specific extension modules, so an A2A agent and an MCP server can both be described in OASF, indexed by the same skill taxonomy, and returned by the same capability query. Each record specifies which protocol it uses, so you always know how to invoke what you find.

A developer building on LangGraph (A2A) and one building on LlamaIndex (MCP) can discover each other's agents through a single query, across organizational boundaries, with no custom integration work required.

### 3. Verifiable trust and provenance

Every record is content-addressed: its CID is a cryptographic hash of its content. Any modification produces a different CID.  This gives you tamper detection and natural versioning at no additional cost. Records can also be cryptographically signed using OIDC flows (including keyless signing via GitHub Actions) or private keys; signatures are logged to the [Rekor](https://docs.sigstore.dev/logging/overview/) transparency log via Sigstore.

For federation between organizations, ADS uses SPIFFE/SPIRE for zero-trust workload identity and mutual TLS, with no manual certificate management.

> **Important:** Signing is optional, not mandatory. An unsigned record can claim any author. For production use, enforce signature verification policies at the consumer level and automate signing in your CI/CD pipeline.

---

## Who is this for?

| If you are… | ADS helps you… |
|---|---|
| Building a multi-agent workflow | Replace hardcoded agent integrations with runtime capability discovery |
| Publishing an agent | Reach all federated consumers with a single publish operation |
| Running a platform on multiple clouds | Use vendor-neutral, OCI-compatible storage with no lock-in |
| Responsible for security or IT ops | Audit agent provenance; enforce signature policies before agents reach production |
| An org that needs both private and shared agents | Run a private node behind your firewall; federate selectively with the public network |

---

## What ADS is not

ADS can look at first glance like several things it isn't. This matters before you decide whether to use it.

| ADS is not… | What to use instead / why the distinction matters |
|---|---|
| A substitute for A2A or MCP | ADS sits *above* those protocols as the discovery layer. It is protocol-agnostic and supports A2A, MCP, and custom protocols through OASF extension modules. |
| Just another agent registry | Unlike platform-specific registries, ADS federates across organizations. One publish operation reaches the entire federated network — not just one vendor's ecosystem. |
| A message broker or transport layer | That is [SLIM](https://docs.agntcy.org/slim/overview/) (Secure Low-Latency Interactive Messaging), a separate AGNTCY component. |
| An orchestration engine | ADS does not schedule or manage agent execution. |
| A proprietary platform | ADS is open source (Apache 2.0) under the Linux Foundation. There is no central gatekeeper. |

The key distinction: A2A defines how agents *communicate*. MCP defines how agents *access tools*. Neither defines how agents *find each other*. ADS fills that gap.

---

## Flow diagram

>```mermaid
sequenceDiagram
    participant User
    participant DHT
    participant ServerA
    participant ServerB
    participant ServerC

    Note over ServerA,ServerC: Publication Phase
    ServerA->>ServerA: Generate record CID
    ServerA->>ServerA: Extract skills from record
    ServerA->>ServerA: Store record locally
    ServerA->>DHT: Announce CID + skills
    ServerB->>ServerB: Generate record CID
    ServerB->>ServerB: Extract skills from record
    ServerB->>ServerB: Store record locally
    ServerB->>DHT: Announce CID + skills
    DHT->>DHT: Update routing tables<br/>(skills→CIDs→servers)

    Note over User,ServerC: Discovery Phase
    User->>DHT: Query by skills
    DHT->>DHT: Search routing tables
    DHT->>User: Return matching CIDs<br/>+ server addresses
    User->>User: Select records
    User->>ServerA: Download record 1
    User->>ServerB: Download record 2


At its core, ADS performs two operations: **announce** and **discover**.

When you publish an agent record, ADS extracts the OASF skill taxonomy, generates a content-addressed CID, stores the record in an OCI-compliant registry, and announces the CID-to-skill and CID-to-server mappings to the DHT. When another agent (or developer) queries for a capability, the DHT resolves the query in two phases: skills → matching CIDs, then CIDs → the server nodes hosting those records. The client then pulls the full record directly from the optimal source.

This two-phase design means there is no central registry that must be online for discovery to work. Any node can go offline; the DHT re-routes around it.

---

## Quick start

Three paths, in ascending order of commitment:

### Query the public network (read-only)

A live, read-only public instance is available for exploration. Requires GitHub org membership in `github.com/agntcy`.

```bash
export DIRECTORY_CLIENT_SERVER_ADDRESS="prod.gateway.ads.outshift.io:443"
export DIRECTORY_CLIENT_AUTH_MODE="github"
dirctl auth login
dirctl search --skill "*"
```

> If you don't have org membership yet, you can publish and experiment using the staging environment: [github.com/agntcy/dir-staging](https://github.com/agntcy/dir-staging).

### Run locally

Deploy a full local node using Docker Compose or Helm. Suitable for development and testing.

```bash
# Using Helm
helm pull oci://ghcr.io/agntcy/dir/helm-charts/dir --version v1.1.0
helm upgrade --install dir oci://ghcr.io/agntcy/dir/helm-charts/dir --version v1.1.0
kubectl port-forward svc/dir-apiserver 8888:8888
```

→ [Full Getting Started guide](https://docs.agntcy.org/dir/getting-started/)

### Deploy and federate

Run a production node on AWS EKS and optionally join the federated public network.

→ → Production Deployment · Running a Federated Instance (see [docs.agntcy.org](https://docs.agntcy.org))

---

## Use cases

- **Dynamic multi-agent coordination.** An orchestrating agent queries ADS at runtime to find the best available specialist for a subtask — no hardcoded integrations, no manual wiring between frameworks.
- **Federated enterprise deployment.** Your internal node holds proprietary agents not shared externally. It federates with the public network so your agents can discover external agents while remaining private themselves.
- **CI/CD-integrated agent publishing.** On merge to main, your pipeline validates, signs, and publishes agent records to ADS automatically — using the [GitHub Actions provided in the repo](https://github.com/agntcy/dir/tree/main/.github/actions).
- **Agent marketplace.** Publish agents to the directory; consumers discover them by skill. No central approval process, no platform dependency.
- **Security and provenance audit.** Your IT or security team queries ADS for all deployed agents, checks signatures, and flags unsigned records before they reach production.

For an end-to-end reference implementation showing ADS alongside SLIM, Identity, and Observability, see [coffeeAgntcy](https://github.com/agntcy/coffeeAgntcy) — AGNTCY's reference application built around a multi-agent coffee supply chain scenario.

---

## Features

Each feature below is described by what it does and the problem it solves.

| Feature | What it does | Problem it solves |
|---|---|---|
| **Capability-based discovery** | Finds agents by OASF skill taxonomy, not by name or endpoint | You don't know which agent to call — only what you need it to do |
| **Distributed DHT routing** | Announces and resolves records via libp2p Kad-DHT across federated nodes | Centralized registries are single points of failure and governance bottlenecks |
| **Content-addressed naming (CIDs)** | Every record is identified by a cryptographic hash of its content | Any modification is detectable; records are immutable and globally unique without a central authority |
| **Cryptographic signing** | Records can be signed via OIDC, GitHub OIDC (keyless), or private keys; signatures logged to Rekor | Unsigned records can't be trusted in an open network; provenance must be verifiable |
| **OCI-based distributed storage** | Records stored and transferred as OCI artifacts; compatible with Docker Registry, Harbor, and cloud registries | Avoids new storage infrastructure; plugs into existing enterprise tooling |
| **SPIFFE/SPIRE federation** | Zero-trust workload identity and mTLS for inter-node communication | Cross-organizational federation needs cryptographic authentication without manual certificate management |
| **Runtime discovery** | Watches Kubernetes pods and Docker containers for OASF annotations; auto-indexes them | Dynamically deployed agents need to be discoverable without manual registration |
| **Multi-protocol support** | OASF extension modules carry A2A, MCP, and custom protocol metadata alongside capability data | A single query should surface agents regardless of how they were built |
| **MCP server integration** | Exposes ADS search, push, pull, and verify as MCP tools; works in Cursor, VS Code, Codex | Developers should be able to discover and verify agents without leaving their editor |

---

## Repository structure

The `agntcy/dir` repository is organized around five top-level concerns:

| Directory | Contents |
|---|---|
| `api/` | Protocol Buffer definitions and gRPC service interfaces for the Directory API |
| `cli/` | Source for `dirctl` — the primary command-line interface for interacting with ADS |
| `client/` | Go SDK client library (`github.com/agntcy/dir/client`) |
| `sdk/` | Python (`dir-py`) and JavaScript (`dir-js`) SDK implementations |
| `auth/` | Authentication middleware, including SPIFFE/SPIRE and GitHub OAuth integration |
| `mcp/` | Directory MCP server — exposes ADS functionality to MCP-compatible IDEs |
| `docs/` | Local documentation sources |
| `gui/` | Experimental graphical interface for Directory |

Deployable artifacts — `dir-apiserver`, `dir-ctl`, `dir-reconciler`, `dir-runtime-discovery`, `dir-runtime-server` — are built as Docker images and distributed via GitHub Packages (`ghcr.io/agntcy`). Helm charts are published as OCI artifacts.

→ [Full repository](https://github.com/agntcy/dir)

---

## Development and contributing

ADS is an open source project under Apache 2.0. Contributions are welcome across all components.

- **Issues and PRs:** [github.com/agntcy/dir/issues](https://github.com/agntcy/dir/issues)
- **Specification:** [spec.dir.agntcy.org](https://spec.dir.agntcy.org) (Internet Draft — feedback welcome via the spec repo)
- **Contributing guide:** AGNTCY Contributing Guide
- **Code of Conduct:** [github.com/agntcy/governance](https://github.com/agntcy/governance)

The CI pipeline runs unit tests, end-to-end tests, and CSIT (Continuous System Integration Testing) across versions and environments on every pull request.

---

## Known limitations and other resources

**Current limitations:**

- The public testbed at `prod.gateway.ads.outshift.io` is **read-only** and requires GitHub org membership in `github.com/agntcy`. Use [github.com/agntcy/dir-staging](https://github.com/agntcy/dir-staging) to publish agents without requesting membership first.
- ADS and SLIM specifications are published as IETF Internet Drafts — stable, but subject to revision before finalization.
- Advanced DHT performance optimization and extended cross-network federation protocols are under active development.

**Related resources:**

| Resource | What it covers |
|---|---|
| [OASF documentation](https://docs.agntcy.org/oasf/open-agentic-schema-framework/) | The schema used to describe agents in ADS records |
| [OASF skill taxonomy](https://schema.oasf.outshift.com) | Full list of valid skill IDs and names — required when writing OASF records |
| [SLIM overview](https://docs.agntcy.org/slim/overview/) | Secure transport layer for agent communication |
| [AGNTCY Identity](https://docs.agntcy.org/identity/identity/) | Cryptographically verifiable agent identity |
| [coffeeAgntcy](https://github.com/agntcy/coffeeAgntcy) | End-to-end reference application using ADS, SLIM, Identity, and Observability |
| [ADS Spec](https://spec.dir.agntcy.org) | Internet Draft specification |
| [AGNTCY blog](https://blogs.agntcy.org) | Technical deep-dives on ADS, SLIM, federation, and security |

---

## Get help

- **Documentation:** [docs.agntcy.org](https://docs.agntcy.org)
- **Slack:** [Join the AGNTCY community](https://join.slack.com/t/agntcy/shared_invite/zt-3hb4p7bo0-5H2otGjxGt9OQ1g5jzK_GQ)
- **GitHub Discussions:** [github.com/agntcy/dir/discussions](https://github.com/agntcy/dir/discussions)
- **Issues:** [github.com/agntcy/dir/issues](https://github.com/agntcy/dir/issues)

---
