---
title: "Deploy OpenVidu Meet on a single server"
description: "Production deployment of OpenVidu Meet on one Linux server: prerequisites, ports, domain and TLS certificates, and the OpenVidu CLI command."
---

# Deploy OpenVidu Meet on a single server

This section contains the instructions to deploy a production-ready deployment of OpenVidu Meet in a single server.

!!! info

    This guide shows a single-node installation in a Linux machine. To see other deployment options, such as deploying in cloud providers like AWS, Azure, Google Cloud, DigitalOcean or Oracle Cloud, or deploying in a multi-node architecture, check the [Other deployment options](#other-deployment-options) section at the end of this page.

## Prerequisites

### OS

- **Ubuntu** 22.04 or newer.
- User with **root** permissions (via `sudo`).

### Recommended hardware

- At least 4 GB RAM and 4 CPU cores.
- Generous disk space (100 GB recommended), especially if you plan to record your meetings.

### Networking

- A public IP, that doesn't change between restarts (a static IP).
- (Recommended) A domain name (FQDN) pointing to the public IP.
- Port rules: these inbound ports must reach the server from the internet. The OpenVidu CLI checks them before it installs anything, and stops if a required one is closed.

    | Protocol | Ports         | Source          | Requirement                                                                 |
    | -------- | ------------- | --------------- | --------------------------------------------------------------------------- |
    | TCP      | 443           | 0.0.0.0/0, ::/0 | Required                                                                    |
    | TCP      | 22            | your machine    | Required when you deploy from your machine over SSH                         |
    | TCP      | 80            | 0.0.0.0/0, ::/0 | Recommended: Let's Encrypt needs it to obtain the certificate               |
    | UDP      | 443           | 0.0.0.0/0, ::/0 | Recommended for optimal performance and media quality                       |
    | TCP      | 7881          | 0.0.0.0/0, ::/0 | Recommended for optimal performance and media quality                       |
    | UDP      | 50000 - 60000 | 0.0.0.0/0, ::/0 | Recommended for optimal performance and media quality                       |

    The [port rules of OpenVidu Single Node](../../docs/self-hosting/single-node/on-premises/install.md#port-rules) explain each one.

## Installation

OpenVidu Meet is installed with the [OpenVidu CLI](../../docs/self-hosting/openvidu-cli.md) (`ov`), which deploys an OpenVidu Single Node with OpenVidu Meet on. [Install the CLI](../../docs/self-hosting/openvidu-cli.md#install-the-openvidu-cli) on your machine or on the server, then deploy from an empty directory.

From your machine, over SSH:

```bash
mkdir openvidu-meet && cd openvidu-meet
ov stack deploy meet --environment on-premises \
  --ssh ubuntu@<server-ip> --ssh-key ~/.ssh/id_ed25519 \
  --domain-name <your-domain> --certificate-type letsencrypt \
  --mode auto
```

Or on the server itself:

```bash
sudo ov stack deploy meet --environment on-premises --this-node \
  --domain-name <your-domain> --certificate-type letsencrypt
```

Without `--domain-name`, a server with a public IPv4 address gets an `sslip.io` name derived from it, with a Let's Encrypt certificate. The deploy generates every credential, waits until OpenVidu is ready and prints its URL. OpenVidu Meet is served at that URL; the initial administrator is `admin`, and these commands print its password and the API key of the OpenVidu Meet REST API:

```bash
ov stack config get meet-initial-admin-password
ov stack config get meet-initial-api-key
```

The [OpenVidu Single Node installation guide](../../docs/self-hosting/single-node/on-premises/install.md) covers every option: your own certificate, the port check, assisted mode and the PRO edition.

## Administration

The OpenVidu CLI operates the deployment from the directory you deployed it from, or from the server itself (`sudo ov stack …` there):

```bash
ov stack status    # the state of each service
ov stack stop      # stop OpenVidu Meet
ov stack start     # start it again
ov stack restart   # restart it
```

OpenVidu Meet is under the hood an OpenVidu Platform deployment, so you can refer to the [OpenVidu Platform Single Node administration guide](../../docs/self-hosting/single-node/on-premises/admin.md) for more advanced management tasks, including:

- [Check the status of services](../../docs/self-hosting/single-node/on-premises/admin.md#status)
- [Check logs](../../docs/self-hosting/single-node/on-premises/admin.md#logs)
- [Upgrade OpenVidu Meet to a newer version](../../docs/self-hosting/single-node/upgrade.md)
- [Uninstall OpenVidu Meet](../../docs/self-hosting/single-node/on-premises/admin.md#destroy)

## Other deployment options

This guide has covered the installation of OpenVidu Meet as a single-node deployment on a Linux server. Under the hood OpenVidu Meet is an OpenVidu Platform deployment, so there are further deployment options available:

- If you prefer a cloud deployment, choose your provider and follow the corresponding guide:

    - **AWS**: One OpenVidu CLI command creates the machines with a CloudFormation template. [AWS deployment](../../docs/self-hosting/single-node/aws/install.md)
    - **Azure**: One OpenVidu CLI command creates the machines with a Bicep template. [Azure deployment](../../docs/self-hosting/single-node/azure/install.md)
    - **GCP**: One OpenVidu CLI command creates the machines with a Terraform template. [GCP deployment](../../docs/self-hosting/single-node/gcp/install.md)
    - **DigitalOcean**: One OpenVidu CLI command creates the machines with a Terraform template. [DigitalOcean deployment](../../docs/self-hosting/single-node/digitalocean/install.md)
    - **OCI**: One OpenVidu CLI command creates the machines with a Terraform template. [OCI deployment](../../docs/self-hosting/single-node/oracle/install.md)

- **Deploy OpenVidu Meet in a multi-node architecture**: there are multi-node deployment options available to make your OpenVidu Meet installation scalable and fault-tolerant. Check out the [Advanced deployments](./advanced.md) section for more information.
