---
title: How Eventials cut live streaming incidents by 90% with OpenVidu
draft: false
date:
  created: 2026-11-04
slug: eventials-live-streaming-openvidu
description: >-
  How Brazilian webinar platform Eventials streams live broadcasts to 30,000+
  viewers on OpenVidu, and why incidents dropped after moving to OpenVidu 3.
cover_image: poster-light.webp
categories:
  - Success story
  - Vertical
tags:
  - WebRTC
  - Self-hosted
  - Live streaming
  - Webinars
  - LiveKit
  - Scalability
  - Migration
authors:
  - patxi
---

# How Eventials cut live streaming incidents by 90% with OpenVidu

![Eventials and OpenVidu customer success story](/assets/images/blog/YYYY/MM/eventials-live-streaming-openvidu/poster-light.webp#only-light "Eventials + OpenVidu"){ .round-corners }
![Eventials and OpenVidu customer success story](/assets/images/blog/YYYY/MM/eventials-live-streaming-openvidu/poster-dark.webp#only-dark "Eventials + OpenVidu"){ .round-corners }

Sometimes, companies face challenges for which they envision a solution that doesn't exist. **[Eventials :fontawesome-solid-external-link:{.external-link-icon}](https://eventials.com){:target="_blank"}** is one of them. When tackling 30,000+ viewer live streams, the team needed an infrastructure that could scale, while at the same time kept the costs low and under control, all of them without breaking their sanity. 

We talked to **Henrique Otsuka**, Head of Information Technology at Eventials, about how they produce those broadcasts on OpenVidu: what they tried before, why he led the move to OpenVidu 3, and how separating interaction from distribution lets them scale. For 13 years Eventials has run webinars, white-label corporate learning platforms and professional live streaming production for organizations across Latin America, being the largest webinar platform in Brazil.

<!-- more -->

## What is Eventials?

We started the interview by asking Henrique to describe the platform, and what role video plays within it:

> "Eventials is a technology platform specializing in webinars, corporate education through white-label Learning Management Systems (LMS), and professional live streaming production.
>
> We serve organizations that use video as a strategic tool for communication, training, and engagement. For these customers, stability, audiovisual quality, and the ability to support large audiences are essential.
>
> Our challenge is to deliver interactive experiences while simultaneously distributing content to thousands of viewers securely and reliably."


## Where OpenVidu fits

Given that the main Eventials' challenge was distributing iteractive video experiences to thousands of viewers, we asked where does OpenVidu sit in that picture:

> "OpenVidu powers real-time audiovisual communication between presenters and participants, as well as the video composition process.
>
> We use OpenVidu 3 with LiveKit and WebComposite Egress to render custom layouts developed in React directly on our servers, without relying on the presenter's computer for processing.

However, video processing for Eventials does not stop there, as Henrique says:

> The composed video is converted to RTMP and forwarded to AWS Elemental, which handles processing and distribution through HLS and CDN.
>
> This architecture separates interactive production from large-scale distribution, allowing each component to scale independently."

So the presenters' room is a regular OpenVidu Room. Presenters and invited participants join over WebRTC, with sub-second latency between them. The broadcast is composed on the server, and egress opens Eventials' own React layout in a headless browser and records it as a single video. That's what OpenVidu calls a Room Composite Egress with a [custom template](/docs/reference/egress.md#layouts-and-custom-templates): the output looks like Eventials' product, instead of a grid of raw cameras. Then, the output is sent as an RTMP stream. Egress pushes the composed video [over RTMP](/docs/reference/egress.md#streams) to AWS Elemental, which packages it as HLS and hands it to a CDN for the audience.

Eventials makes a smart use of WebRTC and HLS technologies, by chaining them and getting the best from both worlds. WebRTC and HLS are good at opposite things: WebRTC gives the presenters a real conversation, while HLS and a CDN give tens of thousands of viewers a cheap, cacheable stream. Our post on [WebRTC vs HLS and DASH](/blog/posts/2026/09/low-latency-live-streaming.md) goes deeper into that trade-off.

![Eventials architecture: presenters join an OpenVidu Room over WebRTC, a Room Composite Egress renders a custom React layout and pushes RTMP to AWS Elemental, which delivers HLS through a CDN to 30,000+ viewers](/assets/images/blog/YYYY/MM/eventials-live-streaming-openvidu/architecture-light.svg#only-light){ loading=lazy }
![Eventials architecture: presenters join an OpenVidu Room over WebRTC, a Room Composite Egress renders a custom React layout and pushes RTMP to AWS Elemental, which delivers HLS through a CDN to 30,000+ viewers](/assets/images/blog/YYYY/MM/eventials-live-streaming-openvidu/architecture-dark.svg#only-dark){ loading=lazy }

## Before OpenVidu: composing in the browser

We were interested on what Eventials used or considered before OpenVidu, so we asked Henrique explicitly about it:

> "We experimented with several approaches to audiovisual composition and delivering the resulting stream to our streaming infrastructure.
>
> One approach involved performing composition directly in the browser using Canvas, with processing handled by the presenter's computer and the resulting video transmitted over WebRTC for subsequent conversion to RTMP.
>
> We also explored rendering Next.js interfaces in serverless computing environments.
>
> These approaches presented challenges related to performance, stability, and synchronization, particularly when processing depended on the presenter's hardware and network connectivity.
>
> We were looking for a solution that could centralize audiovisual composition on the server side and simplify the integration between WebRTC and RTMP."

Composing on the presenter's machine sounds cheap, but it has a major drawback: any hiccup on that machine goes straight into the broadcast that thousands of people are watching. Moving composition to the server takes the presenter's hardware out of the critical path.

## Why OpenVidu, and why they moved to OpenVidu 3

We asked Eventials on the decision that led them to choose OpenVidu for their critical video infrastructure:

> "We adopted OpenVidu 2 in 2022 because it supported audiovisual composition with customizable layouts, synchronization with presenters, and WebRTC-to-RTMP conversion.
>
> However, we experienced stability and troubleshooting challenges in certain scenarios.

Indeed, later on, Henrique personally still choose OpenVidu again after studying the migration path and the features and architecture of OpenVidu 3:

> In 2026, I personally led the decision to migrate to OpenVidu 3 after thoroughly studying its architecture and documentation. My previous experience with LiveKit and familiarity with Pion also influenced that decision.
>
> The integration with the LiveKit ecosystem represented an opportunity to improve stability, simplify communication between microservices, and expand the capabilities available to support Eventials' business logic.
>
> Infrastructure autonomy and cost control were also important factors."

OpenVidu 3 is built on LiveKit and 100% compatible with LiveKit APIs and SDKs, and that was a key factor in his decision. The team was able to use their knowledge on LiveKit's SDKs and the Pion WebRTC stack, while OpenVidu added the self-hosted deployment, scaling and operations around it.

## Integration and architecture

We asked Henrique about how did the integration go:

> "The integration was significantly simplified by the SDKs, which made managing rooms, participants, devices, and WebRTC connections much easier.
>
> Our architecture uses microservices to integrate sessions with Eventials' business logic, while the frontend manages the participants' audiovisual experience.
>
> The main challenges involved network fluctuations, connection recovery, and providing clear feedback to users during connectivity issues.
>
> With OpenVidu 3, integration with LiveKit's capabilities and the ability to compose custom React layouts contributed to a more stable and flexible architecture."

We were interested on how they deployed and managed the stack, so asked if they could give us some details:

> "We operate a regionally distributed infrastructure to serve customers across Latin America, including Brazil, Chile, and Mexico.
>
> This distribution is designed to reduce latency and minimize connectivity issues caused by international network routes and different internet service providers."

Regional distribution pays off twice in this architecture. Presenters connect to a media server close to them, and the RTMP leg from Egress to the ingest endpoint stays short. That second part is easy to overlook: RTMP and SRT are sensitive to long distances, which is why we recommend placing ingest endpoints close to the servers running Egress. Self-hosting is what lets Eventials choose those locations, across the [deployment types](/docs/self-hosting/deployment-types.md) OpenVidu supports.

## Most valuable features

Audiovisual composition, self-hosting, and the LiveKit compatibility were the main factors that drove Eventials towards choosing OpenVidu. However, once integrated, which other features of the OpenVidu platform matter most to Eventials?

> "The most important capabilities for us are audiovisual composition, WebRTC-to-RTMP conversion, and integration with LiveKit's features.
>
> WebComposite Egress allows us to produce broadcasts with customized React layouts, rendered directly on our servers.
>
> We also use features such as webhooks, Data Channels, room and participant management, connection quality events, and automatic reconnection.
>
> These capabilities simplify integration with our microservices and allow us to build experiences tailored to our customers' needs."

We asked Henrique about the OpenVidu edition they use:

> "We use **OpenVidu PRO**, primarily because of our platform's operational requirements and the need to maintain control over our audiovisual infrastructure.
>
> We also value having access to specialized support for a technology that plays an essential role in our operations."

## Eventials' experience with OpenVidu

What changed for Eventials once adopting OpenVidu?

> "Adopting OpenVidu allowed us to reduce development complexity and focus our engineering efforts on Eventials' core product capabilities.
>
> The most significant improvement came with the migration to OpenVidu 3, which delivered greater stability and better integration with our platform's services.
>
> Previously, we experienced incidents involving video freezes, audio loss, black screens, Egress failures, and difficulties recovering connections.
>
> **Following the migration, we estimate that incidents related to live streaming operations decreased by approximately 90%.**"

However, there were also other factors beside end-user experience that paid back: 

> In addition to improving the customer experience, we reduced the need for operational intervention and increased our ability to evolve the platform.
>
> Self-hosting also provides greater cost predictability and control, although we do not have a consolidated financial comparison with SaaS alternatives."

For a live broadcast, every one of those incidents is visible. A frozen frame or a black screen in a webinar ends up watched by thousands of people. Hence, cutting them by an estimated 90% means fewer emergencies for the operations team during events, and more time to build the product.

## Scaling for the biggest events

How does the platform behave when the audience is at its largest?

> "Our architecture separates interactive WebRTC communication from large-scale video distribution through AWS Elemental and CDN.
>
> This allows us to scale viewership without proportionally increasing the number of connections to our OpenVidu servers.
>
> We have successfully served **more than 30,000 concurrent viewers during a single event** and validated up to 30 concurrent WebRTC rooms with four participants each.
>
> For these scenarios, we focus on infrastructure capacity planning, regional server distribution, and monitoring the entire audiovisual pipeline, from WebRTC publishing to delivery to the end viewer."

Notice the asymmetry: more than 30,000 viewers, against a WebRTC layer validated for around a hundred active participants. The audience never touches the media servers, so it can grow without the OpenVidu deployment growing with it. What does have to scale is Egress, since composing video in a headless browser is the most CPU-intensive job in the pipeline. That's why capacity planning comes first in Henrique's list. If you're planning a similar setup, our [scalability roadmap for video conferencing](/blog/posts/2026/06/scalability-in-videoconferencing-systems.md) covers the media-plane side of it.

## About OpenVidu's support and documentation

We asked about their experience with OpenVidu support and documentation, and what we should improve. Henrique was honest:

> "Our experience has been positive regarding the platform's technological evolution, particularly with the OpenVidu 3 architecture.
>
> However, during complex incidents involving OpenVidu 2, the support team was not always able to effectively identify or resolve the underlying issues, requiring our engineering team to conduct independent investigations.
>
> During the migration to OpenVidu 3, we received support in the form of testing credits, which made it easier to evaluate the new architecture.
>
> I believe the main opportunities for improvement are in documentation covering advanced production scenarios, troubleshooting, infrastructure sizing, and diagnosing Egress and WebRTC connection failures."

That's fair, and it's the kind of feedback we want. Diagnosing failures in a live media pipeline is hard, and the documentation should carry more of that weight. Some of it is already there: a [recording troubleshooting guide](/docs/troubleshooting/recording.md) that covers Egress CPU limits and failed recordings, the [observability stack](/docs/self-hosting/production-ready/observability/index.md) with the OpenVidu Dashboard (which will get a full rework for OpenVidu 3.10) and Grafana, and [how-to guides](/docs/self-hosting/how-to-guides/index.md) for production setups. We also write up real failures in public, like the [full disk that broke recordings across a whole cluster](/blog/posts/2026/10/black-hole-node.md). Sizing and advanced production scenarios are where we still have work to do.

## What's next for Eventials on the WebRTC side?

What does the team want to build next?

> "We are exploring opportunities to integrate live streaming with artificial intelligence, including automatic transcription, subtitles, summary generation, and audiovisual content analysis.
>
> We also see significant potential in using AI agents integrated with our media infrastructure, leveraging the capabilities of the LiveKit ecosystem.
>
> These possibilities are part of our long-term technology vision, although we do not currently have a publicly defined roadmap for their implementation."

Most of that maps onto pieces OpenVidu already ships. [Live Captions](/docs/ai/live-captions.md#local-providers) transcribe a Room in real time, with providers that run on your own servers if the audio must not leave your infrastructure. For summaries and analysis, [custom agents](/docs/ai/custom-agents.md) join a Room like any participant. Our post on [building a transcriber and summarizer agent](/blog/posts/2026/08/transcriber-summarizer-agent.md) shows one end to end.

## Henrique's advice for teams scaling WebRTC

We closed by asking what he would tell an engineering team struggling to scale live video on their own WebRTC infrastructure:

> "My main recommendation is to separate the infrastructure responsible for interactive communication from the infrastructure used to distribute video to large audiences.
>
> WebRTC is excellent for low-latency interactions, but it is not necessarily the most efficient approach for delivering content to tens of thousands of viewers.
>
> I also believe it is essential to invest in observability, connection recovery, and troubleshooting capabilities, as the biggest challenges tend to emerge under real-world production conditions.
>
> Finally, I recommend adopting established technologies and keeping business logic decoupled from the underlying media infrastructure.
>
> OpenVidu does not eliminate the complexity of WebRTC, but it allows engineering teams to focus more on the product experience and the platform's evolution."

## Key takeaways

- **Split interaction from distribution.** Presenters talk over WebRTC; the audience watches over HLS and a CDN. Each side scales on its own terms.
- **Compose on the server, not on the presenter's laptop.** A Room Composite Egress with a custom React template turns the room into a branded broadcast, independent of anyone's hardware or home connection.
- **The audience never touches the media servers.** 30,000+ concurrent viewers in one event, on a WebRTC layer validated for up to 120 active participants.
- **The move to OpenVidu 3 paid off.** Eventials estimates live streaming incidents dropped by about 90%, freeing the team from firefighting during events.
- **Regional deployment is part of the design.** Media servers in Brazil, Chile and Mexico keep both the presenters' connections and the RTMP leg short.
- **Observability is a must-have.** Henrique's advice, and his feedback to us, both come back to being able to diagnose what breaks in production.
- **Building on self-hosted solutions such as OpenVidu leaves room for working on the product experience.** Eventials experience shows that by adopting OpenVidu and getting rid of the WebRTC management and egress, made room for them to work more on the product experience.

## Thiking about building a live streaming or webinar platform?

If you need presenters on WebRTC and a broadcast composed on your own servers, [OpenVidu Platform](/docs/index.md) gives you the SDKs, the [Egress service](/docs/reference/egress.md) Eventials uses for composition and RTMP output, and the self-hosted deployment to run it all where your audience is. Start with the [deployment types](/docs/self-hosting/deployment-types.md) to find the setup that fits your scale.

If what you need is a ready-made videoconferencing app instead of building one from scratch, then have a look at [OpenVidu Meet](/meet/index.md).

And if you're not sure which fits, the [Meet vs Platform comparison](/openvidu-meet-vs-openvidu-platform.md) helps you decide.

!!! tip "Thinking about your own success story?"
    We're always happy to talk to teams building real-time features. If you're an OpenVidu user with a story like this one, [get in touch](/support/index.md): we'll do the writing, you get the visibility and the backlinks.

*Our thanks to Henrique Otsuka and the Eventials team for sharing their experience.*
