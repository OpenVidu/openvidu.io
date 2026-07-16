## 3.8.0

For the Release Notes of OpenVidu Meet 3.8.0, please visit here: [OpenVidu Meet 3.8.0](https://openvidu.io/3.8.0/meet/releases/#380)

### Changelog

- **mediasoup updates**: all restrictions on using [mediasoup as the RTC engine](https://openvidu.io/3.8.0/docs/self-hosting/production-ready/performance/#about-mediasoup-integration) have been addressed. Previous versions of mediasoup had [several limitations](https://openvidu.io/3.7.0/docs/self-hosting/production-ready/performance/#limitations) that prevented OpenVidu from fully leveraging its capabilities. These have now all been resolved, making mediasoup comparable to Pion in terms of features while delivering the 2x performance boost. Below is the complete list of mediasoup-related improvements:
  - Upgrade mediasoup from v3.19.19 to **v3.19.21** ([changes](https://github.com/versatica/mediasoup/compare/3.19.19...3.19.21) ).
  - [**ConnectionQuality**](https://docs.livekit.io/intro/basics/rooms-participants-tracks/webhooks-events/#connection-quality) events now available in mediasoup.
  - **Screen Share simulcast greatly improved**: layer selection was buggy when screens became static, causing low-quality layers to always take precedence once the screen started moving again. The result was low-resolution screen sharing that was barely legible. This has now been fixed, and simulcast layer selection properly chooses high-quality layers as long as each participant's network bandwidth allows it.
  - **RTX support**: mediasoup now fully supports RTX, the retransmission mechanism that mitigates packet loss in media traffic. This greatly improves video behavior in poor network conditions.
  - **DTX support**: mediasoup now fully implements DTX (Discontinuous Transmission) for Opus audio. This is an important optimization that reduces the audio bitrate when participants are not speaking. It saves up to 90% of the bitrate during silence periods, without affecting speech quality once they start speaking again.
  - Support for **H264**, **VP9**, and **AV1** video codecs: previous versions of mediasoup forced the VP8 video codec due to certain limitations. These issues have now been resolved, so the remaining codecs are allowed.
  - **SVC** in AV1 and VP9: now that mediasoup supports the AV1 and VP9 codecs, SVC (Scalable Video Coding) is also available. SVC is a modern approach to multi-layered video encoding, where a single stream is encoded in multiple qualities and the server forwards only the layers each consumer needs. It is more efficient than simulcast, since the sender encodes just once instead of producing several independent streams.
- **Deployment improvements**:
  - Fixed several race conditions in the deployment process that could end up in a broken deployment.
  - Fixed a rare config synchronization problem caused by a Redis timeout in OpenVidu Elastic and OpenVidu High Availability deployments.
  - If no domain is defined for the OpenVidu deployment, the public IP is now used as the domain instead of [sslip.io](https://sslip.io/) .
  - The Promtail service of OpenVidu's [observability stack](https://openvidu.io/3.8.0/docs/self-hosting/production-ready/observability/) has been replaced by [Alloy](https://grafana.com/docs/alloy/latest/) . Promtail has been deprecated and Alloy is now the recommended log collector for OpenVidu deployments.
  - **Oracle Deployment**: scale-in implemented for OpenVidu Elastic and OpenVidu High Availability. See [Custom scale-in strategy](https://openvidu.io/3.8.0/docs/self-hosting/elastic/oracle/install/#custom-scale-in-strategy) for OpenVidu Elastic in Oracle and [Custom scale-in strategy](https://openvidu.io/3.8.0/docs/self-hosting/ha/oracle/install/#custom-scale-in-strategy) for OpenVidu High Availability in Oracle.
  - **GCP Deployment**: there was a bug in the cron job that triggered the graceful shutdown of the same Media Node multiple times, ultimately causing a forced shutdown of OpenVidu services without waiting for rooms to finish. GCP now properly waits for rooms to finish before shutting down the Media Node. See commit [#82ae32b](https://github.com/OpenVidu/openvidu/commit/82ae32b9fe0865192faaeb8d1a96151a96b2f969) .
  - **Azure Deployment**: fixed a bug in the High Availability deployment that could cause a failed Media Node to never be deleted and re-deployed. See commit [#99d7660](https://github.com/OpenVidu/openvidu/commit/99d76604053219119c8fd15ca23a2d4d0a6fcb3b) .
- **Improved TURN security**: OpenVidu now blocks all private IPs when relaying traffic through the TURN server, except for the known private IPs of each node. On startup, the OpenVidu cluster automatically configures itself, auto-discovering the private IP of each node and allowing private TURN relay traffic only between those specific IPs. This happens automatically, with no need for manual whitelisting. It improves the overall security of the deployment and prevents TURN-relay-abuse attacks. You can learn all about TURN server security here: [TURN server security](https://openvidu.io/3.8.0/docs/self-hosting/how-to-guides/turn-security/).
- **Speech Processing agent**: important fixes to the memory management of [Speech Processing agents](https://openvidu.io/3.8.0/docs/ai/openvidu-agents/speech-processing-agent/). Previously, the agent could enter a memory-consumption loop without freeing memory, which could ultimately cause a memory shortage on the node hosting it. Multiple memory leaks have been addressed, improving the stability of the agent when running for long periods.
- **LiveKit stack updated to v1.12.0**: OpenVidu is now based on LiveKit v1.12.0. See the complete list of changes from the previous supported version here: [v1.9.12 vs v1.12.0](https://github.com/livekit/livekit/compare/v1.9.12...v1.12.0) .
- New configuration property **`advertise_internal_ip`** available in [`livekit.yaml`](https://openvidu.io/3.8.0/docs/self-hosting/configuration/reference/#livekityaml) to enable announcing the private IP in ICE host candidates when `use_external_ip` is true. This allows clients to connect to the OpenVidu deployment from both private and public networks.
- **Fixed nil pointer dereference** in OpenVidu Server that could cause an unexpected crash of the service ([Issue 8](https://github.com/OpenVidu/openvidu-livekit/issues/8) ).
- **openvidu-browser-v2compatibility**: method [Stream.reconnect](https://docs.openvidu.io/en/stable/api/openvidu-browser/classes/Stream.html#reconnect) of OpenVidu v2 API is now wired up to work in OpenVidu v3. You can learn more about updating your OpenVidu v2 web application to work against an OpenVidu v3 deployment in the [OpenVidu v2 compatibility guide](https://docs.openvidu.io/en/stable/openvidu3/#2-update-your-application) .

### Version table

| Artifact               | Version                                                                        | Info | Link |
| ---------------------- | ------------------------------------------------------------------------------ | ---- | ---- |
| livekit/livekit-server | v1.12.0                                                                        |      |      |
| mediasoup              | 3.19.21                                                                        |      |      |
| livekit/egress         | v1.12.0 (commit [#783a287](https://github.com/livekit/egress/commit/783a287) ) |      |      |
| livekit/ingress        | v1.5.0 (commit [#2ce1b32](https://github.com/livekit/ingress/commit/2ce1b32) ) |      |      |
| livekit/agents         | v1.6.4                                                                         |      |      |
| MinIO                  | 2026-06-04T00-54-11Z                                                           |      |      |
| Caddy                  | 2.11.4                                                                         |      |      |
| MongoDB                | 8.0.26                                                                         |      |      |
| Redis                  | 8.6.4                                                                          |      |      |
| Grafana                | 12.4.4                                                                         |      |      |
| Prometheus             | 3.12.0                                                                         |      |      |
| Mimir                  | 3.1.0                                                                          |      |      |
| Alloy                  | 1.17.0                                                                         |      |      |
| Loki                   | 3.7.2                                                                          |      |      |

## 3.7.0

For the Release Notes of OpenVidu Meet 3.7.0, please visit here: [OpenVidu Meet 3.7.0](https://openvidu.io/3.7.0/meet/releases/#370)

### Changelog

- **Scale in for Digital Ocean deployments**: OpenVidu Elastic and OpenVidu High Availability in Digital Ocean now support graceful scale-in operations, allowing you to reduce the number of Media Nodes when they are not needed. You can learn more about our scale-in strategies here:
  - [Custom scale-in strategy for Digital Ocean in OpenVidu Elastic](https://openvidu.io/3.7.0/docs/self-hosting/elastic/digitalocean/install/#custom-scale-in-strategy).
  - [Custom scale-in strategy for Digital Ocean in OpenVidu High Availability](https://openvidu.io/3.7.0/docs/self-hosting/ha/digitalocean/install/#custom-scale-in-strategy).
- **Oracle Cloud Infrastructure support**: OpenVidu can now be deployed in Oracle Cloud Infrastructure (OCI) using our new Terraform templates. For now we only support Single Node deployments in OCI, but planning to support Elastic and High Availability deployments soon.
  - [OpenVidu Single Node COMMUNITY](https://openvidu.io/3.7.0/docs/self-hosting/single-node/oracle/install/) in OCI.
  - [OpenVidu Single Node PRO](https://openvidu.io/3.7.0/docs/self-hosting/single-node-pro/oracle/install/) in OCI.
- **LiveKit stack updated to v1.9.12**: OpenVidu is now based on LiveKit v1.9.12, which includes multiple improvements and bug fixes in the core media processing engine. For more details, check the [LiveKit v1.9.12 release notes](https://github.com/livekit/livekit/releases/tag/v1.9.12) .
- **Ingress updated to latest**: the Ingress service has been updated to recent commit [#cfbaa74](https://github.com/livekit/ingress/commit/cfbaa74) with multiple improvements and bug fixes over last official release.
- **mediasoup upgrade to latest**: mediasoup has been upgraded to recent version [**3.19.19**](https://github.com/versatica/mediasoup/releases/tag/3.19.19) . OpenVidu PRO has been stuck in mediasoup 3.12.16 since 2023 due to some compatibility issues within our middlewares. We have now overcome those limitations and we are able to upgrade to a recent mediasoup version, which includes almost 3 years of improvements and bug fixes. You can learn more about mediasoup integration in OpenVidu here: [About mediasoup integration](https://openvidu.io/3.7.0/docs/self-hosting/production-ready/performance/#about-mediasoup-integration).
- **S3 Server-Side Encryption for external S3 buckets**: all OpenVidu deployments rely on S3 storage to store recordings and configurations. Every OpenVidu deployment comes with an embedded S3 storage based on Minio, but you can also configure an external S3 bucket if you prefer. Now OpenVidu supports Server-Side Encryption (SSE) for these external S3 storages, which means that all your data stored in S3 can be encrypted at rest. Learn how to enable it here: [Server-side encryption](https://openvidu.io/3.7.0/docs/self-hosting/how-to-guides/external-s3/#server-side-encryption).
- **Support for chained version upgrades**: OpenVidu now supports chained version upgrades, which means that you can upgrade from any previous version to 3.7.0 directly in a single command, without having to upgrade to intermediate versions first. This also applies to any future versions of OpenVidu. Check out the Upgrade documentation for your specific deployment:
  - [OpenVidu Single Node COMMUNITY](https://openvidu.io/3.7.0/docs/self-hosting/single-node/)
  - [OpenVidu Single Node PRO](https://openvidu.io/3.7.0/docs/self-hosting/single-node-pro/)
  - [OpenVidu Elastic](https://openvidu.io/3.7.0/docs/self-hosting/elastic/)
  - [OpenVidu High Availability](https://openvidu.io/3.7.0/docs/self-hosting/ha/)
- **Updated chainguard MinIO fork fixing recent CVEs**:
  - MinIO is Vulnerable to SSE Metadata Injection via Replication Headers: [CVE-2026-34204](https://github.com/advisories/GHSA-3rh2-v3gr-35p9)
  - MinIO affected a DoS via Unbounded Memory Allocation in S3 Select CSV Parsing: [CVE-2026-39414](https://github.com/advisories/GHSA-h749-fxx7-pwpg)
  - MinIO LDAP login brute-force via user enumeration and missing rate limit: [CVE-2026-33419](https://github.com/advisories/GHSA-jv87-32hw-hh99)
- **Bug fixes in v2compatibility module**:
  - A wrong S3 directory was being used.
  - Track leak when using method [`replaceTrack`](https://docs.openvidu.io/en/stable/api/openvidu-browser/classes/Publisher.html#replacetrack) : fixed an issue where this method did not stop the previous existing track, causing resource leaks. This could lead to media resource exhaustion on mobile devices and trigger unexpected mute events.

### Version table

| Artifact               | Version                                                                        | Info | Link |
| ---------------------- | ------------------------------------------------------------------------------ | ---- | ---- |
| livekit/livekit-server | v1.9.12                                                                        |      |      |
| mediasoup              | 3.19.19                                                                        |      |      |
| livekit/egress         | v1.12.0 (commit [#ba781b4](https://github.com/livekit/egress/commit/ba781b4) ) |      |      |
| livekit/ingress        | v1.4.3 (commit [#cfbaa74](https://github.com/livekit/ingress/commit/cfbaa74) ) |      |      |
| livekit/agents         | v1.4.4                                                                         |      |      |
| MinIO                  | 2026-05-04T00-27-21Z                                                           |      |      |
| Caddy                  | 2.11.2                                                                         |      |      |
| MongoDB                | 8.0.21                                                                         |      |      |
| Redis                  | 8.6.2                                                                          |      |      |
| Grafana                | 12.3.6                                                                         |      |      |
| Prometheus             | 3.11.3                                                                         |      |      |
| Promtail / Loki        | 3.5.12                                                                         |      |      |
| Mimir                  | 3.0.6                                                                          |      |      |

## 3.6.0

For the Release Notes of OpenVidu Meet 3.6.0, please visit here: [OpenVidu Meet 3.6.0](https://openvidu.io/3.6.0/meet/releases/#360)

### Changelog

- **DigitalOcean support**: we continue expanding our cloud-native deployment options. OpenVidu now officially supports deployments in DigitalOcean using its native resources (Droplets, Spaces, Load Balancers...) through our new Terraform templates:

  - [OpenVidu Single Node COMMUNITY](https://openvidu.io/3.6.0/docs/self-hosting/single-node/digitalocean/install/) in DigitalOcean.
  - [OpenVidu Single Node PRO](https://openvidu.io/3.6.0/docs/self-hosting/single-node-pro/digitalocean/install/) in DigitalOcean.
  - [OpenVidu Elastic](https://openvidu.io/3.6.0/docs/self-hosting/elastic/digitalocean/install/) in DigitalOcean.
  - [OpenVidu High Availability](https://openvidu.io/3.6.0/docs/self-hosting/ha/digitalocean/install/) in DigitalOcean.

  Info

  **OpenVidu Elastic** and **OpenVidu High Availability** do not support [autoscaling](https://openvidu.io/3.6.0/docs/self-hosting/production-ready/scalability/#autoscaling) in release 3.6.0. This is a work in progress and will be available in a future release.

- **Plain Docker Compose deployment**: OpenVidu Single Node COMMUNITY can now be deployed using a plain Docker Compose. This is an installer-free, less opinionated deployment option, friendlier with GitOps procedures. See [Plain Docker Compose installation](https://openvidu.io/3.6.0/docs/self-hosting/single-node/on-premises/install/#plain-docker-compose-installation) for more details.

- **Local providers for Live Captions**: the [Live Captions](https://openvidu.io/3.6.0/docs/ai/live-captions/) service now supports [local providers](https://openvidu.io/3.6.0/docs/ai/live-captions/#local-providers) that will run in your own nodes, offline, without the need of configuring and paying a third-party service. This greatly aligns with the self-hosted, private nature of OpenVidu deployments. Currently we support:

  - [Vosk](https://github.com/alphacep/vosk-api): available in OpenVidu COMMUNITY deployments, it supports multiple languages and can run on modest hardware.
  - [Sherpa](https://github.com/k2-fsa/sherpa-onnx): available in OpenVidu PRO deployments, it offers state-of-the-art accuracy and performance. It also offers GPU acceleration if your Media Nodes are equipped with an NVIDIA GPU.

- **New cloud providers for Live Captions**: we have also expanded the collection of supported third-party AI [cloud providers](https://openvidu.io/3.6.0/docs/ai/live-captions/#cloud-providers): [MistralAI](https://mistral.ai/), [NVIDIA Riva](https://www.nvidia.com/en-us/ai-data-science/products/riva/), [Spitch](https://spitch.app/), [ElevenLabs](https://elevenlabs.io/), [Simplismart](https://simplismart.ai/).

- **Deployment improvements**

  - It is now possible to deploy a custom application on the same host as OpenVidu Single Node and serve it directly at the root path `/`. Learn how to do it [here](https://openvidu.io/3.6.0/meet/embedded/deploy-your-app/#deploy-alongside-openvidu).
  - OpenVidu now supports restricted-network deployments (for example, NAT environments) for both internal and external clients out of the box. Before, clients connecting from the same network where OpenVidu was deployed could experience connection issues. Now, OpenVidu handles these scenarios transparently.
  - OpenVidu now works out of the box in networks without hairpinning NAT support (where a host cannot reach itself through its public IP).
  - TURN relay security has been hardened to reduce exposure to SSRF-style abuse. Learn more: [TURN server security threats](https://www.enablesecurity.com/blog/turn-server-security-threats/) .
  - The deployment flows for **Azure** and **GCP** include multiple stability fixes, as well as corrections to minor typos and configuration issues that could affect the installation process.

- **Egress improvements**

  - Egress containers now check available disk space before accepting new requests, preventing immediate failures on full disks ([#3478328](https://github.com/OpenVidu/egress/commit/3478328cae4553b066552c01b37b7761455c990c) ).
  - On crash recovery, egress now preserves backup recordings by copying `/home/egress/tmp/` to `/home/egress/backup_storage/` before cleanup ([#3dbd892](https://github.com/OpenVidu/egress/commit/3dbd8923d746bc897c3b522de1594582be689292) ).
  - `cpu_cost.max_cpu_utilization` now applies to the first egress request as well ([#f0cef66](https://github.com/OpenVidu/egress/commit/f0cef66e4d1f5c1654cd83d938bbcd69c7305782) ). Before this fix, the first request handled by any egress instance would always be accepted regardless of the current CPU load, potentially leading to overloading an already busy Media Node. This fix improves the stability of egresses in clusters under high load.
  - CPU monitoring now considers host-wide utilization (not only egress subprocesses), improving egress distribution across nodes ([#387e600](https://github.com/OpenVidu/egress/commit/387e600c781c931a3e16fd9096472b7117723328) ).
  - Room Composite Egress now works correctly in restricted NAT deployments.

### Breaking changes

- **OpenVidu Meet default path has changed**: the default path for OpenVidu Meet is now `/meet` (previously `/`). You can revert to the previous behavior by following [these instructions](https://openvidu.io/3.6.0/docs/self-hosting/how-to-guides/customize-meet-base-path/#root-path).

### Version table

| Artifact               | Version                                                                        | Info | Link |
| ---------------------- | ------------------------------------------------------------------------------ | ---- | ---- |
| livekit/livekit-server | v1.9.8                                                                         |      |      |
| mediasoup              | 3.12.16                                                                        |      |      |
| livekit/egress         | v1.12.0 (commit [#ba781b4](https://github.com/livekit/egress/commit/ba781b4) ) |      |      |
| livekit/ingress        | v1.4.3 (commit [#e42b67a](https://github.com/livekit/ingress/commit/e42b67a) ) |      |      |
| livekit/agents         | v1.4.4                                                                         |      |      |
| MinIO                  | 2025.10.15                                                                     |      |      |
| Caddy                  | 2.11.1                                                                         |      |      |
| MongoDB                | 8.0.19                                                                         |      |      |
| Redis                  | 8.6.1                                                                          |      |      |
| Grafana                | 12.3.4                                                                         |      |      |
| Prometheus             | 3.9.1                                                                          |      |      |
| Promtail / Loki        | 3.5.11                                                                         |      |      |
| Mimir                  | 3.0.3                                                                          |      |      |

### Patch releases

#### 3.6.1

- **Global cpu monitoring for room allocation**: now OpenVidu will consider host-wide CPU load when deciding where to allocate new Rooms, instead of checking only sub-processes CPU load. This optimizes load distribution across all nodes of your cluster. You can learn more about how Rooms are allocated [here](https://openvidu.io/3.6.1/docs/self-hosting/production-ready/scalability/#rooms).

- **New Troubleshooting recording documentation**: there is now a dedicated section to guide users on how to debug and solve common problems. Starting with [recordings](https://openvidu.io/3.6.1/docs/troubleshooting/recording/).

- **Angular Components**: in recent versions of Firefox, it is no longer allowed to create a new screen track if one is already active, which prevents replacing the shared screen without first unpublishing it. As a result, the UI now automatically adapts when Firefox is detected, avoiding the use of screen replacement (replaceTrack) and instead aligning with the constraints imposed by the browser. See [Angular Components](https://openvidu.io/3.6.1/docs/ui-components/angular-components/).

- **OpenVidu Meet**: optimized lock management by significantly reducing the number of Redis keys, minimizing read and write operations, lowering memory usage, improving TTLs for key deletion, and simplifying the overall system design.

- **Artifact version updates**:

  | Artifact | Version                      | Info | Link |
  | -------- | ---------------------------- | ---- | ---- |
  | MinIO    | RELEASE.2026-03-04T16-04-53Z |      |      |
  | Mimir    | 3.0.4                        |      |      |

## 3.5.0

For the Release Notes of OpenVidu Meet 3.5.0, please visit here: [OpenVidu Meet 3.5.0](https://openvidu.io/3.5.0/meet/releases/#350)

### Changelog

- **ARM support**: OpenVidu can now be deployed in ARM-based systems. This broadens the range of instances in which OpenVidu can be deployed, offering new opportunities and alternatives that may be more cost-effective. To deploy OpenVidu in ARM architecture, you don't have to do anything special: just follow the default installation instructions for your desired OpenVidu deployment type. The installer will automatically detect the architecture and set up the appropriate services.
- **Google Cloud Platform support for all OpenVidu deployments**: we continue to expand our cloud-native deployment options. Now you can deploy [OpenVidu Single Node PRO](https://openvidu.io/3.5.0/docs/self-hosting/single-node-pro/gcp/install/), [OpenVidu Elastic](https://openvidu.io/3.5.0/docs/self-hosting/elastic/gcp/install/) and [OpenVidu High Availability](https://openvidu.io/3.5.0/docs/self-hosting/ha/gcp/install/) in Google Cloud Platform using Terraform templates.
- **LiveKit stack updated to v1.9.8**: OpenVidu is now based on LiveKit v1.9.8, bringing all bug fixes and improvements since version v1.9.0. You can find the [release notes here](https://github.com/livekit/livekit/releases/tag/v1.9.8) .
  - Particularly relevant is the fix for [issue #3858](https://github.com/livekit/livekit/issues/3858), which fixes a fatal problem in the connection of the services with the Redis Cluster.
- **Egress updated to v1.12.0**: the Egress service has been updated to v1.12.0, which includes several improvements and bug fixes when exporting media from rooms. You can find the [release notes here](https://github.com/livekit/egress/releases/tag/v1.12.0) .
  - Particularly relevant is the change of the `unhealthyShutdownWatchdogDelay` value from 20 seconds to 10 minutes (see [commit e86593c](https://github.com/OpenVidu/egress/commit/e86593c25ab20e02d8e6d4a2edc4ac4b03fd2dbc)), preventing premature termination of egress processes under high CPU load or poor network conditions.
- **Ingress updated to latest**: the Ingress service has been updated to latest available commit *[#e42b67a](https://github.com/OpenVidu/ingress/commit/e42b67acf7d2c1ca5b463bb0d8f71bc4f6bf26c5)* with multiple improvements over last official release.
- **Live Captions**:
  - Fixed critical bug that caused slow response when transcribing 3 or more simultaneous participants in the same Room using AWS Transcribe provider. See related issue in the official LiveKit Agents repository ([#3739](https://github.com/livekit/agents/issues/3739)) and PR fixing it ([PR 4111](https://github.com/livekit/agents/pull/4111)).
  - Added [Cartesia](https://cartesia.ai/sonic) and [Soniox](https://soniox.com/) to the list of [supported AI providers](https://openvidu.io/3.5.0/docs/ai/live-captions/#supported-ai-providers).
  - [Interim transcriptions](https://openvidu.io/3.5.0/docs/ai/live-captions/#final-vs-interim-transcriptions) now available for existing [AI providers](https://openvidu.io/3.5.0/docs/ai/live-captions/#supported-ai-providers) Speechmatics and Gladia.
- **MongoDB**: OpenVidu now allows [configuring an external MongoDB](https://openvidu.io/3.5.0/docs/self-hosting/how-to-guides/external-mongodb/) instead of using the bundled one, or you can choose to completely [disable the use of MongoDB](https://openvidu.io/3.5.0/docs/self-hosting/how-to-guides/enable-disable-mongodb/) if your use case can do without services that require a database.
- **New backup and restore documentation for OpenVidu deployments**: we have carefully crafted a new [how-to guide](https://openvidu.io/3.5.0/docs/self-hosting/how-to-guides/backup-and-restore/) explaining how to migrate your existing persistent data (recordings, analytics, monitoring data, etc.) when upgrading or changing your OpenVidu deployment. This process mainly affects the MongoDB and S3 services, responsible for persisting data in OpenVidu deployments.
- **OpenVidu Angular Components updated to support Angular v20**: the [OpenVidu Angular Components library](https://openvidu.io/3.5.0/docs/ui-components/angular-components/) can now be used in applications built with Angular v20.
- **Time Zone fix**: OpenVidu deployments now honor their host time zone by default. Previously OpenVidu always used UTC. This proved a challenge when integrating OpenVidu with a custom app using local time zone. You can revert to UTC by providing the additional installation flag `--forceUTCTimezone`.
- **Oracle (OCI) Single Node and Single Node PRO installation tutorials**: we have created detailed step-by-step guides to help you deploy [OpenVidu Single Node COMMUNITY](https://openvidu.io/3.5.0/docs/self-hosting/single-node/oci/install/) and [OpenVidu Single Node PRO](https://openvidu.io/3.5.0/docs/self-hosting/single-node-pro/oci/install/) in Oracle Cloud Infrastructure using its native resources.

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

For the Release Notes of OpenVidu Meet 3.4.0, please visit here: [OpenVidu Meet 3.4.0](https://openvidu.io/3.4.0/meet/releases/#340)

### Changelog

- **LiveKit stack updated to v1.9.0**: OpenVidu is now based on LiveKit v1.9.0, which includes several improvements and bug fixes. You can find the [release notes here](https://github.com/livekit/livekit/releases/tag/v1.9.0) .
- **Egress updated to v1.10.0**: the Egress service has been updated to v1.10.0, which includes several improvements and bug fixes when exporting media from rooms. You can find the [release notes here](https://github.com/livekit/egress/releases/tag/v1.10.0) .
- **OpenVidu Single Node native deployment in Google Cloud Platform (GCP)**: you can now deploy OpenVidu Single Node in GCP using its native resources thanks to our new Terraform template. Follow the [GCP deployment guide](https://openvidu.io/3.4.0/docs/self-hosting/single-node/gcp/install/). Templates for OpenVidu Elastic and OpenVidu High Availability in GCP are coming soon.
- **No need for a domain name to deploy OpenVidu in production**: thanks to [sslip.io](https://sslip.io/) integration, you can now deploy OpenVidu in production with a valid SSL certificate without owning a custom domain name. Just deploy OpenVidu 3.4.0 and skip the domain name configuration during the installation process: OpenVidu will automatically detect your public IP and provide a secure domain name using sslip.io.
- **OpenVidu agents new configurations**: configure a custom CPU threshold to accept new jobs, and modify the agent's log level. See [Change CPU load threshold](https://openvidu.io/3.4.0/docs/ai/openvidu-agents/speech-processing-agent/#change-cpu-load-threshold) and [Log level](https://openvidu.io/3.4.0/docs/ai/openvidu-agents/speech-processing-agent/#log-level).
- **Custom AI agents now natively support [graceful shutdown](https://openvidu.io/3.4.0/docs/ai/custom-agents/#elasticity-and-graceful-shutdowns)**, ensuring no interruptions in the services provided by your custom agents when your OpenVidu cluster scales down.
- **OpenVidu Dashboard optimizations**: the addition of several new search indexes to the database has significantly improved the response time of the [OpenVidu Dashboard](https://openvidu.io/3.4.0/docs/self-hosting/production-ready/observability/openvidu-dashboard/) when loading historical data.
- Fixed bug that caused empty `participantInfo` object when receiving [transcription events](https://openvidu.io/3.4.0/docs/ai/live-captions/#how-to-receive-live-captions-in-your-frontend-application) using the Speech Processing agent. This fix was also contributed to LiveKit open source ([PR 3735](https://github.com/livekit/livekit/pull/3735) ).
- **New load balancing strategy for Egress**: egresses were previously distributed across Media Nodes using a "binpack" strategy (trying to fill up one node before using the next one). This could lead to unbalanced CPU usage across nodes in certain scenarios. There is now a new load balancing strategy called "cpuload" that prioritizes nodes with lower CPU usage, leading to a more balanced cluster in terms of CPU utilization. This is now the default strategy. Learn how to configure it [here](https://openvidu.io/3.4.0/docs/self-hosting/production-ready/scalability/#egress).
- **Egress ability to auto kill processes under high CPU load can be disabled**: by default, if an egress detects a high CPU load (>95%) during a sustained period of time (10 seconds), the parent process automatically kills the most consuming egress. This helps preventing it from affecting the performance of other processes in the same Media Node. This default behavior can be now disabled if necessary. Learn how to do so [here](https://openvidu.io/3.4.0/docs/self-hosting/production-ready/scalability/#egress-cpu-overload-killer).
- **Extended scalability documentation**: we have improved our [scalability documentation](https://openvidu.io/3.4.0/docs/self-hosting/production-ready/scalability/) explaining in detail how OpenVidu handles Room, Egress, Ingress and Agent allocation in multi-node deployments. All load balancing strategies and how to configure them are now explained in depth.
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

- **OpenVidu Meet**: update authentication methods to use header-based tokens instead of cookies. When [embedding OpenVidu Meet](https://openvidu.io/3.4.0/meet/embedded/intro/), the strategy (`SameSite=Strict`) was causing issues when loading the application and the embedable component from different domains. Using the most permissive cookie policy available (`SameSite=None`) still caused issues in some browsers that block third-party cookies by default. Now OpenVidu Meet avoids cookies and instead uses header-based tokens for authentication, which is more reliable and secure. See [commit 4e80b5a](https://github.com/OpenVidu/openvidu-meet/commit/4e80b5a060c1ae0f8942527dbdc6ee221992caab) .
- **OpenVidu Elastic & High Availability deployments**: Egress/Ingress/Agents services in Media Nodes were not able to reach the LiveKit API when the local OpenVidu server was down or unresponsive. Now all of these services are properly configured to reach any Media Node in the cluster, ensuring fault tolerance upon OpenVidu server failures.

## 3.3.0

### Changelog

- **AI Services**: OpenVidu now supports a catalog of AI services that can be easily integrated into your application to enhance the user experience and add advanced features. These services are delivered through **OpenVidu agents**: a set of pre-configured and ready-to-use AI modules that seamlessly integrate into your Rooms.

  We are starting with the **Speech Processing agent**: it focuses on transcribing audio speech to text and processing the results in various ways. Currently offering the [**Live Captions**](https://openvidu.io/3.3.0/docs/ai/live-captions/) service, which generates live captions for your users' speech with great accuracy to display them in your frontend application. The Live Captions service supports many leading AI providers, such as OpenAI, Google, Azure, Amazon and more (see [Supported AI providers](https://openvidu.io/3.3.0/docs/ai/live-captions/#supported-ai-providers)).

  Of course, you can also implement your own custom agents using the powerful [LiveKit Agents framework](https://docs.livekit.io/agents/) and deploy it along your OpenVidu deployment. Any LiveKit agent is compatible with OpenVidu. Learn how to do so [here](https://openvidu.io/3.3.0/docs/ai/custom-agents/).

- **Use a single domain for your deployment (EXPERIMENTAL)**: OpenVidu deployments now support TURN with TLS without an additional Domain Name using the flag `--experimental-turn-tls-with-main-domain`. This is great for production deployments, as it allows you to use a single domain and still support users behind restrictive firewalls.

  You can deploy any OpenVidu deployment with this feature enabled:

  - **On Premises**: perform a *non-interactive* installation passing the flag. How to perform a non-interactive installation for each OpenVidu deployment: [OpenVidu Single Node COMMUNITY](https://openvidu.io/3.3.0/docs/self-hosting/single-node/on-premises/install/#non-interactive-installation), [OpenVidu Single Node PRO](https://openvidu.io/3.3.0/docs/self-hosting/single-node-pro/on-premises/install/#non-interactive-installation), [OpenVidu Elastic](https://openvidu.io/3.3.0/docs/self-hosting/elastic/on-premises/install/#non-interactive-installation), [OpenVidu High Availability with DNS](https://openvidu.io/3.3.0/docs/self-hosting/ha/on-premises/install-dlb/#non-interactive-installation), [OpenVidu High Availability with NLB](https://openvidu.io/3.3.0/docs/self-hosting/ha/on-premises/install-nlb/#non-interactive-installation).
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

- **OpenVidu Single Node PRO**: OpenVidu Single Node PRO is a new type of OpenVidu deployment targeting users that want to deploy OpenVidu as a single-node setup, but that still want the [2x performance boost](https://openvidu.io/3.2.0/docs/self-hosting/production-ready/performance/) and the [advanced observability](https://openvidu.io/3.2.0/docs/self-hosting/production-ready/observability/) provided by multi-node OpenVidu PRO deployments.

- **Azure deployments (Beta)**: OpenVidu now supports native deployments in Microsoft Azure. You can now deploy [OpenVidu Single Node COMMUNITY](https://openvidu.io/3.2.0/docs/self-hosting/single-node/azure/install/), [OpenVidu Single Node PRO](https://openvidu.io/3.2.0/docs/self-hosting/single-node-pro/azure/install/), [OpenVidu Elastic](https://openvidu.io/3.2.0/docs/self-hosting/elastic/azure/install/) and [OpenVidu High Availability](https://openvidu.io/3.2.0/docs/self-hosting/ha/azure/install/) in Azure using ARM templates. *During version 3.2.0, Azure deployments will be considered in Beta*.

- **New Azure recording tutorials**: OpenVidu deployments in Azure use Azure Blob Storage to store recordings (instead of S3). For this reason, we have extended our recording tutorials with Azure Blob Storage compatible examples. You can find them in the following links:

  - [Recording Basic Azure](https://openvidu.io/3.2.0/docs/tutorials/advanced-features/recording-basic-azure/).
  - [Recording Advanced Azure](https://openvidu.io/3.2.0/docs/tutorials/advanced-features/recording-advanced-azure/).

- **External proxy configuration**: By default, OpenVidu is deployed with an internal [Caddy server](https://caddyserver.com/) to configure and manage SSL certificates. However, there are certain scenarios where using an external proxy might be preferable:

  - You wish to manage SSL certificates manually.
  - A specific proxy server is required for enhanced security.
  - You need to integrate a proxy server already in your infrastructure.

  For any of these cases, now all OpenVidu deployments allow configuring external proxies. You can find the instructions to do so in [this how-to guide](https://openvidu.io/3.2.0/docs/self-hosting/how-to-guides/deploy-with-external-proxy/).

- **LiveKit stack updated to v1.8.4**: OpenVidu 3.2.0 is now based on LiveKit v1.8.4, which includes several improvements and bug fixes. You can find the [release notes here](https://github.com/livekit/livekit/releases/tag/v1.8.4).

- **OpenVidu installer improvements**: Some users have reported issues when installing OpenVidu, which were finally caused by old versions of Docker and/or Docker Compose. The OpenVidu installer now checks both versions and displays a descriptive error message if they are incompatible.

- **OpenVidu Angular Components**: see [Angular Components documentation](https://openvidu.io/3.2.0/docs/ui-components/angular-components/).

  - Virtual Backgrounds improvements: More efficient use of resources by reusing the existing context. Avoid video flickering when changing the background. Improved resource reallocation management for smoother rendering. Contribution to LiveKit’s track-processors-js package ([PR 86](https://github.com/livekit/track-processors-js/pull/86)) resolving an issue affecting its dependencies.
  - Fixed panel reopening issue with [`ovAdditionalPanels`](https://openvidu.io/3.2.0/docs/reference-docs/openvidu-components-angular/directives/AdditionalPanelsDirective.html) directive. Custom panels created with `ovAdditionalPanels` would not reopen correctly after switching between default panels (activities, participants or chat). Now, returning to a custom panel restores it as expected without closing all panels.
  - Minor style fixes.

- **Deployment bug fixes**:

  - OpenVidu On Premises deployments that made use of [v2compatibility module](https://docs.openvidu.io/en/stable/openvidu3/#updating-from-openvidu-v2-to-openvidu-v3) had a wrong configuration affecting the S3 MinIO bucket. This could cause issues when recording sessions from your OpenVidu v2 application. This is now fixed.
  - Wrong Caddy configuration in OpenVidu High Availability deployments made some services not reachable in specific scenarios of fault tolerance. This is now fixed.

### Breaking changes

- For OpenVidu On Premises deployments, the default S3 bucket in MinIO has been renamed from `app-data` to `openvidu-appdata` (in Single Node and Elastic deployments) and from `cluster-data` to `openvidu-clusterdata` (in High Availability deployments).
- Port rules in [OpenVidu High Availability with Network Load Balancer](https://openvidu.io/3.2.0/docs/self-hosting/ha/on-premises/install-nlb/) have changed. Check the port rules from the installation instructions.

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

- **IP cameras support**: OpenVidu now allows you to connect RTSP IP cameras to your Rooms. This feature has been included in our custom fork of the [Ingress](https://docs.livekit.io/home/ingress/overview/) module, which is used to ingest media into a Room. Check out how to do it [here](https://openvidu.io/3.1.0/docs/developing-your-openvidu-app/how-to/#ip-cameras). IP cameras support has also been included into the **v2 compatibility module**. This means that if your OpenVidu 2 application is using the [IP cameras feature](https://docs.openvidu.io/en/stable/advanced-features/ip-cameras/), you can now upgrade your deployment to OpenVidu 3 and keep using this feature.
- **OpenVidu Updater**: you can now update the version of your OpenVidu deployment very easily using our new OpenVidu Updater module. OpenVidu Updater will take care of the whole process, from stopping the services to updating the configuration files. It will also manage backups to allow rollbacks in case of any issue. You can update your OpenVidu deployment from 3.0.0 to 3.1.0:
  - Update your **OpenVidu On Premises** deployment: [Update OpenVidu Single Node](https://openvidu.io/3.1.0/docs/self-hosting/single-node/on-premises/upgrade/), [Update OpenVidu Elastic](https://openvidu.io/3.1.0/docs/self-hosting/elastic/on-premises/upgrade/), [Update OpenVidu High Availability](https://openvidu.io/3.1.0/docs/self-hosting/ha/on-premises/upgrade/).
  - Update your **OpenVidu AWS** deployment: for AWS deployment we recommend updating from 3.0.0 to 3.1.0 by redeploying the CloudFormation. From 3.1.0 onwards OpenVidu Updater will also be able to seamlessly update your AWS deployment.
- **mediasoup stability**: we believe we have reached the right point of maturity to take [mediasoup](https://openvidu.io/3.1.0/docs/self-hosting/production-ready/performance/) as the internal RTC engine from experimental to production ready. There are still some [limitations](https://openvidu.io/3.1.0/docs/self-hosting/production-ready/performance/#limitations) to take into account, but the general stability of the system is now considered production ready.
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

- When using [mediasoup](https://openvidu.io/3.0.0/docs/self-hosting/production-ready/performance/):
  - No `ConnectionQualityChanged` event ([LiveKit reference](https://docs.livekit.io/home/client/events/#Events)).
  - No `TrackStreamStateChanged` event ([LiveKit reference](https://docs.livekit.io/home/client/events/#Events)).
  - Limited [ingress](https://docs.livekit.io/home/ingress/overview/) support: non-simulcast video tracks are not supported. Firefox may experience issues when subscribing to ingress video.

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

- Centralized configuration: OpenVidu now automatically manages and synchronizes the configuration of all its components. This means that updating any configuration parameter in multi-node deployments ([OpenVidu Elastic](https://openvidu.io/3.0.0/docs/self-hosting/deployment-types/#openvidu-elastic) and [OpenVidu High Availability](https://openvidu.io/3.0.0/docs/self-hosting/deployment-types/#openvidu-high-availability)) is as simple as updating the required file in a single node. OpenVidu handles the distribution and restart of the affected services across all nodes. See how easily you can change the configuration [here](https://openvidu.io/3.0.0/docs/self-hosting/configuration/changing-config/).
- [mediasoup](https://openvidu.io/3.0.0/docs/self-hosting/production-ready/performance/) support:
  - Dynacast is now supported ([LiveKit reference](https://docs.livekit.io/home/client/tracks/publish/#Dynamic-broadcasting)).
  - Adaptive Streaming is now supported ([LiveKit reference](https://docs.livekit.io/home/client/tracks/subscribe/#Adaptive-stream)).
  - Speaker Detection events ([LiveKit reference](https://docs.livekit.io/home/client/tracks/subscribe/#Speaker-detection)).
  - Server API method `MutePublishTrack` ([LiveKit reference](https://docs.livekit.io/reference/server/server-apis/#MutePublishedTrack)).
  - Client API method `RemoteTrackPublication.setEnabled` ([LiveKit JS reference](https://docs.livekit.io/client-sdk-js/classes/RemoteTrackPublication.html#setEnabled)).
- [OpenVidu Call](https://openvidu.io/3.0.0/docs/openvidu-call/docs/#run-openvidu-locally):
  - When using it against an [OpenVidu Local Deployment](https://openvidu.io/3.0.0/docs/self-hosting/local/), recordings couldn't be accessed from the application's frontend. This is now fixed and OpenVidu Call is able to access recordings.
  - There was an error when applying Virtual Backgrounds ("No camera tracks found. Cannot apply background"). This is now fixed.
  - Docker image [openvidu/openvidu-call](https://hub.docker.com/r/openvidu/openvidu-call) is now 50% smaller.
- [OpenVidu v2 compatibility](https://docs.openvidu.io/en/stable/openvidu3/#updating-from-openvidu-v2-to-openvidu-v3):
  - There was a race condition when multiple participants connected to the Session at the same time that could cause remote [`streamCreated`](https://docs.openvidu.io/en/stable/api/openvidu-browser/classes/StreamEvent.html) events to not be triggered. This is now fixed.
  - Configuration parameter `V2COMPAT_OPENVIDU_PRO_AWS_S3_BUCKET` did not allow configuring sub-buckets ("openvidu" worked fine, but "openvidu/subbucket" did not). Now it is possible to do so.
  - The operation to list recordings (available for [REST API](https://docs.openvidu.io/en/stable/reference-docs/REST-API/#get-all-recordings), [openvidu-java-client](<https://docs.openvidu.io/en/stable/api/openvidu-java-client/io/openvidu/java/client/OpenVidu.html#listRecordings()>), [openvidu-node-client](https://docs.openvidu.io/en/stable/api/openvidu-node-client/classes/OpenVidu.html#listRecordings)) was limited to 1000 recordings. This is now fixed and all recordings are always returned.
- AWS deployments: all secrets are now synchronized with [AWS Secrets Manager](https://console.aws.amazon.com/secretsmanager). You can update any secret from the AWS console and restart your cluster for them to have immediate effect in all your nodes. This is also true in reverse: you can update any secret inside your node, and after restarting the cluster, the values in AWS Secrets Manager will be properly synchronized.
- New application tutorials available: [iOS](https://openvidu.io/3.0.0/docs/tutorials/application-client/ios/), [Android](https://openvidu.io/3.0.0/docs/tutorials/application-client/android/), [Recording](https://openvidu.io/3.0.0/docs/tutorials/advanced-features/).

### Known limitations

- When using [mediasoup](https://openvidu.io/3.0.0/docs/self-hosting/production-ready/performance/):
  - No `ConnectionQualityChanged` event ([LiveKit reference](https://docs.livekit.io/home/client/events/#Events)).
  - No `TrackStreamStateChanged` event ([LiveKit reference](https://docs.livekit.io/home/client/events/#Events)).

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

- Improved [mediasoup](https://openvidu.io/3.0.0/docs/self-hosting/production-ready/performance/) support:
  - Data messages work ([LiveKit reference](https://docs.livekit.io/home/client/data/#Data-messages)).
  - Ingress supported ([LiveKit reference](https://docs.livekit.io/home/ingress/overview/)).
- Improved [OpenVidu Local Deployment](https://openvidu.io/3.0.0/docs/self-hosting/local/):
  - Fixed Room Composite Egress ([LiveKit reference](https://docs.livekit.io/home/egress/room-composite/)) support when using mediasoup.
  - WebHooks ([LiveKit reference](https://docs.livekit.io/home/server/webhooks/)) supported against a local [OpenVidu Call](https://openvidu.io/3.0.0/docs/openvidu-call/docs/#run-openvidu-locally).
- Production deployments have a better private IP discovery process when there are multiple valid private IPs in the same host. This will make more deployments work out-of-the-box without the need of manual intervention.
- [OpenVidu PRO Evaluation Mode](https://openvidu.io/3.0.0/docs/self-hosting/local/#openvidu-pro) improved. Before, a maximum of 2 Rooms of 8 Participants each could be created. Now the upper limit of Participants still apply, but the number of Rooms is unlimited. For example, you can have 4 Rooms of 2 Participants each, or 1 Room of 8 Participants.
- Minor bug fixes related to [OpenVidu Call](https://openvidu.io/3.0.0/docs/openvidu-call/).

### Known limitations

- When using [mediasoup](https://openvidu.io/3.0.0/docs/self-hosting/production-ready/performance/):
  - No support for Speaker Detection events ([LiveKit reference](https://docs.livekit.io/home/client/tracks/subscribe/#Speaker-detection)).
  - No `ConnectionQualityChanged` event ([LiveKit reference](https://docs.livekit.io/home/client/events/#Events)).
  - No support for Dynacast ([LiveKit reference](https://docs.livekit.io/home/client/tracks/publish/#Dynamic-broadcasting)).
  - No support for Adaptive Streaming ([LiveKit reference](https://docs.livekit.io/home/client/tracks/subscribe/#Adaptive-stream)).
- When using [OpenVidu Call](https://openvidu.io/3.0.0/docs/openvidu-call/docs/#run-openvidu-locally) against an [OpenVidu Local Deployment](https://openvidu.io/3.0.0/docs/self-hosting/local/), recordings cannot be accessed.

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
