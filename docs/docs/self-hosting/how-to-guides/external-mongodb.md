---
title: "Use an external MongoDB with OpenVidu"
description: "Point OpenVidu at a MongoDB deployment you already run instead of the bundled instance, configured with the OpenVidu CLI."
---

# Use an External MongoDB with OpenVidu

You can connect OpenVidu to a managed or self-hosted MongoDB deployment if you prefer to run the database outside of the OpenVidu deployment. This is useful when you already operate a production-ready MongoDB cluster or want to use a cloud-hosted service such as MongoDB Atlas.

When you supply an external connection string, the bundled MongoDB service is not started, to avoid running two instances simultaneously.

## Standard MongoDB deployments

### 1. Prepare the MongoDB connection string

A minimal URI looks like the following:

```text
mongodb://<USERNAME>:<PASSWORD>@<HOST>:27017/?authSource=admin&replicaSet=<REPLICA_SET_NAME>
```

You can also use `mongodb+srv://` URIs for Atlas or DNS SRV-based clusters.

### 2. Set the connection string

Set the external connection string with [`ov stack config set`](../configuration/changing-config.md#view-get-set-unset), which applies the change and recreates only the affected services:

```bash
ov stack config set EXTERNAL_MONGO_URI='mongodb://<USERNAME>:<PASSWORD>@<HOST>:27017/openvidu?authSource=admin'
```

After the change is applied, verify with `ov stack status` that OpenVidu services can reach the external cluster. If a service cannot connect, double-check the connection string and ensure that the MongoDB instance is reachable from the OpenVidu nodes.

## Amazon DocumentDB

Amazon DocumentDB is protocol-compatible with MongoDB and can be used as the external database. Create a DocumentDB cluster with a username and password that OpenVidu will use for authentication, then follow these steps:

!!! warning
    DocumentDB instances are only reachable inside the associated AWS VPC by default. Ensure that the security groups attached to the OpenVidu nodes and the DocumentDB cluster allow traffic so that the nodes can reach the database endpoint.

### 1. Download the AWS trust store

DocumentDB presents a TLS certificate signed by the AWS global trust store. Download the bundle so the services can validate it:

```bash
wget -O mongodb_tls_ca.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
```

### 2. Give the trust store to the services

On a **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } Single Node server, SSH into the node and copy the downloaded file next to the deployment:

```bash
sudo mv mongodb_tls_ca.pem /opt/openvidu/mongodb_tls_ca.pem
```

Each service only sees its own configuration, so mount the file into the three services that connect to MongoDB. Add them to `/opt/openvidu/docker-compose.override.yaml`, the file of your own additions that `ov` never rewrites ([Emergency overrides](../configuration/in-depth.md#emergency-overrides)):

```yaml
services:
  ov-livekit-server:
    volumes:
      - ./mongodb_tls_ca.pem:/certs/mongodb_tls_ca.pem:ro
  ov-dashboard:
    volumes:
      - ./mongodb_tls_ca.pem:/certs/mongodb_tls_ca.pem:ro
  ov-meet:
    volumes:
      - ./mongodb_tls_ca.pem:/certs/mongodb_tls_ca.pem:ro
```

!!! note "PRO deployments"

    OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag } stacks (Single Node PRO, Elastic and High Availability) run on Kubernetes and have no such file on the nodes. How to add a custom CA bundle so the OpenVidu services trust it on a PRO stack deployed with `ov` is not documented yet.

### 3. Configure and apply

Point `EXTERNAL_MONGO_URI` at your DocumentDB cluster, referencing the trust store at the path it is mounted at (`/certs/mongodb_tls_ca.pem`):

```bash
ov stack config set EXTERNAL_MONGO_URI='mongodb://<USERNAME>:<PASSWORD>@<CLUSTER_DOMAIN>.<AWS_REGION>.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=/certs/mongodb_tls_ca.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
```

Then restart the stack, so every service starts with the new mount:

```bash
ov stack restart
```
