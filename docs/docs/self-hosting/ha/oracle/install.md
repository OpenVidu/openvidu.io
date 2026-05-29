---
title: OpenVidu High Availability installation on Oracle Cloud Infrastructure
description: Learn how to deploy OpenVidu High Availability on Oracle Cloud Infrastructure
tags:
  - copyclipboard
---

# OpenVidu High Availability installation: Oracle Cloud Infrastructure

<div class="provider-chip" markdown>

:custom-oracle-cloud-infrastructure:{ .provider-chip-icon } Oracle Cloud Infrastructure

</div>


--8<-- "shared/self-hosting/ha-license-intro.md"

This section describes how to deploy a production-ready OpenVidu High Availability cluster on Oracle Cloud Infrastructure (OCI). The deployed services are identical to those in the [On Premises High Availability installation](../on-premises/install-nlb.md), but are provisioned as OCI resources and the process is fully automated using the Terraform CLI.

- An **OCI Network Load Balancer (NLB)** is the public entry point for the cluster. It distributes HTTPS (443), HTTP (80) and RTMP (1935) traffic across the 4 Master Nodes.
- **OCI Object Storage** (S3-compatible via Customer Secret Keys) is used through two buckets: one for application data and recordings, and another for cluster-wide shared state (including the generated SSH key).
- **OCI Vault** is used to securely store deployment secrets shared across the cluster.
- Media Node scalability is managed through an **OCI Function** that handles scale-in actions, while the OCI Instance Pool itself takes care of scale-out based on system load.

## Prerequisites

* An Oracle Cloud Infrastructure account with permissions to create Compute instances, VCNs, Network Load Balancers, Object Storage buckets, Vaults, Functions and IAM resources.
* [Terraform CLI :fontawesome-solid-external-link:{.external-link-icon}](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli){:target=_blank} installed on your machine.
* Git installed on your machine.

=== "Architecture overview"

    The deployment architecture is as follows:

    <figure markdown>
    ![OpenVidu High Availability Oracle Cloud Infrastructure Architecture](../../../../assets/images/self-hosting/ha/oracle/ha-oracle-architecture.svg){ .svg-img .dark-img }
    <figcaption>OpenVidu High Availability Oracle Cloud Infrastructure Architecture</figcaption>
    </figure>

    - The Network Load Balancer distributes HTTPS traffic to the Master Nodes.
    - If RTMP media is ingested, the Network Load Balancer also routes this traffic to the Master Nodes, which act as a bridge.
    - WebRTC traffic (SRTP/SCTP/STUN/TURN) is routed directly to the Media Nodes.
    - 4 fixed Compute instances are created for the Master Nodes. It must always be 4 Master Nodes to ensure high availability.
    - An OCI Instance Pool of Media Nodes is created to scale the number of Media Nodes based on system load.

## Custom scale-in strategy

We use a custom scale-in strategy to enable the graceful shutdown of Media Nodes, ensuring that active Rooms are never disrupted when the cluster removes a Media Node.

=== "Custom scale-in strategy"

    - An **OCI Function** is deployed and triggered on a regular schedule to manage the scaling of Media Nodes. It checks the **`minNumberOfMediaNodes`** and **`maxNumberOfMediaNodes`** variables, polls the average CPU usage of the Instance Pool, and compares it against **`scaleTargetCPU`**. When a scale-in decision is made, the target Media Node is flagged as "draining" so it stops accepting new Rooms.
    - In a HA deployment, the scale-in function is invoked by whichever Master Node currently holds the `SCALEIN_LOCK` in the OCI Vault, so only one master coordinates scale-in actions at a time.
    - Each Media Node runs a `systemd` daemon that periodically checks whether the instance has been marked as "draining". If so, the graceful shutdown script is triggered, which waits for all active Rooms on that node to end before shutting the instance down.

## Using your own scale-in function image

By default, the OCI Function pulls the scale-in image published by OpenVidu in the Madrid OCIR (`mad.ocir.io`). If you prefer to host the image in your own OCI Registry — for example, to avoid cross-region pulls, comply with internal policies, or pin a customised build — you can build and push it yourself, then point the `scale_in_function_image` variable to your image.

1. From the cloned `openvidu-oracle` repository, navigate to the scale-in function source directory:

    ```bash
    cd openvidu-oracle/pro/scalein-function
    ```

2. Authenticate Docker against your OCI Registry. You will need an [OCI Auth Token :fontawesome-solid-external-link:{.external-link-icon}](https://docs.oracle.com/en-us/iaas/Content/Registry/Tasks/registrygettingauthtoken.htm){:target=_blank} for the user you log in with:

    ```bash
    docker login <region-key>.ocir.io -u '<tenancy-namespace>/<username>' -p '<auth-token>'
    ```

    Replace `<region-key>` with the [OCIR region code :fontawesome-solid-external-link:{.external-link-icon}](https://docs.oracle.com/en-us/iaas/Content/Registry/Concepts/registryprerequisites.htm#regional-availability){:target=_blank} (for example `fra` for Frankfurt, `iad` for Ashburn, `mad` for Madrid).

3. Build and tag the image. The tag must follow the format `<region-key>.ocir.io/<tenancy-namespace>/<repo>:<tag>`:

    ```bash
    docker build -t <region-key>.ocir.io/<tenancy-namespace>/scale-in-function:<tag> .
    ```

4. Push the image to OCIR:

    ```bash
    docker push <region-key>.ocir.io/<tenancy-namespace>/scale-in-function:<tag>
    ```

5. Update `terraform.tfvars` with the new image reference:

    ```hcl
    scale_in_function_image = "<region-key>.ocir.io/<tenancy-namespace>/scale-in-function:<tag>"
    ```

!!! info
    Make sure the OCI Function's compartment has the IAM policies needed to pull from the target repository. If the repository is private, follow the [OCIR pull authentication guide :fontawesome-solid-external-link:{.external-link-icon}](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionspullingimagesfromocir.htm){:target=_blank}.

## Deployment details

1. Clone the OpenVidu repository containing the Terraform files:

    ```bash
    git clone https://github.com/OpenVidu/openvidu-oracle.git
    git -C openvidu-oracle checkout 3.7.0
    cd openvidu-oracle/pro/ha
    ```

2. Copy **`terraform.tfvars.example`** to **`terraform.tfvars`**, update the required parameters with your values, and adjust any optional defaults as needed.
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
    <td>OCI Tenancy OCID. Required for the Object Storage namespace.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>compartment_ocid</code></td>
    <td>OCI Compartment OCID where resources will be created.</td>
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
    <td>OpenVidu PRO license key. Visit <a href="https://openvidu.io/account" target="_blank">https://openvidu.io/account</a> to obtain your license.</td>
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
    <td style="white-space: nowrap;"><code>masterNodeShape</code></td>
    <td style="white-space: nowrap;"><code>"VM.Standard.E4.Flex"</code></td>
    <td>OCI Compute shape for each OpenVidu Master Node. All 4 Master Nodes use the same shape and size.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>masterNodeOcpus</code></td>
    <td style="white-space: nowrap;"><code>2</code></td>
    <td>Number of OCPUs per Master Node (applies to Flex shapes only).</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>masterNodeMemory</code></td>
    <td style="white-space: nowrap;"><code>8</code></td>
    <td>Memory in GB per Master Node (applies to Flex shapes only).</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>masterNodeDiskSize</code></td>
    <td style="white-space: nowrap;"><code>100</code></td>
    <td>Boot disk size in GB for each Master Node.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>mediaNodeShape</code></td>
    <td style="white-space: nowrap;"><code>"VM.Standard.E4.Flex"</code></td>
    <td>OCI Compute shape for the OpenVidu Media Nodes.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>mediaNodeOcpus</code></td>
    <td style="white-space: nowrap;"><code>3</code></td>
    <td>Number of OCPUs for each Media Node (applies to Flex shapes only).</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>mediaNodeMemory</code></td>
    <td style="white-space: nowrap;"><code>4</code></td>
    <td>Memory in GB for each Media Node (applies to Flex shapes only).</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>mediaNodeDiskSize</code></td>
    <td style="white-space: nowrap;"><code>100</code></td>
    <td>Boot disk size in GB for the Media Nodes.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>fixedNumberOfMediaNodes</code></td>
    <td style="white-space: nowrap;"><code>0</code></td>
    <td>If <code>&gt; 0</code>, deploys a fixed number of Media Nodes with no autoscaling and no scale-in OCI Function (<code>initialNumberOfMediaNodes</code>, <code>minNumberOfMediaNodes</code>, <code>maxNumberOfMediaNodes</code>, <code>scaleTargetCPU</code> and <code>scale_in_function_image</code> are ignored). If <code>0</code> (default), the deployment is elastic and autoscaling is enabled.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>initialNumberOfMediaNodes</code></td>
    <td style="white-space: nowrap;"><code>1</code></td>
    <td>Initial number of Media Nodes to deploy. Ignored when <code>fixedNumberOfMediaNodes &gt; 0</code>.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>minNumberOfMediaNodes</code></td>
    <td style="white-space: nowrap;"><code>1</code></td>
    <td>Minimum number of Media Nodes the autoscaling Instance Pool will keep running. Ignored when <code>fixedNumberOfMediaNodes &gt; 0</code>.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>maxNumberOfMediaNodes</code></td>
    <td style="white-space: nowrap;"><code>5</code></td>
    <td>Maximum number of Media Nodes the autoscaling Instance Pool can launch. Ignored when <code>fixedNumberOfMediaNodes &gt; 0</code>.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>scaleTargetCPU</code></td>
    <td style="white-space: nowrap;"><code>50</code></td>
    <td>Target CPU percentage that triggers scale-in/scale-out actions. Ignored when <code>fixedNumberOfMediaNodes &gt; 0</code>.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>scale_in_function_image</code></td>
    <td style="white-space: nowrap;"><code>mad.ocir.io/axp2ice0s7el/openvidu-scalein:main</code></td>
    <td>OCIR image URL consumed by the OCI Function that handles graceful Media Node scale-in. Defaults to the image published by OpenVidu in the Madrid OCIR. See <a href="#using-your-own-scale-in-function-image">Using your own scale-in function image</a> if you want to host it in your own registry. Ignored when <code>fixedNumberOfMediaNodes &gt; 0</code>.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>certificateType</code></td>
    <td style="white-space: nowrap;"><code>"letsencrypt"</code></td>
    <td>Certificate type for the OpenVidu deployment. Options: <ul><li><code>selfsigned</code> - Not recommended for production use. Intended for testing or development environments only. A FQDN is not required.</li><li><code>owncert</code> - Suitable for production environments. Uses your own certificate. A FQDN is required.</li><li><code>letsencrypt</code> - Suitable for production environments. Can be used with or without a FQDN (if no FQDN is provided, a random sslip.io domain will be used).</li></ul>
    <!-- TODO: Remove this warning when sslip.io rate limiting issue is resolved. Track at https://openvidu.discourse.group/t/deployment-without-domain/5474 -->
    <p><strong>Warning:</strong> sslip.io is currently experiencing Let's Encrypt rate limiting issues, which may prevent SSL certificates from being issued. It is recommended to use your own domain name. Check <a href="https://openvidu.discourse.group/t/deployment-without-domain/5474" target="_blank">this community thread</a> for troubleshooting and updates.</p>
    </td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>publicIpAddress</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>A previously created Reserved Public IP OCID to attach to the Network Load Balancer. Leave blank to generate a new public IP.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>domainName</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Domain name for the OpenVidu deployment. Optional — if not provided, a sslip.io domain will be used instead, derived from the NLB public IP.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>ownPublicCertificate</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>If the certificate type is <code>owncert</code>, this parameter specifies the public certificate in base64 format.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>ownPrivateCertificate</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>If the certificate type is <code>owncert</code>, this parameter specifies the private certificate in base64 format.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>initialMeetAdminPassword</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Initial password for the <code>admin</code> user in OpenVidu Meet. Alphanumeric characters only (A-Z, a-z, 0-9). If not provided, a random password will be generated.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>initialMeetApiKey</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Initial API key for OpenVidu Meet. Alphanumeric characters only (A-Z, a-z, 0-9). If not provided, no API key will be set; one can be configured later from the Meet Console.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>bucketAppDataName</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Name of an existing OCI Object Storage bucket for application data and recordings. If left empty, a bucket will be created with a default name.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>bucketClusterDataName</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Name of an existing OCI Object Storage bucket for cluster-wide shared state (including the generated SSH key). If left empty, a bucket will be created with a default name.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>rtcEngine</code></td>
    <td style="white-space: nowrap;"><code>"pion"</code></td>
    <td>WebRTC media engine to use. Options: <ul><li><code>pion</code> - Default media engine.</li><li><code>mediasoup</code> - Alternative media engine with different performance characteristics.</li></ul></td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>vault_ocid</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>OCI KMS Vault OCID for secrets management. If left empty, a new vault will be created.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>key_ocid</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>OCI KMS Key OCID for secrets management. If left empty, a new key will be created.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>additionalInstallFlags</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Additional optional flags to pass to the OpenVidu installer (comma-separated, e.g., <code>--flag1=value, --flag2</code>).</td>
    </tr>
    </tbody>
    </table>
    </div>

  </details>

3. Deploy with Terraform using the following commands:

    ```bash
    terraform init
    terraform apply
    ```

4. Logs will appear in the `terraform apply` console output. Wait for it to finish and display `Apply Complete!`. Then go to [OCI Object Storage :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/object-storage/buckets){:target=_blank} and wait for the SSH key to appear in your configured cluster-data bucket.

    !!! warning
        After downloading the SSH key, it is strongly recommended to **DELETE IT** from the bucket. This file is the private key used to access all 4 Master Nodes — if exposed, unauthorized users could gain access.

5. Set the correct permissions on the SSH key so it can be used.

    === "Linux"
        ```bash
        chmod 600 <PATH_TO_THE_KEY>/<STACK_NAME>-private-key.pem
        ```
    === "Powershell"
        ```powershell
        $KeyPath = "<PATH_TO_THE_KEY>" &&
        icacls $KeyPath /inheritance:r &&
        icacls $KeyPath /grant:r "$($env:USERNAME):(R)"
        ```

### Access OpenVidu

To verify that your OpenVidu deployment is working correctly, check the credentials in the OCI Vault Secrets Manager.

=== "View OpenVidu credentials in the Web"
    1. Navigate to the [OCI Secrets Manager :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/security/secrets){:target="_blank"} in the OCI Console.
    2. Click the secret you want to view.
    3. Scroll down to _"Versions"_, click the _"3 dots"_ menu next to the current version, and select _"View secret contents"_.

        !!! warning
            Click _"Show decoded Base64 digit"_ to see the actual value of the secret.

=== "View OpenVidu credentials in the instance"

    SSH into any of the Master Nodes by running the following command from the directory where your SSH key is located:
    ```bash
    ssh -i <STACK_NAME>-private-key.pem ubuntu@MASTER_NODE_PUBLIC_IP
    ```

    The public IPs of the 4 Master Nodes are listed in the `terraform apply` output as `openvidu_master_node_1_public_ip` … `openvidu_master_node_4_public_ip`. User traffic goes through the Network Load Balancer; the per-master public IPs are intended for SSH access only.

    Then navigate to `/opt/openvidu/config/` where you will find all credentials in the following files:

    - `openvidu.env`
    - `meet.env`

Open **OPENVIDU_URL** and you will see the OpenVidu Meet interface.

Log in with **MEET_INITIAL_ADMIN_PASSWORD** to start using OpenVidu Meet.

## Configure your application to use the deployment

To configure your OpenVidu application, you will need your OCI credentials. You can retrieve them by following the steps in [View OpenVidu credentials in the Web](#view-openvidu-credentials-in-the-web) or [View OpenVidu credentials in the instance](#view-openvidu-credentials-in-the-instance).

Your authentication credentials and the URL to point your applications to are:

--8<-- "shared/self-hosting/oracle-credentials-general.md"

### Troubleshooting initial Oracle Cloud Infrastructure deployment

--8<-- "shared/self-hosting/oracle-troubleshooting.md"

3. If everything appears to be in order, check the [status](../on-premises/admin.md#checking-the-status-of-services) and [logs](../on-premises/admin.md#checking-logs) of the installed OpenVidu services on all Master Nodes and Media Nodes.

### Configuration and administration

Once **OPENVIDU_URL** is reachable, the deployment is complete and working. See the [Administration](./admin.md) section to learn how to manage your OpenVidu High Availability deployment.
