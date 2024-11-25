# Enable and Disable modules

OpenVidu allows you to enable or disable modules to customize your deployment. These modules are:

- **`app`**: The OpenVidu Default App (OpenVidu Call)
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

## Troubleshooting

On any problem, check these sections:

- [Config Troubleshooting](../configuration/changing-config.md#troubleshooting-configuration){:target="_blank"}
- Status and Checking Logs sections of Administration sections of each deployment type:
    - [Single Node](../single-node/on-premises/admin.md#checking-the-status-of-services){:target="_blank"}
    - [Elastic](../elastic/on-premises/admin.md#checking-the-status-of-services){:target="_blank"}
    - [High Availability](../ha/on-premises/admin.md#checking-the-status-of-services){:target="_blank"}
