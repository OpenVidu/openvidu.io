# OpenVidu Elastic administration: AWS

AWS

The deployment of OpenVidu Elastic on AWS is automated using AWS CloudFormation, with Media Nodes managed within an [Auto Scaling Group](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-groups.html) . This group dynamically adjusts the number of instances based on a target average CPU utilization. Internally, the AWS deployment mirrors the on-premises setup, allowing you to follow the same administration and configuration guidelines provided in the [On Premises Elastic](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/admin/index.md) documentation. However, there are specific considerations unique to the AWS environment that are worth keeping in mind.

## Cluster Shutdown and Startup

The Master Node is an EC2 instance, while the Media Nodes are part of an Auto Scaling Group. The process for starting and stopping these components differs. The following sections detail the procedures.

**Shutdown the Cluster**

To shut down the cluster, you need to stop the Media Nodes first and then stop the Master Node. This way, any ongoing session will not be interrupted.

1. Navigate to the [CloudFormation Dashboard](https://console.aws.amazon.com/cloudformation/home) on AWS.

1. Select the CloudFormation Stack that you used to deploy OpenVidu Elastic.

1. In the *"Resources"* tab, locate the resource with the logical ID: **`OpenViduMediaNodeASG`**, and click on it to go to the Auto Scaling Group Dashboard with the Auto Scaling Group of the Media Nodes selected.

   Select Auto Scaling Group

1. Click on *"Actions > Edit"*.

   Edit Auto Scaling Group

1. Set the *"Desired capacity"*, *"Min desired capacity"*, and *"Max desired capacity"* to 0, and click on *"Update"*.

   Set Desired Capacity to 0

1. Wait until the *"Instance Management"* tab shows that there are no instances in the Auto Scaling Group.

   Instance Management

   Warning

   It may happen that some instances are still in the *"Terminating:Wait"* lifecycle state after setting the desired capacity to 0. This is because the Auto Scaling Group waits for the instances to finish processing any ongoing room, ingress, or egress operations before terminating them. This can take a few minutes. If you want to force the termination of the instances, you can manually terminate them from the EC2 Dashboard.

1. After confirming that all Media Node instances are terminated, go back to the CloudFormation Stack and locate the resource with the logical ID: **`OpenViduMasterNode`**. Click on it to go to the EC2 Dashboard with the Master Node instance selected.

   Delete CloudFormation Stack

1. Right-click on the instance and select *"Stop instance"*.

   Stop instance

**Startup the Cluster**

To start the cluster, we recommend starting the Master Node first and then the Media Nodes.

1. Navigate to the [CloudFormation Dashboard](https://console.aws.amazon.com/cloudformation/home) on AWS.

1. Select the CloudFormation Stack that you used to deploy OpenVidu Elastic.

1. Locate the resource with the logical ID: **`OpenViduMasterNode`**. Click on it to go to the EC2 Dashboard with the Master Node instance selected.

   Select CloudFormation Stack

1. Right-click on the instance and select *"Start instance"*.

   Start instance

1. Wait until the instance is running.

1. Go back to the CloudFormation Stack and locate the resource with the logical ID: **`OpenViduMediaNodeASG`**. Click on it to go to the Auto Scaling Group Dashboard with the Auto Scaling Group of the Media Nodes selected.

   Select Auto Scaling Group

1. Click on *"Actions > Edit"*.

   Edit Auto Scaling Group

1. Set the *"Desired capacity"*, *"Min desired capacity"*, and *"Max desired capacity"* to the desired number of Media Nodes, and click on *"Update"*. In this example, we set the desired capacity to 2.

   Set Desired Capacity to 2

1. Wait until the *"Instance Management"* tab shows that there are the desired number of instances in the Auto Scaling Group.

   Instance Management

## Change the instance type

It is possible to change the instance type of both the Master Node and the Media Nodes. However, since the Media Nodes are part of an Auto Scaling Group, the process differs. The following section details the procedures.

**Master Nodes**

Warning

This procedure requires downtime, as it involves stopping the Master Node.

1. [Shutdown the cluster](#shutdown-the-cluster).

   Info

   You can stop only the Master Node instance to change its instance type, but it is recommended to stop the whole cluster to avoid any issues.

1. Go to the CloudFormation Stack and locate the resource with the logical ID: **`OpenViduMasterNode`**. Click on it to go to the EC2 Dashboard with the Master Node instance selected.

   Select CloudFormation Stack

1. Right-click on the instance and select *"Instance Settings > Change Instance Type"*.

   Change instance type

1. Select the new instance type and click on *"Apply"*.

1. [Start the cluster](#startup-the-cluster).

**Media Nodes**

1. Go to the [CloudFormation Dashboard](https://console.aws.amazon.com/cloudformation/home) on AWS.

1. Select the CloudFormation Stack that you used to deploy OpenVidu Elastic.

1. Locate the resource with the logical ID: **`OpenViduMediaNodeLaunchTemplate`**. Click on it to go to the Launch Template Dashboard with the Launch Template of the Media Nodes selected.

   Select Launch Template

1. Click on *"Actions > Modify template (Create new version)"*.

   Edit Launch Template

1. In the *"Instance type"* section, select the new instance type and click on *"Create template version"*.

   Change instance type

1. Go to the CloudFormation Stack and locate the resource with the logical ID: **`OpenViduMediaNodeASG`**. Click on it to go to the Auto Scaling Group Dashboard with the Auto Scaling Group of the Media Nodes selected.

   Select Auto Scaling Group

1. Click on *"Actions > Edit"*.

   Edit Auto Scaling Group

1. In the Launch Template section, select the new version of the launch template we just created at step 5, which is the highest version number.

   Then, click on *"Update"*.

   Info

   By configuring *"Latest"* as the launch template version, you no longer need to update the Auto Scaling Group every time you modify the launch template. The Auto Scaling Group will automatically use the latest version of the launch template.

   Change launch template version

1. Terminate the old instances manually from the EC2 Dashboard if you want to force the termination of the instances. New instances will be launched with the new instance type.

   Info

   If you want to avoid downtime, you can wait until the Auto Scaling Group replaces the old instances with the new ones. But you will need to increase the desired capacity to force the replacement of the instances and then decrease it to the desired number of instances.

## Media Nodes Autoscaling Configuration

To configure the Auto Scaling settings for the Media Nodes, follow the steps outlined below. This configuration allows you to set the parameters that control how the Auto Scaling Group will scale based on the target average CPU utilization.

**Media Nodes Autoscaling Configuration**

1. Navigate to the [CloudFormation Dashboard](https://console.aws.amazon.com/cloudformation/home) on AWS.

1. Select the CloudFormation Stack that you used to deploy OpenVidu Elastic.

1. In the *"Resources"* tab, locate the resource with the logical ID: **`OpenViduMediaNodeASG`** and click on it to go to the Auto Scaling Group Dashboard.

   Select Auto Scaling Group

1. Click on *"Actions > Edit"*.

   Edit Auto Scaling Group

1. To configure scaling policies, navigate to the *"Automatic scaling"* tab within the Auto Scaling Group Dashboard, select the unique *"Target tracking scaling"* autoscaling policy, and click on *"Actions > Edit"*.

   Scaling Policies

1. It will open a panel where you can configure multiple parameters. In this example, we set the target average CPU utilization to 30%. Then, click on *"Update"*.

   Edit Scaling Policies

   Info

   OpenVidu Elastic is by default configured with a *"Target tracking scaling"* policy that scales based on the target average CPU utilization, however, you can configure different autoscaling policies according to your needs. For more information on the various types of autoscaling policies and how to implement them, refer to the [AWS Auto Scaling documentation](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scale-based-on-demand.html) .

## Fixed Number of Media Nodes

If you need to maintain a fixed number of Media Nodes instead of allowing the Auto Scaling Group to dynamically adjust based on CPU utilization, you can configure the desired capacity settings accordingly. Follow the steps below to set a fixed number of Media Nodes:

**Set Fixed Number of Media Nodes**

1. Navigate to the [CloudFormation Dashboard](https://console.aws.amazon.com/cloudformation/home) on AWS.

1. Select the CloudFormation Stack that you used to deploy OpenVidu Elastic.

1. In the *"Resources"* tab, locate the resource with the logical ID: **`OpenViduMediaNodeASG`** and click on it to go to the Auto Scaling Group Dashboard.

   Select Auto Scaling Group

1. Click on *"Actions > Edit"*.

   Edit Auto Scaling Group

1. Set the *"Desired capacity"*, *"Min desired capacity"*, and *"Max desired capacity"* to the fixed number of Media Nodes you require, and click on *"Update"*. In this example, we set the desired capacity to 2.

   Set Fixed Desired Capacity

1. Wait until the *"Instance Management"* tab shows that the Auto Scaling Group has the fixed number of instances running.

   Instance Management

## Administration and configuration

For administration, you can follow the instructions from the [On Premises Elastic Administration](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/admin/index.md) section.

Regarding the configuration, in AWS it is managed similarly to an on-premises deployment. For detailed instructions, please refer to the [Changing Configuration](https://openvidu.io/3.8/docs/self-hosting/configuration/changing-config/index.md) section. Additionally, the [How to Guides](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, an AWS deployment provides the capability to manage global configurations via the AWS Console using AWS Secrets created during the deployment. To manage configurations this way, follow these steps:

**Changing Configuration through AWS Secrets**

1. Navigate to the [CloudFormation Dashboard](https://console.aws.amazon.com/cloudformation/home) on AWS.

1. Select the CloudFormation Stack that you used to deploy OpenVidu Elastic.

1. In the *"Outputs"* tab, click the Link at *"ServicesAndCredentials"*. This will open the AWS Secrets Manager which contains all the configurations of the OpenVidu Elastic Deployment.

   Select Secrets Manager

1. Click on the *"Retrieve secret value"* button to get the JSON with all the information.

   Retrieve Secret Value

1. Modify the parameter you want to change and click on *"Save"*.

1. Go to the EC2 Console and click on *"Reboot instance"* in the Master Node instance to apply the changes.

   Reboot Instance

Changes will be applied automatically in all the nodes of your OpenVidu Elastic deployment.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
