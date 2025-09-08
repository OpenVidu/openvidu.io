---
description: Discover OpenVidu deployment options. Local setup for development, single node for medium load, elastic scalability and high availability clusters.
---

# Deployment types

OpenVidu Meet offers **user-friendly installers** that facilitate quick **on-premises deployments**, so you can self-host your real-time solution in your own infrastructure or any cloud provider.

There are different deployment options available, depending on your needs:

| Type of deployment        | <a href="#openvidu-local-development"><strong>OpenVidu<br><span class="no-break">Local (development)</span></strong>         | <div style="width:10em"><a href="#openvidu-single-node"><strong>OpenVidu<br><span class="no-break">Single Node</span></strong></a></div> | <a href="#openvidu-elastic"><strong>OpenVidu<br><span class="no-break">Elastic</span></strong></a> | <a href="#openvidu-high-availability"><strong>OpenVidu<br><span class="no-break">High Availability</span></strong></a> |
| ------------------------- | ------------------------------------ | -------------------- | ---------------- | -------------------------- |
| **OpenVidu Edition**          | <span class="openvidu-tag openvidu-community-tag">COMMUNITY</span> <span class="openvidu-tag openvidu-pro-tag">PRO</span> | <span class="openvidu-tag openvidu-community-tag">COMMUNITY</span> <span class="openvidu-tag openvidu-pro-tag">PRO</span> | <span class="openvidu-tag openvidu-pro-tag">PRO</span> | <span class="openvidu-tag openvidu-pro-tag">PRO</span> |
| **Suitability**               | For local development in your laptop | For applications with medium user load | For applications with dynamic user load that require scalability | For applications where both scalability and fault tolerance are critical |
| **Features**                  | Friendly Docker Compose setup with Redis, Egress, Ingress, S3 storage and observability. With automatic certificate management to test across devices in your network | <span class="openvidu-tag openvidu-community-tag">COMMUNITY</span> Custom LiveKit distribution with Redis, Egress, Ingress, S3 storage and observability.<br><br><span class="openvidu-tag openvidu-pro-tag">PRO</span> Same features but adding **2x performance** and **advanced observability**. | Same benefits as OpenVidu Single Node plus **2x performance**, **advanced observability** and **scalability** | Same benefits as OpenVidu Elastic plus **fault tolerance** |
| **Number of servers**         | Your laptop | 1 Node | 1 Master Node +<br><span class="no-break">N Media Nodes</span> | 4 Master Nodes +<br><span class="no-break">N Media Nodes</span> |
| **Installation instructions** | [Install](./local.md){ .md-button } | [Install](./single-node/index.md){ .md-button } | [Install](./elastic/index.md){ .md-button } | [Install](./ha/index.md){ .md-button } |

<br>

--8<-- "shared/self-hosting/deployment-types.md"
