# Agent Manifest

An Agent Manifest is a document that describes in detail the following:

* What the agent is capable of.
* How the agent can be consumed if provided as-a-service.
* How the agent can be deployed if provided as a deployable artifact.
* What are the dependencies of the agent, that is, which other agents it relies on.

The manifest is designed to be used by [Agent Connect Protocol](../syntactic_sdk/connect.md) and the [Agent Workflow Server](../agws/workflow-server.md) and stored in the [Agent Directory](../dir/overview.md) with the corresponding OASF extensions.

This document describes the principles of the Agent Manifest definition. Manifest definition can be found [here](https://github.com/agntcy/workflow-srv-mgr/blob/main/wfsm/spec/manifest.json)

Sample manifests can be found [here](https://github.com/agntcy/workflow-srv-mgr/tree/main/wfsm/spec/examples).
