Before it touches your account, `ov` prints a **short plan**, one line per step, and waits for a yes: only `yes` or `y` goes ahead (`-y` answers in advance; it skips the question, never the plan). This is a Single Node COMMUNITY deploy of a stack named `ce12d2` (ams3, 2026-10-29):

```text
This is what ov does in your DigitalOcean account (region ams3, Spaces in ams3); --debug shows every command:

  1. Template: render the single node template into .openvidu/digitalocean/tf-do-openvidu-singlenode.tf
     and its variables into .openvidu/digitalocean/openvidu.auto.tfvars.json (0600)
  2. Machines: create the machine, which installs OpenVidu Community on itself with Terraform (about 1 minute, then OpenVidu installs)
  3. Wait for OpenVidu to answer, read the stack over SSH and register this directory as the stack

Run these in your account? Only yes or y goes ahead [y/N]:
```

`--debug` and `--mode assisted` print every command of that plan instead:

??? example "The full command list (click to expand)"

    ```text
      # Terraform authenticates with the token in the variables file (from DIGITALOCEAN_TOKEN). It
      # renders the template and its variables (0600, they can carry secrets) under .openvidu/digitalocean/:
      terraform -chdir=.openvidu/digitalocean init -input=false -no-color -force-copy
      # Create the machine, which installs OpenVidu on itself (about 1 minute, then OpenVidu installs).
      terraform -chdir=.openvidu/digitalocean apply -auto-approve -input=false -no-color

      # Read back where the stack is, and what it published (URL and credentials in secrets.env,
      # in the stack's Space, read with the Spaces keys; it appears once OpenVidu serves).
      terraform -chdir=.openvidu/digitalocean output
      SPACE="$(terraform -chdir=.openvidu/digitalocean output -raw appDataBucket)"
      env AWS_ACCESS_KEY_ID=$SPACES_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY=$SPACES_SECRET_ACCESS_KEY AWS_SESSION_TOKEN= aws s3 cp s3://$SPACE/secrets.env - --endpoint-url https://ams3.digitaloceanspaces.com
    ```

Then it runs them, waits for OpenVidu (the `apply` returns in about a minute, before OpenVidu is installed, so most of the wait comes afterwards) and registers the stack:

```text
▶ Create the machines on DigitalOcean…
   · apply .openvidu/digitalocean (this returns when Terraform is done)
note: recorded this stack's infrastructure in openvidu-stack.yml, so `ov stack destroy` removes it even if the wait below fails
   ✓ Create the machines on DigitalOcean

▶ Wait for the machines to deploy OpenVidu…
   · waiting for OpenVidu to come up (1s elapsed): the published values are not readable yet: secrets.env is not in the Space openvidu-ce12d2-space-dae2e06c8c yet (the machine writes it as it installs)
   …
   · OpenVidu is up: the stack published its URL and https://openvidu-324jl8-164-92-159-209.sslip.io/health/caddy answers 200
   ✓ Wait for the machines to deploy OpenVidu

▶ Register the stack…

Stack described by the deployment:
  name         ce12d2
  deployment   single_node · digitalocean · community
  modules      dashboard, egress, ingress, meet, observability
  dashboard    https://openvidu-324jl8-164-92-159-209.sslip.io
  nodes        164.92.159.209
✔ registered stack "ce12d2" in /home/me/ce12d2
   ✓ Register the stack

✔ OpenVidu Community (single node) is up on DigitalOcean
  URL:          https://openvidu-324jl8-164-92-159-209.sslip.io/
  credentials:  env AWS_ACCESS_KEY_ID=$SPACES_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY=$SPACES_SECRET_ACCESS_KEY AWS_SESSION_TOKEN= aws s3 cp s3://openvidu-ce12d2-space-dae2e06c8c/secrets.env - --endpoint-url https://ams3.digitaloceanspaces.com
  SSH:          root@164.92.159.209 (key .openvidu/digitalocean/openvidu-ce12d2-key.pem)

Try it:
  ov stack status
  ov stack logs --tail 50
```

The Droplet gets the template's size, `s-4vcpu-8gb` (4 vCPU, 8 GB, 160 GB disk), unless you pass `--param instanceType=<slug>`. DigitalOcean logs you in as `root`.
