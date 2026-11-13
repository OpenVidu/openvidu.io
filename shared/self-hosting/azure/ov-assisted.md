`--mode assisted` runs **nothing at all** in your subscription. It writes the rendered template to `.openvidu/azure/` and prints the commands, for you to read, change and run yourself:

```bash
ov stack deploy openvidu --cloud azure --azure-location northeurope \
  --certificate-type letsencrypt --mode assisted
```

```text
── PLAN · nothing below has run ───────────────────────────────────────
Run these commands yourself in your Azure subscription (location northeurope); ov runs none of them:

  # SSH access: the key pair for this stack, its public half handed to the template.
  …

Nothing above has been run. Once these commands have finished, run this same command again:

  ov stack deploy openvidu --cloud azure --mode assisted

It finds the machines, waits for OpenVidu to come up and registers this directory as the
stack. It creates nothing in your account.
── end of plan ────────────────────────────────────────────────────────
```

On OpenVidu PRO the commands also write the license into a `0600` parameters file (`.openvidu/azure/secure-parameters.json`) instead of the command line.

Once your commands have finished, run the command it ends with. It carries the stack's name, and `openvidu-stack.yml` keeps every parameter. When the deployment has succeeded with the parameters this deploy asks for, the deploy ends without asking anything:

```text
The machines on Azure are there, as this deploy asks for them (Succeeded): it ends here,
creating nothing. It waits for OpenVidu to come up and registers this directory as the stack.

▶ Find the machines on Azure…
…
▶ Wait for the machines to deploy OpenVidu…
…
▶ Register the stack…
…
✔ OpenVidu Community (single node) is up on Azure
```

While the deployment is still running (`Running`, `Accepted`…), it says so and asks you to run the same command again later. If there is no deployment yet, or a parameter changed, it prints the commands again (the update ones, on a deployment that exists). With `--remote-state` it also prints the commands that save the stack's record, without running them, and settings a redeploy applies inside the stack (as `ov stack config set` does) are printed for you to run, not applied.
