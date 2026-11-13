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

Right after a first PRO deploy the wait can take longer than the default 5 minutes: raise it with `--wait-timeout 15m`. On PRO it prints the counts as they change (`master nodes 1/4, media nodes 0/1, services 30/40`); on a cloud it also waits for the media nodes the stack asks for, which join on their own minutes after the deploy. `--wait --joined` is for a High Availability stack still being put together: it waits only for the nodes that have joined so far.

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

## Export the desired state { #export }

`ov stack export` prints the stack's desired state (`openvidu-stack.yml`) with its secrets as `***`; `--show-secrets` prints them, and `--out <file>` writes a file only you can read. `--gitops` turns the secrets into `secrets://` references, so the file can go to a Git repository. `ov stack export --bundle --out <file>` writes the description another machine adopts the stack from, with `ov stack import -f <file>`.
