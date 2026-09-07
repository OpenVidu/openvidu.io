# OpenVidu High Availability installation: Oracle Cloud Infrastructure

Oracle Cloud Infrastructure

Info

OpenVidu High Availability is part of **OpenVidu** **PRO**. Before deploying, you need to [create an OpenVidu account](https://openvidu.io/3.8/account/index.md) to get your license key. There's a 15-day free trial waiting for you!

This section describes how to deploy a production-ready OpenVidu High Availability cluster on Oracle Cloud Infrastructure (OCI). The deployed services are identical to those in the [On Premises High Availability installation](https://openvidu.io/3.8/docs/self-hosting/ha/on-premises/install-nlb/index.md), but are provisioned as OCI resources and the process is fully automated using the Terraform CLI.

- An **OCI Network Load Balancer (NLB)** is the public entry point for the cluster. It distributes HTTPS (443), HTTP (80) and RTMP (1935) traffic across the 4 Master Nodes.
- **OCI Object Storage** (S3-compatible via Customer Secret Keys) is used through two buckets: one for application data and recordings, and another for cluster-wide shared state (including the generated SSH key).
- **OCI Vault** is used to securely store deployment secrets shared across the cluster.
- Media Node scalability is managed through an **OCI Function** that handles scale-in actions, while the OCI Instance Pool itself takes care of scale-out based on system load.

## Prerequisites

- An Oracle Cloud Infrastructure account with permissions to create Compute instances, VCNs, Network Load Balancers, Object Storage buckets, Vaults, Functions and IAM resources.
- [Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) installed on your machine.
- Git installed on your machine.

**Architecture overview**

The deployment architecture is as follows:

OpenVidu High Availability Oracle Cloud Infrastructure Architecture

- The Network Load Balancer distributes HTTPS traffic to the Master Nodes.
- If RTMP media is ingested, the Network Load Balancer also routes this traffic to the Master Nodes, which act as a bridge.
- WebRTC traffic (SRTP/SCTP/STUN/TURN) is routed directly to the Media Nodes.
- 4 fixed Compute instances are created for the Master Nodes. It must always be 4 Master Nodes to ensure high availability.
- An OCI Instance Pool of Media Nodes is created to scale the number of Media Nodes based on system load.

## Custom scale-in strategy

We use a custom scale-in strategy to enable the graceful shutdown of Media Nodes, ensuring that active Rooms are never disrupted when the cluster removes a Media Node.

**Custom scale-in strategy**

- An **OCI Function** is deployed and triggered on a regular schedule. It polls the average CPU of the Instance Pool against **`scaleTargetCPU`** and never scales the pool below **`minNumberOfMediaNodes`**, and when a scale-in decision is made, the target Media Node is flagged as "draining" so it stops accepting new Rooms.
- Because there are 4 Master Nodes, each one runs the scale-in invoker on a cron, but only one master should call the function per cycle. Coordination is done through a `scalein.lock` object stored in the cluster-data Object Storage bucket: the master that wins an atomic compare-and-swap (ETag-based) on this object is the one that invokes the function that cycle. The lock has a 3-minute TTL, so if the master holding it crashes, a peer claims it on the next cycle. Using an Object Storage lock instead of an OCI Vault secret avoids consuming a new secret version on every cycle.
- Each Media Node runs a `systemd` daemon that periodically checks whether the instance has been marked as "draining". If so, the graceful shutdown script is triggered, which waits for all active Rooms on that node to end before shutting the instance down.

## Publishing the scale-in function image

The OCI Function that performs graceful Media Node scale-in runs from a container image that must be hosted in an [OCI Registry (OCIR)](https://docs.oracle.com/en-us/iaas/Content/Registry/Concepts/registryoverview.htm) in the **same region** as the Function. Because of this regional constraint, the **`scale_in_function_image`** parameter is mandatory: you must make the scale-in image available in an OCIR in your deployment's region and point the parameter to it.

Info

If you are deploying in the **Madrid** region (`mad.ocir.io`), you can skip this section entirely. OpenVidu already publishes the scale-in image in the Madrid OCIR, so you only need to set `scale_in_function_image = "mad.ocir.io/axp2ice0s7el/openvidu-oci-scalein:3.8.0"` (the value that was previously used as the default). The steps below are only required when deploying in any other region.

OpenVidu publishes a prebuilt scale-in image on Docker Hub, so there are two ways to get it into your OCIR. Pick the one that best fits your needs:

**Option 1: Use the prebuilt image (recommended)**

Pull the prebuilt image that OpenVidu publishes on Docker Hub and push it, unchanged, to your own OCIR.

1. Pull the image from Docker Hub:

   ```bash
   docker pull docker.io/openvidu/openvidu-oci-scalein:3.8.0
   ```

1. Authenticate Docker against your OCI Registry. You will need an [OCI Auth Token](https://docs.oracle.com/en-us/iaas/Content/Registry/Tasks/registrygettingauthtoken.htm) for the user you log in with:

   ```bash
   docker login <region-key>.ocir.io -u '<tenancy-namespace>/<username>' -p '<auth-token>'
   ```

   Replace `<region-key>` with the [OCIR region code](https://docs.oracle.com/en-us/iaas/Content/Registry/Concepts/registryprerequisites.htm#regional-availability) (for example `fra` for Frankfurt, `iad` for Ashburn, `mad` for Madrid).

   Replace `<username>` with the value matching your authentication setup — the exact format depends on whether your tenancy uses identity domains, federation with IDCS, or local IAM users. See [Pushing Images Using the Docker CLI](https://docs.oracle.com/en-us/iaas/Content/Registry/Tasks/registrypushingimagesusingthedockercli.htm) for the exact pattern in each case (typical forms are `<username>`, `<identity-domain>/<username>`, or `oracleidentitycloudservice/<email>`).

1. Tag the pulled image for your OCIR. The tag must follow the format `<region-key>.ocir.io/<tenancy-namespace>/<repo>:<tag>`:

   ```bash
   docker tag docker.io/openvidu/openvidu-oci-scalein:3.8.0 <region-key>.ocir.io/<tenancy-namespace>/openvidu-oci-scalein:3.8.0
   ```

1. Push the image to your OCIR:

   ```bash
   docker push <region-key>.ocir.io/<tenancy-namespace>/openvidu-oci-scalein:3.8.0
   ```

1. Set `scale_in_function_image` in `terraform.tfvars` to the image reference you just pushed:

   ```hcl
   scale_in_function_image = "<region-key>.ocir.io/<tenancy-namespace>/openvidu-oci-scalein:3.8.0"
   ```

**Option 2: Build the image from source**

Build the scale-in function image yourself from the OpenVidu sources and push it to your OCIR — useful if you want to pin or customise the build. This requires the `openvidu-oracle` repository cloned (see [Deployment details](#deployment-details)).

1. From the cloned `openvidu-oracle` repository, navigate to the scale-in function source directory:

   ```bash
   cd openvidu-oracle/pro/scalein-function
   ```

1. Authenticate Docker against your OCI Registry. You will need an [OCI Auth Token](https://docs.oracle.com/en-us/iaas/Content/Registry/Tasks/registrygettingauthtoken.htm) for the user you log in with:

   ```bash
   docker login <region-key>.ocir.io -u '<tenancy-namespace>/<username>' -p '<auth-token>'
   ```

   Replace `<region-key>` with the [OCIR region code](https://docs.oracle.com/en-us/iaas/Content/Registry/Concepts/registryprerequisites.htm#regional-availability) (for example `fra` for Frankfurt, `iad` for Ashburn, `mad` for Madrid).

   Replace `<username>` with the value matching your authentication setup — the exact format depends on whether your tenancy uses identity domains, federation with IDCS, or local IAM users. See [Pushing Images Using the Docker CLI](https://docs.oracle.com/en-us/iaas/Content/Registry/Tasks/registrypushingimagesusingthedockercli.htm) for the exact pattern in each case (typical forms are `<username>`, `<identity-domain>/<username>`, or `oracleidentitycloudservice/<email>`).

1. Build and tag the image. The tag must follow the format `<region-key>.ocir.io/<tenancy-namespace>/<repo>:<tag>`:

   ```bash
   docker build -t <region-key>.ocir.io/<tenancy-namespace>/scale-in-function:<tag> .
   ```

1. Push the image to OCIR:

   ```bash
   docker push <region-key>.ocir.io/<tenancy-namespace>/scale-in-function:<tag>
   ```

1. Set `scale_in_function_image` in `terraform.tfvars` to the image reference you just pushed:

   ```hcl
   scale_in_function_image = "<region-key>.ocir.io/<tenancy-namespace>/scale-in-function:<tag>"
   ```

Info

Make sure the OCI Function's compartment has the IAM policies needed to pull from the target repository. If the repository lives in a different tenancy from the OCI Function, see [Pulling Images from Repositories in other Tenancies](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionspullingimagescrosstenancy.htm) for the required Endorse/Admit/Define policy statements.

## Deployment details

1. Clone the OpenVidu repository containing the Terraform files:

   ```bash
   git clone https://github.com/OpenVidu/openvidu-oracle.git
   git -C openvidu-oracle checkout 3.8.0
   cd openvidu-oracle/pro/ha
   ```

1. Copy **`terraform.tfvars.example`** to **`terraform.tfvars`**, update the required parameters with your values, and adjust any optional defaults as needed.

   Information about parameters

   ### Mandatory Parameters

   | Input Value               | Description                                                                                                                                                                                                                                                                                                                                                      |
   | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | `tenancy_ocid`            | OCI Tenancy OCID. Required for the Object Storage namespace.                                                                                                                                                                                                                                                                                                     |
   | `compartment_ocid`        | OCI Compartment OCID where resources will be created.                                                                                                                                                                                                                                                                                                            |
   | `user_ocid`               | OCI User OCID used to create Customer Secret Keys for S3-compatible access to Object Storage.                                                                                                                                                                                                                                                                    |
   | `stackName`               | Stack name for the OpenVidu deployment.                                                                                                                                                                                                                                                                                                                          |
   | `openviduLicense`         | OpenVidu PRO license key. Visit [your OpenVidu account](https://openvidu.io/3.8/account/index.md) to obtain your license.                                                                                                                                                                                                                                        |
   | `scale_in_function_image` | OCIR image URL consumed by the OCI Function that handles graceful Media Node scale-in. There is no default value — you must publish this image to an OCI Registry in your deployment's region and point this parameter to it. See [Publishing the scale-in function image](#publishing-the-scale-in-function-image). Ignored when `fixedNumberOfMediaNodes > 0`. |

   ### Optional Parameters

   | Input Value                 | Default Value           | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
   | --------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
   | `region`                    | `"eu-frankfurt-1"`      | OCI region where resources will be created.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
   | `availability_domain`       | `1`                     | Availability Domain number (1, 2, or 3) to use for resources.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
   | `masterNodeShape`           | `"VM.Standard.E4.Flex"` | OCI Compute shape for each OpenVidu Master Node. All 4 Master Nodes use the same shape and size.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
   | `masterNodeOcpus`           | `2`                     | Number of OCPUs per Master Node (applies to Flex shapes only).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
   | `masterNodeMemory`          | `8`                     | Memory in GB per Master Node (applies to Flex shapes only).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
   | `masterNodeDiskSize`        | `100`                   | Boot disk size in GB for each Master Node.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
   | `mediaNodeShape`            | `"VM.Standard.E4.Flex"` | OCI Compute shape for the OpenVidu Media Nodes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
   | `mediaNodeOcpus`            | `3`                     | Number of OCPUs for each Media Node (applies to Flex shapes only).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
   | `mediaNodeMemory`           | `4`                     | Memory in GB for each Media Node (applies to Flex shapes only).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
   | `mediaNodeDiskSize`         | `100`                   | Boot disk size in GB for the Media Nodes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
   | `fixedNumberOfMediaNodes`   | `0`                     | If `> 0`, deploys a fixed number of Media Nodes with no autoscaling and no scale-in OCI Function (`initialNumberOfMediaNodes`, `minNumberOfMediaNodes`, `maxNumberOfMediaNodes`, `scaleTargetCPU` and `scale_in_function_image` are ignored). If `0` (default), the deployment is elastic and autoscaling is enabled.                                                                                                                                                                                                                                                                |
   | `initialNumberOfMediaNodes` | `1`                     | Initial number of Media Nodes to deploy. Ignored when `fixedNumberOfMediaNodes > 0`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
   | `minNumberOfMediaNodes`     | `1`                     | Minimum number of Media Nodes the autoscaling Instance Pool will keep running. Ignored when `fixedNumberOfMediaNodes > 0`.                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
   | `maxNumberOfMediaNodes`     | `5`                     | Maximum number of Media Nodes the autoscaling Instance Pool can launch. Ignored when `fixedNumberOfMediaNodes > 0`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
   | `scaleTargetCPU`            | `50`                    | Target CPU percentage that triggers scale-in/scale-out actions. Ignored when `fixedNumberOfMediaNodes > 0`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
   | `certificateType`           | `"letsencrypt"`         | Certificate type for the OpenVidu deployment. Options: - `selfsigned` - Not recommended for production use. Intended for testing or development environments only. A FQDN is not required. - `owncert` - Suitable for production environments. Uses your own certificate. A FQDN is required. - `letsencrypt` - Suitable for production environments. Can be used with or without a FQDN (if no FQDN is provided, the public IP is used as the domain name and a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability) certificate is issued for it). |
   | `publicIpAddress`           | `(none)`                | A previously created Reserved Public IP OCID to attach to the Network Load Balancer. Leave blank to generate a new public IP.                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
   | `domainName`                | `(none)`                | Domain name for the OpenVidu deployment. Optional — if not provided, the NLB public IP is used as the domain name.                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
   | `ownPublicCertificate`      | `(none)`                | If the certificate type is `owncert`, this parameter specifies the public certificate in base64 format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
   | `ownPrivateCertificate`     | `(none)`                | If the certificate type is `owncert`, this parameter specifies the private certificate in base64 format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
   | `initialMeetAdminPassword`  | `(none)`                | Initial password for the `admin` user in OpenVidu Meet. Alphanumeric characters, underscores or hyphens only (A-Z, a-z, 0-9, \_, -). If not provided, a random password will be generated.                                                                                                                                                                                                                                                                                                                                                                                           |
   | `initialMeetApiKey`         | `(none)`                | Initial API key for OpenVidu Meet. Alphanumeric characters, underscores or hyphens only (A-Z, a-z, 0-9, \_, -). If not provided, no API key will be set; one can be configured later from the Meet Console.                                                                                                                                                                                                                                                                                                                                                                          |
   | `bucketAppDataName`         | `(none)`                | Name of an existing OCI Object Storage bucket for application data and recordings. If left empty, a bucket will be created with a default name.                                                                                                                                                                                                                                                                                                                                                                                                                                      |
   | `bucketClusterDataName`     | `(none)`                | Name of an existing OCI Object Storage bucket for cluster-wide shared state (including the generated SSH key). If left empty, a bucket will be created with a default name.                                                                                                                                                                                                                                                                                                                                                                                                          |
   | `rtcEngine`                 | `"pion"`                | WebRTC media engine to use. Options: - `pion` - Default media engine. - `mediasoup` - Alternative media engine with different performance characteristics.                                                                                                                                                                                                                                                                                                                                                                                                                           |
   | `vault_ocid`                | `(none)`                | OCI KMS Vault OCID for secrets management. If left empty, a new vault will be created.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
   | `key_ocid`                  | `(none)`                | OCI KMS Key OCID for secrets management. If left empty, a new key will be created.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
   | `additionalInstallFlags`    | `(none)`                | Additional optional flags to pass to the OpenVidu installer (comma-separated, e.g., `--flag1=value, --flag2`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

1. Deploy with Terraform using the following commands:

   ```bash
   terraform init
   terraform apply
   ```

1. Logs will appear in the `terraform apply` console output. Wait for it to finish and display `Apply Complete!`. Then go to [OCI Object Storage](https://cloud.oracle.com/object-storage/buckets) and wait for the SSH key to appear in your configured cluster-data bucket.

   Warning

   After downloading the SSH key, it is strongly recommended to **DELETE IT** from the bucket. This file is the private key used to access all 4 Master Nodes — if exposed, unauthorized users could gain access.

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

SSH into any of the Master Nodes by running the following command from the directory where your SSH key is located:

```bash
ssh -i openvidu_private_ssh_key_<STACK_NAME>.pem ubuntu@MASTER_NODE_PUBLIC_IP
```

You can find the public IPs of the 4 Master Nodes (named `<STACK_NAME>-master-node-1` … `<STACK_NAME>-master-node-4`) on the [OCI Compute Instances](https://cloud.oracle.com/compute/instances) page. User traffic goes through the Network Load Balancer; the per-master public IPs are intended for SSH access only.

Then navigate to `/opt/openvidu/config/` where you will find all credentials in the following files:

- `openvidu.env`
- `meet.env`

Open **OPENVIDU_URL** and you will see the OpenVidu Meet interface.

Log in with **MEET_INITIAL_ADMIN_PASSWORD** to start using OpenVidu Meet.

## Configure your application to use the deployment

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

1. If everything appears to be in order, check the [status](https://openvidu.io/3.8/docs/self-hosting/ha/on-premises/admin/#checking-the-status-of-services) and [logs](https://openvidu.io/3.8/docs/self-hosting/ha/on-premises/admin/#checking-logs) of the installed OpenVidu services on all Master Nodes and Media Nodes.

### Configuration and administration

Once **OPENVIDU_URL** is reachable, the deployment is complete and working. See the [Administration](https://openvidu.io/3.8/docs/self-hosting/ha/oracle/admin/index.md) section to learn how to manage your OpenVidu High Availability deployment.
