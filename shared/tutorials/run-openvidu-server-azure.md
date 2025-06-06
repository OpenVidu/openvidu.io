=== "Run OpenVidu locally"

    --8<-- "shared/tutorials/run-openvidu-locally-azure.md"

=== "Deploy OpenVidu in Azure"

    1. Deploy OpenVidu Single Node in Azure following these instructions [to deploy in Azure](../../self-hosting/single-node/azure/install.md).

        !!! info "CPUs to be able to record"

            Make sure you deploy with at least 4 CPUs in the Virtual Machine of Azure.

    2. Point the tutorial to your Azure deployment:
          - Modify file [`.env`](https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/4e90828d801208945fc33aede4cd994abcacdc91/advanced-features/openvidu-recording-basic-node-azure/.env){target="\_blank"} to update the LiveKit and Azure configuration to the values of your Azure deployment. You can get the values of `LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` from the [Check deployment outputs in Azure Key Vault](../../self-hosting/single-node/azure/install.md#check-deployment-outputs-in-azure-key-vault). You can get the values of `AZURE_ACCOUNT_NAME`, `AZURE_ACCOUNT_KEY` and `AZURE_CONTAINER_NAME` from the `openvidu.env` file of your deployment (see [Azure SSH Outputs](../../self-hosting/single-node/azure/install.md#check-deployment-outputs-in-the-instance)).
          - Modify file [`app.js`](https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/4e90828d801208945fc33aede4cd994abcacdc91/advanced-features/openvidu-recording-basic-node-azure/public/app.js#L3) to update the value of `LIVEKIT_URL` to `wss://your.azure.deployment.domain`

    !!! warning

        If you are using self-signed certificate you will need to accept the certificate in the browser before using the tutorial.

    !!! info "Configure Webhooks"

        All [application servers](../application-server/index.md) have an endpoint to receive webhooks from OpenVidu. For this reason, when using a production deployment you need to configure webhooks to point to your local application server in order to make it work. Check the [Send Webhooks to a Local Application Server](../../self-hosting/how-to-guides/enable-webhooks.md#send-webhooks-to-a-local-application-server) section for more information.
