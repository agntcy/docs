#### Agent Deployments
Agent Deployments section lists all the possible ways the agent can be consumed, which we call deployment modes.

Agent Manifest currently supports three deployment modes:
* Source Code Deployment: In this case the agent can be deployed starting from its code. For this deployment mode, the manifest provides:
    * The location where the code is available
    * The framework used for this agent
    * The framework specific configuration needed to run the agent.
* Remote Service Deployment: In this case, the agent does not come as a deployable artefact, but it's already deployed and available as a service. For this deployment mode, the manifest provides:
    * The network endpoint where the agent is available through the ACP
    * The authentication used by ACP for this agent
* Docker Deployment: In this case the agent can be deployed starting from a docker image. It is assumed that once running the docker container expose the agent through ACP. For this deployment mode, the manifest provides:
    * The agent container image
    * The authentication used by ACP for this agent

<details>
<summary> Sample manifest dependency section for the mailcomposer agent</summary>

```json
{
  ...
    "deployments": [
      {
        "type": "source_code",
        "name": "src",
        "url": "git@github.com:agntcy/mailcomposer.git",
        "framework_config": {
          "framework_type": "langgraph",
          "graph": "mailcomposer"
        }
      }
    ]
  ...
}
```


Mailcomposer agent in the example above comes as code written for langraph and available on github.

#### Agent Dependencies

Agent Dependencies section lists all the other agents this agent depends on. We refer to them as `sub-agents`.

Sub-agents are represented as references to other manifests.
This information is needed when the manifest is used for agent deployment to make sure that sub-agents are available or to deploy them if needed.

<details>
<summary> Sample manifest dependency section for the mailcomposer agent</summary>

```json
{
  ...
    "dependencies": [
      {
        "name": "org.agntcy.sample-agent-2",
        "version": "0.0.1"
      },
      {
        "name": "org.agntcy.sample-agent-3",
        "version": "0.0.1"
      }
    ]
  ...
}
```

Mailcomposer agent in the example above depends on `sample-agent-2` and `sample-agent-3`.

</details>