---
title: "OpenVidu vs Agora: A Self-Hosted Alternative"
description: "The self-hosted alternative to Agora: run media servers yourself, own your recordings, and pay a flat per-core rate instead of per-minute by resolution."
# Structured Q&A metadata for this page's FAQ section. It feeds the JSON-LD
# (schema.org FAQPage) emitted by overrides/partials/json-ld.html. Keep in
# sync with the page content below: 'anchor' must match the heading id, and
# each answer must summarize the visible content of its section.
faq:
  - anchor: can-agora-be-self-hosted
    question: "Can Agora be self-hosted?"
    answer: >-
      No. Agora's real-time media runs on SD-RTN, Agora's own Software-Defined Real-Time Network,
      and there is no on-premises deployment of that service. Agora does offer an On-Premise
      Recording SDK that runs a recorder in your own infrastructure, but the calls themselves are
      still routed through Agora's network. OpenVidu is the opposite: it is self-hosted only, with
      no SaaS tier at all.
  - anchor: how-does-agora-pricing-work
    question: "How does Agora pricing work?"
    answer: >-
      Agora bills per user per minute, and the rate depends on the aggregate resolution of all
      video streams that user subscribes to. Agora's published rate card is $0.99 per 1,000 minutes
      for audio, $3.99 for HD video, $8.99 for Full HD, $15.99 for 2K and $35.99 for 2K+, with the
      first 10,000 minutes each month free. Because resolutions are summed across the streams a
      user receives, a larger call can push every participant into a higher-priced tier.
  - anchor: what-does-it-take-to-migrate-from-agora-to-openvidu
    question: "What does it take to migrate from Agora to OpenVidu?"
    answer: >-
      A port of the media layer, not a redesign. Agora's channel plus uid plus RTC token model maps
      onto OpenVidu's room plus identity plus access token model almost one to one, and your server
      keeps the same job: mint a token scoped to a room for a named user. The client code changes,
      because Agora's SDKs are Agora-specific and OpenVidu uses the LiveKit-compatible SDKs.
  - anchor: does-openvidu-work-for-global-audiences-the-way-agoras-sd-rtn-does
    question: "Does OpenVidu work for global audiences the way Agora's SD-RTN does?"
    answer: >-
      Within limits worth being honest about. OpenVidu deploys on AWS, Azure, GCP, DigitalOcean and
      Oracle Cloud, so you can run nodes in the regions your users are in, and a single 4 vCPU node
      is benchmarked at 1 publisher plus 1,000 subscribers for streaming. What you do not get is a
      ready-made global edge network spanning 200+ countries — that is what Agora sells, and
      matching it with self-hosted nodes is real engineering work.
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

# OpenVidu vs Agora

**OpenVidu is an open-source, self-hosted platform for real-time video** — a
[fork of LiveKit](openvidu-vs-livekit.md) that runs on your own servers, in your own cloud account.
Agora is a CPaaS built on SD-RTN, its own global network, billed per user per minute at a rate that
rises with video resolution. This page compares the two on pricing model, data location,
recordings, scale and what a migration actually involves.

<div class="centered-section" markdown>

[Get started with Platform](docs/index.md){ .md-button .md-button--primary }
[Compare Meet vs Platform](openvidu-meet-vs-openvidu-platform.md){ .md-button }

</div>

!!! info "Facts on this page were checked against Agora's own documentation on 16 September 2026"
    Competitor pricing changes often, and Agora publishes both a rate card and volume pricing.
    Every Agora figure below links to the Agora page it came from — check it before making a
    decision.

## At a glance

| | **OpenVidu** | **Agora** |
| --- | --- | --- |
| Model | Self-hosted only, on your infrastructure or your cloud account | CPaaS on SD-RTN, Agora's own global network |
| Pricing unit | Free**COMMUNITY**{ .openvidu-tag .openvidu-community-tag }; flat **$0.0006/core/minute****PRO**{ .openvidu-tag .openvidu-pro-tag }, plus your own server costs | **Per user per minute, priced by aggregate video resolution** — $0.99 to $35.99 per 1,000 minutes |
| Free tier | Everything in **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }, with no usage limit | First 10,000 minutes per month |
| License | Apache 2.0**COMMUNITY**{ .openvidu-tag .openvidu-community-tag } / commercial**PRO**{ .openvidu-tag .openvidu-pro-tag } | Proprietary SaaS |
| Where media is processed | Wherever you deploy — any region, any provider, on-premises | Agora's SD-RTN; region can be restricted with geofencing |
| Recordings | [Bundled Egress](docs/reference/egress.md), written to your own S3-compatible storage | Cloud Recording, billed per minute, written to your own cloud storage |
| Client SDKs | [8 LiveKit-compatible SDKs](docs/tutorials/application-client/index.md), including native Android and iOS | Agora SDKs for web, iOS, Android, desktop and game engines |
| Server API | [Full server API](docs/reference/room-service-api.md) and [webhooks](docs/reference/webhooks.md#events), self-hosted | Agora RESTful APIs and Notifications |
| Ready-to-use app | [OpenVidu Meet](meet/index.md), deployable as-is or [embeddable](meet/embedded/intro.md) | None — SDK only |
| Scaling | [Elastic and HA modes](docs/self-hosting/production-ready/scalability.md)**PRO**{ .openvidu-tag .openvidu-pro-tag }, one-click deploy on 5 cloud providers | Agora's problem, not yours; 200+ countries and regions |

Sources for the Agora column: [Video Calling pricing :fontawesome-solid-external-link:{.external-link-icon}](https://docs.agora.io/en/video-calling/overview/pricing){:target="_blank"},
[agora.io pricing :fontawesome-solid-external-link:{.external-link-icon}](https://www.agora.io/en/pricing/){:target="_blank"},
[Cloud Recording overview :fontawesome-solid-external-link:{.external-link-icon}](https://docs.agora.io/en/cloud-recording/overview/product-overview){:target="_blank"},
[Video Calling overview :fontawesome-solid-external-link:{.external-link-icon}](https://docs.agora.io/en/video-calling/overview/product-overview){:target="_blank"}.

## The part of Agora's pricing that surprises people

Agora's rate card is per 1,000 minutes, and the rate depends on resolution
([Video Calling pricing :fontawesome-solid-external-link:{.external-link-icon}](https://docs.agora.io/en/video-calling/overview/pricing){:target="_blank"},
checked 16 Sep 2026):

| Service | Ratio | Per 1,000 minutes |
| --- | --- | --- |
| Audio | 1:1 | $0.99 |
| Video HD (≤ 921,600 px) | 1:4 | $3.99 |
| Video Full HD (≤ 2,073,600 px) | 1:9 | $8.99 |
| Video 2K (≤ 3,686,400 px) | 1:16 | $15.99 |
| Video 2K+ (> 3,686,400 px) | 1:36 | $35.99 |

The first 10,000 minutes each month are free
([agora.io pricing :fontawesome-solid-external-link:{.external-link-icon}](https://www.agora.io/en/pricing/){:target="_blank"}),
and volume commitments are priced below the card rate — Agora's pricing page currently advertises
RTC "starting at $0.59 per 1,000 minutes".

The mechanic worth understanding before you model costs is how the tier is chosen. Agora's docs
state it plainly: *"Agora calculates video usage for each user based on aggregate resolution, which
is the combined resolution of all video streams a user subscribes to."* Resolutions are **summed**,
not taken per stream. So a four-person call in which everyone sends 720p puts each participant at
3 × 921,600 = 2,764,800 pixels of subscribed video — the **2K** tier, at $15.99 per 1,000 minutes,
even though nobody is sending anything above 720p.

That is not a criticism of the model; it is a faithful reflection of what an SFU actually costs to
run, and it is transparently documented. But it means your bill grows with the *square* of a call's
size, not linearly, and it is why per-minute video pricing tends to surprise teams whose product
grows from 1:1 calls into group sessions.

For contrast, OpenVidu's unit does not know how many people are in the room or what resolution they
are sending. **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } is free; **PRO**{ .openvidu-tag .openvidu-pro-tag } is a
flat **$0.0006 per core per minute** while your cluster runs, on top of your server costs. A worked
example, using OpenVidu's own [published benchmark](docs/self-hosting/production-ready/performance.md)
of 50 concurrent 8-participant conferences on 4 vCPU — **10,000 hours of four-person 720p meetings
in a month**:

| | **Agora (rate card)** | **OpenVidu PRO** |
| --- | --- | --- |
| Billable units | 2,400,000 user-minutes at the 2K tier | 4 vCPU × 43,200 minutes |
| Rate | $15.99 / 1,000 minutes | $0.0006 / core-minute |
| **Monthly** | **≈ $38,400** | **$103.68** + the server |

Two honest asterisks on that table. The Agora figure is the published card rate applied to the
documented aggregate-resolution rule — a real committed-volume contract would be lower, and only
Agora can quote it. The OpenVidu figure is licence cost only: you also pay for the machine and you
own the uptime, and it assumes peak concurrency fits the node (10,000 hours over a month averages
roughly 14 concurrent four-person meetings, well inside the benchmark, but bursty traffic must be
sized for the peak). See the [worked pricing examples](pricing.md) for several cluster sizes.

## Data location, and who holds the media

Agora routes media through **SD-RTN**, which its docs describe as a Software-Defined Real-Time
Network supporting *"video users in over 200 countries and regions"*
([Video Calling overview :fontawesome-solid-external-link:{.external-link-icon}](https://docs.agora.io/en/video-calling/overview/product-overview){:target="_blank"}).
For data-residency requirements Agora offers **geofencing**: you restrict the SDK to a named area
such as Europe, India, Japan, North America, Asia or mainland China, and it will only connect to
SD-RTN nodes inside it
([geofencing :fontawesome-solid-external-link:{.external-link-icon}](https://docs.agora.io/en/server-gateway/develop/network-geofencing){:target="_blank"}).
That is a genuine control, and for many regulated workloads it is enough.

What it does not change is who operates the machines. With OpenVidu there is no third party in the
media path at all: you deploy the media servers where you need them — a specific cloud region, a
specific country, your own datacentre, an air-gapped network — and nothing transits infrastructure
you do not operate. For teams whose compliance answer has to be "our servers, our region, our
retention policy" rather than "our vendor's region", that difference is the whole decision.

Recordings are the one place Agora already behaves the way self-hosters want: Cloud Recording writes
to your own third-party storage — Amazon S3, Azure, Google Cloud, Alibaba, Tencent and others — with
Agora's own servers used only as a fallback if that write fails
([Cloud Recording overview :fontawesome-solid-external-link:{.external-link-icon}](https://docs.agora.io/en/cloud-recording/overview/product-overview){:target="_blank"}).
Credit where it is due. The difference is the meter: Agora bills recording per minute on top of the
call, while OpenVidu's [Egress](docs/reference/egress.md) is bundled in
**COMMUNITY**{ .openvidu-tag .openvidu-community-tag } and runs on cores you are already paying for, writing to
S3-compatible storage (MinIO out of the box).

## What the migration actually involves

Moving from Agora to OpenVidu is a **port of the media layer**. Agora's SDKs are Agora-specific, so
there is no drop-in swap the way there is [coming from LiveKit](openvidu-vs-livekit.md), where the
same SDKs work against OpenVidu with only a URL change.

The concepts map closely, because both are token-authenticated SFU platforms:

| Agora | OpenVidu (LiveKit-compatible) |
| --- | --- |
| Channel, joined by name | [Room](docs/reference/room-service-api.md#rooms), joined by name |
| `uid` — the user identifier inside a channel | Participant `identity` |
| App ID + App Certificate, held on your server | API key + API secret, held on your server |
| RTC token: generated server-side, scoped to a channel name and uid, max 24 h | [Access token](docs/reference/access-tokens.md#video-grants): generated server-side, scoped to a room via the `roomJoin` grant, with its own TTL |
| Host / audience roles | Publish and subscribe grants on the token |
| Cloud Recording REST API | [Egress](docs/reference/egress.md) |
| Notifications (webhooks) | [Webhooks](docs/reference/webhooks.md#events) |

Your server keeps the same job — mint a short-lived token that lets a named user into a named
room — and your application logic about who may join, when to record and what happens on
disconnect carries over unchanged. The client code is the work: swapping Agora's client for one of
OpenVidu's [8 LiveKit-compatible SDKs](docs/tutorials/application-client/index.md).

Two practical notes. You can migrate incrementally, because OpenVidu is just a URL your clients
connect to, so one cohort or one feature can move first. And if what you want is a finished meeting
application rather than an SDK to build one with, [OpenVidu Meet](meet/index.md) is deployable as-is
and [embeddable in your product](meet/embedded/intro.md) with a web component — often a shorter path
than porting SDK code.

## When Agora is still the right call

To be fair about it:

- **Global reach you do not want to operate.** SD-RTN spans 200+ countries and regions, including
  mainland China, where self-hosting has its own regulatory and network realities. Reproducing that
  footprint with your own nodes is a serious project.
- **No infrastructure team.** A CPaaS means nobody carries a pager for media servers. Self-hosting
  moves that responsibility to you, and that is a real cost even when the invoice is smaller.
- **Low or very spiky usage.** 10,000 free minutes a month and per-minute billing after that is
  hard to beat for a product with occasional calls, and it absorbs a sudden 10x without anyone
  sizing a cluster.
- **Breadth of SDK targets.** Agora ships SDKs for game engines and desktop frameworks that a
  WebRTC platform aimed at web and mobile does not cover.

OpenVidu makes sense when data location is a requirement rather than a preference, when sustained
concurrency or group-call sizes make aggregate-resolution billing painful, or when you want the
cost of your video stack to track the hardware you run rather than the minutes your users spend.

## Frequently asked questions

### Can Agora be self-hosted?

No. Agora's real-time media runs on SD-RTN, Agora's own Software-Defined Real-Time Network, and
there is no on-premises deployment of that service. Agora does offer an On-Premise Recording SDK
that runs a recorder in your own infrastructure, but the calls themselves are still routed through
Agora's network. OpenVidu is the opposite: it is
[self-hosted only](docs/self-hosting/deployment-types.md), with no SaaS tier at all.

### How does Agora pricing work?

Agora bills per user per minute, and the rate depends on the aggregate resolution of all video
streams that user subscribes to. Agora's published rate card is $0.99 per 1,000 minutes for audio,
$3.99 for HD video, $8.99 for Full HD, $15.99 for 2K and $35.99 for 2K+, with the first 10,000
minutes each month free. Because resolutions are summed across the streams a user receives, a
larger call can push every participant into a higher-priced tier.

### What does it take to migrate from Agora to OpenVidu?

A port of the media layer, not a redesign. Agora's channel plus `uid` plus RTC token model maps onto
OpenVidu's room plus identity plus access token model almost one to one, and your server keeps the
same job: mint a token scoped to a room for a named user. The client code changes, because Agora's
SDKs are Agora-specific and OpenVidu uses the LiveKit-compatible SDKs.

### Does OpenVidu work for global audiences the way Agora's SD-RTN does?

Within limits worth being honest about. OpenVidu deploys on AWS, Azure, GCP, DigitalOcean and
Oracle Cloud, so you can run nodes in the regions your users are in, and a single 4 vCPU node is
[benchmarked](docs/self-hosting/production-ready/performance.md) at 1 publisher plus 1,000
subscribers for streaming. What you do not get is a ready-made global edge network spanning 200+
countries — that is what Agora sells, and matching it with self-hosted nodes is real engineering
work.

<div class="centered-section" markdown>

[Start with a tutorial](docs/tutorials/application-server/index.md){ .md-button .md-button--primary }
[Comparing Twilio Video instead?](openvidu-vs-twilio-video.md){ .md-button }

</div>

<div class="second-slogan cta-section" data-sal="slide-up">
  <h2 class="cta-title">Modelling the cost of moving off a per-minute video API?</h2>
  <p class="cta-lead">Tell us your concurrency, resolutions and data requirements and we will help you size the cluster and scope the migration.</p>
  <div class="home-buttons">
    <a href="/support/#talk-to-an-expert" class="md-button home-secondary-button">Talk to an expert</a>
  </div>
</div>
