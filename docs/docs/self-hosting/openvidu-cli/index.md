---
title: "Deploy OpenVidu with the OpenVidu CLI"
description: "The OpenVidu CLI deploys and operates OpenVidu on your machine, your servers or five clouds, with one tool and one desired-state file."
page_features: [lazyvideo]
---

# Deploy OpenVidu with the OpenVidu CLI

The **OpenVidu CLI** (`ov`) installs and operates OpenVidu. One tool covers the whole life of a deployment: create it, check it, change its configuration, turn features on and off while it runs, add and remove nodes, and take it down. The same commands work on the OpenVidu running on your laptop and on the one serving your users.

```bash
mkdir my-stack && cd my-stack
ov stack deploy my-stack --cloud aws --aws-region us-east-1   # create the machine; it deploys OpenVidu itself
ov stack status                                               # operate it from this directory
ov stack destroy --delete-data                                # and take it down again
```

!!! info "The OpenVidu CLI and the current installation methods"

    The CLI is a new way to deploy OpenVidu. The existing installation methods ([CloudFormation, Bicep, Terraform and `install.sh`](../deployment-types.md)) are still available and documented in the [Single Node](../single-node/index.md), [Elastic](../elastic/index.md) and [High Availability](../ha/index.md) sections.

## Where you can deploy

| Where OpenVidu runs | Single Node | Elastic | High Availability | Guide |
| --- | :---: | :---: | :---: | --- |
| **Local**: this machine, with Docker, for development | COMMUNITY and PRO | — | — | [Local](deploy/local.md) |
| **On premises**: your own Linux servers, over SSH | COMMUNITY and PRO | PRO | PRO | [On premises](deploy/on-premises.md) |
| **AWS** | COMMUNITY and PRO | PRO | PRO | [AWS](deploy/aws.md) |
| **Azure** | COMMUNITY and PRO | PRO | PRO | [Azure](deploy/azure.md) |
| **Google Cloud** | COMMUNITY and PRO | PRO | PRO | [Google Cloud](deploy/gcp.md) |
| **Oracle Cloud** | COMMUNITY and PRO | PRO | PRO | [Oracle Cloud](deploy/oracle.md) |
| **DigitalOcean** | COMMUNITY and PRO | PRO | PRO | [DigitalOcean](deploy/digitalocean.md) |

The topologies are the ones described in [Deployment types](../deployment-types.md). Elastic and High Availability grow past one machine, so they are OpenVidu PRO only.

## COMMUNITY and PRO: the same commands

`--edition community` (the default) or `--edition pro` is the whole decision. How OpenVidu is installed and run on the machine follows from the edition and is not something you configure:

| | OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } | OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag } |
| --- | --- | --- |
| Deployed with | `ov stack deploy --edition community` | `ov stack deploy --edition pro --openvidu-pro-license <key>` (no license locally) |
| Runs on the server as | Docker Compose and a systemd unit | Kubernetes, with OpenVidu as a Helm release |
| Topologies | Single Node | Single Node, Elastic, High Availability |
| Where the configuration lives | In the node's files (`/opt/openvidu/config/`) | In the cluster (`openvidu.yaml` and the service files, as Kubernetes objects), which any administrator can read |
| Administrators | One client at a time holds the desired state; another one imports a copy | Every client reads the same stack |

A local stack runs on Docker Compose with either edition, so you can develop against OpenVidu PRO without Kubernetes on your laptop, in evaluation mode and with no license. Both editions are deployed, configured and operated with the commands described in this section. The [pricing page](../../../pricing.md) explains what the PRO license includes.

## How a deployment works

### The stack directory

`ov` operates **one stack per directory**. The directory you deploy from becomes the stack: every later command finds the stack in the directory you run it from, with no name and no flags, and `--dir <path>` points at one from anywhere else. Two stacks are two directories.

The directory holds two things:

- **`openvidu-stack.yml`**: the desired state of the deployment. You never have to write it: the deploy flags (`--domain-name`, `--certificate-type`, `--modules`…), `--set key=value` overrides and `-f file.yml` overlays all write into it, and the deploy fills the rest with defaults and **generates every credential the stack needs**. A redeploy from that file reuses the same credentials.
- **`.openvidu/`**: the state the CLI keeps for the stack: how to reach it (SSH key, kubeconfig), the template and variables it applied on a cloud, and its secrets. Keep it private.

### Auto and assisted mode

Every deploy can run in two modes:

- **`--mode auto`** runs the deployment. On a cloud it uses **your own cloud tools** (`aws`, `az`, `terraform`…), already authenticated, and prints every command before running any. It waits for a confirmation; `-y` answers it in advance.
- **`--mode assisted`** runs **nothing**. It writes the same files and prints the same commands for you to review and run yourself. When you are done, `ov stack deploy --cloud <cloud> --mode auto` resumes the deploy: it waits for OpenVidu and registers the stack, with no other flag, because everything is already written in `openvidu-stack.yml`. Until then the directory holds the plan but no stack: `ov stack status` answers `no stack in this directory` (exit `3`).

Both modes print the same commands, so what you review in assisted mode is exactly what auto mode runs.

### Cloud deployments

`--cloud aws|azure|gcp|oracle|digitalocean` makes the deploy create the machines first, from the infrastructure template embedded in the CLI: CloudFormation on AWS, Bicep on Azure and Terraform on Google Cloud, Oracle Cloud and DigitalOcean. Then:

1. **The machines deploy OpenVidu themselves.** Each one downloads the same `ov` build, checks it against the published checksums, and runs `ov stack deploy --this-node` (the first node) or `ov stack join` (every other node). No SSH from your machine is part of the installation.
2. **Your `ov` waits** until OpenVidu answers at its URL.
3. **Your `ov` registers the stack** in your directory: OpenVidu PRO through the cluster credentials (kubeconfig) the stack publishes, OpenVidu COMMUNITY over SSH with the key pair the machine was created with.

From then on, `ov stack status`, `ov stack config`, `ov stack logs` and `ov stack destroy` work from that directory. Recordings and OpenVidu Meet data go to the cloud's object storage (S3, Azure Blob Storage, Cloud Storage, Object Storage or Spaces), so they outlive the machines.

### Remote state

By default everything that drives a cloud stack stays in its directory: the Terraform state, the stack's record and the SSH private key. If you lose the directory, you can still administer the stack itself, but `ov` can no longer change or delete its machines.

`--remote-state` also keeps the stack on its cloud: the Terraform state in a bucket of the stack's own, a **record** of the stack (its infrastructure, no secrets) and the SSH private key in the cloud's secret store. Any machine with credentials for that cloud can then take the stack over with `ov stack import --cloud <cloud> --stack-name <name>`. See [Operate from another machine](operate/remote.md).

## Modules and services

A **module** is a feature of OpenVidu you turn on or off. A **service** is a container (or a Kubernetes workload) that implements it. You choose modules and the deployment works out which services to run:

| Module | What you get | Services it runs |
| --- | --- | --- |
| `livekit-server` | The media server, always on | `ov-livekit-server` |
| `egress` | Recording and streaming out | `ov-egress` |
| `ingress` | RTMP and WHIP ingest | `ov-ingress` |
| `dashboard` | [OpenVidu Dashboard](../production-ready/observability/openvidu-dashboard.md) at `/dashboard` | `ov-dashboard` |
| `meet` | [OpenVidu Meet](../../../meet/index.md) at `/` | `ov-meet` (it brings `egress`) |
| `observability` | Metrics, logs and the [Grafana stack](../production-ready/observability/grafana-stack.md) | `grafana`, `loki`, `prometheus` or `mimir`, `alloy` |
| `v2compatibility` | The OpenVidu 2 REST API, PRO only | `ov-v2compat` |

The data services (`redis`, `mongodb`, `minio`) come up because a module needs them and go away when no module needs them any more. You never name them. [Modules and agents](operate/modules.md) explains how to change the selection on a running stack.

## Next steps

1. [Install the CLI](install.md).
2. Deploy: [locally](deploy/local.md), [on premises](deploy/on-premises.md) or on [AWS](deploy/aws.md), [Azure](deploy/azure.md), [Google Cloud](deploy/gcp.md), [Oracle Cloud](deploy/oracle.md) or [DigitalOcean](deploy/digitalocean.md).
3. Operate it: [status](operate/status.md), [configuration](operate/configuration.md), [modules](operate/modules.md), [scaling](operate/scaling.md), [updates](operate/update.md), [from another machine](operate/remote.md), [destroy](operate/destroy.md).
4. When something goes wrong: [Troubleshooting](troubleshooting.md). Every command: [Command reference](reference.md).
