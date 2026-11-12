---
title: "Upgrade OpenVidu Elastic on AWS"
description: "Upgrade an OpenVidu Elastic AWS stack to a newer OpenVidu version with the OpenVidu CLI, keeping its configuration and data."
---

# Upgrade OpenVidu Elastic: AWS

<div class="provider-chip" markdown>

:material-aws:{ .provider-chip-icon } AWS

</div>

An OpenVidu Elastic stack deployed on AWS with the OpenVidu CLI is upgraded from its own directory, with `ov stack update`. The update changes OpenVidu on the running machines and keeps the stack's configuration and data.

## Update the stack

--8<-- "self-hosting/common/ov-update-pro.md"

<!-- PENDING(docs-integrate): upgrade path for deployments created from the 3.9.0 cloud templates (waiting for Carlos) -->

## Next steps

- [Administer the stack](./admin.md): scale the media nodes, change its configuration and destroy it.
