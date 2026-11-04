---
title: "Deploy OpenVidu on DigitalOcean with the OpenVidu CLI"
description: "Create the Droplets and deploy OpenVidu COMMUNITY or PRO on DigitalOcean with one command of the OpenVidu CLI, then operate and destroy the stack."
page_features: [lazyvideo]
---

# Deploy OpenVidu on DigitalOcean with the OpenVidu CLI

<div class="provider-chip" markdown>

:material-digital-ocean:{ .provider-chip-icon } DigitalOcean

</div>

One command creates the machines and OpenVidu comes up on them. `ov` renders the Terraform module embedded in its own binary for the edition and topology you ask for, applies it with **your own `terraform` and API token**, and the machines deploy OpenVidu themselves with the same `ov` build. When OpenVidu answers, `ov` registers the stack in your directory, and you operate it from there.

<!-- VIDEO: deploy-digitalocean.mp4 (docs-video) -->

## Requirements

- The [OpenVidu CLI](../install.md).
- A DigitalOcean account and [**Terraform** :fontawesome-solid-external-link:{.external-link-icon}](https://developer.hashicorp.com/terraform/install){:target="_blank"} on your PATH: `ov` drives your own Terraform, so the provider plugins, the state and the audit trail are the ones that apply.
- `$DIGITALOCEAN_TOKEN`: the API token Terraform authenticates with.
- The Spaces keys `$SPACES_ACCESS_KEY_ID` / `$SPACES_SECRET_ACCESS_KEY`: the deployment's object storage and (DigitalOcean has no managed secret store) its secret store are both a Space, written and read with these. `ov` uses the `aws` CLI as the S3 client to read that Space back.
- A region: `--do-region`, else `$DO_REGION`, else the template's default `ams3`.
- Permission to create Droplets, a firewall, a Space with a bucket-scoped Spaces key, SSH keys and the stack's tag (and, for Elastic and High Availability, a VPC and a load balancer).
- For OpenVidu PRO, your **license** (`--openvidu-pro-license`). The deploy checks it is there before it touches your account.

You need no key pair and no domain: the template generates an SSH key pair for the stack, and without `--domain-name` the stack derives a `sslip.io` name from its public IP (on High Availability, from the load balancer's), so Let's Encrypt has a name to certify on Single Node and Elastic. Use your own domain for anything real.

## Deploy

An empty directory is the stack. Choose the edition and topology:

=== "Single Node **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud digitalocean \
      --certificate-type letsencrypt --mode auto
    ```

    One Droplet (`s-4vcpu-8gb` by default — 4 vCPU, 8 GB, 160 GB disk, `--param instanceType=<slug>` to change it) running OpenVidu on Docker Compose.

=== "Single Node **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud digitalocean \
      --edition pro --openvidu-pro-license <your-license> \
      --certificate-type letsencrypt --mode auto
    ```

    One Droplet running OpenVidu PRO on Kubernetes. `--param kubeAPIAllowedCidr=<cidr>` limits who can reach the cluster API on port 6443, which gives full control of the stack: do not leave it open to `0.0.0.0/0` on a production stack.

    This is how the deploy of a stack named `dpdo1` ends: `ov` waits until the stack publishes its kubeconfig and the cluster answers, then registers it:

    ```text
    …
       · OpenVidu is up: the stack published its kubeconfig and the cluster API answers at openvidu-wakvlb-188-166-126-9.sslip.io:6443
    …
    ✔ OpenVidu Pro (single node) is up on DigitalOcean
      URL:          https://openvidu-wakvlb-188-166-126-9.sslip.io/
      credentials:  env AWS_ACCESS_KEY_ID=$SPACES_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY=$SPACES_SECRET_ACCESS_KEY AWS_SESSION_TOKEN= aws s3 cp s3://openvidu-dpdo1-space-ef16b466b1/secrets.env - --endpoint-url https://ams3.digitaloceanspaces.com
      kubeconfig:   .openvidu/digitalocean/kubeconfig.yaml
    ```

=== "Elastic **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud digitalocean \
      --edition pro --openvidu-pro-license <your-license> --deployment-type elastic \
      --certificate-type letsencrypt --mode auto
    ```

    One master node and an autoscaling pool of media nodes, in a VPC the template creates. The media nodes scale between `minNumberOfMediaNodes` and `maxNumberOfMediaNodes` (`--param`), or `--set infrastructure.mediaNodes.fixedCount=N` runs exactly N of them.

    <!-- PENDING-RUN (docs-ov, dw): digitalocean pro elastic with today's ov -->

=== "High Availability **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud digitalocean \
      --edition pro --openvidu-pro-license <your-license> --deployment-type ha \
      --mode auto
    ```

    Four master nodes behind a passthrough load balancer, plus an autoscaling pool of media nodes.

    The load balancer passes TLS through untouched, and Caddy on the masters terminates it with the certificate type you choose:

    - **`selfsigned`**, the default on High Availability: a certificate the four masters share. Browsers warn about it, so it is for trying the topology out.
    - **`owncert`**, for production: your own certificate for your domain, base64-encoded. Add these flags to the command above:

        ```bash
        --domain-name openvidu.example.com --certificate-type owncert \
          --owncert-public-key "$(base64 -w0 fullchain.pem)" \
          --owncert-private-key "$(base64 -w0 privkey.pem)"
        ```

    Let's Encrypt and ZeroSSL do **not** work on this topology: their HTTP challenge reaches a port 80 that only redirects to HTTPS, so the certificate is never issued and `ov stack status --wait` times out. Without `--domain-name` the stack answers at a `sslip.io` name derived from the load balancer's address; with your own domain, point it at that address (the `loadBalancerIp` output of `terraform -chdir=.openvidu/digitalocean output`).

    This is how the deploy of a stack named `demo-ha` ends, followed by `ov stack status --wait` confirming that every node and service is ready:

    ```text
    …
    ✔ OpenVidu Pro (high availability) is up on DigitalOcean
      URL:          https://openvidu-j78sfb-129-212-214-216.sslip.io/
      credentials:  env AWS_ACCESS_KEY_ID=$SPACES_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY=$SPACES_SECRET_ACCESS_KEY AWS_SESSION_TOKEN= aws s3 cp s3://openvidu-demo-ha-space-appdata-b62adba1a3/secrets.env - --endpoint-url https://ams3.digitaloceanspaces.com
      kubeconfig:   .openvidu/digitalocean/kubeconfig.yaml

    $ ov stack status --wait
    waiting for https://openvidu-j78sfb-129-212-214-216.sslip.io to be ready (Ctrl-C to stop)…
    ✔ demo-ha is ready (https://openvidu-j78sfb-129-212-214-216.sslip.io)
    ```

Before it touches your account, the deploy prints exactly what it will run and asks for confirmation (`-y` answers it in advance; the list is still printed). This is the output of a Single Node COMMUNITY deploy of a stack named `ce12d2` (ams3, 2026-10-29):

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

Then it runs them, waits for OpenVidu and registers the stack. The `apply` returns in about a minute — before OpenVidu is installed — so the wait is the real one: `ov` polls the Space for `secrets.env`, then checks the published URL answers Caddy's health check:

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

The Droplet gets the template's size, `s-4vcpu-8gb` (4 vCPU, 8 GB, 160 GB disk), unless you pass `--param instanceType=<slug>`. DigitalOcean logs you in as `root`; add your own DigitalOcean console keys with `--param sshKeyNames=<name,…>`.

## What the deploy creates

| Resource | Notes |
| --- | --- |
| Droplets | One for Single Node; master nodes and an autoscaling pool of media nodes for Elastic and High Availability |
| A firewall | The ports OpenVidu needs, open to the internet (and outbound everywhere) |
| A VPC | Elastic and High Availability only |
| A load balancer | High Availability only |
| A Space and a bucket-scoped Spaces key | Recordings and OpenVidu Meet data; also the stack's secret store (`secrets.env`). `--param spaceName=<name>` uses your own |
| An SSH key pair and the stack's tag | The template generates the key; `ov` keeps the private half in `.openvidu/digitalocean/` |

`ov` writes the stack's infrastructure into `openvidu-stack.yml` **before** creating it, so `ov stack destroy` in the directory removes whatever a failed deploy left behind.

## Access OpenVidu

The deploy prints the URL of the deployment. OpenVidu Meet answers at `/`, and OpenVidu Dashboard at `/dashboard/`, with a valid certificate:

```console
$ D=openvidu-324jl8-164-92-159-209.sslip.io
$ curl -s -o /dev/null -w "meet %{http_code}\n" https://$D/
meet 302
$ curl -s -o /dev/null -w "dashboard %{http_code}\n" https://$D/dashboard/
dashboard 200
```

The credentials are in `secrets.env` in the stack's Space, the command printed on the `credentials:` line. These are the keys of a Single Node COMMUNITY stack (values replaced by their length):

```text
DASHBOARD_ADMIN_PASSWORD       <set, 44 chars>
DASHBOARD_ADMIN_USERNAME       dashboardadmin
DASHBOARD_URL                  https://openvidu-324jl8-164-92-159-209.sslip.io/dashboard/
DOMAIN_NAME                    openvidu-324jl8-164-92-159-209.sslip.io
ENABLED_MODULES                egress,ingress,dashboard,meet,observability
EXTERNAL_S3_ACCESS_KEY         <set, 20 chars>
EXTERNAL_S3_ENDPOINT           https://ams3.digitaloceanspaces.com
EXTERNAL_S3_SECRET_KEY         <set, 43 chars>
LIVEKIT_API_KEY                <set, 15 chars>
LIVEKIT_API_SECRET             <set, 44 chars>
LIVEKIT_URL                    wss://openvidu-324jl8-164-92-159-209.sslip.io/
OPENVIDU_URL                   https://openvidu-324jl8-164-92-159-209.sslip.io/
S3_APP_DATA_BUCKET             openvidu-ce12d2-space-dae2e06c8c
…
```

`ov stack config get <key>` reads any of them from the running stack. `secrets.env` is a copy made at the deploy: after a later `ov stack config set`, the node's files are the truth, not the Space.

Your applications connect with `LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`, as with any other OpenVidu deployment.

To look inside a machine, use the key pair the deploy generated (the `SSH:` line). The login user is `root`, and the node has `ov` too, so `ov stack …` there operates the same stack:

```bash
ssh -i .openvidu/digitalocean/openvidu-ce12d2-key.pem root@164.92.159.209
```

## Review the commands first: assisted mode

`--mode assisted` runs **nothing at all** in your account. It writes the rendered template and its variables into `.openvidu/digitalocean/` and prints the same commands, for you to read, change and run yourself:

```bash
ov stack deploy openvidu --cloud digitalocean \
  --certificate-type letsencrypt --mode assisted
```

It ends with the command that continues the deploy once you have run them. This is the end for Community, which reads the stack from the machine over SSH:

```text
Nothing above has been run. Run it yourself, then continue the deploy — the Terraform
state and this directory's record are enough, this CLI reads everything else back:

  ov stack deploy --cloud digitalocean --mode auto

From there the deploy waits for OpenVidu to come up, reads the stack from the machine
over SSH (as `ov stack import --ssh` does) with the key the template generated (its private key output), and registers
this directory as the stack, exactly as it would have done here.
```

On OpenVidu PRO the continuation reads the kubeconfig the stack published instead of using SSH. That command needs no flags: the Terraform state and every parameter are already in place, and `terraform apply` is idempotent, so a resume applies the same state again (a no-op that refreshes the outputs) and then waits for OpenVidu.

## Change a parameter of the stack

`ov stack deploy --cloud digitalocean --param Name=Value` in the stack's directory runs `terraform apply` again with the parameters that changed. Any parameter the template declares can be set this way. For example, the maximum number of media nodes of an Elastic stack:

```bash
ov stack deploy --cloud digitalocean --param maxNumberOfMediaNodes=3 --mode auto -y
```

See [Scaling](../operate/scaling.md) for media nodes and [Configuration](../operate/configuration.md) for OpenVidu's own settings, which change without touching the machines.

## Destroy the stack

One command deletes the machines too. You must say what happens to the recordings and OpenVidu Meet data: `--keep-data` leaves the Space, `--delete-data` deletes it. A Space must be empty to go, and the machine writes into it until it is gone, so the Space is emptied between two passes:

```console
$ ov stack destroy -y --delete-data
This is what will be deleted from your DigitalOcean account:

  # Everything the Terraform state in .openvidu/digitalocean holds: the Droplets, the VPC, the
  # firewalls, the load balancer and the Spaces. A Space must be empty to go, and the master
  # writes into it until it is gone, so the Spaces are emptied between two passes.
  terraform -chdir=.openvidu/digitalocean init -input=false -no-color -force-copy
  terraform -chdir=.openvidu/digitalocean destroy -auto-approve -input=false -no-color
  env AWS_ACCESS_KEY_ID=$SPACES_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY=$SPACES_SECRET_ACCESS_KEY AWS_SESSION_TOKEN= aws s3 rm s3://openvidu-ce12d2-space-dae2e06c8c --recursive --endpoint-url https://ams3.digitaloceanspaces.com
  terraform -chdir=.openvidu/digitalocean destroy -auto-approve -input=false -no-color

--delete-data: the recordings and Meet data are in the Spaces: this deletes them.

▶ Delete the machines on DigitalOcean…
   · destroy .openvidu/digitalocean (this returns when Terraform is done)
   · empty the Space openvidu-ce12d2-space-dae2e06c8c so it can be deleted
   · destroy .openvidu/digitalocean (this returns when Terraform is done)
   ✓ Delete the machines on DigitalOcean
✔ removed stack "ce12d2" from this directory
```

With `--delete-data` the Space the template created goes with the stack: the destroy empties it and Terraform deletes it. With `--keep-data` the Space leaves the Terraform state first, so one destroy takes the rest and the Space stays, with the recordings, Meet data and this deployment's `secrets.env`. A Space of your own (`--param spaceName=<name>`) stays either way. `--keep-infrastructure` tears the deployment down but leaves the Droplet running (and says so, because it is still costing money). More options in [Destroy](../operate/destroy.md).

!!! warning "The Space is the secret store"

    DigitalOcean has no managed secret store, so the stack's own Space holds both the recordings and `secrets.env` (the URLs and credentials). The Space is created without `force_destroy`, so `--delete-data` empties it in an explicit, separate step before deleting; `--keep-data` leaves it, `secrets.env` and recordings and all. Keep the Spaces keys available whenever you operate the stack.

## Next steps

- [Check the status](../operate/status.md) of the stack and run its health check.
- [Change its configuration](../operate/configuration.md) or [its modules](../operate/modules.md).
- [Operate it from another machine](../operate/remote.md), with `--remote-state`.
