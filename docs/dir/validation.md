# Validation

The Directory enforces validation on all records before accepting them.
Validation is performed using the [OASF SDK](https://github.com/agntcy/oasf-sdk), which requires an OASF schema server URL for validation.

## Required Configuration

**The Directory server requires an OASF schema URL to start.** You must provide a valid OASF schema server URL for validation to work.

### Environment Variable

```bash
DIRECTORY_SERVER_OASF_API_VALIDATION_SCHEMA_URL=https://schema.oasf.outshift.com task server:start
```

### YAML Configuration

```yaml
# server.config.yml
oasf_api_validation:
  schema_url: "https://schema.oasf.outshift.com"
listen_address: "0.0.0.0:8888"
```

## Validation Behavior

The Directory server uses API-based validation against the configured OASF schema server:

- **Validation Method**:
  HTTP requests to the OASF schema server API
- **Errors vs Warnings**:
  Only errors cause validation to fail.
  Warnings are returned but do not affect the validation result.
- **Schema Version Detection**:
  The schema version is automatically detected from each record's `schema_version` field
- **Supported Versions**:
  The OASF SDK decoder supports specific schema versions (currently:
  0.3.1, 0.7.0, 0.8.0).
  Records using unsupported versions will fail validation.
- **Unknown Classes**:
  Classes (modules, skills, domains) not defined in the OASF schema are rejected with an error.
  Records must only use classes that are defined in the configured OASF schema instance.

## OASF Instance Configurations

While there is only one validation method (API validation), you can configure the Directory server to use different OASF instances.
The choice of OASF instance affects which records are accepted and how compatible your directory instance is with other directory instances.

### 1. Official OASF Instance

Using the official OASF instance (`https://schema.oasf.outshift.com`) provides the baseline for the official network.
Records validated here form the most strict, compatible set.

**Network Compatibility:**

- **Can Pull From**:
  Official OASF instance only
- **Can Be Pulled By**:
  Official OASF instance only

**Configuration:**

```yaml
oasf_api_validation:
  schema_url: "https://schema.oasf.outshift.com"
```

### 2. Custom OASF Instance (Additional Taxonomy)

Using a custom OASF instance with extensions that add to the taxonomy (modules, skills, domains - extends but doesn't change or remove).
Records using the extended taxonomy can only be pulled by nodes using the exact same extended taxonomy.

**Network Compatibility:**

- **Can Pull From**:
  Official OASF instance, custom instances with same extended taxonomy
- **Can Be Pulled By**:
  Custom instances with same extended taxonomy only

**Configuration:**

```yaml
oasf_api_validation:
  schema_url: "https://your-custom-oasf-instance.com"
```

### 3. Custom OASF Instance (Changed Taxonomy)

Using a custom OASF instance with extensions that modify the taxonomy (modules, skills, domains - changes or removes from taxonomy).
Completely incompatible with all other options.
Can only work with nodes using the exact same changed taxonomy.

**Network Compatibility:**

- **Can Pull From**:
  Custom instances with same changed taxonomy only
- **Can Be Pulled By**:
  Custom instances with same changed taxonomy only

**Configuration:**

```yaml
oasf_api_validation:
  schema_url: "https://your-custom-oasf-instance.com"
```

## Deploying a Local OASF Instance

You can deploy a local OASF instance alongside the Directory server for testing or development purposes.

### Testing with Local OASF Server

To test with a local OASF instance deployed alongside the directory server:

1. **Enable OASF in Helm values** - Edit `install/charts/dir/values.yaml`:

   ```yaml
   apiserver:
     oasf:
       enabled: true
   ```

2. **Set schema URL to use the deployed OASF instance** - In the same file, set:

   ```yaml
   apiserver:
     config:
       oasf_api_validation:
         schema_url: "http://dir-ingress-controller.dir-server.svc.cluster.local"
   ```

   Replace `dir` with your Helm release name and `dir-server` with your namespace if different.

3. **Deploy**:
   ```bash
   task build
   task deploy:local
   ```

The OASF instance will be deployed as a subchart in the same namespace and automatically configured for multi-version routing via ingress.

### Using a Locally Built OASF Image

If you want to deploy with a locally built OASF image (e.g., containing `0.9.0-dev` schema files), you need to load the image into Kind **before** deploying.
The `task deploy:local` command automatically creates a cluster and loads images, but it doesn't load custom OASF images.
Follow these steps:

1. **Create the Kind cluster first**:

   ```bash
   task deploy:kubernetes:setup-cluster
   ```

   This creates the cluster and loads the Directory server images.

2. **Build and tag your local OASF image**:

   ```bash
   cd /path/to/oasf/server
   docker build -t ghcr.io/agntcy/oasf-server:latest .
   ```

3. **Load the OASF image into Kind**:

   ```bash
   kind load docker-image ghcr.io/agntcy/oasf-server:latest --name agntcy-cluster
   ```

4. **Configure values.yaml** to use the local image:

   ```yaml
   oasf:
     enabled: true
     image:
       repository: ghcr.io/agntcy/oasf-server
       versions:
         - server: latest
           schema: 0.9.0-dev
           default: true
   ```

5. **Deploy with Helm** (don't use `task deploy:local` as it will recreate the cluster):
   ```bash
   helm upgrade --install dir ./install/charts/dir \
     -f ./install/charts/dir/values.yaml \
     -n dir-server --create-namespace
   ```

**Note**:
If you update the local OASF image, reload it into Kind and restart the deployment:

```bash
kind load docker-image ghcr.io/agntcy/oasf-server:latest --name agntcy-cluster
kubectl rollout restart deployment/dir-oasf-0-9-0-dev -n dir-server
```

## Related Documentation

- [OASF Validation Service](../oasf/validation.md) - Detailed validation service documentation
- [Validation Comparison](../oasf/validation-comparison.md) - Comparison between API validator and JSON Schema
- [OASF Extensions](https://github.com/agntcy/oasf/blob/main/CONTRIBUTING.md#oasf-extensions) - Information about creating OASF extensions
