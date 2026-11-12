---
title: "Administer OpenVidu Elastic on DigitalOcean"
description: "Operate an OpenVidu Elastic DigitalOcean stack with the CLI: scale the media nodes, change a parameter, and destroy the stack."
---

# OpenVidu Elastic administration: DigitalOcean

<div class="provider-chip" markdown>

:material-digital-ocean:{ .provider-chip-icon } DigitalOcean

</div>

The stack is operated from the directory that deployed it, with the same `ov stack` commands as any other OpenVidu deployment. The canonical operations page covers them all: [status](../../single-node/on-premises/admin.md#status), [describe](../../single-node/on-premises/admin.md#describe), the [health test](../../single-node/on-premises/admin.md#health-test), [logs](../../single-node/on-premises/admin.md#logs) and [start, stop and restart](../../single-node/on-premises/admin.md#start-stop-and-restart). Its [configuration](../../configuration/changing-config.md) and its [modules](../../how-to-guides/enable-disable-modules.md) are changed the same way as anywhere else.

This page covers only what is specific to DigitalOcean.

## Change a parameter of the stack

`ov stack deploy <name> --cloud digitalocean --param Name=Value` in the stack's directory runs `terraform apply` again with the parameters that changed. Any parameter the template declares can be set this way. Always name the stack in a redeploy: without the name it is registered again as `openvidu`.

For example, the master node's size (`masterNodeInstanceType`) or the media nodes' (`mediaNodeInstanceType`):

```bash
ov stack deploy openvidu --cloud digitalocean --param masterNodeInstanceType=s-8vcpu-16gb --mode auto -y
```

Before asking to go ahead, the redeploy reads Terraform's plan and says what it does: a new size resizes a Droplet in place (powered off for a few minutes, and none can move to a size with a smaller disk), and a change to what a node boots with creates it again. The media node size is baked into the autoscaler, so running media nodes keep their size until they are replaced.

For OpenVidu's own settings, which change without touching the machines, see [Changing configuration](../../configuration/changing-config.md).

## Scale the media nodes { #scale-the-media-nodes }

On a DigitalOcean Elastic stack the media nodes **autoscale** by default: the template's autoscaler runs between a minimum and a maximum and drains nodes gracefully when load drops. The minimum, the maximum and a fixed count are template parameters:

- `minNumberOfMediaNodes`, `maxNumberOfMediaNodes`: the range the autoscaler keeps.
- `fixedNumberOfMediaNodes`: `0` autoscales (the default); a positive number runs exactly that many media nodes and deploys no autoscaler.

On the first deploy, `--set infrastructure.mediaNodes.fixedCount=N` sets the fixed count as well. On a stack that is already running, change any of them with a redeploy from the stack's directory:

```bash
ov stack deploy openvidu --cloud digitalocean --param maxNumberOfMediaNodes=3 --mode auto -y
```

Or run exactly one media node:

```bash
ov stack deploy openvidu --cloud digitalocean --param fixedNumberOfMediaNodes=1 --mode auto -y
```

A media node that a change removes is never cut: the template marks it with the stack's draining tag, its watcher drains it (it takes no new rooms and waits for the rooms, recordings and ingests it holds to end) and then it leaves the cluster and is deleted. This is the same graceful drain the autoscaler runs on a scale-in. See [Autoscaling](../../production-ready/scalability.md#autoscaling) for the general model.

## Operate from another machine

--8<-- "self-hosting/digitalocean/ov-remote.md"

## Destroy the stack

--8<-- "self-hosting/digitalocean/ov-destroy.md"

## Backup and restore

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
