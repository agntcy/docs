# Extensions

Extensions provide additional descriptors to the AI agent data model with the goal to:

- Enrich the data model generically based on given requirements
- Provide a way for the community to extend the data model schema
- Enable data model consumers/services to provide custom functionalities

Each extension is described using its `name` and its respective `version` fields, with FQDN specified using `{name}/{version}` value.
These values can be used by content consumers to identify specific extensions in order to perform custom operations.

## Usage

Extensions define custom descriptors added to the agent data model to support custom behaviour,
both for the data layer and application layer purposes.
Consider two scenarios where extensions are added to the agent data model depending on their respective use-case:

```{image} ../_static/data_extension_usage.png
:alt: Data Layer Extension Usage
:width: 90%
:align: center
```
<br>

- **Serving Data Layer** can be done by adding extensions to further describe the agent without an application-specific purpose.
For example, this could be an extension that adds a link to a contact form which is only visible when pulling and working with the given agent.

```{image} ../_static/application_extension_usage.png
:alt: Application Layer Extension Usage
:width: 80%
:align: center
```
<br>

- **Serving Application Layer** can be done by adding extensions that are required by specific applications.
For example, this could be an extension that adds categorisation details to describe agents capabilities.
Application such as search can then rely on this data for indexing and serving.
