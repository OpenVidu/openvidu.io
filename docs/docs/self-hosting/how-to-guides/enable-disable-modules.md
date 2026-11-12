---
title: "Enable and disable OpenVidu modules"
description: "Turn OpenVidu modules on or off on a running stack with the CLI, so a deployment runs only the services it needs, and let the data services follow."
---

# Enable and disable modules

A **module** is a feature of OpenVidu you turn on or off; a **service** is the container (or Kubernetes workload) that implements it. You choose modules and the deployment works out which services to run. `ov stack module` changes the selection on a **running** stack, with minimal impact.

## Modules and services { #modules-and-services }

The modules are:

| Module | What you get | Services it runs |
| --- | --- | --- |
| `livekit-server` | The media server, always on | `ov-livekit-server` |
| `egress` | Recording and streaming out | `ov-egress` |
| `ingress` | RTMP and WHIP ingest | `ov-ingress` |
| `dashboard` | OpenVidu Dashboard at `/dashboard` | `ov-dashboard` |
| `meet` | [OpenVidu Meet](../../../meet/index.md) at `/meet` | `ov-meet` (it brings `egress`) |
| `observability` | Metrics, logs and the [Grafana stack](../production-ready/observability/grafana-stack.md) | `grafana`, `loki`, `prometheus` or `mimir`, `alloy` |
| `v2compatibility` | The OpenVidu 2 REST API (**PRO**{ .openvidu-tag .openvidu-pro-tag } only) | `ov-v2compat` |

List the current selection with `ov stack module ls`:

```console
$ ov stack module ls
MODULE           ENABLED   ROLE
livekit-server   yes       base
egress           yes       selected
ingress          yes       selected
dashboard        yes       selected
meet             yes       selected
observability    yes       selected
```

`base` is always on, `selected` means you enabled it, `dependency` means another module requires it (such as `egress` under `meet`), and `off` means it is not running. On a PRO stack, the listing also shows what each module requires and which data services the selection brings in.

Changing the selection is **incremental**: `ov` starts only the new services (and recreates the ones whose configuration changed, such as the media server), or stops the removed ones; nothing else is touched. `--dry-run` previews the change. The example below is from a local stack; the exact command lines differ by deployment type, as explained after the examples.

```console
$ ov stack module add meet
enable:  meet
modules: livekit-server, egress  →  livekit-server, egress, meet
incremental change: start mongodb,ov-meet; restart the media server (its config changed); other services keep running.
✔ updated openvidu-stack.yml
✓ docker compose up -d --no-deps --force-recreate mongodb ov-livekit-server ov-meet
modules updated
```

Removing is just as incremental:

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

On a Community server the same commands rewrite `modules:` in `config/openvidu.yaml`, render the configuration again and recreate the affected services. On PRO the change is a `helm upgrade`, and the components whose configuration changed roll out after the command returns; follow them with `ov stack status`. `v2compatibility` is PRO only, so a Community stack refuses it (exit `2`).

### Data services follow the modules

The data services (**`redis`, `mongodb` and `minio`**) are never named directly. They come up because a module needs them and go away when no module needs them anymore. Dependencies between modules are handled for you too: `meet` needs `egress`, so adding `meet` to a stack without `egress` enables both:

```console
$ ov stack module add meet
enable:  egress, meet
modules: livekit-server  →  livekit-server, egress, meet
incremental change: start minio,mongodb,ov-egress,ov-meet,redis; restart the media server (its config changed); other services keep running.
…
```

## Agents { #agents }

An **agent** is an AI container that runs beside the media server (live captions and the like). Its definition carries the image, an `enabled` flag, the options of what runs it and the agent's own configuration. Agents are not modules: each one is a file of its own, and `ov stack agent` reads and rewrites them.

```console
$ ov stack agent ls
AGENT                     ENABLED   IMAGE                                                  STATE
agent-speech-processing   no        docker.io/openvidu/agent-speech-processing-vosk:main   -
```

Turn one on or off, live. `ov` sets `enabled` in the definition, regenerates the agents' Compose file (or runs a `helm upgrade` on PRO) and creates or removes just that agent's service:

```console
$ ov stack agent enable speech-processing
enable: agent-speech-processing (docker.io/openvidu/agent-speech-processing-vosk:main)
✓ set enabled=true in config/agent-speech-processing.yaml
✓ sudo ov stack render --this-node
✓ docker compose --env-file data/runtime/compose.env up -d --force-recreate --no-deps agent-speech-processing
agent agent-speech-processing enabled
```

Disabling removes the container; the definition stays, so `enable` brings it back. The first start pulls the agent image, which is large (the models are inside it), so allow some time. `<name>` is the file's name without the extension, with or without the `agent-` prefix.

- On a **Community** stack the definitions are `config/agent-<name>.yaml` on the node, and an agent of your own is one more such file.
- On a **local** stack they are the `agent-*.yaml` files in the deployment directory.
- On a **PRO** stack they are configuration documents of the stack (the chart ships `speech-processing`, disabled), and `enable`/`disable` writes the document and runs one `helm upgrade`.

## Troubleshooting

On any problem, check these sections:

- [Config Troubleshooting](../configuration/changing-config.md#troubleshooting-configuration)
- [Status and health checks](../single-node/on-premises/admin.md#status)
