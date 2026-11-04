---
title: "Deploy OpenVidu locally with the OpenVidu CLI"
description: "Run a local OpenVidu development stack on Docker with the OpenVidu CLI: deploy, reach it over your LAN, add and remove modules live, read logs and destroy."
page_features: [lazyvideo]
---

# Deploy OpenVidu locally with the OpenVidu CLI

A local stack is OpenVidu running on your own machine with **Docker Compose**, for development. `ov` materializes a real `docker compose` project you can inspect and edit, starts it, waits for it to be ready, and then operates it: list the published ports, grow and shrink the module selection without redeploying, read the logs, and take it down.

<a class="glightbox" href="/assets/videos/platform/self-hosting/openvidu-cli/deploy-local.mp4" data-type="video"><video class="round-corners lazy-video" src="/assets/videos/platform/self-hosting/openvidu-cli/deploy-local.mp4" preload="none" muted playsinline loop></video></a>

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
materializing the deployment into ./labc and starting it (the first run downloads images)…
wrote spec to openvidu-stack.yml
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

`ov` waits for the endpoints itself and prints the banner with the URLs and credentials; `--no-wait` skips the wait. The banner lists only what the enabled modules serve. `--no-lan` keeps this example on `localhost` ([access over your LAN](#access-it-over-your-lan) is on by default). The stack name (`labc` here) is optional; omit it and `ov` auto-names it `stack1`.

The deployment is a normal `docker compose` project inside the stack directory (`./labc` here, or `./openvidu-local-<name>` by default). Its files are real and yours to edit: the configuration is `config/openvidu.yaml` and the service files beside it, and `ov stack config` changes them for you ([Configuration](../operate/configuration.md)). After editing a file by hand, `ov stack deploy` applies it.

=== "Deploy OpenVidu PRO locally"

    `--edition pro` runs OpenVidu PRO on the same Docker Compose engine (not Kubernetes): the PRO media server, Egress, Ingress and the OpenVidu 2 compatibility API, locally. It needs **no license**:

    ```console
    $ mkdir labp-stack && cd labp-stack
    $ ov stack deploy labp --environment local --edition pro --local-dir ./labp --no-lan
    materializing the deployment into ./labp and starting it (the first run downloads images)…
    wrote spec to openvidu-stack.yml
    ✓ docker compose up -d --remove-orphans
    ✔ OpenVidu compose deployment started in ./labp
    ✔ stack "labp" recorded in this directory
      OpenVidu Meet API: http://localhost:9080
    waiting for OpenVidu to be ready (Ctrl-C to stop waiting; the deployment keeps running)…
      ⏳ still starting: Meet, Dashboard (0s)
      ⏳ still starting: Meet, Dashboard (2s)
      ⏳ still starting: Meet, Dashboard (4s)

    ====================================================
    🎉 OpenVidu is ready! 🎉
    ====================================================

    This deployment is for local development only. Do not use it in production.

    ------------------ OpenVidu Meet -------------------
      - Access from this machine:
          - http://localhost:9080
      - Credentials:
          - Username: admin
          - Password: admin
          - API Key:  meet-api-key

    ----------------- LiveKit Server API ---------------
      - Access from this machine:
          - http://localhost:7880
          - ws://localhost:7880
      - Credentials:
          - API Key:    devkey
          - API Secret: secret

    ------------------- Other Services -----------------
      - OpenVidu Dashboard:
          - URL:      http://localhost:7880/dashboard
          - Username: admin
          - Password: admin
      - MinIO Console:
          - URL:      http://localhost:7880/minio-console
          - Username: minioadmin
          - Password: minioadmin
    ====================================================
    Operate this deployment with `ov stack ...`.
    ```

    A local OpenVidu PRO deployment runs in **evaluation mode**, for development and testing: at most 8 participants across all rooms and 5 minutes per room. It takes no license: `--openvidu-pro-license` is refused (exit `4`, `license (--openvidu-pro-license) cannot be set on a local stack`) before any container starts. Every module is on by default, `v2compatibility` included. A licensed deployment belongs on a server or a cloud: see the [pricing page](../../../../pricing.md) for what the license includes. The OpenVidu Dashboard of a local stack is the Community one, because the PRO dashboard checks the license when it starts.

!!! warning "One local OpenVidu runs at a time"

    Each stack is **namespaced** by its compose project (its containers, volumes and network are per-stack), so you can keep several side by side — each in its own directory — and `ov stack destroy --delete-data` on one never touches another's data. But all stacks bind the **same host ports** (7880, 9080, 9000, and, since local is dev-only, Redis 6379 and MongoDB 27017), so only one can run at once. Deploying a new one while another runs fails, naming the reason (`a local OpenVidu stack is already running — only one runs at a time`); `--free-ports` stops the running one first (it asks, or `-y`) and keeps its data.

## Access it over your LAN

From a phone or another computer on your network you need HTTPS, which the `openvidu-local.dev` wildcard domain provides. **LAN access is on by default**: the deploy detects this machine's private IP and the banner adds the URLs (`Access from other devices in your LAN: https://192-168-0-27.openvidu-local.dev:7443`). `--lan-ip` overrides the detected IP, and `--no-lan` keeps the stack on `localhost` only. The URLs replace the dots of the IP with dashes (`192.168.1.214` → `192-168-1-214`):

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
LAN        6443        tcp     Your application backend (localhost:6080) over HTTPS for the LAN (listed always: the container publishes it; it answers once LAN access is on)
LAN        5443        tcp     Your application frontend (localhost:5080) over HTTPS for the LAN (listed always: the container publishes it; it answers once LAN access is on)
LAN        7443        tcp     OpenVidu / LiveKit server API over HTTPS/WSS for the LAN (listed always: the container publishes it; it answers once LAN access is on)
Debug      6379        tcp     Redis
Debug      9000        tcp     MinIO S3 API (recordings storage)
WebRTC     3478        udp     TURN relay for WebRTC media (UDP)
WebRTC     7881        tcp     WebRTC media over TCP (fallback when UDP is blocked)
WebRTC     7900-7999   udp     WebRTC media (UDP)
```

Only the ports the enabled modules use are listed: this stack has `egress`, so Redis and MinIO are there, but no MongoDB, no Meet (9080) and no ingress. The **LAN** ports are listed always, even with `--no-lan`: the container publishes them, and they answer once LAN access is on. The **Debug** group exposes Redis, MongoDB and MinIO on the host because local is dev-only. Add `-o wide` for the compose service that owns each port.

## Add and remove modules on the running stack

The module selection changes **incrementally**, without redeploying. Preview with `--dry-run`, then apply:

```console
$ ov stack module add meet
enable:  meet
modules: livekit-server, egress  →  livekit-server, egress, meet
incremental change: start mongodb,ov-meet; restart the media server (its config changed); other services keep running.
✔ updated openvidu-stack.yml
✓ docker compose up -d --no-deps --force-recreate mongodb ov-livekit-server ov-meet
modules updated
```

The command returns once the new services are started, not once they answer: OpenVidu Meet takes some seconds more. `ov stack status --wait` waits for it.

Only the new services start (and the media server restarts because its config changed); nothing else is touched. Removing a module is just as incremental:

```console
$ ov stack module rm meet
disable: meet
modules: livekit-server, egress, meet  →  livekit-server, egress
incremental change: stop mongodb,ov-meet; restart the media server (its config changed); other services keep running.
✔ updated openvidu-stack.yml
✓ docker compose rm -sf mongodb ov-meet
✓ docker compose up -d --no-deps --force-recreate ov-livekit-server
modules updated
```

Dependencies are handled for you: `meet` needs `egress`, so adding `meet` to a stack without it enables both, and `module rm egress` while `meet` is on leaves `egress` running and says so (`nothing to do: … still required by another enabled module`). See [Modules and agents](../operate/modules.md) for the full picture.

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

`--delete-data` removes the Docker volumes (recordings, rooms, Meet's configuration); `--delete-config` removes the deployment directory (`docker-compose.yaml` and `config/`). Locally they are independent: `--delete-config` alone leaves the volumes. The spec (`openvidu-stack.yml`) stays and records the stack's name, so `ov stack deploy` in the same directory brings the stack back, with its data unless you deleted it.

## Operate it by hand: assisted mode

Nothing here is magic: every operation can be done by hand in the deployment directory with `docker compose`, and that is exactly what `--mode assisted` prints instead of running. It writes the files and prints the one command to start them:

```console
$ ov stack deploy dev --environment local --no-lan --mode assisted
wrote spec to openvidu-stack.yml
# Deployment files ready in ./openvidu-local-dev. Start OpenVidu with:
  (cd ./openvidu-local-dev && docker compose up -d --remove-orphans)
(edit ./openvidu-local-dev/config/ to customize, then `ov stack deploy` again; operate it with `ov stack ...`)
✔ stack "dev" recorded in this directory
  OpenVidu Meet API: http://localhost:9080
```

From there you drive the project yourself: `docker compose config --services` is the authority on what is enabled, `COMPOSE_PROFILES` in `.env` selects the modules, and `COMPOSE_PROFILES='*' docker compose down` tears everything down whatever the current selection. Turning a module off by hand takes more than editing `.env` — Compose does not stop a container when its profile stops being active, and the media server's `livekit.yaml` must change with the data services. `ov stack module add/rm` does that bookkeeping for you.

## Next steps

- [Deploy on your own servers](on-premises.md) or on [AWS](aws.md), [Azure](azure.md), [Google Cloud](gcp.md), [Oracle Cloud](oracle.md) or [DigitalOcean](digitalocean.md).
- Operate it: [status](../operate/status.md), [configuration](../operate/configuration.md), [modules and agents](../operate/modules.md).
- The full [command reference](../reference.md).
