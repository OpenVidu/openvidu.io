`--mode assisted` runs **nothing at all** in your project. It writes the rendered template and its variables to `.openvidu/gcp/` and prints the commands, for you to read, change and run yourself:

```bash
ov stack deploy openvidu --cloud gcp --gcp-project my-project \
  --certificate-type letsencrypt --mode assisted
```

```text
── PLAN · nothing below has run ───────────────────────────────────────
Run these commands yourself in your Google Cloud project my-project (region europe-west2, zone europe-west2-b); ov runs none of them:

  # The template, rendered from the one embedded in this CLI for the single node topology,
  …

Nothing above has been run. Once these commands have finished, run this same command again:

  ov stack deploy openvidu --cloud gcp --mode assisted

It finds the machines, waits for OpenVidu to come up and registers this directory as the
stack. It creates nothing in your account.
── end of plan ────────────────────────────────────────────────────────
```

Once your commands have finished, run the command it ends with. It carries only the stack's name (without it the stack is registered as `openvidu`): every parameter is already in `openvidu-stack.yml`. When the Terraform state is there and `terraform plan` changes nothing, the deploy ends without asking anything:

```text
The machines on Google Cloud are there, as this deploy asks for them (applied): it ends here,
creating nothing. It waits for OpenVidu to come up and registers this directory as the stack.

▶ Find the machines on Google Cloud…
…
▶ Wait for the machines to deploy OpenVidu…
…
▶ Register the stack…
…
✔ OpenVidu Community (single node) is up on Google Cloud
```

If there is no state yet, or the plan would change something, it prints the commands again. With `--remote-state` it also prints the commands that save the stack's record, without running them, and settings a redeploy applies inside the stack (as `ov stack config set` does) are printed for you to run, not applied.
