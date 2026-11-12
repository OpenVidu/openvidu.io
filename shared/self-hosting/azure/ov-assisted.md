`--mode assisted` runs **nothing at all** in your subscription. It writes the rendered template to `.openvidu/azure/` and prints the same commands, for you to read, change and run yourself:

```bash
ov stack deploy openvidu --cloud azure --azure-location northeurope \
  --certificate-type letsencrypt --mode assisted
```

It ends with the command that continues the deploy once you have run them. This is the end for Community, which reads the stack from the machine over SSH:

```text
Nothing above has been run. Run it yourself, then continue the deploy with this
command; this CLI reads everything else back from the deployment:

  ov stack deploy openvidu --cloud azure --mode auto

From there the deploy waits for OpenVidu to come up, reads the stack from the machine
over SSH (as `ov stack import --ssh` does) with the key pair above, and registers
this directory as the stack, exactly as it would have done here.
```

That command carries the stack's name, which `openvidu-stack.yml` keeps; the desired state and every parameter are already there too, and a deployment that already succeeded is **reused**, not created again.

On OpenVidu PRO the plan also writes the license into a `0600` parameters file (`.openvidu/azure/secure-parameters.json`) instead of the command line, and the continuation reads the access the stack published instead of using SSH. The end of a PRO Single Node plan (stack `dpaz0`):

```text
  ov stack deploy openvidu --cloud azure --mode auto

From there the deploy waits for OpenVidu to come up, reads the access the stack
published and registers this directory as the stack, exactly as it would have done here.
```

Until you continue, the directory holds the plan but no stack: `ov stack status` answers `no stack in this directory` (exit `3`).
