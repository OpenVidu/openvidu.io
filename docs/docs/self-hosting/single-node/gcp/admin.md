---
title: "Administer OpenVidu Single Node on Google Cloud"
description: "Administer OpenVidu Single Node on Google Cloud from the directory that deployed it: change a parameter, operate it remotely and destroy it."
---

# OpenVidu Single Node administration: Google Cloud Platform

<div class="provider-chip" markdown>

:material-google-cloud:{ .provider-chip-icon } Google Cloud Platform

</div>

A Google Cloud stack is operated from the directory that deployed it, with the same commands as any other OpenVidu stack. The canonical operations are documented once, on the On Premises page:

- [Status](../on-premises/admin.md#status), [describe](../on-premises/admin.md#describe), [health test](../on-premises/admin.md#health-test) and [logs](../on-premises/admin.md#logs).
- [Start, stop and restart](../on-premises/admin.md#start-stop-and-restart).
- [Change the configuration](../../configuration/changing-config.md) of OpenVidu and [enable or disable modules](../../how-to-guides/enable-disable-modules.md), which change without touching the machine.

This page covers what is specific to a Google Cloud stack.

## Change a parameter of the stack { #change-a-parameter-of-the-stack }

`ov stack deploy <name> --cloud gcp --param Name=Value` in the stack's directory runs `terraform apply` again with the parameters that changed. Any parameter the template declares can be set this way. For example, the instance type:

```bash
ov stack deploy openvidu --cloud gcp --param instanceType=e2-standard-8 --mode auto -y
```

A new machine type is an update in place: the instance carries `allow_stopping_for_update`, so Google Cloud stops the machine for a few minutes and starts it with the new type. On a stack that already exists, auto mode runs `terraform plan` first (it changes nothing) and the plan says what it found before asking to go ahead.

For OpenVidu's own settings, which change without touching the machine, see [Changing configuration](../../configuration/changing-config.md).

## Operate from another machine { #operate-from-another-machine }

--8<-- "self-hosting/gcp/ov-remote.md"

## Destroy the stack { #destroy-the-stack }

--8<-- "self-hosting/gcp/ov-destroy.md"

## Backup and restore { #backup-and-restore }

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
