---
title: "Administer OpenVidu Single Node on Oracle Cloud"
description: "Operate an OpenVidu Single Node stack on Oracle Cloud with the OpenVidu CLI: change a parameter, run it from another machine and destroy it."
---

# OpenVidu Single Node administration: Oracle Cloud Infrastructure

--8<-- "self-hosting/oracle/provider-chip.md"

The sections up to [Export the desired state](#export) are the operations every OpenVidu stack shares, with the same commands wherever it runs. The rest of the page is specific to a Single Node stack on Oracle Cloud.

--8<-- "self-hosting/common/ov-operate.md"

## Change a parameter of the stack { #change-a-parameter-of-the-stack }

Any parameter the Oracle template declares is changed from the stack's directory with `ov stack deploy <name> --cloud oracle --param Name=Value`, which runs `terraform apply` again with the parameters that changed. For example, to resize the instance, change its shape (and, on a Flex shape, its OCPUs and memory):

```bash
ov stack deploy openvidu --cloud oracle --param instanceType=VM.Standard.E4.Flex \
  --param instanceOCPUs=4 --param instanceMemory=16 --mode auto -y
```

A redeploy reads Terraform's plan first: a change to the instance's shape, OCPUs or memory restarts it in place, while a change to what it boots with (a `--param` of its first-boot data, such as `domainName` or `certificateType`, or a newer OpenVidu CLI) recreates it from scratch, and it comes back with a new public IP, so a domain pointed at it must be pointed again. The plan says which before you answer. The settings a redeploy gives (`--domain-name`, `--certificate-type` and the own certificate, the license, any other friendly flag, `--set` and `--set-secret`) never reach the template: `ov` applies them in the running stack, as `ov stack config set` does, and the machine is not touched.

To change OpenVidu's own settings without touching the machine, use [its configuration](../../configuration/changing-config.md#view-get-set-unset), not a redeploy.

## Operate from another machine { #operate-from-another-machine }

--8<-- "self-hosting/oracle/ov-remote.md"

## Destroy the stack { #destroy-the-stack }

--8<-- "self-hosting/oracle/ov-destroy.md"

## Backup and restore { #backup-and-restore }

--8<-- "self-hosting/oracle/backup-and-restore.md"
