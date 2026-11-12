---
title: "Upgrade OpenVidu High Availability on Oracle Cloud"
description: "Update an OpenVidu High Availability stack on Oracle Cloud to a new version with ov stack update, keeping its configuration and data."
---

# Upgrade OpenVidu High Availability: Oracle Cloud Infrastructure

--8<-- "self-hosting/oracle/provider-chip.md"

An Oracle Cloud High Availability stack is updated with the OpenVidu CLI, from the directory that deployed it, the same way as any other PRO stack. The update changes OpenVidu, not the machines: the four masters, the media nodes, their size and their count stay as they are.

## Update the stack { #update-the-stack }

--8<-- "self-hosting/common/ov-update-pro.md"

## A deployment from the 3.9.0 cloud templates { #a-deployment-from-the-390-cloud-templates }

--8<-- "self-hosting/common/ov-upgrade-cloud-templates.md"

## Next steps { #next-steps }

- [Administer the stack](./admin.md): change a parameter, scale the media nodes, operate it from another machine, destroy it.
