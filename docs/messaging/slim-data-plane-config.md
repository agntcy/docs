# SLIM Data Plane Configuration Documentation

This document provides comprehensive documentation for configuring the SLIM data plane. The configuration is written in YAML format and defines how the data plane runtime, services, authentication, and observability components operate.

## Configuration Structure Overview

The SLIM configuration file consists of three main sections:

- Observability and logging configuration
  ```yaml
  tracing:
    # ... tracing options
  ```
- Runtime behavior configuration
  ```yaml
  runtime:
    # ... runtime options
  ```
- Services configuration
  ```yaml
  services:
    # ... service configurations
  ```

## Top-Level Configuration Sections

### Tracing Configuration

The `tracing` section configures logging, observability, and OpenTelemetry integration.

#### Basic Tracing Options

```yaml
tracing:
  # Logging level - controls verbosity of log output
  # Available options: trace, debug, info, warn, error
  # Default: info
  log_level: debug

  # Whether to display thread names in log output
  # Default: true
  display_thread_names: true

  # Whether to display thread IDs in log output
  # Default: false
  display_thread_ids: true

  # Additional log filtering (optional)
  # Can be used to filter logs by module or target
  # Default: "info"
  filter: "slim=debug"
```

#### OpenTelemetry Configuration

```yaml
tracing:
  opentelemetry:
    # Enable OpenTelemetry integration for distributed tracing
    # Default: false
    enabled: true

    # Service name for telemetry identification
    # Default: "slim-data-plane"
    service_name: "slim-data-plane"

    # Service version for telemetry
    # Default: "v0.1.0"
    service_version: "v0.2.0"

    # Environment identifier (e.g., prod, staging, dev)
    # Default: "development"
    environment: "production"

    # Metrics collection interval in seconds
    # Default: 30
    metrics_interval_secs: 60

    # gRPC configuration for OpenTelemetry exporter
    grpc:
      endpoint: "http://otel-collector:4317"
      tls:
        insecure: true
```

### Runtime Configuration

The `runtime` section configures the async runtime behavior and resource
allocation.

```yaml
runtime:
  # Number of worker threads for the async runtime
  # 0 = use all available CPU cores
  # Default: 0
  n_cores: 4

  # Thread name prefix for runtime worker threads
  # Default: "slim"
  thread_name: "slim-data-plane"

  # Timeout for graceful shutdown - how long to wait for tasks to complete
  # Format: "<number>s", "<number>ms", "<number>m", "<number>h"
  # Default: "10s"
  drain_timeout: "30s"
```

### Services Configuration

The `services` section defines SLIM service instances and their network configurations. Each service is identified by a unique ID in the format `slim/<instance_number>`.

## Service Configuration

### Basic Service Structure

```yaml
services:
  # Service identifier - format: slim/<instance_number>
  slim/0:
    # Optional node ID override
    # If not specified, uses the service identifier
    node_id: "my-node-01"

    # Data plane API configuration
    dataplane:
      servers: [...] # Server endpoints this instance will listen on
      clients: [...] # Client connections this instance will make

    # Control plane API configuration (optional)
    controller:
      servers: [...] # Control plane server endpoints
      clients: [...] # Control plane client connections
```

## Server Configuration

Servers define endpoints that the SLIM instance will listen on for incoming connections.

### Basic Server Configuration

```yaml
dataplane:
  servers:
    - endpoint: "0.0.0.0:46357"
      tls:
        insecure: false # Default: false
```

### TLS Server Configuration

```yaml
dataplane:
  servers:
    - endpoint: "0.0.0.0:46357"
      tls:
        # TLS configuration
        insecure: false

        # Server certificate and key (required for TLS)
        cert_file: "./certs/server-cert.pem"
        key_file: "./certs/server-key.pem"

        # CA certificate for client verification (mTLS)
        ca_file: "./certs/ca-cert.pem"

        # Alternative: inline PEM content
        # cert_pem: |
        #   -----BEGIN CERTIFICATE-----
        #   ...
        #   -----END CERTIFICATE-----
        # key_pem: |
        #   -----BEGIN PRIVATE KEY-----
        #   ...
        #   -----END PRIVATE KEY-----

        # TLS version constraint
        # Options: "tls1.2", "tls1.3"
        # Default: "tls1.3"
        tls_version: "tls1.3"

        # Certificate auto-reload interval (optional)
        # reload_interval: "1h"

        # Include system CA certificates
        # Default: true
        include_system_ca_certs_pool: false

      # HTTP/2 configuration
      http2_only: true

      # Message size limits (in MiB)
      max_frame_size: 4

      # Connection limits
      max_concurrent_streams: 100
      max_header_list_size: 16384 # 16 KiB

      # Buffer sizes for gRPC server
      # Default: 1048576 (1 MiB) for both
      read_buffer_size: 1048576 # 1 MiB
      write_buffer_size: 1048576 # 1 MiB

      # Connection keepalive settings
      keepalive:
        max_connection_idle: "3600s" # Close idle connections after 1 hour
        max_connection_age: "7200s" # Maximum connection lifetime
        max_connection_age_grace: "300s" # Grace period before force close
        time: "120s" # Keepalive ping interval
        timeout: "20s" # Keepalive ping timeout

      # Arbitrary user-provided metadata (optional)
      # Can contain strings, numbers, lists, or nested objects
      metadata:
        role: "ingress"
        replicas: 3
        environment: "production"
        tags:
          - "dataplane"
          - "grpc"
        config:
          feature_flags:
            enable_tracing: true
```

### Server Authentication

#### Basic Authentication

```yaml
dataplane:
  servers:
    - endpoint: "0.0.0.0:46357"
      auth:
        basic:
          username: "admin"
          password: "secret123"
          # Can use environment variable references
          # password: "${env:ADMIN_PASSWORD}"
```

#### JWT Authentication

```yaml
dataplane:
  servers:
    - endpoint: "0.0.0.0:46357"
      auth:
        jwt:
          # Claims validation
          claims:
            audience: "slim-dataplane"
            issuer: "slim-auth-service"
            subject: "dataplane-access"
            # Custom claims for additional validation
            custom_claims:
              role: "dataplane-user"
              permissions: "read,write"

          # Token validation key configuration
          key:
            # For signature verification (server side)
            decoding:
              algorithm: "ES256" # ECDSA with SHA-256

              # Public key for verification (choose one)
              file: "./keys/jwt-public.pem"
              # OR inline PEM:
              # pem: |
              #   -----BEGIN PUBLIC KEY-----
              #   ...
              #   -----END PUBLIC KEY-----
```

## Client Configuration

Clients define outbound connections that the SLIM instance will establish to other services.

### Basic Client Configuration

```yaml
dataplane:
  clients:
    - endpoint: "http://remote-slim:46357"
      tls:
        insecure: true # No TLS
```

### TLS Client Configuration

```yaml
dataplane:
  clients:
    - endpoint: "http://remote-slim:46357"
      tls:
        insecure: false

        # Server verification
        ca_file: "./certs/ca-cert.pem"

        # Client certificate for mTLS (optional)
        cert_file: "./certs/client-cert.pem"
        key_file: "./certs/client-key.pem"

        # Skip server name verification (insecure)
        # Default: false
        insecure_skip_verify: false

        # TLS version
        tls_version: "tls1.3"

      # Optional origin for client requests
      origin: "https://my-client.example.com"

      # Compression type (not yet implemented)
      # compression: "gzip"

      # Connection timeouts (0s means no timeout)
      # Default: 0s for both
      connect_timeout: "10s"
      request_timeout: "30s"

      # Buffer configuration
      buffer_size: 8192

      # Custom headers
      headers:
        x-client-id: "slim-instance-01"
        x-environment: "production"

      # Rate limiting
      # Format: "<requests>/<duration_in_seconds>"
      rate_limit: "100/60" # 100 requests per minute

      # HTTP Proxy configuration (optional)
      proxy:
        # Proxy server URL
        url: "http://proxy.example.com:8080"

        # Proxy authentication (optional)
        username: "proxy-user"
        password: "${env:PROXY_PASSWORD}"

        # TLS configuration for HTTPS proxies
        tls:
          insecure: false
          ca_file: "./certs/proxy-ca.crt"

        # Additional headers for proxy requests
        headers:
          x-proxy-client: "slim-dataplane"
          user-agent: "slim/1.0"

      # Connection keepalive
      keepalive:
        tcp_keepalive: "60s"
        http2_keepalive: "60s"
        timeout: "10s"
        permit_without_stream: false

      # Arbitrary user-provided metadata (optional)
      metadata:
        client_type: "data-sync"
        priority: "high"
        region: "us-west-2"
```

### Client Authentication

#### HTTP Proxy Configuration

```yaml
dataplane:
  clients:
    - endpoint: "remote-slim:46357"
      # HTTP proxy for corporate environments
      proxy:
        url: "http://corporate-proxy.company.com:8080"
        username: "proxy-user"
        password: "${env:PROXY_PASSWORD}"
        headers:
          x-department: "engineering"
          x-cost-center: "12345"

      # HTTPS proxy with TLS verification
    - endpoint: "external-service:443"
      proxy:
        url: "https://secure-proxy.company.com:8443"
        tls:
          insecure: false
          ca_file: "/etc/ssl/certs/corporate-ca.crt"
        username: "${env:PROXY_USER}"
        password: "${env:PROXY_PASS}"
```

#### Basic Authentication

```yaml
dataplane:
  clients:
    - endpoint: "remote-slim:46357"
      auth:
        basic:
          username: "client-user"
          password: "${env:CLIENT_PASSWORD}"
```

#### JWT Authentication

```yaml
dataplane:
  clients:
    - endpoint: "remote-slim:46357"
      auth:
        jwt:
          # Claims to include in generated tokens
          claims:
            audience: "remote-slim"
            issuer: "local-slim"
            subject: "client-connection"
            custom_claims:
              client_id: "slim-instance-01"

          # Token expiration
          duration: "1h"

          # Signing key configuration
          key:
            encoding:
              algorithm: "HS256" # HMAC with SHA-256

              # Signing key (choose one method)
              file: "./keys/jwt-signing.key"
              # OR for HMAC algorithms, direct secret:
              # pem: "my-secret-key"
```

## Supported JWT Algorithms

### Symmetric Algorithms (HMAC)

- `HS256` - HMAC using SHA-256
- `HS384` - HMAC using SHA-384
- `HS512` - HMAC using SHA-512

### Asymmetric Algorithms (RSA)

- `RS256` - RSA signature with SHA-256
- `RS384` - RSA signature with SHA-384
- `RS512` - RSA signature with SHA-512

### Asymmetric Algorithms (ECDSA)

- `ES256` - ECDSA using P-256 and SHA-256
- `ES384` - ECDSA using P-384 and SHA-384

### EdDSA

- `EdDSA` - EdDSA signature algorithms

## Configuration Value Substitution

SLIM supports dynamic configuration value substitution from multiple sources, allowing you to externalize sensitive data and make configurations more flexible.

### Environment Variable Substitution

Configuration values can reference environment variables using the
`${env:VARIABLE_NAME}` syntax:

```yaml
tracing:
  log_level: "${env:LOG_LEVEL}" # Falls back to default if not set

runtime:
  n_cores: "${env:WORKER_THREADS}"

services:
  slim/0:
    dataplane:
      servers:
        - endpoint: "0.0.0.0:${env:LISTEN_PORT}"
          auth:
            basic:
              username: "${env:AUTH_USERNAME}"
              password: "${env:AUTH_PASSWORD}"
```

### File Content Substitution

Configuration values can also reference file contents using the `${file:PATH}` syntax. This is particularly useful for certificates, keys, and other sensitive content:

```yaml
services:
  slim/0:
    dataplane:
      servers:
        - endpoint: "0.0.0.0:46357"
          tls:
            # Load certificate content from files
            cert_file: "/etc/slim/certs/server.crt"
            key_file: "/etc/slim/certs/server.key"
            ca_file: "/etc/slim/certs/ca.crt"
          auth:
            basic:
              # Load password from a secure file
              password: "${file:/run/secrets/admin_password}"
            jwt:
              key:
                decoding:
                  # Load JWT public key from file
                  file: "/etc/slim/keys/jwt-public.pem"
```

### Substitution Examples

#### Mixed Environment and File Sources

```yaml
tracing:
  log_level: "${env:LOG_LEVEL}"
  opentelemetry:
    service_name: "${env:SERVICE_NAME}"
    grpc:
      endpoint: "${env:OTEL_ENDPOINT}"

services:
  slim/0:
    node_id: "${env:NODE_ID}"
    dataplane:
      servers:
        - endpoint: "0.0.0.0:${env:DATAPLANE_PORT}"
          tls:
            cert_file: "/etc/certs/server.crt"
            key_file: "/etc/certs/server.key"
          auth:
            basic:
              username: "${env:AUTH_USER}"
              password: "${file:/run/secrets/auth_password}"
```

#### Kubernetes Secrets Integration

```yaml
# Perfect for Kubernetes deployments with mounted secrets
services:
  slim/0:
    dataplane:
      servers:
        - endpoint: "0.0.0.0:46357"
          tls:
            # Kubernetes mounted certificate files
            cert_file: "/var/run/secrets/tls/tls.crt"
            key_file: "/var/run/secrets/tls/tls.key"
          auth:
            jwt:
              key:
                decoding:
                  # JWT public key from Kubernetes secret
                  file: "/var/run/secrets/jwt/public.key"
```

#### Docker Secrets Integration

```yaml
# For Docker Swarm or Compose with secrets
services:
  slim/0:
    dataplane:
      servers:
        - endpoint: "0.0.0.0:46357"
          auth:
            basic:
              username: "${env:AUTH_USERNAME}"
              # Docker secret mounted as file
              password: "${file:/run/secrets/db_password}"
```

#### SPIFFE/SPIRE Integration with Sidecar Helper

```yaml
# Perfect for SPIFFE deployments with spiffe-helper sidecar
# The spiffe-helper sidecar automatically rotates certificates
services:
  slim/0:
    dataplane:
      servers:
        - endpoint: "0.0.0.0:46357"
          tls:
            insecure: false
            # Certificates managed by spiffe-helper sidecar
            cert_file: "/var/run/secrets/spiffe/tls.crt"
            key_file: "/var/run/secrets/spiffe/tls.key"
            ca_file: "/var/run/secrets/spiffe/ca-bundle.crt"
          auth:
            jwt:
              claims:
                # Use SPIFFE ID as the subject
                subject: "${env:SPIFFE_ID}"
                audience: "slim-cluster"
              key:
                decoding:
                  algorithm: "RS256"
                  # JWT bundle updated by spiffe-helper
                  file: "/var/run/secrets/spiffe/jwt-bundle.pem"

      clients:
        - endpoint: "${env:PEER_ENDPOINT}"
          tls:
            # Client certificates from spiffe-helper
            cert_file: "/var/run/secrets/spiffe/tls.crt"
            key_file: "/var/run/secrets/spiffe/tls.key"
            ca_file: "/var/run/secrets/spiffe/ca-bundle.crt"
          headers:
            # Include SPIFFE ID in headers for peer identification
            x-spiffe-id: "${env:SPIFFE_ID}"
```

### Substitution Rules and Behavior

1. **Exact Replacement**: The entire configuration value must be a substitution expression

   - ✅ Valid: `password: "${env:PASSWORD}"`
   - ❌ Invalid: `password: "prefix-${env:PASSWORD}-suffix"`

2. **Error Handling**: If a substitution fails (file not found, environment variable not set), configuration loading will fail

3. **File Content**: File substitution reads the entire file content as a string, including newlines

4. **Security**: File paths are relative to the working directory where SLIM starts, or absolute paths

5. **Nested Structures**: Substitution works in arrays and nested objects:

    ```yaml
    services:
      slim/0:
        dataplane:
          clients:
            - endpoint: "${env:PEER1_ENDPOINT}"
              headers:
                authorization: "${file:/etc/slim/tokens/peer1.token}"
            - endpoint: "${env:PEER2_ENDPOINT}"
              headers:
                authorization: "${file:/etc/slim/tokens/peer2.token}"
    ```

## Complete Configuration Examples

### Development Configuration (No Security)

```yaml
# config/development.yaml
tracing:
  log_level: debug
  display_thread_names: true
  display_thread_ids: true

runtime:
  n_cores: 0
  thread_name: "slim-dev"
  drain_timeout: "5s"

services:
  slim/0:
    dataplane:
      servers:
        - endpoint: "0.0.0.0:46357"
          tls:
            insecure: true
      clients: []
```

### Production Configuration with mTLS

```yaml
# config/production.yaml
tracing:
  log_level: info
  display_thread_names: false
  display_thread_ids: false
  opentelemetry:
    enabled: true
    service_name: "slim-dataplane"
    service_version: "v1.0.0"
    environment: "production"

runtime:
  n_cores: 0
  thread_name: "slim-prod"
  drain_timeout: "30s"

services:
  slim/0:
    node_id: "${env:NODE_ID}"
    dataplane:
      servers:
        - endpoint: "0.0.0.0:46357"
          tls:
            insecure: false
            # Use file paths for certificates
            cert_file: "/etc/slim/certs/server.crt"
            key_file: "/etc/slim/certs/server.key"
            ca_file: "/etc/slim/certs/ca.crt"
            tls_version: "tls1.3"
          keepalive:
            max_connection_idle: "1800s"
            time: "300s"
            timeout: "60s"

      clients:
        - endpoint: "peer1.example.com:46357"
          tls:
            insecure: false
            ca_file: "/etc/slim/certs/ca.crt"
            cert_file: "/etc/slim/certs/client.crt"
            key_file: "/etc/slim/certs/client.key"
          connect_timeout: "15s"
          request_timeout: "120s"

    controller:
      servers:
        - endpoint: "0.0.0.0:46358"
          tls:
            insecure: false
            cert_file: "/etc/slim/certs/server.crt"
            key_file: "/etc/slim/certs/server.key"
```

### JWT Authentication Configuration

```yaml
# config/jwt-auth.yaml
tracing:
  log_level: info

runtime:
  n_cores: 4
  thread_name: "slim-jwt"
  drain_timeout: "15s"

services:
  slim/0:
    dataplane:
      servers:
        - endpoint: "0.0.0.0:46357"
          tls:
            insecure: false
            cert_file: "./certs/server.crt"
            key_file: "./certs/server.key"
          auth:
            jwt:
              claims:
                audience: "slim-cluster"
                issuer: "slim-auth"
                subject: "dataplane-access"
              key:
                decoding:
                  algorithm: "ES256"
                  file: "./keys/jwt-public.pem"

      clients:
        - endpoint: "remote.example.com:46357"
          tls:
            ca_file: "./certs/ca.crt"
          auth:
            jwt:
              claims:
                audience: "remote-slim"
                issuer: "local-slim"
              duration: "2h"
              key:
                encoding:
                  algorithm: "ES256"
                  file: "./keys/jwt-private.pem"
```

### Containerized Deployment Configuration

```yaml
# config/container.yaml - Ideal for Kubernetes/Docker deployments
tracing:
  log_level: "${env:LOG_LEVEL}"
  opentelemetry:
    enabled: true
    service_name: "${env:SERVICE_NAME}"
    environment: "${env:ENVIRONMENT}"
    grpc:
      endpoint: "${env:OTEL_COLLECTOR_ENDPOINT}"

runtime:
  n_cores: "${env:WORKER_THREADS}"
  thread_name: "${env:SERVICE_NAME}"
  drain_timeout: "${env:SHUTDOWN_TIMEOUT}"

services:
  slim/0:
    node_id: "${env:POD_NAME}" # Kubernetes pod name
    dataplane:
      servers:
        - endpoint: "0.0.0.0:${env:DATAPLANE_PORT}"
          tls:
            insecure: false
            # Kubernetes TLS secret mounted as files
            cert_file: "/var/run/secrets/kubernetes.io/tls/tls.crt"
            key_file: "/var/run/secrets/kubernetes.io/tls/tls.key"
            ca_file: "/var/run/secrets/kubernetes.io/ca/ca.crt"
          auth:
            jwt:
              claims:
                audience: "${env:JWT_AUDIENCE}"
                issuer: "${env:JWT_ISSUER}"
              key:
                decoding:
                  algorithm: "RS256"
                  # JWT public key from Kubernetes secret
                  file: "/var/run/secrets/jwt/public.key"

      clients:
        - endpoint: "${env:PEER_ENDPOINT}"
          # Corporate proxy configuration
          proxy:
            url: "${env:HTTP_PROXY}"
            username: "${env:PROXY_USER}"
            password: "${env:PROXY_PASSWORD}"

          tls:
            ca_file: "/var/run/secrets/kubernetes.io/ca/ca.crt"
            cert_file: "/var/run/secrets/kubernetes.io/tls/tls.crt"
            key_file: "/var/run/secrets/kubernetes.io/tls/tls.key"
          headers:
            x-service-account: "${file:/var/run/secrets/kubernetes.io/serviceaccount/token}"
            x-cluster-id: "${env:CLUSTER_ID}"

    controller:
      servers:
        - endpoint: "0.0.0.0:${env:CONTROLLER_PORT}"
          tls:
            cert_file: "/var/run/secrets/kubernetes.io/tls/tls.crt"
            key_file: "/var/run/secrets/kubernetes.io/tls/tls.key"
          auth:
            basic:
              username: "${env:CONTROLLER_USER}"
              # Password from Kubernetes secret file
              password: "${file:/var/run/secrets/controller/password}"
```

### SPIFFE/SPIRE Zero Trust Configuration

```yaml
# config/spiffe.yaml - SPIFFE/SPIRE with spiffe-helper sidecar
# This configuration works with spiffe-helper managing certificate rotation
tracing:
  log_level: "${env:LOG_LEVEL}"
  opentelemetry:
    enabled: true
    service_name: "slim-spiffe-${env:SPIFFE_ID}"
    environment: "${env:ENVIRONMENT}"

runtime:
  n_cores: "${env:WORKER_THREADS}"
  thread_name: "slim-spiffe"
  drain_timeout: "30s"

services:
  slim/0:
    # Use SPIFFE ID as node identifier
    node_id: "${env:SPIFFE_ID}"

    dataplane:
      servers:
        - endpoint: "0.0.0.0:${env:DATAPLANE_PORT}"
          tls:
            insecure: false
            # Automatically rotated certificates from spiffe-helper
            cert_file: "/var/run/secrets/spiffe/svid.pem"
            key_file: "/var/run/secrets/spiffe/svid_key.pem"
            ca_file: "/var/run/secrets/spiffe/bundle.pem"

            # Faster rotation to match SPIFFE certificate lifetimes
            reload_interval: "30m"
            tls_version: "tls1.3"

          auth:
            jwt:
              claims:
                # SPIFFE ID-based claims
                audience: "spiffe://trust-domain/slim-cluster"
                issuer: "spiffe://trust-domain/slim-issuer"
                subject: "${env:SPIFFE_ID}"
                custom_claims:
                  spiffe_id: "${env:SPIFFE_ID}"
                  trust_domain: "${env:SPIFFE_TRUST_DOMAIN}"
              key:
                decoding:
                  algorithm: "RS256"
                  # JWT bundle managed by spiffe-helper
                  file: "/var/run/secrets/spiffe/jwt_bundle.pem"

          keepalive:
            # Shorter intervals for dynamic environment
            max_connection_idle: "600s"
            time: "60s"
            timeout: "10s"

      clients:
        - endpoint: "${env:PEER_ENDPOINT}"
          tls:
            insecure: false
            # Same SPIFFE certificates for client authentication
            cert_file: "/var/run/secrets/spiffe/svid.pem"
            key_file: "/var/run/secrets/spiffe/svid_key.pem"
            ca_file: "/var/run/secrets/spiffe/bundle.pem"
            reload_interval: "30m"

          # SPIFFE-specific headers for service mesh integration
          headers:
            x-spiffe-id: "${env:SPIFFE_ID}"
            x-trust-domain: "${env:SPIFFE_TRUST_DOMAIN}"
            x-workload-selector: "${env:WORKLOAD_SELECTOR}"

          connect_timeout: "10s"
          request_timeout: "30s"

          auth:
            jwt:
              claims:
                audience: "${env:PEER_SPIFFE_ID}"
                issuer: "${env:SPIFFE_ID}"
                subject: "${env:SPIFFE_ID}"
              duration: "5m" # Short-lived tokens
              key:
                encoding:
                  algorithm: "RS256"
                  # Private key for JWT signing from spiffe-helper
                  file: "/var/run/secrets/spiffe/jwt_key.pem"

    controller:
      servers:
        - endpoint: "0.0.0.0:${env:CONTROLLER_PORT}"
          tls:
            insecure: false
            cert_file: "/var/run/secrets/spiffe/svid.pem"
            key_file: "/var/run/secrets/spiffe/svid_key.pem"
            ca_file: "/var/run/secrets/spiffe/bundle.pem"
            reload_interval: "30m"

          auth:
            jwt:
              claims:
                audience: "spiffe://trust-domain/slim-controller"
                issuer: "spiffe://trust-domain/slim-issuer"
                subject: "${env:SPIFFE_ID}"
              key:
                decoding:
                  algorithm: "RS256"
                  file: "/var/run/secrets/spiffe/jwt_bundle.pem"
```
