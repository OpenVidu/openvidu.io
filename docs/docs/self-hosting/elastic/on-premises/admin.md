---
title: "Administer OpenVidu Elastic on-premises"
description: "Administer OpenVidu Elastic on your own servers with the OpenVidu CLI: add and drain media nodes, operate the stack, and back up its data."
---

# OpenVidu Elastic administration: On-premises

<div class="provider-chip" markdown>

:material-server:{ .provider-chip-icon } On-premises

</div>

The sections up to [Export the desired state](#export) are the operations every OpenVidu stack shares, with the same commands wherever it runs. The rest of the page is specific to an Elastic stack on your own servers.

--8<-- "self-hosting/common/ov-operate.md"

## Add a media node { #add-a-media-node }

Elastic scales by adding media nodes. From the stack's directory, `ov stack join` enrolls a new machine as a media node. There are three ways to run it:

- **Over SSH** (the usual way): `ov stack join --ssh ubuntu@<media-node> --as media`. See [Join a media node](install.md#join-a-media-node).
- **On the machine itself**: run `ov stack join --this-node --as media` on the node, as root, with the address and token `ov stack join-info` prints on the master (treat the token as a secret). Pipe them so the token touches no file or command line:

    ```bash
    ssh <master> sudo ov stack join-info | ssh <media-node> sudo ov stack join --this-node --as media --join-info -
    ```

- **Review the commands first**: add `--mode assisted` to the SSH form; it prints the commands and runs nothing.

An Elastic stack has one master, so every other machine joins `--as media`. On a cloud stack the media nodes autoscale instead; see [Autoscaling](../../production-ready/scalability.md#autoscaling).

## Take a media node out { #take-a-node-out }

`join` leaves `ov` on the server, so a media node can leave by itself. Log in to it and drain it:

```console
$ ssh ubuntu@172.30.0.102 sudo ov stack leave --this-node --drain --uninstall
⏳ draining node-172-30-0-102: no new rooms come here; waiting, with no time limit, for the ones it holds
  …
✔ node-172-30-0-102 has no sessions left.
✔ this machine left the stack.
```

`ov stack leave --this-node` stops the node agent, so the stack sees the node leave; `--uninstall` also removes the agent (the server can join again later). Only a media node leaves: on the master the command is refused and touches nothing.

## Graceful drain { #graceful-drain }

A media node that is being removed must not drop the rooms, recordings or ingests it holds. With `--drain`, the stack stops sending new rooms to the node, and the command waits, **with no time limit**, until everything the node holds has ended, then leaves. The stack deletes the node afterwards. If the command is interrupted, the node keeps draining, and running it again resumes the wait.

A cloud media node that the autoscaler is about to terminate runs exactly this on its own. That is why autoscaling never cuts a live session: the node finishes its rooms before the machine is removed.

## Destroy

`ov stack destroy` from the stack's directory removes OpenVidu from the cluster; the machines and their node agents stay. As on a [single node](../../single-node/on-premises/admin.md#destroy), it must be told what happens to the data: `--keep-data` keeps the stack's data, configuration and credentials on the master and leaves the media nodes joined, so the same `ov stack deploy` brings the stack back; `--delete-data` removes all of it.

```console
$ ov stack destroy --delete-data -y
uninstalling OpenVidu…
removing the stack's resources…
stack removed, with its data and its configuration
✔ removed stack "el" from this directory
```

`--delete-data` cannot be undone: back up first. To take a media node out of the cluster afterwards, run `sudo ov stack leave --this-node --uninstall` on it.

## Backup and restore

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
