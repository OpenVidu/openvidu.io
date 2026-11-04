---
title: "Modules and agents of an OpenVidu stack"
description: "List, add and remove OpenVidu modules on a running stack with the CLI, let its data services follow, and enable or disable AI agents live."
---

# Modules and agents

A **module** is a feature of OpenVidu you turn on or off; a **service** is the container (or Kubernetes workload) that implements it. You choose modules and the deployment works out which services to run. The modules are `egress`, `ingress`, `dashboard`, `meet`, `observability` and `v2compatibility` (PRO only); `livekit-server`, the media server, is always on.

## List modules

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

This is a Community server. `base` is always there, `selected` is what you asked for, `off` is not running. On a PRO stack the listing shows what each module requires, and which data services the selection brings:

```console
$ ov stack module ls
MODULE            ENABLED   REQUIRES
egress            yes       redis, minio
ingress           yes       redis
dashboard         yes       redis, mongodb
meet              yes       egress, redis, mongodb, minio
observability     yes       -
v2compatibility   no        redis
data services (derived from the module selection): redis=yes  mongodb=yes  minio=no
```

## Add and remove modules, live

Changing the selection is **incremental**: `ov` starts only the new services (and recreates the ones whose configuration changed, such as the media server), or stops the removed ones; nothing else is touched. Preview with `--dry-run`, then apply. On a Community server, `modules` is a value of `config/openvidu.yaml`:

```console
$ ov stack module add meet
enable:  meet
modules: ingress, dashboard, observability  →  ingress, dashboard, meet, observability
on-premise change: rewrite modules: in config/openvidu.yaml, render config/ into data/runtime/ again, recreate the affected services; the rest keep running.
✓ set modules=ingress,dashboard,meet,observability in config/openvidu.yaml
✓ sudo ov stack render --this-node
✓ docker compose --env-file data/runtime/compose.env up -d --force-recreate --no-deps ov-livekit-server ov-meet
modules updated
```

Removing is just as incremental:

```console
$ ov stack module rm meet
disable: meet
modules: ingress, dashboard, meet, observability  →  ingress, dashboard, observability
on-premise change: rewrite modules: in config/openvidu.yaml, render config/ into data/runtime/ again, recreate the affected services; the rest keep running.
✓ set modules=ingress,dashboard,observability in config/openvidu.yaml
✓ sudo ov stack render --this-node
✓ docker compose --env-file data/runtime/compose.env up -d --force-recreate --no-deps ov-livekit-server
✓ docker compose --env-file data/runtime/compose.env rm --stop --force ov-meet
modules updated
```

The spec follows the stack: `openvidu-stack.yml` records the new selection. On PRO the change is a `helm upgrade`, and the components whose configuration changed roll out after the command returns; follow them with `ov stack status`.

## Data services follow the modules

The data services (**`redis`, `mongodb` and `minio`**) are never named directly. They come up because a module needs them and go away when no module needs them any more. Dependencies between modules are handled for you too: `meet` needs `egress`, so adding `meet` to a stack without `egress` enables both (a local stack here):

```console
$ ov stack module add meet
enable:  egress, meet
modules: livekit-server  →  livekit-server, egress, meet
incremental change: start minio,mongodb,ov-egress,ov-meet,redis; restart the media server (its config changed); other services keep running.
…
```

## Agents

An **agent** is an AI container that runs beside the media server (live captions and the like). Its definition carries the image, an `enabled` flag, `docker_options` (GPUs, limits, extra volumes) and the agent's own configuration (for example the speech-to-text provider and its credentials). Agents are not modules: each one is a file of its own, and `ov stack agent` reads and rewrites them.

```console
$ ov stack agent ls
AGENT                     ENABLED   IMAGE                                                  STATE
agent-speech-processing   no        docker.io/openvidu/agent-speech-processing-vosk:main   -
```

Turn one on or off, live. `ov` sets `enabled` in the definition, regenerates the agents' Compose file (or runs a `helm upgrade` on PRO) and creates or removes just that agent's service:

```console
$ ov stack agent enable speech-processing
enable: agent-speech-processing (docker.io/openvidu/agent-speech-processing-vosk:main)
on-premise change: set enabled in the agent's definition, render config/ into data/runtime/ again (docker-compose.agents.yaml with it), create the agent's service; the rest keep running.
✓ set enabled=true in config/agent-speech-processing.yaml
✓ sudo ov stack render --this-node
✓ docker compose --env-file data/runtime/compose.env up -d --force-recreate --no-deps agent-speech-processing
agent agent-speech-processing enabled
```

```console
$ ov stack agent ls -o wide
AGENT                     ENABLED   IMAGE                                                  STATE     STATUS                  FILE
agent-speech-processing   yes       docker.io/openvidu/agent-speech-processing-vosk:main   running   Up Less than a second   config/agent-speech-processing.yaml
```

Disabling removes the container; the definition stays, so `enable` brings it back. The first start pulls the agent image, which is large (the models are inside it), so give it time.

- On a **Community** stack the definitions are `config/agent-<name>.yaml` on the node, and an agent of your own is one more such file. The next deploy (or `ov stack agent enable`) picks it up.
- On a **local** stack they are the `agent-*.yaml` files in the deployment directory.
- On a **PRO** stack they are entries of the release's `agents` values (the chart ships `speech-processing`, disabled), and `enable`/`disable` is a `helm upgrade`.

`<name>` is the file's name without the extension, with or without the `agent-` prefix.

## Next steps

- [Change the configuration](configuration.md) of the stack.
- [Scale](scaling.md) an Elastic or HA stack.
- The full [command reference](../reference.md).
