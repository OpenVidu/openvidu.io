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
  - anchor: can-i-embed-openvidu-meet-in-my-application-like-the-jitsi-iframe-api
    question: "Can I embed OpenVidu Meet in my application like the Jitsi iframe API?"
    answer: >-
      Yes. An <openvidu-meet> web component or an iframe put OpenVidu Meet inside your own page,
      and a direct link opens it on its own. A REST API creates and manages rooms and recordings
      from your backend, and webhooks report meeting and recording events. Jitsi Meet's documented
      path is its IFrame API (external_api.js) and the React SDK built on it, where rooms are
      created when the first participant opens the meeting URL, and self-hosted Jitsi sends no
      webhooks.
  - anchor: is-jitsi-free-to-self-host
    question: "Is Jitsi free to self-host?"
    answer: >-
      Yes. Jitsi Meet, Jicofo and Jitsi Videobridge are all Apache 2.0, the same license as OpenVidu
      COMMUNITY. Jitsi itself has no self-hosted paid edition the way OpenVidu does.
  - anchor: does-jitsi-have-a-recording-feature
    question: "Does Jitsi have a recording feature?"
    answer: >-
      Yes, via Jibri. A per-participant recording
      permission in the JWT decides who may start one. The difference is afterwards: Jibri writes
      the file to a directory and runs your finalize script, so storing it, serving it and
      controlling who may watch or delete it are your application's job, whereas OpenVidu Meet keeps
      each recording in the app with a player, sharing and deletion governed by room permissions.
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
| Embedding in your app | An [`<openvidu-meet>` web component](meet/embedded/reference/webcomponent.md) or an [iframe](meet/embedded/reference/iframe.md) put Meet inside your own page, and a [direct link](meet/embedded/reference/direct-link.md) opens it on its own instead. Your backend drives it through a [REST API](meet/embedded/reference/rest-api.md) for rooms and recordings, and receives [webhooks](meet/embedded/reference/webhooks.md) for meeting and recording events | The [IFrame API :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-iframe/){:target="_blank"} (`external_api.js`, `new JitsiMeetExternalAPI(...)`), a [React SDK :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-react-sdk/){:target="_blank"} built on it, and the lower-level `lib-jitsi-meet`. Rooms are created when the first participant opens the meeting URL; the documented backend hook is the [Reservation System :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/devops-guide/reservation/){:target="_blank"}, which Jitsi *queries* on an external service you implement. Self-hosted Jitsi sends no webhooks |
| Recording | [Built in](meet/features/recordings/overview.md) to OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }. A participant with the `canRecord` permission starts it from the app or the [REST API](meet/embedded/reference/rest-api.md), and the recording then lives in the app as something you manage: [listed, played in a built-in player, shared, downloaded and deleted](meet/features/recordings/management.md), each action governed by room member permissions | [Jibri :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jitsi/jibri){:target="_blank"} supports recording the same way OpenVidu does, with a per-participant `recording` permission in the [JWT your backend signs :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jitsi/jitsi-meet/blob/stable/jitsi-meet_11248/react/features/base/jwt/constants.ts){:target="_blank"} that decides who may start one. The difference is what happens next: Jibri writes the file to its [recording directory and hands it to a finalize script :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jitsi/jibri/blob/master/src/main/resources/reference.conf){:target="_blank"}, so storing it, serving it and deciding who may watch or delete it are your application's job |
| Roles and permissions | A [room is persistent](meet/features/rooms/overview.md) and hosts as many meetings as you need over time, keeping its links and settings. [Moderator and Speaker roles](meet/features/rooms/access.md#predefined-roles) come predefined, can be changed per room and refined per member down to individual permissions — including who may retrieve or delete that room's recordings — and moderators can be [promoted or demoted mid-meeting](meet/features/meetings/role-management.md) | A moderator role, plus per-participant feature flags such as `recording`, `livestreaming`, `transcription`, `lobby`, `moderation`, `screen-sharing`, `send-groupchat` and `create-polls`, carried in the [JWT your backend signs :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jitsi/jitsi-meet/blob/stable/jitsi-meet_11248/react/features/base/jwt/constants.ts){:target="_blank"}. They are decided when the token is issued rather than in an admin screen, and they cover what someone may do during the meeting, not access to the recordings afterwards |
| Branding | An admin sets the meeting view's [colour scheme](meet/features/rooms/management.md#room-appearance) from the app's "Configuration" page, and OpenVidu Meet runs on your own domain | App name, welcome-page logo, watermarks and provider name are set in the [`interface_config.js` :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jitsi/jitsi-meet/blob/stable/jitsi-meet_11248/interface_config.js){:target="_blank"} and [`config.js` :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-configuration/){:target="_blank"} files on the server, and applied by redeploying the web frontend |
| Autoscaling | [Elastic and HA deployments](docs/self-hosting/production-ready/scalability.md)**PRO**{ .openvidu-tag .openvidu-pro-tag }: one product to configure, with one-click deploy for 5 cloud providers | Videobridges [scale horizontally :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-scalable/){:target="_blank"}, and the handbook notes "Building a scalable infrastructure is not a task for beginning Jitsi Administrators", recommending Ansible or Puppet; growing the pool automatically needs the separate `jitsi-autoscaler` service, which deploys instances as a Nomad batch job, in Oracle Cloud, in DigitalOcean or through a custom model you implement (detailed below) |
| License | Apache 2.0**COMMUNITY**{ .openvidu-tag .openvidu-community-tag } / commercial**PRO**{ .openvidu-tag .openvidu-pro-tag } | [Apache 2.0 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jitsi/jitsi-meet/blob/master/LICENSE){:target="_blank"} |
| Commercial support | Priority support from the OpenVidu team for your own self-hosted deployment**PRO**{ .openvidu-tag .openvidu-pro-tag } | None from the people who make Jitsi: 8x8's [own FAQ :fontawesome-solid-external-link:{.external-link-icon}](https://developer.8x8.com/jaas/docs/faq/){:target="_blank"} states "8x8 offers no commercial support, SLA or professional services for Self-hosted Jitsi deployments" |

Every Jitsi row above is cited in the cell — to Jitsi's own documentation and source code, and to
8x8's for the support row — and was checked against Jitsi's current stable release,
`stable/jitsi-meet_11248` (September 2026). Jitsi Meet and OpenVidu Meet **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } are both free to
self-host under Apache 2.0, and Jitsi Meet ships [app-level features OpenVidu Meet doesn't have
yet](#where-jitsi-still-has-the-edge). The practical split is what you get without building it:
OpenVidu Meet bundles recording management, per-member permissions and a backend REST API with
webhooks into the app itself, while Jitsi Meet hands the recording file to your infrastructure and
leaves room management to the client that joins.

<div class="centered-section" markdown>

[Deploy OpenVidu Meet in minutes](meet/getting-started.md){ .md-button .md-button--primary }

</div>

## Architecture at a glance

The biggest practical difference isn't a feature — it's what you have to deploy and keep running.

| | **OpenVidu** | **Jitsi** |
| --- | --- | --- |
| Components to operate | A [fork of LiveKit](openvidu-vs-livekit.md), optionally with mediasoup as the media engine**PRO**{ .openvidu-tag .openvidu-pro-tag } and [OpenVidu Meet](meet/index.md) as a web frontend — one integrated stack | Prosody (XMPP signaling), Jicofo (conference focus), Jitsi Videobridge (SFU, Java), and the Jitsi Meet web frontend — four separately-versioned components, a single bundle|
| License | Apache 2.0**COMMUNITY**{ .openvidu-tag .openvidu-community-tag } / commercial**PRO**{ .openvidu-tag .openvidu-pro-tag } | Apache 2.0 |
| Recording/streaming | [Egress](docs/reference/egress.md) bundled by default. Recording is expensive either way: our own reference calls it "many orders of magnitude more CPU cycles than the rooms themselves", so capacity for it has to be planned | Jibri, deployed as an additional bundle, with Jitsi asking for [one machine per concurrent recording and 8 GB RAM for 1080x720 :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-requirements/){:target="_blank"} |
| Horizontal scaling | [Elastic & HA modes](docs/self-hosting/production-ready/scalability.md)**PRO**{ .openvidu-tag .openvidu-pro-tag } distribute *rooms* across media servers, one product to configure and one-click deploy for 5 cloud providers. A single room is hosted on a single media server, so one meeting grows only as far as that machine does; [spreading one room across servers](docs/self-hosting/production-ready/scalability.md) is on the roadmap | Bridge relays ([`relay` :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jitsi/jitsi-videobridge/blob/stable/jitsi-meet_11248/jvb/src/main/resources/reference.conf){:target="_blank"} in the Videobridge configuration, still [`octo` :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jitsi/jicofo/blob/stable/jitsi-meet_11248/jicofo-common/src/main/resources/reference.conf){:target="_blank"} in Jicofo's) carry media between Videobridges, so a single conference can span several bridges and is not bounded by one machine. Growing the pool itself needs a separate `jitsi-autoscaler` service, which launches instances as a Nomad batch job, in Oracle Cloud, in DigitalOcean or through a custom deployment model you write |
| Admin dashboard | [OpenVidu Dashboard](docs/self-hosting/production-ready/observability/openvidu-dashboard.md)**COMMUNITY**{ .openvidu-tag .openvidu-community-tag }, per-room and per-participant views**PRO**{ .openvidu-tag .openvidu-pro-tag } | None bundled |
| Ready-to-use app | [OpenVidu Meet](meet/index.md), embeddable via [iframe](meet/embedded/step-by-step-guide.md#use-an-iframe) or [web component](meet/embedded/step-by-step-guide.md#use-the-web-component) | Jitsi Meet, embeddable via iframe, lib-jitsi-meet, or native SDKs |
| Hosted/cloud option | None — [self-hosted](docs/self-hosting/deployment-types.md) only, on your own infrastructure. One-click deploy for [5 cloud providers](docs/self-hosting/single-node/index.md) | [Jitsi as a Service :fontawesome-solid-external-link:{.external-link-icon}](https://jaas.8x8.vc/){:target="_blank"} (8x8), MAU-priced |
| Pricing | Free**COMMUNITY**{ .openvidu-tag .openvidu-community-tag }, flat **$0.0006/core/minute****PRO**{ .openvidu-tag .openvidu-pro-tag } | Free self-hosted; JaaS from **$0.35/MAU** (decreasing with volume), recording is a separate $0.01/min add-on |

## Recording: what happens to the file

The two projects record a meeting the same way, but they differ in what you are given afterwards.
OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } ships
[Egress](docs/reference/egress.md) wired up by default and writes to S3-compatible storage, and
OpenVidu Meet then treats each recording as part of the product: a
[recordings view](meet/features/recordings/management.md) lists them, a built-in player plays them
back, and sharing, downloading and deleting are governed by the same room member permissions as the
meeting itself. Jitsi's Jibri writes the file to a directory and runs your finalize script over it.
From that point the recording is outside Jitsi: storing it, serving it and deciding who may watch or
delete it are your application's job.

## Scaling: Elastic/HA vs bridge relays plus a separate autoscaler

Both projects scale horizontally, but they scale different things, and the honest comparison has a
point in Jitsi's favour.

OpenVidu's [Elastic and HA modes](docs/self-hosting/production-ready/scalability.md) are delivered
as a configured product: you pick a mode and OpenVidu's automated deployments handle the rest. What
they distribute is rooms. A single room is hosted on a single media server, so one meeting is
bounded by one machine, and spreading the participants of one room across servers is on the roadmap
rather than shipped. Jitsi has no such bound: its bridge relay was built precisely so that one
conference can span several Videobridges.

Jitsi splits the problem into two layers, and it's worth being precise about which one the **bridge
relay** actually solves. The relay lets Videobridge instances forward media to each other, so a
conference can span bridges in different regions with participants connecting to their nearest one —
but it only routes media across a pool of bridges that's already running. It doesn't decide how many
bridges to run: that's Jicofo's job in real time (bridge selection from reported load), and it's a
fixed pool unless something else grows or shrinks it. The feature is still called **Octo** in
[Jicofo's configuration :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jitsi/jicofo/blob/stable/jitsi-meet_11248/jicofo-common/src/main/resources/reference.conf){:target="_blank"}
and was renamed to [`relay` :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jitsi/jitsi-videobridge/blob/stable/jitsi-meet_11248/jvb/src/main/resources/reference.conf){:target="_blank"}
in the Videobridge's, so you will meet both names in the same deployment.

Actually autoscaling that pool needs a third, separate component — [`jitsi-autoscaler` :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jitsi/jitsi-autoscaler){:target="_blank"},
its own microservice with sidecars on every Videobridge reporting load to a Redis-backed
autoscaler, which then launches or kills instances via a cloud-provider integration. It's real, but
it's DIY: its own deployment, its own Redis, and instances come up as a Nomad batch job, in Oracle
Cloud, in DigitalOcean or through a custom deployment model you write yourself — there is no
AWS/Azure/GCP integration out of the box. On top of that, the relay has to be enabled with matching
settings on both sides: Jicofo's own configuration warns that the two flags "MUST be in sync
(otherwise bridges will crash because they won't know how to deal with octo channels)". Sharding
across Prosody/Jicofo/JVB clusters is your own design to get right.

## Client integration: SDKs

Jitsi offers several depths of integration: an iframe-based External API for the simplest embed,
the lower-level `lib-jitsi-meet` JavaScript library if you want your own UI on top of Jitsi's
connection and room primitives, and pre-built iOS, Android and React Native SDKs that reuse the
Jitsi Meet app experience. What they have in common is the shape of the product they expose. All of
them model a meeting, so the SDKs are high level and quick to adopt as long as what you are building
is a videoconference.

OpenVidu exposes the LiveKit model instead: participants, individual audio, video and screen tracks,
data messages, and server-side pieces like Egress, Ingress and agents. It is a lower-level set of
primitives, so a videoconference takes more assembling, but so does anything that is not one — a
live stream, a drone feed, a kiosk, a bot that consumes the media. That is the versatility
difference, across 8 client SDKs including native iOS and Android, with
[OpenVidu Meet's own embedding path](meet/embedded/intro.md) for teams that want the finished app
inside their product rather than a UI built from primitives.

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

### Can I embed OpenVidu Meet in my application like the Jitsi iframe API?

Yes. An [`<openvidu-meet>` web component](meet/embedded/reference/webcomponent.md) or an
[iframe](meet/embedded/reference/iframe.md) put OpenVidu Meet inside your own page, and a
[direct link](meet/embedded/reference/direct-link.md) opens it on its own. A
[REST API](meet/embedded/reference/rest-api.md) creates and manages rooms and recordings from your
backend, and [webhooks](meet/embedded/reference/webhooks.md) report meeting and recording events.
Jitsi Meet's documented path is its [IFrame API :fontawesome-solid-external-link:{.external-link-icon}](https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-iframe/){:target="_blank"}
(`external_api.js`) and the React SDK built on it, where rooms are created when the first
participant opens the meeting URL; self-hosted Jitsi sends no webhooks.

### Is Jitsi free to self-host?

Yes. Jitsi Meet, Jicofo and Jitsi Videobridge are all Apache 2.0, the same license as OpenVidu
**COMMUNITY**{ .openvidu-tag .openvidu-community-tag }. Jitsi itself has no self-hosted paid edition the way OpenVidu does.

### Does Jitsi have a recording feature?

Yes, via Jibri. A per-participant recording permission
in the JWT decides who may start one. The difference is afterwards: Jibri writes the file to a
directory and runs your finalize script, so storing it, serving it and controlling who may watch or
delete it are your application's job, whereas OpenVidu Meet keeps each recording in the app with a
player, sharing and deletion governed by room permissions.

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
