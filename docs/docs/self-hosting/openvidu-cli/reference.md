---
title: "OpenVidu CLI command reference"
description: "Reference for the OpenVidu CLI: global flags, exit codes and every ov stack command with its purpose and main flags, linking to the full guides."
---

# Command reference

The OpenVidu CLI operates **the stack in a directory** (`--dir`, default the current one). This page lists every `ov stack` command with its purpose and main flags; `ov help stack <command>` prints the authoritative flag list of each one. The task-oriented guides are linked throughout.

## Global flags

| Flag | Meaning |
| --- | --- |
| `--dir <path>` | Stack directory to operate on (default `.`). Its state lives in `<dir>/.openvidu`, and relative paths resolve against it. |
| `-o, --output <fmt>` | `table` (default), `json`, `yaml`, `wide`, `name`, plus `jsonpath=<expr>` and `go-template=<expr>` for scripting. |
| `--non-interactive` | Never prompt; a missing required value is an error. |
| `-y, --yes` | Assume "yes" for confirmations (for example `destroy`). |
| `--dry-run` | Compute and print what would happen; change nothing. |
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
| `5` | Plan not empty (`plan --detailed-exitcode`) |
| `6` | A deploy or join stopped before touching the node: a required port is closed, or the node's firewall drops the pod networks (PRO) |
| `8` | `stack test` or `stack check-ports` failed |

## Deploy

### `ov stack deploy [NAME]`

Creates the stack described by the configuration and records it in the directory. There is **no wizard**: a missing required value fails naming the field. See the deploy guides: [local](deploy/local.md), [on premises](deploy/on-premises.md), [AWS](deploy/aws.md), [Azure](deploy/azure.md), [Google Cloud](deploy/gcp.md), [Oracle Cloud](deploy/oracle.md), [DigitalOcean](deploy/digitalocean.md).

| Flag | Purpose |
| --- | --- |
| `--edition community\|pro` | Which OpenVidu (default `community`). PRO needs `--openvidu-pro-license`. |
| `--environment <where>` | `local`, `on-premises` or a cloud. Where the machines are. |
| `--deployment-type single_node\|elastic\|ha` | The topology. Elastic and HA deploy the master; other nodes `join` it. |
| `--ssh [user@]host` | Deploy to another machine over SSH (`--ssh-user`, `--ssh-key`, `--ssh-port`). |
| `--this-node` | Deploy on the machine `ov` runs on (Linux server only). |
| `--cloud <cloud>` | Create the machines on a cloud first; they deploy OpenVidu themselves. |
| `--mode auto\|assisted` | Run everything, or print the commands for you to run. |
| `--domain-name`, `--certificate-type`, `--enabled-modules`, … | Friendly flags, each setting one configuration key. |
| `-f <file>`, `--set key=value`, `--set-secret key=value` | A spec overlay, a single key, a secret. |
| `--param Name=Value`, `--remote-state` | A cloud template parameter; also keep the stack's state on the cloud. |
| `--skip-port-check` | Deploy without the inbound-port preflight. |
| `--no-wait`, `--wait-timeout` | Skip or bound the wait for readiness. |

### `ov stack plan`

Previews what a deploy or a configuration change would do, without changing anything. `--detailed-exitcode` exits `5` when the plan is non-empty. See [Configuration](operate/configuration.md#preview-a-change-ov-stack-plan).

### `ov stack update`

Brings a **Community** server to the version of this `ov`, merging your edits three ways and rolling back on failure. PRO upgrades by deploying again. See [Update and migrate](operate/update.md).

### `ov stack migrate [NAME]`

Converts, once, a Community single node that `install.sh` 3.9.0 installed into the tree `ov` deploys, keeping its configuration, certificates and data. See [Update and migrate](operate/update.md#migrate-a-node-installed-by-installsh).

## Live operations

All of these resolve the directory's stack with no arguments. See [Status and health checks](operate/status.md).

| Command | What it does |
| --- | --- |
| `ov stack status [--wait]` | Per-service state. `--wait` blocks until ready. |
| `ov stack describe` | The stack's record, endpoints and configuration summary. |
| `ov stack start` / `stop` / `restart` | Control the whole stack (per-service control is not available yet). |
| `ov stack test` | Active health check; exit `8` on failure. |
| `ov stack logs [--tail N] [--since …] [-f]` | Fetch or follow logs (`--tail` is per service). |
| `ov stack export [--gitops]` | Print the spec; `--gitops` externalizes secrets to `secrets://` references. |

## Configuration

See [Configuration](operate/configuration.md).

| Command | What it does |
| --- | --- |
| `ov stack config view` | The configuration the stack runs with. |
| `ov stack config get <key>` | One value (model key, flag, alias or env key). |
| `ov stack config set k=v …` | Change values, recreating only the services that read them. `--dry-run` shows the plan. |
| `ov stack config unset <key>` | Back to the default. |
| `ov stack config edit` | Edit the configuration in `$EDITOR`. |
| `ov stack render` | Render `config/` into the runtime tree (Community). `--this-node` for the local node. |

## Modules, agents and ports

See [Modules and agents](operate/modules.md).

| Command | What it does |
| --- | --- |
| `ov stack module ls` | Modules on/off and what each requires. |
| `ov stack module add <id>` / `rm <id>` | Turn a module on or off, live; the data services follow. |
| `ov stack agent ls` | The agents of the stack, each with its state and image. |
| `ov stack agent enable <name>` / `disable <name>` | Turn an agent on or off, live. `--dry-run` prints the commands. |
| `ov stack ports` | The ports the stack needs (read live from Docker on a local stack). |
| `ov stack check-ports` | Verify the inbound ports of a node actually arrive. Exit `8` on failure. |

## Nodes of a multi-node stack

An Elastic or HA stack is deployed on one machine; every other machine joins it. See [Scaling](operate/scaling.md).

| Command | What it does |
| --- | --- |
| `ov stack join-info [--format env\|json] [--wait]` | On the deployed node: print the address and token another machine needs to join. |
| `ov stack join --this-node --as master\|media` | On the joining machine (as root): enrol it in the stack. |
| `ov stack join --ssh [user@]host --as master\|media` | From the stack's directory: join a machine over SSH. `--skip-port-check` skips the port check. |
| `ov stack kubeconfig --this-node [--server <address>]` | On the deployed node: print the cluster's administrative kubeconfig. |
| `ov stack leave --this-node [--drain] [--uninstall]` | On a joined node: take it out of the stack. `--drain` leaves gracefully (media nodes); `--uninstall` removes the agent. |

## Recover a stack directory

### `ov stack import [NAME]`

Adopts a deployed stack into the directory, so every verb works afterwards. See [Operate from another machine](operate/remote.md).

| Flag | Source |
| --- | --- |
| `--this-node` | The stack on this machine. |
| `--ssh [user@]host` | A node over SSH (`--ssh-key`, `--ssh-port`). |
| `--kubeconfig <path>` | A PRO stack, from its cluster credential (`--kube-context`). |
| `-f <file>` | A description document. |
| `--cloud <cloud> --stack-name <name>` | A stack deployed with `--remote-state`, from its cloud record (infrastructure included). `--openvidu-pro-license` and `--param` supply the secrets the record leaves out. |
| `--replace` | Overwrite the stack recorded in this directory. |

## Teardown

### `ov stack destroy`

Tears the deployment down and removes the directory's record. See [Destroy](operate/destroy.md).

| Flag | Purpose |
| --- | --- |
| `--delete-data` / `--keep-data` | What becomes of the data and recordings (one is **required** on a cloud). |
| `--delete-config` | Also remove the deployment directory (server/local). Implies `--delete-data`. |
| `--keep-context` | Keep the directory's record after teardown. |
| `--keep-infrastructure` | Cloud: tear the deployment down but keep the machines running. |

## Housekeeping

`ov version` · `ov help [command]` · `ov completion bash|zsh|fish|powershell`.
