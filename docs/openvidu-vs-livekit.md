---
title: "OpenVidu vs LiveKit: A Self-Hosted LiveKit Fork"
description: "OpenVidu is a fork of LiveKit — 100% API-compatible, self-hosted only, with mediasoup for 2x performance and Egress/Ingress bundled by default."
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
      only the server URL needs to point at your OpenVidu deployment instead of LiveKit.
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
      your own infrastructure or cloud account.
  - anchor: why-does-openvidu-use-mediasoup-instead-of-livekits-own-engine
    question: "Why does OpenVidu use mediasoup instead of LiveKit's own engine?"
    answer: >-
      LiveKit's own media engine (Pion) is written in Go, which requires a garbage collector and a
      relatively heavy runtime — a real cost in a performance-critical media server. OpenVidu replaces
      it with mediasoup, a C++ media engine, while keeping every other part of the LiveKit stack (SDKs,
      API, token model) unchanged. OpenVidu's own benchmarks show roughly double the media-track capacity
      per server as a result.
hide:
  - navigation
  - toc
  - footer
  - search-bar
  - version-selector
tags: []
---

# OpenVidu vs LiveKit

OpenVidu is a **fork of LiveKit** — 100% compatible with its client and server SDKs, so your
existing LiveKit code runs against OpenVidu unchanged. We swapped LiveKit's media engine for
**mediasoup** and bundled what self-hosted LiveKit otherwise leaves for you to assemble yourself:
Egress, Ingress, S3-compatible storage, and an admin dashboard, all wired up by default.

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

| | **OpenVidu** | **LiveKit** |
| --- | --- | --- |
| Identity | Fork of LiveKit, 100% API/SDK-compatible | The upstream open-source project |
| Media engine | **mediasoup** (C++) | Pion (Go) |
| Self-hosted | ✅ COMMUNITY (free) + PRO (paid) | ✅ Apache 2.0, free |
| Hosted/Cloud | ❌ none — self-hosted only | ✅ LiveKit Cloud (managed SaaS) |
| Egress/Ingress | Bundled by default, pre-wired to Redis + S3 | Separate services you deploy yourself, wired to your own Redis (self-hosted); "without additional setup" on Cloud only |
| Admin dashboard | ✅ OpenVidu Dashboard, bundled | Not bundled |
| Observability | Bundled Grafana/Loki/Alloy/Mimir stack (PRO) | Prometheus metrics exposed; dashboards are DIY |
| Pricing | Flat **$0.0006/core/minute** (PRO) | Multi-dimensional Cloud pricing (agent-session minutes, concurrent sessions, SIP minutes) |

## What OpenVidu bundles that self-hosted LiveKit doesn't

Deploying LiveKit's Egress and Ingress services yourself means running them as **separate
processes**, each wired to the same Redis instance as your LiveKit server, with your own API keys
and sizing (LiveKit's own docs recommend at least 4 CPUs / 4GB RAM per instance). None of that is
optional plumbing you can skip — recording and streaming simply don't work until it's wired up.

OpenVidu COMMUNITY ships all of it pre-integrated by default:

- **Egress and Ingress already connected to a Redis instance** — no separate deployment step.
- **S3-compatible storage for recordings**, pre-configured (MinIO) out of the box.
- **An administration dashboard** to monitor Room status in real time and historically — participants, published tracks, Egress/Ingress activity.
- **A Docker Compose local development environment** with automatic certificate management, so you can test on real mobile devices on your LAN without extra setup.

## 2x the performance, benchmarked

OpenVidu's headline performance claim comes specifically from the mediasoup-for-Pion engine swap,
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

LiveKit's **Agents framework** is also more general-purpose than what OpenVidu ships today: it's a
full Python/Node.js toolkit for building arbitrary voice, video, and telephony AI agents from
scratch. OpenVidu currently ships a smaller catalog of pre-built, ready-to-enable agents (starting
with live captions and transcription) rather than a framework to build your own — turnkey for what
it covers, narrower in scope.

## Pricing

OpenVidu PRO's pricing is a single number: **$0.0006 per core per minute**, billed while your
cluster is running. LiveKit Cloud's pricing is metered across several different dimensions instead
— agent-session minutes, concurrent agent sessions, SIP minutes, and per-provider inference cost —
reflecting LiveKit's product focus shifting toward voice-AI agents. The two don't reduce to one
comparable number; if you're pricing out a plain video-conferencing use case rather than an
AI-agent-heavy one, see OpenVidu's own [worked examples](pricing.md) for concrete monthly costs at
several cluster sizes.

## Frequently asked questions

### Is OpenVidu compatible with LiveKit?

Yes. OpenVidu is a fork of LiveKit and is 100% compatible with its client and server SDKs and its
API. Any application built for LiveKit works against an OpenVidu deployment with no code changes —
only the server URL needs to point at your OpenVidu deployment instead of LiveKit.

### Can I migrate an existing LiveKit app to OpenVidu?

Yes, and there's no real "migration" work involved beyond redeploying: your existing LiveKit client
and server code, and any third-party LiveKit tutorials or examples you've already integrated, run
unmodified against OpenVidu.

### Does OpenVidu have a hosted or cloud option?

No. OpenVidu is self-hosted only, in both its free COMMUNITY edition and its paid PRO edition.
There is no OpenVidu-hosted SaaS equivalent to LiveKit Cloud — every OpenVidu deployment runs on
your own infrastructure or cloud account.

### Why does OpenVidu use mediasoup instead of LiveKit's own engine?

LiveKit's own media engine (Pion) is written in Go, which requires a garbage collector and a
relatively heavy runtime — a real cost in a performance-critical media server. OpenVidu replaces it
with mediasoup, a C++ media engine, while keeping every other part of the LiveKit stack (SDKs, API,
token model) unchanged. OpenVidu's own benchmarks show roughly double the media-track capacity per
server as a result.

<div style="text-align: center; margin: 2em 0;" markdown>

[Start with a tutorial](docs/tutorials/application-server/index.md){ .md-button .md-button--primary }
[Evaluating mediasoup directly instead?](openvidu-vs-mediasoup.md){ .md-button }

</div>
