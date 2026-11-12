Before it touches your account, `ov` prints a **short plan**, one numbered line per step, and asks to go ahead. `-y` answers yes in advance: it skips the question, not the plan. `--debug` (and [assisted mode](#review-the-commands-first-assisted-mode)) print the commands themselves instead. This is the plan of a Single Node COMMUNITY deploy of a stack named `ce10` (region `us-east-1`):

```text
note: recorded this stack's infrastructure in openvidu-stack.yml, so the command that continues this deploy needs no flags
This is what ov does in your AWS account (region us-east-1); --debug shows every command:

  1. SSH key: import the stack's own key pair into the region (.openvidu/aws/openvidu-ce10-key.pem)
  2. Template: render the single node template into .openvidu/aws/cf-openvidu-singlenode.yaml
     and its parameters into .openvidu/aws/cfn-parameters.json (0600)
  3. Bucket: stage the template in the S3 bucket openvidu-cfn-templates-123456789012-us-east-1 (created once, reused by every stack)
  4. Network: the region's default VPC, vpc-0a1b2c3d4e5f60789 (the template places the machine there)
  5. Machines: Create the CloudFormation stack openvidu-ce10 with the machine, which installs OpenVidu Community on itself (about 10 minutes)
  6. Wait for OpenVidu to answer, read the stack over SSH and register this directory as the stack

Run these in your account? Only yes or y goes ahead [y/N]:
```

On Elastic and High Availability the **Network** step names the subnets it chose (the master in the first zone, or the masters across zones on High Availability, and the media nodes in all of them), and a deploy with a domain adds a **Domain** step. The full command list, with every `aws` call, is what `--debug` and assisted mode print:

??? example "The same deploy with `--debug`: every command"

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

The `retargeted` note is expected: the machine deployed OpenVidu on itself, and `ov` points your directory at its public address. A region that does not offer the default instance type (`c6a.xlarge` is not available in `eu-south-2`, for example) gets the equivalent `c5` or `m5` size, and the deploy says so. A type you choose yourself is never replaced: if the region does not offer it, the deploy stops before creating anything.
