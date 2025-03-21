# Agent Workflow Server

The [Agent Workflow Server](https://github.com/agntcy/workflow-srv) enables participation in the Internet of Agents. It accommodates AI Agents from diverse frameworks and exposes them through Agent Connect Protocol [(ACP)](/pages/connect), regardless of their underlying implementation.

> **NOTE**: If you wish to quickly deploy and run your Agent, please check out the user-facing [Workflow Server Manager](https://github.com/agntcy/workflow-srv-mgr) instead.

## Getting Started

### Prerequisites

You need to have installed the following software to run the Agent Workflow Server:

- Python 3.12 (or above)
- Poetry 2.0 (or above)

### Local development

1. Clone Agent Workflow Server repository: ` git clone https://github.com/agntcy/workflow-srv.git`

1. Copy example env file and adapt if necessary: `cp .env.example .env`

1. Create a virtual environment and install the server dependencies: `poetry install`

1. Install an agent ([See examples](https://github.com/agntcy/acp-sdk/examples/mailcomposer))

   > e.g.: `pip install agntcy/acp-sdk/examples/mailcomposer`

1. Start the server: `poetry run server`

### Generating API

1. If it's the first time you're cloning this repo, initialize submodule: `git submodule update --init --recursive`

1. Run `make generate-api`

Generated code (API routes template and modes) is under `src/agent_workflow_server/generated`.

- If needed, API routes template could be manually copied and implemented under `src/agent_workflow_server/apis`
- Models should not be copied over different places nor modified, but referenced as they are

### Authentication

The Agent Workflow Server, and the underlying Agent, could be optionally authenticated via a pre-defined API Key:

- Set `API_KEY` environment variable with a pre-defined value to enable authentication
- Include the same value in requests from clients via `x-api-key` header

### API Documentation

Once the Agent Workflow Server is running, interactive API docs are available under `/docs` endpoint, redoc documentation under `/redoc` endpoint

## Contributing

### ACP API Contribution

Agent Workflow Server implements ACP specification to expose Agents functionalities. To contribute to the ACP API, check out [Agent Connect Protocol Specification
](https://github.com/agntcy/acp-spec).

### Adapters SDK Contribution

Agent Workflow Server supports different agentic frameworks via `Adapters`.

The process of implementing support of a new framework is pretty straightforward, as the server dinamically loads `Adapters` at runtime.

`Adapters` are placed under `src/agent_workflow_server/agents/adapters` and must implement `BaseAdapter` class.

To support a new framework, or extend functionality, one must implement the `load_agent` method. To invoke that agent, one must implement the `astream` method.

See example below, supposing support to a new framework `MyFramework` should be added.

```python
# src/agent_workflow_server/agents/adapters/myframework.py

class MyAgent(BaseAgent):
    def __init__(self, agent: object):
        self.agent = agent

    async def astream(self, input: dict, config: dict):
        # Call your agent here (and stream events)
        # e.g.: 
        async for event in self.agent.astream(
            input=input, config=config
        ):
            yield event


class MyAdapter(BaseAdapter):
    def load_agent(self, agent: object):
        # Check if `agent` is supported by MyFramework and if so return it
        # e.g.:
        if isinstance(agent, MyAgentType):
            return MyAgent(agent)
        # Optionally add support to other Agent Types:
        # e.g.:
        # if isinstance(agent, MyOtherAgentType):
        #     return MyAgent(MyAgentTypeConv(agent))

```

> For detailed contributing guidelines, please see
> [CONTRIBUTING.md](docs/CONTRIBUTING.md)
