---
title: "Administer OpenVidu Single Node on Google Cloud"
description: "Administer OpenVidu Single Node on Google Cloud from the directory that deployed it: change a parameter, operate it remotely and destroy it."
---

# OpenVidu Single Node administration: Google Cloud Platform

<div class="provider-chip" markdown>

:material-google-cloud:{ .provider-chip-icon } Google Cloud Platform

</div>

The sections up to [Export the desired state](#export) are the operations every OpenVidu stack shares, with the same commands wherever it runs. The rest of the page is specific to a Single Node stack on Google Cloud.

--8<-- "self-hosting/common/ov-operate.md"

## Change a parameter of the stack { #change-a-parameter-of-the-stack }

`ov stack deploy <name> --cloud gcp --param Name=Value` in the stack's directory runs `terraform apply` again with the parameters that changed. Any parameter the template declares can be set this way. For example, the instance type:

```bash
ov stack deploy openvidu --cloud gcp --param instanceType=e2-standard-8 --mode auto -y
```

A new machine type is an update in place: the instance carries `allow_stopping_for_update`, so Google Cloud stops the machine for a few minutes and starts it with the new type. A change to what the machine **boots with** is different: a `--param` of its first-boot data (such as `domainName` or `certificateType`) or another OpenVidu CLI build makes Terraform recreate the machine from scratch, so what is on its disk is lost and OpenVidu is down until it installs again (the static address stays, so the public IP does not change). On a stack that already exists, auto mode runs `terraform plan` first (it changes nothing), and the plan says which of the two it is — it prints `REPLACES the machine` for a recreate — before asking to go ahead. Run `--mode assisted` to read Terraform's plan yourself first. The settings a redeploy gives (`--domain-name`, `--certificate-type` and the own certificate, the license, any other friendly flag, `--set` and `--set-secret`) never reach the template: `ov` applies them in the running stack, as `ov stack config set` does, and the machine is not touched.

For OpenVidu's own settings, which change without touching the machine, see [Changing configuration](../../configuration/changing-config.md).

## Operate from another machine { #operate-from-another-machine }

--8<-- "self-hosting/gcp/ov-remote.md"

## Destroy the stack { #destroy-the-stack }

--8<-- "self-hosting/gcp/ov-destroy.md"

## Backup and restore { #backup-and-restore }

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
