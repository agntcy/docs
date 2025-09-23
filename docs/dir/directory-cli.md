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
    dirctl pull baeareihdr6t7s6sr2q4zo456sza66eewqc7huzatyfgvoupaqyjw23ilvi
    ```

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

#### `dirctl pull <cid>`

Retrieves records by their Content Identifier (CID).

??? example

```bash
# Pull record content
dirctl pull baeareihdr6t7s6sr2q4zo456sza66eewqc7huzatyfgvoupaqyjw23ilvi

# Pull with signature verification
dirctl pull <cid> --signature --public-key public.key
```

#### `dirctl delete <cid>`

Removes records from storage.

??? example

```bash
# Delete a record
dirctl delete baeareihdr6t7s6sr2q4zo456sza66eewqc7huzatyfgvoupaqyjw23ilvi
```

#### `dirctl info <cid>`

Displays metadata about stored records.

??? example

```bash
# Show record metadata
dirctl info baeareihdr6t7s6sr2q4zo456sza66eewqc7huzatyfgvoupaqyjw23ilvi
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

# Multiple criteria (AND logic)
dirctl routing list --skill "AI" --locator "docker-image"

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

# Advanced search with scoring
dirctl routing search --skill "web-development" --limit 10 --min-score 1
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

#### `dirctl sign <cid> [flags]`

Signs records for integrity and authenticity.

??? example

```bash
# Sign with private key
dirctl sign <cid> --key private.key

# Sign with OIDC (keyless signing)
dirctl sign <cid> --oidc --fulcio-url https://fulcio.example.com
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
    CID=$(dirctl push my-agent.json)
    ```

1. Publish for discovery

    ```bash
    dirctl routing publish $CID
    ```

1. Verify the record is published

    ```bash
    dirctl routing list --cid $CID
    ```

1. Check routing statistics

    ```bash
    dirctl routing info
    ```

### Discovery Workflow

The following workflow demonstrates how to discover records from the network:

1. Search for records by skill

    ```bash
    dirctl routing search --skill "AI" --limit 10
    ```

1. Search with multiple criteria

    ```bash
    dirctl routing search --skill "AI" --locator "docker-image" --min-score 2
    ```

1. Pull interesting records
    ```bash
    dirctl pull <discovered-cid>
    ```

### Synchronization Workflow

The following workflow demonstrates how to synchronize records between remote directories and your local instance:

1. Create sync with remote peer

    ```bash
    SYNC_ID=$(dirctl sync create https://peer.example.com)
    ```

1. Monitor sync progress

    ```bash
    dirctl sync status $SYNC_ID
    ```

1. List all syncs

    ```bash
    dirctl sync list
    ```

1. Clean up when done

    ```bash
    dirctl sync delete $SYNC_ID
    ```

## Command Organization

The CLI follows a clear service-based organization:

- **Storage**: Direct record management (`push`, `pull`, `delete`, `info`).
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
