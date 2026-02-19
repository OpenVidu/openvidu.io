---
title: Upgrade OpenVidu Elastic - Digital Ocean
description: How to upgrade OpenVidu Elastic on Digital Ocean deployments
---

# Upgrade OpenVidu Elastic - Digital Ocean

In Digital Ocean environments, we recommend upgrading by redeploying [OpenVidu Elastic Digital Ocean](../digitalocean/install.md) stack using the latest version. This approach ensures that all components are updated accurately and consistently, as Digital Ocean terraform files and related configurations may vary between releases. Redeploying guarantees that all necessary changes are properly applied.

However, if you prefer not to redeploy, it is also possible to upgrade OpenVidu Elastic in place. The following steps outline how to perform an in-place upgrade of your OpenVidu Elastic deployment on Digital Ocean:

## Upgrading OpenVidu Elastic on Digital Ocean

1. SSH into your Master Node server.
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

4. Answer `Yes` to the question and your OpenVidu Elastic will be upgraded to the asked version. For each version, the system will ask you to confirm the upgrade.
5. A `diff` will be shown with the changes made in the configuration files. You can review the changes and decide if you want to apply them or not. If you want to apply the changes, answer `Yes` to the question. If you want to discard the changes and stop the upgrading process, simply answer `No`.
6. Once the upgrade is finished, it will ask you to pull the images of the services. Answer `Yes` if you want to do it.
7. After the upgrade, **you need to terminate the Media Nodes** to apply the changes to run the Media Nodes with the new version. Go to your Digital Ocean web, Droplets tab, select the Media Nodes instances and terminate them. The fixed autoscale pool will automatically launch new Media Nodes with the updated configuration.
8. Once the Media Nodes are up and running, you can start OpenVidu Elastic again by executing the following command in the Master Node:

    ```bash
    systemctl start openvidu && journalctl -f -u openvidu
    ```

    The `journalctl` command will show you the logs of the OpenVidu services. You can stop the logs by pressing `Ctrl + C`.

## Backups and Rollback

When you finish the upgrade process, you will have a backup of the previous version in the `/opt/openvidu/backups` directory. The backup only contains the previous configuration files that have changed in the upgrade process.
To roll back to the previous version, you have to copy the files from the backup to the OpenVidu directory. You can do it with the following command:

```bash
cp -r /opt/openvidu/backups/<DATE>_<VERSION>/* /opt/openvidu
/usr/local/bin/store_secret.sh save OPENVIDU_VERSION "<VERSION>"
/usr/local/bin/store_secret.sh fullsave
```

Where `<DATE>` and `<VERSION>` are the date and version of the backup you want to restore. For example:

```
cp -r /opt/openvidu/backups/2025-02-12-09-50-46_3.0.0/* /opt/openvidu
/usr/local/bin/store_secret.sh save OPENVIDU_VERSION "3.0.0"
/usr/local/bin/store_secret.sh fullsave
```

Notice the `store_secret.sh` command at the end. This command is necessary to update the `OPENVIDU_VERSION` secret in Digital Ocean secret.env, which is used by the Digital Ocean deployment to know which version of OpenVidu should be running in Media Nodes. You need to do this in the Master Node only.

Remember to **terminate the Media Nodes** after rolling back to the previous version so the fixed autoscaling can launch new Media Nodes with the restored configuration. You can do this by going to your Digital Ocean web to the Droplets tab, selecting the Media Nodes instances, and terminating them.

## Recommendations

- Always upgrade all the nodes of your OpenVidu Elastic deployment. Otherwise, you may face compatibility issues between the different versions of OpenVidu running in your deployment.
- On any upgrade problem, a redeployment is always recommended for a clean installation.
- Keep your Docker and Docker Compose versions updated.
- Remove non-used images and containers to free up disk space. For example, after the upgrade, when OpenVidu is running, you can remove the old images with the following command:

    ```bash
    docker image prune -a
    ```

    This command will remove all the images that are not being used by any container.
