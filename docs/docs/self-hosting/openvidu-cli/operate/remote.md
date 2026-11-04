---
title: "Operate an OpenVidu stack from another machine"
description: "Adopt a running OpenVidu stack into a new directory with ov stack import, over SSH, a kubeconfig or its cloud record kept by remote state."
---

# Operate from another machine

`ov` operates one stack per directory. To operate a running stack from a machine that has no directory for it (a colleague's laptop, a CI runner, a replacement for a lost directory), use **`ov stack import`**. It reads the description the stack publishes about itself and writes the two files a deploy would have left (`openvidu-stack.yml` and the `.openvidu/` state), so every `ov stack` verb works afterwards.

## Import a stack

| Source | What it adopts |
| --- | --- |
| `--this-node` | The stack running on **this machine** (reads its published description; escalates with `sudo` for root-only files). |
| `--ssh [user@]host` | A node over **SSH** (with `--ssh-key`, `--ssh-port`). |
| `--kubeconfig <path>` | A **PRO** stack, from the cluster credential. The stack holds its own desired state, so nothing has to have been published. |
| `-f <file>` | A description document you already have. |
| `--cloud <cloud> --stack-name <name>` | A stack deployed with `--remote-state`, from the **record** it keeps on the cloud, infrastructure included. |

Over SSH, `ov` shows what it found and asks before saving (the document names hosts your client would connect to); `-y` answers in advance:

```console
$ mkdir -p ~/stacks/web && cd ~/stacks/web
$ ov stack import web --ssh ubuntu@172.30.0.96 --ssh-key ~/.ssh/id_ed25519 -y

Stack described by the deployment:
  name         web
  deployment   single_node · on-premises · community
  version      ov-admin
  dashboard    https://172-30-0-96.openvidu-local.dev
  nodes        172.30.0.96
  published    by ov/ov-admin on 2026-10-29 14:41 UTC (generation 1)

✔ imported stack "web" into /home/me/stacks/web
  desired state: /home/me/stacks/web/openvidu-stack.yml

Try it:
  ov stack status
  ov stack logs --tail 50
```

If the node has lost its desired state, the import rebuilds it from the files `ov` deployed under `/opt/openvidu` and says so (`note: the stack published no desired state; rebuilt it from the files …`).

## One administrator or a team: COMMUNITY and PRO

The import behaves differently per edition, because the two store their configuration in different places (see [Configuration](configuration.md#where-the-configuration-lives)).

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    The configuration lives in the node's files, and each client holds a **copy** in its own `openvidu-stack.yml`. `config get` and `config view` read the node, so a change another client made is what you see next time you ask. `config set` also adopts the node's values into your own spec, with a note (`openvidu-stack.yml now follows the node for: …`). `ov stack plan`, on the other hand, compares your spec with the node: a value another client changed shows as a change your redeploy would undo.

    What can go stale is a client's `openvidu-stack.yml` between commands. The public IP and the owncert files another client set are never read back, because they live in that client's spec, not in a file of the node. The copy matters for a **redeploy**, which renders the tree from the spec. Before one, `ov stack plan` shows whether your copy differs from the node, and `ov stack import --ssh … --replace` refreshes it.

    In short, a Community deployment is a **single-administrator** product: comfortable for one person or one pipeline, workable for a few who coordinate.

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    The stack holds its own desired state, so two clients **cannot drift apart**: both read and write the same release, and `ov stack config view` always answers from it. Any administrator with credentials points a directory at the stack and operates it: a **team** product. A lost directory is reconstructed from the deployment itself (`--kubeconfig`, or `sudo ov stack import --this-node` on the node), never stale.

## Recover a cloud stack, infrastructure included

`--kubeconfig` adopts the cluster but not the machines under it: that directory can operate OpenVidu, not delete its cloud resources or change its template parameters. By default the stack's directory is the only place that drives the machines, and if it is lost, it is lost.

A deploy with **`--remote-state`** also keeps the stack on its cloud, so another machine can take it over completely. It prints where on its last lines (an Elastic stack named `dpaws2`):

```console
✔ OpenVidu Pro (elastic) is up on AWS
  URL:          https://openvidu-239b62-51-95-197-8.sslip.io/
  credentials:  aws secretsmanager get-secret-value --secret-id openvidu-elastic-eu-south-2-openvidu-dpaws2 --query SecretString --output text --region eu-south-2
  kubeconfig:   .openvidu/aws/kubeconfig.yaml
  record:       s3://openvidu-cfn-templates-123456789012-eu-south-2/openvidu-dpaws2/registry/openvidu-stack.yml (from another machine: ov stack import --cloud aws --stack-name openvidu-dpaws2)
  SSH key:      Secrets Manager secret openvidu/openvidu-dpaws2/ssh-private-key (the private half, for that import)
```

From an empty directory on another machine, `ov stack import --cloud` reads that record and registers the stack. `--stack-name` takes the stack's name **on the cloud**, exactly as the `record:` line prints it: `openvidu-<name>` for a stack deployed as `<name>`, not the name of its directory. The record never holds a secret, so a parameter the template marks sensitive, the license above all, is passed again, exactly as the deploy took it:

```console
$ mkdir -p ~/stacks/dpaws2 && cd ~/stacks/dpaws2
$ ov stack import --cloud aws --aws-region eu-south-2 --stack-name openvidu-dpaws2 --openvidu-pro-license <license> -y
This is what will be read from AWS to import the stack openvidu-dpaws2 (nothing there is changed):
…
▶ Read the stack's record from AWS…
   ✓ Read the stack's record from AWS

▶ Write this directory's copy…
   ✓ Write this directory's copy

▶ Read what the stack published…
   ✓ Read what the stack published

▶ Register the stack…

Stack described by the deployment:
  name         dpaws2
  deployment   elastic · aws · pro
  version      ov-admin
  modules      dashboard, egress, ingress, meet, observability
  dashboard    https://openvidu-239b62-51-95-197-8.sslip.io
  published    by ov-deployer/ov-admin (from the Helm release) on 2026-11-04 03:43 UTC (generation 1)

✔ registered stack "dpaws2" in /home/me/stacks/dpaws2
   ✓ Register the stack

✔ imported the AWS stack openvidu-dpaws2 (elastic) into /home/me/stacks/dpaws2
  URL:          https://openvidu-239b62-51-95-197-8.sslip.io/
  kubeconfig:   .openvidu/aws/kubeconfig.yaml
  SSH key:      both halves, the private one from the stack's secret store on the cloud.

From here, as from the directory that deployed it:
  ov stack status
  ov stack deploy --cloud aws --param Name=Value   # change a template parameter
  ov stack destroy --keep-data   # or --delete-data: what becomes of the recordings
```

From then on, `ov stack status`, `ov stack deploy <name> --cloud … --param …` (with the stack's name, `dpaws2` here) and `ov stack destroy` work here as they did in the directory that deployed the stack (a destroy from the imported directory deletes the machines too). Without `--openvidu-pro-license` the import stops before registering anything and says which flag is missing; `--mode assisted` prints the reads and runs nothing. A stack deployed **without** `--remote-state` has no record to read: the way back is its deploying directory, or `--kubeconfig` for the cluster alone.

### What `--remote-state` stores per cloud

Everything that drives the stack, kept where the stack's infrastructure already lives, so another machine with that cloud's credentials can take it over:

| Where it is kept | AWS | Azure | Google Cloud, Oracle, DigitalOcean |
| --- | --- | --- | --- |
| **Terraform state** | (CloudFormation; no state file) | (Bicep; no state file) | a bucket of the stack's own (`<stack>-terraform-state`) |
| **The record** (infrastructure, no secrets) | the template bucket (`<stack>/registry/`) | a Key Vault secret (`OPENVIDU-REGISTRY`) | the state bucket (`openvidu/registry/`) |
| **The SSH private key** `ov` generated | a Secrets Manager secret (`openvidu/<stack>/ssh-private-key`) | the stack's Key Vault (`OPENVIDU-SSH-PRIVATE-KEY`) | in the Terraform state |

All of it is deleted by `ov stack destroy`.

## Next steps

- [Destroy](destroy.md) a stack, including the `--remote-state` cleanup.
- [Update and migrate](update.md).
- The full [command reference](../reference.md).
