# OpenVidu High Availability administration: Google Cloud Platform

Google Cloud Platform

The deployment of OpenVidu High Availability on Google Cloud Platform is automated using Infrastructure Manager in Google Cloud Console, with 4 Virtual Machine Instances as Master Nodes and any number of Media Nodes managed within a [Managed Instance Group](https://docs.cloud.google.com/compute/docs/instance-groups?hl=en) . The Managed Instance Group of Media Nodes is configured to scale based on the target average CPU usage.

Internally, the Google Cloud Platform High Availability deployment mirrors the On Premises High Availability deployment, allowing you to follow the same administration and configuration guidelines provided in the [On Premises High Availability](https://openvidu.io/3.10/docs/self-hosting/ha/on-premises/admin/index.md) documentation. However, there are specific considerations unique to the Google Cloud Platform environment that are worth keeping in mind:

## Cluster shutdown and startup

You can start and stop the OpenVidu High Availability cluster at any time. The following sections detail the procedures:

> **Deployments with a fixed number of Media Nodes**
>
> With **`fixedNumberOfMediaNodes`** greater than `0` (see [Fixed Number of Media Nodes](#fixed-number-of-media-nodes)) there is no autoscaler to edit, and the scale-in Cloud Run Function brings the group back to the fixed number within 5 minutes. To shut the cluster down, first pause the Cloud Scheduler job `<STACK_NAME>-scale-scheduler` in [Cloud Scheduler](https://console.cloud.google.com/cloudscheduler) {:target="*blank"}, then set the* "Number of instances"\_ of the Managed Instance Group to `0` instead of its minimum and maximum. To start it up, set the number of instances back and resume the job.

**Shutting down the cluster**

To shut down the cluster, you need to stop the Media Nodes and then stop the Master Nodes.

1. Navigate to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .
1. Then click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.
1. On this tab, go to the **Group Size & autoscaling** tab and change the *"Minimum"* and *"Maximum"* number of instances to 0.
1. Click *"Save"* and wait for the operation to complete. You can check the progress in the *"VM instances"* tab.
1. After confirming that all Media Node instances are terminated, in *"VM instances"* tab select the instance called `<STACK_NAME>-master-node-1`. Click on it to go to the Master Node 1 instance. There, click on "Stop" to stop the instance.
1. Repeat step 5 for all the Master Nodes.

**Starting up the cluster**

To start the cluster, start the Master Nodes first and then the Media Nodes.

1. Navigate to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .
1. In *"VM instances"* tab select the instance called `<STACK_NAME>-master-node-1`, here click on start to start the Master Node 1.
1. Wait until the instance is running.
1. Repeat step 2 and 3 for all the Master Nodes until they are all up and running.
1. Go to the *"Instance Groups"* tab, and there click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.
1. Go to **Group Size & autoscaling** tab and change the *"Minimum"* and *"Maximum"* number of instances to your desired values.
1. Click *"Save"* and wait for it to complete. You can check the progress in the *"Instances"* tab.

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
1. Go back to the *"Instance Group"* and click on *"Edit"*
1. In *"Instance template & overrides"* change the template for the one you've created previously and then *"Save"*.
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
   > Currently there is only one rule to scale out. We are actively working on providing a graceful scale-in process for Media Nodes to avoid active Rooms disruption.

> **Info**
>
> OpenVidu High Availability is by default configured with a *"Target tracking scaling"* policy that scales based on the target average CPU usage. However, you can configure different autoscaling policies according to your needs. For more information on the various types of autoscaling policies and how to implement them, refer to the [Google Cloud Platform MIG documentation](https://docs.cloud.google.com/compute/docs/autoscaler?hl=en#autoscaling_policy) .

## Fixed Number of Media Nodes

The **`fixedNumberOfMediaNodes`** input value selects how the number of Media Nodes in the Managed Instance Group `<STACK_NAME>-media-node-group` is managed:

- **Autoscaling mode** (`0`, the default): an autoscaler adds Media Nodes based on CPU usage, between **minNumberOfMediaNodes** and **maxNumberOfMediaNodes**, and a scale-in Cloud Run Function, run every 5 minutes by a Cloud Scheduler job, drains the Media Nodes above the autoscaler's recommendation.
- **Fixed mode** (a value greater than `0`): no autoscaler is deployed. The same scale-in Cloud Run Function keeps the group at that number of Media Nodes: it drains the extra ones and adds the missing ones. **initialNumberOfMediaNodes**, **minNumberOfMediaNodes**, **maxNumberOfMediaNodes** and **scaleTargetCPU** are ignored.

**Change Fixed Number of Media Nodes**

1. Go to [Infrastructure Manager](https://console.cloud.google.com/infra-manager/deployments) in the GCP Console and select the deployment of OpenVidu High Availability.
1. Edit the deployment, set the input value **`fixedNumberOfMediaNodes`** to the number of Media Nodes you want, keep the rest of the input values as they are, and update the deployment. If you deployed with the Terraform CLI instead, set the variable and run `terraform apply`.
1. Wait for the update to complete. The scale-in Cloud Run Function brings the group to the new number on its next run, within 5 minutes. You can follow the Media Nodes in the Managed Instance Group called `<STACK_NAME>-media-node-group`.

Raising the number adds Media Nodes. Lowering it drains the extra Media Nodes gracefully, with the same mechanism as an automatic scale-in: they leave the Managed Instance Group but keep running in *"VM instances"* while they drain, stop accepting new Rooms, and delete themselves when their ongoing Rooms, recordings and ingests end. The drain starts within about 5 minutes of the update: the function runs every 5 minutes, and each Media Node notices within a minute that it has left the group.

### Activate or Deactivate Autoscaling

**Activate Autoscaling**

1. Follow the steps of the *"Change Fixed Number of Media Nodes"* tab above, setting **`fixedNumberOfMediaNodes`** to `0`. Change **minNumberOfMediaNodes**, **maxNumberOfMediaNodes** and **scaleTargetCPU** too if you do not want their current values.
1. When the update completes, the autoscaler is deployed again and scales on CPU usage, starting from the Media Nodes that are running. If there are fewer than **minNumberOfMediaNodes**, the autoscaler adds Media Nodes up to it. If there are more than **maxNumberOfMediaNodes**, the scale-in Cloud Run Function drains the extra ones gracefully, down to the autoscaler's recommendation.

**Deactivate Autoscaling**

1. Follow the steps of the *"Change Fixed Number of Media Nodes"* tab above, setting **`fixedNumberOfMediaNodes`** to the number of Media Nodes you want.
1. When the update completes, the autoscaler is removed, and the scale-in Cloud Run Function brings the group to that number on its next run: if more Media Nodes are running, the extra ones are drained gracefully; if fewer are running, Media Nodes are added.

> **What an update changes**
>
> - An update never resizes the Managed Instance Group by itself: Terraform sets its size only when the deployment is created, to **initialNumberOfMediaNodes** (or to **fixedNumberOfMediaNodes** in fixed mode). After that, only the autoscaler and the scale-in Cloud Run Function change it, as described above.
> - In fixed mode, if the size of the group is changed by other means, for example by hand in the GCP Console, the scale-in Cloud Run Function brings it back to **fixedNumberOfMediaNodes** on its next run.

## Administration and configuration

Regarding the administration of your deployment, you can follow the instructions in the [On Premises High Availability Administration](https://openvidu.io/3.10/docs/self-hosting/ha/on-premises/admin/index.md) section.

Regarding the configuration of your deployment, you can follow the instructions in section [Changing Configuration](https://openvidu.io/3.10/docs/self-hosting/configuration/changing-config/index.md). Additionally, the [How to Guides](https://openvidu.io/3.10/docs/self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, a Google Cloud Platform deployment provides the capability to manage global configurations via the Google Cloud Platform Console using Secrets Manager created during the deployment:

**Changing configuration through Secrets Manager**

1. Navigate to the [GCP Secrets Manager](https://console.cloud.google.com/security/secret-manager) on Google Cloud Platform.
1. Click on the desired secret you want to change and click on *"New Version"*.
1. Enter the new secret value on *"Secret Value"* field and click on *"Add new version"*.
1. Go to the Master Node resource whose secrets you want to change and click on *"Stop"* -> *"Start"* to apply the changes to the OpenVidu High Availability deployment.

Changes will be applied automatically in all the nodes of your OpenVidu High Availability deployment.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.10/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
