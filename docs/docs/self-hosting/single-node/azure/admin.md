---
title: "Administer OpenVidu Single Node on Azure"
description: "Administer an OpenVidu Single Node stack on Azure with the CLI: change a template parameter, operate it from another machine, and destroy it."
---

# OpenVidu Single Node administration: Azure

<div class="provider-chip" markdown>

:material-microsoft-azure:{ .provider-chip-icon } Azure

</div>

The Azure stack is operated from the directory that deployed it, with the same `ov stack` commands as any other OpenVidu stack. The day-to-day operations are documented once, for an on-premises deployment, and apply here unchanged:

- [Status](../on-premises/admin.md#status), [describe](../on-premises/admin.md#describe) and the [health test](../on-premises/admin.md#health-test).
- [Logs](../on-premises/admin.md#logs), and [start, stop and restart](../on-premises/admin.md#start-stop-and-restart).
- [Change its configuration](../../configuration/changing-config.md) and [enable or disable modules](../../how-to-guides/enable-disable-modules.md).

## Change a parameter of the stack

`ov stack deploy openvidu --cloud azure --param Name=Value` in the stack's directory runs the deployment again with only the parameters that changed; a redeploy with the same parameters reuses the stack as it is. Any parameter the template declares can be set this way, for example the VM size:

```bash
ov stack deploy openvidu --cloud azure --param instanceType=Standard_D8s_v3 --mode auto -y
```

See [Changing configuration](../../configuration/changing-config.md) for OpenVidu's own settings, which change without touching the machine.

## Operate from another machine

--8<-- "self-hosting/azure/ov-remote.md"

## Destroy the stack

--8<-- "self-hosting/azure/ov-destroy.md"

## Backup and restore

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
