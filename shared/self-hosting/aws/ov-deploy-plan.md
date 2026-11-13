Before it touches your account, `ov` prints a **short plan**, one numbered line per step, and asks to go ahead. `-y` answers yes in advance: it skips the question, not the plan. `--debug` prints the commands themselves, and [assisted mode](#review-the-commands-first-assisted-mode) prints them and runs nothing. This is the plan of a Single Node COMMUNITY deploy of a stack named `ce10` (region `us-east-1`):

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

On Elastic and High Availability the **Network** step names the subnets it chose, the **Machines** step creates the master and the media nodes (four masters on High Availability), and a deploy with a domain adds a **Domain** step.

Then `ov` creates the machines, waits for OpenVidu and registers the stack in this directory. The machines take a few minutes; most of the wait is OpenVidu installing on them. The deploy ends with the stack's address and how to read its credentials:

```text
…
✔ OpenVidu Community (single node) is up on AWS
  URL:          https://openvidu-40mfas-54-82-78-43.sslip.io/
  credentials:  aws secretsmanager get-secret-value --secret-id openvidu-us-east-1-openvidu-ce10 --query SecretString --output text --region us-east-1
  SSH:          ubuntu@54.82.78.43 (key .openvidu/aws/openvidu-ce10-key.pem)

Try it:
  ov stack status
  ov stack logs --tail 50
```

A region that does not offer the default instance type (`c6a.xlarge` is not available in `eu-south-2`, for example) gets the equivalent `c5` or `m5` size, and the deploy says so. A type you choose yourself is never replaced: if the region does not offer it, the deploy stops before creating anything.
