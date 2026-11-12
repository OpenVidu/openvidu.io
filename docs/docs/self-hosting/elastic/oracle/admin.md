---
title: "Administer OpenVidu Elastic on Oracle Cloud"
description: "Operate an OpenVidu Elastic stack on Oracle Cloud with the OpenVidu CLI: scale the media nodes, change a parameter and destroy the stack."
---

# OpenVidu Elastic administration: Oracle Cloud Infrastructure

--8<-- "self-hosting/oracle/provider-chip.md"

The sections up to [Export the desired state](#export) are the operations every OpenVidu stack shares, with the same commands wherever it runs. The rest of the page is specific to an Elastic stack on Oracle Cloud.

--8<-- "self-hosting/common/ov-operate.md"

## Change a parameter of the stack { #change-a-parameter-of-the-stack }

Any parameter the Oracle template declares is changed from the stack's directory with `ov stack deploy <name> --cloud oracle --param Name=Value`, which runs `terraform apply` again with the parameters that changed. A redeploy reads Terraform's plan first and says what it does before you answer: an instance whose shape, OCPUs or memory change restarts in place, while a change to what the master boots with (a `--param` of its first-boot data, such as `domainName` or `certificateType`, or a newer OpenVidu CLI) `REPLACES the master`, which comes back with a new public IP. The settings a redeploy gives (`--domain-name`, `--certificate-type` and the own certificate, the license, any other friendly flag, `--set` and `--set-secret`) never reach the template: `ov` applies them in the running stack, as `ov stack config set` does, and the machine is not touched.

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

`--set infrastructure.mediaNodes.fixedCount=N` sets the same fixed count, on the first deploy or on a redeploy. To check the node's inbound ports, use `ov stack check-ports`: a cloud PRO stack keeps no SSH access in its record, so the command exits `2` and prints the one that does work, `ov stack check-ports --ssh <user>@<master> --ssh-key <key>` (the master's public address, and the private key the template keeps in Object Storage, at the object the `ssh_private_key_object` output names: see [Access OpenVidu](install.md#access-openvidu)). Run that command between `ov stack stop` and `ov stack start` to verify the media ports too.

## Operate from another machine { #operate-from-another-machine }

--8<-- "self-hosting/oracle/ov-remote.md"

## Destroy the stack { #destroy-the-stack }

--8<-- "self-hosting/oracle/ov-destroy.md"

## Backup and restore { #backup-and-restore }

--8<-- "self-hosting/oracle/backup-and-restore.md"
