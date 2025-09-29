# OASF SDK

The OASF SDK provides three services for working with OASF records:

* Validation: Validate OASF records against schema specifications.
* Translation: Convert OASF records to different formats (GitHub Copilot MCP, A2A).
* Decoding: Convert between JSON, Go structs, and Protocol Buffer structures.

The proto files can be found [here](https://buf.build/agntcy/oasf-sdk).

## Installation

The OASF SDK is available as a Go module and a Helm chart.

Add the OASF SDK package to your Go project:

```bash
go install github.com/agntcy/oasf-sdk/pkg@latest
```

Deploy the OASF SDK server using the provided Helm chart:

```bash
helm install oasf-sdk ./helm/oasf-sdk
```

## Usage

The OASF SDK can be used in two ways:

As a Go Package, you can import and use the packages directly in your Go application.

As a gRPC Service, you can deploy the server and communicate via gRPC.

## Decoding Service

The decoding service converts between different data formats and creates OASF-compliant records.

### `JsonToProto`

Converts a JSON object to a Protocol Buffer Struct.

```go
func JsonToProto(data []byte) (*structpb.Struct, error)
```

**Parameters:**

* `data`: JSON data as byte array

Returns `*structpb.Struct`: Protocol Buffer Struct representation.

### `StructToProto`

Converts a Go struct to a Protocol Buffer Struct.

```go
func StructToProto(goObj any) (*structpb.Struct, error)
```

**Parameters:**

* `goObj`: Any Go struct or object

Returns `*structpb.Struct`: Protocol Buffer Struct representation.

### `ProtoToStruct`

Converts a Protocol Buffer Struct to a Go struct.

```go
func ProtoToStruct[T any](obj *structpb.Struct) (*T, error)
```

**Parameters:**

* `obj`: Protocol Buffer Struct to convert

Returns `*T`: Pointer to the converted Go struct.


### `DecodeRecord`

Decodes a record object into a structured format based on its schema version.

```go
func DecodeRecord(record *structpb.Struct) (*decodingv1.DecodeRecordResponse, error)
```

**Parameters:**

* `record`: OASF record as Protocol Buffer Struct

Returns `*decodingv1.DecodeRecordResponse`: decoded record response with version-specific structure.

### `GetRecordSchemaVersion`

Extracts the schema version from a record object.

```go
func GetRecordSchemaVersion(record *structpb.Struct) (string, error)
```

**Parameters:**

* `record`: OASF record as Protocol Buffer Struct

Returns `string`: schema version (e.g., "v0.3.1", "v0.7.0").

## Translation Service

The translation service converts OASF records into GitHub Copilot MCP and A2A configuration structures.

### GitHub Copilot MCP

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

### A2A

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

### Example Usage

**Prerequisites:**

* Translation SDK binary, distributed via [GitHub Releases](https://github.com/agntcy/oasf-sdk/releases)
* Translation SDK docker images, distributed via [GitHub Packages](https://github.com/orgs/agntcy/packages?repo_name=oasf-sdk)

Start the OASF SDK as a docker container, which will listen for incoming requests on port 31234:

```bash
docker run -p 31234:31234 ghcr.io/agntcy/oasf-sdk:latest
```

**GitHub Copilot MCP:**

Create a GitHub Copilot config from the OASF data model using the RecordToGHCopilot RPC method. You can pipe the output to a file wherever you want to save the config.

```bash
cat e2e/fixtures/translation_record.json | jq '{record: .}' | grpcurl -plaintext -d @ localhost:31234 agntcy.oasfsdk.translation.v1.TranslationService/RecordToGHCopilot
```

Output:

```json
{
  "data": {
    "mcpConfig": {
      "inputs": [
        {
          "description": "Secret value for GITHUB_PERSONAL_ACCESS_TOKEN",
          "id": "GITHUB_PERSONAL_ACCESS_TOKEN",
          "password": true,
          "type": "promptString"
        }
      ],
      "servers": {
        "github": {
          "args": [
            "run",
            "-i",
            "--rm",
            "-e",
            "GITHUB_PERSONAL_ACCESS_TOKEN",
            "ghcr.io/github/github-mcp-server"
          ],
          "command": "docker",
          "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:GITHUB_PERSONAL_ACCESS_TOKEN}"
          }
        }
      }
    }
  }
}
```

**A2A:**

To extract A2A card from the OASF data model, use the `RecordToA2A` RPC method.

```bash
cat e2e/fixtures/translation_record.json | jq '{record: .}' | grpcurl -plaintext -d @ localhost:31234 agntcy.oasfsdk.translation.v1.TranslationService/RecordToA2A
```

Output:

```json
{
  "data": {
    "a2aCard": {
      "capabilities": {
        "pushNotifications": false,
        "streaming": true
      },
      "defaultInputModes": [
        "text"
      ],
      "defaultOutputModes": [
        "text"
      ],
      "description": "An agent that performs web searches and extracts information.",
      "name": "example-agent",
      "skills": [
        {
          "description": "Performs web searches to retrieve information.",
          "id": "browser",
          "name": "browser automation"
        }
      ],
      "url": "http://localhost:8000"
    }
  }
}
```

## Validation Service

The validation service validates OASF records against JSON schemas. It supports both embedded schemas and custom schema URLs. The validation service supports the following features:

* Validates records against embedded schema versions (v0.3.1 and v0.7.0).
* Supports custom schema URLs for remote validation.
* Returns detailed validation errors.
* Automatic schema version detection from records.

Use `ValidateRecord` to validate a record against a specified schema URL or its embedded schema version.

**Parameters:**

* `record`: The OASF record to validate (as a Protocol Buffer Struct)
* `options`: Optional validation options

**Returns:**

* `bool`: Whether the record is valid
* `[]string`: List of validation errors (empty if valid)
* `error`: Any error that occurred during validation

**Options:**

* `WithSchemaURL(url string)`: Validate against a custom schema URL instead of embedded schemas

### Example Usage

```go
package main

import (
	"fmt"
	"log"

	"github.com/agntcy/oasf-sdk/pkg/decoder"
	"github.com/agntcy/oasf-sdk/pkg/validator"
)

func main() {
	// Create a new validator instance with embedded schemas
	v, err := validator.New()
	if err != nil {
		log.Fatalf("Failed to create validator: %v", err)
	}

	// Sample OASF record data as a Go struct
	recordData := map[string]interface{}{
		"name":           "example.org/my-agent",
		"schema_version": "v0.7.0",
		"version":        "v1.0.0",
		"description":    "An example agent for demonstration",
		"authors":        []string{"Your Name <your.email@example.com>"},
		"created_at":     "2025-01-01T00:00:00Z",
		"domains": []map[string]interface{}{
			{
				"id":   101,
				"name": "technology/internet_of_things",
			},
		},
		"locators": []map[string]interface{}{
			{
				"type": "docker_image",
				"url":  "ghcr.io/example/my-agent:latest",
			},
		},
		"skills": []map[string]interface{}{
			{
				"name": "natural_language_processing/natural_language_understanding",
				"id":   101,
			},
		},
	}

	// Convert Go struct to protobuf format using OASF SDK decoder
	recordStruct, err := decoder.StructToProto(recordData)
	if err != nil {
		log.Fatalf("Failed to convert struct to proto: %v", err)
	}

	// Validate using embedded schemas (default behavior)
	isValid, errors, err := v.ValidateRecord(recordStruct)
	if err != nil {
		log.Fatalf("Validation failed: %v", err)
	}

	fmt.Printf("Record is valid: %t\n", isValid)
	if len(errors) > 0 {
		fmt.Println("Validation errors:")
		for _, errMsg := range errors {
			fmt.Printf("  - %s\n", errMsg)
		}
	} else {
		fmt.Println("No validation errors found!")
	}

	// Optional: Validate against a specific schema URL
	isValidURL, errorsURL, err := v.ValidateRecord(
		recordStruct,
		validator.WithSchemaURL("https://schema.oasf.outshift.com/schema/0.7.0/objects/record"),
	)
	if err != nil {
		log.Fatalf("URL validation failed: %v", err)
	}

	fmt.Printf("Record is valid (URL schema): %t\n", isValidURL)
	if len(errorsURL) > 0 {
		fmt.Println("URL validation errors:")
		for _, errMsg := range errorsURL {
			fmt.Printf("  - %s\n", errMsg)
		}
	}
}
```
