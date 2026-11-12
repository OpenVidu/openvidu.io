---
title: "Administer OpenVidu High Availability on DigitalOcean"
description: "Operate an OpenVidu High Availability DigitalOcean stack with the CLI: scale the media nodes, change a parameter, and destroy it."
---

# OpenVidu High Availability administration: DigitalOcean

<div class="provider-chip" markdown>

:material-digital-ocean:{ .provider-chip-icon } DigitalOcean

</div>

The sections up to [Export the desired state](#export) are the operations every OpenVidu stack shares, with the same commands wherever it runs. The rest of the page is specific to a High Availability stack on DigitalOcean.

--8<-- "self-hosting/common/ov-operate.md"

## Change a parameter of the stack

`ov stack deploy <name> --cloud digitalocean --param Name=Value` in the stack's directory runs `terraform apply` again with the parameters that changed. Any parameter the template declares can be set this way. Always name the stack in a redeploy: without the name it is registered again as `openvidu`.

For example, the master nodes' size (`masterNodesInstanceType`) or the media nodes' (`mediaNodeInstanceType`):

```bash
ov stack deploy openvidu --cloud digitalocean --param masterNodesInstanceType=s-8vcpu-16gb --mode auto -y
```

Before asking to go ahead, the redeploy reads Terraform's plan and says what it does: a new size resizes a Droplet in place (powered off for a few minutes, and none can move to a size with a smaller disk), and a change to what a node boots with creates it again. There are always four master nodes; the media node size is baked into the autoscaler, so running media nodes keep their size until they are replaced.

!!! warning "Do not rotate the API token with a redeploy"

    On High Availability, master-1's boot script carries the API token, so a redeploy that changes `$DIGITALOCEAN_TOKEN` plans `REPLACES master-1`. Do not rotate the token with a redeploy.

For OpenVidu's own settings, which change without touching the machines, see [Changing configuration](../../configuration/changing-config.md).

## Scale the media nodes { #scale-the-media-nodes }

On a DigitalOcean High Availability stack the media nodes **autoscale** by default: the template's autoscaler runs between a minimum and a maximum and drains nodes gracefully when load drops. The minimum, the maximum and a fixed count are template parameters:

- `minNumberOfMediaNodes`, `maxNumberOfMediaNodes`: the range the autoscaler keeps.
- `fixedNumberOfMediaNodes`: `0` autoscales (the default); a positive number runs exactly that many media nodes and deploys no autoscaler.

On the first deploy or on a redeploy, `--set infrastructure.mediaNodes.fixedCount=N` sets the fixed count as well. On a stack that is already running, change any of them with a redeploy from the stack's directory:

```bash
ov stack deploy openvidu --cloud digitalocean --param maxNumberOfMediaNodes=3 --mode auto -y
```

Or run exactly one media node:

```bash
ov stack deploy openvidu --cloud digitalocean --param fixedNumberOfMediaNodes=1 --mode auto -y
```

A media node that a change removes is never cut: the template marks it with the stack's draining tag, its watcher drains it (it takes no new rooms and waits for the rooms, recordings and ingests it holds to end) and then it leaves the cluster and is deleted. The redeploy's `terraform apply` waits for that drain, up to `$OPENVIDU_MEDIA_DRAIN_TIMEOUT` seconds (7200 by default; set it in the redeploy's environment), and past that limit the node is deleted as it is. This is the same graceful drain the autoscaler runs on a scale-in. The four master nodes are fixed and never scale. See [Autoscaling](../../production-ready/scalability.md#autoscaling) for the general model.

## Operate from another machine

--8<-- "self-hosting/digitalocean/ov-remote.md"

## Destroy the stack

--8<-- "self-hosting/digitalocean/ov-destroy.md"

## Backup and restore

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
