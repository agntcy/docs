# Agent Workflow Server Manager

The workflow server manager (`wfsm`) is a command line tool that streamlines the process of wrapping an agent into a container image, starting the container and exposing the agent functionality through the Agent Connect Protocol (ACP)

The `wfsm` tool takes an [agent manifest](manifest.md) as input and based on it spins up a web server container exposing the agent through ACP through REST api

## Getting started

### Prerequisites

The utility requires docker engine,  `docker` and `docker-compose` to be present on the host 
To make sure the docker setup is correct on the host execute the 
```bash
wfsm check
```
command. In case the command signals error you can pass the `-v` flag to display verbose information about the failure.

## Installation

Download the release version corresponding to the host architecture from the available [release versions](https://github.com/agntcy/workflow-srv-mgr/tags), and unpack it to a folder at your convenience.

## Run 

Execute the unpacked binary - it'll output the usage string with the available flags and options. 

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


## Test the results

The exposed rest endpoints can be accessed with regular tools (curl, postman)

## Examples

Example manifests can be found in the [wfsm tool](https://github.com/agntcy/workflow-srv-mgr/examples) repository.

> Warning!
> paths to the manifests and the paths inside the manifest definitions in the example commands need to be correct on the environment they are executed in!


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




