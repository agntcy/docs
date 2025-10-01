# Features and Usage Scenarios

This document defines a basic overview of main Directory features, components, and usage
scenarios. All code snippets below are tested against the Directory `v0.3.0` release.

!!! note
    Although the following example is shown for a CLI-based usage scenario, the same
    functionality can be performed using language-specific SDKs.

## Prerequisites

The following prerequisites are required to follow the examples below:

- Locally available Directory CLI client
- Running instance of Directory API server

To deploy the necessary components, please refer to the [Getting Started](getting-started.md)
guide.

## Build

This example demonstrates how to define a Record using provided tooling to prepare for
publication.

To start, generate an example Record that matches the data model schema defined in
[OASF Record specification](https://schema.oasf.outshift.com/0.7.0/objects/record) using the
[OASF Record Sample generator](https://schema.oasf.outshift.com/sample/0.7.0/objects/record).

```bash
# Generate an example data model
cat << EOF > record.json
{
    "name": "my-record",
    "version": "v1.0.0",
    "description": "insert description here",
    "schema_version": "0.7.0",
    "skills": [
        {
            "id": 201,
            "name": "images_computer_vision/image_segmentation"
        }
    ],
    "authors": [
        "Jane Doe"
    ],
    "created_at": "2025-08-11T16:20:37.159072Z",
    "locators": [
        {
            "type": "source_code",
            "url": "https://github.com/agntcy/oasf/blob/main/record"
        }
    ]
}
EOF
```

## Store

This example demonstrates the interaction with the local storage layer using the CLI client.
The storage layer uses an OCI-compliant registry (powered by [Zot](https://github.com/project-zot/zot)) to store records as OCI
artifacts with [content-addressable identifiers](https://github.com/multiformats/cid) (CIDs).
When a record is pushed, it is stored as an OCI blob and the CID is calculated by converting
the SHA256 OCI digest into a CIDv1 format using CID multihash encoding. Each record is then
tagged with its CID in the registry, enabling direct lookup and ensuring content
integrity through cryptographic addressing.

```bash
# Push the record and store its CID to a file
dirctl push record.json > record.cid

# Set the CID as a variable for easier reference
RECORD_CID=$(cat record.cid)

# Pull the record
# Returns the same data as record.json
dirctl pull $RECORD_CID

# Lookup basic metadata about the record
# Returns annotations, creation timestamp and OASF schema version
dirctl info $RECORD_CID
```

## Signing and Verification

Establishing trust and authenticity is critical in distributed AI agent ecosystems, where
records may be shared across multiple nodes and networks. By cryptographically signing
records, publishers can prove authorship and ensure data integrity, while consumers can
verify that records haven't been tampered with and originate from trusted sources before
deploying or executing agent code.

Signatures and public keys are stored in the OCI registry as referrer artifacts that
maintain subject relationships with their associated records. When a record is signed, the
signature is attached as a Cosign-compatible OCI artifact. Public keys are similarly stored
as separate OCI artifacts, creating a verifiable chain of trust through OCI's native
referrer mechanism.

Server-side verification leverages Zot's trust extension through GraphQL queries that check
both signature validity and trust status. When public keys are uploaded to Zot, they enable
the registry to mark signatures as "trusted" when they can be cryptographically verified
against the stored public keys. The verification process queries Zot's search API to
retrieve signature metadata including the `IsSigned` and `IsTrusted` status, allowing the
Directory server to make trust decisions based on the cryptographic verification performed
by the underlying OCI registry infrastructure.

### Method 1: OIDC-based Interactive

This process relies on creating and uploading to the OCI registry a signature for the record
using identity-based OIDC signing flow which can later be verified. The signing process
opens a browser window to authenticate the user with an OIDC identity provider. These
operations are implemented using [Sigstore](https://www.sigstore.dev/).

```bash
# Push record with signature
dirctl push record.json --sign

# Alternatively, sign a pushed record
dirctl sign $RECORD_CID

# Verify record
dirctl verify $RECORD_CID
```

### Method 2: OIDC-based Non-Interactive

This method is designed for automated environments such as CI/CD pipelines where
browser-based authentication is not available. It uses OIDC tokens provided by the
execution environment (like GitHub Actions) to sign records. The signing process uses a
pre-obtained OIDC token along with provider-specific configuration to establish identity
without user interaction.

```
- name: Push and sign record
  run: |
    bin/dirctl push record.json --sign \
      --oidc-token ${{ steps.oidc-token.outputs.token }} \
      --oidc-provider-url "https://token.actions.githubusercontent.com" \
      --oidc-client-id "https://github.com/${{ github.repository }}/.github/workflows/demo.yaml@${{ github.ref }}"

- name: Run verify command
  run: |
    echo "Running dir verify command"
    bin/dirctl verify $RECORD_CID
```

### Method 3: Self-Managed Keys

This method is suitable for non-interactive use cases, such as CI/CD pipelines, where
browser-based authentication is not possible or desired. Instead of OIDC, a signing keypair
is generated (e.g., with Cosign), and the private key is used to sign the record.

```bash
# Generate a key-pair for signing
# This creates 'cosign.key' (private) and 'cosign.pub' (public)
cosign generate-key-pair

# Set COSIGN_PASSWORD shell variable if you password-protected the private key
export COSIGN_PASSWORD=your_password_here

# Push record with signature 
dirctl push record.json --sign --key cosign.key

# Verify the signed record
dirctl verify $RECORD_CID
```

## Announce

This example demonstrates how to publish records to allow content discovery across the
network. Publication requests are processed asynchronously in the background using a
scheduler that manages DHT announcements. To avoid stale data, it is recommended to
republish the data periodically as the data across the network has TTL.

Note that this operation only works for the objects already pushed to the local storage
layer, i.e., it is required to first push the data before publication.

```bash
# Publish the record across the network
dirctl routing publish $RECORD_CID
```

If the data is not published to the network, it cannot be discovered by other peers. For
published data, peers may try to reach out over the network to request specific objects for
verification and replication. Network publication may fail if you are not connected to the
network.

## Discover

This example demonstrates how to discover records both locally and across the network using
two distinct commands for different use cases.

### Local Discovery

Use `dirctl routing list` to discover records stored locally on this peer only. This queries
the server's local storage index and does not search other peers on the network.

```bash
# List all local records
dirctl routing list

# List local records with specific skill
dirctl routing list --skill "images_computer_vision/image_segmentation"

# List records with multiple criteria (AND logic)
dirctl routing list --skill "images_computer_vision/image_segmentation" \
                    --locator "source_code"

# List specific record by CID
dirctl routing list --cid $RECORD_CID
```

### Network Discovery

Use `dirctl routing search` to discover records from other peers across the network. This
uses cached network announcements and filters out local records.

```bash
# Search for records with exact skill match
dirctl routing search --skill "images_computer_vision/image_segmentation"

# Search for records with skill prefix match (finds all NLP-related skills)
dirctl routing search --skill "images_computer_vision"

# Search with multiple criteria (OR logic with minimum score)
dirctl routing search --skill "images_computer_vision" \
                      --skill "images_computer_vision" \
                      --min-score 2

# Search with result limiting
dirctl routing search --skill "images_computer_vision" \
                      --limit 5
```

Network search supports hierarchical matching where skills, domains, and modules use both
exact and prefix matching (e.g., `images_computer_vision` matches both `images_computer_vision`
and `images_computer_vision/image_segmentation` as a prefix).

Note that network search results are not guaranteed to be available, valid, or up to date as
they rely on cached announcements from other peers.

## Search

This example demonstrates how to search for records in your local directory using various filters
and query parameters. The search functionality allows you to find records based on specific
attributes like name, version, skills, locators, and extensions using structured query
filters with wildcard support. All searches are case insensitive.

Search operations leverage an SQLite database for efficient record indexing and querying,
supporting pagination and returning Content Identifier (CID) values that can be used with
other Directory commands like `pull`, `info`, and `verify`.

```bash
# Basic search for records by name
dirctl search --query "name=my-agent-name"

# Search for records with a specific version
dirctl search --query "version=v1.0.0"

# Search for records that have a particular skill by ID
dirctl search --query "skill-id=10201"

# Search for records with a specific skill name
dirctl search --query "skill-name=images_computer_vision/image_segmentation"

# Search for records with a specific locator type and URL
dirctl search --query "locator=docker_image:https://example.com/my-agent"

# Search for records with a specific module
dirctl search --query "module=my-custom-module"

# Combine multiple query filters (AND operation)
dirctl search \
  --query "name=my-agent" \
  --query "version=v1.0.0" \
  --query "skill-name=images_computer_vision/image_segmentation"

# Use pagination to limit results and specify offset
dirctl search \
  --query "skill-name=images_computer_vision/image_segmentation" \
  --limit 10 \
  --offset 0

# Get the next page of results
dirctl search \
  --query "skill-name=images_computer_vision/image_segmentation" \
  --limit 10 \
  --offset 10
```

### Wildcard Search

The search functionality supports wildcard patterns for flexible matching:

```bash
# Asterisk (*) wildcard - matches zero or more characters
dirctl search --query "name=web*"              # Find all web-related agents
dirctl search --query "version=v1.*"           # Find all v1.x versions
dirctl search --query "skill-name=audio*"      # Find Audio-related skills
dirctl search --query "locator=http*"          # Find HTTP-based locators

# Question mark (?) wildcard - matches exactly one character
dirctl search --query "version=v1.0.?"         # Find version v1.0.x (single digit)
dirctl search --query "name=???api"            # Find 3-character names ending in "api"
dirctl search --query "skill-name=Pytho?"      # Find skills with single character variations

# List wildcards ([]) - matches any character within brackets
dirctl search --query "name=agent-[0-9]"       # Find agents with numeric suffixes
dirctl search --query "version=v[0-9].*"       # Find versions starting with v + digit
dirctl search --query "skill-name=[A-M]*"      # Find skills starting with A-M
dirctl search --query "locator=[hf]tt[ps]*"    # Find HTTP/HTTPS/FTP locators

# Complex wildcard combinations
dirctl search --query "name=api-*-service" --query "version=v2.*"
dirctl search --query "skill-name=*machine*learning*"
dirctl search --query "name=web-[0-9]?" --query "version=v?.*.?"
```

**Available Query Types:**

- `name` - Search by record name
- `version` - Search by record version  
- `skill-id` - Search by skill ID number
- `skill-name` - Search by skill name
- `locator` - Search by locator (format: `type:url`)
- `module` - Search by module name

**Query Format:**

All queries use the format `field=value`. Multiple queries are combined with AND logic,
meaning results must match all specified criteria.

## Sync

The sync feature enables one-way synchronization of records and other objects between
remote Directory instances and your local node. This feature supports distributed AI agent
ecosystems by allowing you to replicate content from multiple remote directories, creating
local mirrors for offline access, backup, and cross-network collaboration.

**How Sync Works**: Directory leverages [Zot](https://zotregistry.dev/), a cloud-native OCI
registry, as the underlying synchronization engine. When you create a sync operation, the
system dynamically configures Zot's sync extension to pull content from remote registries.
Objects are stored as OCI artifacts (manifests, blobs, and tags), enabling container-native
synchronization with automatic polling, retry mechanisms, and secure credential exchange
between Directory nodes.

This example demonstrates how to synchronize records between remote directories and your
local instance.

### Basic Sync Operations

```bash
# Create a sync operation to start periodic poll from remote (sync all records)
dirctl sync create https://remote-directory.example.com:8888

# Sync specific records by CID
dirctl sync create https://remote-directory.example.com:8888 \
                   --cids cid1,cid2,cid3

# List all sync operations
dirctl sync list

# Check the status of a specific sync operation
dirctl sync status <sync-id>

# Delete a sync operation to stop periodic poll from remote
dirctl sync delete <sync-id>
```

### Advanced Sync with Routing

You can combine routing search with sync operations to selectively synchronize records that
match specific criteria:

```bash
# Search for agents with a given skill across
# the network and sync them automatically
dirctl routing search --skill "Audio" --json | dirctl sync create --stdin
```

This creates separate sync operations for each remote peer found in the search results,
syncing only the specific CIDs that matched your search criteria.

## gRPC Error Codes

The following table lists the gRPC error codes returned by the server APIs, along with a
description of when each code is used:

| Error Code                 | Description                                                  |
| -------------------------- | ------------------------------------------------------------ |
| `codes.InvalidArgument`    | When client provides an invalid or malformed argument, such |
|                            | as a missing or invalid record reference or record.         |
| `codes.NotFound`           | When the requested object does not exist in the local store |
|                            | or across the network.                                       |
| `codes.FailedPrecondition` | When the server environment or configuration is not in the  |
|                            | required state (e.g., failed to create a directory or temp  |
|                            | file).                                                       |
| `codes.Internal`           | When an unexpected internal error occurs, such as I/O       |
|                            | failures, serialization errors, or other server-side        |
|                            | issues.                                                      |
| `codes.Canceled`           | When the operation is canceled by the client or context     |
|                            | expires.                                                     |
| `codes.Unauthenticated`    | When the client is not authenticated to perform the         |
|                            | operation.                                                   |
| `codes.PermissionDenied`   | When the client does not have permission to perform the     |
|                            | operation.                                                   |
