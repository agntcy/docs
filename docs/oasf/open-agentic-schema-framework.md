# Open Agentic Schema Framework

The [Open Agentic Schema Framework (OASF)](https://schema.oasf.agntcy.org/) is a standardized schema system for
defining and managing AI agent capabilities, interactions, and metadata. It
provides a structured way to describe agent attributes, capabilities, and
relationships using attribute-based taxonomies. The framework includes
development tools, schema validation, and hot-reload capabilities for rapid
schema development, all managed through a Taskfile-based workflow and
containerized development environment. The OASF serves as the foundation for
interoperable AI agent systems, enabling consistent definition and discovery of
agent capabilities across distributed systems.

## Features

The OASF defines a set of standards for AI agent content representation that aims to:

- Define common data structure to facilitate content standardisation, validation, and interoperability.
- Ensure unique agent identification to address content discovery and consumption.
- Provide extension capabilities to enable third-party features.

A core component in OASF is to implement data types and core objects that define the skills of autonomous agents. This component helps in announcing and discovering agents with these skills across various data platforms.

A convenient way to browse and use the OASF schema is through the [Open Agentic Schema Framework Server](oasf-server.md).

See [Creating an Agent Record](../how-to-guides/agent-record-guide.md) for more information on the Agent Record.

The current skill set taxonomy is described in [Taxonomy of AI Agent Skills](taxonomy.md).

The guidelines to upgrade and maintain OASF are outlined in the [OASF Contribution Guide](workflow.md).