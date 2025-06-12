# IO Mapper Agent

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-fbab2c.svg)](https://github.com/agntcy/acp-sdk/blob/main/CODE_OF_CONDUCT.md)

## About the IO Mapper Agent

When connecting agents in an application, the output of an agent needs to be compatible with the input of the agent that is connected to it. This compatibility needs to be guaranteed at three different levels:

1. Transport level: the two agents need to use the same transport protocol.
2. Format level: the two agents need to carry information using the same format (for example, the same JSON data structures).
3. Semantic level: the two agents need to “talk about the same thing”.

Communication between agents is not possible if there are discrepancies between the agents at any of these levels.

Ensuring that agents are semantically compatible, that is, the output of the one agent contains the information needed
by later agents, is an problem of composition or planning in the application. The IO Mapper Agent
addresses level 2 and 3 compatibility. It is a component, implemented as an agent, that can make use of an LLM
to transform the output of one agent to become compatible to the input of another agent. This can mean
many different things:

- JSON structure transcoding: A JSON dictionary needs to be remapped into another JSON dictionary.
- Text summarisation: A text needs to be summarised or some information needs to be removed.
- Text translation: A text needs to be translated from one language to another.
- Text manipulation: Part of the information of one text needs to be reformulated into another text.
- A combination of the above.

The IO mapper Agent can be fed the schema definitions of inputs and outputs as defined by the `Agent Connect Protocol <https://github.com/agntcy/acp-spec>`_.

## Getting Started

### Prerequisites

- [Poetry](https://python-poetry.org/)
- [cmake](https://cmake.org/)

### Use in your project

To install the IO Mapper Agent, run the following command:

```sh
pip install agntcy-iomapper
```

To get a local copy up and running, follow the steps below.



####  Clone the repository

``` sh
git clone https://github.com/agntcy/iomapper-agnt.git
```

#### Install dependecies

``` sh
poetry install
```

## Usage

There are several different ways to leverage the IO Mapper functions in
Python. There is an [How to use the Agent IO mapping](#how-to-use-the-agent-io-mapping) using
models that can be invoked on different AI platforms and an imperative
interface that does deterministic JSON remapping without using any AI
models.

## Key Features

The IO Mapper Agent uses an LLM to transform the inputs (typically the
output of an agent) to match the desired output (typically the input of
another agent). As such, it additionally supports specifying the model
prompts for the translation. The configuration object provides a
specification for the system and default user prompts:

This project supports specifying model interactions using
[LangGraph](https://langchain-ai.github.io/langgraph/).

## How to use the Agent IO mapping

!!! note
    For each example, the detailed process of creating agents and
    configuring the respective multi-agent software is omitted. Instead,
    only the essential steps for configuring and integrating the IO mapper
    agent are presented.

## LangGraph

We support usages with both LangGraph state defined with TypedDict or as
a Pydantic object

## Entities

### IOMappingAgentMetadata

::: agntcy_iomapper.base.IOMappingAgentMetadata

### IOMappingAgent

::: agntcy_iomapper.agent.IOMappingAgent

## LangGraph Example 1

This example involves a multi-agent software system designed to process a create
engagement campaign and share within an organization. It interacts with an agent
specialized in creating campaigns, another agent specialized in identifying suitable
users. The information is then relayed to an IO mapper, which converts the list
of users and the campaign details to present statistics about the campaign.

### Define an agent io mapper metadata

```python
metadata = IOMappingAgentMetadata(
    input_fields=["selected_users", "campaign_details.name"],
    output_fields=["stats.status"],
)
```


The above instruction directs the IO mapper agent to utilize the `selected_users`
and `name` from the `campaign_details` field and map them to the `stats.status`.
No further information is needed since the type information can be derived from
the input data which is a pydantic model.

!!! note "Tip"
    Both input_fields and output_fields can also be sourced with a list composed
    of str and/or instances of FieldMetadata as the bellow example shows

```python
metadata = IOMappingAgentMetadata(
    input_fields=[
        FieldMetadata(
            json_path="selected_users", description="A list of users to be targeted"
        ),
        FieldMetadata(
            json_path="campaign_details.name",
            description="The name that can be used by the campaign",
            examples=["Campaign A"]
        ),
    ],
    output_fields=["stats"],
)
```

### Define an Instance of the Agent

```
mapping_agent = IOMappingAgent(metadata=metadata, llm=llm)
```

### Add the node to the LangGraph graph

```python
workflow.add_node(
    "io_mapping",
    mapping_agent.langgraph_node,
)
```

### Add the Edge

With the edge added, you can run the your LangGraph graph.

```python
workflow.add_edge("create_communication", "io_mapping")
workflow.add_edge("io_mapping", "send_communication")
```

## LangGraph Example 2

This example involves a multi-agent software system designed to process a list
of ingredients. It interacts with an agent specialized in recipe books to identify
feasible recipes based on the provided ingredients. The information is then relayed
to an IO mapper, which converts it into a format suitable for display to the user.

### Define an Agent IO Mapper Metadata

```python
metadata = IOMappingAgentMetadata(
    input_fields=["documents.0.page_content"],
    output_fields=["recipe"],
    input_schema=TypeAdapter(GraphState).json_schema(),
    output_schema={
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "ingredients": {"type": "array", "items": {"type": "string"}},
            "instructions": {"type": "string"},
        },
        "required": ["title", "ingredients, instructions"],
    },
)
```

### Define an Instance of the Agent

```python
mapping_agent = IOMappingAgent(metadata=metadata, llm=llm)
```

### Add the node to the LangGraph graph

```python
graph.add_node(
    "recipe_io_mapper",
    mapping_agent.langgraph_node,
)
```

### Add the Edge

With the edge added, you can run the your LangGraph graph.

```python
graph.add_edge("recipe_expert", "recipe_io_mapper")
```

## LlamaIndex

We support both LlamaIndex Workflow and the new AgentWorkflow multi agent software

### Entities

#### IOMappingInputEvent

... agntcy_iomapper.IOMappingInputEvent

#### IOMappingOutputEvent

... agntcy_iomapper.IOMappingOutputEvent

## Example of usage in a LlamaIndex workflow

In this example we recreate the campaign workflow using `LlamaIndex workflow <https://docs.llamaindex.ai/en/stable/module_guides/workflow/>`_

### Begin by importing the neccessary object

```python
from agntcy_iomapper import IOMappingAgent, IOMappingAgentMetadata
```

### Define the workflow

```python hl_lines="35-49"
class CampaignWorkflow(Workflow):
    @step
    async def prompt_step(self, ctx: Context, ev: StartEvent) -> PickUsersEvent:
        await ctx.set("llm", ev.get("llm"))
        return PickUsersEvent(prompt=ev.get("prompt"))

    @step
    async def pick_users_step(
        self, ctx: Context, ev: PickUsersEvent
    ) -> CreateCampaignEvent:
        return CreateCampaignEvent(list_users=users)

    # The step that will trigger IO mapping
    @step
    async def create_campaign(
        self, ctx: Context, ev: CreateCampaignEvent
    ) -> IOMappingInputEvent:
        prompt = f"""
        You are a campaign builder for company XYZ. Given a list of selected users and a user prompt, create an engaging campaign.
        Return the campaign details as a JSON object with the following structure:
        {{
            "name": "Campaign Name",
            "content": "Campaign Content",
            "is_urgent": yes/no
        }}
        Selected Users: {ev.list_users}
        User Prompt: Create a campaign for all users
        """
        parser = PydanticOutputParser(output_cls=Campaign)
        llm = await ctx.get("llm", default=None)

        llm_response = llm.complete(prompt)
        try:
            campaign_details = parser.parse(str(llm_response))
            metadata = IOMappingAgentMetadata(
                input_fields=["selected_users", "campaign_details.name"],
                output_fields=["stats"],
            )
            config = LLamaIndexIOMapperConfig(llm=llm)

            io_mapping_input_event = IOMappingInputEvent(
                metadata=metadata,
                config=config,
                data=OverallState(
                    campaign_details=campaign_details,
                    selected_users=ev.list_users,
                ),
            )
            return io_mapping_input_event
        except Exception as e:
            print(f"Error parsing campaign details: {e}")
            return StopEvent(result=f"{e}")

    @step
    async def after_translation(self, evt: IOMappingOutputEvent) -> StopEvent:
        return StopEvent(result="Done")
```

!!!note "Tip"
    The highlighted lines shows how the io mapper can be triggered

### Add The IO mapper step

```python
w = CampaignWorkflow()
IOMappingAgent.as_worfklow_step(workflow=w)
```

## Example of usage in a LlamaIndex AgentWorkflow

In this example we recreate the recipe workflow using `LlamaIndex AgentWorkflow <https://docs.llamaindex.ai/en/stable/module_guides/workflow/>`_

### Import the necessary objects

```
from agntcy_iomapper import FieldMetadata, IOMappingAgent, IOMappingAgentMetadata
```

### Define an instance of the IOMappingAgentMetadata

```python
mapping_metadata = IOMappingAgentMetadata(
        input_fields=["documents.0.text"],
        output_fields=[
            FieldMetadata(
                json_path="recipe",
                description="this is a recipe for the ingredients you've provided",
            )
        ],
        input_schema=TypeAdapter(GraphState).json_schema(),
        output_schema={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "ingredients": {"type": "array", "items": {"type": "string"}},
                "instructions": {"type": "string"},
            },
            "required": ["title", "ingredients, instructions"],
        },
    )
```


### Finally define the IOMappingAgent and add it to the AgentWorkflow.

Important to note that a tool is passed, to instruct the io mapper where to go next in the flow.

```python
io_mapping_agent = IOMappingAgent.as_workflow_agent(
    mapping_metadata=mapping_metadata,
    llm=llm,
    name="IOMapperAgent",
    description="Useful for mapping a recipe document into recipe object",
    can_handoff_to=["Formatter_Agent"],
    tools=[got_to_format],
)


io_mapping_agent = IOMappingAgent.as_workflow_agent(
    mapping_metadata=mapping_metadata,
    llm=llm,
    name="IOMapperAgent",
    description="Useful for mapping a recipe document into recipe object",
    can_handoff_to=["Formatter_Agent"],
    tools=[got_to_format],
)
```


## Use Examples

1. Install:
  - `cmake <https://cmake.org/>`_
  - `pip <https://pip.pypa.io/en/stable/installation/>`_

2. From the `examples` folder run the desired make command, for example:

```bash
make make run_lg_eg_py
```

## Contributing

Contributions are what make the open source community such an amazing place to
learn, inspire, and create. Any contributions you make are **greatly
appreciated**. For detailed contributing guidelines, please see
`CONTRIBUTING.md <https://github.com/agntcy/acp-sdk/blob/main/docs/CONTRIBUTING.md>`_


## Copyright Notice and License

`Copyright Notice and License <https://github.com/agntcy/acp-sdk/blob/main/LICENSE>`_

Copyright (c) 2025 Cisco and/or its affiliates.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.