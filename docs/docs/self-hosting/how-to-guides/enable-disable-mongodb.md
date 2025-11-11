---
description: Learn how to enable or disable the bundled MongoDB service used by OpenVidu services such as Dashboard, Meet, and analytics storage.
---

# Enable and disable MongoDB
OpenVidu stores application data in MongoDB for these services:

- OpenVidu Dashboard
- OpenVidu Meet
- Analytics (sent by OpenVidu Server)

The bundled MongoDB service runs automatically, but you can control it with the `MONGO_ENABLED` setting in `openvidu.env`.

You may want to disable the bundled MongoDB service to just use OpenVidu Core Platform services, but these would imply that the mentioned services will be disabled as they cannot operate without a MongoDB service.

## Update `openvidu.env`

1. SSH into one of your Master Nodes (or the Single Node deployment).
2. Open the `openvidu.env` file located at:

    - **Single Node**: `/opt/openvidu/config/openvidu.env`
    - **Elastic / High Availability**: `/opt/openvidu/config/cluster/openvidu.env`

3. Set the value of `MONGO_ENABLED` depending on the behavior you want:

    ```bash
    # Enable MongoDB service and related services
    MONGO_ENABLED=true

    # Disable MongoDB service and related services
    MONGO_ENABLED=false
    ```

    If you want to use an external MongoDB, check the [Configure an external MongoDB](external-mongodb.md) guide for more details.

## Apply the change

Restart the node so the updated configuration is applied across the deployment:

```bash
systemctl restart openvidu
```

After the restart completes, confirm that the expected services (OpenVidu Dashboard, OpenVidu Meet, analytics) can connect to MongoDB.
