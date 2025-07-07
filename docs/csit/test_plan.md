# CSIT SLIM Test Plan

This pgae outlines the proposed test plan for CSIT (Cisco Systems Integration Testing) of SLIM (Secure Light-weight IoT Messaging) networks. The core idea revolves around defining network topologies via a YAML configuration, deploying SLIM instances using Helm, and leveraging a new Python-based SLIM client for message simulation and metric collection.

## 1. Basic Idea

The fundamental concept is to enable comprehensive testing of SLIM network configurations by:
*   **Topology Definition**: Describing the SLIM network's topology, including SLIM nodes (servers) and clients, their interconnections, and routing paths, within a structured YAML file.
*   **Automated Deployment**: Utilizing existing Helm charts for the streamlined deployment of SLIM instances based on the defined topology.
*   **Client Simulation**: Implementing a flexible Python SLIM client to simulate various message-passing scenarios and collect relevant metrics.

## 2. Key Components

### 2.1. Topology Definition (YAML File)

A YAML file will serve as the single source of truth for defining the SLIM network topology. This file will specify:
*   **Clients**: Configuration for individual SLIM clients, including authentication methods, Multi-Level Security (MLS) group details (if applicable), and the SLIM server(s) they connect to.
*   **Servers (SLIM Nodes)**: Configuration for SLIM server instances, including their authentication methods and defined routes for message forwarding.

**Example `topology.yaml`:**

```yaml
topology:
    clients:
        "agentA":
            auth:
                spireJwt: true
            mls:
                group: group1
                moderator: true
                invites:
                    - "agentB"
            connectedTo:
                - "slim_1"
        "agentB":
            auth:
                spireJwt: true
            connectedTo:
                - "slim_4"
    servers:
        "slim_1":
            auth:
                spireMtls: true
            routes:
                - "agentB > slim_2"
                - "agentB > slim_3"
        "slim_2":
            auth:
                spireMtls: true
            routes:
                - "agentB > slim_4"
        "slim_3":
            auth:
                spireMtls: true
            routes:
                - "agentB > slim_4"
        "slim_4":
            auth:
                spireMtls: true
```

> Alternatively we may think of separating server connection and subscription (route) configs, because in real world connections in between SLIM servers nodes might be given, any connection might not be possible physically.

### 2.2. SLIM Instance Deployment

SLIM instances (server nodes) will be deployed using existing [Helm chart](https://github.com/agntcy/slim/tree/main/charts/slim). The test framework will orchestrate the deployment based on the `servers` section defined in the `topology.yaml`, SLIM configurations will be generated from these definitions.

### 2.3. Python SLIM Client

A new SLIM client will be developed in Python, leveraging existing SLIM bindings. This client has to be configurable to facilitate various testing scenarios:
*   **Message Publishing**: Capable of publishing a specified number of messages to a configurable topic name. This allows for testing message throughput and reliability from the client side.
*   **Message Subscription**: Configurable to subscribe to a given topic name and wait for incoming messages. This enables verification of message delivery and routing.
*   **Metrics Exposure**: The client will expose metrics, potentially via Prometheus, on the number of messages sent and received. 
*   

Thus, we can test p2p and broadcast messaging as well.

## 3. Test Flow Overview

1.  **Topology Definition**: Defines the desired SLIM network topology in a `topology.yaml` file.
2.  **SLIM Deployment**: The test automation framework reads the `topology.yaml` and uses Helm to deploy the specified SLIM server instances.
3.  **Client Simulation**: The Python SLIM clients are created as Kubernetes Jobs / Pods with generated SLIM configuration based on `clients` section of the `topology.yaml`. They then begin publishing and/or subscribing to messages as per the test scenario.
4.  **Metrics Collection & Analysis**: Metrics exposed by the Python clients (and eventually SLIM servers) are collected.
   
This structured approach ensures repeatable, scalable, and comprehensive testing of SLIM network configurations and functionalities. 
 
