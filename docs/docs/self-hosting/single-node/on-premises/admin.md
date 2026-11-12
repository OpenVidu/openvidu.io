---
title: "Administer OpenVidu Single Node on-premises"
description: "Administer OpenVidu Single Node on your own servers with the OpenVidu CLI: status, logs, the health check, start and stop, and backup."
---

# OpenVidu Single Node administration: On-premises

<div class="provider-chip" markdown>

:material-server:{ .provider-chip-icon } On-premises

</div>


Every command on this page operates on **the stack in the current directory** (the one the deploy created, or one adopted with [`ov stack import`](#operate-from-another-machine)), with no name and no flags. From anywhere else, `--dir <path>` points to it. On the server itself the stack directory is `/opt/openvidu/stack`, so `sudo ov stack status` works there with no directory to name.

This page is the canonical operations reference for every Single Node deployment, on your own servers and on every cloud.

## Status { #status }

`ov stack status` prints the state of each node. On a Community server it also shows the data disk, the filesystem that holds `/opt/openvidu`, where the recordings and the databases grow:

```console
$ ov stack status
HOST          ROLE     STATE    DATA DISK USED
172.30.0.96   single   active   55% (397.0 GiB free)
```

From 85% used the status adds a warning. On a PRO stack (Kubernetes) it shows the workloads instead, one row per service (`SERVICE NODES READY STATE`), and after them each node's disk (`NODE ROLE DISK USED FREE SIZE`, the node's root filesystem where the stack's volumes grow); it warns at 85% used or when the node reports `DiskPressure`. A node it cannot reach over SSH shows `unreachable` in its row, and the exit code is still `0`.

`--wait` blocks until the stack is ready. On a Community server it probes the node itself (Caddy, the media server and each enabled module's web endpoint) over the stack's own transport, so no DNS or route from your machine is needed:

```console
$ ov stack status --wait
waiting for OpenVidu to be ready on the node (Ctrl-C to stop waiting; the deployment keeps running)…
  ⏳ still starting: openvidu, meet (0s)
  ⏳ still starting: openvidu (5s)
✔ OpenVidu is ready at https://172-30-0-96.openvidu-local.dev (caddy, openvidu, dashboard, meet)
```

Right after a first PRO deploy, while the node pulls the images and some pods restart before they settle, the wait can take longer than the default 5 minutes: raise it with `--wait-timeout 15m`.

## Describe { #describe }

`ov stack describe` prints the stack's record, endpoints and a configuration summary:

```console
$ ov stack describe
Stack:       qce1
Type:        single_node
Environment: on-premises
Edition:     community
Endpoint:    https://172-30-0-150.openvidu-local.dev
Spec:        openvidu-stack.yml
Access:      ssh

Nodes:
  172.30.0.150     single       active
```

`Access` says how this directory reaches the stack: `ssh` for a Community server, `kube` (the cluster API) for a PRO stack, `local` for a stack on this machine.

## Health test { #health-test }

`ov stack test` is an active health check. It exits `8` on failure, so it works in CI:

```console
$ ov stack test
✓ openvidu-active    172.30.0.96   active
all 1 check(s) passed
```

On PRO it checks the cluster API and the pods:

```console
$ ov stack test
✓ Kubernetes API reachable
✓ 16/16 pods ready
all 2 check(s) passed
```

## Logs { #logs }

`ov stack logs` fetches the logs of the whole stack as one interleaved stream; `--since` limits the time window and `-f` follows them live. On a server they come from the node's journal, so `--tail N` is the last N lines of the whole stack (`--since` takes a journal value such as `'1 hour ago'`):

```console
$ ov stack logs --tail 8
==> 172.30.0.96 (single) <==
Nov 04 03:26:57 node-172-30-0-96 docker[4229]: mongodb            | {"t":{"$date":"2026-11-04T03:26:57.833+00:00"}, …
Nov 04 03:26:58 node-172-30-0-96 docker[4229]: ov-livekit-server  | 2026-11-04T03:26:58.118Z        WARN        livekit  …
…
```

Per-service logs through `ov` are not available yet. Read one service's logs with the engine underneath: `docker compose logs <service>` in the deployment directory on a Community server, or `kubectl -n <namespace> logs <pod>` on PRO.

## Ports { #ports }

`ov stack check-ports` verifies that the inbound ports a stack needs actually reach the server, so it needs SSH access to the node. It runs a temporary listener on the node and probes it, so TCP **and** UDP (and the media range) are really verified. It is the single most useful check before going live, because a stack with a blocked media port looks perfectly healthy and simply has no media.

Against a running stack, `ov` can only connect to the ports, and it says so rather than reporting a false result: an open UDP port and a dropped one look the same while the stack holds them. To re-verify the media path end to end, take the ports back for a few seconds:

```bash
ov stack stop && ov stack check-ports && ov stack start
```

It exits `8` when a required port fails (a recommended one is a warning, exit `0`), and never changes a firewall: the fix is printed for you to run. Useful flags: `--ports required|all`, `--domain-name <name>` to probe another address, `--ssh [user@]host` to check a machine before deploying to it, `-o json` for every verdict. `ov stack ports`, which reads the published host ports live, is for a **local** stack only; on a server use `check-ports`.

## Start, stop and restart { #start-stop-and-restart }

`ov stack start`, `ov stack stop` and `ov stack restart` control the whole stack: on a server, the systemd unit on the node; on PRO, every workload of the release.

```console
$ ov stack restart
✓ [172.30.0.96 single] systemctl restart openvidu
restart completed on 1 node(s)
```

`--dry-run` prints the commands and runs none. Restarting a single service is not available yet; these commands always act on the whole stack.

## Configuration

Change the configuration from the stack's directory with `ov stack config` (`view`, `get`, `set`, `unset`), and preview a change before applying it. See [Changing the configuration](../../configuration/changing-config.md). A Community deployment keeps the configuration in the node's files (`/opt/openvidu/config/`); a PRO deployment keeps it in the cluster, where any administrator reads and writes the same documents.

## Modules

A **module** is a feature of OpenVidu you turn on or off while the stack runs (`meet`, `observability`, `ingress`, `v2compatibility` and the rest). Change the selection with `ov stack module add|rm`; the deployment works out which services to run. See [Enable and disable modules](../../how-to-guides/enable-disable-modules.md).

## Operate from another machine { #operate-from-another-machine }

To operate the stack from a machine that has no directory for it (a colleague's laptop, a CI runner, a replacement for a lost directory), use **`ov stack import`**. It reads the description the stack publishes about itself and writes the two files a deploy would have left (`openvidu-stack.yml` and the `.openvidu/` state), so every `ov stack` command works afterwards.

```console
$ mkdir -p ~/stacks/web && cd ~/stacks/web
$ ov stack import web --ssh ubuntu@172.30.0.96 --ssh-key ~/.ssh/id_ed25519 -y

Stack described by the deployment:
  name         web
  deployment   single_node · on-premises · community
  dashboard    https://172-30-0-96.openvidu-local.dev
  nodes        172.30.0.96
  published    by ov/ov-admin on 2026-10-29 14:41 UTC (generation 1)

✔ imported stack "web" into /home/me/stacks/web
  desired state: /home/me/stacks/web/openvidu-stack.yml
```

The two editions store their configuration in different places, so importing behaves differently:

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    The configuration lives in the node's files, and each client holds a **copy** in its own `openvidu-stack.yml`. `config get` and `config view` read the node, so you see a change another client made. A Community deployment is a **single-administrator** product: suited to one person or one pipeline, and workable for a small team that coordinates. On the node itself, `sudo ov stack import --this-node` rebuilds the directory; over SSH, `ov stack import --ssh … --replace` refreshes a stale copy.

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    The stack holds its own desired state, so two clients **cannot drift apart**: both read and write the same release, and `ov stack config view` always answers from it. Any administrator with the cluster credential (`--kubeconfig <file>`) can point a directory at the stack and operate it, which makes PRO a **team** product. On a PRO master, `sudo ov stack kubeconfig --this-node --server <public-address>` prints the credential.

For a cloud stack kept on its cloud with `--remote-state`, any machine with that cloud's credentials can take it over completely: see [Remote state](../../openvidu-cli.md#remote-state).

## Destroy { #destroy }

`ov stack destroy` tears the deployment down and removes the directory's record. It asks for confirmation (type the stack name, or pass `-y`); `--dry-run` changes nothing and prints exactly what it would do.

On a server, the stack is stopped and disabled; its files and data stay under `/opt/openvidu`, so `ov stack deploy --mode auto` in the same directory brings it back with its data and configuration:

```console
$ ov stack destroy -y
✓ [172.30.0.96 single] systemctl stop openvidu
✓ [172.30.0.96 single] systemctl disable openvidu
stack stopped and disabled on all nodes (its files and data stay under /opt/openvidu)
✔ removed stack "web" from this directory
```

Two flags go further:

- `--delete-data` removes the deployment's data after teardown (`/opt/openvidu/data`: MongoDB, MinIO, Redis, recordings, metrics and logs, certificates).
- `--delete-config` removes the deployment directory (`/opt/openvidu` with the systemd unit), so the data goes with it.

## Backup and restore { #backup-and-restore }

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows. A destroy without `--delete-data` keeps the data under `/opt/openvidu/data`, so a later deploy in the same directory brings the stack back as it was.
