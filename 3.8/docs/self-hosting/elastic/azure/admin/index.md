# OpenVidu Elastic administration: Azure

Azure

The deployment of OpenVidu Elastic on Azure is automated using Azure Resource Manager Templates, with Media Nodes managed within a [Virtual Machine Scale Set](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/overview) . This group dynamically adjusts the number of instances based on a target average CPU usage.

Internally, the Azure Elastic deployment mirrors the On Premises Elastic deployment, allowing you to follow the same administration and configuration guidelines of the [On Premises Elastic](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/admin/index.md) documentation. However, there are specific considerations unique to the Azure environment that are worth keeping in mind:

## Cluster shutdown and startup

The Master Node is a Virtual Machine Instance, while the Media Nodes are part of a Virtual Machine Scale Set. The process for starting and stopping these components differs:

**Shutting down the cluster**

To shut down the cluster, you need to stop the Media Nodes and then stop the Master Node.

Gracefully stopping Media Nodes

There is currently a limitation with Media Nodes that prevents them from stopping gracefully on a manual shutdown — they will terminate immediately without waiting for active Rooms to complete.

Wait for your active Rooms to finish before stopping the cluster, or SSH into each Media Node and run **`/usr/local/bin/stop_media_node.sh`** to drain it manually before stopping.

1. Navigate to the [Azure Portal Dashboard](https://portal.azure.com/#home) and go to the Resource Group where you deployed OpenVidu Elastic.
1. Then click into the Virtual Machine Scale Set resource called `<STACK_NAME>-mediaNodeScaleSet` and click *"Availability + scale"* on the left panel, then click the *"Scaling"* option. Selecting scaling menu Scale Set
1. On this tab, scroll to the bottom and modify the *"Instance Limits"* to 0. Edit Scaling Set Group
1. Click *"Save"* and wait for it to complete. You can check the progress in the *"Instances"* tab. Location Instance Tab
1. After confirming that all Media Node instances are terminated, go back to the Resource Group and locate the resource called *"stackName-VM-MasterNode"*. Click on it to go to the Master Node instance. There, click on *"Stop"* to stop the instance. Delete Deployment Stack

**Starting up the cluster**

To start the cluster, first start the Master Node and then the Media Nodes.

1. Navigate to the [Azure Portal Dashboard](https://portal.azure.com/#home) and go to the Resource Group where you deployed OpenVidu Elastic.
1. In the resource group click on the resource called *"stackName-VM-MasterNode"*, then click *"Start"* to start the Master Node. Start Master Node
1. Wait until the instance is running.
1. Go back to the Resource Group, and there click into the Virtual Machine Scale Set resource called *"stackName-mediaNodeScaleSet"* and click *"Availability + scale"* on the left panel, then click the *"Scaling"* option. Selecting scaling menu Scale Set
1. On this tab, modify the *"Instance Limits"* to your desired values. Edit Scaling Set Group
1. Click *"Save"* and wait for it to complete. You can check the progress in the *"Instances"* tab. Location Instance Tab

## Change the instance type

It is possible to change the instance type of both the Master Node and the Media Nodes. However, since the Media Nodes are part of a Virtual Machine Scale Set, the process differs. The following section details the procedures:

**Master Nodes**

Warning

This procedure requires downtime, as it involves stopping the Master Node.

1. [Shutdown the cluster](#shutting-down-the-cluster).

   Info

   You can stop only the Master Node instance to change its instance type, but it is recommended to stop the whole cluster to avoid any issues.

1. Go to the Azure Resource Group where you deployed and locate the resource with the name *"stackName-VM-MasterNode"* and click on it.

1. On the left panel click on *"Availability + scale"* tab and inside click on *"Size"* tab. Then select the size you desire and click on *"Resize"*

   Change instance type master

1. [Start the cluster](#starting-up-the-cluster).

**Media Nodes**

Info

This will forcibly restart the Media Nodes. If you want to stop them gracefully to avoid the disruption of active Rooms, check the [Shutting down the cluster](#shutting-down-the-cluster) tab.

1. Go to the [Azure Portal Dashboard](https://portal.azure.com/#home) on Azure.
1. Select the Resource Group where you deployed OpenVidu Elastic.
1. Locate the resource with the name *"stackName-mediaNodeScaleSet"*. Click on it to navigate to the Virtual Machine Scale Set.
1. On the left panel click on *"Availability + scale"* tab, then on *"Size"*. Change instance type media
1. Select the new instance type and click on *"Resize"*.

## Media Nodes Autoscaling Configuration

You can modify the autoscaling configuration of the Media Nodes by adjusting the scaling rules of the Virtual Machine Scale Set:

**Media Nodes Autoscaling Configuration**

1. Go to the [Azure Portal Dashboard](https://portal.azure.com/#home) on Azure.

1. Select the Resource Group where you deployed OpenVidu Elastic.

1. Locate the resource with the name *"stackName-mediaNodeScaleSet"* and click on it.

1. On the left panel click on *"Availability + scale"* tab and inside click on *"Scaling"* option. Select scaling option

1. In the *"Default"* box you will find a section called *"Rules"*. Here you can add new rules or modify existing ones.

   Info

   Currently there is only one rule to scale out. We are actively working on providing a graceful scale-in process for Media Nodes to avoid active Rooms disruption.

   Rules section

**Modify existing rules**

Click on the rule you want to modify and change the **Criteria** as desired. To accept the changes click on *"Update*".

Modify an existing rule

**Add a new rule**

Click on *"Add a rule"* option and fill the **Criteria** as desired. To add the rule click on *"Add"*.

Modify an existing rule

Info

OpenVidu Elastic is by default configured with a *"Target tracking scaling"* policy that scales based on the target average CPU usage. However, you can configure different autoscaling policies according to your needs. For more information on the various types of autoscaling policies and how to implement them, refer to the [Azure Scaling Set documentation](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-autoscale-portal) .

## Fixed Number of Media Nodes

If you prefer to maintain a fixed number of Media Nodes instead of allowing the Virtual Machine Scale Set to perform dynamic scaling:

**Set Fixed Number of Media Nodes**

1. Go to the [Azure Portal Dashboard](https://portal.azure.com/#home) on Azure.
1. Select the Resource Group where you deployed OpenVidu Elastic, locate the resource with the name *"stackName-mediaNodeScaleSet"* and click on it
1. On the left panel click on *"Availability + scale"* and then in *"Scaling"* tab. Selecting scaling menu Scale Set
1. On this tab, scroll to the bottom and modify the *"Instance Limits"* to the value of fixed number of Media Nodes you want. In this case it is set to 2. Edit Scaling Set Group
1. Click *"Save"* and wait for it to complete. You can check the progress in the *"Instances"* tab. Location Instance Tab

## Administration and configuration

Regarding the administration of your deployment, you can follow the instructions in section [On Premises Elastic Administration](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/admin/index.md).

Regarding the configuration of your deployment, you can follow the instructions in section [Changing Configuration](https://openvidu.io/3.8/docs/self-hosting/configuration/changing-config/index.md). Additionally, the [How to Guides](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, an Azure deployment provides the capability to manage global configurations via the Azure portal using Key Vault Secrets created during the deployment:

**Changing configuration through Key Vault secrets**

1. Navigate to the [Azure Portal Dashboard](https://portal.azure.com/#home) on Azure.
1. Select the Resource Group where you deployed OpenVidu Elastic.
1. In the *"stackname-keyvault"* resource, click on *"Objects"* -> *"Secrets"* on the left panel. This will show you all the secrets that are stored in the Key Vault of the OpenVidu Elastic deployment. Azure Key Vault secrets location
1. Click on the desired secret you want to change and click on *"New Version"*. Azure Key Vault New Version Secret
1. Enter the new secret value on *"Secret Value"* field and click on *"Create"*. Azure Key Vault New Version Secret Create
1. Go to the Master Node resource and click on *"Restart"* to apply the changes to the OpenVidu Elastic deployment. Reboot Instance

Changes will be applied automatically.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
