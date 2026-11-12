`--mode assisted` runs **nothing at all** in your project. It writes the rendered template and its variables to `.openvidu/gcp/` and prints the same commands, for you to read, change and run yourself:

```bash
ov stack deploy openvidu --cloud gcp --gcp-project my-project \
  --certificate-type letsencrypt --mode assisted
```

It ends with the command that continues the deploy once you have run them. This is the end for Community, which reads the stack from the machine over SSH:

```text
Nothing above has been run. Run it yourself, then continue the deploy — the Terraform
state and this directory's record are enough, this CLI reads everything else back:

  ov stack deploy openvidu --cloud gcp --mode auto

From there the deploy waits for OpenVidu to come up, reads the stack from the machine
over SSH (as `ov stack import --ssh` does) with the key the template generated (its private key output), and registers
this directory as the stack, exactly as it would have done here.
```

On OpenVidu PRO the continuation reads the access the stack published instead of using SSH. The command carries only the stack's name (without it the stack is registered as `openvidu`); every parameter is already in `openvidu-stack.yml`, and `terraform apply` is idempotent, so a resume applies the same state again (a no-op that refreshes the outputs) and then waits for OpenVidu.
