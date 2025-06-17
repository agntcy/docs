# Usage Scenarios

The following section showcases a few usage scenarios of the Agent Directory.

Although the following example is shown for CLI-based usage scenario, there is
an effort on exposing the same functionality via SDKs.

## Requirements

- Directory CLI client, distributed via [GitHub Releases](https://github.com/agntcy/dir/releases)
- Directory API server, outlined in the [Deployment](#deployment) section.

## Build

Some [examples](../dir/dir-record-example.md) are reported to show how to describe data in a record
and how to build such data models using directory cli to prepare for publication.

Generate an example agent that matches the data model schema defined in
[Agent Data Model](api/core/v1alpha1/agent.proto) specification.

```bash
cat << EOF > model.json
{
  "name": "my-agent",
  "skills": [
    {"category_name": "Text Generation"},
    {"category_name": "Fact Extraction"}
  ]
}
EOF
```

Alternatively, build the same agent data model using the CLI client.
The build process allows additional operations to be performed,
which is useful for agent model enrichment and other custom use-cases.

```bash
# Define the build config
cat << EOF > build.config.yml
builder:
  # Base agent model path
  base-model: "model.json"

  # Disable the LLMAnalyzer plugin
  llmanalyzer: false

  # Disable the runtime plugin
  runtime: false
EOF

# Build the agent
dirctl build . > built.model.json

# Override above example
mv built.model.json model.json
```

## Signing and Verification

This process relies on attaching signature to the agent data model using identity-based OIDC signing flow which can be verified by other clients.
The signing process opens a browser window to authenticate the user
with an OIDC identity provider.
The verification process validates the agent signature against the identity provider and signature transparency services.
These operations are implemented using [Sigstore](https://www.sigstore.dev/).

```bash
## Sign the agent data model
cat model.json | dirctl sign --stdin > signed.model.json

## Verify agent data models
cat model.json | dirctl verify --stdin
cat signed.model.json | dirctl verify --stdin

## Verify signature using custom parameters:
# 1. Only trust users with "cisco.com" addresses
# 2. Only trust issuers from "github.com"
dirctl verify signed.model.json \
   --oidc-identity "(.*)@cisco.com" \
   --oidc-issuer "(.*)github.com(.*)"

## Replace the base agent model with a signed one
rm -rf model.json
mv signed.model.json model.json
```

## Store

This example demonstrates the interaction with the local storage layer.
It is used as an content-addressable object store for directory-specific models and serves both the local and network-based operations (if enabled).

```bash
# push and store content digest
dirctl push model.json > model.digest
DIGEST=$(cat model.digest)

# pull
dirctl pull $DIGEST

# lookup
dirctl info $DIGEST
```

## Announce

This examples demonstrates how to publish the data to allow content discovery.
To avoid stale data, it is recommended to republish the data periodically
as the data across the network has TTL.

Note that this operation only works for the objects already pushed to local storage layer, ie.
you must first push the data before being able to perform publication.

```bash
# Publish the data to your local data store.
dirctl publish $DIGEST

# Publish the data across the network.
dirctl publish $DIGEST --network
```

If the data is not published to the network, it cannot be discovered by other peers.
For published data, peers may try to reach out over network
and request specific objects for verification and replication.
Network publication may fail if you are not connected to any peers.

## Discover

This examples demonstrates how to discover published data locally or across the network.
This API supports both unicast- mode for routing to specific objects,
and multicast mode for attribute-based matching and routing.

There are two modes of operation, a) local mode where the data is queried from the local data store, and b) network mode where the data is queried across the network.

Discovery is performed using full-set label matching, ie. the results always fully match the requested query.
Note that it is not guaranteed that the data is available, valid, or up to date as results.

```bash
# Get a list of peers holding a specific agent data model
dirctl list --digest $DIGEST

# Discover the agent data models in your local data store that can fully satisfy your search query.
dirctl list "/skills/Text Generation"
dirctl list "/skills/Text Generation" "/skills/Fact Extraction"

# Discover the agent data models across the network that can fully satisfy your search query.
dirctl list "/skills/Text Generation" --network
dirctl list "/skills/Text Generation" "/skills/Fact Extraction" --network
```

It is also possible to get an aggregated summary about the data held in your local data store or across the network.
This is used for routing decisions when traversing the network.
Note that for network search, you will not query your own data, but only the data of other peers.

```bash
# Get a list of labels and basic summary details about the data you currently have in your local data store.
dirctl list info

# Get a list of labels and basic summary details about the data you across the reachable network.
dirctl list info --network
```
