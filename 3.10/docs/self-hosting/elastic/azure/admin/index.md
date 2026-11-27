# OpenVidu Elastic administration: Azure

Azure

The deployment of OpenVidu Elastic on Azure is automated using Azure Resource Manager Templates, with Media Nodes managed within a [Virtual Machine Scale Set](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/overview) . This group dynamically adjusts the number of instances based on a target average CPU usage.

Internally, the Azure Elastic deployment mirrors the On Premises Elastic deployment, allowing you to follow the same administration and configuration guidelines of the [On Premises Elastic](https://openvidu.io/latest/docs/self-hosting/elastic/on-premises/admin/index.md) documentation. However, there are specific considerations unique to the Azure environment that are worth keeping in mind:

## Cluster shutdown and startup

The Master Node is a Virtual Machine Instance, while the Media Nodes are part of a Virtual Machine Scale Set. The process for starting and stopping these components differs:

**Shutting down the cluster**

To shut down the cluster, you need to stop the Media Nodes and then stop the Master Node.

> **Gracefully stopping Media Nodes**
>
> There is currently a limitation with Media Nodes that prevents them from stopping gracefully on a manual shutdown — they will terminate immediately without waiting for active Rooms to complete.
>
> Wait for your active Rooms to finish before stopping the cluster, or SSH into each Media Node and run **`/usr/local/bin/stop_media_node.sh`** to drain it manually before stopping.

1. Navigate to the [Azure Portal Dashboard](https://portal.azure.com/#home) and go to the Resource Group where you deployed OpenVidu Elastic.
1. Then click into the Virtual Machine Scale Set resource called `<STACK_NAME>-mediaNodeScaleSet` and click *"Availability + scale"* on the left panel, then click the *"Scaling"* option.
1. On this tab, scroll to the bottom and modify the *"Instance Limits"* to 0.
1. Click *"Save"* and wait for it to complete. You can check the progress in the *"Instances"* tab.
1. After confirming that all Media Node instances are terminated, go back to the Resource Group and locate the resource called *"stackName-VM-MasterNode"*. Click on it to go to the Master Node instance. There, click on *"Stop"* to stop the instance.

**Starting up the cluster**

To start the cluster, first start the Master Node and then the Media Nodes.

1. Navigate to the [Azure Portal Dashboard](https://portal.azure.com/#home) and go to the Resource Group where you deployed OpenVidu Elastic.
1. In the resource group click on the resource called *"stackName-VM-MasterNode"*, then click *"Start"* to start the Master Node.
1. Wait until the instance is running.
1. Go back to the Resource Group, and there click into the Virtual Machine Scale Set resource called *"stackName-mediaNodeScaleSet"* and click *"Availability + scale"* on the left panel, then click the *"Scaling"* option.
1. On this tab, modify the *"Instance Limits"* to your desired values.
1. Click *"Save"* and wait for it to complete. You can check the progress in the *"Instances"* tab.

## Change the instance type

It is possible to change the instance type of both the Master Node and the Media Nodes. However, since the Media Nodes are part of a Virtual Machine Scale Set, the process differs. The following section details the procedures:

**Master Nodes**

> **Warning**
>
> This procedure requires downtime, as it involves stopping the Master Node.

1. [Shutdown the cluster](#shutting-down-the-cluster).

   > **Info**
   >
   > You can stop only the Master Node instance to change its instance type, but it is recommended to stop the whole cluster to avoid any issues.

1. Go to the Azure Resource Group where you deployed and locate the resource with the name *"stackName-VM-MasterNode"* and click on it.

1. On the left panel click on *"Availability + scale"* tab and inside click on *"Size"* tab. Then select the size you desire and click on *"Resize"*

1. [Start the cluster](#starting-up-the-cluster).

**Media Nodes**

> **Info**
>
> This will forcibly restart the Media Nodes. If you want to stop them gracefully to avoid the disruption of active Rooms, check the [Shutting down the cluster](#shutting-down-the-cluster) tab.

1. Go to the [Azure Portal Dashboard](https://portal.azure.com/#home) on Azure.
1. Select the Resource Group where you deployed OpenVidu Elastic.
1. Locate the resource with the name *"stackName-mediaNodeScaleSet"*. Click on it to navigate to the Virtual Machine Scale Set.
1. On the left panel click on *"Availability + scale"* tab, then on *"Size"*.
1. Select the new instance type and click on *"Resize"*.

## Media Nodes Autoscaling Configuration

You can modify the autoscaling configuration of the Media Nodes by adjusting the scaling rules of the Virtual Machine Scale Set:

**Media Nodes Autoscaling Configuration**

1. Go to the [Azure Portal Dashboard](https://portal.azure.com/#home) on Azure.

1. Select the Resource Group where you deployed OpenVidu Elastic.

1. Locate the resource with the name *"stackName-mediaNodeScaleSet"* and click on it.

1. On the left panel click on *"Availability + scale"* tab and inside click on *"Scaling"* option.

1. In the *"Default"* box you will find a section called *"Rules"*. Here you can add new rules or modify existing ones.

   > **Info**
   >
   > Currently there is only one rule to scale out. We are actively working on providing a graceful scale-in process for Media Nodes to avoid active Rooms disruption.

**Modify existing rules**

Click on the rule you want to modify and change the **Criteria** as desired. To accept the changes click on *"Update*".

**Add a new rule**

Click on *"Add a rule"* option and fill the **Criteria** as desired. To add the rule click on *"Add"*.

> **Info**
>
> OpenVidu Elastic is by default configured with a *"Target tracking scaling"* policy that scales based on the target average CPU usage. However, you can configure different autoscaling policies according to your needs. For more information on the various types of autoscaling policies and how to implement them, refer to the [Azure Scaling Set documentation](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-autoscale-portal) .

## Fixed Number of Media Nodes

The **Fixed Number Of Media Nodes** parameter of the template selects how the number of Media Nodes is managed:

- **Autoscaling mode** (`0`, the default): the autoscale setting of the Virtual Machine Scale Set adds and removes Media Nodes based on CPU usage, between **Min Number Of Media Nodes** and **Max Number Of Media Nodes**, as described in [Media Nodes Autoscaling Configuration](#media-nodes-autoscaling-configuration).
- **Fixed mode** (a value greater than `0`): the autoscale profile of the Scale Set is pinned to that number, with its minimum, maximum and default instance counts all set to it, so CPU usage never changes the number of Media Nodes. **Initial Number Of Media Nodes**, **Min Number Of Media Nodes**, **Max Number Of Media Nodes** and **Scale Target CPU** are ignored.

**Change Fixed Number of Media Nodes**

1. Go to the [Azure Portal Dashboard](https://portal.azure.com/#home) on Azure.
1. Select the Resource Group where you deployed OpenVidu Elastic, and on the left panel click on *"Settings"* > *"Deployments"*.
1. Select the deployment of OpenVidu and click on *"Redeploy"*.
1. Set **Fixed Number Of Media Nodes** to the number of Media Nodes you want, keep the rest of the parameters as they are, and click on *"Review + create"* and then on *"Create"*.
1. Wait for the deployment to complete. The autoscale setting then brings the Scale Set to the new number. You can follow the Media Nodes in the *"Instances"* tab of the resource *"stackName-mediaNodeScaleSet"*.

Raising the number adds Media Nodes. To lower it, first remove the extra Media Nodes gracefully as described in [Lower the number of Media Nodes](#lower-the-number-of-media-nodes), and then redeploy with the new number.

### Lower the number of Media Nodes

Media Nodes protect themselves from scale-in, so that only a graceful drain removes them, and Azure does not accept an autoscale setting whose minimum or maximum is below the number of Media Nodes that are running. A redeploy that sets **Fixed Number Of Media Nodes**, **Min Number Of Media Nodes** or **Max Number Of Media Nodes** below that number fails with `UnsupportedCapacity`. Remove the extra Media Nodes first:

1. Go to the Resource Group where you deployed OpenVidu Elastic, click into the Virtual Machine Scale Set resource called *"stackName-mediaNodeScaleSet"* and click *"Availability + scale"* on the left panel, then click the *"Scaling"* option.

1. Select *"Manual scale"*, keep the instance count as it is and click *"Save"*. The autoscale setting no longer adds or removes Media Nodes.

1. For each Media Node to remove, select it in the *"Instances"* tab, click on *"Run command"* > *"RunShellScript"*, and run:

   ```bash
   sudo systemd-run --unit=openvidu-stop-media-node --setenv=HOME=/root /usr/local/bin/stop_media_node.sh
   ```

   The Media Node stops accepting new Rooms and removes itself from the Scale Set when its ongoing Rooms, recordings and ingests end. `systemd-run` keeps the drain running after the Run command returns, however long the Rooms last.

1. When the Scale Set has the number of Media Nodes you want, redeploy with it as described in the *"Change Fixed Number of Media Nodes"* tab above, or with the new **Min Number Of Media Nodes** in autoscaling mode. The redeploy turns autoscaling back on.

### Switch between autoscaling and a fixed number

**Back to autoscaling**

1. Follow the steps of the *"Change Fixed Number of Media Nodes"* tab above, setting **Fixed Number Of Media Nodes** to `0`. Change **Min Number Of Media Nodes**, **Max Number Of Media Nodes** and **Scale Target CPU** too if you do not want their current values.
1. When the deployment completes, the autoscale setting scales on CPU usage again, starting from the Media Nodes that are running, and adds Media Nodes if there are fewer than **Min Number Of Media Nodes**. **Min Number Of Media Nodes** and **Max Number Of Media Nodes** cannot be below the Media Nodes that are running: to go lower, remove the extra ones first as described in [Lower the number of Media Nodes](#lower-the-number-of-media-nodes).

**From autoscaling to a fixed number**

1. Follow the steps of the *"Change Fixed Number of Media Nodes"* tab above, setting **Fixed Number Of Media Nodes** to the number of Media Nodes you want.
1. When the deployment completes, the autoscale setting is pinned to that number, and Media Nodes are added if fewer are running. If more Media Nodes are running than the number you set, remove the extra ones first as described in [Lower the number of Media Nodes](#lower-the-number-of-media-nodes): Azure does not accept the deployment otherwise.

> **What a redeploy changes**
>
> - A redeploy never changes the number of Media Nodes by itself: the template does not set the instance count of the Scale Set, only the limits of its autoscale setting, which then adds Media Nodes up to its minimum. **Initial Number Of Media Nodes** applies only when the deployment is created.
> - The autoscale setting is rewritten from the template parameters, so changes made by hand to its rules or instance limits in the portal (see [Media Nodes Autoscaling Configuration](#media-nodes-autoscaling-configuration)) are replaced.

## Administration and configuration

Regarding the administration of your deployment, you can follow the instructions in section [On Premises Elastic Administration](https://openvidu.io/latest/docs/self-hosting/elastic/on-premises/admin/index.md).

Regarding the configuration of your deployment, you can follow the instructions in section [Changing Configuration](https://openvidu.io/latest/docs/self-hosting/configuration/changing-config/index.md). Additionally, the [How to Guides](https://openvidu.io/latest/docs/self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, an Azure deployment provides the capability to manage global configurations via the Azure portal using Key Vault Secrets created during the deployment:

**Changing configuration through Key Vault secrets**

1. Navigate to the [Azure Portal Dashboard](https://portal.azure.com/#home) on Azure.
1. Select the Resource Group where you deployed OpenVidu Elastic.
1. In the *"stackname-keyvault"* resource, click on *"Objects"* -> *"Secrets"* on the left panel. This will show you all the secrets that are stored in the Key Vault of the OpenVidu Elastic deployment.
1. Click on the desired secret you want to change and click on *"New Version"*.
1. Enter the new secret value on *"Secret Value"* field and click on *"Create"*.
1. Go to the Master Node resource and click on *"Restart"* to apply the changes to the OpenVidu Elastic deployment.

Changes will be applied automatically.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/latest/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
