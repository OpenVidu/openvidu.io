# Backup and restore OpenVidu deployments

## Overview

Keeping reliable backups of your OpenVidu data guarantees that recordings, observability metrics, operational statistics, and OpenVidu Meet data survive unexpected update failures or planned migrations. The **most critical data to protect** in any OpenVidu deployment is located on the node of your installation: on the single node of a Single Node deployment, or on any master node of Elastic and High Availability deployments. Specifically:

- **OpenVidu deployment files** (`/opt/openvidu/`). You may want to back them up to preserve specific configurations. Specifically:

  - `/opt/openvidu/config/`: main configuration files for OpenVidu Platform and OpenVidu Meet.
  - `/opt/openvidu/docker-compose.yaml` and `/opt/openvidu/docker-compose.override.yaml`: Docker Compose files that define the services.

  They can be regenerated in new installations, but you lose any custom settings on every reinstallation.

- **OpenVidu data** (`/opt/openvidu/data/`): persistent data stored by OpenVidu services. The most relevant data is:

  - **OpenVidu Platform Data**
    - S3: egress outputs such as recordings.
    - MongoDB: statistics for rooms, egress, and ingress operations.
  - **OpenVidu Meet Data**
    - S3-compatible storage: meeting recordings.
    - MongoDB: rooms, users, permissions, and recording links.

You can back up and restore OpenVidu deployments using one of the following four methods, depending on your infrastructure capabilities and backup requirements:

1. Direct snapshots of OpenVidu nodes via your infrastructure provider.
1. File-level snapshots of `/opt/openvidu/` on master nodes.
1. Only backup data from MinIO/S3 and MongoDB.
1. Only snapshots provided by external services used for S3 or MongoDB.

## Which backup method should I use?

First, identify where your S3 and MongoDB services run. SSH to your OpenVidu deployment node (or any master node) and inspect these environment variables:

- `EXTERNAL_S3_ENDPOINT`: blank when MinIO runs internally within the deployment.
- `EXTERNAL_MONGO_URI`: blank when MongoDB runs internally within the deployment.

Find both variables in the OpenVidu configuration files:

- **Single Node**: `/opt/openvidu/config/openvidu.env`
- **Elastic & High Availability**: `/opt/openvidu/config/cluster/openvidu.env`

With that information, pick the backup approach that best fits your scenario:

| Scenario & use cases                                                                                                                                                                                                                                                                                                                    | Recommended method                                                                                                                                             |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - You are using S3 (MinIO) and MongoDB internally with your deployment. - Your infrastructure provider allows VM snapshots. - You need a fast copy of the entire machine with all deployment data. - Ideal for quick rollbacks after failed upgrades or OS patching. - Great when compliance requires full-system images on a schedule. | [Method 1: Direct snapshots of OpenVidu nodes via your infrastructure provider](#method-1-direct-snapshots-of-openvidu-nodes-via-your-infrastructure-provider) |
| - You are using S3 (MinIO) and MongoDB internally with your deployment. - Your infrastructure provider or hypervisor does not allow VM snapshots. - You only want to save the OpenVidu deployment config and data, not the full VM.                                                                                                     | [Method 2: File-level snapshots of `/opt/openvidu/` on master nodes](#method-2-file-level-snapshots-of-optopenvidu-on-master-nodes)                            |
| - You are using S3 (MinIO) and MongoDB internally with your deployment. - You just want to back up OpenVidu Platform and OpenVidu Meet data. - You want to move your S3/MinIO and MongoDB data to a new OpenVidu installation.                                                                                                          | [Method 3: Only backup data from MinIO/S3 and MongoDB](#method-3-only-backup-data-from-minios3-and-mongodb)                                                    |
| - You are using external S3 and MongoDB services in your deployment. - You just want to back up OpenVidu Platform and OpenVidu Meet data. - You want to reduce operational overhead by delegating data backups.                                                                                                                         | [Method 4: Only snapshots provided by external services used for S3 or MongoDB](#method-4-only-snapshots-provided-by-external-services-used-for-s3-or-mongodb) |

## Method 1: Direct snapshots of OpenVidu nodes via your infrastructure provider

If you deploy OpenVidu on a cloud provider **without externalizing S3 or MongoDB**, snapshotting the compute nodes that host those services is enough. This approach captures the entire installation, including the disks where MinIO and MongoDB store their data.

1. Identify the nodes:
   - **Single Node**: snapshot the VM that runs the whole stack.
   - **Elastic & High Availability**: snapshot every master node. Media nodes can be reprovisioned because they do not keep stateful data.
1. Follow your cloud provider's snapshot workflow:
   - AWS: Check [Amazon EBS snapshots](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-snapshots.html) and [Amazon Machine Images (AMIs)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) .
   - Azure: Check [VM backups from VM settings](https://learn.microsoft.com/en-us/azure/backup/backup-azure-vms-first-look-arm) .
   - Google Cloud: Check [Backup and DR Service for Compute Engine instances and disks](https://docs.cloud.google.com/backup-disaster-recovery/docs/concepts/backupdr-for-compute-engine?hl=en) .
   - DigitalOcean: Check [Snapshots](https://docs.digitalocean.com/products/snapshots/) .
   - Oracle Cloud: Check [Block volume backups](https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/blockvolumebackups.htm) .
1. Automate snapshots using your provider's scheduler (AWS Backup, Azure Automation, Cloud Scheduler, DigitalOcean snapshot policies, OCI backup policies) for consistent recovery points.
1. Restore by cloning a new node from the snapshot/AMI and updating DNS or load balancer targets.
1. Check the [After restore](#after-restore) section to verify everything works correctly.

## Method 2: File-level snapshots of `/opt/openvidu/` on master nodes

When you still host MinIO and MongoDB inside the OpenVidu nodes but lack hypervisor or cloud-level snapshots, you can capture the full application state by backing up `/opt/openvidu/` with [restic](https://restic.net/) . This directory includes OpenVidu configuration, MinIO data, and MongoDB volumes for deployments that keep everything local to the master nodes.

Run the following procedure on **each master node** in Single Node or Elastic/HA deployments. Media nodes do not require backups because they do not keep stateful data.

### Prerequisites

- A [compatible backend storage for restic](https://restic.readthedocs.io/en/v0.18.1/030_preparing_a_new_repo.html) .
- Enough free space in the backend to hold the backups. The first snapshot will be a full copy of `/opt/openvidu/`, while subsequent snapshots will only store incremental changes.

Warning

Backing up `/opt/openvidu/` in HA environments using this method requires enough disk space to hold independent snapshots from every master node. Each snapshot contains the full MinIO and MongoDB datasets from that specific node, which may lead to significant storage requirements.

### Backup and Restore example

In this example, we use an [S3-compatible object storage](https://restic.readthedocs.io/en/v0.18.1/030_preparing_a_new_repo.html#amazon-s3) service as the restic backend. You can adapt the commands if you prefer another supported backend.

First, export reusable variables once per shell session on each master node. Adjust the repository URL, credentials, and cache paths to match your environment:

```bash
export RESTIC_REPOSITORY="s3:https://backup.example.com/openvidu-backups"
export RESTIC_PASSWORD="<RESTIC_PASSWORD>"
export OV_RESTIC_CACHE="/var/lib/openvidu-backups-restic/cache"
export AWS_ACCESS_KEY_ID="<BACKUP_S3_ACCESS_KEY>"
export AWS_SECRET_ACCESS_KEY="<BACKUP_S3_SECRET_KEY>"
export AWS_DEFAULT_REGION="<S3_REGION>"
```

- `RESTIC_REPOSITORY`: S3 endpoint where the restic backup repository will be stored. Use the HTTPS URL for managed S3 or the HTTP/HTTPS URL of your external MinIO instance (for example, `s3:https://s3.amazonaws.com/<bucket>` or `s3:http://minio-backup.local:9000/<bucket>`).
- `RESTIC_PASSWORD`: Use a strong password. Keep it safe; it encrypts the restic backup repository and is required for restores.
- `RESTIC_HOST_TAG`: Unique identifier for the node (for example, its hostname or IP address). With this tag, you can differentiate snapshots from multiple master nodes for HA deployments. **You need to use a different value on every master node**.
- `OV_RESTIC_CACHE`: Local path to store restic cache data.
- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`: Credentials that grant access to the backup bucket in the external S3-compatible service.
- `AWS_DEFAULT_REGION`: Required by some S3 providers (including AWS). For MinIO you can set any placeholder value (for example, `us-east-1`).

**Backup**

For each master node, SSH into the node and perform the following steps:

1. Export the variables defined above.

1. Define the `RESTIC_HOST_TAG` variable with a unique identifier for the node. It can be any string but ensure it differs between nodes. For example:

   **Single Node**

   ```bash
   export RESTIC_HOST_TAG="single-node"
   ```

   **Elastic**

   ```bash
   export RESTIC_HOST_TAG="master-node"
   ```

   **High Availability**

   ```bash
   export RESTIC_HOST_TAG="master-node-1"
   # export RESTIC_HOST_TAG="master-node-2"
   # export RESTIC_HOST_TAG="master-node-3"
   # ... repeat for every master node
   ```

1. Prepare the cache directory (first run only):

   ```bash
   sudo mkdir -p "$OV_RESTIC_CACHE"
   sudo chmod 700 "$OV_RESTIC_CACHE"
   ```

1. Initialize the repository the first time you run the backup (skip on subsequent runs):

   ```bash
   sudo docker run --rm \
       -v "$OV_RESTIC_CACHE":/root/.cache/restic \
       -e RESTIC_REPOSITORY="$RESTIC_REPOSITORY" \
       -e RESTIC_PASSWORD="$RESTIC_PASSWORD" \
       -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
       -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
       -e AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION" \
       restic/restic:latest init
   ```

   Ensure the S3 or MinIO bucket exists beforehand and that the access key has permissions to create objects within it.

1. Create a snapshot of `/opt/openvidu/`:

   ```bash
   sudo docker run --rm \
       --hostname "$RESTIC_HOST_TAG" \
       -v "$OV_RESTIC_CACHE":/root/.cache/restic \
       -v /opt/openvidu:/opt/openvidu:ro \
       -e RESTIC_REPOSITORY="$RESTIC_REPOSITORY" \
       -e RESTIC_PASSWORD="$RESTIC_PASSWORD" \
       -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
       -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
       -e AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION" \
       restic/restic:latest backup /opt/openvidu \
           --host "${RESTIC_HOST_TAG:?mandatory}" \
           --tag openvidu \
           --tag master
   ```

   Restic deduplicates the directory tree against previous runs and stores the snapshot in the remote S3-compatible repository. Repeat this step on every master node to keep their states independent.

1. Verify the snapshot and capture its ID for future restores:

   ```bash
   sudo docker run --rm \
       -v "$OV_RESTIC_CACHE":/root/.cache/restic \
       -e RESTIC_REPOSITORY="$RESTIC_REPOSITORY" \
       -e RESTIC_PASSWORD="$RESTIC_PASSWORD" \
       -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
       -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
       -e AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION" \
       restic/restic:latest snapshots --host "${RESTIC_HOST_TAG:?mandatory}"
   ```

1. Repeat the backup procedure on every master node.

**Restore**

For each master node, SSH into the node and perform the following steps:

1. Stop all master nodes. Execute this on every master node before proceeding with the restore:

   ```bash
   sudo systemctl stop openvidu
   ```

1. Export the same variables used during backups. Stop OpenVidu services before restoring data.

1. Define the `RESTIC_HOST_TAG` variable with a unique identifier for the node. It can be any string but ensure it differs between nodes. For example:

   **Single Node**

   ```bash
   export RESTIC_HOST_TAG="single-node"
   ```

   **Elastic**

   ```bash
   export RESTIC_HOST_TAG="master-node"
   ```

   **High Availability**

   ```bash
   export RESTIC_HOST_TAG="master-node-1"
   # export RESTIC_HOST_TAG="master-node-2"
   # export RESTIC_HOST_TAG="master-node-3"
   # ... repeat for every master node
   ```

1. Review available snapshots for the node:

   ```bash
   sudo docker run --rm \
       -v "$OV_RESTIC_CACHE":/root/.cache/restic \
       -e RESTIC_REPOSITORY="$RESTIC_REPOSITORY" \
       -e RESTIC_PASSWORD="$RESTIC_PASSWORD" \
       -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
       -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
       -e AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION" \
       restic/restic:latest snapshots --host "${RESTIC_HOST_TAG:?mandatory}"
   ```

1. Restore the desired snapshot to a temporary directory (replace `<SNAPSHOT_ID>` with the ID you selected):

   Remove any previous restore data and create a fresh directory:

   ```bash
   sudo rm -rf /tmp/openvidu-restore
   sudo mkdir -p /tmp/openvidu-restore
   ```

   Export the snapshot ID you want to restore:

   ```bash
   export SNAPSHOT_ID="<SNAPSHOT_ID>"
   ```

   ```bash
   sudo docker run --rm \
       -v "$OV_RESTIC_CACHE":/root/.cache/restic \
       -v /tmp/openvidu-restore:/restore \
       -e RESTIC_REPOSITORY="$RESTIC_REPOSITORY" \
       -e RESTIC_PASSWORD="$RESTIC_PASSWORD" \
       -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
       -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
       -e AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION" \
       restic/restic:latest restore "$SNAPSHOT_ID" \
           --host "${RESTIC_HOST_TAG:?mandatory}" \
           --target /restore
   ```

   Restic recreates `/tmp/openvidu-restore/opt/openvidu/` with the contents from the snapshot.

1. With OpenVidu still stopped, remove the existing `/opt/openvidu/` directory to prepare for the restore:

   ```bash
   sudo rm -rf /opt/openvidu/
   ```

1. Synchronize the restored data back to `/opt/openvidu/` and preserve permissions:

   ```bash
   sudo rsync -aHAX /tmp/openvidu-restore/opt/openvidu/ /opt/openvidu/
   ```

1. Restart the OpenVidu services and verify that MinIO, MongoDB, and the platform components start correctly. Remove `/tmp/openvidu-restore` once the restoration is validated.

   ```bash
   sudo systemctl start openvidu
   sudo rm -rf /tmp/openvidu-restore
   ```

1. Repeat the restore procedure on every master node if needed.

1. Check the [After restore](#after-restore) section to verify everything works correctly.

## Method 3: Only backup data from MinIO/S3 and MongoDB

Generate portable snapshots using [restic](https://restic.net/) when you need point-in-time backups of MinIO objects and MongoDB collections. Run these backups from an **external machine with enough disk space** (for example, a bastion host or operations workstation) that can reach your OpenVidu network.

### Prerequisites

- A separate machine with network access to OpenVidu. Ports 9100 TCP (MinIO) and 20000 TCP (MongoDB) must be reachable from the backup machine to the OpenVidu deployment node or master nodes.

  Info

  You can run the backup commands from any OpenVidu node or master node, but it is **not recommended** because it adds load to production services and it requires extra disk space on those nodes to stage the backup data.

- Enough disk space on the backup machine to stage at least one full copy of your MinIO buckets and MongoDB dump before uploading to S3.

- A [compatible backend storage for restic](https://restic.readthedocs.io/en/v0.18.1/030_preparing_a_new_repo.html) .

Export the following variables once on your backup machine so that every command reuses the same paths and credentials:

```bash
export OV_BACKUP_DIR="$HOME/openvidu-backups"
export OPENVIDU_NODE_IP="<OPENVIDU_NODE_IP>"
export MONGO_ADMIN_USER="<MONGO_ADMIN_USER>"
export MONGO_ADMIN_PASSWORD="<MONGO_ADMIN_PASSWORD>"
# The following are only needed if you are using the default MinIO instance
# that comes with OpenVidu deployments. If you are using AWS S3
# or any other external S3-compatible service, skip these two variables.
export MINIO_ADMIN_USER="<MINIO_ADMIN_USER>"
export MINIO_ADMIN_PASSWORD="<MINIO_ADMIN_PASSWORD>"
# If you are using AWS S3, use the appropriate endpoint, e.g.:
# export RESTIC_REPOSITORY="s3:https://s3.amazonaws.com/<bucket>"
export RESTIC_REPOSITORY="s3:https://backup.example.com/openvidu-data"
export RESTIC_PASSWORD="<RESTIC_PASSWORD>"
export RESTIC_HOST_TAG="openvidu-data-backups"
export AWS_ACCESS_KEY_ID="<BACKUP_S3_ACCESS_KEY>"
export AWS_SECRET_ACCESS_KEY="<BACKUP_S3_SECRET_KEY>"
export AWS_DEFAULT_REGION="<S3_REGION>"
```

Replace the placeholders with values from your deployment. All credentials are available in the `openvidu.env` file(s).

About the exported variables:

- `<OPENVIDU_NODE_IP>`: IP address used to reach the OpenVidu node from the backup machine. In Single Node deployments this is the node’s own IP; in Elastic/HA deployments use the IP of any master node.
- `<MONGO_ADMIN_USER>` and `<MONGO_ADMIN_PASSWORD>`: MongoDB admin credentials (`MONGO_ADMIN_USERNAME`, `MONGO_ADMIN_PASSWORD`).
- `<MINIO_ADMIN_USER>` and `<MINIO_ADMIN_PASSWORD>`: MinIO credentials (`MINIO_ADMIN_USERNAME`, `MINIO_ADMIN_PASSWORD`). Use them only if you are using the default MinIO instance that comes with OpenVidu deployments. If you are using AWS S3 or any other external S3-compatible service, skip these two variables.
- `RESTIC_REPOSITORY`: S3 endpoint where the encrypted restic backup repository will live (for example, `s3:https://s3.amazonaws.com/<bucket>` or `s3:http://minio-backup.local:9000/<bucket>`).
- `RESTIC_PASSWORD`: Strong password that encrypts the restic backup repository. Keep it safe; you need it for every restore.
- `RESTIC_HOST_TAG`: Label that identifies the host in restic snapshots. Adjust it if you manage several OpenVidu environments from the same backup machine.
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_DEFAULT_REGION`: Credentials and region required by your S3-compatible provider.

### Backup and Restore

**Backup**

1. Prepare the staging directories (first run only):

   ```bash
   mkdir -p "$OV_BACKUP_DIR/backup/s3" "$OV_BACKUP_DIR/backup/mongodb"
   ```

1. Initialize the remote restic backup repository the first time you run the backup:

   ```bash
   docker run --rm \
       -e RESTIC_REPOSITORY="$RESTIC_REPOSITORY" \
       -e RESTIC_PASSWORD="$RESTIC_PASSWORD" \
       -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
       -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
       -e AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION" \
       restic/restic:latest init
   ```

   Ensure the bucket exists and that the credentials can create objects before running the command.

1. Dump MongoDB data into the staging directory:

   ```bash
   # Remove previous dumps
   sudo rm -rf "$OV_BACKUP_DIR/backup/mongodb/dump"

   # Create dump directory with correct permissions
   mkdir -p "$OV_BACKUP_DIR/backup/mongodb"
   sudo chown 999:999 "$OV_BACKUP_DIR/backup/mongodb"

   # Dump all databases with oplog for point-in-time recovery
   sudo docker run --rm \
       --network host \
       -v "$OV_BACKUP_DIR/backup/mongodb":/backup \
       mongo:latest mongodump \
           --host "${OPENVIDU_NODE_IP}" \
           --port 20000 \
           --username "${MONGO_ADMIN_USER}" \
           --password "${MONGO_ADMIN_PASSWORD}" \
           --out /backup/dump \
           --oplog

   # Remove admin database dump to avoid restoring users/roles
   sudo rm -rf "$OV_BACKUP_DIR/backup/mongodb/dump/admin"
   ```

   Warning

   Store your current Meet Admin user and password safely; you will need them to access OpenVidu Meet after the restore.

   Warning

   Note that admin database users and roles are not backed up with this method. If you need to back them up, remove the last `rm -rf` command, but ensure your new installation has the same admin user for the restore to work.

1. Mirror S3 buckets to the staging directory:

   **MinIO**

   If you are using the default MinIO instance that comes with OpenVidu deployments, run:

   ```bash
   sudo docker run --rm \
       --network host \
       --user "$(id -u):$(id -g)" \
       -e MC_CONFIG_DIR="/tmp/.mc" \
       -v "$OV_BACKUP_DIR/backup/s3":/backup \
       --entrypoint sh \
       minio/mc:latest -c "\
           mc alias set openvidu http://${OPENVIDU_NODE_IP}:9100 ${MINIO_ADMIN_USER} ${MINIO_ADMIN_PASSWORD} && \
           mc ls openvidu | while IFS= read -r line; do \
               bucket=\${line##* } && bucket=\${bucket%/} && [ -n \"\${bucket}\" ] && \
               mc mirror --overwrite openvidu/\${bucket} /backup/\${bucket}; \
           done \
       "
   ```

   **AWS/External S3**

   If you are using AWS S3 or any S3-compatible service (other than MinIO), run:

   ```bash
   # Export OpenVidu S3 credentials and region
   export OPENVIDU_AWS_ACCESS_KEY_ID=<YOUR_S3_ACCESS_KEY>
   export OPENVIDU_AWS_SECRET_ACCESS_KEY=<YOUR_S3_SECRET_KEY>
   export OPENVIDU_AWS_DEFAULT_REGION=<YOUR_S3_REGION>
   export OPENVIDU_S3_ENDPOINT="https://s3.${OPENVIDU_AWS_DEFAULT_REGION}.amazonaws.com"

   # The name of these buckets can be found in the openvidu.env file as
   # EXTERNAL_S3_BUCKET_APP_DATA and EXTERNAL_S3_BUCKET_CLUSTER_DATA
   export EXTERNAL_S3_BUCKET_APP_DATA="openvidu-appdata-xxxxx"

   # (Optional) EXTERNAL_S3_BUCKET_CLUSTER_DATA is only needed for High Availability deployments
   # and usually can be skipped because it only contains internal metrics cluster data.
   export EXTERNAL_S3_BUCKET_CLUSTER_DATA="openvidu-clusterdata-xxxxx"

   # Backup application data bucket
   sudo docker run --rm \
       --user "$(id -u):$(id -g)" \
       -v "$OV_BACKUP_DIR/backup/s3":/backup \
       -e AWS_ACCESS_KEY_ID="$OPENVIDU_AWS_ACCESS_KEY_ID" \
       -e AWS_SECRET_ACCESS_KEY="$OPENVIDU_AWS_SECRET_ACCESS_KEY" \
       -e AWS_DEFAULT_REGION="$OPENVIDU_AWS_DEFAULT_REGION" \
       amazon/aws-cli s3 sync \
           --endpoint-url "$OPENVIDU_S3_ENDPOINT" \
           "s3://${EXTERNAL_S3_BUCKET_APP_DATA}" "/backup/openvidu-appdata"

   # Optional: Cluster data bucket for HA deployments
   sudo docker run --rm \
       --user "$(id -u):$(id -g)" \
       -v "$OV_BACKUP_DIR/backup/s3":/backup \
       -e AWS_ACCESS_KEY_ID="$OPENVIDU_AWS_ACCESS_KEY_ID" \
       -e AWS_SECRET_ACCESS_KEY="$OPENVIDU_AWS_SECRET_ACCESS_KEY" \
       -e AWS_DEFAULT_REGION="$OPENVIDU_AWS_DEFAULT_REGION" \
       amazon/aws-cli s3 sync \
           --endpoint-url "$OPENVIDU_S3_ENDPOINT" \
           "s3://${EXTERNAL_S3_BUCKET_CLUSTER_DATA}" "/backup/openvidu-clusterdata"
   ```

1. Create a restic snapshot of the staged data and push it to S3:

   ```bash
   sudo docker run --rm \
       --hostname "$RESTIC_HOST_TAG" \
       -v "$OV_BACKUP_DIR/backup":/backup:ro \
       -e RESTIC_REPOSITORY="$RESTIC_REPOSITORY" \
       -e RESTIC_PASSWORD="$RESTIC_PASSWORD" \
       -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
       -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
       -e AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION" \
       restic/restic:latest backup /backup \
           --host "${RESTIC_HOST_TAG:?mandatory}" \
           --tag openvidu \
           --tag data
   ```

   Restic uploads only the changed files thanks to its built-in deduplication. Remove the contents of `$OV_BACKUP_DIR/backup/` after each successful run if you want to reclaim local disk space.

1. Verify the snapshot and capture the ID for future restores:

   ```bash
   sudo docker run --rm \
       -e RESTIC_REPOSITORY="$RESTIC_REPOSITORY" \
       -e RESTIC_PASSWORD="$RESTIC_PASSWORD" \
       -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
       -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
       -e AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION" \
       restic/restic:latest snapshots --host "${RESTIC_HOST_TAG:?mandatory}"
   ```

**Restore**

1. Ensure the same environment variables used for backups are exported on the restore machine.

1. List the available snapshots and pick the one you want to recover:

   ```bash
   sudo docker run --rm \
       -e RESTIC_REPOSITORY="$RESTIC_REPOSITORY" \
       -e RESTIC_PASSWORD="$RESTIC_PASSWORD" \
       -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
       -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
       -e AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION" \
       restic/restic:latest snapshots --host "${RESTIC_HOST_TAG:?mandatory}"
   ```

1. Restore the snapshot contents into a local staging directory (replace `<SNAPSHOT_ID>` with the ID selected above):

   ```bash
   # Clean previous restore data
   sudo rm -rf "$OV_BACKUP_DIR/restore"
   # Create fresh restore directory
   mkdir -p "$OV_BACKUP_DIR/restore"

   # Export the snapshot ID to restore
   export SNAPSHOT_ID="<SNAPSHOT_ID>"

   # Restore snapshot
   sudo docker run --rm \
       -v "$OV_BACKUP_DIR/restore":/restore \
       -e RESTIC_REPOSITORY="$RESTIC_REPOSITORY" \
       -e RESTIC_PASSWORD="$RESTIC_PASSWORD" \
       -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
       -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
       -e AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION" \
       restic/restic:latest restore "$SNAPSHOT_ID" --target /restore \
           --host "${RESTIC_HOST_TAG:?mandatory}"
   ```

   The folder now contains `backup/minio/` and `backup/mongodb/` with the data captured in that snapshot.

1. Restore MongoDB from the extracted dump:

   ```bash
   sudo docker run --rm \
       --network host \
       -v "$OV_BACKUP_DIR/restore/backup/mongodb":/backup \
       mongo:latest mongorestore \
           --host "${OPENVIDU_NODE_IP}" \
           --port 20000 \
           --username "${MONGO_ADMIN_USER}" \
           --password "${MONGO_ADMIN_PASSWORD}" \
           --authenticationDatabase admin \
           --drop \
           /backup/dump
   ```

   The `--drop` flag removes existing collections before importing the backup, guaranteeing an exact rollback to the selected snapshot.

   Warning

   If the command fails with the following error in HA deployments...

   ```text
   Failed: openvidu.events: error dropping collection: (NotWritablePrimary) not primary
   ```

   ... try executing it with a different `OPENVIDU_NODE_IP` that points to another master node in HA deployments until it succeeds.

1. Restore S3 objects by mirroring the buckets back into OpenVidu:

   **MinIO**

   ```bash
   docker run --rm \
       --network host \
       --user "$(id -u):$(id -g)" \
       -e MC_CONFIG_DIR="/tmp/.mc" \
       -v "$OV_BACKUP_DIR/restore/backup/s3":/backup \
       --entrypoint sh \
       minio/mc:latest -c "
           set -e
           mc alias set openvidu http://${OPENVIDU_NODE_IP}:9100 ${MINIO_ADMIN_USER} ${MINIO_ADMIN_PASSWORD}
           for bucket in /backup/*; do
               [ -d \"\$bucket\" ] || continue
               mc mirror --overwrite \"\$bucket\" \"openvidu/\${bucket##*/}\"
           done
       "
   ```

   **AWS/External S3**

   ```bash
   # Export OpenVidu S3 credentials and region
   export OPENVIDU_AWS_ACCESS_KEY_ID=<YOUR_S3_ACCESS_KEY>
   export OPENVIDU_AWS_SECRET_ACCESS_KEY=<YOUR_S3_SECRET_KEY>
   export OPENVIDU_AWS_DEFAULT_REGION=<YOUR_S3_REGION>
   export OPENVIDU_S3_ENDPOINT="https://s3.${OPENVIDU_AWS_DEFAULT_REGION}.amazonaws.com"

   # The name of these buckets can be found in the openvidu.env file as
   # EXTERNAL_S3_BUCKET_APP_DATA and EXTERNAL_S3_BUCKET_CLUSTER_DATA
   export EXTERNAL_S3_BUCKET_APP_DATA="openvidu-appdata-xxxxx"
   # (Optional) EXTERNAL_S3_BUCKET_CLUSTER_DATA is only needed for High Availability deployments
   # and usually can be skipped because it only contains internal metrics cluster data.
   export EXTERNAL_S3_BUCKET_CLUSTER_DATA="openvidu-clusterdata-xxxxx"

   # Backup application data bucket
   sudo docker run --rm \
       --user "$(id -u):$(id -g)" \
       -v "$OV_BACKUP_DIR/restore/backup/s3":/backup \
       -e AWS_ACCESS_KEY_ID="$OPENVIDU_AWS_ACCESS_KEY_ID" \
       -e AWS_SECRET_ACCESS_KEY="$OPENVIDU_AWS_SECRET_ACCESS_KEY" \
       -e AWS_DEFAULT_REGION="$OPENVIDU_AWS_DEFAULT_REGION" \
       amazon/aws-cli s3 sync \
           --endpoint-url "$OPENVIDU_S3_ENDPOINT" \
           "/backup/openvidu-appdata" "s3://${EXTERNAL_S3_BUCKET_APP_DATA}"

   # Optional: Cluster data bucket for HA deployments
   sudo docker run --rm \
       --user "$(id -u):$(id -g)" \
       -v "$OV_BACKUP_DIR/restore/backup/s3":/backup \
       -e AWS_ACCESS_KEY_ID="$OPENVIDU_AWS_ACCESS_KEY_ID" \
       -e AWS_SECRET_ACCESS_KEY="$OPENVIDU_AWS_SECRET_ACCESS_KEY" \
       -e AWS_DEFAULT_REGION="$OPENVIDU_AWS_DEFAULT_REGION" \
       amazon/aws-cli s3 sync \
           --endpoint-url "$OPENVIDU_S3_ENDPOINT" \
           "/backup/openvidu-clusterdata" "s3://${EXTERNAL_S3_BUCKET_CLUSTER_DATA}"
   ```

1. (Optional) Clean the staging directories once you confirm the restore:

   ```bash
   sudo rm -rf "$OV_BACKUP_DIR/restore"
   ```

Info

If any of the MongoDB or MinIO restore commands fail, check the version compatibility between the Docker images used in the backup/restore process and the versions running in your OpenVidu deployment. You can check the versions in the [Release Notes](https://openvidu.io/3.8/docs/releases/index.md) and adjust the image tags in the `docker run` commands to match your environment.

## Method 4: Only snapshots provided by external services used for S3 or MongoDB

When you use **managed S3-compatible services or managed MongoDB providers**, rely on their built-in snapshot and backup capabilities.

- **S3/Object storage providers**

  - AWS S3: [AWS Backup for S3](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html)
  - Azure Storage: [Blob storage snapshots](https://learn.microsoft.com/azure/storage/blobs/snapshots-overview)
  - Google Cloud Storage: implement [Object Versioning and Retention](https://cloud.google.com/storage/docs/object-versioning)

- **MongoDB providers**

  - MongoDB Atlas: [Cloud backups and snapshots](https://www.mongodb.com/docs/atlas/backup/cloud-backup/snapshot-management/)
  - AWS DocumentDB: [DocumentDB Backups and snapshots](https://docs.aws.amazon.com/documentdb/latest/developerguide/backup_restore.html)
  - Azure Cosmos DB for MongoDB: [Online backup and on-demand data restore in Azure Cosmos DB](https://learn.microsoft.com/en-us/azure/cosmos-db/online-backup-and-restore)

## After restore

To ensure everything works correctly after restoring data, follow these steps:

1. **Check that the following parameters are correctly configured**:

   If you are restoring a system with new private and public IPs or domain names, ensure that the configuration files reflect the new values after the restore.

   **Single Node**

   - The `DOMAIN_NAME` in `/opt/openvidu/config/openvidu.env` reflects the correct domain name for your deployment, and the domain DNS records or load balancer point to the appropriate node.

   **Elastic**

   - The `DOMAIN_NAME` in `/opt/openvidu/config/cluster/openvidu.env` reflects the correct domain name for your deployment, and the domain DNS records or load balancer point to the appropriate master nodes.

   - Ensure that the master node has the correct private IP configured in `/opt/openvidu/config/node/master-node.env` for the `MASTER_NODE_PRIVATE_IP` variable:

     ```text
     MASTER_NODE_PRIVATE_IP=<MASTER_NODE_PRIVATE_IP>
     ```

   - Ensure that all media nodes have the correct private IP configured in `/opt/openvidu/config/node/media-node.env` for the `MEDIA_NODE_PRIVATE_IP` variable and `MASTER_NODE_PRIVATE_IP` variable is correctly set:

     ```text
     MEDIA_NODE_PRIVATE_IP=<MEDIA_NODE_PRIVATE_IP>
     MASTER_NODE_PRIVATE_IP=<MASTER_NODE_PRIVATE_IP>
     ```

   - In case you need to reinstall Media Nodes, follow [this command](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/install/#non-interactive-installation)

   **High Availability**

   - The `DOMAIN_NAME` in `/opt/openvidu/config/cluster/openvidu.env` reflects the correct domain name for your deployment, and the domain DNS records or load balancer point to the appropriate master nodes.

   - Ensure that all master nodes have the correct private IP configured in `/opt/openvidu/config/node/master-node.env` for the `MASTER_NODE_X_IP` variables:

     ```text
     MASTER_NODE_1_PRIVATE_IP=<MASTER_NODE_1_PRIVATE_IP>
     MASTER_NODE_2_PRIVATE_IP=<MASTER_NODE_2_PRIVATE_IP>
     MASTER_NODE_3_PRIVATE_IP=<MASTER_NODE_3_PRIVATE_IP>
     MASTER_NODE_4_PRIVATE_IP=<MASTER_NODE_4_PRIVATE_IP>
     ```

   - Ensure that all media nodes have the correct private IP configured in `/opt/openvidu/config/node/media-node.env` for the `MEDIA_NODE_PRIVATE_IP` variables and `MASTER_NODE_X_IP` variables are correctly set:

     ```text
     MEDIA_NODE_PRIVATE_IP=<MEDIA_NODE_PRIVATE_IP>
     MASTER_NODE_1_PRIVATE_IP=<MASTER_NODE_1_PRIVATE_IP>
     MASTER_NODE_2_PRIVATE_IP=<MASTER_NODE_2_PRIVATE_IP>
     MASTER_NODE_3_PRIVATE_IP=<MASTER_NODE_3_PRIVATE_IP>
     MASTER_NODE_4_PRIVATE_IP=<MASTER_NODE_4_PRIVATE_IP>
     ```

   - In case you need to reinstall Media Nodes, follow [this command](https://openvidu.io/3.8/docs/self-hosting/ha/on-premises/install-dlb/#non-interactive-installation)

1. **Check if all containers are running smoothly**

   ```bash
   docker ps
   ```

1. **Verify Data Integrity**: Check that recordings, observability metrics, and operational data are intact and accessible.

1. **In any cloud deployment**: If you followed [Method 1](#method-1-direct-snapshots-of-openvidu-nodes-via-your-infrastructure-provider), ensure that the restored VMs have the correct security groups, IAM roles, and network configurations.

## About restic

[Method 2](#method-2-file-level-snapshots-of-optopenvidu-on-master-nodes) and [Method 3](#method-3-only-backup-data-from-minios3-and-mongodb) use [restic](https://restic.net/) , an open-source CLI that creates encrypted, deduplicated backups to a wide range of storage backends such as S3, local disks, and SFTP servers. In this guide we call the official Docker image and use S3-compatible storage as the backend for ease of use, but you can install restic natively on your Linux distribution by following the [official installation instructions](https://restic.readthedocs.io/en/stable/020_installation.html) and use any supported backend.
