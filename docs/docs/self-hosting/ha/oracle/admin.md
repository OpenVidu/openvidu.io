---
title: "Administer OpenVidu High Availability on Oracle Cloud"
description: "Operate an OpenVidu High Availability stack on Oracle Cloud with the OpenVidu CLI: scale the media nodes, change a parameter and destroy it."
---

# OpenVidu High Availability administration: Oracle Cloud Infrastructure

--8<-- "self-hosting/oracle/provider-chip.md"

The sections up to [Export the desired state](#export) are the operations every OpenVidu stack shares, with the same commands wherever it runs. The rest of the page is specific to a High Availability stack on Oracle Cloud.

--8<-- "self-hosting/common/ov-operate.md"

## Change a parameter of the stack { #change-a-parameter-of-the-stack }

Any parameter the Oracle template declares is changed from the stack's directory with `ov stack deploy <name> --cloud oracle --param Name=Value`, which runs `terraform apply` again with the parameters that changed. A redeploy reads Terraform's plan first and says what it does before you answer: an instance whose shape, OCPUs or memory change restarts in place. Masters 2-4 are never recreated for their boot script; a change to what master-1 boots with (a `--param` of its first-boot data or a newer OpenVidu CLI) replaces master-1 only. The settings a redeploy gives (`--domain-name`, `--certificate-type` and the own certificate, the license, any other friendly flag, `--set` and `--set-secret`) never reach the template: `ov` applies them in the running stack, as `ov stack config set` does, and the machine is not touched.

To change OpenVidu's own settings without touching the machines, use [its configuration](../../configuration/changing-config.md#view-get-set-unset), not a redeploy.

## Scale the media nodes { #scale-the-media-nodes }

The number of media nodes is a variable of the template, so it changes with a redeploy that names the stack and the variable. On a cloud stack the media nodes **autoscale** by default: the OCI Instance Pool runs between `minNumberOfMediaNodes` and `maxNumberOfMediaNodes`, adding a node when the pool's average CPU goes over `scaleTargetCPU`, and the scale-in OCI Function removes nodes gracefully when load drops. See [Autoscaling](../../production-ready/scalability.md#autoscaling).

Run exactly N media nodes, with no autoscaling and no scale-in Function:

```bash
ov stack deploy openvidu --cloud oracle --param fixedNumberOfMediaNodes=2 --mode auto
```

Back to autoscaling, with another ceiling (outside `eu-madrid-1`, autoscaling needs `--param scale_in_function_image=<image>` too: see the [requirements](install.md#requirements)):

```bash
ov stack deploy openvidu --cloud oracle --param fixedNumberOfMediaNodes=0 \
  --param maxNumberOfMediaNodes=6 --mode auto
```

!!! info "The media nodes that go drain first"

    No live session is cut. Lowering the count or narrowing the autoscaling range detaches the nodes that go, newest first: each one takes no new rooms, waits for the rooms, recordings and ingests on it to end, leaves the cluster and terminates itself, and the apply waits for that, up to `$OPENVIDU_MEDIA_DRAIN_TIMEOUT` seconds (7200 by default), using `oci` and `jq` on your machine. Raising the count leaves the running nodes untouched, and destroying the whole stack drains nothing. To follow a node that drains, read its `openvidu-scale-in` tag (`draining`, then `left`) in the OCI console.

`--set infrastructure.mediaNodes.fixedCount=N` sets the same fixed count, on the first deploy or on a redeploy. To [check the ports](#ports) of a node, the key to pass is the one the template keeps in Object Storage ([Access OpenVidu](install.md#access-openvidu)).

A change of the number of media nodes returns when the cloud has taken it: the new machines boot and join on their own, minutes later. `ov stack status --wait` waits for them, since on a cloud it counts the media nodes the stack asks for, not only the ones that have joined (`media nodes 1/2` until the second is in).

## Operate from another machine { #operate-from-another-machine }

--8<-- "self-hosting/oracle/ov-remote.md"

## Destroy the stack { #destroy-the-stack }

--8<-- "self-hosting/oracle/ov-destroy.md"

## Backup and restore { #backup-and-restore }

--8<-- "self-hosting/oracle/backup-and-restore.md"
