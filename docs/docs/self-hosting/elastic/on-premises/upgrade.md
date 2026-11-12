---
title: "Upgrade OpenVidu Elastic on-premises"
description: "Update an OpenVidu Elastic deployment on your own servers with the OpenVidu CLI, and convert an install.sh cluster, keeping its configuration and data."
---

# Upgrade OpenVidu Elastic: On-premises

<div class="provider-chip" markdown>

:material-server:{ .provider-chip-icon } On-premises

</div>

**A release of `ov` deploys the same release of OpenVidu.** Updating a stack means running the command with the `ov` of the version you want: [install that version](../../openvidu-cli.md#install-the-openvidu-cli) first.

## Update the stack

Run `ov stack update` from the stack's directory, with the new `ov` on your `PATH`. The update changes OpenVidu, not the machines: the nodes, their size and the number of media nodes stay as they are.

--8<-- "self-hosting/common/ov-update-pro.md"

## Migrate a deployment installed by install.sh

With the cluster's nodes named, **`ov stack update`** converts, once, an Elastic cluster installed with the published `install.sh` (3.9.0) into the stack `ov` deploys, on the same machines, keeping the configuration with your edits, the certificates and the data. Run it from an empty directory. This is the same conversion as a [Single Node](../../single-node/upgrade.md#migrate-a-deployment-installed-by-installsh); only the node list differs.

`--ssh` names the master `ov` talks to, and `--media-node` names each media node by address (an Elastic cluster has no `--master-node`, since its one master is the `--ssh` node). The media nodes must all be named; the SSH user, key and port apply to every node:

```bash
ov stack update el --ssh ubuntu@10.0.0.5 --ssh-key ~/.ssh/key --media-node 10.0.0.7 --dry-run
ov stack update el --ssh ubuntu@10.0.0.5 --ssh-key ~/.ssh/key --media-node 10.0.0.7
```

The cluster becomes Kubernetes on the same machines. It is converted in order: the media nodes stop before the master, then `ov` installs Kubernetes on the master, deploys OpenVidu and joins the nodes. **The data stays in place**: the stores keep their directories, which become the chart's volumes (static PersistentVolumes bound to the chart's claims, kept when the stack is destroyed), and MongoDB's one member is renamed to the chart's member 0. Caddy issues its certificates again, and the logs and metrics of the `observability` module start anew (Grafana's own data is kept). On test machines an Elastic conversion took about 5 minutes.

A conflict (an edit on the lines `ov` changes) stops it before anything runs (exit `4`), so does a node without the disk space it needs (exit `9`), and a failure rolls it back to the unchanged 3.9.0. Because the images become this `ov`'s, converting with the `ov` of the release you want is also the update to it.

## Next steps

- [Administer the cluster](admin.md): add and drain media nodes, operate the stack.
- The full [OpenVidu CLI reference](../../openvidu-cli.md#command-reference).
