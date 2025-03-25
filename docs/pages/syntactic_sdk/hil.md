# Human in the Loop Agent (Coming soon)

In many cases, agentic applications require human input.  

Involving the human requires two things:

* Interrupting a multi-application flow to wait for human input. This is provided by the different frameworks in different ways, but corresponds to pausing the application and resuming it when input is available.
* Engaging with the human to collect the input. This can happen in many ways and each application will have its own preferences.

The Human in the Loop (HIL) Agent is an agent that implements most common methods to engage with humans.

Few examples below:

* Webhook: the agent calls a provided webhook to request for input and receive it through OpenAPI or REST.
* Email engagement: the agent sends an email and offers a web interface to provide input.
* Webex, Slack, or other engagement: the agent uses a messaging paltform to request input. 
