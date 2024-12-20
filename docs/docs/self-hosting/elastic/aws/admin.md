# OpenVidu Elastic: AWS Administration

The deployment of OpenVidu Elastic on AWS is automated using AWS CloudFormation, with Media Nodes managed within an [Auto Scaling Group](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-groups.html){:target=_blank}. This group dynamically adjusts the number of instances based on a target average CPU utilization. Internally, the AWS deployment mirrors the on-premises setup, allowing you to follow the same administration and configuration guidelines provided in the [On Premises Elastic](../on-premises/admin.md) documentation. However, there are specific considerations unique to the AWS environment that are worth taking into account.

## Cluster Shutdown and Startup

The Master Node is an EC2 instance, while the Media Nodes are part of an Auto Scaling Group. The process for starting and stopping these components differs. The following sections detail the procedures.

=== "Shutdown the Cluster"

    To shut down the cluster, you need to stop the Media Nodes first and then stop the Master Node. This way, any ongoing session will not be interrupted.

    1. Navigate to the [CloudFormation Dashboard](https://console.aws.amazon.com/cloudformation/home){:target=_blank} on AWS.
    2. Select the CloudFormation Stack that you used to deploy OpenVidu Elastic.
    3. In the _"Resources"_ tab, locate the resource with the logical ID: **`OpenViduMediaNodeASG`**, and click on it to go to the Auto Scaling Group Dashboard with the Auto Scaling Group of the Media Nodes selected.
        <figure markdown>
        ![Select Auto Scaling Group](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-select-media-asg.png){ .svg-img .dark-img }
        </figure>
    4. Click on _"Actions > Edit"_.
        <figure markdown>
        ![Edit Auto Scaling Group](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-edit-media-asg.png){ .svg-img .dark-img }
        </figure>
    5. Set the _"Desired capacity"_, _"Min desired capacity"_, and _"Max desired capacity"_ to 0, and click on _"Update"_.
        <figure markdown>
        ![Set Desired Capacity to 0](../../../../assets/images/self-hosting/shared/aws-admin-set-desired-capacity-stop.png){ .svg-img .dark-img }
        </figure>
    6. Wait until the _"Instance Management"_ tab shows that there are no instances in the Auto Scaling Group.
        <figure markdown>
        ![Instance Management](../../../../assets/images/self-hosting/shared/aws-admin-instance-management-stop.png){ .svg-img .dark-img }
        </figure>

        !!! warning
            
            It may happen that some instances are still in the _"Terminating:Wait"_ lifecycle state after setting the desired capacity to 0. This is because the Auto Scaling Group waits for the instances to finish processing any ongoing room, ingress, or egress operations before terminating them. This can take a few minutes. If you want to force the termination of the instances, you can manually terminate them from the EC2 Dashboard.

    7. After confirming that all Media Node instances are terminated, go back to the CloudFormation Stack and locate the resource with the logical ID: **`OpenViduMasterNode`**. Click on it to go to the EC2 Dashboard with the Master Node instance selected.
        <figure markdown>
        ![Delete CloudFormation Stack](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-select-master.png){ .svg-img .dark-img }
        </figure>
    8. Right-click on the instance and select _"Stop instance"_.
        <figure markdown>
        ![Stop instance](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-stop-master.png){ .svg-img .dark-img }
        </figure>

=== "Startup the Cluster"

    To start the cluster, we recommend starting the Master Node first and then the Media Nodes.

    1. Navigate to the [CloudFormation Dashboard](https://console.aws.amazon.com/cloudformation/home){:target=_blank} on AWS.
    2. Select the CloudFormation Stack that you used to deploy OpenVidu Elastic.
    3. Locate the resource with the logical ID: **`OpenViduMasterNode`**. Click on it to go to the EC2 Dashboard with the Master Node instance selected.
        <figure markdown>
        ![Select CloudFormation Stack](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-select-master.png){ .svg-img .dark-img }
        </figure>
    4. Right-click on the instance and select _"Start instance"_.
        <figure markdown>
        ![Start instance](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-start-master.png){ .svg-img .dark-img }
        </figure>
    5. Wait until the instance is running.
    6. Go back to the CloudFormation Stack and locate the resource with the logical ID: **`OpenViduMediaNodeASG`**. Click on it to go to the Auto Scaling Group Dashboard with the Auto Scaling Group of the Media Nodes selected.
        <figure markdown>
        ![Select Auto Scaling Group](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-select-media-asg.png){ .svg-img .dark-img }
        </figure>
    7. Click on _"Actions > Edit"_.
        <figure markdown>
        ![Edit Auto Scaling Group](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-edit-media-asg.png){ .svg-img .dark-img }
        </figure>
    8. Set the _"Desired capacity"_, _"Min desired capacity"_, and _"Max desired capacity"_ to the desired number of Media Nodes, and click on _"Update"_. In this example, we set the desired capacity to 2.
        <figure markdown>
        ![Set Desired Capacity to 2](../../../../assets/images/self-hosting/shared/aws-admin-set-desired-capacity-start.png){ .svg-img .dark-img }
        </figure>
    9. Wait until the _"Instance Management"_ tab shows that there are the desired number of instances in the Auto Scaling Group.
        <figure markdown>
        ![Instance Management](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-instance-management-start.png){ .svg-img .dark-img }
        </figure>


## Change the instance type

It is possible to change the instance type of both the Master Node and the Media Nodes. However, since the Media Nodes are part of an Auto Scaling Group, the process differs. The following section details the procedures.

=== "Master Nodes"

    !!! warning
        
        This procedure requires downtime, as it involves stopping the Master Node.

    1. [Shutdown the cluster](#shutdown-the-cluster).

        !!! info
            
            You can stop only the Master Node instance to change its instance type, but it is recommended to stop the whole cluster to avoid any issues.
    2. Go to the CloudFormation Stack and locate the resource with the logical ID: **`OpenViduMasterNode`**. Click on it to go to the EC2 Dashboard with the Master Node instance selected.
        <figure markdown>
        ![Select CloudFormation Stack](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-select-master.png){ .svg-img .dark-img }
        </figure>
    3. Right-click on the instance and select _"Instance Settings > Change Instance Type"_.
        <figure markdown>
        ![Change instance type](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-master-instance-type.png){ .svg-img .dark-img }
        </figure>
    4. Select the new instance type and click on _"Apply"_.
    5. [Start the cluster](#startup-the-cluster).

=== "Media Nodes"

    1. Go to the [CloudFormation Dashboard](https://console.aws.amazon.com/cloudformation/home){:target=_blank} on AWS.
    2. Select the CloudFormation Stack that you used to deploy OpenVidu Elastic.
    3. Locate the resource with the logical ID: **`OpenViduMediaNodeLaunchTemplate`**. Click on it to go to the Launch Template Dashboard with the Launch Template of the Media Nodes selected.
        <figure markdown>
        ![Select Launch Template](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-select-launch-template.png){ .svg-img .dark-img }
        </figure>
    4. Click on _"Actions > Modify template (Create new version)"_.
        <figure markdown>
        ![Edit Launch Template](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-action-modify-template.png){ .svg-img .dark-img }
        </figure>
    5. In the _"Instance type"_ section, select the new instance type and click on _"Create template version"_.
        <figure markdown>
        ![Change instance type](../../../../assets/images/self-hosting/shared/aws-admin-template-instance-type.png){ .svg-img .dark-img }
        </figure>
    6. Go to the CloudFormation Stack and locate the resource with the logical ID: **`OpenViduMediaNodeASG`**. Click on it to go to the Auto Scaling Group Dashboard with the Auto Scaling Group of the Media Nodes selected.
        <figure markdown>
        ![Select Auto Scaling Group](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-select-media-asg.png){ .svg-img .dark-img }
        </figure>
    7. Click on _"Actions > Edit"_.
        <figure markdown>
        ![Edit Auto Scaling Group](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-edit-media-asg.png){ .svg-img .dark-img }
        </figure>
    8. In the Launch Template section, select the new version of the launch template we just created at step 5, which is the highest version number.

        Then, click on _"Update"_.

        !!! info
            
            By configuring _"Latest"_ as the launch template version, you no longer need to update the Auto Scaling Group every time you modify the launch template. The Auto Scaling Group will automatically use the latest version of the launch template.

        ![Change launch template version](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-asg-update-launch-template.png){ .svg-img .dark-img }

    9. Terminate the old instances manually from the EC2 Dashboard if you want to force the termination of the instances. New instances will be launched with the new instance type.

        !!! info
            
            If you want to avoid downtime, you can wait until the Auto Scaling Group replaces the old instances with the new ones. But you will need to increase the desired capacity to force the replacement of the instances and then decrease it to the desired number of instances.

## Media Nodes Autoscaling Configuration

To configure the Auto Scaling settings for the Media Nodes, follow the steps outlined below. This configuration allows you to set the parameters that control how the Auto Scaling Group will scale based on the target average CPU utilization.

=== "Media Nodes Autoscaling Configuration"

    1. Navigate to the [CloudFormation Dashboard](https://console.aws.amazon.com/cloudformation/home){:target=_blank} on AWS.
    2. Select the CloudFormation Stack that you used to deploy OpenVidu Elastic.
    3. In the _"Resources"_ tab, locate the resource with the logical ID: **`OpenViduMediaNodeASG`** and click on it to go to the Auto Scaling Group Dashboard.
        <figure markdown>
        ![Select Auto Scaling Group](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-select-media-asg.png){ .svg-img .dark-img }
        </figure>
    4. Click on _"Actions > Edit"_.
        <figure markdown>
        ![Edit Auto Scaling Group](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-edit-media-asg.png){ .svg-img .dark-img }
        </figure>
    5. To configure scaling policies, navigate to the _"Automatic scaling"_ tab within the Auto Scaling Group Dashboard, select the unique _"Target tracking scaling"_ autoscaling policy, and click on _"Actions > Edit"_.
        <figure markdown>
        ![Scaling Policies](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-automatic-scaling.png){ .svg-img .dark-img }
        </figure>
    6. It will open a panel where you can configure multiple parameters. In this example, we set the target average CPU utilization to 30%. Then, click on _"Update"_.
        <figure markdown>
        ![Edit Scaling Policies](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-edit-scaling-policies.png){ .svg-img .dark-img }
        </figure>

        !!! info
            
            OpenVidu Elastic is by default configured with a _"Target tracking scaling"_ policy that scales based on the target average CPU utilization, however, you can configure different autoscaling policies according to your needs. For more information on the various types of autoscaling policies and how to implement them, refer to the [AWS Auto Scaling documentation](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scale-based-on-demand.html){:target=_blank}.

## Fixed Number of Media Nodes

If you need to maintain a fixed number of Media Nodes instead of allowing the Auto Scaling Group to dynamically adjust based on CPU utilization, you can configure the desired capacity settings accordingly. Follow the steps below to set a fixed number of Media Nodes:

=== "Set Fixed Number of Media Nodes"

    1. Navigate to the [CloudFormation Dashboard](https://console.aws.amazon.com/cloudformation/home){:target=_blank} on AWS.
    2. Select the CloudFormation Stack that you used to deploy OpenVidu Elastic.
    3. In the _"Resources"_ tab, locate the resource with the logical ID: **`OpenViduMediaNodeASG`** and click on it to go to the Auto Scaling Group Dashboard.
        <figure markdown>
        ![Select Auto Scaling Group](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-select-media-asg.png){ .svg-img .dark-img }
        </figure>
    4. Click on _"Actions > Edit"_.
        <figure markdown>
        ![Edit Auto Scaling Group](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-edit-media-asg.png){ .svg-img .dark-img }
        </figure>
    5. Set the _"Desired capacity"_, _"Min desired capacity"_, and _"Max desired capacity"_ to the fixed number of Media Nodes you require, and click on _"Update"_. In this example, we set the desired capacity to 2.
        <figure markdown>
        ![Set Fixed Desired Capacity](../../../../assets/images/self-hosting/shared/aws-admin-set-desired-capacity-start.png){ .svg-img .dark-img }
        </figure>
    6. Wait until the _"Instance Management"_ tab shows that the Auto Scaling Group has the fixed number of instances running.
        <figure markdown>
        ![Instance Management](../../../../assets/images/self-hosting/elastic/aws/aws-elastic-admin-instance-management-start.png){ .svg-img .dark-img }
        </figure>


## Administration and Configuration

For administration, you can follow the instructions from the [On Premises Elastic Administration](../on-premises/admin.md) section.

Regarding the configuration, in AWS it is managed similarly to an on-premises deployment. For detailed instructions, please refer to the [Changing Configuration](../../../self-hosting/configuration/changing-config.md) section. Additionally, the [How to Guides](../../../self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, an AWS deployment provides the capability to manage global configurations via the AWS Console using AWS Secrets created during the deployment. To manage configurations this way, follow these steps:

=== "Changing Configuration through AWS Secrets"

    1. Navigate to the [CloudFormation Dashboard](https://console.aws.amazon.com/cloudformation/home){:target=_blank} on AWS.
    2. Select the CloudFormation Stack that you used to deploy OpenVidu Elastic.
    3. In the _"Outputs"_ tab, click the Link at _"ServicesAndCredentials"_. This will open the AWS Secrets Manager which contains all the configurations of the OpenVidu Elastic Deployment.
        <figure markdown>
        ![Select Secrets Manager](../../../../assets/images/self-hosting/elastic/aws/outputs.png){ .svg-img .dark-img }
        </figure>
    4. Click on the _"Retrieve secret value"_ button to get the JSON with all the information.
        <figure markdown>
        ![Retrieve Secret Value](../../../../assets/images/self-hosting/elastic/aws/1-secrets-retrieve.png){ .svg-img .dark-img }
        </figure>
    5. Modify the parameter you want to change and click on _"Save"_. The changes will be applied to the OpenVidu Elastic deployment.
    6. Go to the EC2 Console and click on _"Reboot instance"_ in the Master Node instance to apply the changes.
        <figure markdown>
        ![Reboot Instance](../../../../assets/images/self-hosting/elastic/aws/reboot-instance.png){ .svg-img .dark-img }
        </figure>

    The changes will be applied automatically in all the Nodes of the OpenVidu Elastic deployment.
