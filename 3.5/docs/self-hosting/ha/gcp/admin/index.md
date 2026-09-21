# OpenVidu High Availability administration: Google Cloud Platform

The deployment of OpenVidu High Availability on Google Cloud Platform is automated using Infra Structure Manager in Google Cloud Console, with 4 Virtual Machine Instances as Master Nodes and any number of Media Nodes managed within a [Managed Instance Group](https://cloud.google.com/compute/docs/instance-groups?hl=en) . The Managed Instance Group of Media Nodes is configured to scale based on the target average CPU usage.

Internally, the Google Cloud Platform High Availability deployment mirrors the On Premises High Availability deployment, allowing you to follow the same administration and configuration guidelines provided in the [On Premises High Availability](https://openvidu.io/3.5/docs/self-hosting/ha/on-premises/admin/index.md) documentation. However, there are specific considerations unique to the Google Cloud Platform environment that are worth taking into account:

## Cluster shutdown and startup

You can start and stop the OpenVidu High Availability cluster at any time. The following sections detail the procedures:

**Shutting down the cluster**

To shut down the cluster, you need to stop the Media Nodes and then stop the Master Nodes.

1. Navigate to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .
1. Then click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.
1. On this tab, go at the **Group Size & autoscaling** tab and change the *"Minimun"* and *"Maximum"* number of instances to 0.
1. Click on save and wait, it needs the lambda function to run until is completed, you can check how is going in the *"VM instances"* tab.
1. After confirming that all Media Node instances are terminated, in *"VM instances"* tab select the instance called `<STACK_NAME>-master-node-1`. Click on it to go to the Master Node 1 instance. There, click on "Stop" to stop the instance.
1. Repeat step 5 for all the Master Nodes.

**Starting up the cluster**

To start the cluster, start the Master Nodes first and then the Media Nodes.

1. Navigate to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .
1. In *"VM instances"* tab select the instance called `<STACK_NAME>-master-node-1`, here click on start to start the Master Node 1.
1. Wait until the instance is running.
1. Repeat step 2 and 3 for all the Master Nodes until they are all up and running.
1. Go to the *"Instance Groups"* tab, and there click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.
1. Go to **Group Size & autoscaling** tab and change the *"Minimun"* and *"Maximum"* number of instances to your desired ones.
1. Click on save and wait until is completed. You can check the progress in the *"Instances"* tab.

## Change the instance type

It is possible to change the instance type of both the Master Node and the Media Nodes. The following section details the procedures.

**Master Nodes**

> **Warning**
>
> This procedure requires downtime, as it involves stopping the Master Node.

1. [Shutdown the cluster](#shutting-down-the-cluster).
1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) and locate the resource with the name `<STACK_NAME>-master-node-1` and click on it.
1. Click on *"Edit"* and inside change the *"Machine Type"*. Then select the size you desire and click on *"Save"*
1. Repeat steps 2 and 3 for all the Master Nodes just in case you want to resize all of them, if not just do it for the ones you want.
1. [Start the cluster](#starting-up-the-cluster).

**Media Nodes**

> **Info**
>
> This will delete the media nodes without the graceful delete option, if you want to stop them gracefully check the [Shutdown the Cluster](#shutting-down-the-cluster) tab

1. Go to the *"Instance Group"* tab and select the resource called `<STACK_NAME>-media-node-group` and click on the *"Template"*.
1. To change the size click on *"Create similar"* and create a new one with the desired size.
1. Go back to the *"Instace Group"* and click on *"Edit"*
1. In *"Instace template & overrides"* change the template for the one you've created previously and then *"Save"*.
1. Delete the old sized instances.

## Media Nodes Autoscaling Configuration

You can modify the autoscaling configuration of the Media Nodes by adjusting the scaling signals of the Managed Instance Group:

**Media Nodes Autoscaling Configuration**

1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .

1. Go to the *"Instance Groups"* tab, and there click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.

1. On this tab, go to *"Group size & autoscaling"* and change the tab called *"Autoscaling signals"*

1. In the *"Default"* box you will find a section called *"Rules"*. Here you can add new rules or modify existing ones.

   > **Warning**
   >
   > Currently there is only one rule to scale out. We are actively working in providing a graceful scale in process for Media Nodes to avoid active Rooms disruption.

> **Info**
>
> OpenVidu High Availability is by default configured with a *"Target tracking scaling"* policy that scales based on the target average CPU usage. However, you can configure different autoscaling policies according to your needs. For more information on the various types of autoscaling policies and how to implement them, refer to the [Google Cloud Platform MIG documentation](https://cloud.google.com/compute/docs/autoscaler?hl=en#autoscaling_policy) .

## Fixed Number of Media Nodes

If you prefer to maintain a fixed number of Media Nodes instead of allowing the Managed Instance Group to perform dynamic scaling:

**Set Fixed Number of Media Nodes**

1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .
1. Go to the *"Instance Groups"* tab, and there click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.
1. On this tab, go to *"Group size & autoscaling"* and change the *"Auto-scaling mode"* to **Off**, then set the *"Number of instances"* on the top to the value of fixed number of Media Nodes you want. In this case is set to 3. Click on save next and wait to be applied

> **Info**
>
> This will delete the media nodes if you have set them to less than the number of media nodes that existed, if you want to stop them gracefully check the [Shutdown the Cluster](#shutting-down-the-cluster) tab.

### Deactivate Scale In

If you want a fixed number of Media Nodes you probably want to deactivate the Cloud Run Function that controls scale in actions. Follow these steps to do it:

**Deactivate Cloud Run Function**

1. Go to the [Cloud Scheduler Jobs](https://console.cloud.google.com/cloudscheduler) and select the scheduler that controls the trigger of the Cloud Run Function you want to deactivate, then click on *"Pause"* and it will not execute more until you click on *"Resume"* whenever you want to make the cluster scale in again.

## Administration and configuration

Regarding the administration of your deployment, you can follow the instructions in section [On Premises High Availability Administration](https://openvidu.io/3.5/docs/self-hosting/ha/on-premises/admin/index.md) section.

Regarding the configuration of your deployment, you can follow the instructions in section [Changing Configuration](https://openvidu.io/3.5/docs/self-hosting/configuration/changing-config/index.md). Additionally, the [How to Guides](https://openvidu.io/3.5/docs/self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, a Google Cloud Platform deployment provides the capability to manage global configurations via the Google Cloud Platform Console using Secrets Manager created during the deployment:

**Changing configuration through Secrets Manager**

1. Navigate to the [GCP Secrets Manager](https://console.cloud.google.com/security/secret-manager) on Google Cloud Platform.
1. Click on the desired secret you want to change and click on *"New Version"*.
1. Enter the new secret value on *"Secret Value"* filed and click on *"Add new version"*.
1. Go to the Master Node resource you've want to change the secrets on and click on *"Stop"* -> *"Start"* to apply the changes to the OpenVidu High Availability deployment.

Changes will be applied automatically.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.5/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
