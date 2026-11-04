---
title: "OpenVidu CLI command reference"
description: "Reference for the OpenVidu CLI: global flags, exit codes and every ov stack command with its purpose and main flags, linking to the full guides."
---

# Command reference

The OpenVidu CLI operates **the stack in a directory** (`--dir`, the current directory by default). This page lists every `ov stack` command with its purpose and main flags; `ov help stack <command>` prints the authoritative flag list of each one. The task-oriented guides are linked throughout.

## Global flags

| Flag | Meaning |
| --- | --- |
| `--dir <path>` | Stack directory to operate on (default `.`). Its state lives in `<dir>/.openvidu`, and relative paths resolve against it. |
| `-o, --output <fmt>` | `table` (default), `json`, `yaml`, `wide`, `name`, plus `jsonpath=<expr>` and `go-template=<expr>` for scripting. |
| `--non-interactive` | Never prompt; a missing required value is an error. |
| `-y, --yes` | Assume "yes" for confirmations (for example `destroy`). |
| `--dry-run` | Compute and print what would happen; change nothing. A command that cannot preview rejects the flag (exit `2`) rather than ignoring it: `deploy` (preview one with `--mode assisted` or `ov stack plan`), `join`, `leave`, `import`, and `export` with `--out`, `--to-stack` or `--gitops`. |
| `-v, --verbose` / `--debug` | More logging. |
| `-h, --help` | Help. |
| `-V, --cli-version` | Print the CLI version. |

## Exit codes

| Code | Meaning |
| :---: | --- |
| `0` | Success |
| `1` | Error |
| `2` | Usage error |
| `3` | No stack in the directory |
| `4` | Configuration validation failed |
| `5` | Plan not empty (`plan --detailed-exitcode`), or `config file apply\|edit --dry-run` would change something |
| `6` | A deploy or join stopped before touching the node: a required port is closed, or the node's firewall drops the pod networks (PRO) |
| `7` | A configuration document changed since it was read (`config file apply` without `--force`) |
| `8` | `stack test` failed, or `stack check-ports` found a required port failing (or, on PRO, the node's firewall dropping the pod networks) |
| `9` | An update or migration stopped before touching the node: a filesystem lacks the space it needs |

## Deploy

### `ov stack deploy [NAME]`

Creates the stack described by the configuration and records it in the directory. There is **no wizard**: if a required value is missing, the command fails and names the field. See the deploy guides: [local](deploy/local.md), [on premises](deploy/on-premises.md), [AWS](deploy/aws.md), [Azure](deploy/azure.md), [Google Cloud](deploy/gcp.md), [Oracle Cloud](deploy/oracle.md), [DigitalOcean](deploy/digitalocean.md).

| Flag | Purpose |
| --- | --- |
| `--edition community\|pro` | Which OpenVidu edition (default `community`). PRO needs `--openvidu-pro-license`, except locally. |
| `--environment <where>` | `local`, `on-premises` or a cloud. Where the machines are. |
| `--deployment-type single_node\|elastic\|ha` | The topology. Elastic and HA deploy the master; other nodes `join` it. |
| `--ssh [user@]host` | Deploy to another machine over SSH (`--ssh-user`, `--ssh-key`, `--ssh-port`). |
| `--this-node` | Deploy on the machine `ov` runs on (Linux server only). |
| `--cloud <cloud>` | Create the machines on a cloud first; they deploy OpenVidu themselves. |
| `--mode auto\|assisted` | Run everything, or print the commands for you to run. |
| `--domain-name`, `--certificate-type`, `--enabled-modules`, … | Shorthand flags, each setting one configuration key. |
| `--modules`, `--lan` / `--no-lan`, `--local-dir`, `--free-ports` | Local only: the module selection, access from your network, where the Compose project goes, and stopping whatever holds the ports. |
| `-f <file>`, `--set key=value`, `--set-secret key=value` | An overlay of `openvidu-stack.yml`, a single key, a secret. |
| `--param Name=Value`, `--remote-state` | A cloud template parameter; also keep the stack's state on the cloud. |
| `--skip-port-check` | Deploy without the port preflight (locally, that the host ports are free; remotely, that the inbound ports reach the node). |
| `--no-wait`, `--wait-timeout` | Skip or limit the wait for readiness (`5m` by default; `40m` with `--cloud`). |

### `ov stack plan`

Previews what a deploy or a configuration change would do, without changing anything. `--detailed-exitcode` exits `5` when the plan is not empty. See [Configuration](operate/configuration.md#preview-a-change-ov-stack-plan).

### `ov stack update`

Brings a Community server or a PRO stack to the version of this `ov`, merging your edits to its configuration three ways, checking the disk first and rolling back on failure. To update a local stack, deploy it again with the new `ov`. See [Update and migrate](operate/update.md).

### `ov stack migrate [NAME]`

Converts, once, a deployment that `install.sh` 3.9.0 installed (Community, a PRO single node, Elastic or High Availability) into the stack `ov` deploys, on the same machines, keeping its configuration, certificates and data. `--master-node` and `--media-node` name the other machines of a cluster. See [Update and migrate](operate/update.md#migrate-a-deployment-installed-by-installsh).

## Live operations

All of these operate on the directory's stack, with no arguments. See [Status and health checks](operate/status.md).

| Command | What it does |
| --- | --- |
| `ov stack status [--wait]` | The state of each node, or of each pod on PRO. `--wait` blocks until ready (`--wait-timeout`, 5 minutes by default). |
| `ov stack describe` | The stack's record, endpoints and configuration summary. |
| `ov stack start` / `stop` / `restart` | Control the whole stack (per-service control is not available yet). |
| `ov stack test` | Active health check; exit `8` on failure. |
| `ov stack logs [--tail N] [--since …] [-f]` | Fetch or follow the whole stack's logs (`--tail` counts per service on a local stack, in total on a server). |
| `ov stack export [--out <file>] [--gitops] [--bundle] [--to-stack]` | Print `openvidu-stack.yml` (`--out` writes it to a file); `--gitops` externalizes the secrets to `secrets://` references; `--bundle` prints the self-contained description `ov stack import -f` reads; `--to-stack` publishes that description on the stack, for `import --ssh`. |

## Configuration

See [Configuration](operate/configuration.md).

| Command | What it does |
| --- | --- |
| `ov stack config view` | The configuration the stack runs with. |
| `ov stack config get <key>` | One value, by its path in `openvidu.yaml` (`domain.name`), model key, flag, alias or old `openvidu.env` name. |
| `ov stack config set k=v …` | Change values, recreating only the services that read them. `--dry-run` shows the plan. |
| `ov stack config unset <key>` | Return a value to its default. |
| `ov stack config edit` | Edit `openvidu.yaml` in `$EDITOR` (secrets as `***` unless `--show-secrets`). |
| `ov stack config file ls` | The stack's configuration documents: `openvidu.yaml` and the service files (`livekit.yaml`, `caddy.yaml`, `agent-<name>.yaml`…). |
| `ov stack config file get <doc>` / `edit <doc>` / `diff <file>` / `apply <file>` | Read, edit, compare or upload one document. `apply` validates it first, restarts only what reads it, and refuses a document changed since you read it (exit `7`) unless `--force`. |
| `ov stack render` | Render `config/` into the runtime tree (Community). `--this-node` for the local node. |

## Modules, agents and ports

See [Modules and agents](operate/modules.md).

| Command | What it does |
| --- | --- |
| `ov stack module ls` | Modules on/off and what each requires. |
| `ov stack module add <id>` / `rm <id>` | Turn a module on or off, live; the data services follow. |
| `ov stack agent ls` | The agents of the stack, each with its state and image. |
| `ov stack agent enable <name>` / `disable <name>` | Turn an agent on or off, live. `--dry-run` prints the commands. |
| `ov stack ports` | Local stack only: the host ports the deployment publishes, read live from Docker. |
| `ov stack check-ports` | Verify that a node's inbound ports are actually reachable (needs SSH access to the node). Exit `8` on failure. |

## Nodes of a multi-node stack

An Elastic or HA stack is deployed on one machine; every other machine joins it. See [Scaling](operate/scaling.md).

| Command | What it does |
| --- | --- |
| `ov stack join-info [--format env\|json] [--wait <duration>]` | On the deployed node: print the address and token another machine needs to join. |
| `ov stack join --this-node --as master\|media` | On the joining machine (as root): enroll it in the stack. |
| `ov stack join --ssh [user@]host --as master\|media` | From the stack's directory: join a machine over SSH. `--skip-port-check` skips the port check. |
| `ov stack kubeconfig --this-node [--server <address>]` | On the deployed node: print the cluster's administrative kubeconfig. |
| `ov stack leave --this-node [--drain] [--uninstall]` | On a joined node: take it out of the stack. `--drain` leaves gracefully (media nodes); `--uninstall` removes the agent. |

## Recover a stack directory

### `ov stack import [NAME]`

Adopts a deployed stack into the directory, so every command works afterwards. See [Operate from another machine](operate/remote.md).

| Flag | Source |
| --- | --- |
| `--this-node` | The stack on this machine. |
| `--ssh [user@]host` | A node over SSH (`--ssh-key`, `--ssh-port`). |
| `--kubeconfig <path>` | A PRO stack, from its cluster credential (`--kube-context`). |
| `-f <file>` | A description document. |
| `--cloud <cloud> --stack-name <name>` | A stack deployed with `--remote-state`, from its cloud record (infrastructure included). `<name>` is the stack's name on the cloud, `openvidu-<name>` by default, as the deploy prints it on its `record:` line. `--openvidu-pro-license` and `--param` supply the secrets the record leaves out. |
| `--replace` | Overwrite the stack recorded in this directory. |

## Teardown

### `ov stack destroy`

Tears the deployment down and removes the directory's record. Without `-y` it asks you to type the stack's name. See [Destroy](operate/destroy.md).

| Flag | Purpose |
| --- | --- |
| `--delete-data` / `--keep-data` | What becomes of the data and recordings. `--keep-data` is the default on a server and locally; on a cloud one of the two is **required**. |
| `--delete-config` | Also remove the deployment directory: on a server `/opt/openvidu` and its unit, data included; locally the compose and config files, keeping the volumes unless `--delete-data`. |
| `--keep-context` | Keep the directory's record after teardown. |
| `--keep-infrastructure` | Cloud: tear the deployment down but keep the machines running. |

## Housekeeping

`ov version` · `ov help [command]` · `ov completion bash|zsh|fish|powershell`.
