---
description: Configure OpenVidu to use an external MongoDB deployment instead of the bundled database instance.
---

# Configure an external MongoDB

You can connect OpenVidu to a managed or self-hosted MongoDB deployment if you prefer to run the database outside of the OpenVidu deployment. This is useful when you already operate a production-ready MongoDB cluster or want to use a cloud-hosted service such as MongoDB Atlas.

When you supply an external connection string, the internal MongoDB service will be disabled automatically to avoid running two instances simultaneously.

## Prepare the MongoDB connection string

A minimal URI looks like the following:

```text
mongodb://<USERNAME>:<PASSWORD>@<HOST>:27017/?authSource=admin?replicaSet=<REPLICA_SET_NAME>
```

You can also use `mongodb+srv://` URIs for Atlas or DNS SRV-based clusters.

## Update `openvidu.env`

1. SSH into one of your Master Nodes (or the Single Node deployment).
2. Open the `openvidu.env` file located at:

    - **Single Node**: `/opt/openvidu/config/openvidu.env`
    - **Elastic / High Availability**: `/opt/openvidu/config/cluster/openvidu.env`

3. Provide the external connection string at `EXTERNAL_MONGO_URI` and let `MONGO_ENABLED` set to `true`:

    ```bash
    MONGO_ENABLED=true
    EXTERNAL_MONGO_URI=mongodb://<USERNAME>:<PASSWORD>@<HOST>:27017/openvidu?authSource=admin
    ```

   Do not use quotation marks around the connection string.

## Apply the change

Restart the node so the new database configuration is applied across the deployment:

```bash
systemctl restart openvidu
```

After the restart, verify that OpenVidu services can reach the external cluster. If all services function correctly, the configuration is complete. If not, double-check the connection string and ensure that the MongoDB instance is accessible from the OpenVidu nodes.
