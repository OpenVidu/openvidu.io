# OpenVidu Single Node PRO on Oracle Cloud Infrastructure — Step-by-step Guide

This page explains how to create a VM in Oracle Cloud Infrastructure (OCI), configure networking, and prepare it for OpenVidu Single Node PRO. Installing, administering, and upgrading OpenVidu Single Node PRO itself is covered in the On-Premises documentation.

## Overview / prerequisites

- OCI account with permission to create compute instances and networking resources.

______________________________________________________________________

## 1. Create the VM (compute instance)

1. Log in to your [**Oracle Cloud Infrastructure**](https://cloud.oracle.com/) account.

1. Search for **Instances** and open it, then click *"Create instance"*.

1. Set a name for the instance (for example, `openvidu-singlenode`), or keep the default name.

1. Change the image to Ubuntu *"Canonical Ubuntu 24.04"*.

1. Select the shape for your OpenVidu server. We recommend **1 OCPU or more and at least 4 GB of RAM** for OpenVidu to run correctly. Then click *"Next"*.

   > **Note**
   >
   > You can also use ARM-based instances. OpenVidu supports ARM, and the [**Always Free-eligible**](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) tier includes an ARM instance at no cost.

1. In the **Security** tab, keep the default options and click *"Next"*.

1. Create a new `VNIC` with a new `virtual cloud network` and a new `public subnet`.

1. Scroll down and download the private key for the new instance so that you can connect via SSH. Then click *"Next"*.

1. In the **Storage** tab, select *"Specify a custom boot volume size"* and set it to **100 GB** instead of 50 GB. You can keep 50 GB, but OpenVidu may fail due to insufficient disk space. Then click *"Next"*.

1. Review the configuration and click *"Create"*.

______________________________________________________________________

## 2. Attach a public IP address to the instance

1. Open the instance details and go to the **VNIC** resource, then to the *"Networking"* tab.
1. Open the *"IP administration"* tab. In the row of the existing IPv4 address, click the three dots menu and select *"Edit"*.
1. Select *"Ephemeral public IP"* and click *"Update"*.

______________________________________________________________________

## 3. Port rules in the network security lists

OpenVidu and WebRTC require specific inbound rules on the instance network security (OCI NSG or subnet security list) and on the instance firewall (configured later).

The [minimum inbound ports to allow](https://openvidu.io/3.5/docs/self-hosting/single-node-pro/on-premises/install/#port-rules) must be included in the NSG rules.

1. From the instance *"Details"* page, click the *"Virtual cloud network"* resource.
1. Go to the *"Security"* tab and click the default security list.
1. In the *"Security Rules"* tab, add the following **Ingress rules**.

> **Ingress Rules**

______________________________________________________________________

## 4. SSH access, OpenVidu installation, and firewall rules

> **Warning**
>
> Open the required ports before installing OpenVidu so you avoid connectivity issues.

1. SSH into the instance:

```bash
ssh -i private_key_downloaded.key ubuntu@PUBLIC_IP
sudo apt update && sudo apt upgrade -y
```

1. Install and start the `firewall-cmd` tool:

```bash
sudo apt install firewalld -y
sudo systemctl enable firewalld
sudo systemctl start firewalld
```

1. Clean the existing `iptables` rules, accept all inputs, disable `iptables` persistence at startup, and restart the network service if required:

```bash
sudo iptables -F
sudo iptables -P INPUT ACCEPT
sudo systemctl disable netfilter-persistent
```

1. Add the required firewall rules:

```bash
firewall-cmd --add-port=80/tcp
firewall-cmd --permanent --add-port=80/tcp

firewall-cmd --add-port=443/tcp
firewall-cmd --permanent --add-port=443/tcp

firewall-cmd --add-port=443/udp
firewall-cmd --permanent --add-port=443/udp

firewall-cmd --add-port=1935/tcp
firewall-cmd --permanent --add-port=1935/tcp

firewall-cmd --add-port=7881/tcp
firewall-cmd --permanent --add-port=7881/tcp

firewall-cmd --add-port=7885/udp
firewall-cmd --permanent --add-port=7885/udp

firewall-cmd --add-port=9000/tcp
firewall-cmd --permanent --add-port=9000/tcp

firewall-cmd --add-port=50000-60000/udp
firewall-cmd --permanent --add-port=50000-60000/udp
```

1. Apply the rules and verify that they are correctly configured:

```bash
firewall-cmd --reload
firewall-cmd --runtime-to-permanent

firewall-cmd --list-all
```

1. Follow the [On-Premises install instructions](https://openvidu.io/3.5/docs/self-hosting/single-node-pro/on-premises/install/index.md) to install OpenVidu PRO on the instance.

______________________________________________________________________

## 5. Administration and upgrade

- For administration of this OpenVidu Single Node PRO deployment, see the [On-Premises administration section](https://openvidu.io/3.5/docs/self-hosting/single-node-pro/on-premises/admin/index.md).
- To upgrade OpenVidu PRO, see the [On-Premises upgrade section](https://openvidu.io/3.5/docs/self-hosting/single-node-pro/on-premises/upgrade/index.md).
