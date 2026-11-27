# OpenVidu Elastic administration: Google Cloud Platform

Google Cloud Platform

The deployment of OpenVidu Elastic on Google Cloud Platform is automated using Infrastructure Manager in Google Cloud Console, with Media Nodes managed within a [Managed Instance Group](https://docs.cloud.google.com/compute/docs/instance-groups?hl=en) . This group dynamically adjusts the number of instances based on a target average CPU usage.

Internally, the Google Cloud Platform Elastic deployment mirrors the On Premises Elastic deployment, allowing you to follow the same administration and configuration guidelines of the [On Premises Elastic](https://openvidu.io/3.10/docs/self-hosting/elastic/on-premises/admin/index.md) documentation. However, there are specific considerations unique to the Google Cloud Platform environment that are worth keeping in mind:

## Cluster shutdown and startup

The Master Node is a Virtual Machine Instance, while the Media Nodes are part of a Managed Instance Group. The process for starting and stopping these components differs:

> **Deployments with a fixed number of Media Nodes**
>
> With **`fixedNumberOfMediaNodes`** greater than `0` (see [Fixed Number of Media Nodes](#fixed-number-of-media-nodes)) there is no autoscaler to edit, and the scale-in Cloud Run Function brings the group back to the fixed number within 5 minutes. To shut the cluster down, first pause the Cloud Scheduler job `<STACK_NAME>-scale-scheduler` in [Cloud Scheduler](https://console.cloud.google.com/cloudscheduler) {:target="*blank"}, then set the* "Number of instances"\_ of the Managed Instance Group to `0` instead of its minimum and maximum. To start it up, set the number of instances back and resume the job.

**Shutting down the cluster**

To shut down the cluster, you need to stop the Media Nodes and then stop the Master Node.

1. Navigate to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .
1. Then click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.
1. On this tab, go to the **Group Size & autoscaling** tab and change the *"Minimum"* and *"Maximum"* number of instances to 0.
1. Click *"Save"* and wait for it to complete. You can check the progress in the *"VM instances"* tab.
1. After confirming that all Media Node instances are terminated, in *"VM instances"* tab select the instance called `<STACK_NAME>-master-node`. Click on it to go to the Master Node instance. There, click on "Stop" to stop the instance.

**Starting up the cluster**

To start the cluster, first start the Master Node and then the Media Nodes.

1. Navigate to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .
1. In *"VM instances"* tab select the instance called `<STACK_NAME>-master-node`, then click *"Start"* to start the Master Node.
1. Wait until the instance is running.
1. Go to the *"Instance Groups"* tab, and there click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.
1. Go to the **Group Size & autoscaling** tab and change the *"Minimum"* and *"Maximum"* number of instances to your desired values.
1. Click *"Save"* and wait for it to complete. You can check the progress in the *"Instances"* tab.

## Change the instance type

It is possible to change the instance type of both the Master Node and the Media Nodes. However, since the Media Nodes are part of a Managed Instance Group, the process differs. The following section details the procedures:

**Master Nodes**

> **Warning**
>
> This procedure requires downtime, as it involves stopping the Master Node.

1. [Shutdown the cluster](#shutting-down-the-cluster).

   > **Info**
   >
   > You can stop only the Master Node instance to change its instance type, but it is recommended to stop the whole cluster to avoid any issues.

1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) and locate the resource with the name `<STACK_NAME>-master-node` and click on it.

1. Click on *"Edit"* and inside change the *"Machine Type"*. Then select the size you desire and click on *"Save"*

1. [Start the cluster](#starting-up-the-cluster).

**Media Nodes**

> **Info**
>
> This will delete the media nodes without the graceful delete option. If you want to stop them gracefully, check the [Shutdown the Cluster](#shutting-down-the-cluster) tab.

1. Go to the *"Instance Group"* tab and select the resource called `<STACK_NAME>-media-node-group` and click on the *"Template"*.
1. To change the size click on *"Create similar"* and create a new one with the desired size.
1. Go back to the *"Instance Group"* and click on *"Edit"*.
1. In *"Instance template & overrides"*, change the template to the one you created previously, and then click *"Save"*.
1. Delete the old instances.

## Media Nodes Autoscaling Configuration

You can modify the autoscaling configuration of the Media Nodes by adjusting the scaling signals of the Managed Instance Group:

**Media Nodes Autoscaling Configuration**

1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/compute/overview) .
1. Go to the *"Instance Groups"* tab, and there click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on *"Edit"*.
1. On this tab, go to *"Group size & autoscaling"* and change the tab called *"Autoscaling signals"*
1. In this tab you will find the signal currently in use. Here you can add new signals or modify existing ones.

> **Info**
>
> OpenVidu Elastic is by default configured with a *"Target tracking scaling"* policy that scales based on the target average CPU usage. However, you can configure different autoscaling policies according to your needs. For more information on the various types of autoscaling policies and how to implement them, refer to the [Google Cloud Platform MIG documentation](https://docs.cloud.google.com/compute/docs/autoscaler?hl=en#autoscaling_policy) .

## Fixed Number of Media Nodes

The **`fixedNumberOfMediaNodes`** input value selects how the number of Media Nodes in the Managed Instance Group `<STACK_NAME>-media-node-group` is managed:

- **Autoscaling mode** (`0`, the default): an autoscaler adds Media Nodes based on CPU usage, between **minNumberOfMediaNodes** and **maxNumberOfMediaNodes**, and a scale-in Cloud Run Function, run every 5 minutes by a Cloud Scheduler job, drains the Media Nodes above the autoscaler's recommendation.
- **Fixed mode** (a value greater than `0`): no autoscaler is deployed. The same scale-in Cloud Run Function keeps the group at that number of Media Nodes: it drains the extra ones and adds the missing ones. **initialNumberOfMediaNodes**, **minNumberOfMediaNodes**, **maxNumberOfMediaNodes** and **scaleTargetCPU** are ignored.

**Change Fixed Number of Media Nodes**

1. Go to [Infrastructure Manager](https://console.cloud.google.com/infra-manager/deployments) in the GCP Console and select the deployment of OpenVidu Elastic.
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

Regarding the administration of your deployment, you can follow the instructions in section [On Premises Elastic Administration](https://openvidu.io/3.10/docs/self-hosting/elastic/on-premises/admin/index.md).

Regarding the configuration of your deployment, you can follow the instructions in section [Changing Configuration](https://openvidu.io/3.10/docs/self-hosting/configuration/changing-config/index.md). Additionally, the [How to Guides](https://openvidu.io/3.10/docs/self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, a Google Cloud Platform deployment provides the capability to manage global configurations via the Google Cloud Platform Console using Secrets Manager created during the deployment:

**Changing configuration through Secrets Manager**

1. Navigate to the [GCP Secrets Manager](https://console.cloud.google.com/security/secret-manager) on Google Cloud Platform.
1. Click on the desired secret you want to change and click on *"New Version"*.
1. Enter the new secret value on *"Secret Value"* field and click on *"Add new version"*.
1. Go to the Master Node resource and click on *"Stop"* -> *"Start"* to apply the changes to the OpenVidu Elastic deployment.

Changes will be applied automatically.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.10/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
