# Upgrade OpenVidu Single Node PRO

There are two ways to upgrade an OpenVidu Single Node PRO deployment:

- **Redeploying** your cloud provider's template with the new version. This is what we recommend when you deployed OpenVidu from one of our templates. See [Redeploying from your cloud template](#redeploying-from-your-cloud-template).
- **Upgrading in place** with OpenVidu's updater, which keeps your configuration and data. This is the only option for on-premises deployments, and it also works on every cloud provider. See [Upgrading OpenVidu Single Node](#upgrading-openvidu-single-node).

## Redeploying from your cloud template

| Provider         | Redeploy with the latest version                                                                                                          |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **AWS**          | [OpenVidu Single Node PRO CloudFormation](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/aws/install/index.md)                 |
| **Azure**        | [OpenVidu Single Node PRO Azure](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/azure/install/index.md)                        |
| **Google Cloud** | [OpenVidu Single Node PRO Google Cloud Platform](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/gcp/install/index.md)          |
| **DigitalOcean** | [OpenVidu Single Node PRO DigitalOcean](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/digitalocean/install/index.md)          |
| **Oracle Cloud** | [OpenVidu Single Node PRO Oracle Cloud Infrastructure](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/oracle/install/index.md) |

If you prefer not to redeploy, the in-place procedure below works on all of these providers too.

OpenVidu offers an updater that allows you to upgrade your OpenVidu deployment in an easy and automated way. The updater will take care of the whole process, from stopping the services to updating the configuration files.

## Upgrading OpenVidu Single Node

Upgrade OpenVidu Single Node is very simple. These are the steps you need to follow:

1. SSH into your OpenVidu Single Node server.

1. Execute the following command:

   ```text
   sh <(curl -fsSL http://get.openvidu.io/update/latest/update.sh)
   ```

   To upgrade to a specific version instead, replace `latest` with the version number (e.g. `3.x.y`).

1. This will execute an update script which will guide you from the version you have installed to the latest one. The first thing you will see in the output is the following:

   ```text
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

1. **Confirm each version upgrade.** You can jump straight to the latest release no matter how far behind you are, the updater will automatically apply every intermediate upgrade in sequence.

   For each intermediate version, the updater will ask you to confirm the upgrade, display a diff of configuration file changes, ask whether to apply the diff, and ask whether to pull updated Docker images. You must confirm each step.

   Warning

   The updater will flag any deployment breaking changes if they are present. Pay special attention to these, as they may require you to update firewall rules, open or close specific ports, or perform other manual configuration changes.

   Pulling Docker images

   When upgrading across multiple intermediate versions, answer `No` when the updater asks whether to pull images at each intermediate step. Only answer `Yes` for the final version.

   Any missing images will be pulled automatically when you run `systemctl start openvidu`.

1. Start OpenVidu with the following command:

```bash
systemctl start openvidu && journalctl -f -u openvidu
```

The `journalctl` command will show you the logs of the OpenVidu services. You can stop the logs by pressing `Ctrl + C`.

## Backups and Rollback

When you finish the upgrade process, you will have a backup of the previous version in the `/opt/openvidu/backups` directory. To backup to a specific date and version, you can execute the following command:

```bash
cp -r /opt/openvidu/backups/<DATE>_<VERSION>/* /opt/openvidu
```

Where `<DATE>` and `<VERSION>` are the date and version of the backup you want to restore. For example:

```text
cp -r /opt/openvidu/backups/2025-02-12-09-50-46_3.0.0/* /opt/openvidu
```

In the previous command, you have to replace the date and version with the one you want to restore.

## Recommendations

- On any upgrade problem, a redeployment is always recommended for a clean installation.

- Keep your Docker and Docker Compose versions updated.

- Remove non-used images and containers to free up disk space. For example, after the upgrade, when OpenVidu is running, you can remove the old images with the following command:

  ```bash
  docker image prune -a
  ```

  This command will remove all the images that are not being used by any container.
