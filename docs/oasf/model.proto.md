# Package: schema.model

<div class="comment"><span></span><br/></div>


### Agent Diagram

```mermaid
classDiagram
direction LR

%% The data model defines a schema for AI agent content representation. The schema provides a way to describe agent's features, constraints, artifact locators, versioning, ownership, or relevant details.

class Agent {
  + string name
  + string version
  + List~string~ authors
  + string created_at
  + Map~string,  string~ annotations
  + List~string~ skills
  + List~Locator~ locators
  + List~Extension~ extensions
}
Agent --> `Locator`
Agent --> `Extension`
Agent --o `Locator`

%% Locators provide actual artifact locators of an agent. For example, this can reference sources such as helm charts, docker images, binaries, etc.

class Locator {
  + string url
  + string type
  + Map~string,  string~ annotations
  + Optional~uint64~ size
  + Optional~string~ digest
}
Agent --o `Extension`

%% Extensions provide dynamic descriptors for an agent. For example, security and categorization features can be described using extensions.

class Extension {
  + string name
  + string version
  + Map~string,  string~ annotations
  + bytes specs
}

```

## Message: Agent
<div style="font-size: 12px; margin-top: -10px;" class="fqn">FQN: schema.model.Agent</div>

<div class="comment"><span>The data model defines a schema for AI agent content representation. The schema provides a way to describe agent's features, constraints, artifact locators, versioning, ownership, or relevant details.</span><br/></div>

| Field       | Ordinal | Type           | Label    | Description                                                                                                |
|-------------|---------|----------------|----------|------------------------------------------------------------------------------------------------------------|
| name        | 1       | string         |          | Name of the agent.                                                                                         |
| version     | 2       | string         |          | Version of the agent.                                                                                      |
| authors     | 3       | string         | Repeated | List of agent’s authors in the form of `author-name <author-email>`.                                     |
| created_at  | 4       | string         |          | Creation timestamp of the agent in the RFC3339 format. Specs: https://www.rfc-editor.org/rfc/rfc3339.html  |
| annotations | 5       | string, string | Map      | Additional metadata associated with this agent.                                                            |
| skills      | 6       | string         | Repeated | List of skills that this agent is capable of performing. Specs: https://schema.oasf.agntcy.org/skills      |
| locators    | 7       | Locator        | Repeated | List of source locators where this agent can be found or used from.                                        |
| extensions  | 8       | Extension      | Repeated | List of extensions that describe this agent more in depth.                                                 |



### Locator Diagram

```mermaid
classDiagram
direction LR

%% Locators provide actual artifact locators of an agent. For example, this can reference sources such as helm charts, docker images, binaries, etc.

class Locator {
  + string url
  + string type
  + Map~string,  string~ annotations
  + Optional~uint64~ size
  + Optional~string~ digest
}

```
### Extension Diagram

```mermaid
classDiagram
direction LR

%% Extensions provide dynamic descriptors for an agent. For example, security and categorization features can be described using extensions.

class Extension {
  + string name
  + string version
  + Map~string,  string~ annotations
  + bytes specs
}

```

## Message: Locator
<div style="font-size: 12px; margin-top: -10px;" class="fqn">FQN: schema.model.Agent.Locator</div>

<div class="comment"><span>Locators provide actual artifact locators of an agent. For example, this can reference sources such as helm charts, docker images, binaries, etc.</span><br/></div>

| Field       | Ordinal | Type           | Label    | Description                                                                        |
|-------------|---------|----------------|----------|------------------------------------------------------------------------------------|
| url         | 1       | string         |          | Location URI where this source locator can be found.                               |
| type        | 2       | string         |          | Type of the source locator, for example: "docker-image", "binary", "source-code".  |
| annotations | 3       | string, string | Map      | Metadata associated with this source locator.                                      |
| size        | 4       | uint64         | Optional | Size in bytes of the source locator pointed by the `url` property.                 |
| digest      | 5       | string         | Optional | Digest of the source locator pointed by the `url` property.                        |




## Message: Extension
<div style="font-size: 12px; margin-top: -10px;" class="fqn">FQN: schema.model.Agent.Extension</div>

<div class="comment"><span>Extensions provide dynamic descriptors for an agent. For example, security and categorization features can be described using extensions.</span><br/></div>

| Field       | Ordinal | Type           | Label | Description                                                                                   |
|-------------|---------|----------------|-------|-----------------------------------------------------------------------------------------------|
| name        | 1       | string         |       | Name of the extension.                                                                        |
| version     | 2       | string         |       | Version of the extension.                                                                     |
| annotations | 3       | string, string | Map   | Metadata associated with this extension.                                                      |
| specs       | 4       | bytes          |       | Value of the data, it is available directly or can be constructed by fetching from some URL.  |






<!-- Created by: Proto Diagram Tool -->
<!-- https://github.com/GoogleCloudPlatform/proto-gen-md-diagrams -->
