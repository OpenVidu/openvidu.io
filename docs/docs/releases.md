---
description: Explore the latest OpenVidu releases, including new features, updates and bug fixes for each version of the platform.
---

## 3.3.0

### Changelog

- **AI Services**: OpenVidu now supports a catalog of AI services that can be easily integrated into your application to enhance the user experience and add advanced features. These services are delivered through **OpenVidu agents**: a set of pre-configured and ready-to-use AI modules that seamlessly integrate into your Rooms.

    We are starting with the **Speech Processing agent**: it focuses on transcribing audio speech to text and processing the results in various ways. Currently offering the [**Live Captions**](ai/live-captions.md) service, which generates live captions for your users' speech with great accuracy to display them in your frontend application. The Live Captions service supports many leading AI providers, such as OpenAI, Google, Azure, Amazon and more (see [Supported AI providers](ai/live-captions.md#supported-ai-providers)).

    Of course, you can also implement your own custom agents using the powerful [LiveKit Agents framework](https://docs.livekit.io/agents/){:target="\_blank"} and deploy it along your OpenVidu deployment. Any LiveKit agent is compatible with OpenVidu. Learn how to do so [here](ai/custom-agents.md).

- **Use a single domain for your deployment (EXPERIMENTAL)**: OpenVidu deployments now support TURN with TLS without an additional Domain Name using the flag `--experimental-turn-tls-with-main-domain`. This is great for production deployments, as it allows you to use a single domain and still support users behind restrictive firewalls.

    You can deploy any OpenVidu deployment with this feature enabled:

      - **On Premises**: perform a _non-interactive_ installation passing the flag. How to perform a non-interactive installation for each OpenVidu deployment: [OpenVidu Single Node COMMUNITY](self-hosting/single-node/on-premises/install.md#non-interactive-installation), [OpenVidu Single Node PRO](self-hosting/single-node-pro/on-premises/install.md#non-interactive-installation), [OpenVidu Elastic](self-hosting/elastic/on-premises/install.md#non-interactive-installation), [OpenVidu High Availability with DNS](self-hosting/ha/on-premises/install-dlb.md#non-interactive-installation), [OpenVidu High Availability with NLB](self-hosting/ha/on-premises/install-nlb.md#non-interactive-installation).
      - **AWS**: when deploying the CloudFormation template, add the flag `--experimental-turn-tls-with-main-domain` to the parameter named `(Optional) Additional Installer Flags"`, and leave empty parameters under `(Optional) TURN server configuration with TLS`.
      - **Azure**: when deploying the ARM template, add the flag `--experimental-turn-tls-with-main-domain` to the parameter named `(Optional) Additional Install Flags`, and leave empty parameters under `(Optional) TURN server configuration with TLS`.

- **Azure deployment bug fixes**:
    - Media Nodes are now automatically deleted if the installation process fails, preventing unwanted resources being left in your Azure account.
    - A misconfiguration was preventing the TURN server from working correctly in Azure. This is now fixed.
    - Fixed a race condition during the deployment process in Azure that sometimes caused problems when creating multiple subnets concurrently ([9728d96](https://github.com/OpenVidu/openvidu/commit/9728d96){:target="\_blank"}).

### Version table

| Artifact               | Version | Info | Link         |
| ---------------------- | ------- | ---- | ---------- |
| livekit/livekit-server | v1.8.4  | :material-information-outline:{ title="Version of livekit-server in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/livekit/livekit/releases/tag/v1.8.4){:target="\_blank"} |
| mediasoup              | 3.12.16 | :material-information-outline:{ title="Version of mediasoup in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/versatica/mediasoup/releases/tag/3.12.16){:target="\_blank"} |
| livekit/egress         | v1.9.1  | :material-information-outline:{ title="Egress version used by OpenVidu deployments. Used to export media from a Room (for example, recordings or RTMP broadcasting)" } | [:octicons-link-24:](https://github.com/livekit/egress/releases/tag/v1.9.1){:target="\_blank"} |
| livekit/ingress        | v1.4.3  | :material-information-outline:{ title="Ingress version used by OpenVidu deployments. Used to import media into a Room (for example, an MP4 video or an RTSP stream)" } | [:octicons-link-24:](https://github.com/livekit/ingress/releases/tag/v1.4.3){:target="\_blank"} |
| livekit/agents        | v1.1.4  | :material-information-outline:{ title="LiveKit Agents framework version. Used to add AI capabilities to your Rooms" } | [:octicons-link-24:](https://github.com/livekit/agents/releases/tag/livekit-agents%401.1.4){:target="\_blank"} |
| MinIO | 2025.5.24 | :material-information-outline:{ title="Version of S3 MinIO used by OpenVidu deployments. Used to store recordings and common node configurations. In <i>OpenVidu High Availability</i> this is an instance of a <i>Minio Multi-Node</i>" } | [:octicons-link-24:](https://github.com/minio/minio/releases/tag/RELEASE.2025-05-24T17-08-30Z){:target="\_blank"} |
| Caddy | 2.10.0 | :material-information-outline:{ title="Version of Caddy used by OpenVidu deployments. It is a reverse proxy used as a load balancer to distribute client connections across your nodes and automatically manage your TLS certificate" } |  [:octicons-link-24:](https://github.com/caddyserver/caddy/releases/tag/v2.10.0){:target="\_blank"}|
| MongoDB | 8.0.9 | :material-information-outline:{ title="Version of MongoDB used by OpenVidu deployments. Used to store analytics and monitoring persistent data. In <i>OpenVidu High Availability</i> this is an instance of a <i>MongoDB Replica Set</i>" } | [:octicons-link-24:](https://www.mongodb.com/docs/manual/release-notes/8.0/#8.0.9---may-1--2025){:target="\_blank"} |
| Redis | 7.4.4 | :material-information-outline:{ title="Version of Redis used by OpenVidu deployments. Used to share transient information between Media Nodes and coordinate them. In <i>OpenVidu High Availability</i> this is an instance of a <i>Redis Cluster</i>" } | [:octicons-link-24:](https://github.com/redis/redis/releases/tag/7.4.4){:target="\_blank"} |
| Grafana | 11.6.2 | :material-information-outline:{ title="Version of Grafana used by OpenVidu deployments. Observability module used to query and visualize logs and metrics in dashboards" } | [:octicons-link-24:](https://github.com/grafana/grafana/releases/tag/v11.6.2){:target="\_blank"} |
| Prometheus | 3.4.0 | :material-information-outline:{ title="Version of Prometheus used by OpenVidu deployments. Observability module from Grafana stack, used to collect metrics from Media Nodes and send them to Mimir" } | [:octicons-link-24:](https://github.com/prometheus/prometheus/releases/tag/v3.4.0){:target="\_blank"} |
| Promtail / Loki | 3.5.1 | :material-information-outline:{ title="Version of loki and promtail used by OpenVidu deployments. Observability modules from Grafana stack, used to collect logs from all services (Promtail) and stored them (Loki)" } | [:octicons-link-24:](https://github.com/grafana/loki/releases/tag/v3.5.1){:target="\_blank"} |
| Mimir | 2.16.0 | :material-information-outline:{ title="Version of Mimir used by OpenVidu deployments. Observability module from Grafana stack, used to store metrics from Prometheus" } | [:octicons-link-24:](https://github.com/grafana/mimir/releases/tag/mimir-2.16.0){:target="\_blank"} |

## 3.2.0

### Changelog

- **OpenVidu Single Node PRO**: OpenVidu Single Node PRO is a new type of OpenVidu deployment targeting users that want to deploy OpenVidu as a single-node setup but that still want the [2x performance boost](self-hosting/production-ready/performance.md) and the [advanced observability](self-hosting/production-ready/observability/index.md) provided by multi-node OpenVidu PRO deployments.
- **Azure deployments (Beta)**: OpenVidu now supports native deployments in Microsoft Azure. You can now deploy [OpenVidu Single Node COMMUNITY](self-hosting/single-node/azure/install.md), [OpenVidu Single Node PRO](self-hosting/single-node-pro/azure/install.md), [OpenVidu Elastic](self-hosting/elastic/azure/install.md) and [OpenVidu High Availability](self-hosting/ha/azure/install.md) in Azure using ARM templates. _During version 3.2.0, Azure deployments will be considered in Beta_.
- **New Azure recording tutorials**: OpenVidu deployments in Azure use Azure Blob Storage to store recordings (instead of S3). For this reason, we have extended our recording tutorials with Azure Blob Storage compatible examples. You can find them in the following links:
    - [Recording Basic Azure](tutorials/advanced-features/recording-basic-azure.md).
    - [Recording Advanced Azure](tutorials/advanced-features/recording-advanced-azure.md).

- **External proxy configuration**: By default, OpenVidu is deployed with an internal [Caddy server](https://caddyserver.com/){:target="\_blank"} to configure and manage SSL certificates. However, there are certain scenarios where using an external proxy might be preferable:
    - You wish to manage SSL certificates manually.
    - A specific proxy server is required for enhanced security.
    - You need to integrate a proxy server already in your infrastructure.

    For any of these cases, now all OpenVidu deployments allow configuring external proxies. You can find the instructions to do so in [this how-to guide](self-hosting/how-to-guides/deploy-with-external-proxy.md).

- **LiveKit stack updated to v1.8.4**: OpenVidu 3.2.0 is now based on LiveKit v1.8.4, which includes several improvements and bug fixes. You can find the [release notes here](https://github.com/livekit/livekit/releases/tag/v1.8.4).
- **OpenVidu installer improvements**: Some users have reported issues when installing OpenVidu, which were finally caused by old versions of Docker and/or Docker Compose. The OpenVidu installer now checks both versions and displays a descriptive error message if they are incompatible.
- **OpenVidu Angular Components**: see [Angular Components documentation](ui-components/angular-components.md).
    - Virtual Backgrounds improvements: More efficient use of resources by reusing the existing context. Avoid video flickering when changing the background. Improved resource reallocation management for smoother rendering. Contribution to LiveKit’s track-processors-js package ([PR 86](https://github.com/livekit/track-processors-js/pull/86)) resolving an issue affecting its dependencies.
    - Fixed panel reopening issue with [`ovAdditionalPanels`](reference-docs/openvidu-components-angular/directives/AdditionalPanelsDirective.html) directive. Custom panels created with `ovAdditionalPanels` would not reopen correctly after switching between default panels (activities, participants or chat). Now, returning to a custom panel restores it as expected without closing all panels.
    - Minor style fixes.

- **Deployment bug fixes**:
    - OpenVidu On Premises deployments that made use of [v2compatibility module](https://docs.openvidu.io/en/stable/openvidu3/#updating-from-openvidu-v2-to-openvidu-v3){:target="\_blank"} had a wrong configuration affecting the S3 MinIO bucket. This could cause issues when recording sessions from your OpenVidu v2 application. This is now fixed.
    - Wrong Caddy configuration in OpenVidu High Availability deployments made some services not reachable in specific scenarios of fault tolerance. This is now fixed.
 
### Breaking changes

- For OpenVidu On Premises deployments, the default S3 bucket in MinIO has been renamed from `app-data` to `openvidu-appdata` (in Single Node and Elastic deployments) and from `cluster-data` to `openvidu-clusterdata` (in High Availability deployments).
- Port rules in [OpenVidu High Availability with Network Load Balancer](self-hosting/ha/on-premises/install-nlb.md) have changed. Check the port rules from the installation instructions.

### Version table

| Artifact               | Version | Info | Link         |
| ---------------------- | ------- | ---- | ---------- |
| livekit/livekit-server | v1.8.4  | :material-information-outline:{ title="Version of livekit-server in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/livekit/livekit/releases/tag/v1.8.4){:target="\_blank"} |
| mediasoup              | 3.12.16 | :material-information-outline:{ title="Version of mediasoup in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/versatica/mediasoup/releases/tag/3.12.16){:target="\_blank"} |
| livekit/egress         | v1.9.1  | :material-information-outline:{ title="Egress version used by OpenVidu deployments. Used to export media from a Room (for example, recordings or RTMP broadcasting)" } | [:octicons-link-24:](https://github.com/livekit/egress/releases/tag/v1.9.1){:target="\_blank"} |
| livekit/ingress        | v1.4.3  | :material-information-outline:{ title="Ingress version used by OpenVidu deployments. Used to import media into a Room (for example, an MP4 video or an RTSP stream)" } | [:octicons-link-24:](https://github.com/livekit/ingress/releases/tag/v1.4.3){:target="\_blank"} |
| MinIO | 2025.5.24 | :material-information-outline:{ title="Version of S3 MinIO used by OpenVidu deployments. Used to store recordings and common node configurations. In <i>OpenVidu High Availability</i> this is an instance of a <i>Minio Multi-Node</i>" } | [:octicons-link-24:](https://github.com/minio/minio/releases/tag/RELEASE.2025-05-24T17-08-30Z){:target="\_blank"} |
| Caddy | 2.10.0 | :material-information-outline:{ title="Version of Caddy used by OpenVidu deployments. It is a reverse proxy used as a load balancer to distribute client connections across your nodes and automatically manage your TLS certificate" } |  [:octicons-link-24:](https://github.com/caddyserver/caddy/releases/tag/v2.10.0){:target="\_blank"}|
| MongoDB | 8.0.9 | :material-information-outline:{ title="Version of MongoDB used by OpenVidu deployments. Used to store analytics and monitoring persistent data. In <i>OpenVidu High Availability</i> this is an instance of a <i>MongoDB Replica Set</i>" } | [:octicons-link-24:](https://www.mongodb.com/docs/manual/release-notes/8.0/#8.0.9---may-1--2025){:target="\_blank"} |
| Redis | 7.4.4 | :material-information-outline:{ title="Version of Redis used by OpenVidu deployments. Used to share transient information between Media Nodes and coordinate them. In <i>OpenVidu High Availability</i> this is an instance of a <i>Redis Cluster</i>" } | [:octicons-link-24:](https://github.com/redis/redis/releases/tag/7.4.4){:target="\_blank"} |
| Grafana | 11.6.2 | :material-information-outline:{ title="Version of Grafana used by OpenVidu deployments. Observability module used to query and visualize logs and metrics in dashboards" } | [:octicons-link-24:](https://github.com/grafana/grafana/releases/tag/v11.6.2){:target="\_blank"} |
| Prometheus | 3.4.0 | :material-information-outline:{ title="Version of Prometheus used by OpenVidu deployments. Observability module from Grafana stack, used to collect metrics from Media Nodes and send them to Mimir" } | [:octicons-link-24:](https://github.com/prometheus/prometheus/releases/tag/v3.4.0){:target="\_blank"} |
| Promtail / Loki | 3.5.1 | :material-information-outline:{ title="Version of loki and promtail used by OpenVidu deployments. Observability modules from Grafana stack, used to collect logs from all services (Promtail) and stored them (Loki)" } | [:octicons-link-24:](https://github.com/grafana/loki/releases/tag/v3.5.1){:target="\_blank"} |
| Mimir | 2.16.0 | :material-information-outline:{ title="Version of Mimir used by OpenVidu deployments. Observability module from Grafana stack, used to store metrics from Prometheus" } | [:octicons-link-24:](https://github.com/grafana/mimir/releases/tag/mimir-2.16.0){:target="\_blank"} |

## 3.1.0

### Changelog

- **IP cameras support**: OpenVidu now allows you to connect RTSP IP cameras to your Rooms. This feature has been included in our custom fork of the [Ingress](https://docs.livekit.io/home/ingress/overview/){target="\_blank"} module, which is used to ingest media into a Room. Check out how to do it [here](developing-your-openvidu-app/how-to.md#ip-cameras). IP cameras support has also been included into the **v2 compatibility module**. This means that if your OpenVidu 2 application is using the [IP cameras feature](https://docs.openvidu.io/en/stable/advanced-features/ip-cameras/){target="\_blank"}, you can now upgrade your deployment to OpenVidu 3 and keep using this feature.
- **OpenVidu Updater**: you can now update the version of your OpenVidu deployment very easily using our new OpenVidu Updater module. OpenVidu Updater will take care of the whole process, from stopping the services to updating the configuration files. It will also manage backups to allow rollbacks in case of any issue. You can update your OpenVidu deployment from 3.0.0 to 3.1.0:
    - Update your **OpenVidu On Premises** deployment: [Update OpenVidu Single Node](self-hosting/single-node/on-premises/upgrade.md), [Update OpenVidu Elastic](self-hosting/elastic/on-premises/upgrade.md), [Update OpenVidu High Availability](self-hosting/ha/on-premises/upgrade.md).
    - Update your **OpenVidu AWS** deployment: for AWS deployment we recommend updating from 3.0.0 to 3.1.0 by redeploying the CloudFormation. From 3.1.0 onwards OpenVidu Updater will also be able to seamlessly update your AWS deployment.
- **mediasoup stability**: we believe we have reached the right point of maturity to take [mediasoup](self-hosting/production-ready/performance.md) as the internal RTC engine from experimental to production ready. There are still some [limitations](self-hosting/production-ready/performance.md#limitations) to take into account, but the general stability of the system is now considered production ready.
- **v2 Compatibility bug fixes**: there have been several improvements to the compatibility between OpenVidu v2 applications and OpenVidu v3 deployments:
    - **REST API**: Field `clientData` of the [Connection object](https://docs.openvidu.io/en/stable/reference-docs/REST-API/#the-connection-object){target="\_blank"} wasn't being properly set. Now it is.
    - **Webhook**: webhook event [`webrtcConnectionCreated`](https://docs.openvidu.io/en/stable/reference-docs/openvidu-server-webhook/#webrtcconnectioncreated){target="\_blank"} wasn't being sent when an audio-only Publisher published to the Session. Now it is.
    - **openvidu-browser-v2compatibility**:
        - Event [`videoElementCreated`](https://docs.openvidu.io/en/stable/api/openvidu-browser/interfaces/StreamManagerEventMap.html#videoElementCreated){target="\_blank"} wasn't being triggered for Subscriber participants. Now it is.
        - Event [`streamCreated`](https://docs.openvidu.io/en/stable/api/openvidu-browser/interfaces/SessionEventMap.html#streamCreated){target="\_blank"} wasn't being triggered by the Session object for Streams coming from audio-only Publishers. Now it is.
        - Event [`streamPropertyChanged`](https://docs.openvidu.io/en/stable/api/openvidu-browser/classes/StreamPropertyChangedEvent.html){target="\_blank"} wasn't being triggered when an audio-only Publisher muted/unmuted its audio. Now it is.

### Version table

| Artifact               | Version | Info | Link         |
| ---------------------- | ------- | ---- | ---------- |
| livekit/livekit-server | v1.8.3  | :material-information-outline:{ title="Version of livekit-server in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/livekit/livekit/releases/tag/v1.8.3){:target="\_blank"} |
| mediasoup              | 3.12.16 | :material-information-outline:{ title="Version of mediasoup in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/versatica/mediasoup/releases/tag/3.12.16){:target="\_blank"} |
| livekit/egress         | v1.9.0  | :material-information-outline:{ title="Egress version used by OpenVidu deployments. Used to export media from a Room (for example, recordings or RTMP broadcasting)" } | [:octicons-link-24:](https://github.com/livekit/egress/releases/tag/v1.9.0){:target="\_blank"} |
| livekit/ingress        | v1.4.3  | :material-information-outline:{ title="Ingress version used by OpenVidu deployments. Used to import media into a Room (for example, an MP4 video or an RTSP stream)" } | [:octicons-link-24:](https://github.com/livekit/ingress/releases/tag/v1.4.3){:target="\_blank"} |
| MinIO | 2025.2.7 | :material-information-outline:{ title="Version of S3 MinIO used by OpenVidu deployments. Used to store recordings and common node configurations. In <i>OpenVidu High Availability</i> this is an instance of a <i>Minio Multi-Node</i>" } | [:octicons-link-24:](https://github.com/minio/minio/releases/tag/RELEASE.2025-02-07T23-21-09Z){:target="\_blank"} |
| Caddy | 2.8.4 | :material-information-outline:{ title="Version of Caddy used by OpenVidu deployments. It is a reverse proxy used as a load balancer to distribute client connections across your nodes and automatically manage your TLS certificate" } |  [:octicons-link-24:](https://github.com/caddyserver/caddy/releases/tag/v2.8.4){:target="\_blank"}|
| MongoDB | 8.0.4 | :material-information-outline:{ title="Version of MongoDB used by OpenVidu deployments. Used to store analytics and monitoring persistent data. In <i>OpenVidu High Availability</i> this is an instance of a <i>MongoDB Replica Set</i>" } | [:octicons-link-24:](https://www.mongodb.com/docs/manual/release-notes/8.0/#8.0.4---dec-9--2024){:target="\_blank"} |
| Redis | 7.4.2 | :material-information-outline:{ title="Version of Redis used by OpenVidu deployments. Used to share transient information between Media Nodes and coordinate them. In <i>OpenVidu High Availability</i> this is an instance of a <i>Redis Cluster</i>" } | [:octicons-link-24:](https://github.com/redis/redis/releases/tag/7.4.2){:target="\_blank"} |
| Grafana | 11.5.1 | :material-information-outline:{ title="Version of Grafana used by OpenVidu deployments. Observability module used to query and visualize logs and metrics in dashboards" } | [:octicons-link-24:](https://github.com/grafana/grafana/releases/tag/v11.5.1){:target="\_blank"} |
| Prometheus | 3.1.0 | :material-information-outline:{ title="Version of Prometheus used by OpenVidu deployments. Observability module from Grafana stack, used to collect metrics from Media Nodes and send them to Mimir" } | [:octicons-link-24:](https://github.com/prometheus/prometheus/releases/tag/v3.1.0){:target="\_blank"} |
| Promtail / Loki | 3.3.2 | :material-information-outline:{ title="Version of loki and promtail used by OpenVidu deployments. Observability modules from Grafana stack, used to collect logs from all services (Promtail) and stored them (Loki)" } | [:octicons-link-24:](https://github.com/grafana/loki/releases/tag/v3.3.2){:target="\_blank"} |
| Mimir | 2.15.0 | :material-information-outline:{ title="Version of Mimir used by OpenVidu deployments. Observability module from Grafana stack, used to store metrics from Prometheus" } | [:octicons-link-24:](https://github.com/grafana/mimir/releases/tag/mimir-2.15.0){:target="\_blank"} |

## 3.0.0

### Changelog

- **General Availability of OpenVidu 3**, which is considered now stable and production-ready. Beta versions of OpenVidu 3 are preparing to be discontinued (including [3.0.0-beta1](#300-beta1), [3.0.0-beta2](#300-beta2) and [3.0.0-beta3](#300-beta3)).

### Known limitations

- When using [mediasoup](self-hosting/production-ready/performance.md):
    - No `ConnectionQualityChanged` event ([LiveKit reference](https://docs.livekit.io/home/client/events/#Events){target="\_blank"}).
    - No `TrackStreamStateChanged` event ([LiveKit reference](https://docs.livekit.io/home/client/events/#Events){target="\_blank"}).
    - Limited [ingress](https://docs.livekit.io/home/ingress/overview/){target="\_blank"} support: non-simulcast video tracks are not supported. Firefox may experience issues when subscribing to ingress video.

### Version table

| Artifact               | Version | Info | Link         |
| ---------------------- | ------- | ---- | ---------- |
| livekit/livekit-server | v1.8.0  | :material-information-outline:{ title="Version of livekit-server in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/livekit/livekit/releases/tag/v1.8.0){:target="\_blank"} |
| mediasoup              | 3.12.16 | :material-information-outline:{ title="Version of mediasoup in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/versatica/mediasoup/releases/tag/3.12.16){:target="\_blank"} |
| livekit/egress         | v1.8.4  | :material-information-outline:{ title="Egress version used by OpenVidu deployments. Used to export media from a Room (for example, recordings or RTMP broadcasting)" } | [:octicons-link-24:](https://github.com/livekit/egress/releases/tag/v1.8.4){:target="\_blank"} |
| livekit/ingress        | v1.4.2  | :material-information-outline:{ title="Ingress version used by OpenVidu deployments. Used to import media into a Room (for example, an MP4 video or an RTSP stream)" } | [:octicons-link-24:](https://github.com/livekit/ingress/releases/tag/v1.4.2){:target="\_blank"} |
| MinIO | 2024.10.13 | :material-information-outline:{ title="Version of S3 MinIO used by OpenVidu deployments. Used to store recordings and common node configurations. In <i>OpenVidu High Availability</i> this is an instance of a <i>Minio Multi-Node</i>" } | [:octicons-link-24:](https://github.com/minio/minio/releases/tag/RELEASE.2024-10-13T13-34-11Z){:target="\_blank"} |
| Caddy | 2.8.4 | :material-information-outline:{ title="Version of Caddy used by OpenVidu deployments. It is a reverse proxy used as a load balancer to distribute client connections across your nodes and automatically manage your TLS certificate" } |  [:octicons-link-24:](https://github.com/caddyserver/caddy/releases/tag/v2.8.4){:target="\_blank"}|
| MongoDB | 7.0.15 | :material-information-outline:{ title="Version of MongoDB used by OpenVidu deployments. Used to store analytics and monitoring persistent data. In <i>OpenVidu High Availability</i> this is an instance of a <i>MongoDB Replica Set</i>" } | [:octicons-link-24:](https://www.mongodb.com/docs/manual/release-notes/7.0-changelog/#std-label-7.0.15-changelog){:target="\_blank"} |
| Redis | 7.4.1 | :material-information-outline:{ title="Version of Redis used by OpenVidu deployments. Used to share transient information between Media Nodes and coordinate them. In <i>OpenVidu High Availability</i> this is an instance of a <i>Redis Cluster</i>" } | [:octicons-link-24:](https://github.com/redis/redis/releases/tag/7.4.1){:target="\_blank"} |
| Grafana | 11.3.0 | :material-information-outline:{ title="Version of Grafana used by OpenVidu deployments. Observability module used to query and visualize logs and metrics in dashboards" } | [:octicons-link-24:](https://github.com/grafana/grafana/releases/tag/v11.3.0){:target="\_blank"} |
| Prometheus | 2.55.0 | :material-information-outline:{ title="Version of Prometheus used by OpenVidu deployments. Observability module from Grafana stack, used to collect metrics from Media Nodes and send them to Mimir" } | [:octicons-link-24:](https://github.com/prometheus/prometheus/releases/tag/v2.55.0){:target="\_blank"} |
| Promtail / Loki | 3.2.1 | :material-information-outline:{ title="Version of loki and promtail used by OpenVidu deployments. Observability modules from Grafana stack, used to collect logs from all services (Promtail) and stored them (Loki)" } | [:octicons-link-24:](https://github.com/grafana/loki/releases/tag/v3.2.1){:target="\_blank"} |
| Mimir | 2.14.1 | :material-information-outline:{ title="Version of Mimir used by OpenVidu deployments. Observability module from Grafana stack, used to store metrics from Prometheus" } | [:octicons-link-24:](https://github.com/grafana/mimir/releases/tag/mimir-2.14.1){:target="\_blank"} |

## 3.0.0-beta3

### Changelog

- Centralized configuration: OpenVidu now automatically manages and synchronizes the configuration of all its components. This means that updating any configuration parameter in multi-node deployments ([OpenVidu Elastic](self-hosting/deployment-types.md#openvidu-elastic) and [OpenVidu High Availability](self-hosting/deployment-types.md#openvidu-high-availability)) is as simple as updating the required file in a single node. OpenVidu handles the distribution and restart of the affected services across all nodes. See how easily you can change the configuration [here](self-hosting/configuration/changing-config.md).
- [mediasoup](self-hosting/production-ready/performance.md) support:
    - Dynacast is now supported ([LiveKit reference](https://docs.livekit.io/home/client/tracks/publish/#Dynamic-broadcasting){target="\_blank"}).
    - Adaptive Streaming is now supported ([LiveKit reference](https://docs.livekit.io/home/client/tracks/subscribe/#Adaptive-stream){target="\_blank"}).
    - Speaker Detection events ([LiveKit reference](https://docs.livekit.io/home/client/tracks/subscribe/#Speaker-detection){target="\_blank"}).
    - Server API method `MutePublishTrack` ([LiveKit reference](https://docs.livekit.io/reference/server/server-apis/#MutePublishedTrack){target="\_blank"}).
    - Client API method `RemoteTrackPublication.setEnabled` ([LiveKit JS reference](https://docs.livekit.io/client-sdk-js/classes/RemoteTrackPublication.html#setEnabled){target="\_blank"}).
- [OpenVidu Call](openvidu-call/docs.md#run-openvidu-locally):
    - When using it against an [OpenVidu Local Deployment](self-hosting/local.md), recordings couldn't be accessed from the application's frontend. This is now fixed and OpenVidu Call is able to access recordings.
    - There was an error when applying Virtual Backgrounds ("No camera tracks found. Cannot apply background"). This is now fixed.
    - Docker image [openvidu/openvidu-call](https://hub.docker.com/r/openvidu/openvidu-call){target="\_blank"} is now 50% smaller.
- [OpenVidu v2 compatibility](https://docs.openvidu.io/en/stable/openvidu3/#updating-from-openvidu-v2-to-openvidu-v3){target="\_blank"}:
    - There was a race condition when multiple participants connected to the Session at the same time that could cause remote [`streamCreated`](https://docs.openvidu.io/en/stable/api/openvidu-browser/classes/StreamEvent.html){target="\_blank"} events to not be triggered. This is now fixed.
    - Configuration parameter `V2COMPAT_OPENVIDU_PRO_AWS_S3_BUCKET` did not allow configuring sub-buckets ("openvidu" worked fine, but "openvidu/subbucket" did not). Now it is possible to do so.
    - The operation to list recordings (available for [REST API](https://docs.openvidu.io/en/stable/reference-docs/REST-API/#get-all-recordings){target="\_blank"}, [openvidu-java-client](https://docs.openvidu.io/en/stable/api/openvidu-java-client/io/openvidu/java/client/OpenVidu.html#listRecordings()){target="\_blank"}, [openvidu-node-client](https://docs.openvidu.io/en/stable/api/openvidu-node-client/classes/OpenVidu.html#listRecordings){target="\_blank"}) was limited to 1000 recordings. This is now fixed and all recordings are always returned.
- AWS deployments: all secrets are now synchronized with [AWS Secrets Manager](https://console.aws.amazon.com/secretsmanager){target="\_blank"}. You can update any secret from the AWS console and restart your cluster for them to have immediate effect in all your nodes. This is also true in reverse: you can update any secret inside your node, and after restarting the cluster, the values in AWS Secrets Manager will be properly synchronized.
- New application tutorials available: [iOS](tutorials/application-client/ios.md), [Android](tutorials/application-client/android.md), [Recording](tutorials/advanced-features/index.md).

### Known limitations

- When using [mediasoup](self-hosting/production-ready/performance.md):
    - No `ConnectionQualityChanged` event ([LiveKit reference](https://docs.livekit.io/home/client/events/#Events){target="\_blank"}).
    - No `TrackStreamStateChanged` event ([LiveKit reference](https://docs.livekit.io/home/client/events/#Events){target="\_blank"}).

### Version table

| Artifact               | Version | Info | Link         |
| ---------------------- | ------- | ---- | ---------- |
| livekit/livekit-server | v1.7.2  | :material-information-outline:{ title="Version of livekit-server in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/livekit/livekit/releases/tag/v1.7.2){:target="\_blank"} |
| mediasoup              | 3.12.16 | :material-information-outline:{ title="Version of mediasoup in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/versatica/mediasoup/releases/tag/3.12.16){:target="\_blank"} |
| livekit/egress         | v1.8.2  | :material-information-outline:{ title="Egress version used by OpenVidu deployments. Used to export media from a Room (for example, recordings or RTMP broadcasting)" } | [:octicons-link-24:](https://github.com/livekit/egress/releases/tag/v1.8.2){:target="\_blank"} |
| livekit/ingress        | v1.4.2  | :material-information-outline:{ title="Ingress version used by OpenVidu deployments. Used to import media into a Room (for example, an MP4 video or an RTSP stream)" } | [:octicons-link-24:](https://github.com/livekit/ingress/releases/tag/v1.4.2){:target="\_blank"} |
| MinIO | 2024.6.13 | :material-information-outline:{ title="Version of S3 MinIO used by OpenVidu deployments. Used to store recordings and common node configurations. In <i>OpenVidu High Availability</i> this is an instance of a <i>Minio Multi-Node</i>" } | [:octicons-link-24:](https://github.com/minio/minio/releases/tag/RELEASE.2024-06-13T22-53-53Z){:target="\_blank"} |
| Caddy | 2.8.4 | :material-information-outline:{ title="Version of Caddy used by OpenVidu deployments. It is a reverse proxy used as a load balancer to distribute client connections across your nodes and automatically manage your TLS certificate" } |  [:octicons-link-24:](https://github.com/caddyserver/caddy/releases/tag/v2.8.4){:target="\_blank"}|
| MongoDB | 7.0.11 | :material-information-outline:{ title="Version of MongoDB used by OpenVidu deployments. Used to store analytics and monitoring persistent data. In <i>OpenVidu High Availability</i> this is an instance of a <i>MongoDB Replica Set</i>" } | [:octicons-link-24:](https://www.mongodb.com/docs/manual/release-notes/7.0-changelog/#std-label-7.0.11-changelog){:target="\_blank"} |
| Redis | 7.2.5 | :material-information-outline:{ title="Version of Redis used by OpenVidu deployments. Used to share transient information between Media Nodes and coordinate them. In <i>OpenVidu High Availability</i> this is an instance of a <i>Redis Cluster</i>" } | [:octicons-link-24:](https://github.com/redis/redis/releases/tag/7.2.5){:target="\_blank"} |
| Grafana | 10.3.3 | :material-information-outline:{ title="Version of Grafana used by OpenVidu deployments. Observability module used to query and visualize logs and metrics in dashboards" } | [:octicons-link-24:](https://github.com/grafana/grafana/releases/tag/v10.3.3){:target="\_blank"} |
| Prometheus | 2.50.1 | :material-information-outline:{ title="Version of Prometheus used by OpenVidu deployments. Observability module from Grafana stack, used to collect metrics from Media Nodes and send them to Mimir" } | [:octicons-link-24:](https://github.com/prometheus/prometheus/releases/tag/v2.50.1){:target="\_blank"} |
| Promtail / Loki | 2.8.9 | :material-information-outline:{ title="Version of loki and promtail used by OpenVidu deployments. Observability modules from Grafana stack, used to collect logs from all services (Promtail) and stored them (Loki)" } | [:octicons-link-24:](https://github.com/grafana/loki/releases/tag/v2.8.9){:target="\_blank"} |
| Mimir | 2.11.0 | :material-information-outline:{ title="Version of Mimir used by OpenVidu deployments. Observability module from Grafana stack, used to store metrics from Prometheus" } | [:octicons-link-24:](https://github.com/grafana/mimir/releases/tag/mimir-2.11.0){:target="\_blank"} |

## 3.0.0-beta2

### Changelog

- Improved [mediasoup](self-hosting/production-ready/performance.md) support:
    - Data messages work ([LiveKit reference](https://docs.livekit.io/home/client/data/#Data-messages){:target="\_blank"}).
    - Ingress supported ([LiveKit reference](https://docs.livekit.io/home/ingress/overview/){:target="\_blank"}).
- Improved [OpenVidu Local Deployment](self-hosting/local.md):
    - Fixed Room Composite Egress ([LiveKit reference](https://docs.livekit.io/home/egress/room-composite/){:target="\_blank"}) support when using mediasoup.
    - WebHooks ([LiveKit reference](https://docs.livekit.io/home/server/webhooks/){:target="\_blank"}) supported against a local [OpenVidu Call](openvidu-call/docs.md#run-openvidu-locally).
- Production deployments have a better private IP discovery process when there are multiple valid private IPs in the same host. This will make more deployments work out-of-the-box without the need of manual intervention.
- [OpenVidu PRO Evaluation Mode](self-hosting/local.md#openvidu-pro) improved. Before, a maximum a 2 Rooms of 8 Participants each could be created. Now the upper limit of Participants still apply, but the number of Rooms is unlimited. For example you can have 4 Rooms of 2 Participants each, or 1 Room of 8 Participants.
- Minor bug fixes related to [OpenVidu Call](openvidu-call/index.md).

### Known limitations

- When using [mediasoup](self-hosting/production-ready/performance.md):
    - No support for Speaker Detection events ([LiveKit reference](https://docs.livekit.io/home/client/tracks/subscribe/#Speaker-detection){target="\_blank"}).
    - No `ConnectionQualityChanged` event ([LiveKit reference](https://docs.livekit.io/home/client/events/#Events){target="\_blank"}).
    - No support for Dynacast ([LiveKit reference](https://docs.livekit.io/home/client/tracks/publish/#Dynamic-broadcasting){target="\_blank"}).
    - No support for Adaptive Streaming ([LiveKit reference](https://docs.livekit.io/home/client/tracks/subscribe/#Adaptive-stream){target="\_blank"}).
- When using [OpenVidu Call](openvidu-call/docs.md#run-openvidu-locally) against an [OpenVidu Local Deployment](self-hosting/local.md), recordings cannot be accessed.

### Version table

| Artifact               | Version | Info | Link         |
| ---------------------- | ------- | ---- | ---------- |
| livekit/livekit-server | v1.6.0  | :material-information-outline:{ title="Version of livekit-server in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/livekit/livekit/releases/tag/v1.6.0){:target="\_blank"} |
| mediasoup              | 3.12.16 | :material-information-outline:{ title="Version of mediasoup in which OpenVidu is based on" } | [:octicons-link-24:](https://github.com/versatica/mediasoup/releases/tag/3.12.16){:target="\_blank"} |
| livekit/egress         | v1.8.2  | :material-information-outline:{ title="Egress version used by OpenVidu deployments. Used to export media from a Room (for example, recordings or RTMP broadcasting)" } | [:octicons-link-24:](https://github.com/livekit/egress/releases/tag/v1.8.2){:target="\_blank"} |
| livekit/ingress        | v1.2.0  | :material-information-outline:{ title="Ingress version used by OpenVidu deployments. Used to import media into a Room (for example, an MP4 video or an RTSP stream)" } | [:octicons-link-24:](https://github.com/livekit/ingress/releases/tag/v1.2.0){:target="\_blank"} |
| MinIO | 2024.06.13 | :material-information-outline:{ title="Version of S3 MinIO used by OpenVidu deployments. Used to store recordings and common node configurations. In <i>OpenVidu High Availability</i> this is an instance of a <i>Minio Multi-Node</i>" } | [:octicons-link-24:](https://github.com/minio/minio/releases/tag/RELEASE.2024-06-13T22-53-53Z){:target="\_blank"} |
| Caddy | 2.7.6 | :material-information-outline:{ title="Version of Caddy used by OpenVidu deployments. It is a reverse proxy used as a load balancer to distribute client connections across your nodes and automatically manage your TLS certificate" } |  [:octicons-link-24:](https://github.com/caddyserver/caddy/releases/tag/v2.7.6){:target="\_blank"}|
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
| Caddy | 2.7.6 | :material-information-outline:{ title="Version of Caddy used by OpenVidu deployments. It is a reverse proxy used as a load balancer to distribute client connections across your nodes and automatically manage your TLS certificate" } |  [:octicons-link-24:](https://github.com/caddyserver/caddy/releases/tag/v2.7.6){:target="\_blank"}|
| MongoDB | 7.0.11 | :material-information-outline:{ title="Version of MongoDB used by OpenVidu deployments. Used to store analytics and monitoring persistent data. In <i>OpenVidu High Availability</i> this is an instance of a <i>MongoDB Replica Set</i>" } | [:octicons-link-24:](https://www.mongodb.com/docs/manual/release-notes/7.0-changelog/#std-label-7.0.11-changelog){:target="\_blank"} |
| Redis | 7.2.5 | :material-information-outline:{ title="Version of Redis used by OpenVidu deployments. Used to share transient information between Media Nodes and coordinate them. In <i>OpenVidu High Availability</i> this is an instance of a <i>Redis Cluster</i>" } | [:octicons-link-24:](https://github.com/redis/redis/releases/tag/7.2.5){:target="\_blank"} |
| Grafana | 10.3.3 | :material-information-outline:{ title="Version of Grafana used by OpenVidu deployments. Observability module used to query and visualize logs and metrics in dashboards" } | [:octicons-link-24:](https://github.com/grafana/grafana/releases/tag/v10.3.3){:target="\_blank"} |
| Prometheus | 2.50.1 | :material-information-outline:{ title="Version of Prometheus used by OpenVidu deployments. Observability module from Grafana stack, used to collect metrics from Media Nodes and send them to Mimir" } | [:octicons-link-24:](https://github.com/prometheus/prometheus/releases/tag/v2.50.1){:target="\_blank"} |
| Promtail / Loki | 2.8.9 | :material-information-outline:{ title="Version of loki and promtail used by OpenVidu deployments. Observability modules from Grafana stack, used to collect logs from all services (Promtail) and stored them (Loki)" } | [:octicons-link-24:](https://github.com/grafana/loki/releases/tag/v2.8.9){:target="\_blank"} |
| Mimir | 2.11.0 | :material-information-outline:{ title="Version of Mimir used by OpenVidu deployments. Observability module from Grafana stack, used to store metrics from Prometheus" } | [:octicons-link-24:](https://github.com/grafana/mimir/releases/tag/mimir-2.11.0){:target="\_blank"} |