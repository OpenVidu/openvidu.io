---
title: "Administer OpenVidu High Availability on AWS"
description: "Administer an OpenVidu High Availability AWS stack with the OpenVidu CLI: scale the media nodes, change parameters, operate it remotely and destroy it."
---

# OpenVidu High Availability administration: AWS

<div class="provider-chip" markdown>

:material-aws:{ .provider-chip-icon } AWS

</div>

The sections up to [Export the desired state](#export) are the operations every OpenVidu stack shares, with the same commands wherever it runs. The rest of the page is specific to a High Availability stack on AWS.

--8<-- "self-hosting/common/ov-operate.md"

## Change a parameter of the stack

`ov stack deploy <name> --cloud aws --param Name=Value` in the stack's directory updates the CloudFormation stack with the parameters that changed. Any parameter the template declares can be set this way, for example the media node instance size:

```bash
ov stack deploy openvidu --cloud aws --param MediaNodeInstanceType=c6a.2xlarge --mode auto -y
```

The stack that exists is updated with the parameters that changed; a redeploy with the same parameters reuses it as it is. For OpenVidu's own settings, which change without touching the machines, see [Changing configuration](../../configuration/changing-config.md).

!!! info

    On a High Availability stack, the domain and the TURN domain do not change once the stack exists: the load balancers serve the ACM certificate of the names the stack was created with. A redeploy with another `--domain-name` or `--turn-domain-name`, and an `ov stack config set domain-name=…` or `turn-domain-name=…`, are refused with exit `4` and nothing written. To change the domain, destroy the stack and deploy it again. A Single Node or Elastic stack serves its certificate from Caddy, so its domain changes like anywhere else.

## Scale the media nodes { #scale-the-media-nodes }

The media nodes **autoscale** by default: an AWS Auto Scaling Group runs between a minimum and a maximum and removes nodes gracefully when load drops. The minimum, the maximum and a fixed count are parameters of the template:

| Parameter | Meaning |
| --- | --- |
| `MinNumberOfMediaNodes`, `MaxNumberOfMediaNodes` | The autoscaling range |
| `FixedNumberOfMediaNodes` | A fixed number of media nodes (`0` = autoscaling, the default) |

On the first deploy and on a redeploy alike, `--set infrastructure.mediaNodes.fixedCount=N` sets the fixed count (the same as `--param FixedNumberOfMediaNodes=N`). Change it from the stack's directory, for example raising the ceiling:

```bash
ov stack deploy openvidu --cloud aws --param MaxNumberOfMediaNodes=3 --mode auto -y
```

The master nodes are a fixed set of four and are not scaled. A media node that is scaled in is **drained gracefully**: the stack stops sending it new rooms and the machine is removed only once the rooms, recordings and ingests it holds have ended. That is why autoscaling never cuts a live session. See [Autoscaling](../../production-ready/scalability.md#autoscaling) for how the scaling signal works.

## Operate from another machine

--8<-- "self-hosting/aws/ov-remote.md"

## Destroy the stack

--8<-- "self-hosting/aws/ov-destroy.md"

## Backup and restore

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
