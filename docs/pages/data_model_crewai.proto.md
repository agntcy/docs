# Package: schema.model.crewai

<div class="comment"><span>SPDX-FileCopyrightText: Copyright (c) 2025 Cisco and/or its affiliates. SPDX-License-Identifier: Apache-2.0</span><br/></div>

## Imports

| Import | Description |
|--------|-------------|



## Options

| Name | Value | Description |
|------|-------|-------------|




### CrewaiAgentExtensionSpecs Diagram

```mermaid
classDiagram
direction LR

%% CrewaiAgentExtensionSpecs defines an extension schema that encodes CrewAI agent information.

class CrewaiAgentExtensionSpecs {
  + string name
  + string role
  + string goal
  + string backstory
  + string llm
  + List~Task~ task
}
CrewaiAgentExtensionSpecs --> `Task`
CrewaiAgentExtensionSpecs --o `Task`

%% Basic information about CrewAI agent tasks.

class Task {
  + string name
  + string description
  + string context
  + string expected_output
  + string output_format
}

```

## Message: CrewaiAgentExtensionSpecs
<div style="font-size: 12px; margin-top: -10px;" class="fqn">FQN: schema.model.crewai.CrewaiAgentExtensionSpecs</div>

<div class="comment"><span>CrewaiAgentExtensionSpecs defines an extension schema that encodes CrewAI agent information.</span><br/></div>

| Field     | Ordinal | Type   | Label    | Description |
|-----------|---------|--------|----------|-------------|
| name      | 1       | string |          |             |
| role      | 2       | string |          |             |
| goal      | 3       | string |          |             |
| backstory | 4       | string |          |             |
| llm       | 5       | string |          |             |
| task      | 6       | Task   | Repeated |             |



### Task Diagram

```mermaid
classDiagram
direction LR

%% Basic information about CrewAI agent tasks.

class Task {
  + string name
  + string description
  + string context
  + string expected_output
  + string output_format
}

```

## Message: Task
<div style="font-size: 12px; margin-top: -10px;" class="fqn">FQN: schema.model.crewai.CrewaiAgentExtensionSpecs.Task</div>

<div class="comment"><span>Basic information about CrewAI agent tasks.</span><br/></div>

| Field           | Ordinal | Type   | Label | Description |
|-----------------|---------|--------|-------|-------------|
| name            | 1       | string |       |             |
| description     | 2       | string |       |             |
| context         | 3       | string |       |             |
| expected_output | 4       | string |       |             |
| output_format   | 5       | string |       |             |






<!-- Created by: Proto Diagram Tool -->
<!-- https://github.com/GoogleCloudPlatform/proto-gen-md-diagrams -->
