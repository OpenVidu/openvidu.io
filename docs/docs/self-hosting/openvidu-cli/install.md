---
title: "Install the OpenVidu CLI"
description: "Download the OpenVidu CLI for Linux on amd64 or arm64, verify it against its published checksums and put it on your PATH."
---

# Install the OpenVidu CLI

The OpenVidu CLI is a single static binary, `ov`, published for Linux on **amd64** (x86_64) and **arm64** (aarch64).

## Requirements

- A Linux machine. It can be your workstation or the server you deploy on.
- `curl`, `gunzip` and `sha256sum`, available on every common distribution.
- What each kind of deployment drives:
    - **Local**: [Docker :fontawesome-solid-external-link:{.external-link-icon}](https://docs.docker.com/engine/install/){:target="_blank"} with the Compose plugin.
    - **On premises**: SSH access to your servers. `ov` installs whatever else the servers need.
    - **A cloud**: that cloud's own CLI, authenticated. Each [deployment guide](index.md#where-you-can-deploy) lists it.

## Download and verify

Every release publishes the binaries and a `SHA256SUMS` file at `https://get.openvidu.io/cli/<version>/`. A published version never changes.

```bash
OV_VERSION=3.10.0
ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
curl -fsSLO https://get.openvidu.io/cli/${OV_VERSION}/ov_linux_${ARCH}.gz
curl -fsSLO https://get.openvidu.io/cli/${OV_VERSION}/SHA256SUMS
sha256sum --check --ignore-missing SHA256SUMS
```

The check must print `OK` for the file you downloaded:

```console
$ sha256sum --check --ignore-missing SHA256SUMS
ov_linux_amd64.gz: OK
```

## Install

```bash
gunzip ov_linux_${ARCH}.gz
sudo install -m 0755 ov_linux_${ARCH} /usr/local/bin/ov
```

Check that it runs: `ov version` (or `ov -V`) prints the version you downloaded.

```console
$ ov version
ov 3.10.0
```

The version of `ov` matters: **a release of `ov` deploys the same release of OpenVidu**. `ov` X.Y.Z deploys OpenVidu X.Y.Z, and the cloud machines it creates download that same build. To deploy or update to another version, use the `ov` of that version.

## Shell completion

```bash
ov completion bash | sudo tee /etc/bash_completion.d/ov > /dev/null
```

`ov completion` also generates scripts for `zsh`, `fish` and `powershell`.

## Getting help

`ov help` lists the commands, and `ov help stack <command>` prints every flag of one of them:

```console
$ ov help stack
Usage:
  ov stack <subcommand> [operands] [flags]

Subgroups:
  stack agent    list, enable and disable the stack's agents
  stack config   view and change the stack's configuration
  stack module   list, enable and disable the stack's modules

Subcommands:
  check-ports          check that the inbound ports a stack needs actually arrive
  check-ports-listen   internal: hold this node's ports for `check-ports`
  deploy               deploy a new stack and record it in this directory
  describe             show detailed live information about the stack
  destroy              tear down the deployment (destructive)
  export               serialize the stack's desired state to openvidu-stack.yml
  import               adopt a deployed stack into this directory (this machine, SSH, a kubeconfig, or its record on the cloud)
  join                 join a machine to a running stack as a control-plane or media node
  join-info            print what another machine needs to join this stack (address and token)
  kubeconfig           print the administrative kubeconfig of the stack running on this machine
  leave                take this machine out of the stack it joined (stops its node agent)
  logs                 fetch or follow the stack's logs
  migrate              convert a deployment install.sh 3.9.0 made (Community, a Professional single node, Elastic or HA) into the stack ov deploys
  plan                 preview what a deploy or a config change would do
  ports                show the published Docker ports of the local deployment
  render               render config/ into data/runtime/ (Community on Docker Compose)
  restart              restart the stack (whole stack; per-service not yet supported)
  start                start the stack (whole stack; per-service not yet supported)
  status               show live health/status of the stack
  stop                 stop the stack (whole stack; per-service not yet supported)
  test                 verify the stack (connectivity)
  update               update the stack to this ov's version, keeping your edits to its files

Run 'ov help stack <subcommand>' for more information.
```

The [command reference](reference.md) describes all of them.

## Next steps

Deploy OpenVidu: [locally](deploy/local.md), [on premises](deploy/on-premises.md) or on [AWS](deploy/aws.md), [Azure](deploy/azure.md), [Google Cloud](deploy/gcp.md), [Oracle Cloud](deploy/oracle.md) or [DigitalOcean](deploy/digitalocean.md).
