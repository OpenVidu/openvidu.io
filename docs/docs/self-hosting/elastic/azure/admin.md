---
title: "Administer OpenVidu Elastic on Azure"
description: "Administer an OpenVidu Elastic stack on Azure with the CLI: change a parameter, scale the media nodes, operate it remotely, and destroy it."
---

# OpenVidu Elastic administration: Azure

<div class="provider-chip" markdown>

:material-microsoft-azure:{ .provider-chip-icon } Azure

</div>

The sections up to [Export the desired state](#export) are the operations every OpenVidu stack shares, with the same commands wherever it runs. The rest of the page is specific to an Elastic stack on Azure.

--8<-- "self-hosting/common/ov-operate.md"

## Change a parameter of the stack

`ov stack deploy openvidu --cloud azure --param Name=Value` in the stack's directory runs the deployment again with only the parameters that changed; a redeploy with the same parameters reuses the stack as it is. Any parameter the template declares can be set this way, for example the media node size:

```bash
ov stack deploy openvidu --cloud azure --param mediaNodeInstanceType=Standard_F16s_v2 --mode auto -y
```

The media node **count** is a parameter too; see [Scale the media nodes](#scale-the-media-nodes) below. See [Changing configuration](../../configuration/changing-config.md) for OpenVidu's own settings, which change without touching the machines.

## Scale the media nodes { #scale-the-media-nodes }

On Azure the media nodes **autoscale** by default: the Virtual Machine Scale Set runs between `minNumberOfMediaNodes` and `maxNumberOfMediaNodes`, and a media node being removed drains gracefully, so autoscaling never cuts a live session. The range and a fixed count are template parameters, set when you deploy:

- `minNumberOfMediaNodes`, `maxNumberOfMediaNodes`: the autoscaling range.
- `fixedNumberOfMediaNodes` (`0` = autoscaling, the default): a value greater than `0` pins the scale set to exactly that many media nodes, and CPU usage no longer changes the count. At the first deploy, `--set infrastructure.mediaNodes.fixedCount=N` sets it too.

!!! warning "Changing the count on an existing Azure stack is not verified yet"

    Changing the media node count or the autoscaling limits of an Azure stack that is already running, by redeploying with new values, has not been verified on Azure yet. This page will cover it once it has.

See [Autoscaling](../../production-ready/scalability.md#autoscaling) for how autoscaling works across clouds.

## Operate from another machine

--8<-- "self-hosting/azure/ov-remote.md"

## Destroy the stack

--8<-- "self-hosting/azure/ov-destroy.md"

## Backup and restore

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
