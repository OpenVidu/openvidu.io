---
title: "Upgrade OpenVidu Elastic on Oracle Cloud"
description: "Update an OpenVidu Elastic stack on Oracle Cloud to a new version with ov stack update, keeping its configuration and data."
---

# Upgrade OpenVidu Elastic: Oracle Cloud Infrastructure

--8<-- "self-hosting/oracle/provider-chip.md"

An Oracle Cloud Elastic stack is updated with the OpenVidu CLI, from the directory that deployed it, the same way as any other PRO stack. The update changes OpenVidu, not the machines: the nodes, their size and the number of media nodes stay as they are.

## Update the stack { #update-the-stack }

--8<-- "self-hosting/common/ov-update-pro.md"

<!-- PENDING(docs-integrate): upgrade path for deployments created from the 3.9.0 cloud templates (waiting for Carlos) -->

## Next steps { #next-steps }

- [Administer the stack](./admin.md): change a parameter, scale the media nodes, operate it from another machine, destroy it.
