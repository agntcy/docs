# Directory CLI

The Directory CLI (dirctl) provides comprehensive command-line tools for interacting with the Directory system, including storage, routing, search, and security operations.

## Installation

The Directory CLI can be installed in the following ways:

### Using Homebrew

```bash
brew tap agntcy/dir https://github.com/agntcy/dir/
brew install dirctl
```

### Using Release Binaries

```bash
# Download from GitHub Releases
curl -L https://github.com/agntcy/dir/releases/latest/download/dirctl-linux-amd64 -o dirctl
chmod +x dirctl
sudo mv dirctl /usr/local/bin/
```

### Using Source

```bash
git clone https://github.com/agntcy/dir
cd dir
task build-dirctl
```

### Using Container Image

```bash
docker pull ghcr.io/agntcy/dir-ctl:latest
docker run --rm ghcr.io/agntcy/dir-ctl:latest --help
```

## Quick Start

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

## Directory MCP Server

The Directory MCP Server provides a standardized interface for AI assistants and tools to interact with the AGNTCY Agent Directory and work with OASF agent records.

The Directory MCP Server exposes Directory functionality through MCP, allowing AI assistants to:

- Work with OASF schemas and validate agent records.
- Search and discover agent records from the Directory.
- Push and pull records to/from Directory servers.
- Navigate OASF skill and domain taxonomies.
- Generate agent records automatically from codebases.

The MCP server runs via the `dirctl` CLI tool and acts as a bridge between AI development environments and the Directory infrastructure, making it easier to work with agent metadata in your development workflow.

### Configuration

**Binary Configuration:**

Add the MCP server to your IDE's MCP configuration using the absolute path to the `dirctl` binary.

**Example Cursor configuration (`~/.cursor/mcp.json`):**

```json
{
  "mcpServers": {
    "dir-mcp-server": {
      "command": "/absolute/path/to/dirctl",
      "args": ["mcp", "serve"]
    }
  }
}
```

**Docker Configuration:**

Add the MCP server to your IDE's MCP configuration using Docker.

??? example "Example Cursor configuration (`~/.cursor/mcp.json`)"

    ```json
    {
    "mcpServers": {
        "dir-mcp-server": {
        "command": "docker",
        "args": [
            "run",
            "--rm",
            "-i",
            "ghcr.io/agntcy/dir-ctl:latest",
            "mcp",
            "serve"
        ]
        }
    }
    }
    ```

**Environment Variables:**

Configure the MCP server behavior using environment variables:

- `DIRECTORY_CLIENT_SERVER_ADDRESS` - Directory server address (default: `0.0.0.0:8888`)
- `DIRECTORY_CLIENT_AUTH_MODE` - Authentication mode: `none`, `x509`, `jwt`, `token`
- `DIRECTORY_CLIENT_SPIFFE_TOKEN` - Path to SPIFFE token file (for token authentication)
- `DIRECTORY_CLIENT_TLS_SKIP_VERIFY` - Skip TLS verification (set to `true` if needed)

??? example "Example with environment variables"

    ```json
    {
    "mcpServers": {
        "dir-mcp-server": {
        "command": "/usr/local/bin/dirctl",
        "args": ["mcp", "serve"],
        "env": {
            "DIRECTORY_CLIENT_SERVER_ADDRESS": "dir.example.com:8888",
            "DIRECTORY_CLIENT_AUTH_MODE": "none",
            "DIRECTORY_CLIENT_TLS_SKIP_VERIFY": "false"
        }
        }
    }
    }
    ```

### Directory MCP Server Tools

Using the Directory MCP Server, you can access the following tools:

- `agntcy_oasf_list_versions` - Lists all available OASF schema versions supported by the server.
- `agntcy_oasf_get_schema` - Retrieves the complete OASF schema JSON content for the specified version.
- `agntcy_oasf_get_schema_skills` - Retrieves skills from the OASF schema with hierarchical navigation support.
- `agntcy_oasf_get_schema_domains` - Retrieves domains from the OASF schema with hierarchical navigation support.
- `agntcy_oasf_validate_record` - Validates an OASF agent record against the OASF schema.
- `agntcy_dir_push_record` - Pushes an OASF agent record to a Directory server.
- `agntcy_dir_pull_record` - Pulls an OASF agent record from the local Directory node by its CID (Content Identifier).
- `agntcy_dir_search_local` - Searches for agent records on the local directory node using structured query filters.

For a full list of tools and usage examples, see the [Directory MCP Server documentation](https://github.com/agntcy/dir/blob/main/mcp/README.md).

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

## Command Reference

### Storage Operations

#### `dirctl push <file>`

Stores records in the content-addressable store. Has the following features:

- Supports OASF v1, v2, v3 record formats
- Content-addressable storage with CID generation
- Optional cryptographic signing
- Data integrity validation

??? example

    ```bash
    # Push from file
    dirctl push agent-model.json

    # Push from stdin
    cat agent-model.json | dirctl push --stdin

    # Push with signature
    dirctl push agent-model.json --sign --key private.key
    ```

#### `dirctl pull <reference>`

Retrieves records by their Content Identifier (CID) or name reference.

**Supported Reference Formats:**

| Format | Description |
|--------|-------------|
| `<cid>` | Direct lookup by CID |
| `<name>` | Retrieves the latest version |
| `<name>:<version>` | Retrieves the specified version |
| `<name>@<cid>` | Hash-verified lookup (fails if resolved CID doesn't match) |
| `<name>:<version>@<cid>` | Hash-verified lookup for a specific version |

??? example

    ```bash
    # Pull by CID
    dirctl pull baeareihdr6t7s6sr2q4zo456sza66eewqc7huzatyfgvoupaqyjw23ilvi

    # Pull by name (latest version)
    dirctl pull cisco.com/agent

    # Pull by name with specific version
    dirctl pull cisco.com/agent:v1.0.0

    # Pull with hash verification
    dirctl pull cisco.com/agent@bafyreib...
    dirctl pull cisco.com/agent:v1.0.0@bafyreib...

    # Pull with signature verification
    dirctl pull <cid> --signature --public-key public.key
    ```

**Hash Verification:**

The `@<cid>` suffix enables hash verification. This command fails if the resolved CID doesn't match the expected digest:

```bash
# Succeeds if cisco.com/agent:v1.0.0 resolves to bafyreib...
dirctl pull cisco.com/agent:v1.0.0@bafyreib...

# Fails with error if CIDs don't match
dirctl pull cisco.com/agent@wrong-cid
# Error: hash verification failed: resolved CID "bafyreib..." does not match expected digest "wrong-cid"
```

**Version Resolution:**

When no version is specified, commands return the most recently created record (by record's `created_at` field). This allows non-semver tags like `latest`, `dev`, or `stable`.

#### `dirctl delete <cid>`

Removes records from storage.

??? example

    ```bash
    # Delete a record
    dirctl delete baeareihdr6t7s6sr2q4zo456sza66eewqc7huzatyfgvoupaqyjw23ilvi
    ```

#### `dirctl info <reference>`

Displays metadata about stored records using CID or name reference.

**Supported Reference Formats:**

| Format | Description |
|--------|-------------|
| `<cid>` | Direct lookup by content address |
| `<name>` | Displays the most recently created version |
| `<name>:<version>` | Displays the specified version |
| `<name>@<cid>` | Hash-verified lookup |
| `<name>:<version>@<cid>` | Hash-verified lookup for a specific version |

??? example

    ```bash
    # Info by CID (existing)
    dirctl info baeareihdr6t7s6sr2q4zo456sza66eewqc7huzatyfgvoupaqyjw23ilvi

    # Info by name (latest version)
    dirctl info cisco.com/agent --output json

    # Info by name with specific version
    dirctl info cisco.com/agent:v1.0.0 --output json
    ```

### Import Operations

Import records from external registries into DIR. Supports automated batch imports from various registry types.

#### `dirctl import [flags]`

Fetch and import records from external registries.

**Supported Registries:**

- `mcp` - Model Context Protocol registry v0.1

**Configuration Options:**

| Flag | Environment Variable | Description | Required | Default |
|------|---------------------|-------------|----------|---------|
| `--type` | - | Registry type (mcp, a2a) | Yes | - |
| `--url` | - | Registry base URL | Yes | - |
| `--filter` | - | Registry-specific filters (key=value, repeatable) | No | - |
| `--limit` | - | Maximum records to import (0 = no limit) | No | 0 |
| `--dry-run` | - | Preview without importing | No | false |
| `--debug` | - | Enable debug output (shows MCP source and OASF record for failures) | No | false |
| `--force` | - | Force reimport of existing records (skip deduplication) | No | false |
| `--enrich-config` | - | Path to MCPHost configuration file (mcphost.json) | No | importer/enricher/mcphost.json |
| `--enrich-skills-prompt` | - | Optional: path to custom skills prompt template or inline prompt | No | "" (uses default) |
| `--enrich-domains-prompt` | - | Optional: path to custom domains prompt template or inline prompt | No | "" (uses default) |
| `--server-addr` | DIRECTORY_CLIENT_SERVER_ADDRESS | DIR server address | No | localhost:8888 |

!!! note

    By default, the importer performs deduplication: it builds a cache of existing records (by name and version) and skips importing records that already exist. This prevents duplicate imports when running the import command multiple times. Use `--force` to bypass deduplication and reimport existing records. Use `--debug` to see detailed output including which records were skipped and why imports failed.

??? example

    ```bash
    # Import from MCP registry
    dirctl import --type=mcp --url=https://registry.modelcontextprotocol.io/v0.1

    # Import with debug output (shows detailed diagnostics for failures)
    dirctl import --type=mcp \
      --url=https://registry.modelcontextprotocol.io/v0.1 \
      --debug

    # Force reimport of existing records (skips deduplication)
    dirctl import --type=mcp \
      --url=https://registry.modelcontextprotocol.io/v0.1 \
      --force

    # Import with time-based filter
    dirctl import --type=mcp \
      --url=https://registry.modelcontextprotocol.io/v0.1 \
      --filter=updated_since=2025-08-07T13:15:04.280Z

    # Combine multiple filters
    dirctl import --type=mcp \
      --url=https://registry.modelcontextprotocol.io/v0.1 \
      --filter=search=github \
      --filter=version=latest \
      --filter=updated_since=2025-08-07T13:15:04.280Z

    # Limit number of records
    dirctl import --type=mcp \
      --url=https://registry.modelcontextprotocol.io/v0.1 \
      --limit=50

    # Preview without importing (dry run)
    dirctl import --type=mcp \
      --url=https://registry.modelcontextprotocol.io/v0.1 \
      --dry-run
    ```

### Routing Operations

The routing commands manage record announcement and discovery across the peer-to-peer network.

#### `dirctl routing publish <cid>`

Announces records to the network for discovery by other peers. The command does the following:

- Announces record to DHT network.
- Makes record discoverable by other peers.
- Stores routing metadata locally.
- Enables network-wide discovery.

??? example

    ```bash
    # Publish a record to the network
    dirctl routing publish baeareihdr6t7s6sr2q4zo456sza66eewqc7huzatyfgvoupaqyjw23ilvi
    ```

#### `dirctl routing unpublish <cid>`

Removes records from network discovery while keeping them in local storage. The command does the following:

- Removes DHT announcements.
- Stops network discovery.
- Keeps record in local storage.
- Cleans up routing metadata.

??? example

    ```bash
    # Remove from network discovery
    dirctl routing unpublish baeareihdr6t7s6sr2q4zo456sza66eewqc7huzatyfgvoupaqyjw23ilvi
    ```

#### `dirctl routing list [flags]`

Queries local published records with optional filtering.

The following flags are available:

- `--skill <skill>` - Filter by skill (repeatable)
- `--locator <type>` - Filter by locator type (repeatable)
- `--domain <domain>` - Filter by domain (repeatable)
- `--module <module>` - Filter by module name (repeatable)
- `--cid <cid>` - List specific record by CID
- `--limit <number>` - Limit number of results

??? example

    ```bash
    # List all local published records
    dirctl routing list

    # List by skill
    dirctl routing list --skill "AI"
    dirctl routing list --skill "Natural Language Processing"

    # List by locator type
    dirctl routing list --locator "docker-image"

    # List by module
    dirctl routing list --module "runtime/framework"

    # Multiple criteria (AND logic)
    dirctl routing list --skill "AI" --locator "docker-image"
    dirctl routing list --domain "healthcare" --module "runtime/language"

    # Specific record by CID
    dirctl routing list --cid baeareihdr6t7s6sr2q4zo456sza66eewqc7huzatyfgvoupaqyjw23ilvi

    # Limit results
    dirctl routing list --skill "AI" --limit 5
    ```

#### `dirctl routing search [flags]`

Discovers records from other peers across the network.

The following flags are available:

- `--skill <skill>` - Search by skill (repeatable)
- `--locator <type>` - Search by locator type (repeatable)
- `--domain <domain>` - Search by domain (repeatable)
- `--module <module>` - Search by module name (repeatable)
- `--limit <number>` - Maximum results to return
- `--min-score <score>` - Minimum match score threshold

The output includes the following:

- Record CID and provider peer information
- Match score showing query relevance
- Specific queries that matched
- Peer connection details

??? example

    ```bash
    # Search for AI records across the network
    dirctl routing search --skill "AI"

    # Search with multiple criteria
    dirctl routing search --skill "AI" --skill "ML" --min-score 2

    # Search by locator type
    dirctl routing search --locator "docker-image"

    # Search by module
    dirctl routing search --module "runtime/framework"

    # Advanced search with scoring
    dirctl routing search --skill "web-development" --limit 10 --min-score 1
    dirctl routing search --domain "finance" --module "validation" --min-score 2
    ```

**Output includes:**

#### `dirctl routing info`

Shows routing statistics and summary information.

The output includes the following:

- Total published records count
- Skills distribution with counts
- Locators distribution with counts
- Helpful usage tips

??? example

    ```bash
    # Show local routing statistics
    dirctl routing info
    ```

### Search & Discovery

#### `dirctl search [flags]`

General content search across all records using the search service.

The following flags are available:

- `--query <key=value>` - Search criteria (repeatable)
- `--limit <number>` - Maximum results
- `--offset <number>` - Result offset for pagination

??? example

    ```bash
    # Search by record name
    dirctl search --query "name=my-agent"

    # Search by version
    dirctl search --query "version=v1.0.0"

    # Search by skill ID
    dirctl search --query "skill-id=10201"

    # Complex search with multiple criteria
    dirctl search --limit 10 --offset 0 \
    --query "name=my-agent" \
    --query "skill-name=Text Completion" \
    --query "locator=docker-image:https://example.com/image"
    ```

### Security & Verification

#### Name Verification

Record name verification proves that the signing key is authorized by the domain claimed in the record's name field.

**Requirements:**

- Record name must include a protocol prefix: `https://domain/path` or `http://domain/path`
- A JWKS file must be hosted at `<scheme>://<domain>/.well-known/jwks.json`
- The record must be signed with the private key corresponding to a public key present in that JWKS file

**Workflow:**

1. Push a record with a verifiable name.

    ```bash
    dirctl push record.json --output raw
    # Returns: bafyreib...
    ```

2. Sign the record (triggers automatic verification).

    ```bash
    dirctl sign <cid> --key private.key
    ```

3. Check verification status using [`dirctl naming verify`](./directory-cli.md#dirctl-naming-verify-reference).

#### `dirctl sign <cid> [flags]`

Signs records for integrity and authenticity. When signing a record with a verifiable name (e.g., `https://domain/path`), the system automatically attempts to verify domain authorization via JWKS. See [Name Verification](#name-verification) for details.

??? example

    ```bash
    # Sign with private key
    dirctl sign <cid> --key private.key

    # Sign with OIDC (keyless signing)
    dirctl sign <cid> --oidc --fulcio-url https://fulcio.example.com
    ```

#### `dirctl naming verify <reference>`

Verifies that a record's signing key is authorized by the domain claimed in its name field. Checks if the signing key matches a public key in the domain's JWKS file hosted at `/.well-known/jwks.json`.

**Supported Reference Formats:**

| Format | Description |
|--------|-------------|
| `<cid>` | Verify by content address |
| `<name>` | Verify the most recently created version |
| `<name>:<version>` | Verify a specific version |

??? example

    ```bash
    # Verify by CID
    dirctl naming verify bafyreib... --output json

    # Verify by name (latest version)
    dirctl naming verify cisco.com/agent --output json

    # Verify by name with specific version
    dirctl naming verify cisco.com/agent:v1.0.0 --output json
    ```

    Example verification response:

    ```json
    {
    "cid": "bafyreib...",
    "verified": true,
    "domain": "cisco.com",
    "method": "jwks",
    "key_id": "key-1",
    "verified_at": "2026-01-21T10:30:00Z"
    }
    ```

#### `dirctl verify <record> <signature> [flags]`

Verifies record signatures.

??? example

    ```bash
    # Verify with public key
    dirctl verify record.json signature.sig --key public.key
    ```

### Synchronization

#### `dirctl sync create <url>`

Creates peer-to-peer synchronization.

??? example

    ```bash
    # Create sync with remote peer
    dirctl sync create https://peer.example.com
    ```

#### `dirctl sync list`

Lists active synchronizations.

??? example

    ```bash
    # Show all active syncs
    dirctl sync list
    ```

#### `dirctl sync status <sync-id>`

Checks synchronization status.

??? example

    ```bash
    # Check specific sync status
    dirctl sync status abc123-def456-ghi789
    ```

#### `dirctl sync delete <sync-id>`

Removes synchronization.

??? example

    ```bash
    # Delete a sync
    dirctl sync delete abc123-def456-ghi789
    ```

## Configuration

### Server Connection

```bash
# Connect to specific server
dirctl --server-addr localhost:8888 routing list

# Use environment variable
export DIRECTORY_CLIENT_SERVER_ADDRESS=localhost:8888
dirctl routing list
```

### SPIFFE Authentication

```bash
# Use SPIFFE Workload API
dirctl --spiffe-socket-path /run/spire/sockets/agent.sock routing list
```

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

## Command Organization

The CLI follows a clear service-based organization:

- **Storage**: Direct record management (`push`, `pull`, `delete`, `info`).
- **Import**: Batch imports from external registries (`import`).
- **Routing**: Network announcement and discovery (`routing publish`, `routing list`, `routing search`).
- **Search**: General content search (`search`).
- **Security**: Signing and verification (`sign`, `verify`).
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

For more advanced usage, troubleshooting, and development workflows, see the [AGNTCY documentation](https://docs.agntcy.org/dir/).
