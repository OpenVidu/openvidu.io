---
title: "Deploy OpenVidu on AWS with the OpenVidu CLI"
description: "Create the EC2 machines and deploy OpenVidu COMMUNITY or PRO on AWS with one command of the OpenVidu CLI, then operate and destroy the stack."
page_features: [lazyvideo]
---

# Deploy OpenVidu on AWS with the OpenVidu CLI

<div class="provider-chip" markdown>

:material-aws:{ .provider-chip-icon } AWS

</div>

One command creates the machines and OpenVidu comes up on them. `ov` renders the CloudFormation template embedded in its own binary for the edition and topology you ask for, applies it with **your own `aws` CLI**, and the machines deploy OpenVidu themselves with the same `ov` build. When OpenVidu answers, `ov` registers the stack in your directory, and you operate it from there.

<!-- VIDEO: deploy-aws.mp4 (docs-video) -->

## Requirements

- The [OpenVidu CLI](../install.md).
- An AWS account and the [`aws` CLI :fontawesome-solid-external-link:{.external-link-icon}](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html){:target="_blank"}, **authenticated**: `aws sts get-caller-identity` must answer. `ov` runs your own client, so your profile, region and audit trail are the ones that apply. `--aws-profile` picks a named profile.
- Permissions to create CloudFormation stacks with IAM resources, EC2 instances, Elastic IPs, security groups, S3 buckets and Secrets Manager secrets.
- A region: `--aws-region`, else `$AWS_REGION`, else the one `aws configure` has.
- For OpenVidu PRO, your **license** (`--openvidu-pro-license`). The deploy checks it is there before it touches your account.

You need no key pair and, except for High Availability, no domain: the deploy generates an SSH key pair for the stack, and without `--domain-name` the machine derives a `sslip.io` name from its public IP, so Let's Encrypt has a name to certify. Use your own domain for anything real. High Availability needs your own domain and an ACM certificate for it (see its tab below).

## Deploy

An empty directory is the stack. Choose the edition and topology:

=== "Single Node **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud aws --aws-region us-east-1 \
      --certificate-type letsencrypt --mode auto
    ```

    One EC2 instance (`c6a.xlarge` by default, `--aws-instance-type` to change it) running OpenVidu on Docker Compose.

=== "Single Node **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud aws --aws-region us-east-1 \
      --edition pro --openvidu-pro-license <your-license> \
      --certificate-type letsencrypt --mode auto
    ```

    One EC2 instance running OpenVidu PRO on Kubernetes. `--aws-kube-api-cidr` limits who can reach the cluster API on port 6443, which gives full control of the stack: do not leave it open to `0.0.0.0/0` on a production stack.

    This is how the deploy of a stack named `dpaws1` ends: `ov` waits until the stack publishes its kubeconfig and the cluster answers, then registers it:

    ```text
    …
       · OpenVidu is up: the stack published its kubeconfig and the cluster API answers at 89.60.28.34:6443
    …
    ✔ OpenVidu Pro (single node) is up on AWS
      URL:          https://openvidu-geepav-89-60-28-34.sslip.io/
      credentials:  aws secretsmanager get-secret-value --secret-id openvidu-eu-south-2-openvidu-dpaws1 --query SecretString --output text --region eu-south-2
      kubeconfig:   .openvidu/aws/kubeconfig.yaml
    ```

=== "Elastic **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud aws --aws-region us-east-1 \
      --edition pro --openvidu-pro-license <your-license> --deployment-type elastic \
      --param OpenViduVPC=vpc-0123456789abcdef0 \
      --param OpenViduMasterNodeSubnet=subnet-aaaa1111 \
      --param OpenViduMediaNodeSubnets=subnet-aaaa1111,subnet-bbbb2222 \
      --certificate-type letsencrypt --mode auto
    ```

    One master node and an auto scaling group of media nodes, in the VPC and subnets you name. The media nodes scale between `MinNumberOfMediaNodes` and `MaxNumberOfMediaNodes` (`--param`), or `--set infrastructure.mediaNodes.fixedCount=N` runs exactly N of them.

    <!-- PENDING-RUN (docs-ov, dw): aws pro elastic with today's ov -->

=== "High Availability **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    High Availability needs three things of your own: a **domain**, an **ACM certificate** for it in the same region, and a **VPC with three or more subnets in different availability zones** (the four masters spread across them so the cluster survives losing a zone). A region's default VPC has one subnet per zone, so this picks them:

    ```bash
    mkdir openvidu && cd openvidu
    VPC=$(aws ec2 describe-vpcs --filters Name=is-default,Values=true \
      --query 'Vpcs[0].VpcId' --output text)
    SUBNETS=$(aws ec2 describe-subnets --filters Name=vpc-id,Values=$VPC Name=default-for-az,Values=true \
      --query 'Subnets[].SubnetId' --output text | tr '\t' ,)
    ov stack deploy openvidu --cloud aws --aws-region us-east-1 \
      --edition pro --openvidu-pro-license <your-license> --deployment-type ha \
      --domain-name openvidu.example.com \
      --param OpenViduCertificateARN=arn:aws:acm:us-east-1:123456789012:certificate/<id> \
      --param OpenViduVPC=$VPC \
      --param OpenViduMasterNodeSubnets=$SUBNETS \
      --param OpenViduMediaNodeSubnets=$SUBNETS \
      --mode auto
    ```

    Four master nodes behind a Network Load Balancer, plus an auto scaling group of media nodes. TLS ends at the load balancer with the ACM certificate ([Create AWS certificate for HA](../../how-to-guides/create-configure-AWS-certificate.md)), so `--certificate-type` does not apply. With only two subnets the CloudFormation stack fails to create (`Fn::Select` cannot find index 2).

    When the deploy ends, **point the domain at the load balancer**: a CNAME (or a Route 53 ALIAS record) to the stack's `NLBDNS` output. Nothing serves the domain until you do. This prints it (the CloudFormation stack is `openvidu-<name>`):

    ```bash
    aws cloudformation describe-stacks --stack-name openvidu-openvidu --region us-east-1 \
      --query "Stacks[0].Outputs[?OutputKey=='NLBDNS'].OutputValue" --output text
    ```

    Because the load balancer terminates TLS, `ov stack status --wait` counts the nodes and services and leaves the URL to it. This is the wait of a stack named `demo-ha`:

    ```console
    $ ov stack status --wait
    note: the stack runs behind a proxy that terminates TLS, so its URL is checked at that proxy: the wait counts nodes and services only
    waiting for https://openvidu.example.com to be ready (Ctrl-C to stop)…
      ⏳ master nodes 4/4, media nodes 1/1, services 41/49 (0s)
    …
      ⏳ master nodes 4/4, media nodes 1/1, services 48/49 (44s)
    ✔ demo-ha is ready (every node and service; its URL answers at the proxy in front of it)
    ```

Before it touches your account, the deploy prints exactly what it will run and asks for confirmation (`-y` answers it in advance; the list is still printed). This is the output of a Single Node COMMUNITY deploy of a stack named `ce10`:

```text
This is what will be done in your AWS account (region us-east-1):

  # SSH access: the key pair for this stack (.openvidu/aws/openvidu-ce10-key.pem), its public half imported here.
  aws ec2 import-key-pair --key-name openvidu-ce10-key --public-key-material fileb://.openvidu/aws/openvidu-ce10-key.pub --region us-east-1

  # The template, rendered from the one embedded in this CLI for the single node topology,
  # and its parameters, written out for you to read (the parameters file is 0600: it
  # can carry secrets, such as Meet's seed credentials or a private key):
  #   .openvidu/aws/cf-openvidu-singlenode.yaml
  #   .openvidu/aws/cfn-parameters.json
  # CloudFormation takes a template this size from S3: stage it in a bucket of your
  # account, created once and reused by every stack.
  BUCKET=openvidu-cfn-templates-123456789012-us-east-1
  aws s3api head-bucket --bucket $BUCKET --region us-east-1 2>/dev/null || aws s3api create-bucket --bucket $BUCKET --region us-east-1

  # Create the machine. DeployedBy=instance: it installs OpenVidu with the OpenVidu
  # CLI and CloudFormation finishes once it serves. `deploy` returns then (about 10 minutes).
  aws cloudformation deploy --stack-name openvidu-ce10 --template-file .openvidu/aws/cf-openvidu-singlenode.yaml --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM --no-fail-on-empty-changeset --s3-bucket openvidu-cfn-templates-123456789012-us-east-1 --s3-prefix openvidu-ce10 --parameter-overrides file://.openvidu/aws/cfn-parameters.json --region us-east-1

  # Read back where the stack is and what it published: its address, URL and
  # credentials (OPENVIDU_URL is "none" until OpenVidu serves). The secret's name is
  # the stack's SharedInfoSecret output.
  aws cloudformation describe-stacks --stack-name openvidu-ce10 --query 'Stacks[0].Outputs' --output json --region us-east-1
  SECRET="$(aws cloudformation describe-stacks --stack-name openvidu-ce10 --query 'Stacks[0].Outputs[?OutputKey=='\''SharedInfoSecret'\''].OutputValue' --output text --region us-east-1)"
  aws secretsmanager get-secret-value --secret-id $SECRET --query SecretString --output text --region us-east-1
```

Then it runs them, waits for OpenVidu and registers the stack. The whole deploy took 6 minutes:

```text
▶ Create the machines on AWS…
   · SSH key pair for this stack: .openvidu/aws/openvidu-ce10-key.pem
   · import its public half into us-east-1 as the key pair openvidu-ce10-key
   · create the S3 bucket openvidu-cfn-templates-123456789012-us-east-1 that stages the template (once per account and region)
   · create the CloudFormation stack openvidu-ce10 from .openvidu/aws/cf-openvidu-singlenode.yaml (this returns when CloudFormation is done)
note: recorded this stack's infrastructure in openvidu-stack.yml, so `ov stack destroy` removes it even if the wait below fails
   ✓ Create the machines on AWS

▶ Wait for the machines to deploy OpenVidu…
   · OpenVidu is up: the stack published its URL and https://openvidu-40mfas-54-82-78-43.sslip.io/health/caddy answers 200
   ✓ Wait for the machines to deploy OpenVidu

▶ Register the stack…

Stack described by the deployment:
  name         ce10
  deployment   single_node · aws · community
  version      ov-admin
  modules      dashboard, egress, ingress, meet, observability
  dashboard    https://openvidu-40mfas-54-82-78-43.sslip.io
  nodes        54.82.78.43
  published    by ov/ov-admin on 2026-10-29 11:48 UTC (generation 1)

note: this stack was deployed on the machine itself, so its desired state named 127.0.0.1; retargeted at 54.82.78.43, the host this import reached
✔ registered stack "ce10" in /home/me/ce10
   ✓ Register the stack

✔ OpenVidu Community (single node) is up on AWS
  URL:          https://openvidu-40mfas-54-82-78-43.sslip.io/
  credentials:  aws secretsmanager get-secret-value --secret-id openvidu-us-east-1-openvidu-ce10 --query SecretString --output text --region us-east-1
  SSH:          ubuntu@54.82.78.43 (key .openvidu/aws/openvidu-ce10-key.pem)

Try it:
  ov stack status
  ov stack logs --tail 50
```

A region that does not offer the default instance type (`c6a.xlarge` is missing from `eu-south-2`, for one) gets the same size in `c5` or `m5`, and the deploy says so. A type you choose yourself is never replaced: if the region does not offer it, the deploy stops before creating anything.

## What the deploy creates

| Resource | Notes |
| --- | --- |
| A CloudFormation stack, `openvidu-<name>` | Holds every resource below except the key pair; `--aws-stack-name` names it |
| EC2 instances | One for Single Node; master nodes and an auto scaling group of media nodes for Elastic and High Availability |
| An Elastic IP and security groups | The ports OpenVidu needs, open to the internet |
| A Network Load Balancer | High Availability only |
| An S3 bucket and an IAM user scoped to it | Recordings and OpenVidu Meet data. `--aws-app-data-bucket` uses your own bucket |
| A Secrets Manager secret | What the stack publishes: URL and credentials (and the kubeconfig on PRO) |
| An EC2 key pair, `openvidu-<name>-key` | Only its public half; the private half stays in `.openvidu/aws/` |
| The bucket `openvidu-cfn-templates-<account>-<region>` | Stages the template, shared by every stack of the account in that region |

`ov` writes the stack's infrastructure into `openvidu-stack.yml` **before** creating it, so `ov stack destroy` in the directory removes whatever a failed deploy left behind.

## Access OpenVidu

The deploy prints the URL of the deployment. OpenVidu Meet answers at `/`, and OpenVidu Dashboard at `/dashboard/`, with a valid certificate:

```console
$ D=openvidu-40mfas-54-82-78-43.sslip.io
$ curl -s -o /dev/null -w "meet %{http_code}\n" https://$D/
meet 302
$ curl -s -o /dev/null -w "dashboard %{http_code}\n" https://$D/dashboard/
dashboard 200
```

The credentials are in the stack's Secrets Manager secret, the command printed on the `credentials:` line. These are the keys of a Single Node COMMUNITY stack (values replaced by their length):

```text
DASHBOARD_ADMIN_PASSWORD       <set, 44 chars>
DASHBOARD_ADMIN_USERNAME       dashboardadmin
DASHBOARD_URL                  https://openvidu-40mfas-54-82-78-43.sslip.io/dashboard/
DOMAIN_NAME                    openvidu-40mfas-54-82-78-43.sslip.io
ENABLED_MODULES                egress,ingress,dashboard,meet,observability
GRAFANA_ADMIN_PASSWORD         <set, 44 chars>
GRAFANA_ADMIN_USERNAME         grafanaadmin
GRAFANA_URL                    https://openvidu-40mfas-54-82-78-43.sslip.io/grafana/
LIVEKIT_API_KEY                <set, 15 chars>
LIVEKIT_API_SECRET             <set, 44 chars>
LIVEKIT_URL                    wss://openvidu-40mfas-54-82-78-43.sslip.io/
MEET_INITIAL_ADMIN_PASSWORD    <set, 44 chars>
MEET_INITIAL_ADMIN_USER        admin
MEET_INITIAL_API_KEY           <set, 44 chars>
MEET_URL                       https://openvidu-40mfas-54-82-78-43.sslip.io/
OPENVIDU_URL                   https://openvidu-40mfas-54-82-78-43.sslip.io/
S3_APP_DATA_BUCKET             openvidu-appdata-d56324d0
…
```

`ov stack config get <key>` reads any of them from the running stack. The secret is a copy made at the deploy: after a later `ov stack config set`, the stack is the truth, not the secret.

Your applications connect with `LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`, as with any other OpenVidu deployment.

To look inside a machine, use the key pair the deploy generated (the `SSH:` line). The node has `ov` too, so `sudo ov stack …` there operates the same stack:

```bash
ssh -i .openvidu/aws/openvidu-ce10-key.pem ubuntu@54.82.78.43
```

## Review the commands first: assisted mode

`--mode assisted` runs **nothing at all** in your account. It writes the rendered template and its parameters into `.openvidu/aws/` and prints the same commands, for you to read, change and run yourself:

```bash
ov stack deploy openvidu --cloud aws --aws-region us-east-1 \
  --certificate-type letsencrypt --mode assisted
```

It ends with the command that continues the deploy once you have run them. On OpenVidu PRO the continuation reads the kubeconfig the stack published; on Community it reads the stack from the machine over SSH. This output is from a PRO Elastic deploy:

```text
Nothing above has been run. Run it yourself, then continue the deploy — naming
the stack is enough, this CLI reads everything else back from it:

  ov stack deploy --cloud aws --mode auto

From there the deploy waits for OpenVidu to come up, reads the kubeconfig the stack
published and registers this directory as the stack, exactly as it would have done here.
```

That command needs no flags: the desired state, the CloudFormation stack's name and every parameter are already in `openvidu-stack.yml`, and a CloudFormation stack that already exists is **reused**, not created again.

## Change a parameter of the stack

`ov stack deploy --cloud aws --param Name=Value` in the stack's directory updates the CloudFormation stack with the parameters that changed. Any parameter the template declares can be set this way. For example, the maximum number of media nodes of an Elastic stack:

```bash
ov stack deploy --cloud aws --param MaxNumberOfMediaNodes=3 --mode auto -y
```

See [Scaling](../operate/scaling.md) for media nodes and [Configuration](../operate/configuration.md) for OpenVidu's own settings, which change without touching the machines.

## Destroy the stack

One command deletes the machines too. You must say what happens to the recordings and OpenVidu Meet data: `--keep-data` leaves the S3 bucket, `--delete-data` deletes it.

```console
$ ov stack destroy -y --delete-data
This is what will be deleted from your AWS account:

  # The machines (for elastic/HA also their auto-scaling group and load balancer),
  # the Elastic IP, the security groups and the secret.
  # elastic/HA: first let the media nodes go without draining their sessions.
  aws autoscaling delete-lifecycle-hook --auto-scaling-group-name '$(aws cloudformation describe-stack-resource --stack-name openvidu-ce10 --logical-resource-id MediaNodeAutoScalingGroup --query StackResourceDetail.PhysicalResourceId --output text --region us-east-1)' --lifecycle-hook-name openvidu-media-drain --region us-east-1
  aws cloudformation delete-stack --stack-name openvidu-ce10 --region us-east-1

  # The key pair this stack's deploy imported.
  aws ec2 delete-key-pair --key-name openvidu-ce10-key --region us-east-1

  # The template this stack's deploy staged (the bucket stays: every stack in the
  # region shares it).
  aws s3 rm s3://openvidu-cfn-templates-123456789012-us-east-1/openvidu-ce10/ --recursive --only-show-errors --region us-east-1
…

▶ Delete the machine on AWS…
   · delete the CloudFormation stack openvidu-ce10 (instance, Elastic IP, security group, secret)
   · wait for the resources to go
   · deleted the bucket openvidu-appdata-d56324d0 and everything in it
   · delete the key pair openvidu-ce10-key
   · delete the template this deploy staged in s3://openvidu-cfn-templates-123456789012-us-east-1/openvidu-ce10/
   ✓ Delete the machine on AWS
✔ removed stack "ce10" from this directory
```

The bucket `openvidu-cfn-templates-<account>-<region>` stays, because every stack of the region shares it. More options in [Destroy](../operate/destroy.md).

!!! warning "Reusing a stack name"

    Secrets Manager deletes a secret with a recovery window, so its name stays taken for some days. Deploying a new stack with the same name in the same region fails until then. Free the name with `aws secretsmanager delete-secret --secret-id openvidu-<region>-openvidu-<name> --force-delete-without-recovery`.

## Next steps

- [Check the status](../operate/status.md) of the stack and run its health check.
- [Change its configuration](../operate/configuration.md) or [its modules](../operate/modules.md).
- [Operate it from another machine](../operate/remote.md), with `--remote-state`.
