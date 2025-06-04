---
title: OpenVidu Single Node PRO administration on AWS
description: Learn how to perform administrative tasks on an AWS OpenVidu Single Node PRO deployment
---

# <span class="openvidu-tag openvidu-pro-tag" style="font-size: .5em">PRO</span> OpenVidu Single Node administration: AWS

AWS deployment of OpenVidu Single Node is internally identical to the on-premises deployment, so you can follow the same instructions from the [On Premises Single Node](../on-premises/admin-pro.md) for administration and configuration. The only difference is that the deployment is automated with AWS CloudFormation.

However, there are certain things worth mentioning:

## Start and stop OpenVidu through AWS Console

You can start and stop all services as explained in the [On Premises Single Node](../on-premises/admin-pro.md#starting-stopping-and-restarting-openvidu) section. But you can also start and stop the EC2 instance directly from the AWS Console. This will stop all services running in the instance and reduce AWS costs.

--8<-- "shared/self-hosting/single-node/aws-start-stop.md"

--8<-- "shared/self-hosting/single-node/aws-change-instance-type.md"

## Administration and configuration

For administration, you can follow the instructions from the [On Premises Single Node Administration](../on-premises/admin-pro.md) section.

Regarding the configuration, in AWS it is managed similarly to an on-premises deployment. For detailed instructions, please refer to the [Changing Configuration](../../configuration/changing-config.md) section. Additionally, the [How to Guides](../../how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

--8<-- "shared/self-hosting/single-node/aws-config.md"
