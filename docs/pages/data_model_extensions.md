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

## Examples

[comment]: <BASE EXTENSION>

```{include} ../../phoenix-directory/cli/builder/extensions/base/README.md
```

```{tab} base.spec.json
```{literalinclude} ../../phoenix-directory/cli/builder/extensions/base/spec.json
:language: json
```

```{tab} base.example.json
```{literalinclude} ../../phoenix-directory/cli/builder/extensions/base/example.json
:language: json
```

[comment]: <RUNTIME EXTENSION>

```{include} ../../phoenix-directory/registryold/client/builder/extensions/runtime/README.md
```

```{tab} runtime.spec.json
```{literalinclude} ../../phoenix-directory/registryold/client/builder/extensions/runtime/spec.json
:language: json
```

```{tab} runtime.example.json
```{literalinclude} ../../phoenix-directory/registryold/client/builder/extensions/runtime/example.json
:language: json
```

[comment]: <LLM ANALYZER EXTENSION>

```{include} ../../phoenix-directory/registryold/client/builder/extensions/llmanalyzer/README.md
```

```{tab} llmanalyzer.spec.json
```{literalinclude} ../../phoenix-directory/registryold/client/builder/extensions/llmanalyzer/spec.json
:language: json
```

```{tab} llmanalyzer.example.json
```{literalinclude} ../../phoenix-directory/registryold/client/builder/extensions/llmanalyzer/example.json
:language: json
```

[comment]: <CREWAI EXTENSION>

```{include} ../../phoenix-directory/registryold/client/builder/extensions/crewai/README.md
```

```{tab} crewai.spec.json
```{literalinclude} ../../phoenix-directory/registryold/client/builder/extensions/crewai/spec.json
:language: json
```

```{tab} crewai.example.json
```{literalinclude} ../../phoenix-directory/registryold/client/builder/extensions/crewai/example.json
:language: json
```

[comment]: <SECURITY EXTENSION>

```{include} ../../phoenix-directory/registryold/client/builder/extensions/security/README.md
```

```{tab} security.spec.json
```{literalinclude} ../../phoenix-directory/registryold/client/builder/extensions/security/spec.json
:language: json
```

```{tab} security.example.json
```{literalinclude} ../../phoenix-directory/registryold/client/builder/extensions/security/example.json
:language: json
```

[comment]: <CATEGORY EXTENSION>

```{include} ../../phoenix-directory/registryold/client/builder/extensions/category/README.md
```

```{tab} category.spec.json
```{literalinclude} ../../phoenix-directory/registryold/client/builder/extensions/category/spec.json
:language: json
```

```{tab} category.example.json
```{literalinclude} ../../phoenix-directory/registryold/client/builder/extensions/category/example.json
:language: json
```
