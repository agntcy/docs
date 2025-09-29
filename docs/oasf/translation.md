# Translation Service

The translation service converts OASF records into GitHub Copilot MCP and A2A configuration structures.

## GitHub Copilot MCP

`RecordToGHCopilot` translates an OASF record into a GitHub Copilot MCP configuration structure.

```go
func RecordToGHCopilot(record *structpb.Struct) (*GHCopilotMCPConfig, error)
```

**Returns:**

`*GHCopilotMCPConfig`: MCP configuration for GitHub Copilot

**GHCopilotMCPConfig Structure:**

```go
type GHCopilotMCPConfig struct {
    Servers map[string]MCPServer `json:"servers"`
    Inputs  []MCPInput           `json:"inputs"`
}

type MCPServer struct {
    Command string            `json:"command"`
    Args    []string          `json:"args"`
    Env     map[string]string `json:"env"`
}

type MCPInput struct {
    ID          string `json:"id"`
    Type        string `json:"type"`
    Password    bool   `json:"password"`
    Description string `json:"description"`
}
```

## A2A

`RecordToA2A` translates an OASF record into an A2A card structure.

```go
func RecordToA2A(record *structpb.Struct) (*A2ACard, error)
```

**Returns:**

`*A2ACard`: A2A card configuration

**A2ACard Structure:**

```go
type A2ACard struct {
    Name               string          `json:"name"`
    Description        string          `json:"description"`
    URL                string          `json:"url"`
    Capabilities       map[string]bool `json:"capabilities"`
    DefaultInputModes  []string        `json:"defaultInputModes"`
    DefaultOutputModes []string        `json:"defaultOutputModes"`
    Skills             []A2ASkill      `json:"skills"`
}

type A2ASkill struct {
    ID          string `json:"id"`
    Name        string `json:"name"`
    Description string `json:"description"`
}
```

## Example Usage

For detailed examples, see the [OASF SDK repository](https://github.com/agntcy/oasf-sdk/blob/main/USAGE.md).
