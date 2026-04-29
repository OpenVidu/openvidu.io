---
title: Upgrade OpenVidu Elastic on DigitalOcean
description: How to upgrade OpenVidu Elastic on DigitalOcean deployments.
---

# Upgrade OpenVidu Elastic: DigitalOcean

<div class="provider-chip" markdown>

:material-digital-ocean:{ .provider-chip-icon } DigitalOcean

</div>


In DigitalOcean environments, we recommend upgrading by redeploying [OpenVidu Elastic DigitalOcean](../digitalocean/install.md) stack using the latest version. This approach ensures that all components are updated accurately and consistently, as DigitalOcean terraform files and related configurations may vary between releases. Redeploying guarantees that all necessary changes are properly applied.

However, if you prefer not to redeploy, it is also possible to upgrade OpenVidu Elastic in place. The following steps outline how to perform an in-place upgrade of your OpenVidu Elastic deployment on DigitalOcean:

## Upgrading OpenVidu Elastic on DigitalOcean

1. SSH into your Master Node server.
2. Execute the following command in the Master Node:

    ```
    sh <(curl -fsSL http://get.openvidu.io/update/latest/update.sh)
    ```

    To upgrade to a specific version instead, replace `latest` with the version number (e.g. `3.x.y`).

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

4. **Confirm each version upgrade.** You can jump straight to the latest release no matter how far behind you are, the updater will automatically apply every intermediate upgrade in sequence.

    For each intermediate version, the updater will ask you to confirm the upgrade, display a diff of configuration file changes, ask whether to apply the diff, and ask whether to pull updated Docker images. You must confirm each step.

    !!! warning
        The updater will flag any deployment breaking changes if they are present. Pay special attention to these, as they may require you to update firewall rules, open or close specific ports, or perform other manual configuration changes.

    !!! info "Pulling Docker images"
        When upgrading across multiple intermediate versions, answer `No` when the updater asks whether to pull images at each intermediate step. Only answer `Yes` for the final version.

        Any missing images will be pulled automatically when you run `systemctl start openvidu`.


5. After the last intermediate upgrade completes, **you need to terminate the Media Nodes** to apply the changes. Go to your DigitalOcean web, Droplets tab, select the Media Nodes instances and terminate them. The DigitalOcean Autoscale Pool will make new media nodes, or the fixed pool if you have fixed media nodes.
6. Once the Media Nodes are up and running, start OpenVidu Elastic again by executing the following command in the Master Node:

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

Notice the `store_secret.sh` command at the end. This command is necessary to update the `OPENVIDU_VERSION` secret in DigitalOcean secret.env, which is used by the DigitalOcean deployment to know which version of OpenVidu should be running in Media Nodes. You need to do this in the Master Node only.

Remember to **terminate the Media Nodes** after rolling back to the previous version so the Autoscale Pool can launch new Media Nodes with the restored configuration. You can do this by going to your DigitalOcean web to the Droplets tab, selecting the Media Nodes instances, and terminating them.

## Recommendations

- Always upgrade all the nodes of your OpenVidu Elastic deployment. Otherwise, you may face compatibility issues between the different versions of OpenVidu running in your deployment.
- On any upgrade problem, a redeployment is always recommended for a clean installation.
- Keep your Docker and Docker Compose versions updated.
- Remove non-used images and containers to free up disk space. For example, after the upgrade, when OpenVidu is running, you can remove the old images with the following command:

    ```bash
    docker image prune -a
    ```

    This command will remove all the images that are not being used by any container.
