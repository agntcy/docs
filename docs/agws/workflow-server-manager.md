# Workflow Server Manager

The Workflow Server Manager (WFSM) is a command line tool that streamlines the process of wrapping an agent into a container image, starting the container, and exposing the agent functionality through the Agent Connect Protocol (ACP).

The WFSM tool takes an [Agent Manifest](../manifest/manifest.md) as input and based on it spins up a web server container exposing the agent through ACP through REST api.

## Getting Started

### Prerequisites

The utility requires Docker engine, `docker`, and `docker-compose` to be present on the host.

To make sure the docker setup is correct on the host, execute the following:

```bash
wfsm check
```

In case the command signals error you can pass the `-v` flag to display verbose information about the failure.

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


## Run

Execute the unpacked binary. This outputs the usage string with the available flags and options.

```bash

$ wfsm

ACP Workflow Server Manager Tool

Wraps an agent into a web server and exposes the agent functionality through ACP.
It also provides commands for managing existing deployments and cleanup tasks

Usage:
  wfsm [command]

Available Commands:
  check       Checks the prerequisites for the command
  completion  Generate the autocompletion script for the specified shell
  deploy      Build an ACP agent
  help        Help about any command
  list        List an ACP agents running in the deployment
  logs        Show logs of an ACP agent deployment(s)
  stop        Stop an ACP agent deployment

Flags:
  -h, --help      help for wfsm
  -v, --version   version for wfsm

Use "wfsm [command] --help" for more information about a command.

```

## Test the Results

The exposed REST endpoints can be accessed with regular tools (for example, Curl or Postman).

## Examples

Example manifests can be found in the [WFSM Tool](https://github.com/agntcy/workflow-srv-mgr/tree/main/examples) repository.

> Note:
> Paths to the manifests and the paths inside the manifest definitions in the example commands need to be correct on the environment they are executed in!


### Expose the [Mail Composer](https://github.com/agntcy/acp-sdk/tree/main/examples/mailcomposer) LangGraph agent through ACP workflow server

```bash
wfsm deploy -m examples/langgraph_manifest.json -e examples/env_vars.yaml
```

### Expose the [Email Reviewer](https://github.com/agntcy/acp-sdk/tree/main/examples/email_reviewer) llama deploy workflow agent through ACP workflow server

```bash
wfsm deploy -m examples/llama_manifest.json -e examples/env_vars.yaml
```

### Expose an agent with dependencies through the ACP workflow server

```bash
wfsm deploy -m examples/manifest_with_deps.json -e examples/env_vars_with_deps.yaml
```


>Make sure the url to the manifest of the dependent agent is either an absolute path or a relative path to the directory you are running `wfsm` tool.

### Run agent from docker image

Run deploy with `--dryRun` to build images.

```bash
wfsm deploy -m examples/langgraph_manifest.json -e examples/env_vars.yaml --dryRun
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

Run `wfsm` again now with `--deploymentOption=docker`:


```bash
wfsm deploy -m examples/langgraph_manifest.json -e examples/env_vars.yaml --deploymentOption=docker
```