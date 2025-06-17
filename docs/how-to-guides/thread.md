Building Applications with ACP Threads
======================================

ACP Node supports threads, where a thread contains the accumulated state of a sequence of runs.

In this tutorial, we will explore how to create a LangGraph agent with threads, wrap it in an ACP node, and leverage the various functionalities that come with using threads.

Learning Objectives
-------------------

In this short tutorial you will learn:

  * How to create a manifest for a LangGraph agent from code
  * Deploy the agent with Workflow Server
  * Use thread endpoints effectively

Prerequisites
------------------

  * poetry
  * python version <4.0,>=3.9
  * `Workflow server manager <https://docs.agntcy.org/pages/agws/workflow_server_manager.html#installation>`_
  * An Editor of your choice


Implementation Walkthrough
----------------------------

Together we will, create a LangGraph agent, deploy it on a Workflow Server, and utilize its threading capabilities. You can find the agent's source code here: `Mail Composer Agent Source Code <https://github.com/agntcy/agentic-apps/blob/main/mailcomposer/mailcomposer/mailcomposer.py>`_.
The agent we will work with is called **Mail Composer**, which specializes in composing emails for marketing campaigns.

Setup
^^^^^

Create a new poetry project
++++++++++++++++++++++++++++

.. code-block:: console

   poetry new agent_with_thread


.. note::

    As of this writing, `angtcy_acp` only supports Python versions specified as `requires-python = "<4.0,>=3.10.0"`. Therefore, before proceeding to the next step, ensure you edit the `pyproject.toml` file and set the `requires-python` variable to:

.. code-block:: console

   requires-python = "<4.0,>=3.10.0"

Install dependencies
++++++++++++++++++++

.. code-block:: console

   poetry add langgraph langchain langchain-openai pydantic agntcy_acp

Within the `src/agent_with_thread` directory, create two new files: the first named `agent.py` and the second named `state.py`.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: console

   cd src/agent_with_thread && touch agent.py  && touch state.py


Copy and Paste `this code <https://github.com/agntcy/agentic-apps/blob/main/mailcomposer/mailcomposer/mailcomposer.py>`_ in the agent.py file

Change the following lines:

From

.. code:: python
    if is_stateless:
        print("mailcomposer - running in stateless mode")
        graph = graph_builder.compile()
    else:
        print("mailcomposer - running in stateful mode")
        checkpointer = InMemorySaver()
        graph = graph_builder.compile(checkpointer=checkpointer)

To

.. code:: python

    checkpointer = InMemorySaver()
    graph = graph_builder.compile(checkpointer=checkpointer)


Copy and Paste `this code <https://github.com/agntcy/agentic-apps/blob/main/mailcomposer/mailcomposer/state.py>`_ in the state.py file

.. note::

    The creation of a LangGraph agent is outside the scope of this guide. If you're unfamiliar with how to create one, refer to this tutorial provided by the LangGraph team: `LangGraph Agent Tutorial <https://langchain-ai.github.io/langgraph/agents/agents/#1-install-dependencies>`_.


Define agent manifest
^^^^^^^^^^^^^^^^^^^^^

1. At the same level as the `src` file, create a new directory named `deploy` and inside src/agent_with_thread create a new Python file called `generate_manifest.py`.

.. code-block:: console

   mkdir ../../deploy && touch generate_manifest.py


2. In the `generate_manifest.py` file, import all the necessary libraries.

   .. code-block:: python

      from pathlib import Path
      from pydantic import AnyUrl
      from state import AgentState, OutputState, ConfigSchema
      from agntcy_acp.manifest import (
          AgentManifest,
          AgentDeployment,
          DeploymentOptions,
          LangGraphConfig,
          EnvVar,
          AgentMetadata,
          AgentACPSpec,
          AgentRef,
          Capabilities,
          SourceCodeDeployment,
      )


3. Define the agent manifest, in code.

  .. code-block:: python
     :emphasize-lines: 10,16

      manifest = AgentManifest(
        metadata=AgentMetadata(
            ref=AgentRef(name="org.agntcy.agent_with_thread", version="0.0.1", url=None),
            description="Offer a chat interface to compose an email for a marketing campaign. Final output is the email that could be used for the campaign"),
        specs=AgentACPSpec(
            input=AgentState.model_json_schema(),
            output=OutputState.model_json_schema(),
            config=ConfigSchema.model_json_schema(),
            capabilities=Capabilities(
                threads=True,
                callbacks=False,
                interrupts=False,
                streaming=None
            ),
            custom_streaming_update=None,
            thread_state=AgentState.model_json_schema(),
            interrupts=None
            ),
        deployment=AgentDeployment(
            deployment_options=[
                DeploymentOptions(
                    root = SourceCodeDeployment(
                        type="source_code",
                        name="source_code_local",
                        url=AnyUrl("file://../"),
                        framework_config=LangGraphConfig(
                            framework_type="langgraph", # or "llamaindex" if yout agent is written with that particular framework,
                            graph="agent_with_thread.agent:graph" # if a llamaindex agent than the key for the entrypoint is path
                        )
                    )
                )
            ],
            env_vars=[
                EnvVar(name="AZURE_OPENAI_API_KEY", desc="Azure key for the OpenAI service"),
                EnvVar(name="AZURE_OPENAI_ENDPOINT", desc="Azure endpoint for the OpenAI service")
            ],
            dependencies=[]
          )
      )

      #Write the result in a json file

      with open(f"{Path(__file__).parent}/../../deploy/manifest.json", "w") as f:
          f.write(manifest.model_dump_json(
              exclude_unset=True,
              exclude_none=True,
              indent=2
          ))

  .. note::

    You might have some indentation problems if you copy and paste the above code, make sure to fix them before you proceed.

With the above code we've defined the manifest for our agent and in it we set threads with as one of it capabilities, and for that reason we also had to define the thread_state, so that the workflow server knows the model for the threads. For more detail about the manifest `here <https://docs.agntcy.org/pages/agws/manifest.html>`_.

Now you should be able to generate the agent manifest by running

  .. code-block:: console

      poetry run python generate_manifest.py

Confirm that there is file called manifest.json inside deploy folder.


Run and test the Agent
^^^^^^^^^^^^^^^^^^^^^^

1. Create the agent configuration file

   First you need to create a configuration file that will hold the environment variables needed by the agent. To know more about the structure of this file go `here <https://docs.agntcy.org/pages/agws/workflow_server_manager.html#configuration>`_.

   Go to deploy folder previously created and create a file called config.yaml.

    .. code-block:: console

        cd ../../deploy && touch config.yaml

  Paste the code bellow, inside config.yaml and replace the environment variables accordingly.

    .. code-block:: yaml

        config:
            org.agntcy.agent_with_thread:
                port: 52393
                apiKey: 799cccc7-49e4-420a-b0a8-e4de949ae673
                id: 45fb3f84-c0d7-41fb-bae3-363ca8f8092a
                envVars:
                  AZURE_OPENAI_API_KEY: [YOUR AZURE OPEN API KEY]
                  AZURE_OPENAI_ENDPOINT: https://[YOUR ENDPOINT].openai.azure.com


2. Deploy the agent using the Workflow Server (`Workflow Server Repository <https://github.com/agntcy/workflow-srv>`_) and the Workflow Server Manager (`Workflow Server Manager Repository <https://github.com/agntcy/workflow-srv-mgr>`_).

   From the root of this project run:

    .. code-block:: console

       wfsm deploy -m deploy/manifest.json -c deploy/config.yaml --dryRun=false

3. Test your Agent

Create a new thread
++++++++++++++++++++

.. code-block:: console

    curl -X 'POST' \
      'http://127.0.0.1:52393/threads' \
      -H 'accept: application/json' \
      -H 'x-api-key: 799cccc7-49e4-420a-b0a8-e4de949ae673' \
      -H 'Content-Type: application/json' \
      -d '{
      "thread_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "metadata": {},
      "if_exists": "raise"
    }'


Run the thread
+++++++++++++++

.. code-block:: console

    curl -X 'POST' \
      'http://127.0.0.1:52393/threads/3fa85f64-5717-4562-b3fc-2c963f66afa6/runs/wait' \
      -H 'accept: application/json' \
      -H 'x-api-key: 799cccc7-49e4-420a-b0a8-e4de949ae673' \
      -H 'Content-Type: application/json' \
      -d '{
      "agent_id": "45fb3f84-c0d7-41fb-bae3-363ca8f8092a",
      "input": {
        "is_completed": null,
        "messages": [{"type": "human", "content": "Email about wooden spoon be inventive on regarding email body"}]
      },
      "metadata": {},
      "config": {
        "tags": [
          "string"
        ],
        "recursion_limit": 10,
        "configurable": {
          "test": true,
          "thread_id":"3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }
      },
      "stream_mode": null,
      "on_disconnect": "cancel",
      "multitask_strategy": "reject",
      "after_seconds": 0,
      "stream_subgraphs": false,
      "if_not_exists": "reject"
    }'


Get the state
++++++++++++++

.. code-block:: console

    curl -X 'GET' \
      'http://127.0.0.1:53032/threads/3fa85f64-5717-4562-b3fc-2c963f66afa6' \
      -H 'accept: application/json' \
      -H 'x-api-key: 8280bb5a-ced8-44d6-bb38-71a69ba2cb31'

This will return a the current state of the thread in the format specified in the manifest.

Get the state history
+++++++++++++++++++++

.. code-block:: console

    curl -X 'GET' \
      'http://127.0.0.1:52393/threads/3fa85f64-5717-4562-b3fc-2c963f66afa6' \
      -H 'accept: application/json' \
      -H 'x-api-key: 799cccc7-49e4-420a-b0a8-e4de949ae673'

This will return a the entire state for every run of the given thread_id.

Final Words
++++++++++++

Do not stop here check our open api documentation and try out the more `endpoints <https://spec.acp.agntcy.org/#tag/threads>`_.

Thank you for reading