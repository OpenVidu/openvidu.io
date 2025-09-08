---
description: Discover OpenVidu deployment options. Local setup for development, single node for medium load, elastic scalability and high availability clusters.
---

# Deployment types

OpenVidu offers **user-friendly installers** that facilitate quick **on-premises deployments**, so you can self-host your real-time solution in your own infrastructure or any cloud provider.

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

## Node services

OpenVidu is composed of several services that work together to provide a complete videoconferencing solution. Every service runs as a Docker container, coordinated with Docker Compose.

### Master Node services

| SERVICE                | DESCRIPTION |
| :--------------------- | :---------- |
| **[OpenVidu Meet](../../meet/index.md)**      | A high-quality video calling service based on OpenVidu. |
| **OpenVidu Dashboard** | Web application interface for managing your cluster and visualizing your Rooms. |
| **OpenVidu Operator**  | Module that supervises the high availability services and updates the loadbalancing configuration dynamically. |
| **Redis**              | Database used to share transient information between Media Nodes and coordinate them. In [OpenVidu High Availability](#openvidu-high-availability) this is an instance of a [Redis Cluster :fontawesome-solid-external-link:{.external-link-icon}](https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/){:target=_blank}. |
| **MongoDB**            | Database used to store analytics and monitoring persistent data. In [OpenVidu High Availability](#openvidu-high-availability) this is an instance of a [MongoDB Replica Set :fontawesome-solid-external-link:{.external-link-icon}](https://www.mongodb.com/docs/manual/replication/){:target=_blank}. |
| **Minio**              | S3 bucket used to store recordings and common node configurations. In [OpenVidu High Availability](#openvidu-high-availability) this is an instance of a [Minio Multi-Node :fontawesome-solid-external-link:{.external-link-icon}](https://min.io/docs/minio/linux/operations/install-deploy-manage/deploy-minio-multi-node-multi-drive.html#){:target=_blank}. |
| **Caddy**              | Reverse proxy used as a loadbalancer to distribute client connections across your nodes and automatically manage your TLS certificate. |
| **Mimir (observability)**    | Module used to store metrics from Prometheus. |
| **Promtail (observability)** | Module used to collect logs from all services and send them to Loki. |
| **Loki (observability)**     | Module used to store logs. |
| **Grafana (observability)**  | Module used to visualize logs and metrics in dashboards. |

### Media Node services

| SERVICE             | DESCRIPTION |
| :------------------ | :---------- |
| **OpenVidu Server** | Media server used to stream real-time video, audio and data. Based on SFUs LiveKit and mediasoup. |
| **Egress Server**   | Module used to export media from a Room (for example, recordings or RTMP broadcasting). See [Egress :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/home/egress/overview/){:target=_blank}. |
| **Ingress Server**  | Module used to import media into a Room (for example, an MP4 video or an RTSP stream). See [Ingress :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/home/ingress/overview/){:target=_blank}. |
| **Agents**          | Modules used to add AI capabilities to Rooms. See [AI Services](../ai/overview.md). |
| **Caddy**           | Reverse proxy used as a loadbalancer to distribute the load generated by the Media Nodes over the Minio, Mimir and Loki cluster. |
| **Prometheus (observability)** | Module used to collect metrics from OpenVidu Server and send them to Loki. |
| **Promtail (observability)**   | Module used to collect logs from all services and send them to Loki. |
