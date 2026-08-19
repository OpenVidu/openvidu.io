---
title: "Install OpenVidu Elastic on DigitalOcean"
description: "Deploy OpenVidu Elastic on DigitalOcean with Terraform, then point your application at the result."
---

# OpenVidu Elastic installation: DigitalOcean

<div class="provider-chip" markdown>

:material-digital-ocean:{ .provider-chip-icon } DigitalOcean

</div>


--8<-- "self-hosting/common/elastic-license-intro.md"

This section describes how to deploy a production-ready OpenVidu Elastic instance on DigitalOcean. The deployed services are identical to those in the [On Premises Elastic installation](../on-premises/install.md), but are provisioned as DigitalOcean resources and can be automated using Terraform CLI.

- DigitalOcean **Spaces Object Storage** (S3-compatible) is used for storing application data, recordings.
- Media Node scalability is managed via an **automated process (DigitalOcean Functions)** that scales the number of Media Nodes based on system load, although you can use a fixed number of media nodes.

## Prerequisites

* You need to have a DigitalOcean account with a [Personal Access Token :fontawesome-solid-external-link:{.external-link-icon}](https://docs.digitalocean.com/reference/api/create-personal-access-token/){:target="_blank"}.
* You need to have installed [Terraform CLI :fontawesome-solid-external-link:{.external-link-icon}](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli){:target="_blank"}.
* You need to have installed Git.

=== "Architecture overview"

    This is what the deployment architecture looks like:

    ![OpenVidu Elastic DigitalOcean Architecture](../../../../assets/images/platform/self-hosting/elastic/digitalocean/elastic-architecture.svg){ .round-corners .dark-img loading=lazy }

    - The Master Node acts as a Load Balancer, managing the traffic and distributing it among the Media Nodes and deployed services in the Master Node.
    - The Master Node has its own Caddy server acting as a Layer 4 (for TURN with TLS and RTMPS) and Layer 7 (for OpenVidu Dashboard, OpenVidu Meet, etc., APIs) reverse proxy.
    - WebRTC traffic (SRTP/SCTP/STUN/TURN) is routed directly to the Media Nodes.
    - An automated process using DigitalOcean Functions handles the scale-in and scale-out of Media Nodes based on system load.

--8<-- "self-hosting/digitalocean/custom-scale-in.md"

## Deployment details

1. Clone the OpenVidu repository with the terraform files:
    ```bash
    git clone https://github.com/OpenVidu/openvidu-digitalocean.git
    git -C openvidu-digitalocean checkout 3.8.0
    cd openvidu-digitalocean/pro/elastic
    ```
2. Copy **terraform.tfvars.example** to **terraform.tfvars**, update the required parameters with your values, and optionally adjust defaults.

    ??? details "Information about parameters"

        ### Mandatory Parameters

        | Input Value | Description |
        |---|---|
        | `doToken`{ .nowrap } | DigitalOcean Personal Access Token for API authentication. |
        | `stackName`{ .nowrap } | Stack name for OpenVidu deployment. |
        | `openviduLicense`{ .nowrap } | OpenVidu License for PRO deployments. Go [here](https://openvidu.io/account){:target="_blank"} for more information. |

        ### Optional Parameters

        | Input Value | Default Value | Description |
        |---|---|---|
        | `region`{ .nowrap } | `"ams3"`{ .nowrap } | DigitalOcean region where resources will be created. |
        | `masterNodeInstanceType`{ .nowrap } | `"s-4vcpu-8gb"`{ .nowrap } | Specifies the DigitalOcean Droplet size for your Master Node. |
        | `mediaNodeInstanceType`{ .nowrap } | `"s-4vcpu-8gb"`{ .nowrap } | Specifies the DigitalOcean Droplet size for your Media Nodes. |
        | `initialNumberOfMediaNodes`{ .nowrap } | `1`{ .nowrap } | Number of initial media nodes to deploy. |
        | `minNumberOfMediaNodes`{ .nowrap } | `1`{ .nowrap } | Minimum number of media nodes to deploy (for reference, manual scaling required). |
        | `maxNumberOfMediaNodes`{ .nowrap } | `5`{ .nowrap } | Maximum number of media nodes to deploy (for reference, manual scaling required). |
        | `scaleTargetCPU`{ .nowrap } | `50`{ .nowrap } | Target CPU percentage to scale up or down. |
        | `fixedNumberOfMediaNodes`{ .nowrap } | `0`{ .nowrap } | Fixed number of media nodes to create (0 = use autoscaling). |
        | `rtcEngine`{ .nowrap } | `"pion"`{ .nowrap } | Media Engine. Available options: `pion`, `mediasoup`. |
        | `certificateType`{ .nowrap } | `"letsencrypt"`{ .nowrap } | Certificate type for OpenVidu deployment. Options: <ul><li>`selfsigned` - Not recommended for production use. Just for testing purposes or development environments. You don't need a FQDN to use this option.</li><li>`owncert` - Valid for production environments. Use your own certificate. You need a FQDN to use this option.</li><li>`letsencrypt` - Valid for production environments. Can be used with or without a FQDN (if no FQDN is provided, the public IP is used as the domain name and a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability){:target="_blank"} certificate is issued for it).</li></ul> |
        | `domainName`{ .nowrap } | `(none)`{ .nowrap } | Domain name for the OpenVidu Deployment. Not mandatory; if not provided, the public IP is used as the domain name. |
        | `ownPublicCertificate`{ .nowrap } | `(none)`{ .nowrap } | If certificate type is 'owncert', this parameter will be used to specify the public certificate in base64 format. |
        | `ownPrivateCertificate`{ .nowrap } | `(none)`{ .nowrap } | If certificate type is 'owncert', this parameter will be used to specify the private certificate in base64 format. |
        | `initialMeetAdminPassword`{ .nowrap } | `(none)`{ .nowrap } | Initial password for the 'admin' user in OpenVidu Meet. If not provided, a random password will be generated. |
        | `initialMeetApiKey`{ .nowrap } | `(none)`{ .nowrap } | Initial API key for OpenVidu Meet. If not provided, no API key will be set and the user can set it later from Meet Console. |
        | `spaceName`{ .nowrap } | `(none)`{ .nowrap } | Name of the DigitalOcean Space (S3-compatible bucket) to store application data and recordings. If empty, a bucket will be created with default name. |
        | `spaceRegion`{ .nowrap } | `"ams3"`{ .nowrap } | DigitalOcean Spaces region where the bucket will be created. |
        | `spacesAccessId`{ .nowrap } | `(none)`{ .nowrap } | Access key ID for DigitalOcean Spaces (S3-compatible). Required if spaceName is empty. |
        | `spacesSecretKey`{ .nowrap } | `(none)`{ .nowrap } | Secret access key for DigitalOcean Spaces (S3-compatible). Required if spaceName is empty. |
        | `additionalInstallFlags`{ .nowrap } | `(none)`{ .nowrap } | Additional optional flags to pass to the OpenVidu installer (comma-separated, e.g., '--flag1=value, --flag2'). Currently we only have one flag that is `--force-utc-timezone` to force UTC as the timezone for OpenVidu. By default, OpenVidu uses the timezone configured in the host machine where it is installed. Note that in general it is recommended to use UTC, and DigitalOcean Droplets already default to UTC, so this flag is not usually necessary. |

    !!! warning

        In DigitalOcean, you need [Space Access Keys :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.digitalocean.com/spaces/access_keys){:target="_blank"} to create a bucket. If you leave the **spaceName** variable empty, you must configure these keys with full access so a new bucket can be created. [Here is how :fontawesome-solid-external-link:{.external-link-icon}](https://docs.digitalocean.com/products/spaces/how-to/manage-access/#access-keys){:target="_blank"}.
        
1. Use the following commands to deploy with terraform.
  ```bash
  terraform init
  terraform apply
  ```
1. You will see logs appear in the terraform apply execution console. Wait for it to finish and display `Apply Complete!`. Now go to [Space Object Storage](https://cloud.digitalocean.com/spaces){:target="_blank"} and wait for the ssh key to appear in the bucket you have configured.   

    !!! warning
        After downloading the SSH key, it is highly recommended to **DELETE IT** from the bucket. This file is the private key used to access the droplet. If exposed, unauthorized users could gain access to the instance.

    ![SSH Key in Bucket](../../../../assets/images/platform/self-hosting/elastic/digitalocean/bucket-ssh-key.png){ .round-corners loading=lazy }

2. Give the SSH Key the necessary permissions for it to work.

    === "Linux"
        Command in Linux:
        ```
        chmod 600 <PATH_TO_THE_KEY>/openvidu_ssh_key_elastic.pem
        ```
    === "Powershell"
        Command in powershell:
        ```
        $KeyPath = "<PATH_TO_THE_KEY>" &&
        icacls $KeyPath /inheritance:r &&
        icacls $KeyPath /grant:r "$($env:USERNAME):(R)"
        ```

### Access OpenVidu

To verify that your OpenVidu deployment works correctly wait for the `secrets.env` to appear in the bucket that you've configured and open it to view the credentials of OpenVidu.

=== "View OpenVidu credentials in the Web"
    Go to the Space Object Storage bucket that you've configured and download the `secrets.env` file.

    ![Secrets.env in Bucket](../../../../assets/images/platform/self-hosting/elastic/digitalocean/secrets-env.png){ .round-corners loading=lazy }


=== "View OpenVidu credentials in the instance"

    SSH to the instance by running this command from the directory where your SSH key is located:
    ```
    ssh -i openvidu_ssh_key_elastic.pem root@PUBLIC_DROPLET_IP
    ```

    Then navigate to /opt/openvidu/ and you will find all credentials needed in the `secrets.env`.

Then open **OPENVIDU_URL** and you will see the OpenVidu Meet interface. Log in with **MEET_INITIAL_ADMIN_PASSWORD** and you will be able to enjoy the features of OpenVidu Meet.

## Configure your application to use the deployment 

You may need your Digital Ocean credentials to configure your OpenVidu application. You can check these secrets following these steps ([View OpenVidu credentials in the Web](#view-openvidu-credentials-in-the-web)) or ([View OpenVidu credentials in the instance](#view-openvidu-credentials-in-the-instance)).

Your authentication credentials and the URL to point your applications to are:

--8<-- "self-hosting/digitalocean/credentials-general.md"
--8<-- "self-hosting/digitalocean/credentials-v2compatibility.md"

### Troubleshooting initial DigitalOcean deployment creation

--8<-- "self-hosting/digitalocean/troubleshooting.md"

3. If everything seems fine, check the [status](../on-premises/admin.md#checking-the-status-of-services) and the [logs](../on-premises/admin.md#checking-logs) of the installed OpenVidu services.

### Configuration and administration

When your **OPENVIDU_URL** is reachable, it means that everything has gone well. Now you can check the [Administration](./admin.md) section to learn how to manage your deployment.
