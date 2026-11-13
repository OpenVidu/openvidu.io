`--mode assisted` runs **nothing at all** in your tenancy. It writes the rendered template and its variables to `.openvidu/oracle/` and prints the same commands, for you to read, change and run yourself:

```bash
ov stack deploy openvidu --cloud oracle --oci-region eu-madrid-1 --mode assisted
```

It ends with the command that continues the deploy once you have run them. This is the end of a PRO deploy; Community's continuation reads the stack over SSH instead:

```text
Nothing above has been run. Run it yourself, then continue the deploy — the Terraform
state and this directory's record are enough, this CLI reads everything else back:

  ov stack deploy openvidu --cloud oracle --mode auto

From there the deploy waits for OpenVidu to come up, reads the access the stack
published and registers this directory as the stack, exactly as it would have done here.
```

On Community the continuation reads the stack from the machine over SSH with the key the template generated; on PRO it reads the access the stack published instead. The continuation needs no flags: every parameter is already in place, so a resume applies the same state again and then waits for OpenVidu.
