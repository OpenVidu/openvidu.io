- The [OpenVidu CLI](/docs/self-hosting/openvidu-cli.md#install-the-openvidu-cli).
- An AWS account and the [`aws` CLI :fontawesome-solid-external-link:{.external-link-icon}](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html){:target="_blank"}, **authenticated**: `aws sts get-caller-identity` must succeed. `ov` runs your own client, so your profile, region and audit trail are the ones that apply. `--aws-profile` selects a named profile.
- Permissions to create CloudFormation stacks with IAM resources, EC2 instances, Elastic IPs, security groups, S3 buckets and Secrets Manager secrets.
- A region: `--aws-region`, otherwise `$AWS_REGION`, otherwise the one set with `aws configure`.
- For OpenVidu PRO, your **license** (`--openvidu-pro-license`): [create an OpenVidu account :fontawesome-solid-external-link:{.external-link-icon}](/account.md){:target="_blank"} to get one; there is a 15-day free trial. The deploy checks that it is present before it touches your account.

You need no key pair and, except for High Availability, no domain: the deploy generates an SSH key pair for the stack, and without `--domain-name` the machine derives an `sslip.io` name from its public IP, so Let's Encrypt has a name to certify. Use your own domain for anything beyond testing.
