# OpenVidu Elastic installation: Google Cloud Platform

> **Info**
>
> OpenVidu Elastic is part of **OpenVidu PRO**. Before deploying, you need to [create an OpenVidu account](https://openvidu.io/account/) to get your license key. There's a 15-day free trial waiting for you!

This section contains the instructions to deploy a production-ready OpenVidu Elastic deployment in Google Cloud Platform. Deployed services are the same as the [On Premises Elastic installation](https://openvidu.io/3.5/docs/self-hosting/elastic/on-premises/install/index.md) but they will be resources in Google Cloud Platform and you can automate the process in the Google Cloud Console.

To deploy OpenVidu into Google Cloud Platform you just need to log into your [Infrastructure Manager](https://console.cloud.google.com/infra-manager/deployments) in the GCP console. Then follow the next steps to fill the parameters of your choice.

**Architecture overview**

This is how the architecture of the deployment looks like:

OpenVidu Elastic Google Cloud Platform Architecture

- The Master Node acts as a Load Balancer, managing the traffic and distributing it among the Media Nodes and deployed services in the Master Node.
- The Master Node has its own Caddy server acting as a Layer 4 (for TURN with TLS and RTMPS) and Layer 7 (for OpenVidu Dashboard, OpenVidu Meet, etc., APIs) reverse proxy.
- WebRTC traffic (SRTP/SCTP/STUN/TURN) is routed directly to the Media Nodes.
- A Managed Instace Group of Media Nodes is created to scale the number of Media Nodes based on the system load.

We use a custom scale-in strategy to allow the graceful shutdown of Media Nodes. In this way we ensure no disruption of active Rooms when the cluster tries to remove a Media Node.

**Custom scale-in strategy**

- The Managed Instance Group (MIG) is set to Scale OUT only.
- We use a lambda function to check if the MIG current size is more than the recommended size that it targets.
- If the current size is more than the recommended size we calculate the number of instances that should scale in and we remove them from the MIG.
- The instances have a cron job that checks every minute if they are out of the MIG and runs the graceful shutdown script if they are out of the MIG.

## Deployment details

> **Info**
>
> We recommend to create a new project to deploy OpenVidu there, avoiding possible conflicts between resources. Enable [Secrets Manager Api](https://console.cloud.google.com/security/secret-manager) first in that project and then deploy the stack. You might need to deploy multiple times to let the APIs activate.

To deploy OpenVidu, first you need to create a new deployment in the top left button as you can see in the image.

Once you click the button you will see this window.

Fill **Deployment ID** with any name that you desire like openvidu-elastic-deployment, next choose the **Region** that you prefer, leave **Terraform version** in the 1.5.7 and for **Service Account** you will need to create a new one with *"Owner"* permissions, in order to do that click on *"Service Account"* label and then into *"New Service Account"*, choose your service account name click on *"Create and Continue"* and then select the *"Owner"* role, click on *"Continue"* and the in *"Done"*.

> **Warning**
>
> If you change the region in the previous step, don't forget to change the [region and zone](https://docs.cloud.google.com/compute/docs/regions-zones?hl=en) in the terraform values.

> **New Service Account Steps**
>
> Step 1: Create Service Account
>
> Step 2: Service Account Details
>
> Step 3: Grant Permissions
>
> Step 4: Complete Setup

- Fill **Git repository** with this link `https://github.com/OpenVidu/openvidu.git` that corresponds to our git repository where are allocated the terraform files to deploy openvidu.
- Fill the **Git directory** with the following path `openvidu-deployment/pro/elastic/gcp`
- For the **Git ref** use `v3.5.0` corresponding to the version

Finally click on continue.

## Input Values

In Google Cloud Platform there is no such thing like template with parameters, you will need to introduce by yourself in the console the parameters that are declared in our terraform files, so there is a detailed table of all the optional and non-optional parameters.

### Mandatory Parameters

| Input Value     | Description                                                                              |
| --------------- | ---------------------------------------------------------------------------------------- |
| projectId       | GCP project id where the resources will be created.                                      |
| stackName       | Stack name for OpenVidu deployment.                                                      |
| openviduLicense | Your OpenVidu License, get one [here](https://openvidu.io/account) if you dont have one. |

### Optional Parameters

| Input Value               | Default Value    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| region                    | "europe-west2"   | GCP region where resources will be created.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| zone                      | "europe-west2-b" | GCP zone that some resources will use.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| certificateType           | "letsEncrypt"    | Certificate type for OpenVidu deployment. Options: - **[selfsigned]** Not recommended for production use. Just for testing purposes or development environments. You don't need a FQDN to use this option. - **[owncert]** Valid for production environments. Use your own certificate. You need a FQDN to use this option. - **[letsencrypt]** Valid for production environments. Can be used with or without a FQDN (if no FQDN is provided, a random sslip.io domain will be used). **Warning:** sslip.io is currently experiencing Let's Encrypt rate limiting issues, which may prevent SSL certificates from being generated. It is recommended to use your own domain name. Check [this community thread](https://openvidu.discourse.group/t/deployment-without-domain/5474) for troubleshooting and updates. |
| publicIpAddress           | (none)           | Previously created Public IP address for the OpenVidu Deployment. Blank will generate a public IP.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| domainName                | (none)           | Domain name for the OpenVidu Deployment.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ownPublicCertificate      | (none)           | If certificate type is 'owncert', this parameter will be used to specify the public certificate in base64 format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ownPrivateCertificate     | (none)           | If certificate type is 'owncert', this parameter will be used to specify the private certificate in base64 format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| initialMeetAdminPassword  | (none)           | Initial password for the 'admin' user in OpenVidu Meet. If not provided, a random password will be generated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| initialMeetApiKey         | (none)           | Initial API key for OpenVidu Meet. If not provided, no API key will be set and the user can set it later from Meet Console.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| masterNodeInstanceType    | "e2-standard-2"  | Specifies the GCE machine type for your OpenVidu Master Node.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| mediaNodeInstanceType     | "e2-standard-2"  | Specifies the GCE machine type for your OpenVidu Media Nodes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| initialNumberOfMediaNodes | 1                | Number of initial media nodes to deploy.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| minNumberOfMediaNodes     | 1                | Minimum number of media nodes to deploy.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| maxNumberOfMediaNodes     | 5                | Maximum number of media nodes to deploy.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| scaleTargetCPU            | 50               | Target CPU percentage to scale out or in.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| bucketName                | (none)           | Name of the GCS bucket to store data and recordings. If empty, a bucket will be created.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| rtcEngine                 | "pion"           | RTCEngine media engine to use. Allowed values are 'pion' and 'mediasoup'.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| additionalInstallFlags    | (none)           | Additional optional flags to pass to the OpenVidu installer (comma-separated, e.g., '--flag1=value, --flag2').                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| turnDomainName            | (none)           | (Optional) Domain name for the TURN server with TLS. Only needed if your users are behind restrictive firewalls.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| turnOwnPublicCertificate  | (none)           | (Optional) This setting is applicable if the certificate type is set to 'owncert' and the TurnDomainName is specified. Specify the certificate in base64 format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| turnOwnPrivateCertificate | (none)           | (Optional) This setting is applicable if the certificate type is set to 'owncert' and the TurnDomainName is specified. Specify the certificate in base64 format.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

For more detail you can check the [variables.tf](https://github.com/OpenVidu/openvidu/blob/master/openvidu-deployment/pro/elastic/gcp/variables.tf) file to see more information about the inputs.

> **Warning**
>
> It's important that you put the input variables with the same name as they appear in the table like in the next image.

## Deploying the stack

Whenever you are satisfied with your input values, just click on *"Continue"* and then in *"Create deployment"*. Now it will validate the deployment and create all the resources. Wait around 7 to 12 minutes for the nodes to install openvidu.

> **Warning**
>
> In case of failure, check the cloud build logs that appears on the top of the screen and redeploy with the changes that are causing the deployment to fail, if it is something about some API delete the deployment and deploy another one, it should work now. If it keeps failing contact us.

When everything is ready, you can check the secrets on the [Secret Manager](https://console.cloud.google.com/security/secret-manager) or by connecting through SSH to the instances:

**Check deployment outputs in GCP Secret Manager**

1. Go to the [Secret Manager](https://console.cloud.google.com/security/secret-manager) .
1. Once you are in the Secret Manager you will see all the secrets by their name.
1. Here click on the secret of your choice, choose the last version and then click on the *"3 dots"* -> *"View secret value"* to retrieve that secret.

**Check deployment outputs in the instance**

SSH to the Master Node by gcloud command generated in the web console and navigate to the config folder `/opt/openvidu/config/cluster`. Files with the deployment outputs are:

- `openvidu.env`
- `master_node/meet.env`

To find out the command go to [Compute Engine Instances](https://console.cloud.google.com/compute/instances) and click on the arrow close to the SSH letters and then *"View gcloud command"*.

To install gcloud in your shell follow the official [instructions](https://cloud.google.com/sdk/docs/install?hl=en#linux) .

## Configure your application to use the deployment

You need your Google Cloud Platform secret outputs to configure your OpenVidu application. You can check these secrets by searching in the Secrets Manager with any of these two ways ([Check deployment outputs in GCP Secret Manager](#check-deployment-outputs-in-gcp-secret-manager)) or ([Check deployment outputs in the instance](#check-deployment-outputs-in-the-instance)).

Your authentication credentials and URL to point your applications would be:

**OpenVidu Meet**:

- **`OPENVIDU_URL`**: The URL to access OpenVidu Meet, which is always `https://yourdomain.example.io/`
- **`MEET_INITIAL_ADMIN_USER`**: User to access OpenVidu Meet Console. It is always `admin`.
- **`MEET_INITIAL_ADMIN_PASSWORD`**: Password to access OpenVidu Meet Console.
- **`MEET_INITIAL_API_KEY`**: API key to use OpenVidu Meet Embedded and OpenVidu Meet REST API.

> **Note**
>
> The `MEET_INITIAL_ADMIN_USER`, `MEET_INITIAL_ADMIN_PASSWORD`, and `MEET_INITIAL_API_KEY` values are initial settings that cannot be changed from GCP Secret Manager. They can only be changed from the Meet Console.

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

1. If everything seems fine, check the [status](https://openvidu.io/3.5/docs/self-hosting/elastic/on-premises/admin/#checking-the-status-of-services) and the [logs](https://openvidu.io/3.5/docs/self-hosting/elastic/on-premises/admin/#checking-logs) of the installed OpenVidu services.

## Configuration and administration

When your Google Cloud Platform deployment reaches the **`Active`** state, it means that all the resources have been created. You will need to wait about 7 to 12 minutes to let the instances install OpenVidu as we mentioned before. When this time has elapsed, try connecting to the deployment URL. If it doesn't work, we recommend checking the previous section. Once finished you can check the [Administration](https://openvidu.io/3.5/docs/self-hosting/elastic/gcp/admin/index.md) section to learn how to manage your deployment.
