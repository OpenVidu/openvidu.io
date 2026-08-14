# OpenVidu Single Node PRO administration: Azure

Azure

Azure OpenVidu Single Node PRO deployments are internally identical to On Premises Single Node PRO deployments, so you can follow the same instructions from [On Premises Single Node PRO](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/admin/index.md) documentation for administration and configuration. The only difference is that the deployment is automated with ARM Templates from Azure.

However, there are certain things worth mentioning:

## Start and stop OpenVidu through Azure Portal

You can start and stop all services as explained in the [On Premises Single Node PRO](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/admin/#starting-stopping-and-restarting-openvidu) section. But you can also start and stop the Virtual Machine instance directly from Azure Portal. This will stop all services running in the instance and reduce Azure costs.

**Stop OpenVidu Single Node PRO**

1. Go to [Azure Portal Dashboard](https://portal.azure.com/#home) of Azure and enter into the resource group where you deployed OpenVidu Single Node PRO.
1. There, you will find the Virtual Machine that runs OpenVidu. Its name should be something like **yourstackname-VM-CE**. Click on it.
1. In the Virtual Machine section, click the stop button to stop the Virtual Machine (and therefore OpenVidu).

Stop instance

**Start OpenVidu Single Node PRO**

1. Go to [Azure Portal Dashboard](https://portal.azure.com/#home) of Azure and enter into the resource group where you deployed OpenVidu Single Node PRO.
1. There, you will find the Virtual Machine that runs OpenVidu. Its name should be something like **yourstackname-VM-CE**. Click on it.
1. In the Virtual Machine section, click the start button to start the Virtual Machine (and therefore OpenVidu).

Start instance

## Change the instance type

You can change the instance type of the OpenVidu Single Node PRO instance to adapt it to your needs. To do this, follow these steps:

1. Go to [Azure Portal Dashboard](https://portal.azure.com/#home) of Azure and enter into the resource group where you deployed OpenVidu Single Node PRO.

1. There, you will find the Virtual Machine that runs OpenVidu. Its name should be something like **yourstackname-VM-CE**. Click on it.

1. In the left panel click on *"Availability + scale"* -> *"Size"*.

   **Change instance type**

   Change instance type

1. Select the new instance type and click on *"Resize"*.

## Administration and configuration

Regarding the administration of your deployment, you can follow the instructions in section [On Premises Single Node PRO Administration](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/admin/index.md).

Regarding the configuration of your deployment, you can follow the instructions in section [Changing Configuration](https://openvidu.io/3.8/docs/self-hosting/configuration/changing-config/index.md). Additionally, the [How to Guides](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, an Azure deployment provides the capability to manage global configurations via the Azure portal using Key Vault Secrets created during the deployment:

**Changing configuration through Key Vault secrets**

1. Navigate to the [Azure Portal Dashboard](https://portal.azure.com/#home) on Azure.
1. Select the Resource Group where you deployed your OpenVidu Single Node PRO Stack.
1. In the *"stackname-keyvault"* resource, click on *"Objects"* -> *"Secrets"* on the left panel. This will show you all the secrets that are stored in the Key Vault of the OpenVidu deployment. Azure Key Vault secrets location
1. Click on the desired secret you want to change and click on *"New Version"*. Azure Key Vault New Version Secret
1. Enter the new secret value on *"Secret Value"* field and click on *"Create"*. Azure Key Vault New Version Secret Create
1. Go to the Instance resource of OpenVidu and click on *"Restart"* to apply the changes to the OpenVidu Single Node PRO deployment. Reboot Instance

Changes will be applied automatically.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
