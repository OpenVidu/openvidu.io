# Enable Webhooks

If you need to integrate OpenVidu with other services, you can use webhooks to send notifications about events that occur in your OpenVidu deployment. This guide explains how to enable webhooks.

## OpenVidu Server Configuration

1. SSH into one of your Master Nodes (or Single Node).
2. Add to the file `livekit.yaml` the following configuration:

    ```yaml
    webhook:
        api_key: ${openvidu.LIVEKIT_API_KEY:?mandatory}
        urls:
        ...
            - https://<YOUR_WEBHOOK_URL>
    ```

    The file is located at:

    - **Single Node**: `/opt/openvidu/config/livekit.yaml`
    - **Elastic / High Availability**: `/opt/openvidu/config/cluster/media_node/livekit.yaml`

    Make sure the `webhook` section exists in the file, and if it doesn't, add it as stated in the previous snippet. Then, add the URL where you want to receive the webhook notifications. In this example, `<YOUR_WEBHOOK_URL>` is the URL where you want to receive the notifications.

3. Restart the Master Node (or Single Node) to apply the changes:

    ```bash
    systemctl restart openvidu
    ```

    This command will restart the services which changed their configuration files in your entire OpenVidu deployment.

## <span class="openvidu-tag openvidu-pro-tag">PRO</span> V2 Compatibility Configuration

!!!info
    Before deploying OpenVidu PRO, you need to [create an OpenVidu account](https://openvidu.io/account){:target=_blank} to get your license key.
    There's a 15-day free trial waiting for you!

If you are using the V2 Compatibility module, you can also enable webhooks for the V2 Compatibility layer.

1. SSH into one of your Master Nodes (or Single Node).
2. Add to the file `v2compatibility.env` the following parameters:

    ```
    V2COMPAT_OPENVIDU_WEBHOOK=true
    V2COMPAT_OPENVIDU_WEBHOOK_ENDPOINT=https://<YOUR_WEBHOOK_URL>
    ```

    Where `<YOUR_WEBHOOK_URL>` is the URL where you want to receive the notifications.

    Check in the [Configuration Reference](/docs/self-hosting/configuration/reference/#pro-v2compatibilityenv){:target=_blank} all the webhook events that you can receive setting up the parameter `V2COMPAT_OPENVIDU_WEBHOOK_EVENTS`.
