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

Changing the selection is **incremental**: `ov` starts only the new services (and recreates the ones whose configuration changed, such as the media server), or stops the removed ones; nothing else is touched. `--dry-run` previews the change. On a local stack:

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

On a Community server the same commands rewrite `modules:` in `config/openvidu.yaml`, render the configuration again and recreate the affected services (`✓ set modules=… in config/openvidu.yaml`). The spec follows the stack: `openvidu-stack.yml` records the new selection. On PRO the change is a `helm upgrade`, and the components whose configuration changed roll out after the command returns; follow them with `ov stack status`.

## Data services follow the modules

The data services (**`redis`, `mongodb` and `minio`**) are never named directly. They come up because a module needs them and go away when no module needs them any more. Dependencies between modules are handled for you too: `meet` needs `egress`, so adding `meet` to a stack without `egress` enables both (locally and on PRO; on a Community server, `meet` runs the egress service itself without listing `egress` as a module):

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
- On a **PRO** stack they are configuration documents of the stack (`agent-<name>.yaml`, the chart ships `speech-processing`, disabled), and `enable`/`disable` writes the document and runs one `helm upgrade` that creates or removes the agent's workload.

`<name>` is the file's name without the extension, with or without the `agent-` prefix.

## Next steps

- [Change the configuration](configuration.md) of the stack.
- [Scale](scaling.md) an Elastic or HA stack.
- The full [command reference](../reference.md).
