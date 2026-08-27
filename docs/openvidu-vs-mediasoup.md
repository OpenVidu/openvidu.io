---
title: "OpenVidu vs mediasoup: Platform vs Raw SFU Library"
description: "mediasoup is a low-level SFU library, not a platform. See exactly what OpenVidu already built on top of it — signaling, rooms, auth, recording, API."
# Structured Q&A metadata for this page's FAQ section. It feeds the JSON-LD
# (schema.org FAQPage) emitted by overrides/partials/json-ld.html. Keep in
# sync with the page content below: 'anchor' must match the heading id, and
# each answer must summarize the visible content of its section.
faq:
  - anchor: is-mediasoup-a-competitor-to-openvidu
    question: "Is mediasoup a competitor to OpenVidu?"
    answer: >-
      Not really — mediasoup is a low-level SFU library, not a finished platform. It provides the
      media-routing primitives (Workers, Routers, Transports, Producers, Consumers) but deliberately
      leaves signaling, room management, authentication, recording, and a server API for the
      integrating application to build. OpenVidu is a full platform in which all of that is already
      built — using mediasoup itself as its media engine.
  - anchor: does-openvidu-use-mediasoup
    question: "Does OpenVidu use mediasoup?"
    answer: >-
      Yes. OpenVidu is a fork of LiveKit that can replace LiveKit's default media engine (Pion) with
      mediasoup, for roughly double the media-track capacity per server. Every other part of the
      platform — rooms, signaling, authentication, the server API, recording — is built on top of
      that engine and shipped ready to use.
  - anchor: can-i-use-mediasoup-directly-instead-of-a-platform
    question: "Can I use mediasoup directly instead of a platform?"
    answer: >-
      Yes, and for some teams with genuinely unusual low-level requirements it's the right call — but
      go in aware of the scope: mediasoup's own documentation is explicit that signaling, room
      persistence, authentication, a managed recording API, a REST API, an admin dashboard, and
      native mobile SDKs are all out of scope by design. You would build every one of those yourself.
hide:
  - feedback
  - navigation
  - toc
  - footer
  - search-bar
  - version-selector
tags: []
page_features:
  - setupwowjs
---

# OpenVidu vs mediasoup

**mediasoup isn't a competing platform** — it's a low-level media-routing library OpenVidu can use
internally as its media engine, replacing Pion, the engine used by upstream LiveKit (see
[OpenVidu vs LiveKit](openvidu-vs-livekit.md)). If you're evaluating
"build directly on mediasoup" against "use OpenVidu," this page is for you: here's exactly what
mediasoup leaves for you to build yourself, and what OpenVidu already built on that same
foundation.

<div style="text-align: center; margin: 2em 0;" markdown>

[Get started with Platform](docs/index.md){ .md-button .md-button--primary }
[Compare with LiveKit instead](openvidu-vs-livekit.md){ .md-button }

</div>

## What mediasoup gives you

mediasoup is genuinely excellent at what it does: a C++ media engine exposed as a Node.js module
(or Rust crate), built around Workers, Routers, and Transports that receive and selectively forward
audio/video streams (Producers and Consumers), with simulcast and SVC support, plus its own
congestion control. OpenVidu adopted it for its performance over Pion — see
[OpenVidu vs LiveKit](openvidu-vs-livekit.md) for the benchmark numbers.

## What you'd build yourself

mediasoup's own documentation is direct about what's intentionally left out — design goals, not
gaps to be filled in a future release:

- **No signaling protocol.** mediasoup's own FAQ states that it provides no signaling protocol
  between clients and server: it's *"up to the application"* to carry that traffic over
  *"WebSocket, HTTP or whichever communication means."*
- **No room or session model.** There's no "room" resource with its own identity, metadata, or
  lifecycle — just Routers, a media-routing primitive.
- **No authentication system.** Since auth has to travel over whatever signaling channel you build,
  it's entirely your application's responsibility too.
- **No managed recording.** The documented pattern is manually piping raw RTP into an external tool
  like GStreamer or FFmpeg — there's no recording API to call.
- **No REST API, no admin dashboard.** mediasoup exposes only a programmatic library API — no HTTP
  surface, no UI of any kind.
- **No native mobile SDKs.** Only a JS client library and a C++ library are officially provided —
  no Swift, Kotlin, or Flutter SDK.
- **No clustering orchestration.** Routers on different hosts can be connected, but mediasoup's own
  scalability docs state plainly that the required information exchange between them is *"up [to]
  the application to implement"* — there's no built-in mechanism.

## OpenVidu already built all of this — on the same engine

OpenVidu runs on mediasoup for exactly the performance reasons you'd choose it yourself, and ships
everything on top of it ready to use:

| | **OpenVidu** | **mediasoup** |
| --- | --- | --- |
| Media engine | [mediasoup](docs/self-hosting/production-ready/performance.md), integrated | The library itself |
| Signaling | Bundled | Build it yourself |
| Room/session model | [Bundled](docs/reference/room-service-api.md#rooms) | Not provided |
| Authentication | [JWT tokens with grants](docs/developing-your-openvidu-app/how-to.md#generate-access-tokens), bundled | Not provided |
| Recording (Egress) | [Bundled](docs/developing-your-openvidu-app/how-to.md#recording) (S3-compatible storage) | Manual RTP piping to GStreamer/FFmpeg |
| Server/REST API | Full [server API](docs/developing-your-openvidu-app/how-to.md) | None |
| Webhooks | Bundled [event set](docs/developing-your-openvidu-app/how-to.md#webhooks) | None |
| Dashboard | [OpenVidu Dashboard](docs/self-hosting/production-ready/observability/openvidu-dashboard.md) | None |
| Client SDKs | [8 SDKs, including native Android and iOS](docs/tutorials/application-client/index.md) | JS + C++ only |
| Clustering | [One-click automated deployment](docs/self-hosting/deployment-types.md) with autoscaling on 5 cloud providers | Your own orchestration |

## When raw mediasoup is still the right call

To be fair about it: some teams have genuinely unusual low-level requirements — custom routing
topologies, non-standard transport needs, or a signaling architecture they can't build around an
off-the-shelf room model. Two capabilities in particular stay on mediasoup's side of the line:
**low-level tuning of the engine itself** and **interconnecting servers with your own topology** by
piping media between mediasoup instances. OpenVidu exposes plenty of configuration, but not
mediasoup's own API — if you need to program Routers and Transports directly, the library is the
right level to work at.

For those specific cases, building directly on mediasoup is the right call, as long as you accept
that you're also signing up to build and maintain everything in the table above. For most teams
building a real-time video application, that's a lot of platform to rebuild on top of a library,
when a full platform like OpenVidu has already built it — on this exact engine.

## Frequently asked questions

### Is mediasoup a competitor to OpenVidu?

Not really — mediasoup is a low-level SFU library, not a finished platform. It provides the
media-routing primitives (Workers, Routers, Transports, Producers, Consumers) but deliberately
leaves signaling, room management, authentication, recording, and a server API for the integrating
application to build. OpenVidu is a full platform in which all of that is already built — using
mediasoup itself as its media engine.

### Does OpenVidu use mediasoup?

Yes. OpenVidu is a fork of LiveKit that can replace LiveKit's default media engine (Pion) with
mediasoup, for roughly double the media-track capacity per server. Every other part of the platform
— rooms, signaling, authentication, the server API, recording — is built on top of that engine and
shipped ready to use.

### Can I use mediasoup directly instead of a platform?

Yes, and for some teams with genuinely unusual low-level requirements it's the right call — but go
in aware of the scope: mediasoup's own documentation is explicit that signaling, room persistence,
authentication, a managed recording API, a REST API, an admin dashboard, and native mobile SDKs are
all out of scope by design. You would build every one of those yourself.

<div style="text-align: center; margin: 2em 0;" markdown>

[Start with a tutorial](docs/tutorials/application-server/index.md){ .md-button .md-button--primary }

</div>

<div class="second-slogan wow animated animatedFadeInUp fadeInUp" style="margin: 6em 0; text-align: center">
  <h2 style="margin-bottom: 0.5em">Weighing a DIY mediasoup build against a ready platform?</h2>
  <p style="margin-bottom: 1.5em">Tell us what you are building and we will help you scope the tradeoffs.</p>
  <div class="home-buttons">
    <a href="/support/#talk-to-an-expert" class="md-button home-secondary-button">Talk to an expert</a>
  </div>
</div>
