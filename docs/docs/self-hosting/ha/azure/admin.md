---
title: "Administer OpenVidu High Availability on Azure"
description: "Administer an OpenVidu High Availability stack on Azure with the CLI: change a parameter, scale the media nodes, operate it remotely, and destroy it."
---

# OpenVidu High Availability administration: Azure

<div class="provider-chip" markdown>

:material-microsoft-azure:{ .provider-chip-icon } Azure

</div>

The Azure stack is operated from the directory that deployed it, with the same `ov stack` commands as any other OpenVidu stack. The day-to-day operations are documented once, for an on-premises deployment, and apply here unchanged:

- [Status](../../single-node/on-premises/admin.md#status), [describe](../../single-node/on-premises/admin.md#describe) and the [health test](../../single-node/on-premises/admin.md#health-test).
- [Logs](../../single-node/on-premises/admin.md#logs), and [start, stop and restart](../../single-node/on-premises/admin.md#start-stop-and-restart).
- [Change its configuration](../../configuration/changing-config.md) and [enable or disable modules](../../how-to-guides/enable-disable-modules.md).

## Change a parameter of the stack

`ov stack deploy openvidu --cloud azure --param Name=Value` in the stack's directory runs the deployment again with only the parameters that changed; a redeploy with the same parameters reuses the stack as it is. Any parameter the template declares can be set this way, for example the media node size:

```bash
ov stack deploy openvidu --cloud azure --param mediaNodeInstanceType=Standard_F16s_v2 --mode auto -y
```

The master nodes are a fixed four; High Availability does not change that. The media node **count** is a parameter; see [Scale the media nodes](#scale-the-media-nodes) below. See [Changing configuration](../../configuration/changing-config.md) for OpenVidu's own settings, which change without touching the machines.

## Scale the media nodes { #scale-the-media-nodes }

On Azure the media nodes **autoscale** by default: the Virtual Machine Scale Set runs between `minNumberOfMediaNodes` and `maxNumberOfMediaNodes`, and a media node being removed drains gracefully, so autoscaling never cuts a live session. The minimum, the maximum and a fixed count are template parameters:

- `minNumberOfMediaNodes`, `maxNumberOfMediaNodes`: the autoscaling range.
- `fixedNumberOfMediaNodes` (`0` = autoscaling, the default): a value greater than `0` pins the scale set to exactly that many media nodes, and CPU usage no longer changes the count.

Change any of them from the stack's directory:

```bash
ov stack deploy openvidu --cloud azure --param maxNumberOfMediaNodes=3 --mode auto -y
```

At the **first** deploy, `--set infrastructure.mediaNodes.fixedCount=N` sets the fixed count as well.

!!! note "Lowering the count on Azure"

    Each media node protects itself from scale-in, and Azure refuses an autoscale update whose minimum or maximum falls below the protected instances. So a redeploy fails while more media nodes are running than the new minimum (`UnsupportedCapacity`). Drain the extra media nodes gracefully first, then redeploy with the lower number.

See [Autoscaling](../../production-ready/scalability.md#autoscaling) for how autoscaling works across clouds.

## Operate from another machine

--8<-- "self-hosting/azure/ov-remote.md"

## Destroy the stack

--8<-- "self-hosting/azure/ov-destroy.md"

## Backup and restore

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
