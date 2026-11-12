---
title: "Install OpenVidu Elastic on AWS"
description: "Create the EC2 machines and deploy OpenVidu Elastic on AWS with one command of the OpenVidu CLI, then operate the stack from its directory."
---

# OpenVidu Elastic installation: AWS

<div class="provider-chip" markdown>

:material-aws:{ .provider-chip-icon } AWS

</div>

--8<-- "self-hosting/common/elastic-license-intro.md"

One command creates the machines and OpenVidu comes up on them. `ov` renders the CloudFormation template embedded in its own binary for the Elastic topology and applies it with **your own `aws` CLI**. The machines then deploy OpenVidu themselves with the same `ov` build. When OpenVidu answers, `ov` registers the stack in your directory, and you operate it from there.

The deployed services are the same as in the [On Premises Elastic installation](../on-premises/install.md); on AWS the machines and their resources are created for you.

!!! info
    Port `9000` is MinIO's port. This deployment stores recordings and application data in Amazon S3 instead of MinIO, so MinIO is not deployed and port `9000` does not need to be open.

=== "Architecture overview"

    This is how the architecture of the deployment looks:

    ![OpenVidu Elastic AWS Architecture](../../../../assets/images/platform/self-hosting/elastic/aws/elastic-architecture.svg){ .round-corners .dark-img loading=lazy }

    - The Master Node acts as a Load Balancer, managing the traffic and distributing it among the Media Nodes and deployed services in the Master Node.
    - The Master Node has its own Caddy server acting as a Layer 4 (for TURN with TLS and RTMPS) and Layer 7 (for OpenVidu Dashboard, OpenVidu Meet, etc., APIs) reverse proxy.
    - WebRTC traffic (SRTP/SCTP/STUN/TURN) is routed directly to the Media Nodes.
    - An autoscaling group of Media Nodes is created to scale the number of Media Nodes based on the system load.

## Requirements

--8<-- "self-hosting/aws/ov-requirements.md"

Elastic also needs a **VPC** of yours with public subnets, one for the master node and one or more for the media nodes. Without `--param OpenViduVPC=…`, the deploy uses the region's default VPC and its default subnets.

## Deploy

The stack lives in its own empty directory. Elastic runs in a VPC of yours: one subnet for the master and one or more for the media nodes. This uses the region's default VPC, the master in its first subnet and the media nodes spread over all of them:

```bash
mkdir openvidu && cd openvidu
VPC=$(aws ec2 describe-vpcs --filters Name=is-default,Values=true \
  --query 'Vpcs[0].VpcId' --output text)
SUBNETS=$(aws ec2 describe-subnets --filters Name=vpc-id,Values=$VPC Name=default-for-az,Values=true \
  --query 'Subnets[].SubnetId' --output text | tr '\t' ,)
ov stack deploy openvidu --cloud aws --aws-region us-east-1 \
  --edition pro --openvidu-pro-license <your-license> --deployment-type elastic \
  --param OpenViduVPC=$VPC \
  --param OpenViduMasterNodeSubnet=${SUBNETS%%,*} \
  --param OpenViduMediaNodeSubnets=$SUBNETS \
  --certificate-type letsencrypt --mode auto
```

One master node and an auto scaling group of media nodes, in the VPC and subnets you name. The media nodes scale between `MinNumberOfMediaNodes` and `MaxNumberOfMediaNodes` (`--param`), or, at the first deploy, `--set infrastructure.mediaNodes.fixedCount=N` runs exactly N of them. To change the count later, see [Scale the media nodes](./admin.md#scale-the-media-nodes).

This is how the deploy of a stack named `dpaws2` (in `eu-south-2`) ends: `ov` waits until the stack publishes its kubeconfig and the cluster answers, then registers it:

```text
…
   · OpenVidu is up: the stack published its kubeconfig and the cluster API answers at 51.95.197.8:6443
…
✔ OpenVidu Pro (elastic) is up on AWS
  URL:          https://openvidu-239b62-51-95-197-8.sslip.io/
  credentials:  aws secretsmanager get-secret-value --secret-id openvidu-elastic-eu-south-2-openvidu-dpaws2 --query SecretString --output text --region eu-south-2
  kubeconfig:   .openvidu/aws/kubeconfig.yaml
```

## What the deploy runs

--8<-- "self-hosting/aws/ov-deploy-plan.md"

## What the deploy creates

--8<-- "self-hosting/aws/ov-resources.md"

## Access OpenVidu

--8<-- "self-hosting/aws/ov-access.md"

## Review the commands first: assisted mode

--8<-- "self-hosting/aws/ov-assisted.md"

## Troubleshooting

--8<-- "self-hosting/aws/troubleshooting.md"

## Next steps

- [Administer the stack](./admin.md): scale the media nodes, change its configuration and destroy it.
- [Build your app](../../../build-your-app/index.md) against it, or follow a [tutorial](../../../tutorials/application-server/index.md): it connects with `LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` (`ov stack config get livekit-api-key` and `livekit-api-secret` print them).
