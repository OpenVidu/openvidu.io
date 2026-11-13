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

Run `ov stack update` from the stack's directory, with the new `ov` on your `PATH`.

--8<-- "self-hosting/common/ov-update-pro.md"

## Migrate a deployment installed by install.sh

With the cluster's nodes named, **`ov stack update`** converts, once, an Elastic cluster installed with the published `install.sh` (3.9.0) into the stack `ov` deploys, on the same machines, keeping the configuration with your edits, the certificates and the data. Run it from an empty directory. This is the same conversion as a [Single Node](../../single-node/upgrade.md#migrate-a-deployment-installed-by-installsh); only the node list differs. A cluster at a release older than 3.9.0 updates to 3.9.0 with its own updater first.

`--ssh` names the master `ov` talks to, and `--media-node` names each media node by address (an Elastic cluster has no `--master-node`, since its one master is the `--ssh` node). The media nodes must all be named; the SSH user, key and port apply to every node:

```bash
ov stack update el --ssh ubuntu@10.0.0.5 --ssh-key ~/.ssh/key --media-node 10.0.0.7 --dry-run
ov stack update el --ssh ubuntu@10.0.0.5 --ssh-key ~/.ssh/key --media-node 10.0.0.7
```

**The data stays in place**, in its directories on the master (even a later `ov stack destroy --delete-data` keeps them). The logs and metrics of the `observability` module start anew. On test machines an Elastic conversion took about 5 minutes.

A conflict (an edit on the lines `ov` changes) stops it before anything runs. A failure before OpenVidu is installed rolls back to the unchanged 3.9.0. Past that point nothing is rolled back: the command fails with the installed stack stopped, and prints the commands to retire it once `ov stack status --wait` passes and the commands to put it back.

## Next steps

- [Administer the cluster](admin.md): add and drain media nodes, operate the stack.
- The [OpenVidu CLI commands](../../openvidu-cli.md#command-reference).
