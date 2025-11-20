---
title: Backup and restore OpenVidu deployments
description: Learn how to safeguard OpenVidu recordings, observability metrics, and operational data by backing up and restoring MinIO/S3 storage and MongoDB across all deployment models.
---

# Backup and restore OpenVidu data

Keeping reliable backups of your OpenVidu data guarantees that recordings, observability metrics, and operational statistics survive unexpected failures or planned migrations. The **most critical data to protect** depends on the product you deploy:

- **OpenVidu Platform**
    - S3 storage stores egress outputs such as recordings.
    - MongoDB keeps statistics for rooms, egress, and ingress operations.
- **OpenVidu Meet**
    - S3-compatible storage retains all meeting recordings.
    - MongoDB stores rooms, Meet users, permissions, and recording links.

You can backup and restore following three different strategies:

1. Direct snapshots of OpenVidu nodes.
2. Backup file containing MinIO/S3 and MongoDB data.
3. Snapshots offered by external services.

## How can I know which method to use?

First, identify where your S3 and MongoDB services run. SSH to your OpenVidu deployment node (or any master node) and inspect these environment variables:

- `EXTERNAL_S3_ENDPOINT`: leave blank when MinIO runs inside the deployment.
- `EXTERNAL_MONGO_URI`: leave blank when MongoDB runs inside the deployment.

Find both variables in the OpenVidu configuration files:

- **Single Node**: `/opt/openvidu/config/openvidu.env`
- **Elastic & High Availability**: `/opt/openvidu/config/cluster/openvidu.env`

With that information, pick the backup approach that fits your scenario:

- [Method 1: Snapshots of OpenVidu nodes](#method-1-snapshots-of-openvidu-nodes)
    - Both `EXTERNAL_S3_ENDPOINT` and `EXTERNAL_MONGO_URI` are blank.
    - Your deployment runs on virtualized or cloud infrastructure that supports VM snapshots.
- [Method 2: Backup file containing MinIO/S3 and MongoDB data](#method-2-backup-file-containing-minios3-and-mongodb-data)
    - Both `EXTERNAL_S3_ENDPOINT` and `EXTERNAL_MONGO_URI` are blank.
    - You run on bare metal without snapshots capability or want portable backup data outside the infrastructure provider.
- [Method 3: Snapshots offered by external services](#method-3-snapshots-offered-by-external-services)
    - At least one of `EXTERNAL_S3_ENDPOINT` or `EXTERNAL_MONGO_URI` points to an external service.
    - Your managed storage or database provider offers its own snapshot or backup tooling.

## Method 1: Snapshots of OpenVidu nodes

If you deploy OpenVidu on a cloud provider **without externalizing S3 or MongoDB**, snapshotting the compute nodes that host those services is usually enough. This approach captures the entire installation, including the disks where MinIO and MongoDB store their data.

1. Identify the nodes:
    - **Single Node**: snapshot the VM that runs the whole stack.
    - **Elastic & High Availability**: snapshot every master node. Media nodes can be reprovisioned because they do not keep stateful data.
2. Follow your cloud provider's snapshot workflow:
    - AWS: [Create Amazon EBS snapshots](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html) and [restore an EC2 instance from a snapshot/AMI](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/creating-an-ami-ebs.html).
    - Azure: [Managed disk snapshots](https://learn.microsoft.com/azure/virtual-machines/disks-snapshots) and [restore VMs from snapshots](https://learn.microsoft.com/azure/virtual-machines/linux/disks-recover-snapshot).
    - Google Cloud: [Persistent disk snapshots](https://cloud.google.com/compute/docs/disks/create-snapshots) and [create disks or instances from snapshots](https://cloud.google.com/compute/docs/disks/create-disk-from-snapshot).
3. Automate snapshots using your provider's scheduler (AWS Backup, Azure Automation, Cloud Scheduler) for consistent recovery points.
4. Restore by cloning a new node from the snapshot/AMI, updating DNS or load balancer targets, and verifying that MinIO and MongoDB services start with intact data.


## Method 2: Backup with restic and snapshots

Generate portable snapshots using [restic](https://restic.net/) when you need point-in-time data snapshots locally or sync it with multiple storage providers. Run these backups from an **external machine with enough disk space** (for example, a bastion host or operations workstation) that can reach your OpenVidu network.

### Prerequisites

- A separated machine with network access to OpenVidu. Ports 9100 TCP (MinIO) and 20000 TCP (MongoDB) must be reachable from the backup machine to the OpenVidu deployment node or master nodes.
- Ensure that the backup machine has enough disk space to hold at least one full backup of your MinIO and MongoDB data.
- Install MongoDB and MinIO clients with its corresponding version in the deployment. You can find the versions of MongoDB and MinIO in the [Release Notes](../../releases.md#version-table) page.
- Install `restic` CLI tool for incremental backups and encryption. In this example we will use restic with docker and a local repository, but you can adapt it to your preferred backend (S3, Azure Blob, etc). See [restic documentation](https://restic.readthedocs.io/en/stable/) for more details.

In the instructions we will use Docker and `latest` tags for simplicity. In production environments, use specific version tags that match your deployment.

Export the following variables once on your backup machine, so every command below can reference the same paths and credentials without changing directories:

```bash
export OV_BACKUP_DIR="$HOME/openvidu-backups"
export OPENVIDU_NODE_IP="<OPENVIDU_NODE_IP>"
export MONGO_ADMIN_USER="<MONGO_ADMIN_USER>"
export MONGO_ADMIN_PASSWORD="<MONGO_ADMIN_PASSWORD>"
export MINIO_ADMIN_USER="<MINIO_ADMIN_USER>"
export MINIO_ADMIN_PASSWORD="<MINIO_ADMIN_PASSWORD>"
export RESTIC_PASSWORD="<RESTIC_PASSWORD>"
```

Replace the placeholders with the values from your deployment. All subsequent commands assume these variables stay defined in your shell session. All credentials can be found in the `openvidu.env` file(s) of your deployment.

About the exported variables:

- `<OPENVIDU_NODE_IP>`: IP address to access the OpenVidu node from the backup machine. In Single Node deployments, this is the node's own IP. In Elastic/HA deployments, use the IP of any master node.
- `<MONGO_ADMIN_USER>` and `<MONGO_ADMIN_PASSWORD>`: MongoDB admin credentials found in `openvidu.env` as `MONGO_ADMIN_USERNAME` and `MONGO_ADMIN_PASSWORD`.
- `<MINIO_ADMIN_USER>` and `<MINIO_ADMIN_PASSWORD>`: MinIO credentials found in `openvidu.env` as `MINIO_ADMIN_USERNAME` and `MINIO_ADMIN_PASSWORD`.
- `<RESTIC_PASSWORD>`: strong password to encrypt restic snapshots. Keep it safe because you will need it for restores.

### Backup steps

1. Create a backup directory and initialize restic repository (only first time):

    ```bash
    # Create backup directory layout
    mkdir -p "$OV_BACKUP_DIR/restic-repo"
    mkdir -p "$OV_BACKUP_DIR/backup/minio" "$OV_BACKUP_DIR/backup/mongodb"
    docker run --rm -it \
        -u "$(id -u):$(id -g)" \
        -v "$OV_BACKUP_DIR/restic-repo":/restic-repo \
        -e RESTIC_REPOSITORY=/restic-repo \
        -e RESTIC_PASSWORD="$RESTIC_PASSWORD" \
        restic/restic:latest init
    ```

    This keeps the encrypted repository in `restic-repo/` while using the `backup/` subfolders as a temporary staging area for the raw MongoDB dumps and MinIO objects that restic ingests in a later step.

    The directory structure will look like this:

    ```
    openvidu-backups/
    ├── restic-repo/          # Encrypted restic repository
    └── backup/               # Temporary staging area
        ├── minio/            # MinIO data dump
        └── mongodb/          # MongoDB dump
    ```

    !!! info
        You can configure restic to use multiple backends (S3, Azure Blob, etc) instead of doing it locally. Refer to the [restic documentation](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html) for more details. These instructions use a local repository for simplicity but can be adapted to other backends.

2. Backup MongoDB data and Minio data into the staging directory:

    ```bash
    # Remove previous dump if any (restic will handle previous backups)
    rm -rf "$OV_BACKUP_DIR/backup/mongodb/dump"
    docker run --rm \
      --network host \
      --user "$(id -u):$(id -g)" \
                -v "$OV_BACKUP_DIR/backup/mongodb":/backup \
      mongo:latest mongodump \
          --host "${OPENVIDU_NODE_IP}" \
          --port 20000 \
          --username "${MONGO_ADMIN_USER}" \
          --password "${MONGO_ADMIN_PASSWORD}" \
          --out /backup/dump \
          --oplog

    ```

3. Backup MinIO data:

    ```bash
    # MinIO backup
    docker run --rm \
        --network host \
        --user "$(id -u):$(id -g)" \
        -e MC_CONFIG_DIR="/tmp/.mc" \
        -v "$OV_BACKUP_DIR/backup/minio":/backup \
        --entrypoint sh \
        minio/mc:latest -c "\
            mc alias set openvidu http://${OPENVIDU_NODE_IP}:9100 ${MINIO_ADMIN_USER} ${MINIO_ADMIN_PASSWORD} && \
            mc ls openvidu | while IFS= read -r line; do \
                bucket=\${line##* } && bucket=\${bucket%/} && [ -n \"\${bucket}\" ] && \
                mc mirror --overwrite openvidu/\${bucket} /backup/\${bucket}; \
            done \
        "
    ```

4. Create a restic snapshot of the actual state of the backup data:

    ```bash
    docker run --rm -it \
        -u "$(id -u):$(id -g)" \
        -v "$OV_BACKUP_DIR/restic-repo":/restic-repo \
        -v "$OV_BACKUP_DIR/backup":/backup \
        -e RESTIC_REPOSITORY=/restic-repo \
        -e RESTIC_PASSWORD="$RESTIC_PASSWORD" \
        restic/restic:latest backup /backup
    ```

    Restic copies the staged data into the encrypted `restic-repo/`. After confirming the snapshot, you can clear the contents of `$OV_BACKUP_DIR/backup/` before the next backup run to reclaim disk space.

5. Check the created snapshots:

    ```bash
    docker run --rm -it \
        -u "$(id -u):$(id -g)" \
        -v "$OV_BACKUP_DIR/restic-repo":/restic-repo \
        -e RESTIC_REPOSITORY=/restic-repo \
        -e RESTIC_PASSWORD="$RESTIC_PASSWORD" \
        restic/restic:latest snapshots
    ```

    This command lists all the snapshots stored in the restic repository, along with their timestamps and IDs.

### Restore steps

TODO

## Method 3: Snapshots offered by external services

When you use **managed S3-compatible services or managed MongoDB providers**, rely on their built-in snapshot and backup capabilities.

- **S3/Object storage providers**
    - AWS S3: [AWS Backup for S3](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html)
    - Azure Storage: [Blob storage snapshots](https://learn.microsoft.com/azure/storage/blobs/snapshots-overview)
    - Google Cloud Storage: implement [Object Versioning and Retention](https://cloud.google.com/storage/docs/object-versioning)

- **MongoDB providers**
    - MongoDB Atlas: [Cloud backups and snapshots](https://www.mongodb.com/docs/atlas/backup-restore/)
    - AWS DocumentDB: [Automated snapshots](https://docs.aws.amazon.com/documentdb/latest/developerguide/backup_restore.html)
    - Azure Cosmos DB for MongoDB: [Continuous backups](https://learn.microsoft.com/azure/cosmos-db/mongodb/continuous-backup-restore-introduction)
    - Google Cloud: [AlloyDB / Cloud Bigtable snapshot guidance](https://cloud.google.com/alloydb/docs/manage/automatic-backups)
