---
title: "Update and migrate an OpenVidu stack"
description: "Update an OpenVidu stack with the OpenVidu CLI, keeping your configuration edits and rolling back on failure, and migrate an install.sh deployment."
---

# Update and migrate

**A release of `ov` deploys the same release of OpenVidu**: `ov` X.Y.Z deploys OpenVidu X.Y.Z. So updating a stack means running the command with the `ov` of the version you want: [install that version](../install.md) first. Every plan and every message names the version the stack runs and the one it moves to.

## Update a stack

`ov stack update` brings a Community server or a PRO stack to the version of this `ov`. To update a local stack, deploy it again with the new `ov` (`ov stack deploy` in its directory).

```bash
ov stack update --dry-run   # the plan
ov stack update             # asks, then updates
```

Without `-y`, it asks for confirmation; with no terminal, `-y` is required. A stack that already runs this version says so and does nothing:

```console
$ ov stack update --dry-run
stack "web" on 10.5.0.3 already runs main, the version of this ov: nothing to update
```

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    **Your edits survive a three-way merge.** Every file `ov` manages (`docker-compose.yaml` and `config/`) is merged three ways: the file as the installed version wrote it (kept on the node under `.ov/base/<version>/`), the file on the node now, and the new version's file. `config/openvidu.yaml` is merged by values, the other files by lines. A file nobody edited becomes the new version's. An edit to lines the new version does not change is kept: the plan lists the file as `~ … (your edits kept)` when the new version also changes it, and counts it as unchanged otherwise. An edit on the **same lines** (or the same value) is a conflict: the update stops before touching anything (exit `4`) and names the file:

    ```console
    $ ov stack update --dry-run
    update stack "web" on 10.5.0.3 from OpenVidu main to main
    configuration: 0 file(s) take main's version, 0 keep your edits, 0 new, 0 removed, 19 unchanged, 1 in conflict
      ! config/livekit.yaml (your edits touch the lines main changes)
    steps on the node:
      back up config/, docker-compose.yaml, the unit and the CLI to /opt/openvidu/.ov/update/main
      write the files, the unit and this CLI; pull main's images while main runs; render; restart
    ov: your edits to /opt/openvidu/config/livekit.yaml touch the lines main changes, so they cannot be carried over by themselves. Undo those edits on the node (keep a copy), run the update, and apply them again to the new file
    ```

    **The disk is checked first.** For each filesystem on the node, the plan compares what the update writes there (the backup, the new files, the new images), plus a margin, with the free space. If one does not have enough room, the update stops before anything changes (exit `9`) and says how much space is missing and where.

    With no conflict, the update backs up, writes the new files, pulls the new images **while the old version still runs**, renders and restarts, so the stack is down only for the restart:

    ```console
    $ ov stack update -y
    update stack "web" on 10.5.0.3 from OpenVidu main to main
    configuration: 0 file(s) take main's version, 1 keep your edits, 0 new, 0 removed, 19 unchanged
      ~ config/livekit.yaml (your edits kept)
    …
    disk space on the node (each need with a margin of 10% plus 1.0 GiB, for the estimates and the services' first writes):
      FILESYSTEM                            NEEDS        FREE
      overlay (/)                         1.3 GiB   255.6 GiB  ok
    …
    ✓ [10.5.0.3 single] install this CLI at /usr/local/bin/ov
    ✓ [10.5.0.3 single] render config/ into data/runtime/ (ov stack render) — 0 created, 1 updated, 21 unchanged, 0 removed
    ✓ [10.5.0.3 single] docker compose --env-file data/runtime/compose.env pull --quiet
    ✓ [10.5.0.3 single] systemctl restart openvidu
    ✔ stack "web" updated from main to main
    waiting for OpenVidu to be ready on the node (Ctrl-C to stop waiting; the deployment keeps running)…
      ⏳ still starting: openvidu, dashboard, meet, grafana (0s)
    …
    ✔ OpenVidu is ready at https://playground.openvidu-local.dev (caddy, openvidu, dashboard, meet, grafana)
    ```

    **A failure rolls back.** If a step fails once the update has started, the backup under `.ov/update/<version it ran>/` is restored (the previous `ov` included, since the unit renders the configuration with it on every start) and the stack is started again at the version it ran. The command then fails and says so:

    ```console
    $ ov stack update -y
    …
    ✗ [10.5.0.3 single] docker compose --env-file data/runtime/compose.env pull --quiet
        output:  … Error manifest for busybox:0.0.0-missing not found: manifest unknown
    ✓ [10.5.0.3 single] systemctl stop openvidu || true
    ✓ [10.5.0.3 single] rm -r -f config '.ov/base' && cp -a '.ov/update/main'/config . && …
    ✓ [10.5.0.3 single] systemctl daemon-reload && systemctl start openvidu
    …
    ov: the update from main to main failed and was rolled back: the node runs main again, unchanged (the backup stays in /opt/openvidu/.ov/update/main)
    ```

    If the rollback itself fails, the error lists the commands to run by hand. (The versions read `main` here because these runs used a development build of `ov`; a release names its version.)

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    The update installs this `ov`'s chart over the release, with the values from the stack's configuration documents:

    - **Your configuration is merged.** The documents (`openvidu.yaml` and the service files) are merged with this version's against the base kept in the cluster since the deploy or the last update: `openvidu.yaml` by values, the service files by lines. A setting the new version adds gets its default value; a default nobody touched moves to the new one; your values, comments and secrets stay. A value that both you and the new version changed is a conflict: the update stops before touching anything (exit `4`) and names it.
    - **The plan comes from a dry run of the upgrade itself:** the chart, each image that changes, the workloads whose pods are replaced and the values that move (secrets as `***`).
    - **The nodes' disk is checked first:** the images each node lacks, against its free space. A node without enough free space stops the update (exit `9`).
    - **A failure rolls back.** After confirmation the update backs the documents up in the cluster, writes them, runs `helm upgrade --wait` and waits for the stack (`--wait-timeout`, 10 minutes by default). If the upgrade or the wait fails, it runs `helm rollback` to the revision the stack ran and puts the documents back.

    Run it from the stack's directory, with the new `ov` on your `PATH`.

An older `ov` refuses to downgrade a stack.

## Migrate a deployment installed by `install.sh`

**`ov stack migrate`**, run once from an empty directory, turns a deployment installed with the published `install.sh` (3.9.0) into a stack that `ov` deploys and operates, on the same machines. It converts a Community single node, a PRO single node, an Elastic cluster and a High Availability cluster, and keeps the configuration with your edits, the certificates and the data (Meet's rooms and users, recordings).

```bash
ov stack migrate web --ssh ubuntu@<host> --ssh-key ~/.ssh/key --dry-run   # the plan
ov stack migrate web --ssh ubuntu@<host> --ssh-key ~/.ssh/key             # asks, then migrates
sudo ov stack migrate web --this-node                                      # on the node itself
ov stack migrate el --ssh ubuntu@10.0.0.5 --media-node 10.0.0.7           # Elastic
ov stack migrate ha --ssh ubuntu@10.0.0.5 --master-node 10.0.0.6 \
  --master-node 10.0.0.7 --master-node 10.0.0.8 --media-node 10.0.0.9      # High Availability
```

`--ssh` names the node `ov` talks to (the master); `--master-node` (the other masters of HA) and `--media-node` name the rest, by address, with the same SSH user, key and port. A Community node becomes the plain Docker Compose tree `ov` deploys; a PRO deployment becomes Kubernetes on the same machines.

The plan names both versions and merges your edits three ways, as the update does; this time the base is the file the 3.9.0 installer wrote, which `ov` reproduces byte for byte:

```console
$ ov stack migrate web --ssh ubuntu@10.5.0.3 --ssh-key ~/.ssh/id_ed25519 --dry-run
migrate stack "web" on 10.5.0.3 from OpenVidu 3.9.0, installed by install.sh, to main
found: OpenVidu 3.9.0 Community at playground.openvidu-local.dev (on-premises, certificate owncert), modules: egress,ingress,dashboard,meet,observability
configuration: 19 file(s) become ov's, 1 keep your edits, 1 new
  ~ config/livekit.yaml (your edits kept)
steps on the node:
  systemctl stop openvidu
  …
  then as a deploy: ov's tree, the unit, this CLI, the render, the pull, the start
…
(dry run — nothing changed; the node still runs the installed 3.9.0)
```

Running it (type the stack name, or `-y`) stops the installed stack, backs it up to `.ov/migrate/3.9.0/`, converts `config/openvidu.env` into `config/openvidu.yaml`, moves MongoDB's files to the layout `ov` runs, removes the installer's leftovers, and then does what a deploy does. Your edits to the Meet service in `docker-compose.override.yaml` carry over as an `ov-meet` entry of the new override; an application of your own in Meet's place stays yours, with the `meet` module off. Since the images become this `ov`'s, **migrating with the `ov` of the release you want is also the update to it**. A conflict (an edit on the lines `ov` changes) stops it before anything runs (exit `4`), so does a node without the disk space it needs (exit `9`), and a failure rolls it back to the unchanged 3.9.0: on Community at any step after the stack is stopped, on PRO up to the moment the chart is installed. A node at an older release updates to 3.9.0 with its own updater first. A PRO deployment (single node, Elastic or High Availability) starts the logs and metrics of the `observability` module anew (`data/loki_data` and `data/prometheus_data` are not carried over); Grafana's own data is kept.

A PRO cluster is migrated in order: the media nodes stop before the masters, then `ov` installs Kubernetes on the master, deploys OpenVidu and joins the other nodes. On a single node and on Elastic the data directories become the chart's volumes in place. On High Availability the data is copied before the stack stops (a dump of MongoDB, Redis's RDB, the MinIO bucket, under `/opt/openvidu/data/migrate`) and handed over to the chart's clustered data services (`▶ Hand the data over to the chart…` in the output). On test machines an Elastic migration took about 5 minutes and a High Availability one about 20. Nothing of the installer remains on a node that has already been migrated, so a second run is refused (`… it is not a deployment install.sh made`); operate it with `ov stack` from the directory the migration recorded.

## Next steps

- [Change the configuration](configuration.md) or [the modules](modules.md).
- [Operate the stack from another machine](remote.md).
- The full [command reference](../reference.md).
