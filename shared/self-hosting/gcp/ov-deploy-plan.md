Before it touches your project, `--mode auto` shows a **short plan**: one numbered line per step, what is done and where, without the commands. Then it asks whether to run it, and only `yes` or `y` goes ahead (`-y` answers in advance, and the plan still appears; no answer or any other answer creates nothing). This is the plan of a Single Node COMMUNITY deploy of a stack named `ce12g` (europe-west2, 2026-10-29):

```text
This is what ov does in your Google Cloud project my-project (region europe-west2, zone europe-west2-b); --debug shows every command:

  1. Template: render the single node template into .openvidu/gcp/tf-gpc-openvidu-singlenode.tf
     and its variables into .openvidu/gcp/openvidu.auto.tfvars.json (0600)
  2. Machines: create the machine, which installs OpenVidu Community on itself with Terraform (about 2 minutes, then OpenVidu installs)
  3. Wait for OpenVidu to answer, read the stack over SSH and register this directory as the stack

Run these in your account? Only yes or y goes ahead [y/N]:
```

The commands themselves are not in the short plan. `--debug` prints them instead, and [assisted mode](#assisted-mode) prints the same list and runs nothing. These are the commands for the deploy above:

??? example "The commands themselves (`--debug`, or assisted mode)"

    ```text
    This is what will be done in your Google Cloud project my-project (region europe-west2, zone europe-west2-b):

      # Render the template and its variables (0600, they can carry secrets):
      #   .openvidu/gcp/tf-gpc-openvidu-singlenode.tf
      #   .openvidu/gcp/openvidu.auto.tfvars.json
      terraform -chdir=.openvidu/gcp init -input=false -no-color -force-copy
      # Create the machine; it installs OpenVidu on itself. `apply` returns when Terraform is done (about 2 minutes); OpenVidu comes up after.
      terraform -chdir=.openvidu/gcp apply -auto-approve -input=false -no-color

      # Read back where the stack is (`terraform output -raw <name>` prints a sensitive output).
      terraform -chdir=.openvidu/gcp output
      # What the stack published: URL and credentials, as Secret Manager secrets under the prefix the stack outputs (OPENVIDU_URL appears once OpenVidu serves).
      PREFIX="$(terraform -chdir=.openvidu/gcp output -raw secret_prefix)"
      gcloud secrets versions access latest --secret=${PREFIX}OPENVIDU_URL --project=my-project
    ```

Then it runs them, waits for OpenVidu and registers the stack. The `apply` returns in about two minutes, before OpenVidu is installed, so most of the waiting comes afterwards:

```text
▶ Create the machines on Google Cloud…
   …
note: recorded this stack's infrastructure in openvidu-stack.yml, so `ov stack destroy` removes it even if the wait below fails
   ✓ Create the machines on Google Cloud

▶ Wait for the machines to deploy OpenVidu…
   · waiting for OpenVidu to come up: the stack has not published its URL yet (OpenVidu is still installing)
   …
   · OpenVidu is up: the stack published its URL and https://openvidu-uj9zj7-34-105-214-170.sslip.io/health/caddy answers 200
   ✓ Wait for the machines to deploy OpenVidu

▶ Register the stack…
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
