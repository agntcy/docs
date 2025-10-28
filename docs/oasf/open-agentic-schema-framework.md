# Open Agentic Schema Framework

The [Open Agentic Schema Framework (OASF)](https://schema.oasf.outshift.com/) is
a standardized schema system for defining and managing AI agent capabilities,
interactions, and metadata.
It provides a structured way to describe agent attributes, capabilities, and
relationships using attribute-based taxonomies.
The framework includes development tools, schema validation, and hot-reload
capabilities for rapid schema development, all managed through a Taskfile-based
workflow and containerized development environment.
The OASF serves as the foundation for interoperable AI agent systems, enabling
consistent definition and discovery of agent capabilities across distributed
systems.

OASF is highly inspired from
[OCSF (Open Cybersecurity Schema Framework)](https://ocsf.io/) in terms of data
modeling philosophy but also in terms of implementation.
The server is a derivative work of OCSF schema server and the schema update
workflows reproduce those developed by OCSF.

## Features

OASF defines a set of standards for AI agent content representation that aims
to:

- Define common data structure to facilitate content standardization,
  validation, and interoperability.
- Ensure unique agent identification to address content discovery and
  consumption.
- Provide extension capabilities to enable third-party features.

## Key Concepts

At the core of OASF is the
[record object](https://schema.oasf.outshift.com/objects/record), which serves
as the primary data structure for representing collections of information and
metadata relevant to agentic AI applications.

OASF records can be annotated with **skills** and **domains** to enable
effective announcement and discovery across agentic systems.
Additionally, **modules** provide a flexible mechanism to extend records with
additional information in a modular and composable way, supporting a wide range
of agentic use cases.

## Schema Expansion and Contributions

The Open Agentic Schema Framework (OASF) is designed with extensibility in mind
and is expected to evolve to capture new use cases and capabilities.
A key area of anticipated expansion includes the definition and management of
**Skills**, **Domains** and **Modules** for AI agentic records.

We welcome contributions from the community to help shape the future of OASF.
For detailed guidelines on how to contribute, including information on proposing
new features, reporting bugs, and submitting code, please refer to our
[contributing guide](contributing.md).

OASF can be extended with private schema extensions, allowing you to leverage
all features of the framework, such as validation.
See the relevant section in the
[contributing guide](contributing.md#oasf-extensions) for instructions on adding
an extension to the schema.
An OASF instance with schema extensions can be hosted, allowing you to use your
own schema server for record validation.

Alternatively, records can be extended by adding arbitrary JSON objects to the
`modules` list, using module names that do not conflict with existing OASF
modules.
However, this approach is the least recommended, as validation will be skipped
for these modules if the record is validated against the standard OASF schema.

## Useful Links

A convenient way to browse and use the OASF schema is through the
[Open Agentic Schema Framework Server](https://schema.oasf.outshift.com) hosted
by Outshift by Cisco.

To deploy the server either locally or as a hosted service, see the
[server's guide](oasf-server.md) for more information.

See [Creating an Agent Record](../how-to-guides/agent-record-guide.md) for more
information on the Agent Record.

The current skill set taxonomy is described in
[Taxonomy of AI Agent Skills](https://schema.oasf.outshift.com/skill_categories).
