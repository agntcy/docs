# OASF Data Model Schema

## Overview

The data model defines a schema for AI agent content representation. The schema provides a way to describe agent's features, constraints, artifact locators, versioning, ownership, or relevant details.

## Agent Message

```proto
syntax = "proto3";

package schema.model;

message Agent {
    // Name of the agent.
    string name = 1;

    // Version of the agent.
    string version = 2;

    // List of agent's authors in the form of `author-name <author-email>`.
    repeated string authors = 3;

    // Creation timestamp of the agent in the RFC3339 format.
    // Specs: https://www.rfc-editor.org/rfc/rfc3339.html
    string created_at = 4;

    // Additional metadata associated with this agent.
    map<string, string> annotations = 5;

    // List of skills that this agent is capable of performing.
    // Specs: https://schema.oasf.agntcy.org/skills
    repeated string skills = 6;

    // List of source locators where this agent can be found or used from.
    repeated Locator locators = 7;

    // List of extensions that describe this agent more in depth.
    repeated Extension extensions = 8;
}
```

## Locator Message

Locators provide actual artifact locators of an agent. For example, this can reference sources such as helm charts, docker images, binaries, etc.

```proto
message Locator {
    // Location URI where this source locator can be found.
    string url = 1;

    // Type of the source locator, for example: "docker-image", "binary", "source-code".
    string type = 2;

    // Metadata associated with this source locator.
    map<string, string> annotations = 3;

    // Size in bytes of the source locator pointed by the `url` property.
    optional uint64 size = 4;

    // Digest of the source locator pointed by the `url` property.
    optional string digest = 5;
}
```

## Extension Message

Extensions provide dynamic descriptors for an agent. For example, security and categorization features can be described using extensions.

```proto
message Extension {
    // Name of the extension.
    string name = 1;

    // Version of the extension.
    string version = 2;

    // Metadata associated with this extension.
    map<string, string> annotations = 3;

    // Value of the data, it is available directly
    // or can be constructed by fetching from some URL.
    bytes specs = 4;
}
```
