---
title: "Deploy OpenVidu on Azure with the OpenVidu CLI"
description: "Create the virtual machines and deploy OpenVidu COMMUNITY or PRO on Azure with one command of the OpenVidu CLI, then operate and destroy the stack."
page_features: [lazyvideo]
---

# Deploy OpenVidu on Azure with the OpenVidu CLI

<div class="provider-chip" markdown>

:material-microsoft-azure:{ .provider-chip-icon } Azure

</div>

One command creates the machines and OpenVidu comes up on them. `ov` renders the Bicep template embedded in its own binary for the edition and topology you ask for, applies it with **your own `az` CLI** (which compiles the Bicep), and the machines deploy OpenVidu themselves with the same `ov` build. When OpenVidu answers, `ov` registers the stack in your directory, and you operate it from there.

<a class="glightbox" href="/assets/videos/platform/self-hosting/openvidu-cli/deploy-azure-ce.mp4" data-type="video"><video class="round-corners lazy-video" src="/assets/videos/platform/self-hosting/openvidu-cli/deploy-azure-ce.mp4" preload="none" muted playsinline loop></video></a>

The video shows a Single Node COMMUNITY deploy from an empty directory to `ov stack destroy`.

## Requirements

- The [OpenVidu CLI](../install.md).
- An Azure subscription and the [`az` CLI :fontawesome-solid-external-link:{.external-link-icon}](https://learn.microsoft.com/cli/azure/install-azure-cli){:target="_blank"}, **authenticated**: `az account show` must answer. `ov` runs your own client, so your login, subscription and audit trail are the ones that apply. `az` compiles the Bicep itself, so no separate Bicep install is needed.
- A location: `--azure-location`, else `$AZURE_LOCATION`. The resource group defaults to `openvidu-<name>-rg`, or `ov-<name>-rg` when the name is long (see [Names may be shortened](#destroy-the-stack)); `--azure-resource-group` names your own. With the name `openvidu` of these examples, the group is `ov-openvidu-rg` and the Key Vault `ov-openvidu-keyvault`.
- Permission to create resource groups and everything in them: virtual machines, a static public IP, a network security group, a Storage Account with a Blob container, a Key Vault, and for Elastic and High Availability a load balancer and a scale set of media nodes.
- **Quota for the VM size.** The template's default size is `Standard_D4s_v3` (4 vCPU, Standard DSv3 family). A low family quota in a location limits how many of these stacks run at once; raise it, or pick a smaller size with `--param instanceType=<size>`.
- For OpenVidu PRO, your **license** (`--openvidu-pro-license`). The deploy checks it is there before it touches your subscription.

You need no key pair and no domain: the deploy generates an SSH key pair for the stack, and without `--domain-name` the stack derives a `sslip.io` name from its public IP (on High Availability, from the load balancer's), so Let's Encrypt has a name to certify on Single Node and Elastic. Use your own domain for anything real.

## Deploy

An empty directory is the stack. Choose the edition and topology. The commands name the stack `openvidu`; the outputs come from real runs of stacks with other names.

=== "Single Node **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud azure --azure-location northeurope \
      --certificate-type letsencrypt --mode auto
    ```

    One virtual machine (`Standard_D4s_v3` by default, `--param instanceType=<size>` to change it) running OpenVidu on Docker Compose.

=== "Single Node **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud azure --azure-location northeurope \
      --edition pro --openvidu-pro-license <your-license> \
      --certificate-type letsencrypt --mode auto
    ```

    One virtual machine running OpenVidu PRO on Kubernetes. `--param kubeApiAllowedCidr=<cidr>` limits who can reach the cluster API on port 6443, which gives full control of the stack: do not leave it open to `0.0.0.0/0` on a production stack.

    This is how the deploy of a stack named `dpaz1` ends: `ov` waits until the stack publishes its kubeconfig and the cluster answers, then registers it:

    ```text
    …
       · OpenVidu is up: the stack published its kubeconfig and the cluster API answers at 104.41.221.2:6443
    …
    ✔ OpenVidu Pro (single node) is up on Azure
      URL:          https://openvidu-j064da-104-41-221-2.sslip.io/
      credentials:  az keyvault secret show --vault-name openvidu-dpaz1-keyvault --name OPENVIDU-URL --query value -o tsv
      kubeconfig:   .openvidu/azure/kubeconfig.yaml
    ```

=== "Elastic **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud azure --azure-location northeurope \
      --edition pro --openvidu-pro-license <your-license> --deployment-type elastic \
      --certificate-type letsencrypt --mode auto
    ```

    One master node and a scale set of media nodes. The media nodes scale between `minNumberOfMediaNodes` and `maxNumberOfMediaNodes` (`--param`), or, at the first deploy, `--set infrastructure.mediaNodes.fixedCount=N` runs exactly N of them. To change the count later, see [Scaling](../operate/scaling.md).

    This is how the deploy of a stack named `dpaz2` ends: `ov` waits until the stack publishes its kubeconfig and the cluster answers, then registers it:

    ```text
    …
       · OpenVidu is up: the stack published its kubeconfig and the cluster API answers at 52.138.152.30:6443
    …
    ✔ OpenVidu Pro (elastic) is up on Azure
      URL:          https://openvidu-i4mxo8-52-138-152-30.sslip.io/
      credentials:  az keyvault secret show --vault-name openvidu-dpaz2-keyvault --name OPENVIDU-URL --query value -o tsv
      kubeconfig:   .openvidu/azure/kubeconfig.yaml
    ```

=== "High Availability **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    <a class="glightbox" href="/assets/videos/platform/self-hosting/openvidu-cli/deploy-azure-ha.mp4" data-type="video"><video class="round-corners lazy-video" src="/assets/videos/platform/self-hosting/openvidu-cli/deploy-azure-ha.mp4" preload="none" muted playsinline loop></video></a>

    ```bash
    mkdir openvidu && cd openvidu
    ov stack deploy openvidu --cloud azure --azure-location northeurope \
      --edition pro --openvidu-pro-license <your-license> --deployment-type ha \
      --mode auto
    ```

    Four master nodes behind a passthrough load balancer, plus a scale set of media nodes.

    The load balancer passes TLS through untouched, and Caddy on the masters terminates it with the certificate type you choose:

    - **`selfsigned`**, the default on High Availability: a certificate the four masters share. Browsers warn about it, so it is for trying the topology out.
    - **`owncert`**, for production: your own certificate for your domain, base64-encoded. Add these flags to the command above:

        ```bash
        --domain-name openvidu.example.com --certificate-type owncert \
          --owncert-public-key "$(base64 -w0 fullchain.pem)" \
          --owncert-private-key "$(base64 -w0 privkey.pem)"
        ```

        On a cloud the certificate travels as a template parameter, so pass its content, base64-encoded as above, not the path to the file.

    Let's Encrypt and ZeroSSL do **not** work on this topology: their HTTP challenge reaches a port 80 that only redirects to HTTPS, so the certificate is never issued and `ov stack status --wait` times out. Without `--domain-name` the stack answers at a `sslip.io` name derived from the load balancer's address; with your own domain, point it at that address (the deployment's `publicIp` output: `az deployment group show --resource-group <group> --name <deployment> --query properties.outputs.publicIp.value -o tsv`, with the group and deployment names the plan printed). Do it as soon as the deploy ends: `ov stack status --wait` waits until the stack answers at its domain (`URL not answering yet` until then).

    Five machines take more vCPU quota than the default sizes of a single node: the run below passed `--param masterNodeInstanceType=Standard_D2s_v3 --param mediaNodeInstanceType=Standard_F4s_v2` to fit the location's quota.

    This is how the deploy of a stack named `demo-ha` ends, followed by `ov stack status --wait` confirming that every node and service is ready:

    ```text
    …
    ✔ OpenVidu Pro (high availability) is up on Azure
      URL:          https://openvidu-zksfiv-20-107-185-207.sslip.io/
      credentials:  az keyvault secret show --vault-name ov-demo-ha-keyvault --name OPENVIDU-URL --query value -o tsv
      kubeconfig:   .openvidu/azure/kubeconfig.yaml

    $ ov stack status --wait
    waiting for https://openvidu-zksfiv-20-107-185-207.sslip.io to be ready (Ctrl-C to stop)…
    ✔ demo-ha is ready (https://openvidu-zksfiv-20-107-185-207.sslip.io)
    ```

Before it touches your subscription, the deploy prints exactly what it will run and asks for confirmation (`-y` answers it in advance; the list is still printed). This is the output of a Single Node COMMUNITY deploy of a stack named `ce12a` (northeurope, 2026-10-29):

```text
This is what will be done in your Azure subscription (location northeurope):

  # SSH access: the key pair for this stack, its public half handed to the template.
  #   .openvidu/azure/openvidu-ce12a-key.pub
  # The template, rendered from the one embedded in this CLI for the single node topology,
  # written out for you to read (az compiles the Bicep itself):
  #   .openvidu/azure/cf-openvidu-singlenode.bicep
  az group create --name openvidu-ce12a-rg --location northeurope --only-show-errors -o none
  # Create the machine. deployedBy=instance: it installs OpenVidu on itself with the
  # OpenVidu CLI. The command returns when Azure is done (about 4 minutes); OpenVidu comes up after.
  az deployment group create --resource-group openvidu-ce12a-rg --name openvidu-ce12a --template-file .openvidu/azure/cf-openvidu-singlenode.bicep --only-show-errors --query properties.provisioningState -o tsv --parameters certificateType=letsencrypt deployedBy=instance … stackName=openvidu-ce12a 'publicIpAddressObject={"newOrExistingOrNone":"new","name":"openvidu-ce12a-pip"}' adminSshKey="{\"sshPublicKey\":\"$(cat .openvidu/azure/openvidu-ce12a-key.pub)\"}"

  # What the stack published: URL and credentials, as secrets in the Key Vault the deployment outputs (OPENVIDU_URL appears once
  # OpenVidu serves: until then this read fails, and the command that continues the deploy waits for it).
  az deployment group show --resource-group openvidu-ce12a-rg --name openvidu-ce12a --query properties.outputs -o json
  KV="$(az deployment group show --resource-group openvidu-ce12a-rg --name openvidu-ce12a --query properties.outputs.sharedInfoKeyVault.value -o tsv)"
  az keyvault secret show --vault-name $KV --name OPENVIDU-URL --query value -o tsv
```

Azure takes its parameters inline on the `az deployment group create` line; there is no separate parameters file. Then it runs them, waits for OpenVidu and registers the stack. The `az deployment group create` returns in about four minutes — once Azure has provisioned the VM, but before OpenVidu is installed — so the wait is the real one: `ov` polls the Key Vault for the stack's `OPENVIDU-URL` secret, then checks the published URL answers Caddy's health check:

```text
▶ Create the machines on Azure…
   · create the resource group openvidu-ce12a-rg in northeurope
   · create the machines from .openvidu/azure/cf-openvidu-singlenode.bicep (this returns when Azure is done)
note: recorded this stack's infrastructure in openvidu-stack.yml, so `ov stack destroy` removes it even if the wait below fails
   ✓ Create the machines on Azure

▶ Wait for the machines to deploy OpenVidu…
   · waiting for OpenVidu to come up (2s elapsed): the published values are not readable yet: no secret exists in openvidu-ce12a-keyvault yet
   · waiting for OpenVidu to come up (1m11s elapsed): the stack has not published its URL yet (OpenVidu is still installing)
   …
   · OpenVidu is up: the stack published its URL and https://openvidu-zclupo-40-112-77-3.sslip.io/health/caddy answers 200
   ✓ Wait for the machines to deploy OpenVidu

▶ Register the stack…

Stack described by the deployment:
  name         ce12a
  deployment   single_node · azure · community
  version      ov-admin
  modules      dashboard, egress, ingress, meet, observability
  dashboard    https://openvidu-zclupo-40-112-77-3.sslip.io
  nodes        40.112.77.3
  published    by ov/ov-admin on 2026-10-29 16:37 UTC (generation 1)

note: this stack was deployed on the machine itself, so its desired state named 127.0.0.1; retargeted at 40.112.77.3, the host this import reached
✔ registered stack "ce12a" in /home/me/ce12a
   ✓ Register the stack

✔ OpenVidu Community (single node) is up on Azure
  URL:          https://openvidu-zclupo-40-112-77-3.sslip.io/
  credentials:  az keyvault secret show --vault-name openvidu-ce12a-keyvault --name OPENVIDU-URL --query value -o tsv
  SSH:          ubuntu@40.112.77.3 (key .openvidu/azure/openvidu-ce12a-key.pem)

Try it:
  ov stack status
  ov stack logs --tail 50
```

The `retargeted` note is expected: the machine deployed OpenVidu on itself, and `ov` points your directory at its public address. The VM gets the template's size, `Standard_D4s_v3`, and a 100 GB OS disk unless you pass `--param instanceType=<size>`. A low quota for the VM's family limits how many stacks run in a location at once.

## What the deploy creates

| Resource | Notes |
| --- | --- |
| A resource group, `openvidu-<name>-rg` | Holds everything the stack is; `--azure-resource-group` names it; tagged `created-by=openvidu-cli` |
| Virtual machines | One for Single Node; master nodes and a scale set of media nodes for Elastic and High Availability |
| A static public IP and a network security group | The ports OpenVidu needs, open to the internet |
| A load balancer | High Availability only |
| A Storage Account and a Blob container (`openvidu-appdata`) | Recordings and OpenVidu Meet data. `--param storageAccountName=<name>` uses your own |
| A Key Vault, `openvidu-<name>-keyvault` | What the stack publishes: URL and credentials (and the kubeconfig on PRO) |
| An SSH key pair | `ov` generates it; the private half stays in `.openvidu/azure/` |

`ov` writes the stack's infrastructure into `openvidu-stack.yml` **before** creating it, so `ov stack destroy` in the directory removes whatever a failed deploy left behind.

## Access OpenVidu

The deploy prints the URL of the deployment. OpenVidu Meet answers at `/`, and OpenVidu Dashboard at `/dashboard/`, with the Let's Encrypt certificate of the Single Node example:

```console
$ D=openvidu-zclupo-40-112-77-3.sslip.io
$ curl -s -o /dev/null -w "meet %{http_code}\n" https://$D/
meet 302
$ curl -s -o /dev/null -w "dashboard %{http_code}\n" https://$D/dashboard/
dashboard 200
```

The credentials are secrets in the stack's Key Vault, the command printed on the `credentials:` line. These are the keys of a Single Node COMMUNITY stack (values replaced by their length; the storage account's key masked too):

```text
vault openvidu-ce12a-keyvault
AZURE-STORAGE-ACCOUNT-KEY      <set, 88 chars>
AZURE-STORAGE-ACCOUNT-NAME     ovdatammuudi34y26y2
AZURE-STORAGE-CONTAINER-NAME   openvidu-appdata
DASHBOARD-ADMIN-PASSWORD       <set, 44 chars>
DASHBOARD-ADMIN-USERNAME       dashboardadmin
DASHBOARD-URL                  https://openvidu-zclupo-40-112-77-3.sslip.io/dashboard/
DOMAIN-NAME                    openvidu-zclupo-40-112-77-3.sslip.io
ENABLED-MODULES                egress,ingress,dashboard,meet,observability
LIVEKIT-API-KEY                <set, 15 chars>
LIVEKIT-API-SECRET             <set, 44 chars>
LIVEKIT-URL                    wss://openvidu-zclupo-40-112-77-3.sslip.io/
OPENVIDU-URL                   https://openvidu-zclupo-40-112-77-3.sslip.io/
…
```

`ov stack config get <key>` reads any of them from the running stack. The secret is a copy made at the deploy: after a later `ov stack config set`, the stack's configuration is the truth (the node's files on Community, `openvidu.yaml` in the cluster on PRO), not the copy.

Your applications connect with the values of `LIVEKIT-URL`, `LIVEKIT-API-KEY` and `LIVEKIT-API-SECRET` (`LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` in your application's environment), as with any other OpenVidu deployment. Key Vault does not allow `_` in a secret name, so the keys use `-`.

To look inside a machine, use the key pair the deploy generated (the `SSH:` line). The login user is `ubuntu`, and the node has `ov` too, so `sudo ov stack …` there operates the same stack:

```bash
ssh -i .openvidu/azure/openvidu-ce12a-key.pem ubuntu@40.112.77.3
```

## Review the commands first: assisted mode

`--mode assisted` runs **nothing at all** in your subscription. It writes the rendered template into `.openvidu/azure/` and prints the same commands, for you to read, change and run yourself:

```bash
ov stack deploy openvidu --cloud azure --azure-location northeurope \
  --certificate-type letsencrypt --mode assisted
```

It ends with the command that continues the deploy once you have run them. This is the end for Community, which reads the stack from the machine over SSH:

```text
Nothing above has been run. Run it yourself, then continue the deploy — naming
the resource group is enough, this CLI reads everything else back from it:

  ov stack deploy --cloud azure --mode auto

From there the deploy waits for OpenVidu to come up, reads the stack from the machine
over SSH (as `ov stack import --ssh` does) with the key pair above, and registers
this directory as the stack, exactly as it would have done here.
```

That command needs no flags: the desired state and every parameter are already in `openvidu-stack.yml`, and a deployment that already succeeded is **reused**, not created again.

On OpenVidu PRO the plan also writes the license into a `0600` parameters file (`.openvidu/azure/secure-parameters.json`) instead of the command line, and the continuation reads the kubeconfig the stack published instead of using SSH. The end of a PRO Single Node plan (stack `dpaz0`):

```text
  ov stack deploy --cloud azure --mode auto

From there the deploy waits for OpenVidu to come up, reads the kubeconfig the stack
published and registers this directory as the stack, exactly as it would have done here.
```

Until you continue, the directory holds the plan but no stack: `ov stack status` answers `no stack in this directory` (exit `3`).

## Change a parameter of the stack

`ov stack deploy <name> --cloud azure --param Name=Value` in the stack's directory runs the deployment again with the parameters that changed. Any parameter the template declares can be set this way. For example, the maximum number of media nodes of an Elastic stack:

```bash
ov stack deploy openvidu --cloud azure --param maxNumberOfMediaNodes=3 --mode auto -y
```

See [Scaling](../operate/scaling.md) for media nodes and [Configuration](../operate/configuration.md) for OpenVidu's own settings, which change without touching the machines.

## Destroy the stack

One command deletes the machines too. You must say what happens to the recordings and OpenVidu Meet data: `--keep-data` leaves them, `--delete-data` deletes them. The whole stack is one resource group, so deleting it is the teardown:

```console
$ ov stack destroy -y --delete-data
This is what will be deleted from your Azure subscription:

  # The resource group, which holds everything the stack is: machines, disks, network,
  # load balancer, Key Vault and storage account.
  az group delete --name openvidu-ce12a-rg --yes --only-show-errors

--delete-data: the recordings and Meet data are in the storage account: this deletes them.

▶ Delete the machines on Azure…
   · delete the resource group openvidu-ce12a-rg (this returns when Azure is done)
   ✓ Delete the machines on Azure
✔ removed stack "ce12a" from this directory
```

With `--delete-data` the storage account goes with the resource group, recordings and all. With `--keep-data` the account first moves to a resource group of its own, `<group>-data`, so deleting the stack's group leaves it. `--keep-infrastructure` tears the deployment down but leaves the VM running (and says so, because it is still costing money). More options in [Destroy](../operate/destroy.md).

!!! warning "Names may be shortened"

    A Key Vault name may be at most 24 characters, so when `openvidu-<name>-keyvault` would exceed it, `ov` shortens the prefix from `openvidu-` to `ov-` (resource group `ov-<name>-rg`, Key Vault `ov-<name>-keyvault`). Take the stack's cloud name from the `record:` line the deploy prints; it is what `ov stack import --cloud azure --stack-name <name>` needs.

## Next steps

- [Check the status](../operate/status.md) of the stack and run its health check.
- [Change its configuration](../operate/configuration.md) or [its modules](../operate/modules.md).
- [Operate it from another machine](../operate/remote.md), with `--remote-state`.
