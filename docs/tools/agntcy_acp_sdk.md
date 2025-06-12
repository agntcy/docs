# Agntcy ACP Client

## Introduction

The Agent Connect Protocol SDK is an open-source library designed to
facilitate the adoption of the Agent Connect Protocol. It offers tools
for client implementations, enabling seamless integration, and communication
between multi-agent systems.

The SDK is current available in [Python](https://pypi.org/project/agntcy-acp/) [![PyPI version](https://img.shields.io/pypi/v/agntcy-acp.svg)](https://pypi.org/project/agntcy-acp/).

## Getting Started with the client

To use the package, follow the steps below.

### Requirements

Python 3.9+

### Installation

Install the latest version from PyPi:
```shell
pip install agntcy-acp
```

### Usage

``` python
from agntcy_acp import AsyncACPClient, AsyncApiClient, ApiException
from agntcy_acp.models import RunCreate

# Defining the host is optional and defaults to http://localhost
config = ApiClientConfiguration(
    host="https://localhost:8081/", 
    api_key={"x-api-key": os.environ["API_KEY"]}, 
    retries=3
)

# Enter a context with an instance of the API client
async with AsyncApiClient(config) as api_client:
    agent_id = 'agent_id_example' # str | The ID of the agent.
    client = AsyncACPClient(api_client)
    
    try:
      api_response = client.create_run(RunCreate(agent_id="my-agent-id"))
      print(f"Run {api_response.run_id} is currently {api_response.status}")
    except ApiException as e:
        print("Exception when calling create_run: %s\n" % e)
```

### Documentation for API Endpoints

The complete documentation for all of the API Endpoints are
available in the reference documentation for the API clients:

  * [ACPClient](https://agntcy.github.io/acp-sdk/html/agntcy_acp.html#agntcy_acp.ACPClient)
  * [AsyncACPClient](https://agntcy.github.io/acp-sdk/html/agntcy_acp.html#agntcy_acp.AsyncACPClient)

## Using ACP with LangGraph

The SDK provides integration with LangGraph with the {py:obj}`agntcy_acp.langgraph.ACPNode` class
that can be used as a graph node:

```python
from enum import Enum
from typing import List, Optional

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from agntcy_acp import ApiClientConfiguration
from agntcy_acp.langgraph.acp_node import ACPNode


class Type(Enum):
    human = 'human'
    assistant = 'assistant'
    ai = 'ai'

class Message(BaseModel):
    type: Type = Field(
        ...,
        description='indicates the originator of the message, a human or an assistant',
    )
    content: str = Field(..., description='the content of the message', title='Content')

class InputSchema(BaseModel):
    messages: Optional[List[Message]] = Field(None, title='Messages')
    is_completed: Optional[bool] = Field(None, title='Is Completed')

class OutputSchema(BaseModel):
    messages: Optional[List[Message]] = Field(None, title='Messages')
    is_completed: Optional[bool] = Field(None, title='Is Completed')
    final_email: Optional[str] = Field(
        None,
        description='Final email produced by the mail composer',
        title='Final Email',
    )

class StateMeasures(BaseModel):
    input: InputSchema
    output: OutputSchema

def main():
    # Instantiate the local ACP node for the remote agent
    acp_node = ACPNode(
        name="mailcomposer",
        agent_id='50272dfd-4c77-4529-abbb-419bb1724230',
        client_config=ApiClientConfiguration.fromEnvPrefix("COMPOSER_"),
        input_path="input",
        input_type=InputSchema,
        output_path="output",
        output_type=OutputSchema,
    )

    # Create the state graph
    sg = StateGraph(StateMeasures)

    # Add edges
    sg.add_edge(START, acp_node.get_name())
    sg.add_edge(acp_node.get_name(), END)

    graph = sg.compile()
    output_state = graph.invoke({
      "input": InputSchema(content=input), 
      "output": OutputSchema(content="bad-output"),
    })
```

## Using the CLI to generate Agent-specific bindings

The Client SDK includes a CLI tool to generate models or OpenAPI specs
specific to an agent using the manifest descriptor. With these models
the agent-specific data sent to ACP can be validated. By default,
only the ACP parameters are validated by the SDK client.

The CLI also provides validators for the ACP descriptor and manifest
files.

You can use the CLI easily:
  * using [poetry](https://python-poetry.org/): `poetry run acp --help`
  * with the package installed: `python3 -m agntcy_acp --help`

Usage: `acp [OPTIONS] COMMAND [ARGS]...`

  Options:

  * `--help`  Show this message and exit.

Commands:

* `generate-agent-models [OPTIONS] AGENT_DESCRIPTOR_PATH`

    Generate pydantic models from agent manifest or descriptor.

  Options:
    
    * `--output-dir TEXT`
    
      Pydantic models for specific agent based on provided
      agent descriptor or agent manifest  [required]

    * `--model-file-name TEXT`
    
      Filename containing the pydantic model of the agent
      schemas

* `generate-agent-oapi [OPTIONS] AGENT_DESCRIPTOR_PATH`

    Generate OpenAPI Spec from agent manifest or descriptor

  Options:

    * `--output TEXT`
    
      OpenAPI output file

* `validate-acp-descriptor [OPTIONS] AGENT_DESCRIPTOR_PATH`

    Validate the Agent Descriptor contained in the file AGENT_DESCRIPTOR_PATH
    against the ACP specification

* `validate-acp-manifest [OPTIONS] AGENT_MANIFEST_PATH`

    Validate the Agent Manifest contained in the file AGENT_MANIFEST_PATH
    against the Manifest specification


## Testing

To run the various unit tests in the package, run `make test`.

## Roadmap

See the [open issues](https://github.com/agntcy/acp-sdk/issues) for a list of proposed features and known issues.

## Client Reference API

For a detailed description of the classes and functions in the SDK, please see the
[agntcy-acp Package Documentation](https://agntcy.github.io/acp-sdk/index.html).