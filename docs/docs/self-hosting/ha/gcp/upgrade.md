---
title: Upgrade OpenVidu High Availability - Google Cloud Platform
description: How to upgrade OpenVidu High Availability on Google Cloud Platform deployments.
---
# Upgrade OpenVidu High Availability - GCP

In Google Cloud Platform environments, we recommend upgrading by redeploying [OpenVidu High Availability Google Cloud Platform](../gcp/install.md) stack using the latest version. This approach ensures that all components are updated accurately and consistently, as Google Cloud Platform terrafrom files and related configurations may vary between releases. Redeploying guarantees that all necessary changes are properly applied.

However, if you prefer not to redeploy, it is also possible to upgrade OpenVidu High Availability in place. The following steps outline how to perform an in-place upgrade of your OpenVidu High Availability deployment on Google Cloud Platform:

## Upgrading OpenVidu High Availability on Google Cloud Platform

1. SSH into one of your Master Node server.
2. Execute the following command in the Master Node:

    ```
    sh <(curl -fsSL http://get.openvidu.io/update/latest/update.sh)
    ```

    !!! info
        If instead of upgrading to the latest version you want to upgrade to a specific version, you can execute the following command:

        ```bash
        sh <(curl -fsSL http://get.openvidu.io/update/<VERSION>/update.sh)
        ```

        Where `<VERSION>` is the version you want to upgrade to.

3. This will execute an update script which will guide you from the version you have installed to the latest one. The first thing you will see in the output is the following:

    ```
    Stopping OpenVidu service...
    Backing up files...

        - Backing up file '/opt/openvidu/config' to '/opt/openvidu/backups/<DATE>_<VERSION>/config'
        ... More files ...

    --------------------
    📦 Backup directory: /opt/openvidu/backups/<DATE>_<VERSION>/
    --------------------

    --------------------
    🚀 Updating OpenVidu from 3.x.x to 3.y.y
    --------------------

    ? Do you want to update from 3.x.x to 3.y.y? ›
    • Yes
      No
    ```

4. Answer `Yes` to the question and your Master Node will be upgraded to the asked version. For each version, the system will ask you to confirm the upgrade.
5. A `diff` will be shown with the changes made in the configuration files. You can review the changes and decide if you want to apply them or not. If you want to apply the changes, answer `Yes` to the question. If you want to discard the changes and stop the upgrading process, simply answer `No`.
6. Once the upgrade is finished, it will ask you to pull the images of the services. Answer `Yes` if you want to do it.
7. **Repeat the steps 1 to 6 in all the Master Nodes of your deployment.** This is important because the Master Nodes need to be running the same version of OpenVidu.
8. After upgrading all your Master Nodes, **you need to delete the Media Nodes** to apply the changes to run the Media Nodes with the new version. Go to your Google Cloud Platform Console, Compute Engine instances, selecting the Media Nodes instances, and terminating them. The MIG will automatically launch new Media Nodes with the updated configuration.
9. Once the Media Nodes are up and running, execute the following command in every Master Node to start OpenVidu High Availability again:

    ```bash
    systemctl start openvidu && journalctl -f -u openvidu
    ```

    The `journalctl` command will show you the logs of the OpenVidu services. You can stop the logs by pressing `Ctrl + C`.

## Backups and Rollback

When you finish the upgrade process, you will have a backup of the previous version in the `/opt/openvidu/backups` directory. The backup only contains the previous configuration files that have changed in the upgrade process.
To roll back to the previous version, you have to copy the files from the backup to the OpenVidu directory on each Master Node. You can do it with the following command:

```bash
cp -r /opt/openvidu/backups/<DATE>_<VERSION>/* /opt/openvidu
/usr/local/bin/store_secret.sh save OPENVIDU_VERSION "<VERSION>"
```

Where `<DATE>` and `<VERSION>` are the date and version of the backup you want to restore. For example:

```
cp -r /opt/openvidu/backups/2025-02-12-09-50-46_3.0.0/* /opt/openvidu
/usr/local/bin/store_secret.sh save OPENVIDU_VERSION "3.0.0"
```

Notice the `store_secret.sh` command at the end. This command is necessary to update the `OPENVIDU_VERSION` secret in GCP Secret Manager, which is used by the Google Cloud Platform deployment to know which version of OpenVidu should be running in Media Nodes. You need to do this in the Master Node only.

Remember to **delete the Media Nodes** after rolling back to the previous version so the MIG can launch new Media Nodes with the restored configuration. You can do this by going to your Google Cloud Platform Console, Compute Engine instances, selecting the Media Nodes instances, and terminating them.

## Recommendations

- Always upgrade all the nodes of your OpenVidu High Availability deployment. Otherwise, you may face compatibility issues between the different versions of OpenVidu running in your deployment.
- On any upgrade problem, a redeployment is always recommended for a clean installation.
- Keep your Docker and Docker Compose versions updated.
- Remove non-used images and containers to free up disk space. For example, after the upgrade, when OpenVidu is running, you can remove the old images with the following command:

    ```bash
    docker image prune -a
    ```

    This command will remove all the images that are not being used by any container.
