---
title: OpenVidu Single Node administration on Azure
description: Learn how to perform administrative tasks on an Azure OpenVidu Single Node deployment
---

# OpenVidu Single Node Administration: Azure

Azure deployment of OpenVidu Single Node is internally identical to the on-premises deployment and AWS deployment, so you can follow the same instructions from the [On Premises Single Node](../on-premises/admin.md) for administration and configuration. The only difference is that the deployment is automated with ARM Templates from Azure.

However, there are certain things worth mentioning:

## Start and stop OpenVidu through Azure Portal

You can start and stop all services as explained in the [On Premises Single Node](../on-premises/admin.md#starting-stopping-and-restarting-openvidu) section. But you can also start and stop the Virtual Machine instance directly from Azure Portal. This will stop all services running in the instance and reduce Azure costs.

=== "Stop OpenVidu Single Node"

    1. Go to [Azure Portal Dashboard](https://portal.azure.com/#home){:target="_blank"} of Azure and enter into the resource group where you deployed OpenVidu Single Node.
    2. There, you will find the Virtual Machine that runs OpenVidu, its name should be something like **yourstackname-VM-CE**, click on it.
    3. In the section of the Virtual Machine click on stop button to stop the Virtual Mache and in consequence OpenVidu.

    <figure markdown>
    ![Stop instance](../../../../assets/images/self-hosting/single-node/azure/stop-instance.png){ .svg-img .dark-img }
    </figure>

=== "Start OpenVidu Single Node"

    1. Go to [Azure Portal Dashboard](https://portal.azure.com/#home){:target="_blank"} of Azure and enter into the resource group where you deployed OpenVidu Single Node.
    2. There, you will find the Virtual Machine that runs OpenVidu, its name should be something like **yourstackname-VM-CE**, click on it.
    3. In the section of the Virtual Machine click on start button to start the Virtual Mache and in consequence OpenVidu.

    <figure markdown>
    ![Start instance](../../../../assets/images/self-hosting/single-node/azure/start-instance.png){ .svg-img .dark-img }
    </figure>

## Change the instance type

You can change the instance type of the OpenVidu Single Node instance to adapt it to your needs. To do this, follow these steps:

1. Go to [Azure Portal Dashboard](https://portal.azure.com/#home){:target="_blank"} of Azure and enter into the resource group where you deployed OpenVidu Single Node.
2. There, you will find the Virtual Machine that runs OpenVidu, its name should be something like **yourstackname-VM-CE**, click on it.
3. In the left pannel you will find a section called _"Availability + scale"_, click on it and then in _"Size"_ tab.

    === "Change instance type"

        <figure markdown>
        ![Change instance type](../../../../assets/images/self-hosting/single-node/azure/azure-instance-type.png){ .svg-img .dark-img }
        </figure>

4. Select the new instance type and click on _"Resize"_.

## Administration and Configuration (TODO)

For administration, you can follow the instructions from the [On Premises Single Node Administration](../on-premises/admin.md) section.

Regarding the configuration, in Azure it is managed similarly to an on-premises deployment or an AWS deployment. For detailed instructions, please refer to the [Changing Configuration](../../configuration/changing-config.md) section. Additionally, the [How to Guides](../../how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, an Azure deployment provides the capability to manage global configurations via the Azure portal using KeyVault Secrets created during the deployment. To manage configurations this way, follow these steps:

=== "Changing Configuration through KeyVault secrets"

    1. Navigate to the [Azure Portal Dashboard](https://portal.azure.com/#home){:target=_blank} on Azure.
    2. Select the Resource Group where you deployed your OpenVidu Single Node Stack.
    3. In the _"stackname-keyvault"_ resource, click at _"Objects -> Secrets"_ on the left panel. This will open the KeyVault Secrets Manager which contains all the configurations of the OpenVidu Single Node deployment.
        <figure markdown>
        ![Select KeyVault Secrets Manager](../../../../assets/images/self-hosting/single-node/azure/outputs.png){ .svg-img .dark-img }
        </figure>
    4. Click on the _"Retrieve secret value"_ button to get the JSON with all the information.
        <figure markdown>
        ![Retrieve Secret Value](../../../../assets/images/self-hosting/single-node/azure/1-secrets-retrieve.png){ .svg-img .dark-img }
        </figure>
    5. Modify the parameter you want to change and click on _"Save"_. The changes will be applied to the OpenVidu Single Node deployment.
    6. Go to the Instance resource of OpenVidu and click on _"Restart"_ to apply the changes to the Master Node.
        <figure markdown>
        ![Reboot Instance](../../../../assets/images/self-hosting/single-node/azure/reboot-instance.png){ .svg-img .dark-img }
        </figure>

    The changes will be applied automatically.
