`--mode assisted` runs **nothing at all** in your account. It writes the rendered template and its parameters to `.openvidu/aws/` and prints the same commands, for you to read, change and run yourself:

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
