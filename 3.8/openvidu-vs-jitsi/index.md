# OpenVidu vs Jitsi

OpenVidu and Jitsi are both **open-source, self-hosted video platforms** — but built on different architectures, with different defaults for what you get out of the box. This page compares the two on architecture, recording, scaling, client SDKs and pricing.

[Get started with Platform](https://openvidu.io/3.8/docs/index.md) [Compare Meet vs Platform](https://openvidu.io/3.8/openvidu-meet-vs-openvidu-platform/index.md)

Jitsi spans both Meet and Platform

Jitsi Meet works both as a ready-to-use application and, via its SDKs, as a building block for a custom app — the two audiences OpenVidu splits into **OpenVidu Meet** and **OpenVidu Platform**.

## Architecture at a glance

The biggest practical difference isn't a feature — it's what you have to deploy and keep running.

|                       | **OpenVidu**                                                                                                                                                                                                                                                 | **Jitsi**                                                                                                                                                                                                      |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Components to operate | A [fork of LiveKit](https://openvidu.io/3.8/openvidu-vs-livekit/index.md), optionally with mediasoup as the media engine**PRO** and [OpenVidu Meet](https://openvidu.io/3.8/meet/index.md) as a web frontend — one integrated stack                          | Prosody (XMPP signaling), Jicofo (conference focus), Jitsi Videobridge (SFU, Java), and the Jitsi Meet web frontend — four separately-versioned components, a single bundle                                    |
| License               | Apache 2.0**COMMUNITY** / commercial**PRO**                                                                                                                                                                                                                  | Apache 2.0                                                                                                                                                                                                     |
| Recording/streaming   | [Egress bundled by default](https://openvidu.io/3.8/docs/reference/egress/index.md), no extra hardware sizing                                                                                                                                                | Jibri, can be deployed as an additional bundle                                                                                                                                                                 |
| Horizontal scaling    | [Elastic & HA modes](https://openvidu.io/3.8/docs/self-hosting/production-ready/scalability/index.md)**PRO**, one product to configure & one-click deploy for 5 cloud providers                                                                              | Octo relays media across an existing pool of Videobridges; actually growing that pool needs a separate `jitsi-autoscaler` service, supporting only Oracle OCI, DigitalOcean or a custom provider you implement |
| Admin dashboard       | [OpenVidu Dashboard](https://openvidu.io/3.8/docs/self-hosting/production-ready/observability/openvidu-dashboard/index.md)**COMMUNITY**, per-room and per-participant views**PRO**                                                                           | None bundled                                                                                                                                                                                                   |
| Ready-to-use app      | [OpenVidu Meet](https://openvidu.io/3.8/meet/index.md), embeddable via [iframe](https://openvidu.io/3.8/meet/embedded/step-by-step-guide/#use-an-iframe) or [web component](https://openvidu.io/3.8/meet/embedded/step-by-step-guide/#use-the-web-component) | Jitsi Meet, embeddable via iframe, lib-jitsi-meet, or native SDKs                                                                                                                                              |
| Hosted/cloud option   | None — [self-hosted](https://openvidu.io/3.8/docs/self-hosting/deployment-types/index.md) only, on your own infrastructure. One-click deploy for [5 cloud providers](https://openvidu.io/3.8/docs/self-hosting/single-node/index.md)                         | [Jitsi as a Service](https://jaas.8x8.vc/) (8x8), MAU-priced                                                                                                                                                   |
| Pricing               | Free**COMMUNITY**, flat **$0.0006/core/minute\*\*\*\*PRO**                                                                                                                                                                                                   | Free self-hosted; JaaS from **$0.35/MAU** (decreasing with volume), recording is a separate $0.01/min add-on                                                                                                   |

## Recording: bundled Egress vs Jibri

This is the sharpest operational difference between the two projects. OpenVidu **COMMUNITY** ships [Egress](https://openvidu.io/3.8/docs/reference/egress/index.md) wired up by default, writing to S3-compatible storage out of the box. Jitsi's Jibri is the service responsible for recordings, but storing and serving the resulting files is left to you.

## Scaling: Elastic/HA vs Octo plus a separate autoscaler

Both projects scale horizontally, but the operational shape differs. OpenVidu's [Elastic and HA modes](https://openvidu.io/3.8/docs/self-hosting/production-ready/scalability/index.md) are delivered as a configured product: you pick a mode and OpenVidu's automated deployments handle the rest.

Jitsi splits the problem into two layers, and it's worth being precise about which one **Octo** actually solves. Octo is a relay protocol that lets Videobridge instances forward media to each other, so a conference can span bridges in different regions with participants connecting to their nearest one — but it only routes media across a pool of bridges that's already running. It doesn't decide how many bridges to run: that's Jicofo's job in real time (bridge selection from reported load), and it's a fixed pool unless something else grows or shrinks it. Actually autoscaling that pool needs a third, separate component — [`jitsi-autoscaler`](https://github.com/jitsi/jitsi-autoscaler) , its own microservice with sidecars on every Videobridge reporting load to a Redis-backed autoscaler, which then launches or kills instances via a cloud-provider integration. It's real, but it's DIY: its own deployment, its own Redis, and only Oracle OCI, DigitalOcean or a custom provider you write yourself are supported — no AWS/Azure/GCP integration out of the box. On top of that, Octo itself has to be enabled with matching settings on both the Videobridge and Jicofo, or bridges crash, and sharding across Prosody/Jicofo/JVB clusters is your own design to get right.

## Client integration: SDKs

Jitsi offers a broader set of integration depths than a typical low-level SFU: an iframe-based External API for the simplest embed, the lower-level `lib-jitsi-meet` JavaScript library if you want to build your own UI on top of Jitsi's connection/room primitives, and pre-built iOS, Android and React Native SDKs that reuse the Jitsi Meet app experience directly.

OpenVidu's approach is the LiveKit-compatible SDK set — 8 client SDKs including native iOS and Android — plus [OpenVidu Meet's own embedding path](https://openvidu.io/3.8/meet/embedded/intro/index.md) for teams that want the finished app experience inside their product rather than building a custom UI from primitives.

## Where Jitsi still has the edge

Jitsi Meet ships app-level features OpenVidu Meet doesn't have yet: a lobby, where a moderator approves each participant before letting them in — OpenVidu Meet's equivalent, locked rooms, is on the roadmap but not shipped; breakout rooms and a collaborative whiteboard; and native mobile apps for iOS and Android.

## Pricing

Both projects are free to self-host under Apache 2.0. The difference shows up if you want a hosted option or paid support: OpenVidu **PRO** is a flat **$0.0006 per core per minute** for self-hosted Elastic/HA deployments in your own infrastructure, while 8x8's JaaS is a *hosted* Monthly-Active-User model starting at $0.35/MAU (with a 25-MAU free developer tier), and charges recording separately at $0.01/minute. See [worked examples](https://openvidu.io/3.8/pricing/index.md) for OpenVidu's concrete monthly costs at several cluster sizes.

## Frequently asked questions

### Is Jitsi free to self-host?

Yes. Jitsi Meet, Jicofo and Jitsi Videobridge are all Apache 2.0, the same license as OpenVidu **COMMUNITY**. The paid option is 8x8's hosted Jitsi as a Service (JaaS), not a self-hosted PRO tier — Jitsi itself has no self-hosted paid edition the way OpenVidu does.

### Does Jitsi have a recording feature?

Yes, via Jibri, a component that drives a headless Chrome browser and ffmpeg to capture exactly what a participant sees. Storing and serving the resulting files is left to you, whereas OpenVidu's Egress writes to S3-compatible storage out of the box.

### Can I embed Jitsi in my own app?

Yes — via an iframe API, the lower-level `lib-jitsi-meet` JavaScript library for a fully custom UI, or pre-built iOS/Android/React Native SDKs that reuse the Jitsi Meet app experience. This makes Jitsi span both the "ready-to-use app" and "SDK" audiences that OpenVidu splits into Meet and Platform.

[Start with a tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/index.md) [Evaluating a raw SFU instead?](https://openvidu.io/3.8/openvidu-vs-janus/index.md)

## Weighing OpenVidu against Jitsi for your deployment?

Tell us about your use case and we will help you size it and compare the tradeoffs.

[Talk to an expert](/support/#talk-to-an-expert)
