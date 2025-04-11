# Getting started with AGNTCY compoenents: build your first app

This tutorial guides you through the process of building a distributed multi-agent application using [LangGraph](https://www.langchain.com/Langgraph) and leveraging [Agent Connect Protocol (ACP)](https://docs.agntcy.org/pages/syntactic_sdk/connect.html) and other **AGNTCY** components and tools.

The sample app used for this tutorial is a **Marketing Campaign Manager** agent. A "pre-cooked" version of this application is available [here](https://github.com/agntcy/acp-sdk/tree/main/examples/marketing-campaign).


> For this tutorial we are using LangGraph, but other frameworks can also be used.


## Overview
The **Marketing Campaign Manager** we are building implements a LangGraph graph which:
* Interact with a user to gather the description of the email marketing campaign they wants to launch.
* Uses an already existing [Mail Composer Agent](https://github.com/agntcy/acp-sdk/tree/main/examples/mailcomposer), capable of composing emails for the marketing campaign. This agent is written using LangGraph, it provides a Agent Manifest which allows to deploy it through the Agent Workflow Server and be consumed through ACP.
* Uses an already existing [Email Reviewer Agent](https://github.com/agntcy/acp-sdk/tree/main/examples/email_reviewer) capable of revieving an email and adjust it for a specific target audience. This agent is written using [LlamaIndex](https://www.llamaindex.ai/framework) and similarly to the previous agent, it provides a Agent Manifest which allows to deploy it through the [Agent Workflow Server](https://docs.agntcy.org/pages/agws/workflow_server.html) and be consumed through ACP.
* Uses [Twilio Sendgrid](https://sendgrid.com/) API to deliver the marketing campaign email to the intended recipient. We will consume this API leveraging the capabilities of the [API Bridge Agent](https://docs.agntcy.org/pages/syntactic_sdk/api_bridge_agent.html).


This tutorial is structured in the following steps:

1. [Create a Basic LangGraph Skeleton Application](#step-1-create-a-basic-LangGraph-skeleton-application): Set up a LangGraph application structure to serve as the base of your multi-agent software.

2. [Generate Models from Agent Manifests](#step-2-generate-models-from-agent-manifests): Use agent manifests to generate models defining data structures and interfaces.

3. [State Definition](#step-3-state-definition): Create states to manage the flow of your multi-agent software (MAS).

4. [Multi-Agent Application Development](#step-4-multi-agent-application-development): Use ACP SDK to integrate ACP nodes into your LangGraph application.

5. [API Bridge Integration](#step-5-api-bridge-integration): Connect natural language outputs to structured API requests.

6. [I/O Mapper Integration](#step-6-io-mapper-integration): Adjust inputs and outputs between different agents such that they match in format and meaning.

### Final Thoughts

- [Resulting Graph and Conclusion](#resulting-graph-and-conclusion): Review the complete graph and summarize the key takeaways from this tutorial.


## Prerequisites

- A working installation of [Python](https://www.python.org/) 3.9 or higher
- [Poetry](https://pypi.org/project/poetry/) v2 or greater
- [ACP SDK](https://github.com/agntcy/acp-sdk): Includes a CLI for generating models, OpenAPI specifications, and validating agent manifests


## Step 1: Create a Basic LangGraph Skeleton Application

Begin by setting up a **simple LangGraph** skeleton application with the following nodes:

*Start, Mail Composer, Email Reviewer, Send Mail, and End*


![Skeleton LangGraph Application](./_static/marketing_campaign_skeleton.png)

This setup is a basic framework with **placeholders for each task** in the workflow. It sets the stage for **transforming** these nodes into remote **ACP nodes**, allowing the interaction with **real remote agents**.

The ultimate goal of this application is to compose and review emails that will be sent to a mail recipient. Each node represents a task to be performed in this process, from composing the email to reviewing it, and finally sending it.
### Skeleton Code Example

```python
# marketing_campaign_skeleton.py

from LangGraph.graph import StateGraph, START, END
from LangGraph.graph.state import CompiledStateGraph
from langchain_core.runnables.graph import MermaidDrawMethod
from pydantic import BaseModel, Field
from typing import Optional, List

# Define the overall state with placeholders for future use
class OverallState(BaseModel):
    messages: List[str] = Field([], description="Chat messages")
    has_composer_completed: Optional[bool] = Field(None, description="Flag indicating if the mail composer has successfully completed its task")
    mailcomposer_output: Optional[str] = Field(None, description="Output from Mail Composer")
    email_reviewer_output: Optional[str] = Field(None, description="Output from Email Reviewer")
    sendgrid_result: Optional[str] = Field(None, description="Result from SendGrid API call")

def mail_composer(state: OverallState) -> OverallState:
    # Placeholder logic for composing mail
    print("Composing mail...")
    state.mailcomposer_output = "Draft email content"
    state.has_composer_completed = True
    return state

def email_reviewer(state: OverallState) -> OverallState:
    # Placeholder logic for reviewing email
    print("Reviewing email...")
    state.email_reviewer_output = "Reviewed email content"
    return state

def send_mail(state: OverallState) -> OverallState:
    # Placeholder logic for sending email
    print("Sending email...")
    state.sendgrid_result = "Email sent successfully"
    return state

# Build the state graph with placeholder nodes
def build_skeleton_graph() -> CompiledStateGraph:
    sg = StateGraph(OverallState)

    # Add placeholder nodes
    sg.add_node(mail_composer)
    sg.add_node(email_reviewer)
    sg.add_node(send_mail)

    # Define the flow of the graph
    sg.add_edge(START, mail_composer.__name__)
    sg.add_edge(mail_composer.__name__, email_reviewer.__name__)
    sg.add_edge(email_reviewer.__name__, send_mail.__name__)
    sg.add_edge(send_mail.__name__, END)

    graph = sg.compile()
    graph.name = "Marketing Campaign Manager"
    with open("marketing_campaign_skeleton.png", "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
        ))
    return graph

# Compile and skeleton graph
if __name__ == "__main__":
    graph = build_skeleton_graph()
    print("Skeleton graph compiled successfully.")
```

Follow the guide [here](https://langchain-ai.github.io/LangGraph/tutorials/introduction/#part-1-build-a-basic-chatbot) to know how build a LangGraph application.


## Step 2: Generate Models from Agent Manifests

In this step, you will **generate** models based on the agent manifests to define the **input, output and config schemas** for each agent involved in MAS. The models are created using the `acp generate-agent-models` cli command, which reads the agent manifest files and produces Python files that encapsulate the agent's data structures and interfaces necessary for integration.

### What is an Agent Manifest?

An Agent Manifest is a detailed document outlining an agent's capabilities, deployment methods, data structure specifications and dependencies on other agents. It provides** essential information** for ensuring agents can communicate and work together within the **Agent Connect Protocol** and **Workflow Server ecosystem**. [Learn more](https://docs.agntcy.org/pages/agws/manifest.html)

### Schema and Type Generation

We will use two agents whose manifests ([Mail Composer Manifest](https://github.com/agntcy/acp-sdk/blob/main/examples/mailcomposer/deploy/mailcomposer.json) and [Email Reviewer Manifest](https://github.com/agntcy/acp-sdk/blob/main/examples/email_reviewer/deploy/email_reviewer.json)) are provided within the [ACP SDK](https://github.com/agntcy/acp-sdk) repository. To proceed, you need to clone the repository and execute the following commands within the cloned directory:

```bash
# Install dependencies
export POETRY_VIRTUALENVS_IN_PROJECT=true
poetry install

# Activate the virtual environment
source .venv/bin/activate

# Generate models for Mail Composer
poetry run acp generate-agent-models examples/mailcomposer/deploy/mailcomposer.json --output-dir examples/marketing-campaign/src/marketing_campaign --model-file-name mailcomposer.py

# Generate models for Email Reviewer
poetry run acp generate-agent-models examples/email_reviewer/deploy/email_reviewer.json --output-dir examples/marketing-campaign/src/marketing_campaign --model-file-name email_reviewer.py
```

Generated model files:
- [Mail Composer Model](https://github.com/agntcy/acp-sdk/blob/main/examples/marketing-campaign/src/marketing_campaign/mailcomposer.py)
- [Email Reviewer Model](https://github.com/agntcy/acp-sdk/blob/main/examples/marketing-campaign/src/marketing_campaign/email_reviewer.py)

General structure:
- **Pydantic Models**: Each file includes Pydantic models that represent the **configuration**, **input**, and **output** schemas,  enforcing type validation.
- **Input, Output and Config Schemas**: These schemas handle incoming and outgoing data and the configuration of the agent.


## Step 3: State Definition

State management is fundamental to **track progress and outcomes** so that each agent can interact effectively with others following the right workflow. In this step, we will define the states necessary to manage the flow of your multi-agent software.

### Understanding State in Multi-Agent Systems

State in multi-agent systems refers to the structured data that represents the **current status of the application**. It includes information about the inputs, outputs, and **intermediate results** of each agent's operations. Effective state management allows for the **coordination and synchronization of agent activities**.

### State Definition in the Marketing Campaign Example

In the marketing campaign example, the state is defined in [state.py](https://github.com/agntcy/acp-sdk/blob/main/examples/marketing-campaign/src/marketing_campaign/state.py). This file outlines the data structures that will be used to track the flow and results of the campaign tasks.

#### Key Components:

- **OverallState**: This is the main class that encapsulates various aspects of the state, including:
  -  messages
  -  operation logs
  -  completion flags for different tasks. 

  It serves as the central repository for tracking the application's progress.

    ```python
    class OverallState(BaseModel):
        messages: List[mailcomposer.Message] = Field([], description="Chat messages")
        operation_logs: List[str] = Field([],
                                            description="An array containing all the operations performed and their result. Each operation is appended to this array with a timestamp.",
                                            examples=[["Day DD HH:MM:SS Operation performed: email sent Result: OK",
                                                    "Day DD HH:MM:SS Operation X failed"]])
        has_composer_completed: Optional[bool] = Field(None, description="Flag indicating if the mail composer has successfully completed its task")
        has_reviewer_completed: Optional[bool] = None
        has_sender_completed: Optional[bool] = None
        mailcomposer_state: Optional[MailComposerState] = None
        email_reviewer_state: Optional[MailReviewerState] = None
        target_audience: Optional[email_reviewer.TargetAudience] = None
        sendgrid_state: Optional[SendGridState] = None
    ```

- **MailComposerState, MailReviewerState, SendGridState**: These classes represent the specific states of individual components within the application. Each state class manages its own input and output data to take track of each task's progress and results.

    ```python

    from agntcy_acp.LangGraph.api_bridge import APIBridgeOutput, APIBridgeInput
    from marketing_campaign import mailcomposer
    from marketing_campaign import email_reviewer

    class MailComposerState(BaseModel):
        input: Optional[mailcomposer.InputSchema] = None
        output: Optional[mailcomposer.OutputSchema] = None

    class MailReviewerState(BaseModel):
        input: Optional[email_reviewer.InputSchema] = None
        output: Optional[email_reviewer.OutputSchema] = None

    class SendGridState(BaseModel):
        input: Optional[APIBridgeInput] = None
        output: Optional[APIBridgeOutput] = None
    ```

> **Note**: The `input` and `output` fields of the `MailComposerState` and `MailReviewerState` are **directly derived from the schemas generated** in [Step 2](#step-2-generate-models-from-agent-manifests) using the agent manifests. This means these states are automatically created based on the manifests, and there is no need to manually define them.



## Step 4: Multi-Agent Application Development

Now, let's enhance the skeleton setup by **transforming** LangGraph nodes **into ACP nodes** using `agntcy_acp` **sdk**. ACP nodes allow network communication between agents by using the [Agent Connect Protocol (ACP)](https://spec.acp.agntcy.org/#/docs/README?id=start-a-run-of-an-agent-and-poll-for-completion).
This enables remote invocation, configuration, and output retrieval with the goal of allowing heterogeneous and distributed agents to interoperate.


### Why Use ACP Nodes?

1. **Remote Execution**: ACP nodes run on a Workflow Server, making it possible to execute tasks remotely.
2. **Technology Independence**: ACP allows agents to be implemented in various technologies, such as LangGraph, LlamaIndex, etc., without compatibility issues. This gives the flexibility to choose the best agent for the specific task.
3. **Interoperability**: ACP ensures that agents can communicate and work together, regardless of the underlying technology, by adhering to a standardized protocol.
<!-- [Learn more](https://docs.agntcy.org/pages/syntactic_sdk/agntcy_acp_reference.html#acpnode) -->


### Add Mail Composer and Email Reviewer ACP Nodes

To integrate the Mail Composer and Email Reviewer as ACP nodes, we first need to fill in the client configuration for the remote agents.

In this example, the `ApiClientConfiguration.fromEnvPrefix` method uses the provided `PREFIX_` (e.g., `MAILCOMPOSER_` or `EMAIL_REVIEWER_`) to automatically create configuration values like `PREFIX_ID` and `PREFIX_API_KEY` by reading them from the environment variables. This simplifies the setup process.

```python
from agntcy_acp import ApiClientConfiguration

# Fill in client configuration for the remote agent
MAILCOMPOSER_AGENT_ID = os.environ.get("MAILCOMPOSER_ID", "")
EMAIL_REVIEWER_AGENT_ID = os.environ.get("EMAIL_REVIEWER_ID", "")
SENDGRID_HOST = os.environ.get("SENDGRID_HOST", "http://localhost:8080")
MAILCOMPOSER_CLIENT_CONFIG = ApiClientConfiguration.fromEnvPrefix("MAILCOMPOSER_")
EMAIL_REVIEWER_CONFIG = ApiClientConfiguration.fromEnvPrefix("EMAIL_REVIEWER_")
```

### Mail Composer ACP Node

```python
from agntcy_acp.LangGraph.acp_node import ACPNode

acp_mailcomposer = ACPNode(
    name="mailcomposer",
    agent_id=MAILCOMPOSER_AGENT_ID,
    client_config=MAILCOMPOSER_CLIENT_CONFIG,
    input_path="mailcomposer_state.input",
    input_type=mailcomposer.InputSchema,
    output_path="mailcomposer_state.output",
    output_type=mailcomposer.OutputSchema,
)
```

### Email Reviewer ACP Node

```python
acp_email_reviewer = ACPNode(
    name="email_reviewer",
    agent_id=EMAIL_REVIEWER_AGENT_ID,
    client_config=EMAIL_REVIEWER_CONFIG,
    input_path="email_reviewer_state.input",
    input_type=email_reviewer.InputSchema,
    output_path="email_reviewer_state.output",
    output_type=email_reviewer.OutputSchema,
)
```

> **Note**: The `_ path` fields indicate where to find the input and output in the `OverallState`, while the `_type` fields specify the type of the input and output schemas.


Finally, replace the placeholder nodes in the state graph with the newly defined ACP nodes:

```python
sg.add_node(acp_mailcomposer)
sg.add_node(acp_email_reviewer)
```


## Step 5: API Bridge Integration

The API Bridge **converts natural language outputs into structured API requests**. Indeed the input of the API Bridge will be in natural language, but the [SendGrid APIs](https://github.com/twilio/sendgrid-oai/blob/main/spec/json/tsg_mail_v3.json) require a specifically structured format. The API Bridge ensures that the **correct endpoint and request format** are used.


### Overview of the API Bridge

The API Bridge Agent project provides a Tyk middleware plugin that allows users to interact with traditional REST APIs using natural language. It acts as a translator between human language and structured API requests/responses.

#### Key Features:

- **Natural Language Conversion**: Converts natural language queries into valid API requests based on OpenAPI specifications.
- **Response Transformation**: Transforms API responses back into natural language explanations for better clarity.
- **Integration with Tyk API Gateway**: Operates as a plugin, allowing easy integration without modifying existing API implementations.
- **Language Processing**: Utilizes Azure OpenAI’s GPT models to process and understand natural language inputs
- **Schema Validation and Security**: Maintains API schema validation and security for robust and secure interactions.


### Add SendGrid API Bridge Node

To integrate the SendGrid API Bridge, we first need to provide a valid API key and host. In this example, we retrieve `SENDGRID_API_KEY` and `SENDGRID_HOST` from environment variables.

```python
# Instantiate APIBridge Agent Node
sendgrid_api_key = os.environ.get("SENDGRID_API_KEY", None)
if sendgrid_api_key is None:
    raise ValueError("SENDGRID_API_KEY environment variable is not set")

send_email = APIBridgeAgentNode(
    name="sendgrid",
    input_path="sendgrid_state.input",
    output_path="sendgrid_state.output",
    service_api_key=sendgrid_api_key,
    hostname=SENDGRID_HOST,
    service_name="sendgrid/v3/mail/send"
)
```

> **Explanation**:
> - The `_path` fields indicate where to find the input and output in the `OverallState`, as explained in [Step 4](#step-4-multi-agent-application-development).
> - The `service_name` field specifies the endpoint manually (`sendgrid/v3/mail/send`). However, the API Bridge can **automatically determine** the correct endpoint based on the natural language request if this field is not provided. [Learn more](https://docs.agntcy.org/pages/syntactic_sdk/api_bridge_agent.html)

Finally, replace the `send_email` placeholder node defined in [Step 1](#step-1-create-a-basic-LangGraph-skeleton-application) with this new `send_email` node.


## Step 6: Input and Output Processing and I/O Mapper Integration

In this section, we will explore how to handle inputs and outputs effectively within the workflow. Managing the flow of data between agents allows to maintain the integrity of the process.

To achieve this, we not only added the **I/O Mapper**, a powerful tool that automatically transforms outputs from one node to match the input requirements of the next using an LLM, but also **introduced additional nodes** to demonstrate how to perform **manual mapping**. This combination showcases both automated and manual approaches handle the state within the application.

### Why Use I/O Mapper?

The I/O Mapper ensures compatibility between agents by **transforming outputs to meet the input requirements** of subsequent agents. It addresses both **format-level** and **semantic-level** compatibility by leveraging an LLM to perform tasks such as:

- **JSON Structure Transcoding**: Remapping JSON dictionaries.
- **Text Summarization**: Reducing or refining text content.
- **Text Translation**: Translating text between languages.
- **Text Manipulation**: Reformulating or extracting specific information.


### I/O Processing Overview

Among the three nodes added so far, some additional nodes are required to handle input and output transformations effectively. Specifically, In the [Marketing Campaign MAS](examples/marketing-campaign/src/marketing_campaign/app.py), the following nodes were added:

- **`process_inputs`**: Processes the user's input, updates the `OverallState`, and initializes the `mailcomposer_state` with messages to ensure they are correctly interpreted by the `mailcomposer`. It also checks if the user has completed their interaction (e.g., input is "OK"), which means the user is satisfied about the composed email.

- **`prepare_sendgrid_input`**: This node prepares the input for the SendGrid API. It constructs a query in natural language to send an email, using the corrected email content from the `email_reviewer` and configuration details like the recipient and sender email addresses.

- **`prepare_output`**: This node consolidates the outputs of the application. It updates the `OverallState` with the final email content and logs the result of the email send operation.

At the end of the documen, we will present the final graph that incorporates all these nodes and demonstrates the complete flow.


### Conditional Edge with I/O Mapper

The edge between the `mailcomposer` and subsequent nodes is a **conditional edge**. This edge uses the `check_final_email` **function to determine the next step** to be executed. The condition works as follows:

- If the user input is **not "OK"**, the graph transitions to the `prepare_output` node, allowing the user to interact with the `mailcomposer` again.
- If the user input is **"OK"**, the graph transitions to the `email_reviewer` node and continues through the workflow.

The conditional edge is implemented with the I/O Mapper, which ensures that the outputs of one node are transformed to match the input requirements of the next node. Here's the code for the conditional edge:

```python
add_io_mapped_conditional_edge(
    sg,
    start=acp_mailcomposer,
    path=check_final_email,
    iomapper_config_map={
        "done": {
            "end": acp_email_reviewer,
            "metadata": {
                "input_fields": ["mailcomposer_state.output.final_email", "target_audience"]
            }
        },
        "user": {
            "end": "prepare_output",
            "metadata": None
        }
    },
    llm=llm
)
```

#### Explanation of Parameters and Workflow Behavior:

- **`start=acp_mailcomposer`**: Specifies the starting node for the conditional edge, which is the `mailcomposer`.
- **`path=check_final_email`**: This is the function that determines the condition for the edge. It returns either `"done"` or `"user"`.
  - `"done"` indicates that the user is satisfied with the composed email, so to go to the `email_reviewer`.
  - `"user"` indicates that the user is not satisfied, and move towards `prepare_output` to log the results and loops back to the user.

- **`"input_fields": ["mailcomposer_state.output.final_email", "target_audience"]`**: Specifies what to map:
  - `"mailcomposer_state.output.final_email"`: Automatically takes the `final_email` output from the `mailcomposer` and maps it to the input defined in the manifest of the `email_reviewer`
  - `"target_audience"`: is populated during `process_inputs` from the configuration, required by `email_reviewer`

> **Note**: All paths specified in the `input_fields` are rooted in the `OverallState`


### Resulting Graph and Conclusion

Below is the final graph that represents the **complete process** of composing, reviewing, and sending an email. This graph shows how agents are connected, how inputs and outputs are processed, and how the application adapts dynamically based on user interactions.

![Final LangGraph Application](./_static/marketing_campaign_final.png)

The MAS begins with the `process_inputs` node and transitions to the `mailcomposer` node, where the email draft is created. A **conditional edge** allows the user to interact with the `mailcomposer` until they are satisfied with the composed email. Once confirmed, the workflow proceeds through the following nodes in sequence:

1. **`email_reviewer`**: Reviews and refines the email content.
2. **`prepare_sendgrid_input`**: Prepares the input for the SendGrid API.
3. **`sendgrid`**: Sends the email using the SendGrid API.
4. **`prepare_output`**: Consolidates the final output and logs the result.

This graph highlights the **importance of input and output transformations**, the role of the **I/O Mapper** in ensuring compatibility between agents, and the flexibility provided by conditional edges to adapt the workflow dynamically. With this setup, the system achieves a robust and user-friendly process for managing email campaigns.

### Conclusion

In this tutorial, we demonstrated how to build a Multi-Agent System (MAS) using the ACP SDK. Starting from a basic LangGraph skeleton application, we progressively integrated agents, defined states, and implemented advanced features such as the I/O Mapper and API Bridge integration. These components allowed us to create a dynamic and flexible flow that ensures compatibility between agents and adapts to user interactions.

By following this approach, you can design and implement your own MAS tailored to specific use cases, leveraging the power of ACP to enable communication and collaboration between distributed agents. The tools and techniques presented here provide a solid foundation for building scalable, efficient, and user-friendly multi-agent software.