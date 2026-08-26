# OpenVidu Single Node **PRO** installation: Oracle Cloud Infrastructure

Oracle Cloud Infrastructure

This section describes two ways to install OpenVidu Single Node on Oracle Cloud Infrastructure:

- [**Web Console**](#web-console): Can be deployed without installing anything on your machine, but requires more manual steps and has some limitations. For example, recordings are stored on the machine itself rather than in OCI Object Storage.
- [**Terraform**](#terraform): More powerful and fully automated, but requires the Terraform CLI to be installed on your machine.

## Web Console

This page explains how to create a Compute instance in Oracle Cloud Infrastructure (OCI), configure networking, and prepare it for an OpenVidu Single Node PRO On-Premises installation. Installing, administering, and upgrading OpenVidu Single Node PRO itself is covered in the On-Premises documentation.

### Prerequisites

- An OCI account with permission to create Compute instances and networking resources.

______________________________________________________________________

### 1. Create the Compute instance

1. Log in to your [**Oracle Cloud Infrastructure**](https://cloud.oracle.com/) account.

1. Search for **Instances**, open it, and click *"Create instance"*.

   OCI create instance

1. Set a name for the instance (for example, `openvidu-singlenode`), or keep the default.

1. Change the image to *"Canonical Ubuntu 24.04"*.

   Instance select image

1. Select the shape for your OpenVidu server. We recommend **at least 1 OCPU and 4 GB of RAM** for OpenVidu to run correctly. Then click *"Next"*.

   Note

   ARM-based instances are also supported. OpenVidu supports ARM, and the [**Always Free-eligible**](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) tier includes an ARM instance at no cost.

1. In the **Security** tab, keep the default options and click *"Next"*.

1. Create a new `VNIC` with a new `virtual cloud network` and a new `public subnet`.

   Network configuration

1. Scroll down and download the private key for the instance so you can connect via SSH. Then click *"Next"*.

   Download SSH key

1. In the **Storage** tab, select *"Specify a custom boot volume size"* and set it to **100 GB** instead of the default 50 GB. You can keep 50 GB, but OpenVidu may fail due to insufficient disk space. Then click *"Next"*.

   Volume size configuration

1. Review the configuration and click *"Create"*.

______________________________________________________________________

### 2. Attach a public IP address to the instance

1. Open the instance details, navigate to the **VNIC** resource, and go to the *"Networking"* tab.

   VNIC location

1. Open the *"IP administration"* tab. In the row of the existing IPv4 address, click the three-dots menu and select *"Edit"*.

   Edit IPv4

1. Select *"Ephemeral public IP"* and click *"Update"*.

   Create Ephemeral Public IPv4

______________________________________________________________________

### 3. Port rules in the network security lists

OpenVidu and WebRTC require specific inbound rules on both the instance network security (OCI NSG or subnet security list) and the instance firewall (configured later).

The [minimum inbound ports to allow](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/install/#port-rules) must be included in the security list rules.

1. From the instance *"Details"* page, click the *"Virtual cloud network"* resource.

   VCN location

1. Go to the *"Security"* tab and click the default security list.

   Security tab

1. In the *"Security Rules"* tab, add the following **Ingress rules**.

Ingress Rules

Ingress rule 1 Ingress rule 2 Ingress rule 3 Ingress rule 4 Ingress rule 5 Ingress rule 6 Ingress rule 7 Ingress rule 8

______________________________________________________________________

### 4. SSH access, OpenVidu installation, and firewall rules

Warning

Open the required ports in the OS firewall before installing OpenVidu to avoid connectivity issues.

1. SSH into the instance:

   ```bash
   ssh -i private_key_downloaded.key ubuntu@PUBLIC_IP
   sudo apt update && sudo apt upgrade -y
   ```

1. Install and start the `firewalld` tool:

   ```bash
   sudo apt install firewalld -y
   sudo systemctl enable firewalld
   sudo systemctl start firewalld
   ```

1. Clear the existing `iptables` rules, set the default input policy to ACCEPT, disable `iptables` persistence at startup, and restart the network service if required:

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

1. Apply the rules and verify they are correctly configured:

   ```bash
   firewall-cmd --reload
   firewall-cmd --runtime-to-permanent

   firewall-cmd --list-all
   ```

1. Follow the [On-Premises install instructions](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/install/index.md) to install OpenVidu **PRO** on the instance.

______________________________________________________________________

### 5. Administration and upgrade

- For administration of this OpenVidu Single Node PRO deployment, see the [Administration](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/oracle/admin/index.md) section.
- To upgrade OpenVidu, see the [Upgrade](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/upgrade/index.md) section.

## Terraform

This section contains instructions for deploying a production-ready OpenVidu Single Node **PRO** deployment on Oracle Cloud Infrastructure. The deployed services are the same as in the [On-Premises Single Node installation](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/install/index.md), but the process is fully automated through the Terraform CLI. OCI Object Storage is used to store recordings and other persistent data.

### Prerequisites

- An Oracle Cloud Infrastructure account with the required permissions to create Compute instances, VCNs, and Object Storage buckets.
- The [Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) installed on your machine.
- Git installed on your machine.

**Architecture overview**

The deployment architecture is as follows:

OpenVidu Single Node Oracle Cloud Infrastructure Architecture

### Deployment details

1. Clone the OpenVidu repository containing the Terraform files:

   ```bash
   git clone https://github.com/OpenVidu/openvidu-oracle.git
   git -C openvidu-oracle checkout 3.8.0
   cd openvidu-oracle/pro/singlenode
   ```

1. Copy **`terraform.tfvars.example`** to **`terraform.tfvars`**, update the required parameters with your values, and adjust any optional defaults as needed.

   Information about parameters

   #### Mandatory Parameters

   | Input Value        | Description                                                                                                               |
   | ------------------ | ------------------------------------------------------------------------------------------------------------------------- |
   | `tenancy_ocid`     | OCI Tenancy OCID. Required for the Object Storage namespace.                                                              |
   | `compartment_ocid` | OCI Compartment OCID where resources will be created.                                                                     |
   | `user_ocid`        | OCI User OCID used to create Customer Secret Keys for S3-compatible access to Object Storage.                             |
   | `stackName`        | Stack name for the OpenVidu deployment.                                                                                   |
   | `openviduLicense`  | OpenVidu PRO license key. Visit [your OpenVidu account](https://openvidu.io/account/) to obtain your license. |

   #### Optional Parameters

   | Input Value                | Default Value           | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
   | -------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
   | `region`                   | `"eu-frankfurt-1"`      | OCI region where resources will be created.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
   | `availability_domain`      | `1`                     | Availability Domain number (1, 2, or 3) to use for resources.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
   | `instanceType`             | `"VM.Standard.E4.Flex"` | OCI Compute shape for the OpenVidu instance.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
   | `instanceOCPUs`            | `4`                     | Number of OCPUs for the instance (applies to Flex shapes only).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
   | `instanceMemory`           | `4`                     | Memory in GB for the instance (applies to Flex shapes only).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
   | `certificateType`          | `"letsencrypt"`         | Certificate type for the OpenVidu deployment. Options: - `selfsigned` - Not recommended for production use. Intended for testing or development environments only. A FQDN is not required. - `owncert` - Suitable for production environments. Uses your own certificate. A FQDN is required. - `letsencrypt` - Suitable for production environments. Can be used with or without a FQDN (if no FQDN is provided, the public IP is used as the domain name and a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability) certificate is issued for it). |
   | `domainName`               | `(none)`                | Domain name for the OpenVidu deployment. Optional — if not provided, the public IP is used as the domain name.                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
   | `ownPublicCertificate`     | `(none)`                | If the certificate type is `owncert`, this parameter specifies the public certificate in base64 format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
   | `ownPrivateCertificate`    | `(none)`                | If the certificate type is `owncert`, this parameter specifies the private certificate in base64 format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
   | `initialMeetAdminPassword` | `(none)`                | Initial password for the `admin` user in OpenVidu Meet. Alphanumeric characters, underscores or hyphens only (A-Z, a-z, 0-9, \_, -). If not provided, a random password will be generated.                                                                                                                                                                                                                                                                                                                                                                                           |
   | `initialMeetApiKey`        | `(none)`                | Initial API key for OpenVidu Meet. Alphanumeric characters, underscores or hyphens only (A-Z, a-z, 0-9, \_, -). If not provided, no API key will be set; one can be configured later from the Meet Console.                                                                                                                                                                                                                                                                                                                                                                          |
   | `bucketName`               | `(none)`                | Name of the OCI Object Storage bucket for application data and recordings. If left empty, a bucket will be created with a default name.                                                                                                                                                                                                                                                                                                                                                                                                                                              |
   | `RTCEngine`                | `"pion"`                | WebRTC media engine to use. Options: - `pion` - Default media engine. - `mediasoup` - Alternative media engine with different performance characteristics.                                                                                                                                                                                                                                                                                                                                                                                                                           |
   | `vault_ocid`               | `(none)`                | OCI KMS Vault OCID for secrets management. If left empty, a new vault will be created.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
   | `key_ocid`                 | `(none)`                | OCI KMS Key OCID for secrets management. If left empty, a new key will be created.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
   | `additionalInstallFlags`   | `(none)`                | Additional optional flags to pass to the OpenVidu installer (comma-separated, e.g., `--flag1=value, --flag2`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

1. Deploy with Terraform using the following commands:

   ```bash
   terraform init
   terraform apply
   ```

1. Logs will appear in the `terraform apply` console output. Wait for it to finish and display `Apply Complete!`. Then go to [OCI Object Storage](https://cloud.oracle.com/object-storage/buckets) and wait for the SSH key to appear in your configured bucket.

   Warning

   After downloading the SSH key, it is strongly recommended to **DELETE IT** from the bucket. This file is the private key used to access the instance — if exposed, unauthorized users could gain access.

   SSH Key in bucket

1. Set the correct permissions on the SSH key so it can be used.

   **Linux**

   ```bash
   chmod 600 <PATH_TO_THE_KEY>/openvidu_private_ssh_key_<STACK_NAME>.pem
   ```

   **Powershell**

   ```powershell
   $KeyPath = "<PATH_TO_THE_KEY>" &&
   icacls $KeyPath /inheritance:r &&
   icacls $KeyPath /grant:r "$($env:USERNAME):(R)"
   ```

### Access OpenVidu

To verify that your OpenVidu deployment is working correctly, check the credentials in the OCI Vault Secrets Manager.

**View OpenVidu credentials in the Web**

1. Navigate to the [OCI Secrets Manager](https://cloud.oracle.com/security/secrets) in the OCI Console.

1. Click the secret you want to view.

1. Scroll down to *"Versions"*, click the *"3 dots"* menu next to the current version, and select *"View secret contents"*.

   View Secret

   Warning

   Click *"Show decoded Base64 digit"* to see the actual value of the secret.

**View OpenVidu credentials in the instance**

SSH into the instance by running the following command from the directory where your SSH key is located:

```bash
ssh -i openvidu_private_ssh_key_<STACK_NAME>.pem ubuntu@PUBLIC_INSTANCE_IP
```

Then navigate to `/opt/openvidu/config/` where you will find all credentials in the following files:

- `openvidu.env`
- `meet.env`

Open **OPENVIDU_URL** and you will see the OpenVidu Meet interface.

Log in with **MEET_INITIAL_ADMIN_PASSWORD** to start using OpenVidu Meet.

### Configure your application to use the deployment

To configure your OpenVidu application, you will need your OCI credentials. You can retrieve them by following the steps in [View OpenVidu credentials in the Web](#view-openvidu-credentials-in-the-web) or [View OpenVidu credentials in the instance](#view-openvidu-credentials-in-the-instance).

Your authentication credentials and the URL to point your applications to are:

**OpenVidu Meet**:

- **`OPENVIDU_URL`**: The URL used to access OpenVidu Meet, always `https://yourdomain.example.io/`.
- **`MEET_INITIAL_ADMIN_USER`**: The user account for accessing the OpenVidu Meet Console. Always `admin`.
- **`MEET_INITIAL_ADMIN_PASSWORD`**: The password for accessing the OpenVidu Meet Console.
- **`MEET_INITIAL_API_KEY`**: The API key for using the OpenVidu Meet Embedded and OpenVidu Meet REST API.

Note

`MEET_INITIAL_ADMIN_USER`, `MEET_INITIAL_ADMIN_PASSWORD`, and `MEET_INITIAL_API_KEY` are initial settings only. Changing them here will not affect the deployment — they can only be modified from the Meet Console.

**OpenVidu Platform:**

- **`LIVEKIT_URL`**: The URL used with LiveKit SDKs. This can be either `wss://yourdomain.example.io/` or `https://yourdomain.example.io/`, depending on the client library you are using.
- **`LIVEKIT_API_KEY`**: The API key for LiveKit SDKs.
- **`LIVEKIT_API_SECRET`**: The API secret for LiveKit SDKs.

### Troubleshooting initial Oracle Cloud Infrastructure deployment

If something goes wrong during the initial Oracle Cloud Infrastructure deployment, you will not be able to reach the **OPENVIDU_URL**. This can happen due to a misconfiguration in the parameters, insufficient permissions, or a problem with OCI services. The steps below will help you troubleshoot the issue and identify the root cause:

1. Check whether the instance is running. If it is not, review the output of the `terraform apply` command for any errors.

1. If the instance is running, SSH into it and inspect the logs by running the following command:

   ```text
   cat /var/log/cloud-init-output.log
   ```

   These logs contain detailed information about the Oracle Cloud Infrastructure deployment process.

1. If everything appears to be in order, check the [status](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/admin/#checking-the-status-of-services) and [logs](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/admin/#checking-logs) of the installed OpenVidu services.

### Configuration and administration

Once **OPENVIDU_URL** is reachable, the deployment is complete and working. See the [Administration](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/oracle/admin/index.md) section to learn how to manage your deployment.
