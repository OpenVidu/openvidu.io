---
title: "Scale OpenVidu media nodes with the CLI"
description: "Scale an Elastic or High Availability OpenVidu stack: autoscaling or a fixed media-node count, join and remove nodes, and drain them gracefully."
---

# Scaling

Elastic and High Availability stacks grow past one machine with **media nodes**. They are OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag } only. The stack is deployed on the master; every media node (and, for HA, every other master) **joins** it.

## Autoscaling vs a fixed count

On a cloud stack the media nodes **autoscale** by default: the cloud's auto scaling group runs between a minimum and a maximum you set, and removes nodes gracefully when load drops (see [Graceful drain](#graceful-drain)). The minimum and maximum are template parameters (`MinNumberOfMediaNodes` / `MaxNumberOfMediaNodes` on AWS, and the equivalents on each cloud), changed with `--param`.

To run **exactly N media nodes with no autoscaling**, set a fixed count — on every cloud:

```bash
ov stack deploy --cloud aws --set infrastructure.mediaNodes.fixedCount=3 --mode auto -y
# equivalently, through the template parameter:
ov stack deploy --cloud aws --param FixedNumberOfMediaNodes=3 --mode auto -y
```

`0` (the default) means autoscaling.

## Redeploy with `--param`

Any parameter the cloud template declares is changed from the stack's directory with `ov stack deploy --cloud <cloud> --param Name=Value`. The stack that exists is **updated** with the parameters that changed, compared against what it runs with; a redeploy with the same parameters reuses it as it is. For example, raising the ceiling of an Elastic stack:

```console
$ ov stack deploy --cloud aws --param MaxNumberOfMediaNodes=3 --mode auto -y
The CloudFormation stack ov-aws-im2 already exists (CREATE_COMPLETE): the parameters that changed are applied to it
as an update; CloudFormation keeps every resource they do not touch.
…
▶ Create the machines on AWS…
   · update the CloudFormation stack ov-aws-im2 with the parameters that changed (this returns when CloudFormation is done)
   ✓ Create the machines on AWS
…
```

Whether a parameter is changed in place or replaces a machine is the template's; when it matters, check first with a change set or `terraform plan`.

!!! note "Azure Elastic and HA"

    Each media node protects itself from scale-in, and Azure refuses an autoscale update whose minimum or maximum falls below the protected instances. So a redeploy while more media nodes run than the new minimum fails on Azure. Lower the count when fewer nodes are running.

## Add a node to an on-premises stack

On your own servers you add nodes yourself. From the stack's directory, `ov stack join --ssh` reads the join address and token from the deployed master and joins the machine over SSH:

```console
$ ov stack join --ssh ubuntu@172.30.0.97 --as media
→ reading the join address and token from 172.30.0.96

▶ Connect…
   ✓ Connect

▶ Join the cluster…
   · upload the OpenVidu node-agent installer
   · join 172.30.0.97 to the stack as a media node
   ✓ Join the cluster

▶ Leave the OpenVidu CLI on the node…
   ✓ Leave the OpenVidu CLI on the node

▶ Wait for the stack to see the node…
   ✓ Wait for the stack to see the node

✔ 172.30.0.97 joined the stack as a media node.
```

The token never appears on screen. The login, key and port default to the ones the stack recorded (`--ssh-user`, `--ssh-key`, `--ssh-port` override them). The join returns once the stack sees the node ready, so what it schedules there already exists. `--as master` adds an HA control-plane node (HA masters 2-4); it is refused on an Elastic stack and on any single node. A master join takes `--domain`, `--lb-host` and `--public-ip`, the names the cluster API must stay reachable at.

`join` runs a port check before anything is installed (`--skip-port-check` to turn it off); a required port closed exits `6` with the rule to add, scoped to the source.

### Joining the machine itself

On the machine that will join, `ov stack join --this-node --as master|media` enrols it directly (as root). It takes the address and token from `--address`/`--token` or the environment variables `OPENVIDU_JOIN_ADDRESS` and `OPENVIDU_JOIN_TOKEN`. Get those from the deployed node:

```bash
ov stack join-info          # prints OPENVIDU_JOIN_ADDRESS and OPENVIDU_JOIN_TOKEN
```

<!-- PENDING-RUN (docs-ov): ov stack join-info output -->

`ov stack join-info --wait 30m` blocks until the cluster is up; `--format json` for machine consumption.

## Take a node out

`join` leaves `ov` on the server, so the server can leave by itself. Log into it and drain it:

```console
$ ssh ubuntu@172.30.0.97 sudo ov stack leave --this-node --drain --uninstall
⏳ draining fake-vm-172-30-0-97: no new rooms come here; waiting, with no time limit, for the ones it holds
  still serving after 0s: openvidu-elastic/ov-egress-7v7tk openvidu-elastic/ov-ingress-6hshv openvidu-elastic/ov-livekit-server-zgkhk
✔ fake-vm-172-30-0-97 has no sessions left.
✔ this machine left the stack.
```

- `ov stack leave --this-node` stops the node agent so the stack sees the node leave and stops scheduling on it.
- `--uninstall` also removes the node agent (the same server can join again later).
- `--drain` (media nodes) leaves **gracefully**.

## Graceful drain

A media node that is being removed must not drop the rooms, recordings or ingests it holds. With `--drain`, the stack stops sending new rooms to the node, and the command waits — **with no time limit** — until everything the node holds has ended, then leaves. The stack deletes the node afterwards. Interrupted, the node keeps draining, and running the command again resumes the wait.

This is exactly what a cloud autoscaler's about-to-terminate media node runs on its own, which is why autoscaling never cuts a live session: the node finishes its rooms before the machine goes.

## Next steps

- Deploy an [Elastic or HA stack on your servers](../deploy/on-premises.md) or on [AWS](../deploy/aws.md).
- [Change a template parameter](../deploy/aws.md#change-a-parameter-of-the-stack) of a cloud stack.
- The full [command reference](../reference.md).
