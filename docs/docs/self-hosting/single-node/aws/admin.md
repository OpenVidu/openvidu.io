---
title: "Administer OpenVidu Single Node on AWS"
description: "Administer an OpenVidu Single Node AWS stack with the OpenVidu CLI: change parameters, operate it remotely and destroy it."
---

# OpenVidu Single Node administration: AWS

<div class="provider-chip" markdown>

:material-aws:{ .provider-chip-icon } AWS

</div>

The sections up to [Export the desired state](#export) are the operations every OpenVidu stack shares, with the same commands wherever it runs. The rest of the page is specific to a Single Node stack on AWS.

--8<-- "self-hosting/common/ov-operate.md"

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
