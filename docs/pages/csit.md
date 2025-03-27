# Continuous System Integration Testing

The Agncty Continuous System Integration Testing (CSIT) system design needs to
meet the continuously expanding requirements of Agntcy projects including Agent
Gateway Protocol, Agent Directory, and others.

Tests can be run locally using taskfile or in GitHub Actions.

The directory structure of the CSIT is the following:

```
csit
└── integrations
│   ├── Taskfile.yaml                   # Task definitions
│   ├── docs                            # Documentations
│   ├── environment
│   │   └── kind                        # kind related manifests
│   ├── agntcy-dir                      # Agent directory related tests, components, and so on
│   │   ├── components                  # The compontents charts
│   │   ├── examples                    # The examples that can be used for testing
│   │   ├── manifests                   # Requred manifests for the tests
│   │   └── tests                       # Tests
│   └── agntcy-agp                      # Agent Gateway related tests, components, and so on
│       └── agentic-apps                # Agentic apps for gateway tests
│           ├── autogen_agent
│           └── langchain_agent
│
└── samples
    ├── app1                            # Agentic application example
    │   ├── model.json                  # Required model file
    │   ├── build.config.yaml           # Required build configuration file
    ├── app2                            # Another agentic application example
    │   ├── model.json
    │   ├── build.config.yaml
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
    cd integrations
    task kind:create
    task test:env:directory:deploy
    ```

1. Run the tests:

    ```bash
    task test:directory
    ```

1. When finished, the test cluster can be cleared:

    ```bash
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
      test:env:new-component:deploy:
        desc: Desription of deployig new component elements
        cmds:
          - # Command for deploying your components if needed

      test:env:new-component:cleanup:
        desc: Desription of cleaning up component elements
        cmds:
          - # Command for cleaning up your components if needed

      test:new-component:
        desc: Desription of the test
        cmds:
          - # Commands to set up and run your test
    ```

1. Test locally

    Before pushing your changes, test them locally to ensure everything works as
    expected.

    ```bash
    task kind:create
    task test:env:new-componet:deploy
    task test:new-component
    task test:env:new-componet:cleanup
    task kind:destroy
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
cd samples/[app-name]
task run:test

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
