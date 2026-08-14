# OpenVidu Single Node PRO installation: DigitalOcean

DigitalOcean

This section describes two ways to install OpenVidu Single Node PRO on DigitalOcean:

- [**Web Console**](#web-console): Can be deployed without installing anything on your machine, but it requires more manual steps and has some limitations. For example, recordings are stored on the machine (instead of Digital Ocean Spaces Object Storage).
- [**Terraform**](#terraform): More powerful and automated, but it requires installing the Terraform CLI on your machine.

## **Web Console**

This page explains how to create a Droplet (VM) in DigitalOcean, configure networking, and prepare it for OpenVidu Single Node PRO On Premises. Installing, administering, and upgrading OpenVidu Single Node PRO itself is covered in the On-Premises documentation.

### Prerequisites

- DigitalOcean account with permission to create Droplets and networking resources.

______________________________________________________________________

### 1. Create the Droplet

1. Log in to your [**DigitalOcean**](https://cloud.digitalocean.com/) account.
1. Search for **Droplets**, click it, and then click *"Create Droplet"*. Create Droplet
1. Choose a region and then change the image to Ubuntu *"24.04 (LTS) x64"* if it is not selected yet. OS Selection
1. Select the size for your OpenVidu server. We recommend **4 CPUs or more and at least 4 GB of RAM** for OpenVidu to run correctly.
1. Scroll down to Authentication Method and choose the one you prefer. This will be used to connect to the instance via terminal. If you want to use an SSH key, follow the instructions shown when you click New SSH Key. Create New SSH Key
1. Review the configuration and click *"Create Droplet"*, you can change the hostname of the droplet if you want (for example, `openvidu-singlenode-pro`).

______________________________________________________________________

### 2. Port rules in the network security lists

OpenVidu and WebRTC require specific inbound rules on the Firewall network security for it to work.

The [minimum inbound ports to allow](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/install/#port-rules) must be included in the Firewall rules.

1. Click the droplet, then go to *"Networking"*, scroll down and click on *"Edit"* in **Firewall** section. Edit Firewall Rules

1. Now click on *"Create Firewall"* and in **Inbound Rules** add the following rules. Inbound rules

   Warning

   It is important that you make sure the protocol is the one that is shown in the image.

1. Name the firewall, then scroll to the bottom and search for your Droplet by name. Select it to apply the firewall rules to it. Firewall apply to droplet

______________________________________________________________________

### 3. SSH access and OpenVidu installation

1. SSH into the instance:

   ```bash
   ssh -i private_key_downloaded.key root@PUBLIC_IP
   sudo apt update && sudo apt upgrade -y
   ```

1. Follow the [On-Premises install instructions](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/install/#guided-installation) to install OpenVidu on the instance.

______________________________________________________________________

### 4. Administration and upgrade

- For administration of this OpenVidu Single Node PRO deployment, see the [On-Premises administration section](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/admin/index.md).
- To upgrade OpenVidu, see the [Upgrade section](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/upgrade/index.md).

## **Terraform**

This section contains instructions for deploying a production-ready OpenVidu Single Node PRO deployment on DigitalOcean. The deployed services are the same as in the [On Premises Single Node installation](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/install/index.md), but the process is automated through the Terraform CLI. Additionally, DigitalOcean Spaces (S3-compatible storage) is used to store recordings and other persistent data.

### Prerequisites

- You need to have a DigitalOcean account with a [Personal Access Token](https://docs.digitalocean.com/reference/api/create-personal-access-token/) .
- You need to have installed [Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) .
- You need to have installed Git.

**Architecture overview**

This is what the deployment architecture looks like:

OpenVidu Single Node PRO DigitalOcean Architecture

### Deployment details

1. Clone the OpenVidu repository with the terraform files:

   ```text
   git clone https://github.com/OpenVidu/openvidu-digitalocean.git
   git -C openvidu-digitalocean checkout 3.8.0
   cd openvidu-digitalocean/pro/singlenode
   ```

1. Copy **terraform.tfvars.example** to **terraform.tfvars**, update the required parameters with your values, and optionally adjust defaults.

   Information about parameters

   #### Mandatory Parameters

   | Input Value       | Description                                                                                        |
   | ----------------- | -------------------------------------------------------------------------------------------------- |
   | `doToken`         | DigitalOcean Personal Access Token for API authentication.                                         |
   | `stackName`       | Stack name for OpenVidu deployment.                                                                |
   | `openviduLicense` | OpenVidu License for PRO deployments. Go [here](https://openvidu.io/account) for more information. |

   #### Optional Parameters

   | Input Value                | Default Value   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
   | -------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | `region`                   | `"ams3"`        | DigitalOcean region where resources will be created.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
   | `instanceType`             | `"s-2vcpu-4gb"` | Specifies the DigitalOcean Droplet size for your OpenVidu instance.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
   | `certificateType`          | `"letsencrypt"` | Certificate type for OpenVidu deployment. Options: - `selfsigned` - Not recommended for production use. Just for testing purposes or development environments. You don't need a FQDN to use this option. - `owncert` - Valid for production environments. Use your own certificate. You need a FQDN to use this option. - `letsencrypt` - Valid for production environments. Can be used with or without a FQDN (if no FQDN is provided, the public IP is used as the domain name and a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability) certificate is issued for it). |
   | `domainName`               | `(none)`        | Domain name for the OpenVidu Deployment. Not mandatory; if not provided, the public IP is used as the domain name.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
   | `ownPublicCertificate`     | `(none)`        | If certificate type is 'owncert', this parameter will be used to specify the public certificate in base64 format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
   | `ownPrivateCertificate`    | `(none)`        | If certificate type is 'owncert', this parameter will be used to specify the private certificate in base64 format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
   | `initialMeetAdminPassword` | `(none)`        | Initial password for the 'admin' user in OpenVidu Meet. If not provided, a random password will be generated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
   | `initialMeetApiKey`        | `(none)`        | Initial API key for OpenVidu Meet. If not provided, no API key will be set and the user can set it later from Meet Console.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
   | `rtcEngine`                | `pion`          | RTCEngine media engine to use. Values are pion or mediasoup.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
   | `spaceName`                | `(none)`        | Name of the DigitalOcean Space (S3-compatible bucket) to store application data and recordings. If empty, a bucket will be created with default name.                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
   | `spaceRegion`              | `"ams3"`        | DigitalOcean Spaces region where the bucket will be created.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
   | `spacesAccessId`           | `(none)`        | Access key ID for DigitalOcean Spaces (S3-compatible). Required if spaceName is empty.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
   | `spacesSecretKey`          | `(none)`        | Secret access key for DigitalOcean Spaces (S3-compatible). Required if spaceName is empty.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
   | `additionalInstallFlags`   | `(none)`        | Additional optional flags to pass to the OpenVidu installer (comma-separated, e.g., '--flag1=value, --flag2'). Currently we only have one flag that is `--force-utc-timezone` to force UTC as the timezone for OpenVidu. By default, OpenVidu uses the timezone configured in the host machine where it is installed. Note that in general it is recommended to use UTC, and DigitalOcean Droplets already default to UTC, so this flag is not usually necessary.                                                                                                                                           |

   Warning

   In DigitalOcean, you need [Space Access Keys](https://cloud.digitalocean.com/spaces/access_keys) to create a bucket. If you leave the **spaceName** variable empty, you must configure these keys with full access so a new bucket can be created. [Here is how](https://docs.digitalocean.com/products/spaces/how-to/manage-access/#access-keys) .

1. Use the following commands to deploy with terraform.

   ```bash
   terraform init
   terraform apply
   ```

1. You will see logs appear in the terraform apply execution console. Wait for it to finish and display `Apply Complete!`. Now go to [Space Object Storage](https://cloud.digitalocean.com/spaces) and wait for the ssh key to appear in the bucket you have configured.

   Warning

   After downloading the SSH key, it is highly recommended to **DELETE IT** from the bucket. This file is the private key used to access the droplet. If exposed, unauthorized users could gain access to the instance.

   SSH Key in Bucket

1. Give the SSH Key the necessary permissions for it to work.

   **Linux**

   Command in linux:

   ```text
   chmod 600 <PATH_TO_THE_KEY>/openvidu_ssh_key_snpro.pem
   ```

   **Powershell**

   Command in powershell:

   ```text
   $KeyPath = "<PATH_TO_THE_KEY>" &&
   icacls $KeyPath /inheritance:r &&
   icacls $KeyPath /grant:r "$($env:USERNAME):(R)"
   ```

### Access OpenVidu

To verify that your OpenVidu deployment works correctly wait for the `secrets.env` to appear in the bucket that you've configured and open it to view the credentials of OpenVidu.

**View OpenVidu credentials in the Web**

- Go to the Space Object Storage bucket that you've configured and download the `secrets.env` file. Secrets.env in Bucket

**View OpenVidu credentials in the instance**

SSH to the instance by running this command from the directory where your SSH key is located:

```text
ssh -i openvidu_ssh_key_snpro.pem root@PUBLIC_DROPLET_IP
```

Then navigate to /opt/openvidu/ and you will find all credentials needed in the `secrets.env`.

Then open **OPENVIDU_URL** and you will see the OpenVidu Meet interface. Log in with **MEET_INITIAL_ADMIN_PASSWORD** and you will be able to enjoy the features of OpenVidu Meet.

### Configure your application to use the deployment

You may need your Digital Ocean credentials to configure your OpenVidu application. You can check these secrets following these steps ([View OpenVidu credentials in the Web](#view-openvidu-credentials-in-the-web)) or ([View OpenVidu credentials in the instance](#view-openvidu-credentials-in-the-instance)).

Your authentication credentials and the URL to point your applications to are:

**OpenVidu Meet**:

- **`OPENVIDU_URL`**: The URL to access OpenVidu Meet, which is always `https://yourdomain.example.io/`
- **`MEET_INITIAL_ADMIN_USER`**: User to access OpenVidu Meet Console. It is always `admin`.
- **`MEET_INITIAL_ADMIN_PASSWORD`**: Password to access OpenVidu Meet Console.
- **`MEET_INITIAL_API_KEY`**: API key to use OpenVidu Meet Embedded and OpenVidu Meet REST API.

Note

The `MEET_INITIAL_ADMIN_USER`, `MEET_INITIAL_ADMIN_PASSWORD`, and `MEET_INITIAL_API_KEY` values are initial settings that changing them will not affect to the deployment. They can only be changed from the Meet Console.

**OpenVidu Platform:**

- **`LIVEKIT_URL`**: The URL to use LiveKit SDKs, which can be `wss://yourdomain.example.io/` or `https://yourdomain.example.io/` depending on the client library you are using.
- **`LIVEKIT_API_KEY`**: API Key for LiveKit SDKs.
- **`LIVEKIT_API_SECRET`**: API Secret for LiveKit SDKs.

### Troubleshooting initial DigitalOcean deployment creation

If something goes wrong during the initial DigitalOcean deployment creation, you won't be able to reach the **OPENVIDU_URL**. It could be due to a misconfiguration in the parameters, a lack of permissions, or a problem with services. When this happens, the following steps can help you troubleshoot the issue and identify what went wrong:

1. Check whether the instance or instances are running. If they are not, check whether the `terraform apply` command logged an error.

1. If the instance or instances are running, SSH into the instance and check the logs by running this command:

   ```text
   cat /var/log/cloud-init-output.log
   ```

   These logs will give you more information about the DigitalOcean deployment creation process.

1. If everything seems fine, check the [status](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/admin/#checking-the-status-of-services) and the [logs](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/admin/#checking-logs) of the installed OpenVidu services.

### Configuration and administration

When your **OPENVIDU_URL** is reachable, it means that everything has gone well. Now you can check the [Administration](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/digitalocean/admin/index.md) section to learn how to manage your deployment.
