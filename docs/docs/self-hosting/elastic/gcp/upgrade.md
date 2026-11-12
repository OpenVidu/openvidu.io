---
title: "Upgrade OpenVidu Elastic on Google Cloud"
description: "Upgrade an existing OpenVidu Elastic deployment on Google Cloud to a newer OpenVidu version, keeping its configuration and its data."
---

# Upgrade OpenVidu Elastic: Google Cloud Platform

<div class="provider-chip" markdown>

:material-google-cloud:{ .provider-chip-icon } Google Cloud Platform

</div>

An Elastic stack on Google Cloud is upgraded from the directory that deployed it, with `ov stack update`. The update changes OpenVidu on the machines that are already running; it does not recreate the infrastructure.

## Update the stack { #update-the-stack }

--8<-- "self-hosting/common/ov-update-pro.md"

<!-- PENDING(docs-integrate): upgrade path for deployments created from the 3.9.0 cloud templates (waiting for Carlos) -->

## Next steps { #next-steps }

- [Administer the stack](./admin.md): change a parameter, scale the media nodes, operate it from another machine and destroy it.
