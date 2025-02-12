# Services

## Composition

The service layer is content-centric and revolves around _generation_, _serving_, and _consumption_ of AI agent data models.
In order to serve these operations, we can decompose the service plane by layers based on their respective responsibilities.

```{image} ../_static/service_composition.png
:alt: Service Layer Composition
:width: 100%
:align: center
```
<br>

- **Data Layer** - tools, services, and processes centered around _generation_ of agent data models. 
  Examples of this include build tools and SDKs used to compile agent data models from given sources such as GitHub repositories.

- **Storage Layer** - tools, services, and processes centered around _serving_ of agent data models.
  Examples of this include storage services and SDKs for publication and retrival of agent data model contents.

- **Application Layer** - tools, services, and processes centered around _consumption_ of agent data models.
  Examples of this include third-party applications such as search service that rely on agent data model contents to perform or expose certain operations.

In order to support the service layers, implementations should expose interfaces that conform to the requirements described below.

## Content Management

This interface is responsible for all the operations around agent data model **generation** and **publication** operations.

- **Build** - Clients MUST be able to build agent data models. 
  Build defines an interface for generating an agent data model from a given source such as code, GitHub repository, Docker image, etc.
  The produced artifact conforms to the agent data model schema described in previous chapter.
  _This interface is part of the Data Layer_.

- **Push** - Clients MUST be able to store content to a given destination.
  Publish defines an interface responsible for storing agent data models to local or
  remote services from where they can later be retrieved.
  _This interface is part of the Storage Layer_.

## Content Discovery

This interface is responsible for all the operations around agent data model **search** and **retrieve** operations.

- **Pull** - Clients MUST be able to pull published content.
  Retrival defines an interface for retrieving agent data models stored on local or remote services.
  _This interface is part of the Storage Layer_.

- **Search** - Clients MAY be able to list or otherwise query published content.
  Search defines an interface responsible for discovering published agent data models based on given search parameters.
  _This interface is part of the Application Layer_.
