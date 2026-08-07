---
title: "Upgrade OpenVidu Single Node PRO"
description: "Upgrade an OpenVidu Single Node PRO deployment to a newer version, in place with the updater or by redeploying your cloud template."
---

# Upgrade OpenVidu Single Node <span class="openvidu-tag openvidu-pro-tag" style="font-size: .6em; vertical-align: text-bottom">PRO</span>

There are two ways to upgrade an OpenVidu Single Node PRO deployment:

- **Redeploying** your cloud provider's template with the new version. This is what we recommend when you deployed OpenVidu from one of our templates. See [Redeploying from your cloud template](#redeploying-from-your-cloud-template).
- **Upgrading in place** with OpenVidu's updater, which keeps your configuration and data. This is the only option for on-premises deployments, and it also works on every cloud provider. See [Upgrading OpenVidu Single Node](#upgrading-openvidu-single-node).

## Redeploying from your cloud template

| Provider | Redeploy with the latest version |
| -------- | -------------------------------- |
| :material-aws:{ .provider-chip-icon } **AWS** | [OpenVidu Single Node PRO CloudFormation](./aws/install.md) |
| :material-microsoft-azure:{ .provider-chip-icon } **Azure** | [OpenVidu Single Node PRO Azure](./azure/install.md) |
| :material-google-cloud:{ .provider-chip-icon } **Google Cloud** | [OpenVidu Single Node PRO Google Cloud Platform](./gcp/install.md) |
| :material-digital-ocean:{ .provider-chip-icon } **DigitalOcean** | [OpenVidu Single Node PRO DigitalOcean](./digitalocean/install.md) |
| :custom-oracle-cloud-infrastructure:{ .provider-chip-icon } **Oracle Cloud** | [OpenVidu Single Node PRO Oracle Cloud Infrastructure](./oracle/install.md) |

If you prefer not to redeploy, the in-place procedure below works on all of these providers too.

--8<-- "shared/self-hosting/on-premises/single-node/upgrade.md"
