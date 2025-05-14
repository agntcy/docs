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

## Using AGP with a Proxy Server
In this tutorial, we'll configure and run the AGP-MCP Proxy to enable
communication between an AGP-based client (from the previous section) and a
time-server that uses the SSE (Server-Sent Events) transport. Follow the steps
below to complete the setup:

### Step 1: Runnig the AGP node.
Before starting, ensure you have an AGP node up and running. If you don't
already have one, refer to the steps provided in the previous session to start it.

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
Here's what each command option means:
| Option | Description |
|-------------------------|------------------------------------------------------|
| -c, --config | Path to the AGP configuration file |
| -s, --svc-name | Service name to look for in the configuration file |
| -n, --name | Name of the MCP Proxy (format: org/ns/type) |
| -m, --mcp-server | Address of the MCP Server (e.g., http://localhost:8000/sse) |

An example of the configuration file is available at ```./config/cp-proxy-config.yaml```
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

In addtion, the option ```--name``` is the name used by AGP to route messages
to the proxy, while the ```--mpc-server``` option indicates the address of the
MCP server.

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


