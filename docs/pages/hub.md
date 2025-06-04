# AGNTCY Agent Hub

A public instance of the Agent Directory is available at
[https://hub.agntcy.org/](https://hub.agntcy.org/). In
this section we describe the main features of this instance which is provided __AS
IS__ to the community to help users familiarize themselves with the Agent
Directory. In this section we will use the name Hub to indicate
hub.agntcy.org.

Hub is designed to provide a robust multi-organization platform for hosting and
managing Agent Directory Records, which we will refer to as simply "records" or
"agent records." Its primary aim is to deliver a hub-like user experience,
offering easy navigation and management for users. Hub acts as a centralized
point for organizing and accessing agent records. This service is enhanced by a
gRPC API that supports efficient service communication and integration, ensuring
seamless interaction between components.

Hub serves as a central platform for hosting and managing various
agent-related services. The main purpose is to provide a comprehensive solution
for developers and IT admins to register, discover, and manage records in an
organized manner. By offering a secure environment for authentication and user
management, it ensures that organizations can confidently manage their agent
directories and related services.

## Core Concepts

The Hub is organized around a few basic concepts:

* Users - A user is the basic unit of authentication and authorization in the 
Hub, usually corresponding to a human or service account.
* Organization - An organization provides a way to group users for sharing agents
and handling administrative tasks. A user can belong to many organizations, but
organizations are flat and cannot belong to one another.
* Agent Records - An Agent Record is a collection of data and metadata about a
particular agentic application or service. The schema of the Record is defined
in [OASF](oasf.md) and contains, for example, a
[collection of skills](oasf-taxonomy.md).
* Repositories - A agent repository collects agent records that describe
different versions of the same agent into one location to provide an overview of
its history and current status. A Record can belong to only one repo, while a
user or organization may access many different repos and by extension their
agent records.

The [Agent Directory Service (ADS)](dir.md) provides storage for agent records
while the Hub provides access control with Users and their Organizations and
management of agent records in their Repos.

## Features

Hub enables users to:

* View and search for public agent repositories.
* Create repositories.
* Publish Agent Records.
* Access multiple separate organizations.

## Using the Hub

### Signing up for the Hub and Logging in

To get started with the Hub, sign up for free at the [AGNCTY Agent Directory
homepage](https://hub.agntcy.org/). You can sign up with your GitHub account or
by providing an email and password. Once your account is created, simply log in.
When first logging in, you are prompted to create a name for your default
organization. This organization is a personal space where all repositories
belong to you.

![Logging in](../_static/login.png)

### Explore Page

"The Explore page allows users to browse and search through available agent repositories.

![The Explore Page](../_static/explore.png)

You can refine the results using predefined filters and open search:

* Use the **Search** bar to search for a text string in a repository name. To
clear the search bar, click the **×**.
* Use the drop-down **Filters** list to narrow the results by Agent Skill.
* Use the drop-down **Sort by** list to sort the displayed items by Most Recent
or Oldest.

You can change organizations by clicking the Org drop-down list and selecting
another organization.

### Agent Directory Page

The Agent Directory Page allows you to view, edit, and create agent repositories
in the Hub. Here the records are displayed in a table with customizable columns.

You can select which columns are displayed, and in which order, by clicking the
**Arrange Columns** button (**▥**).

You can reload the listed items by clicking the **Reload** button (**⟳**).

You can refine the results using predefined filters and open search:

* Use the **Search** bar to search for a text string in an agent repository
name. To clear the search, click the **×**.
* Use the drop-down **Filters** list to narrow the results by Agent Skill.
* Use the drop-down **Sort by** list to sort the displayed items by Most Recent
or Oldest.

![The Agent Directory Page](../_static/directory.png)

#### Agent Actions

Clicking the three dots (**⁝**) at the end of any row in the Agent Directory
table opens a drop-down list of actions you can perform on that agent
repository.

* Click **Open Details** to [view the agent details](#agent-details).
* Click **Edit** to edit the agent.
* Click **Delete** to remove the agent repo from the directory, including all
of its agent records.

#### Agent Details

Clicking on an agent repository opens the Agent Details page with further
information on the agent repository.

![The Agent Details Page](../_static/agent.png)

The **General** tab lists the following information from the agent record:

* A description of the agent.
* The skills associated with the agent.
* The version number and date of publishing.
* The CLI command to push a new version of the agent.

The **Versions** tab lists the published versions of the agent.

The **Settings** tab allows the owner to change the
visibility of the agent.

#### Create

To list an agent in the Hub:

1. Click the **+ New Repository** button.
1. Enter the repository name and description.
1. Select the visibility for your agent repository.
    * Public agent repositories appear in search results.
    * Private agent repositories are only visible in your organization.
1. Click **Publish**.
1. You can also publish the agent repository using the generated CLI command.
1. Click **Finish**.

Your agent repository is created in the Hub.

### Settings

The settings page allows you to manage your organizations and users.

#### Organizations

Organizations represent groups of users within the Hub, each with its own
repositories. Users can be member of many organizations. The organizations
available to you are listed under the **Organizations** tab.

Clicking the three dots (**⁝**) at the end of any row in the table opens a
drop-down list of actions you can perform on that organization.

* Click **Switch** to switch to the organization.

You can reload the listed items by clicking the **Reload** button (**⟳**).

#### Users

The users in a organization are listed under the **Users** tab.

You can invite other users to the organization by clicking the **+ Invite User**
button.

> Note: You cannot invite other users to your personal organization created
> during signing up. To collaborate with others, create a new organization and
> invite them to it.

Clicking the three dots (**⁝**) at the end of any row in the table opens a
drop-down list of actions you can perform on that user.

* Click **Edit** to edit the user's role.
* Click **Delete** to delete the user.

You can reload the listed items by clicking the **Reload** button (**⟳**).

### Using the Hub through CLI

You can use the Hub through the CLI. Binary packages and installation of
the `dirctl` command line tool are available in multiple forms on GitHub:
* [container image](https://github.com/agntcy/dir/pkgs/container/dir-ctl)
* [homebrew](https://github.com/agntcy/dir/tree/main/HomebrewFormula)
* [binary](https://github.com/agntcy/dir/releases)

Details on other uses of the `dirctl` command to interact with the
Agent Directory are
[available in the documentation](https://github.com/agntcy/dir/pkgs/container/dir-ctl).
After installation, use the `dirctl hub` command to list the available commands.

#### Create a Conforming Agent Directory Record

An Agent Directory record is stored in JSON format. The record is specific
to one entry in the Agent Directory. The structure of each AD record is
defined by the
[Open Agentic Schema Framework](https://schema.oasf.agntcy.org/objects/agent)
starting at the root with an [Agent object](https://schema.oasf.agntcy.org/objects/agent).


#### Signing Agent Directory Records

You must sign the record before pushing to Hub. Unsigned records are
rejected by the API.

To sign an agent record in the file `agent.json` using the default provider [sigstore](https://www.sigstore.dev/), run:

```shell
dirctl sign agent.json
```

The login page to  opens in your browser. Use your credentials to log in. The
agent record will be augmented with a generated signature and will be output
in JSON format. The new signed agent record can be pushed to the Hub.

For further details on signing, please see
[the Agent Directory HOWTO](dir-howto.md#signing-and-verification).

#### Logging In

Use the `dirctl hub login` command to log in. The login page opens in your
browser. Use your credentials to log in.

#### Listing Organizations

Use the `dirctl hub orgs` command to list the organizations you are a member of.

#### Pushing and Pulling Agent Directory Records
To push the agent record stored in the file `agent.json`, use the command:

```shell
dirctl hub push "<org>/<repo>:<version>" agent.json
```

To pull the agent record, use the command:

```shell
dirctl hub pull "<org>/<repo>:<version>"
```

Alternatively, you can use `dirctl hub pull "<digest>"` instead.

#### Verifying an Agent Directory Record Signature

The verification process allows validation of the agent record signature
against a specific identity.

To verify that an agent record is properly signed, you can run `dirctl
verify agent.json`.

To verify the signature against a specific identity, for example to check if an
agent record originates from GitHub Agntcy users, run:

```bash
dirctl verify agent.json \ 
                 --oidc-issuer "(.*)github.com(.*)" \
                 --oidc-identity "(.*)@agntcy.com"
```

For further details on verification, please see
[the Agent Directory HOWTO](dir-howto.md#signing-and-verification).
