---
title: "Administer OpenVidu Elastic on Oracle Cloud"
description: "Operate an OpenVidu Elastic stack on Oracle Cloud with the OpenVidu CLI: scale the media nodes, change a parameter and destroy the stack."
---

# OpenVidu Elastic administration: Oracle Cloud Infrastructure

--8<-- "self-hosting/oracle/provider-chip.md"

An Oracle Cloud Elastic stack is operated from the directory that deployed it, with the same commands as any other stack. The canonical operations page documents them all:

- [Status](../../single-node/on-premises/admin.md#status), [describe](../../single-node/on-premises/admin.md#describe), the [health test](../../single-node/on-premises/admin.md#health-test) and the [logs](../../single-node/on-premises/admin.md#logs).
- [Start, stop and restart](../../single-node/on-premises/admin.md#start-stop-and-restart).
- [Change its configuration](../../configuration/changing-config.md#view-get-set-unset) and [enable or disable modules](../../how-to-guides/enable-disable-modules.md#modules-and-services).

What follows is specific to an Oracle Cloud deployment.

## Change a parameter of the stack { #change-a-parameter-of-the-stack }

Any parameter the Oracle template declares is changed from the stack's directory with `ov stack deploy <name> --cloud oracle --param Name=Value`, which runs `terraform apply` again with the parameters that changed. A redeploy reads Terraform's plan first and says what it does before you answer: an instance whose shape, OCPUs or memory change restarts in place, while a change to what the master boots with (the domain, the certificate, the license, the Meet credentials or a newer OpenVidu CLI) `REPLACES the master`, which comes back with a new public IP.

To change OpenVidu's own settings without touching the machines, use [its configuration](../../configuration/changing-config.md#view-get-set-unset), not a redeploy.

## Scale the media nodes { #scale-the-media-nodes }

The number of media nodes is a variable of the template, so it changes with a redeploy that names the stack and the variable. On a cloud stack the media nodes **autoscale** by default: the OCI Instance Pool runs between `minNumberOfMediaNodes` and `maxNumberOfMediaNodes`, adding a node when the pool's average CPU goes over `scaleTargetCPU`, and the scale-in OCI Function removes nodes gracefully when load drops. See [Autoscaling](../../production-ready/scalability.md#autoscaling).

Run exactly N media nodes, with no autoscaling and no scale-in Function:

```bash
ov stack deploy openvidu --cloud oracle --param fixedNumberOfMediaNodes=2 --mode auto
```

Back to autoscaling, with another ceiling:

```bash
ov stack deploy openvidu --cloud oracle --param fixedNumberOfMediaNodes=0 \
  --param maxNumberOfMediaNodes=6 --mode auto
```

!!! info "The media nodes that go drain first"

    No live session is cut. Lowering `fixedNumberOfMediaNodes`, narrowing the autoscaling range, or moving between a fixed count and the autoscaler (whose start sets the pool to `initialNumberOfMediaNodes`) detaches the nodes that go, newest first. Each one takes no new rooms, waits for the rooms, recordings and ingests on it to end, leaves the cluster and terminates itself, and the apply waits for that, up to `$OPENVIDU_MEDIA_DRAIN_TIMEOUT` seconds (7200 by default). This runs on your machine, with `oci` and `jq`. Raising the count adds media nodes and leaves the running ones untouched. The destroy of the whole stack drains nothing.

    A media node takes no SSH, so to follow one that drains, read its `openvidu-scale-in` tag (`draining`, then `left`) in the OCI console, or its watcher's log on its serial console:

    ```bash
    oci compute console-history capture --instance-id <node-ocid>   # prints the history's id
    oci compute console-history get-content --instance-console-history-id <id> \
      --length 1000000 --file - | grep openvidu-scalein-watch
    ```

On the first deploy, `--set infrastructure.mediaNodes.fixedCount=N` sets the same fixed count. `ov stack check-ports` does not apply to this stack: it needs SSH access to the node, and the stack is operated without it (exit `2`).

## Operate from another machine { #operate-from-another-machine }

--8<-- "self-hosting/oracle/ov-remote.md"

## Destroy the stack { #destroy-the-stack }

--8<-- "self-hosting/oracle/ov-destroy.md"

## Backup and restore { #backup-and-restore }

--8<-- "self-hosting/oracle/backup-and-restore.md"
