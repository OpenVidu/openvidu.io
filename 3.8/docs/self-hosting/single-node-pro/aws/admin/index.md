# OpenVidu Single Node PRO administration: AWS

AWS

AWS deployment of OpenVidu Single Node PRO is internally identical to the on-premises deployment, so you can follow the same instructions from the [On Premises Single Node PRO](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/admin/index.md) for administration and configuration. The only difference is that the deployment is automated with AWS CloudFormation.

However, there are certain things worth mentioning:

## Start and stop OpenVidu through AWS Console

You can start and stop all services as explained in the [On Premises Single Node PRO](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/admin/#starting-stopping-and-restarting-openvidu) section. But you can also start and stop the EC2 instance directly from the AWS Console. This will stop all services running in the instance and reduce AWS costs.

**Stop OpenVidu Single Node**

1. Go to the [EC2 Dashboard](https://console.aws.amazon.com/ec2/v2/home#Instances:sort=instanceId) of AWS.
1. Right-click on the instance you want to start and select *"Stop instance"*.

Stop instance

**Start OpenVidu Single Node**

1. Go to the [EC2 Dashboard](https://console.aws.amazon.com/ec2/v2/home#Instances:sort=instanceId) of AWS.
1. Right-click on the instance you want to start and select *"Start instance"*.

Start instance

## Change the instance type

You can change the instance type of the OpenVidu Single Node instance to adapt it to your needs. To do this, follow these steps:

1. [Stop the instance](#start-and-stop-openvidu-through-aws-console).

1. Right-click on the instance and select *"Instance Settings > Change Instance Type"*.

   **Change instance type**

   Change instance type

1. Select the new instance type and click on *"Apply"*.

## Administration and configuration

For administration, you can follow the instructions from the [On Premises Single Node PRO Administration](https://openvidu.io/3.8/docs/self-hosting/single-node-pro/on-premises/admin/index.md) section.

Regarding the configuration, in AWS it is managed similarly to an on-premises deployment. For detailed instructions, please refer to the [Changing Configuration](https://openvidu.io/3.8/docs/self-hosting/configuration/changing-config/index.md) section. Additionally, the [How to Guides](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, an AWS deployment provides the capability to manage global configurations via the AWS Console using AWS Secrets created during the deployment. To manage configurations this way, follow these steps:

**Changing Configuration through AWS Secrets**

1. Navigate to the [CloudFormation Dashboard](https://console.aws.amazon.com/cloudformation/home) on AWS.
1. Select the CloudFormation Stack that you used to deploy OpenVidu Single Node.
1. In the *"Outputs"* tab, click the Link at *"ServicesAndCredentials"*. This will open the AWS Secrets Manager which contains all the configurations of the OpenVidu Single Node deployment. Select Secrets Manager
1. Click on the *"Retrieve secret value"* button to get the JSON with all the information. Retrieve Secret Value
1. Modify the parameter you want to change and click on *"Save"*.
1. Go to the EC2 Console and click on *"Reboot instance"* to apply the changes to the Master Node. Reboot Instance

Changes will be applied automatically.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
