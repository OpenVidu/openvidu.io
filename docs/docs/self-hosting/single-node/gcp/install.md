---
title: OpenVidu Single Node installation on Google Cloud Platform
description: Learn how to deploy OpenVidu Single Node on Google Cloud Platform using Google Cloud Platform Console
tags:
  - copyclipboard
---

# OpenVidu Single Node <span class="openvidu-tag openvidu-community-tag" style="font-size: .6em; vertical-align: text-bottom">COMMUNITY</span> installation: Google Cloud Platform

This section contains the instructions to deploy a production-ready OpenVidu Single Node <span class="openvidu-tag openvidu-community-tag" style="font-size: 12px">COMMUNITY</span> deployment in Google Cloud Platform. Deployed services are the same as the [On Premises Single Node installation](../on-premises/install.md) but automate the process with Google Cloud Console.

To deploy OpenVidu into Google Cloud Platform you just need to log into your [Infrastructure Manager :fontawesome-solid-external-link:{.external-link-icon}](https://console.cloud.google.com/infra-manager/deployments){:target=_blank} in the GCP console. Then follow the next steps to fill the parameters of your choice.

=== "Architecture overview"

    This is how the architecture of the deployment looks like:

    <figure markdown>
    ![OpenVidu Single Node Google Cloud Platform Architecture](../../../../assets/images/self-hosting/single-node/gcp/single-node-gcp-architecture.svg){ .svg-img .dark-img }
    <figcaption>OpenVidu Single Node Google Cloud Platform Architecture</figcaption>
    </figure>

## Deployment details

--8<-- "shared/self-hosting/gcp-info-deployment.md"

To deploy OpenVidu, first you need to create a new deployment in the top left button as you can see in the image.

<figure markdown>
![Google Cloud Platform create new deployment](../../../../assets/images/self-hosting/shared/gcp-create-deployment.png){ .svg-img .dark-img }
</figure>

Once you click the button you will see this window.

<figure markdown>
![Google Cloud Platform create new deployment window](../../../../assets/images/self-hosting/shared/gcp-create-deployment-window.png){ .svg-img .dark-img }
</figure>

* Fill **Deployment ID** with any name that you desire (for example openvidu-singlenode-deployment).   
* Change the **Region** for the one that you prefer.
!!! warning
    If you change the region in the previous step, don't forget to change the [region and zone :fontawesome-solid-external-link:{.external-link-icon}](https://docs.cloud.google.com/compute/docs/regions-zones?hl=en){:target=_blank} in the terraform values.

* Leave **Terraform version** in the 1.5.7.   
* For **Service Account** you will need to create a new one with _"Owner"_ permissions, in order to do that click on _"Service Account"_ label and then into _"New Service Account"_, choose your service account name click on _"Create and Continue"_ and then select the _"Owner"_ role, click on _"Continue"_ and the in _"Done"_.   
??? details "New Service Account Steps"

    <figure markdown>
    ![Google Cloud Platform create new Service Account step 1](../../../../assets/images/self-hosting/shared/gcp-create-service-account-1.png){ .svg-img .dark-img }
    <figcaption>Step 1: Create Service Account</figcaption>
    </figure>

    <figure markdown>
    ![Google Cloud Platform create new Service Account step 2](../../../../assets/images/self-hosting/shared/gcp-create-service-account-2.png){ .svg-img .dark-img }
    <figcaption>Step 2: Service Account Details</figcaption>
    </figure>

    <figure markdown>
    ![Google Cloud Platform create new Service Account step 3](../../../../assets/images/self-hosting/shared/gcp-create-service-account-3.png){ .svg-img .dark-img }
    <figcaption>Step 3: Grant Permissions</figcaption>
    </figure>

    <figure markdown>
    ![Google Cloud Platform create new Service Account step 4](../../../../assets/images/self-hosting/shared/gcp-create-service-account-4.png){ .svg-img .dark-img }
    <figcaption>Step 4: Complete Setup</figcaption>
    </figure>

* Fill **Git repository** with this link <span class="copy-inline" data-copy="https://github.com/OpenVidu/openvidu.git"><code>https://github.com/OpenVidu/openvidu.git</code><span class="copy-btn" title="Copy">:material-content-copy:</span></span> that corresponds to our git repository where are allocated the terraform files to deploy openvidu. 
* Fill the **Git directory** with the following path <span class="copy-inline" data-copy="openvidu-deployment/community/singlenode/gcp"><code>openvidu-deployment/community/singlenode/gcp</code><span class="copy-btn" title="Copy">:material-content-copy:</span></span> 
* For the **Git ref** use <span class="copy-inline" data-copy="v3.5.0"><code>v3.5.0</code><span class="copy-btn" title="Copy">:material-content-copy:</span></span> corresponding to the version 

Finally click on continue.

## Input Values

In Google Cloud Platform there is no such thing like template with parameters, you will need to introduce by yourself in the console the parameters that are declared in our terraform files, so there is a detailed table of all the optional and non-optional parameters.

### Mandatory Parameters
<div style="text-align: center;">
    <table border="1" cellspacing="0" cellpadding="6" style="margin: 0 auto;">
      <tr>
        <th>Input Value</th>
        <th>Description</th>
      </tr>
      <tr>
        <td>projectId</td>
        <td>GCP project id where the resources will be created.</td>
      </tr>
      <tr>
        <td>stackName</td>
        <td>Stack name for OpenVidu deployment.</td>
      </tr>
    </table>
</div>

### Optional Parameters
<div style="text-align: center;">
    <table border="1" cellspacing="0" cellpadding="6" style="margin: 0 auto;">
      <tr>
        <th>Input Value</th>
        <th>Default Value</th>
        <th>Description</th>
      </tr>
      <tr>
        <td>region</td>
        <td>"europe-west2"</td>
        <td>GCP region where resources will be created.</td>
      </tr>
      <tr>
        <td>zone</td>
        <td>"europe-west2-b"</td>
        <td>GCP zone that some resources will use.</td>
      </tr>
      <tr>
        <td>certificateType</td>
        <td>"letsEncrypt"</td>
        <td>Certificate type for OpenVidu deployment. Options:
          <ul>
            <li><strong>[selfsigned]</strong> Not recommended for production use. Just for testing purposes or development environments. You don't need a FQDN to use this option.</li>
            <li><strong>[owncert]</strong> Valid for production environments. Use your own certificate. You need a FQDN to use this option.</li>
            <li><strong>[letsencrypt]</strong> Valid for production environments. Can be used with or without a FQDN (if no FQDN is provided, a random sslip.io domain will be used).</li>
          </ul>
              </td>    </tr>
      <tr>
      <tr>
        <td>publicIpAddress</td>
        <td>(none)</td>
        <td>Previously created Public IP address for the OpenVidu Deployment. Blank will generate a public IP.</td>
      </tr>
      <tr>
        <td>domainName</td>
        <td>(none)</td>
        <td>Domain name for the OpenVidu Deployment.</td>
      </tr>
      <tr>
        <td>ownPublicCertificate</td>
        <td>(none)</td>
        <td>If certificate type is 'owncert', this parameter will be used to specify the public certificate in base64 format.</td>
      </tr>
      <tr>
        <td>ownPrivateCertificate</td>
        <td>(none)</td>
        <td>If certificate type is 'owncert', this parameter will be used to specify the private certificate in base64 format.</td>
      </tr>
      <tr>
        <td>initialMeetAdminPassword</td>
        <td>(none)</td>
        <td>Initial password for the 'admin' user in OpenVidu Meet. If not provided, a random password will be generated.</td>
      </tr>
      <tr>
        <td>initialMeetApiKey</td>
        <td>(none)</td>
        <td>Initial API key for OpenVidu Meet. If not provided, no API key will be set and the user can set it later from Meet Console.</td>
      </tr>
      <tr>
        <td>instanceType</td>
        <td>"e2-standard-2"</td>
        <td>Specifies the GCE machine type for your OpenVidu instance.</td>
      </tr>
      <tr>
        <td>bucketName</td>
        <td>(none)</td>
        <td>Name of the GCS bucket to store data and recordings. If empty, a bucket will be created.</td>
      </tr>
      <tr>
        <td>additionalInstallFlags</td>
        <td>(none)</td>
        <td>Additional optional flags to pass to the OpenVidu installer (comma-separated, e.g., '--flag1=value, --flag2').</td>
      </tr>
    </table>
</div>

For more detail you can check the [variables.tf :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/OpenVidu/openvidu/blob/master/openvidu-deployment/community/singlenode/gcp/variables.tf){:target=_blank} file to see more information about the inputs.   

!!! warning
    It's important that you put the input variables with the same name as they appear in the table like in the next image.

    <figure markdown>
    ![Google Cloud Platform input variables](../../../../assets/images/self-hosting/shared/gcp-input-variables.png){ .svg-img .dark-img }
    </figure>

## Deploying the stack

--8<-- "shared/self-hosting/gcp-deploying-stack.md"

## Configure your application to use the deployment 

You need your Google Cloud Platform secret outputs to configure your OpenVidu application. You can check these secrets by searching in the Secrets Manager with any of these two ways ([Check deployment outputs in GCP Secret Manager](#check-deployment-outputs-in-gcp-secret-manager)) or ([Check deployment outputs in the instance](#check-deployment-outputs-in-the-instance)).

Your authentication credentials and URL to point your applications would be:

--8<-- "shared/self-hosting/gcp-credentials-general.md"

## Troubleshooting initial Google Cloud Platform deployment creation

--8<-- "shared/self-hosting/gcp-troubleshooting.md"

3. If everything seems fine, check the [status](../on-premises/admin.md#checking-the-status-of-services) and the [logs](../on-premises/admin.md#checking-logs) of the installed OpenVidu services.

## Configuration and administration

When your Google Cloud Platform deployment reaches the **`Active`** state, it means that all the resources have been created. You will need to wait around 5 to 10 minutes for the instance to install OpenVidu as we mentioned before. When this time has elapsed, try connecting to the deployment URL. If it doesn't work, we recommend checking the previous section. Once finished you can check the [Administration](./admin.md) section to learn how to manage your deployment.
