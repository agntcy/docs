# Agent Manifest

## Introduction

An Agent Manifest is a document that describes in detail the following:
* What the agent is capable of.
* How the agent can be consumed if provided as-a-service.
* How the agent can be deployed if provided as a deployable artifact.
* What are the dependencies of the agent, that is, which other agents it relies on.

The manifest is designed to be used by [Agent Connect Protocol](../syntactic_sdk/connect.md) and the Workflow Server and stored in the Agent Directory with the corresponding OASF extensions.

This document describes the principles of the Agent Manifest definition. Manifest definition can be found [here](https://github.com/agntcy/workflow-srv-mgr/blob/main/wfsm/spec/manifest.yaml)

Sample manifests can be found [here](https://github.com/agntcy/workflow-srv-mgr/tree/main/wfsm/spec/examples).

## Agent Manifest Structure

Agent Manifest includes the following sections:
* [Agent Identification and Metadata](#agent-identification-and-metadata)
* [Agent Interface Data Structure Specification](#agent-interface-data-structure-specification)
* [Agent Deployment and Consumption](#agent-deployment-and-consumption)
* [Agent Dependencies](#agent-dependencies)

### Agent Identification and Metadata

Agent Manifest must uniquely identify an agent within the namespace it is part of. This is done through a unique name and a version.

Agent Manifest must include a natural language description that describes what the agent is capable of doing. This allows user and potentially other agents to select the agent that best fits a given task.

Agent Manifest can include metadata that provides additional information about the agent, such as ownership, timestamps, tags, and so on.


<details>
<summary>Sample descriptor metadata section for the mailcomposer agent</summary>

```json
{
  "metadata": {
    "ref": {
      "name": "org.agntcy.mailcomposer",
      "version": "0.0.1",
      "url": "https://github.com/agntcy/acp-spec/blob/main/docs/sample_acp_descriptors/mailcomposer.json"
    },
    "description": "This agent is able to collect user intent through a chat interface and compose wonderful emails based on that."
  }
  ...
}
```

Metadata for a mail composer agent named `org.agntcy.mailcomposer` version `0.0.1`.

</details>


<a id="agent-interface-data-structure-specification"></a>
### Agent Interface Data Structure Specification
Agents willing to interoperate with other agents expose an interface that allow for invocation and configuration.

Agent Connect Protocol specifies a standard for this interface. However, it specifies methods to configure and invoke agents, but it does not specify the format of the data structures that an agent expects and produces for such configurations and invocations.

The specification of these data structures is included in what we call the Agent ACP descriptor, which can be provided by ACP itself, but it is also defined as part of the Agent Manifest.

Agent `specs` section includes ACP invocation capabilities, e.g. `streaming`, `callbacks`, `interrupts` etc.,  and the JSON schema definitions for ACP interactions:
   * Agent Configuration.
   * Run Input.
   * Run Output.
   * Interrupt and Resume Payloads.
   * Thread State.

<details>
<summary>Sample  specs section for the mailcomposer agent</summary>

```json
{
  ...
    "specs": {
      "capabilities": {
        "threads": true,
        "interrupts": true,
        "callbacks": true
      },
      "input": {
        "type": "object",
        "description": "Agent Input",
        "properties": {
            "message": {
                "type": "string",
                "description": "Last message of the chat from the user"
            }
        }
      },
      "thread_state": {
        "type": "object",
        "description": "The state of the agent",
        "properties": {
          "messages": {
            "type": "array",
            "description": "Full chat history",
            "items": {
                "type": "string",
                "description": "A message in the chat"
            }
          }
        }
      },
      "output": {
        "type": "object",
        "description": "Agent Input",
        "properties": {
            "message": {
                "type": "string",
                "description": "Last message of the chat from the user"
            }
        }
      },
      "config": {
        "type": "object",
        "description": "The configuration of the agent",
        "properties": {
          "style": {
            "type": "string",
            "enum": ["formal", "friendly"]
          }
        }
      },
      "interrupts": [
        {
          "interrupt_type": "mail_send_approval",
          "interrupt_payload": {
            "type": "object",
            "title": "Mail Approval Payload",
            "description": "Description of the email",
            "properties": {
              "subject": {
                "title": "Mail Subject",
                "description": "Subject of the email that is about to be sent",
                "type": "string"
              },
              "body": {
                "title": "Mail Body",
                "description": "Body of the email that is about to be sent",
                "type": "string"
              },
              "recipients": {
                "title": "Mail recipients",
                "description": "List of recipients of the email",
                "type": "array",
                "items": {
                    "type": "string",
                    "format": "email"
                }
              }
            },
            "required": [
              "subject",
              "body",
              "recipients"
            ]
          },
          "resume_payload": {
            "type": "object",
            "title": "Email Approval Input",
            "description": "User Approval for this email",
            "properties": {
              "reason": {
                "title": "Approval Reason",
                "description": "Reason to approve or decline",
                "type": "string"
              },
              "approved": {
                "title": "Approval Decision",
                "description": "True if approved, False if declined",
                "type": "boolean"
              }
            },
            "required": [
              "approved"
            ]
          }
        }
      ]
    }
  ...
}
```
The agent supports threads, interrupts, and callback.

It declares schemas for input, output, and config:
* As input, it expects the next message of the chat from the user.
* As output, it produces the next message of the chat from the agent.
* As config it expects the style of the email to be written.

It supports one kind of interrupt, which is used to ask user for approval before sending the email. It provides subject, body, and recipients of the email as interrupt payload and expects approval as input to resume.

It supports a thread state which holds the chat history.

</details>

<a id="agent-deployment-and-consumption"></a>
### Agent Deployment and Consumption

Agents can be provided in two different forms, which we call deployment options:

* **As a service**: a network endpoint that exposes an interface to the agent (for example, Agent Connect Protocol).
* **As a deployable artifact**, for example:
   * A docker image, which once deployed exposes an interface to the agent (for example, Agent Connect Protocol).
   * A source code bundle, which can be executed within the specific runtime and framework it is built on.

The same agent can support one or more deployment options.

Agent Manifest currently supports three deployment otions:
* Source Code Deployment: In this case the agent can be deployed starting from its code. For this deployment mode, the manifest provides:
    * The location where the code is available
    * The framework used for this agent
    * The framework specific configuration needed to run the agent.
* Remote Service Deployment: In this case, the agent does not come as a deployable artefact, but it's already deployed and available as a service. For this deployment mode, the manifest provides:
    * The network endpoint where the agent is available through the ACP
    * The authentication used by ACP for this agent
* Docker Deployment: In this case the agent can be deployed starting from a docker image. It is assumed that once running the docker container expose the agent through ACP. For this deployment mode, the manifest provides:
    * The agent container image
    * The authentication used by ACP for this agent

<details>
<summary>Sample manifest dependency section for the mailcomposer agent</summary>

```json
{
  ...
    "deployments": [
      {
        "type": "source_code",
        "name": "src",
        "url": "git@github.com:agntcy/mailcomposer.git",
        "framework_config": {
          "framework_type": "langgraph",
          "graph": "mailcomposer"
        }
      }
    ]
  ...
}
```

Mailcomposer agent in the example above comes as code written for LangGraph and available on Github.

<a id="agent-dependencies"></a>
</details>

### Agent Dependencies

An agent may depend on other agents, which means that at some point of its execution it needs to invoke them to accomplish its tasks. We refer to these other agents as **sub-agents**.  A user who wants to use the agent, needs to know this information and check that the dependencies are satisfied, that is, make sure that the sub-agents are available.
This may imply simply checking that sub-agents are reachable or deploying them, according to the deployment modes they support.

The Agent Manifest must include a list of all sub-agents in the form of a list of references to their manifests.

Note the recursive nature of Agent Manifests that can point in turn to other Agent Manifests as dependencies.

<details>
<summary>Sample manifest dependency section for the mailcomposer agent</summary>

```json
{
  ...
    "dependencies": [
      {
        "name": "org.agntcy.sample-agent-2",
        "version": "0.0.1"
      },
      {
        "name": "org.agntcy.sample-agent-3",
        "version": "0.0.1"
      }
    ]
  ...
}
```

Mailcomposer agent in the example above depends on `sample-agent-2` and `sample-agent-3`.

</details>

<a id="agent-deployments"></a>


