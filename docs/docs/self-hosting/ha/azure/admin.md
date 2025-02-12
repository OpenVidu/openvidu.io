---
title: OpenVidu High Availability administration on Azure
description: Learn how to perform administrative tasks on an Azure OpenVidu High Availability deployment
---

# OpenVidu High Availability Administration: Azure

The deployment of OpenVidu High Availability on Azure is automated using Templates from ARM, with 4 Virtual Machine Instances as Master Nodes and any number of Media Nodes managed within an [Virtual Machine Scaling Set](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/overview){:target=_blank}. The Virtual Machine Scale Set of Media Nodes is configured to scale based on the target average CPU utilization.   

Internally, the Azure deployment mirrors the on-premises setup, allowing you to follow the same administration and configuration guidelines provided in the [On Premises High Availability](../on-premises/admin.md) documentation. However, there are specific considerations unique to the Azure environment that are worth taking into account.

## Cluster Shutdown and Startup

You can start and stop the OpenVidu High Availability cluster at any time. The following sections detail the procedures.

=== "Shutdown the Cluster"

    To shut down the cluster, you need to stop the Media Nodes and then stop the Master Nodes.

    !!! warning "Gracefully stop of Media Nodes"

        We have a limitation in Media Nodes that makes them to doesn't stop gracefully, be carefull stopping Media Nodes because they will simply stop without waiting for the possible ongoing sesion. You may wait for them to finish and then stop the cluster.   
        We are working on removing this limitation, to leave the same behavior as we have in AWS or in OnPremises deployments. Currently the Media Nodes have a script that can make a gracefully stop of them, ssh to the Media Node you want to stop and execute `./usr/local/bin/stop_media_node.sh`

    1. Navigate to the [Azure Portal Dashboard](https://portal.azure.com/#home){:target=_blank} and go to the Resource Group where you deployed OpenVidu HA.
    2. Then click into the Virtual Machine Scale Set resource called _"stackName-mediaNodeScaleSet"_ and click _"Availability + scale"_ on the left panel, here click on _"Scaling"_ option.
        <figure markdown>
        ![Selecting scaling menu Scale Set](../../../../assets/images/self-hosting/ha/azure/azure-ha-admin-scaling-tab.png){ .svg-img .dark-img }
        </figure>
    3. On this tab, go at the very bottom and modify the _"Instance Limits"_ to 0.
        <figure markdown>
        ![Edit Scaling Set Group](../../../../assets/images/self-hosting/ha/azure/azure-ha-admin-edit-media-ss-to-stop.png){ .svg-img .dark-img }
        </figure>
    4. Click on save and wait until is completed, you can check how is going in the _"Instances"_ tab.
        <figure markdown>
        ![Location Instance Tab](../../../../assets/images/self-hosting/ha/azure/azure-admin-instance-tab.png){ .svg-img .dark-img }
        </figure>
    5. After confirming that all Media Node instances are terminated, go back to the Resource Group and locate the resource called _"stackName-VM-MasterNode1"_. Click on it to go to the Master Node 1 instance. There, click on _"Stop"_ to stop the instance.
        <figure markdown>
        ![Delete Deployment Stack](../../../../assets/images/self-hosting/ha/azure/azure-ha-admin-stop-master.png){ .svg-img .dark-img }
        </figure>
    6. Repeat step 5 for all the Master Nodes to stop them all.

=== "Startup the Cluster"

    To start the cluster, we recommend starting the Master Node first and then the Media Nodes.

    1. Navigate to the [Azure Portal Dashboard](https://portal.azure.com/#home){:target=_blank} and go to the Resource Group where you deployed OpenVidu HA.
    2. In the resource group click on the resource called _"stackName-VM-MasterNode1"_, here click on start to start the Master Node 1.
        <figure markdown>
        ![Start Master Node](../../../../assets/images/self-hosting/ha/azure/azure-ha-admin-start-master.png){ .svg-img .dark-img }
        </figure>
    3. Wait until the instance is running.
    4. Repeat the step 2 and 3 for all the Master Nodes until they are all up and running.
    5. Go back to the Resource Group, and there click into the Virtual Machine Scale Set resource called _"stackName-mediaNodeScaleSet"_ and click _"Availability + scale"_ on the left panel, here click on _"Scaling"_ option.
        <figure markdown>
        ![Selecting scaling menu Scale Set](../../../../assets/images/self-hosting/ha/azure/azure-ha-admin-scaling-tab.png){ .svg-img .dark-img }
        </figure>
    6. On this tab, go at the very bottom and modify the _"Instance Limits"_ to your desired ones.
        <figure markdown>
        ![Edit Scaling Set Group](../../../../assets/images/self-hosting/ha/azure/azure-ha-admin-edit-media-ss-to-start.png){ .svg-img .dark-img }
        </figure>
    7. Click on save and wait until is completed, you can check how is going in the _"Instances"_ tab.
        <figure markdown>
        ![Location Instance Tab](../../../../assets/images/self-hosting/ha/azure/azure-admin-instance-tab.png){ .svg-img .dark-img }
        </figure>


## Change the instance type

It is possible to change the instance type of both the Master Node and the Media Nodes. The following section details the procedures.

=== "Master Nodes"

    !!! warning
        
        This procedure requires downtime, as it involves stopping the Master Node.

    1. [Shutdown the cluster](#shutdown-the-cluster).
    2. Go to the Azure Resource Group where you deployed and locate the resource with the name _"stackName-VM-MasterNode1"_ and click on it.
    3. On the left panel click on _"Availability + scale"_ tab and inside click on _"Size"_ tab. Then select the size you desire and click on _"Resize"_
        <figure markdown>
        ![Change instance type master](../../../../assets/images/self-hosting/ha/azure/azure-instance-type-master.png){ .svg-img .dark-img }
        </figure>
    4. Repeat steps 2 and 3 for all the Master Nodes just in case you want to resize all of them, if not just do it for the ones you want.
    4. [Start the cluster](#startup-the-cluster).

=== "Media Nodes"

    !!! info
        
        This will restart the media nodes without the gracefully delete option, if you want to stop them gracefully check the [Shutdown the Cluster](#shutdown-the-cluster) tab

    1. Go to the [Azure Portal Dashboard](https://portal.azure.com/#home){:target=_blank} on Azure.
    2. Select the Resource Group where you deployed OpenVidu High Availability.
    3. Locate the resource with the name _"stackName-mediaNodeScaleSet"_. Click on it to go to the Virtual Machine Scale Set.
    4. On the left panel click on _"Availability + scale"_ tab and inside click on _"Size"_.
        <figure markdown>
        ![Change instance type media](../../../../assets/images/self-hosting/ha/azure/azure-instance-type-media.png){ .svg-img .dark-img }
        </figure>
    5. Select the new instance type and click on _"Resize"_.

## Media Nodes Autoscaling Configuration

To configure the Auto Scaling settings for the Media Nodes, follow the steps outlined below. This configuration allows you to set the parameters that control how the Virtual Machine Scale Set will scale based on the target average CPU utilization.

=== "Media Nodes Autoscaling Configuration"

    1. Go to the [Azure Portal Dashboard](https://portal.azure.com/#home){:target=_blank} on Azure.
    2. Select the Resource Group where you deployed OpenVidu High Availavility.
    3. Locate the resource with the name _"stackName-mediaNodeScaleSet"_ and click on it.
    4. On the left panel click on _"Availability + scale"_ tab and inside click on _"Scaling"_ option.
        <figure markdown>
        ![Select scaling option](../../../../assets/images/self-hosting/ha/azure/azure-ha-admin-scaling-tab.png){ .svg-img .dark-img }
        </figure>
    5. To configure scaling policies, navigate to the very bottom in the _"Default"_ box, you will find there a section called _"Rules"_. Here you can add new rules or else modify the existing ones
        
        !!! warning

            You will find just one rule to scale out, thats because we have not implemented the gracefully delete of the media nodes and we are not scaling in this cluster by default.

        <figure markdown>
        ![Rules section](../../../../assets/images/self-hosting/ha/azure/azure-rules-section-ss.png){ .svg-img .dark-img }
        </figure>

    === "Modify existing rules"
        
        If you chose to modifying an existing rule you just need to click on the rule you want to modify and change the **Criteria** based on your choices. When you are done, click on _"Update_".
        <figure markdown>
        ![Modify an existing rule](../../../../assets/images/self-hosting/ha/azure/azure-rules-modify-rule-ss.png){ .svg-img .dark-img }
        </figure>

    === "Add a new rule"

        If you chose to add a new rule you just need to click on _"Add a rule"_ option and fill the **Criteria** based on your choices. When you are done, click on _"Add"_.
        <figure markdown>
        ![Modify an existing rule](../../../../assets/images/self-hosting/ha/azure/azure-rules-add-rule-ss.png){ .svg-img .dark-img }
        </figure>

    !!! info
        
        OpenVidu High Availability is by default configured with a _"Target tracking scaling"_ policy that scales based on the target average CPU utilization, however, you can configure different autoscaling policies according to your needs. For more information on the various types of autoscaling policies and how to implement them, refer to the [Azure Scaling Set documentation](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-autoscale-portal){:target=_blank}.

## Fixed Number of Media Nodes

If you need to maintain a fixed number of Media Nodes instead of allowing the Virtual Machine Scale Set to dynamically adjust based on CPU utilization, you can configure the desired capacity settings accordingly. Follow the steps below to set a fixed number of Media Nodes:

=== "Set Fixed Number of Media Nodes"

    1. Go to the [Azure Portal Dashboard](https://portal.azure.com/#home){:target=_blank} on Azure.
    2. Select the Resource Group where you deployed OpenVidu High Availability, locate the resource with the name _"stackName-mediaNodeScaleSet"_ and click on it
    3. On the left panel click on _"Availability + scale"_ and then in _"Scaling"_ tab.
        <figure markdown>
        ![Selecting scaling menu Scale Set](../../../../assets/images/self-hosting/ha/azure/azure-ha-admin-scaling-tab.png){ .svg-img .dark-img }
        </figure>
    4. On this tab, go at the very bottom and modify the _"Instance Limits"_ to the value of fixed number of media nodes you want. In this case is set to 2.
        <figure markdown>
        ![Edit Scaling Set Group](../../../../assets/images/self-hosting/ha/azure/azure-ha-admin-edit-media-ss-fixed.png){ .svg-img .dark-img }
        </figure>
    5. Click on save and wait until is completed, you can check how is going in the _"Instances"_ tab.
        <figure markdown>
        ![Location Instance Tab](../../../../assets/images/self-hosting/ha/azure/azure-admin-instance-tab.png){ .svg-img .dark-img }
        </figure>


## Administration and Configuration (TODO)

For administration, you can follow the instructions from the [On Premises High Availability Administration](../on-premises/admin.md) section.

Regarding the configuration, in Azure it is managed similarly to an on-premises deployment. For detailed instructions, please refer to the [Changing Configuration](../../configuration/changing-config.md) section. Additionally, the [How to Guides](../../how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, an Azure deployment provides the capability to manage global configurations via the Azure portal using KeyVault Secrets created during the deployment. To manage configurations this way, follow these steps:

=== "Changing Configuration through KeyVault secrets"

    1. Navigate to the [Azure Portal Dashboard](https://portal.azure.com/#home){:target=_blank} on Azure.
    2. Select the Resource Group where you deployed your OpenVidu High Availability Stack.
    3. In the _"stackname-keyvault"_ resource, click at _"Objects -> Secrets"_ on the left panel. This will open the KeyVault Secrets Manager which contains all the configurations of the OpenVidu High Availability deployment.
        <figure markdown>
        ![Select KeyVault Secrets Manager](../../../../assets/images/self-hosting/ha/azure/outputs.png){ .svg-img .dark-img }
        </figure>
    4. Click on the _"Retrieve secret value"_ button to get the JSON with all the information.
        <figure markdown>
        ![Retrieve Secret Value](../../../../assets/images/self-hosting/ha/azure/1-secrets-retrieve.png){ .svg-img .dark-img }
        </figure>
    5. Modify the parameter you want to change and click on _"Save"_. The changes will be applied to the OpenVidu High Availability deployment.
    6. Go to the Instance resource of OpenVidu and click on _"Restart"_ to apply the changes to the Master Node.
        <figure markdown>
        ![Reboot Instance](../../../../assets/images/self-hosting/ha/azure/reboot-instance.png){ .svg-img .dark-img }
        </figure>

    The changes will be applied automatically.