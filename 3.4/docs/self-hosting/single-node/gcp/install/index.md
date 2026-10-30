# OpenVidu Single Node COMMUNITY installation: Google Cloud Platform

> **Warning**
>
> Google Cloud Platform deployments are considered in Beta in version 3.4.X of OpenVidu.

This section contains the instructions of how to deploy a production-ready OpenVidu Single Node deployment in Google Cloud Platform. Deployed services are the same as the [On Premises Single Node installation](https://openvidu.io/3.4/docs/self-hosting/single-node/on-premises/install/index.md) but they will be resources in Google Cloud Platform and you can automate the process in the Google Cloud Console.

To deploy OpenVidu into Google Cloud Platform you just need to log into your [Infrastructure Manager](https://console.cloud.google.com/infra-manager/deployments) in the GCP console. Then follow the next steps to fill the parameters of your choice.

**Architecture overview**

This is how the architecture of the deployment looks like:

OpenVidu Single Node Google Cloud Platform Architecture

## Deployment details

> **Info**
>
> We recommend to create a new project to deploy OpenVidu there, avoiding possible conflicts.

To deploy OpenVidu, first you need to create a new deployment in the top left button as you can see in the image.

Once you click the button you will see this window.

Fill **Deployment ID** with any name that you desire like openvidu-singlenode-deployment, next choose the **Region** that you prefer, leave **Terraform version** in the 1.5.7 and for **Service Account** you will need to create a new one with *"Owner"* permissions, in order to do that click on *"Service Account"* label and then into *"New Service Account"*, choose your service account name click on *"Create and Continue"* and then select the *"Owner"* role, click on *"Continue"* and the in *"Done"*.

For the **Git repository** put this link `https://github.com/OpenVidu/openvidu.git` that corresponds to our git repository where are allocated the terraform files to deploy openvidu. In the **Git directory** introduce the following path `openvidu-deployment/community/singlenode/gcp` and for the **Git ref** put `v3.4.1` corresponding to the version then click on continue.

**New Service Account Steps**

Step 1: Create Service Account

Step 2: Service Account Details

Step 3: Grant Permissions

Step 4: Complete Setup

## Input Values

In Google Cloud Platform there is no such thing like template with parameters, you will need to introduce by yourself in the console the parameters that are declared in our terraform files, so there is a detailed table of all the optional and non-optional parameters.

### Mandatory Parameters

| Input Value | Description                                         |
| ----------- | --------------------------------------------------- |
| projectId   | GCP project id where the resources will be created. |
| stackName   | Stack name for OpenVidu deployment.                 |

### Optional Parameters

| Input Value               | Default Value    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| region                    | "europe-west1"   | GCP region where resources will be created.                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| zone                      | "europe-west1-b" | GCP zone that some resources will use.                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| certificateType           | "letsEncrypt"    | Certificate type for OpenVidu deployment. Options: - **[selfsigned]** Not recommended for production use. Just for testing purposes or development environments. You don't need a FQDN to use this option. - **[owncert]** Valid for production environments. Use your own certificate. You need a FQDN to use this option. - **[letsencrypt]** Valid for production environments. Can be used with or without a FQDN (if no FQDN is provided, a random sslip.io domain will be used). |
|                           |                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| publicIpAddress           | (none)           | Previously created Public IP address for the OpenVidu Deployment. Blank will generate a public IP.                                                                                                                                                                                                                                                                                                                                                                                     |
| domainName                | (none)           | Domain name for the OpenVidu Deployment.                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ownPublicCertificate      | (none)           | If certificate type is 'owncert', this parameter will be used to specify the public certificate.                                                                                                                                                                                                                                                                                                                                                                                       |
| ownPrivateCertificate     | (none)           | If certificate type is 'owncert', this parameter will be used to specify the private certificate.                                                                                                                                                                                                                                                                                                                                                                                      |
| initialMeetAdminPassword  | (none)           | Initial password for the 'admin' user in OpenVidu Meet. If not provided, a random password will be generated.                                                                                                                                                                                                                                                                                                                                                                          |
| initialMeetApiKey         | (none)           | Initial API key for OpenVidu Meet. If not provided, no API key will be set and the user can set it later from Meet Console.                                                                                                                                                                                                                                                                                                                                                            |
| instanceType              | "e2-standard-8"  | Specifies the GCE machine type for your OpenVidu instance.                                                                                                                                                                                                                                                                                                                                                                                                                             |
| bucketName                | (none)           | Name of the S3 bucket to store data and recordings. If empty, a bucket will be created.                                                                                                                                                                                                                                                                                                                                                                                                |
| additionalInstallFlags    | (none)           | Additional optional flags to pass to the OpenVidu installer (comma-separated, e.g., '--flag1=value, --flag2').                                                                                                                                                                                                                                                                                                                                                                         |
| turnDomainName            | (none)           | (Optional) Domain name for the TURN server with TLS. Only needed if your users are behind restrictive firewalls.                                                                                                                                                                                                                                                                                                                                                                       |
| turnOwnPublicCertificate  | (none)           | (Optional) This setting is applicable if the certificate type is set to 'owncert' and the TurnDomainName is specified.                                                                                                                                                                                                                                                                                                                                                                 |
| turnOwnPrivateCertificate | (none)           | (Optional) This setting is applicable if the certificate type is set to 'owncert' and the TurnDomainName is specified.                                                                                                                                                                                                                                                                                                                                                                 |

For more detail you can check the [variables.tf](https://github.com/OpenVidu/openvidu/blob/master/openvidu-deployment/community/singlenode/gcp/variables.tf) file to see more information about the inputs.

> **Warning**
>
> It's important that you put the input variables with the same name as they appear in the table like in the next image.

## Deploying the stack

Whenever you are satisfied with your input values, just click on *"Continue"* and then in *"Create deployment"*. Now it will validate the deployment and create all the resources. Wait about 5 to 10 minutes to let the instance install OpenVidu.

> **Warning**
>
> In case of failure, check the cloud build logs that appears on the top of the screen and redeploy with the changes that are causing the deployment to fail, if it keeps failing contact us.

When everything is ready, you can check the secrets on the [Secret Manager](https://console.cloud.google.com/security/secret-manager) or by connecting through SSH to the instance:

**Check deployment outputs in Google Cloud Platform Secret Manager**

1. Go to the [Secret Manager](https://console.cloud.google.com/security/secret-manager) .
1. Once you are in the Secret Manager you will see all the secrets by their name.
1. Here click on the secret of your choice or whatever you need to check and click again in the last version of that secret.

**Check deployment outputs in the instance**

SSH to the instance by gcloud command generated in the web console and navigate to the config folder `/opt/openvidu/config`. Files with the deployment outputs are:

- `openvidu.env`
- `meet.env`

To find out the command go to [Compute Engine Instances](https://console.cloud.google.com/compute/instances) and click on the arrow close to the SSH letters and then *"View gcloud command"*.

To install gcloud in your shell follow the official [instructions](https://cloud.google.com/sdk/docs/install?hl=en#linux) .

## Configure your application to use the deployment

You need your Google Cloud Platform secret outputs to configure your OpenVidu application. You can check these secrets by searching in the Secrets Manager with any of these two ways ([Check deployment outputs in Google Cloud Platform Secret Manager](#check-deployment-outputs-in-google-cloud-platform-secret-manager)) or ([Check deployment outputs in the instance](#check-deployment-outputs-in-the-instance)).

Your authentication credentials and URL to point your applications would be:

- **URL**: The value in the Secret Manager of `OPENVIDU_URL`. In the instance in `openvidu.env` find `DOMAIN_NAME` and build it into a URL. The URL would be `https://your.domain.name/`. If you want the `LIVEKIT_URL` find the value in the Secret Manager of `LIVEKIT_URL` or build the URL with the `DOMAIN_NAME`as `wss://your.domain.name/`.
- **API Key**: The value in the Secret Manager of `LIVEKIT_API_KEY` or in the instance in `openvidu.env`.
- **API Secret**: The value in the Secret Manager of `LIVEKIT-API-SECRET` or in the instance in `openvidu.env`.

## Troubleshooting initial Google Cloud Platform deployment creation

If something goes wrong during the initial GCP deployment creation, your stack may reach some failed status for multiple reasons. It could be due to a misconfiguration in the parameters, a lack of permissions, or a problem with GCP services. When this happens, the following steps can help you troubleshoot the issue and identify what went wrong:

1. Check if the instance or instances are running. If they are not, check the GCP cloud build logs for any error messages.

1. If the instance or instances are running, SSH into the instance and check the logs by running this command:

   - `journalctl -u google-startup-scripts | cat`

   These logs will give you more information about the GCP deployment creation process.

1. If everything seems fine, check the [status](https://openvidu.io/3.4/docs/self-hosting/single-node/on-premises/admin/#checking-the-status-of-services) and the [logs](https://openvidu.io/3.4/docs/self-hosting/single-node/on-premises/admin/#checking-logs) of the installed OpenVidu services.

## Configuration and administration

When your Google Cloud Platform deployment reaches the **`Active`** state, it means that all the resources have been created. You will need to wait about 5 to 10 minutes to let the instance install OpenVidu as we mentioned before. When this time has elapsed, try connecting to the deployment URL. If it doesn't work, we recommend checking the previous section. Once finished you can check the [Administration](https://openvidu.io/3.4/docs/self-hosting/single-node/gcp/admin/index.md) section to learn how to manage your deployment.
