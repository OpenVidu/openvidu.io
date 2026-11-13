---
title: "Upgrade OpenVidu High Availability on-premises"
description: "Update an OpenVidu High Availability cluster on your own servers with the OpenVidu CLI, and convert an install.sh cluster, keeping its data."
---

# Upgrade OpenVidu High Availability: On-premises

<div class="provider-chip" markdown>

:material-server:{ .provider-chip-icon } On-premises

</div>

**A release of `ov` deploys the same release of OpenVidu.** Updating a stack means running the command with the `ov` of the version you want: [install that version](../../openvidu-cli.md#install-the-openvidu-cli) first.

## Update the stack

Run `ov stack update` from the stack's directory, with the new `ov` on your `PATH`.

--8<-- "self-hosting/common/ov-update-pro.md"

## Migrate a deployment installed by install.sh

With the cluster's nodes named, **`ov stack update`** converts, once, a High Availability cluster installed with the published `install.sh` (3.9.0) into the stack `ov` deploys, on the same machines, keeping the configuration with your edits, the certificates and the data. Run it from an empty directory. This is the same conversion as a [Single Node](../../single-node/upgrade.md#migrate-a-deployment-installed-by-installsh); only the node list and the data hand-over differ. A cluster at a release older than 3.9.0 updates to 3.9.0 with its own updater first.

`--ssh` names the master `ov` talks to, `--master-node` names the three other masters, and `--media-node` names each media node, both repeatable and both an address. The masters named must be **exactly the four** the cluster lists, none left out; the SSH user, key and port apply to every node:

```bash
ov stack update ha --ssh ubuntu@10.0.0.5 --ssh-key ~/.ssh/key \
  --master-node 10.0.0.6 --master-node 10.0.0.7 --master-node 10.0.0.8 \
  --media-node 10.0.0.9 --dry-run
```

**The data is copied over.** With the installed stack still running, `ov` copies MongoDB, Redis and the MinIO application bucket, and loads them into the new stack once its masters have joined. What clients write between the copy and the stop is lost: seconds. The copy of MongoDB uses the official `mongo:<version>` image, so a registry mirror (`images.registry`) must hold it. Grafana's own data and the logs and metrics of the `observability` module start anew. On test machines a High Availability conversion took about 20 minutes.

A conflict (an edit on the lines `ov` changes) stops it before anything runs. A failure before OpenVidu is installed rolls back to the unchanged 3.9.0. Past that point nothing is rolled back: the command fails with the installed stack stopped, and prints the commands to retire it once `ov stack status --wait` passes and the commands to put it back.

## Next steps

- [Administer the cluster](admin.md): join and drain nodes, operate the stack.
- The [OpenVidu CLI commands](../../openvidu-cli.md#command-reference).
