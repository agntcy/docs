## Agent Manifest

Agent Manifest is a descriptor that contains all the needed information to know how:
* Identify an agent
* Know its capabilities
* Consume its capabilities
* Deploy the agent

The Agent Manifest can be obtained from the Agent Directory or can be obtained through an [ACP call](#retrieve-agent-manifest-from-its-identifier).
Note that when the manifest is retrieved through ACP, the information about the deployment modes is superfluous, because it is already deployed.

### Agent manifest sections and examples

We present the details of a sample manifest through the various manifest sections.

<details>
<summary>Full sample manifest</summary>

[filename](docs/sample_manifests/mailcomposer.json ':include :type=code')

</details>

#### Agent Metadata

Agent Metadata section contains all the information about agent identification and a description of what the agent does.
It contains unique name which together with a version constitutes the unique identifier of the agent. The uniqueness must be guaranteed within the server it is part of and more generally in the Agent Directory domain it belongs to.

<details>
<summary>Sample manifest metadata section for the mailcomposer agent</summary>

```json
{
  "metadata": {
    "ref": {
      "name": "org.agntcy.mailcomposer",
      "version": "0.0.1",
      "url": "https://github.com/agntcy/acp-spec/blob/main/docs/sample_manifests/mailcomposer.json"
    },
    "description": "This agent is able to collect user intent through a chat interface and compose wonderful emails based on that."
  }
  ...
}
```

Metadata for a mail composer agent named `org.agntcy.mailcomposer` version `0.0.1`.

</details>

#### Agent Specs

Agent Specs section includes ACP invocation capabilities and the schema definitions for ACP interactions.

The ACP capabilities that the agent support, e.g. `streaming`, `callbacks`, `interrupts` etc.

The schemas of all the objects that this agent supports for:
   * Agent Configuration
   * Run Input
   * Run Output
   * Interrupt and Resume Payloads
   * Thread State

Note that these schemas are needed in the agent manifest, since they are agent specific and are not defined by ACP, i.e. ACP defines a generic JSON object for the data structures listed above.

<details>
<summary>Sample metadata specs section for the mailcomposer agent</summary>

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
* As input, it expects the next message of the chat from the user
* As output, it produces the next message of the chat from the agent
* As config it expects the style of the email to be written.

It supports one kind of interrupt, which is used to ask user for approval before sending the email. It provides subject, body, and recipients of the email as interrupt payload and expects approval as input to resume.

It supports a thread state which holds the chat history.

</details>
