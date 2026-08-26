# OpenVidu High Availability administration: Google Cloud Platform

Google Cloud Platform

The deployment of OpenVidu High Availability on Google Cloud Platform is automated using Infrastructure Manager in Google Cloud Console, with 4 Virtual Machine Instances as Master Nodes and any number of Media Nodes managed within a [Managed Instance Group](https://cloud.google.com/compute/docs/instance-groups?hl=en) . The Managed Instance Group of Media Nodes is configured to scale based on the target average CPU usage.

Internally, the Google Cloud Platform High Availability deployment mirrors the On Premises High Availability deployment, allowing you to follow the same administration and configuration guidelines provided in the [On Premises High Availability](https://openvidu.io/3.8/docs/self-hosting/ha/on-premises/admin/index.md) documentation. However, there are specific considerations unique to the Google Cloud Platform environment that are worth keeping in mind:

## Cluster shutdown and startup

You can start and stop the OpenVidu High Availability cluster at any time. The following sections detail the procedures:

**Shutting down the cluster**

To shut down the cluster, you need to stop the Media Nodes and then stop the Master Nodes.

1. Navigate to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .

1. Then click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.

   Edit Button Location MIG

1. On this tab, go to the **Group Size & autoscaling** tab and change the *"Minimum"* and *"Maximum"* number of instances to 0.

   Edit MIG

1. Click *"Save"* and wait for the operation to complete. You can check the progress in the *"VM instances"* tab.

   Save Edits MIG

1. After confirming that all Media Node instances are terminated, in *"VM instances"* tab select the instance called `<STACK_NAME>-master-node-1`. Click on it to go to the Master Node 1 instance. There, click on "Stop" to stop the instance.

   Stop Master Node MIG

1. Repeat step 5 for all the Master Nodes.

**Starting up the cluster**

To start the cluster, start the Master Nodes first and then the Media Nodes.

1. Navigate to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .

1. In *"VM instances"* tab select the instance called `<STACK_NAME>-master-node-1`, here click on start to start the Master Node 1.

   Start Master Node

1. Wait until the instance is running.

1. Repeat step 2 and 3 for all the Master Nodes until they are all up and running.

1. Go to the *"Instance Groups"* tab, and there click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.

   Edit Button Location MIG

1. Go to **Group Size & autoscaling** tab and change the *"Minimum"* and *"Maximum"* number of instances to your desired values.

   Edit MIG

1. Click *"Save"* and wait for it to complete. You can check the progress in the *"Instances"* tab.

   Save Edits MIG

## Change the instance type

It is possible to change the instance type of both the Master Node and the Media Nodes. The following section details the procedures.

**Master Nodes**

Warning

This procedure requires downtime, as it involves stopping the Master Node.

1. [Shutdown the cluster](#shutting-down-the-cluster).

1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) and locate the resource with the name `<STACK_NAME>-master-node-1` and click on it.

1. Click on *"Edit"* and inside change the *"Machine Type"*. Then select the size you desire and click on *"Save"*

   Change instance type master

1. Repeat steps 2 and 3 for all the Master Nodes just in case you want to resize all of them, if not just do it for the ones you want.

1. [Start the cluster](#starting-up-the-cluster).

**Media Nodes**

Info

This will delete the media nodes without the graceful delete option, if you want to stop them gracefully check the [Shutdown the Cluster](#shutting-down-the-cluster) tab

1. Go to the *"Instance Group"* tab and select the resource called `<STACK_NAME>-media-node-group` and click on the *"Template"*.

   Select Template MIG

1. To change the size click on *"Create similar"* and create a new one with the desired size.

   Create Similar Template

1. Go back to the *"Instance Group"* and click on *"Edit"*

   Edit Button Location MIG

1. In *"Instance template & overrides"* change the template for the one you've created previously and then *"Save"*.

   Change Template MIG

1. Delete the old sized instances.

   Delete old sized instances MIG

## Media Nodes Autoscaling Configuration

You can modify the autoscaling configuration of the Media Nodes by adjusting the scaling signals of the Managed Instance Group:

**Media Nodes Autoscaling Configuration**

1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .

1. Go to the *"Instance Groups"* tab, and there click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.

   Edit Button Location MIG

1. On this tab, go to *"Group size & autoscaling"* and change the tab called *"Autoscaling signals"*

1. In the *"Default"* box you will find a section called *"Rules"*. Here you can add new rules or modify existing ones.

   Warning

   Currently there is only one rule to scale out. We are actively working on providing a graceful scale-in process for Media Nodes to avoid active Rooms disruption.

   Signals MIG

Info

OpenVidu High Availability is by default configured with a *"Target tracking scaling"* policy that scales based on the target average CPU usage. However, you can configure different autoscaling policies according to your needs. For more information on the various types of autoscaling policies and how to implement them, refer to the [Google Cloud Platform MIG documentation](https://cloud.google.com/compute/docs/autoscaler?hl=en#autoscaling_policy) .

## Fixed Number of Media Nodes

If you prefer to maintain a fixed number of Media Nodes instead of allowing the Managed Instance Group to perform dynamic scaling:

**Set Fixed Number of Media Nodes**

1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .

1. Go to the *"Instance Groups"* tab, and there click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.

   Edit Button Location MIG

1. On this tab, go to *"Group size & autoscaling"* and change the *"Auto-scaling mode"* to **Off**, then set the *"Number of instances"* on the top to the fixed number of Media Nodes you want. In this case, it is set to 3. Click *"Save"* and wait for it to be applied.

   Fixed Number Media Nodes

Info

This will delete the media nodes if you have set them to less than the number of media nodes that existed, if you want to stop them gracefully check the [Shutdown the Cluster](#shutting-down-the-cluster) tab.

### Deactivate Scale In

If you want a fixed number of Media Nodes you probably want to deactivate the Cloud Run Function that controls scale in actions. Follow these steps to do it:

**Deactivate Cloud Run Function**

1. Go to the [Cloud Scheduler Jobs](https://console.cloud.google.com/cloudscheduler) and select the scheduler that controls the trigger of the Cloud Run Function you want to deactivate, then click on *"Pause"* and it will not execute more until you click on *"Resume"* whenever you want to make the cluster scale in again.

   Deactivate Scale In

## Administration and configuration

Regarding the administration of your deployment, you can follow the instructions in the [On Premises High Availability Administration](https://openvidu.io/3.8/docs/self-hosting/ha/on-premises/admin/index.md) section.

Regarding the configuration of your deployment, you can follow the instructions in section [Changing Configuration](https://openvidu.io/3.8/docs/self-hosting/configuration/changing-config/index.md). Additionally, the [How to Guides](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, a Google Cloud Platform deployment provides the capability to manage global configurations via the Google Cloud Platform Console using Secrets Manager created during the deployment:

**Changing configuration through Secrets Manager**

1. Navigate to the [GCP Secrets Manager](https://console.cloud.google.com/security/secret-manager) on Google Cloud Platform.

1. Click on the desired secret you want to change and click on *"New Version"*.

   Google Cloud Platform Secrets Manager New Version Secret

1. Enter the new secret value on *"Secret Value"* field and click on *"Add new version"*.

   Google Cloud Platform Secrets Manager New Version Secret Create

1. Go to the Master Node resource whose secrets you want to change and click on *"Stop"* -> *"Start"* to apply the changes to the OpenVidu High Availability deployment.

Changes will be applied automatically in all the nodes of your OpenVidu High Availability deployment.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
