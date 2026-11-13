---
title: "Administer OpenVidu Single Node on Azure"
description: "Administer an OpenVidu Single Node stack on Azure with the CLI: change a template parameter, operate it from another machine, and destroy it."
---

# OpenVidu Single Node administration: Azure

<div class="provider-chip" markdown>

:material-microsoft-azure:{ .provider-chip-icon } Azure

</div>

The sections up to [Export the desired state](#export) are the operations every OpenVidu stack shares, with the same commands wherever it runs. The rest of the page is specific to a Single Node stack on Azure.

--8<-- "self-hosting/common/ov-operate.md"

## Change a parameter of the stack

`ov stack deploy openvidu --cloud azure --param Name=Value` in the stack's directory runs the deployment again with only the parameters that changed; a redeploy with the same parameters reuses the stack as it is. Any parameter the template declares can be set this way, for example the VM size:

```bash
ov stack deploy openvidu --cloud azure --param instanceType=Standard_D8s_v3 --mode auto -y
```

See [Changing configuration](../../configuration/changing-config.md) for OpenVidu's own settings, which change without touching the machine. The settings a redeploy gives as flags (`--domain-name`, `--certificate-type`, the license, `--set`) are applied the same way, in the running stack.

## Operate from another machine

--8<-- "self-hosting/azure/ov-remote.md"

## Destroy the stack

--8<-- "self-hosting/azure/ov-destroy.md"

## Backup and restore

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
