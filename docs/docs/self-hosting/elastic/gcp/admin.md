---
title: "Administer OpenVidu Elastic on Google Cloud"
description: "Administer OpenVidu Elastic on Google Cloud from its directory: change a parameter, scale the media nodes, operate it remotely and destroy it."
---

# OpenVidu Elastic administration: Google Cloud Platform

<div class="provider-chip" markdown>

:material-google-cloud:{ .provider-chip-icon } Google Cloud Platform

</div>

A Google Cloud stack is operated from the directory that deployed it, with the same commands as any other OpenVidu stack. The canonical operations are documented once, on the On Premises page:

- [Status](../../single-node/on-premises/admin.md#status), [describe](../../single-node/on-premises/admin.md#describe), [health test](../../single-node/on-premises/admin.md#health-test) and [logs](../../single-node/on-premises/admin.md#logs).
- [Start, stop and restart](../../single-node/on-premises/admin.md#start-stop-and-restart).
- [Change the configuration](../../configuration/changing-config.md) of OpenVidu and [enable or disable modules](../../how-to-guides/enable-disable-modules.md), which change without touching the machines.

This page covers what is specific to a Google Cloud Elastic stack.

## Change a parameter of the stack { #change-a-parameter-of-the-stack }

`ov stack deploy <name> --cloud gcp --param Name=Value` in the stack's directory runs `terraform apply` again with the parameters that changed. Any parameter the template declares can be set this way. For example, the media-node instance type:

```bash
ov stack deploy openvidu --cloud gcp --param mediaNodeInstanceType=e2-standard-8 --mode auto -y
```

On a stack that already exists, auto mode runs `terraform plan` first (it changes nothing) and the plan says what it found before asking to go ahead. Whether a parameter change applies in place or replaces a machine depends on the template. For OpenVidu's own settings, which change without touching the machines, see [Changing configuration](../../configuration/changing-config.md).

## Scale the media nodes { #scale-the-media-nodes }

An Elastic stack scales beyond one machine by adding **media nodes**, in a managed instance group. By default the media nodes **autoscale**: the group runs between a minimum and a maximum, and removes nodes gracefully when load drops. The minimum, the maximum and a fixed count are parameters of the template:

| Parameter | Meaning |
| --- | --- |
| `minNumberOfMediaNodes`, `maxNumberOfMediaNodes` | the autoscaling range |
| `fixedNumberOfMediaNodes` | `0` (the default) autoscales; a value greater than `0` runs exactly that many media nodes, with no autoscaler |

At the first deploy, `--set infrastructure.mediaNodes.fixedCount=N` sets the fixed count as well. On a stack that is already running, change any of these with the template parameter. For example, raising the ceiling:

```bash
ov stack deploy openvidu --cloud gcp --param maxNumberOfMediaNodes=3 --mode auto -y
```

Lowering the count drains the extra media nodes **gracefully**: a media node that is being removed stops accepting new rooms and keeps running until the rooms, recordings and ingests it holds have ended, then leaves. That is why a scale-in never cuts a live session. For the general autoscaling model, see [Scalability](../../production-ready/scalability.md#autoscaling).

## Operate from another machine { #operate-from-another-machine }

--8<-- "self-hosting/gcp/ov-remote.md"

## Destroy the stack { #destroy-the-stack }

--8<-- "self-hosting/gcp/ov-destroy.md"

## Backup and restore { #backup-and-restore }

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
