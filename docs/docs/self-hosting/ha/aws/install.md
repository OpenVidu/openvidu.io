---
title: OpenVidu High Availability installation on AWS
description: Learn how to deploy OpenVidu High Availability on AWS using CloudFormation
---

# OpenVidu High Availability installation: AWS

!!! info
    
    OpenVidu High Availability is part of **OpenVidu <span class="openvidu-tag openvidu-pro-tag" style="font-size: 12px; vertical-align: top;">PRO</span>**. Before deploying, you need to [create an OpenVidu account](/account/){:target="_blank"} to get your license key.
    There's a 15-day free trial waiting for you!

This section contains the instructions to deploy a production-ready OpenVidu High Availability deployment in AWS. Deployed services are the same as the [On Premises High Availability installation](../on-premises/install-nlb.md) but automate the process with AWS CloudFormation.

First of all, import the template in the AWS CloudFormation console. You can click the following button...

[:fontawesome-brands-aws:{style="font-size:36px; margin-right: 14px"} Deploy to AWS](https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=OpenViduHA&templateURL=https://s3.eu-west-1.amazonaws.com/get.openvidu.io/pro/ha/latest/aws/cf-openvidu-ha.yaml){.md-button .deploy-button .deploy-to-aws-btn target="_blank"}

...or access your [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation/home?#/stacks/new){:target=_blank} and manually set this S3 URL in the `Specify template` section:

```
https://s3.eu-west-1.amazonaws.com/get.openvidu.io/pro/ha/latest/aws/cf-openvidu-ha.yaml
```

!!! info
    
    If you want to deploy a specific version of OpenVidu HA, replace `latest` with the version you want to deploy. For example, to deploy version `3.2.0`, use the following URL:

    ```
    https://s3.eu-west-1.amazonaws.com/get.openvidu.io/pro/ha/3.2.0/aws/cf-openvidu-ha.yaml
    ```

This is how the architecture of the deployment looks like.

=== "Architecture overview"

    <figure markdown>
    ![OpenVidu High Availability AWS Architecture](../../../../assets/images/self-hosting/ha/aws/ha-aws-architecture.svg){ .svg-img .dark-img }
    <figcaption>OpenVidu High Availability AWS Architecture</figcaption>
    </figure>

    - The Load Balancer distributes HTTPS traffic to the Master Nodes.
    - If RTMP media is ingested, the Load Balancer also routes this traffic to the Media Nodes.
    - WebRTC traffic (SRTP/SCTP/STUN/TURN) is routed directly to the Media Nodes.
    - 4 fixed EC2 Instances are created for the Master Nodes. It must always be 4 Master Nodes to ensure high availability.
    - An autoscaling group of Media Nodes is created to scale the number of Media Nodes based on the system load.

=== "Architecture overview with TURN over TLS"

    <figure markdown>
    ![OpenVidu High Availability AWS Architecture with TURN over TLS](../../../../assets/images/self-hosting/ha/aws/ha-aws-architecture-turn.svg){ .svg-img .dark-img }
    <figcaption>OpenVidu High Availability AWS Architecture with TURN over TLS</figcaption>
    </figure>

    - The Load Balancer distributes HTTPS traffic to the Master Nodes.
    - If RTMP media is ingested, the Load Balancer also routes this traffic to the Media Nodes.
    - WebRTC traffic (SRTP/SCTP/STUN/TURN) is routed directly to the Media Nodes.
    - An additional Load Balancer is created to route TURN over TLS traffic to the TURN server running on the Media Nodes. It is used to allow users behind restrictive firewalls to connect to the Media Nodes.
    - 4 fixed EC2 Instances are created for the Master Nodes. It must always be 4 Master Nodes to ensure high availability.
    - An autoscaling group of Media Nodes is created to scale the number of Media Nodes based on the system load.

## CloudFormation Parameters

Depending on your needs, you need to fill the following CloudFormation parameters:

### Domain and Load Balancer configuration

In this section, you need to specify the domain name and the SSL certificate to use from AWS Certificate Manager.

=== "Domain and Load Balancer configuration"

    The parameters in this section might look like this:

    ![Domain and Load Balancer configuration](../../../../assets/images/self-hosting/ha/aws/domain-and-lb-config.png)

    Set the **DomainName** parameter to the domain name you intend to use for your OpenVidu deployment. Ensure this domain is not currently pointing to any other service; you can temporarily point it elsewhere.

    For the **OpenViduCertificateARN** parameter, specify the ARN of the SSL certificate you wish to use. This certificate should be created in the AWS Certificate Manager and configured for the domain specified in **DomainName**.

### OpenVidu HA Configuration

In this section, you need to specify some properties needed for the OpenVidu HA deployment.

=== "OpenVidu HA Configuration"

    Parameters of this section look like this:

    ![OpenVidu HA Configuration](../../../../assets/images/self-hosting/ha/aws/openvidu-ha-config.png)

    Make sure to provide the **OpenViduLicense** parameter with the license key. If you don't have one, you can request one [here](/account/){:target="_blank"}.

    For the **RTCEngine** parameter, you can choose between **Pion** (the default engine used by LiveKit) and **Mediasoup** (with a boost in performance). Learn more about the differences [here](../../../production-ready/performance/).

### EC2 Instance Configuration

You need to specify some properties for the EC2 instances that will be created.

=== "EC2 Instance configuration"

    Parameters in this section look like this:

    ![EC2 Instance configuration](../../../../assets/images/self-hosting/ha/aws/ec2-instance-config.png)

    Simply select the type of instance you want to deploy at **MasterNodeInstanceType** and **MediaNodeInstanceType**, the SSH key you want to use to access the machine at **KeyName**, and the Amazon Image ID (AMI) to use at **AmiId**.

    By default, the parameter **AmiId** is configured to use the latest Amazon Linux AMI, so ideally you don’t need to modify this.

### Media Nodes Autoscaling Group Configuration

The number of Media Nodes can scale up or down based on the system load. You can configure the minimum and maximum number of Media Nodes and a target CPU utilization to trigger the scaling up or down.

=== "Media Nodes Autoscaling Group Configuration"

    Parameters in this section look like this:

    ![Media Nodes Autoscaling Group Configuration](../../../../assets/images/self-hosting/ha/aws/media-nodes-asg-config.png)

    The **InitialNumberOfMediaNodes** parameter specifies the initial number of Media Nodes to deploy. The **MinNumberOfMediaNodes** and **MaxNumberOfMediaNodes** parameters specify the minimum and maximum number of Media Nodes that you want to be deployed.

    The **ScaleTargetCPU** parameter specifies the target CPU utilization to trigger the scaling up or down. The goal is to keep the CPU utilization of the Media Nodes close to this value. The autoscaling policy is based on [Target Tracking Scaling Policy](https://docs.aws.amazon.com/autoscaling/application/userguide/target-tracking-scaling-policy-overview.html){:target="_blank"}.

### S3 bucket for application data, cluster data and recordings

You can specify two S3 buckets to store the application data, cluster data, and recordings.

=== "S3 bucket for application data and recordings"

    Parameters in this section look like this:

    ![S3 bucket for application data and recordings](../../../../assets/images/self-hosting/ha/aws/aws-s3-bucket.png)

    If these parameters are not specified, new S3 buckets will be created by the CloudFormation stack.

### VPC Configuration

In this section, you need to specify the VPC and Subnet configuration for the deployment.

=== "VPC Configuration"

    Parameters in this section look like this:

    ![VPC Configuration](../../../../assets/images/self-hosting/ha/aws/vpc-config.png)

    The **OpenViduVPC** parameter specifies the VPC where the deployment will be created.

    The **OpenViduMasterNodeSubnets** specifies the subnets where the Master Nodes will be deployed. You can specify a maximum of 4 subnets.

    The **OpenViduMediaNodeSubnets** specifies the subnets where the Media Nodes will be deployed. There is no limit on the number of subnets you can specify.

    !!! warning

        - It is recommended to deploy in a region with at least 4 availability zones and deploy the Master Nodes in 4 subnets, one in each availability zone. This is to ensure high availability.
        - You must use public subnets for the Master Nodes and Media Nodes and have enabled the auto-assign public IP option.

### (Optional) TURN server configuration with TLS

This section is optional. It is useful when your users are behind a restrictive firewall that blocks UDP traffic.

=== "TURN server configuration with TLS"

    Parameters in this section look like this:

    ![TURN server configuration with TLS](../../../../assets/images/self-hosting/ha/aws/turn-config.png)

    Set the **TurnDomainName** parameter to the domain name you intend to use for your TURN server. Ensure this domain is not currently pointing to any other service; you can temporarily point it elsewhere.

    For the **TurnCertificateARN** parameter, specify the ARN of the SSL certificate you wish to use. This certificate should be created in the AWS Certificate Manager and configured for the domain specified in **TurnDomainName**.

## Volumes Configuration

In this section, you need to specify the configuration for the EBS volumes that will be created for the Master Nodes. Master Nodes will host all the recordings and metrics data replicated across all of them. The disk size of the EBS volumes is the same for all Master Nodes.

=== "Volumes Configuration"

    Parameters in this section look like this:

    ![Volumes Configuration](../../../../assets/images/self-hosting/ha/aws/volumes-config.png)

    The **MasterNodesDiskSize** parameter specifies the size of the EBS volumes in GB.

## Deploying the stack

When you are ready with your CloudFormation parameters, just click on _"Next"_, specify in _"Stack failure options"_ the option _"Preserve successfully provisioned resources"_ to be able to troubleshoot the deployment in case of error, click on _"Next"_ again, and finally _"Submit"_.

When everything is ready, you will see the following links in the _"Outputs"_ section of CloudFormation:

=== "CloudFormation Outputs"

    ![CloudFormation Outputs](../../../../assets/images/self-hosting/ha/aws/outputs.png)

## Configure your application to use the deployment

The Output Key **ServicesAndCredentials** of the [previous section](#deploying-the-stack) points to an AWS Secret Manager secret that contains all URLs and credentials to access the services deployed. You can access the secret by clicking on the link in the **Output Value** column.

Then, click on **Retrieve secret value** to get the JSON with all the information.

<div class="grid-container">

<div class="grid-50"><p><a class="glightbox" href="../../../../../assets/images/self-hosting/ha/aws/1-secrets-retrieve.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="../../../../../assets/images/self-hosting/ha/aws/1-secrets-retrieve.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="../../../../../assets/images/self-hosting/ha/aws/2-secrets.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="../../../../../assets/images/self-hosting/ha/aws/2-secrets.png" loading="lazy"/></a></p></div>

</div>

To point your applications to your OpenVidu deployment, check the values of the JSON secret. All access credentials of all services are defined in this object.

Your authentication credentials and URL to point your applications would be:

- Applications developed with LiveKit SDK:
    - **URL**: The value in the AWS Secret of `DOMAIN_NAME` as a URL. It could be `wss://openvidu.example.io/` or `https://openvidu.example.io/` depending on the SDK you are using.
    - **API Key**: The value in the AWS Secret of `LIVEKIT_API_KEY`
    - **API Secret**: The value in the AWS Secret of `LIVEKIT_API_SECRET`

- Applications developed with OpenVidu v2:
    - **URL**: The value in the AWS Secret of `DOMAIN_NAME` as a URL. For example, `https://openvidu.example.io/`
    - **Username**: `OPENVIDUAPP`
    - **Password**: The value in the AWS Secret of `LIVEKIT_API_SECRET`

## Troubleshooting Initial CloudFormation Stack Creation

--8<-- "shared/self-hosting/aws-troubleshooting.md"

4. If everything seems fine, check the [status](../on-premises/admin.md#checking-the-status-of-services) and the [logs](../on-premises/admin.md#checking-logs) of the installed OpenVidu services in all the Master Nodes and Media Nodes.

## Configuration and administration

When your CloudFormation stack reaches the **`CREATE_COMPLETE`** status, your OpenVidu High Availability deployment is ready to use. You can check the [Administration](./admin.md) section to learn how to manage your deployment.
