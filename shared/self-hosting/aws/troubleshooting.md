**The CloudFormation stack failed to create.** `ov` runs `aws cloudformation deploy` as you, so a create that ends in `CREATE_FAILED` (a bad parameter, a missing permission, an AWS-side problem) surfaces as an error from your own `aws` CLI. `ov` records the stack's infrastructure in `openvidu-stack.yml` **before** creating anything, so you can always clean a failed attempt up from the directory:

```bash
ov stack destroy --delete-data   # or --keep-data
```

To see why the machine itself did not finish deploying OpenVidu, SSH into the instance with the key pair the deploy generated (in `.openvidu/aws/`) and read `/var/log/cloud-init-output.log` and `/var/log/cloud-init.log`.

**The deploy timed out waiting for OpenVidu.** The machines were created but did not finish deploying OpenVidu within the wait window (`--wait-timeout`, 40 minutes by default with `--cloud`). The infrastructure already exists, so simply resume, reusing what is there:

```bash
ov stack deploy --cloud aws --mode auto
```

**Deploying fails because the stack name is still in use.** Secrets Manager keeps a deleted secret for a recovery window, so for several days after a destroy a new stack with the **same name in the same region** cannot be created. Free the name with `aws secretsmanager delete-secret --secret-id <secret> --force-delete-without-recovery`, where `<secret>` is the name on the deploy's `credentials:` line, or deploy with a different name or region.

For closed ports, Let's Encrypt and port 80, cloud quotas and the other generic cases, see [Troubleshooting the OpenVidu CLI](/docs/self-hosting/openvidu-cli.md#troubleshooting).
