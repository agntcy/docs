# Package: schema.model

<div class="comment"><span>SPDX-FileCopyrightText: Copyright (c) 2025 Cisco and/or its affiliates. SPDX-License-Identifier: Apache-2.0</span><br/></div>

## Imports

| Import | Description |
|--------|-------------|



## Options

| Name | Value | Description |
|------|-------|-------------|




### AgentDataModel Diagram

```mermaid
classDiagram
direction LR

%% The data model defines a schema for AI agent content representation. The schema provides a way to describe agent's features, constraints, artifact locators, versioning, ownership, or relevant details.

class AgentDataModel {
  + string digest
  + string name
  + string version
  + List~string~ authors
  + Map~string,  string~ annotations
  + string created_at
  + List~Locator~ locators
  + List~Extension~ extensions
}
AgentDataModel --> `Locator`
AgentDataModel --> `Extension`
AgentDataModel --o `Locator`

%% Locators provide actual artifact locators of an agent. For example, this can reference sources such as helm charts, docker images, binaries, etc.

class Locator {
  + Map~string,  string~ annotations
  + string name
  + string type
  + string url
  + uint64 size
  + string digest
}
AgentDataModel --o `Extension`

%% Extensions provide dynamic descriptors for an agent. For example, security and categorization features can be described using extensions.

class Extension {
  + Map~string,  string~ annotations
  + string name
  + string version
  + bytes specs
}

```

## Message: AgentDataModel
<div style="font-size: 12px; margin-top: -10px;" class="fqn">FQN: schema.model.AgentDataModel</div>

<div class="comment"><span>The data model defines a schema for AI agent content representation. The schema provides a way to describe agent's features, constraints, artifact locators, versioning, ownership, or relevant details.</span><br/></div>

| Field       | Ordinal | Type           | Label    | Description                                                                                       |
|-------------|---------|----------------|----------|---------------------------------------------------------------------------------------------------|
| digest      | 1       | string         |          | Digest defines complete content fingerprint. It can be used as a globally-unique ID of an Agent.  |
| name        | 2       | string         |          | Name of the agent                                                                                 |
| version     | 3       | string         |          | Version of the agent                                                                              |
| authors     | 4       | string         | Repeated | List of agent’s authors in the form of `author-name <author-email>`                             |
| annotations | 5       | string, string | Map      | Additional metadata associated with this agent                                                    |
| created_at  | 6       | string         |          | Timestamp of the agent creation time                                                              |
| locators    | 7       | Locator        | Repeated | List of source locators where this agent can be found or used from                                |
| extensions  | 8       | Extension      | Repeated | List of extensions that describe this agent and its capabilities more in depth                    |



### Locator Diagram

```mermaid
classDiagram
direction LR

%% Locators provide actual artifact locators of an agent. For example, this can reference sources such as helm charts, docker images, binaries, etc.

class Locator {
  + Map~string,  string~ annotations
  + string name
  + string type
  + string url
  + uint64 size
  + string digest
}

```
### Extension Diagram

```mermaid
classDiagram
direction LR

%% Extensions provide dynamic descriptors for an agent. For example, security and categorization features can be described using extensions.

class Extension {
  + Map~string,  string~ annotations
  + string name
  + string version
  + bytes specs
}

```

## Message: Locator
<div style="font-size: 12px; margin-top: -10px;" class="fqn">FQN: schema.model.AgentDataModel.Locator</div>

<div class="comment"><span>Locators provide actual artifact locators of an agent. For example, this can reference sources such as helm charts, docker images, binaries, etc.</span><br/></div>

| Field       | Ordinal | Type           | Label | Description                                                        |
|-------------|---------|----------------|-------|--------------------------------------------------------------------|
| annotations | 1       | string, string | Map   | Metadata associated with this source locator                       |
| name        | 2       | string         |       | Name of the source locator for this agent                          |
| type        | 3       | string         |       | Type of the source locator, e.g. `docker-image, helm-chart`        |
| url         | 4       | string         |       | Location URI where this source locator can be found                |
| size        | 5       | uint64         |       | Size in bytes of the source locator pointed by the `url` property  |
| digest      | 6       | string         |       | Digest of the source locator pointed by the `url` property         |




## Message: Extension
<div style="font-size: 12px; margin-top: -10px;" class="fqn">FQN: schema.model.AgentDataModel.Extension</div>

<div class="comment"><span>Extensions provide dynamic descriptors for an agent. For example, security and categorization features can be described using extensions.</span><br/></div>

| Field       | Ordinal | Type           | Label | Description                                                                              |
|-------------|---------|----------------|-------|------------------------------------------------------------------------------------------|
| annotations | 1       | string, string | Map   | Metadata associated with this extension                                                  |
| name        | 2       | string         |       | Name of the extension attached to this agent                                             |
| version     | 3       | string         |       | Version of the extension attached to this agent                                          |
| specs       | 4       | bytes          |       | Generic specification schema of this extension. Value of this property is JSON-encoded.  |






<!-- Created by: Proto Diagram Tool -->
<!-- https://github.com/GoogleCloudPlatform/proto-gen-md-diagrams -->
