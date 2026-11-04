---
title: "Status and health checks of an OpenVidu stack"
description: "Check an OpenVidu stack with the OpenVidu CLI: live status, describe, logs, the health test, the port checks, and start, stop and restart."
---

# Status and health checks

Every command on this page resolves **the stack in the current directory** (or the one `--dir` points at), with no name and no flags. They work the same whether the stack runs locally, on your servers or on a cloud, except `check-ports`, which is for servers and clouds only.

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

On an Elastic or High Availability stack it waits until, at the same time, the stack's URL answers and every node and service is ready, counting them by tier:

```console
$ ov stack status --wait
waiting for https://172-30-0-96.openvidu-local.dev to be ready (Ctrl-C to stop)…
  ⏳ master nodes 1/1, media nodes 1/1, services 12/20, URL not answering yet (5s)
  ⏳ master nodes 1/1, media nodes 1/1, services 17/20 (1m45s)
  ⏳ master nodes 1/1, media nodes 1/1, services 19/20 (2m34s)
✔ el is ready (https://172-30-0-96.openvidu-local.dev)
```

When it gives up, it names the pods still starting.

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

## Logs

`ov stack logs` fetches the logs of the whole stack, one interleaved stream. `--tail N` is per service; `--since` bounds the window; `-f` follows them live:

```console
$ ov stack logs --tail 8
==> 172.30.0.96 (single) <==
Oct 29 14:46:10 fake-vm-172-30-0-96 docker[2534]: redis              | 1:M 29 Oct 2026 14:46:10.134 * Background saving terminated with success
Oct 29 14:46:13 fake-vm-172-30-0-96 docker[2534]: ov-livekit-server  | 2026-10-29T14:46:13.802Z        INFO        livekit.agents        service/agentservice.go:351        last worker deregistered …
…
```

Per-service logs through `ov` are not available yet; omit the service for the whole stack, or read one service's logs with the engine underneath (`docker compose logs <service>` locally, `kubectl logs` on PRO).

## Check the ports

`ov stack check-ports` verifies that the inbound ports a stack needs actually arrive at a server or a cloud machine. A local stack has no firewall to check: there it exits with code `2` and points at [`ov stack ports`](#list-the-published-ports). It runs a temporary listener on the node and probes it, so TCP **and** UDP (and the media range) are really verified — which dialling a running stack cannot do. It is the single most useful check before going live, because a stack with a blocked media port looks perfectly healthy and simply has no media.

Against a **stopped or not-yet-deployed** node it gives the complete check:

```console
$ ov stack check-ports
…
Required
  the stack does not work without these
  ✓ 443/tcp           open
  ✓ 443/udp           open
  ✓ 80/tcp            open

Recommended
  it works without these, but every call is worse
  ✓ 50000-60000/udp   open
  ✓ 7881/tcp          open
```

Against a **running** stack it can only dial the ports, and it says so honestly instead of pretending — an open UDP port and a dropped one are indistinguishable while the stack holds them:

```console
$ ov stack check-ports
the stack is RUNNING, so its ports could only be dialled — probed from this machine only
PORT        NEED       STATE          WHERE   DETAIL
✓ 443/tcp   required   open           -       something is listening and answered
– 443/udp   required   inconclusive   -       UDP has no handshake: with nothing of ours listening on the node, an open port and a dropped one look identical from here
✗ 80/tcp    required   dropped        node    the path is open but nothing is listening — the service that should own this port is not up
note: to verify the media path end to end, stop the stack first: ov stack stop && ov stack check-ports && ov stack start
```

To re-verify the media path end to end, take the ports back for a few seconds:

```bash
ov stack stop && ov stack check-ports && ov stack start
```

It exits `8` when any probed port fails, and never changes a firewall — the fix is printed for you to run. Useful flags: `--ports required|all`, `--domain-name <name>` to probe another address, `-o json` for every verdict. A local deployment has no firewall to check; use [`ov stack ports`](#list-the-published-ports) there.

## List the published ports

`ov stack ports` reports the ports the stack needs, from its configuration. On a local stack it reads the published host ports live from Docker, grouped by what each one is for:

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
