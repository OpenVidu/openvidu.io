---
title: "Administer OpenVidu High Availability on-premises"
description: "Administer OpenVidu High Availability on your own servers with the OpenVidu CLI: join and drain nodes, operate the stack, and back up its data."
---

# OpenVidu High Availability administration: On-premises

<div class="provider-chip" markdown>

:material-server:{ .provider-chip-icon } On-premises

</div>

The sections up to [Export the desired state](#export) are the operations every OpenVidu stack shares, with the same commands wherever it runs. The rest of the page is specific to a High Availability stack on your own servers.

--8<-- "self-hosting/common/ov-operate.md"

## Add a media node { #add-a-media-node }

From the stack's directory, `ov stack join --ssh ubuntu@<media-node> --as media` reads the join address and token from a master, checks the ports, installs the node agent and joins the machine, returning once the stack sees it ready. There are three ways to run it, exactly as on [Elastic](../../elastic/on-premises/admin.md#add-a-media-node): over SSH, on the machine itself (`--this-node` with `ov stack join-info` for the address and token), or with `--mode assisted` to print the commands and run nothing.

## Add a master node

High Availability runs four masters. A master is added with `--as master` (masters 2-4), which takes `--domain`, `--lb-host` and `--public-ip`, the addresses at which the stack's remote admin control protocol (port `6443`) must remain reachable:

```bash
ov stack join --ssh ubuntu@<master> --as master --lb-host <load-balancer> --public-ip <master's public IP>
```

A master join checks the cluster's internal ports in both directions with the masters already in the stack (the API on `6443/tcp`, etcd on `2379-2380/tcp`, the kubelet on `10250/tcp`, the overlay on `8472/udp`) and confirms the node carries the labels the stack schedules by. See [Deploy with a DNS record per master](install-nlb.md#deploy-with-a-dns-record-per-master) and [In production: behind a load balancer](install-nlb.md#behind-a-load-balancer).

## Take a media node out { #take-a-node-out }

`join` leaves `ov` on the server, so a media node can leave by itself. Log in to it and drain it:

```console
$ ssh ubuntu@172.30.0.114 sudo ov stack leave --this-node --drain --uninstall
⏳ draining node-172-30-0-114: no new rooms come here; waiting, with no time limit, for the ones it holds
✔ node-172-30-0-114 has no sessions left.
✔ this machine left the stack.
```

`ov stack leave --this-node` stops the node agent, so the stack sees the node leave; `--uninstall` also removes the agent (the server can join again later). **Only a media node leaves**: on a master the command is refused and touches nothing, because stopping a master stops the stack.

## Graceful drain { #graceful-drain }

A media node that is being removed must not drop the rooms, recordings or ingests it holds. With `--drain`, the stack stops sending new rooms to the node, and the command waits, **with no time limit**, until everything the node holds has ended, then leaves. The stack deletes the node afterwards. If the command is interrupted, the node keeps draining, and running it again resumes the wait.

## Destroy

`ov stack destroy` from the stack's directory removes OpenVidu from the cluster; the machines and their node agents stay. As on a [single node](../../single-node/on-premises/admin.md#destroy), it must be told what happens to the data: `--keep-data` keeps the stack's data, configuration and credentials on the masters and leaves the media nodes joined, so the same `ov stack deploy` brings the stack back; `--delete-data` removes all of it.

```console
$ ov stack destroy --delete-data -y
uninstalling OpenVidu…
removing the stack's resources…
stack removed, with its data and its configuration
✔ removed stack "ha" from this directory
```

`--delete-data` cannot be undone: back up first. To take a media node out of the cluster afterwards, run `sudo ov stack leave --this-node --uninstall` on it.

## Backup and restore

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
