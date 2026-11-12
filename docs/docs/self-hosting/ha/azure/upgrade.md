---
title: "Upgrade OpenVidu High Availability on Azure"
description: "Upgrade an existing OpenVidu High Availability deployment on Azure to a newer OpenVidu version, keeping its configuration and data."
---

# Upgrade OpenVidu High Availability: Azure

<div class="provider-chip" markdown>

:material-microsoft-azure:{ .provider-chip-icon } Azure

</div>

An OpenVidu High Availability stack on Azure is an OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag } stack. It is updated from the directory that operates it with `ov stack update`, exactly as any other PRO stack: the update changes OpenVidu on the four master nodes and the media nodes, and leaves the machines, their sizes and the number of media nodes as they are.

## Update the stack

--8<-- "self-hosting/common/ov-update-pro.md"

<!-- PENDING(docs-integrate): upgrade path for deployments created from the 3.9.0 cloud templates (waiting for Carlos) -->

Once the stack is updated, go on operating it from its [Administration](./admin.md) page.
