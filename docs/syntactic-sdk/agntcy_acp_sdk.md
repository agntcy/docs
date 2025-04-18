# Agntcy ACP Client SDK

## Introduction

The Agent Connect Protocol SDK is an open-source library designed to
facilitate the adoption of the Agent Connect Protocol. It offers tools
for client implementations, enabling seamless integration, and communication
between multi-agent systems.

The SDK is current available in [Python](https://pypi.org/project/agntcy-acp/) [![PyPI version](https://img.shields.io/pypi/v/agntcy-acp.svg)](https://pypi.org/project/agntcy-acp/).

## Getting Started with the client

To use the package, follow the steps below.

### Requirements.

Python 3.9+

### Installation

Install the latest version from PyPi:
```shell
pip install agntcy-acp
```

### Usage

```python
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

All URIs are relative to *http://localhost*

## Using ACP with LangGraph


## Testing

To test the package, run `make test`.

## Roadmap

See the [open issues](https://github.com/agntcy/acp-sdk/issues) for a list of proposed features and known issues.