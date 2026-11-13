---
title: "The OpenVidu CLI"
description: "Install the OpenVidu CLI that deploys and operates OpenVidu, and look up its commands, flags, exit codes, remote state and the fixes for common problems."
---

# The OpenVidu CLI

The **OpenVidu CLI** (`ov`) deploys and operates OpenVidu: locally, on your own servers and on AWS, Azure, Google Cloud, Oracle Cloud and DigitalOcean. One tool covers the whole life of a deployment: create it, check it, change its configuration, turn features on and off while it runs, add and remove nodes, update it and take it down. [How OpenVidu is deployed](deployment-types.md#how-openvidu-is-deployed) explains the model behind it (one stack per directory, auto and assisted modes, COMMUNITY and PRO); each deployment guide shows it at work.

This page covers the tool itself: how to install it, its commands at a glance, its exit codes, how a cloud stack is kept on its cloud, and the fixes for the most common problems. `ov help stack <command>` is the full reference of each command's flags.

## Install the OpenVidu CLI { #install-the-openvidu-cli }

The OpenVidu CLI is a single static binary, `ov`, published for Linux on **amd64** (x86_64) and **arm64** (aarch64).

### Requirements

- A Linux machine (macOS and Windows are not supported yet). It can be your workstation or the server you deploy on.
- `curl`, `gunzip` and `sha256sum`, which every common distribution ships.
- Depending on where you deploy:
    - **Local**: [Docker :fontawesome-solid-external-link:{.external-link-icon}](https://docs.docker.com/engine/install/){:target="_blank"} with the Compose plugin.
    - **On premises**: SSH access to your servers. `ov` installs whatever else the servers need.
    - **A cloud**: that cloud's own CLI, authenticated. Each cloud's installation guide lists it.

### Download and verify

Every release publishes the binaries and a `SHA256SUMS` file at `https://get.openvidu.io/cli/<version>/`. A published version never changes.

```bash
OV_VERSION=3.10.0
ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
curl -fsSLO https://get.openvidu.io/cli/${OV_VERSION}/ov_linux_${ARCH}.gz
curl -fsSLO https://get.openvidu.io/cli/${OV_VERSION}/SHA256SUMS
sha256sum --check --ignore-missing SHA256SUMS
```

The check must print `OK` (or your locale's word for it) for the file you downloaded:

```console
$ sha256sum --check --ignore-missing SHA256SUMS
ov_linux_amd64.gz: OK
```

### Install

```bash
gunzip ov_linux_${ARCH}.gz
sudo install -m 0755 ov_linux_${ARCH} /usr/local/bin/ov
```

Check that it runs: `ov version` prints the version you downloaded.

```console
$ ov version
ov 3.10.0
```

The version of `ov` matters: **a release of `ov` deploys the same release of OpenVidu**. `ov` X.Y.Z deploys OpenVidu X.Y.Z, and the cloud machines it creates download that same build. To deploy or update to another version, use the `ov` of that version.

### Shell completion

```bash
ov completion bash | sudo tee /etc/bash_completion.d/ov > /dev/null
```

`ov completion` also generates scripts for `zsh`, `fish` and `powershell`.

### Getting help

`ov help stack` lists the commands, and `ov help stack <command>` prints every flag of one of them. The [commands](#command-reference) below link to the guides that use them.

### Files `ov` keeps on your machine { #files-ov-keeps-on-your-machine }

| File | What it holds |
| --- | --- |
| `.openvidu/` in each stack directory | The state of that stack: how to reach it, the template and variables applied on a cloud, and its secrets. Keep it private. |
| `~/.config/openvidu/known_hosts` (or `$OV_KNOWN_HOSTS`) | The SSH host keys of the machines `ov` has connected to, separate from your own `known_hosts`. A machine is trusted on the first connection; a different key later stops the command before anything runs. |
| `~/.cache/openvidu/image-sizes.json` | Image sizes read for an update's disk check. |

## Global flags { #global-flags }

Every `ov stack` command operates on **the stack in a directory**: the current one, or the one `--dir` names.

| Flag | Meaning |
| --- | --- |
| `--dir <path>` | Stack directory to operate on (default `.`). Its state lives in `<dir>/.openvidu`. |
| `-o, --output <fmt>` | `table` (default), `json`, `yaml`, `wide`, `name`, plus `jsonpath=<expr>` and `go-template=<expr>` for scripting. |
| `--non-interactive` | Never prompt; a missing required value is an error. |
| `-y, --yes` | Assume "yes" for confirmations. It never answers what `destroy` must be told with `--keep-data` or `--delete-data`. |
| `--dry-run` | Print what would happen; change nothing. A command that cannot preview refuses the flag (exit `2`); preview a deploy with `--mode assisted` or `ov stack plan`. |
| `-v, --verbose` / `--debug` | More detail: `-v` adds each step's output and each service's instances in `status`; `--debug` adds the commands themselves. |
| `-h, --help` | Help. |
| `-V, --cli-version` | Print the CLI version. |

## Exit codes { #exit-codes }

| Code | Meaning |
| :---: | --- |
| `0` | Success |
| `1` | Error |
| `2` | Usage error |
| `3` | No stack in the directory |
| `4` | Configuration validation failed |
| `5` | Plan not empty (`plan --detailed-exitcode`), or `config file apply\|edit --dry-run` would change something |
| `6` | A deploy or join stopped before touching the node: a required port does not reach it |
| `7` | A configuration document changed since it was read (`config file apply` without `--force`) |
| `8` | `stack test` failed, or `stack check-ports` found a required port failing |
| `9` | An update stopped before touching the node: a filesystem there lacks the space it needs |
| `10` | A cloud deploy, destroy or import stopped before touching the cloud: a tool is missing on this machine, the cloud's CLI has no session, or the region's quota cannot hold the stack |

## Commands { #command-reference }

Every `ov stack` command works on the stack of the current directory (or the one `--dir` names). This is the map; `ov help stack <command>` lists every flag, and the linked guides show each command at work.

| Command | What it does | Guide |
| --- | --- | --- |
| `ov stack deploy [NAME]` | Create the stack, or apply a changed spec to it. There is no wizard: a missing required value fails and names its flag. `--environment`, `--edition`, `--deployment-type`, `--ssh`/`--this-node` or `--cloud`, and `--mode auto\|assisted` say what and where. | [Local](local.md), [on premises](single-node/on-premises/install.md), [AWS](single-node/aws/install.md), [Azure](single-node/azure/install.md), [Google Cloud](single-node/gcp/install.md), [Oracle Cloud](single-node/oracle/install.md), [DigitalOcean](single-node/digitalocean/install.md) |
| `ov stack plan` | Preview a deploy or a configuration change. | [Preview a change](configuration/changing-config.md#preview-a-change) |
| `ov stack update [NAME]` | Bring a Community server or a PRO stack to this `ov`'s version, rolling back on failure. With `--ssh`, convert an `install.sh` 3.9.0 deployment. | [Upgrade](single-node/upgrade.md) |
| `ov stack status [--wait]` · `describe` · `test` · `logs` | Check the stack: the state of each service and node, its record and endpoints, an active health check, the logs. | [Administration](single-node/on-premises/admin.md#status) |
| `ov stack start` · `stop` · `restart` | Control the whole stack. | [Administration](single-node/on-premises/admin.md#status) |
| `ov stack config view\|get\|set\|unset\|edit` · `config file …` | Read and change the running configuration, recreating only what reads a changed value. | [Changing the configuration](configuration/changing-config.md) |
| `ov stack module ls\|add\|rm` · `agent ls\|enable\|disable` | Turn modules and agents on and off, live. | [Modules](how-to-guides/enable-disable-modules.md) |
| `ov stack check-ports` · `ports` | Verify that the node's inbound ports really reach it; list a local stack's host ports. | [Check the ports](single-node/on-premises/install.md#check-the-ports) |
| `ov stack join` · `join-info` · `leave --this-node` | Add a node to an Elastic or High Availability stack; take a media node out. | [Elastic](elastic/on-premises/install.md), [administration](elastic/on-premises/admin.md#take-a-node-out) |
| `ov stack export` · `import` | Print the stack's description (secrets masked); adopt a stack into a directory. | [Operate from another machine](single-node/on-premises/admin.md#operate-from-another-machine) |
| `ov stack destroy --keep-data\|--delete-data` | Tear the stack down. One of the two flags is required: `--keep-data` leaves its data, configuration and credentials so the same `ov stack deploy` brings it back; `--delete-data` leaves nothing. | [Destroy](single-node/on-premises/admin.md#destroy) |
| `ov version` · `ov help` · `ov completion` | Housekeeping. | |

## Remote state { #remote-state }

By default everything that drives a cloud stack stays in its directory: the Terraform state (on the clouds that use Terraform), the stack's record and the SSH private key. If you lose the directory, you can still import the stack and administer OpenVidu on it (`ov stack import --ssh` to the server or to a master node), but `ov` can no longer change or delete its machines.

`--remote-state` on the deploy also keeps the stack on its cloud, so any machine with credentials for that cloud can take it over with `ov stack import --cloud <cloud> --stack-name openvidu-<name>` (the name on the deploy's `record:` line). From then on, `ov stack status`, `ov stack deploy <name> --cloud <cloud> --param …` and `ov stack destroy` work there as they did in the directory that deployed the stack (a destroy from the imported directory deletes the machines too).

| Where it is kept | AWS | Azure | Google Cloud, Oracle Cloud, DigitalOcean |
| --- | --- | --- | --- |
| **Terraform state** | (CloudFormation; no state file) | (Bicep; no state file) | a dedicated bucket: `<project>-<stack>-<hash>-terraform-state` on Google Cloud, `<stack>-<8 hex>-terraform-state` on Oracle Cloud and DigitalOcean |
| **The record** (infrastructure, no secrets) | the template bucket (`<stack>/registry/`) | a Blob container (`openvidu-registry`) of a storage account the template creates in the stack's resource group (`ovreg<hash>`) | the state bucket (`openvidu/registry/`) |
| **The machines' SSH private key** | a Secrets Manager secret (`openvidu/<stack>/ssh-private-key`) | the stack's Key Vault (`OPENVIDU-SSH-PRIVATE-KEY`) | in the Terraform state |

A PRO stack is imported with `--openvidu-pro-license`. On Azure, where an Azure Policy forbids shared key access to storage accounts, `--remote-state` cannot keep the record: carry the stack with `ov stack export --bundle --out <file>` and `ov stack import -f <file>` instead. `ov stack destroy` deletes everything `--remote-state` kept. Each cloud's administration page shows an import.

## Troubleshooting { #troubleshooting }

The problems specific to one cloud are in the Troubleshooting section of that cloud's installation guides.

### A deploy stopped with exit code 6: a port does not reach the node

Before anything is installed, a remote deploy (and `ov stack join`) checks the node's inbound ports. A **required** port that does not arrive (`443/tcp`, or `22/tcp` for `ov` itself) stops it with exit `6`, and it prints the rule to add for the firewall it found.

```console
$ ov stack deploy web --environment on-premises --ssh ubuntu@172.30.0.96 …
…
checking the inbound ports before installing anything…
  Ports of 172.30.0.96 (Community single node)
  PORT             SCOPE   LEVEL        STATE   TO OPEN
  443/tcp          public  required     closed  sudo ufw allow 443/tcp
  443/udp          public  recommended  open
  80/tcp           public  recommended  open
  50000-60000/udp  public  recommended  open
  7881/tcp         public  recommended  open
  22/tcp           admin   required     open
  1 of 6 checked port(s) do NOT reach the node: 443/tcp
ov: nothing was installed: 443/tcp must reach the node first. ov changes no firewall: add the rules above and deploy again (--skip-port-check deploys anyway)
```

On PRO, the node's own firewall must also let the stack's internal networks (`10.42.0.0/16` and `10.43.0.0/16`) reach it; the check prints the rules to add when it does not.

`ov` never changes a firewall: run the printed fix on the node, then deploy again. A **recommended** port that is not reachable only warns. Run [`ov stack check-ports`](single-node/on-premises/install.md#check-the-ports) at any time for the full report, UDP included.

### No media, but every service is healthy

This is almost always a blocked **UDP** port (`443/udp` or the media range). HTTPS works and the stack looks fine, but media never arrives. Probing a running stack cannot prove this, so stop it for a few seconds, run the full check, and start it again whatever the check reports:

```bash
ov stack stop && ov stack check-ports; ov stack start
```

Keep the `;` before `start`: the check exits non-zero when it finds a problem, and with `&&` the stack would stay stopped. Open the ports the report flags on the node and on any perimeter firewall (cloud security group, router). On a PRO cloud stack of Google Cloud, Oracle Cloud or DigitalOcean, the check prints the `--ssh … --ssh-key …` to add and where that key is.

### Let's Encrypt fails: port 80 must be reachable

`--certificate-type letsencrypt` (and `zerossl`) obtains a certificate over HTTP, so **port 80 must reach the node** from the internet. If it is blocked, certificate issuance fails even though 443 is open. Open `80/tcp`, or use `owncert` to bring your own certificate, or `selfsigned` for a throwaway deployment.

### High Availability never gets ready with Let's Encrypt

On Google Cloud, Azure, Oracle Cloud and DigitalOcean, a High Availability stack sits behind a load balancer that passes TLS through to the masters. Let's Encrypt's HTTP challenge reaches a port 80 that only redirects to HTTPS, so the certificate is never issued and `ov stack status --wait` times out. Deploy High Availability with the default `selfsigned` certificate, or with `owncert` for production. On AWS the load balancer terminates TLS with an ACM certificate, so the question does not arise.

### No domain: the `sslip.io` fallback

A deploy with no `--domain-name` on a machine with a public IPv4 address derives an `sslip.io` name from it (for example `openvidu-40mfas-54-82-78-43.sslip.io`), so Let's Encrypt has a name to certify. On a High Availability cloud stack the name comes from the load balancer's address, except on AWS, where High Availability always needs a domain. This is fine for testing; use your own domain for anything real. A machine without a public IPv4 address, or one you reach by hostname, still needs `--domain-name`.

### A cloud quota blocked the deploy

Where `ov` can read the quota, the deploy stops before touching the cloud (exit `10`); otherwise the error comes from your cloud's CLI. Request a quota increase, pick a smaller size (the size parameters of each installation guide), or deploy in another region.

### A cloud deploy timed out while waiting for OpenVidu

The machines were created but did not finish deploying OpenVidu within the wait window (`--wait-timeout`, default 40 minutes with `--cloud`). The infrastructure already exists, so simply **resume**: it waits and registers the stack, reusing what is there:

```bash
ov stack deploy <name> --cloud <cloud> --mode auto
```

Name the stack; no other flag is needed, because everything is already in `openvidu-stack.yml`.

### A cloud create failed partway

`ov` records the stack's infrastructure in `openvidu-stack.yml` **before** creating anything, so a failed attempt can always be cleaned up from the directory:

```bash
ov stack destroy --delete-data   # or --keep-data
```

### Something is wrong at runtime: read the logs

```bash
ov stack logs --tail 100      # every service, one stream
ov stack logs -f              # follow live
ov stack status               # per-service state and each node's disk
ov stack test                 # active health check
```

### I lost the stack's directory { #lost-the-stack-directory }

The directory holds the handle to the stack, not the stack itself. Recreate it with [`ov stack import`](single-node/on-premises/admin.md#operate-from-another-machine):

- **PRO:** `ov stack import --ssh <user>@<master>` (on High Availability, any of the four masters), or `sudo ov stack import --this-node` on the master itself. The stack holds its own state, so nothing is lost.
- **Community:** `ov stack import --ssh ubuntu@<host> --ssh-key <key>` (rebuilt from the node's files if needed).
- **A cloud stack deployed with `--remote-state`:** `ov stack import --cloud <cloud> --stack-name openvidu-<name>` brings back the infrastructure too, so `ov stack destroy` and `--param` redeploys work again ([Remote state](#remote-state)). Without `--remote-state`, only the deploying directory can drive the machines.
