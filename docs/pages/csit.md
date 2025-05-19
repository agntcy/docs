# Continuous System Integration Testing

The Agncty Continuous System Integration Testing (CSIT) system design needs to
meet the continuously expanding requirements of Agntcy projects including Agent
Gateway Protocol, Agent Directory, and others.

Tests can be run locally using taskfile or in GitHub Actions.

The directory structure of the CSIT is the following:

```
csit
├── benchmarks                                    # Benchmark tests
│   ├── agntcy-agp                                # Benchmark tests for AGP
│   │   ├── Taskfile.yml                          # Tasks for AGP benchmark tests
│   │   └── tests
│   ├── agntcy-dir                                # Benchmark tests for ADS
│   │   ├── Taskfile.yml                          # Tasks for ADS benchmark tests
│   │   └── tests
│   ├── go.mod
│   ├── go.sum
│   └── Taskfile.yml
├── integrations                                  # Integration tests
│   ├── agntcy-agp                                # Integration tests for [agntcy/agp](https://github.com/agntcy/agp)
│   │   ├── agentic-apps
│   │   ├── Taskfile.yml                          # Tasks for AGP integration tests
│   │   └── tests
│   ├── agntcy-apps                               # Integration tests for ([agntcy/agentic-apps](https://github.com/agntcy/agentic-apps))
│   │   ├── agentic-apps
│   │   ├── Taskfile.yml                          # Tasks for agentic-apps integration tests
│   │   └──  tools
│   ├── agntcy-dir                                # Integration tests for [agntcy/dir](https://github.com/agntcy/dir)
│   │   ├── components
│   │   ├── examples
│   │   ├── manifests
│   │   ├── Taskfile.yml                          # Tasks for ADS integration tests
│   │   └── tests
│   ├── environment                               # Test environment helpers
│   │   └── kind
│   ├── Taskfile.yml                              # Tasks for integration tests
│   └── testutils                                 # Go test utils
├── samples                                       # Sample applications for testing
│   ├── crewai
│   │   └── simple_crew           # Agentic application example
│   │       ├── agent.base.json   # Required agent base model
│   │       ├── build.config.yml  # Required build configuration file
│   ├── model.json        # Required model file
│   ├── langgraph
│   └── research              # Agentic application example
│   │       ├── agent.base.json   # Required agent base model
│   │       ├── build.config.yml  # Required build configuration file
│   │       ├── model.json        # Required model file
│   │       ├── Taskfile.yml      # Tasks for samples tests
│   │       └── tests
│   ├── llama-index
│   │   └── research              # Agentic application example
│   │       ├── agent.base.json   # Required agent base model
│   │       ├── build.config.yml  # Required build configuration file
│   │       ├── model.json        # Required model file
│   │       ├── Taskfile.yml      # Tasks for samples tests
│   │       └── tests
├── ....
├── ....                             # Tasks for Samples
└── Taskfile.yml                     # Repository level task definintions
```

In the Taskfiles, all required tasks and steps are defined in a structured manner. Each CSIT component contains its necessary tasks within dedicated Taskfiles, with higher-level Taskfiles incorporating lower-level ones to efficiently leverage their defined tasks.

## Tasks

You can list all the task defined in the Taskfiles using the `task -l` or simply run `task`.
The following tasks are defined:

```bash
task: Available tasks for this project:
* benchmarks:directory:test:                              All ADS benchmark test
* benchmarks:gateway:test:                                All AGP benchmark test
* integrations:apps:download:wfsm-bin:                    Get wfsm binary from GitHub
* integrations:apps:get-marketing-campaign-cfgs:          Populate marketing campaign config file
* integrations:apps:init-submodules:                      Initialize submodules
* integrations:apps:run-marketing-campaign:               Run marketing campaign
* integrations:directory:download:dirctl-bin:             Get dirctl binary from GitHub
* integrations:directory:test:                            All directory test
* integrations:directory:test-env:bootstrap:deploy:       Deploy Directory network peers
* integrations:directory:test-env:cleanup:                Remove agntcy directory test env
* integrations:directory:test-env:deploy:                 Deploy Agntcy directory test env
* integrations:directory:test-env:network:cleanup:        Remove Directory network peers
* integrations:directory:test-env:network:deploy:         Deploy Directory network peers
* integrations:directory:test:compile:samples:            Agntcy compiler test in samples
* integrations:directory:test:compiler:                   Agntcy compiler test
* integrations:directory:test:delete:                     Directory agent delete test
* integrations:directory:test:list:                       Directory agent list test
* integrations:directory:test:networking:                 Directory agent networking test
* integrations:directory:test:push:                       Directory agent push test
* integrations:gateway:build:agentic-apps:                Build agentic containers
* integrations:gateway:test-env:cleanup:                  Remove agent gateway test env
* integrations:gateway:test-env:deploy:                   Deploy agntcy gateway test env
* integrations:gateway:test:mcp-server:                   Test MCP over AGP
* integrations:gateway:test:mcp-server:agp-native:        Test AGP native MCP server
* integrations:gateway:test:mcp-server:mcp-proxy:         Test MCP server via MCP proxy
* integrations:gateway:test:sanity:                       Sanity gateway test
* integrations:kind:create:                               Create kind cluster
* integrations:kind:destroy:                              Destroy kind cluster
* integrations:version:                                   Get version
* samples:agents:run:test:                                Run test
* samples:autogen:kind:                                   Run app in kind
* samples:autogen:lint:                                   Run lint with black
* samples:autogen:lint-fix:                               Run lint and autofix with black
* samples:autogen:run:test:                               Run tests
* samples:crewai:run:crew:                                Run crew
* samples:crewai:run:test:                                Run crew
* samples:evaluation:run:crew:                            Run application main
* samples:langgraph:run:test:                             Run tests
* samples:llama-deploy:run:app:                           Run application main
* samples:llama-deploy:run:test:                          Run tests
* samples:llama-index:run:test:                           Run tests
```

## Integration Tests

The integration tests are testing interactions between integrated components.

### Directory structure

The CSIT integrations directory contains the tasks that create the test
environment, deploy the components to be tested, and run the tests.

### Running Integration Tests Locally

For running tests locally, we need to create a test cluster and deploy the test environment on it before running the tests.
Make sure the following tools are installed:
  - [Taskfile](https://taskfile.dev/installation/)
  - [Go](https://go.dev/doc/install)
  - [Docker](https://docs.docker.com/get-started/get-docker/)
  - [Kind](https://kind.sigs.k8s.io/docs/user/quick-start#installation)
  - [Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
  - [Helm](https://helm.sh/docs/intro/install/)

To run tests locally:

1. Create the cluster and deploy the environment:

    ```bash
    task integrations:kind:create
    task integrations:directory:test-env:deploy
    # OR change dir to integratons directory
    cd integrations
    task kind:create
    task directory:test-env:deploy
    ```

1. Run the tests:

    ```bash
    task integrations:directory:test
    # OR change dir to integratons directory
    cd integrations
    task directory:test
    ```

1. When finished, the test cluster can be cleared:

    ```bash
    task integrations:kind:destroy
    # OR change dir to integratons directory
    cd integrations
    task kind:destroy
    ```

### Contributing Tests

Contributing your own tests to the project is a great way to improve the
robustness and coverage of the testing suite.

To add your tests:

1. Fork and Clone the Repository

    Fork the repository to your GitHub account. Clone your fork to your local machine.

    ```bash
    git clone https://github.com/your-username/repository.git
    cd repository
    ```

1. Create a new branch

    Create a new branch for your additions to keep your changes organized and separate from the main codebase.

    ```bash
    git checkout -b add-new-test
    ```

1. Navigate to the Integrations directory

    Locate the integrations directory where the test components are organized.

    ```bash
    cd integrations
    ```

1. Add your test

    Following the existing structure, create a new sub-directory for your test
    if necessary. For example, `integrations/new-component`. Add all necessary
    test files, such as scripts, manifests, and configuration files.

1. Update Taskfile

    Modify the Taskfile.yaml to include tasks for deploying and running your new
    test.

    ```yaml
    tasks:
      new-component:test-env:deploy:
        desc: Desription of deployig new component elements
        cmds:
          - # Command for deploying your components if needed

      new-component:test-env:cleanup:
        desc: Desription of cleaning up component elements
        cmds:
          - # Command for cleaning up your components if needed

      new-component:test:
        desc: Desription of the test
        cmds:
          - # Commands to set up and run your test
    ```

1. Test locally

    Before pushing your changes, test them locally to ensure everything works as
    expected.

    ```bash
    task integrations:kind:create
    task integrations:new-componet:test-env:deploy
    task integrations:new-component:test
    task integrations:new-componet:test-env:cleanup
    task integrations:kind:destroy
    ```

1. Document your test

    Update the documentation in the docs folder to include details on the new
    test. Explain the purpose of the test, any special setup instructions, and
    how it fits into the overall testing strategy.

1. Commit and push your changes

    Commit your changes with a descriptive message and push them to your fork.

    ```bash
    git add .
    git commit -m "feat: add new test for component X"
    git push origin add-new-test
    ```

1. Submit a pull request

    Go to the original repository on GitHub and submit a pull request from your
    branch. Provide a detailed description of what your test covers and any
    additional context needed for reviewers.

## Samples

The samples directory in the CSIT repository serves two primary purposes related
to the testing of agentic applications.

### Running Samples Tests Locally

For running tests locally, we need the following tools to build the sample applications:
  - [Taskfile](https://taskfile.dev/installation/)
  - [Python 3.12.X](https://www.python.org/downloads/)
  - [Poetry](https://python-poetry.org/docs/#installation)
  - [Docker](https://docs.docker.com/get-started/get-docker/)
  - [Kind](https://kind.sigs.k8s.io/docs/user/quick-start#installation)
  - [Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)

Run the test:

```bash
task samples:<app-name>:run:test
# OR change dir to integratons directory
cd samples/<app-name>
task run:test
```

### Compilation and Execution Verification

The agentic applications stored within the `samples` directory are subjected to
sample tests. These tests are designed to run whenever changes are made to the
agentic apps to ensure they compile correctly and are able to execute as
expected.

### Base for Agent Directory Integration Test

The agentic applications in the `samples` directory also serve as the foundation
for the agent model build and push test. This specific test checks for the
presence of two required files: `model.json` and `build.config.yaml`. If these
files are present within an agentic application, the integration agent model
build and push tests are triggered. This test is crucial for validating the
construction and verification of the agent model, ensuring that all necessary
components are correctly configured and operational.
