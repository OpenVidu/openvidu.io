---
title: "WebRTC Live Streaming to Thousands of Viewers"
description: "Self-hosted WebRTC live streaming with sub-second latency: WHIP ingest, HLS output, autoscaling media nodes, and where the real limits are."
# Structured Q&A metadata for this page's FAQ section. It feeds the JSON-LD
# (schema.org FAQPage) emitted by overrides/partials/json-ld.html. Keep in
# sync with the page content below: 'anchor' must match the heading id, and
# each answer must summarize the visible content of its section.
faq:
  - anchor: is-webrtc-good-for-live-streaming-to-many-viewers
    question: "Is WebRTC good for live streaming to many viewers?"
    answer: >-
      It is the only mainstream option that delivers sub-second latency, so it is the right choice
      when viewers act on what they see — auctions, betting, live shopping, remote operation,
      interactive events. It is the wrong choice when you only need playback at massive scale with
      no interaction: HLS and DASH over a CDN are cheaper for that, at 10–45 seconds of delay.
  - anchor: how-many-viewers-can-one-openvidu-room-handle
    question: "How many viewers can one OpenVidu Room handle?"
    answer: >-
      OpenVidu's documented benchmark is 1 publisher and up to 1000 subscribers in a single Room on
      a 4-CPU server. A single Room is not yet distributed across several Media Nodes, so 1000
      viewers is the practical per-Room ceiling today; OpenVidu Elastic and High Availability scale
      the number of simultaneous Rooms, not the size of one. Beyond that, add an HLS output for the
      non-interactive audience.
  - anchor: how-do-i-push-a-stream-into-openvidu
    question: "How do I push a stream into OpenVidu?"
    answer: >-
      Through Ingress, which accepts WHIP (WebRTC over HTTP, the only input that can skip
      transcoding), RTMP from encoders such as OBS, and URL pull for HLS streams, media files and
      RTSP IP cameras. OBS has spoken WHIP natively since version 30, with no plugin and no code.
  - anchor: can-openvidu-output-hls-as-well-as-webrtc
    question: "Can OpenVidu output HLS as well as WebRTC?"
    answer: >-
      Yes. Egress can produce HLS segments and a playlist, push an RTMP or SRT stream to one or more
      ingest URLs, write files and capture thumbnails — from the same Room, at the same time.
      A common design is WebRTC for the interactive core and HLS over a CDN for the long tail of
      passive viewers.
  - anchor: what-does-self-hosted-live-streaming-cost
    question: "What does self-hosted live streaming cost?"
    answer: >-
      OpenVidu COMMUNITY is open source and free, so you pay only for your own servers and
      bandwidth. OpenVidu PRO, which adds the Elastic and High Availability deployments and
      autoscaling, is $0.0006 per core per minute for the cores available to your cluster. Neither
      edition charges per viewer or per streamed minute, so cost tracks the capacity you provision
      rather than the size of your audience.
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

# WebRTC live streaming

**WebRTC live streaming** delivers a live video feed to viewers in under a second, instead of the
10 to 45 seconds a conventional HLS or DASH stream takes — which is what you need whenever the
audience has to *act* on what they are watching. This page covers when that trade-off is worth
making, how a stream gets into a self-hosted [OpenVidu Platform](docs/index.md) deployment and back
out again, how far it scales, and where it stops being the right tool.

<div class="centered-section" markdown>

[Get started with Platform](docs/getting-started.md){ .md-button .md-button--primary }
[Read the WHIP walkthrough](blog/posts/2026/09/low-latency-whip-ingestion.md){ .md-button }

</div>

## How much latency can your use case tolerate?

Latency is the time between a frame being captured at the source and rendered on a viewer's screen.
"Live" covers a range of nearly three orders of magnitude, and the number you need depends on
whether a human or a system has to react before it is too late — not on how important the content
is.

| Category | Latency | Typical use cases |
|---|---|---|
| High latency | > 45 s | Legacy live streaming setups |
| Typical latency | 10–45 s | Most live OTT streaming services, video on demand |
| Low latency | < 10 s | Premium live sports, financial news, eSports |
| Ultra-low latency | < 1 s | Interactive live streaming: live commentary, in-play betting |
| Near-real-time | < 100 ms | Videoconferencing, cloud gaming |

Our post on [low latency live streaming](blog/posts/2026/09/low-latency-live-streaming.md) works
through why the tiers exist and why "low latency" is used to mean anything from ten seconds to a
fraction of one.

## WebRTC vs HLS and DASH

HLS and DASH cut the stream into segments, write a playlist and let the player buffer a few of them
before showing anything. That design is what makes them cheap to deliver over any CDN, and it is
also what puts a floor under their latency. WebRTC has no segments and no playlist: media is sent
as it is encoded, over UDP, with loss handled by the transport rather than by buffering.

| | WebRTC | HLS / DASH |
|---|---|---|
| Typical latency | Sub-second | 10–45 s (2–5 s tuned) |
| Transport | UDP, peer connection | HTTP segments |
| Delivery | Media server (SFU) | Any HTTP CDN |
| Interaction back from the viewer | Yes, same connection | No, needs a side channel |
| Cost at very large audiences | Scales with server capacity | Scales with cheap CDN bandwidth |
| Player support | Every modern browser, natively | Every modern browser and TV, natively |

The two are not rivals so much as different answers to different questions, and a lot of production
systems run both from the same source. Everything below assumes you have decided you need the
sub-second half.

## Getting a stream in: the ingest path

In OpenVidu Platform, everything that arrives from outside a Room comes through
[Ingress](docs/reference/ingress.md):

| Input | What it is | Transcoding |
|---|---|---|
| `WHIP_INPUT` | A WHIP endpoint: the broadcaster publishes over WebRTC with a single HTTP `POST` of an SDP offer. OBS Studio has supported it natively since version 30 | The only input that can skip it |
| `RTMP_INPUT` | An RTMP endpoint with a stream key, for any conventional encoder | Always transcoded |
| `URL_INPUT` | OpenVidu pulls from a URL you supply: HLS streams, media files, and RTSP IP cameras | Always transcoded |

Whatever comes in is published into the Room as an ordinary participant, so viewers subscribe to it
exactly like any other track. The
[WHIP ingestion walkthrough](blog/posts/2026/09/low-latency-whip-ingestion.md) builds this end to
end — a browser publisher, an OBS scene and a viewer page — on a local Docker Compose deployment.

## Getting the stream out: WebRTC, HLS, RTMP, files

[Egress](docs/reference/egress.md) exports media out of a Room, and one transcoded Egress can fan
out to several outputs at once: a file, HLS segments plus a playlist, an RTMP or SRT stream pushed
to one or more ingest URLs, and periodic thumbnails. That is what makes the hybrid design practical
— the interactive audience stays on WebRTC while the same Room feeds an HLS playlist that a CDN
serves to everyone else.

Files and segments upload to S3-compatible storage, Google Cloud Storage, Azure Blob Storage or
Alibaba Cloud OSS, and a deployment ships with a bundled S3-compatible store so output has
somewhere to land with no extra setup.

!!! warning "Egress is expensive"

    Transcoding costs orders of magnitude more CPU than relaying the Room itself. Budget for it
    separately, and prefer Track Egress — the one type that writes the published track as-is,
    without transcoding — whenever the output format allows it.

## How far does it scale?

This is where honest numbers matter more than adjectives.

| Scenario | What OpenVidu does today |
|---|---|
| One stream, up to ~1000 viewers | Documented benchmark: 1 publisher and up to **1000 subscribers in a single Room** on a 4-CPU server |
| Many simultaneous streams | **OpenVidu Elastic** and **High Availability** distribute Rooms across several Media Nodes, with autoscaling so capacity follows demand |
| One stream, far beyond 1000 viewers | A single Room is **not yet distributed across Media Nodes**. Cascading media servers is on the roadmap, not shipped |
| A passive audience of any size | Add an **HLS segment output** and serve it from a CDN, accepting that tier's latency for viewers who do not interact |

The load-balancing strategy for placing new Rooms is configurable (by CPU load, system load, room
count, client count, track count or bandwidth) — see
[scalability](docs/self-hosting/production-ready/scalability.md).

Two things are worth knowing before you plan a production stream. First, the media server is
**mediasoup**, not the Pion SFU that base LiveKit uses, which the
[performance benchmarks](docs/self-hosting/production-ready/performance.md) put at roughly **2× the
tracks per server**. Second, availability depends on the deployment type: a Single Node is **not**
fault tolerant, OpenVidu Elastic tolerates losing a Media Node (the Room is rebuilt elsewhere after
a short interruption) but its single Master Node is still a single point of failure, and only
OpenVidu High Availability, with four Master Nodes, survives losing one of those. The
[fault tolerance](docs/self-hosting/production-ready/fault-tolerance.md) page has the failure matrix.

## The cost model

OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } is open source and free: you pay
your cloud provider for servers and egress bandwidth, and nothing else. OpenVidu
**PRO**{ .openvidu-tag .openvidu-pro-tag }, which is what adds Elastic and High Availability
deployments and autoscaling, costs **$0.0006 per core per minute** for the cores available to the
cluster while it is running — see the [worked examples](pricing.md).

The practical consequence for streaming is that **nothing is billed per viewer or per streamed
minute**. Your bill tracks the capacity you keep provisioned, so an audience that doubles inside
your existing headroom is free, and the lever you manage is autoscaling rather than a rate card.
That is the opposite of the CPaaS model, and it is usually the reason teams with predictable,
recurring streams move to self-hosting.

## When OpenVidu is not the right answer

- **A one-way broadcast to a huge passive audience.** If nobody talks back, sub-second latency buys
  you nothing and a plain HLS-over-CDN stack is cheaper and simpler.
- **A single stream that must reach far more than a thousand viewers with sub-second latency.**
  Until Rooms cascade across Media Nodes, that needs a hybrid design or a different architecture —
  [comparing OpenVidu](docs/comparing-openvidu.md) is explicit that this is work in progress, and
  that LiveKit Cloud's massive rooms currently cover it where open-source LiveKit does not.
- **A video-on-demand catalogue.** OpenVidu records and exports; it is not a VOD platform, a
  packager or a DRM system.
- **You want someone else to run it.** OpenVidu is self-hosted only: there is no hosted tier. If
  running media servers is not something your team wants to own, a CPaaS is the honest answer.

## Frequently asked questions

### Is WebRTC good for live streaming to many viewers?

It is the only mainstream option that delivers sub-second latency, so it is the right choice when
viewers act on what they see — auctions, betting, live shopping, remote operation, interactive
events. It is the wrong choice when you only need playback at massive scale with no interaction:
HLS and DASH over a CDN are cheaper for that, at 10–45 seconds of delay.

### How many viewers can one OpenVidu Room handle?

OpenVidu's documented benchmark is 1 publisher and up to 1000 subscribers in a single Room on a
4-CPU server. A single Room is not yet distributed across several Media Nodes, so 1000 viewers is
the practical per-Room ceiling today; OpenVidu Elastic and High Availability scale the number of
simultaneous Rooms, not the size of one. Beyond that, add an HLS output for the non-interactive
audience.

### How do I push a stream into OpenVidu?

Through Ingress, which accepts WHIP (WebRTC over HTTP, the only input that can skip transcoding),
RTMP from encoders such as OBS, and URL pull for HLS streams, media files and RTSP IP cameras. OBS
has spoken WHIP natively since version 30, with no plugin and no code.

### Can OpenVidu output HLS as well as WebRTC?

Yes. Egress can produce HLS segments and a playlist, push RTMP or SRT to platforms such as YouTube
or Twitch, write MP4 files and capture thumbnails — from the same Room, at the same time. A common
design is WebRTC for the interactive core and HLS over a CDN for the long tail of passive viewers.

### What does self-hosted live streaming cost?

OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } is open source and free, so you pay
only for your own servers and bandwidth. OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }, which
adds the Elastic and High Availability deployments and autoscaling, is $0.0006 per core per minute
for the cores available to your cluster. Neither edition charges per viewer or per streamed minute,
so cost tracks the capacity you provision rather than the size of your audience.

<div class="centered-section" markdown>

[Get started with Platform](docs/getting-started.md){ .md-button .md-button--primary }
[Compare Meet vs Platform](openvidu-meet-vs-openvidu-platform.md){ .md-button }

</div>

<div class="second-slogan cta-section" data-sal="slide-up">
  <h2 class="cta-title">Sizing a live-streaming deployment?</h2>
  <p class="cta-lead">Tell us your publisher and viewer numbers and we will help you size it and pick the right architecture.</p>
  <div class="home-buttons">
    <a href="/support/#talk-to-an-expert" class="md-button home-secondary-button">Talk to an expert</a>
  </div>
</div>
