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