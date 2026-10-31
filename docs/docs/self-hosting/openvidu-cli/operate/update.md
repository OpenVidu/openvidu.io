---
title: "Update and migrate an OpenVidu stack"
description: "Update a Community OpenVidu server with a three-way merge and rollback, upgrade PRO by deploying again, and migrate a node installed by install.sh."
---

# Update and migrate

**A release of `ov` deploys the same release of OpenVidu**: `ov` 3.10.0 deploys OpenVidu 3.10.0. So updating a stack means running the command with the `ov` of the version you want — [install that version](../install.md) first. Every plan and every message names the version the stack runs and the one it goes to; an older `ov` refuses to downgrade.

## Update a Community server

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    `ov stack update` brings a Community stack on a server to the version of this `ov`.

    ```bash
    ov stack update --dry-run   # the plan
    ov stack update             # asks, then updates
    ```

    **Your edits survive a three-way merge.** Every file `ov` manages (`docker-compose.yaml` and `config/`) is merged by lines against three sides: the file as the installed version wrote it (kept on the node under `.ov/base/<version>/`), the file on the node now, and the new version's file. A file nobody edited becomes the new version's; an edit away from what the new version changes is kept; an edit on the **same lines** is a conflict, and the update stops before touching anything (exit `4`), naming the file:

    ```console
    $ ov stack update --dry-run
    update stack "web" on 172.30.0.10 from OpenVidu main to main
    configuration: 0 file(s) take main's version, 0 keep your edits, 0 new, 0 removed, 19 unchanged, 1 in conflict
      ! config/livekit.yaml (your edits touch the lines main changes)
    steps on the node:
      back up config/, docker-compose.yaml, the unit and the CLI to /opt/openvidu/.ov/update/main
      write the files, the unit and this CLI; pull main's images while main runs; render; restart
    ov: your edits to /opt/openvidu/config/livekit.yaml touch the lines main changes, so they cannot be carried over by themselves. Undo those edits on the node (keep a copy), run the update, and apply them again to the new file
    ```

    With no conflict, the update backs up, writes the new files, pulls the new images **while the old version still runs**, renders and restarts — so the stack is down only for the restart:

    ```console
    $ ov stack update -y
    update stack "web" on 172.30.0.10 from OpenVidu main to main
    configuration: 0 file(s) take main's version, 1 keep your edits, 0 new, 0 removed, 19 unchanged
      ~ config/livekit.yaml (your edits kept)
    …
    ✓ [172.30.0.10 single] docker compose --env-file config/openvidu.env pull --quiet
    ✓ [172.30.0.10 single] render config/ into data/runtime/ (ov stack render) — 0 created, 1 updated, 20 unchanged, 0 removed
    ✓ [172.30.0.10 single] systemctl restart openvidu
    ✔ stack "web" updated from main to main
    …
    ✔ OpenVidu is ready at https://172-30-0-10.openvidu-local.dev (caddy, openvidu, dashboard, meet, grafana)
    ```

    Without `-y` it asks (and `-y` is required with no terminal). A stack that already runs this version has nothing to do and says so.

    **A failure rolls back.** If a step fails once the update has started, the backup under `.ov/update/<version it ran>/` is restored — the previous `ov` included, since the unit renders the configuration with it on every start — and the stack is started again at the version it ran. The command fails saying so:

    ```console
    $ ov stack update -y
    …
    ✗ [172.30.0.10 single] docker compose --env-file config/openvidu.env pull --quiet
        output:  … Error manifest for busybox:0.0.0-missing not found: manifest unknown
    ✓ [172.30.0.10 single] systemctl stop openvidu || true
    ✓ [172.30.0.10 single] rm -r -f config '.ov/base' && cp -a '.ov/update/main'/config . && …
    ✓ [172.30.0.10 single] systemctl daemon-reload && systemctl start openvidu
    …
    ov: the update from main to main failed and was rolled back: the node runs main again, unchanged (the backup stays in /opt/openvidu/.ov/update/main)
    ```

    If the rollback itself fails, the error lists its commands to run by hand.

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    PRO stacks are not updated by `ov stack update` yet. **Deploy again with the new `ov`** to upgrade the release in place:

    ```bash
    ov stack deploy --edition pro   # from the stack's directory, with the new ov on your PATH
    ```

    This runs a `helm upgrade`, after a confirmation. The credentials and volumes are kept, and the values are rebuilt in three layers: the new chart's defaults for the topology, then every setting changed on the release since it was installed (`config set`, modules), then the spec, which wins. A chart default that changed since the release was installed reaches it, unless the release had set that value itself.

## Migrate a node installed by `install.sh`

A Community single node installed with the published `install.sh` (3.9.0) becomes a stack `ov` deploys and operates with **`ov stack migrate`**, run once from an empty directory. It keeps the node's configuration with your edits, its certificates and the data of MongoDB, MinIO and Redis (Meet's rooms and users, recordings).

```bash
ov stack migrate web --ssh ubuntu@<host> --ssh-key ~/.ssh/key --dry-run   # the plan
ov stack migrate web --ssh ubuntu@<host> --ssh-key ~/.ssh/key             # asks, then migrates
sudo ov stack migrate web --this-node                                      # on the node itself
```

The plan names both versions and merges your edits the same three ways the update does — the base this time being the file the 3.9.0 installer wrote, which `ov` reproduces byte for byte:

```console
$ ov stack migrate web --ssh ubuntu@172.30.0.10 --ssh-key ~/.ssh/id_ed25519 --dry-run
migrate stack "web" on 172.30.0.10 from OpenVidu 3.9.0, installed by install.sh, to main
found: OpenVidu 3.9.0 Community at 172-30-0-10.openvidu-local.dev (on-premises, certificate owncert), modules: egress,ingress,dashboard,meet,observability
configuration: 19 file(s) become ov's, 1 keep your edits, 0 new
  ~ config/livekit.yaml (your edits kept)
steps on the node:
  systemctl stop openvidu
  …
  then as a deploy: ov's tree, the unit, this CLI, the render, the pull, the start
(dry run — nothing changed; the node still runs the installed 3.9.0)
```

Running it (type the stack name, or `-y`) stops the installed stack, backs it up to `.ov/migrate/3.9.0/`, moves MongoDB's files to the layout `ov` runs, removes the installer's leftovers, and then does what a deploy does. Since the images become this `ov`'s, **migrating with the `ov` of the release you want is also the update to it**. A conflict (an edit on the lines `ov` changes) stops it before anything runs, exit `4`, and a failure after the stack is stopped rolls it back to the unchanged 3.9.0. A node at an older release updates to 3.9.0 with its own updater first; a PRO deployment is not migratable this way yet.

## Next steps

- [Change the configuration](configuration.md) or [the modules](modules.md).
- [Operate the stack from another machine](remote.md).
- The full [command reference](../reference.md).
