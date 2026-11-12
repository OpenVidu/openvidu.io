---
title: "Administer OpenVidu Single Node on DigitalOcean"
description: "Operate an OpenVidu Single Node DigitalOcean stack with the CLI: change a parameter, run it from another machine, and destroy it."
---

# OpenVidu Single Node administration: DigitalOcean

<div class="provider-chip" markdown>

:material-digital-ocean:{ .provider-chip-icon } DigitalOcean

</div>

The stack is operated from the directory that deployed it, with the same `ov stack` commands as any other OpenVidu deployment. The canonical operations page covers them all: [status](../on-premises/admin.md#status), [describe](../on-premises/admin.md#describe), the [health test](../on-premises/admin.md#health-test), [logs](../on-premises/admin.md#logs) and [start, stop and restart](../on-premises/admin.md#start-stop-and-restart). Its [configuration](../../configuration/changing-config.md) and its [modules](../../how-to-guides/enable-disable-modules.md) are changed the same way as anywhere else.

This page covers only what is specific to DigitalOcean.

## Change a parameter of the stack

`ov stack deploy <name> --cloud digitalocean --param Name=Value` in the stack's directory runs `terraform apply` again with the parameters that changed. Any parameter the template declares can be set this way. Always name the stack in a redeploy: without the name it is registered again as `openvidu`.

The most common change is the Droplet size:

```bash
ov stack deploy openvidu --cloud digitalocean --param instanceType=s-8vcpu-16gb --mode auto -y
```

Before asking to go ahead, the redeploy reads Terraform's plan and says what it does. A new size is resized in place, with the Droplet powered off for a few minutes (none can move to a size with a smaller disk). A change to what the Droplet boots with (the domain, the certificate, the license, the Meet credentials, another OpenVidu CLI) creates it again from scratch, with a new public IP, so a domain pointed at it has to be pointed again; the plan says `REPLACES the Droplet`.

For OpenVidu's own settings, which change without touching the machine, see [Changing configuration](../../configuration/changing-config.md).

## Operate from another machine

--8<-- "self-hosting/digitalocean/ov-remote.md"

## Destroy the stack

--8<-- "self-hosting/digitalocean/ov-destroy.md"

## Backup and restore

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
