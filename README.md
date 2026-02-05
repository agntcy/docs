# Documentation Repository for AGNTCY

This repository contains the documentation for the project, built using Material for MkDocs.
The documentation sources are written in Markdown.

## Table of Contents

- [Documentation Repository Internet of Agent](#documentation-repository-internet-of-agent)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [macOS](#macos)
    - [Linux](#linux)
    - [Windows](#windows)
  - [Running local live server](#running-local-live-server)
  - [Building the Documentation](#building-the-documentation)
  - [Contributing](#contributing)
  - [Release guide](#release-guide)
- [Copyright Notice](#copyright-notice)

## Installation

### Prerequisites

To build the documentation locally, you need to install the following dependencies:

- [Taskfile](https://taskfile.dev/)
- [Uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Golang](https://go.dev/doc/devel/release#go1.24.0)

### macOS

- Install Taskfile and uv using Homebrew:

   ```sh
   brew install go-task/tap/go-task
   brew install uv
   ```

### Linux

- Install Taskfile and uv using bash:

   ```sh
   sh -c '$(curl -fsSL https://taskfile.dev/install.sh)'
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### Windows

- Install Taskfile and uv using scoop:

   ```sh
   scoop install go-task
   scoop install main/uv
   ```

## Running local live server

   ```sh
   task run
   ```

## Building the Documentation

To build the documentation, run the following command:

   ```sh
   task build
   ```

This will generate the HTML documentation in the *.build/site* directory.

## Contributing

See the [How to Contribute](/docs/contributing.md) page for more information.

## Release guide

### Prerequisites

Before creating a release, ensure that:

- All necessary features and fixes are merged into the `main` branch.

### Steps

1. Create and annotate the release tag:
   ```sh
   git tag -a v0.2.1 -m "v0.2.1"
   ```
2. Push the tag to trigger the GitHub Action:
   ```sh
   git push origin v0.2.1
   ```
3. Wait for the GitHub Action to complete building the documentation artifacts.
4. Navigate to the [releases page](https://github.com/agntcy/docs/releases) on GitHub.
5. Find the draft release created by the GitHub Action.
6. Select the previous version tag to compare against.
7. Click "Generate release notes" in the draft release.
8. Review the generated release notes.
9. Publish the release.

# Copyright Notice

[Copyright Notice and License](./LICENSE.md)

Copyright AGNTCY Contributors (https://github.com/agntcy)
