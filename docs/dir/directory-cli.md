# Directory CLI Guide

The Directory CLI (`dirctl`) provides comprehensive command-line tools for interacting with the Directory system, including storage, routing, search, and security operations.

This guide provides an overview of how to get started with the CLI, how to use its features, as well as common workflows and usage examples.

For detailed reference information, see the [Directory CLI Reference](directory-cli-reference.md).

## Installation

The Directory CLI can be installed in the following ways:

=== "Using Homebrew"

    ```bash
    brew tap agntcy/dir https://github.com/agntcy/dir/
    brew install dirctl
    ```

=== "Using Release Binaries"

    ```bash
    # Download from GitHub Releases
    curl -L https://github.com/agntcy/dir/releases/latest/download/dirctl-linux-amd64 -o dirctl
    chmod +x dirctl
    sudo mv dirctl /usr/local/bin/
    ```

=== "Using Source"

    ```bash
    git clone https://github.com/agntcy/dir
    cd dir
    task build-dirctl
    ```

=== "Using Container Image"

    ```bash
    docker pull ghcr.io/agntcy/dir-ctl:latest
    docker run --rm ghcr.io/agntcy/dir-ctl:latest --help
    ```

## Quick Start

### Local Daemon (No External Dependencies)

The fastest way to get a fully functional local directory is to run the built-in daemon:

```bash
# Start the daemon (runs apiserver + reconciler in one process)
dirctl daemon start

# Or start with a custom config file
dirctl daemon start --config /path/to/config.yaml
```

This starts a gRPC server on `localhost:8888` with embedded SQLite and a filesystem OCI store. All data is stored under `~/.agntcy/dir/` by default. No PostgreSQL, Docker, or external registry required. Without `--config`, built-in defaults are used; when provided, the file is read as the complete configuration.

Once the daemon is running, use any `dirctl` command against it:

```bash
dirctl --server-addr localhost:8888 push my-agent.json
```

To stop the daemon:

```bash
dirctl daemon stop
```

### Using an Existing Server

The following example demonstrates how to store, publish, search, and retrieve a record using the Directory CLI:

1. Store a record

    ```bash
    dirctl push my-agent.json
    ```

    Returns: `baeareihdr6t7s6sr2q4zo456sza66eewqc7huzatyfgvoupaqyjw23ilvi`

1. Publish for network discovery

    ```bash
    dirctl routing publish baeareihdr6t7s6sr2q4zo456sza66eewqc7huzatyfgvoupaqyjw23ilvi
    ```

1. Search for records

    ```bash
    dirctl routing search --skill "AI" --limit 10
    ```

1. Retrieve a record

    ```bash
    # Pull by CID
    dirctl pull baeareihdr6t7s6sr2q4zo456sza66eewqc7huzatyfgvoupaqyjw23ilvi

    # Or pull by name (if the record has a verifiable name)
    dirctl pull cisco.com/agent:v1.0.0
    ```

!!! note "Name-based References"
    
    The CLI supports Docker-style name references in addition to CIDs. Records can be pulled using formats like `name`, `name:version`, or `name:version@cid` for hash-verified lookups. See [Name Verification](#name-verification) for details.

!!! note "Authentication for remote Directory servers"
    
    When accessing a remote Directory server, authenticate first with `dirctl auth login`. For the overall auth model, IdP options, and how OIDC relates to SPIFFE/SPIRE, see [OIDC Authentication for Directory](directory-oidc-authentication.md). See [Authentication](#authentication) below for CLI command usage.

## Common Workflows

### Publishing Workflow

The following workflow demonstrates how to publish a record to the network:

1. Store your record

    ```bash
    # Using --output raw for clean scripting
    CID=$(dirctl push my-agent.json --output raw)
    echo "Stored with CID: $CID"
    ```

1. Publish for discovery

    ```bash
    dirctl routing publish $CID
    ```

1. Verify the record is published

    ```bash
    # Use JSON output for programmatic verification
    dirctl routing list --cid $CID --output json
    ```

1. Check routing statistics

    ```bash
    dirctl routing info
    ```

### Discovery Workflow

The following workflow demonstrates how to discover records from the network:

1. Search for records by skill

    ```bash
    # Use JSON output to process results
    dirctl routing search --skill "AI" --limit 10 --output json
    ```

1. Search with multiple criteria

    ```bash
    dirctl routing search --skill "AI" --locator "docker-image" --min-score 2 --output json
    ```

1. Pull discovered records
    ```bash
    # Extract CIDs and pull records
    dirctl routing search --skill "AI" --output json | \
      jq -r '.[].record_ref.cid' | \
      xargs -I {} dirctl pull {}
    ```

### Synchronization Workflow

The following workflow demonstrates how to synchronize records between remote directories and your local instance:

1. Create sync with remote peer

    ```bash
    # Using --output raw for clean variable capture
    SYNC_ID=$(dirctl sync create https://peer.example.com --output raw)
    echo "Sync created with ID: $SYNC_ID"
    ```

1. Monitor sync progress

    ```bash
    # Use JSON output for programmatic monitoring
    dirctl sync status $SYNC_ID --output json
    ```

1. List all syncs

    ```bash
    # Use JSONL output for streaming results
    dirctl sync list --output jsonl
    ```

1. Clean up when done

    ```bash
    dirctl sync delete $SYNC_ID
    ```

### Advanced Synchronization: Search-to-Sync Pipeline

Automatically sync records that match specific criteria from the network:

```bash
# Search for AI-related records and create sync operations
dirctl routing search --skill "AI" --output json | dirctl sync create --stdin

# This creates separate sync operations for each remote peer found,
# syncing only the specific CIDs that matched your search criteria
```

### Import Workflow

Import records from external registries (e.g. MCP registry) with optional signing and rate limiting:

```bash
# 1. Preview import with dry run
dirctl import --type=mcp \
  --url=https://registry.modelcontextprotocol.io/v0.1 \
  --limit=10 \
  --dry-run

# 2. Perform actual import with debug output
dirctl import --type=mcp \
  --url=https://registry.modelcontextprotocol.io/v0.1 \
  --filter=updated_since=2025-08-07T13:15:04.280Z \
  --debug

# 3. Force reimport to update existing records
dirctl import --type=mcp \
  --url=https://registry.modelcontextprotocol.io/v0.1 \
  --limit=10 \
  --force

# 4. Import with signing enabled
dirctl import --type=mcp \
  --url=https://registry.modelcontextprotocol.io/v0.1 \
  --limit=5 \
  --sign

# 5. Import with rate limiting for LLM API calls
dirctl import --type=mcp \
  --url=https://registry.modelcontextprotocol.io/v0.1 \
  --enrich-rate-limit=5 \
  --debug

# 6. Search imported records
dirctl search --query "module=runtime/mcp"
```

### Export Workflow

Export records from the Directory into formats consumable by external tools and agentic CLIs:

```bash
# 1. Export a single record as an A2A AgentCard
dirctl export my-agent:1.0 --format=a2a --output-file=./agent-card.json

# 2. Export a single record as a SKILL.md for Cursor, Claude Code, etc.
dirctl export my-agent:1.0 --format=agent-skill --output-file=./SKILL.md

# 3. Export a single record as a GitHub Copilot MCP config
dirctl export my-agent:1.0 --format=mcp-ghcopilot --output-file=./mcp.json
```

Batch export uses `--output-dir` with search filters to export multiple records at once. Each format handles batch output differently:

```bash
# Batch export A2A records — one JSON file per record
dirctl export --output-dir=./exports/ --format=a2a --module "integration/a2a"
# Result: ./exports/my-agent.json, ./exports/other-agent.json, ...

# Batch export skills — one subdirectory per skill with SKILL.md
dirctl export --output-dir=./exports/ --format=agent-skill --module "core/language_model/agentskills"
# Result: ./exports/code-review/SKILL.md, ./exports/testing/SKILL.md, ...

# Batch export MCP servers — all merged into a single config file
dirctl export --output-dir=./exports/ --format=mcp-ghcopilot --module "integration/mcp"
# Result: ./exports/mcp.json (contains all matched servers)
```

By default, when multiple versions of the same record exist, only the latest semver version is exported. Use `--all-versions` to export every version (the version is appended to the filename to avoid collisions).

### Event Streaming Workflow

Listen to directory events and process them (e.g. filter by type or labels):

```bash
# Listen to all events (human-readable)
dirctl events listen

# Stream events as JSONL for processing
dirctl events listen --output jsonl | jq -c .

# Filter and process specific event types
dirctl events listen --types RECORD_PUSHED --output jsonl | \
  jq -c 'select(.type == "EVENT_TYPE_RECORD_PUSHED")' | \
  while read event; do
    CID=$(echo "$event" | jq -r '.resource_id')
    echo "New record pushed: $CID"
  done

# Monitor events with label filters
dirctl events listen --labels /skills/AI --output jsonl | \
  jq -c '.resource_id' >> ai-records.log

# Extract just resource IDs from events
dirctl events listen --output raw | tee event-cids.txt
```

## Output Formats

All `dirctl` commands support multiple output formats via the `--output` (or `-o`) flag, making it easy to switch between human-readable output and machine-processable formats.

### Available Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| `human` | Human-readable, formatted output with colors and tables (default) | Interactive terminal use |
| `json` | Pretty-printed JSON with indentation | Debugging, single-record processing |
| `jsonl` | Newline-delimited JSON (compact, one object per line) | Streaming, batch processing, logging |
| `raw` | Raw values only (e.g., CIDs, IDs) | Shell scripting, piping to other commands |

### Usage

```bash
# Human-readable output (default)
dirctl routing list

# JSON output (pretty-printed)
dirctl routing list --output json
dirctl routing list -o json

# JSONL output (streaming-friendly)
dirctl events listen --output jsonl

# Raw output (just values)
dirctl push my-agent.json --output raw
```

### Piping and Processing

Structured formats (`json`, `jsonl`, `raw`) automatically route data to **stdout** and metadata messages to **stderr**, enabling clean piping to tools like `jq`:

```bash
# Process JSON output with jq
dirctl routing search --skill "AI" -o json | jq '.[] | .cid'

# Stream events and filter by type
dirctl events listen -o jsonl | jq -c 'select(.type == "EVENT_TYPE_RECORD_PUSHED")'

# Capture CID for scripting
CID=$(dirctl push my-agent.json -o raw)
echo "Stored with CID: $CID"

# Chain commands
dirctl routing list -o json | jq -r '.[].cid' | xargs -I {} dirctl pull {}
```

### Format Selection Guidelines

- **`human`**: Default for terminal interaction, provides context and formatting
- **`json`**: Best for debugging or when you need readable structured data
- **`jsonl`**: Ideal for streaming events, logs, or processing large result sets line-by-line
- **`raw`**: Perfect for shell scripts and command chaining where you only need the value

## Authentication

Authentication is required when accessing remote Directory servers. This section focuses on how `dirctl` authenticates and how to use the relevant CLI commands.

For the broader model, including `Envoy` and `ext-authz`, IdP-agnostic OIDC support, Dex as an optional broker, and how external OIDC access differs from internal SPIFFE/SPIRE trust, see [OIDC Authentication for Directory](directory-oidc-authentication.md).

| Command | Description |
|---------|-------------|
| `dirctl auth login` | Authenticate via OIDC (browser PKCE, headless, or device flow) |
| `dirctl auth logout` | Clear cached authentication credentials |
| `dirctl auth status` | Show current authentication status |

### OIDC Authentication

OIDC is the default authentication model for remote Directory access. The main CLI usage patterns are:

- **Interactive login** (PKCE) via `dirctl auth login`
- **Headless login** via `dirctl auth login --no-browser`
- **Device flow** via `dirctl auth login --device` (no browser needed on this machine)
- **Pre-issued token** via `--auth-token` / `DIRECTORY_CLIENT_AUTH_TOKEN` (CI, scripts, service users)

#### Interactive login (`dirctl auth login`)

Authenticate as a human user using OIDC Authorization Code + PKCE.

```bash
# Using flags
dirctl auth login \
  --oidc-issuer "https://prod.idp.ads.outshift.io" \
  --oidc-client-id "dirctl"

# Or using environment variables
export DIRECTORY_CLIENT_OIDC_ISSUER="https://prod.idp.ads.outshift.io"
export DIRECTORY_CLIENT_OIDC_CLIENT_ID="dirctl"
dirctl auth login
```

What happens:

1. The CLI opens browser-based login against your OIDC issuer
2. You authenticate with your credentials
3. The CLI caches the token at `~/.config/dirctl/auth-token.json`
4. Subsequent commands can reuse the cached token (auto-detect or `--auth-mode=oidc`)

```bash
# Force re-login even if already authenticated
dirctl auth login --force

# Headless: show URL only, do not open browser automatically
dirctl auth login --no-browser
```

#### Device flow login (`dirctl auth login --device`)

Authenticate without a browser on the current machine. Useful for SSH sessions, containers, or remote servers.

```bash
dirctl auth login --device \
  --oidc-issuer "https://prod.idp.ads.outshift.io" \
  --oidc-client-id "dirctl"
```

The same environment variables from interactive login apply (`DIRECTORY_CLIENT_OIDC_ISSUER`, `DIRECTORY_CLIENT_OIDC_CLIENT_ID`).

What happens:

1. The CLI displays a code and a URL
2. You open the URL on any device (phone, another computer) and enter the code
3. You authenticate with your credentials
4. The CLI polls until authorization completes, then caches the token

#### `dirctl auth status`

Check your current authentication status.

```bash
dirctl auth status
```

Example output:

```
Status: Authenticated
  Provider: oidc
  Subject: johndoe
  Issuer: https://prod.idp.ads.outshift.io
  Email: johndoe@example.com
  Principal type: human
  Cached at: 2026-01-15T10:30:00+00:00
  Token: Valid ✓
  Expires: 2026-01-15T11:30:00+00:00
  Cache file: /home/johndoe/.config/dirctl/auth-token.json
```

#### `dirctl auth logout`

Clear cached authentication credentials.

```bash
dirctl auth logout
```

#### Using Authenticated Commands

Once authenticated, cached credentials are automatically detected and used:

```bash
# Push to remote Directory server (auto-detects and uses cached OIDC credentials)
dirctl push my-agent.json

# Search remote Directory server (auto-detects authentication)
dirctl --server-addr=prod.gateway.ads.outshift.io:443 search --skill "natural_language_processing"

# Pull from remote Directory server (auto-detects authentication)
dirctl pull baeareihdr6t7s6sr2q4zo456sza66eewqc7huzatyfgvoupaqyjw23ilvi
```

**Authentication mode behavior:**

- **No `--auth-mode` flag (default)**: Auto-detects authentication in this order: SPIFFE (if available in Kubernetes/SPIRE environment), OIDC (explicit token or cached token), then insecure (for local development).
- **Explicit `--auth-mode=oidc`**: Forces OIDC authentication.
- **Other modes**: Use `--auth-mode=x509`, `--auth-mode=jwt`, or `--auth-mode=tls` for specific authentication methods.

```bash
# Force OIDC auth even if SPIFFE is available
dirctl --auth-mode=oidc push my-agent.json
```

#### Pre-issued Tokens (CI and Service Users)

For CI/CD pipelines and automation, pass a pre-issued JWT token directly:

```bash
# GitHub Actions OIDC
dirctl search --name "*" \
  --server-addr "prod.gateway.ads.outshift.io:443" \
  --auth-mode=oidc \
  --auth-token "<github-oidc-jwt>" \
  --output json

# Service user with pre-generated token
export DIRECTORY_CLIENT_AUTH_TOKEN="<service-user-jwt>"
export DIRECTORY_CLIENT_SERVER_ADDRESS="prod.gateway.ads.outshift.io:443"
dirctl search --auth-mode=oidc
```

### Other Authentication Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `oidc` | OIDC bearer/JWT auth | Human login, pre-issued tokens, and CI workload identity |
| `x509` | SPIFFE X.509 certificates | Kubernetes workloads with SPIRE |
| `jwt` | SPIFFE JWT tokens | Service-to-service authentication |
| `token` | SPIFFE token file | Pre-provisioned credentials |
| `tls` | mTLS with certificates | Custom PKI environments |
| `insecure` / `none` | No auth, skip auto-detect | Testing, local development |
| (empty) | Auto-detect: SPIFFE → OIDC → insecure | Default behavior (recommended) |

## Configuration

### Server Connection

```bash
# Connect to specific server
dirctl --server-addr localhost:8888 routing list

# Use environment variable
export DIRECTORY_CLIENT_SERVER_ADDRESS=localhost:8888
dirctl routing list
```

### Authentication

```bash
# OIDC authentication (most common)
export DIRECTORY_CLIENT_OIDC_ISSUER="https://prod.idp.ads.outshift.io"
export DIRECTORY_CLIENT_OIDC_CLIENT_ID="dirctl"
dirctl auth login

# Pre-issued token (CI/service users)
export DIRECTORY_CLIENT_AUTH_TOKEN="<jwt>"
dirctl --auth-mode=oidc routing list

# SPIFFE Workload API (Kubernetes)
dirctl --spiffe-socket-path /run/spire/sockets/agent.sock routing list
```

## Command Organization

The CLI follows a clear service-based organization:

- **Daemon**: Local directory server (`daemon start`, `daemon stop`, `daemon status`).
- **Auth**: OIDC authentication (`auth login`, `auth logout`, `auth status`).
- **Storage**: Direct record management (`push`, `pull`, `delete`, `info`).
- **Import**: Batch imports from external registries (`import`).
- **Export**: Export records to external formats (`export`).
- **Routing**: Network announcement and discovery (`routing publish`, `routing list`, `routing search`).
- **Search**: General content search (`search`).
- **Security**: Signing, verification, and validation (`sign`, `verify`, `validate`, `naming verify`).
- **Sync**: Peer synchronization (`sync`).

Each command group provides focused functionality with consistent flag patterns and clear separation of concerns.

## Getting Help

Use the following commands to get help with the CLI:

- General help
    ```bash
    dirctl --help
    ```

- Command group help
    ```bash
    dirctl routing --help
    ```

- Specific command help
    ```bash
    dirctl routing search --help
    ```

For more advanced usage, troubleshooting, and development workflows, see the [AGNTCY documentation](https://docs.agntcy.org/dir/overview/).
