---
title: "OpenVidu vs LiveKit: A Self-Hosted LiveKit Fork"
description: "OpenVidu is a fork of LiveKit — 100% API-compatible, self-hosted only, with an optional mediasoup engine for 2x performance and Egress/Ingress bundled by default."
# Structured Q&A metadata for this page's FAQ section. It feeds the JSON-LD
# (schema.org FAQPage) emitted by overrides/partials/json-ld.html. Keep in
# sync with the page content below: 'anchor' must match the heading id, and
# each answer must summarize the visible content of its section.
faq:
  - anchor: is-openvidu-compatible-with-livekit
    question: "Is OpenVidu compatible with LiveKit?"
    answer: >-
      Yes. OpenVidu is a fork of LiveKit and is 100% compatible with its client and server SDKs and its API.
      Any application built for LiveKit works against an OpenVidu deployment with no code changes —
      only the server URL needs to point at your OpenVidu deployment instead of LiveKit. Even AI agents
      developed for LiveKit work seamlessly in OpenVidu.
  - anchor: can-i-migrate-an-existing-livekit-app-to-openvidu
    question: "Can I migrate an existing LiveKit app to OpenVidu?"
    answer: >-
      Yes, and there's no real "migration" work involved beyond redeploying: your existing LiveKit client
      and server code, and any third-party LiveKit tutorials or examples you've already integrated, run
      unmodified against OpenVidu.
  - anchor: does-openvidu-have-a-hosted-or-cloud-option
    question: "Does OpenVidu have a hosted or cloud option?"
    answer: >-
      No. OpenVidu is self-hosted only, in both its free COMMUNITY edition and its paid PRO edition.
      There is no OpenVidu-hosted SaaS equivalent to LiveKit Cloud — every OpenVidu deployment runs on
      your own infrastructure or cloud account. However, OpenVidu does provide production-ready
      single-node, Elastic and HA deployments for the five major cloud providers, which you run in your
      own cloud account.
  - anchor: why-does-openvidu-use-mediasoup-instead-of-livekits-own-engine
    question: "Why does OpenVidu use mediasoup instead of LiveKit's own engine?"
    answer: >-
      LiveKit's own media engine (Pion) is written in Go, which requires a garbage collector and a
      relatively heavy runtime — a real cost in a performance-critical media server. OpenVidu supports
      Pion, but it can replace it with mediasoup, a C++ media engine, while keeping every other part of
      the LiveKit stack (SDKs, API, token model) unchanged. OpenVidu's own benchmarks show roughly double
      the media-track capacity per server as a result.
hide:
  - navigation
  - toc
  - footer
  - search-bar
  - version-selector
tags: []
---

# OpenVidu vs LiveKit

OpenVidu is an ecosystem of modules for real-time media applications, built around a **fork of
LiveKit** — 100% compatible with its client and server SDKs, so your existing LiveKit code runs
against OpenVidu unchanged. It supports both LiveKit's Pion media engine and **mediasoup** (~2x more
efficient than Pion), and it bundles what self-hosted LiveKit otherwise leaves for you to assemble
yourself: Egress, Ingress, S3-compatible storage, observability, and an admin dashboard, all wired
up by default.

<div style="text-align: center; margin: 2em 0;" markdown>

[Get started with Platform](docs/index.md){ .md-button .md-button--primary }
[Compare Meet vs Platform](openvidu-meet-vs-openvidu-platform.md){ .md-button }

</div>

## Same SDKs, zero migration cost

Because OpenVidu is a fork, not a rewrite, this is the same code you'd write for LiveKit itself:

=== "Application client (browser)"

    ```javascript
    import { Room } from "livekit-client";

    const room = new Room();
    await room.connect("wss://your-openvidu-deployment", token);
    await room.localParticipant.enableCameraAndMicrophone();
    ```

=== "Application server (Node)"

    ```javascript
    import { AccessToken } from "livekit-server-sdk";

    const token = new AccessToken(API_KEY, API_SECRET, { identity: "user-1" });
    token.addGrant({ roomJoin: true, room: "my-room" });
    return await token.toJwt();
    ```

Any LiveKit tutorial, any third-party LiveKit example, works against an OpenVidu deployment with
only the server URL changed — there's no OpenVidu-specific SDK to learn.

## At a glance

| | **OpenVidu** | **LiveKit** (self-hosted) |
| --- | --- | --- |
| Identity | Fork of LiveKit, 100% API/SDK-compatible | The upstream open-source project |
| Media engine | Pion<span class="openvidu-tag openvidu-community-tag" style="font-size: .7em">COMMUNITY</span> or [**mediasoup**](docs/self-hosting/production-ready/performance.md) (~2x more efficient)<span class="openvidu-tag openvidu-pro-tag" style="font-size: .7em">PRO</span> | Pion |
| Autoscaling | Yes: [Elastic](docs/self-hosting/elastic/index.md) & [HA](docs/self-hosting/ha/index.md) modes<span class="openvidu-tag openvidu-pro-tag" style="font-size: .7em">PRO</span> | Autoscaling is yours to build and operate |
| License | Apache 2.0<span class="openvidu-tag openvidu-community-tag" style="font-size: .7em">COMMUNITY</span> / commercial<span class="openvidu-tag openvidu-pro-tag" style="font-size: .7em">PRO</span> | Apache 2.0 |
| Egress/Ingress | [Bundled by default](docs/developing-your-openvidu-app/how-to.md)<span class="openvidu-tag openvidu-community-tag" style="font-size: .7em">COMMUNITY</span> | Separate services you deploy and operate yourself |
| AI agents | [OpenVidu Agents](docs/ai/overview.md) (on top of LiveKit's Agent framework), speech-processing agent bundled | LiveKit's Agent framework, DIY (no agent bundled) |
| High-level integrations | [OpenVidu Meet](meet/index.md), a ready-to-use videoconferencing application, optionally [embeddable in your own app](meet/embedded/intro.md) | None |
| Dashboard | [OpenVidu Dashboard](docs/self-hosting/production-ready/observability/openvidu-dashboard.md)<span class="openvidu-tag openvidu-community-tag" style="font-size: .7em">COMMUNITY</span>, with detailed per-room and per-participant views<span class="openvidu-tag openvidu-pro-tag" style="font-size: .7em">PRO</span> | No |
| Observability | Bundled [Grafana dashboards](docs/self-hosting/production-ready/observability/grafana-stack.md)<span class="openvidu-tag openvidu-pro-tag" style="font-size: .7em">PRO</span> | Prometheus metrics exposed; dashboards are DIY |
| Cloud automation | [One-click automated deployments](docs/self-hosting/deployment-types.md) on AWS, Azure, GCP, DigitalOcean and OCI | None — Helm chart or manual VM setup |
| Pricing | Free<span class="openvidu-tag openvidu-community-tag" style="font-size: .7em">COMMUNITY</span>, flat **$0.0006/core/minute**<span class="openvidu-tag openvidu-pro-tag" style="font-size: .7em">PRO</span> | Free |

LiveKit Cloud, LiveKit's managed SaaS, is out of scope for this table — see
[Where LiveKit still has the edge](#where-livekit-still-has-the-edge) for what it does better than
any self-hosted option, OpenVidu included.

## What OpenVidu bundles that self-hosted LiveKit doesn't

Deploying LiveKit's Egress and Ingress services yourself means running them as **separate
processes**, each with its own API keys and sizing (LiveKit's own docs recommend at least 4 CPUs /
4GB RAM per instance). None of that is optional plumbing you can skip — recording and streaming
simply don't work until it's wired up.

OpenVidu <span class="openvidu-tag openvidu-community-tag" style="font-size: .8em">COMMUNITY</span> ships all of it pre-integrated by default:

- [**Egress and Ingress**](docs/developing-your-openvidu-app/how-to.md) — no separate deployment step.
- [**S3-compatible storage for recordings**](docs/tutorials/advanced-features/recording-basic-s3.md), pre-configured (MinIO) out of the box.
- [**An admin dashboard**](docs/self-hosting/production-ready/observability/openvidu-dashboard.md) to monitor Room status in real time and historically — participants, published tracks, Egress/Ingress activity.
- [**A Docker Compose local development environment**](docs/self-hosting/local.md) with automatic certificate management, so you can test on real mobile devices on your LAN without extra setup.
- [**Five production-ready cloud deployments**](docs/self-hosting/deployment-types.md) to get you started in minutes on AWS, Azure, GCP, DigitalOcean or Oracle Cloud.

## 2x the performance with mediasoup, benchmarked

OpenVidu's headline performance claim comes specifically from the mediasoup engine integration,
not from marketing copy: the OpenVidu team built its own load-testing tool
([`openvidu-loadtest`](https://github.com/OpenVidu/openvidu-loadtest)) after finding that
SDK-simulated clients understate real-world load compared to real browser clients. Benchmarked on
identical hardware (an AWS `m6in.xlarge`, 4 vCPU), mediasoup handles roughly **2x** the media
tracks that stock LiveKit (Pion) does on the same server. Concretely:

- Single Node, 4 CPU: up to **50 simultaneous 8-participant video conferences**.
- Streaming: **1 publisher + 1000 subscribers** in a single Room, 4 CPUs.

See the full methodology and numbers in [Performance](docs/self-hosting/production-ready/performance.md).

## Where LiveKit still has the edge

To be direct about it: LiveKit Cloud's **distributed global mesh** — a proprietary orchestration
layer LiveKit built specifically so a single session isn't bound to one server, targeting "millions
of real-time participants per session" — has no equivalent in either open-source LiveKit or
OpenVidu today. Self-hosted OSS LiveKit (like OpenVidu) is capped at whatever a single node can
handle per room; that mesh capability is exclusive to LiveKit's paid, hosted product.

If you're weighing the underlying media engine rather than the platform, see
[OpenVidu vs mediasoup](openvidu-vs-mediasoup.md) for the equivalent honest account of when raw
mediasoup is the right call.

## Pricing

OpenVidu <span class="openvidu-tag openvidu-community-tag" style="font-size: .7em">COMMUNITY</span> is free, forever, and so is self-hosted LiveKit. The difference is at
the top end: OpenVidu offers first-class, production-ready Elastic and HA self-hosted deployments on
a pay-per-core basis, which self-hosted LiveKit does not.

OpenVidu <span class="openvidu-tag openvidu-pro-tag" style="font-size: .8em">PRO</span>'s pricing is a single number: **$0.0006 per core per minute**, billed while
your cluster is running. See our [worked examples](pricing.md) for concrete monthly costs at several
cluster sizes.

Combined with the mediasoup engine, that pricing gives OpenVidu a hard-to-match price/performance
ratio.

## 12+ years building real-time media

The OpenVidu team has spent more than 12 years building real-time media services and applications:

- **Low-level media engines.** Some OpenVidu engineers worked on [Kurento Media Server](https://github.com/Kurento/kurento) — the background that made swapping a Go media engine for a C++ one a tractable project rather than a gamble.
- **Developer experience.** We built OpenVidu to make life easier for developers building media services, and that shows in everything shipped around our LiveKit fork: Egress, Ingress, S3-compatible storage, automated deployments for five clouds, and more.
- **End-user experience.** Ultimately we all want to ship applications our users love, so we put real effort into helping developers get there.
- **Ready-to-use videoconferencing apps.** We recently released OpenVidu Meet - a standalone, brandable application you can use as-is or embed directly into your own product.
- **Applied research.** We keep pushing real-time media into new territory through applied research.

## Frequently asked questions

### Is OpenVidu compatible with LiveKit?

Yes. OpenVidu is a fork of LiveKit and is 100% compatible with its client and server SDKs and its
API. Any application built for LiveKit works against an OpenVidu deployment with no code changes —
only the server URL needs to point at your OpenVidu deployment instead of LiveKit. Even AI agents developed
for LiveKit work seamlessly in OpenVidu.

### Can I migrate an existing LiveKit app to OpenVidu?

Yes, and there's no real "migration" work involved beyond redeploying: your existing LiveKit client
and server code, and any third-party LiveKit tutorials or examples you've already integrated, run
unmodified against OpenVidu.

### Does OpenVidu have a hosted or cloud option?

No. OpenVidu is self-hosted only, in both its free <span class="openvidu-tag openvidu-community-tag" style="font-size: .8em">COMMUNITY</span> edition and its paid <span class="openvidu-tag openvidu-pro-tag" style="font-size: .8em">PRO</span> edition.
There is no OpenVidu-hosted SaaS equivalent to LiveKit Cloud — every OpenVidu deployment runs on
your own infrastructure or cloud account.

However, OpenVidu does provide production-ready single-node, Elastic and HA deployments for the five
major cloud providers, which you run in your own cloud account. See the
[deployment types page](docs/self-hosting/deployment-types.md) for details.

### Why does OpenVidu use mediasoup instead of LiveKit's own engine?

LiveKit's own media engine (Pion) is written in Go, which requires a garbage collector and a
relatively heavy runtime — a real cost in a performance-critical media server. OpenVidu supports
Pion, but it can replace it with mediasoup, a C++ media engine, while keeping every other part of the
LiveKit stack (SDKs, API, token model) unchanged.
[OpenVidu's own benchmarks](docs/self-hosting/production-ready/performance.md) show roughly double
the media-track capacity per server as a result.

<div style="text-align: center; margin: 2em 0;" markdown>

[Start with a tutorial](docs/tutorials/application-server/index.md){ .md-button .md-button--primary }
[Evaluating mediasoup directly instead?](openvidu-vs-mediasoup.md){ .md-button }

</div>
