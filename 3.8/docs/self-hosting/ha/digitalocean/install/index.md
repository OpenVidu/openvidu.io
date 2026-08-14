# OpenVidu High Availability installation: DigitalOcean

DigitalOcean

Info

OpenVidu High Availability is part of **OpenVidu PRO**. Before deploying, you need to [create an OpenVidu account](https://openvidu.io/account/) to get your license key. There's a 15-day free trial waiting for you!

This section describes how to deploy a production-ready OpenVidu High Availability setup on DigitalOcean. The deployed services are equivalent to those in the [On Premises High Availability installation](https://openvidu.io/3.8/docs/self-hosting/ha/on-premises/install-nlb/index.md), but provisioned as DigitalOcean resources and automated using Terraform CLI.

- DigitalOcean **Spaces Object Storage** (S3-compatible) is used for storing application data, recordings, and cluster data.
- Media Node scalability is managed via an **automated process (DigitalOcean Functions)** that scales the number of Media Nodes based on system load, although you can use a fixed number of media nodes.

## Prerequisites

- You need to have a DigitalOcean account with a [Personal Access Token](https://docs.digitalocean.com/reference/api/create-personal-access-token/) .
- You need to have installed [Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) .
- You need to have installed Git.

**Architecture overview**

This is what the deployment architecture looks like:

OpenVidu High Availability DigitalOcean Architecture

- The Load Balancer distributes HTTPS traffic to the Master Nodes.
- If RTMP media is ingested, the Load Balancer also routes this traffic to the Master Nodes, which act as a bridge.
- WebRTC traffic (SRTP/SCTP/STUN/TURN) is routed directly to the Media Nodes.
- 4 fixed Droplets are created for the Master Nodes. It must always be 4 Master Nodes to ensure high availability.
- An automated process using DigitalOcean Functions handles the scale-in and scale-out of Media Nodes based on system load.

## Custom scale-in strategy

We use a custom scale-in strategy to enable the graceful shutdown of Media Nodes, ensuring that active Rooms are never disrupted when the cluster removes a Media Node.

**Custom scale-in strategy**

- A Lambda function is deployed on a four-minute schedule to manage the scaling of Media Nodes. It does this by checking the **`minNumberOfMediaNodes`** and **`maxNumberOfMediaNodes`** variables, polling the average CPU usage, and comparing it against **`scaleTargetCPU`**. Once a scale-in decision is made, the main tag is removed from the target Media Node and a "draining" tag is applied to mark it as ready for shutdown.
- Each instance runs a cron job that checks every two minutes whether the "draining" tag is present. If it is, the graceful shutdown script is triggered, which waits for all active rooms on that node to conclude before shutting down.

## Deployment details

1. Clone the OpenVidu repository with the terraform files:

   ```bash
   git clone https://github.com/OpenVidu/openvidu-digitalocean.git
   git -C openvidu-digitalocean checkout 3.8.0
   cd openvidu-digitalocean/pro/ha
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

   | Input Value                 | Default Value   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
   | --------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | `region`                    | `"ams3"`        | DigitalOcean region where resources will be created.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
   | `masterNodesInstanceType`   | `"s-4vcpu-8gb"` | Specifies the DigitalOcean Droplet size for your Master Node.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
   | `mediaNodeInstanceType`     | `"s-4vcpu-8gb"` | Specifies the DigitalOcean Droplet size for your Media Nodes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
   | `initialNumberOfMediaNodes` | `1`             | Number of initial media nodes to deploy.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
   | `minNumberOfMediaNodes`     | `1`             | Minimum number of media nodes to deploy (for reference, manual scaling required).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
   | `maxNumberOfMediaNodes`     | `5`             | Maximum number of media nodes to deploy (for reference, manual scaling required).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
   | `scaleTargetCPU`            | `50`            | Target CPU percentage to scale up or down.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
   | `fixedNumberOfMediaNodes`   | `0`             | Fixed number of media nodes to create (0 = use autoscaling).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
   | `rtcEngine`                 | `"pion"`        | Media Engine. Available options: `pion`, `mediasoup`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
   | `certificateType`           | `"letsencrypt"` | Certificate type for OpenVidu deployment. Options: - `selfsigned` - Not recommended for production use. Just for testing purposes or development environments. You don't need a FQDN to use this option. - `owncert` - Valid for production environments. Use your own certificate. You need a FQDN to use this option. - `letsencrypt` - Valid for production environments. Can be used with or without a FQDN (if no FQDN is provided, the public IP is used as the domain name and a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability) certificate is issued for it). |
   | `domainName`                | `(none)`        | Domain name for the OpenVidu Deployment. Not mandatory; if not provided, the public IP is used as the domain name.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
   | `ownPublicCertificate`      | `(none)`        | If certificate type is 'owncert', this parameter will be used to specify the public certificate in base64 format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
   | `ownPrivateCertificate`     | `(none)`        | If certificate type is 'owncert', this parameter will be used to specify the private certificate in base64 format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
   | `initialMeetAdminPassword`  | `(none)`        | Initial password for the 'admin' user in OpenVidu Meet. If not provided, a random password will be generated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
   | `initialMeetApiKey`         | `(none)`        | Initial API key for OpenVidu Meet. If not provided, no API key will be set and the user can set it later from Meet Console.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
   | `volumeSize`                | `100`           | Size of the additional volume in GB for Master Node.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
   | `spaceAppDataName`          | `(none)`        | Name of the DigitalOcean Space (S3-compatible bucket) to store application data and recordings. If empty, a bucket will be created with default name.                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
   | `spaceClusterDataName`      | `(none)`        | Name of the DigitalOcean Space (S3-compatible bucket) to store cluster data. If empty, a bucket will be created with default name.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
   | `spaceRegion`               | `"ams3"`        | DigitalOcean Spaces region where the bucket will be created.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
   | `spacesAccessId`            | `(none)`        | Access key ID for DigitalOcean Spaces (S3-compatible). Required if spaceAppDataName or spaceClusterDataName is empty.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
   | `spacesSecretKey`           | `(none)`        | Secret access key for DigitalOcean Spaces (S3-compatible). Required if spaceAppDataName or spaceClusterDataName is empty.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
   | `additionalInstallFlags`    | `(none)`        | Additional optional flags to pass to the OpenVidu installer (comma-separated, e.g., '--flag1=value, --flag2'). Currently we only have one flag that is `--force-utc-timezone` to force UTC as the timezone for OpenVidu. By default, OpenVidu uses the timezone configured in the host machine where it is installed. Note that in general it is recommended to use UTC, and DigitalOcean Droplets already default to UTC, so this flag is not usually necessary.                                                                                                                                           |

   Warning

   In DigitalOcean, you need [Space Access Keys](https://cloud.digitalocean.com/spaces/access_keys) to create a bucket. If you leave the **spaceAppDataName** or **spaceClusterDataName** variable empty, you must configure these keys with full access so a new bucket can be created. [Here is how](https://docs.digitalocean.com/products/spaces/how-to/manage-access/#access-keys) .

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
   chmod 600 <PATH_TO_THE_KEY>/openvidu_ssh_key_ha.pem
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
ssh -i openvidu_ssh_key_ha.pem root@PUBLIC_DROPLET_IP
```

Then navigate to /opt/openvidu/ and you will find all required credentials in `secrets.env`.

Then open **OPENVIDU_URL** and you will see the OpenVidu Meet interface. Log in with **MEET_INITIAL_ADMIN_PASSWORD** and you will be able to enjoy the features of OpenVidu Meet.

## Configure your application to use the deployment

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

**OpenVidu V2 Compatibility Credentials**

This section is only needed if you want to use OpenVidu v2 compatibility.

- **URL**: The URL to access OpenVidu, which is the value of `OPENVIDU_URL` (e.g., `https://yourdomain.example.io/`)
- **Username**: Basic auth user for OpenVidu v2 compatibility. It is always `OPENVIDUAPP`.
- **Password**: Basic auth password for OpenVidu v2 compatibility is the same as `LIVEKIT_API_SECRET`.

### Troubleshooting initial DigitalOcean deployment creation

If something goes wrong during the initial DigitalOcean deployment creation, you won't be able to reach the **OPENVIDU_URL**. It could be due to a misconfiguration in the parameters, a lack of permissions, or a problem with services. When this happens, the following steps can help you troubleshoot the issue and identify what went wrong:

1. Check whether the instance or instances are running. If they are not, check whether the `terraform apply` command logged an error.

1. If the instance or instances are running, SSH into the instance and check the logs by running this command:

   ```text
   cat /var/log/cloud-init-output.log
   ```

   These logs will give you more information about the DigitalOcean deployment creation process.

1. If everything seems fine, check the [status](https://openvidu.io/3.8/docs/self-hosting/ha/on-premises/admin/#checking-the-status-of-services) and the [logs](https://openvidu.io/3.8/docs/self-hosting/ha/on-premises/admin/#checking-logs) of the installed OpenVidu services.

### Configuration and administration

When your **OPENVIDU_URL** is reachable, it means that everything has gone well. Now you can check the [Administration](https://openvidu.io/3.8/docs/self-hosting/ha/digitalocean/admin/index.md) section to learn how to manage your deployment.
