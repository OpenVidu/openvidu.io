---
title: "Deploy OpenVidu on Oracle Cloud with the OpenVidu CLI"
description: "Create the compute instances and deploy OpenVidu COMMUNITY or PRO on Oracle Cloud with one command of the OpenVidu CLI, then operate and destroy the stack."
page_features: [lazyvideo]
---

# Deploy OpenVidu on Oracle Cloud with the OpenVidu CLI

--8<-- "self-hosting/oracle/provider-chip.md"

One command creates the machines and OpenVidu comes up on them. `ov` renders the Terraform module embedded in its own binary for the edition and topology you ask for, applies it with **your own `terraform` and OCI API key**, and the machines deploy OpenVidu themselves with the same `ov` build. When OpenVidu answers, `ov` registers the stack in your directory, and you operate it from there.

<a class="glightbox" href="/assets/videos/platform/self-hosting/openvidu-cli/deploy-oracle-ce.mp4" data-type="video"><video class="round-corners lazy-video" src="/assets/videos/platform/self-hosting/openvidu-cli/deploy-oracle-ce.mp4" preload="none" muted playsinline loop></video></a>

The video shows a Single Node COMMUNITY deploy from an empty directory to `ov stack destroy`.

## Requirements

- The [OpenVidu CLI](../install.md).
- An Oracle Cloud tenancy and [**Terraform** :fontawesome-solid-external-link:{.external-link-icon}](https://developer.hashicorp.com/terraform/install){:target="_blank"} on your PATH: `ov` drives your own Terraform, so the provider plugins, the state and the audit trail are the ones that apply. With `--remote-state` the `oci` backend needs Terraform **1.12.0 or later**.
- Your **OCI API key** configured (`~/.oci/config`), which Terraform and the `oci` reads use.
- The tenancy, compartment and user OCIDs (`--oci-tenancy` / `--oci-compartment` / `--oci-user`, else `$OCI_TENANCY_OCID` / `$OCI_COMPARTMENT_OCID` / `$OCI_USER_OCID`) and a region (`--oci-region`, else `$OCI_REGION`, else your `oci` configuration's).
- Permission to create compute instances, a virtual cloud network with a subnet and network security group, an Object Storage bucket, a Customer Secret Key and (unless `--oci-vault`) a KMS vault for the stack's secrets.
- **One Customer Secret Key per stack.** The template mints a Customer Secret Key for the instance to reach Object Storage over its S3-compatible API. OCI caps Customer Secret Keys at **2 per user**, so at most two of these stacks run under one user at a time.
- For OpenVidu PRO, your **license** (`--openvidu-pro-license`). The deploy checks it is there before it touches your tenancy.

You need no key pair and no domain: the template generates an SSH key pair for the stack, and without `--domain-name` the stack derives a `sslip.io` name from its public IP (on High Availability, from the load balancer's), so Let's Encrypt has a name to certify on Single Node and Elastic. Use your own domain for anything real.

## Deploy

An empty directory is the stack. Choose the edition and topology:

=== "Single Node **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud oracle --oci-region eu-madrid-1 \
      --oci-vault ocid1.vault.oc1.eu-madrid-1.<vault> \
      --certificate-type letsencrypt --mode auto
    ```

    One compute instance (`VM.Standard.E4.Flex` with 4 OCPUs and 8 GB by default, `--param instanceType=<shape>` to change it) running OpenVidu on Docker Compose.

=== "Single Node **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud oracle --oci-region eu-madrid-1 \
      --oci-vault ocid1.vault.oc1.eu-madrid-1.<vault> \
      --edition pro --openvidu-pro-license <your-license> \
      --certificate-type letsencrypt --mode auto
    ```

    One compute instance running OpenVidu PRO on Kubernetes. `--param kubeAPIAllowedCidr=<cidr>` limits who can reach the cluster API on port 6443, which gives full control of the stack: do not leave it open to `0.0.0.0/0` on a production stack.

    This is how the deploy of a stack named `dpoci1` ends: `ov` waits until the stack publishes its kubeconfig and the cluster answers, then registers it:

    ```text
    …
       · OpenVidu is up: the stack published its kubeconfig and the cluster API answers at 51.170.35.19:6443
    …
    ✔ OpenVidu Pro (single node) is up on Oracle Cloud
      URL:          https://openvidu-9ox1vk-51-170-35-19.sslip.io/
      credentials:  oci secrets secret-bundle get-secret-bundle-by-name --secret-name OPENVIDU_URL --vault-id ocid1.vault.oc1.eu-madrid-1.<vault> --query 'data."secret-bundle-content".content' --raw-output --region eu-madrid-1 | base64 -d
      kubeconfig:   .openvidu/oracle/kubeconfig.yaml
    ```

=== "Elastic **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud oracle --oci-region eu-madrid-1 \
      --oci-vault ocid1.vault.oc1.eu-madrid-1.<vault> \
      --edition pro --openvidu-pro-license <your-license> --deployment-type elastic \
      --certificate-type letsencrypt --mode auto
    ```

    One master node and an autoscaling pool of media nodes. The media nodes scale between `minNumberOfMediaNodes` and `maxNumberOfMediaNodes` (`--param`), or `--set infrastructure.mediaNodes.fixedCount=N` runs exactly N of them.

    This is how the deploy of a stack named `dpoci2` ends: `ov` waits until the stack publishes its kubeconfig and the cluster answers, then registers it:

    ```text
    …
       · OpenVidu is up: the stack published its kubeconfig and the cluster API answers at 51.170.59.236:6443
    …
    ✔ OpenVidu Pro (elastic) is up on Oracle Cloud
      URL:          https://openvidu-m3l4vn-51-170-59-236.sslip.io/
      credentials:  oci secrets secret-bundle get-secret-bundle-by-name --secret-name OPENVIDU_URL --vault-id ocid1.vault.oc1.eu-madrid-1.<vault> --query 'data."secret-bundle-content".content' --raw-output --region eu-madrid-1 | base64 -d
      kubeconfig:   .openvidu/oracle/kubeconfig.yaml
    ```

=== "High Availability **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    <a class="glightbox" href="/assets/videos/platform/self-hosting/openvidu-cli/deploy-oracle-ha.mp4" data-type="video"><video class="round-corners lazy-video" src="/assets/videos/platform/self-hosting/openvidu-cli/deploy-oracle-ha.mp4" preload="none" muted playsinline loop></video></a>

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud oracle --oci-region eu-madrid-1 \
      --oci-vault ocid1.vault.oc1.eu-madrid-1.<vault> \
      --edition pro --openvidu-pro-license <your-license> --deployment-type ha \
      --mode auto
    ```

    Four master nodes behind a passthrough network load balancer, plus an autoscaling pool of media nodes.

    The load balancer passes TLS through untouched, and Caddy on the masters terminates it with the certificate type you choose:

    - **`selfsigned`**, the default on High Availability: a certificate the four masters share. Browsers warn about it, so it is for trying the topology out.
    - **`owncert`**, for production: your own certificate for your domain, base64-encoded. Add these flags to the command above:

        ```bash
        --domain-name openvidu.example.com --certificate-type owncert \
          --owncert-public-key "$(base64 -w0 fullchain.pem)" \
          --owncert-private-key "$(base64 -w0 privkey.pem)"
        ```

    Let's Encrypt and ZeroSSL do **not** work on this topology: their HTTP challenge reaches a port 80 that only redirects to HTTPS, so the certificate is never issued and `ov stack status --wait` times out. Without `--domain-name` the stack answers at a `sslip.io` name derived from the load balancer's address; with your own domain, point it at that address (the `nlb_public_ip` output of `terraform -chdir=.openvidu/oracle output`). Do it as soon as the deploy ends: `ov stack status --wait` waits until the stack answers at its domain (`URL not answering yet` until then).

    This is how the deploy of a stack named `demo-ha` ends, followed by `ov stack status --wait` confirming that every node and service is ready:

    ```text
    …
    ✔ OpenVidu Pro (high availability) is up on Oracle Cloud
      URL:          https://openvidu-qbgqz3-51-170-44-98.sslip.io/
      credentials:  oci secrets secret-bundle get-secret-bundle-by-name --secret-name OPENVIDU_URL --vault-id ocid1.vault.oc1.eu-madrid-1.<vault> --query 'data."secret-bundle-content".content' --raw-output --region eu-madrid-1 | base64 -d
      kubeconfig:   .openvidu/oracle/kubeconfig.yaml

    $ ov stack status --wait
    waiting for https://openvidu-qbgqz3-51-170-44-98.sslip.io to be ready (Ctrl-C to stop)…
      ⏳ master nodes 4/4, media nodes 1/1, services 41/49 (0s)
      ⏳ master nodes 4/4, media nodes 1/1, services 42/49 (2s)
      ⏳ master nodes 4/4, media nodes 1/1, services 44/49 (8s)
      ⏳ master nodes 4/4, media nodes 1/1, services 46/49 (10s)
      ⏳ master nodes 4/4, media nodes 1/1, services 47/49 (13s)
      ⏳ master nodes 4/4, media nodes 1/1, services 48/49 (17s)
    ✔ demo-ha is ready (https://openvidu-qbgqz3-51-170-44-98.sslip.io)
    ```

Before it touches your tenancy, the deploy prints exactly what it will run and asks for confirmation (`-y` answers it in advance; the list is still printed). This is the output of a Single Node COMMUNITY deploy of a stack named `ce12o` (eu-madrid-1, 2026-10-29, OCIDs and the Object Storage namespace shown as placeholders):

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

Then it runs them, waits for OpenVidu and registers the stack. The `apply` returns in about three minutes — before OpenVidu is installed — so the wait is the real one: `ov` polls the vault for the stack's `OPENVIDU_URL` secret and checks the published URL answers Caddy's health check:

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

The instance gets the template's shape, `VM.Standard.E4.Flex` with 4 OCPUs and 8 GB, and a 100 GB boot volume, unless you pass `--param instanceType=<shape>`.

## What the deploy creates

| Resource | Notes |
| --- | --- |
| Compute instances | One for Single Node; master nodes and an autoscaling pool of media nodes for Elastic and High Availability |
| A virtual cloud network, subnet and network security group | The ports OpenVidu needs, open to the internet |
| A load balancer | High Availability only |
| An Object Storage bucket and a Customer Secret Key | Recordings and OpenVidu Meet data, reached over the S3-compatible API. `--param bucketName=<name>` uses your own |
| A KMS vault, one secret per key | What the stack publishes: URL and credentials (and the kubeconfig on PRO). `--oci-vault` reuses one; else one vault per stack |
| An SSH key pair | The template generates it; `ov` keeps the private half in `.openvidu/oracle/` |

`ov` writes the stack's infrastructure into `openvidu-stack.yml` **before** creating it, so `ov stack destroy` in the directory removes whatever a failed deploy left behind.

## Access OpenVidu

The deploy prints the URL of the deployment. OpenVidu Meet answers at `/`, and OpenVidu Dashboard at `/dashboard/`, with the Let's Encrypt certificate of the Single Node example:

```console
$ D=openvidu-u57z2l-51-170-56-241.sslip.io
$ curl -s -o /dev/null -w "meet %{http_code}\n" https://$D/
meet 302
$ curl -s -o /dev/null -w "dashboard %{http_code}\n" https://$D/dashboard/
dashboard 200
```

The credentials are secrets in the stack's vault, base64-encoded, the command printed on the `credentials:` line. These are the keys of a Single Node COMMUNITY stack (values replaced by their length):

```text
DASHBOARD_ADMIN_PASSWORD       <set, 44 chars>
DASHBOARD_ADMIN_USERNAME       dashboardadmin
DASHBOARD_URL                  https://openvidu-u57z2l-51-170-56-241.sslip.io/dashboard/
DOMAIN_NAME                    openvidu-u57z2l-51-170-56-241.sslip.io
ENABLED_MODULES                egress,ingress,dashboard,meet,observability
EXTERNAL_S3_ACCESS_KEY         <set, 40 chars>
EXTERNAL_S3_ENDPOINT           https://<namespace>.compat.objectstorage.eu-madrid-1.oraclecloud.com
EXTERNAL_S3_SECRET_KEY         <set, 44 chars>
LIVEKIT_API_KEY                <set, 15 chars>
LIVEKIT_API_SECRET             <set, 44 chars>
LIVEKIT_URL                    wss://openvidu-u57z2l-51-170-56-241.sslip.io/
OPENVIDU_URL                   https://openvidu-u57z2l-51-170-56-241.sslip.io/
S3_APP_DATA_BUCKET             openvidu-ce12o-appdata-9f79dd
…
```

`ov stack config get <key>` reads any of them from the running stack. The secret is a copy made at the deploy: after a later `ov stack config set`, the node's files are the truth, not the vault.

Your applications connect with `LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`, as with any other OpenVidu deployment.

To look inside a machine, use the key pair the deploy generated (the `SSH:` line). The login user is `ubuntu`, and the node has `ov` too, so `sudo ov stack …` there operates the same stack:

```bash
ssh -i .openvidu/oracle/openvidu-ce12o-key.pem ubuntu@51.170.56.241
```

## Review the commands first: assisted mode

`--mode assisted` runs **nothing at all** in your tenancy. It writes the rendered template and its variables into `.openvidu/oracle/` and prints the same commands, for you to read, change and run yourself:

```bash
ov stack deploy openvidu --cloud oracle --oci-region eu-madrid-1 \
  --oci-vault ocid1.vault.oc1.eu-madrid-1.<vault> \
  --certificate-type letsencrypt --mode assisted
```

It ends with the command that continues the deploy once you have run them. This is the end for Community, which reads the stack from the machine over SSH:

```text
Nothing above has been run. Run it yourself, then continue the deploy — the Terraform
state and this directory's record are enough, this CLI reads everything else back:

  ov stack deploy --cloud oracle --mode auto

From there the deploy waits for OpenVidu to come up, reads the stack from the machine
over SSH (as `ov stack import --ssh` does) with the key the template generated (its private key output), and registers
this directory as the stack, exactly as it would have done here.
```

On OpenVidu PRO the continuation reads the kubeconfig the stack published instead of using SSH. That command needs no flags: the Terraform state and every parameter are already in place, and `terraform apply` is idempotent, so a resume applies the same state again (a no-op that refreshes the outputs) and then waits for OpenVidu.

## Change a parameter of the stack

`ov stack deploy <name> --cloud oracle --param Name=Value` in the stack's directory runs `terraform apply` again with the parameters that changed. Any parameter the template declares can be set this way. For example, the maximum number of media nodes of an Elastic stack:

```bash
ov stack deploy openvidu --cloud oracle --param maxNumberOfMediaNodes=3 --mode auto -y
```

Name the stack (`openvidu` in these examples), or the redeploy registers it under the default name. See [Scaling](../operate/scaling.md) for media nodes and [Configuration](../operate/configuration.md) for OpenVidu's own settings, which change without touching the machines.

## Destroy the stack

One command deletes the machines too. You must say what happens to the recordings and OpenVidu Meet data: `--keep-data` leaves the bucket, `--delete-data` deletes it:

```console
$ ov stack destroy -y --delete-data
This is what will be deleted from your Oracle Cloud tenancy (compartment ocid1.compartment.oc1..<compartment>):

  # Everything the Terraform state in .openvidu/oracle holds: the instances, the network, the
  # vault and its secrets (a vault stays pending deletion for the period Oracle imposes).
  terraform -chdir=.openvidu/oracle init -input=false -no-color -force-copy
  terraform -chdir=.openvidu/oracle destroy -auto-approve -input=false -no-color

--delete-data: the recordings and Meet data are in the Object Storage buckets: this deletes them.

▶ Delete the machines on Oracle Cloud…
   · destroy .openvidu/oracle (this returns when Terraform is done)
   ✓ Delete the machines on Oracle Cloud
✔ removed stack "ce12o" from this directory
```

`--delete-data` empties and deletes the Object Storage bucket the template created, recordings and all; `--keep-data` takes it out of the Terraform state first, so the destroy leaves it and names it. A bucket of your own (`--param bucketName=<name>`) stays either way. A vault the template created (no `--oci-vault`) is not deleted immediately: OCI schedules it for deletion after a waiting period of at least 7 days. `--keep-infrastructure` tears the deployment down but leaves the instance running (and says so, because it is still costing money). More options in [Destroy](../operate/destroy.md).

!!! warning "Vaults and Customer Secret Keys"

    Without `--oci-vault`, the template creates one KMS vault per stack, and OCI only deletes a vault after a waiting period of at least 7 days. Reuse one with `--oci-vault <ocid>`, but never share a vault between two live stacks: the secrets have fixed names inside the vault and the second would overwrite the first's. OCI also caps Customer Secret Keys at 2 per user, and each stack mints one, so at most two of these stacks run under one user at a time.

## Next steps

- [Check the status](../operate/status.md) of the stack and run its health check.
- [Change its configuration](../operate/configuration.md) or [its modules](../operate/modules.md).
- [Operate it from another machine](../operate/remote.md), with `--remote-state`.
