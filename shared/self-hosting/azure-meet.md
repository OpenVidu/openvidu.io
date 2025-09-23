### OpenVidu Meet Credentials

Configure the initial credentials for accessing OpenVidu Meet:

=== "OpenVidu Meet credentials"

    Parameters in this section look like this:

    ![OpenVidu Meet credentials](../../../../assets/images/self-hosting/shared/azure-meet-credentials.png)

    - **InitialMeetAdminPassword**: Initial password for the "admin" user in OpenVidu Meet. If not provided, a random password will be generated and stored in the Azure Key Vault.
    - **InitialMeetApiKey**: Initial API key for OpenVidu Meet. If not provided, no API key will be set and the user can configure it later from the Meet Console.

    Both parameters are optional. If you don't specify them, you can retrieve the generated credentials from the Azure Key Vault after deployment.
