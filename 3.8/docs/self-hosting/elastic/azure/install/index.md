# OpenVidu Elastic installation: Azure

Azure

Info

OpenVidu Elastic is part of **OpenVidu PRO**. Before deploying, you need to [create an OpenVidu account](https://openvidu.io/account/) to get your license key. There's a 15-day free trial waiting for you!

This section describes how to deploy a production-ready OpenVidu Elastic instance on Azure. The deployed services are identical to those in the [On Premises Elastic installation](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/install/index.md), but are provisioned as Azure resources and can be automated through an ARM Template Spec.

To import the template into Azure, click the button below and you will be redirected to Azure.

Deploy to Azure

**Architecture overview**

This is what the deployment architecture looks like:

OpenVidu Elastic Azure Architecture

- The Master Node acts as a Load Balancer, managing the traffic and distributing it among the Media Nodes and deployed services in the Master Node.
- The Master Node has its own Caddy server acting as a Layer 4 (for TURN with TLS and RTMPS) and Layer 7 (for OpenVidu Dashboard, OpenVidu Meet, etc., APIs) reverse proxy.
- WebRTC traffic (SRTP/SCTP/STUN/TURN) is routed directly to the Media Nodes.
- A Virtual Machine Scale Set (VMSS) of Media Nodes is created to scale the number of Media Nodes based on the system load.

We use a custom scale-in strategy to allow the graceful shutdown of Media Nodes. In this way we ensure no disruption of active Rooms when the cluster tries to remove a Media Node.

**Custom scale-in strategy**

- All instances in the Media Node Virtual Machine Scale Set (VMSS) are protected to prevent their automatic shutdown.
- We receive and use the shutdown event to execute a custom Automation runbook.
- The Automation runbook determines the instance that has to be terminated and executes the appropriate commands in all internal services to prevent them from accepting new jobs (new Rooms, new Egresses, new Ingresses, new Agents...).
- Only when all the jobs hosted by the selected instance finish, it is automatically terminated.

## Template Parameters

To deploy the template, you need to fill in the following parameters.

### Resource Group and Stack Name

Select your **Subscription** and the **Resource Group** where you want to deploy OpenVidu.

Azure Instance configuration

Warning

It is highly recommended to deploy OpenVidu in a brand new Azure Resource Group. Reusing an existing Resource Group can lead to conflicts. The only reason to reuse an existing Resource Group is to use the same **IP** and **Azure Blob Storage Account** as a previous OpenVidu deployment. The rest of resources are not reusable and should be eliminated before deploying OpenVidu in the same Resource Group.

Select the **Region** and choose a descriptive **Stack Name**. It will be used as a prefix in the name of all the resources created by the template.

Azure Instance configuration

### Domain and SSL Certificate Configuration

There are three possible scenarios for this section:

**Let's Encrypt Without Domain Name**

If you don't have a Domain Name and want to quickly test OpenVidu on Azure, you can use this option by selecting **Certificate Type** as *letsencrypt* and keeping the rest of the parameters empty.

It will deploy OpenVidu with a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability) certificate issued for the public IP created for the deployment.

Let's Encrypt certificates

**Let's Encrypt With Domain Name (recommended)**

For a production-ready setup, this scenario is ideal when you have an **FQDN (Fully Qualified Domain Name)** and a **Public IP** at your disposal. It leverages the services of Let's Encrypt to automatically generate valid certificates.

First, make sure your FQDN points to the Public IP you are going to use.

Then, fill in the following parameters:

Let's Encrypt certificates

As you can see, specify **Public IP Address** with the Public IP that the domain points to, **Domain Name** with your FQDN, and **Lets Encrypt Email** with your email address for Let’s Encrypt notifications. These parameters are mandatory.

**Custom Certificates**

Opt for this method if you possess **your own certificate for an existing FQDN**. It enables you to deploy OpenVidu on Azure using your certificates.

Ensure your FQDN points to a previously created Public IP.

The configured parameters would look like this:

Custom certificates

Specify the certificate files in base64 in **Own Public Certificate** and **Own Private Certificate**. The **Domain Name** and **Public IP Address** parameters are mandatory.

Certificates need to be in PEM format and base64 encoded. You can encode them using the following command in a terminal where `fullchain.pem` is your public certificate and `privkey.pem` is your private certificate:

```bash
base64 -w 0 fullchain.pem # OwnPublicCertificate
base64 -w 0 privkey.pem # OwnPrivateCertificate
```

**Self-Signed Certificate**

This is the most straightforward option for deploying OpenVidu on Azure when you do not have a Fully Qualified Domain Name (FQDN). This method allows for the immediate use of OpenVidu with ARM Templates.

However, this convenience comes with the caveat that users will need to manually accept the certificate in their web browsers. Please be aware that this configuration is solely for developmental and testing purposes and is not suitable for a real production environment.

These are the parameters needed in this section to use self-signed certificates:

Self-signed certificates

You don’t need to specify any parameters; just select the **CertificateType** as *self-signed*. The domain name used will be an Azure-generated one.

### OpenVidu Meet Credentials

Configure the initial credentials for accessing OpenVidu Meet:

**OpenVidu Meet credentials**

Parameters in this section look like this:

OpenVidu Meet credentials

- **InitialMeetAdminPassword**: Initial password for the "admin" user in OpenVidu Meet. If not provided, a random password will be generated and stored in the Azure Key Vault.
- **InitialMeetApiKey**: Initial API key for OpenVidu Meet. If not provided, no API key will be set and the user can configure it later from the Meet Console.

Both parameters are optional. If you don't specify them, you can retrieve the generated credentials from the Azure Key Vault after deployment.

### OpenVidu Elastic Configuration

In this section, you need to specify some properties needed for the OpenVidu Elastic deployment.

**OpenVidu Elastic Configuration**

Parameters of this section look like this:

OpenVidu Elastic Configuration

Make sure to provide the **OpenVidu License** parameter with the license key. If you don't have one, you can request one [here](https://openvidu.io/account/).

For the **RTC Engine** parameter, you can choose between **Pion** (the default engine used by LiveKit) and **Mediasoup** (with a boost in performance). Learn more about the differences [here](https://openvidu.io/3.8/docs/self-hosting/production-ready/performance/index.md).

### Azure Instance Configuration

You need to specify some properties for the Azure instances that will be created.

**Azure Instance configuration**

Parameters in this section look like this:

Azure Instance configuration

Simply select the type of instance you want for your Master Node in **Master Node Instance Type** and the type for your Media Nodes in **Media Node Instance Type**. Fill in **Admin Username**, which will be set as the admin username on the instances. Select the SSH key you created previously in **SSH public key source** (or create a new one in the same drop-down) to allow SSH access to the instances.

### Media Nodes Virtual Machine Scale Set (VMSS) Configuration

The number of Media Nodes can scale up based on the system load. You can configure the minimum and maximum number of Media Nodes and a target CPU utilization to trigger the scaling up.

**Media Nodes Virtual Machine Scale Set (VMSS) Configuration**

Parameters in this section look like this:

Media Nodes Virtual Machine Scale Set (VMSS) Configuration

The **Initial Number Of Media Nodes** parameter specifies the initial number of Media Nodes to deploy. The **Min Number Of Media Nodes** and **Max Number Of Media Nodes** parameters specify the minimum and maximum number of Media Nodes that you want to be deployed.

The **Scale Target CPU** parameter specifies the target CPU utilization to trigger the scaling up or down. The goal is to keep the CPU utilization of the Media Nodes close to this value. The autoscaling policy is based on [Azure Monitor autoscale metrics](https://learn.microsoft.com/en-us/azure/architecture/best-practices/auto-scaling#use-the-azure-monitor-autoscale-feature) .

### Scale In

Azure instances may only wait at most 15 minutes when the Scale Set flags them for termination after detecting a surplus of CPU capacity. This is a problem for those active Rooms hosted by the instance that can last longer than that. To avoid the disruption of active Rooms, we have implemented a custom scale-in strategy that gracefully shuts down flagged instances only after all active jobs have finished.

Due to Azure limitations, this strategy has the minor drawback that it can take up to 5 minutes from the time an instance is flagged for termination until the shutdown process is gracefully initiated.

**Automation Account Configuration**

The name of an Automation Account, needed to execute the scale-in runbook. It must be unique for the resource group it belongs to (leave it blank to use an autogenerated name). This resource cannot be reused between deployments.

Automation account name

### Storage Account

You need to fill some parameters about the storage account that the deployment will use to save the recordings.

Warning

Recordings are not available in OpenVidu v2 Compatibility mode (v2compat) for OpenVidu Azure deployments.

**Azure Storage Account configuration**

Parameters in this section look like this:

Azure Instance configuration

**Storage Account Name**: leave blank to create a new Storage Account for this deployment. You can specify an already existing Storage Account name if you want (remember it must belong to the same resource group as your deployment).

**Container Name** is the name that you desire for the container that of the storage account where the recordings will be saved. If you leave it blank it will create the container with name `openvidu-appdata`.

### (Optional) Additional flags

Additional optional flags to pass to the OpenVidu installer (comma-separated, e.g., `--flag1=value, --flag2`).

**(Optional) Additional flags**

Parameters in this section look like this:

OpenVidu Meet credentials

For example (optional), you can use `--force-utc-timezone` to force UTC as the timezone for OpenVidu. By default, OpenVidu uses the timezone configured on the host machine where it is installed. In general, UTC is recommended, and [Azure VMs already default to UTC](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/time-sync), so this flag is not usually necessary.

## Deploying the stack

Whenever you are satisfied with your Template parameters, just click on *"Next"* to trigger the validation process. If correct, click on *"Create"* to start the deployment process (which will take about 7 to 12 minutes).

Warning

In case of failure, it may be due to a role creation failure. In this case, redeploy in a new resource group and change the **Stack Name**. To remove a role in a resource group, visit [Remove Azure role assignments](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-remove) .

When everything is ready, you can check the output secrets on the Key Vault or by connecting through SSH to the instance:

**Check deployment outputs in Azure Key Vault**

1. Go to the Key Vault created called **yourstackname-keyvault** in the Resource Group that you deployed. You can access it from the [Azure Portal Dashboard](https://portal.azure.com/#home) .

1. Once you are in the Key Vault, click *"Objects"* 🡒 *"Secrets"* in the left panel.

   Azure Key Vault secrets location

1. Click the secret you want to inspect, then click the current version of that secret.

   Azure Key Vault Secret Version

1. You will see many properties, but the value you need is at the bottom. Click *"Show Secret Value"* to reveal it.

   Check deployment outputs in Azure Key Vault

**Check deployment outputs in the instance**

SSH to the Master Node instance and navigate to the config folder `/opt/openvidu/config/cluster`. Files with the access credentials outputs are:

- `openvidu.env`
- `master_node/meet.env`

## Configure your application to use the deployment

You need your Azure deployment outputs to configure your OpenVidu application. If you have permissions to access the Key Vault you will be able to check there all the outputs ([Check deployment outputs in Azure Key Vault](#check-deployment-outputs-in-azure-key-vault)). If you don't have permissions to access the Key Vault you can still check the outputs directly in the instance through SSH ([Check deployment outputs in the instance](#check-deployment-outputs-in-the-instance)).

Your authentication credentials and the URL to point your applications to are:

**OpenVidu Meet**:

- **`OPENVIDU-URL`**: The URL to access OpenVidu Meet, which is always `https://yourdomain.example.io/`
- **`MEET-INITIAL-ADMIN-USER`**: User to access OpenVidu Meet Console. It is always `admin`.
- **`MEET-INITIAL-ADMIN-PASSWORD`**: Password to access OpenVidu Meet Console.
- **`MEET-INITIAL-API-KEY`**: API key to use OpenVidu Meet Embedded and OpenVidu Meet REST API.

Note

The `MEET-INITIAL-ADMIN-USER`, `MEET-INITIAL-ADMIN-PASSWORD`, and `MEET-INITIAL-API-KEY` values are initial settings that cannot be changed from Azure Key Vault. They can only be changed from the Meet Console.

**OpenVidu Platform:**

- **`LIVEKIT-URL`**: The URL to use LiveKit SDKs, which can be `wss://yourdomain.example.io/` or `https://yourdomain.example.io/` depending on the client library you are using.
- **`LIVEKIT-API-KEY`**: API Key for LiveKit SDKs.
- **`LIVEKIT-API-SECRET`**: API Secret for LiveKit SDKs.

**OpenVidu V2 Compatibility Credentials**

This section is only needed if you want to use OpenVidu v2 compatibility.

- **URL**: The URL to access OpenVidu, which is the value of `OPENVIDU-URL` (e.g., `https://yourdomain.example.io/`)
- **Username**: Basic auth user for OpenVidu v2 compatibility. It is always `OPENVIDUAPP`.
- **Password**: Basic auth password for OpenVidu v2 compatibility is the same as `LIVEKIT-API-SECRET`.

## Troubleshooting initial Azure stack creation

If something goes wrong during the initial Azure stack creation, your stack may reach some failed status for multiple reasons. It could be due to a misconfiguration in the parameters, a lack of permissions, or a problem with Azure services. When this happens, the following steps can help you troubleshoot the issue and identify what went wrong:

1. Check if the instance or instances are running. If they are not, check the Azure deployment events for any error messages.

1. If the instance or instances are running, SSH into the instance and check the logs of the following files:

   - `/var/log/cloud-init-output.log`
   - `/var/log/cloud-init.log`

   These logs will give you more information about the Azure stack creation process.

1. If everything seems fine, check the [status](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/admin/#checking-the-status-of-services) and the [logs](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/admin/#checking-logs) of the installed OpenVidu services.

## Configuration and administration

When your Azure stack reaches the **`Succeeded`** status, it means that all resources have been created. You will need to wait about 7 to 12 minutes for the instances to install OpenVidu. After this time, try connecting to the deployment URL. If it doesn't work, we recommend checking the previous section. Once everything is ready, you can check the [Administration](https://openvidu.io/3.8/docs/self-hosting/elastic/azure/admin/index.md) section to learn how to manage your deployment.
