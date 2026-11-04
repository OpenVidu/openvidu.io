---
title: "Status and health checks of an OpenVidu stack"
description: "Check an OpenVidu stack with the OpenVidu CLI: live status, describe, logs, the health test, the port checks, and start, stop and restart."
---

# Status and health checks

Every command on this page resolves **the stack in the current directory** (or the one `--dir` points at), with no name and no flags. They work the same whether the stack runs locally, on your servers or on a cloud, except `check-ports`, which needs SSH access to a node.

## Status

`ov stack status` prints the state of each node or service. On a Community server it is the nodes:

```console
$ ov stack status
HOST          ROLE     STATE
172.30.0.96   single   active
```

On a local stack it is this machine:

```console
$ ov stack status
HOST        ROLE    STATE
localhost   local   running
```

On a local stack, `ov stack status --wait` prints the same banner as the deploy, with the URLs and credentials, once everything answers.

On a PRO stack (Kubernetes) it is the workloads:

```console
$ ov stack status
POD                                READY  STATE
caddy-proxy-86f66c6568-czv58       1/1    Running
grafana-5df667c689-pwj4t           0/1    ContainerCreating
mongodb-0                          0/2    PodInitializing
ov-dashboard-59f996c5fb-4ks7n      1/1    Running
ov-livekit-server-87mw2            0/1    PodInitializing
ov-meet-cbbf88b85-kkrvx            1/1    Running
…
```


### Wait until ready

`--wait` blocks until the stack is ready. On a Community server it probes the node itself (Caddy, the media server and each enabled module's web) over the stack's own transport, so no DNS or route from your machine is needed:

```console
$ ov stack status --wait
waiting for OpenVidu to be ready on the node (Ctrl-C to stop waiting; the deployment keeps running)…
  ⏳ still starting: openvidu, meet (0s)
  ⏳ still starting: openvidu (5s)
✔ OpenVidu is ready at https://172-30-0-96.openvidu-local.dev (caddy, openvidu, dashboard, meet)
```

On an Elastic or High Availability stack it waits until, at the same time, the stack's URL answers and every node and service is ready, counting them by tier and naming the pods that are still restarting:

```console
$ ov stack status --wait
waiting for https://172-30-0-101.openvidu-local.dev to be ready (Ctrl-C to stop)…
  ⏳ master nodes 1/1, media nodes 1/1, services 12/20, restarting: ov-dashboard-6ccd78b5c9-78jqv, ov-meet-7648647fdb-vhqsr (0s)
…
  ⏳ master nodes 1/1, media nodes 1/1, services 18/20, restarting: ov-dashboard-6ccd78b5c9-78jqv, ov-meet-7648647fdb-vhqsr (2m51s)
✔ el is ready (https://172-30-0-101.openvidu-local.dev)
```

When it gives up, it names the pods still starting. Right after a first PRO deploy, while the nodes pull the images and some pods restart before they settle, the wait can take longer than the default 5 minutes: raise it with `--wait-timeout 15m`.

## Describe

`ov stack describe` prints the stack's record, endpoints and a configuration summary.

On a Community server, reached over SSH:

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

`Access` says how this directory reaches the stack: `ssh` for a Community server, `kube` (the cluster API) for a PRO stack, `local` for a stack on this machine. A local OpenVidu PRO stack:

```console
$ ov stack describe
Stack:       qal2
Type:        single_node
Environment: local
Edition:     pro
Endpoint:    http://localhost:7880
Spec:        openvidu-stack.yml
Access:      local

Nodes:
  localhost        local        running
```


## Health test

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

## Logs

`ov stack logs` fetches the logs of the whole stack, one interleaved stream; `--since` bounds the window and `-f` follows them live. On a server they come from the node's journal, so `--tail N` is the last N lines of the whole stack (`--since` takes a journal value such as `'1 hour ago'`); on a local stack `--tail` is per service, and on PRO it is capped at 200 (`--since` takes a duration such as `1h`):

```console
$ ov stack logs --tail 8
==> 172.30.0.96 (single) <==
Nov 04 03:26:57 fake-vm-172-30-0-96 docker[4229]: mongodb            | {"t":{"$date":"2026-11-04T03:26:57.833+00:00"},"s":"I",  "c":"-",        "id":9023600, "ctx":" …
Nov 04 03:26:57 fake-vm-172-30-0-96 docker[4229]: mongodb            | {"t":{"$date":"2026-11-04T03:26:57.835+00:00"},"s":"I",  "c":"NETWORK",  "id":6788700, "ctx":" …
Nov 04 03:26:58 fake-vm-172-30-0-96 docker[4229]: ov-livekit-server  | 2026-11-04T03:26:58.118Z        WARN        livekit        service/utils.go:85        error ha …
…
```

Per-service logs through `ov` are not available yet. Read one service's logs with the engine underneath: `docker compose logs <service>` in the deployment directory locally, or `kubectl --kubeconfig <file> logs <pod>` on PRO. A cloud stack keeps its kubeconfig in `.openvidu/<cloud>/kubeconfig.yaml`; on premises, `sudo ov stack kubeconfig --this-node --server <public-address>` on the master prints one.

## Check the ports

`ov stack check-ports` verifies that the inbound ports a stack needs actually arrive at a server or a cloud machine, so it needs SSH access to the node: a stack deployed over SSH, or a Community cloud stack. A local stack has no firewall to check, and a PRO cloud stack registered through its kubeconfig has no SSH access recorded; both exit with code `2` (the local one pointing at [`ov stack ports`](#list-the-published-ports)). It runs a temporary listener on the node and probes it, so TCP **and** UDP (and the media range) are really verified, which dialling a running stack cannot do. It is the single most useful check before going live, because a stack with a blocked media port looks perfectly healthy and simply has no media.

Against a **stopped or not-yet-deployed** node it gives the complete check. `ov` holds the ports with a temporary listener on the node (the node's own `python3`, or `ov` itself when the node has none) and probes them from your machine:

```console
$ ov stack check-ports
Inbound ports of 172-30-0-96.openvidu-local.dev (172.30.0.96)
  state     fresh — nothing of ours is deployed here, so every port was free to measure
  method    a temporary listener on the node (its own python3; nothing written to disk)
  verdict   all 6 checked port(s) arrive at the node

Required
  the stack does not work without these
  ✓ 443/tcp           open
      Caddy — the probe arrived at the node — the whole path is open
  ✓ 22/tcp            open
      SSH — ov is connected to the node over SSH

Recommended
  it works without these, but every call is worse
  ✓ 443/udp           open
      OpenVidu LiveKit Server — the probe arrived at the node — the whole path is open
  ✓ 80/tcp            open
      Caddy — the probe arrived at the node — the whole path is open
  ✓ 50000-60000/udp   open
      OpenVidu LiveKit Server — 5 of the 5 sampled ports answered (of 50000-60000): the range is open as far as sampling can show
  ✓ 7881/tcp          open
      OpenVidu LiveKit Server — the probe arrived at the node — the whole path is open
…
```

Against a **running** stack it can only dial the ports, and it says so instead of pretending: an open UDP port and a dropped one look the same while the stack holds them, and the media range is bound only for connected participants:

```console
$ ov stack check-ports
Inbound ports of 172-30-0-96.openvidu-local.dev (172.30.0.96)
  state     running — the stack holds these ports, so they could only be dialled
  method    probes from this machine only (no listener on the node)
  verdict   4 checked port(s) arrive; 2 could not be established (443/udp, 50000-60000/udp)

Required
  the stack does not work without these
  ✓ 443/tcp           open
      Caddy — something is listening and answered
  ✓ 22/tcp            open
      SSH — ov is connected to the node over SSH

Recommended
  it works without these, but every call is worse
  – 443/udp           inconclusive
      OpenVidu LiveKit Server — UDP has no handshake: with nothing of ours listening on the node, an open port and a dropped one look identical from here
      Participants behind restrictive networks are relayed over TURN/TLS on 443/tcp instead of UDP.
  – 50000-60000/udp   inconclusive
      OpenVidu LiveKit Server — not checkable while the stack runs: it binds ports of this range only for the participants connected at the moment, so a probe cannot tell an open port from a dropped one
      Media is relayed through TURN on 443, which adds latency and load and lowers quality under load.
  ✓ 80/tcp            open
      Caddy — something is listening and answered
  ✓ 7881/tcp          open
      OpenVidu LiveKit Server — something is listening and answered

Not established
  443/udp, 50000-60000/udp
  the running stack holds these ports, or binds them only on demand. To measure them end to end:
  ov stack stop && ov stack check-ports && ov stack start
…
```

To re-verify the media path end to end, take the ports back for a few seconds:

```bash
ov stack stop && ov stack check-ports && ov stack start
```

It exits `8` when a required port fails (a recommended one is a warning, exit `0`), and never changes a firewall: the fix is printed for you to run. Besides the ports it checks that the domain resolves to the node and that the node reaches the image registries. Useful flags: `--ports required|all`, `--domain-name <name>` to probe another address, `--ssh [user@]host` to check a machine before deploying to it, `-o json` for every verdict.

## List the published ports

`ov stack ports` is for a local stack (elsewhere it exits `2`; use `check-ports` on a server). It reads the host ports the deployment publishes live from Docker, grouped by what each one is for:

```console
$ ov stack ports
CATEGORY   PORT        PROTO   PURPOSE
API        7880        tcp     OpenVidu / LiveKit server API (HTTP & WebSocket); also serves the Dashboard, MinIO console and Developer UI
WebRTC     3478        udp     TURN relay for WebRTC media (UDP)
WebRTC     7881        tcp     WebRTC media over TCP (fallback when UDP is blocked)
WebRTC     7900-7999   udp     WebRTC media (UDP)
…
```

Add `-o wide` for the service that owns each port.

## Start, stop and restart

`ov stack start`, `ov stack stop` and `ov stack restart` control the whole stack: on a server, the systemd unit on each node; on PRO, every workload of the release; on a local stack, `docker compose`.

```console
$ ov stack restart
✓ [172.30.0.96 single] systemctl restart openvidu
restart completed on 1 node(s)
```

`--dry-run` prints the commands and runs none. Restarting a single service is not available yet (omit the service for the whole stack).

## Next steps

- [Change the configuration](configuration.md) or [the modules](modules.md).
- [Scale](scaling.md) an Elastic or HA stack.
- The full [command reference](../reference.md).
