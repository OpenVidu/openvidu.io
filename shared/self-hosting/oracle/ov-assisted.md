`--mode assisted` runs **nothing at all** in your tenancy. It writes the rendered template and its variables to `.openvidu/oracle/` and prints the commands, for you to read, change and run yourself:

```bash
ov stack deploy openvidu --cloud oracle --oci-region eu-madrid-1 --mode assisted
```

```text
── PLAN · nothing below has run ───────────────────────────────────────
Run these commands yourself in your Oracle Cloud tenancy (region eu-madrid-1, compartment ocid1.compartment.oc1..<compartment>); ov runs none of them:

  …

Nothing above has been run. Once these commands have finished, run this same command again:

  ov stack deploy openvidu --cloud oracle --mode assisted

It finds the machines, waits for OpenVidu to come up and registers this directory as the
stack. It creates nothing in your account.
── end of plan ────────────────────────────────────────────────────────
```

Once your commands have finished, run the command it ends with. It needs no other flags: every parameter is already in `openvidu-stack.yml`. When the Terraform state is there and `terraform plan` changes nothing, the deploy ends without asking anything:

```text
The machines on Oracle Cloud are there, as this deploy asks for them (applied): it ends here,
creating nothing. It waits for OpenVidu to come up and registers this directory as the stack.

▶ Find the machines on Oracle Cloud…
…
▶ Wait for the machines to deploy OpenVidu…
…
▶ Register the stack…
…
✔ OpenVidu Community (single node) is up on Oracle Cloud
```

If there is no state yet, or the plan would change something, it prints the commands again. With `--remote-state` it also prints the commands that save the stack's record, without running them, and settings a redeploy applies inside the stack (as `ov stack config set` does) are printed for you to run, not applied.
