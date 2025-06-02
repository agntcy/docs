# SLIM-MCP

This tutorial demonstrates how to use SLIM (Secure Low-Latency Interactive Messaging) to transport
MCP (Model Context Protocol) messages. SLIM offers two primary integration
options, depending on whether you're building a new system or integrating with
an existing MCP server:

1. **Using SLIM as an MCP Custom Transport Protocol**: MCP is designed to support
   multiple transport protocols, with SLIM now available as one of these options.
   To implement SLIM as a custom transport, you can install the SLIM-MCP package
   through pip and integrate it directly into your application. This approach is
   ideal for new systems where you control both client and server components,
   providing native SLIM support for efficient MCP message transport.

2. **Using SLIM with a Proxy Server**: If you have an existing MCP server running
   that uses SSE (Server-Sent Events) for transport, you can integrate SLIM by
   deploying a proxy server. This proxy handles translation between SLIM clients
   and your SSE-based MCP server, allowing SLIM clients to connect seamlessly
   without requiring modifications to your existing server, making it an
   effective solution for established systems.

This tutorial guides you through both integration methods. You'll learn how to
use SLIM as a custom transport for MCP and how to configure the proxy server to
enable SLIM support for an SSE-based MCP server. By the end, you'll have all the
necessary tools to integrate SLIM with MCP in a way that best fits your system's
architecture.

## Using SLIM as an MCP Custom Transport Protocol

In this section of the tutorial, we implement and deploy two sample
applications:

 - A [LlamaIndex
   agent](https://github.com/agntcy/slim/tree/main/data-plane/integrations/mcp/slim-mcp/examples/llamaindex-time-agent)
   that communicates with an MCP server over SLIM to perform time queries and
   timezone conversions.
 - An [MCP time
   server](https://github.com/agntcy/slim/tree/main/data-plane/integrations/mcp/slim-mcp/examples/mcp-server-time)
   that implements SLIM as its transport protocol and processes requests from the
   LlamaIndex agent.

### Prerequisites

- [UV](https://docs.astral.sh/uv/getting-started/installation/) - A Python
  package installer and environment manager.
- [Docker](https://docs.docker.com/get-started/get-docker/) - For running the
  SLIM instance.

### Setting Up the SLIM Instance

Since the client and server communicate using SLIM, we first need to deploy
a SLIM instance. We are using a pre-built Docker image for this purpose.

First, execute the following command to create a configuration file for SLIM:

```bash
cat << EOF > ./config.yaml
tracing:
  log_level: debug
  display_thread_names: true
  display_thread_ids: true

runtime:
  n_cores: 0
  thread_name: "slim-data-plane"
  drain_timeout: 10s

services:
  slim/0:
    pubsub:
      servers:
        - endpoint: "0.0.0.0:46357"
          tls:
            insecure: true

      clients: []
    controller:
      server:
        endpoint: "0.0.0.0:46358"
        tls:
          insecure: true
EOF
```

Now launch the SLIM instance using the just created configuration file:

```bash
docker run -it \
    -v ./config.yaml:/config.yaml -p 46357:46357 \
    ghcr.io/agntcy/slim:latest /slim --config /config.yaml
```

This command deploys an SLIM instance that listens on port 46357 for incoming
connections. This instance serves as the communication backbone between our
client and server applications.

### Implementing the MCP Server

Next, we'll implement a simple MCP server that processes requests from the
LlamaIndex agent. This server demonstrates how to use SLIM as a custom
transport protocol.

First, create a new directory for our MCP server project:

```bash
mkdir -p mcp-server-time/src/mcp_server_time
cd mcp-server-time
```

Now, create a `pyproject.toml` file in the project root to define the project
dependencies:

```toml
# pyproject.toml
[project]
name = "mcp-server-time"
version = "0.1.0"
description = "MCP server providing tools for time queries and timezone conversions"
requires-python = ">=3.10"
dependencies = ["mcp==1.6.0", "slim-mcp>=0.1.0", "click>=8.1.8"]

[project.scripts]
mcp-server-time = "mcp_server_time:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Next, let's implement the MCP server that handles time queries and timezone
conversions. This implementation is based on the [official MCP example
server](https://github.com/modelcontextprotocol/servers/tree/main/src/time),
modified to support both SLIM and SSE as transport protocols.

Create the following files in your project directory:

<details>

<summary><b>src/mcp_server_time/__init__.py</b></summary>

<br>

```python
# src/mcp_server_time/__init__.py

from .server import main

if __name__ == "__main__":
    main()
```

</details>

<br>

<details>

<summary><b>src/mcp_server_time/server.py</b></summary>

<br>

```python
# src/mcp_server_time/server.py

"""
MCP Time Server - A server designed to handle time and timezone conversion functionalities.
This module offers tools to retrieve the current time across various timezones and convert times between them.
"""

import asyncio
import json
import logging
from collections.abc import Sequence
from datetime import datetime, timedelta
from enum import Enum
from zoneinfo import ZoneInfo

import click
from mcp import types
from mcp.server.lowlevel import Server
from mcp.shared.exceptions import McpError
from pydantic import BaseModel

from slim_mcp import SLIMServer, init_tracing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TimeTools(str, Enum):
    """Enumeration of available time-related tools."""

    GET_CURRENT_TIME = "get_current_time"  # Tool to get current time in a timezone
    CONVERT_TIME = "convert_time"  # Tool to convert time between timezones


class TimeResult(BaseModel):
    """Model representing a time result with timezone information."""

    timezone: str  # IANA timezone name
    datetime: str  # ISO formatted datetime string
    is_dst: bool  # Whether the timezone is in daylight saving time


class TimeConversionResult(BaseModel):
    """Model representing the result of a time conversion between timezones."""

    source: TimeResult  # Source timezone information
    target: TimeResult  # Target timezone information
    time_difference: str  # String representation of time difference (e.g., "+2.0h")


class TimeConversionInput(BaseModel):
    """Model for time conversion input parameters."""

    source_tz: str  # Source timezone
    time: str  # Time to convert in HH:MM format
    target_tz_list: list[str]  # List of target timezones


def get_local_tz(local_tz_override: str | None = None) -> ZoneInfo:
    """
    Get the local timezone information.

    Args:
        local_tz_override: Optional timezone override string

    Returns:
        ZoneInfo: The local timezone information

    Raises:
        McpError: If timezone cannot be determined
    """
    if local_tz_override:
        return ZoneInfo(local_tz_override)

    # Get local timezone from datetime.now()
    tzinfo = datetime.now().astimezone(tz=None).tzinfo
    if tzinfo is not None:
        return ZoneInfo(str(tzinfo))
    raise McpError(
        types.ErrorData(
            code=types.INTERNAL_ERROR,
            message="Could not determine local timezone - tzinfo is None",
        )
    )


def get_zoneinfo(timezone_name: str) -> ZoneInfo:
    """
    Get ZoneInfo object for a given timezone name.

    Args:
        timezone_name: IANA timezone name

    Returns:
        ZoneInfo: The timezone information

    Raises:
        McpError: If timezone is invalid
    """
    try:
        return ZoneInfo(timezone_name)
    except Exception as e:
        raise McpError(
            types.ErrorData(
                code=types.INTERNAL_ERROR,
                message=f"Invalid timezone: {str(e)}",
            )
        )


class TimeServer:
    """Core time server implementation providing time-related functionality."""

    def get_current_time(self, timezone_name: str) -> TimeResult:
        """
        Get current time in specified timezone.

        Args:
            timezone_name: IANA timezone name

        Returns:
            TimeResult: Current time information in the specified timezone
        """
        timezone = get_zoneinfo(timezone_name)
        current_time = datetime.now(timezone)

        return TimeResult(
            timezone=timezone_name,
            datetime=current_time.isoformat(timespec="seconds"),
            is_dst=bool(current_time.dst()),
        )

    def convert_time(
        self, source_tz: str, time_str: str, target_tz: str
    ) -> TimeConversionResult:
        """
        Convert time between timezones.

        Args:
            source_tz: Source timezone name
            time_str: Time to convert in HH:MM format
            target_tz: Target timezone name

        Returns:
            TimeConversionResult: Converted time information

        Raises:
            ValueError: If time format is invalid
        """
        source_timezone = get_zoneinfo(source_tz)
        target_timezone = get_zoneinfo(target_tz)

        try:
            parsed_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            raise ValueError("Invalid time format. Expected HH:MM [24-hour format]")

        # Create a datetime object for today with the specified time
        now = datetime.now(source_timezone)
        source_time = datetime(
            now.year,
            now.month,
            now.day,
            parsed_time.hour,
            parsed_time.minute,
            tzinfo=source_timezone,
        )

        # Convert to target timezone
        target_time = source_time.astimezone(target_timezone)

        # Calculate time difference between timezones
        source_offset = source_time.utcoffset() or timedelta()
        target_offset = target_time.utcoffset() or timedelta()
        hours_difference = (target_offset - source_offset).total_seconds() / 3600

        # Format time difference string
        if hours_difference.is_integer():
            time_diff_str = f"{hours_difference:+.1f}h"
        else:
            # For fractional hours like Nepal's UTC+5:45
            time_diff_str = f"{hours_difference:+.2f}".rstrip("0").rstrip(".") + "h"

        return TimeConversionResult(
            source=TimeResult(
                timezone=source_tz,
                datetime=source_time.isoformat(timespec="seconds"),
                is_dst=bool(source_time.dst()),
            ),
            target=TimeResult(
                timezone=target_tz,
                datetime=target_time.isoformat(timespec="seconds"),
                is_dst=bool(target_time.dst()),
            ),
            time_difference=time_diff_str,
        )


class TimeServerApp:
    """Main application class for the MCP Time Server."""

    def __init__(self, local_timezone: str | None = None):
        """
        Initialize the Time Server application.

        Args:
            local_timezone: Optional override for local timezone
        """
        self.app: Server = Server("mcp-time")
        self.time_server = TimeServer()
        self.local_tz = str(get_local_tz(local_timezone))
        self._setup_tools()

    def _setup_tools(self):
        """Setup tool definitions and handlers for the MCP server."""

        @self.app.list_tools()
        async def list_tools() -> list[types.Tool]:
            """
            List available time tools.

            Returns:
                list[types.Tool]: List of available time-related tools
            """
            return [
                types.Tool(
                    name=TimeTools.GET_CURRENT_TIME.value,
                    description="Get current time in a specific timezones",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "timezone": {
                                "type": "string",
                                "description": f"IANA timezone name (e.g., 'America/New_York', 'Europe/London'). Use '{self.local_tz}' as local timezone if no timezone provided by the user.",
                            }
                        },
                        "required": ["timezone"],
                    },
                ),
                types.Tool(
                    name=TimeTools.CONVERT_TIME.value,
                    description="Convert time between timezones",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "source_timezone": {
                                "type": "string",
                                "description": f"Source IANA timezone name (e.g., 'America/New_York', 'Europe/London'). Use '{self.local_tz}' as local timezone if no source timezone provided by the user.",
                            },
                            "time": {
                                "type": "string",
                                "description": "Time to convert in 24-hour format (HH:MM)",
                            },
                            "target_timezone": {
                                "type": "string",
                                "description": f"Target IANA timezone name (e.g., 'Asia/Tokyo', 'America/San_Francisco'). Use '{self.local_tz}' as local timezone if no target timezone provided by the user.",
                            },
                        },
                        "required": ["source_timezone", "time", "target_timezone"],
                    },
                ),
            ]

        @self.app.call_tool()
        async def call_tool(
            name: str, arguments: dict
        ) -> Sequence[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            """
            Handle tool calls for time queries.

            Args:
                name: Name of the tool to call
                arguments: Dictionary of tool arguments

            Returns:
                Sequence of content types containing the tool response

            Raises:
                ValueError: If tool name is unknown or arguments are invalid
            """

            result: TimeResult | TimeConversionResult

            try:
                match name:
                    case TimeTools.GET_CURRENT_TIME.value:
                        timezone = arguments.get("timezone")
                        if not timezone:
                            raise ValueError("Missing required argument: timezone")
                        result = self.time_server.get_current_time(timezone)

                    case TimeTools.CONVERT_TIME.value:
                        if not all(
                            k in arguments
                            for k in ["source_timezone", "time", "target_timezone"]
                        ):
                            raise ValueError("Missing required arguments")
                        result = self.time_server.convert_time(
                            arguments["source_timezone"],
                            arguments["time"],
                            arguments["target_timezone"],
                        )
                    case _:
                        raise ValueError(f"Unknown tool: {name}")

                return [
                    types.TextContent(
                        type="text", text=json.dumps(result.model_dump(), indent=2)
                    )
                ]

            except Exception as e:
                raise ValueError(f"Error processing mcp-server-time query: {str(e)}")

    async def handle_session(self, session, slim_server, tasks):
        """
        Handle a single session with proper error handling and logging.

        Args:
            session: The session to handle
            slim_server: The SLIM server instance
            tasks: Set of active tasks
        """
        try:
            async with slim_server.new_streams(session) as streams:
                logger.info(
                    f"new session started - session_id: {session.id}, active_sessions: {len(tasks)}"
                )
                await self.app.run(
                    streams[0],
                    streams[1],
                    self.app.create_initialization_options(),
                )
                logger.info(
                    f"session {session.id} ended - active_sessions: {len(tasks)}"
                )
        except Exception:
            logger.error(
                f"Error handling session {session.id}",
                extra={"session_id": session.id},
                exc_info=True,
            )
            raise


async def cleanup_tasks(tasks):
    """
    Clean up all tasks and wait for their completion.

    Args:
        tasks: Set of tasks to clean up
    """
    for task in tasks:
        if not task.done():
            task.cancel()

    if tasks:
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception:
            logger.error("Error during task cleanup", exc_info=True)
            raise


async def serve_slim(
    local_timezone: str | None = None,
    organization: str = "org",
    namespace: str = "ns",
    mcp_server: str = "time-server",
    config: dict = {},
) -> None:
    """
    Main server function that initializes and runs the time server using SLIM transport.

    Args:
        local_timezone: Optional override for local timezone
        organization: Organization name
        namespace: Namespace name
        mcp_server: MCP server name
        config: Server configuration dictionary
    """
    await init_tracing({"log_level": "info"})
    time_app = TimeServerApp(local_timezone)
    tasks: set[asyncio.Task] = set()

    async with SLIMServer(config, organization, namespace, mcp_server) as slim_server:
        try:
            async for new_session in slim_server:
                task = asyncio.create_task(
                    time_app.handle_session(new_session, slim_server, tasks)
                )
                tasks.add(task)
        except Exception:
            logger.error("Error in session handler", exc_info=True)
            raise
        finally:
            await cleanup_tasks(tasks)
            logger.info("Server stopped")


def serve_sse(
    local_timezone: str | None = None,
    port: int = 8000,
) -> None:
    """
    Main server function that initializes and runs the time server using SSE transport.

    Args:
        local_timezone: Optional override for local timezone
        port: Server listening port
    """
    time_app = TimeServerApp(local_timezone)

    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.responses import Response
    from starlette.routing import Mount, Route

    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await time_app.app.run(
                streams[0], streams[1], time_app.app.create_initialization_options()
            )
        return Response()

    starlette_app = Starlette(
        debug=True,
        routes=[
            Route("/sse", endpoint=handle_sse, methods=["GET"]),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

    import uvicorn

    uvicorn.run(starlette_app, host="0.0.0.0", port=port)


class DictParamType(click.ParamType):
    name = "dict"

    def convert(self, value, param, ctx):
        import json

        if isinstance(value, dict):
            return value  # Already a dict (for default value)
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            self.fail(f"{value} is not valid JSON", param, ctx)


@click.command(context_settings={"auto_envvar_prefix": "MCP_TIME_SERVER"})
@click.option(
    "--local-timezone", type=str, help="Override local timezone", default=None
)
@click.option("--transport", default="slim", help="transport option: slim or sse")
@click.option(
    "--port",
    default="8000",
    type=int,
    help="listening port, used only with sse transport",
)
@click.option(
    "--organization",
    default="org",
    help="server organization, used only with slim transport",
)
@click.option(
    "--namespace", default="ns", help="server namespace, used only with slim transport"
)
@click.option(
    "--mcp-server",
    default="time-server",
    help="server name, used only with slim transport",
)
@click.option(
    "--config",
    default={
        "endpoint": "http://127.0.0.1:46357",
        "tls": {
            "insecure": True,
        },
    },
    type=DictParamType(),
    help="slim server configuration, used only with slim transport",
)
def main(local_timezone, transport, port, organization, namespace, mcp_server, config):
    """
    MCP Time Server - Time and timezone conversion functionality for MCP.
    """

    if transport == "slim":
        import asyncio

        asyncio.run(
            serve_slim(local_timezone, organization, namespace, mcp_server, config)
        )
    else:
        serve_sse(local_timezone, port)
```

</details>

<br>

The core component of the server implementation is the `serve_slim` function.
This function establishes a connection with our SLIM instance and handles all
incoming client sessions. It leverages the `SLIMServer` class to create a SLIM
server instance that listens for and processes client connections.

External clients can address this server using the SLIM name
`org/ns/time-server`.

```python
async def serve_slim(
    local_timezone: str | None = None,
    organization: str = "org",
    namespace: str = "ns",
    mcp_server: str = "time-server",
    config: dict = {},
) -> None:
    """
    Main server function that initializes and runs the time server using SLIM transport.

    Args:
        local_timezone: Optional override for local timezone
        organization: Organization name
        namespace: Namespace name
        mcp_server: MCP server name
        config: Server configuration dictionary
    """
    await init_tracing({"log_level": "info"})
    time_app = TimeServerApp(local_timezone)
    tasks: set[asyncio.Task] = set()

    async with SLIMServer(config, organization, namespace, mcp_server) as slim_server:
        try:
            async for new_session in slim_server:
                task = asyncio.create_task(
                    time_app.handle_session(new_session, slim_server, tasks)
                )
                tasks.add(task)
        except Exception:
            logger.error("Error in session handler", exc_info=True)
            raise
        finally:
            await cleanup_tasks(tasks)
            logger.info("Server stopped")
```

After implementing all the necessary files, your project structure looks
like this:

```bash
mcp-server-time/
├── src/
│   └── mcp_server_time/
│       ├── __init__.py
│       └── server.py
└── pyproject.toml
```

To launch the server and begin listening for incoming connections, navigate to
the project directory and run:

```bash
uv run mcp-server-time --local-timezone Europe/London
```

### Implementing the LlamaIndex Agent
With our MCP server up and running, let's implement a LlamaIndex agent that
will interact with the server. This agent will send time queries and timezone
conversion requests to our MCP server using the SLIM transport protocol.

First, create a new directory for our LlamaIndex agent project:

```bash
mkdir -p llamaindex-time-agent/src/llamaindex_time_agent
cd llamaindex-time-agent
```

Next, create a `pyproject.toml` file to define the agent's dependencies:

```toml
# pyproject.toml

[project]
name = "llamaindex-time-agent"
version = "0.1.0"
description = "A llamaindex agent using MCP server over SLIM for time queries"
requires-python = ">=3.12"
dependencies = [
    "mcp==1.6.0",
    "slim-mcp>=0.1.0",
    "click>=8.1.8",
    "llama-index>=0.12.29",
    "llama-index-llms-azure-openai>=0.3.2",
    "llama-index-llms-ollama>=0.5.4",
    "llama-index-llms-openai-like>=0.3.4",
    "llama-index-tools-mcp>=0.1.2",
]

[project.scripts]
llamaindex-time-agent = "llamaindex_time_agent:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Let's create the Python files for our LlamaIndex agent that will handle
time queries and timezone conversions. Create the following files in your
project directory:

<details>
<summary><b>src/llamaindex_time_agent/__init__.py</b></summary>
<br>

```python
# src/llamaindex_time_agent/__init__.py

from .main import main

if __name__ == "__main__":
    main()
```

</details>

<br>

<details>
<summary><b>src/llamaindex_time_agent/main.py</b></summary>
<br>

```python
# src/llamaindex_time_agent/main.py

# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

import asyncio
import logging

import click
from dotenv import load_dotenv
from llama_index.core.agent.workflow import ReActAgent
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.ollama import Ollama
from llama_index.tools.mcp import McpToolSpec

from slim_mcp import SLIMClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def amain(
    llm_type, llm_endpoint, llm_key, organization, namespace, mcp_server, city, config
):
    if llm_type == "azure":
        kwargs = {
            "engine": "gpt-4o-mini",
            "model": "gpt-4o-mini",
            "is_chat_model": True,
            "azure_endpoint": llm_endpoint,
            "api_key": llm_key,
            "api_version": "2024-08-01-preview",
        }
        llm = AzureOpenAI(**kwargs)
    elif llm_type == "ollama":
        kwargs = {
            "model": "llama3.2",
        }
        llm = Ollama(**kwargs)
    else:
        raise Exception("LLM type must be azure or ollama")

    logger.info("Starting SLIM client")
    async with SLIMClient(
        config,
        "org",
        "ns",
        "time-agent",
        organization,
        namespace,
        mcp_server,
    ) as client1:
        async with client1.to_mcp_session() as mcp_session:
            logger.info("Creating MCP tool spec")

            await mcp_session.initialize()

            mcp_tool_spec = McpToolSpec(
                client=mcp_session,
            )

            tools = await mcp_tool_spec.to_tool_list_async()

            agent = ReActAgent(llm=llm, tools=tools)

            response = await agent.run(
                user_msg=f"What is the current time in {city}?",
            )

            print(response)

            await mcp_session.close()


class DictParamType(click.ParamType):
    name = "dict"

    def convert(self, value, param, ctx):
        import json

        if isinstance(value, dict):
            return value  # Already a dict (for default value)
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            self.fail(f"{value} is not valid JSON", param, ctx)


@click.command(context_settings={"auto_envvar_prefix": "TIME_AGENT"})
@click.option("--llm-type", default="azure")
@click.option("--llm-endpoint", default=None)
@click.option("--llm-key", default=None)
@click.option("--mcp-server-organization", default="org")
@click.option("--mcp-server-namespace", default="ns")
@click.option("--mcp-server-name", default="time-server")
@click.option("--city", default="New York")
@click.option(
    "--config",
    default={
        "endpoint": "http://127.0.0.1:46357",
        "tls": {
            "insecure": True,
        },
    },
    type=DictParamType(),
)
def main(
    llm_type,
    llm_endpoint,
    llm_key,
    mcp_server_organization,
    mcp_server_namespace,
    mcp_server_name,
    city,
    config,
):
    try:
        asyncio.run(
            amain(
                llm_type,
                llm_endpoint,
                llm_key,
                mcp_server_organization,
                mcp_server_namespace,
                mcp_server_name,
                city,
                config,
            )
        )
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e
```


</details>

<br>

The key component of the agent is the `amain` function, which handles:

1. LLM configuration (Azure OpenAI or Ollama).
2. SLIM client initialization and connection to our MCP server.
3. Tool setup and agent execution.

The agent establishes its identity through the SLIM name `org/ns/time-agent`,
which is used for addressing.

After implementing all the necessary files, your agent project structure should
look like this:

```bash
llamaindex-time-agent/
├── src/
│   └── llamaindex_time_agent/
│       ├── __init__.py
│       └── main.py
└── pyproject.toml
```
To run the agent, navigate to the project directory and use one of the following
commands based on your preferred LLM:

**Option 1: Using Azure OpenAI:**
```bash
uv run llamaindex-time-agent \
    --llm-type=azure \
    --llm-endpoint=${AZURE_OPENAI_ENDPOINT} \
    --llm-key=${AZURE_OPENAI_API_KEY} \
    --city 'New York'
```

**Option 2: Using Ollama (locally):**
```bash
uv run llamaindex-time-agent \
    --llm-type=ollama \
    --city 'New York'
```

The agent connects to the MCP server through SLIM, send a time query for the
specified city, and display the response.

## Using SLIM with a Proxy Server for SSE-based MCP Servers

In this section, we demonstrate how to set up and configure the SLIM-MCP Proxy
Server. This proxy enables SLIM-based clients to communicate with existing MCP
servers that use SSE (Server-Sent Events) as their transport protocol. By
following these steps, you'll create a bridge between SLIM clients and SSE-based
MCP servers without modifying the servers themselves.

### Setting Up the SLIM Node

First, ensure you have a SLIM node running in your environment. If you haven't
already set one up, follow the instructions provided in the previous section to
[deploy an SLIM instance](#setting-up-the-slim-instance).

### Running the MCP Server with SSE Transport

Let's set up the time-server using the SSE transport protocol instead of
SLIM. The server implementation is the same as described in the previous section,
but we configure it to use SSE:

```bash
uv run mcp-server-time --local-timezone Europe/London --transport sse
```

Once the server starts successfully, you should see logs similar to this:

```bash
INFO:     Started server process [27044]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

At this point, your time-server is up and running with SSE transport.

### Setting up the SLIM-MCP Proxy

To enable SLIM clients to communicate with the SSE-based time-server, you'll need
to configure and run the SLIM-MCP Proxy Server. Follow these steps to set up a
local proxy instance:

1. **Determine your local IP address** (works on both macOS and Linux):
   ```bash
   # For macOS
   LOCAL_ADDRESS=$(ifconfig | grep --color=never "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)

   # For Linux
   LOCAL_ADDRESS=$(ip addr show | grep --color=never "inet " | grep -v 127.0.0.1 | awk '{print $2}' | cut -d/ -f1 | head -n 1)

   # Verify the IP was found correctly
   echo "Using local IP address: ${LOCAL_ADDRESS}"
   ```

   > If the automatic detection doesn't work for your system, you can manually
   > set your IP address:
   > ```bash
   > LOCAL_ADDRESS=192.168.1.10  # Replace with your actual local IP address
   > ```

2. **Create the configuration file for the proxy**:
   ```bash
   cat << EOF > ./config-proxy.yaml
   # SLIM-MCP Proxy Configuration

   # Tracing settings for log visibility
   tracing:
     log_level: info
     display_thread_names: true
     display_thread_ids: true

   # Runtime configuration
   runtime:
     n_cores: 0
     thread_name: "slim-data-plae"
     drain_timeout: 10s

   # Service configuration for connecting to the SLIM node
   services:
     slim/0:
       pubsub:
         clients:
           - endpoint: "http://${LOCAL_ADDRESS}:46357"
             tls:
               insecure: true
   EOF
   ```

3. **Run the proxy using Docker**:
   ```bash
   docker run -it \
     -v $(pwd)/config-proxy.yaml:/config-proxy.yaml \
     ghcr.io/agntcy/slim/mcp-proxy:latest /slim-mcp-proxy \
     --config /config-proxy.yaml \
     --svc-name slim/0 \
     --name org/mcp/proxy \
     --mcp-server http://${LOCAL_ADDRESS}:8000/sse
   ```

   This command:
   - Mounts your local configuration file into the container.
   - Uses the official SLIM-MCP proxy image.
   - Sets the service name and proxy identifier.
   - Configures the connection to your SSE-based MCP server.

### Running the Agent with the Proxy

Finally, you can run the LlamaIndex agent as shown in the previous section. The
agent automatically connects to the proxy, which then relays messages to
and from the MCP server. Notice that the proxy is reachable using the name
`org/mcp/proxy`:

```bash
uv run llamaindex-time-agent \
    --llm-type=azure \
    --llm-endpoint=${AZURE_OPENAI_ENDPOINT} \
    --llm-key=${AZURE_OPENAI_API_KEY} \
    --city 'New York' \
    --mcp-server-organization "org" \
    --mcp-server-namespace "mcp" \
    --mcp-server-name "proxy"
```

With this setup, your SLIM client can now communicate seamlessly with the
SSE-based MCP server through the proxy, without requiring any changes to the
server implementation.


