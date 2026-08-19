---
title: "Install OpenVidu Single Node COMMUNITY on Google Cloud"
description: "Deploy OpenVidu Single Node COMMUNITY on Google Cloud from a deployment stack in the Google Cloud console, then point your application at the result."
---

# OpenVidu Single Node **COMMUNITY**{ .openvidu-tag .openvidu-community-tag .openvidu-tag-heading } installation: Google Cloud Platform

<div class="provider-chip" markdown>

:material-google-cloud:{ .provider-chip-icon } Google Cloud Platform

</div>


This section contains instructions for deploying a production-ready OpenVidu Single Node **COMMUNITY**{ .openvidu-tag .openvidu-community-tag style="font-size: 12px" } deployment on Google Cloud Platform. The deployed services are the same as in the [On Premises Single Node installation](../on-premises/install.md), but the process is automated through the Google Cloud Console.

To deploy OpenVidu on Google Cloud Platform, log in to [Infrastructure Manager :fontawesome-solid-external-link:{.external-link-icon}](https://console.cloud.google.com/infra-manager/deployments){:target="_blank"} in the GCP Console. Then follow the next steps and fill in your preferred parameters.

=== "Architecture overview"

    This is what the deployment architecture looks like:

    ![OpenVidu Single Node Google Cloud Platform Architecture](../../../../assets/images/platform/self-hosting/single-node/gcp/single-node-architecture.svg){ .round-corners .dark-img loading=lazy }

## Deployment details

--8<-- "self-hosting/gcp/info-deployment.md"

To deploy OpenVidu, first create a new deployment using the top-left button, as shown in the image.

![Google Cloud Platform create new deployment](../../../../assets/images/platform/self-hosting/shared/gcp/create-deployment.png){ .round-corners loading=lazy }

Once you click the button, you will see this window.

![Google Cloud Platform create new deployment window](../../../../assets/images/platform/self-hosting/shared/gcp/create-deployment-window.png){ .round-corners loading=lazy }

* Fill **Deployment ID** with any name you prefer (for example, openvidu-singlenode-deployment).   
* Change the **Region** to the one you prefer.
!!! warning

    If you change the region in the previous step, don't forget to update the [region and zone :fontawesome-solid-external-link:{.external-link-icon}](https://docs.cloud.google.com/compute/docs/regions-zones?hl=en){:target="_blank"} in the Terraform values.

* Leave **Terraform version** as 1.5.7.   
* For **Service Account**, you will need to create a new one with _"Owner"_ permissions. To do this, click the _"Service Account"_ label and then _"New Service Account"_. Choose your service account name, click _"Create and Continue"_, select the _"Owner"_ role, click _"Continue"_, and then _"Done"_.   
??? details "New Service Account Steps"

    ![Google Cloud Platform create new Service Account step 1](../../../../assets/images/platform/self-hosting/shared/gcp/create-service-account-1.png){ .round-corners loading=lazy }
    /// caption
    Step 1: Create Service Account
    ///

    ![Google Cloud Platform create new Service Account step 2](../../../../assets/images/platform/self-hosting/shared/gcp/create-service-account-2.png){ .round-corners loading=lazy }
    /// caption
    Step 2: Service Account Details
    ///

    ![Google Cloud Platform create new Service Account step 3](../../../../assets/images/platform/self-hosting/shared/gcp/create-service-account-3.png){ .round-corners loading=lazy }
    /// caption
    Step 3: Grant Permissions
    ///

    ![Google Cloud Platform create new Service Account step 4](../../../../assets/images/platform/self-hosting/shared/gcp/create-service-account-4.png){ .round-corners loading=lazy }
    /// caption
    Step 4: Complete Setup
    ///

* Fill **Git repository** with this link, which corresponds to our Git repository where the Terraform files to deploy OpenVidu are located:

    ```
    https://github.com/OpenVidu/openvidu.git
    ```

* Fill the **Git directory** with the following path:

    ```
    openvidu-deployment/community/singlenode/gcp
    ```

* For the **Git ref**, use the version you want to deploy:

    ```
    v3.8.0
    ```

Finally, click Continue.

## Input Values

In Google Cloud Platform, there is no built-in template with parameters. You need to manually enter the parameters declared in our Terraform files into the console, so below is a detailed table of all optional and mandatory parameters.

### Mandatory Parameters
| Input Value | Description |
|---|---|
| projectId | GCP project id where the resources will be created. |
| stackName | Stack name for OpenVidu deployment. |

### Optional Parameters
| Input Value | Default Value | Description |
|---|---|---|
| region | "europe-west2" | GCP region where resources will be created. |
| zone | "europe-west2-b" | GCP zone that some resources will use. |
| certificateType | "letsEncrypt" | Certificate type for OpenVidu deployment. Options: <ul> <li>**[selfsigned]** Not recommended for production use. Just for testing purposes or development environments. You don't need a FQDN to use this option.</li> <li>**[owncert]** Valid for production environments. Use your own certificate. You need a FQDN to use this option.</li> <li>**[letsencrypt]** Valid for production environments. Can be used with or without a FQDN (if no FQDN is provided, the public IP is used as the domain name and a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability){:target="_blank"} certificate is issued for it).</li> </ul> |
| publicIpAddress | (none) | Previously created Public IP address for the OpenVidu Deployment. Blank will generate a public IP. |
| domainName | (none) | Domain name for the OpenVidu Deployment. |
| ownPublicCertificate | (none) | If certificate type is 'owncert', this parameter will be used to specify the public certificate in base64 format. |
| ownPrivateCertificate | (none) | If certificate type is 'owncert', this parameter will be used to specify the private certificate in base64 format. |
| initialMeetAdminPassword | (none) | Initial password for the 'admin' user in OpenVidu Meet. If not provided, a random password will be generated. |
| initialMeetApiKey | (none) | Initial API key for OpenVidu Meet. If not provided, no API key will be set and the user can set it later from Meet Console. |
| instanceType | "e2-standard-2" | Specifies the GCE machine type for your OpenVidu instance. |
| bucketName | (none) | Name of the GCS bucket to store data and recordings. If empty, a bucket will be created. |
| additionalInstallFlags | (none) | Additional optional flags to pass to the OpenVidu installer (comma-separated, e.g., '--flag1=value, --flag2'). |

For more details, you can check the [variables.tf :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/OpenVidu/openvidu/blob/master/openvidu-deployment/community/singlenode/gcp/variables.tf){:target="_blank"} file to see additional information about the inputs.   

!!! warning
    It's important that you enter the input variables with the exact same names as they appear in the table, as shown in the next image.

    ![Google Cloud Platform input variables](../../../../assets/images/platform/self-hosting/shared/gcp/input-variables.png){ .round-corners loading=lazy }

## Deploying the stack

--8<-- "self-hosting/gcp/deploying-stack.md"

## Configure your application to use the deployment 

You need the secret outputs from Google Cloud Platform to configure your OpenVidu application. You can check these secrets in Secret Manager using either of these two methods: ([Check deployment outputs in GCP Secret Manager](#check-deployment-outputs-in-gcp-secret-manager)) or ([Check deployment outputs in the instance](#check-deployment-outputs-in-the-instance)).

Your authentication credentials and the URL to point your applications to are:

--8<-- "self-hosting/gcp/credentials-general.md"

## Troubleshooting initial Google Cloud Platform deployment creation

--8<-- "self-hosting/gcp/troubleshooting.md"

3. If everything seems fine, check the [status](../on-premises/admin.md#checking-the-status-of-services) and the [logs](../on-premises/admin.md#checking-logs) of the installed OpenVidu services.

## Configuration and administration

When your Google Cloud Platform deployment reaches the **`Active`** state, it means that all resources have been created. You will need to wait around 5 to 10 minutes for the instance to install OpenVidu, as mentioned before. After this time, try connecting to the deployment URL. If it doesn't work, we recommend checking the previous section. Once everything is ready, you can check the [Administration](./admin.md) section to learn how to manage your deployment.
