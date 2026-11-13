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

A key can be named by its path in `openvidu.yaml`, the model key, the deploy flag that sets it (`domain-name`) or its old `openvidu.env` name. `config get` prints secrets in plain text.

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

Settings that shape whole files (the certificate type and its files, the TURN domain, an external proxy) are set the same way. An owncert value is the path of a PEM file, a base64 PEM or the PEM itself:

```console
$ ov stack config set certificate-type=owncert owncert-public-key=/home/me/fullchain.pem owncert-private-key=/home/me/privkey.pem
KEY                                            CHANGE    NEW       IMPACT
openviduStack.certificate.type                 changed   owncert   appRestart
openviduStack.certificate.owncert.privateKey   added     ***       appRestart
openviduStack.certificate.owncert.publicKey    added     ***       appRestart

restart: [caddy-proxy]
…
configuration applied
```

If you edited those files on the very lines the change rewrites, nothing is written and the message names the file.

What the deployment sets once (MongoDB's credentials, Meet's initial admin and API key) cannot be changed on a running stack:

```console
$ ov stack config set mongo-admin-password=abc
ov: openviduStack.credentials.mongoAdminPassword is set when the stack is deployed and does not change on a running node: the service that owns it keeps the value it was first started with, and the rest would stop connecting
```

## Service files { #service-files }

`openvidu.yaml` holds the settings; the service files hold what a single service reads, such as the media server's `livekit.yaml` or OpenVidu Meet's `meet.env`. `ov stack config file` works on any of them:

| Command | What it does |
| --- | --- |
| `ov stack config file ls` | Lists the documents and the services that read each one. |
| `ov stack config file get <doc> [--out <file>]` | Prints one document, or writes it to a file. |
| `ov stack config file edit <doc>` | Opens it in `$EDITOR` and applies it when you save. |
| `ov stack config file diff <file>` | Shows how a file differs from the stack's document, and what applying it would restart. |
| `ov stack config file apply <file> [--as <doc>]` | Uploads a document. It is validated before anything is written, and only the services that read it restart. |

`file apply` refuses a document that changed since you read it, so two administrators cannot overwrite each other's edits; `--force` applies it anyway. `--dry-run` prints the diff and the restarts and writes nothing.

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

When the stack cannot be reached, the plan prints `restart: not computed (<why>)`.

## Where the configuration lives { #where-the-configuration-lives }

This is the main operational difference between the editions.

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    **The node's files are the source of truth**: `config/openvidu.yaml` and the service files under `/opt/openvidu/config/`, readable only by root. A change keeps the document's comments and order and recreates the services whose files changed. Editing a file by hand (`sudo`) and running `sudo systemctl restart openvidu` also works: a typo in `openvidu.yaml` stops the start, naming the line.

    Every administrator's `openvidu-stack.yml` is a copy. Before a redeploy, `ov stack plan` shows whether your copy differs from the node, and `ov stack import --ssh … --replace` refreshes it ([Operate from another machine](../single-node/on-premises/admin.md#operate-from-another-machine)).

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    **The documents in the stack are the source of truth.** Every administrator reads and writes the same documents, so no client can be stale. Only the services that read a changed value restart.

=== "Local"

    **The directory's files are the source of truth**, with a Community server's layout inside the stack's local directory: `config/openvidu.yaml` and the service files. `config set` recreates the services whose files changed; after editing a file by hand, `ov stack deploy` applies it.

The settings a single edition has, and the chart values with no setting of their own, are covered in [OpenVidu configuration system in depth](in-depth.md#settings-only-one-edition-has).

## Secrets { #secrets }

At deploy time, `ov` generates every missing credential and **pins** it into `openvidu-stack.yml`, so a redeploy reuses it instead of replacing it (which would leave MongoDB and MinIO locked out of their data).

`ov stack export` prints `openvidu-stack.yml` with its secrets **masked** as `***`:

- `--show-secrets` prints the real values: do not share its output.
- `--out <file>` writes the spec to a file only you can read; `--bundle --out <file>` writes the importable copy, secrets included.
- `--gitops` turns every secret into a `secrets://` reference, so the file is safe to commit to a Git repository.

Keep the `.openvidu/` directory private: it holds the stack's state and secrets.

## Troubleshooting configuration

If a change does not take effect or a service fails to start:

1. Check the state of the stack's services:

    ```bash
    ov stack status
    ```

    A service stuck `restarting` or `failed` is usually reading a value it cannot parse.

2. Follow the logs of the affected service:

    ```bash
    ov stack logs
    ```

    On OpenVidu PRO you can follow one service, for example `ov stack logs ov-livekit-server -f`.

3. Preview what your desired state would change against what the stack runs, to find a drifted or half-applied value:

    ```bash
    ov stack plan
    ```

For the health check, see [Status](../single-node/on-premises/admin.md#status). For generic CLI troubleshooting, see [Troubleshooting](../openvidu-cli.md#troubleshooting).
