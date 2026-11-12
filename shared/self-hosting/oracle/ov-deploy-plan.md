Before it touches your tenancy, the deploy prints exactly what it will run and asks for confirmation (`-y` confirms in advance; the list is printed anyway). This is the output of a Single Node COMMUNITY deploy of a stack named `ce12o` (eu-madrid-1, 2026-10-29; OCIDs and the Object Storage namespace shown as placeholders):

??? example "The full plan (click to expand)"

    ```text
    This is what will be done in your Oracle Cloud tenancy (region eu-madrid-1, compartment ocid1.compartment.oc1..<compartment>):

      # Terraform authenticates with your OCI API key (~/.oci/config); so does the state
      # bucket's backend, which needs Terraform 1.12.0 or later.
      # The template, rendered from the one embedded in this CLI for the single node topology,
      # and its variables, written out for you to read (the variables file is 0600: it
      # can carry secrets, such as Meet's seed credentials or a private key):
      #   .openvidu/oracle/tf-oracle-openvidu-singlenode.tf
      #   .openvidu/oracle/openvidu.auto.tfvars.json
      terraform -chdir=.openvidu/oracle init -input=false -no-color -force-copy
      # Create the machine. deployedBy=instance: it installs OpenVidu on itself with the
      # OpenVidu CLI. `apply` returns when Terraform is done (about 3 minutes, then OpenVidu installs); OpenVidu comes up after.
      terraform -chdir=.openvidu/oracle apply -auto-approve -input=false -no-color

      # Read back where the stack is (sensitive outputs, such as a generated SSH key, show as
      # <sensitive>: `terraform output -raw <name>` prints one).
      terraform -chdir=.openvidu/oracle output
      # What the stack published: URL and credentials, as secrets in the stack's vault, base64 (OPENVIDU_URL appears once
      # OpenVidu serves: until then this read fails, and the command that continues the deploy waits for it).
      VAULT="$(terraform -chdir=.openvidu/oracle output -raw vault_id)"
      oci secrets secret-bundle get-secret-bundle-by-name --secret-name OPENVIDU_URL --vault-id $VAULT --query 'data."secret-bundle-content".content' --raw-output --region eu-madrid-1 | base64 -d
    ```

Then it runs them, waits for OpenVidu and registers the stack. The `apply` returns in about three minutes, before OpenVidu is installed, so most of the waiting comes afterwards: `ov` polls the vault for the stack's `OPENVIDU_URL` secret and checks the published URL answers Caddy's health check:

```text
▶ Create the machines on Oracle Cloud…
   · initialize Terraform in .openvidu/oracle (downloads the provider)
   · apply .openvidu/oracle (this returns when Terraform is done)
note: recorded this stack's infrastructure in openvidu-stack.yml, so `ov stack destroy` removes it even if the wait below fails
   ✓ Create the machines on Oracle Cloud

▶ Wait for the machines to deploy OpenVidu…
   · waiting for OpenVidu to come up (2m16s elapsed): the stack has not published its URL yet (OpenVidu is still installing)
   …
   · OpenVidu is up: the stack published its URL and https://openvidu-u57z2l-51-170-56-241.sslip.io/health/caddy answers 200
   ✓ Wait for the machines to deploy OpenVidu

▶ Register the stack…

Stack described by the deployment:
  name         ce12o
  deployment   single_node · oracle · community
  version      ov-admin
  modules      dashboard, egress, ingress, meet, observability
  dashboard    https://openvidu-u57z2l-51-170-56-241.sslip.io
  nodes        51.170.56.241
  published    by ov/ov-admin on 2026-10-29 16:38 UTC (generation 1)

note: this stack was deployed on the machine itself, so its desired state named 127.0.0.1; retargeted at 51.170.56.241, the host this import reached
✔ registered stack "ce12o" in /home/me/ce12o
   ✓ Register the stack

✔ OpenVidu Community (single node) is up on Oracle Cloud
  URL:          https://openvidu-u57z2l-51-170-56-241.sslip.io/
  credentials:  oci secrets secret-bundle get-secret-bundle-by-name --secret-name OPENVIDU_URL --vault-id ocid1.vault.oc1.eu-madrid-1.<vault> --query 'data."secret-bundle-content".content' --raw-output --region eu-madrid-1 | base64 -d
  SSH:          ubuntu@51.170.56.241 (key .openvidu/oracle/openvidu-ce12o-key.pem)

Try it:
  ov stack status
  ov stack logs --tail 50
```

The `retargeted` note is expected: the machine deployed OpenVidu on itself, and `ov` points your directory at its public address. On a single node the instance gets the template's shape, `VM.Standard.E4.Flex` with 4 OCPUs and 8 GB, and a 100 GB boot volume, unless you pass `--param instanceType=<shape>` (and `--param instanceOCPUs=<n>`, `--param instanceMemory=<gb>` for Flex shapes).
