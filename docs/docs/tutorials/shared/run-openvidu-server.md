=== "Run OpenVidu locally"

    --8<-- "docs/docs/tutorials/shared/run-openvidu-locally.md"

=== "Deploy OpenVidu"

    To use a production-ready OpenVidu deployment, visit the official [deployment guide](/docs/self-hosting/deployment-types/).

    !!! info "Configure Webhooks"

        All [application servers](../application-server/index.md){:target="\_blank"} have an endpoint to receive webhooks from OpenVidu. For this reason, when using a production deployment you need to configure webhooks to point to your local application server in order to make it work. Check the [Send Webhooks to a Local Application Server](../../self-hosting/how-to-guides/enable-webhooks.md#send-webhooks-to-a-local-application-server){:target="\_blank"} section for more information.
