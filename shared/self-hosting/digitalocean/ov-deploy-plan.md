Before it touches your account, the deploy prints exactly what it will run and asks for confirmation (`-y` confirms in advance; the list is printed anyway). This is the output of a Single Node COMMUNITY deploy of a stack named `ce12d2` (ams3, 2026-10-29):

??? example "The full plan (click to expand)"

    ```text
    This is what will be done in your DigitalOcean account (region ams3, Spaces in ams3):

      # Terraform authenticates with the token in the variables file (from DIGITALOCEAN_TOKEN).
      # The template, rendered from the one embedded in this CLI for the single node topology,
      # and its variables, written out for you to read (the variables file is 0600: it
      # can carry secrets, such as Meet's seed credentials or a private key):
      #   .openvidu/digitalocean/tf-do-openvidu-singlenode.tf
      #   .openvidu/digitalocean/openvidu.auto.tfvars.json
      terraform -chdir=.openvidu/digitalocean init -input=false -no-color -force-copy
      # Create the machine. deployedBy=instance: it installs OpenVidu on itself with the
      # OpenVidu CLI. `apply` returns when Terraform is done (about 1 minute, then OpenVidu installs); OpenVidu comes up after.
      terraform -chdir=.openvidu/digitalocean apply -auto-approve -input=false -no-color

      # Read back where the stack is (sensitive outputs, such as a generated SSH key, show as
      # <sensitive>: `terraform output -raw <name>` prints one).
      terraform -chdir=.openvidu/digitalocean output
      # What the stack published: URL and credentials in secrets.env, in the stack's Space
      # (it appears once OpenVidu serves: until then this read fails, and the command that continues the deploy waits for it). Read with the Spaces keys.
      SPACE="$(terraform -chdir=.openvidu/digitalocean output -raw appDataBucket)"
      env AWS_ACCESS_KEY_ID=$SPACES_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY=$SPACES_SECRET_ACCESS_KEY AWS_SESSION_TOKEN= aws s3 cp s3://$SPACE/secrets.env - --endpoint-url https://ams3.digitaloceanspaces.com
    ```

Then it runs them, waits for OpenVidu and registers the stack. The `apply` returns in about a minute, before OpenVidu is installed, so most of the waiting comes afterwards: `ov` polls the Space for `secrets.env`, then checks that the published URL passes Caddy's health check:

```text
▶ Create the machines on DigitalOcean…
   · initialize Terraform in .openvidu/digitalocean (downloads the provider)
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
  version      ov-admin
  modules      dashboard, egress, ingress, meet, observability
  dashboard    https://openvidu-324jl8-164-92-159-209.sslip.io
  nodes        164.92.159.209
  published    by ov/ov-admin on 2026-10-29 16:36 UTC (generation 1)

note: this stack was deployed on the machine itself, so its desired state named 127.0.0.1; retargeted at 164.92.159.209, the host this import reached
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

The `retargeted` note is expected: the machine deployed OpenVidu on itself, and `ov` points your directory at its public address. The Droplet gets the template's size, `s-4vcpu-8gb` (4 vCPU, 8 GB, 160 GB disk), unless you pass `--param instanceType=<slug>`. DigitalOcean logs you in as `root`.
