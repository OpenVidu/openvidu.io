---
title: "Administer OpenVidu High Availability on Google Cloud"
description: "Administer OpenVidu High Availability on Google Cloud from its directory: change a parameter, scale the media nodes, operate it remotely and destroy it."
---

# OpenVidu High Availability administration: Google Cloud Platform

<div class="provider-chip" markdown>

:material-google-cloud:{ .provider-chip-icon } Google Cloud Platform

</div>

The sections up to [Export the desired state](#export) are the operations every OpenVidu stack shares, with the same commands wherever it runs. The rest of the page is specific to a High Availability stack on Google Cloud.

--8<-- "self-hosting/common/ov-operate.md"

## Change a parameter of the stack { #change-a-parameter-of-the-stack }

`ov stack deploy <name> --cloud gcp --param Name=Value` in the stack's directory runs `terraform apply` again with the parameters that changed. Any parameter the template declares can be set this way. For example, the master-node instance type:

```bash
ov stack deploy openvidu --cloud gcp --param masterNodeInstanceType=e2-standard-8 --mode auto -y
```

On a stack that already exists, auto mode runs `terraform plan` first (it changes nothing) and the plan says what it found before asking to go ahead. A new node size is an update in place (the machines carry `allow_stopping_for_update`), but a change to what a machine **boots with** — the domain, the certificate, the license, the Meet credentials or another OpenVidu CLI build — makes Terraform recreate that machine from scratch: its disk is lost and it is down until it installs again (the reserved addresses stay, so the public IPs do not change). The plan prints `REPLACES the machine` when it will; run `--mode assisted` to read Terraform's plan yourself first. For OpenVidu's own settings, which change without touching the machines, see [Changing configuration](../../configuration/changing-config.md).

## Scale the media nodes { #scale-the-media-nodes }

A High Availability stack scales its **media nodes** in a managed instance group. By default the media nodes **autoscale**: the group runs between a minimum and a maximum, and removes nodes gracefully when load drops. The four master nodes are fixed. The minimum, the maximum and a fixed count are parameters of the template:

| Parameter | Meaning |
| --- | --- |
| `minNumberOfMediaNodes`, `maxNumberOfMediaNodes` | the autoscaling range |
| `fixedNumberOfMediaNodes` | `0` (the default) autoscales; a value greater than `0` runs exactly that many media nodes, with no autoscaler |

`--set infrastructure.mediaNodes.fixedCount=N` sets the fixed count the same way (`--param fixedNumberOfMediaNodes=N` is its template-parameter form). Any of these — the autoscaling range or the fixed count — works on the first deploy and can be changed on a later redeploy. For example, raising the ceiling:

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
