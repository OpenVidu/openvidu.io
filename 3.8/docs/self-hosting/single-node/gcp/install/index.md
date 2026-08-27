# OpenVidu Single Node installation: Google Cloud Platform

Google Cloud Platform

This section contains instructions for deploying a production-ready OpenVidu Single Node deployment on Google Cloud Platform, in either the COMMUNITY or PRO edition. The deployed services are the same as in the [On Premises Single Node installation](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/install/index.md), but the process is automated through the Google Cloud Console.

Info

OpenVidu Single Node Pro is part of **OpenVidu** **PRO**. Before deploying, you need to [create an OpenVidu account](https://openvidu.io/account/) to get your license key. There's a 15-day free trial waiting for you!

To deploy OpenVidu on Google Cloud Platform, log in to [Infrastructure Manager](https://console.cloud.google.com/infra-manager/deployments) in the GCP Console. Then follow the next steps and fill in your preferred parameters.

**Architecture overview**

This is what the deployment architecture looks like:

OpenVidu Single Node Google Cloud Platform Architecture

## Deployment details

Info

We recommend to create a new project to deploy OpenVidu there, avoiding possible conflicts between resources. Enable [Secrets Manager Api](https://console.cloud.google.com/security/secret-manager) first in that project and then deploy the stack. You might need to deploy multiple times to let the APIs activate.

To deploy OpenVidu, first create a new deployment using the top-left button, as shown in the image.

Google Cloud Platform create new deployment

Once you click the button, you will see this window.

Google Cloud Platform create new deployment window

- Fill **Deployment ID** with any name you prefer (for example, openvidu-singlenode-deployment).
- Change the **Region** to the one you prefer.

Warning

If you change the region in the previous step, don't forget to update the [region and zone](https://docs.cloud.google.com/compute/docs/regions-zones?hl=en) in the Terraform values.

- Leave **Terraform version** as 1.5.7.
- For **Service Account**, you will need to create a new one with *"Owner"* permissions. To do this, click the *"Service Account"* label and then *"New Service Account"*. Choose your service account name, click *"Create and Continue"*, select the *"Owner"* role, click *"Continue"*, and then *"Done"*.

New Service Account Steps

Google Cloud Platform create new Service Account step 1

Step 1: Create Service Account

Google Cloud Platform create new Service Account step 2

Step 2: Service Account Details

Google Cloud Platform create new Service Account step 3

Step 3: Grant Permissions

Google Cloud Platform create new Service Account step 4

Step 4: Complete Setup

- Fill **Git repository** with this link, which corresponds to our Git repository where the Terraform files to deploy OpenVidu are located:

  ```text
  https://github.com/OpenVidu/openvidu.git
  ```

- Fill the **Git directory** with the path corresponding to the edition you want to deploy:

  **OpenVidu COMMUNITY**

  ```text
  openvidu-deployment/community/singlenode/gcp
  ```

  **OpenVidu PRO**

  ```text
  openvidu-deployment/pro/singlenode/gcp
  ```

- For the **Git ref**, use the version you want to deploy:

  ```text
  v3.8.0
  ```

Finally, click Continue.

## Input Values

In Google Cloud Platform, there is no built-in template with parameters. You need to manually enter the parameters declared in our Terraform files into the console, so below is a detailed table of all optional and mandatory parameters.

### Mandatory Parameters

| Input Value             | Description                                                                                                                               |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| projectId               | GCP project id where the resources will be created.                                                                                       |
| stackName               | Stack name for OpenVidu deployment.                                                                                                       |
| openviduLicense **PRO** | Only required for the PRO edition. Your OpenVidu License. Get one [here](https://openvidu.io/account/) if you don't have one. |

### Optional Parameters

| Input Value              | Default Value    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------ | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| region                   | "europe-west2"   | GCP region where resources will be created.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| zone                     | "europe-west2-b" | GCP zone that some resources will use.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| certificateType          | "letsEncrypt"    | Certificate type for OpenVidu deployment. Options: - **[selfsigned]** Not recommended for production use. Just for testing purposes or development environments. You don't need a FQDN to use this option. - **[owncert]** Valid for production environments. Use your own certificate. You need a FQDN to use this option. - **[letsencrypt]** Valid for production environments. Can be used with or without a FQDN (if no FQDN is provided, the public IP is used as the domain name and a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability) certificate is issued for it). |
| publicIpAddress          | (none)           | Previously created Public IP address for the OpenVidu Deployment. Blank will generate a public IP.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| domainName               | (none)           | Domain name for the OpenVidu Deployment.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ownPublicCertificate     | (none)           | If certificate type is 'owncert', this parameter will be used to specify the public certificate in base64 format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ownPrivateCertificate    | (none)           | If certificate type is 'owncert', this parameter will be used to specify the private certificate in base64 format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| initialMeetAdminPassword | (none)           | Initial password for the 'admin' user in OpenVidu Meet. If not provided, a random password will be generated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| initialMeetApiKey        | (none)           | Initial API key for OpenVidu Meet. If not provided, no API key will be set and the user can set it later from Meet Console.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| instanceType             | "e2-standard-2"  | Specifies the GCE machine type for your OpenVidu instance.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| bucketName               | (none)           | Name of the GCS bucket to store data and recordings. If empty, a bucket will be created.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| rtcEngine **PRO**        | "pion"           | RTCEngine media engine to use. Allowed values are 'pion' and 'mediasoup'. Only applies to the PRO edition.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| additionalInstallFlags   | (none)           | Additional optional flags to pass to the OpenVidu installer (comma-separated, e.g., '--flag1=value, --flag2').                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

For more details, you can check the variables.tf file to see additional information about the inputs: [COMMUNITY](https://github.com/OpenVidu/openvidu/blob/v3.8.0/openvidu-deployment/community/singlenode/gcp/variables.tf) / [PRO](https://github.com/OpenVidu/openvidu/blob/v3.8.0/openvidu-deployment/pro/singlenode/gcp/variables.tf) .

Warning

It's important that you enter the input variables with the exact same names as they appear in the table, as shown in the next image.

Google Cloud Platform input variables

## Deploying the stack

When you are satisfied with your input values, click *"Continue"* and then *"Create deployment"*. The deployment will be validated and all resources will be created. Wait around 5 to 10 minutes for the instance to install OpenVidu.

Warning

In case of failure, check the Cloud Build logs that appear at the top of the screen and redeploy after applying the required changes. If the issue is related to an API, delete the deployment and create a new one. If it keeps failing, contact us.

Google Cloud Platform input variables

When everything is ready, you can check the secrets on the [Secret Manager](https://console.cloud.google.com/security/secret-manager) or by connecting through SSH to the instance:

**Check deployment outputs in GCP Secret Manager**

1. Go to the [Secret Manager](https://console.cloud.google.com/security/secret-manager) .

1. Once you are in Secret Manager, you will see all secrets by name.

   Google Cloud Platform Secrets location

1. Click the secret you want, select the latest version, and then click *"3 dots"* -> *"View secret value"* to retrieve it.

   Google Cloud Platform Secrets version

**Check deployment outputs in the instance**

SSH into the instance using the `gcloud` command generated in the web console, then navigate to the `/opt/openvidu/config` folder. Files with the deployment outputs are:

- `openvidu.env`
- `meet.env`

To find the command, go to [Compute Engine Instances](https://console.cloud.google.com/compute/instances) , click the arrow next to **SSH**, and then click *"View gcloud command"*.

Google Cloud Platform gcloud command

To install `gcloud` in your shell, follow the official [instructions](https://cloud.google.com/sdk/docs/install?hl=en#linux) .

## Configure your application to use the deployment

You need the secret outputs from Google Cloud Platform to configure your OpenVidu application. You can check these secrets in Secret Manager using either of these two methods: ([Check deployment outputs in GCP Secret Manager](#check-deployment-outputs-in-gcp-secret-manager)) or ([Check deployment outputs in the instance](#check-deployment-outputs-in-the-instance)).

Your authentication credentials and the URL to point your applications to are:

**OpenVidu Meet**:

- **`OPENVIDU_URL`**: The URL to access OpenVidu Meet, which is always `https://yourdomain.example.io/`
- **`MEET_INITIAL_ADMIN_USER`**: User to access OpenVidu Meet Console. It is always `admin`.
- **`MEET_INITIAL_ADMIN_PASSWORD`**: Password to access OpenVidu Meet Console.
- **`MEET_INITIAL_API_KEY`**: API key to use OpenVidu Meet Embedded and OpenVidu Meet REST API.

Note

The `MEET_INITIAL_ADMIN_USER`, `MEET_INITIAL_ADMIN_PASSWORD`, and `MEET_INITIAL_API_KEY` values are initial settings that cannot be changed from GCP Secret Manager. They can only be changed from the Meet Console.

**OpenVidu Platform:**

- **`LIVEKIT_URL`**: The URL to use LiveKit SDKs, which can be `wss://yourdomain.example.io/` or `https://yourdomain.example.io/` depending on the client library you are using.
- **`LIVEKIT_API_KEY`**: API Key for LiveKit SDKs.
- **`LIVEKIT_API_SECRET`**: API Secret for LiveKit SDKs.

**OpenVidu V2 Compatibility Credentials**

This section is only needed if you want to use OpenVidu v2 compatibility.

- **URL**: The URL to access OpenVidu, which is the value of `OPENVIDU_URL` (e.g., `https://yourdomain.example.io/`)
- **Username**: Basic auth user for OpenVidu v2 compatibility. It is always `OPENVIDUAPP`.
- **Password**: Basic auth password for OpenVidu v2 compatibility is the same as `LIVEKIT_API_SECRET`.

## Troubleshooting initial Google Cloud Platform deployment creation

If something goes wrong during the initial GCP deployment creation, your stack may reach some failed status for multiple reasons. It could be due to a misconfiguration in the parameters, a lack of permissions, or a problem with GCP services. When this happens, the following steps can help you troubleshoot the issue and identify what went wrong:

1. Check if the instance or instances are running. If they are not, check the GCP cloud build logs for any error messages.

1. If the instance or instances are running, SSH into the instance and check the logs by running this command:

   - `journalctl -u google-startup-scripts | cat`

   These logs will give you more information about the GCP deployment creation process.

1. If everything seems fine, check the [status](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/#checking-the-status-of-services) and the [logs](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/#checking-logs) of the installed OpenVidu services.

## Configuration and administration

When your Google Cloud Platform deployment reaches the **`Active`** state, it means that all resources have been created. You will need to wait around 5 to 10 minutes for the instance to install OpenVidu, as mentioned before. After this time, try connecting to the deployment URL. If it doesn't work, we recommend checking the previous section. Once everything is ready, you can check the [Administration](https://openvidu.io/3.8/docs/self-hosting/single-node/gcp/admin/index.md) section to learn how to manage your deployment.
