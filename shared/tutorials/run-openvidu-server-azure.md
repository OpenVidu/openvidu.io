=== "Run OpenVidu locally"

    --8<-- "shared/tutorials/run-openvidu-locally-azure.md"

=== "Deploy OpenVidu in Azure"

    1. You will need to deploy a Single Node Community Edition in Azure to be able to test this tutorial, follow this instructions [to deploy in Azure](../../self-hosting/single-node/azure/install.md)

    !!! info "CPUs to be able to record"

        Make sure you deploy with at least 4 CPUs in the Virtual Machine of Azure.

    2. Next step is changing some credentials and URLs in the source code:   
    Go to the `.env` and change the LiveKit configuration and Azure configuration to the values of the single node deployment you've deployed in Azure. To check this values go to [Azure Key Vault Outputs](../../self-hosting/single-node/azure/install.md#azure-key-vault-outputs), once you know how to retrieve the outputs, you will need to get the value of the **LIVEKIT_API_KEY** and **LIVEKIT_API_SECRET** to change them in the `.env`, for the **LIVEKIT_URL** use *wss://domainname*, you will need to change the first line, where is declared **LIVEKIT_URL** of `app.js` with this value too.   
    For the Azure configuration go to [Azure SSH Outputs](../../self-hosting/single-node/azure/install.md#check-outputs-in-the-instance), once you are reading `openvidu.env` check for values of **AZURE_ACCOUNT_NAME**, **AZURE_ACCOUNT_KEY** and **AZURE_CONTAINER_NAME** and change the `.env` with those values.

    !!! warning
        If you are using selfsigned certificate you will need to accept the certificate in the browser before using the tutorial. 