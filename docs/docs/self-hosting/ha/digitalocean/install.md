---
title: OpenVidu High Availability installation on Digital Ocean
description: Learn how to deploy OpenVidu High Availability on Digital Ocean
tags:
  - copyclipboard
---

# OpenVidu High Availability installation: Digital Ocean

!!! info
    
    OpenVidu High Availability is part of **OpenVidu <span class="openvidu-tag openvidu-pro-tag" style="font-size: 12px; vertical-align: top;">PRO</span>**. Before deploying, you need to [create an OpenVidu account](/account/){:target=_blank} to get your license key.
    There's a 15-day free trial waiting for you!

This section contains the instructions to deploy a production-ready OpenVidu High Availability deployment in Digital Ocean. Deployed services are the same as the [On Premises High Availability installation](../on-premises/install.md) but they will be resources in Digital Ocean and you can automate the process with Terraform CLI.

## Prerequisites

* You need to have a Digital Ocean account with a [Personal Access Token :fontawesome-solid-external-link:{.external-link-icon}](https://docs.digitalocean.com/reference/api/create-personal-access-token/){:target=_blank}.
* You need to have installed [Terraform CLI :fontawesome-solid-external-link:{.external-link-icon}](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli){:target=_blank}.
* You need to have installed Git.

=== "Architecture overview"

    This is how the architecture of the deployment looks like:

    <figure markdown>
    ![OpenVidu High Availability Digital Ocean Architecture](../../../../assets/images/self-hosting/ha/digitalocean/ha-do-architecture.svg){ .svg-img .dark-img }
    <figcaption>OpenVidu High Availability Digital Ocean Architecture</figcaption>
    </figure>

    - The Load Balancer distributes HTTPS traffic to the Master Nodes.
    - If RTMP media is ingested, the Load Balancer also routes this traffic to the Master Nodes that they act as a bridge.
    - WebRTC traffic (SRTP/SCTP/STUN/TURN) is routed directly to the Media Nodes.
    - 4 fixed Droplets are created for the Master Nodes. It must always be 4 Master Nodes to ensure high availability.


--8<-- "shared/self-hosting/do-custom-scale-in.md"

## Deployment details
1. To deploy OpenVidu, first you need clone the repository that lodges the terraform files. You can do that with the following command in a terminal:
    ```
    git clone https://github.com/OpenVidu/openvidu-digitalocean.git \
    && cd openvidu-digitalocean/pro/ha
    ```
2. Copy **terraform.tfvars.example** to **terraform.tfvars**, update the required parameters with your values, and optionally adjust defaults, then proceed to the next step.
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
    <td style="white-space: nowrap;"><code>do_token</code></td>
    <td>Digital Ocean Personal Access Token for API authentication.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>stackName</code></td>
    <td>Stack name for OpenVidu deployment.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>openviduLicense</code></td>
    <td>OpenVidu License for PRO deployments. Go <a href="https://openvidu.io/account" target="_blank">here</a> for more information.</td>
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
    <td style="white-space: nowrap;"><code>"ams3"</code></td>
    <td>Digital Ocean region where resources will be created.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>masterNodesInstanceType</code></td>
    <td style="white-space: nowrap;"><code>"s-4vcpu-8gb"</code></td>
    <td>Specifies the Digital Ocean Droplet size for your Master Node.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>mediaNodeInstanceType</code></td>
    <td style="white-space: nowrap;"><code>"s-4vcpu-8gb"</code></td>
    <td>Specifies the Digital Ocean Droplet size for your Media Nodes.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>fixedNumberOfMediaNodes</code></td>
    <td style="white-space: nowrap;"><code>4</code></td>
    <td>Fixed number of Media Nodes.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>rtcEngine</code></td>
    <td style="white-space: nowrap;"><code>"pion"</code></td>
    <td>Media Engine. Available options: <code>pion</code>, <code>mediasoup</code>.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>certificateType</code></td>
    <td style="white-space: nowrap;"><code>"letsencrypt"</code></td>
    <td>Certificate type for OpenVidu deployment. Options: <ul><li><code>selfsigned</code> - Not recommended for production use. Just for testing purposes or development environments. You don't need a FQDN to use this option.</li><li><code>owncert</code> - Valid for production environments. Use your own certificate. You need a FQDN to use this option.</li><li><code>letsencrypt</code> - Valid for production environments. Can be used with or without a FQDN (if no FQDN is provided, a random sslip.io domain will be used).</li></ul></td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>domainName</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Domain name for the OpenVidu Deployment.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>ownPublicCertificate</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>If certificate type is 'owncert', this parameter will be used to specify your public certificate in base64.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>ownPrivateCertificate</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>If certificate type is 'owncert', this parameter will be used to specify your private certificate in base64.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>initialMeetAdminPassword</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Initial password for the 'admin' user in OpenVidu Meet. If not provided, a random password will be generated.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>initialMeetApiKey</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Initial API key for OpenVidu Meet. If not provided, no API key will be set and the user can set it later from Meet Console.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>volumeSize</code></td>
    <td style="white-space: nowrap;"><code>100</code></td>
    <td>Size of the additional volume in GB for Master Node.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>spaceAppDataName</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Name of the DigitalOcean Space (S3-compatible bucket) to store application data and recordings. If empty, a bucket will be created with default name.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>spaceClusterDataName</code></td>
    <td style="white-space: nowrap;"><code>(none)</code></td>
    <td>Name of the DigitalOcean Space (S3-compatible bucket) to store cluster data. If empty, a bucket will be created with default name.</td>
    </tr>
    <tr>
    <td style="white-space: nowrap;"><code>spaceRegion</code></td>
    <td style="white-space: nowrap;"><code>"ams3"</code></td>
    <td>Digital Ocean Spaces region where the bucket will be created.</td>
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
3. Use the following commands to deploy with terraform.
  ```
  terraform init && terraform apply
  ```
4. Wait until in the Space Object Storage bucket that you've configurated appears the SSH Key.

    !!! warning
        Once you've downloaded that SSH Key please **DELETE IT** from the bucket. This SSH Key is the private key used to connect to the droplet so if someone gets it, they could be capable of entering the instance.

5. Go to where you downloaded your SSH Key and run the following command:
  ```
  chmod 600 your_private_key.pem
  ```

## Checking credentials

After waiting about 5 to 10 minutes to let the droplet run the installation of OpenVidu you can check the credentials in the instance.

=== "Check deployment outputs in the instance"

    SSH to the instance by running this command in the path where you have the SSH Key:
    ```
    ssh -i your_private_key.pem root@PUBLIC_DROPLET_IP
    ```

    Then navigate to /opt/openvidu/ and you will find all credentials needed in the `secrets.env`

=== "Check deployment outputs in the Web"

    - Go to the Space Object Storage bucket that you've configurated and download the `secrets.env` file.

## Configure your application to use the deployment 

You may need your Digital Ocean credentials to configure your OpenVidu application. You can check these secrets following these steps ([Check deployment outputs in the instance](#check-deployment-outputs-in-the-instance)) or by ([Check deployment outputs in the web](#check-deployment-outputs-in-the-web)).

Your authentication credentials and URL to point your applications would be:

--8<-- "shared/self-hosting/do-credentials-general.md"
--8<-- "shared/self-hosting/do-credentials-v2compatibility.md"

### Troubleshooting initial Digital Ocean deployment creation

--8<-- "shared/self-hosting/do-troubleshooting.md"

3. If everything seems fine, check the [status](../on-premises/admin.md#checking-the-status-of-services) and the [logs](../on-premises/admin.md#checking-logs) of the installed OpenVidu services.

### Configuration and administration

When your **OPENVIDU_URL** is reachable, it means that everything has gone well. Now you can check the [Administration](./admin.md) section to learn how to manage your deployment.
