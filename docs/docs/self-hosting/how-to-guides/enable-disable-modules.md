---
description: Learn how to enable or disable OpenVidu modules to customize your deployment configuration.
---

# Enable and disable modules

OpenVidu allows you to enable or disable modules to customize your deployment. These modules are:

- **`app`**: The OpenVidu Default App (OpenVidu Call)
- **`observability`**: Grafana, Loki, Mimir, and Promtail observability services.
- **`v2compatibility`**: OpenVidu V2 Compatibility. (Only available in OpenVidu Pro)

These modules are configured in the parameter `COMPOSE_PROFILES` at:

- **Single Node**: `/opt/openvidu/config/openvidu.env`
- **Elastic / High Availability**:
    - `Master Node`: `/opt/openvidu/config/cluster/node/master_node.env`
    - `Media Node`: `/opt/openvidu/config/cluster/node/media_node.env`

This parameter is one of the parameters that is not replicated per node in the cluster. To enable or disable a module, you need to modify the parameter in all the nodes where you want to apply the changes.

For example, to enable only `v2compatibility` and `app`, the parameter should look like this:

```bash
COMPOSE_PROFILES=app,v2compatibility
```

After modifying the parameter, you need to restart the node to apply the changes:

```bash
systemctl restart openvidu
```
