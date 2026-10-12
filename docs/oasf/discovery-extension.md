# Discovery Extension

The [discovery object](https://schema.oasf.outshift.com/objects/discovery)
carries the OASF skills and domains of an artifact on their own, without a
record around them, so that other formats can embed them as an extension.
A consumer can then search those artifacts by skill and domain with the same
vocabulary as OASF records.

## Payload

| Attribute        | Requirement | Description                                                 |
|------------------|-------------|-------------------------------------------------------------|
| `schema_version` | required    | The OASF version the payload conforms to.                   |
| `skills`         | required    | Skill references (`name` and/or `id`), as in a record.      |
| `domains`        | recommended | Domain references (`name` and/or `id`), as in a record.     |

```json
{
  "schema_version": "1.2.0",
  "skills": [{"name": "software_engineering/code_debugging/error_handling", "id": 60602}],
  "domains": [{"name": "technology/networking/network_security", "id": 10305}]
}
```

A payload validates on its own like any other schema object, for example
through `POST /api/validate/object/discovery` on the
[OASF server](oasf-server.md).
An unknown skill or domain fails with the same error as inside a record.

## Extension Key

The extension key is the reverse-DNS string `org.agntcy.discovery.v1`.

The key is permanent: once artifacts carry it, it is not renamed.
A change to the payload that is not backward compatible gets a new key, such
as `org.agntcy.discovery.v2`.

## Embedding

The payload is the same in every host format.
Only its placement differs, because each host format fixes how an extension is
wrapped: the payload goes, unchanged, into the slot that the host format
reserves for extension data under the key.

| Host format    | Where the key goes                  | Where the payload goes     |
|----------------|-------------------------------------|----------------------------|
| A2A Agent Card | `uri` of an `AgentExtension`        | `params` of that extension |
| AI Catalog     | key of the entry's `extensions` map | value of that key          |

### A2A Agent Card

In an [A2A Agent Card](https://a2a-protocol.org/latest/specification/), the
payload is the `params` of an `AgentExtension` in `capabilities.extensions`:

```json
{
  "capabilities": {
    "extensions": [
      {
        "uri": "org.agntcy.discovery.v1",
        "description": "OASF skills and domains",
        "params": {
          "schema_version": "1.2.0",
          "skills": [{"name": "software_engineering/code_debugging/error_handling", "id": 60602}],
          "domains": [{"name": "technology/networking/network_security", "id": 10305}]
        }
      }
    ]
  }
}
```

### AI Catalog Entry

In an [AI Catalog](https://ai-catalog.io/spec/) entry, the payload is the value
of the key in the entry's `extensions` map:

```json
{
  "specVersion": "1.0",
  "entries": [
    {
      "identifier": "urn:example:agents:network-debugger",
      "type": "application/a2a-agent-card+json",
      "version": "1.0.0",
      "url": "https://agents.example.com/network-debugger/.well-known/agent-card.json",
      "extensions": {
        "org.agntcy.discovery.v1": {
          "schema_version": "1.2.0",
          "skills": [{"name": "software_engineering/code_debugging/error_handling", "id": 60602}],
          "domains": [{"name": "technology/networking/network_security", "id": 10305}]
        }
      }
    }
  ]
}
```
