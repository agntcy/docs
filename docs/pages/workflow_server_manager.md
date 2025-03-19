# Workflow Server Manager

The workflow server manager (wfsm) is a command line tool that streamlines the process of wrapping an agent into a container image, starting the container and exposing the agent functionality through the Agent Connect Protocol (ACP)

The `wfsm` tool takes an agent manifest as input and based on it starts a web server container exposing the agent through ACP through REST api

## Getting started

### Prerequisites

The utility requires docker engine,  `docker` and `docker-compose` to be present on the host 

## Installation

Download the release version corresponding to the host architecture from GitHub, and unpack it to a folder at your convenience.

## Run 

Execute the unpacked binary -it'll output the usage string with the available flags and options. 
