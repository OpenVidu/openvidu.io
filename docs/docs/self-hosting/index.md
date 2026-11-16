---
title: "Self-host OpenVidu anywhere with one CLI"
description: "Self-host OpenVidu on your laptop, your own servers or five clouds, from one server to a fault-tolerant cluster, deployed and operated with one CLI."
page_features:
  - terminalrecording
hide:
  - toc
---

# Self-host OpenVidu anywhere

**Run OpenVidu on infrastructure you control**: on your laptop, on your own servers or on AWS, Azure, Google Cloud, Oracle Cloud and DigitalOcean, from a single server to a fault-tolerant cluster. One tool, the [OpenVidu CLI](openvidu-cli.md) (`ov`), deploys it and operates it, with the same commands wherever it runs.

[Install the OpenVidu CLI](openvidu-cli.md#install-the-openvidu-cli){ .md-button .md-button--primary } [Compare deployment types](deployment-types.md){ .md-button }

## Choose your deployment

<div class="grid cards two-cols" markdown>

-   :material-laptop:{ .lg .middle } **Local**

    ---

    OpenVidu on your machine with Docker Compose, in either edition, with certificates that work across your network.

    **For** developing and testing your application.

    [:octicons-arrow-right-24: Run OpenVidu locally](local.md)

-   :material-server:{ .lg .middle } **Single Node** **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } **PRO**{ .openvidu-tag .openvidu-pro-tag }

    ---

    Every service on one server, ready for production. PRO adds **2x performance** and **advanced observability**.

    **For** a medium, steady load: hundreds of participants on a powerful server.

    [:octicons-arrow-right-24: Deploy Single Node](single-node/index.md)

-   :material-server-network:{ .lg .middle } **Elastic** **PRO**{ .openvidu-tag .openvidu-pro-tag }

    ---

    A master node and a cluster of media nodes that grows and shrinks with your rooms.

    **For** applications whose load changes and keeps growing.

    [:octicons-arrow-right-24: Deploy Elastic](elastic/index.md)

-   :material-shield-check:{ .lg .middle } **High Availability** **PRO**{ .openvidu-tag .openvidu-pro-tag }

    ---

    Four master nodes and a cluster of media nodes: everything Elastic does, plus **fault tolerance** in every service.

    **For** services that must keep running when a node fails.

    [:octicons-arrow-right-24: Deploy High Availability](ha/index.md)

</div>

## Runs where you do

<div class="grid cards three-cols" markdown>

-   :material-laptop:{ .lg .middle } **Your laptop**

    Linux with Docker. On Windows and macOS, a Docker Compose project runs it on Docker Desktop.

    [Local](local.md)

-   :material-server:{ .lg .middle } **Your own servers**

    Over SSH, or on the server itself.

    [Single&nbsp;Node](single-node/on-premises/install.md) · [Elastic](elastic/on-premises/install.md) · [High&nbsp;Availability](ha/on-premises/index.md)

-   :material-aws:{ .lg .middle } **AWS**

    CloudFormation, with your `aws` CLI.

    [Single&nbsp;Node](single-node/aws/install.md) · [Elastic](elastic/aws/install.md) · [High&nbsp;Availability](ha/aws/install.md)

-   :material-microsoft-azure:{ .lg .middle } **Azure**

    Bicep, with your `az` CLI.

    [Single&nbsp;Node](single-node/azure/install.md) · [Elastic](elastic/azure/install.md) · [High&nbsp;Availability](ha/azure/install.md)

-   :material-google-cloud:{ .lg .middle } **Google Cloud**

    Terraform, with your `gcloud` sign-in.

    [Single&nbsp;Node](single-node/gcp/install.md) · [Elastic](elastic/gcp/install.md) · [High&nbsp;Availability](ha/gcp/install.md)

-   :custom-oracle-cloud-infrastructure:{ .lg .middle } **Oracle Cloud**

    Terraform, with your `oci` CLI.

    [Single&nbsp;Node](single-node/oracle/install.md) · [Elastic](elastic/oracle/install.md) · [High&nbsp;Availability](ha/oracle/install.md)

-   :material-digital-ocean:{ .lg .middle } **DigitalOcean**

    Terraform, with your API token.

    [Single&nbsp;Node](single-node/digitalocean/install.md) · [Elastic](elastic/digitalocean/install.md) · [High&nbsp;Availability](ha/digitalocean/install.md)

</div>

On a cloud, `ov` creates the machines from the infrastructure template built into it, with your own cloud tools and credentials, and the machines deploy OpenVidu themselves. Recordings and OpenVidu Meet data go to the cloud's object storage, so they outlive the machines.

## One CLI, from the first deploy to the last

Each deployment, a **stack**, lives in its own directory, and every `ov stack` command works on the stack of the directory you run it from. Every deploy runs in one of two modes:

- **Auto** runs it for you. On a cloud, `ov` uses your own cloud tools, and shows its plan and asks once before creating anything.
- **Assisted** runs nothing. `ov` prints the exact commands for you to review and run; on a cloud, the same `ov stack deploy` then finds the machines and finishes the job.

Then one command for each task, from that directory:

```bash
mkdir openvidu && cd openvidu
ov stack deploy openvidu --cloud aws --aws-region us-east-1 \
  --edition pro --openvidu-pro-license <your-license> --deployment-type elastic \
  --certificate-type letsencrypt --mode auto       # or --mode assisted

ov stack status                       # the state of every service and node
ov stack config get livekit-api-key   # the credentials your application connects with
ov stack update                       # bring the stack to this ov's version
ov stack destroy --delete-data        # take it down (--keep-data keeps it for a redeploy)
```

`ov stack config set` changes the running configuration and recreates only what reads it, `ov stack module` turns features on and off live, and `ov stack logs` shows every service in one stream. [The OpenVidu CLI](openvidu-cli.md#command-reference) lists every command.

## See it in action

A real run from the end-to-end tests of `ov`: OpenVidu Elastic deployed on AWS in auto mode, checked, scaled from one media node to two with a redeploy, and destroyed. **Edited** cuts the long waits; **Full real time** shows how long each step really takes.

<div class="ov-rec" data-rec="aws-elastic-auto"></div>

Every cloud installation guide has the recordings of its own deployment, in auto and assisted mode.

## Get started

<div class="grid cards" markdown>

-   :material-numeric-1-circle:{ .lg .middle } **Install `ov`**

    ---

    A single static binary for Linux, on amd64 and arm64, checked against the release's checksums.

    [:octicons-arrow-right-24: Install the OpenVidu CLI](openvidu-cli.md#install-the-openvidu-cli)

-   :material-numeric-2-circle:{ .lg .middle } **Pick a deployment type**

    ---

    Editions, servers and features of the four, side by side, and where each one runs.

    [:octicons-arrow-right-24: Compare deployment types](deployment-types.md)

-   :material-numeric-3-circle:{ .lg .middle } **Deploy it**

    ---

    Follow the guide for your deployment type and your servers or cloud. Single Node PRO, Elastic and High Availability need a license: [create an OpenVidu account :fontawesome-solid-external-link:{.external-link-icon}](../../account.md){:target="_blank"} for a 15-day free trial.

    [:octicons-arrow-right-24: See the pricing](../../pricing.md)

</div>
