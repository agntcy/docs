# Verifying an Identity

## Using the User Interface

The "Verify Identity" screen allows users to verify a digital badge, typically a JOSE (JSON Object Signing and Encryption) enveloped badge. This screen is designed for quick and secure verification.

1.  **Access the Screen**: Navigate to the "Verify Identity" page.

    ![Verify Identity](../assets/identity/identity_service/verify-identity.png)

2.  **Provide the Badge**:
    - **Option A (File Upload)**: Click or drag and drop a JSON file (max 3MB) containing the JOSE enveloped badge into the "Details" area.
    - **Option B (Text Input)**: Paste the JOSE enveloped badge string directly into the "Badge" text field.

    !!! note
        We support both the JOSE enveloped badge or the full JSON badge content that you can obtain from the Agentic Services. The JOSE enveloped badge is a compact representation of the badge, while the full JSON badge contains all the details in a structured format.

3.  **Initiate Verification**: Click the "Verify" button.
4.  **View Results**: The "Verification Results" section will populate with the outcome of the badge verification.

    ![Verify Identity Results](../assets/identity/identity_service/verify-identity-done.png)

## Using the Python SDK

To verify an identity using the Python SDK, follow these steps:

1. **Install the Python SDK:** Ensure you have the Python SDK installed. Refer to the [SDK section](./identity_service_sdk.md) of the documentation for detailed installation instructions.

2. **Use the following code snippet:**

    ```Python
    from identityservice.sdk import IdentityServiceSdk as Sdk

    from dotenv import load_dotenv
    load_dotenv()

    identity_sdk = Sdk(
        api_key="{YOUR_ORGANIZATION_API_KEY}"
    )

    try:
        print(
            "Got badge: ",
            identity_sdk.verify_badge(
                "{JOSE_ENVELOPED_BADGE}"
            ),
        )
    except Exception as e:
        print("Error verifying badge: ", e)

    ```

    !!! note
        Replace `{YOUR_ORGANIZATION_API_KEY}` with your actual [Organization API Key](./identity_service_api_access.md#organization-api-key) and `{JOSE_ENVELOPED_BADGE}` with the JOSE enveloped badge you want to verify.
