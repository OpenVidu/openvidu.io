---
description: Explore the latest OpenVidu releases, including new features, updates and bug fixes for each version of the platform.
---

## 3.0.0-beta2

### Changelog

- Improved [mediasoup](self-hosting/production-ready/performance.md) support:
    - Data messages work ([LiveKit reference](https://docs.livekit.io/realtime/client/data-messages/#Data-messages){:target="\_blank"}).
    - Ingress supported ([LiveKit reference](https://docs.livekit.io/realtime/ingress/overview/){:target="\_blank"}).
- Improved [OpenVidu Local Deployment](self-hosting/local.md):
    - Fixed Room Composite Egress ([LiveKit reference](https://docs.livekit.io/realtime/egress/room-composite/){:target="\_blank"}) support when using mediasoup.
    - WebHooks ([LiveKit reference](https://docs.livekit.io/realtime/server/webhooks/){:target="\_blank"}) supported against a local [OpenVidu Call](openvidu-call/docs.md#run-openvidu-locally).
- Production deployments have a better private IP discovery process when there are multiple valid private IPs in the same host. This will make work more deployments out-of-the-box without the need of manual intervention.
- [OpenVidu PRO Evaluation Mode](self-hosting/local.md#openvidu-pro) improved. Before a maximum a 2 Rooms of 8 Participants each could be created. Now the upper limit of Participants still apply, but the number of Rooms is unlimited. For example you can have 4 Rooms of 2 Participants each, or 1 Room of 8 Participants.
- Minor bug fixes related to [OpenVidu Call](openvidu-call/index.md).

### Known limitations

- When using [mediasoup](self-hosting/production-ready/performance.md):
    - No support for Speaker Detection events ([LiveKit reference](https://docs.livekit.io/realtime/client/receive/#Speaker-detection){target="\_blank"}).
    - No `ConnectionQualityChanged` event ([LiveKit reference](https://docs.livekit.io/realtime/client/events/#Events){target="\_blank"}).
    - No support for Dynacast ([LiveKit reference](https://docs.livekit.io/realtime/client/publish/#Dynamic-broadcasting){target="\_blank"}).
    - No support for Adaptive Streaming ([LiveKit reference](https://docs.livekit.io/realtime/client/receive/#Adaptive-stream){target="\_blank"}).
- When using [OpenVidu Call](openvidu-call/docs.md#run-openvidu-locally) against an [OpenVidu Local Deployment](self-hosting/local.md), recordings cannot be accessed.

### Version table

| Artifact               | Version | Info | Link         |
| ---------------------- | ------- | ---- | ---------- |
| livekit/livekit-server | v1.6.0  | :material-information-outline:{ title="Version of livekit-server in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/livekit/livekit/releases/tag/v1.6.0){:target="\_blank"} |
| mediasoup              | 3.12.16 | :material-information-outline:{ title="Version of mediasoup in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/versatica/mediasoup/releases/tag/3.12.16){:target="\_blank"} |
| livekit/egress         | v1.8.2  | :material-information-outline:{ title="Egress version used by OpenVidu deployments. Used to export media from a Room (for example, recordings or RTMP broadcasting)" } | [:octicons-link-24:](https://github.com/livekit/egress/releases/tag/v1.8.2){:target="\_blank"} |
| livekit/ingress        | v1.2.0  | :material-information-outline:{ title="Ingress version used by OpenVidu deployments. Used to import media into a Room (for example, an MP4 video or an RTSP stream)" } | [:octicons-link-24:](https://github.com/livekit/ingress/releases/tag/v1.2.0){:target="\_blank"} |
| MinIO | 2024.06.13 | :material-information-outline:{ title="Version of S3 MinIO used by OpenVidu deployments. Used to store recordings and common node configurations. In <i>OpenVidu High Availability</i> this is an instance of a <i>Minio Multi-Node</i>" } | [:octicons-link-24:](https://github.com/minio/minio/releases/tag/RELEASE.2024-06-13T22-53-53Z){:target="\_blank"} |
| Caddy | 2.7.6 | :material-information-outline:{ title="Version of Caddy used by OpenVidu deployments. It is a reverse proxy used as a loadbalancer to distribute client connections across your nodes and automatically manage your TLS certificate" } |  [:octicons-link-24:](https://github.com/caddyserver/caddy/releases/tag/v2.7.6){:target="\_blank"}|
| MongoDB | 7.0.11 | :material-information-outline:{ title="Version of MongoDB used by OpenVidu deployments. Used to store analytics and monitoring persistent data. In <i>OpenVidu High Availability</i> this is an instance of a <i>MongoDB Replica Set</i>" } | [:octicons-link-24:](https://www.mongodb.com/docs/manual/release-notes/7.0-changelog/#std-label-7.0.11-changelog){:target="\_blank"} |
| Redis | 7.2.5 | :material-information-outline:{ title="Version of Redis used by OpenVidu deployments. Used to share transient information between Media Nodes and coordinate them. In <i>OpenVidu High Availability</i> this is an instance of a <i>Redis Cluster</i>" } | [:octicons-link-24:](https://github.com/redis/redis/releases/tag/7.2.5){:target="\_blank"} |
| Grafana | 10.3.3 | :material-information-outline:{ title="Version of Grafana used by OpenVidu deployments. Observability module used to query and visualize logs and metrics in dashboards" } | [:octicons-link-24:](https://github.com/grafana/grafana/releases/tag/v10.3.3){:target="\_blank"} |
| Prometheus | 2.50.1 | :material-information-outline:{ title="Version of Prometheus used by OpenVidu deployments. Observability module from Grafana stack, used to collect metrics from Media Nodes and send them to Mimir" } | [:octicons-link-24:](https://github.com/prometheus/prometheus/releases/tag/v2.50.1){:target="\_blank"} |
| Promtail / Loki | 2.8.9 | :material-information-outline:{ title="Version of loki and promtail used by OpenVidu deployments. Observability modules from Grafana stack, used to collect logs from all services (Promtail) and stored them (Loki)" } | [:octicons-link-24:](https://github.com/grafana/loki/releases/tag/v2.8.9){:target="\_blank"} |
| Mimir | 2.11.0 | :material-information-outline:{ title="Version of Mimir used by OpenVidu deployments. Observability module from Grafana stack, used to store metrics from Prometheus" } | [:octicons-link-24:](https://github.com/grafana/mimir/releases/tag/mimir-2.11.0){:target="\_blank"} |

## 3.0.0-beta1

### Version table

| Artifact               | Version | Info | Link         |
| ---------------------- | ------- | ---- | ---------- |
| livekit/livekit-server | v1.6.0  | :material-information-outline:{ title="Version of livekit-server in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/livekit/livekit/releases/tag/v1.6.0){:target="\_blank"} |
| mediasoup              | 3.12.16 | :material-information-outline:{ title="Version of mediasoup in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/versatica/mediasoup/releases/tag/3.12.16){:target="\_blank"} |
| livekit/egress         | v1.8.2  | :material-information-outline:{ title="Egress version used by OpenVidu deployments. Used to export media from a Room (for example, recordings or RTMP broadcasting)" } | [:octicons-link-24:](https://github.com/livekit/egress/releases/tag/v1.8.2){:target="\_blank"} |
| livekit/ingress        | v1.2.0  | :material-information-outline:{ title="Ingress version used by OpenVidu deployments. Used to import media into a Room (for example, an MP4 video or an RTSP stream)" } | [:octicons-link-24:](https://github.com/livekit/ingress/releases/tag/v1.2.0){:target="\_blank"} |
| MinIO | 2024.06.13 | :material-information-outline:{ title="Version of S3 MinIO used by OpenVidu deployments. Used to store recordings and common node configurations. In <i>OpenVidu High Availability</i> this is an instance of a <i>Minio Multi-Node</i>" } | [:octicons-link-24:](https://github.com/minio/minio/releases/tag/RELEASE.2024-06-13T22-53-53Z){:target="\_blank"} |
| Caddy | 2.7.6 | :material-information-outline:{ title="Version of Caddy used by OpenVidu deployments. It is a reverse proxy used as a loadbalancer to distribute client connections across your nodes and automatically manage your TLS certificate" } |  [:octicons-link-24:](https://github.com/caddyserver/caddy/releases/tag/v2.7.6){:target="\_blank"}|
| MongoDB | 7.0.11 | :material-information-outline:{ title="Version of MongoDB used by OpenVidu deployments. Used to store analytics and monitoring persistent data. In <i>OpenVidu High Availability</i> this is an instance of a <i>MongoDB Replica Set</i>" } | [:octicons-link-24:](https://www.mongodb.com/docs/manual/release-notes/7.0-changelog/#std-label-7.0.11-changelog){:target="\_blank"} |
| Redis | 7.2.5 | :material-information-outline:{ title="Version of Redis used by OpenVidu deployments. Used to share transient information between Media Nodes and coordinate them. In <i>OpenVidu High Availability</i> this is an instance of a <i>Redis Cluster</i>" } | [:octicons-link-24:](https://github.com/redis/redis/releases/tag/7.2.5){:target="\_blank"} |
| Grafana | 10.3.3 | :material-information-outline:{ title="Version of Grafana used by OpenVidu deployments. Observability module used to query and visualize logs and metrics in dashboards" } | [:octicons-link-24:](https://github.com/grafana/grafana/releases/tag/v10.3.3){:target="\_blank"} |
| Prometheus | 2.50.1 | :material-information-outline:{ title="Version of Prometheus used by OpenVidu deployments. Observability module from Grafana stack, used to collect metrics from Media Nodes and send them to Mimir" } | [:octicons-link-24:](https://github.com/prometheus/prometheus/releases/tag/v2.50.1){:target="\_blank"} |
| Promtail / Loki | 2.8.9 | :material-information-outline:{ title="Version of loki and promtail used by OpenVidu deployments. Observability modules from Grafana stack, used to collect logs from all services (Promtail) and stored them (Loki)" } | [:octicons-link-24:](https://github.com/grafana/loki/releases/tag/v2.8.9){:target="\_blank"} |
| Mimir | 2.11.0 | :material-information-outline:{ title="Version of Mimir used by OpenVidu deployments. Observability module from Grafana stack, used to store metrics from Prometheus" } | [:octicons-link-24:](https://github.com/grafana/mimir/releases/tag/mimir-2.11.0){:target="\_blank"} |