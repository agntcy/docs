# Workflow Server Manager

The workflow server manager (wfsm) is a command line tool that streamlines the process of wrapping an agent into a container image, starting the container and exposing the agent functionality through the Agent Connect Protocol (ACP)

The `wfsm` tool takes an [agent manifest](manifest.md) as input and based on it spins up a web server container exposing the agent through ACP through REST api

## Getting started

### Prerequisites

The utility requires docker engine,  `docker` and `docker-compose` to be present on the host 

## Installation

Download the release version corresponding to the host architecture from the available [release versions](https://github.com/agntcy/workflow-srv-mgr/tags), and unpack it to a folder at your convenience.

## Run 

Execute the unpacked binary - it'll output the usage string with the available flags and options. 

```bash
./build/wfsm

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

Flags:
  -h, --help      help for wfsm
  -v, --version   version for wfsm

Use "wfsm [command] --help" for more information about a command.
```


## Test the results

The exposed rest endpoints can be accessed with regular tools (curl, postman)

