# Hosted AGNTCY Agent Directory

A public hosted instance of the Agent Directory is available at
[https://hub.agntcy.org/](https://hub.agntcy.org/). In
this section we describe the main features of this instance which is provided __AS
IS__ to the community to help users familiarize themselves with the Agent
Directory.

AGNTCY Agent Directory is designed to provide a robust multi-organization platform for hosting and
managing Agent Directory Records, which we will refer to as simply "records" or
"agent records." AGNTCY Agent Directory acts as a centralized
point for organizing and accessing agent records. This hosted service is enhanced by a
gRPC API that supports efficient service communication and integration, ensuring
seamless interaction between components.


AGNTCY Hub serves as a central platform for hosting and managing various
agent-related services. The main purpose of the Agent Directory Service
component of Hub is to provide a comprehensive solution
for developers and IT admins to register, discover, and manage records in an
organized manner. By offering a secure environment for authentication and user
management, it ensures that organizations can confidently manage their agent
directories and related services.

## Core Concepts

The AGNTCY Agent Directory is organized around a few basic concepts:

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
while the frontend hosted AGNTCY Agent Directory provides access control with
Users and their Organizations and management of agent records in their Repos.

## Features

AGNTCY Agent Directory enables users to:

* View and search for public agent records.
* View your organization's public and private agent records.
* Publish agent records to an agent repository.
* Access multiple separate organizations.
* Invite other users your organizations.

## Using the Hub

### Signing up for the hosted AGNTCY Agent Directory and Logging in

To get started with the hosted AGNTCY Agent Directory, sign up for free at the [AGNCTY Agent Directory
homepage](https://hub.agntcy.org/). You can sign up with your GitHub account or
by providing an email and password. Once your account is created, simply log in.
When first logging in, you are prompted to create a name for your default
organization. This organization is a personal space where all repositories
belong to you.

![Logging in](../_static/login.png)

### View and Search for Agents

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

### Manage Agents associated with Your Organization

The Agent Directory Page allows you to view, edit, and create agent repositories
in the AGNTCY Agent Directory. Here the records are displayed in a table with customizable columns.

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

## Add an Agent Directory Record to the AGNTCY Agent Directory
Agent directory records are associated with a repository. A repository must
exist first for an agent record to be added to it.

### Create a new agent repository
To add an agent repository in the AGNTCY Agent Directory:

1. Click the **+ New Repository** button.
1. Enter the repository name.
1. Select the visibility for your agent repository.
    * Public agent repositories appear in search results.
    * Private agent repositories are only visible in your organization.
1. Click **Publish**.
1. You can also publish the agent repository using the generated CLI command.
1. Click **Finish**.

At this point, you have an empty repository ready for agent records.

### Adding an Agent Directory Record to a Repository
Adding an Agent Directory Record has these prerequisites:
1. You need to install the AGNTCY Agent Directory command line tool, `dirctl`.
1. You need an agent record that conforms to AGNTCY Agent Directory requirements.
1. You need to sign your agent record.

#### Pre-req 1: Install `dirctl`
Binary packages and installation of the AGNTCY Agent Directory `dirctl`
command line tool are available in multiple forms on GitHub:
* [container image](https://github.com/agntcy/dir/pkgs/container/dir-ctl)
* [homebrew](https://github.com/agntcy/dir/tree/main/HomebrewFormula)
* [binary](https://github.com/agntcy/dir/releases)

After installation, use the `dirctl` and `dirctl hub` commands to list the
available commands.

#### Pre-req 2: Create a Conforming Agent Directory Record
An Agent Directory record is stored in JSON format. The record is specific
to one entry in the Agent Directory. The structure of each AD record is
defined by the
[Open Agentic Schema Framework](https://schema.oasf.agntcy.org/objects/agent)
starting at the root with an [Agent object](https://schema.oasf.agntcy.org/objects/agent).

To be useful, an agent record should include at least the following:
* Name of the agent (the name MUST match the organization and repository name in the AGNTCY Agent Directory),
* Version of the agent (use semantic convention)
* Description (something to help any viewer understand what your agent does, what is the use case it is applicable to, expected inputs and outputs, LLM used, runtime, etc)
* Locator, per [OASF locator objects](https://schema.oasf.agntcy.org/objects/locator?extensions=)
   * type(s) (source code, agent as a service, docker image, etc) matching the supported types in the OASF locator objects
   *  url (corresponding address to find the agent)
* Skills - MUST follow the [OASF skills schema](https://schema.oasf.agntcy.org/skills?extensions=)

And it will look like this
```
{
  "name": "organization/my-agent",
  "version": "2.0",
  "description": "This agent takes any text input and condenses it down to 3 bullets of less than 100 characters each using any LLM.",
  "locators": \[
    {
      "url": "https://github.com/example/agent_A",
      "type": "package-source-code"
    }
  \],
  "skills": \[
    {
      "class_uid": 10201
    }
  \]
}
```


#### Pre-req 3: Signing Agent Directory Records using `dirctl`
You must sign the record before pushing it to the AGNTCY Agent Directory. Unsigned records are
rejected by the API.

To sign an agent record in the file `agent.json` using the default provider [sigstore](https://www.sigstore.dev/), run:

```shell
dirctl sign agent.json > agent.signed.json
```

The signing service login page opens in your browser. Use your credentials to log in. The
agent record will be augmented with a generated signature and will be output
in JSON format. The new signed agent record can be pushed to the Hub.

For further details on signing, please see
[the Agent Directory HOWTO](dir-howto.md#signing-and-verification).

#### Pushing Agent Directory Records using `dirctl`
Once all pre-requisites are complete, you are ready to push an agent record to an agent repository
that you have write access to.

Pushing and pulling agent directory records is done using thd `dirctl` tool.

From your terminal window:
1. Login to your AGNTCY Agent Directory account

      ```dirctl hub login```

   The login page opens in your browser. Use your credentials to log in.
3. Verify your AGNTCY Agent Directory organizations and which one you are currently logged into:

      ```dirctl hub orgs```

   Switch organizations as needed to the organization that you want to push your agent record to:

      ```dirctl hub orgs switch```

5. Push your signed, conforming agent record to the desired organization/repository:

      ```dirctl hub push <organization/repository_name> <local filename of your signed agent json file>```

7. When you're done, logout of your hub account

      ```dirctl hub logout```

#### Pulling Agent Directory Records using `dirctl`

You can also pull an agent directory record via `dirctl` using the command listed on the agent details page.


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

## Managing Organizations and Users

### Settings

The settings page allows you to manage your organizations and their users.

#### List Organizations

Organizations represent groups of users within the Hub, each with its own
repositories. Users can be member of many organizations. The organizations
available to you are listed under the **Organizations** tab.

#### Switch Organization
The organization the user is currently signed in is displayed in bold in the organization list and indicated in the dropdown at the top of the left side menu.

To switch organization:

1. Click on the dropdown at the top of the left side menu
1. Select the organization to switch to
1. Follow the login procedure

#### Create a new organization

To create a new organization:

1. Click the **+ Create Organization** button.
1. Enter the organization name.
1. Click the **Create organization** button.
1. Click the **Finish** button.


#### Manage Users

The list of users of the current organization are accessible by clicking on the organization (in bold) in the list.

You can invite other users to the organization by clicking the **+ Invite User**
button.

```{NOTE}
You cannot invite other users to your personal organization created
during signing up. To collaborate with others, create a new organization and invite them to it.
```


## Troubleshooting pushing agents to the AGNTCY Agent Directory
`Error: failed to validate access token: invalid session token`
You forgot to login to your AGNTCY Agent Directory account

`Error: failed to push agent: could not receive response: rpc error: code = InvalidArgument desc = agent: invalid value in agent name`
The “agent name” attribute in the json file does not match the organization/repository in the Hub.

`Error: failed to push agent: could not receive response: rpc error: code = AlreadyExists desc = agent: data model with same version already exists`
You are trying to upload a new agent record with the same name and version as one that exists already. Update the version number in the json file.

Details on other uses of the `dirctl` command to interact with the
Agent Directory are
[available in the documentation](https://github.com/agntcy/dir/pkgs/container/dir-ctl).
After installation, use the `dirctl hub` command to list the available commands.