---
title: "Upgrade OpenVidu High Availability on AWS"
description: "Upgrade an OpenVidu High Availability AWS stack to a newer OpenVidu version with the OpenVidu CLI, keeping its configuration and data."
---

# Upgrade OpenVidu High Availability: AWS

<div class="provider-chip" markdown>

:material-aws:{ .provider-chip-icon } AWS

</div>

An OpenVidu High Availability stack deployed on AWS with the OpenVidu CLI is upgraded from its own directory, with `ov stack update`. The update changes OpenVidu on the running machines and keeps the stack's configuration and data.

## Update the stack

--8<-- "self-hosting/common/ov-update-pro.md"

## A deployment from the 3.9.0 cloud templates { #a-deployment-from-the-390-cloud-templates }

--8<-- "self-hosting/common/ov-upgrade-cloud-templates.md"

## Next steps

- [Administer the stack](./admin.md): scale the media nodes, change its configuration and destroy it.
