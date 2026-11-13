`--mode assisted` runs **nothing at all** in your account. It only reads what it needs to write the plan (the default VPC, the instance types the region offers, and, with a domain, the Route 53 zone), writes the rendered template and its parameters to `.openvidu/aws/`, and prints the same commands, for you to read, change and run yourself:

```bash
ov stack deploy pro --cloud aws --aws-region us-east-1 \
  --edition pro --openvidu-pro-license <your-license> \
  --certificate-type letsencrypt --mode assisted
```

It ends with the command that continues the deploy once you have run them. On OpenVidu PRO the continuation reads the access the stack published; on Community it reads the stack from the machine over SSH. This output is from a PRO Single Node deploy of a stack named `pro`:

```text
Nothing above has been run. Run it yourself, then continue the deploy with this
command; this CLI reads everything else back from the stack:

  ov stack deploy pro --cloud aws --mode auto

From there the deploy waits for OpenVidu to come up, reads the access the stack
published and registers this directory as the stack, exactly as it would have done here.
```

The continuation **carries the stack's name** (`pro`): without it the stack would be registered as `openvidu`. It needs no other flags, since every parameter is already in `openvidu-stack.yml`, and a CloudFormation stack that already exists is **reused**, not created again.
