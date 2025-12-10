---
title: OpenVidu Single Node installation on Google Cloud Platform
description: Learn how to deploy OpenVidu Single Node on Google Cloud Platform using Google Cloud Platform Console
tags:
  - copyclipboard
---

# OpenVidu Single Node on Oracle Cloud Infrastructure — Step by Step Guide

This page documents creating a VM in Oracle Cloud Infrastructure (OCI) and updating network policies. Installing, administrating, and updating OpenVidu Single Node are refered to On Premises install.

## Overview / prerequisites
- OCI account with permission to create compute instances and networking resources.

---

## 1. Create the VM (Compute instance)
1. Login into your [**Oracle Cloud Infrastructure** :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/) account.
2. Search for instances and click on it, then click on _"Create Instance"_.
    <figure markdown>
    ![OCI create instance](../../../../assets/images/self-hosting/single-node/oracle/create-instance.png){ .svg-img .dark-img }
    </figure>
3. Change the name of the instance (e.g., openvidu-singlenode) or leave it as it was, as you prefer.
4. Change the image to Ubuntu _"Canonical Ubuntu 24.04"_.
    <figure markdown>
    ![Instance select image](../../../../assets/images/self-hosting/single-node/oracle/select-image.png){ .svg-img .dark-img }
    </figure>
5. Change the shape for the shape you want in your openvidu server, we recommend to use **1 OCPU or more and at least 4 GB of RAM** for OpenVidu to work correctly, then click on _"Next"_.
6. Don't touch anything in the **Security** tab, just click on _"Next"_.
7. Create a new ´VNIC´ with a new ´virtual cloud network´ and new ´public subnet´.
    <figure markdown>
    ![Network configuration](../../../../assets/images/self-hosting/single-node/oracle/network-config.png){ .svg-img .dark-img }
    </figure>
8. Go down, and download the private key of the new instance to be able to SSH to it. Then click on _"Next"_.
    <figure markdown>
    ![Download SSH key](../../../../assets/images/self-hosting/single-node/oracle/download-ssh-key.png){ .svg-img .dark-img }
    </figure>
9. For the Storage tab select _"Specifiy a custom boot volume size"_ and fill it with 100 GB instead of 50 GB, you can keep it in 50GB but OpenVidu may fail. Then click on _"Next"_.
    <figure markdown>
    ![Volume size configuration](../../../../assets/images/self-hosting/single-node/oracle/volume-size-config.png){ .svg-img .dark-img }
    </figure>
10. Review that everything is fine and click on _"Create"_.
---

## 2. Attaching a Public Ip Address to the instance
1. Go to _"VNIC"_ resource by clicking on the instance details, then into the _"Networking"_ tab.
    <figure markdown>
    ![VNIC location](../../../../assets/images/self-hosting/single-node/oracle/vnic-location.png){ .svg-img .dark-img }
    </figure>
2. Click on _"Ip administration"_ tab and then in the three dots of the only IPv4 address that appears, then click on _"Edit"_.
    <figure markdown>
    ![Edit IPv4](../../../../assets/images/self-hosting/single-node/oracle/edit-ipv4.png){ .svg-img .dark-img }
    </figure>
3. Select _"Ephemeral public IP"_ and click on _"Update"_.
    <figure markdown>
    ![Create Ephemeral Public IPv4](../../../../assets/images/self-hosting/single-node/oracle/ipv4-ephemeral-public-address.png){ .svg-img .dark-img }
    </figure>
---

## 3. Port rules in the Network Security Rules
OpenVidu and WebRTC need the following inbound rules on the instance's network security (OCI NSG or subnet security list) and on the instance firewall (we will check this later).

The [minimum inbound ports to allow](../on-premises/install.md#port-rules) will be included in the NSG rules.

1. Go to the _"Details"_ of the instance and click on the _"Virtual cloud network"_ resource that appears there
    <figure markdown>
    ![VCN location](../../../../assets/images/self-hosting/single-node/oracle/vcn-location.png){ .svg-img .dark-img }
    </figure>
2. Go to _"Security"_ tab and click on the existing default security list
    <figure markdown>
    ![Security tab](../../../../assets/images/self-hosting/single-node/oracle/security-tab.png){ .svg-img .dark-img }
    </figure>
3. In _"Security Rules"_ tab add these **Ingress Rules**.   

??? "Ingress Rules"
    <figure markdown>
    ![Ingress rule 1](../../../../assets/images/self-hosting/single-node/oracle/ingress-rule1.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 2](../../../../assets/images/self-hosting/single-node/oracle/ingress-rule2.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 3](../../../../assets/images/self-hosting/single-node/oracle/ingress-rule3.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 4](../../../../assets/images/self-hosting/single-node/oracle/ingress-rule4.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 5](../../../../assets/images/self-hosting/single-node/oracle/ingress-rule5.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 6](../../../../assets/images/self-hosting/single-node/oracle/ingress-rule6.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 7](../../../../assets/images/self-hosting/single-node/oracle/ingress-rule7.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 8](../../../../assets/images/self-hosting/single-node/oracle/ingress-rule8.png){ .svg-img .dark-img }
    </figure>

---

## 4. SSH to instance, OpenVidu installation and firewall rules.
!!! warning 
    Open ports before installing OpenVidu so you don't have any conflict.
    
1. SSH into the instance:
```
ssh -i private_key_downloaded.key ubuntu@PUBLIC_IP
sudo apt update && sudo apt upgrade -y
```
2. Now add firewall rules in the instance just like before with the security rules. First you need to install firewall-cmd and start it, you can do it with this commands:
```
sudo apt install firewalld -y
systemctl enable firewalld
systemctl start firewalld
```
3. Then clean the iptables rules, accept all inputs, deactivate iptables at start and restart network service:
```
sudo iptables -F
sudo iptables -P INPUT ACCEPT
sudo systemctl disable netfilter-persistent

```
4. The firewall rules are the following:
```
firewall-cmd --add-port=80/tcp
firewall-cmd --permanent --add-port=80/tcp

```
```
firewall-cmd --add-port=443/tcp
firewall-cmd --permanent --add-port=443/tcp

```
```
firewall-cmd --add-port=443/udp
firewall-cmd --permanent --add-port=443/udp

```
```
firewall-cmd --add-port=1935/tcp
firewall-cmd --permanent --add-port=1935/tcp

```
```
firewall-cmd --add-port=7881/tcp
firewall-cmd --permanent --add-port=7881/tcp

```
```
firewall-cmd --add-port=7885/udp
firewall-cmd --permanent --add-port=7885/udp

```
```
firewall-cmd --add-port=9000/tcp
firewall-cmd --permanent --add-port=9000/tcp

```
```
firewall-cmd --add-port=50000-60000/udp
firewall-cmd --permanent --add-port=50000-60000/udp

```

Finish it with the next command to apply the rules and to check if the rules are correct:
```
firewall-cmd --reload
firewall-cmd --runtime-to-permanent

```
```
firewall-cmd --list-all

```
5. Follow the [Install instructions](../on-premises/install.md) for the On-Premises deployment to install OpenVidu in the instance.


---

## 5. Administration and Upgrade
* In [On Premises Administration section](../on-premises/admin.md) you will find all the administration of this OpenVidu Single Node deployment.   
* To upgrade OpenVidu check the [On Premises Upgrade section](../on-premises/upgrade.md).