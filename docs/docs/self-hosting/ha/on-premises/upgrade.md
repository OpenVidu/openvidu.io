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

The cluster becomes Kubernetes on the same machines, converted in order: every other node stopped, then the master `ov` talks to, Kubernetes installed on it, OpenVidu deployed, and the rest of the nodes joining (masters first, then media).

**The data is handed over to the chart.** HA's masters share the cluster's data, and the chart gives each store its own pods, so the data is **copied out and loaded in**, not left in place: with the installed stack still running, `ov` dumps MongoDB, Redis's RDB and the MinIO application bucket into `/opt/openvidu/data/migrate`, and once the chart is installed and the masters have joined, three pods restore them into the cluster's data services (you will see `▶ Hand the data over to the chart…` in the output). MongoDB's dump and restore are the one step that does not run the chart's image: they use the official `mongo:<version>` image of the same server version, so a registry mirror (`images.registry`) must hold it for the conversion. What clients write between the copy and the stop is what is lost: seconds. Grafana's own data is not carried in HA, and the logs and metrics of the `observability` module start anew. On test machines a High Availability conversion took about 20 minutes.

A conflict (an edit on the lines `ov` changes) stops it before anything runs (exit `4`), a cluster of a size other than the chart's four masters is refused (exit `4`), a node without the disk space it needs stops it (exit `9`). A failure **before `helm install`** rolls it back to the unchanged 3.9.0; from `helm install` on nothing is rolled back (the chart's pods have run on the data), and the command exits `1` with the installed stack left stopped but not retired, naming the commands to retire it once `ov stack status --wait` passes and the commands to put it back. Because the images become this `ov`'s, converting with the `ov` of the release you want is also the update to it.

## Next steps

- [Administer the cluster](admin.md): join and drain nodes, operate the stack.
- The full [OpenVidu CLI reference](../../openvidu-cli.md#command-reference).
