Every command below operates on **the stack in the current directory**: the one the deploy created, or one adopted with `ov stack import`. From anywhere else, `--dir <path>` points to it; on a node `ov` deployed, `sudo ov stack status` works with no directory. `ov help stack <command>` lists every flag.

## Status { #status }

`ov stack status` prints the state of the stack and the disk of each node, where the recordings and the databases grow:

```console
$ ov stack status
HOST          ROLE     STATE    DATA DISK USED
172.30.0.96   single   active   55% (397.0 GiB free)
```

On a PRO stack it shows one row per service, then each node's disk. It warns when a disk is 85% used.

`--wait` blocks until the stack is ready:

```console
$ ov stack status --wait
waiting for OpenVidu to be ready on the node (Ctrl-C to stop waiting; the deployment keeps running)…
  ⏳ still starting: openvidu, meet (0s)
  ⏳ still starting: openvidu (5s)
✔ OpenVidu is ready at https://172-30-0-96.openvidu-local.dev (caddy, openvidu, dashboard, meet)
```

Right after a first PRO deploy the wait can take longer than the default 5 minutes: raise it with `--wait-timeout 15m`. On PRO it prints the counts as they change (`services 14/16` on a Single Node, `master nodes 1/4, media nodes 0/1, services 30/40` on Elastic and High Availability); on a cloud it also waits for the media nodes the stack asks for, which join on their own minutes after the deploy. `--wait --joined` is for a High Availability stack still being put together: it waits only for the nodes that have joined so far.

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

## Health test { #health-test }

`ov stack test` is an active health check. It exits non-zero on failure, so it works in CI:

```console
$ ov stack test
✓ openvidu-active    172.30.0.96   active
all 1 check(s) passed
```

On PRO it checks that the stack is reachable and that every service is ready:

```console
$ ov stack test
✓ stack reachable
✓ 16/16 services ready
all 2 check(s) passed
```

## Logs { #logs }

`ov stack logs` fetches the logs of the whole stack as one stream; `--tail N`, `--since` and `-f` (follow) work as usual:

```console
$ ov stack logs --tail 8
==> 172.30.0.96 (single) <==
Nov 04 03:26:57 node-172-30-0-96 docker[4229]: mongodb            | {"t":{"$date":"2026-11-04T03:26:57.833+00:00"}, …
Nov 04 03:26:58 node-172-30-0-96 docker[4229]: ov-livekit-server  | 2026-11-04T03:26:58.118Z        WARN        livekit  …
…
```

On a PRO stack, `ov stack logs SERVICE` fetches one service's logs (`ov stack logs meet --since 30m`). On a Community server, read one service's logs with Docker Compose on the node, as root: `cd /opt/openvidu && sudo docker compose --env-file data/runtime/compose.env logs <service>`.

## Ports { #ports }

`ov stack check-ports` verifies that the inbound ports the stack needs really reach the server, TCP **and** UDP. It is the most useful check before going live: a stack with a blocked media port looks healthy and simply has no media.

Against a running stack the check can only connect to the ports, and UDP cannot be verified that way. To verify everything, stop the stack for a few seconds and start it again **whatever the check reports**:

```bash
ov stack stop && ov stack check-ports; ov stack start
```

Keep the `;` before `start`: the check exits non-zero when it finds a problem, and with `&&` the stack would stay stopped. On a PRO stack on Google Cloud, Oracle Cloud or DigitalOcean, give the check the master and its key: `ov stack check-ports --ssh <user>@<master> --ssh-key <key>`.

The check never changes a firewall: it prints the fix for you to run. `--ssh [user@]host` checks a machine before deploying to it.

## Start, stop and restart { #start-stop-and-restart }

`ov stack start`, `ov stack stop` and `ov stack restart` control the whole stack. They stop OpenVidu, not the machines.

```console
$ ov stack restart
✓ [172.30.0.96 single] systemctl restart openvidu
restart completed on 1 node(s)
```

Restarting a single service is not available yet.

## Configuration { #configuration }

`ov stack config` reads and changes the configuration of the running stack (`view`, `get`, `set`, `unset`, `edit`, and `file` for the service files), recreating only the services that read a changed value; `ov stack plan` previews a change. See [How to change OpenVidu configuration](/docs/self-hosting/configuration/changing-config.md).

## Modules and agents { #modules-and-agents }

A **module** is a feature of OpenVidu you turn on or off while the stack runs (`meet`, `observability`, `ingress`…): `ov stack module ls` lists them and `ov stack module add|rm` changes the selection. An **agent** adds AI capabilities to rooms: `ov stack agent ls` lists the stack's agents and `ov stack agent enable|disable <name>` turns one on or off, live. See [Enable and disable modules](/docs/self-hosting/how-to-guides/enable-disable-modules.md).

## Scripts and exit codes { #exit-codes }

Every command runs unattended as well. `-o json` (or `yaml`, `jsonpath=<expr>`, `go-template=<expr>`) prints what a command reports in a form a script reads, `--non-interactive` turns a missing value into an error instead of a question, and `-y` answers the confirmations (never the `--keep-data` or `--delete-data` a destroy must be told). `ov --help` lists the flags every command takes. The exit code says what happened:

| Code | Meaning |
| :---: | --- |
| `0` | Success |
| `1` | Error |
| `2` | Usage error |
| `3` | No stack in the directory |
| `4` | Configuration validation failed |
| `5` | Plan not empty (`plan --detailed-exitcode`), or `config file apply\|edit --dry-run` would change something |
| `6` | A deploy or join stopped before touching the node: a required port does not reach it, or (PRO) the node's firewall drops the stack's internal networks |
| `7` | A configuration document changed since it was read (`config file apply` without `--force`) |
| `8` | `stack test` failed, or `stack check-ports` found what would stop a deploy with `6` |
| `9` | An update stopped before touching the node: a filesystem there lacks the space it needs |
| `10` | A cloud deploy, destroy or import stopped before touching the cloud: a tool is missing on this machine, the cloud's CLI has no session, or the region's quota cannot hold the stack |

## Export the desired state { #export }

`ov stack export` prints the stack's desired state (`openvidu-stack.yml`) with its secrets as `***`; `--show-secrets` prints them, and `--out <file>` writes a file only you can read. `--gitops` turns the secrets into `secrets://` references, so the file can go to a Git repository. `ov stack export --bundle --out <file>` writes the description another machine adopts the stack from, with `ov stack import -f <file>`.
