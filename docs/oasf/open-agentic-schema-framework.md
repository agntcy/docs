# Open Agentic Schema Framework

The [Open Agentic Schema Framework (OASF)](https://schema.oasf.outshift.com/) is
a common vocabulary for describing and discovering agentic resources.

OASF defines a standard, extensible way to describe what an agentic resource,
such as an agent or an MCP server, can do.
Other systems can then find, validate, and use that resource without custom
integration work.
Publishers describe resources as OASF records.
A service such as the [Agent Directory Service]([[ agntcy.dir_url ]]) can store
and search them, or systems can exchange them directly.

## Scope and Role of OASF

OASF is a schema framework.
It defines how the attributes of an agentic resource are described:
the structure of a record, the taxonomies used to annotate it, and the
extension mechanism used to add more detail.

OASF is:

- A schema for describing agentic resources, with a core
  [record object](https://schema.oasf.outshift.com/objects/record).
- A set of taxonomies of skills and domains for annotating records.
- A modular extension mechanism (modules) for adding detail to a record,
  such as MCP servers or A2A card details.
- A validation framework, so any record can be checked against the schema.

OASF is not:

- A runtime or an agent framework. OASF describes agents, and a framework runs
  them.
- A communication protocol. Agents communicate over A2A, MCP, SLIM, or any other
  protocol, and OASF records can describe how.
- A registry. Records are stored and discovered through a service such as the
  [Agent Directory Service]([[ agntcy.dir_url ]]).
- A definition of what every record must contain.
  Beyond the core record attributes, the content of a record is up to the
  publisher, who chooses the skills, domains, and modules that fit the resource.

## Key Strengths

- OASF is extensible: any capability can be added to a record as a module, and
  the schema itself can be extended with private extensions that still benefit
  from validation.
- OASF is discoverable: skills and domains come from shared taxonomies, so
  records can be searched with the same vocabulary regardless of who published
  them.
- OASF is interoperable: records can describe and be translated to formats such
  as A2A cards and MCP configurations, and OASF skills and domains can be
  embedded in those formats.

## Key Concepts

At the core of OASF is the
[record object](https://schema.oasf.outshift.com/objects/record), which serves
as the primary data structure for representing collections of information and
metadata relevant to agentic AI applications.

A record consists of:

- Basic information: name, description, version, authors, creation time, and the
  OASF schema version it conforms to.
- Skills: what the resource can do, taken from the
  [skills taxonomy](https://schema.oasf.outshift.com/skill_categories).
- Domains: where the resource is useful, taken from the
  [domains taxonomy](https://schema.oasf.outshift.com/domain_categories).
- Locators: where the resource can be found, such as a source code repository or
  a container image.
- Modules: additional, composable details about the resource, taken from the
  [modules catalog](https://schema.oasf.outshift.com/module_categories).

## What You Can Describe

The core record is enough to announce a resource and make it discoverable.
Modules add the detail needed to use it.

| To describe...                   | Use                                                                                       |
|----------------------------------|-------------------------------------------------------------------------------------------|
| Any resource, at a minimum       | The core record: basic information, skills, domains, and locators.                        |
| MCP servers the agent depends on | The MCP module, which describes the MCP servers required to run and interact with it.     |
| An A2A card                      | The A2A module, which describes the card details for communication over the A2A protocol. |
| Language model behavior          | The Language Model modules, such as prompts and agent skills.                             |
| Agent structure                  | The Agent Spec module, which describes the structure of agentic systems and workflows.    |
| Observability and evaluation     | The Observability and Evaluation modules.                                                 |
| Anything else                    | A [private extension](contributing.md#oasf-extensions) of the schema.                     |

Runtime and manifest information belongs in the record as well, through its
locators and modules, so that a consuming system can find a record and have what
it needs to use the resource.

To embed only the skills and domains of an artifact in another format, see the
[discovery extension](discovery-extension.md).
To convert a record to an MCP or A2A configuration, see
[translation](translation.md).

## Who Should Use OASF

OASF is most useful if one of these describes you:

- You publish agentic resources and want other systems and developers to find
  them by capability.
- You build systems that consume agentic resources and need to search for,
  select, and connect to the right ones at runtime.
- You operate a catalog or registry and need a consistent, validated record
  format across many publishers.
- You maintain your own agent format or protocol and want it to interoperate
  with others through a shared vocabulary.

Typical scenarios:

- A developer publishes an agent with its skills and MCP dependencies, and
  other developers search for it by skill.
- A running multi-agent system queries a directory for the right agent, and uses
  the record to find everything it needs to connect to it.
- An organization hosts its own OASF server with private extensions, and uses it
  to validate the records of its internal agents.

## Our Point of View

- Skills are the core of discovery. What a resource can do is the most useful
  thing to search by, so OASF puts skills and domains at the center of every
  record.
- A framework for describing agentic resources must be extensible. The agentic
  ecosystem evolves quickly, so new capabilities are added as modules and
  extensions, not by changing the core.
- Interoperability comes from a shared vocabulary. OASF does not replace
  existing protocols and formats. It gives systems a common way to describe
  resources, whatever format and runtime they use.

OASF is highly inspired from
[OCSF (Open Cybersecurity Schema Framework)](https://ocsf.io/) not only in terms of data
modeling philosophy but also in terms of implementation.
The server is a derivative work of OCSF schema server and the schema update
workflows reproduce those developed by OCSF.

## Get Started

1. Browse the schema in the
   [OASF server](https://schema.oasf.outshift.com), hosted by Outshift by Cisco.
2. Create your first record by following
   [Creating an Agent Record](agent-record-guide.md).
3. [Validate](validation.md) the record against the schema.
4. Publish and discover records with the
   [Agent Directory Service]([[ agntcy.dir_url ]]).

To work with records in code, see the [OASF SDK](oasf-sdk.md).
To deploy your own schema server, locally or as a hosted service, see the
[server's guide](oasf-server.md).

## Schema Expansion and Contributions

OASF is designed with extensibility in mind and is expected to evolve to capture
new use cases and capabilities.
A key area of anticipated expansion includes the definition and management of
skills, domains, and modules for agentic AI records.

We welcome contributions from the community to help shape the future of OASF.
For detailed guidelines on how to contribute, including information on proposing
new features, reporting bugs, and submitting code, see the
[contributing guide](contributing.md).

OASF can be extended with private schema extensions, allowing you to leverage
all features of the framework, such as validation.
See the relevant section in the
[contributing guide](contributing.md#oasf-extensions) for instructions on adding
an extension to the schema.
An OASF instance with schema extensions can be hosted, allowing you to use your
own schema server for record validation.

The current skill set taxonomy is described in
[Taxonomy of AI Agent Skills](https://schema.oasf.outshift.com/skill_categories).
