---
title: "OpenVidu vs Jitsi: Two Self-Hosted Platforms Compared"
description: "OpenVidu and Jitsi are both open-source, self-hosted video platforms. Compare architecture, recording, scaling, SDKs and pricing to pick the right one."
# Structured Q&A metadata for this page's FAQ section. It feeds the JSON-LD
# (schema.org FAQPage) emitted by overrides/partials/json-ld.html. Keep in
# sync with the page content below: 'anchor' must match the heading id, and
# each answer must summarize the visible content of its section.
faq:
  - anchor: is-openvidu-meet-a-self-hosted-alternative-to-zoom-or-google-meet
    question: "Is OpenVidu Meet a self-hosted alternative to Zoom or Google Meet?"
    answer: >-
      Yes. OpenVidu Meet is an open-source, self-hosted video conferencing application that runs on
      your own servers — the same class of product as Jitsi Meet, and a ready-to-use alternative to
      Zoom or Google Meet for teams that need meetings, recordings and chat without sending media
      to a third-party SaaS. It installs with a single command and the COMMUNITY edition is free
      under Apache 2.0.
  - anchor: can-i-embed-openvidu-meet-in-my-saas-like-the-jitsi-iframe-api
    question: "Can I embed OpenVidu Meet in my SaaS like the Jitsi iframe API?"
    answer: >-
      Yes. OpenVidu Meet embeds with an <openvidu-meet> web component, an iframe or a direct link,
      and adds a REST API to create and manage rooms and recordings from your backend plus webhooks
      for events. Jitsi Meet's documented path is its IFrame API (external_api.js) and the React SDK
      built on it, where rooms are created when the first participant opens the meeting URL.
  - anchor: is-jitsi-free-to-self-host
    question: "Is Jitsi free to self-host?"
    answer: >-
      Yes. Jitsi Meet, Jicofo and Jitsi Videobridge are all Apache 2.0, the same license as OpenVidu
      COMMUNITY. The paid option is 8x8's hosted Jitsi as a Service (JaaS), not a self-hosted PRO
      tier — Jitsi itself has no self-hosted paid edition the way OpenVidu does.
  - anchor: does-jitsi-have-a-recording-feature
    question: "Does Jitsi have a recording feature?"
    answer: >-
      Yes, via Jibri, a component that drives a headless Chrome browser and ffmpeg to capture
      exactly what a participant sees. Storing and serving the resulting files is left to you,
      whereas OpenVidu's Egress writes to S3-compatible storage out of the box.
  - anchor: can-i-embed-jitsi-in-my-own-app
    question: "Can I embed Jitsi in my own app?"
    answer: >-
      Yes — via an iframe API, the lower-level lib-jitsi-meet JavaScript library for a fully custom
      UI, or pre-built iOS/Android/React Native SDKs that reuse the Jitsi Meet app experience. This
      makes Jitsi span both the "ready-to-use app" and "SDK" audiences that OpenVidu splits into
      Meet and Platform.
hide:
  - feedback
  - navigation
  - toc
  - footer
  - search-bar
  - version-selector
tags: []
page_features:
  - revealonscroll
---

# OpenVidu vs Jitsi

OpenVidu and Jitsi are both **open-source, self-hosted video platforms** — but built on different
architectures, with different defaults for what you get out of the box. This page compares the two
ready-to-use meeting apps, **OpenVidu Meet and Jitsi Meet**, and then the platforms underneath them:
architecture, recording, scaling, client SDKs and pricing.

<div class="centered-section" markdown>

[Get started with Platform](docs/index.md){ .md-button .md-button--primary }
[Compare Meet vs Platform](openvidu-meet-vs-openvidu-platform.md){ .md-button }

</div>

!!! tip "Jitsi spans both Meet and Platform"
    Jitsi Meet works both as a ready-to-use application and, via its SDKs, as a building block for
    a custom app — the two audiences OpenVidu splits into **OpenVidu Meet** and **OpenVidu
    Platform**.

## OpenVidu Meet vs Jitsi Meet

Jitsi Meet is the app most teams reach for when they want a self-hosted alternative to Zoom or
Google Meet. **[OpenVidu Meet](meet/index.md) is a product of that same class**: an open-source,
self-hosted video conferencing application — rooms, moderation, recording, chat, screen sharing
and virtual backgrounds — that you deploy on your own servers and can embed in your own product.
The rest of this page compares the platforms underneath; this section compares the two apps.

| | **OpenVidu Meet** | **Jitsi Meet** |
| --- | --- | --- |
| Deployment | A single installer command on one Ubuntu server, [Docker Compose for local development](meet/deployment/local.md), or [ready-made templates](meet/deployment/overview.md) for AWS, Azure, Google Cloud, DigitalOcean and Oracle Cloud | Self-hosting documented as a Debian/Ubuntu `apt` [quick install :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-quickstart/){:target="_blank"}, a [Docker Compose release archive :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-docker/){:target="_blank"} or openSUSE packages, installing Prosody, Jicofo, Videobridge and the web frontend |
| Embedding in your app | [`<openvidu-meet>` web component](meet/embedded/reference/webcomponent.md), [iframe](meet/embedded/reference/iframe.md) or [direct link](meet/embedded/reference/direct-link.md), plus a [REST API](meet/embedded/reference/rest-api.md) to create and manage rooms and recordings from your backend and [webhooks](meet/embedded/reference/webhooks.md) for meeting and recording events | The [IFrame API :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-iframe/){:target="_blank"} (`external_api.js`, `new JitsiMeetExternalAPI(...)`), a [React SDK :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-react-sdk/){:target="_blank"} built on it, and the lower-level `lib-jitsi-meet`. Rooms are created when the first participant opens the meeting URL; the documented backend hook is the [Reservation System :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/devops-guide/reservation/){:target="_blank"}, which Jitsi *queries* on an external service you implement |
| Recording | [Built in](meet/features/recordings/overview.md) to OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }: started from the app or the REST API by a participant with the `canRecord` permission, stored on the server, with playback, sharing and deletion governed by room member permissions | [Jibri :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jitsi/jibri){:target="_blank"}, a separate component driving a Chrome instance and ffmpeg. Jitsi's [requirements page :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-requirements/){:target="_blank"} states "Jibri needs ONE system per recording. One Jibri instance = one meeting", at least 8 GB RAM for 1080x720, and that co-hosting it with Jitsi Meet "is not recommended" |
| Roles and permissions | [Moderator and Speaker predefined roles](meet/features/rooms/access.md#predefined-roles), fine-tuned per member with custom permissions, and [promotion or demotion of moderators during a meeting](meet/features/meetings/role-management.md) | A moderator role. On a self-hosted install, who can create rooms and moderate is set up through the [secure domain :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/devops-guide/secure-domain/){:target="_blank"} configuration or [JWT token authentication :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/devops-guide/token-authentication/){:target="_blank"}, which the handbook recommends over secure domain |
| Branding | An admin sets the meeting view's [colour scheme](meet/features/rooms/management.md#room-appearance) from the app's "Configuration" page, and OpenVidu Meet runs on your own domain | App name, welcome-page logo, watermarks and provider name are edited in the `interface_config.js` and [`config.js` :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-configuration/){:target="_blank"} files on the server; the shipped `interface_config.js` notes it "is considered deprecated" and that options will move to `config.js` |
| Autoscaling | [Elastic and HA deployments](docs/self-hosting/production-ready/scalability.md)**PRO**{ .openvidu-tag .openvidu-pro-tag }: one product to configure, with one-click deploy for 5 cloud providers | Videobridges [scale horizontally :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-scalable/){:target="_blank"}, and the handbook notes "Building a scalable infrastructure is not a task for beginning Jitsi Administrators", recommending Ansible or Puppet; growing the pool automatically needs the separate `jitsi-autoscaler` service (detailed below) |
| License | Apache 2.0**COMMUNITY**{ .openvidu-tag .openvidu-community-tag } / commercial**PRO**{ .openvidu-tag .openvidu-pro-tag } | [Apache 2.0 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jitsi/jitsi-meet/blob/master/LICENSE){:target="_blank"} |
| Commercial support | Priority support from the OpenVidu team for your own self-hosted deployment**PRO**{ .openvidu-tag .openvidu-pro-tag } | 8x8's [JaaS FAQ :fontawesome-solid-external-link:{.external-link-icon}](https://developer.8x8.com/jaas/docs/faq/){:target="_blank"} states "8x8 provides commercial Support and SLA for JaaS customers" and "8x8 offers no commercial support, SLA or professional services for Self-hosted Jitsi deployments" |

Every Jitsi row above is taken from Jitsi's own documentation, linked in the cell. Both apps are
free to self-host under Apache 2.0, and Jitsi Meet ships [app-level features OpenVidu Meet doesn't
have yet](#where-jitsi-still-has-the-edge). The practical split is what you get without building
it: OpenVidu Meet bundles recording, per-member permissions and a backend REST API into the app
itself, while Jitsi Meet keeps recording in a separate component and leaves room management to the
client that joins.

<div class="centered-section" markdown>

[Deploy OpenVidu Meet in minutes](meet/getting-started.md){ .md-button .md-button--primary }

</div>

## Architecture at a glance

The biggest practical difference isn't a feature — it's what you have to deploy and keep running.

| | **OpenVidu** | **Jitsi** |
| --- | --- | --- |
| Components to operate | A [fork of LiveKit](openvidu-vs-livekit.md), optionally with mediasoup as the media engine**PRO**{ .openvidu-tag .openvidu-pro-tag } and [OpenVidu Meet](meet/index.md) as a web frontend — one integrated stack | Prosody (XMPP signaling), Jicofo (conference focus), Jitsi Videobridge (SFU, Java), and the Jitsi Meet web frontend — four separately-versioned components, a single bundle|
| License | Apache 2.0**COMMUNITY**{ .openvidu-tag .openvidu-community-tag } / commercial**PRO**{ .openvidu-tag .openvidu-pro-tag } | Apache 2.0 |
| Recording/streaming | [Egress bundled by default](docs/reference/egress.md), no extra hardware sizing | Jibri, can be deployed as an additional bundle |
| Horizontal scaling | [Elastic & HA modes](docs/self-hosting/production-ready/scalability.md)**PRO**{ .openvidu-tag .openvidu-pro-tag }, one product to configure & one-click deploy for 5 cloud providers | Octo relays media across an existing pool of Videobridges; actually growing that pool needs a separate `jitsi-autoscaler` service, supporting only Oracle OCI, DigitalOcean or a custom provider you implement |
| Admin dashboard | [OpenVidu Dashboard](docs/self-hosting/production-ready/observability/openvidu-dashboard.md)**COMMUNITY**{ .openvidu-tag .openvidu-community-tag }, per-room and per-participant views**PRO**{ .openvidu-tag .openvidu-pro-tag } | None bundled |
| Ready-to-use app | [OpenVidu Meet](meet/index.md), embeddable via [iframe](meet/embedded/step-by-step-guide.md#use-an-iframe) or [web component](meet/embedded/step-by-step-guide.md#use-the-web-component) | Jitsi Meet, embeddable via iframe, lib-jitsi-meet, or native SDKs |
| Hosted/cloud option | None — [self-hosted](docs/self-hosting/deployment-types.md) only, on your own infrastructure. One-click deploy for [5 cloud providers](docs/self-hosting/single-node/index.md) | [Jitsi as a Service :fontawesome-solid-external-link:{.external-link-icon}](https://jaas.8x8.vc/){:target="_blank"} (8x8), MAU-priced |
| Pricing | Free**COMMUNITY**{ .openvidu-tag .openvidu-community-tag }, flat **$0.0006/core/minute****PRO**{ .openvidu-tag .openvidu-pro-tag } | Free self-hosted; JaaS from **$0.35/MAU** (decreasing with volume), recording is a separate $0.01/min add-on |

## Recording: bundled Egress vs Jibri

This is the sharpest operational difference between the two projects. OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } ships
[Egress](docs/reference/egress.md) wired up by default, writing to
S3-compatible storage out of the box. Jitsi's Jibri is the service responsible for recordings, but
storing and serving the resulting files is left to you.

## Scaling: Elastic/HA vs Octo plus a separate autoscaler

Both projects scale horizontally, but the operational shape differs. OpenVidu's
[Elastic and HA modes](docs/self-hosting/production-ready/scalability.md) are delivered as a
configured product: you pick a mode and OpenVidu's automated deployments handle the rest.

Jitsi splits the problem into two layers, and it's worth being precise about which one **Octo**
actually solves. Octo is a relay protocol that lets Videobridge instances forward media to each
other, so a conference can span bridges in different regions with participants connecting to their
nearest one — but it only routes media across a pool of bridges that's already running. It doesn't
decide how many bridges to run: that's Jicofo's job in real time (bridge selection from reported
load), and it's a fixed pool unless something else grows or shrinks it. Actually autoscaling that
pool needs a third, separate component — [`jitsi-autoscaler` :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jitsi/jitsi-autoscaler){:target="_blank"},
its own microservice with sidecars on every Videobridge reporting load to a Redis-backed
autoscaler, which then launches or kills instances via a cloud-provider integration. It's real, but
it's DIY: its own deployment, its own Redis, and only Oracle OCI, DigitalOcean or a custom provider
you write yourself are supported — no AWS/Azure/GCP integration out of the box. On top of that, Octo
itself has to be enabled with matching settings on both the Videobridge and Jicofo, or bridges
crash, and sharding across Prosody/Jicofo/JVB clusters is your own design to get right.

## Client integration: SDKs

Jitsi offers a broader set of integration depths than a typical low-level SFU: an iframe-based
External API for the simplest embed, the lower-level `lib-jitsi-meet` JavaScript library if you want
to build your own UI on top of Jitsi's connection/room primitives, and pre-built iOS, Android and
React Native SDKs that reuse the Jitsi Meet app experience directly.

OpenVidu's approach is the LiveKit-compatible SDK set — 8 client SDKs including native iOS and
Android — plus [OpenVidu Meet's own embedding path](meet/embedded/intro.md) for teams that want the
finished app experience inside their product rather than building a custom UI from primitives.

## Where Jitsi still has the edge

Jitsi Meet ships app-level features OpenVidu Meet doesn't have yet: a lobby, where a moderator
approves each participant before letting them in — OpenVidu Meet's equivalent, locked rooms, is on
the roadmap but not shipped; breakout rooms and a collaborative whiteboard; and native mobile apps
for iOS and Android.

## Pricing

Both projects are free to self-host under Apache 2.0. The difference shows up if you want a hosted
option or paid support: OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag } is a flat **$0.0006 per core per minute** for
self-hosted Elastic/HA deployments in your own infrastructure, while 8x8's JaaS is a *hosted*
Monthly-Active-User model starting at $0.35/MAU (with a 25-MAU free developer tier), and charges
recording separately at $0.01/minute. See [worked examples](pricing.md) for OpenVidu's concrete
monthly costs at several cluster sizes.

## Frequently asked questions

### Is OpenVidu Meet a self-hosted alternative to Zoom or Google Meet?

Yes. [OpenVidu Meet](meet/index.md) is an open-source, self-hosted video conferencing application
that runs on your own servers — the same class of product as Jitsi Meet, and a ready-to-use
alternative to Zoom or Google Meet for teams that need meetings, recordings and chat without
sending media to a third-party SaaS. It installs with a single command and the
**COMMUNITY**{ .openvidu-tag .openvidu-community-tag } edition is free under Apache 2.0.

### Can I embed OpenVidu Meet in my SaaS like the Jitsi iframe API?

Yes. OpenVidu Meet embeds with an [`<openvidu-meet>` web component](meet/embedded/reference/webcomponent.md),
an [iframe](meet/embedded/reference/iframe.md) or a [direct link](meet/embedded/reference/direct-link.md),
and adds a [REST API](meet/embedded/reference/rest-api.md) to create and manage rooms and recordings
from your backend plus [webhooks](meet/embedded/reference/webhooks.md) for events. Jitsi Meet's
documented path is its [IFrame API :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-iframe/){:target="_blank"}
(`external_api.js`) and the React SDK built on it, where rooms are created when the first
participant opens the meeting URL.

### Is Jitsi free to self-host?

Yes. Jitsi Meet, Jicofo and Jitsi Videobridge are all Apache 2.0, the same license as OpenVidu
**COMMUNITY**{ .openvidu-tag .openvidu-community-tag }. The paid option is 8x8's hosted Jitsi as a Service (JaaS), not a self-hosted PRO
tier — Jitsi itself has no self-hosted paid edition the way OpenVidu does.

### Does Jitsi have a recording feature?

Yes, via Jibri, a component that drives a headless Chrome browser and ffmpeg to capture exactly what
a participant sees. Storing and serving the resulting files is left to you, whereas OpenVidu's Egress
writes to S3-compatible storage out of the box.

### Can I embed Jitsi in my own app?

Yes — via an iframe API, the lower-level `lib-jitsi-meet` JavaScript library for a fully custom UI,
or pre-built iOS/Android/React Native SDKs that reuse the Jitsi Meet app experience. This makes
Jitsi span both the "ready-to-use app" and "SDK" audiences that OpenVidu splits into Meet and
Platform.

<div class="centered-section" markdown>

[Start with a tutorial](docs/tutorials/application-server/index.md){ .md-button .md-button--primary }
[Evaluating a raw SFU instead?](openvidu-vs-janus.md){ .md-button }

</div>

<div class="second-slogan cta-section" data-sal="slide-up">
  <h2 class="cta-title">Weighing OpenVidu against Jitsi for your deployment?</h2>
  <p class="cta-lead">Tell us about your use case and we will help you size it and compare the tradeoffs.</p>
  <div class="home-buttons">
    <a href="/support/#talk-to-an-expert" class="md-button home-secondary-button">Talk to an expert</a>
  </div>
</div>
