---
title: Upgrade OpenVidu Elastic on DigitalOcean
description: How to upgrade OpenVidu Elastic on DigitalOcean deployments.
---

# Upgrade OpenVidu Elastic: DigitalOcean

<div class="provider-chip" markdown>

:material-digital-ocean:{ .provider-chip-icon } DigitalOcean

</div>

For DigitalOcean environments, we recommend upgrading by redeploying the [OpenVidu Elastic DigitalOcean](../digitalocean/install.md) stack using the latest version. This approach ensures that all components are updated accurately and consistently, since DigitalOcean Terraform files and related configurations may differ between releases. Redeploying guarantees that all necessary changes are properly applied.

If you would prefer not to redeploy, an in-place upgrade is also possible. The steps below describe how to perform an in-place upgrade of your OpenVidu Elastic deployment on DigitalOcean.

## Upgrading OpenVidu Elastic on DigitalOcean

1. SSH into your Master Node.
2. Execute the following command in the Master Node:

    ```
    sh <(curl -fsSL http://get.openvidu.io/update/latest/update.sh)
    ```

    To upgrade to a specific version instead, replace `latest` with the version number (e.g. `3.7.0`).

3. This will run an update script that guides you from your currently installed version to the target one. The output will begin with the following:

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

4. **Confirm each version upgrade.** You can jump straight to the latest release regardless of how far behind you are — the updater will automatically apply every intermediate upgrade in sequence.

    For each intermediate version, the updater will prompt you to confirm the upgrade, display a diff of configuration file changes, ask whether to apply the diff, and ask whether to pull updated Docker images. You must confirm each step.

    !!! warning
        The updater will flag any breaking changes if they are present. Pay close attention to these, as they may require you to update firewall rules, open or close specific ports, or make other manual configuration changes.

    !!! info "Pulling Docker images"
        When upgrading across multiple intermediate versions, answer `No` when the updater asks whether to pull images at each intermediate step. Only answer `Yes` for the final version.

        Any missing images will be pulled automatically when you run `systemctl start openvidu`.


5. After the final intermediate upgrade completes, **you need to terminate the Media Nodes** to apply the changes. Go to the DigitalOcean web console, navigate to the Droplets tab, select your Media Node instances, and terminate them. The DigitalOcean Function will provision new Media Nodes automatically, or the Fixed Autoscale Pool will do so if you have configured fixed Media Nodes.
6. Once the Media Nodes are up and running, restart OpenVidu Elastic by running the following command on the Master Node:

    ```bash
    systemctl start openvidu && journalctl -f -u openvidu
    ```

    The `journalctl` command will show you the logs of the OpenVidu services. You can stop the logs by pressing `Ctrl + C`.

## Backups and Rollback

Once the upgrade is complete, a backup of the previous version will be available in the `/opt/openvidu/backups` directory. The backup contains only the configuration files that were changed during the upgrade.

To roll back to the previous version, copy the files from the backup back to the OpenVidu directory using the following command:

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

Note the `store_secret.sh` command at the end. This is required to update the `OPENVIDU_VERSION` secret in the DigitalOcean `secret.env` file, which the DigitalOcean deployment uses to determine which version of OpenVidu should be running on the Media Nodes. This only needs to be run on the Master Node.

Remember to **terminate the Media Nodes** after rolling back so that the Autoscale Pool can launch new Media Nodes with the restored configuration. You can do this from the DigitalOcean web console by navigating to the Droplets tab, selecting the Media Node instances, and terminating them.

## Recommendations

- Always upgrade all nodes in your OpenVidu Elastic deployment. Running mismatched versions across nodes may cause compatibility issues.
- If you encounter any problems during an upgrade, a full redeployment is always the recommended path to a clean installation.
- Keep your Docker and Docker Compose versions up to date.
- Remove unused images and containers to free up disk space. For example, once the upgrade is complete and OpenVidu is running, you can remove old images with the following command:

    ```bash
    docker image prune -a
    ```

    This command will remove all the images that are not being used by any container.
