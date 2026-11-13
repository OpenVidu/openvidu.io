**`ov` prints the commands and runs none of them.** It writes the rendered template and its variables to `.openvidu/digitalocean/`. This is the plan of a COMMUNITY stack named `openvidu`:

```text
── PLAN · nothing below has run ───────────────────────────────────────
Run these commands yourself in your DigitalOcean account (region ams3, Spaces in ams3); ov runs none of them:

  …

Nothing above has been run. Once these commands have finished, run this same command again:

  ov stack deploy openvidu --cloud digitalocean --mode assisted

It finds the machines, waits for OpenVidu to come up and registers this directory as the
stack. It creates nothing in your account.
── end of plan ────────────────────────────────────────────────────────
```

**Run them yourself**, with your own credentials. Read them first, and change them if you need to.

**Then run the command the plan ends with.** It carries the stack's name, which `openvidu-stack.yml` keeps along with every parameter: without it the stack is registered again as `openvidu`. When the Terraform state is there and `terraform plan` changes nothing, `ov` finds the machines, waits for OpenVidu and registers the stack, creating nothing:

```text
The machines on DigitalOcean are there, as this deploy asks for them (applied): it ends here,
creating nothing. It waits for OpenVidu to come up and registers this directory as the stack.

▶ Find the machines on DigitalOcean…
…
▶ Wait for the machines to deploy OpenVidu…
…
▶ Register the stack…
…
✔ OpenVidu Community (single node) is up on DigitalOcean
```

If there is no state yet, or the plan would change something, it prints the commands again. With `--remote-state` it also prints the commands that save the stack's record, without running them, and settings a redeploy applies inside the stack (as `ov stack config set` does) are printed for you to run, not applied.
