`--mode assisted` runs **nothing at all** in your account. It writes the rendered template and its variables to `.openvidu/digitalocean/` and prints the same commands, for you to read, change and run yourself:

```bash
ov stack deploy openvidu --cloud digitalocean \
  --certificate-type letsencrypt --mode assisted
```

It ends with the command that continues the deploy once you have run them. This is the end for Community, which reads the stack from the machine over SSH:

```text
Nothing above has been run. Run it yourself, then continue the deploy — the Terraform
state and this directory's record are enough, this CLI reads everything else back:

  ov stack deploy <name> --cloud digitalocean --mode auto

From there the deploy waits for OpenVidu to come up, reads the stack from the machine
over SSH (as `ov stack import --ssh` does) with the key the template generated (its private key output), and registers
this directory as the stack, exactly as it would have done here.
```

The continuation carries the stack's name, which `openvidu-stack.yml` keeps: without it the stack is registered again as `openvidu`. On OpenVidu PRO it reads the access the stack published instead of using SSH. Every parameter is already in place, so a resume applies the same state again and then waits for OpenVidu.
