# Architecture

We introduce below the main logical components that are used by Phoenix project.

## SDKs

Building refers to a process of obtaining an agent data model artifact from a source such as 
source code or GitHub repository. 
Build process can be executed locally or remotely depending on the user's choice.
BuiltKit SDK provides the necessary tooling such as APIs, CLIs, programming-language specific bindings and 
extensions required to build an agent data model from source.
It also enables the development of the tooling needed to support different build sources such as IDE extensions, UI uploads, etc.
Similarly to BuildKit SDK, API SDK provides the necessary tooling to interact with the rest of the Phoenix project services.

## Storage

Storage service provides the necessary API to store and retrieve agent data model contents.
Storage providers such as content-addressable storage, distributed hash table, or other key-value storage systems
are supported. For the storage provider, OCI registry will be used.
OCI Registries are distributed services and provide content-addressing that uniquely identifies files by
their cryptographic hash, wallowing them to be retrieved from any node in the
network that has a copy.
This approach enhances data availability, reduces
reliance on any single point of failure, and enables efficient and secure file
sharing across the network.
OCI Registries also integrates seamlessly with other technologies, and are very prevalent in modern computing,
ensuring usage and addressing adoption by levering existing robust internet infrastructure.

[Project ZOT by Cisco](https://github.com/project-zot/zot) offers a viable OCI registry implementation which can be the
first supported OCI registry provider for the storage service.

## Security

Content integrity is provided by the OCI registry storage service by design while data
authenticity and provenance is provided by the associated Public Key Infrastructure used on the client-side
to sign the generated agent data models.
Security service provides verification capabilities for agent data models.

## Directory

This service is a gateway to access storage and security services, while also
enabling additional optional services. Service node provides a common RPC endpoint
which executes basic operations such as data publication, retrieval
and a number of security validation operations such as integrity, provenance
and ownership.

### Announcer Service

Announcer service provides an PubSub API for relevant operations performed by the Directory service.
This can include a number of different events such as publication of a new agent data model, its removal.
It is used as a supporting service for other services that compose Directory service.

### Search Service

Search service provides advanced search capabilities over published agent data models.
For example, users may be able to find agents that match given constraints and capabilities in order to find
a matching agent for given use-cases.
Search service leverages Announcer Service for its indexing tasks.

### Web Service

Web service exposes the necessary logic to support the creation of services in the form
of dashboard related to agent data models content generation, publication, and consumption.
It leverages both the Search service to provide more granular search capabilities, but also
its own Listing service for exact matching queries or relational data.
