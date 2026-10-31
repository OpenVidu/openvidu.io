---
title: "Deploy OpenVidu locally with the OpenVidu CLI"
description: "Run a local OpenVidu development stack on Docker with the OpenVidu CLI: deploy, reach it over your LAN, add and remove modules live, read logs and destroy."
page_features: [lazyvideo]
---

# Deploy OpenVidu locally with the OpenVidu CLI

A local stack is OpenVidu running on your own machine with **Docker Compose**, for development. `ov` materializes a real `docker compose` project you can inspect and edit, starts it, waits for it to be ready, and then operates it: list the published ports, grow and shrink the module selection without redeploying, read the logs, and take it down.

<!-- VIDEO: deploy-local.mp4 (docs-video) -->

A local stack runs on Docker Compose with **either edition**, so you can develop against OpenVidu PRO without Kubernetes on your laptop. The [`ov` CLI](../install.md) is Linux-only for now.

## Requirements

- [Docker :fontawesome-solid-external-link:{.external-link-icon}](https://docs.docker.com/engine/install/){:target="_blank"} installed and running, with the Compose plugin.
- The [OpenVidu CLI](../install.md).

## Deploy

An empty directory is the stack. Make one and work from it (or point `--dir` at it). Start with a subset of modules so you can grow it later:

```console
$ mkdir labc-stack && cd labc-stack
$ ov stack deploy labc --environment local --local-dir ./labc --no-lan \
    --modules livekit-server,egress
wrote spec to openvidu-stack.yml
materializing the deployment into ./labc and starting it (the first run downloads images)…
✓ docker compose up -d --remove-orphans
✔ OpenVidu compose deployment started in ./labc
✔ stack "labc" recorded in this directory
waiting for OpenVidu to be ready (Ctrl-C to stop waiting; the deployment keeps running)…
  ⏳ still starting: MinIO (0s)

====================================================
🎉 OpenVidu is ready! 🎉
====================================================

This deployment is for local development only. Do not use it in production.

----------------- LiveKit Server API ---------------
  - Access from this machine:
      - http://localhost:7880
      - ws://localhost:7880
  - Credentials:
      - API Key:    devkey
      - API Secret: secret

------------------- Other Services -----------------
  - MinIO Console:
      - URL:      http://localhost:7880/minio-console
      - Username: minioadmin
      - Password: minioadmin
====================================================
Operate this deployment with `ov stack ...`.
```

`ov` waits for the endpoints itself and prints the banner with the URLs and credentials; `--no-wait` skips the wait. The banner lists only what the enabled modules serve. The stack name (`labc` here) is optional; omit it and `ov` auto-names it `stack1`.

The deployment is a normal `docker compose` project inside the stack directory (`./labc` here, or `./openvidu-local-<name>` by default). Its files are real and yours to edit; to apply a change, deploy again or restart (see [the manual walkthrough](#operate-it-by-hand-assisted-mode)).

=== "Deploy OpenVidu PRO locally"

    `--edition pro` runs OpenVidu PRO on the same Docker Compose engine (not Kubernetes) — the Pro media engine and the Pro images, locally:

    ```console
    $ mkdir qal2 && cd qal2
    $ ov stack deploy qal2 --environment local --edition pro --no-lan --openvidu-pro-license <your-license>
    wrote spec to openvidu-stack.yml
    materializing the deployment into ./openvidu-local-qal2 and starting it (the first run downloads images)…
    ✓ docker compose up -d --remove-orphans
    ✔ OpenVidu compose deployment started in ./openvidu-local-qal2
    ✔ stack "qal2" recorded in this directory
      OpenVidu Meet API: http://localhost:9080
    waiting for OpenVidu to be ready (Ctrl-C to stop waiting; the deployment keeps running)…
      ⏳ still starting: OpenVidu, Meet, Dashboard, MinIO (0s)
      ⏳ still starting: Meet, Dashboard (2s)
    …
      ⏳ still starting: Meet, Dashboard (21s)

    ====================================================
    🎉 OpenVidu is ready! 🎉
    ====================================================

    This deployment is for local development only. Do not use it in production.

    ------------------ OpenVidu Meet -------------------
      - Access from this machine:
          - http://localhost:9080
      - Credentials:
          - Username: admin
          - Password: ********
          - API Key:  meet-api-key

    ----------------- LiveKit Server API ---------------
      - Access from this machine:
          - http://localhost:7880
          - ws://localhost:7880
      - Credentials:
          - API Key:    devkey
          - API Secret: ********
    …
    ```

    `--no-lan` keeps the stack on `localhost`, without the HTTPS access from other devices of your network.

!!! warning "One local OpenVidu runs at a time"

    Each stack is **namespaced** by its compose project (its containers, volumes and network are per-stack), so you can keep several side by side — each in its own directory — and `ov stack destroy --delete-data` on one never touches another's data. But all stacks bind the **same host ports** (7880, 9080, 9000, and, since local is dev-only, Redis 6379 and MongoDB 27017), so only one can run at once. Deploying a new one detects the running stack and offers to stop it and start the new one (`--free-ports`).

## Access it over your LAN

By default the stack is reachable only from this machine, over plain HTTP on `localhost`. To reach it from a phone or another computer on your network you need HTTPS, which the `openvidu-local.dev` wildcard domain provides. Deploy with `--lan` (and `--lan-ip` to override the auto-detected private IP), and build the URLs by replacing the dots of your IP with dashes (`192.168.1.214` → `192-168-1-214`):

| | Local | From your network |
|---|---|---|
| OpenVidu (LiveKit) | `http://localhost:7880` | `https://192-168-1-214.openvidu-local.dev:7443` |
| Your app's frontend | `http://localhost:5080` | `https://192-168-1-214.openvidu-local.dev:5443` |
| Your app's backend | `http://localhost:6080` | `https://192-168-1-214.openvidu-local.dev:6443` |
| OpenVidu Meet | `http://localhost:9080/meet` | `https://192-168-1-214.openvidu-local.dev:9443/meet` |

## Show the published ports

`ov stack ports` reports the host ports the deployment publishes (read live from Docker), grouped by what each one is for:

```console
$ ov stack ports
CATEGORY   PORT        PROTO   PURPOSE
API        7880        tcp     OpenVidu / LiveKit server API (HTTP & WebSocket); also serves the Dashboard, MinIO console and Developer UI
Debug      6379        tcp     Redis
Debug      9000        tcp     MinIO S3 API (recordings storage)
WebRTC     3478        udp     TURN relay for WebRTC media (UDP)
WebRTC     7881        tcp     WebRTC media over TCP (fallback when UDP is blocked)
WebRTC     7900-7999   udp     WebRTC media (UDP)
```

Only the ports the enabled modules actually use are listed: this stack has `egress`, so Redis and MinIO are there, but no MongoDB, no Meet (9080) and no ingress. A **LAN** group (7443, 9443, 5443, 6443) appears only with `--lan`; the **Debug** group exposes Redis, MongoDB and MinIO on the host because local is dev-only. Add `-o wide` for the compose service that owns each port.

## Add and remove modules on the running stack

The module selection changes **incrementally**, without redeploying. Preview with `--dry-run`, then apply:

```console
$ ov stack module add meet
enable:  meet
modules: livekit-server, egress  →  livekit-server, egress, meet
incremental change: start mongodb,ov-meet; restart the media server (its config changed); other services keep running.
✓ docker compose restart ov-livekit-server
✓ docker compose up -d --no-deps mongodb ov-meet
modules updated
```

Only the new services start (and the media server restarts because its config changed); nothing else is touched. Removing a module is just as incremental:

```console
$ ov stack module rm meet
disable: meet
modules: livekit-server, egress, meet  →  livekit-server, egress
incremental change: stop mongodb,ov-meet; restart the media server (its config changed); other services keep running.
✓ docker compose rm -sf mongodb ov-meet
✓ docker compose restart ov-livekit-server
modules updated
```

Dependencies are handled for you: `meet` needs `egress`, so adding `meet` to a stack without it enables both, and `ov` refuses to remove a module another enabled one still requires. See [Modules and agents](../operate/modules.md) for the full picture.

## Read the logs

`--tail N` is per service, interleaved:

```console
$ ov stack logs --tail 6
ov-egress-1  | 2026-10-29T15:40:52.368+0100	INFO	egress	server/server.go:163	service ready	{"nodeID": "NE_SEV3ZHAPBwir", "clusterID": ""}
redis-1      | 1:M 29 Oct 2026 15:40:51.186 * Done loading RDB, keys loaded: 3, keys expired: 1.
minio-1      | WebUI: http://localhost:7880/minio-console
ov-livekit-server-1  | 2026-10-29T15:41:24.909+0100	INFO	livekit	service/server.go:343	starting LiveKit server	{"portHttp": 7880, "nodeID": "ND_yHVTbNtCro9A", "nodeIP": "172.19.0.2", "version": "1.13.7", …}
caddy-proxy-1        | {"level":"info","ts":1793284658.2489977,"logger":"http.log","msg":"server running","name":"srv0","protocols":["h1","h2","h3"]}
…
```

Follow them live with `ov stack logs -f`. Per-service logs through `ov` are not available yet; read them with Compose in the deployment directory instead (`cd labc && docker compose logs -f ov-livekit-server`).

## Destroy

The destroy also removes the directory's record:

```console
$ ov stack destroy --delete-data -y
✓ docker compose --profile * down -v
local deployment torn down
✔ removed stack "labc" from this directory
```

`--delete-data` removes the Docker volumes (recordings, rooms, Meet's configuration); `--delete-config` also removes the deployment directory (`docker-compose.yaml` and the config files). They are independent. The spec (`openvidu-stack.yml`) stays and records the stack's name, so `ov stack deploy` in the same directory brings it back.

## Operate it by hand: assisted mode

Nothing here is magic: every operation can be done by hand in the deployment directory with `docker compose`, and that is exactly what `--mode assisted` prints instead of running. It writes the files and prints the one command to start them:

```console
$ ov stack deploy dev --environment local --no-lan --mode assisted
wrote spec to openvidu-stack.yml
# Deployment files ready in ./openvidu-local-dev. Start OpenVidu with:
  (cd ./openvidu-local-dev && docker compose up -d --remove-orphans)
(edit the files in ./openvidu-local-dev to customize; then operate it with `ov stack ...`)
✔ stack "dev" recorded in this directory
  OpenVidu Meet API: http://localhost:9080
```

From there you drive the project yourself: `docker compose config --services` is the authority on what is enabled, `COMPOSE_PROFILES` in `.env` selects the modules, and `COMPOSE_PROFILES='*' docker compose down` tears everything down whatever the current selection. Turning a module off by hand takes more than editing `.env` — Compose does not stop a container when its profile stops being active, and the media server's `livekit.yaml` must change with the data services. `ov stack module add/rm` does that bookkeeping for you.

## Next steps

- [Deploy on your own servers](on-premises.md) or on [AWS](aws.md), [Azure](azure.md), [Google Cloud](gcp.md), [Oracle Cloud](oracle.md) or [DigitalOcean](digitalocean.md).
- Operate it: [status](../operate/status.md), [configuration](../operate/configuration.md), [modules and agents](../operate/modules.md).
- The full [command reference](../reference.md).
