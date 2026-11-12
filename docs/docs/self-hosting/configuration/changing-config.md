---
title: "Change OpenVidu configuration"
description: "View, get, set and unset an OpenVidu stack's configuration with the OpenVidu CLI, work on whole service files, manage secrets and preview every change."
---

# How to change OpenVidu configuration

`ov stack config` reads and changes the configuration of a **running** stack with minimal impact: it recreates only the services that read a changed value, while the rest keep running. Every command operates on the stack in the current directory (see [the stack directory](../deployment-types.md#the-stack-directory)).

The configuration is one YAML document, **`openvidu.yaml`**, with a comment above each value, plus the service files beside it (`livekit.yaml`, `caddy.yaml`, the agents' `agent-<name>.yaml`…). Every edition and environment has the same documents; only where they are stored differs ([see below](#where-the-configuration-lives)).

!!! info "No more editing files on every node"

    You no longer edit `openvidu.env` on each node and run `systemctl restart openvidu` by hand. `ov stack config set` writes the value, renders the configuration and recreates only the services that need it, on every node of the deployment.

## View, get, set, unset { #view-get-set-unset }

`ov stack config view` prints the whole `openvidu.yaml` as the stack runs it, comments included, with the secrets as `***` (`--show-secrets` prints them). `ov stack config get` reads one value; these are three names of the same setting on a Community server:

```console
$ ov stack config get domain.name
172-30-0-96.openvidu-local.dev
$ ov stack config get openviduStack.domain.name
172-30-0-96.openvidu-local.dev
$ ov stack config get DOMAIN_NAME
172-30-0-96.openvidu-local.dev
```

`config get` prints secrets in plain text (`ov stack config get DASHBOARD_ADMIN_PASSWORD`). For a setting nobody has changed, it prints the default.

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

Some settings shape whole files besides `openvidu.yaml`: the certificate type and its files, the TURN domain, an external proxy, the public IP, UTC. `set` applies them just like any other setting: it renders the files they shape and merges the change into your own edits. An owncert value is the path of a PEM file, a base64 PEM or the PEM itself. On a stack at `video.example.com`:

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

What the deployment sets once (MongoDB's credentials, Meet's initial admin and API key) is **refused** on a running stack (exit `4`): the service that owns it keeps the value it was first started with, and a changed value would only lock the others out:

```console
$ ov stack config set mongo-admin-password=abc
ov: openviduStack.credentials.mongoAdminPassword is set when the stack is deployed and does not change on a running node: the service that owns it keeps the value it was first started with, and the rest would stop connecting
```

## Service files { #service-files }

`openvidu.yaml` holds the settings; the service files hold what a single service reads, such as the media server's `livekit.yaml` or OpenVidu Meet's `meet.env`. `ov stack config file` works on any of them:

| Command | What it does |
| --- | --- |
| `ov stack config file ls` | Lists the documents, the services that read each one, where it is kept and whether it differs from the one the installed version ships. |
| `ov stack config file get <doc> [--out <file>]` | Prints one document (`--out` writes it to a file of mode `0600`, secrets included). |
| `ov stack config file edit <doc>` | Opens it in `$EDITOR` and applies it when you save. |
| `ov stack config file diff <file>` | Shows how a file differs from the stack's document, and what applying it would restart. |
| `ov stack config file apply <file> [--as <doc>]` | Uploads a document. It is validated and the stack rendered with it before anything is written (exit `4` if either fails), and only the services that read it restart. |

`file apply` refuses a document that changed since your `file get` or `file edit` read it (exit `7`), so two administrators cannot overwrite each other's edits; `--force` applies it anyway. `--dry-run` prints the diff and the restarts and writes nothing (exit `5` when it would change something).

## Preview a change { #preview-a-change }

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

`--detailed-exitcode` exits `5` when the plan is not empty, which is useful as a pipeline gate.

On a **PRO**{ .openvidu-tag .openvidu-pro-tag } stack, the services a change restarts are the ones the chart computes, the same set that [`ov stack config set --dry-run`](#view-get-set-unset) of that change reports: `ov stack plan` writes the change into the stack's `openvidu.yaml` as `config set` would and renders the chart with and without it, so the `restart:` line names the services whose pods would roll out. When the stack cannot be reached, or `config set` would refuse the change, the plan prints `restart: not computed (<why>)` instead and a note on standard error says why.

## Where the configuration lives { #where-the-configuration-lives }

This is the main operational difference between the editions.

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    **The node's files are the source of truth.** `config/openvidu.yaml` and the service files under `/opt/openvidu/config/` are what `view` and `get` read and what `set`, `unset` and `edit` write. A change rewrites the value in the document, keeping its comments and order, renders `config/` into the runtime tree ([`ov stack render`](in-depth.md#render-the-configuration-tree)) and recreates the services whose rendered files changed; `openvidu-stack.yml` is then updated to match the node. Editing a file by hand and running `sudo systemctl restart openvidu` is also supported: the unit renders before every start (a typo in `openvidu.yaml` stops it, naming the line), and the next `set`, `edit` or `plan` sees the edit.

    Because the source of truth is on the node, every administrator's `openvidu-stack.yml` is a copy, and a redeploy renders the tree from that copy. Before a redeploy, `ov stack plan` shows whether your copy differs from the node, and `ov stack import --ssh … --replace` refreshes it ([Operate from another machine](../single-node/on-premises/admin.md#operate-from-another-machine)).

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    **The documents in the cluster are the source of truth.** `openvidu.yaml` is a Secret of the stack's namespace (`ov-config-openvidu.yaml`) and each service file is a ConfigMap (`ov-config-livekit.yaml`…), kept outside the Helm release. `set` changes `openvidu.yaml`, validates and renders the stack with it, and applies it as a `helm upgrade`; each pod renders its documents when it starts, so only the pods that read a changed value restart. A chart value with no setting of its own is refused (such values go in the stack's [`cluster-overrides.yaml`](in-depth.md#emergency-overrides)). The stack holds its own configuration, so no client can be stale and every administrator reads the same documents.

=== "Local"

    **The directory's files are the source of truth**, with a Community server's layout inside the stack's local directory: `config/openvidu.yaml` and the service files. `config set` recreates the services whose files changed; after editing a file by hand, `ov stack deploy` applies it.

The settings a single edition has, and the chart values with no setting of their own, are covered in [OpenVidu configuration system in depth](in-depth.md#settings-only-one-edition-has).

## Secrets { #secrets }

Credentials are never written in plain text where they do not belong. At deploy time, `ov` generates every missing credential and **pins** it into `openvidu-stack.yml`, so a redeploy reuses it instead of replacing it (which would leave MongoDB and MinIO locked out of their data).

`ov stack export` prints `openvidu-stack.yml` with its secrets **masked** as `***`:

- `--show-secrets` prints the real values, the PRO license and the owncert keys included: do not share its output. A spec with masked secrets is refused as input (exit `4`).
- `--out <file>` writes the spec to a file of mode `0600`; `--bundle --out <file>` writes the importable copy, secrets included.
- `--gitops` prints `openvidu-stack.yml` with every secret externalized to a `secrets://` reference, so the file is safe to commit to a Git repository while the values stay out of it.

Keep the `.openvidu/` directory private: it holds the stack's state and secrets.

## Troubleshooting configuration

If a change does not take effect or a service fails to start:

1. Check the state of the stack's services:

    ```bash
    ov stack status
    ```

    A service stuck `restarting` or `failed` is usually reading a value it cannot parse. On a Community server, the systemd unit renders `config/` before every start and stops with the offending file and line when a value is malformed.

2. Follow the logs of the affected service:

    ```bash
    ov stack logs
    ```

    On OpenVidu PRO you can follow one service, for example `ov stack logs ov-livekit-server -f`.

3. Preview what your desired state would change against what the stack runs, to find a drifted or half-applied value:

    ```bash
    ov stack plan
    ```

For the health check and the full status report, see [Status and health checks](../single-node/on-premises/admin.md#status). For generic CLI troubleshooting and exit codes, see [Troubleshooting](../openvidu-cli.md#troubleshooting).
