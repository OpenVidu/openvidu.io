---
title: OpenVidu Single Node PRO installation on Oracle Cloud Infrastructure
description: Learn how to deploy OpenVidu Single Node on Oracle Cloud Infrastructure in two ways
tags:
  - copyclipboard
---

# OpenVidu Single Node <span class="openvidu-tag openvidu-pro-tag" style="font-size: .6em; vertical-align: text-bottom">PRO</span> installation: Oracle Cloud Infrastructure

<div class="provider-chip" markdown>

:custom-oracle-cloud-infrastructure:{ .provider-chip-icon } Oracle Cloud Infrastructure

</div>

This section describes two ways to install OpenVidu Single Node on Oracle Cloud Infrastructure:

* [**Web Console**](#web-console): Can be deployed without installing anything in your machine, but it requires more manual steps and has some limitations. For example, recordings are stored in the machine (instead of OCI Object Storage).
* [**Terraform**](#terraform): More powerful and automated, but it requires Terraform CLI installed on your machine.


## **Web Console**

This page explains how to create a Compute instance in Oracle Cloud Infrastructure (OCI), configure networking, and prepare it for OpenVidu Single Node PRO On Premises. Installing, administrating, and upgrading OpenVidu Single Node PRO itself is covered in the On-Premises documentation.

### Prerequisites

- OCI account with permission to create Compute instances and networking resources.

---

### 1. Create the Compute instance

1. Log in to your [**Oracle Cloud Infrastructure** :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/){:target=_blank} account.
2. Search for **Instances** and open it, then click _"Create instance"_.
    <figure markdown>
    ![OCI create instance](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/create-instance.png){ .svg-img .dark-img }
    </figure>
3. Set a name for the instance (for example, `openvidu-singlenode`), or keep the default name.
4. Change the image to Ubuntu _"Canonical Ubuntu 24.04"_.
    <figure markdown>
    ![Instance select image](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/select-image.png){ .svg-img .dark-img }
    </figure>
5. Select the shape for your OpenVidu server. We recommend **1 OCPU or more and at least 4 GB of RAM** for OpenVidu to run correctly. Then click _"Next"_.

    !!! note
        You can also use ARM-based instances. OpenVidu supports ARM, and the [**Always Free-eligible**](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm){:target="_blank"} tier includes an ARM instance at no cost.
6. In the **Security** tab, keep the default options and click _"Next"_.
7. Create a new `VNIC` with a new `virtual cloud network` and a new `public subnet`.
    <figure markdown>
    ![Network configuration](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/network-config.png){ .svg-img .dark-img }
    </figure>
8. Scroll down and download the private key for the new instance so that you can connect via SSH. Then click _"Next"_.
    <figure markdown>
    ![Download SSH key](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/download-ssh-key.png){ .svg-img .dark-img }
    </figure>
9. In the **Storage** tab, select _"Specify a custom boot volume size"_ and set it to **100 GB** instead of 50 GB. You can keep 50 GB, but OpenVidu may fail due to insufficient disk space. Then click _"Next"_.
    <figure markdown>
    ![Volume size configuration](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/volume-size-config.png){ .svg-img .dark-img }
    </figure>
10. Review the configuration and click _"Create"_.

---

### 2. Attach a public IP address to the instance

1. Open the instance details and go to the **VNIC** resource, then to the _"Networking"_ tab.
    <figure markdown>
    ![VNIC location](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/vnic-location.png){ .svg-img .dark-img }
    </figure>
2. Open the _"IP administration"_ tab. In the row of the existing IPv4 address, click the three-dots menu and select _"Edit"_.
    <figure markdown>
    ![Edit IPv4](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/edit-ipv4.png){ .svg-img .dark-img }
    </figure>
3. Select _"Ephemeral public IP"_ and click _"Update"_.
    <figure markdown>
    ![Create Ephemeral Public IPv4](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ipv4-ephemeral-public-address.png){ .svg-img .dark-img }
    </figure>

---

### 3. Port rules in the network security lists

OpenVidu and WebRTC require specific inbound rules on the instance network security (OCI NSG or subnet security list) and on the instance firewall (configured later).

The [minimum inbound ports to allow](../on-premises/install.md#port-rules) must be included in the security list rules.

1. From the instance _"Details"_ page, click the _"Virtual cloud network"_ resource.
    <figure markdown>
    ![VCN location](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/vcn-location.png){ .svg-img .dark-img }
    </figure>
2. Go to the _"Security"_ tab and click the default security list.
    <figure markdown>
    ![Security tab](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/security-tab.png){ .svg-img .dark-img }
    </figure>
3. In the _"Security Rules"_ tab, add the following **Ingress rules**.

??? "Ingress Rules"
    <figure markdown>
    ![Ingress rule 1](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule1.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 2](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule2.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 3](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule3.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 4](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule4.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 5](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule5.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 6](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule6.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 7](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule7.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 8](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule8.png){ .svg-img .dark-img }
    </figure>

---

### 4. SSH access, OpenVidu installation, and firewall rules

!!! warning
    Open the required ports in the OS firewall before installing OpenVidu to avoid connectivity issues.

1. SSH into the instance:

    ```bash
    ssh -i private_key_downloaded.key ubuntu@PUBLIC_IP
    sudo apt update && sudo apt upgrade -y
    ```

2. Install and start the `firewalld` tool:

    ```bash
    sudo apt install firewalld -y
    sudo systemctl enable firewalld
    sudo systemctl start firewalld
    ```

3. Clean the existing `iptables` rules, accept all inputs, disable `iptables` persistence at startup, and restart the network service if required:

    ```bash
    sudo iptables -F
    sudo iptables -P INPUT ACCEPT
    sudo systemctl disable netfilter-persistent
    ```

4. Add the required firewall rules:

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

5. Apply the rules and verify they are correctly configured:

    ```bash
    firewall-cmd --reload
    firewall-cmd --runtime-to-permanent

    firewall-cmd --list-all
    ```

6. Follow the [On-Premises install instructions](../on-premises/install.md) to install OpenVidu <span class="openvidu-tag openvidu-pro-tag" style="font-size: .6em; vertical-align: text-bottom">PRO</span> on the instance.

    <!-- TODO: Remove this warning when sslip.io rate limiting issue is resolved. Track at https://openvidu.discourse.group/t/deployment-without-domain/5474 -->
    !!! warning "sslip.io rate limiting"
        **sslip.io** is currently experiencing **Let's Encrypt rate limiting issues**, which may prevent SSL certificates from being generated. It is recommended to use your own domain name. Check [this community thread :fontawesome-solid-external-link:{.external-link-icon}](https://openvidu.discourse.group/t/deployment-without-domain/5474){:target="_blank"} for troubleshooting and updates.

---

### 5. Administration and upgrade

- For administration of this OpenVidu Single Node PRO deployment, see the [Administration](./admin.md) section.
- To upgrade OpenVidu, see the [Upgrade](./upgrade.md) section.

## **Terraform**

This section contains instructions for deploying a production-ready OpenVidu Single Node <span class="openvidu-tag openvidu-pro-tag" style="font-size: 12px">PRO</span> deployment on Oracle Cloud Infrastructure. The deployed services are the same as in the [On Premises Single Node installation](../on-premises/install.md), but the process is automated through the Terraform CLI. Additionally, OCI Object Storage is used to store recordings and other persistent data.

### Prerequisites
* You need to have an Oracle Cloud Infrastructure account with the required permissions to create Compute instances, VCNs, and Object Storage buckets.
* You need to have installed [Terraform CLI :fontawesome-solid-external-link:{.external-link-icon}](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli){:target=_blank}.
* You need to have installed Git.

=== "Architecture overview"

    This is what the deployment architecture looks like:

    <figure markdown>
    ![OpenVidu Single Node Oracle Cloud Infrastructure Architecture](../../../../assets/images/self-hosting/single-node/oracle/single-node-oracle-architecture.svg){ .svg-img .dark-img }
    <figcaption>OpenVidu Single Node Oracle Cloud Infrastructure Architecture</figcaption>
    </figure>

### Deployment details

1. Clone the OpenVidu repository with the Terraform files:
    ```bash
    git clone https://github.com/OpenVidu/openvidu-oracle.git
    cd openvidu-oracle/pro/singlenode
    ```
2. Copy **terraform.tfvars.example** to **terraform.tfvars**, update the required parameters with your values, and optionally adjust defaults.
  <details>
    <summary>Information about parameters</summary>

    <h4>Mandatory Parameters</h4>

    <div align="center">
    <table>
    <thead>
    <tr>
    <th>Input Value</th>
    <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <td style="white-space: nowrap;"><code>tenancy_ocid</code></td>
    <td>OCI Tenancy OCID. Required for Object Storage namespace.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>compartment_ocid</code></td>
    <td>OCI Compartment OCID where the resources will be created.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>user_ocid</code></td>
    <td>OCI User OCID used to create Customer Secret Keys for S3-compatible access to Object Storage.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>stackName</code></td>
    <td>Stack name for the OpenVidu deployment.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>openviduLicense</code></td>
    <td>OpenVidu PRO license key. Visit <a href="https://openvidu.io/account" target="_blank">https://openvidu.io/account</a> to get your license.</td>
    </tr>
    </tbody>
    </table>
    </div>

    <h4>Optional Parameters</h4>

    <div align="center">
    <table>
    <thead>
    <tr>
    <th>Input Value</th>
    <th>Default Value</th>
    <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <td style="white-space: nowrap;"><code>region</code></td>
    <td style="white-space: nowrap;"><code>"eu-frankfurt-1"</code></td>
    <td>OCI region where resources will be created.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>availability_domain</code></td>
    <td style="white-space: nowrap;"><code>1</code></td>
    <td>Availability Domain number (1, 2, or 3) to use for resources.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>instanceType</code></td>
    <td style="white-space: nowrap;"><code>"VM.Standard.E4.Flex"</code></td>
    <td>OCI Compute shape for the OpenVidu instance.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>instanceOCPUs</code></td>
    <td style="white-space: nowrap;"><code>4</code></td>
    <td>Number of OCPUs for the instance (only applies to Flex shapes).</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>instanceMemory</code></td>
    <td style="white-space: nowrap;"><code>4</code></td>
    <td>Memory in GB for the instance (only applies to Flex shapes).</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>certificateType</code></td>
    <td style="white-space: nowrap;"><code>"letsencrypt"</code></td>
    <td>Certificate type for OpenVidu deployment. Options: <ul><li><code>selfsigned</code> - Not recommended for production use. Just for testing purposes or development environments. You don't need a FQDN to use this option.</li><li><code>owncert</code> - Valid for production environments. Use your own certificate. You need a FQDN to use this option.</li><li><code>letsencrypt</code> - Valid for production environments. Can be used with or without a FQDN (if no FQDN is provided, a random sslip.io domain will be used).</li></ul>
    <!-- TODO: Remove this warning when sslip.io rate limiting issue is resolved. Track at https://openvidu.discourse.group/t/deployment-without-domain/5474 -->
    <p><strong>Warning:</strong> sslip.io is currently experiencing Let's Encrypt rate limiting issues, which may prevent SSL certificates from being generated. It is recommended to use your own domain name. Check <a href="https://openvidu.discourse.group/t/deployment-without-domain/5474" target="_blank">this community thread</a> for troubleshooting and updates.</p>
    </td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>publicIpAddress</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Previously created Reserved Public IP address for the OpenVidu deployment. Leave blank to generate a new public IP.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>domainName</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Domain name for the OpenVidu deployment. Not mandatory; if not provided, a sslip.io domain will be used instead.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>ownPublicCertificate</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>If certificate type is 'owncert', this parameter will be used to specify the public certificate URL.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>ownPrivateCertificate</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>If certificate type is 'owncert', this parameter will be used to specify the private certificate URL.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>initialMeetAdminPassword</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Initial password for the 'admin' user in OpenVidu Meet. Only alphanumeric characters (A-Z, a-z, 0-9). If not provided, a random password will be generated.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>initialMeetApiKey</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Initial API key for OpenVidu Meet. Only alphanumeric characters (A-Z, a-z, 0-9). If not provided, no API key will be set and the user can set it later from Meet Console.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>bucketName</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Name of the OCI Object Storage bucket for application data and recordings. If empty, a bucket will be created with a default name.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>RTCEngine</code></td>
    <td style="white-space: nowrap;"><code>"pion"</code></td>
    <td>WebRTC media engine to use. Options: <ul><li><code>pion</code> - Default media engine.</li><li><code>mediasoup</code> - Alternative media engine with different performance characteristics.</li></ul></td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>vault_ocid</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>OCI KMS Vault OCID for secrets management. If empty, a new vault will be created.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>key_ocid</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>OCI KMS Key OCID for secrets management. If empty, a new key will be created.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>additionalInstallFlags</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Additional optional flags to pass to the OpenVidu installer (comma-separated, e.g., '--flag1=value, --flag2').</td>
    </tr>
    </tbody>
    </table>
    </div>

  </details>

3. Use the following commands to deploy with Terraform.
  ```bash
  terraform init
  terraform apply
  ```
4. You will see logs appear in the `terraform apply` execution console. Wait for it to finish and display `Apply Complete!`. Now go to [OCI Object Storage :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/object-storage/buckets){:target=_blank} and wait for the SSH key to appear in the bucket you have configured.

    !!! warning
        After downloading the SSH key, it is highly recommended to **DELETE IT** from the bucket. This file is the private key used to access the instance. If exposed, unauthorized users could gain access to the instance.
    <figure markdown>
    ![SSH Key in bucket](../../../../assets/images/self-hosting/single-node/oracle/bucket-ssh-key-pro.png){ .svg-img .dark-img }
    </figure>


5. Give the SSH key the necessary permissions for it to work.

    === "Linux"
        Command in Linux:
        ```
        chmod 600 <PATH_TO_THE_KEY>/openvidu_ssh_key_sn.pem
        ```
    === "Powershell"
        Command in PowerShell:
        ```
        $KeyPath = "<PATH_TO_THE_KEY>" &&
        icacls $KeyPath /inheritance:r &&
        icacls $KeyPath /grant:r "$($env:USERNAME):(R)"
        ```

### Access OpenVidu

To verify that your OpenVidu deployment works correctly, you can check the credentials in the OCI Vault Secrets Manager.

=== "View OpenVidu credentials in the Web"
    1. Navigate to the [OCI Secrets Manager :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/security/secrets){:target="_blank"} in the OCI Console.
    2. Click on the secret you want to view to see its value.
    3. Go down to _"Versions"_ and in the current version click the _"3 dots"_ and then _"View secret contents"_.
        <figure markdown>
        ![View Secret](../../../../assets/images/self-hosting/single-node/oracle/view-secret.png){ .svg-img .dark-img }
        </figure>

        !!! warning
            Click on _"Show decoded Base64 digit"_ to see the true value of the secret.

=== "View OpenVidu credentials in the instance"

    SSH to the instance by running this command from the directory where your SSH key is located:
    ```
    ssh -i openvidu_ssh_key_sn.pem ubuntu@PUBLIC_INSTANCE_IP
    ```

    Then navigate to `/opt/openvidu/config/` and you will find all credentials in the following files:

    - `openvidu.env`
    - `meet.env`

Then open **OPENVIDU_URL** and you will see the OpenVidu Meet interface. Log in with **MEET_INITIAL_ADMIN_PASSWORD** and you will be able to enjoy the features of OpenVidu Meet.

### Configure your application to use the deployment

You may need your OCI credentials to configure your OpenVidu application. You can check these secrets by following these steps ([View OpenVidu credentials in the Web](#view-openvidu-credentials-in-the-web)) or ([View OpenVidu credentials in the instance](#view-openvidu-credentials-in-the-instance)).

Your authentication credentials and the URL to point your applications to are:

--8<-- "shared/self-hosting/oracle-credentials-general.md"

### Troubleshooting initial Oracle Cloud Infrastructure deployment creation

--8<-- "shared/self-hosting/oracle-troubleshooting.md"

3. If everything seems fine, check the [status](../on-premises/admin.md#checking-the-status-of-services) and the [logs](../on-premises/admin.md#checking-logs) of the installed OpenVidu services.

### Configuration and administration

When your **OPENVIDU_URL** is reachable, it means that everything has gone well. Now you can check the [Administration](./admin.md) section to learn how to manage your deployment.
