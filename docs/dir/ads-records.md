# ADS Records

Directory uses [Open Agent Schema Framework](https://schema.oasf.outshift.com) (OASF) which defines a standardized schema for representing agents and their capabilities using [OASF Record specification](https://schema.oasf.outshift.com/0.7.0/objects/record). This ensures interoperability and consistency across different implementations of the directory service.

## Content Identifier

The content identifier of the record is a [Content IDentifier](https://github.com/multiformats/cid) (CID) hash digest which makes it:

- Globally unique
- Content-addressable
- Collision-resistant
- Immutable

## Verifiable Names

Records must include a `name` field with a domain-based identifier that enables name verification. When a record uses a verifiable name:

- The name must include a protocol prefix: `https://domain/path` or `http://domain/path`.
- The domain must host a JWKS file at `<scheme>://<domain>/.well-known/jwks.json`.
- Records signed with a private key associated with a public key present in that JWKS file can be verified as authorized by the domain.

See the [Directory CLI documentation](directory-cli.md#name-verification) for details on name verification workflows.

## Example Email Agent

You can generate your own example records using the [OASF Record Sample generator](https://schema.oasf.outshift.com/sample/0.7.0/objects/record). Below is an example OASF record for an email agent that is capable of sending and receiving emails.

!!! note

    This record uses `0.7.0` of the OASF specification.

```json
{
    "schema_version": "0.7.0",
    "name": "https://cisco.com/agents/email-agent",
    "version": "v1.0.0",
    "authors": [
      "Cisco Systems Inc."
    ],
    "description": "An agent that can send and receive emails.",
    "created_at": "2025-08-11T16:20:37.159072Z",
    "skills": [
        {
            "id": 10306,
            "name": "natural_language_processing/information_retrieval_synthesis/information_retrieval_synthesis_search"
        },
        {
            "id": 10202,
            "name": "natural_language_processing/natural_language_generation/summarization"
        },
        {
            "id": 60103,
            "name": "retrieval_augmented_generation/retrieval_of_information/document_retrieval"
        }
    ],
    "locators": [
      {
        "url": "https://github.com/agntcy/agentic-apps/tree/main/email_reviewer",
        "type": "source_code"
      },
      {
        "url": "https://github.com/agntcy/agentic-apps/tree/main/email_reviewer/pyproject.toml",
        "type": "python_package"
      }
    ]
}
```

!!! note

    The `name` field uses a verifiable domain-based format (`https://cisco.com/agents/email-agent`). When signed with a key authorized by the domain's JWKS file at `https://cisco.com/.well-known/jwks.json`, this record can be pulled using the convenient reference `cisco.com/agents/email-agent:v1.0.0` instead of its CID.
