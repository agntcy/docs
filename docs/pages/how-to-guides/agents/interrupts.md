# Interrupts Langgraph

This tutorial guides you through creating an agentic mail composer application with interrupts capability. Interrupts allow your agent to pause execution, prompt the user for additional information, and then resume processing.

## Overview

We'll build a mail composer agent that helps users draft marketing emails. The agent follows this workflow:
1. Engage in conversation with the user to gather email content details
2. Generate a well-structured marketing email
3. Use interrupts to ask for email format preferences
4. Deliver the final email in the requested format

## Prerequisites

- Python 3.9 or higher
- Poetry 2.0 or higher
- Workflow Server Manager (wfsm)
- Azure OpenAI API key and endpoint

## Setting up the Project

First, let's set up our project using Poetry:

```bash
# Create a new Poetry project
poetry new --python='>=3.9,<4.0' mailcomposer-agent
cd mailcomposer-agent

# Add all dependencies
poetry add python-dotenv langgraph langchain-openai langchain pydantic agntcy-acp

# Install the current project
poetry install
```

Poetry automatically creates the project structure with a src/ directory, so we'll use that convention for our files.

## Step 1: Creating the Basic Mail Composer Agent

Let's start by creating the basic mail composer agent without interrupt functionality. We'll need two files:

1. First, create the state models:

```python
# filepath: src/mailcomposer_agent/state.py
from enum import Enum
from typing import Optional, Annotated

from pydantic import BaseModel, Field
import operator

class Type(Enum):
    human = 'human'
    assistant = 'assistant'
    ai = 'ai'


class Message(BaseModel):
    type: Type = Field(
        ...,
        description='indicates the originator of the message, a human or an assistant',
    )
    content: str = Field(..., description='the content of the message')


class ConfigSchema(BaseModel):
    test: bool


class AgentState(BaseModel):
    messages: Annotated[Optional[list[Message]], operator.add] = []
    is_completed: Optional[bool] = None

class StatelessAgentState(BaseModel):
    messages: Optional[list[Message]] = []
    is_completed: Optional[bool] = None


class OutputState(AgentState):
    final_email: Optional[str] = Field(
        default=None,
        description="Final email produced by the mail composer, in html format"
    )

class StatelessOutputState(StatelessAgentState):
    final_email: Optional[str] = Field(
        default=None,
        description="Final email produced by the mail composer, in html format"
    )
```

2. Now, let's create the logic for our mail composer agent:

```python
# filepath: src/mailcomposer_agent/mailcomposer.py
import os
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from langchain_openai import AzureChatOpenAI
from pydantic import SecretStr
from langchain.prompts import PromptTemplate

from .state import (
    OutputState,
    AgentState,
    StatelessAgentState,
    StatelessOutputState,
    Message,
    Type as MsgType,
)

api_key = os.getenv("AZURE_OPENAI_API_KEY")
if not api_key:
    raise ValueError("AZURE_OPENAI_API_KEY must be set as an environment variable.")

azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
if not azure_endpoint:
    raise ValueError("AZURE_OPENAI_ENDPOINT must be set as an environment variable.")

is_stateless = os.getenv("STATELESS", "true").lower() == "true"

llm = AzureChatOpenAI(
    api_key=SecretStr(api_key),
    azure_endpoint=azure_endpoint,
    model="gpt-4o",
    openai_api_type="azure_openai",
    api_version="2024-07-01-preview",
    temperature=0,
    max_retries=10,
    seed=42,
)

# Writer and subject role prompts
MARKETING_EMAIL_PROMPT_TEMPLATE = PromptTemplate.from_template(
    """
You are a highly skilled writer and you are working for a marketing company.
Your task is to write formal and professional emails. We are building a publicity campaign and we need to send a massive number of emails to many clients.
The email must be compelling and adhere to our marketing standards.

If you need more details to complete the email, please ask me.
Once you have all the necessary information, please create the email body. The email must be engaging and persuasive. The subject that cannot exceed 5 words (no bold).
The email should be in the following format
{{separator}}
subject
body
{{separator}}
DO NOT FORGET TO ADD THE SEPARATOR BEFORE THE SUBECT AND AFTER THE EMAIL BODY!
SHOULD NEVER HAPPPEN TO HAVE THE SEPARATOR AFTER THE SUBJECT AND BEFORE THE EMAIL BODY! NEVER AFTER THE SUBJECT!
DO NOT ADD EXTRA TEXT IN THE EMAIL, LIMIT YOURSELF IN GENERATING THE EMAIL
""",
    template_format="jinja2",
)

SEPARATOR = "**************"

def extract_mail(messages) -> str:
    for m in reversed(messages):
        splits: list[str] = []
        if isinstance(m, Message):
            if m.type == MsgType.human:
                continue
            splits = m.content.split(SEPARATOR)
        if isinstance(m, dict):
            if m.get("type", "") == "human":
                continue
            splits = m.get("content", "").split(SEPARATOR)
        if len(splits) >= 3:
            return splits[len(splits) - 2].strip()
        elif len(splits) == 2:
            return splits[1].strip()
        elif len(splits) == 1:
            return splits[0]
    return ""

def should_format_email(state: AgentState | StatelessAgentState):
    # In the basic version, we just return END
    return END

def convert_messages(messages: list) -> list[BaseMessage]:
    converted = []
    for m in messages:
        if isinstance(m, Message):
            mdict = m.model_dump()
        else:
            mdict = m
        if mdict["type"] == "human":
            converted.append(HumanMessage(content=mdict["content"]))
        else:
            converted.append(AIMessage(content=mdict["content"]))

    return converted

# Define mail_agent function
def email_agent(
    state: AgentState | StatelessAgentState,
) -> OutputState | AgentState | StatelessOutputState | StatelessAgentState:
    """This agent is a skilled writer for a marketing company, creating formal and professional emails for publicity campaigns.
    It interacts with users to gather the necessary details.
    Once the user approves by sending "is_completed": true, the agent outputs the finalized email in "final_email".
    """
    # Check subsequent messages and handle completion
    return final_output(state) if state.is_completed else generate_email(state)

def final_output(
    state: AgentState | StatelessAgentState,
) -> OutputState | AgentState | StatelessOutputState | StatelessAgentState:
    final_mail = extract_mail(state.messages)

    output_state: OutputState = OutputState(
        messages=state.messages,
        is_completed=state.is_completed,
        final_email=final_mail,
    )
    return output_state

def generate_email(
    state: AgentState | StatelessAgentState,
) -> (
    OutputState | AgentState | StatelessOutputState | StatelessAgentState
):  # Append messages from state to initial prompt
    messages = [
        Message(
            type=MsgType.human,
            content=MARKETING_EMAIL_PROMPT_TEMPLATE.format(separator=SEPARATOR),
        )
    ] + state.messages

    # Call the LLM
    ai_message = Message(
        type=MsgType.ai, content=str(llm.invoke(convert_messages(messages)).content)
    )

    if is_stateless:
        return {"messages": state.messages + [ai_message]}
    else:
        return {"messages": [ai_message]}

# Build the graph
if is_stateless:
    graph_builder = StateGraph(StatelessAgentState, output=StatelessOutputState)
else:
    graph_builder = StateGraph(AgentState, output=OutputState)

graph_builder.add_node("email_agent", email_agent)

graph_builder.add_edge(START, "email_agent")
graph_builder.add_edge("email_agent", END)

if is_stateless:
    print("mailcomposer - running in stateless mode")
    graph = graph_builder.compile()
else:
    print("mailcomposer - running in stateful mode")
    checkpointer = InMemorySaver()
    graph = graph_builder.compile(checkpointer=checkpointer)
```

> **Note**: The checkpointer setup in `build_graph()` is critical for interrupts to work properly.
> When using interrupts, we must run the agent in stateful mode with a checkpointer configured:
>
> * The checkpointer preserves the graph's execution state when an interrupt occurs,
> allowing it to resume from exactly where it left off after receiving user input.\
> Without this persistence mechanism, the graph would have no memory of what happened
> before the interrupt, making it impossible to continue execution correctly.

## Step 2: Generating the Agent Manifest

Next, we need to generate a manifest for our agent. This will allow it to be deployed and used by other systems. Let's create a manifest generator:

```python
# filepath: src/mailcomposer_agent/generate_manifest.py
from pathlib import Path
from pydantic import AnyUrl
from mailcomposer_agent.state import ConfigSchema, StatelessAgentState, StatelessOutputState
from agntcy_acp.manifest import (
    AgentManifest,
    AgentDeployment,
    DeploymentOptions,
    LangGraphConfig,
    EnvVar,
    AgentMetadata,
    AgentACPSpec,
    AgentRef,
    Capabilities,
    SourceCodeDeployment,
)

manifest = AgentManifest(
    metadata=AgentMetadata(
        ref=AgentRef(name="org.agntcy.mailcomposer", version="0.0.1"),
        description="Offer a chat interface to compose an email for a marketing campaign. Final output is the email that could be used for the campaign"
    ),
    specs=AgentACPSpec(
        input=StatelessAgentState.model_json_schema(),
        output=StatelessOutputState.model_json_schema(),
        config=ConfigSchema.model_json_schema(),
        capabilities=Capabilities(
            threads=False,
            callbacks=False,
            interrupts=False,  # No interrupts yet
            streaming=None
        ),
        custom_streaming_update=None,
        thread_state=None,
        interrupts=None  # No interrupts defined yet
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
                        graph="mailcomposer_agent.mailcomposer:graph"
                    )
                )
            )
        ],
        env_vars=[
            EnvVar(name="AZURE_OPENAI_API_KEY", desc="Azure key for the OpenAI service"),
            EnvVar(name="AZURE_OPENAI_ENDPOINT", desc="Azure endpoint for the OpenAI service")
        ],
        dependencies=[]
    )
)

output_dir = Path(__file__).parent.parent.parent / "deploy"
output_dir.mkdir(exist_ok=True)

with open(output_dir / "mailcomposer.json", "w") as f:
    f.write(manifest.model_dump_json(
        exclude_unset=True,
        exclude_none=True,
        indent=2
    ))

print(f"Manifest successfully generated at {output_dir / 'mailcomposer.json'}")
```

Now let's run the manifest generator:

```bash
# Run the manifest generator
poetry run python -m mailcomposer_agent.generate_manifest

# Expected output:
# Manifest successfully generated at /path/to/mailcomposer-agent/deploy/mailcomposer.json
```

With our agent code implemented and the manifest generated, our basic mail composer agent without interrupts is now ready to work. You can already deploy and run it to generate marketing emails through conversation. In the next step, we'll enhance it with interrupt capabilities for a more interactive experience.

## Step 3: Adding Interrupts to the Agent

Now, let's enhance our agent with interrupt capability. Interrupts allow our agent to pause execution, ask the user for additional information, and then resume processing.

> ### Understanding Interrupts in LangGraph
>
> In LangGraph, implementing the `interrupt()` function **requires a stateful application** to preserve state across pauses and resumptions:
>
> * **How interrupts work**: The `interrupt()` function pauses execution at a specific point, often to await human input or external data. When invoked, LangGraph throws a `GraphInterrupt` exception, halting execution and surfacing the interrupt information to the client.
>
> * **Resuming execution**: To resume, the application must provide a `Command` object with the resume key set to the value returned by the `interrupt()` function.
>
> * **State preservation**: When an `interrupt()` occurs, the current state of the graph—including variables, execution progress, and other data—is saved, allowing accurate resumption from the interruption point.
>
> * **Stateless limitations**: Stateless applications cannot retain information about previous interactions, making interrupts impractical as they would lack necessary context to resume correctly.
>
> * **Implementation considerations**: When using `interrupt()`, implement a persistence mechanism (database, in-memory store, etc.) to maintain state during interruptions and ensure seamless resumption.

<!--
### Understanding Interrupts in LangGraph

In LangGraph, implementing the `interrupt()` function necessitates a stateful application because it relies on preserving the application's state across pauses and resumptions. Here's why:

The `interrupt()` function allows a graph's execution to pause at a specific point, often to await human input or external data, before resuming. When an `interrupt()` is invoked, LangGraph throws a `GraphInterrupt` exception, halting the execution and surfacing the interrupt information to the client. To resume execution, the application must provide a `Command` object with the resume key set to the value returned by the `interrupt()` function.

#### The Necessity of Stateful Applications

Stateful applications maintain context between different stages of execution. In the case of LangGraph, when an `interrupt()` occurs, the current state of the graph—including variables, execution progress, and any other relevant data—is saved. This preserved state is crucial for accurately resuming execution from the point of interruption.

In contrast, stateless applications do not retain any information about previous interactions. If an `interrupt()` were used in a stateless context, the application would lack the necessary information to resume execution correctly, leading to potential errors or inconsistent behavior.

#### Implications for Application Design

When designing applications with LangGraph that utilize `interrupt()`, it's essential to implement a persistence mechanism to store the application's state during interruptions. This can involve using databases, in-memory data stores, or other storage solutions to ensure that the state is accurately saved and can be retrieved upon resumption. -->


### Adding Interrupt Support to Our Agent

We need to make the following additions to `mailcomposer.py`:

1. First, add the import for interrupts at the top of the file:

```python
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt  # Add this import for interrupts
```

2. Add the `format_email` function after the `SEPARATOR` constant:

```python
def format_email(state):
    answer = interrupt(
        Message(
            type=MsgType.assistant,
            content="In what format would like your email to be?",
        )
    )
    answer_content = Message(**answer)
    email = extract_mail(state.messages)
    answer_content.content += " This is the email: " + email
    state.messages = (state.messages or []) + [answer_content]
    state_after_formating = generate_email(state)

    interrupt(
        Message(
            type=MsgType.assistant, content="The email is formatted, please confirm"
        )
    )

    state_after_formating = StatelessAgentState(
        **state_after_formating, is_completed=True
    )
    return final_output(state_after_formating)
```

3. Update the `should_format_email` function to check for format requests:

```python
def should_format_email(state: AgentState | StatelessAgentState):
    if state.is_completed and not is_stateless:
        return "format_email"
    return END
```

4. Finally, update the `graph` structure to add the `format_email` node and conditional edges:

```python
if is_stateless:
    graph_builder = StateGraph(StatelessAgentState, output=StatelessOutputState)
else:
    graph_builder = StateGraph(AgentState, output=OutputState)

graph_builder.add_node("email_agent", email_agent)
graph_builder.add_node("format_email", format_email)  # Add this node

graph_builder.add_edge(START, "email_agent")
# This node will only be added in stateful mode since langgraph requires checkpointer if any node should interrupt
graph_builder.add_conditional_edges("email_agent", should_format_email)
graph_builder.add_edge("format_email", END)
graph_builder.add_edge("email_agent", END)

if is_stateless:
    print("mailcomposer - running in stateless mode")
    graph = graph_builder.compile()
else:
    print("mailcomposer - running in stateful mode")
    checkpointer = InMemorySaver()
    graph = graph_builder.compile(checkpointer=checkpointer)
```

The additions we've made implement a formatting feature that:
1. Interrupts the normal flow to ask for formatting preferences
2. Processes the user's response to format the email accordingly
3. Interrupts again to confirm the formatting
4. Completes the email generation process with the requested formatting

## Step 4: Updating the Manifest for Interrupts

Now we need to** update our generated manifest JSON file to include interrupt support**. Open the generated `mailcomposer.json` and make the following key changes:

1. In the capabilities section, change `interrupts` from `false` to `true`:

```json
"capabilities": {
  "threads": false,
  "interrupts": true,  // Change from false to true
  "callbacks": false
}
```

2. Add the interrupts array in the `specs` section:

```json
"interrupts": [
  {
    "interrupt_type": "format_email",
    "interrupt_payload": {
      "$defs": {
        "Message": {
          "properties": {
            "type": {
              "$ref": "#/$defs/Type",
              "description": "indicates the originator of the message, a human or an assistant"
            },
            "content": {
              "description": "the content of the message",
              "title": "Content",
              "type": "string"
            }
          },
          "required": ["type", "content"],
          "title": "Message",
          "type": "object"
        },
        "Type": {
          "enum": ["human", "assistant", "ai"],
          "title": "Type",
          "type": "string"
        }
      }
    },
    "resume_payload": {
      "$defs": {
        "Message": {
          "properties": {
            "type": {
              "$ref": "#/$defs/Type",
              "description": "indicates the originator of the message, a human or an assistant"
            },
            "content": {
              "description": "the content of the message",
              "title": "Content",
              "type": "string"
            }
          },
          "required": ["type", "content"],
          "title": "Message",
          "type": "object"
        },
        "Type": {
          "enum": ["human", "assistant", "ai"],
          "title": "Type",
          "type": "string"
        }
      }
    }
  }
]
```

These changes inform the ACP infrastructure that our agent uses interrupts and specify the format and structure of the interrupt payloads.

## Step 5: Creating the Test Client

To test our Mail Composer Agent with interrupts, we'll create a simple client script that can interact with the agent directly:


```python
# filepath: src/mailcomposer_agent/main.py
import os
from dotenv import load_dotenv, find_dotenv

from mailcomposer_agent.mailcomposer import graph
from mailcomposer_agent.state import Message, OutputState, Type as MsgType
from langgraph.types import Command

def main():
    load_dotenv(dotenv_path=find_dotenv(usecwd=True))

    is_stateless = os.getenv("STATELESS", "true").lower() == "true"
    print(f"Running with STATELESS={is_stateless}")

    output = OutputState(messages=[], final_email=None)
    is_completed = False

    thread = {"configurable": {"thread_id": "foo"}}

    while True:
        if output.messages and len(output.messages) > 0:
            m = output.messages[-1]
            print(f"[Assistant] \t\t>>> {m.content}")
        if output.final_email:
            break
        message = input("YOU [Type OK when you are happy with the email proposed] >>> ")

        if is_stateless:
            nextinput = output.messages + [Message(content=message, type=MsgType.human)]
        else:
            nextinput = [Message(content=message, type=MsgType.human)]

        if message == "OK":
            is_completed = True

        out = graph.invoke(
            {"messages": nextinput, "is_completed": is_completed},
            thread,
        )

        try:
            curr_state = graph.get_state(thread)
            print(f"Current state has {len(curr_state.tasks)} tasks")

            # Check if graph is interrupted by mailcomposer
            while len(curr_state.tasks) and len(curr_state.tasks[0].interrupts) > 0:
                print(f"Interrupt detected with {len(curr_state.tasks[0].interrupts)} interrupts")
                message = input("YOU [INTERRUPT: Type format preference] >>> ")

                command = Command(
                    resume=Message(
                        content=message, type=MsgType.human
                    ).model_dump()
                )

                # Send a signal to the graph to resume execution
                graph.invoke(command, config=thread)
                curr_state = graph.get_state(thread)

        except ValueError as e:
            print(f"Error getting state: {e}")
            # If we get No checkpointer set error
            if "No checkpointer set" in str(e):
                print("Make sure STATELESS=false in your .env file and rebuild the graph")
                break

        output: OutputState = OutputState.model_validate(out)

    print("Final email is:")
    print(output.final_email)

if __name__ == "__main__":
    main()
```

### Running the Agent Locally

You can run the agent locally using the main.py script:

```bash
# Create a .env file with your Azure OpenAI credentials
echo "AZURE_OPENAI_API_KEY=your_api_key" > .env
echo "AZURE_OPENAI_ENDPOINT=your_endpoint" >> .env
echo "STATELESS=false" >> .env

# Run the agent
poetry run python -m mailcomposer_agent.main
```

## Step 6: Running with Workflow Server Manager

Now that we've created our mail composer agent with interrupt support, we can deploy and run it using the Workflow Server Manager (wfsm).

### Setting up the Environment

First, download the Workflow Server Manager for your platform:

```bash
# For macOS with Apple Silicon
curl -L https://github.com/agntcy/workflow-srv-mgr/releases/download/v0.2.2/wfsm0.2.2_darwin_arm64.tar.gz -o wfsm.tar.gz
tar -xzf wfsm.tar.gz
chmod +x wfsm
```

> For other platforms, download the appropriate binary from the [releases page](https://github.com/agntcy/workflow-srv-mgr/releases)

Next, create a configuration file for our mail composer agent:

```yaml
# filepath: mailcomposer-agent/mailcomposer_config.yaml
config:
    org.agntcy.mailcomposer:
        port: 12345
        apiKey: a1b2c3d4-e5f6-a7b8-c9d0-e1f2a3b4c5d6
        id: a1a1a1a1-b2b2-c3c3-d4d4-e5e5e5e5e5e5
        envVars:
          STATELESS: "false"
          AZURE_OPENAI_API_KEY: "your_azure_openai_api_key"
          AZURE_OPENAI_ENDPOINT: "your_azure_openai_endpoint"
```

Replace the placeholders with your actual Azure OpenAI credentials.

### Deploying the Agent

Now, deploy the mail composer agent using wfsm:

```bash
./wfsm deploy -m ./deploy/mailcomposer.json -c ./mailcomposer_config.yaml -b ghcr.io/agntcy/acp/wfsrv:v0.2.7 --dryRun=false
```

## Step 7: Testing Interrupts via Workflow Server

After deploying your agent, you can test the interrupt functionality by directly calling the workflow server API. This allows you to verify that both interrupts work correctly.

For this test, we'll use curl commands to simulate a conversation that includes interrupts.

```bash
curl -X 'POST' \
  'http://127.0.0.1:52384/runs/wait' \
  -H 'accept: application/json' \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
  "agent_id": "YOUR_AGENT_ID",
  "input": {
        "is_completed": true,
      "messages": [
        {
          "type": "human",
          "content": "Email about wooden spoon be inventive on regarding email body"
        },
        {
          "type": "ai",
          "content": "**************\nDiscover Our Wooden Spoons\n**************\nDear [Client'\''s Name],\n\nI hope this message finds you well. We are excited to introduce our latest collection of handcrafted wooden spoons, designed to bring elegance and functionality to your kitchen. Each spoon is meticulously crafted from sustainably sourced wood, ensuring durability and a unique touch to your culinary experience.\n\nOur wooden spoons are not only a practical tool but also a beautiful addition to your kitchen decor. Whether you'\''re stirring, serving, or tasting, these spoons offer a comfortable grip and a smooth finish that enhances your cooking process.\n\nWe invite you to explore our collection and discover the perfect wooden spoon that suits your style and needs. As a valued client, you can enjoy an exclusive discount on your first purchase. Simply use the code WOODEN10 at checkout.\n\nThank you for considering our products. We look forward to serving you with quality and craftsmanship.\n\nWarm regards,\n\n[Your Name]\n[Your Position]\n[Company Name]\n[Contact Information]\n**************"
        },
        {
          "type": "human",
          "content": "OK"
        }
      ]
  },
  "metadata": {},
  "config": {
    "tags": [
      "string"
    ],
    "recursion_limit": 10,
    "configurable": {
      "test": true,
      "thread_id": "1"
    }
  },
  "stream_mode": null,
  "on_disconnect": "cancel",
  "multitask_strategy": "reject",
  "after_seconds": 0,
  "on_completion": "delete"
}'
```

The agent should respond with "interrupted" status and ask what format the email should be:

```bash
{
  "run": {
    "run_id": "YOUR_RUN_ID",
    "thread_id": "YOUR_THREAD_ID",
    "agent_id": "YOUR_AGENT_ID",
    "created_at": "2025-05-23T12:36:24.093877",
    "updated_at": "2025-05-23T12:36:24.106818",
    "status": "interrupted",
    "creation": {
      "agent_id": "YOUR_AGENT_ID",
      "input": {
        "is_completed": true,
        "messages": [
          {
            "type": "human",
            "content": "Email about wooden spoon be inventive on regarding email body"
          },
          {
            "type": "ai",
            "content": "**************\nDiscover Our Wooden Spoons\n**************\nDear [Client's Name],\n\nI hope this message finds you well. We are excited to introduce our latest collection of handcrafted wooden spoons, designed to bring elegance and functionality to your kitchen. Each spoon is meticulously crafted from sustainably sourced wood, ensuring durability and a unique touch to your culinary experience.\n\nOur wooden spoons are not only a practical tool but also a beautiful addition to your kitchen decor. Whether you're stirring, serving, or tasting, these spoons offer a comfortable grip and a smooth finish that enhances your cooking process.\n\nWe invite you to explore our collection and discover the perfect wooden spoon that suits your style and needs. As a valued client, you can enjoy an exclusive discount on your first purchase. Simply use the code WOODEN10 at checkout.\n\nThank you for considering our products. We look forward to serving you with quality and craftsmanship.\n\nWarm regards,\n\n[Your Name]\n[Your Position]\n[Company Name]\n[Contact Information]\n**************"
          },
          {
            "type": "human",
            "content": "OK"
          }
        ]
      },
      "metadata": {},
      "config": {
        "tags": [
          "string"
        ],
        "recursion_limit": 10,
        "configurable": {
          "test": true,
          "thread_id": "1"
        }
      },
      "webhook": null,
      "stream_mode": null,
      "on_disconnect": "cancel",
      "multitask_strategy": "reject",
      "after_seconds": null,
      "on_completion": "delete"
    }
  },
  "output": {
    "type": "interrupt",
    "interrupt": {
      "format_email": {
        "type": "assistant",
        "content": "In what format would like your email to be?"
      }
    }
  }
}
```

Next, respond to the first interrupt with a formatting preference:

```bash
curl -X 'POST' \
  'http://127.0.0.1:52384/runs/YOUR_RUN_ID' \
  -H 'accept: application/json' \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '        {
          "type": "human",
          "content": "Format my email in html"
        }'
```

The response shows that the request is being processed:

```bash
{
  "run_id": "YOUR_RUN_ID",
  "thread_id": "YOUR_THREAD_ID",
  "agent_id": "YOUR_AGENT_ID",
  "created_at": "2025-05-23T12:36:24.093877",
  "updated_at": "2025-05-23T12:43:09.484371",
  "status": "pending",
  "creation": {
    "agent_id": "YOUR_AGENT_ID",
    "input": {
      "is_completed": true,
      "messages": [
        {
          "type": "human",
          "content": "Email about wooden spoon be inventive on regarding email body"
        },
        {
          "type": "ai",
          "content": "**************\nDiscover Our Wooden Spoons\n**************\nDear [Client's Name],\n\nI hope this message finds you well. We are excited to introduce our latest collection of handcrafted wooden spoons, designed to bring elegance and functionality to your kitchen. Each spoon is meticulously crafted from sustainably sourced wood, ensuring durability and a unique touch to your culinary experience.\n\nOur wooden spoons are not only a practical tool but also a beautiful addition to your kitchen decor. Whether you're stirring, serving, or tasting, these spoons offer a comfortable grip and a smooth finish that enhances your cooking process.\n\nWe invite you to explore our collection and discover the perfect wooden spoon that suits your style and needs. As a valued client, you can enjoy an exclusive discount on your first purchase. Simply use the code WOODEN10 at checkout.\n\nThank you for considering our products. We look forward to serving you with quality and craftsmanship.\n\nWarm regards,\n\n[Your Name]\n[Your Position]\n[Company Name]\n[Contact Information]\n**************"
        },
        {
          "type": "human",
          "content": "OK"
        }
      ]
    },
    "metadata": {},
    "config": {
      "tags": [
        "string"
      ],
      "recursion_limit": 10,
      "configurable": {
        "test": true,
        "thread_id": "1"
      }
    },
    "webhook": null,
    "stream_mode": null,
    "on_disconnect": "cancel",
    "multitask_strategy": "reject",
    "after_seconds": null,
    "on_completion": "delete"
  }
}
```

Then respond to the second interrupt that confirms the formatting:

```bash
curl -X 'POST' \
  'http://127.0.0.1:52384/runs/YOUR_RUN_ID' \
  -H 'accept: application/json' \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '        {
          "type": "human",
          "content": "OK"
        }'
```

Finally, retrieve the formatted email:

```bash
curl -X 'GET' \
  'http://127.0.0.1:52384/runs/YOUR_RUN_ID/wait' \
  -H 'accept: application/json' \
  -H 'x-api-key: YOUR_API_KEY'
```

The response will include the HTML-formatted email:

```bash
{
  "run": {
    "run_id": "YOUR_RUN_ID",
    "thread_id": "YOUR_THREAD_ID",
    "agent_id": "YOUR_AGENT_ID",
    "created_at": "2025-05-23T12:36:24.093877",
    "updated_at": "2025-05-23T12:49:58.635417",
    "status": "success",
    "creation": {
      "agent_id": "YOUR_AGENT_ID",
      "input": {
        "is_completed": true,
        "messages": [
          {
            "type": "human",
            "content": "Email about wooden spoon be inventive on regarding email body"
          },
          {
            "type": "ai",
            "content": "**************\nDiscover Our Wooden Spoons\n**************\nDear [Client's Name],\n\nI hope this message finds you well. We are excited to introduce our latest collection of handcrafted wooden spoons, designed to bring elegance and functionality to your kitchen. Each spoon is meticulously crafted from sustainably sourced wood, ensuring durability and a unique touch to your culinary experience.\n\nOur wooden spoons are not only a practical tool but also a beautiful addition to your kitchen decor. Whether you're stirring, serving, or tasting, these spoons offer a comfortable grip and a smooth finish that enhances your cooking process.\n\nWe invite you to explore our collection and discover the perfect wooden spoon that suits your style and needs. As a valued client, you can enjoy an exclusive discount on your first purchase. Simply use the code WOODEN10 at checkout.\n\nThank you for considering our products. We look forward to serving you with quality and craftsmanship.\n\nWarm regards,\n\n[Your Name]\n[Your Position]\n[Company Name]\n[Contact Information]\n**************"
          },
          {
            "type": "human",
            "content": "OK"
          }
        ]
      },
      "metadata": {},
      "config": {
        "tags": [
          "string"
        ],
        "recursion_limit": 10,
        "configurable": {
          "test": true,
          "thread_id": "1"
        }
      },
      "webhook": null,
      "stream_mode": null,
      "on_disconnect": "cancel",
      "multitask_strategy": "reject",
      "after_seconds": null,
      "on_completion": "delete"
    }
  },
  "output": {
    "type": "result",
    "values": {
      "messages": [
        {
          "type": "ai",
          "content": "Sure, I can help you format an email in HTML. Here's an example based on the previous wooden spoon email:\n\n```html\n<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Discover Our Wooden Spoons</title>\n</head>\n<body style=\"font-family: Arial, sans-serif; line-height: 1.6; color: #333;\">\n    <table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">\n        <tr>\n            <td align=\"center\">\n                <table width=\"600\" cellpadding=\"20\" cellspacing=\"0\" border=\"0\" style=\"border: 1px solid #ddd; background-color: #f9f9f9;\">\n                    <tr>\n                        <td>\n                            <h2 style=\"color: #555;\">Discover Our Wooden Spoons</h2>\n                            <p>Dear [Client's Name],</p>\n                            <p>I hope this message finds you well. We are excited to introduce our latest collection of handcrafted wooden spoons, designed to bring elegance and functionality to your kitchen. Each spoon is meticulously crafted from sustainably sourced wood, ensuring durability and a unique touch to your culinary experience.</p>\n                            <p>Our wooden spoons are not only a practical tool but also a beautiful addition to your kitchen decor. Whether you're stirring, serving, or tasting, these spoons offer a comfortable grip and a smooth finish that enhances your cooking process.</p>\n                            <p>We invite you to explore our collection and discover the perfect wooden spoon that suits your style and needs. As a valued client, you can enjoy an exclusive discount on your first purchase. Simply use the code <strong>WOODEN10</strong> at checkout.</p>\n                            <p>Thank you for considering our products. We look forward to serving you with quality and craftsmanship.</p>\n                            <p>Warm regards,</p>\n                            <p>[Your Name]<br>\n                            [Your Position]<br>\n                            [Company Name]<br>\n                            [Contact Information]</p>\n                        </td>\n                    </tr>\n                </table>\n            </td>\n        </tr>\n    </table>\n</body>\n</html>\n```\n\nThis HTML email template includes basic styling and structure to ensure it looks professional and is easy to read. You can customize the content and styles as needed to fit your specific requirements."
        }
      ],
      "is_completed": true,
      "final_email": "Sure, I can help you format an email in HTML. Here's an example based on the previous wooden spoon email:\n\n```html\n<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Discover Our Wooden Spoons</title>\n</head>\n<body style=\"font-family: Arial, sans-serif; line-height: 1.6; color: #333;\">\n    <table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">\n        <tr>\n            <td align=\"center\">\n                <table width=\"600\" cellpadding=\"20\" cellspacing=\"0\" border=\"0\" style=\"border: 1px solid #ddd; background-color: #f9f9f9;\">\n                    <tr>\n                        <td>\n                            <h2 style=\"color: #555;\">Discover Our Wooden Spoons</h2>\n                            <p>Dear [Client's Name],</p>\n                            <p>I hope this message finds you well. We are excited to introduce our latest collection of handcrafted wooden spoons, designed to bring elegance and functionality to your kitchen. Each spoon is meticulously crafted from sustainably sourced wood, ensuring durability and a unique touch to your culinary experience.</p>\n                            <p>Our wooden spoons are not only a practical tool but also a beautiful addition to your kitchen decor. Whether you're stirring, serving, or tasting, these spoons offer a comfortable grip and a smooth finish that enhances your cooking process.</p>\n                            <p>We invite you to explore our collection and discover the perfect wooden spoon that suits your style and needs. As a valued client, you can enjoy an exclusive discount on your first purchase. Simply use the code <strong>WOODEN10</strong> at checkout.</p>\n                            <p>Thank you for considering our products. We look forward to serving you with quality and craftsmanship.</p>\n                            <p>Warm regards,</p>\n                            <p>[Your Name]<br>\n                            [Your Position]<br>\n                            [Company Name]<br>\n                            [Contact Information]</p>\n                        </td>\n                    </tr>\n                </table>\n            </td>\n        </tr>\n    </table>\n</body>\n</html>\n```\n\nThis HTML email template includes basic styling and structure to ensure it looks professional and is easy to read. You can customize the content and styles as needed to fit your specific requirements."
    }
  }
}
```

## Conclusion

In this tutorial, you've built a Mail Composer Agent with interrupt capabilities using LangGraph, running it on the Workflow Server and interacting with it via ACP.

The interrupt feature provided a more interactive experience thanks to the introduction of the human in the loop, allowing the agent to gather additional information during execution and respond dynamically to user needs.

The full working agent code is available in the [agntcy/agentic-apps repository](https://github.com/agntcy/agentic-apps/tree/main/mailcomposer), and you can run it through the Workflow Server exactly as described in this tutorial.
