# Documentation Repository Internet of Agent

This repository contains the documentation for the project, built using Sphinx
with the Read the Docs template. The documentation sources are written in
Markdown.

## Table of Contents

- [Documentation Repository Internet of Agent](#documentation-repository-internet-of-agent)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [macOS](#macos)
    - [Linux](#linux)
    - [Windows](#windows)
  - [Building the Documentation](#building-the-documentation)
  - [Contributing](#contributing)
- [Copyright Notice](#copyright-notice)

## Installation

To build the documentation locally, you need to install Taskfile.

### macOS

- Install Taskfile using Homebrew:

   ```sh
   brew install go-task/tap/go-task

### Linux

- Install Taskfile using bash:

   ```sh
   sh -c '$(curl -fsSL https://taskfile.dev/install.sh)'

### Windows

- Install Taskfile using scoop:

   ```sh
   scoop install go-task

## Building the Documentation

- To build the documentation, run the following command:

   ```sh
   task build

- This will generate the HTML documentation in the .build/docs/html directory.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

Fork the repository. Create a new branch for your feature or bugfix. Make your
changes. Submit a pull request.

# Copyright Notice

[Copyright Notice and License](./LICENSE.md)

Copyright AGNTCY Contributors (https://github.com/agentcy)