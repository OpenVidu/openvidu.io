---
title: "Administer OpenVidu Single Node on-premises"
description: "Administer OpenVidu Single Node on your own servers with the OpenVidu CLI: status, logs, the health check, start and stop, and backup."
---

# OpenVidu Single Node administration: On-premises

<div class="provider-chip" markdown>

:material-server:{ .provider-chip-icon } On-premises

</div>

The sections up to [Export the desired state](#export) are the operations every OpenVidu stack shares, with the same commands wherever it runs. The rest of the page is specific to a Single Node stack on your own servers.

--8<-- "self-hosting/common/ov-operate.md"

## Operate from another machine { #operate-from-another-machine }

To operate the stack from a machine that has no directory for it (a colleague's laptop, a CI runner, a replacement for a lost directory), use **`ov stack import`**. It reads the description the stack publishes about itself and writes the two files a deploy would have left (`openvidu-stack.yml` and the `.openvidu/` state), so every `ov stack` command works afterwards.

```console
$ mkdir -p ~/stacks/web && cd ~/stacks/web
$ ov stack import web --ssh ubuntu@172.30.0.96 --ssh-key ~/.ssh/id_ed25519 -y

Stack described by the deployment:
  name         web
  deployment   single_node · on-premises · community
  dashboard    https://172-30-0-96.openvidu-local.dev
  nodes        172.30.0.96
  published    by ov/ov-admin on 2026-10-29 14:41 UTC (generation 1)

✔ imported stack "web" into /home/me/stacks/web
  desired state: /home/me/stacks/web/openvidu-stack.yml
```

The two editions store their configuration in different places, so importing behaves differently:

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    The configuration lives in the node's files, and each client holds a **copy** in its own `openvidu-stack.yml`. `config get` and `config view` read the node, so you see a change another client made. A Community deployment is a **single-administrator** product: suited to one person or one pipeline, and workable for a small team that coordinates. On the node itself, `sudo ov stack import --this-node` rebuilds the directory; over SSH, `ov stack import --ssh … --replace` refreshes a stale copy.

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    The stack holds its own desired state, so two clients **cannot drift apart**: both read and write the same release, and `ov stack config view` always answers from it. Any administrator who can reach a master node adopts the stack with `ov stack import --ssh <user>@<master>` (the one master on Elastic, any of the four on HA; a Single Node's own node) and operates it from their own directory, which makes PRO a **team** product. On a master itself, `sudo ov stack import --this-node` rebuilds the directory; a copy exported with `ov stack export --bundle --out <file>` is imported elsewhere with `ov stack import -f <file>`.

For a cloud stack kept on its cloud with `--remote-state`, any machine with that cloud's credentials can take it over completely: see [Remote state](../../openvidu-cli.md#remote-state).

## Destroy { #destroy }

`ov stack destroy` tears the stack down and removes the directory's record. It must be told what happens to the data, with one of two flags:

- **`--keep-data`**: the stack is removed, and its data, configuration and credentials stay on its machines. The same `ov stack deploy` from the directory brings it back as it was.
- **`--delete-data`**: nothing of the stack stays on its machines.

With neither flag, the destroy touches nothing and says where the stack's data is. It asks you to type the stack's name unless you pass `-y`, and `--dry-run` prints what it would do without changing anything. Neither flag uninstalls Docker, the cluster software or `ov` from the machines.

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    ```console
    $ ov stack destroy --keep-data -y
    ✓ [172.30.0.96 single] systemctl stop openvidu
    ✓ [172.30.0.96 single] systemctl disable openvidu
    stack stopped and disabled on all nodes (its files and data stay under /opt/openvidu)
      `ov stack deploy` from this directory brings it back as it was; to delete what stayed, destroy the stack with --delete-data (once its record is gone, deploy it again from this directory first)
    ✔ removed stack "web" from this directory
    ```

    `--keep-data` leaves `/opt/openvidu` on the node with its files and data. `--delete-data` removes the whole `/opt/openvidu` (data, configuration and credentials), the systemd unit and the sysctl settings, so a later deploy there is a first deploy.

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    ```console
    $ ov stack destroy --keep-data -y
    uninstalling OpenVidu…
    waiting for the stack's services to stop…
    stack removed; its data (caddy-proxy, grafana, loki, mimir, minio, mongodb, redis) stays on its nodes, with the configuration and credentials it was written with
      `ov stack deploy` from this directory brings it back as it was; to delete what stayed, destroy the stack with --delete-data (once its record is gone, deploy it again from this directory first)
    ✔ removed stack "prod" from this directory
    ```

    `--keep-data` removes OpenVidu's services and keeps their volumes (MongoDB, MinIO with the recordings, Redis, the certificates, metrics and logs) on the nodes, with the configuration and credentials they were written with. `--delete-data` removes the services, the volumes, the configuration and the credentials. Data in an external MongoDB or S3 is never touched.

    The one exception is a Single Node or Elastic stack converted from an `install.sh` installation: `--delete-data` does not delete the data of that installation, which stays in `/opt/openvidu/data` on the node.

!!! warning
    `--delete-data` cannot be undone. Back up what you need first: see [Backup and restore](#backup-and-restore).

To delete what a `--keep-data` destroy left, deploy the stack again from its directory and destroy it with `--delete-data`.

## Backup and restore { #backup-and-restore }

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows. On PRO, back up the MongoDB and S3 data with [Method 3](../../how-to-guides/backup-and-restore.md#method-3-only-backup-data-from-minios3-and-mongodb), or rely on the external services' own backups ([Method 4](../../how-to-guides/backup-and-restore.md#method-4-only-snapshots-provided-by-external-services-used-for-s3-or-mongodb)).
