---
title: "OpenVidu configuration system in depth"
description: "How OpenVidu configuration works: the global document, the service files, variable interpolation, rendering the runtime tree and the emergency overrides."
---

# OpenVidu configuration system in depth

OpenVidu keeps its settings in one global document, **`openvidu.yaml`**, and the service files read values from it through placeholders. This mechanism keeps the configuration consistent and simple to manage: a value defined once in `openvidu.yaml` is referenced across many service configurations. [`ov stack config`](changing-config.md) is how you read and change it.

## How variable interpolation works

A service file (such as `livekit.yaml` or `caddy.yaml`) is rendered on each node that runs it (on **PRO**{ .openvidu-tag .openvidu-pro-tag }, in each pod that mounts it), from these sources:

1. **Text with no placeholder** stands as it is.
2. **`${openvidu.<path>}`** reads the global document `openvidu.yaml`, by path (`${openvidu.domain.name}`) or by the old `openvidu.env` name (`${openvidu.DOMAIN_NAME}`). A key the document does not have takes the model's default, so a newer `ov` can read a key an older document never wrote. No other namespace exists: a bare `${FOO}` is an error, not a value from the environment.
3. **`${node.<key>}`** reads the node's own `config/node.yaml`, which holds the values specific to each machine (for example its private IP). Nothing else supplies it, so a placeholder with no modifier and no value in that file fails the render, naming the file, the line and the placeholder.
4. **`${ov.node.name}`, `${ov.node.role}` and `${ov.node.ip}`** are computed on every render: the machine's host name, its role (`master-node` on Community, or the node's label in a cluster) and the address of the default route.

The placeholder modifiers follow the [Docker Compose interpolation :fontawesome-solid-external-link:{.external-link-icon}](https://docs.docker.com/reference/compose-file/interpolation/){:target="_blank"} syntax:

- `${openvidu.OPENVIDU_PRO_LICENSE:?mandatory}` fails the render if the value is not set, ensuring required settings are not missed.
- `${node.privateIp:-127.0.0.1}` falls back to a default when the value is empty.

An example from a Media Node's `livekit.yaml`:

```yaml
openvidu:
    license: ${openvidu.license}
    cluster_id: ${openvidu.domain.name}
    # On PRO, openvidu.node.private_ip is supplied per-pod by the
    # LIVEKIT_OPENVIDU_NODE_PRIVATE_IP environment variable, not by a placeholder.
```

!!! info "Two values that behave differently"

    A key with no value (`turnDomain.name:`) has none, and the placeholder's modifier decides what happens (`:?` fails, `:-` takes the default); an empty string (`turnDomain.name: ''`) is a value. A list is its items joined by commas, which is how `modules:` reaches the `ENABLED_MODULES` that a service file reads.

## Render the configuration tree { #render-the-configuration-tree }

On a Community stack, `ov stack render` turns `config/` into the files the services mount, under `data/runtime/`: every file with its placeholders expanded from `config/openvidu.yaml`, plus `data/runtime/compose.env` for Compose and `docker-compose.agents.yaml` from the agents' definitions. The systemd unit runs it before every start, so editing a file under `config/` and `sudo systemctl restart openvidu` applies it. If any file fails to render (a required value left blank, an agent without its image), nothing is written and the error names the file and the key (exit `4`).

After a change of the Redis password in `config/openvidu.yaml`:

```console
$ sudo ov stack render --this-node
FILE                                                                       SERVICE                   ACTION
data/runtime/compose.env                                                   -                         update
data/runtime/config/egress/egress.yaml                                     ov-egress                 update
data/runtime/config/ingress/ingress.yaml                                   ov-ingress                update
data/runtime/config/openvidu/livekit.yaml                                  ov-livekit-server         update
data/runtime/config/redis/redis.env                                        redis                     update
…
modules: egress,ingress,dashboard — 0 created, 5 updated, 8 unchanged, 0 removed
```

The updated files are those that read the changed value; they belong to the same services that `config set` recreates. `--dry-run` reports what would be written and writes nothing. A PRO stack has nothing to render here: each pod renders its own documents when it starts. A local stack renders its directory's `config/` the same way.

## Settings only one edition has { #settings-only-one-edition-has }

COMMUNITY and PRO run the same features on different engines, so almost every setting exists in both, under the same key and meaning; only where it is written changes. `ov stack deploy` and `ov stack config set` reject a setting that belongs to the other edition and name the setting and its flag (exit `4`). The exceptions are a handful of settings one edition does not have:

| Setting | Edition | Why |
| --- | --- | --- |
| `openviduStack.rtcEngine` | PRO | the Pro media engine (`--rtc-engine`) |
| `openviduStack.license` | PRO | the license (`--openvidu-pro-license`) |
| `openviduStack.externalAzureBlob.clusterDataContainerName` | PRO | the cluster's own data, which one machine does not have |
| `openviduStack.externalS3.clusterDataBucket` | PRO | the cluster's own data, which one machine does not have |
| `infrastructure.offlineMediaNodes` | PRO | media nodes of Elastic and HA |
| `openviduStack.credentials.mongoReplicaSetKey` | COMMUNITY | the chart generates the replica set's keyfile itself |
| `openviduStack.mongo.enabled` | COMMUNITY | on Kubernetes MongoDB follows the modules |
| Host-network ports (`openviduStack.mongo.internalPort`, `openviduStack.redis.internalPort`, `openviduStack.minio.apiInternalPort`…) | COMMUNITY | on Kubernetes a Service fixes them |

On PRO, any low-level chart value with no setting of its own is **not** a configuration setting; it goes in the stack's [`cluster-overrides.yaml`](#emergency-overrides).

## Emergency overrides { #emergency-overrides }

For the environments the default deployment cannot adapt to. This is not a way to configure OpenVidu (that is `openvidu.yaml` and the service files), and a stack that works needs nothing from it.

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    A Community server keeps the file Docker Compose merges over `docker-compose.yaml` by itself: `/opt/openvidu/docker-compose.override.yaml`. It is yours: `ov` never writes it once the stack is deployed, and `ov stack update` keeps it. It is not under `config/`, so the `config file` verbs do not handle it: edit it on the node and apply it with `sudo systemctl restart openvidu`. It takes Compose's own syntax:

    ```yaml
    services:
      ov-egress:
        environment:
          MY_VARIABLE: my-value
      grafana:
        ports:
          - "3000:3000"
      my-app:
        image: my-registry/my-app:1.4
        network_mode: host
    ```

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    Every PRO stack has the document `cluster-overrides.yaml`, a ConfigMap of the stack's namespace kept outside the Helm release. The deploy creates it empty and never writes it again. It is read, edited and applied like any other document (`ov stack config file get|edit|apply|diff cluster-overrides.yaml`), and every install and upgrade `ov` runs applies it. It has four sections:

    - **`services`**: extra environment variables for the containers of a service, by its name (`ov-egress`, `caddy-proxy`, `redis`, `ov-livekit-server`, `agent-<name>`…).
    - **`values`**: values of the chart with no setting of their own, merged last over everything `ov` builds. This is where a low-level chart value such as `images.registry` (for a private mirror) or a per-service `resources` limit goes. A value that a setting of `openvidu.yaml` already writes is refused, naming the setting to change instead.
    - **`patches`**: a strategic merge patch to any field of an object the stack generates.
    - **`objects`**: whole objects of your own, deployed with the stack and removed with it.

    ```yaml
    services:
      ov-egress:
        environment:
          MY_VARIABLE: my-value
    values:
      ovEgress:
        resources:
          limits:
            memory: 4Gi
    ```

    Nothing tied to licensing can be changed through it: the license, the licensing daemon and the licensed services' command, mounts and configuration render are refused (exit `4`). For a private image mirror, one line of `values` changes the registry of every image the stack runs:

    ```yaml
    values:
      images:
        registry: mirror.example:5000
    ```
