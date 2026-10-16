---
title: "OpenVidu vs Twilio Video: Self-Hosted Alternative"
description: "The self-hosted alternative to Twilio Video: run the media servers yourself, own the recordings, and pay per core instead of per participant-minute."
# Structured Q&A metadata for this page's FAQ section. It feeds the JSON-LD
# (schema.org FAQPage) emitted by overrides/partials/json-ld.html. Keep in
# sync with the page content below: 'anchor' must match the heading id, and
# each answer must summarize the visible content of its section.
faq:
  - anchor: is-twilio-programmable-video-being-discontinued
    question: "Is Twilio Programmable Video being discontinued?"
    answer: >-
      No, not any more. Twilio announced an end of life for Programmable Video in late 2023, with a
      shutdown date that was later moved to 5 December 2026, and then reversed that decision on
      21 October 2024: Twilio Video "will remain a standalone product as part of our customer
      engagement platform". The product is generally available today. Many teams still went looking
      for an exit path during that period, which is the most common reason people compare Twilio
      Video with a self-hosted platform.
  - anchor: can-i-migrate-from-twilio-video-to-a-self-hosted-platform-without-rewriting-my-client
    question: "Can I migrate from Twilio Video to a self-hosted platform without rewriting my client?"
    answer: >-
      Not entirely. Twilio's client SDKs are Twilio-specific, so the code that connects, publishes
      and subscribes has to be rewritten against OpenVidu's LiveKit-compatible SDKs. The concepts
      map almost one to one — Room, Participant, Track, and a JWT minted on your server that grants
      access to a named room — so the work is a port of the media layer, not a redesign of your
      application. Your backend keeps the same shape: mint a token, create or close rooms, receive
      webhooks.
  - anchor: how-does-openvidu-pricing-compare-with-twilio-video
    question: "How does OpenVidu pricing compare with Twilio Video?"
    answer: >-
      They are different units. Twilio Video bills $0.004 per participant per minute in Group Rooms,
      plus composition and storage for recordings, so the bill tracks usage. OpenVidu COMMUNITY is
      free and OpenVidu PRO is $0.0006 per core per minute for the cluster you run, so the bill
      tracks capacity and your own server costs. Low, spiky usage usually favours the per-minute
      model; sustained usage favours the per-core one.
  - anchor: can-i-keep-using-twilio-for-sms-and-voice-while-self-hosting-video
    question: "Can I keep using Twilio for SMS and voice while self-hosting video?"
    answer: >-
      Yes. Programmable Video is a separate product from Twilio Voice and Messaging, and nothing
      about running your own media servers affects them. A common shape is exactly this split:
      Twilio keeps the telephony and notifications, where a CPaaS is hard to beat, and video moves
      in-house where data location and sustained concurrency make self-hosting worth it.
  - anchor: where-are-recordings-stored-with-openvidu
    question: "Where are recordings stored with OpenVidu?"
    answer: >-
      In your own S3-compatible storage. OpenVidu's Egress service is bundled and pre-wired to an
      S3-compatible bucket (MinIO out of the box), so recorded files never leave infrastructure you
      control and there is no per-GB-per-day storage meter. Twilio stores recordings on its own
      platform by default and offers an External S3 Recordings option to write them to your bucket
      instead.
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

# OpenVidu vs Twilio Video

**OpenVidu is an open-source, self-hosted platform for real-time video** — a
[fork of LiveKit](openvidu-vs-livekit.md) that runs on your own servers, in your own cloud account.
Twilio Programmable Video is a CPaaS: Twilio runs the media servers and bills you per participant
per minute. This page compares the two on pricing model, data location, recordings, scale and what
a migration actually involves.

<div class="centered-section" markdown>

[Get started with Platform](docs/index.md){ .md-button .md-button--primary }
[Compare Meet vs Platform](openvidu-meet-vs-openvidu-platform.md){ .md-button }

</div>

!!! info "Facts on this page were checked against Twilio's own documentation on 16 September 2026"
    Competitor pricing and product status change often. Every Twilio figure below links to the
    Twilio page it came from — check it before making a decision.

## Is Twilio Programmable Video being discontinued?

This is the first question most people arrive with, so: **no, not any more.**

Twilio announced an end of life for Programmable Video in late 2023, with a shutdown date that was
later moved to 5 December 2026. On **21 October 2024** Twilio reversed that decision. In Twilio's
own words: *"after extensive feedback from our community and consideration for our vision for the
future of customer engagement, we are thrilled to announce a reversal of this decision"*
([Twilio blog, 21 Oct 2024 :fontawesome-solid-external-link:{.external-link-icon}](https://www.twilio.com/en-us/blog/twilio-video-update-2024){:target="_blank"}),
and the accompanying changelog entry states that Twilio Video *"will remain a standalone product as
part of our customer engagement platform"*
([Twilio changelog :fontawesome-solid-external-link:{.external-link-icon}](https://www.twilio.com/en-us/changelog/-twilio-video-will-remain-a-standalone-product){:target="_blank"}).
Programmable Video is generally available today and Twilio has continued to ship features for it.

So this is not a page about a shutdown. It exists because a lot of teams spent 2024 building an
exit plan they never had to use, and came out of it wanting the same thing: a video stack whose
lifecycle they control. That is the honest case for self-hosting, and it is the case this page
makes.

## At a glance

| | **OpenVidu** | **Twilio Programmable Video** |
| --- | --- | --- |
| Model | Self-hosted only, on your infrastructure or your cloud account | CPaaS — Twilio runs the media servers |
| Pricing unit | Free**COMMUNITY**{ .openvidu-tag .openvidu-community-tag }; flat **$0.0006/core/minute****PRO**{ .openvidu-tag .openvidu-pro-tag }, plus your own server costs | **$0.004 per participant per minute** in Group Rooms, plus recording composition and storage |
| License | Apache 2.0**COMMUNITY**{ .openvidu-tag .openvidu-community-tag } / commercial**PRO**{ .openvidu-tag .openvidu-pro-tag } | Proprietary SaaS |
| Where media is processed | Wherever you deploy — any region, any provider, on-premises | One of Twilio's 9 media regions, or Global Low Latency |
| Participants per room | Bounded by the server you run ([50 concurrent 8-participant conferences on 4 vCPU](docs/self-hosting/production-ready/performance.md), benchmarked) | Up to 50 per Room |
| Recordings | [Bundled Egress](docs/reference/egress.md), written to your own S3-compatible storage | Stored by Twilio; External S3 Recordings writes to your bucket |
| Client SDKs | [8 LiveKit-compatible SDKs](docs/tutorials/application-client/index.md), including native Android and iOS | Twilio Video SDKs for JS, iOS and Android |
| Server API | [Full server API](docs/reference/room-service-api.md) and [webhooks](docs/reference/webhooks.md#events), self-hosted | Twilio REST API and webhooks |
| Ready-to-use app | [OpenVidu Meet](meet/index.md), deployable as-is or [embeddable](meet/embedded/intro.md) | None — SDK only |
| Scaling | [Elastic and HA modes](docs/self-hosting/production-ready/scalability.md)**PRO**{ .openvidu-tag .openvidu-pro-tag }, one-click deploy on 5 cloud providers | Twilio's problem, not yours |
| Telephony / SMS in the same account | No | Yes — Voice, Messaging and Flex |

Sources for the Twilio column: [pricing :fontawesome-solid-external-link:{.external-link-icon}](https://www.twilio.com/en-us/video/pricing){:target="_blank"},
[Rooms API :fontawesome-solid-external-link:{.external-link-icon}](https://www.twilio.com/docs/video/api/rooms-resource){:target="_blank"},
[media regions :fontawesome-solid-external-link:{.external-link-icon}](https://www.twilio.com/docs/video/ip-address-whitelisting){:target="_blank"},
[recordings :fontawesome-solid-external-link:{.external-link-icon}](https://www.twilio.com/docs/video/api/recordings-resource){:target="_blank"}.

## The pricing models don't reduce to one number

Twilio Video's published rates are per unit of usage
([pricing :fontawesome-solid-external-link:{.external-link-icon}](https://www.twilio.com/en-us/video/pricing){:target="_blank"},
checked 16 Sep 2026):

- **$0.004** per participant per minute in Group Rooms, participant recordings included.
- **$0.01** per composed minute to turn participant recordings into a single playable MP4.
- **$0.00167** per GB per day of media storage, first 10 GB free.
- **$0.027** per room per minute for real-time transcription.

OpenVidu's is per unit of capacity: **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } is free, and
**PRO**{ .openvidu-tag .openvidu-pro-tag } is a flat **$0.0006 per core per minute** while your cluster runs, on top of
whatever your servers cost. Recording, storage and transcription are not separately metered — they
run on the cores you are already paying for.

A worked example, using OpenVidu's own
[published benchmark](docs/self-hosting/production-ready/performance.md): **10,000 hours of
four-person meetings in a month**.

| | **Twilio Video** | **OpenVidu PRO** |
| --- | --- | --- |
| Billable units | 2,400,000 participant-minutes | 4 vCPU × 43,200 minutes |
| Rate | $0.004 / participant-minute | $0.0006 / core-minute |
| **Monthly** | **$9,600** | **$103.68** + the server |

The asterisk on the right-hand column is real and worth stating: OpenVidu's number is licence cost,
not total cost. You also pay for the machine, and you own the uptime. It assumes peak concurrency
fits the node — 10,000 hours spread across a month averages roughly 14 concurrent four-person
meetings, well inside the 50-concurrent-8-participant figure OpenVidu benchmarks on 4 vCPU, but a
bursty traffic shape needs sizing for the peak, not the average. See the
[worked pricing examples](pricing.md) for several cluster sizes.

The shape of the two curves is what matters more than either number. Per-participant-minute billing
is close to free at low volume and grows linearly forever; per-core billing has a floor and then
flattens. Somewhere between those two lines is the point where self-hosting starts paying for
itself, and where that point falls depends on your concurrency, not on your total minutes.

## Data location, and who holds the media

With Twilio, media is decrypted, processed and re-encrypted by a Twilio SFU in one of nine media
regions — `au1`, `br1`, `de1`, `ie1`, `in1`, `jp1`, `sg1`, `us1`, `us2` — or `gll`, Global Low
Latency, which is the default
([media regions :fontawesome-solid-external-link:{.external-link-icon}](https://www.twilio.com/docs/video/ip-address-whitelisting){:target="_blank"}).
You choose the region; Twilio holds the infrastructure. One constraint worth knowing early if you
are working to a data-residency requirement: Twilio's own docs state that *"the API Key you use to
create Access Tokens must be in the United States (US1) region"*
([access tokens :fontawesome-solid-external-link:{.external-link-icon}](https://www.twilio.com/docs/video/tutorials/user-identity-access-tokens){:target="_blank"}).

With OpenVidu there is no such question to answer, because there is no third party in the media
path. You deploy the media servers where you need them — a specific cloud region, a specific
country, your own datacentre, an air-gapped network — and the media never reaches a machine you do
not operate. This is the reason most people end up on this page, ahead of cost.

Recordings follow the same logic. Twilio stores recordings on its platform by default and offers
[External S3 Recordings :fontawesome-solid-external-link:{.external-link-icon}](https://www.twilio.com/docs/video/api/recordings-resource){:target="_blank"}
to write them to your own bucket, with a per-GB-per-day meter on Twilio-side storage. OpenVidu's
[Egress](docs/reference/egress.md) is bundled in **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } and pre-wired to
S3-compatible storage (MinIO out of the box), so the file lands in your bucket as the only copy,
with no storage meter.

## What the migration actually involves

Be clear-eyed about this: **moving from Twilio Video to OpenVidu is a rewrite of your media layer.**
Twilio's SDKs are Twilio-specific, so there is no drop-in swap the way there is
[coming from LiveKit](openvidu-vs-livekit.md), where the same SDKs work against OpenVidu with only
a URL change.

The good news is that the concepts line up almost exactly, because both are token-authenticated,
room-based SFU platforms:

| Twilio Video | OpenVidu (LiveKit-compatible) |
| --- | --- |
| `Room`, joined with `connect(token, { name })` | `Room`, joined with `room.connect(url, token)` |
| `Participant`, `LocalParticipant` | `Participant`, `LocalParticipant` |
| `Track` / `TrackPublication` | `Track` / `TrackPublication` |
| Access Token: JWT signed with an API Key Secret, carrying an identity and a `VideoGrant` scoped to a room name | [Access token](docs/reference/access-tokens.md#video-grants): JWT signed with your API secret, carrying an identity and a `roomJoin` grant scoped to a room name |
| REST API to create, list and complete Rooms | [Room service API](docs/reference/room-service-api.md) |
| Status callbacks | [Webhooks](docs/reference/webhooks.md#events) |
| Recording + Composition API | [Egress](docs/reference/egress.md), composited or per-track |

So the port is mechanical rather than architectural: your token-minting endpoint changes which
library it calls and which grant it writes, your client swaps one SDK for another with the same
object model, and your webhook handler changes its event names. Application logic — who may join
which room, when to start recording, what to do when someone leaves — carries over unchanged.

Two practical notes. First, you can do this incrementally: OpenVidu is just a URL your clients
connect to, so a single cohort or a single feature can move first. Second, if what you actually
want is a finished meeting application rather than an SDK to build one with,
[OpenVidu Meet](meet/index.md) is a deployable app you can
[embed in your product](meet/embedded/intro.md) with a web component — for some Twilio Video
integrations that is a shorter path than porting the SDK code at all.

## When Twilio Video is still the right call

Honestly: often.

- **You have no infrastructure team.** A CPaaS means nobody carries a pager for media servers.
  Self-hosting moves that responsibility to you, and that is a real cost even when the invoice is
  smaller.
- **Your usage is low or very spiky.** Per-participant-minute billing is close to free for a
  product with occasional calls, and it absorbs a sudden 10x without anyone sizing a cluster.
- **You need voice, SMS and video in one account.** Twilio's own stated direction for Video is
  tighter integration with Voice, Messaging and Flex. If your product is already built on Twilio,
  that consolidation is worth real money in engineering time.
- **You want global reach without operating it.** Twilio's Global Low Latency routing and media
  regions are there on day one; matching that with self-hosted nodes in several regions is work.

OpenVidu makes sense when data location is a requirement rather than a preference, when sustained
concurrency makes per-minute billing painful, or when you want the lifecycle of your video stack to
be your own decision — which, after the 2024 end-of-life episode, is a reason a lot of teams now
say out loud.

## Frequently asked questions

### Can I migrate from Twilio Video to a self-hosted platform without rewriting my client?

Not entirely. Twilio's client SDKs are Twilio-specific, so the code that connects, publishes and
subscribes has to be rewritten against OpenVidu's LiveKit-compatible SDKs. The concepts map almost
one to one — Room, Participant, Track, and a JWT minted on your server that grants access to a
named room — so the work is a port of the media layer, not a redesign of your application. Your
backend keeps the same shape: mint a token, create or close rooms, receive webhooks.

### How does OpenVidu pricing compare with Twilio Video?

They are different units. Twilio Video bills $0.004 per participant per minute in Group Rooms, plus
composition and storage for recordings, so the bill tracks usage. OpenVidu
**COMMUNITY**{ .openvidu-tag .openvidu-community-tag } is free and OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag } is
$0.0006 per core per minute for the cluster you run, so the bill tracks capacity and your own
server costs. Low, spiky usage usually favours the per-minute model; sustained usage favours the
per-core one.

### Where are recordings stored with OpenVidu?

In your own S3-compatible storage. OpenVidu's [Egress](docs/reference/egress.md) service is bundled
and pre-wired to an S3-compatible bucket (MinIO out of the box), so recorded files never leave
infrastructure you control and there is no per-GB-per-day storage meter. Twilio stores recordings
on its own platform by default and offers an External S3 Recordings option to write them to your
bucket instead.

### Can I keep using Twilio for SMS and voice while self-hosting video?

Yes. Programmable Video is a separate product from Twilio Voice and Messaging, and nothing about
running your own media servers affects them. A common shape is exactly this split: Twilio keeps the
telephony and notifications, where a CPaaS is hard to beat, and video moves in-house where data
location and sustained concurrency make self-hosting worth it.

<div class="centered-section" markdown>

[Start with a tutorial](docs/tutorials/application-server/index.md){ .md-button .md-button--primary }
[Comparing Agora instead?](openvidu-vs-agora.md){ .md-button }

</div>

<div class="second-slogan cta-section" data-sal="slide-up">
  <h2 class="cta-title">Planning a move off a per-minute video API?</h2>
  <p class="cta-lead">Tell us your concurrency and data requirements and we will help you size the cluster and scope the migration.</p>
  <div class="home-buttons">
    <a href="/support/#talk-to-an-expert" class="md-button home-secondary-button">Talk to an expert</a>
  </div>
</div>
