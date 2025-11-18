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
go get github.com/agntcy/oasf-sdk/pkg@latest
```

Deploy the OASF SDK server using the provided Helm chart:

```bash
helm install oasf-sdk ./helm/oasf-sdk
```

Alternatively, you can deploy the OASF SDK server using the provided Docker image:

```bash
docker run -p 31234:31234 ghcr.io/agntcy/oasf-sdk:latest
```

## Usage

The OASF SDK can be used in two ways: 

* As a Go Package you can import and use the packages directly in your Go application.
* As a gRPC Service you can deploy the server and communicate via gRPC.
