## 3.5.0

> **For the Release Notes of OpenVidu Meet 3.5.0, please visit here: OpenVidu Meet 3.5.0**

### Changelog

- **ARM support**: OpenVidu can now be deployed in ARM-based systems. This broadens the range of instances in which OpenVidu can be deployed, offering new opportunities and alternatives that may be more cost-effective. To deploy OpenVidu in ARM architecture, you don't have to do anything special: just follow the default installation instructions for your desired OpenVidu deployment type. The installer will automatically detect the architecture and set up the appropriate services.
- **Google Cloud Platform support for all OpenVidu deployments**: we continue to expand our cloud-native deployment options. Now you can deploy [OpenVidu Single Node PRO](https://openvidu.io/3.5/docs/self-hosting/single-node-pro/gcp/install/index.md), [OpenVidu Elastic](https://openvidu.io/3.5/docs/self-hosting/elastic/gcp/install/index.md) and [OpenVidu High Availability](https://openvidu.io/3.5/docs/self-hosting/ha/gcp/install/index.md) in Google Cloud Platform using Terraform templates.
- **LiveKit stack updated to v1.9.8**: OpenVidu is now based on LiveKit v1.9.8, bringing all bug fixes and improvements since version v1.9.0. You can find the [release notes here](https://github.com/livekit/livekit/releases/tag/v1.9.8) .
  - Particularly relevant is the fix for [issue #3858](https://github.com/livekit/livekit/issues/3858), which fixes a fatal problem in the connection of the services with the Redis Cluster.
- **Egress updated to v1.12.0**: the Egress service has been updated to v1.12.0, which includes several improvements and bug fixes when exporting media from rooms. You can find the [release notes here](https://github.com/livekit/egress/releases/tag/v1.12.0) .
  - Particularly relevant is the change of the `unhealthyShutdownWatchdogDelay` value from 20 seconds to 10 minutes (see [commit e86593c](https://github.com/OpenVidu/egress/commit/e86593c25ab20e02d8e6d4a2edc4ac4b03fd2dbc)), preventing premature termination of egress processes under high CPU load or poor network conditions.
- **Ingress updated to latest**: the Ingress service has been updated to latest available commit *[#e42b67a](https://medium.com/r/?url=https%3A%2F%2Fgithub.com%2FOpenVidu%2Fingress%2Fcommit%2Fe42b67acf7d2c1ca5b463bb0d8f71bc4f6bf26c5)* with multiple improvements over last official release.
- **Live Captions**:
  - Fixed critical bug that caused slow response when transcribing 3 or more simultaneous participants in the same Room using AWS Transcribe provider. See related issue in the official LiveKit Agents repository ([#3739](https://github.com/livekit/agents/issues/3739)) and PR fixing it ([PR 4111](https://github.com/livekit/agents/pull/4111)).
  - Added [Cartesia](https://cartesia.ai/sonic) and [Soniox](https://soniox.com/) to the list of [supported AI providers](https://openvidu.io/3.5/docs/ai/live-captions/#supported-ai-providers).
  - [Interim transcriptions](https://openvidu.io/3.5/docs/ai/live-captions/#final-vs-interim-transcriptions) now available for existing [AI providers](https://openvidu.io/3.5/docs/ai/live-captions/#supported-ai-providers) Speechmatics and Gladia.
- **MongoDB**: OpenVidu now allows [configuring an external MongoDB](https://openvidu.io/3.5/docs/self-hosting/how-to-guides/external-mongodb/index.md) instead of using the bundled one, or you can choose to completely [disable the use of MongoDB](https://openvidu.io/3.5/docs/self-hosting/how-to-guides/enable-disable-mongodb/index.md) if your use case can do without services that require a database.
- **New backup and restore documentation for OpenVidu deployments**: we have carefully crafted a new [how-to guide](https://openvidu.io/3.5/docs/self-hosting/how-to-guides/backup-and-restore/index.md) explaining how to migrate your existing persistent data (recordings, analytics, monitoring data, etc.) when upgrading or changing your OpenVidu deployment. This process mainly affects the MongoDB and S3 services, responsible for persisting data in OpenVidu deployments.
- **OpenVidu Angular Components updated to support Angular v20**: the [OpenVidu Angular Components library](https://openvidu.io/3.5/docs/ui-components/angular-components/index.md) can now be used in applications built with Angular v20.
- **Time Zone fix**: OpenVidu deployments now honor their host time zone by default. Previously OpenVidu always used UTC. This proved a challenge when integrating OpenVidu with a custom app using local time zone. You can revert to UTC by providing the additional installation flag `--forceUTCTimezone`.
- **Oracle (OCI) Single Node and Single Node PRO installation tutorials**: we have created detailed step-by-step guides to help you deploy [OpenVidu Single Node COMMUNITY](https://openvidu.io/3.5/docs/releases/self-hosting/single-node/oci/install.md) and [OpenVidu Single Node PRO](https://openvidu.io/3.5/docs/releases/self-hosting/single-node-pro/oci/install.md) in Oracle Cloud Infrastructure using its native resources.

### Version table

| Artifact               | Version  | Info | Link |
| ---------------------- | -------- | ---- | ---- |
| livekit/livekit-server | v1.9.8   |      |      |
| mediasoup              | 3.12.16  |      |      |
| livekit/egress         | v1.12.0  |      |      |
| livekit/ingress        | v1.4.3   |      |      |
| livekit/agents         | v1.3.9   |      |      |
| MinIO                  | 2025.9.7 |      |      |
| Caddy                  | 2.10.2   |      |      |
| MongoDB                | 8.0.15   |      |      |
| Redis                  | 8.2.2    |      |      |
| Grafana                | 12.2.0   |      |      |
| Prometheus             | 3.7.1    |      |      |
| Promtail / Loki        | 3.5.7    |      |      |
| Mimir                  | 2.17.1   |      |      |

## 3.4.0

> **For the Release Notes of OpenVidu Meet 3.4.0, please visit here: OpenVidu Meet 3.4.0**

### Changelog

- **LiveKit stack updated to v1.9.0**: OpenVidu is now based on LiveKit v1.9.0, which includes several improvements and bug fixes. You can find the [release notes here](https://github.com/livekit/livekit/releases/tag/v1.9.0) .
- **Egress updated to v1.10.0**: the Egress service has been updated to v1.10.0, which includes several improvements and bug fixes when exporting media from rooms. You can find the [release notes here](https://github.com/livekit/egress/releases/tag/v1.10.0) .
- **OpenVidu Single Node native deployment in Google Cloud Platform (GCP)**: you can now deploy OpenVidu Single Node in GCP using its native resources thanks to our new Terraform template. Follow the [GCP deployment guide](https://openvidu.io/3.5/docs/self-hosting/single-node/gcp/install/index.md). Templates for OpenVidu Elastic and OpenVidu High Availability in GCP are coming soon.
- **No need for a domain name to deploy OpenVidu in production**: thanks to [sslip.io](https://sslip.io/) integration, you can now deploy OpenVidu in production with a valid SSL certificate without owning a custom domain name. Just deploy OpenVidu 3.4.0 and skip the domain name configuration during the installation process: OpenVidu will automatically detect your public IP and provide a secure domain name using sslip.io.
- **OpenVidu agents new configurations**: configure a custom CPU threshold to accept new jobs, and modify the agent's log level. See [Change CPU load threshold](https://openvidu.io/3.5/docs/ai/openvidu-agents/speech-processing-agent/#change-cpu-load-threshold) and [Log level](https://openvidu.io/3.5/docs/ai/openvidu-agents/speech-processing-agent/#log-level).
- **Custom AI agents now natively support [graceful shutdown](https://openvidu.io/3.5/docs/ai/custom-agents/#elasticity-and-graceful-shutdowns)**, ensuring no interruptions in the services provided by your custom agents when your OpenVidu cluster scales down.
- **OpenVidu Dashboard optimizations**: the addition of several new search indexes to the database has significantly improved the response time of the [OpenVidu Dashboard](https://openvidu.io/3.5/docs/self-hosting/production-ready/observability/openvidu-dashboard/index.md) when loading historical data.
- Fixed bug that caused empty `participantInfo` object when receiving [transcription events](https://openvidu.io/3.5/docs/ai/live-captions/#how-to-receive-live-captions-in-your-frontend-application) using the Speech Processing agent. This fix was also contributed to LiveKit open source ([PR 3735](https://github.com/livekit/livekit/pull/3735) ).
- **New load balancing strategy for Egress**: egresses were previously distributed across Media Nodes using a "binpack" strategy (trying to fill up one node before using the next one). This could lead to unbalanced CPU usage across nodes in certain scenarios. There is now a new load balancing strategy called "cpuload" that prioritizes nodes with lower CPU usage, leading to a more balanced cluster in terms of CPU utilization. This is now the default strategy. Learn how to configure it [here](https://openvidu.io/3.5/docs/self-hosting/production-ready/scalability/#egress).
- **Egress ability to auto kill processes under high CPU load can be disabled**: by default, if an egress detects a high CPU load (>95%) during a sustained period of time (10 seconds), the parent process automatically kills the most consuming egress. This helps preventing it from affecting the performance of other processes in the same Media Node. This default behavior can be now disabled if necessary. Learn how to do so [here](https://openvidu.io/3.5/docs/self-hosting/production-ready/scalability/#egress-cpu-overload-killer).
- **Extended scalability documentation**: we have improved our [scalability documentation](https://openvidu.io/3.5/docs/self-hosting/production-ready/scalability/index.md) explaining in detail how OpenVidu handles Room, Egress, Ingress and Agent allocation in multi-node deployments. All load balancing strategies and how to configure them are now explained in depth.
- **Caddy configuration improvements for Elastic and HA**: Improve Caddy to prevent websocket disconnections when new Media Nodes are added or removed.

### Version table

| Artifact               | Version   | Info | Link |
| ---------------------- | --------- | ---- | ---- |
| livekit/livekit-server | v1.9.0    |      |      |
| mediasoup              | 3.12.16   |      |      |
| livekit/egress         | v1.10.0   |      |      |
| livekit/ingress        | v1.4.3    |      |      |
| livekit/agents         | v1.2.6    |      |      |
| MinIO                  | 2025.5.24 |      |      |
| Caddy                  | 2.10.0    |      |      |
| MongoDB                | 8.0.9     |      |      |
| Redis                  | 7.4.4     |      |      |
| Grafana                | 11.6.2    |      |      |
| Prometheus             | 3.4.0     |      |      |
| Promtail / Loki        | 3.5.1     |      |      |
| Mimir                  | 2.16.0    |      |      |

### Patch releases

#### 3.4.1

- **OpenVidu Meet**: update authentication methods to use header-based tokens instead of cookies. When [embedding OpenVidu Meet](https://openvidu.io/3.5/meet/embedded/intro/index.md), the strategy (`SameSite=Strict`) was causing issues when loading the application and the embedable component from different domains. Using the most permissive cookie policy available (`SameSite=None`) still caused issues in some browsers that block third-party cookies by default. Now OpenVidu Meet avoids cookies and instead uses header-based tokens for authentication, which is more reliable and secure. See [commit 4e80b5a](https://github.com/OpenVidu/openvidu-meet/commit/4e80b5a060c1ae0f8942527dbdc6ee221992caab) .
- **OpenVidu Elastic & High Availability deployments**: Egress/Ingress/Agents services in Media Nodes were not able to reach the LiveKit API when the local OpenVidu server was down or unresponsive. Now all of these services are properly configured to reach any Media Node in the cluster, ensuring fault tolerance upon OpenVidu server failures.

## 3.3.0

### Changelog

- **AI Services**: OpenVidu now supports a catalog of AI services that can be easily integrated into your application to enhance the user experience and add advanced features. These services are delivered through **OpenVidu agents**: a set of pre-configured and ready-to-use AI modules that seamlessly integrate into your Rooms.

  We are starting with the **Speech Processing agent**: it focuses on transcribing audio speech to text and processing the results in various ways. Currently offering the [**Live Captions**](https://openvidu.io/3.5/docs/ai/live-captions/index.md) service, which generates live captions for your users' speech with great accuracy to display them in your frontend application. The Live Captions service supports many leading AI providers, such as OpenAI, Google, Azure, Amazon and more (see [Supported AI providers](https://openvidu.io/3.5/docs/ai/live-captions/#supported-ai-providers)).

  Of course, you can also implement your own custom agents using the powerful [LiveKit Agents framework](https://docs.livekit.io/agents/) and deploy it along your OpenVidu deployment. Any LiveKit agent is compatible with OpenVidu. Learn how to do so [here](https://openvidu.io/3.5/docs/ai/custom-agents/index.md).

- **Use a single domain for your deployment (EXPERIMENTAL)**: OpenVidu deployments now support TURN with TLS without an additional Domain Name using the flag `--experimental-turn-tls-with-main-domain`. This is great for production deployments, as it allows you to use a single domain and still support users behind restrictive firewalls.

  You can deploy any OpenVidu deployment with this feature enabled:

  - **On Premises**: perform a *non-interactive* installation passing the flag. How to perform a non-interactive installation for each OpenVidu deployment: [OpenVidu Single Node COMMUNITY](https://openvidu.io/3.5/docs/self-hosting/single-node/on-premises/install/#non-interactive-installation), [OpenVidu Single Node PRO](https://openvidu.io/3.5/docs/self-hosting/single-node-pro/on-premises/install/#non-interactive-installation), [OpenVidu Elastic](https://openvidu.io/3.5/docs/self-hosting/elastic/on-premises/install/#non-interactive-installation), [OpenVidu High Availability with DNS](https://openvidu.io/3.5/docs/self-hosting/ha/on-premises/install-dlb/#non-interactive-installation), [OpenVidu High Availability with NLB](https://openvidu.io/3.5/docs/self-hosting/ha/on-premises/install-nlb/#non-interactive-installation).
  - **AWS**: when deploying the CloudFormation template, add the flag `--experimental-turn-tls-with-main-domain` to the parameter named `(Optional) Additional Installer Flags"`, and leave empty parameters under `(Optional) TURN server configuration with TLS`.
  - **Azure**: when deploying the ARM template, add the flag `--experimental-turn-tls-with-main-domain` to the parameter named `(Optional) Additional Install Flags`, and leave empty parameters under `(Optional) TURN server configuration with TLS`.

- **Azure deployment bug fixes**:

  - Media Nodes are now automatically deleted if the installation process fails, preventing unwanted resources being left in your Azure account.
  - A misconfiguration was preventing the TURN server from working correctly in Azure. This is now fixed.
  - Fixed a race condition during the deployment process in Azure that sometimes caused problems when creating multiple subnets concurrently ([9728d96](https://github.com/OpenVidu/openvidu/commit/9728d96)).

### Version table

| Artifact               | Version   | Info | Link |
| ---------------------- | --------- | ---- | ---- |
| livekit/livekit-server | v1.8.4    |      |      |
| mediasoup              | 3.12.16   |      |      |
| livekit/egress         | v1.9.1    |      |      |
| livekit/ingress        | v1.4.3    |      |      |
| livekit/agents         | v1.1.4    |      |      |
| MinIO                  | 2025.5.24 |      |      |
| Caddy                  | 2.10.0    |      |      |
| MongoDB                | 8.0.9     |      |      |
| Redis                  | 7.4.4     |      |      |
| Grafana                | 11.6.2    |      |      |
| Prometheus             | 3.4.0     |      |      |
| Promtail / Loki        | 3.5.1     |      |      |
| Mimir                  | 2.16.0    |      |      |

## 3.2.0

### Changelog

- **OpenVidu Single Node PRO**: OpenVidu Single Node PRO is a new type of OpenVidu deployment targeting users that want to deploy OpenVidu as a single-node setup, but that still want the [2x performance boost](https://openvidu.io/3.5/docs/self-hosting/production-ready/performance/index.md) and the [advanced observability](https://openvidu.io/3.5/docs/self-hosting/production-ready/observability/index.md) provided by multi-node OpenVidu PRO deployments.

- **Azure deployments (Beta)**: OpenVidu now supports native deployments in Microsoft Azure. You can now deploy [OpenVidu Single Node COMMUNITY](https://openvidu.io/3.5/docs/self-hosting/single-node/azure/install/index.md), [OpenVidu Single Node PRO](https://openvidu.io/3.5/docs/self-hosting/single-node-pro/azure/install/index.md), [OpenVidu Elastic](https://openvidu.io/3.5/docs/self-hosting/elastic/azure/install/index.md) and [OpenVidu High Availability](https://openvidu.io/3.5/docs/self-hosting/ha/azure/install/index.md) in Azure using ARM templates. *During version 3.2.0, Azure deployments will be considered in Beta*.

- **New Azure recording tutorials**: OpenVidu deployments in Azure use Azure Blob Storage to store recordings (instead of S3). For this reason, we have extended our recording tutorials with Azure Blob Storage compatible examples. You can find them in the following links:

  - [Recording Basic Azure](https://openvidu.io/3.5/docs/tutorials/advanced-features/recording-basic-azure/index.md).
  - [Recording Advanced Azure](https://openvidu.io/3.5/docs/tutorials/advanced-features/recording-advanced-azure/index.md).

- **External proxy configuration**: By default, OpenVidu is deployed with an internal [Caddy server](https://caddyserver.com/) to configure and manage SSL certificates. However, there are certain scenarios where using an external proxy might be preferable:

  - You wish to manage SSL certificates manually.
  - A specific proxy server is required for enhanced security.
  - You need to integrate a proxy server already in your infrastructure.

  For any of these cases, now all OpenVidu deployments allow configuring external proxies. You can find the instructions to do so in [this how-to guide](https://openvidu.io/3.5/docs/self-hosting/how-to-guides/deploy-with-external-proxy/index.md).

- **LiveKit stack updated to v1.8.4**: OpenVidu 3.2.0 is now based on LiveKit v1.8.4, which includes several improvements and bug fixes. You can find the [release notes here](https://github.com/livekit/livekit/releases/tag/v1.8.4).

- **OpenVidu installer improvements**: Some users have reported issues when installing OpenVidu, which were finally caused by old versions of Docker and/or Docker Compose. The OpenVidu installer now checks both versions and displays a descriptive error message if they are incompatible.

- **OpenVidu Angular Components**: see [Angular Components documentation](https://openvidu.io/3.5/docs/ui-components/angular-components/index.md).

  - Virtual Backgrounds improvements: More efficient use of resources by reusing the existing context. Avoid video flickering when changing the background. Improved resource reallocation management for smoother rendering. Contribution to LiveKit’s track-processors-js package ([PR 86](https://github.com/livekit/track-processors-js/pull/86)) resolving an issue affecting its dependencies.
  - Fixed panel reopening issue with [`ovAdditionalPanels`](https://openvidu.io/3.5/docs/reference-docs/openvidu-components-angular/directives/AdditionalPanelsDirective.html) directive. Custom panels created with `ovAdditionalPanels` would not reopen correctly after switching between default panels (activities, participants or chat). Now, returning to a custom panel restores it as expected without closing all panels.
  - Minor style fixes.

- **Deployment bug fixes**:

  - OpenVidu On Premises deployments that made use of [v2compatibility module](https://docs.openvidu.io/en/stable/openvidu3/#updating-from-openvidu-v2-to-openvidu-v3) had a wrong configuration affecting the S3 MinIO bucket. This could cause issues when recording sessions from your OpenVidu v2 application. This is now fixed.
  - Wrong Caddy configuration in OpenVidu High Availability deployments made some services not reachable in specific scenarios of fault tolerance. This is now fixed.

### Breaking changes

- For OpenVidu On Premises deployments, the default S3 bucket in MinIO has been renamed from `app-data` to `openvidu-appdata` (in Single Node and Elastic deployments) and from `cluster-data` to `openvidu-clusterdata` (in High Availability deployments).
- Port rules in [OpenVidu High Availability with Network Load Balancer](https://openvidu.io/3.5/docs/self-hosting/ha/on-premises/install-nlb/index.md) have changed. Check the port rules from the installation instructions.

### Version table

| Artifact               | Version   | Info | Link |
| ---------------------- | --------- | ---- | ---- |
| livekit/livekit-server | v1.8.4    |      |      |
| mediasoup              | 3.12.16   |      |      |
| livekit/egress         | v1.9.1    |      |      |
| livekit/ingress        | v1.4.3    |      |      |
| MinIO                  | 2025.5.24 |      |      |
| Caddy                  | 2.10.0    |      |      |
| MongoDB                | 8.0.9     |      |      |
| Redis                  | 7.4.4     |      |      |
| Grafana                | 11.6.2    |      |      |
| Prometheus             | 3.4.0     |      |      |
| Promtail / Loki        | 3.5.1     |      |      |
| Mimir                  | 2.16.0    |      |      |

## 3.1.0

### Changelog

- **IP cameras support**: OpenVidu now allows you to connect RTSP IP cameras to your Rooms. This feature has been included in our custom fork of the [Ingress](https://docs.livekit.io/transport/media/ingress-egress/ingress/) module, which is used to ingest media into a Room. Check out how to do it [here](https://openvidu.io/3.5/docs/developing-your-openvidu-app/how-to/#ip-cameras). IP cameras support has also been included into the **v2 compatibility module**. This means that if your OpenVidu 2 application is using the [IP cameras feature](https://docs.openvidu.io/en/stable/advanced-features/ip-cameras/), you can now upgrade your deployment to OpenVidu 3 and keep using this feature.
- **OpenVidu Updater**: you can now update the version of your OpenVidu deployment very easily using our new OpenVidu Updater module. OpenVidu Updater will take care of the whole process, from stopping the services to updating the configuration files. It will also manage backups to allow rollbacks in case of any issue. You can update your OpenVidu deployment from 3.0.0 to 3.1.0:
  - Update your **OpenVidu On Premises** deployment: [Update OpenVidu Single Node](https://openvidu.io/3.5/docs/self-hosting/single-node/on-premises/upgrade/index.md), [Update OpenVidu Elastic](https://openvidu.io/3.5/docs/self-hosting/elastic/on-premises/upgrade/index.md), [Update OpenVidu High Availability](https://openvidu.io/3.5/docs/self-hosting/ha/on-premises/upgrade/index.md).
  - Update your **OpenVidu AWS** deployment: for AWS deployment we recommend updating from 3.0.0 to 3.1.0 by redeploying the CloudFormation. From 3.1.0 onwards OpenVidu Updater will also be able to seamlessly update your AWS deployment.
- **mediasoup stability**: we believe we have reached the right point of maturity to take [mediasoup](https://openvidu.io/3.5/docs/self-hosting/production-ready/performance/index.md) as the internal RTC engine from experimental to production ready. There are still some [limitations](https://openvidu.io/3.5/docs/self-hosting/production-ready/performance/#limitations) to take into account, but the general stability of the system is now considered production ready.
- **v2 Compatibility bug fixes**: there have been several improvements to the compatibility between OpenVidu v2 applications and OpenVidu v3 deployments:
  - **REST API**: Field `clientData` of the [Connection object](https://docs.openvidu.io/en/stable/reference-docs/REST-API/#the-connection-object) wasn't being properly set. Now it is.
  - **Webhook**: webhook event [`webrtcConnectionCreated`](https://docs.openvidu.io/en/stable/reference-docs/openvidu-server-webhook/#webrtcconnectioncreated) wasn't being sent when an audio-only Publisher published to the Session. Now it is.
  - **openvidu-browser-v2compatibility**:
    - Event [`videoElementCreated`](https://docs.openvidu.io/en/stable/api/openvidu-browser/interfaces/StreamManagerEventMap.html#videoElementCreated) wasn't being triggered for Subscriber participants. Now it is.
    - Event [`streamCreated`](https://docs.openvidu.io/en/stable/api/openvidu-browser/interfaces/SessionEventMap.html#streamCreated) wasn't being triggered by the Session object for Streams coming from audio-only Publishers. Now it is.
    - Event [`streamPropertyChanged`](https://docs.openvidu.io/en/stable/api/openvidu-browser/classes/StreamPropertyChangedEvent.html) wasn't being triggered when an audio-only Publisher muted/unmuted its audio. Now it is.

### Version table

| Artifact               | Version  | Info | Link |
| ---------------------- | -------- | ---- | ---- |
| livekit/livekit-server | v1.8.3   |      |      |
| mediasoup              | 3.12.16  |      |      |
| livekit/egress         | v1.9.0   |      |      |
| livekit/ingress        | v1.4.3   |      |      |
| MinIO                  | 2025.2.7 |      |      |
| Caddy                  | 2.8.4    |      |      |
| MongoDB                | 8.0.4    |      |      |
| Redis                  | 7.4.2    |      |      |
| Grafana                | 11.5.1   |      |      |
| Prometheus             | 3.1.0    |      |      |
| Promtail / Loki        | 3.3.2    |      |      |
| Mimir                  | 2.15.0   |      |      |

## 3.0.0

### Changelog

- **General Availability of OpenVidu 3**, which is considered now stable and production-ready. Beta versions of OpenVidu 3 are preparing to be discontinued (including [3.0.0-beta1](#300-beta1), [3.0.0-beta2](#300-beta2) and [3.0.0-beta3](#300-beta3)).

### Known limitations

- When using [mediasoup](https://openvidu.io/3.5/docs/self-hosting/production-ready/performance/index.md):
  - No `ConnectionQualityChanged` event ([LiveKit reference](https://docs.livekit.io/intro/basics/rooms-participants-tracks/webhooks-events/#sdk-events)).
  - No `TrackStreamStateChanged` event ([LiveKit reference](https://docs.livekit.io/intro/basics/rooms-participants-tracks/webhooks-events/#sdk-events)).
  - Limited [ingress](https://docs.livekit.io/transport/media/ingress-egress/ingress/) support: non-simulcast video tracks are not supported. Firefox may experience issues when subscribing to ingress video.

### Version table

| Artifact               | Version    | Info | Link |
| ---------------------- | ---------- | ---- | ---- |
| livekit/livekit-server | v1.8.0     |      |      |
| mediasoup              | 3.12.16    |      |      |
| livekit/egress         | v1.8.4     |      |      |
| livekit/ingress        | v1.4.2     |      |      |
| MinIO                  | 2024.10.13 |      |      |
| Caddy                  | 2.8.4      |      |      |
| MongoDB                | 7.0.15     |      |      |
| Redis                  | 7.4.1      |      |      |
| Grafana                | 11.3.0     |      |      |
| Prometheus             | 2.55.0     |      |      |
| Promtail / Loki        | 3.2.1      |      |      |
| Mimir                  | 2.14.1     |      |      |

## 3.0.0-beta3

### Changelog

- Centralized configuration: OpenVidu now automatically manages and synchronizes the configuration of all its components. This means that updating any configuration parameter in multi-node deployments ([OpenVidu Elastic](https://openvidu.io/3.5/docs/self-hosting/deployment-types/#openvidu-elastic) and [OpenVidu High Availability](https://openvidu.io/3.5/docs/self-hosting/deployment-types/#openvidu-high-availability)) is as simple as updating the required file in a single node. OpenVidu handles the distribution and restart of the affected services across all nodes. See how easily you can change the configuration [here](https://openvidu.io/3.5/docs/self-hosting/configuration/changing-config/index.md).
- [mediasoup](https://openvidu.io/3.5/docs/self-hosting/production-ready/performance/index.md) support:
  - Dynacast is now supported ([LiveKit reference](https://docs.livekit.io/transport/media/advanced/#dynacast)).
  - Adaptive Streaming is now supported ([LiveKit reference](https://docs.livekit.io/transport/media/subscribe/#Adaptive-stream)).
  - Speaker Detection events ([LiveKit reference](https://docs.livekit.io/transport/media/subscribe/#active-speaker-identification)).
  - Server API method `MutePublishTrack` ([LiveKit reference](https://docs.livekit.io/reference/other/roomservice-api/#MutePublishedTrack)).
  - Client API method `RemoteTrackPublication.setEnabled` ([LiveKit JS reference](https://docs.livekit.io/reference/client-sdk-js/classes/RemoteTrackPublication.html#setEnabled)).
- [OpenVidu Call](https://openvidu.io/3.5/docs/releases/openvidu-call/docs.md#run-openvidu-locally):
  - When using it against an [OpenVidu Local Deployment](https://openvidu.io/3.5/docs/self-hosting/local/index.md), recordings couldn't be accessed from the application's frontend. This is now fixed and OpenVidu Call is able to access recordings.
  - There was an error when applying Virtual Backgrounds ("No camera tracks found. Cannot apply background"). This is now fixed.
  - Docker image [openvidu/openvidu-call](https://hub.docker.com/r/openvidu/openvidu-call) is now 50% smaller.
- [OpenVidu v2 compatibility](https://docs.openvidu.io/en/stable/openvidu3/#updating-from-openvidu-v2-to-openvidu-v3):
  - There was a race condition when multiple participants connected to the Session at the same time that could cause remote [`streamCreated`](https://docs.openvidu.io/en/stable/api/openvidu-browser/classes/StreamEvent.html) events to not be triggered. This is now fixed.
  - Configuration parameter `V2COMPAT_OPENVIDU_PRO_AWS_S3_BUCKET` did not allow configuring sub-buckets ("openvidu" worked fine, but "openvidu/subbucket" did not). Now it is possible to do so.
  - The operation to list recordings (available for [REST API](https://docs.openvidu.io/en/stable/reference-docs/REST-API/#get-all-recordings), [openvidu-java-client](<https://docs.openvidu.io/en/stable/api/openvidu-java-client/io/openvidu/java/client/OpenVidu.html#listRecordings()>), [openvidu-node-client](https://docs.openvidu.io/en/stable/api/openvidu-node-client/classes/OpenVidu.html#listRecordings)) was limited to 1000 recordings. This is now fixed and all recordings are always returned.
- AWS deployments: all secrets are now synchronized with [AWS Secrets Manager](https://console.aws.amazon.com/secretsmanager). You can update any secret from the AWS console and restart your cluster for them to have immediate effect in all your nodes. This is also true in reverse: you can update any secret inside your node, and after restarting the cluster, the values in AWS Secrets Manager will be properly synchronized.
- New application tutorials available: [iOS](https://openvidu.io/3.5/docs/tutorials/application-client/ios/index.md), [Android](https://openvidu.io/3.5/docs/tutorials/application-client/android/index.md), [Recording](https://openvidu.io/3.5/docs/tutorials/advanced-features/index.md).

### Known limitations

- When using [mediasoup](https://openvidu.io/3.5/docs/self-hosting/production-ready/performance/index.md):
  - No `ConnectionQualityChanged` event ([LiveKit reference](https://docs.livekit.io/intro/basics/rooms-participants-tracks/webhooks-events/#sdk-events)).
  - No `TrackStreamStateChanged` event ([LiveKit reference](https://docs.livekit.io/intro/basics/rooms-participants-tracks/webhooks-events/#sdk-events)).

### Version table

| Artifact               | Version   | Info | Link |
| ---------------------- | --------- | ---- | ---- |
| livekit/livekit-server | v1.7.2    |      |      |
| mediasoup              | 3.12.16   |      |      |
| livekit/egress         | v1.8.2    |      |      |
| livekit/ingress        | v1.4.2    |      |      |
| MinIO                  | 2024.6.13 |      |      |
| Caddy                  | 2.8.4     |      |      |
| MongoDB                | 7.0.11    |      |      |
| Redis                  | 7.2.5     |      |      |
| Grafana                | 10.3.3    |      |      |
| Prometheus             | 2.50.1    |      |      |
| Promtail / Loki        | 2.8.9     |      |      |
| Mimir                  | 2.11.0    |      |      |

## 3.0.0-beta2

### Changelog

- Improved [mediasoup](https://openvidu.io/3.5/docs/self-hosting/production-ready/performance/index.md) support:
  - Data messages work ([LiveKit reference](https://docs.livekit.io/transport/data/)).
  - Ingress supported ([LiveKit reference](https://docs.livekit.io/transport/media/ingress-egress/ingress/)).
- Improved [OpenVidu Local Deployment](https://openvidu.io/3.5/docs/self-hosting/local/index.md):
  - Fixed Room Composite Egress ([LiveKit reference](https://docs.livekit.io/transport/media/ingress-egress/egress/composite-recording/)) support when using mediasoup.
  - WebHooks ([LiveKit reference](https://docs.livekit.io/intro/basics/rooms-participants-tracks/webhooks-events/)) supported against a local [OpenVidu Call](https://openvidu.io/3.5/docs/releases/openvidu-call/docs.md#run-openvidu-locally).
- Production deployments have a better private IP discovery process when there are multiple valid private IPs in the same host. This will make more deployments work out-of-the-box without the need of manual intervention.
- [OpenVidu PRO Evaluation Mode](https://openvidu.io/3.5/docs/self-hosting/local/#openvidu-pro) improved. Before, a maximum of 2 Rooms of 8 Participants each could be created. Now the upper limit of Participants still apply, but the number of Rooms is unlimited. For example, you can have 4 Rooms of 2 Participants each, or 1 Room of 8 Participants.
- Minor bug fixes related to [OpenVidu Call](https://openvidu.io/3.5/docs/releases/openvidu-call/index.md).

### Known limitations

- When using [mediasoup](https://openvidu.io/3.5/docs/self-hosting/production-ready/performance/index.md):
  - No support for Speaker Detection events ([LiveKit reference](https://docs.livekit.io/transport/media/subscribe/#active-speaker-identification)).
  - No `ConnectionQualityChanged` event ([LiveKit reference](https://docs.livekit.io/intro/basics/rooms-participants-tracks/webhooks-events/#sdk-events)).
  - No support for Dynacast ([LiveKit reference](https://docs.livekit.io/transport/media/advanced/#dynacast)).
  - No support for Adaptive Streaming ([LiveKit reference](https://docs.livekit.io/transport/media/subscribe/#Adaptive-stream)).
- When using [OpenVidu Call](https://openvidu.io/3.5/docs/releases/openvidu-call/docs.md#run-openvidu-locally) against an [OpenVidu Local Deployment](https://openvidu.io/3.5/docs/self-hosting/local/index.md), recordings cannot be accessed.

### Version table

| Artifact               | Version    | Info | Link |
| ---------------------- | ---------- | ---- | ---- |
| livekit/livekit-server | v1.6.0     |      |      |
| mediasoup              | 3.12.16    |      |      |
| livekit/egress         | v1.8.2     |      |      |
| livekit/ingress        | v1.2.0     |      |      |
| MinIO                  | 2024.06.13 |      |      |
| Caddy                  | 2.7.6      |      |      |
| MongoDB                | 7.0.11     |      |      |
| Redis                  | 7.2.5      |      |      |
| Grafana                | 10.3.3     |      |      |
| Prometheus             | 2.50.1     |      |      |
| Promtail / Loki        | 2.8.9      |      |      |
| Mimir                  | 2.11.0     |      |      |

## 3.0.0-beta1

### Version table

| Artifact               | Version    | Info | Link |
| ---------------------- | ---------- | ---- | ---- |
| livekit/livekit-server | v1.6.0     |      |      |
| mediasoup              | 3.12.16    |      |      |
| livekit/egress         | v1.8.2     |      |      |
| livekit/ingress        | v1.2.0     |      |      |
| MinIO                  | 2024.06.13 |      |      |
| Caddy                  | 2.7.6      |      |      |
| MongoDB                | 7.0.11     |      |      |
| Redis                  | 7.2.5      |      |      |
| Grafana                | 10.3.3     |      |      |
| Prometheus             | 2.50.1     |      |      |
| Promtail / Loki        | 2.8.9      |      |      |
| Mimir                  | 2.11.0     |      |      |
