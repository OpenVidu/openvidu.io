---
title: "Configure an OpenVidu stack with the CLI"
description: "View, get, set, unset and edit an OpenVidu stack's configuration with the OpenVidu CLI, manage secrets and preview every change before you apply it."
---

# Configuration

`ov stack config` reads and changes the configuration of a **running** stack, with the minimal impact: it recreates only the services that read a changed value, while the rest keep running. Every command resolves the stack in the current directory.

The configuration is one YAML document, **`openvidu.yaml`**, with a comment above each value, plus the service files beside it (`livekit.yaml`, `caddy.yaml`, the agents' `agent-<name>.yaml`…). Every edition and environment has the same documents; only where they are kept changes ([see below](#where-the-configuration-lives)).

## View, get, set, unset

`ov stack config view` prints the whole `openvidu.yaml` as the stack runs it, comments included, with the secrets as `***` (`--show-secrets` prints them). `config get` reads one value; these are three names of the same setting on a Community server:

```console
$ ov stack config get domain.name
172-30-0-96.openvidu-local.dev
$ ov stack config get openviduStack.domain.name
172-30-0-96.openvidu-local.dev
$ ov stack config get DOMAIN_NAME
172-30-0-96.openvidu-local.dev
```

`config get` prints secrets in clear (`ov stack config get DASHBOARD_ADMIN_PASSWORD`). A setting nobody changed answers with its default.

A key can be named several ways: its path in `openvidu.yaml` (`domain.name`), the model key (`openviduStack.domain.name`), the deploy flag that sets it (`domain-name`), an alias (`domain`) or its old `openvidu.env` name (`DOMAIN_NAME`). All of them read and write the same setting.

`ov stack config set` changes one or more values. It shows the impact and recreates only what needs it:

```console
$ ov stack config set openviduStack.credentials.dashboardAdminPassword=a-password-of-my-own
KEY                                                CHANGE    NEW   IMPACT
openviduStack.credentials.dashboardAdminPassword   changed   ***   appRestart

restart: [ov-dashboard]
✓ set credentials.dashboardAdminPassword=*** in config/openvidu.yaml
✓ sudo ov stack render --this-node
✓ docker compose --env-file data/runtime/compose.env up -d --force-recreate --no-deps ov-dashboard
✔ updated openvidu-stack.yml
configuration applied
```

`--dry-run` shows the plan and changes nothing. `ov stack config unset <key>` returns a value to its default. `ov stack config edit` opens `openvidu.yaml` in `$EDITOR`, with the secrets as `***` unless `--show-secrets`; a secret left as `***` keeps its value.

Some settings shape whole files besides `openvidu.yaml`: the certificate type and its files, the TURN domain, an external proxy, the public IP, UTC. `set` applies them all the same, rendering the files they shape and merging the change into your own edits. An owncert value is the path of a PEM file, a base64 PEM or the PEM itself. On a stack at `video.example.com`:

```console
$ ov stack config set certificate-type=owncert owncert-public-key=/home/me/fullchain.pem owncert-private-key=/home/me/privkey.pem
KEY                                            CHANGE    NEW       IMPACT
openviduStack.certificate.type                 changed   owncert   appRestart
openviduStack.certificate.owncert.privateKey   added     ***       appRestart
openviduStack.certificate.owncert.publicKey    added     ***       appRestart

restart: [caddy-proxy]
✓ set certificate.type=owncert in config/openvidu.yaml
✓ render config/caddy.yaml with the new parameters
✓ write owncert/video.example.com.cert
✓ write owncert/video.example.com.key
✓ sudo ov stack render --this-node
✓ docker compose --env-file data/runtime/compose.env up -d --force-recreate --no-deps caddy-proxy
✔ updated openvidu-stack.yml
configuration applied
```

If you edited those files on the very lines the change rewrites, nothing is written (exit `4`) and the message names the file: edit it by hand, or apply the change with `ov stack deploy`, which writes the files again.

For example, after editing `config/caddy.yaml` by hand:

```console
$ ov stack config set external-proxy=true
ov: config/caddy.yaml was edited on the node where this change rewrites it: nothing was written; edit the file by hand, or apply the change with `ov stack deploy`, which writes the file again
```

What the deployment sets once (MongoDB's credentials, Meet's initial admin and API key) is **refused** on a running stack (exit `4`): the service that owns it keeps the value it was first started with, and a changed value would only lock the others out:

```console
$ ov stack config set mongo-admin-password=abc
ov: openviduStack.credentials.mongoAdminPassword is set when the stack is deployed and does not change on a running node: the service that owns it keeps the value it was first started with, and the rest would stop connecting
```

## Service files: `ov stack config file`

`openvidu.yaml` holds the settings; the service files hold what a single service reads, such as the media server's `livekit.yaml`. `ov stack config file` works on any of them:

| Command | What it does |
| --- | --- |
| `ov stack config file ls` | Lists the documents, the services that read each one, where it is kept and whether it differs from the one the installed version ships. |
| `ov stack config file get <doc> [--out <file>]` | Prints one document (`--out` writes it to a file of mode `0600`, secrets included). |
| `ov stack config file edit <doc>` | Opens it in `$EDITOR` and applies it when you save. |
| `ov stack config file diff <file>` | Shows how a file differs from the stack's document, and what applying it would restart. |
| `ov stack config file apply <file> [--as <doc>]` | Uploads a document. It is validated and the stack rendered with it before anything is written (exit `4` if either fails), and only the services that read it restart. |

`file apply` refuses a document that changed since your `file get` or `file edit` read it (exit `7`), so two administrators cannot overwrite each other's edit; `--force` applies it anyway. `--dry-run` prints the diff and the restarts and writes nothing (exit `5` when it would change something).

## Preview a change: `ov stack plan`

`ov stack plan` previews what a deploy or a config change would do, without touching anything. It compares the desired state (`openvidu-stack.yml`, plus any deploy flag you pass) with what the stack currently runs and prints what would change and which services would restart:

```console
$ ov stack plan
no changes — desired state already matches current state
```

```console
$ ov stack plan --turn-domain-name turn.172-30-0-96.openvidu-local.dev
KEY                             CHANGE   NEW                                   IMPACT
openviduStack.turnDomain.name   added    turn.172-30-0-96.openvidu-local.dev   appRestart

restart: [caddy-proxy ov-livekit-server]
```

`--detailed-exitcode` exits `5` when the plan is not empty, for gating a pipeline.

## Where the configuration lives

This is the main operational difference between the editions.

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    **The node's files are the source of truth.** `config/openvidu.yaml` and the service files under `/opt/openvidu/config/` are what `view` and `get` read and what `set`, `unset` and `edit` write. A change rewrites the value in the document, keeping its comments and order, renders `config/` into the runtime tree ([`ov stack render`](#render-the-configuration-tree)) and recreates the services whose rendered files changed; then `openvidu-stack.yml` follows the node. Editing a file by hand and `sudo systemctl restart openvidu` is a supported path too: the unit renders before every start (a typo in `openvidu.yaml` stops it, naming the line), and the next `set`, `edit` or `plan` sees the edit.

    Because the source of truth is on the node, every administrator's `openvidu-stack.yml` is a copy that a redeploy renders the tree from. Before a redeploy, `ov stack plan` shows whether your copy differs from the node, and `ov stack import --ssh … --replace` refreshes it ([Operate from another machine](remote.md)).

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    **The documents in the cluster are the source of truth.** `openvidu.yaml` is a Secret of the stack's namespace (`ov-config-openvidu.yaml`) and every service file a ConfigMap (`ov-config-livekit.yaml`…), kept outside the Helm release. `set` changes `openvidu.yaml`, validates and renders the stack with it, and applies it as a `helm upgrade`; each pod renders its documents when it starts, so only the pods that read a changed value restart. A chart value with no setting of its own is refused (it goes in `--helm-values`). The stack holds its own configuration, so no client can be stale and every administrator reads the same documents.

=== "Local"

    **The directory's files are the source of truth**, with a Community server's layout inside the stack's local directory: `config/openvidu.yaml` and the service files. `config set` recreates the services whose files changed; after editing a file by hand, `ov stack deploy` applies it.

## Settings only one edition has

COMMUNITY and PRO run the same features on different engines, so almost every setting exists in both, under the same key and meaning; only where it is written changes. The exceptions are a handful of settings one edition does not have: the PRO license and media engine, the offline media nodes and the cluster's own data bucket or container (PRO only), and some host-network ports and credentials that Kubernetes manages by itself (Community only). `ov stack deploy` and `ov stack config set` refuse a setting of the other edition, naming it and its flag (exit `4`):

```console
$ ov stack deploy pro13 --environment on-premises --edition pro --openvidu-pro-license … --set openviduStack.mongo.internalPort=27018
ov: not a setting of a Professional single_node stack: openviduStack.mongo.internalPort; a value of the chart with no setting of its own goes in --helm-values
```

On PRO, any low-level chart value with no setting of its own goes in `--helm-values`.

## Secrets

Credentials are never written in plain text where they do not belong. At deploy time `ov` generates every missing credential and **pins** it into `openvidu-stack.yml`, so a redeploy reuses it instead of replacing it (which would leave MongoDB and MinIO locked out of their data).

- `--set-secret key=value` (on deploy, or `--set-secret key=@file`, `key=env:VAR`) stores the value under `.openvidu/secrets/` and writes a `secrets://` reference into `openvidu-stack.yml`. The file then carries the reference, not the value.
- `ov stack export --gitops` prints `openvidu-stack.yml` with every secret externalized to a `secrets://` reference, so the file is safe to commit to a Git repository while the values stay out of it. A plain `ov stack export` prints the values themselves, the PRO license and the owncert keys included: do not share its output.

Keep the `.openvidu/` directory private: it holds the stack's state and secrets.

## Render the configuration tree

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

The files updated are those that read the changed value, which are the services `config set` recreates. `--dry-run` reports what would be written and writes nothing. A PRO stack has nothing to render here: each pod renders its own documents when it starts. A local stack renders its directory's `config/` the same way.

## Next steps

- [Modules and agents](modules.md): turn features on and off on a running stack.
- [Operate the stack from another machine](remote.md).
- The full [command reference](../reference.md).
