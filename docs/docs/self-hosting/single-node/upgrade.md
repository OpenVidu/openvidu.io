---
title: "Upgrade OpenVidu Single Node"
description: "Update an OpenVidu Single Node deployment with the OpenVidu CLI, keeping your configuration and data, and convert an install.sh deployment."
---

# Upgrade OpenVidu Single Node

**A release of `ov` deploys the same release of OpenVidu**: `ov` X.Y.Z deploys OpenVidu X.Y.Z. So updating a stack means running the command with the `ov` of the version you want: [install that version](../openvidu-cli.md#install-the-openvidu-cli) first. Every plan and every message names the version the stack runs and the one it moves to. An older `ov` refuses to downgrade a stack.

## Update a stack { #update-a-stack }

`ov stack update` brings a Community server or a PRO stack to the version of this `ov`. Run it from the stack's directory:

```bash
ov stack update --dry-run   # the plan
ov stack update             # asks, then updates
```

Without `-y`, it asks for confirmation; with no terminal, `-y` is required. A stack that already runs this version says so and does nothing. To update a **local** stack, deploy it again with the new `ov` (`ov stack deploy` in its directory).

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    **Your edits survive a three-way merge.** Every file `ov` manages (`docker-compose.yaml` and `config/`) is merged three ways: the file as the installed version wrote it (kept on the node under `.ov/base/<version>/`), the file on the node now, and the new version's file. `config/openvidu.yaml` is merged by values, the other files by lines. A file nobody edited becomes the new version's. An edit to lines the new version does not change is kept. An edit on the **same lines** (or the same value) is a conflict: the update stops before touching anything (exit `4`) and names the file.

    **The disk is checked first.** For each filesystem on the node, the plan compares what the update writes there (the backup, the new files, the new images), plus a margin, with the free space. If one does not have enough room, the update stops before anything changes (exit `9`) and says how much space is missing and where.

    With no conflict, the update backs up, writes the new files, pulls the new images **while the old version still runs**, renders and restarts, so the stack is down only for the restart:

    ```console
    $ ov stack update -y
    update stack "web" on 10.5.0.3 from OpenVidu main to main
    configuration: 0 file(s) take main's version, 1 keep your edits, 0 new, 0 removed, 19 unchanged
      ~ config/livekit.yaml (your edits kept)
    …
    ✓ [10.5.0.3 single] install this CLI at /usr/local/bin/ov
    ✓ [10.5.0.3 single] render config/ into data/runtime/ (ov stack render) — 0 created, 1 updated, 21 unchanged, 0 removed
    ✓ [10.5.0.3 single] docker compose --env-file data/runtime/compose.env pull --quiet
    ✓ [10.5.0.3 single] systemctl restart openvidu
    ✔ stack "web" updated from main to main
    ```

    **A failure rolls back.** If a step fails once the update has started, the backup under `.ov/update/<version it ran>/` is restored (the previous `ov` included) and the stack is started again at the version it ran. The command then fails and says so.

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    --8<-- "self-hosting/common/ov-update-pro.md"

## Migrate a deployment installed by install.sh { #migrate-a-deployment-installed-by-installsh }

With a node named, **`ov stack update`** converts, once, a deployment installed with the published `install.sh` (3.9.0) into a stack that `ov` deploys and operates, on the same machine, keeping the configuration with your edits, the certificates and the data (Meet's rooms and users, recordings). Run it from an empty directory; the stack is recorded there as a deploy would record it, as `NAME` (default `openvidu`).

```bash
ov stack update web --ssh ubuntu@<host> --ssh-key ~/.ssh/key --dry-run   # the plan
ov stack update web --ssh ubuntu@<host> --ssh-key ~/.ssh/key             # asks, then converts it
sudo ov stack update web --this-node                                      # on the node itself
```

A Community node becomes the plain Docker Compose tree `ov` deploys; a PRO single node becomes Kubernetes on the same machine. The plan and the result name both versions: `from OpenVidu 3.9.0, installed by install.sh, to <this ov's version>`.

```console
$ ov stack update web --ssh ubuntu@10.5.0.3 --ssh-key ~/.ssh/id_ed25519 --dry-run
update stack "web" on 10.5.0.3 from OpenVidu 3.9.0, installed by install.sh, to main
found: OpenVidu 3.9.0 Community at playground.openvidu-local.dev (on-premises, certificate owncert), modules: egress,ingress,dashboard,meet,observability
configuration: 19 file(s) become ov's, 1 keep your edits, 1 new
  ~ config/livekit.yaml (your edits kept)
steps on the node:
  systemctl stop openvidu
  …
  then as a deploy: ov's tree, the unit, this CLI, the render, the pull, the start
(dry run — nothing changed; the node still runs the installed 3.9.0)
```

Running it (type the stack name, or `-y`) stops the installed stack, backs it up to `.ov/migrate/3.9.0/`, converts `config/openvidu.env` into `config/openvidu.yaml`, moves MongoDB's files to the layout `ov` runs, removes the installer's leftovers, and then does what a deploy does. Your edits are merged three ways against the file the 3.9.0 installer wrote, which `ov` reproduces byte for byte; an edit on the lines `ov` changes is a conflict that stops the conversion before anything runs (exit `4`), and a node without the disk space it needs stops it too (exit `9`). A Community node rolls back completely on a failure, to the unchanged 3.9.0. A PRO single node becomes Kubernetes: a failure **before `helm install`** rolls back to the unchanged 3.9.0, but from `helm install` on nothing is rolled back (the chart's pods have run on the data). The stack is then recorded, the installed stack left stopped but not retired, and the command exits `1` with both the commands to retire it once `ov stack status --wait` passes and the commands to put it back on the node. Your edits to the Meet service in `docker-compose.override.yaml` carry over as an `ov-meet` entry of the new override; an application of your own in Meet's place stays yours, with the `meet` module off.

Because **the images become this `ov`'s**, migrating with the `ov` of the release you want is also the update to it. A node at a release older than 3.9.0 updates to 3.9.0 with its own updater first. A node that already runs the stack `ov` deploys is not converted: the error says to update it from its own directory, or to record it here first with `ov stack import --ssh …`. Nothing of the installer remains on a node that has already been converted, so a second run is refused.

--8<-- "self-hosting/common/ov-upgrade-cloud-templates.md"

## Next steps

- [Administer the deployment](on-premises/admin.md): status, logs, the health check.
- [Change the configuration](../configuration/changing-config.md) or [the modules](../how-to-guides/enable-disable-modules.md).
- The full [OpenVidu CLI reference](../openvidu-cli.md#command-reference).
