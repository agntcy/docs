# Creating an Agent Record

Follow the steps below to ensure that your agent record is complete and
compliant.
The model provides a structured way to describe your record's features,
capabilities, and dependencies.

## Basic Information

Start by filling out the basic metadata of your record:

- `name`:
  Provide a descriptive name for your record.
- `description`:
  Provide a description for your record.
- `version`:
  Use semantic versioning to indicate the current version of your record.
- `schema_version`:
  Provide the OASF schema version the record needs to be valid against.
  Must be in semantic versioning format (see [https://semver.org/](https://semver.org/)), e.g., `"0.7.0"`.
- `authors`:
  List the authors in the `Name <email>` format.
  Replace `Your Name` and `you@example.com` with the appropriate details. Providing an email is optional.
- `created_at`:
  Use RFC 3339 format to specify when the record was created.

## Define Skills

The skills section outlines the capabilities of the agent record.
Retrieve skill definitions from the
[OASF skills catalog](https://schema.oasf.outshift.com/skill_categories).
Each skill must include the following:

- `name`:
  The name as a unique identifier (including the skill hierarchy) of a specific
  skill or capability (for example,
  `natural_language_processing/natural_language_generation/text_completion`).
- `id`:
  The unique identifier for the skill class.

You can add multiple skills to your record.

## Define Domains

The domains section outlines the domains in which your agent record excels.
Retrieve domain definitions from the
[OASF domains catalog](https://schema.oasf.outshift.com/domain_categories).
Each domain must include the following:

- `name`:
  The name as a unique identifier (including the domain hierarchy) of a specific
  domain (for example, `technology/network_operations`).
- `id`:
  The unique identifier for the domain class.

You can add multiple domains to your agent.

## Add Locators

The locators section provides references to the agent's source code or other
resources.
If the agent is packaged as a Docker container, provide the corresponding image
or registry URL.

You can also provide the source code:

```json
{
  "type": "source_code",
  "url": "https://github.com/agntcy/csit/tree/main/samples/crewai/simple_crew"
}
```

## Specify Modules

The modules section is critical for describing the features and operational
parameters of your record.
To ensure compatibility, you must select extensions from the
[OASF modules catalog](https://schema.oasf.outshift.com/module_categories).

## Validate and Finalize

Double-check that all fields are filled out accurately.
Ensure that extensions and skills are selected from the OASF schema to maintain
compatibility.
Use the [Draft-07](https://schema.oasf.outshift.com/schema/objects/record)
schema of the record or the
[validation endpoint](https://schema.oasf.outshift.com/doc/index.html#/Validation/SchemaWeb.SchemaController.validate_object)
of OASF to validate your record.
Test the agent's configuration to verify that it works as expected.

## Example Agent Record

Below is an example of an agent record for a tourist scheduling coordinator.

```json
{
  "name": "Tourist Scheduling Coordinator",
  "description": "Central scheduling coordinator that matches tourists with tour guides…",
  "version": "2.0.0",
  "schema_version": "1.0.0",
  "authors": ["AGNTCY <example@agntcy.org>"],
  "created_at": "2025-01-01T00:00:00Z",
  "domains": [
    {"name": "hospitality_and_tourism/tourism_management", "id": 1505}
  ],
  "skills": [
    {"name": "agent_orchestration/task_decomposition", "id": 1001},
    {"name": "agent_orchestration/agent_coordination", "id": 1004},
    {"name": "agent_orchestration/multi_agent_planning", "id": 1003}
  ],
  "modules": [
  ],
  "locators": [
    {"type": "source_code", "urls": ["https://github.com/agntcy/agentic-apps/tree/main/tourist_scheduling_system"]}
  ]
} 
```
