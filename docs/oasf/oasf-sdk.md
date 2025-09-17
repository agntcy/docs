# OASF SDK Translation Service

## Prerequisites

- Translation SDK binary, distributed via [GitHub Releases](https://github.com/agntcy/oasf-sdk/releases)
- Translation SDK docker images, distributed via
  [GitHub Packages](https://github.com/orgs/agntcy/packages?repo_name=oasf-sdk)

Let's start the OASF SDK as a docker container, which will listen for incoming requests on port `31234`:

```bash
docker run -p 31234:31234 ghcr.io/agntcy/oasf-sdk:latest
```

## GitHub Copilot config

Create a GitHub Copilot config from the OASF data model using the `RecordToGHCopilot` RPC method.
You can pipe the output to a file wherever you want to save the config.

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

## A2A Card extraction

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

# Validation Service

The OASF SDK Validation Service validates OASF Records against [JSON Schema v0.7](https://json-schema.org/draft-07).
It supports two validation modes:
- **Embedded schemas** - Uses JSON schemas built into the binary (default)
- **Schema URL** - Fetches and validates against the schema URL from the record

## gRPC API

```bash
cat e2e/fixtures/valid_v0.7.0_record.json | jq '{record: .}' | grpcurl -plaintext -d @ localhost:31234 agntcy.oasfsdk.validation.v1.ValidationService/ValidateRecord
```

## Golang example

```go
package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/protobuf/types/known/structpb"
	
	validationv1 "buf.build/gen/go/agntcy/oasf-sdk/grpc/go/validation/v1/validationv1grpc"
	validationpb "buf.build/gen/go/agntcy/oasf-sdk/protocolbuffers/go/validation/v1"
)

func main() {
	// Connect to the validation service
	conn, err := grpc.NewClient("localhost:31234", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("Failed to connect: %v", err)
	}
	defer conn.Close()

	client := validationv1.NewValidationServiceClient(conn)

	// Sample OASF record to validate
	record := map[string]interface{}{
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

	// Convert to protobuf Struct
	recordStruct, err := structpb.NewStruct(record)
	if err != nil {
		log.Fatalf("Failed to convert record to struct: %v", err)
	}

	// Create validation request
	req := &validationpb.ValidateRecordRequest{
		Record: recordStruct,
		// SchemaUrl: "https://schema.oasf.outshift.com/schema/0.7.0/objects/record", // Optional
	}

	// Call validation service
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	resp, err := client.ValidateRecord(ctx, req)
	if err != nil {
		log.Fatalf("Validation failed: %v", err)
	}

	// Print results
	fmt.Printf("Valid: %t\n", resp.IsValid)
	if len(resp.Errors) > 0 {
		fmt.Printf("Errors:\n")
		for _, err := range resp.Errors {
			fmt.Printf("  - %s\n", err)
		}
	}
}
```

## Python Example

```python
import grpc
import json
from google.protobuf.struct_pb2 import Struct

# Import generated protobuf files (assuming they're generated and in your Python path)
# You'll need to generate these from the .proto files using protoc
import validation_v1_pb2
import validation_v1_pb2_grpc

def validate_record():
    # Sample OASF record to validate
    record_data = {
        "name": "example.org/my-agent",
        "schema_version": "v0.7.0",
        "version": "v1.0.0",
        "description": "An example agent for demonstration",
        "authors": ["Your Name <your.email@example.com>"],
        "created_at": "2025-01-01T00:00:00Z",
        "domains": [
            {
                "id": 101,
                "name": "technology/internet_of_things"
            }
        ],
        "locators": [
            {
                "type": "docker_image",
                "url": "ghcr.io/example/my-agent:latest"
            }
        ],
        "skills": [
            {
                "name": "natural_language_processing/natural_language_understanding",
                "id": 101
            }
        ]
    }

    # Create gRPC channel
    with grpc.insecure_channel('localhost:31234') as channel:
        stub = validation_v1_pb2_grpc.ValidationServiceStub(channel)
        
        # Convert dict to protobuf Struct
        record_struct = Struct()
        record_struct.update(record_data)
        
        # Create validation request
        request = validation_v1_pb2.ValidateRecordRequest(
            record=record_struct
            # schema_url="https://schema.oasf.outshift.com/schema/0.7.0/objects/record"  # Optional
        )
        
        try:
            # Call validation service
            response = stub.ValidateRecord(request)
            
            # Print results
            print(f"Valid: {response.is_valid}")
            if response.errors:
                print("Errors:")
                for error in response.errors:
                    print(f"  - {error}")
            else:
                print("No validation errors found!")
                
        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()}: {e.details()}")

if __name__ == "__main__":
    validate_record()
```

## JavaScript Example

```javascript
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

// Load the protobuf definition
const PROTO_PATH = path.join(__dirname, 'proto/agntcy/oasfsdk/validation/v1/validation_service.proto');

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
    includeDirs: [path.join(__dirname, 'proto')]
});

const validationProto = grpc.loadPackageDefinition(packageDefinition).agntcy.oasfsdk.validation.v1;

async function validateRecord() {
    // Sample OASF record to validate
    const recordData = {
        name: "example.org/my-agent",
        schema_version: "v0.7.0",
        version: "v1.0.0",
        description: "An example agent for demonstration",
        authors: ["Your Name <your.email@example.com>"],
        created_at: "2025-01-01T00:00:00Z",
        domains: [
            {
                id: 101,
                name: "technology/internet_of_things"
            }
        ],
        locators: [
            {
                type: "docker_image",
                url: "ghcr.io/example/my-agent:latest"
            }
        ],
        skills: [
            {
                name: "natural_language_processing/natural_language_understanding",
                id: 101
            }
        ]
    };

    // Create gRPC client
    const client = new validationProto.ValidationService(
        'localhost:31234',
        grpc.credentials.createInsecure()
    );

    // Create validation request
    const request = {
        record: recordData
        // schema_url: "https://schema.oasf.outshift.com/schema/0.7.0/objects/record"  // Optional
    };

    return new Promise((resolve, reject) => {
        client.ValidateRecord(request, (error, response) => {
            if (error) {
                console.error('gRPC error:', error);
                reject(error);
                return;
            }

            // Print results
            console.log(`Valid: ${response.is_valid}`);
            if (response.errors && response.errors.length > 0) {
                console.log('Errors:');
                response.errors.forEach(err => {
                    console.log(`  - ${err}`);
                });
            } else {
                console.log('No validation errors found!');
            }

            resolve(response);
        });
    });
}

// Run the validation
validateRecord()
    .then(() => {
        console.log('Validation completed successfully');
        process.exit(0);
    })
    .catch((error) => {
        console.error('Validation failed:', error);
        process.exit(1);
    });
```