# Getting Started: Build Your First Multi-Agent Software

This tutorial guides you through the process of building a distributed multi-agent application using [LangGraph](https://www.langchain.com/langgraph) and leveraging [Agent Connect Protocol (ACP)](https://docs.agntcy.org/pages/syntactic_sdk/connect.html) and other **AGNTCY** components and tools.

The sample app used for this tutorial is a **Marketing Campaign Manager** agent. A "pre-cooked" version of this application is available [here](https://github.com/agntcy/agentic-apps/tree/main/marketing-campaign).

> For this tutorial we are using LangGraph, but other frameworks can also be used.


## Overview
The **Marketing Campaign Manager** we are building implements a LangGraph graph which:
* Interacts with a user to gather the description of the email marketing campaign to launch.
* Uses an already existing [Mail Composer Agent](https://github.com/agntcy/agentic-apps/tree/main/mailcomposer), capable of composing emails for the marketing campaign. This agent is written using LangGraph, it provides an Agent Manifest which allows to deploy it through the Agent Workflow Server and be consumed through ACP.
* Uses an already existing [Email Reviewer Agent](https://github.com/agntcy/agentic-apps/tree/main/email_reviewer) capable of reviewing an email and adjust it for a specific target audience. This agent is written using [LlamaIndex](https://www.llamaindex.ai/framework) and similarly to the previous agent, it provides a Agent Manifest which allows to deploy it through the [Agent Workflow Server](https://docs.agntcy.org/pages/agws/workflow_server.html) and be consumed through ACP.
* Uses [Twilio Sendgrid](https://sendgrid.com/) API to deliver the marketing campaign email to the intended recipient. We will consume this API leveraging the capabilities of the [API Bridge Agent](https://docs.agntcy.org/pages/syntactic_sdk/api_bridge_agent.html).

This tutorial is structured in the following steps:

1. [Create a Basic LangGraph Skeleton Application](#step-1-create-a-basic-langgraph-skeleton-application): Set up a LangGraph application structure to serve as the base of your multi-agent software.

2. [Generate Models from Agent Manifests](#step-2-generate-models-from-agent-manifests): Use agent manifests to generate models defining data structures and interfaces.

3. [State Definition](#step-3-state-definition): Create states to manage the flow of your multi-agent software (MAS).

4. [Multi-Agent Application Development](#step-4-multi-agent-application-development): Use ACP SDK to integrate ACP nodes into your LangGraph application.

5. [API Bridge Integration](#step-5-api-bridge-integration): Connect natural language outputs to structured API requests.

6. [I/O Mapper Integration](#step-6-i-o-mapper-integration): Adapt inputs and outputs between different agents such that they match in format and meaning.

7. [Generate Application Manifest](#step-7-generate-application-manifest): Create a manifest file to define how your application can be deployed and consumed via ACP.

8. [Review Resulting Application](#step-8-review-resulting-application): Analyze the complete workflow and how all components interact with one another.

9. [Execute Application through Workflow Server Manager](#step-9-execute-application-through-workflow-server-manager): Deploy and test the multi-agent system using Workflow Server Manager.

## Prerequisites

- A working installation of [Python](https://www.python.org/) 3.9 or higher
- [poetry](https://pypi.org/project/poetry/) v2 or greater
- [curl](https://curl.se/)


## Step 1: Create a Basic LangGraph Skeleton Application

Let's start by setting up our project environment. You can either use pip to install the required packages or Poetry for dependency management.

### Setting up the project

First, create a new project using Poetry:

```bash
# Create a new Poetry project
poetry new --python='>=3.9,<4.0' marketing-campaign
cd marketing-campaign
```

At this point, it's recommended to open the project folder in your favorite IDE for a better development experience.

Install the dependencies:

```bash
# Add all dependencies
poetry add python-dotenv langgraph langchain-openai langchain "agntcy-acp[iomapper-langgraph]"

# Install the current project (marketing-campaign) and dependencies
poetry install
```


### Building a Simple LangGraph Skeleton

Now let's begin by setting up a **simple LangGraph** skeleton application with the following nodes:

*Start, Mail Composer, Email Reviewer, Send Mail, and End*


![Skeleton LangGraph Application](./_static/marketing_campaign_skeleton.png)

This setup is a basic framework with **placeholders for each task** in the workflow. It sets the stage for **transforming** these nodes into remote **ACP nodes**, allowing the interaction with **real remote agents**.

The ultimate goal of this application is to compose and review emails that will be sent to a mail recipient. Each node represents a task to be performed in this process, from composing the email to reviewing it, and finally sending it.


### Skeleton Code Example

To create the initial structure of our application (skeleton), we need to create a Python file that defines our LangGraph application with placeholder nodes. This serves as the foundation that we'll enhance later with ACP integration.

Let's create a file named `app.py` in the `src/marketing_campaign/` directory with the following content:

```python
# app.py
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
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
def build_app_graph() -> CompiledStateGraph:
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
    print("Graph compiled successfully.")
    return graph

# Compile and skeleton graph
graph = build_app_graph()

```

Let's run our code to make sure everything works as expected:

```bash
poetry run python src/marketing_campaign/app.py
```

You should see the output:
```
"Graph compiled successfully."
```


## Step 2: Generate Models from Agent Manifests

In this step, you will **generate** models based on the agent manifests to define the **input, output and config schemas** for each agent involved in MAS. The models are created using the `acp generate-agent-models` cli command, which reads the agent manifest files and produces Python files that encapsulate the agent's data structures and interfaces necessary for integration.

> **What is an Agent Manifest?**\
> An Agent Manifest is a detailed document outlining an agent's capabilities, deployment methods, data structure specifications and dependencies on other agents. It provides **essential information** for ensuring agents can communicate and work together within the **Agent Connect Protocol** and **Workflow Server ecosystem**. [Learn more](https://docs.agntcy.org/pages/agws/manifest.html)

### Schema and Type Generation

We will use two agents whose manifests

* [Mail Composer Manifest](https://github.com/agntcy/agentic-apps/tree/main/mailcomposer/deploy/mailcomposer.json)
* [Email Reviewer Manifest](https://github.com/agntcy/agentic-apps/tree/main/email_reviewer/deploy/email_reviewer.json)

are provided within the [Agentic Apps](https://github.com/agntcy/agentic-apps) repository. To proceed, let's download the manifest files:

```bash
# Create a manifests directory to store the agent manifests
mkdir -p manifests

# Download Mail Composer Manifest
curl -o manifests/mailcomposer.json https://raw.githubusercontent.com/agntcy/agentic-apps/refs/heads/main/mailcomposer/deploy/mailcomposer.json

# Download Email Reviewer Manifest
curl -o manifests/email_reviewer.json https://raw.githubusercontent.com/agntcy/agentic-apps/refs/heads/main/email_reviewer/deploy/email_reviewer.json
```

Now, we can generate the models using the `acp` command-line tool that was installed as part of our dependencies:

```bash
# Generate models for Mail Composer
poetry run acp generate-agent-models manifests/mailcomposer.json --output-dir ./src/marketing_campaign --model-file-name mailcomposer.py

# Generate models for Email Reviewer
poetry run acp generate-agent-models manifests/email_reviewer.json --output-dir ./src/marketing_campaign --model-file-name email_reviewer.py
```

These commands create the necessary Python files containing the Pydantic models for interacting with these agents.

> **Model File Structure:**
> - **Pydantic Models**: Each file includes Pydantic models that represent the **configuration**, **input**, and **output** schemas, enforcing type validation.
> - **Input, Output and Config Schemas**: These schemas handle incoming and outgoing data and the configuration of the agent.


## Step 3: State Definition

State management is fundamental to **track progress and outcomes** so that each agent can interact effectively with others following the right workflow. In this step, we will define the states necessary to manage the flow of your multi-agent software.

### Understanding State in Multi-Agent Systems

State in multi-agent systems refers to the structured data that represents the **current status of the application**. It includes information about the inputs, outputs, and **intermediate results** of each agent's operations. Effective state management allows for the **coordination and synchronization of agent activities**.

### State Definition in the Marketing Campaign Example

Create a file named `state.py` in the `src/marketing_campaign/` directory that will hold state definitions for the MAS:

```python
# src/marketing_campaign/state.py
from pydantic import BaseModel, Field
from typing import List, Optional
from marketing_campaign import mailcomposer
from marketing_campaign import email_reviewer

class ConfigModel(BaseModel):
    recipient_email_address: str = Field(..., description="Email address of the email recipient")
    sender_email_address: str = Field(..., description="Email address of the email sender")
    target_audience: email_reviewer.TargetAudience = Field(..., description="Target audience for the marketing campaign")

class MailComposerState(BaseModel):
    input: Optional[mailcomposer.InputSchema] = None
    output: Optional[mailcomposer.OutputSchema] = None

class MailReviewerState(BaseModel):
    input: Optional[email_reviewer.InputSchema] = None
    output: Optional[email_reviewer.OutputSchema] = None

class OverallState(BaseModel):
    messages: List[mailcomposer.Message] = Field([], description="Chat messages")
    operation_logs: List[str] = Field([],
                                      description="An array containing all the operations performed and their result. Each operation is appended to this array with a timestamp.",
                                      examples=[["Mar 15 18:10:39 Operation performed: email sent Result: OK",
                                                 "Mar 19 18:13:39 Operation X failed"]])

    has_composer_completed: Optional[bool] = Field(None, description="Flag indicating if the mail composer has succesfully completed its task")
    has_reviewer_completed: Optional[bool] = None
    has_sender_completed: Optional[bool] = None
    mailcomposer_state: Optional[MailComposerState] = None
    email_reviewer_state: Optional[MailReviewerState] = None
    target_audience: Optional[email_reviewer.TargetAudience] = None
```

The `ConfigModel` defines the configuration parameters for the Marketing Campaign application:
* `recipient_email_address`: Specifies who will receive the email (target recipient)
* `sender_email_address`: Defines the email address that will appear in the "From" field
* `target_audience`: Provides details about the audience the email is intended for, allowing the Email Reviewer to optimize content appropriately

After creating the state file, replace the imports in your `app.py` file with:

```python
# Replace all imports at the top of src/marketing_campaign/app.py with:
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from marketing_campaign.state import OverallState

# IMPORTANT: Remove the
# class OverallState(BaseModel):
# definition. Rest of your code remains the same
# ...
```

> **Important**: When updating your application, make sure to remove the placeholder `OverallState` class defined in [Step 1](#step-1-create-a-basic-langgraph-skeleton-application) and import the state classes from your new `state.py` file. This ensures your application uses the proper state definitions that incorporate the agent models generated from the manifests in [Step 2](#step-2-generate-models-from-agent-manifests).

With this state definition in place, your application now has a structured approach for managing the flow of data between agents:

* The `OverallState` class captures the complete state of the application
* The individual component states (`MailComposerState`, `MailReviewerState`) handle the specific data requirements for each agent.

The next step involves transforming our placeholder nodes into actual ACP nodes for remote agent integration.


## Step 4: Multi-Agent Application Development

Now, let's enhance the skeleton setup by **transforming** LangGraph nodes **into ACP nodes** using `agntcy_acp` **sdk**. ACP nodes allow network communication between agents by using the **Agent Connect Protocol (ACP)**.
This enables remote invocation, configuration, and output retrieval with the goal of allowing heterogeneous and distributed agents to interoperate.


> **Why Use ACP?**
> 1. **Remote Execution**: ACP nodes run on a Agent Workflow Server, making it possible to execute tasks remotely.
> 2. **Technology Independence**: ACP allows agents to be implemented in various technologies, such as LangGraph, LlamaIndex, etc., without compatibility issues.
> 3. **Interoperability**: ACP ensures that agents can communicate and work together, regardless of the underlying technology, by adhering to a standardized protocol.
> [Learn more about ACP](https://docs.agntcy.org/pages/syntactic_sdk/connect.html)


### Add Mail Composer and Email Reviewer ACP Nodes

To integrate the Mail Composer and Email Reviewer as ACP nodes, update the `src/marketing_campaign/app.py` file by adding the following imports at the top of the file:

```python
# Add these imports at the top of src/marketing_campaign/app.py
import os
from marketing_campaign import mailcomposer
from marketing_campaign import email_reviewer
from agntcy_acp import ApiClientConfiguration
from agntcy_acp.langgraph.acp_node import ACPNode
```

Then, add the client configuration for the remote agents below your imports:

```python
# Below your imports, fill in client configuration for the remote agents
MAILCOMPOSER_AGENT_ID = os.environ.get("MAILCOMPOSER_ID", "")
EMAIL_REVIEWER_AGENT_ID = os.environ.get("EMAIL_REVIEWER_ID", "")
mailcomposer_client_config = ApiClientConfiguration.fromEnvPrefix("MAILCOMPOSER_")
email_reviewer_client_config = ApiClientConfiguration.fromEnvPrefix("EMAIL_REVIEWER_")
```

Next, define the ACP nodes to **replace** our placeholder functions:

```python
# Mail Composer ACP Node
acp_mailcomposer = ACPNode(
    name="mailcomposer",
    agent_id=MAILCOMPOSER_AGENT_ID,
    client_config=mailcomposer_client_config,
    input_path="mailcomposer_state.input",
    input_type=mailcomposer.InputSchema,
    output_path="mailcomposer_state.output",
    output_type=mailcomposer.OutputSchema,
)

# Email Reviewer ACP Node
acp_email_reviewer = ACPNode(
    name="email_reviewer",
    agent_id=EMAIL_REVIEWER_AGENT_ID,
    client_config=email_reviewer_client_config,
    input_path="email_reviewer_state.input",
    input_type=email_reviewer.InputSchema,
    output_path="email_reviewer_state.output",
    output_type=email_reviewer.OutputSchema,
)
```

> **Note**: The `_path` fields indicate where to find the input and output in the `OverallState`, while the `_type` fields specify the type of the input and output.

Finally, update the `build_app_graph` function to use these ACP nodes instead of the placeholder functions:

```python
# Update your build_app_graph function
def build_app_graph() -> CompiledStateGraph:
    sg = StateGraph(OverallState)

    # Replace placeholder nodes with ACP nodes
    sg.add_node(acp_mailcomposer)
    sg.add_node(acp_email_reviewer)
    sg.add_node(send_mail)  # We'll replace this with an API Bridge Agent node in Step 5

    # Define the flow of the graph
    sg.add_edge(START, acp_mailcomposer.get_name())
    sg.add_edge(acp_mailcomposer.get_name(), acp_email_reviewer.get_name())
    sg.add_edge(acp_email_reviewer.get_name(), send_mail.__name__)
    sg.add_edge(send_mail.__name__, END)

    graph = sg.compile()
    print("Graph compiled successfully.")
    return graph
```


## Step 5: API Bridge Integration

The API Bridge **converts natural language outputs into structured API requests**. The input to the API Bridge is in natural language, but APIs like [SendGrid APIs](https://github.com/twilio/sendgrid-oai/blob/main/spec/json/tsg_mail_v3.json) require specifically structured formats. The API Bridge ensures that the **correct endpoint and request format** are used.

For more detailed information about the API Bridge Agent implementation and configuration, please refer to the [API Bridge documentation](https://docs.agntcy.org/pages/syntactic_sdk/api_bridge_agent.html).

### Add SendGrid API Bridge Node

To integrate the SendGrid API Bridge into our `src/marketing_campaign/app.py` file, add the following imports at the top of your file (along with the previous imports):


```python
# Add these imports at the top of src/marketing_campaign/app.py
from agntcy_acp.langgraph.api_bridge import APIBridgeAgentNode
```

Then add the SendGrid configuration below the existing agent configurations, replacing the placeholder `send_mail` function:

```python
# Remove the placeholder send_mail function in src/marketing_campaign/app.py
# and replace it with this APIBridgeAgentNode:

# Instantiate APIBridge Agent Node
SENDGRID_HOST = os.environ.get("SENDGRID_HOST", "http://localhost:8080")
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


Finally, update your `build_app_graph` function to **replace** the placeholder `send_mail` function defined in [Step 1](#step-1-create-a-basic-langgraph-skeleton-application) with the new `send_email` API Bridge node:

```python
# Update your build_app_graph function
def build_app_graph() -> CompiledStateGraph:
    sg = StateGraph(OverallState)

    # Replace placeholder nodes with ACP nodes
    sg.add_node(acp_mailcomposer)
    sg.add_node(acp_email_reviewer)
    sg.add_node(send_email)  # Replace the placeholder send_mail with the API Bridge

    # Define the flow of the graph
    sg.add_edge(START, acp_mailcomposer.get_name())
    sg.add_edge(acp_mailcomposer.get_name(), acp_email_reviewer.get_name())
    sg.add_edge(acp_email_reviewer.get_name(), send_email.get_name())
    sg.add_edge(send_email.get_name(), END)

    graph = sg.compile()
    print("Graph compiled successfully.")
    return graph
```

At this point, if you want to run your application to see if it compiles [(as at the end of Step 1 above)](#skeleton-code-example), you will
need to set the `SENDGRID_API_KEY` in your environment. This depends on your operating system and
shell, but an example for most shells in most Unix-like OSes:

```shell
export SENDGRID_API_KEY="enter API key here"
```

For a complete setup guide including Tyk gateway configuration and SendGrid API details, see the [SendGrid API Bridge example in the ACP SDK documentation](https://docs.agntcy.org/pages/syntactic_sdk/api_bridge_agent.html#an-example-with-sendgrid-api).


## Step 6: I/O Mapper Integration

In this section, we will explore how to handle inputs and outputs effectively within the workflow. Managing the flow of data between agents allows to maintain the integrity of the process.

To achieve this, we not only add the **I/O Mapper**, a powerful tool that automatically transforms outputs from one node to match the input requirements of the next using an LLM, but also **introduce additional nodes** to demonstrate how to perform **manual mapping**. This combination showcases both automated and manual approaches to handle the state within the application.

> **What is I/O Mapper?**\
> I/O Mapper is a component that ensures compatibility between agents by **transforming outputs to meet the input requirements** of subsequent agents. It addresses both **format-level** and **semantic-level** compatibility by leveraging an LLM to perform tasks such as:
>
> - **JSON Structure Transcoding**: Remapping JSON dictionaries.
> - **Text Summarization**: Reducing or refining text content.
> - **Text Translation**: Translating text between languages.
> - **Text Manipulation**: Reformulating or extracting specific information.
>
> For more details on I/O Mapper functionality and implementation, see the [official I/O Mapper documentation](https://docs.agntcy.org/pages/semantic_sdk/io_mapper.html).


### I/O Processing Overview

Among the three nodes added so far, some additional nodes are required to handle input and output transformations effectively. Specifically, as shown in [Marketing Campaign MAS](https://github.com/agntcy/agentic-apps/tree/main/marketing-campaign/src/marketing_campaign/app.py), the following nodes were added:

- **`process_inputs`**: Processes the user's input, updates the `OverallState`, and initializes the `mailcomposer_state` with messages to ensure they are correctly interpreted by the `mailcomposer`. It also checks if the user has completed their interaction (e.g., input is "OK"), which means the user is satisfied about the composed email.

- **`prepare_sendgrid_input`**: This node prepares the input for the SendGrid API. It constructs a query in natural language to send an email, using the corrected email content from the `email_reviewer` and configuration details like the recipient and sender email addresses.

- **`prepare_output`**: This node consolidates the outputs of the application. It updates the `OverallState` with the final email content and logs the result of the email send operation.

To make this tutorial code fully functional, we need to add implementations for the processing nodes mentioned above:

1. First, update the `src/marketing_campaign/state.py` file to include a SendGridState definition:
    ```python
    # src/marketing_campaign/state.py
    # Add these imports
    from agntcy_acp.langgraph.api_bridge import APIBridgeOutput, APIBridgeInput

    # Add SendGridState class along with existing state classes
    class SendGridState(BaseModel):
        input: Optional[APIBridgeInput] = None
        output: Optional[APIBridgeOutput]= None
    ```
2. Then, update `OverallState` class to include `sendgrid_state` in `src/marketing_campaign/state.py`:
    ```python
    class OverallState(BaseModel):
        # Add sendgrid_state to OverallState
        messages: List[mailcomposer.Message] = Field([], description="Chat messages")
        operation_logs: List[str] = Field([],
                                        description="An array containing all the operations performed and their result. Each operation is appended to this array with a timestamp.",
                                        examples=[["Mar 15 18:10:39 Operation performed: email sent Result: OK",
                                                    "Mar 19 18:13:39 Operation X failed"]])

        has_composer_completed: Optional[bool] = Field(None, description="Flag indicating if the mail composer has succesfully completed its task")
        has_reviewer_completed: Optional[bool] = None
        has_sender_completed: Optional[bool] = None
        mailcomposer_state: Optional[MailComposerState] = None
        email_reviewer_state: Optional[MailReviewerState] = None
        target_audience: Optional[email_reviewer.TargetAudience] = None
        sendgrid_state: Optional[SendGridState] = None  # Add this line
    ```

3. Subsequently, update imports at the top of your `src/marketing_campaign/app.py` file:
    ```python
    # src/marketing_campaign/app.py
    # Update import to include SendGridState
    from marketing_campaign.state import OverallState, MailComposerState, SendGridState

    # Add these imports
    import copy
    from agntcy_acp.langgraph.api_bridge import APIBridgeAgentNode, APIBridgeInput
    from langchain_core.runnables import RunnableConfig
    ```

4. Finally, implement the processing nodes in `src/marketing_campaign/app.py`:
    ```python
    # Add these processing nodes to src/marketing_campaign/app.py
    def process_inputs(state: OverallState, config: RunnableConfig) -> OverallState:
        cfg = config.get('configurable', {})

        user_message = state.messages[-1].content

        if user_message.upper() == "OK":
            state.has_composer_completed = True
        else:
            state.has_composer_completed = False

        state.target_audience = email_reviewer.TargetAudience(cfg["target_audience"])

        state.mailcomposer_state = MailComposerState(
            input=mailcomposer.InputSchema(
                messages=copy.deepcopy(state.messages),
                is_completed=state.has_composer_completed
            )
        )
        return state

    def prepare_sendgrid_input(state: OverallState, config: RunnableConfig) -> OverallState:
        cfg = config.get('configurable', {})
        state.sendgrid_state = SendGridState(
            input=APIBridgeInput(
                query=f""
                    f"Please send an email to {cfg['recipient_email_address']} from {cfg['sender_email_address']}.\n"
                    f"Content of the email should be the following:\n"
                    f"{state.email_reviewer_state.output.corrected_email if (state.email_reviewer_state
                        and state.email_reviewer_state.output
                        and hasattr(state.email_reviewer_state.output, 'corrected_email')
                        ) else ''}"
            )
        )
        return state

    def prepare_output(state: OverallState, config: RunnableConfig) -> OverallState:
        state.messages = copy.deepcopy(
            state.mailcomposer_state.output.messages if (state.mailcomposer_state
                and state.mailcomposer_state.output
                and state.mailcomposer_state.output.messages
            ) else []
        )
        if state.sendgrid_state and state.sendgrid_state.output and state.sendgrid_state.output.result:
            state.operation_logs.append(f"Email Send Operation: {state.sendgrid_state.output.result}")

        return state
    ```

### Conditional Edge with I/O Mapper

The edge between the `mailcomposer` and subsequent nodes is a **conditional edge**. This edge uses the `check_final_email` **function to determine the next step** to be executed. The condition works as follows:

- If the user input is **not "OK"**, the graph transitions to the `prepare_output` node, allowing the user to interact with the `mailcomposer` again.
- If the user input is **"OK"**, the graph transitions to the `email_reviewer` node and continues through the workflow.

The conditional edge is implemented with the I/O Mapper, which ensures that the outputs of one node are transformed to match the input requirements of the next node. Here's how to implement the conditional edge in `src/marketing_campaign/app.py`:

1. Add LLM client for the I/O Mapper. In this example we're using `AzureChatOpenAI`, but you can use any LLM client supported by LangChain:
    ```python
    # Add LLM client to src/marketing_campaign/app.py
    from langchain_openai.chat_models.azure import AzureChatOpenAI

    # Initialize LLM for the I/O Mapper
    llm = AzureChatOpenAI(
        model="gpt-4o-mini",
        api_version="2024-07-01-preview",
        seed=42,
        temperature=0,
    )
    ```

2. Define the conditional edge function in `src/marketing_campaign/app.py`:
    ```python
    # Add conditional edge function to src/marketing_campaign/app.py
    def check_final_email(state: OverallState):
        """Determine whether to proceed to email review or continue user interaction.

        Returns:
            "done": If the mailcomposer has produced a final email
            "user": If we need to continue interacting with the user
        """
        return "done" if (state.mailcomposer_state
                        and state.mailcomposer_state.output
                        and state.mailcomposer_state.output.final_email
                        ) else "user"
    ```

3. Next, update the `build_app_graph` function in `src/marketing_campaign/app.py` to include our new nodes and the `add_io_mapped_conditional_edge` edge:
    ```python
    # Add import for I/O Mapper in src/marketing_campaign/app.py
    from agntcy_acp.langgraph.io_mapper import add_io_mapped_conditional_edge

    # Update build_app_graph 
    def build_app_graph() -> CompiledStateGraph:
        sg = StateGraph(OverallState)

        # Add all nodes to the graph
        sg.add_node(process_inputs)
        sg.add_node(acp_mailcomposer)
        sg.add_node(acp_email_reviewer)
        sg.add_node(send_email)
        sg.add_node(prepare_sendgrid_input)
        sg.add_node(prepare_output)

        # Define the initial flow
        sg.add_edge(START, "process_inputs")
        sg.add_edge("process_inputs", acp_mailcomposer.get_name())

        # Add conditional edge between mailcomposer and either email_reviewer or END, adding io_mappers between them
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

        # Define the remaining flow for the "done" path
        sg.add_edge(acp_email_reviewer.get_name(), "prepare_sendgrid_input")
        sg.add_edge("prepare_sendgrid_input", send_email.get_name())
        sg.add_edge(send_email.get_name(), "prepare_output")
        sg.add_edge("prepare_output", END)

        graph = sg.compile()
        print("Graph compiled successfully.")
        return graph
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

With these additions, our application now has a complete workflow that can:
1. Process user inputs and initialize states
2. Compose emails with the Mail Composer agent
3. Route based on user feedback using conditional edges
4. Review emails with the Email Reviewer agent when needed
5. Prepare and send emails using the SendGrid API Bridge
6. Provide meaningful output back to the user


At this point, if you want to run your application to see if it compiles [(as at the end of Step 1 above)](#skeleton-code-example), you will
need to set some variables for Azure in your environment. This depends on your operating system 
and shell, but an example for most shells in most Unix-like OSes:

```shell
export AZURE_OPENAI_API_KEY="enter API key here"
export AZURE_OPENAI_ENDPOINT="https://resource.azure.openai.com/openai/"
```

## Step 7: Generate Application Manifest

In this step, we will **generate the Agent Manifest** for our Marketing Campaign application. The manifest generation enables our application to be used by other applications and to be deployed through an [Agent Workflow Server](https://github.com/agntcy/workflow-srv).

> **Why Generate an Agent Manifest?**
> 1. **Reusability**: The manifest allows your MAS to be used as a dependency in other applications, so as to allow modular and composable agent architectures.
> 2. **Deployment**: It provides the necessary information for the Workflow Server Manager to deploy and run your application along with its dependencies.
> 3. **Documentation**: It serves as a self-documenting artifact that describes your agent's capabilities, configuration options, and dependencies.

### Creating the Manifest Generator

Let's create a new file called `generate_manifest.py` in the `src/marketing_campaign/` directory:

```python
# src/marketing_campaign/generate_manifest.py
from datetime import datetime, timezone
from pathlib import Path

from agntcy_acp.manifest import (
    AgentACPSpec,
    AgentDependency,
    AgentDeployment,
    AgentManifest,
    AgentRef,
    Capabilities,
    DeploymentManifest,
    DeploymentOptions,
    EnvVar,
    LangGraphConfig,
    Locator,
    Manifest,
    Skill,
    SourceCodeDeployment,
    OASF_EXTENSION_NAME_MANIFEST,
)
from pydantic import AnyUrl

from marketing_campaign.state import ConfigModel, OverallState

# Deps are relative to the main manifest file.
mailcomposer_dependency_manifest = "mailcomposer.json"
email_reviewer_dependency_manifest = "email_reviewer.json"

manifest = AgentManifest(
    name="org.agntcy.marketing-campaign",
    authors=["AGNTCY Internet of Agents Collective"],
    annotations={"type": "langgraph"},
    version="0.3.1",
    locators=[
        Locator(
            url="https://github.com/agntcy/agentic-apps/tree/main/marketing-campaign",
            type="source-code",
        ),
    ],
    description="Offer a chat interface to compose an email for a marketing campaign. Final output is the email that could be used for the campaign",
    created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    schema_version="0.1.3",
    skills=[
        Skill(
            category_name="Natural Language Processing",
            category_uid=1,
            class_name="Dialogue Generation",
            class_uid=10204,
        ),
        Skill(
            category_name="Natural Language Processing",
            category_uid=1,
            class_name="Text Completion",
            class_uid=10201,
        ),
        Skill(
            category_name="Natural Language Processing",
            category_uid=1,
            class_name="Text Paraphrasing",
            class_uid=10203,
        ),
        Skill(
            category_name="Natural Language Processing",
            category_uid=1,
            class_name="Knowledge Synthesis",
            class_uid=10303,
        ),
        Skill(
            category_name="Natural Language Processing",
            category_uid=1,
            class_name="Text Style Transfer",
            class_uid=10206,
        ),
        Skill(
            category_name="Natural Language Processing",
            category_uid=1,
            class_name="Tone and Style Adjustment",
            class_uid=10602,
        ),
    ],
    extensions=[
        Manifest(
            name=OASF_EXTENSION_NAME_MANIFEST,
            version="v0.2.2",
            data=DeploymentManifest(
                acp=AgentACPSpec(
                    input=OverallState.model_json_schema(),
                    output=OverallState.model_json_schema(),
                    config=ConfigModel.model_json_schema(),
                    capabilities=Capabilities(
                        threads=False, callbacks=False, interrupts=False, streaming=None
                    ),
                    custom_streaming_update=None,
                    thread_state=None,
                    interrupts=None,
                ),
                deployment=AgentDeployment(
                    deployment_options=[
                        DeploymentOptions(
                            root=SourceCodeDeployment(
                                type="source_code",
                                name="source_code_local",
                                url=AnyUrl("file://../"),
                                framework_config=LangGraphConfig(
                                    framework_type="langgraph",
                                    graph="marketing_campaign.app:graph",
                                ),
                            )
                        )
                    ],
                    env_vars=[
                        EnvVar(
                            name="AZURE_OPENAI_API_KEY",
                            desc="Azure key for the OpenAI service",
                        ),
                        EnvVar(
                            name="AZURE_OPENAI_ENDPOINT",
                            desc="Azure endpoint for the OpenAI service",
                        ),
                        EnvVar(name="SENDGRID_API_KEY", desc="Sendgrid API key"),
                    ],
                    agent_deps=[
                        AgentDependency(
                            name="mailcomposer",
                            ref=AgentRef(
                                name="org.agntcy.mailcomposer",
                                version="0.0.1",
                                url=AnyUrl(f"file://{mailcomposer_dependency_manifest}"),
                            ),
                            deployment_option=None,
                            env_var_values=None,
                        ),
                        AgentDependency(
                            name="email_reviewer",
                            ref=AgentRef(
                                name="org.agntcy.email_reviewer",
                                version="0.0.1",
                                url=AnyUrl(f"file://{email_reviewer_dependency_manifest}"),
                            ),
                            deployment_option=None,
                            env_var_values=None,
                        ),
                    ],
                ),
            ),
        ),
    ],
)

with open(
    f"{Path(__file__).parent.parent.parent}/manifests/marketing-campaign.json", "w"
) as f:
    json_content = manifest.model_dump_json(
        exclude_unset=True, exclude_none=True, indent=2
    )
    f.write(json_content)
    f.write("\n")
```

### Understanding the Manifest Generator Structure

Let's break down the components of our manifest generator:

1. **Metadata**: Defines basic information as unique name of the agent (`org.agntcy.marketing-campaign`), its version number, and a human-readable description explaining its purpose or functionality.

2. **Specs**: Establishes how the agent communicates by defining expected input/output formats using `OverallState` JSON schemas, configuration options through `ConfigModel`, and supported capabilities.

3. **Deployment**: This section contains deployment-related information:
   - `deployment_options`: Defines how the agent can be deployed
     - `url=AnyUrl("file://.")`: Specifies that the source code is located in the current directory (relative to where the manifest is being used)
     - `framework_config`: Specifies that this is a LangGraph application with the graph defined in `marketing_campaign.app:graph`

   - `env_vars`: Lists the environment variables required by the marketing campaign.
   - `dependencies`: Lists the agents that our application depends on. Each dependency specifies:
     - The local name used to refer to the dependency
     - The reference to the agent manifest file (`./manifests/mailcomposer.json`)

### Generating the Manifest

Now, let's run our script to generate the manifest:

```bash
# Install the current project
poetry install

# Run the manifest generator
poetry run python src/marketing_campaign/generate_manifest.py
```

This will create a file called `marketing-campaign.json` in the `manifests` directory, which contains all the information needed for:

* Using our Marketing Campaign application as a dependency in other applications
* Deploying and running our application through the Workflow Server Manager

We'll focus on the second point and see how to execute our application using the Workflow Server Manager.


## Step 8: Review Resulting Application

Below is the final graph that represents the **complete process** of composing, reviewing, and sending an email. This graph shows how agents are connected, how inputs and outputs are processed, and how the application adapts dynamically based on user interactions.

![Final LangGraph Application](./_static/marketing_campaign_final.png)

Our completed application now implements a robust workflow where:

The MAS begins with the `process_inputs` node and transitions to the `mailcomposer` node, where the email draft is created. A **conditional edge** allows the user to interact with the `mailcomposer` until they are satisfied with the composed email. Once confirmed, the workflow proceeds through the following nodes in sequence:

1. **`email_reviewer`**: Reviews and refines the email content.
2. **`prepare_sendgrid_input`**: Prepares the input for the SendGrid API.
3. **`sendgrid`**: Sends the email using the SendGrid API.
4. **`prepare_output`**: Consolidates the final output and logs the result.

This application review highlights the **importance of input and output transformations**, the role of the **I/O Mapper** in ensuring compatibility between agents, and the flexibility provided by conditional edges to adapt the workflow dynamically. With this architecture, the system achieves a robust and user-friendly process for managing email campaigns.

## Step 9: Execute Application through Workflow Server Manager

After generating the manifest, we can deploy and run our application using the Workflow Server Manager. This allows us to execute the entire multi-agent system as a distributed application with all dependencies properly managed.

### Installing the Workflow Server Manager

First, download the Workflow Server Manager CLI appropriate for your operating system from
the [releases page](https://github.com/agntcy/workflow-srv-mgr/releases). Note that the
latest version may be later (semantically) than the version in the example below. Make sure
to execute these commands from the root directory of your project:

```bash
# For macOS with Apple Silicon (run from project root)
curl -L https://github.com/agntcy/workflow-srv-mgr/releases/download/v0.3.2/wfsm0.3.2_darwin_arm64.tar.gz -o wfsm.tar.gz
tar -xzf wfsm.tar.gz # Keep the extracted wfsm binary it in the project root
chmod +x wfsm
# For other platforms, download the appropriate binary from the releases page
```

Follow these [instructions](https://docs.agntcy.org/pages/agws/workflow_server_manager.html#installation) to install the Agent Workflow Server Manager

### Configuring the Application Environment

Before starting the workflow server, create a configuration file that provides the necessary environment variables for the marketing-campaign application and its dependencies. Create a file named `marketing_campaign_config.yaml` in your project root directory:

```yaml
# marketing_campaign_config.yaml
config:
    email_reviewer:
        port: 0
        apiKey: 799cccc7-49e4-420a-b0a8-e4de949ae673
        id: 45fb3f84-c0d7-41fb-bae3-363ca8f8092a
        envVars:
          AZURE_OPENAI_API_KEY: "[YOUR AZURE OPEN API KEY]"
          AZURE_OPENAI_ENDPOINT: "https://[YOUR ENDPOINT].openai.azure.com"
          AZURE_OPENAI_API_VERSION: "2024-08-01-preview"
    mailcomposer:
        port: 0
        apiKey: a9ee3d6a-6950-4252-b2f0-ad70ce57d603
        id: 76363e34-d684-4cab-b2b7-2721c772e42f
        envVars:
          AZURE_OPENAI_API_KEY: "[YOUR AZURE OPEN API KEY]"
          AZURE_OPENAI_ENDPOINT: "https://[YOUR ENDPOINT].openai.azure.com"
    org.agntcy.marketing-campaign:
        port: 65222
        apiKey: 12737451-d333-41c2-b3dd-12f15fa59b38
        id: d6306461-ea6c-432f-b6a6-c4feaa81c19b
        envVars:
          AZURE_OPENAI_API_KEY: "[YOUR AZURE OPEN API KEY]"
          AZURE_OPENAI_ENDPOINT: "https://[YOUR ENDPOINT].openai.azure.com"
          SENDGRID_HOST: "http://host.docker.internal:8080"
          SENDGRID_API_KEY: "[YOUR SENDGRID_API_KEY]"
          LOG_LEVEL: debug
```

> **Note**: Replace placeholder values with your actual API keys and endpoints. The `SENDGRID_HOST` is set to `http://host.docker.internal:8080` to allow communication with a API Bridge service that will locally run in Docker.

### Setting Up the SendGrid API Bridge

Before testing the full application workflow, you need to set up the SendGrid API Bridge locally. Follow the detailed guide in the [API Bridge documentation](https://docs.agntcy.org/pages/syntactic_sdk/api_bridge_agent.html#an-example-with-sendgrid-api) for complete instructions.

### Deploying the Application

Now, deploy the Marketing Campaign workflow server using the manifest we generated. Run this command from the root directory of your project:

```bash
./wfsm deploy -m ./manifests/marketing-campaign.json -c ./marketing_campaign_config.yaml --dryRun=false
```

If the deployment is successful, you'll see output similar to:
```plaintext
2025-06-16T15:53:19+02:00 INF ---------------------------------------------------------------------
2025-06-16T15:53:19+02:00 INF ACP agent deployment name: org.agntcy.marketing-campaign
2025-06-16T15:53:19+02:00 INF ACP agent running in container: org.agntcy.marketing-campaign, listening for ACP requests on: http://127.0.0.1:65222
2025-06-16T15:53:19+02:00 INF Agent ID: d6306461-ea6c-432f-b6a6-c4feaa81c19b
2025-06-16T15:53:19+02:00 INF API Key: 12737451-d333-41c2-b3dd-12f15fa59b38
2025-06-16T15:53:19+02:00 INF API Docs: http://127.0.0.1:65222/agents/d6306461-ea6c-432f-b6a6-c4feaa81c19b/docs
2025-06-16T15:53:19+02:00 INF ---------------------------------------------------------------------
```

Take note of the **Agent ID**, **API Key**, and **Host** information, as you'll need them to interact with the deployed application.


### Testing the Application with ACP Client

To test our application, we'll use an ACP client that allows us to communicate with the deployed workflow server:

1. Download the client script by running the following command from the root of the project:
    ```bash
    # Download the ACP client example from the agntcy/agentic-apps repository
    curl https://raw.githubusercontent.com/agntcy/agentic-apps/refs/heads/main/marketing-campaign/src/marketing_campaign/main_acp_client.py -o src/marketing_campaign/main_acp_client.py
    ```

2. Set the environment variables with the information from your configuration:
    ```bash
    export MARKETING_CAMPAIGN_HOST="http://localhost:65222"  # Use the host from your logs
    export MARKETING_CAMPAIGN_ID="d6306461-ea6c-432f-b6a6-c4feaa81c19b"  # Use your actual Agent ID
    export MARKETING_CAMPAIGN_API_KEY='{"x-api-key": "12737451-d333-41c2-b3dd-12f15fa59b38"}'  # Use your actual API Key

    # Configuration of the application
    export RECIPIENT_EMAIL_ADDRESS="recipient@example.com"
    export SENDER_EMAIL_ADDRESS="sender@example.com" # Sender email address as configured in SendGrid
    ```

3. Run the ACP client:
    ```bash
    poetry run python src/marketing_campaign/main_acp_client.py
    ```

4. Interact with the application:
   - Describe the marketing campaign email you want to compose
   - Refine the email content through conversation with the Mail Composer agent
   - Type "OK" when you're satisfied with the draft
   - The Email Reviewer agent will review and improve the email for your target audience
   - The email will be sent to the specified recipient via SendGrid

Through this client interaction, you can experience the complete workflow of our multi-agent system, from email composition to delivery, with all the intermediate processing steps handled automatically.

The Workflow Server Manager makes it easy to deploy and run complex multi-agent applications, handling the dependencies, environment configuration, and communication between components.

### Conclusion

In this tutorial, we demonstrated how to build a complete Multi-Agent System (MAS) using the ACP SDK. Starting from a basic LangGraph skeleton application, we progressively:

1. Integrated remote agents using ACP nodes
2. Defined states to manage data flow between components
3. Implemented advanced features such as the I/O Mapper and API Bridge integration
4. Generated a deployable manifest for our application
5. Executed our application through the Workflow Server Manager

These components allowed us to create a dynamic and flexible workflow that ensures compatibility between agents, adapts to user interactions, and can be deployed as a complete distributed system.

By following this approach, you can design and implement your own MAS tailored to specific use cases, leveraging the power of ACP to enable communication and collaboration between distributed agents.
