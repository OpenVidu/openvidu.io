Before it touches your project, the deploy prints exactly what it will run and asks for confirmation (`-y` confirms in advance; the list is printed anyway). This is the output of a Single Node COMMUNITY deploy of a stack named `ce12g` (europe-west2, 2026-10-29):

??? example "The full plan (click to expand)"

    ```text
    This is what will be done in your Google Cloud project my-project (region europe-west2, zone europe-west2-b):

      # The template, rendered from the one embedded in this CLI for the single node topology,
      # and its variables, written out for you to read (the variables file is 0600: it
      # can carry secrets, such as Meet's seed credentials or a private key):
      #   .openvidu/gcp/tf-gpc-openvidu-singlenode.tf
      #   .openvidu/gcp/openvidu.auto.tfvars.json
      terraform -chdir=.openvidu/gcp init -input=false -no-color -force-copy
      # Create the machine. deployedBy=instance: it installs OpenVidu on itself with the
      # OpenVidu CLI. `apply` returns when Terraform is done (about 2 minutes, then OpenVidu installs); OpenVidu comes up after.
      terraform -chdir=.openvidu/gcp apply -auto-approve -input=false -no-color

      # Read back where the stack is (sensitive outputs, such as a generated SSH key, show as
      # <sensitive>: `terraform output -raw <name>` prints one).
      terraform -chdir=.openvidu/gcp output
      # What the stack published: URL and credentials, as Secret Manager secrets under the prefix the stack outputs (OPENVIDU_URL appears once
      # OpenVidu serves: until then this read fails, and the command that continues the deploy waits for it).
      PREFIX="$(terraform -chdir=.openvidu/gcp output -raw secret_prefix)"
      gcloud secrets versions access latest --secret=${PREFIX}OPENVIDU_URL --project=my-project
    ```

Then it runs them, waits for OpenVidu and registers the stack. The `apply` returns in about two minutes, before OpenVidu is installed, so most of the waiting comes afterwards: `ov` polls Secret Manager for the stack's `OPENVIDU_URL` secret, then checks that the published URL passes Caddy's health check:

```text
▶ Create the machines on Google Cloud…
   · initialize Terraform in .openvidu/gcp (downloads the provider)
   · apply .openvidu/gcp (this returns when Terraform is done)
note: recorded this stack's infrastructure in openvidu-stack.yml, so `ov stack destroy` removes it even if the wait below fails
   ✓ Create the machines on Google Cloud

▶ Wait for the machines to deploy OpenVidu…
   · waiting for OpenVidu to come up (3s elapsed): the published values are not readable yet: no secret openvidu-ce12g-* exists yet
   · waiting for OpenVidu to come up (1m11s elapsed): the stack has not published its URL yet (OpenVidu is still installing)
   …
   · OpenVidu is up: the stack published its URL and https://openvidu-uj9zj7-34-105-214-170.sslip.io/health/caddy answers 200
   ✓ Wait for the machines to deploy OpenVidu

▶ Register the stack…

Stack described by the deployment:
  name         ce12g
  deployment   single_node · gcp · community
  version      ov-admin
  modules      dashboard, egress, ingress, meet, observability
  dashboard    https://openvidu-uj9zj7-34-105-214-170.sslip.io
  nodes        34.105.214.170
  published    by ov/ov-admin on 2026-10-29 16:36 UTC (generation 1)

note: this stack was deployed on the machine itself, so its desired state named 127.0.0.1; retargeted at 34.105.214.170, the host this import reached
✔ registered stack "ce12g" in /home/me/ce12g
   ✓ Register the stack

✔ OpenVidu Community (single node) is up on Google Cloud
  URL:          https://openvidu-uj9zj7-34-105-214-170.sslip.io/
  credentials:  gcloud secrets versions access latest --secret=openvidu-ce12g-OPENVIDU_URL --project=my-project  (every secret starts with openvidu-ce12g-)
  SSH:          ubuntu@34.105.214.170 (key .openvidu/gcp/openvidu-ce12g-key.pem)

Try it:
  ov stack status
  ov stack logs --tail 50
```

The `retargeted` note is expected: the machine deployed OpenVidu on itself, and `ov` points your directory at its public address. In this Single Node COMMUNITY example the instance gets the template's machine type, `e2-standard-4`, and a 100 GiB `pd-balanced` boot disk, unless you pass `--param instanceType=<type>`.
