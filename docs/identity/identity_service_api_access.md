# API Access

!!! info "Endpoints"

      - **REST API Endpoint**: https://api.agent-identity.outshift.com
      - **gRPC API Endpoint**: api.grpc.agent-identity.outshift.com
      - **UI Endpoint**: https://agent-identity.outshift.com

Welcome to the API Access documentation for Agent Identity. This section provides detailed information on how to interact with the Agent Identity API, including authentication, endpoints, and usage examples.

## Organization API Key

The Organization API Key is used to authenticate requests made to the Agent Identity API. This key is essential for accessing protected resources and performing actions on behalf of your organization.

You can obtain your Organization API Key from the Agent Identity settings page. Ensure that you keep this key secure and do not expose it in public repositories or client-side code.

![Organization API Key](../assets/identity/identity_service/tenant-api-key.png)

## Agentic Service API Key

The Agentic Service API Key is used to authenticate requests made by your application to the Agent Identity API. This key is specific to your application and should be included in the headers of your API requests or in the Python SDK configuration.

You can generate an Agentic Service API Key from the Agent Identity settings page. Similar to the Organization API Key, ensure that this key is kept secure and not exposed in public repositories or client-side code.

![Agentic Service API Key](../assets/identity/identity_service/app-api-key.png)

## Protodocs

The Protodocs definitions for the Identity Service API can be accessed [here](https://github.com/agntcy/identity-service/tree/main/docs/protodocs/agntcy/identity/service).

## OpenAPI Client

The OpenAPI Client provides a way to interact with the Agent Identity API using standard HTTP requests. You can use any HTTP client library to make requests to the API endpoints defined in the OpenAPI specification.

The OpenAPI specification for the Agent Identity API can be found [here](./identity_service_api.md).