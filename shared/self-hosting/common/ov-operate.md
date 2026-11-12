Every command below operates on **the stack in the current directory**: the one the deploy created, or one adopted with `ov stack import`. From anywhere else, `--dir <path>` points to it. On a node `ov` deployed, the node keeps a stack directory of its own (`/opt/openvidu/stack`), so `sudo ov stack status` works there with no directory to name. Every flag and exit code is in the [command reference](/docs/self-hosting/openvidu-cli.md#command-reference).

## Status { #status }

`ov stack status` prints the state of the stack. On a Community server it shows each node and its data disk, the filesystem that holds `/opt/openvidu`, where the recordings and the databases grow:

```console
$ ov stack status
HOST          ROLE     STATE    DATA DISK USED
172.30.0.96   single   active   55% (397.0 GiB free)
```

On a PRO stack it shows one row per service (`SERVICE NODES READY STATE`), and after them each node's disk (`NODE ROLE DISK USED FREE SIZE`, the node's root filesystem, where the stack's volumes grow). It warns at 85% used, and on PRO also when a node reports `DiskPressure`. A node it cannot reach over SSH shows `unreachable` in its row, and the exit code is still `0`.

`--wait` blocks until the stack is ready. On a Community server it probes the node itself (Caddy, the media server and each enabled module's web endpoint) over the stack's own transport, so no DNS or route from your machine is needed:

```console
$ ov stack status --wait
waiting for OpenVidu to be ready on the node (Ctrl-C to stop waiting; the deployment keeps running)…
  ⏳ still starting: openvidu, meet (0s)
  ⏳ still starting: openvidu (5s)
✔ OpenVidu is ready at https://172-30-0-96.openvidu-local.dev (caddy, openvidu, dashboard, meet)
```

Right after a first PRO deploy, while the nodes pull the images and some services restart before they settle, the wait can take longer than the default 5 minutes: raise it with `--wait-timeout 15m`. On an Elastic or High Availability stack that is still being assembled, `--wait --joined` waits for the nodes that have joined so far and says how many are missing.

## Describe { #describe }

`ov stack describe` prints the stack's record, endpoints and a configuration summary:

```console
$ ov stack describe
Stack:       qce1
Type:        single_node
Environment: on-premises
Edition:     community
Endpoint:    https://172-30-0-150.openvidu-local.dev
Spec:        openvidu-stack.yml
Access:      SSH

Nodes:
  172.30.0.150     single       active
```

`Access` says how `ov` reaches the stack: `SSH` for a Community server, `remote (from this directory)` for a PRO stack this directory operates remotely, `this machine` for a stack deployed on the machine you run `ov` on.

## Health test { #health-test }

`ov stack test` is an active health check. It exits `8` on failure, so it works in CI:

```console
$ ov stack test
✓ openvidu-active    172.30.0.96   active
all 1 check(s) passed
```

On PRO it checks that the stack is reachable and that every service is ready (a service that is not ready is named as `service@node (state)`):

```console
$ ov stack test
✓ stack reachable
✓ 16/16 services ready
all 2 check(s) passed
```

## Logs { #logs }

`ov stack logs` fetches the logs of the whole stack as one interleaved stream; `--since` limits the time window and `-f` follows them live. On a Community server they come from the node's journal, so `--tail N` is the last N lines of the whole stack (`--since` takes a journal value such as `'1 hour ago'`):

```console
$ ov stack logs --tail 8
==> 172.30.0.96 (single) <==
Nov 04 03:26:57 node-172-30-0-96 docker[4229]: mongodb            | {"t":{"$date":"2026-11-04T03:26:57.833+00:00"}, …
Nov 04 03:26:58 node-172-30-0-96 docker[4229]: ov-livekit-server  | 2026-11-04T03:26:58.118Z        WARN        livekit  …
…
```

On a PRO stack, `ov stack logs SERVICE` fetches one service's logs: `ov stack logs ov-meet --since 30m` (the `ov-` prefix is optional, so `logs meet` works too; `--since` takes a duration such as `30m` or `2h`). On a Community server, per-service logs through `ov` are not available yet: read one service's logs with Docker Compose, from the deployment directory on the node (`/opt/openvidu`), with the stack's env file: `docker compose --env-file data/runtime/compose.env logs <service>`.

## Ports { #ports }

`ov stack check-ports` verifies that the inbound ports the stack needs actually reach the server. It runs a temporary listener on the node and probes it, so TCP **and** UDP (and the media range) are really verified. It is the single most useful check before going live, because a stack with a blocked media port looks perfectly healthy and simply has no media.

The check needs SSH access to the node. A Community stack keeps it in its record. A PRO stack on a cloud does not: on AWS and Azure the check logs in to the master as `ubuntu` with the key pair `ov` generated, when the directory holds its private half; on the other clouds it exits `2` and prints the command to run, `ov stack check-ports --ssh <user>@<master> --ssh-key <key>`, and where that key is.

Against a running stack, `ov` can only connect to the ports, and it says so rather than reporting a false result: an open UDP port and a dropped one look the same while the stack holds them. To verify the media path end to end, take the ports back for a few seconds, and start the stack again **whatever the check reports**:

```bash
ov stack stop && ov stack check-ports; ov stack start
```

The `;` before `start` matters: the check exits non-zero when it finds a problem, and with `&&` there the stack would stay stopped. On a PRO stack on Google Cloud, Oracle Cloud or DigitalOcean, give the check the master and its key: `ov stack check-ports --ssh <user>@<master> --ssh-key <key>`.

It exits `8` when a required port fails (a recommended one is a warning, exit `0`), and never changes a firewall: the fix is printed for you to run. Useful flags: `--ports required|all`, `--domain-name <name>` to probe another address, `--ssh [user@]host` to check a machine before deploying to it, `-o json` for every verdict. `ov stack ports`, which reads the published host ports live, is for a **local** stack only.

## Start, stop and restart { #start-stop-and-restart }

`ov stack start`, `ov stack stop` and `ov stack restart` control the whole stack: on a Community server, the systemd unit on the node; on PRO, every service of the stack. They stop OpenVidu, not the machines.

```console
$ ov stack restart
✓ [172.30.0.96 single] systemctl restart openvidu
restart completed on 1 node(s)
```

`--dry-run` prints the commands and runs none. Restarting a single service is not available yet: these commands always act on the whole stack.

## Configuration { #configuration }

`ov stack config` reads and changes the configuration of the running stack (`view`, `get`, `set`, `unset`, `edit`, and `file` for the service files), recreating only the services that read a changed value; `ov stack plan` previews a change. A Community deployment keeps the configuration in the node's files (`/opt/openvidu/config/`); a PRO deployment keeps it in the cluster, where every administrator reads and writes the same documents. See [How to change OpenVidu configuration](/docs/self-hosting/configuration/changing-config.md).

## Modules and agents { #modules-and-agents }

A **module** is a feature of OpenVidu you turn on or off while the stack runs (`meet`, `observability`, `ingress`, `v2compatibility` and the rest): `ov stack module ls` lists them and `ov stack module add|rm` changes the selection, and the deployment works out which services to run. An **agent** adds AI capabilities to rooms: `ov stack agent ls` lists the stack's agents and `ov stack agent enable|disable <name>` turns one on or off, live. See [Enable and disable modules](/docs/self-hosting/how-to-guides/enable-disable-modules.md).

## Export the desired state { #export }

`ov stack export` prints the stack's desired state (`openvidu-stack.yml`) with its secrets (the license, the credentials, the storage keys) as `***`; `--show-secrets` prints them, and `--out <file>` writes them to a file of mode `0600`. `--gitops` externalizes the secrets to `secrets://` references, so the file can go to a Git repository. `ov stack export --bundle --out <file>` writes the self-contained description another machine adopts the stack from, with `ov stack import -f <file>`. A file with masked secrets is refused as input (exit `4`).
