# Workflow Server Manager

The Workflow Server Manager (WFSM) is a command line tool that streamlines the process of wrapping an agent into a container image, starting the container, and exposing the agent functionality through the Agent Connect Protocol (ACP).

The WFSM tool takes an [Agent Manifest](manifest.md) as input and based on it spins up a web server container exposing the agent through ACP through REST api.

## Getting Started

## Installation

Download and unpack the executable binary from the [releases page](https://github.com/agntcy/workflow-srv-mgr/releases)

Alternatively you can execute the installer script by running the following command:
```bash
curl -L https://raw.githubusercontent.com/agntcy/workflow-srv-mgr/refs/heads/main/install.sh | bash
```
The installer script will download the latest release and unpack it into the `bin` folder in the current directory.
The output of the execution looks like this:

```bash
 curl -L https://raw.githubusercontent.com/agntcy/workflow-srv-mgr/refs/heads/install/install.sh | bash                                                           [16:05:58]
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1034  100  1034    0     0   2597      0 --:--:-- --:--:-- --:--:--  2597
Installing the Workflow Server Manager tool:

OS: darwin
ARCH: arm64
AG: 0.0.1-dev.23
TARGET: /Users/johndoe/.wfsm/bin
ARCHIVE_URL: https://github.com/agntcy/workflow-srv-mgr/releases/download/v0.0.1-dev.23/wfsm0.0.1-dev.23_darwin_arm64.tar.gz


Installation complete. The 'wfsm' binary is located at /Users/johndoe/.wfsm/bin/wfsm
```

Listed variables can be overridden by providing the values as variables to the script

### Prerequisites

The utility requires Docker engine, `docker`, and `docker-compose` to be present on the host.

To make sure the docker setup is correct on the host, execute the following:

```bash
wfsm check
```

In case the command signals error you can pass the `-v` flag to display verbose information about the failure.


## Run deploy

Using `wfsm deploy` command agents can be deployed on two platforms: `docker` & `k8s` using `--platform` option.
(Default platform is `docker`).
By default this command runs with `--dryRun` and only generates deployment artifacts (docker-compose.yaml or helm chart) which will be saved in `~/.wfsm` folder. 
Running with `dryRun=false` will result in deploying either a Docker compose file or a Helm chart. (See details in below sections)
The only mandatory parameter is `--manifestPath` which describes agent specification and should contain a valid deployment option. See [Manifest Spec](https://github.com/agntcy/workflow-srv-mgr/blob/main/wfsm/spec/manifest.yaml), example manifests can be found in the [WFSM Tool](https://github.com/agntcy/workflow-srv-mgr/tree/main/examples) repository.
In case of `source_code` deployment options first a Docker image is built in local repository, with a checksum tag generated from source code.

Should there be multiple deployment options users have to set the selected one with `--deploymentOption`.

```bash
wfsm deploy -m examples/langgraph_manifest.json --deploymentOption=src
```

Should an agent have dependencies on other agents, they are handled the same way as the main agent, images are built and then deployed with the same Docker compose or Helm chart, so that will see each other. 
Agent IDs, API keys and agent endpoints are automatically injected in calling agent so that they can reach dependent agents using ACP-SDK.

## Configuration

Environment variables for an agent(s) can be provided in the: 

  - agent manifest *dependencies* definition (see agent manifest)
  - local environment from where `wfsm` is launched
  - env file provided as an option: `wfsm deploy ... --envFilePath=my_env_file`
  - in `wfsm` specific config yaml: `wfsm deploy ... --configPath=my_config.yaml`

Env vars are applied in the below order, meaning that bottom ones override :

 - all env vars from agents manifest(s) `dependencies` section 
 - all *declared* env vars from local env
 - all *prefixed* env vars from local env
 - all *declared* env vars from env file (--envFilePath)
 - all *prefixed* env vars from env file (--envFilePath)
 - env vars from config.yaml (--configPath)
 - defaults defined in manifest `env_vars` section in case values is empty

  *declared env vars* - env vars defined in manifest `env_vars` section:

```yaml
    "env_vars": [
      {
        "desc": "Environment variable for agentA",
        "name": "AZURE_OPENAI_MODEL",
        "required": true,
        "defaultValue": "gpt-4o-mini"        
      },
      ...
    ]  
```

  *prefixed env vars* - env vars prefixed with agent name (or agent deployment name), where there prefix is created upon following rule:
  
    - all letter converted to capital
    - all special character replaced with '_'

       
### Example of configuring environment variables for agents

Let's say you want to set `AZURE_OPENAI_API_KEY` for `mailcomposer` and it's dependency `email_reviewer_1` (deployment name).
Declare `AZURE_OPENAI_API_KEY` env var both for `mailcomposer` and `email_reviewer_1` in their manifest:

```yaml
    "env_vars": [
      {
        "desc": "Environment variable for agentA",
        "name": "AZURE_OPENAI_MODEL",
        "required": true,
        "defaultValue": "gpt-4o-mini"        
      },
      ...
    ]  
```

Example manifests can be found here: [mailcomposer](https://github.com/agntcy/workflow-srv-mgr/blob/main/examples/manifest_with_deps.json) manifest [email_reviewer_1](https://github.com/agntcy/workflow-srv-mgr/blob/main/examples/llama_manifest.json) manifest.

You can run `export AZURE_OPENAI_API_KEY=xxx` in your local shell from where you launch `wfsm` and the env var will be set for both agents.

If you want to set a different key for `email_reviewer_1` then you have to prefix you env var: `AGENT_B_AZURE_OPENAI_API_KEY`.

Same rule applies for env vars declared in a usual env file which you can provide with `--envFilePath=your_env_file` option.

```yaml
# applies to all agents decaling these env vars in their manifest
AZURE_OPENAI_API_KEY="xxxxxxx"

# only apllies to mailcomposer agent
MAILCOMPOSER_AZURE_OPENAI_API_KEY="xxxxxxx"

# only apllies to email_reviewer_1 agent
EMAIL_REVIEWER_1_AZURE_OPENAI_API_KEY="xxxxxxx"
```

These above will override local env values.

Finally you can declare env vars in `config.yaml` (eg. --configPath=config.yaml) like below that will override previous settings:

```yaml
config:
  agent_A:
    envVars:
      "AZURE_OPENAI_API_KEY": "from_config"
  agent_B:
    envVars:
      "AZURE_OPENAI_API_KEY": "from_config"  
```

### Configuration of agent ID, API key, external port

Agent ID's, API keys and external port for main agent are generated/set by `wfsm`.
You can use `--showConfig` option to display the default configuration generated by the tool:

```sh
wfsm deploy --manifestPath example_manifest.yaml --showConfig
```

You can use the default config as a base for you own config, or you can just add additional things you want to override.

```yaml
cat > config.yaml <<EOF
config:
  email_reviewer_1:
    apiKey: ef570bea-1c99-4ff6-8bb1-ac2cf789183f
    id: 7f6b6820-6142-4a0e-976e-c1197a9d9b2c
    port: 9999
  ...
  mailcomposer:
    apiKey: 42787d0d-b5c2-4f80-ad59-1b7bb97e7ca7
    id: 20a82791-0179-4b52-8fe1-4f7dbf688bb4
    port: 9998
EOF

wfsm deploy --manifestPath example_manifest.yaml --showConfig --configPath=config.yaml
```

In case of the above example using `--showConfig` option with a user provided config, you will see a merged config of defaults and user provided values.

By default, if no ports are specified only the main agent will be exposed on the next available local port.
(For k8s see next section.)

Alternatively you can also set these with prefixed env vars:

```sh
MAILCOMPOSER_API_KEY=ef570bea-1c99-4ff6-8bb1-ac2cf789183f
MAILCOMPOSER_ID=20a82791-0179-4b52-8fe1-4f7dbf688bb4
MAILCOMPOSER_PORT=9999

EMAIL_REVIEWER_1_API_KEY=42787d0d-b5c2-4f80-ad59-1b7bb97e7ca7
EMAIL_REVIEWER_1_ID=7f6b6820-6142-4a0e-976e-c1197a9d9b2c
EMAIL_REVIEWER_1_PORT=9998
```

## Configuring deployment to Kubernetes

Deploying agents to Kubernetes is pretty much the same as to Docker you only have to specify `--platform=k8s` or `-p k8s`.
`wfsm` tool will generate a helm chart and values.yaml for each main agent and it's dependencies in `~/.wfsm/<main_agent_name>` folder.
Using `-v` / `--verbose` option you can actually see the generated values file.
For each agent will be deployed a `ConfigMap`, `Secret` (containing env var configs) a `Service` and a `Statefulset`.

Additional k8s specific configs - beside id's & api keys, env vars - can be specified under `k8s` field in the config file.
A full example of config possibilities can be found [here](https://github.com/agntcy/workflow-srv-mgr/blob/main/examples/k8s_example_config.yaml).

```sh
 wfsm deploy -m manifest_with_deps.json --configPath=k8s_example_config.yaml -p k8s --showConfig  
```

In case you run with `--dryRun=false` and you have an active K8s context configured (you can also provide you kube config file directly in `KUBECONFIG` env var) the tool will try to deploy the helm chart to that cluster.

By default, the main agent service type is configured to `NodePort` so that the main agent will be reachable on a local cluster.

You can specify a different namespace using `WFSM_K8S_NAMESPACE` env var.

## Test the Results

The exposed REST endpoints can be accessed with regular tools (for example, Curl or Postman).

## Examples

Example manifests can be found in the [WFSM Tool](https://github.com/agntcy/workflow-srv-mgr/tree/main/examples) repository.

### Expose the [Mail Composer](https://github.com/agntcy/agentic-apps/tree/main/mailcomposer) LangGraph agent through ACP workflow server 

```bash
wfsm deploy -m examples/langgraph_manifest.json -e examples/env_vars
```

### Expose the [Email Reviewer](https://github.com/agntcy/agentic-apps/tree/main/email_reviewer) llama deploy workflow agent through ACP workflow server 

```bash
wfsm deploy -m examples/llama_manifest.json -e examples/env_vars
```

### Expose an agent with dependencies through the ACP workflow server

```bash
wfsm deploy -m examples/manifest_with_deps.json -e examples/env_vars_with_deps
```

### Run agent from docker image

Run deploy to build images.

```bash
wfsm deploy -m examples/langgraph_manifest.json -e examples/env_vars
```

Get the image tag from console athset in the manifest.

```
    "deployment_options": [

      {
        "type": "docker",
        "name": "docker",
        "image": "agntcy/wfsm-mailcomposer:<YOUR_TAG>"
      }
      ...       
    ]
```    

Run `wfsm` again now with `--deploymentOption=docker --dryRun=false`:


```bash
wfsm deploy -m examples/langgraph_manifest.json -e examples/env_vars --deploymentOption=docker --dryRun=false
```