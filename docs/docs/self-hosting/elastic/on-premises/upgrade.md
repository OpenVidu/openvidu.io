---
title: Upgrade OpenVidu Elastic - On premises
description: How to upgrade OpenVidu Elastic on premises deployments
---

# Upgrade OpenVidu Elastic - On premises

OpenVidu offers an updater that allows you to upgrade your OpenVidu deployment in an easy and automated way. The updater will take care of the whole process, from stopping the services to updating the configuration files.

## Upgrading OpenVidu Elastic

Upgrade OpenVidu Elastic is very simple. These are the steps you need to follow:

1. First, ensure to shut down OpenVidu Elastic. SSH into all the nodes and execute the following command:

    ```bash
    systemctl stop openvidu
    ```

2. SSH into your Master Node and your Media Nodes and execute on each of them the following command:

    ```
    sh <(curl -fsSL http://get.openvidu.io/update/latest/update.sh)
    ```

    !!! info
        If instead of upgrading to the latest version you want to upgrade to a specific version, you can execute the following command:

        ```bash
        sh <(curl -fsSL http://get.openvidu.io/update/<VERSION>/update.sh)
        ```

        Where `<VERSION>` is the version you want to upgrade to.

3. In all the nodes, you will see the following output:

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

4. Answer `Yes` to the question and your OpenVidu Elastic will be upgraded to asked version. For each version the system will ask you to confirm the upgrade.
5. Once the upgrade is finished, it will ask you to pull the images of the services. Answer `Yes` if you want to do it.
6. Execute the following command in all the nodes:

```bash
systemctl start openvidu && journalctl -f -u openvidu
```

The `journalctl` command will show you the logs of the OpenVidu services. You can stop the logs by pressing `Ctrl + C`.

## Backups and Rollback

When you finish the upgrade process on each node, you will have a backup of the previous version in the `/opt/openvidu/backups` directory. The backup only contains the previous configuration files that have changed in the upgrade process.
To roll back to the previous version, you have to copy the files from the backup to the OpenVidu directory. You can do it with the following command:

```bash
cp -r /opt/openvidu/backups/<DATE>_<VERSION>/* /opt/openvidu
```

Where `<DATE>` and `<VERSION>` are the date and version of the backup you want to restore. For example:

```
cp -r /opt/openvidu/backups/2025-02-12-09-50-46_3.0.0/* /opt/openvidu
```

You need to do this in all the nodes of your OpenVidu Elastic deployment to restore to the previous version.

## Recommendations

- On any upgrade problem, a redeployment is always recommended for a clean installation.
- Keep your Docker and Docker Compose versions updated.
- Remove non-used images and containers to free up disk space. For example, after the upgrade, when OpenVidu is running, you can remove the old images with the following command:

    ```bash
    docker image prune -a
    ```

    This command will remove all the images that are not being used by any container.
