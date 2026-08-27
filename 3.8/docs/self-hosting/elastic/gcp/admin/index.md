# OpenVidu Elastic administration: Google Cloud Platform

Google Cloud Platform

The deployment of OpenVidu Elastic on Google Cloud Platform is automated using Infrastructure Manager in Google Cloud Console, with Media Nodes managed within a [Managed Instance Group](https://cloud.google.com/compute/docs/instance-groups?hl=en) . This group dynamically adjusts the number of instances based on a target average CPU usage.

Internally, the Google Cloud Platform Elastic deployment mirrors the On Premises Elastic deployment, allowing you to follow the same administration and configuration guidelines of the [On Premises Elastic](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/admin/index.md) documentation. However, there are specific considerations unique to the Google Cloud Platform environment that are worth keeping in mind:

## Cluster shutdown and startup

The Master Node is a Virtual Machine Instance, while the Media Nodes are part of a Managed Instance Group. The process for starting and stopping these components differs:

**Shutting down the cluster**

To shut down the cluster, you need to stop the Media Nodes and then stop the Master Node.

1. Navigate to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .

1. Then click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.

   Edit Button Location MIG

1. On this tab, go to the **Group Size & autoscaling** tab and change the *"Minimum"* and *"Maximum"* number of instances to 0.

   Edit MIG

1. Click *"Save"* and wait for it to complete. You can check the progress in the *"VM instances"* tab.

   Save Edits MIG

1. After confirming that all Media Node instances are terminated, in *"VM instances"* tab select the instance called `<STACK_NAME>-master-node`. Click on it to go to the Master Node instance. There, click on "Stop" to stop the instance.

   Stop Master Node MIG

**Starting up the cluster**

To start the cluster, first start the Master Node and then the Media Nodes.

1. Navigate to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .

1. In *"VM instances"* tab select the instance called `<STACK_NAME>-master-node`, then click *"Start"* to start the Master Node.

   Start Master Node

1. Wait until the instance is running.

1. Go to the *"Instance Groups"* tab, and there click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.

   Edit Button Location MIG

1. Go to the **Group Size & autoscaling** tab and change the *"Minimum"* and *"Maximum"* number of instances to your desired values.

   Edit MIG

1. Click *"Save"* and wait for it to complete. You can check the progress in the *"Instances"* tab.

   Save Edits MIG

## Change the instance type

It is possible to change the instance type of both the Master Node and the Media Nodes. However, since the Media Nodes are part of a Managed Instance Group, the process differs. The following section details the procedures:

**Master Nodes**

Warning

This procedure requires downtime, as it involves stopping the Master Node.

1. [Shutdown the cluster](#shutting-down-the-cluster).

   Info

   You can stop only the Master Node instance to change its instance type, but it is recommended to stop the whole cluster to avoid any issues.

1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) and locate the resource with the name `<STACK_NAME>-master-node` and click on it.

1. Click on *"Edit"* and inside change the *"Machine Type"*. Then select the size you desire and click on *"Save"*

   Change instance type master

1. [Start the cluster](#starting-up-the-cluster).

**Media Nodes**

Info

This will delete the media nodes without the graceful delete option. If you want to stop them gracefully, check the [Shutdown the Cluster](#shutting-down-the-cluster) tab.

1. Go to the *"Instance Group"* tab and select the resource called `<STACK_NAME>-media-node-group` and click on the *"Template"*.

   Select Template MIG

1. To change the size click on *"Create similar"* and create a new one with the desired size.

   Create Similar Template

1. Go back to the *"Instance Group"* and click on *"Edit"*.

   Edit Button Location MIG

1. In *"Instance template & overrides"*, change the template to the one you created previously, and then click *"Save"*.

   Change Template MIG

1. Delete the old instances.

   Delete old sized instances MIG

## Media Nodes Autoscaling Configuration

You can modify the autoscaling configuration of the Media Nodes by adjusting the scaling signals of the Managed Instance Group:

**Media Nodes Autoscaling Configuration**

1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .

1. Go to the *"Instance Groups"* tab, and there click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.

   Edit Button Location MIG

1. On this tab, go to *"Group size & autoscaling"* and change the tab called *"Autoscaling signals"*

1. In this tab you will find the signal currently in use. Here you can add new signals or modify existing ones.

   Signals MIG

Info

OpenVidu Elastic is by default configured with a *"Target tracking scaling"* policy that scales based on the target average CPU usage. However, you can configure different autoscaling policies according to your needs. For more information on the various types of autoscaling policies and how to implement them, refer to the [Google Cloud Platform MIG documentation](https://cloud.google.com/compute/docs/autoscaler?hl=en#autoscaling_policy) .

## Fixed Number of Media Nodes

If you prefer to maintain a fixed number of Media Nodes instead of allowing the Managed Instance Group to perform dynamic scaling:

**Set Fixed Number of Media Nodes**

1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .

1. Go to the *"Instance Groups"* tab, and there click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.

   Edit Button Location MIG

1. On this tab, go to *"Group size & autoscaling"* and change the *"Auto-scaling mode"* to **Off**, then set the *"Number of instances"* on the top to the value of fixed number of Media Nodes you want. In this case it is set to 3. Click *"Save"* and wait for the changes to be applied.

   Fixed Number Media Nodes

Info

This will delete the media nodes if you have set the count lower than the existing number. If you want to stop them gracefully, check the [Shutdown the Cluster](#shutting-down-the-cluster) tab.

### Deactivate Scale In

If you want a fixed number of Media Nodes you probably want to deactivate the Cloud Run Function that controls scale in actions. Follow these steps to do it:

**Deactivate Cloud Run Function**

1. Go to the [Cloud Scheduler Jobs](https://console.cloud.google.com/cloudscheduler) and select the scheduler that controls the trigger of the Cloud Run Function you want to deactivate, then click on *"Pause"* and it will not execute more until you click on *"Resume"* whenever you want to make the cluster scale in again.

   Deactivate Scale In

## Administration and configuration

Regarding the administration of your deployment, you can follow the instructions in section [On Premises Elastic Administration](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/admin/index.md).

Regarding the configuration of your deployment, you can follow the instructions in section [Changing Configuration](https://openvidu.io/3.8/docs/self-hosting/configuration/changing-config/index.md). Additionally, the [How to Guides](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, a Google Cloud Platform deployment provides the capability to manage global configurations via the Google Cloud Platform Console using Secrets Manager created during the deployment:

**Changing configuration through Secrets Manager**

1. Navigate to the [GCP Secrets Manager](https://console.cloud.google.com/security/secret-manager) on Google Cloud Platform.

1. Click on the desired secret you want to change and click on *"New Version"*.

   Google Cloud Platform Secrets Manager New Version Secret

1. Enter the new secret value on *"Secret Value"* field and click on *"Add new version"*.

   Google Cloud Platform Secrets Manager New Version Secret Create

1. Go to the Master Node resource and click on *"Stop"* -> *"Start"* to apply the changes to the OpenVidu Elastic deployment.

Changes will be applied automatically.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
