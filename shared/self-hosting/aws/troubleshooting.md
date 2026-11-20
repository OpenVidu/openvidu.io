**The CloudFormation stack failed to create.** `ov` runs `aws cloudformation deploy` as you, so a create that ends in `CREATE_FAILED` (a bad parameter, a missing permission, an AWS-side problem) surfaces as an error from your own `aws` CLI. `ov` records the stack's infrastructure in `openvidu-stack.yml` **before** creating anything, so you can always clean a failed attempt up from the directory:

```bash
ov stack destroy --delete-data   # or --keep-data
```

To see why the machine itself did not finish deploying OpenVidu, SSH into the instance with the key pair the deploy generated (in `.openvidu/aws/`) and read `/var/log/cloud-init-output.log` and `/var/log/cloud-init.log`.

**The deploy timed out waiting for OpenVidu.** The machines were created but did not finish deploying OpenVidu within the wait window (`--wait-timeout`, 40 minutes by default with `--cloud`). The infrastructure already exists, so simply resume, reusing what is there (name the stack, as on the first deploy: without the name it would be registered as `openvidu`):

```bash
ov stack deploy <name> --cloud aws --mode auto
```

A deploy in assisted mode resumes with `--mode assisted` instead: the error prints the command to run.

**Deploying fails because the stack name is still in use.** Secrets Manager keeps a deleted secret for a recovery window, so for several days after a destroy a new stack with the **same name in the same region** cannot be created. Free the name with `aws secretsmanager delete-secret --secret-id <secret> --force-delete-without-recovery`, where `<secret>` is the name on the deploy's `credentials:` line, or deploy with a different name or region.

**A quota blocked the deploy.** `ov` does not read AWS quotas, so a stack the account's limits cannot hold ends in `CREATE_FAILED`, as an error from your own `aws` CLI. Request a quota increase, pick a smaller size (the size parameters of the installation guide), or deploy in another region, after cleaning up the failed attempt as above.

**No media, but every service is healthy.** This is almost always a blocked **UDP** port (`443/udp` or the media range): HTTPS works and the stack looks fine, but media never arrives. [Ports](/docs/self-hosting/single-node/aws/admin.md#ports) in the administration guide shows how to run the full check, and [Logs](/docs/self-hosting/single-node/aws/admin.md#logs) how to read the logs of every service.
