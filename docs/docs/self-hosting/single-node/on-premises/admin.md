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

`ov stack destroy` tears the deployment down and removes the directory's record. It asks for confirmation (type the stack name, or pass `-y`); `--dry-run` changes nothing and prints exactly what it would do.

On a server, the stack is stopped and disabled; its files and data stay under `/opt/openvidu`, so `ov stack deploy --mode auto` in the same directory brings it back with its data and configuration:

```console
$ ov stack destroy -y
✓ [172.30.0.96 single] systemctl stop openvidu
✓ [172.30.0.96 single] systemctl disable openvidu
stack stopped and disabled on all nodes (its files and data stay under /opt/openvidu)
✔ removed stack "web" from this directory
```

Two flags go further:

- `--delete-data` removes the deployment's data after teardown (`/opt/openvidu/data`: MongoDB, MinIO, Redis, recordings, metrics and logs, certificates).
- `--delete-config` removes the deployment directory (`/opt/openvidu` with the systemd unit), so the data goes with it.

## Backup and restore { #backup-and-restore }

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows. A destroy without `--delete-data` keeps the data under `/opt/openvidu/data`, so a later deploy in the same directory brings the stack back as it was.
