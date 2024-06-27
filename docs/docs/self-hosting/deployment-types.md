OpenVidu offers **user-friendly installers** that facilitate quick **on-premises deployments**, so you can self-host your real-time solution in your own infrastructure or any cloud provider.

There are different deployment options available, depending on your needs:

| Type of deployment        | <a href="/docs/self-hosting/deployment-types/#openvidu-local-development"><strong>OpenVidu<br><span class="no-break">Local (development)</span></strong>         | <a href="/docs/self-hosting/deployment-types/#openvidu-single-node"><strong>OpenVidu<br><span class="no-break">Single Node</span></strong></a> | <a href="/docs/self-hosting/deployment-types/#openvidu-elastic"><strong>OpenVidu<br><span class="no-break">Elastic</span></strong></a> | <a href="/docs/self-hosting/deployment-types/#openvidu-high-availability"><strong>OpenVidu<br><span class="no-break">High Availability</span></strong></a> |
| ------------------------- | ------------------------------------ | -------------------- | ---------------- | -------------------------- |
| **OpenVidu Edition**          | <span class="openvidu-tag openvidu-community-tag">COMMUNITY</span> <span class="openvidu-tag openvidu-pro-tag">PRO</span> | <span class="openvidu-tag openvidu-community-tag">COMMUNITY</span> | <span class="openvidu-tag openvidu-pro-tag">PRO</span> | <span class="openvidu-tag openvidu-pro-tag">PRO</span> |
| **Suitability**               | For local development in your laptop | For applications with medium user load | For applications with dynamic user load that require scalability | For applications where both scalability and fault tolerance are critical |
| **Features**                  | Friendly Docker Compose setup with Redis, Egress, Ingress, S3 storage and observability. With automatic certificate management to test across devices in your network | Custom LiveKit distribution with Redis, Egress, Ingress, S3 storage and observability | Same benefits as OpenVidu Single Node plus **2x performance**, **scalability** and **advanced observability** | Same benefits as OpenVidu Single Node and OpenVidu Elastic plus **fault tolerance** |
| **Number of servers**         | Your laptop | 1 Node | 1 Master Node +<br><span class="no-break">N Media Nodes</span> | 4 Master Nodes +<br><span class="no-break">N Media Nodes</span> |
| **Installation instructions** | [Install](../self-hosting/local.md){ .md-button } | [Install](../self-hosting/single-node/index.md){ .md-button } | [Install](../self-hosting/elastic/index.md){ .md-button } | [Install](../self-hosting/ha/index.md){ .md-button } |

<br>

### OpenVidu Local (development)

To run OpenVidu in your local machine, this is the quickest option. It is a Docker Compose setup that includes all the necessary services to run OpenVidu in your LAN, including automated SSL certificates that will be valid across all devices in your network.

<figure markdown>
  ![OpenVidu Single Node](../../assets/images/openvidu-local-architecture.svg){ .svg-img .dark-img }
  <figcaption>OpenVidu Local (development)</figcaption>
</figure>

### OpenVidu Single Node

This is the simplest production-ready OpenVidu deployment available. It provides all the features you need, but lacks scalability and fault tolerance. But make no mistake about it: it is perfectly suitable for medium-scale production deployments. For most projects OpenVidu Single Node will be enough, at least until your user load gets serious. You can host hundreds of simultaneous participants in your rooms by running OpenVidu Community on a sufficiently powerful server!

It is composed of a single OpenVidu Node hosting all the necessary services in a monolithic setup.

<figure markdown>
  ![OpenVidu Single Node](../../assets/images/openvidu-single-node-architecture.svg){ .svg-img .dark-img }
  <figcaption>OpenVidu Single Node</figcaption>
</figure>

### OpenVidu Elastic

This is the intermediate OpenVidu deployment. It provides **scalability** for your video rooms. Suitable for applications with dynamic load in the media plane that require scalability.

It is composed of two different types of nodes, one of them running on a cluster of multiple servers and the other running as a single monolithic server:

- **A cluster of Media Nodes** hosting all the media-related services. Your video rooms scale up and down thanks to this cluster.
- **A single Master Node** hosting all the support services in a monolithic setup.

<figure markdown>
  ![OpenVidu Elastic](../../assets/images/openvidu-elastic-architecture.svg){ .svg-img .dark-img }
  <figcaption>OpenVidu Elastic</figcaption>
</figure>

### OpenVidu High Availability

This is the most complete OpenVidu deployment. It provides **scalability** for your video rooms and **fault tolerance** in all its services. Suitable for applications where both scalability and availability are critical.

It is composed of two different types of nodes running on two separate clusters:

- **A cluster of Media Nodes** hosting all the media-related services. Your video rooms scale up and down thanks to this cluster. The minimum number of nodes in this cluster is **1**, and it is designed to scale up and down dynamically according to workload.
- **A cluster of Master Nodes** hosting all the support services in their high availability format. Your deployment is fault tolerant thanks to this cluster. The minimum number of nodes in this cluster is **4**, and it is designed to have a fixed number of nodes at all times.

<figure markdown>
  ![OpenVidu High Availability cluster](../../assets/images/openvidu-ha-architecture.svg){ .svg-img .dark-img }
  <figcaption>OpenVidu High Availability cluster</figcaption>
</figure>

## Node services

OpenVidu is composed of several services that work together to provide a complete videoconferencing solution. Every service runs as a Docker container, coordinated with Docker Compose.

### Master Node services

| SERVICE                | DESCRIPTION |
| :--------------------- | :---------- |
| **OpenVidu Dashboard** | Web application interface for managing your cluster and visualizing your Rooms. |
| **Default Application (OpenVidu Call)**      | A fully fledged videoconference web application ready to be used out-of-the-box. |
| **OpenVidu Operator**  | Module that supervises the high availability services and updates the loadbalancing configuration dynamically. |
| **Redis**              | Database used to share transient information between Media Nodes and coordinate them. In [OpenVidu High Availability](#openvidu-high-availability) this is an instance of a [Redis Cluster](https://redis.io/docs/management/scaling/){:target=_blank}. |
| **MongoDB**            | Database used to store analytics and monitoring persistent data. In [OpenVidu High Availability](#openvidu-high-availability) this is an instance of a [MongoDB Replica Set](https://www.mongodb.com/docs/manual/replication/){:target=_blank}. |
| **Minio**              | S3 bucket used to store recordings and common node configurations. In [OpenVidu High Availability](#openvidu-high-availability) this is an instance of a [Minio Multi-Node](https://min.io/docs/minio/linux/operations/install-deploy-manage/deploy-minio-multi-node-multi-drive.html#){:target=_blank}. |
| **Caddy**              | Reverse proxy used as a loadbalancer to distribute client connections across your nodes and automatically manage your TLS certificate. |
| **Mimir (observability)**    | Module used to store metrics from Prometheus. |
| **Promtail (observability)** | Module used to collect logs from all services and send them to Loki. |
| **Loki (observability)**     | Module used to store logs. |
| **Grafana (observability)**  | Module used to visualize logs and metrics in dashboards. |

### Media Node services

| SERVICE             | DESCRIPTION |
| :------------------ | :---------- |
| **OpenVidu Server** | Media server used to stream real-time video, audio and data. Based on SFUs LiveKit and mediasoup. |
| **Egress Server**   | Module used to export media from a Room (for example, recordings or RTMP broadcasting). See [Egress](https://docs.livekit.io/egress-ingress/egress/overview/){:target=_blank}. |
| **Ingress Server**  | Module used to import media into a Room (for example, an MP4 video or an RTSP stream). See [Ingress](https://docs.livekit.io/egress-ingress/ingress/overview/){:target=_blank}. |
| **Caddy**           | Reverse proxy used as a loadbalancer to distribute the load generated by the Media Nodes over the Minio, Mimir and Loki cluster. |
| **Prometheus (observability)** | Module used to collect metrics from OpenVidu Server and send them to Loki. |
| **Promtail (observability)**   | Module used to collect logs from all services and send them to Loki. |

<script>window.setupGallery()</script>
