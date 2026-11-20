---
title: "The OpenVidu CLI"
description: "Install the OpenVidu CLI, the single binary that deploys and operates OpenVidu locally, on your own servers and on five clouds."
---

# The OpenVidu CLI

The **OpenVidu CLI** (`ov`) deploys and operates OpenVidu: locally, on your own servers and on AWS, Azure, Google Cloud, Oracle Cloud and DigitalOcean. Install it on the machine you deploy from. [How OpenVidu is deployed](deployment-types.md#how-openvidu-is-deployed) explains the model behind it, each deployment guide shows the commands that create a stack, and each administration guide the ones that operate it.

## Install the OpenVidu CLI { #install-the-openvidu-cli }

The OpenVidu CLI is a single static binary, `ov`, published for Linux on **amd64** (x86_64) and **arm64** (aarch64).

### Requirements

- A Linux machine (macOS and Windows are not supported yet). It can be your workstation or the server you deploy on.
- `curl`, `gunzip` and `sha256sum`, which every common distribution ships.

What the deployment itself needs (Docker for a local deployment, SSH access to your servers, or a cloud's own CLI) is listed in its guide.

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

`ov help stack` lists the commands, `ov help stack <command>` prints every flag of one of them, and `ov --help` the flags every command takes.

## Next steps

- [Choose a deployment type](deployment-types.md) and follow its installation guide.
- Or try OpenVidu on your own machine first, with a [local deployment](local.md).
