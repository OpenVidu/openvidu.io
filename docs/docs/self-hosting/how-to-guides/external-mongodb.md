---
description: Configure OpenVidu to use an external MongoDB deployment instead of the bundled database instance.
---

# Use an External MongoDB with OpenVidu

You can connect OpenVidu to a managed or self-hosted MongoDB deployment if you prefer to run the database outside of the OpenVidu deployment. This is useful when you already operate a production-ready MongoDB cluster or want to use a cloud-hosted service such as MongoDB Atlas.

When you supply an external connection string, the internal MongoDB service will be disabled automatically to avoid running two instances simultaneously. 

## Standard MongoDB deployments

### 1. Prepare the MongoDB connection string

A minimal URI looks like the following:

```text
mongodb://<USERNAME>:<PASSWORD>@<HOST>:27017/?authSource=admin?replicaSet=<REPLICA_SET_NAME>
```

You can also use `mongodb+srv://` URIs for Atlas or DNS SRV-based clusters.

### 2. Update `openvidu.env`

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

### 3. Restart OpenVidu

Restart the node so the new database configuration is applied across the deployment:

```bash
systemctl restart openvidu
```

After the restart, verify that OpenVidu services can reach the external cluster. If all services function correctly, the configuration is complete. If not, double-check the connection string and ensure that the MongoDB instance is accessible from the OpenVidu nodes.

## Amazon DocumentDB

Amazon DocumentDB is protocol-compatible with MongoDB and can be used as the external database. Create a DocumentDB cluster with a username and password that OpenVidu will use for authentication, then follow these steps:

!!! warning
    DocumentDB instances are only reachable inside the associated AWS VPC by default. Ensure that the security groups attached to the OpenVidu nodes and the DocumentDB cluster allow traffic so that the nodes can reach the database endpoint.

### 1. Download the AWS trust store

SSH into the Single Node deployment or one of the Master Nodes in an Elastic / High Availability cluster and download the AWS trust store bundle, so the services can validate the TLS certificate presented by DocumentDB:


```bash
wget -O mongodb_tls_ca.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
```

### 2. Copy the trust store to OpenVidu configuration

Place the downloaded file so OpenVidu can distribute it across services:

=== "Single Node"

    ```
    sudo mv mongodb_tls_ca.pem /opt/openvidu/config/
    ```

=== "Elastic / High Availability"

    ```
    sudo mv mongodb_tls_ca.pem /opt/openvidu/config/cluster/
    ```

### 3. Configure and restart OpenVidu

Set the `EXTERNAL_MONGO_URI` entry in `openvidu.env` to point to your DocumentDB cluster (replace placeholders with real values):

```bash
EXTERNAL_MONGO_URI=mongodb://<USERNAME>:<PASSWORD>@<CLUSTER_DOMAIN>.<AWS_REGION>.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=/config/mongodb_tls_ca.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false
```

The **`tlsCAFile=/config/mongodb_tls_ca.pem`** parameter is required because OpenVidu mounts the certificate bundle into `/config` for every service, regardless of where you copied the file initially.

Apply the configuration change by restarting OpenVidu:

```
systemctl restart openvidu
```