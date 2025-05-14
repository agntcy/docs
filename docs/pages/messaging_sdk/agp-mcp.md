# AGP-MCP

This tutorial explains how to use AGP (Agent Gateway Protocol) to transport MCP
(Model Context Protocol) messages. AGP supports two main integration options,
depending on whether you're building a new system or working with an existing
MCP server:

1. **Using AGP as an MCP Custom Transport Protocol**: MCP is designed to allow
   custom transport protocols, and AGP has been added as one of these options.
   To use AGP as a custom transport, you can install our AGP-MCP via a pipy
   package and integrate it directly into your application. This approach is
   ideal for new systems where you control both the client and the server,
   enabling native AGP support for transporting MCP messages.
2. **Using AGP with a Proxy Server***: If you already have an MCP server running
   that uses SSE (Server-Sent Events) as MCP transport, you can integrate AGP by
   setting up a proxy server. The proxy translates communication between AGP
   clients and the existing SSE-based MCP server. This allows AGP clients to
   connect seamlessly without requiring changes to the server itself, making it
   a convenient solution for existing systems.

This tutorial will guide you through both approaches. We'll show you how to use
AGP as a custom transport for MCP, as well as how to configure the proxy server
to enable AGP support for an SSE-based MCP server. By the end, you'll have the
tools to integrate AGP with MCP in a way that suits your system's architecture

## Using AGP as an MCP Custom Transport Protocol

For this part of the tutorial, we'll be using two simple applications:

 - A [llamaindex
   agent](https://github.com/agntcy/agp/tree/main/data-plane/integrations/mcp/agp-mcp/examples/llamaindex-time-agent)
   that uses a MCP server over AGP for time queries andtimezone conversions.
 - An [MCP time
   server](https://github.com/agntcy/agp/tree/main/data-plane/integrations/mcp/agp-mcp/examples/mcp-server-time)
   that uses AGP as a custom transport protocol and handles requests from the
   llamaindex agent.

### Prerequisites

- [UV](https://docs.astral.sh/uv/getting-started/installation/)
- [Docker](https://docs.docker.com/get-started/get-docker/)

### Run the AGP Instance

The client and server will communicate using AGP, so we need to run an AGP
instance. We can use the pre-built docker image for this purpose.

Execute the following command:

```bash
cat << EOF > ./config.yaml
tracing:
  log_level: debug
  display_thread_names: true
  display_thread_ids: true

runtime:
  n_cores: 0
  thread_name: "data-plane-gateway"
  drain_timeout: 10s

services:
  gateway/0:
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


docker run -it \
    -v ./config.yaml:/config.yaml -p 46357:46357 \
    ghcr.io/agntcy/agp/gw:latest /gateway --config /config.yaml
```

The above command will run an AGP instance listening on port 46357 for incoming
connections.

### Write the MCP Server

Now, let's write a simple MCP server that will handle requests from the
llamaindex agent. This server will be using AGP as a custom transport protocol.

First, let's write a simple pyproject to install the required dependencies:

```toml
# pyproject.toml
[project]
name = "mcp-server-time"
description = "MCP server providing tools for time queries timezone conversions"
requires-python = ">=3.10"
dependencies = ["mcp>=1.6.0", "agp-mcp>=0.1.1", "click>=8.1.8"]

[project.scripts]
mcp-server-time = "mcp_server_time:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Then let's write the simple MCP server that will handle time queries and
timezone. The server is taken from the [official example provided by
MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/time), and it
is modified to use AGP or SSE as transport protocol.

<details>
<summary>MCP Server</summary>
<br>

```python
# mcp_server_time/__init__.py

from .server import main

if __name__ == "__main__":
    main()
```

```python
# src/mcp_server_time/server.py

"""
MCP Time Server - A server implementation for time and timezone conversion functionality.
This module provides tools for getting current time in different timezones and converting times between timezones.
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

from agp_mcp import AGPServer, init_tracing

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

    async def handle_session(self, session, agp_server, tasks):
        """
        Handle a single session with proper error handling and logging.

        Args:
            session: The session to handle
            agp_server: The AGP server instance
            tasks: Set of active tasks
        """
        try:
            async with agp_server.new_streams(session) as streams:
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


async def serve_agp(
    local_timezone: str | None = None,
    organization: str = "org",
    namespace: str = "ns",
    mcp_server: str = "time-server",
    config: dict = {},
) -> None:
    """
    Main server function that initializes and runs the time server using AGP transport.

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

    async with AGPServer(config, organization, namespace, mcp_server) as agp_server:
        try:
            async for new_session in agp_server:
                task = asyncio.create_task(
                    time_app.handle_session(new_session, agp_server, tasks)
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
@click.option("--transport", default="agp", help="transport option: agp or sse")
@click.option(
    "--port",
    default="8000",
    type=int,
    help="listening port, used only with sse transport",
)
@click.option(
    "--organization",
    default="org",
    help="server organization, used only with agp transport",
)
@click.option(
    "--namespace", default="ns", help="server namespace, used only with agp transport"
)
@click.option(
    "--mcp-server",
    default="time-server",
    help="server name, used only with agp transport",
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
    help="agp server configuration, used only with agp transport",
)
def main(local_timezone, transport, port, organization, namespace, mcp_server, config):
    """
    MCP Time Server - Time and timezone conversion functionality for MCP.
    """

    if transport == "agp":
        import asyncio

        asyncio.run(
            serve_agp(local_timezone, organization, namespace, mcp_server, config)
        )
    else:
        serve_sse(local_timezone, port)
```

</details>


The most important part of the server is the `serve_agp` function. This function
is responsible for initializing the connection with the AGP instance we setup
previously and handling incoming connections. It uses the `AGPServer` class to
create a new AGP server instance and listens for incoming sessions.

Clients can address the server using the AGP topic `org/ns/time-server`.

```python
async def serve_agp(
    local_timezone: str | None = None,
    organization: str = "org",
    namespace: str = "ns",
    mcp_server: str = "time-server",
    config: dict = {},
) -> None:
    """
    Main server function that initializes and runs the time server using AGP transport.

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

    async with AGPServer(config, organization, namespace, mcp_server) as agp_server:
        try:
            async for new_session in agp_server:
                task = asyncio.create_task(
                    time_app.handle_session(new_session, agp_server, tasks)
                )
                tasks.add(task)
        except Exception:
            logger.error("Error in session handler", exc_info=True)
            raise
        finally:
            await cleanup_tasks(tasks)
            logger.info("Server stopped")
```

After writing the files, you project should have the following stricture:

```bash
.
├── mcp_server_time
│   ├── __init__.py
│   └── server.py
└──  pyproject.toml
```

In the folder, run the following command to start the server and listen for
incoming connections:

```bash
uv run mcp-server-time --local-timezone Europe/London
```

### Run the LlamaIndex Agent
Now that we have the MCP server running, let's write a simple LlamaIndex agent
that will use the MCP server to handle time queries and timezone conversions.
The agent will use the AGP transport protocol to communicate with the MCP
server.

First, let's write a simple pyproject to install the required dependencies:

```toml
# pyproject.toml

[project]
name = "llamaindex-time-agent"
version = "0.1.0"
description = "A llamaindex agent using MCP server over AGP for time queries"
requires-python = ">=3.12"
dependencies = [
    "mcp>=1.0.0",
    "agp-mcp>=0.1.1",
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

Then let's write the simple LlamaIndex agent that will handle time queries and
timezone.

<details>
<summary>MCP Server</summary>
<br>

```python
# src/llamaindex_time_agent/__init__.py

from .main import main

if __name__ == "__main__":
    main()
```

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

from agp_mcp import AGPClient

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

    logger.info("Starting AGP client")
    async with AGPClient(
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

The most important part of the agent is the `amain` function. This function is
responsible for initializing the connection with the AGP instance we setup
previously and connect to the MCP server.

The name of the AGP topic that we can use to address the server is
`org/ns/time-agent`.

After writing the files, you project should have the following structure:

```bash
.
├── llamaindex_time_agent
│   ├── __init__.py
│   └── main.py
└── pyproject.toml
```
In the folder, run the following command to start the agent and listen for
incoming connections.

With Azure OpenAI:
```bash
uv run llamaindex-time-agent                    \
    --llm-type=azure                            \
    --llm-endpoint=${AZURE_OPENAI_ENDPOINT}     \
    --llm-key=${AZURE_OPENAI_API_KEY}           \
    --city 'New York'
```

With Ollama:
```bash
uv run llamaindex-time-agent                    \
    --llm-type=ollama                            \
    --city 'New York'
```

## Using AGP with a Proxy Server
In this tutorial, we'll configure and run the AGP-MCP Proxy to enable
communication between an AGP-based client (from the previous section) and a
time-server that uses the SSE (Server-Sent Events) transport. Follow the steps
below to complete the setup:

### Step 1: Runnig the AGP node.
Before starting, ensure you have an AGP node up and running. If you don't
already have one, refer to the steps provided in the previous session to start
it.

### Step 2: Running the Time-Server
We'll now set up the time-server using the SSE transport protocol.
1. Navigate to the time-server directory: 
```
agp/data-plane/integrations/mcp/agp-mcp/examples/mcp-server-time
```
2. Run the time-server using the SSE transpor wit the following command:
```bash
uv run --package mcp-server-time mcp-server-time \
    --local-timezone "America/New_York" --transport sse
```
3. Once the server starts successfully, you should see logs similar to this:
```bash
INFO:     Started server process [27044]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
At this point, your time-server is up and running.

### Step 3: Setting up the AGP-MPC Server
To enable the AGP client to communicate with the SSE-based time-server, you'll
need to configure and run the AGP-MCP Proxy Server. Follow these steps:

#### 3.1 Build the proxy server
1. Navigate to the mcp-proxy folder: 
```
agp/data-plane/integrations/mcp/mcp-proxy
```
2. Build the AGP-MCP proxy by running: 
```bash
task mcp-proxy:build
```

#### 3.2 Run the proxy server
Run the AGP-MCP proxy server using the following command
```bash
cargo run -- --config <configuration> \
    --svc-name <svc_name> \
    --name <proxy_name> \
    --mcp-server <address> 
```
Here's what each command option means: | Option | Description |
|-------------------------|------------------------------------------------------|
| -c, --config | Path to the AGP configuration file | | -s, --svc-name | Service
name to look for in the configuration file | | -n, --name | Name of the MCP
Proxy (format: org/ns/type) | | -m, --mcp-server | Address of the MCP Server
(e.g., http://localhost:8000/sse) |

An example of the configuration file is available at
```./config/cp-proxy-config.yaml```
```yaml
tracing:
  log_level: info
  display_thread_names: true
  display_thread_ids: true

runtime:
  n_cores: 0
  thread_name: "data-plane-gateway"
  drain_timeout: 10s

services:
  gateway/0:
    pubsub:
      clients:
        - endpoint: "http://localhost:46357"
          tls:
            insecure: true
```
In this example the service name to pass to the command with the
```--svc-name``` option is ```gateway/0```

In addtion, the option ```--name``` is the name used by AGP to route messages to
the proxy, while the ```--mpc-server``` option indicates the address of the MCP
server.

Here's an example command to run the AGP-MCP Proxy:
```bash
cargo run -- --config config/mcp-proxy-config.yaml \
    --svc-name gateway/0 \
    --name org/mcp/proxy \
    --mcp-server http://localhost:8000/sse 
```

### Step 4: Running the Agent
Finally, you can now run the agent as shown in the previuos section. The agent
will automatically connect to the proxy and send messages to the MCP server via
the proxy.


