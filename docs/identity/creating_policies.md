# Creating Policies for Agentic Services

The Policies section in the **AGNTCY Identity Service** allows administrators to define rules and permissions for Agentic Services.
This guide will walk you through the process of creating, editing, and managing policies,
ensuring your Agentic Services operate within the desired constraints and capabilities.

## Introducing Task-Based Access Control

The **AGNTCY Identity Service** leverages Task-Based Access Control (TBAC) to enhance the management and security of Agentic Services. TBAC allows administrators to define specific tasks that can be performed by each service and the permissions required to execute these tasks. By integrating TBAC into your policies, you can ensure that each Agentic Service adheres to organizational security standards and operational requirements.

### Benefits of TBAC

- **Enhanced Security:** TBAC provides a granular level of security by defining task-specific permissions, reducing the risk of unauthorized access.
- **Flexibility:** Easily adjust permissions as organizational needs change, ensuring your Agentic Services remain adaptable to evolving requirements.
- **Centralized Management:** Administer all task permissions from a single interface within the Policies section, simplifying oversight and updates.

## 1. Accessing the Policies Section

1. **Navigate to Policies:**

  - From the main dashboard, click on the "Policies" section in the left-hand navigation menu to view existing policies or create new ones.

    ![Navigate to Policies section](../assets/identity/identity_service/policies_01.png)

## 2. Creating a New Policy

1. **Add Policy:**

   - Click on the "Add Policy" button to initiate the creation process. This will open the policy creation wizard.

2. **Policy Details:**

   - **Name:** Enter a descriptive name for your policy (e.g., "Email Policy").
    - **Assigned To:** Select the Agentic Service the policy will apply to (e.g., "SuperAgent").
    - **Description:** Provide a brief description of the policy's purpose and scope.

    ![Policy Details](../assets/identity/identity_service/policies_02.png)

3. **Policy Rules:**

   - **Add Rule:** Define the specific actions and permissions associated with the policy.
    - **Name:** Specify the rule name (e.g., "Search & Read Emails").
    - **Tasks:** Choose the tasks this rule will allow or restrict (e.g., "gmail_find_email").
    - **Action:** Select the action type, such as "Allow" or "Deny".
    - **Needs Approval:** Optionally, specify if this action requires additional approval.

    ![Policy Rule Creation](../assets/identity/identity_service/policies_03.png)
    ![Policy Rule Tasks Selection](../assets/identity/identity_service/policies_04.png)
    ![Policy Rule Submission](../assets/identity/identity_service/policies_05.png)

4. **Add Multiple Rules:**

   - You can add additional rules by clicking "Add Rule" and repeating the steps above for each new rule. This is useful for complex policies requiring multiple permissions.

    ![Multiple Rule Addition](../assets/identity/identity_service/policies_06.png)

5. **Review and Save Policy:**

   - Review all policy details and rules to ensure accuracy. Once satisfied, click "Save" to finalize and save the policy.

    ![Review Policy](../assets/identity/identity_service/policies_07.png)
    ![Review Policy Rule Details](../assets/identity/identity_service/policies_08.png)
    ![Created Policy](../assets/identity/identity_service/policies_09.png)

## 3. Managing Policies

1. **Viewing Policies:**

    - The Policies dashboard displays all existing policies, their assigned Agentic Service, and the creation date. Click on a policy to expand and view detailed rules.

   ![View Policy Details](../assets/identity/identity_service/policies_10.png)

2. **Editing Policies:**

    - To modify an existing policy, select "Edit" from the options menu. Make necessary changes to details or rules, and then save.

    ![Edit Policy Button](../assets/identity/identity_service/policies_11.png)
    ![Edit Policy Details](../assets/identity/identity_service/policies_12.png)

3. **Deleting Policies:**

    - If a policy is no longer needed, select "Delete" from the options menu to remove it from the system. Confirm the deletion when prompted.

## Best Practices

- Regularly review and update policies to align with changing organizational needs and security requirements.
- Utilize the "Needs Approval" feature for actions with higher security implications to maintain oversight.
