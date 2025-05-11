# Creating an Agent Data Model

Follow the steps below to ensure that your data model is complete and compliant.
The model provides a structured way to describe your agent's features, capabilities, and dependencies.
You can find the template for the data model [here](https://github.com/agntcy/csit/blob/main/samples/crewai/simple_crew/model.json).

## Basic Information

Start by filling out the basic metadata of your agent:

* `name`: Provide a descriptive name for your agent.
* `version`: Use semantic versioning to indicate the current version of your agent.
* `authors`: List the authors in the `Name <email>` format. Replace `Your Name` and `you@example.com` with the appropriate details.
* `created_at`: Use ISO 8601 format to specify when the agent was created.

## Define Skills

The skills section outlines your agent’s capabilities. Retrieve skills definitions from the [OASF schema catalog](https://schema.oasf.agntcy.org). Each skill must include the following:

* `category_name`: The category which the skill belongs to (for example, Natural Language Processing).
* `category_uid`: The unique identifier for the category.
* `class_name`: The specific skill or capability (for example, Text Completion or Problem Solving).
* `class_uid`: The unique identifier for the class.

You can add multiple skills to your agent.

## Add Locators

The locators section provides references to the agent's source code or other resources. If the agent is packaged as a Docker container, provide the corresponding image or registry URL.

You can also provide the source code:

```json
    {
      "type": "source-code",
      "url": "https://github.com/agntcy/csit/tree/main/samples/crewai/simple_crew"
    }
```

## Specify Extensions

The extensions section is critical for describing the features and operational parameters of your agent. To ensure compatibility, you must select extensions from the [OASF main features catalog](https://schema.oasf.agntcy.org/main_features?extensions). Examples of common extensions are the following:

1. Runtime Framework  
    Defines the runtime environment for the agent.

1. Observability (Logging and Metrics)  
    Tracks logs and performance metrics.

1. Memory and Orchestration  
    Configure the agent's memory and orchestration behavior.

1. Language Runtime  
    Define the programming language and version used by the agent:

1. I/O Mapper  
    Describe the input/output structure of the agent:

1. LLM Configuration  
    If your agent uses a language model, provide the model details and endpoint.

1. Evaluation  
    Indicate the evaluation mechanism for your agent.


## Validate and Finalize

Double-check that all fields are filled out accurately.
Ensure that extensions and skills are selected from the OASF schema to maintain compatibility.
Test the agent's configuration to verify that it works as expected.
