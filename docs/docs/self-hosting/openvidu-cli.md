---
title: "The OpenVidu CLI"
description: "Install the OpenVidu CLI that deploys and operates OpenVidu, and look up its commands, flags, exit codes, remote state and the fixes for common problems."
---

# The OpenVidu CLI

The **OpenVidu CLI** (`ov`) deploys and operates OpenVidu: locally, on your own servers and on AWS, Azure, Google Cloud, Oracle Cloud and DigitalOcean. One tool covers the whole life of a deployment: create it, check it, change its configuration, turn features on and off while it runs, add and remove nodes, update it and take it down. [How OpenVidu is deployed](deployment-types.md#how-openvidu-is-deployed) explains the model behind it (one stack per directory, auto and assisted modes, COMMUNITY and PRO); each deployment guide shows it at work.

This page is the reference for the tool itself: how to install it, its commands, flags and exit codes, how a cloud stack is kept on its cloud, and the fixes for the most common problems.

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

`ov help stack` lists the commands, and `ov help stack <command>` prints every flag of one of them. The [command reference](#command-reference) below describes all of them.

### Files `ov` keeps on your machine { #files-ov-keeps-on-your-machine }

| File | What it holds |
| --- | --- |
| `.openvidu/` in each stack directory | The state of that stack: how to reach it, the template and variables applied on a cloud, and its secrets. Keep it private. |
| `~/.config/openvidu/known_hosts` (or `$OV_KNOWN_HOSTS`) | The SSH host keys of the machines `ov` has connected to, separate from your own `known_hosts`. A machine is trusted on the first connection; from then on a different key stops the command before anything runs, and the message says how to remove the old key when you know why it changed. A destroy that deletes a cloud stack's machines removes their keys. |
| `~/.cache/openvidu/image-sizes.json` | The size of each image `ov` has read from the registry for an update's disk check, so a later estimate does not use up the registry's pull limit. |

## Global flags { #global-flags }

Every `ov stack` command operates on **the stack in a directory**: the current one, or the one `--dir` names.

| Flag | Meaning |
| --- | --- |
| `--dir <path>` | Stack directory to operate on (default `.`). Its state lives in `<dir>/.openvidu`. A relative path you type resolves against the directory you run `ov` from, unless `--dir` named the stack directory: then against it. |
| `-o, --output <fmt>` | `table` (default), `json`, `yaml`, `wide`, `name`, plus `jsonpath=<expr>` and `go-template=<expr>` for scripting. |
| `--non-interactive` | Never prompt; a missing required value is an error. |
| `-y, --yes` | Assume "yes" for confirmations (for example `destroy`). |
| `--dry-run` | Compute and print what would happen; change nothing. A command that cannot preview rejects the flag (exit `2`) rather than ignoring it: `deploy` without `--cloud` (preview one with `--mode assisted` or `ov stack plan`), `join`, `leave`, `import`, and `export` with `--out`, `--to-stack` or `--gitops`. |
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
| `6` | A deploy or join stopped before touching the node: a required port is closed, or the node's firewall drops the stack's internal networks (PRO) |
| `7` | A configuration document changed since it was read (`config file apply` without `--force`) |
| `8` | `stack test` failed, or `stack check-ports` found a required port failing (or, on PRO, the node's firewall dropping the stack's internal networks) |
| `9` | An update stopped before touching the node: a filesystem there lacks the space it needs |
| `10` | A cloud deploy, destroy or import stopped before touching the cloud: a tool it runs on this machine is missing or too old, the cloud's client has no session, or the cloud's quota in the region cannot hold the stack |

## Command reference { #command-reference }

`ov help stack <command>` prints the authoritative flag list of each command. The guides linked in each section show them at work.

### Deploy, plan and update

**`ov stack deploy [NAME]`** creates the stack described by the configuration and records it in the directory. There is **no wizard**: if a required value is missing, the command fails and names it. See the installation guides: [local](local.md), on premises ([Single Node](single-node/on-premises/install.md), [Elastic](elastic/on-premises/install.md), [High Availability](ha/on-premises/install-nlb.md)), [AWS](single-node/aws/install.md), [Azure](single-node/azure/install.md), [Google Cloud](single-node/gcp/install.md), [Oracle Cloud](single-node/oracle/install.md) and [DigitalOcean](single-node/digitalocean/install.md).

| Flag | Purpose |
| --- | --- |
| `--edition community\|pro` | Which OpenVidu edition (default `community`). PRO needs `--openvidu-pro-license`, except locally. |
| `--environment <where>` | `local`, `on-premises` or a cloud. Where the machines are. |
| `--deployment-type single_node\|elastic\|ha` | The topology. Elastic and High Availability deploy the first master; other nodes `join` it. |
| `--ssh [user@]host` | Deploy to another machine over SSH (`--ssh-user`, `--ssh-key`, `--ssh-port`). |
| `--this-node` | Deploy on the machine `ov` runs on (Linux server only). |
| `--cloud <cloud>` | Create the machines on a cloud first; they deploy OpenVidu themselves. |
| `--mode auto\|assisted` | Run everything, or print the commands for you to run. |
| `--domain-name`, `--certificate-type`, `--owncert-public-key`, … | Shorthand flags, each setting one configuration key. `ov help stack deploy` lists them all. |
| `--modules`, `--lan` / `--no-lan`, `--local-dir`, `--free-ports` | Local only: the module selection, access from your network, where the Compose project goes, and stopping whatever holds the ports. |
| `-f <file>`, `--set key=value`, `--set-secret key=value` | An overlay of `openvidu-stack.yml`, a single key, a secret. |
| `--param Name=Value`, `--remote-state` | A cloud template parameter; also keep the stack's state on the cloud ([Remote state](#remote-state)). |
| `--skip-port-check` | Deploy without the port preflight (locally, that the host ports are free; remotely, that the inbound ports reach the node). |
| `--no-wait`, `--wait-timeout` | Skip or limit the wait for readiness (`5m` by default; `40m` with `--cloud`). |

**`ov stack plan`** previews what a deploy or a configuration change would do, without changing anything. `--detailed-exitcode` exits `5` when the plan is not empty. See [Preview a change](configuration/changing-config.md#preview-a-change).

**`ov stack update [NAME]`** brings a Community server or a PRO stack to the version of this `ov`, merging your edits to its configuration three ways, checking the disk first and rolling back on failure. To update a local stack, deploy it again with the new `ov`. With a node named (`--ssh [user@]host`, or `--this-node` on the node), it converts, once, a deployment that `install.sh` 3.9.0 installed (Community, a PRO single node, Elastic or High Availability) into the stack `ov` deploys, on the same machines, keeping its configuration, certificates and data; `--master-node` and `--media-node` name the other machines of a cluster. See [Upgrade OpenVidu Single Node](single-node/upgrade.md).

### Live operations

All of these operate on the directory's stack, with no arguments. See [Administration](single-node/on-premises/admin.md#status).

| Command | What it does |
| --- | --- |
| `ov stack status [--wait [--joined]]` | The state of each service, and the disk of each node. `--wait` blocks until the stack is ready (`--wait-timeout`, 5 minutes by default). |
| `ov stack describe` | The stack's record, endpoints and configuration summary. |
| `ov stack start` / `stop` / `restart` | Control the whole stack (per-service control is not available yet). |
| `ov stack test` | Active health check; exit `8` on failure. |
| `ov stack logs [SERVICE] [--tail N] [--since …] [-f]` | Fetch or follow the stack's logs. On PRO, `SERVICE` picks one service by the name `ov stack status` shows; on Community and local stacks, read one service's logs with Docker Compose for now. |
| `ov stack export [--out <file>] [--gitops] [--bundle] [--to-stack] [--show-secrets]` | Print `openvidu-stack.yml` with its secrets as `***` (`--show-secrets` prints them; `--out` writes a file of mode `0600`). `--gitops` externalizes the secrets to `secrets://` references; `--bundle` prints the self-contained description `ov stack import -f` reads (`--bundle --out <file>` is the copy to import); `--to-stack` publishes that description on the stack, for `import --ssh`. |

### Configuration

See [How to change OpenVidu configuration](configuration/changing-config.md).

| Command | What it does |
| --- | --- |
| `ov stack config view` | The configuration the stack runs with, secrets as `***`. |
| `ov stack config get <key>` | One value, by its path in `openvidu.yaml` (`domain.name`), model key, flag, alias or old `openvidu.env` name. |
| `ov stack config set k=v …` | Change values, recreating only the services that read them. `--dry-run` shows the plan. |
| `ov stack config unset <key>` | Return a value to its default. |
| `ov stack config edit` | Edit `openvidu.yaml` in `$EDITOR` (secrets as `***` unless `--show-secrets`). |
| `ov stack config file ls` | The stack's configuration documents: `openvidu.yaml` and the service files (`livekit.yaml`, `caddy.yaml`, `agent-<name>.yaml`…). |
| `ov stack config file get <doc>` / `edit <doc>` / `diff <file>` / `apply <file>` | Read, edit, compare or upload one document. `apply` validates it first, restarts only what reads it, and refuses a document changed since you read it (exit `7`) unless `--force`. |
| `ov stack render` | Render `config/` into the runtime tree (Community). `--this-node` for the local node. |

### Modules, agents and ports

See [Enable and disable modules](how-to-guides/enable-disable-modules.md).

| Command | What it does |
| --- | --- |
| `ov stack module ls` | Modules on and off, and what each requires. |
| `ov stack module add <id>` / `rm <id>` | Turn a module on or off, live; the data services follow. |
| `ov stack agent ls` | The agents of the stack, each with its state and image. |
| `ov stack agent enable <name>` / `disable <name>` | Turn an agent on or off, live. `--dry-run` prints the commands. |
| `ov stack ports` | Local stack only: the host ports the deployment publishes, read live from Docker. |
| `ov stack check-ports` | Verify that a node's inbound ports are actually reachable (needs SSH access to the node). Exit `8` on failure. See [Check the ports first](single-node/on-premises/install.md#check-the-ports). |

### Nodes of a multi-node stack

An Elastic or High Availability stack is deployed on one machine; every other machine joins it. See [Elastic administration](elastic/on-premises/admin.md#add-a-media-node).

| Command | What it does |
| --- | --- |
| `ov stack join --ssh [user@]host --as master\|media` | From the stack's directory: join a machine over SSH. `--mode assisted` prints the commands and runs nothing; `--skip-port-check` skips the port check. |
| `ov stack join-info [--format env\|json] [--wait <duration>]` | On the deployed node: print the address and token another machine needs to join. |
| `ov stack join --this-node --as master\|media` | On the joining machine (as root): add it to the stack. `--join-info FILE\|-` reads what `join-info` printed. |
| `ov stack leave --this-node [--drain] [--uninstall]` | On a joined node: take it out of the stack. `--drain` leaves gracefully (media nodes); `--uninstall` removes the node agent. |

### Recover a stack directory: `ov stack import [NAME]`

Adopts a deployed stack into the directory, so every command works afterwards. See [Operate from another machine](single-node/on-premises/admin.md#operate-from-another-machine).

| Flag | Source |
| --- | --- |
| `--this-node` | The stack on this machine. |
| `--ssh [user@]host` | A node over SSH (`--ssh-key`, `--ssh-port`): a Community server, or a master node of a PRO stack (on High Availability, any of the four). |
| `-f <file>` | A description document (what `ov stack export --bundle --out <file>` writes). |
| `--cloud <cloud> --stack-name <name>` | A stack deployed with `--remote-state`, from its cloud record, infrastructure included ([Remote state](#remote-state)). |
| `--replace` | Overwrite the stack recorded in this directory. |

### Teardown: `ov stack destroy`

Tears the deployment down and removes the directory's record. Without `-y` it asks you to type the stack's name. See [Destroy](single-node/on-premises/admin.md#destroy).

| Flag | Purpose |
| --- | --- |
| `--delete-data` / `--keep-data` | What becomes of the data and recordings. `--keep-data` is the default on a COMMUNITY server and locally; on a cloud one of the two is **required**. On an on-premises PRO stack the destroy removes the stack's data: back it up first. |
| `--delete-config` | Also remove the deployment directory: on a server `/opt/openvidu` and its unit, data included; locally the compose and config files, keeping the volumes unless `--delete-data`. |
| `--keep-context` | Keep the directory's record after teardown. |
| `--keep-infrastructure` | Cloud: tear the deployment down but keep the machines running. |

### Housekeeping

`ov version` · `ov help [command]` · `ov completion bash|zsh|fish|powershell`.

## Remote state { #remote-state }

By default everything that drives a cloud stack stays in its directory: the Terraform state (on the clouds that use Terraform), the stack's record and the SSH private key. If you lose the directory, you can still import the stack and administer OpenVidu on it (`ov stack import --ssh` to the server or to a master node), but `ov` can no longer change or delete its machines.

`--remote-state` on the deploy also keeps the stack on its cloud, so any machine with credentials for that cloud can take it over with `ov stack import --cloud <cloud> --stack-name openvidu-<name>` (the name on the deploy's `record:` line). From then on, `ov stack status`, `ov stack deploy <name> --cloud <cloud> --param …` and `ov stack destroy` work there as they did in the directory that deployed the stack (a destroy from the imported directory deletes the machines too).

| Where it is kept | AWS | Azure | Google Cloud, Oracle Cloud, DigitalOcean |
| --- | --- | --- | --- |
| **Terraform state** | (CloudFormation; no state file) | (Bicep; no state file) | a dedicated bucket: `<project>-<stack>-<hash>-terraform-state` on Google Cloud, `<stack>-<8 hex>-terraform-state` on Oracle Cloud and DigitalOcean |
| **The record** (infrastructure, no secrets) | the template bucket (`<stack>/registry/`) | a Blob container (`openvidu-registry`) of a storage account the template creates in the stack's resource group (`ovreg<hash>`) | the state bucket (`openvidu/registry/`) |
| **The SSH private key** `ov` generated | a Secrets Manager secret (`openvidu/<stack>/ssh-private-key`) | the stack's Key Vault (`OPENVIDU-SSH-PRIVATE-KEY`) | in the Terraform state |

On Azure, the record is written with the storage account's key: where an Azure Policy of your organization forbids shared key access, the deploy warns that `--remote-state` cannot keep it, and the way to carry the stack is `ov stack export --bundle --out <file>` and `ov stack import -f <file>`.

A Community stack is imported the same way, with no license: the import takes the SSH private key from where `--remote-state` kept it and operates the stack over SSH. On a PRO stack, without `--openvidu-pro-license` the import stops before registering anything and says which flag is missing; `--mode assisted` prints the reads and runs nothing. A stack deployed **without** `--remote-state` has no record to read: the only way back is the directory that deployed it; `ov stack import --ssh` to the server or to a master node (or `-f` with a copy made by `ov stack export --bundle --out <file>`) adopts OpenVidu, not the machines. `ov stack destroy` deletes everything `--remote-state` kept. Each cloud's administration page shows an import with real output.

## Troubleshooting { #troubleshooting }

The problems specific to one cloud are in the Troubleshooting section of that cloud's installation guides.

### A deploy stopped with exit code 6: a port does not reach the node

Before anything is installed, a remote deploy (and `ov stack join`) checks the node's inbound ports. A **required** port that does not arrive (`443/tcp`, or `22/tcp` for `ov` itself), or the node's firewall dropping the stack's internal networks on PRO, stops the deploy with exit `6`, before anything is installed, and prints the rule to add for the firewall it found.

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

On PRO, the node's own firewall must also let the stack's internal networks (`10.42.0.0/16` and `10.43.0.0/16`) reach it. When it does not, the port check says so before anything is installed:

```text
▶ Check the inbound ports…
…
       ✗ host firewall: the ufw firewall on the node does not let 10.42.0.0/16 and 10.43.0.0/16 reach the node: the pods cannot reach the cluster API, LiveKit or the kubelet, and the deploy does not finish
           sudo ufw allow from 10.42.0.0/16
           sudo ufw allow from 10.43.0.0/16
…
ov: nothing was installed: the pod networks (10.42.0.0/16, 10.43.0.0/16) must reach the node first. ov changes no firewall: add the rules above and deploy again (--skip-port-check deploys anyway)
```

`ov` reads firewalls but never changes them: run the printed fix on the node, then deploy again. A **recommended** port that is not reachable (`443/udp`, `80/tcp`, `7881/tcp` or the media range `50000-60000/udp`) only warns, and the deploy continues; `--skip-port-check` turns the check off. Run [`ov stack check-ports`](single-node/on-premises/install.md#check-the-ports) at any time for the full report: it is the check that verifies UDP, the usual culprit when a stack looks healthy but has no media.

### No media, but every service is healthy

This is almost always a blocked **UDP** port (`443/udp` or the media range). HTTPS works and the stack looks fine, but media never arrives. Probing a running stack cannot prove this, so stop it for a few seconds, run the full check, and start it again whatever the check reports:

```bash
ov stack stop && ov stack check-ports; ov stack start
```

The `;` before `start` matters: the check exits non-zero when it finds a problem, and with `&&` there the stack would stay stopped.

Open the ports the report flags on the node and on any perimeter firewall (cloud security group, router). `check-ports` needs SSH access to the node. A PRO stack on a cloud keeps none in its record: on AWS and Azure the check logs in to the master as `ubuntu` with the key pair `ov` generated, when the directory holds its private half; on the other clouds it exits `2` and prints the command to run, `ov stack check-ports --ssh <user>@<master> --ssh-key <key>`, and where that key is.

### Let's Encrypt fails: port 80 must be reachable

`--certificate-type letsencrypt` (and `zerossl`) obtains a certificate over HTTP, so **port 80 must reach the node** from the internet. If it is blocked, certificate issuance fails even though 443 is open. Open `80/tcp`, or use `owncert` to bring your own certificate, or `selfsigned` for a throwaway deployment.

### High Availability never gets ready with Let's Encrypt

On Google Cloud, Azure, Oracle Cloud and DigitalOcean, a High Availability stack sits behind a load balancer that passes TLS through to the masters. Let's Encrypt's HTTP challenge reaches a port 80 that only redirects to HTTPS, so the certificate is never issued and `ov stack status --wait` times out. Deploy High Availability with the default `selfsigned` certificate, or with `owncert` for production. On AWS the load balancer terminates TLS with an ACM certificate, so the question does not arise.

### No domain: the `sslip.io` fallback

A deploy with no `--domain-name` on a machine with a public IPv4 address derives an `sslip.io` name from it (for example `openvidu-40mfas-54-82-78-43.sslip.io`), so Let's Encrypt has a name to certify. On a High Availability cloud stack the name comes from the load balancer's address. This is fine for testing; use your own domain for anything real. A machine without a public IPv4 address, or one you reach by hostname, still needs `--domain-name`.

### A cloud quota blocked the deploy

When the quota in the region cannot hold the stack, the deploy stops before touching the cloud (exit `10`) on the clouds where `ov` can read it. Otherwise, the cloud refuses to create the machines (an instance-type or vCPU quota, an address or disk limit) and the error comes from your cloud CLI, which `ov` runs as you. Request a quota increase, pick a smaller size with the parameter of your cloud and topology (`--aws-instance-type` on AWS; on the other clouds, the size parameters each installation guide names), or deploy in another region. If a region does not offer the default instance type, `ov` substitutes the same size in another family and says so. A type you chose yourself is never replaced: the deploy stops before creating anything.

### A cloud deploy timed out while waiting for OpenVidu

The machines were created but did not finish deploying OpenVidu within the wait window (`--wait-timeout`, default 40 minutes with `--cloud`). The infrastructure already exists, so simply **resume**: it waits and registers the stack, reusing what is there:

```bash
ov stack deploy <name> --cloud <cloud> --mode auto
```

Name the stack (without the name it would be registered as `openvidu`); no other flag is needed: everything is already in `openvidu-stack.yml`, and a cloud stack that already exists is reused, not created again.

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
