# Multi-Agent Application Composer 

The **Multi-Agent Application Composer** is an agent on its own right meant to automatically compose a Multi-Agent Application starting from user intent.

The composer uses one or more LLMs is able to:
* Interpret a developer intent and the goal of the application they want to build. This could be an iterative process based on a conversation.
* Decompose the user ask into fundamental tasks assignable to agents.
* Search an agent directory to identify suitable agents.
* Assemble agents, potentially invoking them through the Agent Connect Protocol, IO mappers, Semantic  Router Agents, and API Bridge agents into a workflow to accomplish the intended goal.
* Allow the user to review, refine and approve.

The workflow is described in an abstract form, for example using a json data structure.

A compiler is in charge of transforming the abstract description produced by the composer into runnable code, using one of the supported frameworks, and when needed leveraging the Agent Connect Protocol to invoke remote agents. 