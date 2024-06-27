# OpenVidu Single Node Installation: AWS

--8<-- "docs/docs/self-hosting/single-node/shared/v2compat-warning.md"

This section contains the instructions to deploy a production-ready OpenVidu Single Node deployment in AWS. Deployed services are the same as the [On Premises Single Node Installation](../on-premises/install.md) but automate the process with AWS CloudFormation.

First of all, import the template in the AWS CloudFormation console. You can click the following button...

<div class="center-align" markdown>
[Deploy OpenVidu Single Node in :fontawesome-brands-aws:{style="font-size:32px; margin-left: 7px"}](https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=OpenViduSingleNode&templateURL=https://s3.eu-west-1.amazonaws.com/get.openvidu.io/community/singlenode/latest/aws/cf-openvidu-singlenode.yaml){.md-button .deploy-button target="_blank"}
</div>

...or access your [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation/home?#/stacks/new){:target=_blank} and manually set this S3 URL in the `Specify template` section:

```
https://s3.eu-west-1.amazonaws.com/get.openvidu.io/community/singlenode/latest/aws/cf-openvidu-singlenode.yaml
```

=== "Architecture overview"

    This is how the architecture of the deployment looks like:

    <figure markdown>
    ![OpenVidu Single Node AWS Architecture](../../../../assets/images/self-hosting/single-node/aws/single-node-aws-architecture.svg){ .svg-img .dark-img }
    <figcaption>OpenVidu Single Node AWS Architecture</figcaption>
    </figure>

## CloudFormation Parameters

Depending on your needs, you need to fill the following CloudFormation parameters:

--8<-- "docs/docs/self-hosting/shared/aws-ssl-domain.md"

### EC2 Instance Configuration

You need to specify some properties for the EC2 instance that will be created.

=== "EC2 Instance configuration"

    The parameters in this section may look like this:

    ![EC2 Instance configuration](../../../../assets/images/self-hosting/single-node/aws/ec2-instance-config.png)

    Simply select the type of instance you want to deploy at **InstanceType**, the SSH key you want to use to access the machine at **KeyName**, and the Amazon Image ID (AMI) to use at **AmiId**.

    By default, the parameter **AmiId** is configured to use the latest LTS Ubuntu AMI, so ideally you don’t need to modify this.

--8<-- "docs/docs/self-hosting/shared/aws-turn-domain.md"

## Deploying the Stack

When you are ready with your CloudFormation parameters, just click on _"Next"_, specify in _"Stack failure options"_ the option _"Preserve successfully provisioned resources"_ to be able to troubleshoot the deployment in case of error, click on _"Next"_ again, and finally _"Submit"_.

When everything is ready, you will see the following links in the _"Outputs"_ section of CloudFormation with all deployed services.

=== "CloudFormation Outputs"

    ![CloudFormation Outputs](../../../../assets/images/self-hosting/single-node/aws/outputs.png)

## Deployment Credentials

To point your applications to your OpenVidu deployment, check the file of the EC2 instance `/opt/openvidu/.env`. All access credentials of all services are defined in this file.

Just point your app to the **OpenViduServerURL** parameter of the CloudFormation outputs and get the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` from the `.env` file to connect your app to the OpenVidu Single Node deployment.

## Troubleshooting Initial CloudFormation Stack Creation

--8<-- "docs/docs/self-hosting/shared/aws-troubleshooting.md"

4. If everything seems fine, check the [status](../on-premises/admin.md#checking-the-status-of-services) and the [logs](../on-premises/admin.md#checking-logs) of the installed OpenVidu services.

## Configuration and administration

When your CloudFormation stack reaches the **`CREATE_COMPLETE`** status, your OpenVidu Single Node deployment is ready to use. You can check the [Configuration and Administration](../aws/admin.md) section to learn how to manage your deployment.
