---
title: "Upgrade OpenVidu Elastic on DigitalOcean"
description: "Update an OpenVidu Elastic deployment on DigitalOcean to a newer version with the OpenVidu CLI, keeping its configuration and data."
---

# Upgrade OpenVidu Elastic: DigitalOcean

<div class="provider-chip" markdown>

:material-digital-ocean:{ .provider-chip-icon } DigitalOcean

</div>

An OpenVidu Elastic stack on DigitalOcean is a PRO stack, operated from the directory that deployed it. You update it with the OpenVidu CLI, in place, keeping its configuration and data.

## Update the stack

--8<-- "self-hosting/common/ov-update-pro.md"

<!-- PENDING(docs-integrate): upgrade path for deployments created from the 3.9.0 cloud templates (waiting for Carlos) -->

Once the update finishes, operate the stack as usual from its [administration page](./admin.md).
