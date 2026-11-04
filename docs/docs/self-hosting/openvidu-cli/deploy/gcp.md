---
title: "Deploy OpenVidu on Google Cloud with the OpenVidu CLI"
description: "Create the Compute Engine instances and deploy OpenVidu COMMUNITY or PRO on Google Cloud with one OpenVidu CLI command, then operate and destroy it."
page_features: [lazyvideo]
---

# Deploy OpenVidu on Google Cloud with the OpenVidu CLI

<div class="provider-chip" markdown>

:material-google-cloud:{ .provider-chip-icon } Google Cloud Platform

</div>

One command creates the machines and OpenVidu comes up on them. `ov` renders the Terraform module embedded in its own binary for the edition and topology you ask for, applies it with **your own `terraform` and `gcloud` credentials**, and the machines deploy OpenVidu themselves with the same `ov` build. When OpenVidu answers, `ov` registers the stack in your directory, and you operate it from there.

<!-- VIDEO: deploy-gcp.mp4 (docs-video) -->

## Requirements

- The [OpenVidu CLI](../install.md).
- A Google Cloud project and [**Terraform** :fontawesome-solid-external-link:{.external-link-icon}](https://developer.hashicorp.com/terraform/install){:target="_blank"} on your PATH: `ov` drives your own Terraform, so the provider plugins, the state and the audit trail are the ones that apply.
- `gcloud` **application-default credentials** (`gcloud auth application-default login`), which Terraform and the secret reads use.
- A project id: `--gcp-project`, else `$GCP_PROJECT_ID`, else what `gcloud` has configured. `--gcp-region` / `--gcp-zone` default to the template's `europe-west2` / `europe-west2-b`.
- Permission to create Compute Engine instances, a static address, firewall rules, a Cloud Storage bucket, service accounts and Secret Manager secrets. The template also **mints a service-account key** for the storage account egress uploads recordings with, so the project must allow key creation (an `iam.disableServiceAccountKeyCreation` org policy stops the apply).
- For OpenVidu PRO, your **license** (`--openvidu-pro-license`). The deploy checks it is there before it touches your project.

You need no key pair and no domain: the template generates an SSH key pair for the stack, and without `--domain-name` the stack derives a `sslip.io` name from its public IP (on High Availability, from the load balancer's), so Let's Encrypt has a name to certify on Single Node and Elastic. Use your own domain for anything real.

## Deploy

An empty directory is the stack. Choose the edition and topology:

=== "Single Node **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud gcp --gcp-project my-project \
      --certificate-type letsencrypt --mode auto
    ```

    One Compute Engine instance (`e2-standard-4` by default, `--param instanceType=<type>` to change it) running OpenVidu on Docker Compose.

=== "Single Node **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud gcp --gcp-project my-project \
      --edition pro --openvidu-pro-license <your-license> \
      --certificate-type letsencrypt --mode auto
    ```

    One Compute Engine instance running OpenVidu PRO on Kubernetes. `--param kubeAPIAllowedCidr=<cidr>` limits who can reach the cluster API on port 6443, which gives full control of the stack: do not leave it open to `0.0.0.0/0` on a production stack.

    <!-- PENDING-RUN (docs-ov, dw): gcp pro single_node with today's ov -->

=== "Elastic **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud gcp --gcp-project my-project \
      --edition pro --openvidu-pro-license <your-license> --deployment-type elastic \
      --certificate-type letsencrypt --mode auto
    ```

    One master node and a managed instance group of media nodes. The media nodes scale between `minNumberOfMediaNodes` and `maxNumberOfMediaNodes` (`--param`), or `--set infrastructure.mediaNodes.fixedCount=N` runs exactly N of them.

    <!-- PENDING-RUN (mvp-cloud mq2): gcp pro elastic output -->

=== "High Availability **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud gcp --gcp-project my-project \
      --edition pro --openvidu-pro-license <your-license> --deployment-type ha \
      --mode auto
    ```

    Four master nodes behind a passthrough TCP load balancer, plus a managed instance group of media nodes.

    The load balancer passes TLS through untouched, and Caddy on the masters terminates it with the certificate type you choose:

    - **`selfsigned`**, the default on High Availability: a certificate the four masters share. Browsers warn about it, so it is for trying the topology out.
    - **`owncert`**, for production: your own certificate for your domain, base64-encoded. Add these flags to the command above:

        ```bash
        --domain-name openvidu.example.com --certificate-type owncert \
          --owncert-public-key "$(base64 -w0 fullchain.pem)" \
          --owncert-private-key "$(base64 -w0 privkey.pem)"
        ```

    Let's Encrypt and ZeroSSL do **not** work on this topology: their HTTP challenge reaches a port 80 that only redirects to HTTPS, so the certificate is never issued and `ov stack status --wait` times out. Without `--domain-name` the stack answers at a `sslip.io` name derived from the load balancer's address; with your own domain, point it at that address (the `load_balancer_ip` output of `terraform -chdir=.openvidu/gcp output`).

    This is how the deploy of a stack named `demo-ha` ends, followed by `ov stack status --wait` confirming that every node and service is ready:

    ```text
    …
    ✔ OpenVidu Pro (high availability) is up on Google Cloud
      URL:          https://openvidu-3jjbjv-34-39-52-221.sslip.io/
      credentials:  gcloud secrets versions access latest --secret=openvidu-demo-ha-OPENVIDU_URL --project=my-project  (every secret starts with openvidu-demo-ha-)
      kubeconfig:   .openvidu/gcp/kubeconfig.yaml

    $ ov stack status --wait
    waiting for https://openvidu-3jjbjv-34-39-52-221.sslip.io to be ready (Ctrl-C to stop)…
    ✔ demo-ha is ready (https://openvidu-3jjbjv-34-39-52-221.sslip.io)
    ```

Before it touches your project, the deploy prints exactly what it will run and asks for confirmation (`-y` answers it in advance; the list is still printed). This is the output of a Single Node COMMUNITY deploy of a stack named `ce12g` (europe-west2, 2026-10-29):

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

Then it runs them, waits for OpenVidu and registers the stack. The `apply` returns in about two minutes — before OpenVidu is installed — so the wait is the real one: `ov` polls Secret Manager for the stack's `OPENVIDU_URL` secret, then checks the published URL answers Caddy's health check:

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

The instance gets the template's machine type, `e2-standard-4`, and a 100 GiB `pd-balanced` boot disk, unless you pass `--param instanceType=<type>`.

## What the deploy creates

| Resource | Notes |
| --- | --- |
| Compute Engine instances | One for Single Node; master nodes and a managed instance group of media nodes for Elastic and High Availability |
| A static address and a firewall rule | The ports OpenVidu needs, open to the internet |
| A passthrough TCP load balancer | High Availability only |
| A Cloud Storage bucket | Recordings and OpenVidu Meet data. `--param bucketName=<name>` uses your own |
| Two service accounts and a service-account key | The instance's (Meet uses it) and a storage-only one whose key egress uploads with |
| Secret Manager secrets | What the stack publishes: one secret per key, prefixed with the stack name (and the kubeconfig on PRO) |
| An SSH key pair | The template generates it; `ov` keeps the private half in `.openvidu/gcp/` |

`ov` writes the stack's infrastructure into `openvidu-stack.yml` **before** creating it, so `ov stack destroy` in the directory removes whatever a failed deploy left behind.

## Access OpenVidu

The deploy prints the URL of the deployment. OpenVidu Meet answers at `/`, and OpenVidu Dashboard at `/dashboard/`, with a valid certificate:

```console
$ D=openvidu-uj9zj7-34-105-214-170.sslip.io
$ curl -s -o /dev/null -w "meet %{http_code}\n" https://$D/
meet 302
$ curl -s -o /dev/null -w "dashboard %{http_code}\n" https://$D/dashboard/
dashboard 200
```

The credentials are one Secret Manager secret per key, every id prefixed with the stack name, the command printed on the `credentials:` line. These are the keys of a Single Node COMMUNITY stack (values replaced by their length; the service-account key masked whole):

```text
DASHBOARD_ADMIN_PASSWORD       <set, 44 chars>
DASHBOARD_ADMIN_USERNAME       dashboardadmin
DASHBOARD_URL                  https://openvidu-uj9zj7-34-105-214-170.sslip.io/dashboard/
DOMAIN_NAME                    openvidu-uj9zj7-34-105-214-170.sslip.io
ENABLED_MODULES                egress,ingress,dashboard,meet,observability
GCP_CREDENTIALS_JSON           <set>
LIVEKIT_API_KEY                <set, 15 chars>
LIVEKIT_API_SECRET             <set, 44 chars>
LIVEKIT_URL                    wss://openvidu-uj9zj7-34-105-214-170.sslip.io/
OPENVIDU_URL                   https://openvidu-uj9zj7-34-105-214-170.sslip.io/
S3_APP_DATA_BUCKET             my-project-openvidu-ce12g-1300d7
…
```

`ov stack config get <key>` reads any of them from the running stack. The secret is a copy made at the deploy: after a later `ov stack config set`, the node's files are the truth, not Secret Manager. `GCP_CREDENTIALS_JSON` is the exception Terraform writes itself — the one input only Google Cloud knows.

Your applications connect with `LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`, as with any other OpenVidu deployment.

To look inside a machine, use the key pair the deploy generated (the `SSH:` line). The login user is `ubuntu`, and the node has `ov` too, so `sudo ov stack …` there operates the same stack:

```bash
ssh -i .openvidu/gcp/openvidu-ce12g-key.pem ubuntu@34.105.214.170
```

## Review the commands first: assisted mode

`--mode assisted` runs **nothing at all** in your project. It writes the rendered template and its variables into `.openvidu/gcp/` and prints the same commands, for you to read, change and run yourself:

```bash
ov stack deploy openvidu --cloud gcp --gcp-project my-project \
  --certificate-type letsencrypt --mode assisted
```

It ends with the command that continues the deploy once you have run them:

```text
Nothing above has been run. Run it yourself, then continue the deploy — the Terraform
state and this directory's record are enough, this CLI reads everything else back:

  ov stack deploy --cloud gcp --mode auto

From there the deploy waits for OpenVidu to come up, reads the stack from the machine
over SSH (as `ov stack import --ssh` does) with the key the template generated (its private key output), and registers
this directory as the stack, exactly as it would have done here.
```

That command needs no flags: the Terraform state and every parameter are already in place, and `terraform apply` is idempotent, so a resume applies the same state again (a no-op that refreshes the outputs) and then waits for OpenVidu.

## Change a parameter of the stack

`ov stack deploy --cloud gcp --param Name=Value` in the stack's directory runs `terraform apply` again with the parameters that changed. Any parameter the template declares can be set this way. For example, the maximum number of media nodes of an Elastic stack:

```bash
ov stack deploy --cloud gcp --param maxNumberOfMediaNodes=3 --mode auto -y
```

See [Scaling](../operate/scaling.md) for media nodes and [Configuration](../operate/configuration.md) for OpenVidu's own settings, which change without touching the machines.

## Destroy the stack

One command deletes the machines too. You must say what happens to the recordings and OpenVidu Meet data: `--keep-data` leaves the bucket, `--delete-data` deletes it:

```console
$ ov stack destroy -y --delete-data
This is what will be deleted from your Google Cloud project my-project:

  # Everything the Terraform state in .openvidu/gcp holds: the machines, addresses,
  # firewall rules, secrets and service accounts.
  terraform -chdir=.openvidu/gcp init -input=false -no-color -force-copy
  terraform -chdir=.openvidu/gcp destroy -auto-approve -input=false -no-color
  …
--delete-data: the recordings and Meet data are in the Cloud Storage buckets: this deletes them.

▶ Delete the machines on Google Cloud…
   · destroy .openvidu/gcp (this returns when Terraform is done)
   ✓ Delete the machines on Google Cloud
✔ removed stack "ce12g" from this directory
```

`--delete-data` takes the bucket the template created with the stack, recordings and all; `--keep-data` takes it out of the Terraform state first, so the destroy leaves it and names it. A bucket of your own (`--param bucketName=<name>`) is not in the state, so it stays either way. `--keep-infrastructure` tears the deployment down but leaves the instance running (and says so, because it is still costing money). More options in [Destroy](../operate/destroy.md).

!!! warning "Service-account key creation"

    The template mints a Cloud Storage service-account key for egress to upload recordings with. An organization policy that blocks key creation (`iam.disableServiceAccountKeyCreation`) stops the apply. Allow key creation in the project, or the deploy cannot finish.

## Next steps

- [Check the status](../operate/status.md) of the stack and run its health check.
- [Change its configuration](../operate/configuration.md) or [its modules](../operate/modules.md).
- [Operate it from another machine](../operate/remote.md), with `--remote-state`.
