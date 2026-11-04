---
title: "Configure an OpenVidu stack with the CLI"
description: "View, get, set, unset and edit an OpenVidu stack's configuration with the OpenVidu CLI, manage secrets and preview every change before you apply it."
---

# Configuration

`ov stack config` reads and changes the configuration of a **running** stack, with the minimal impact: it recreates only the services that read a changed value, while the rest keep running. Every command resolves the stack in the current directory.

## View, get, set, unset

```console
$ ov stack config view            # the whole configuration the stack runs with
$ ov stack config get openviduStack.domain.name
172-30-0-96.openvidu-local.dev
$ ov stack config get DASHBOARD_ADMIN_PASSWORD
********
```

`config get` prints secrets in clear; the value is masked here. A key exists only when the stack uses it: `DASHBOARD_ADMIN_PASSWORD` needs the `dashboard` module, and without it `config get` fails with `key "DASHBOARD_ADMIN_PASSWORD" is not set`.

A key you never set takes the model's default, and `config get` says so (exit code `1`):

```console
$ ov stack config get rtc-engine
ov: openviduStack.rtcEngine is not set in stack "labp": it takes the model's default, mediasoup
```


A key can be named several ways: the model key (`openviduStack.domain.name`), the deploy flag that sets it (`domain-name`), an alias (`domain`) or the key as it appears in `config/openvidu.env` (`DOMAIN_NAME`). All of them read and write the same setting.

`ov stack config set` changes one or more values. It shows the impact and recreates only what needs it:

```console
$ ov stack config set openviduStack.credentials.dashboardAdminPassword=a-password-of-my-own
KEY                                                CHANGE    NEW   IMPACT
openviduStack.credentials.dashboardAdminPassword   changed   ***   appRestart

restart: [ov-dashboard]
✓ set DASHBOARD_ADMIN_PASSWORD=*** in config/openvidu.env
✓ sudo ov stack render --this-node
✓ docker compose --env-file config/openvidu.env up -d --force-recreate --no-deps ov-dashboard
✔ updated openvidu-stack.yml
configuration applied
```

`--dry-run` shows the plan and changes nothing. `ov stack config unset <key>` returns a value to its default. `ov stack config edit` opens the configuration in `$EDITOR`.

Some settings are not a single key of a file — the certificate type and its files, the TURN domain, an external proxy, the public IP, UTC. `set` applies them all the same, rendering the files they shape and merging the change with your own edits:

```console
$ ov stack config set certificate-type=owncert owncert-public-key=fullchain.pem owncert-private-key=privkey.pem
KEY                                            CHANGE    NEW       IMPACT
openviduStack.certificate.type                 changed   owncert   appRestart
openviduStack.certificate.owncert.privateKey   added     ***       appRestart
openviduStack.certificate.owncert.publicKey    added     ***       appRestart

restart: [caddy-proxy]
✓ render config/caddy.yaml with the new parameters
✓ write owncert/172-30-0-96.openvidu-local.dev.cert
✓ write owncert/172-30-0-96.openvidu-local.dev.key
✓ sudo ov stack render --this-node
✓ docker compose --env-file config/openvidu.env up -d --force-recreate --no-deps caddy-proxy
✔ updated openvidu-stack.yml
configuration applied
```

What the deployment sets once — MongoDB's credentials, Meet's initial admin and API key — is **refused** on a running stack (exit `4`): the store keeps the value it was first started with, and a changed file would only lock the services out.

## Preview a change: `ov stack plan`

`ov stack plan` previews what a deploy or a config change would do, without touching anything. It compares the desired state (`openvidu-stack.yml`) with what the stack currently runs and prints what would change and which services would restart:

```console
$ ov stack plan
no changes — desired state already matches current state
```

```console
$ ov stack plan
KEY                           CHANGE    NEW   IMPACT
openviduStack.meet.basePath   removed   -     appRestart

restart: [caddy-proxy ov-meet]
```

`--detailed-exitcode` exits `5` when the plan is non-empty, for gating a pipeline.

## Where the configuration lives

This is the main operational difference between the editions.

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    **The node's files are the truth.** `config/openvidu.env` and the service files under `config/` are what `view` and `get` read and what `set`, `unset` and `edit` write. A change writes the key in its file, renders `config/` into the runtime tree ([`ov stack render`](#render-the-configuration-tree)) and recreates the services that read it; then `openvidu-stack.yml` is updated so the spec says what the node runs. Editing a file by hand and `sudo systemctl restart openvidu` is a supported path too — the unit renders before every start, and the next `set`, `edit` or `plan` sees the edit.

    Because the truth is on the node, every administrator's `openvidu-stack.yml` is a copy that a redeploy renders the tree from. Keep it current with `ov stack plan`, or [import again](remote.md) before a redeploy.

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    **The Helm release's values are the truth.** No node holds an `openvidu.env`. `set` takes a chart value by its path (`caddyProxy.certificateType=letsencrypt`), or any model name for the value it maps to, and applies it as a `helm upgrade`. The stack holds its own desired state, so no client can be stale and every administrator reads the same release.

## Settings only one edition has

Community is Professional's feature on another engine, so almost every setting exists in both, under the same key and meaning; only where it is written changes. The exceptions are a handful of settings one edition does not have — the Pro license and media engine, the offline media nodes and the cluster-data container (PRO only), and a number of host-network ports and credentials the chart manages itself (Community only). `ov stack deploy` and `ov stack config set` refuse one set for the other edition, naming it and its flag (exit `4`):

```console
$ ov stack deploy pro13 --environment on-premises --edition pro --openvidu-pro-license … --set openviduStack.mongo.internalPort=27018
ov: not a setting of a Professional single_node stack: openviduStack.mongo.internalPort; a value of the chart with no setting of its own goes in --helm-values
```

On PRO, any low-level chart value with no setting of its own goes in `--helm-values`.

## Secrets

Credentials are never written in plain text where they do not belong. At deploy time `ov` generates every missing credential and **pins** it into the spec, so a redeploy reuses it instead of replacing it (which would leave MongoDB and MinIO locked out of their data).

- `--set-secret key=value` (on deploy, or `--set-secret key=@file`, `key=env:VAR`) stores the value under `.openvidu/secrets/` and writes a `secrets://` reference into the spec. The spec then carries the reference, not the value.
- `ov stack export --gitops` prints the spec with every secret externalized to a `secrets://` reference, so the spec is safe to commit to a Git repository while the values stay out of it.

Keep the `.openvidu/` directory private: it holds the stack's state and secrets.

## Render the configuration tree

On a Community stack, `ov stack render` turns `config/` (with its `${openvidu.*}` placeholders) into the runtime files the services mount, under `data/runtime/`, and generates `docker-compose.agents.yaml` from the agent definitions. It is what the systemd unit runs before every start, so editing a file under `config/` and restarting applies it:

```console
$ sudo ov stack render --this-node
FILE                                                 SERVICE             ACTION
data/runtime/config/openvidu/livekit.yaml            ov-livekit-server   update
data/runtime/config/redis/redis.env                  redis               update
…
modules: egress,ingress,dashboard — 0 created, 4 updated, 8 unchanged, 0 removed
```

The files updated are exactly those that read the changed value — the same services `config set` recreates. `--dry-run` reports what would be written and writes nothing. A PRO stack has nothing to render (its truth is the Helm release); a local stack renders only `docker-compose.agents.yaml`.

## Next steps

- [Modules and agents](modules.md): turn features on and off on a running stack.
- [Operate the stack from another machine](remote.md).
- The full [command reference](../reference.md).
