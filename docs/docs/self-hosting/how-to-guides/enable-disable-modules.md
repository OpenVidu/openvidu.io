---
description: Learn how to enable or disable OpenVidu modules to customize your deployment configuration.
---

# Enable and disable modules

OpenVidu allows you to enable or disable modules to customize your deployment. These modules are:

- **`openviduMeet`**: The OpenVidu Meet service.
- **`observability`**: Grafana, Loki, Mimir, and Promtail observability services.
- **`v2compatibility`**: OpenVidu V2 Compatibility. (Only available in OpenVidu Pro)

These modules are configured in the parameter `ENABLED_MODULES`.

- **Single Node**: `/opt/openvidu/config/openvidu.env`
- **Elastic / High Availability**: `/opt/openvidu/config/cluster/openvidu.env`

The environment variable `ENABLED_MODULES` will all the modules enabled would look like this:

```bash
ENABLED_MODULES=app,observability,v2compatibility
```

Simply go to one of your Master Nodes or the only node in a Single Node deployment, edit the `openvidu.env` file, modify the `ENABLED_MODULES` and restart the Master Node or the Single Node deployment with:

```bash
systemctl restart openvidu
```

## About modules configuration

If you've installed OpenVidu with all modules enabled, you may not need to change these configurations. But in case you've installed openvidu with some modules disabled, you may need to configure some parameters when enabling them.

=== "app"

    You need to configure the Livekit configuration to send webhooks to the OpenVidu V2 Compatibility service.

    === "Single Node"

        **Location:** `/opt/openvidu/config/livekit.yaml`

        ```yaml
        webhook:
            api_key: ${openvidu.LIVEKIT_API_KEY:?mandatory}
            urls:
                - http://localhost:${openvidu.DEFAULT_APP_INTERNAL_PORT:?mandatory}/livekit/webhook
        ```

        With this configuration, the Livekit service will send webhooks to the OpenVidu Meet service which is necessary.

    === "Elastic"

        **Location:** `/opt/openvidu/config/cluster/media_node/livekit.yaml`

        ```yaml
        webhook:
            api_key: ${openvidu.LIVEKIT_API_KEY:?mandatory}
            urls:
                - http://master-node:${openvidu.DEFAULT_APP_INTERNAL_PORT:?mandatory}/livekit/webhook
        ```

        With this configuration, the Livekit service will send webhooks to the OpenVidu Meet service which is necessary.

    === "High Availability"

        **Location:** `/opt/openvidu/config/cluster/media_node/livekit.yaml`

        ```yaml
        webhook:
            api_key: ${openvidu.LIVEKIT_API_KEY:?mandatory}
            urls:
                - http://localhost:${openvidu.DEFAULT_APP_INTERNAL_PORT:?mandatory}/livekit/webhook
        ```

        With this configuration, the Livekit service will send webhooks to the OpenVidu Meet service which is necessary.

=== "v2compatibility"

    You need to configure the Livekit configuration to send webhooks to the OpenVidu V2 Compatibility service.

    === "Elastic"

        **Location:** `/opt/openvidu/config/cluster/media_node/livekit.yaml`

        ```yaml
        webhook:
            api_key: ${openvidu.LIVEKIT_API_KEY:?mandatory}
            urls:
                - http://master-node:${openvidu.OPENVIDU_V2COMPAT_INTERNAL_PORT:?mandatory}/livekit/webhook
        ```

        With this configuration, the Livekit service will send webhooks to the OpenVidu V2 Compatibility service which is necessary.

    === "High Availability"

        **Location:** `/opt/openvidu/config/cluster/media_node/livekit.yaml`

        ```yaml
        webhook:
            api_key: ${openvidu.LIVEKIT_API_KEY:?mandatory}
            urls:
                - http://localhost:${openvidu.OPENVIDU_V2COMPAT_INTERNAL_PORT:?mandatory}/livekit/webhook
        ```

        With this configuration, the Livekit service will send webhooks to the OpenVidu V2 Compatibility service which is necessary.

=== "observability"

    You need the following parameters defined in the `openvidu.env` file.
    
    === "Single Node"

        **Location:** `/opt/openvidu/config/openvidu.env`

        ```bash
        GRAFANA_ADMIN_USERNAME="<GRAFANA_ADMIN_USERNAME>"
        GRAFANA_ADMIN_PASSWORD="<GRAFANA_ADMIN_PASSWORD>"
        ```

        With these parameters, you set the username and password for the Grafana admin user.
    
    === "Elastic"

        **Location:** `/opt/openvidu/config/cluster/openvidu.env`

        ```bash
        GRAFANA_ADMIN_USERNAME="<GRAFANA_ADMIN_USERNAME>"
        GRAFANA_ADMIN_PASSWORD="<GRAFANA_ADMIN_PASSWORD>"
        ```

        With these parameters, you set the username and password for the Grafana admin user.

    === "High Availability"

        **Location:** `/opt/openvidu/config/cluster/openvidu.env`

        ```bash
        GRAFANA_ADMIN_USERNAME="<GRAFANA_ADMIN_USERNAME>"
        GRAFANA_ADMIN_PASSWORD="<GRAFANA_ADMIN_PASSWORD>"
        ```

        With these parameters, you set the username and password for the Grafana admin user.


These configurations should be valid just by copying and pasting them into the `livekit.yaml` file. If you want to understand the `${openvidu.VARIABLE:?mandatory}` syntax, please refer to the [Configuration](../configuration/in-depth.md) section.

## Troubleshooting

On any problem, check these sections:

- [Config Troubleshooting](../configuration/changing-config.md#troubleshooting-configuration)
- Status and Checking Logs sections of Administration sections of each deployment type:
    - [Single Node](../single-node/on-premises/admin.md#checking-the-status-of-services)
    - [Elastic](../elastic/on-premises/admin.md#checking-the-status-of-services)
    - [High Availability](../ha/on-premises/admin.md#checking-the-status-of-services)
