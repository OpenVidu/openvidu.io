Before it touches your tenancy, auto mode prints a short plan, one line per step, and waits for a yes (`-y` answers in advance; the plan is printed anyway). This is a Single Node COMMUNITY deploy of a stack named `ce12o` (eu-madrid-1, 2026-10-29; OCIDs and the Object Storage namespace shown as placeholders):

```text
This is what ov does in your Oracle Cloud tenancy (region eu-madrid-1, compartment ocid1.compartment.oc1..<compartment>); --debug shows every command:

  1. Template: render the single node template into .openvidu/oracle/tf-oracle-openvidu-singlenode.tf
     and its variables into .openvidu/oracle/openvidu.auto.tfvars.json (0600)
  2. Machines: create the machine, which installs OpenVidu Community on itself with Terraform (about 3 minutes, then OpenVidu installs)
  3. Wait for OpenVidu to answer, read the stack over SSH and register this directory as the stack

Run these in your account? Only yes or y goes ahead [y/N]:
```

`--debug` and `--mode assisted` print the full command behind each step (see [Review the commands first](#assisted-mode)):

??? example "The commands (`--debug` or `--mode assisted`, click to expand)"

    ```text
      # Terraform authenticates with your OCI API key (~/.oci/config). It renders the template
      # and its variables (0600, they can carry secrets) under .openvidu/oracle/:
      terraform -chdir=.openvidu/oracle init -input=false -no-color -force-copy
      # Create the machine, which installs OpenVidu on itself (about 3 minutes, then OpenVidu installs).
      terraform -chdir=.openvidu/oracle apply -auto-approve -input=false -no-color

      # Read back where the stack is, and what it published (URL and credentials, as base64 secrets
      # in the stack's vault; OPENVIDU_URL appears once OpenVidu serves).
      terraform -chdir=.openvidu/oracle output
      VAULT="$(terraform -chdir=.openvidu/oracle output -raw vault_id)"
      oci secrets secret-bundle get-secret-bundle-by-name --secret-name OPENVIDU_URL --vault-id $VAULT --query 'data."secret-bundle-content".content' --raw-output --region eu-madrid-1 | base64 -d
    ```

Then it runs them, waits for OpenVidu (the `apply` returns in about three minutes, before OpenVidu is installed, so most of the wait comes afterwards) and registers the stack:

```text
▶ Create the machines on Oracle Cloud…
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
  modules      dashboard, egress, ingress, meet, observability
  dashboard    https://openvidu-u57z2l-51-170-56-241.sslip.io
  nodes        51.170.56.241
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

On a single node the instance gets the template's shape, `VM.Standard.E4.Flex` with 4 OCPUs, unless you pass `--param instanceType=<shape>` (and `--param instanceOCPUs=<n>`, `--param instanceMemory=<gb>` for Flex shapes). COMMUNITY gets 8 GB and a 100 GB boot volume; PRO, which runs the whole cluster on one machine, gets 16 GB and a 200 GB boot volume.
