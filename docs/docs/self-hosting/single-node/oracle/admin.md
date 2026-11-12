---
title: "Administer OpenVidu Single Node on Oracle Cloud"
description: "Operate an OpenVidu Single Node stack on Oracle Cloud with the OpenVidu CLI: change a parameter, run it from another machine and destroy it."
---

# OpenVidu Single Node administration: Oracle Cloud Infrastructure

--8<-- "self-hosting/oracle/provider-chip.md"

An Oracle Cloud Single Node stack is operated from the directory that deployed it, with the same commands as any other stack. The canonical operations page documents them all:

- [Status](../on-premises/admin.md#status), [describe](../on-premises/admin.md#describe), the [health test](../on-premises/admin.md#health-test) and the [logs](../on-premises/admin.md#logs).
- [Start, stop and restart](../on-premises/admin.md#start-stop-and-restart).
- [Change its configuration](../../configuration/changing-config.md#view-get-set-unset) and [enable or disable modules](../../how-to-guides/enable-disable-modules.md#modules-and-services).

What follows is specific to an Oracle Cloud deployment.

## Change a parameter of the stack { #change-a-parameter-of-the-stack }

Any parameter the Oracle template declares is changed from the stack's directory with `ov stack deploy <name> --cloud oracle --param Name=Value`, which runs `terraform apply` again with the parameters that changed. For example, to resize the instance, change its shape (and, on a Flex shape, its OCPUs and memory):

```bash
ov stack deploy openvidu --cloud oracle --param instanceType=VM.Standard.E4.Flex \
  --param instanceOCPUs=4 --param instanceMemory=16 --mode auto -y
```

A redeploy reads Terraform's plan first: a change to the instance's shape, OCPUs or memory restarts it in place, while a change to what it boots with (the domain, the certificate, the license, the Meet credentials or a newer OpenVidu CLI) recreates it from scratch, and it comes back with a new public IP, so a domain pointed at it must be pointed again. The plan says which before you answer.

To change OpenVidu's own settings without touching the machine, use [its configuration](../../configuration/changing-config.md#view-get-set-unset), not a redeploy.

## Operate from another machine { #operate-from-another-machine }

--8<-- "self-hosting/oracle/ov-remote.md"

## Destroy the stack { #destroy-the-stack }

--8<-- "self-hosting/oracle/ov-destroy.md"

## Backup and restore { #backup-and-restore }

--8<-- "self-hosting/oracle/backup-and-restore.md"
