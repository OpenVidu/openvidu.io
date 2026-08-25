---
title: "Install OpenVidu Single Node PRO on Oracle Cloud"
description: "Deploy OpenVidu Single Node PRO on Oracle Cloud Infrastructure from the web console or with Terraform, then point your application at the result."
---

# OpenVidu Single Node **PRO**{ .openvidu-tag .openvidu-pro-tag .openvidu-tag-heading } installation: Oracle Cloud Infrastructure

--8<-- "self-hosting/oracle/provider-chip.md"

This section describes two ways to install OpenVidu Single Node on Oracle Cloud Infrastructure:

* [**Web Console**](#web-console): Can be deployed without installing anything on your machine, but requires more manual steps and has some limitations. For example, recordings are stored on the machine itself rather than in OCI Object Storage.
* [**Terraform**](#terraform): More powerful and fully automated, but requires the Terraform CLI to be installed on your machine.


## Web Console

This page explains how to create a Compute instance in Oracle Cloud Infrastructure (OCI), configure networking, and prepare it for an OpenVidu Single Node PRO On-Premises installation. Installing, administering, and upgrading OpenVidu Single Node PRO itself is covered in the On-Premises documentation.

--8<-- "self-hosting/oracle/single-node/webconsole-steps.md"

6. Follow the [On-Premises install instructions](../on-premises/install.md) to install OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag .openvidu-tag-heading } on the instance.

---

### 5. Administration and upgrade

- For administration of this OpenVidu Single Node PRO deployment, see the [Administration](./admin.md) section.
- To upgrade OpenVidu, see the [Upgrade](../upgrade.md) section.

## Terraform

This section contains instructions for deploying a production-ready OpenVidu Single Node **PRO**{ .openvidu-tag .openvidu-pro-tag style="font-size: 12px" } deployment on Oracle Cloud Infrastructure. The deployed services are the same as in the [On-Premises Single Node installation](../on-premises/install.md), but the process is fully automated through the Terraform CLI. OCI Object Storage is used to store recordings and other persistent data.

--8<-- "self-hosting/oracle/single-node/terraform-architecture.md"

### Deployment details

1. Clone the OpenVidu repository containing the Terraform files:

    ```bash
    git clone https://github.com/OpenVidu/openvidu-oracle.git
    git -C openvidu-oracle checkout 3.8.0
    cd openvidu-oracle/pro/singlenode
    ```

2. Copy **`terraform.tfvars.example`** to **`terraform.tfvars`**, update the required parameters with your values, and adjust any optional defaults as needed.

    ??? details "Information about parameters"

        #### Mandatory Parameters

        | Input Value | Description |
        |---|---|
        | `tenancy_ocid`{ .nowrap } | OCI Tenancy OCID. Required for the Object Storage namespace. |
        | `compartment_ocid`{ .nowrap } | OCI Compartment OCID where resources will be created. |
        | `user_ocid`{ .nowrap } | OCI User OCID used to create Customer Secret Keys for S3-compatible access to Object Storage. |
        | `stackName`{ .nowrap } | Stack name for the OpenVidu deployment. |
        | `openviduLicense`{ .nowrap } | OpenVidu PRO license key. Visit [https://openvidu.io/account :fontawesome-solid-external-link:{.external-link-icon}](../../../../account.md){:target="_blank"} to obtain your license. |

        #### Optional Parameters

        | Input Value | Default Value | Description |
        |---|---|---|
        | `region`{ .nowrap } | `"eu-frankfurt-1"`{ .nowrap } | OCI region where resources will be created. |
        | `availability_domain`{ .nowrap } | `1`{ .nowrap } | Availability Domain number (1, 2, or 3) to use for resources. |
        | `instanceType`{ .nowrap } | `"VM.Standard.E4.Flex"`{ .nowrap } | OCI Compute shape for the OpenVidu instance. |
        | `instanceOCPUs`{ .nowrap } | `4`{ .nowrap } | Number of OCPUs for the instance (applies to Flex shapes only). |
        | `instanceMemory`{ .nowrap } | `4`{ .nowrap } | Memory in GB for the instance (applies to Flex shapes only). |
        | `certificateType`{ .nowrap } | `"letsencrypt"`{ .nowrap } | Certificate type for the OpenVidu deployment. Options: <ul><li>`selfsigned` - Not recommended for production use. Intended for testing or development environments only. A FQDN is not required.</li><li>`owncert` - Suitable for production environments. Uses your own certificate. A FQDN is required.</li><li>`letsencrypt` - Suitable for production environments. Can be used with or without a FQDN (if no FQDN is provided, the public IP is used as the domain name and a [Let's Encrypt :fontawesome-solid-external-link:{.external-link-icon}](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability){:target="_blank"} certificate is issued for it).</li></ul> |
        | `domainName`{ .nowrap } | `(none)`{ .nowrap } | Domain name for the OpenVidu deployment. Optional — if not provided, the public IP is used as the domain name. |
        | `ownPublicCertificate`{ .nowrap } | `(none)`{ .nowrap } | If the certificate type is `owncert`, this parameter specifies the public certificate in base64 format. |
        | `ownPrivateCertificate`{ .nowrap } | `(none)`{ .nowrap } | If the certificate type is `owncert`, this parameter specifies the private certificate in base64 format. |
        | `initialMeetAdminPassword`{ .nowrap } | `(none)`{ .nowrap } | Initial password for the `admin` user in OpenVidu Meet. Alphanumeric characters, underscores or hyphens only (A-Z, a-z, 0-9, _, -). If not provided, a random password will be generated. |
        | `initialMeetApiKey`{ .nowrap } | `(none)`{ .nowrap } | Initial API key for OpenVidu Meet. Alphanumeric characters, underscores or hyphens only (A-Z, a-z, 0-9, _, -). If not provided, no API key will be set; one can be configured later from the Meet Console. |
        | `bucketName`{ .nowrap } | `(none)`{ .nowrap } | Name of the OCI Object Storage bucket for application data and recordings. If left empty, a bucket will be created with a default name. |
        | `RTCEngine`{ .nowrap } | `"pion"`{ .nowrap } | WebRTC media engine to use. Options: <ul><li>`pion` - Default media engine.</li><li>`mediasoup` - Alternative media engine with different performance characteristics.</li></ul> |
        | `vault_ocid`{ .nowrap } | `(none)`{ .nowrap } | OCI KMS Vault OCID for secrets management. If left empty, a new vault will be created. |
        | `key_ocid`{ .nowrap } | `(none)`{ .nowrap } | OCI KMS Key OCID for secrets management. If left empty, a new key will be created. |
        | `additionalInstallFlags`{ .nowrap } | `(none)`{ .nowrap } | Additional optional flags to pass to the OpenVidu installer (comma-separated, e.g., `--flag1=value, --flag2`). |

3. Deploy with Terraform using the following commands:

    ```bash
    terraform init
    terraform apply
    ```

4. Logs will appear in the `terraform apply` console output. Wait for it to finish and display `Apply Complete!`. Then go to [OCI Object Storage :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/object-storage/buckets){:target="_blank"} and wait for the SSH key to appear in your configured bucket.

    !!! warning
        After downloading the SSH key, it is strongly recommended to **DELETE IT** from the bucket. This file is the private key used to access the instance — if exposed, unauthorized users could gain access.

    ![SSH Key in bucket](../../../../assets/images/platform/self-hosting/single-node/oracle/bucket-ssh-key-pro.png){ .round-corners loading=lazy }

5. Set the correct permissions on the SSH key so it can be used.

--8<-- "self-hosting/oracle/ssh-key-permissions.md"

--8<-- "self-hosting/oracle/single-node/access-openvidu.md"

--8<-- "self-hosting/oracle/single-node/configure-app.md"