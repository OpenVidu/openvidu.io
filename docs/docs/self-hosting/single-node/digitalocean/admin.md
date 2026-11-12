---
title: "Administer OpenVidu Single Node on DigitalOcean"
description: "Operate an OpenVidu Single Node DigitalOcean stack with the CLI: change a parameter, run it from another machine, and destroy it."
---

# OpenVidu Single Node administration: DigitalOcean

<div class="provider-chip" markdown>

:material-digital-ocean:{ .provider-chip-icon } DigitalOcean

</div>

The sections up to [Export the desired state](#export) are the operations every OpenVidu stack shares, with the same commands wherever it runs. The rest of the page is specific to a Single Node stack on DigitalOcean.

--8<-- "self-hosting/common/ov-operate.md"

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
