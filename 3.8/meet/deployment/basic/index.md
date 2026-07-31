This section contains the instructions to deploy a production-ready deployment of OpenVidu Meet in a single server.

Info

This guide shows a single-node installation in a Linux machine. To see other deployment options, such as deploying in cloud providers like AWS, Azure, or GCP, or deploying in a multi-node architecture, check the [Other deployment options](#other-deployment-options) section at the end of this page.

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

- Port rules: these inbound ports must be open in your firewall and reachable from the internet.

  | Protocol | Ports         | Source          | Requirement                                                        |
  | -------- | ------------- | --------------- | ------------------------------------------------------------------ |
  | TCP      | 80            | 0.0.0.0/0, ::/0 | Mandatory                                                          |
  | TCP      | 443           | 0.0.0.0/0, ::/0 | Mandatory                                                          |
  | UDP      | 443           | 0.0.0.0/0, ::/0 | Mandatory                                                          |
  | TCP      | 7881          | 0.0.0.0/0, ::/0 | Optional, but recommended for optimal perfomance and media quality |
  | UDP      | 50000 - 60000 | 0.0.0.0/0, ::/0 | Optional, but recommended for optimal perfomance and media quality |

## Installation

Run this command in your server to start the installation wizard:

```bash
sh <(curl -fsSL http://get.openvidu.io/community/singlenode/latest/install_meet.sh)
```

Follow the instructions of the installation wizard. They are self-explanatory, but here is a breakdown:

1. Select **Yes** to continue when prompted after the installation summary:

   Installation summary

1. If you have a domain name, enter it when prompted. If you don't have one, just press **Enter** to continue and the public IP will be used as the domain name, with a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability) certificate issued for it:

   Press Enter

1. The installer will ask you to confirm if you want to proceed with the installation. Select **Yes** to start the installation.

   The installation will begin, downloading the software and configuring your server. Once the installation is complete, you will see this message:

   Installation complete

   You can access OpenVidu Meet in your browser using the URL and credentials shown in the installation completion message.

## Administration

You can manage the OpenVidu Meet installation running simple commands on your server:

```bash
# Start OpenVidu Meet
sudo systemctl start openvidu

# Stop OpenVidu Meet
sudo systemctl stop openvidu

# Restart OpenVidu Meet
sudo systemctl restart openvidu
```

OpenVidu Meet is under the hood an OpenVidu Platform deployment, so you can refer to the [OpenVidu Platform Single Node administration guide](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/index.md) for more advanced management tasks, including:

- [Check the status of services](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/#checking-the-status-of-services)
- [Check logs](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/#checking-logs)
- [Upgrade OpenVidu Meet to a newer version](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/upgrade/index.md)
- [Uninstall OpenVidu Meet](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/#uninstalling-openvidu)

## Other deployment options

This guide has covered the manual installation of OpenVidu Meet as a single-node deployment in a Linux server. Under the hood OpenVidu Meet is an OpenVidu Platform deployment, so there are further deployment options available:

- **Non-interactive installation**: you can run the installation wizard in a non-interactive way, providing all the required parameters in a single command. Check the [Non-interactive installation](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/install/#non-interactive-installation) guide for OpenVidu Platform.

- If you prefer a cloud deployment, choose your provider and follow the corresponding guide:

  - **AWS**: CloudFormation-based deployment using native AWS resources. [AWS deployment](https://openvidu.io/3.8/docs/self-hosting/single-node/aws/install/index.md)
  - **Azure**: ARM-based deployment using native Azure resources. [Azure deployment](https://openvidu.io/3.8/docs/self-hosting/single-node/azure/install/index.md)
  - **GCP**: Terraform-based deployment using native GCP resources. [GCP deployment](https://openvidu.io/3.8/docs/self-hosting/single-node/gcp/install/index.md)
  - **DigitalOcean**: Terraform-based deployment using native DigitalOcean resources. [DigitalOcean deployment](https://openvidu.io/3.8/docs/self-hosting/single-node/digitalocean/install/index.md)
  - **OCI**: Terraform-based deployment using native Oracle Cloud Infrastructure resources. [OCI deployment](https://openvidu.io/3.8/docs/self-hosting/single-node/oracle/install/index.md)

- **Deploy OpenVidu Meet in a multi-node architecture**: there are multi-node deployment options available to make your OpenVidu Meet installation scalable and fault-tolerant. Check out the [Advanced deployments](https://openvidu.io/3.8/meet/deployment/advanced/index.md) section for more information.
