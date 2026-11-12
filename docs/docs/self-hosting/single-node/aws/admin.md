---
title: "Administer OpenVidu Single Node on AWS"
description: "Administer an OpenVidu Single Node AWS stack with the OpenVidu CLI: change parameters, operate it remotely and destroy it."
---

# OpenVidu Single Node administration: AWS

<div class="provider-chip" markdown>

:material-aws:{ .provider-chip-icon } AWS

</div>

The AWS stack is operated from the directory that deployed it, with the same `ov stack` commands as any other OpenVidu stack. The canonical operations page documents all of them:

- [Status](../on-premises/admin.md#status), [describe](../on-premises/admin.md#describe) and the [health test](../on-premises/admin.md#health-test).
- [Logs](../on-premises/admin.md#logs) and [ports](../on-premises/admin.md#ports).
- [Start, stop and restart](../on-premises/admin.md#start-stop-and-restart).
- [Change its configuration](../../configuration/changing-config.md) and [enable or disable its modules](../../how-to-guides/enable-disable-modules.md).

This page covers only what is specific to AWS.

## Change a parameter of the stack

`ov stack deploy <name> --cloud aws --param Name=Value` in the stack's directory updates the CloudFormation stack with the parameters that changed. Any parameter the template declares can be set this way. For a Single Node stack, the instance size is the `InstanceType` parameter:

```bash
ov stack deploy openvidu --cloud aws --param InstanceType=c6a.2xlarge --mode auto -y
```

The stack that exists is updated with the parameters that changed; a redeploy with the same parameters reuses it as it is. For OpenVidu's own settings, which change without touching the machine, see [Changing configuration](../../configuration/changing-config.md).

## Operate from another machine

--8<-- "self-hosting/aws/ov-remote.md"

## Destroy the stack

--8<-- "self-hosting/aws/ov-destroy.md"

## Backup and restore

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
