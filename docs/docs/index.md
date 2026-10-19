---
title: "OpenVidu Platform: Self-Hosted WebRTC SDKs"
description: "Build real-time video, audio and AI applications on infrastructure you control, with LiveKit-compatible SDKs and a self-hosted media server."
hide:
  - toc
page_features:
  - landingstyles
  - revealonscroll
---

<div class="ov-landing ov-landing--product" markdown>

<section class="ov-hero" markdown>

![](../assets/images/logos/platform_greyfont_transback.png#only-light){ .ov-hero__logo .skip-gallery .not-selectable width=1648 height=345 }
![](../assets/images/logos/platform_whitefont_transback.png#only-dark){ .ov-hero__logo .skip-gallery .not-selectable width=1648 height=345 }

<h1 class="ov-hero__title">OpenVidu Platform: self-hosted WebRTC SDKs for real-time apps</h1>

<p class="ov-hero__lead" markdown="span">OpenVidu Platform enables you to build real-time applications. You can build your new OpenVidu application from scratch, but it is also very easy to integrate OpenVidu in your already existing application.</p>

<div class="ov-actions" markdown>
[Get started](./getting-started.md){ .ov-btn .ov-btn--ink title="Get started with OpenVidu Platform" }
[Start with a tutorial](./tutorials/application-server/index.md){ .ov-link }
[Build your app](./build-your-app/index.md){ .ov-link }
</div>

</section>

<section class="ov-section" data-sal="slide-up" markdown>

<div class="ov-panel ov-panel--platform" markdown>
<div class="ov-door__head" markdown="span">
<span class="ov-door__name">Your first lines of code</span>
<span class="ov-door__badge">LiveKit-compatible SDKs</span>
</div>

<p class="ov-door__text" markdown="span">Real-time video in your app takes a few lines with our LiveKit fork's SDKs. Building with an AI coding agent? Install the [OpenVidu Agent Plugin](./building-with-ai/agent-plugin.md){ .ov-link }.</p>

<div class="ov-codewin" markdown>

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

</div>
</div>

</section>

<section class="ov-section" markdown>

<h2 class="ov-h2" id="what-is-openvidu-platform">What is OpenVidu Platform?</h2>

<div class="ov-prose" markdown>
OpenVidu is based on WebRTC technology and allows developing any kind of use case you can imagine: one-to-one calls, video conference rooms, massive live-streaming events, management and processing of drones and camera feeds...

OpenVidu gives you **client and server SDKs from our LiveKit fork** for every major language — so you build with familiar, battle-tested APIs — powered at its core by **mediasoup**'s best-in-class media routing. 100% API compatibility, improved performance, and a platform built to be **self-hosted**.
</div>

<div class="ov-figure" data-sal="slide-up" markdown>
![OpenVidu vs LiveKit](../assets/images/platform/home/openvidu-stack-dark.svg#only-dark){ .skip-gallery loading=lazy }
![OpenVidu vs LiveKit](../assets/images/platform/home/openvidu-stack-light.svg#only-light){ .skip-gallery loading=lazy }
/// caption
OpenVidu is a custom fork of LiveKit, 100% compatible in terms of its API and SDKs, with the power of mediasoup at its core. This and other integrations provide improved performance, new features and facilitate the deployment and management of your self-hosted, production-grade cluster.
///
</div>

</section>

<section class="ov-section" markdown>

<h2 class="ov-h2" id="use-cases">Use cases</h2>

<p class="ov-lead">OpenVidu is a super versatile platform that can be used to build just about any kind of real-time application you can think of. Most common use cases can be classified into one of the following categories:</p>

<div class="ov-grid" markdown>

<div class="ov-usecase" data-sal="slide-up" markdown>
<div class="ov-usecase__media" markdown>
![OpenVidu videoconference use case](../assets/images/platform/getting-started/videoconference-light.svg#only-light){ .skip-gallery loading=lazy }
![OpenVidu videoconference use case](../assets/images/platform/getting-started/videoconference-dark.svg#only-dark){ .skip-gallery loading=lazy }
</div>
<div markdown>
### Video conferencing

Video conferencing rooms are virtual spaces where two or more users can send video and audio and interact with each other in real-time. They can scale in size, from a simple 1-to-1 call to a massive video conference with thousands of participants. For example:

- A 1-to-1 **video-call center** to attend your customers face to face.
- An **e-health application** where doctors can treat their patients directly from it, in a private and secure manner using end-to-end encryption.
- A **banking application** where customers may sign a contract, live and recording the call as proof of it.
- A **webinar platform** where speakers can give their talks to large audiences, with the possibility of viewers temporarily turning their cameras to ask questions.

!!! info
    If your use case actually fits into the video conferencing category, [**OpenVidu Meet**](../meet/index.md){.meet-link-color} may be the perfect solution for you. Give it a try! Still not sure? [Compare Meet vs Platform](../openvidu-meet-vs-openvidu-platform.md).
</div>
</div>

<div class="ov-usecase ov-usecase--flip" data-sal="slide-up" markdown>
<div class="ov-usecase__media" markdown>
![OpenVidu livestream use case](../assets/images/platform/getting-started/livestream-light.svg#only-light){ .skip-gallery loading=lazy }
![OpenVidu livestream use case](../assets/images/platform/getting-started/livestream-dark.svg#only-dark){ .skip-gallery loading=lazy }
</div>
<div markdown>
### Live-streaming

Live streaming applications allow one publisher to broadcast video to many viewers. It can be a single video feed, multiple video feeds (webcam and screen share) or there could be even multiple publishers. The general rule is that the ratio of viewers to publishers is very high, in the order of thousands.

Ultra-low latency live-streaming (below 300ms) allows for actual real-time interaction between the viewers and the publishers. This differs from traditional live-streaming platforms where the latency is usually in the order of seconds. In this way you can build applications like:

- A **TEDx-like application**, where a speaker can give a talk to a massive audience of thousands of viewers, who may communicate through a chat. Real time subtitles and translations can be added to the stream.
- An application to **stream sport events**, where viewers can switch between different cameras to watch the game from different angles to increase fan engagement.
- A **global live auction platform** where the auctioneer can be seen by the bidders in real-time with sub-second latency all around the world.
</div>
</div>

<div class="ov-usecase" data-sal="slide-up" markdown>
<div class="ov-usecase__media" markdown>
![OpenVidu AI agents use case](../assets/images/platform/getting-started/ai-agents-light.svg#only-light){ .skip-gallery loading=lazy }
![OpenVidu AI agents use case](../assets/images/platform/getting-started/ai-agents-dark.svg#only-dark){ .skip-gallery loading=lazy }
</div>
<div markdown>
### AI Agents

AI has changed the world, forever. OpenVidu can be used to integrate any kind of AI agent in your application, using real-time audio/video/data tracks as inputs for LLMs or any other kind of AI model. With these capabilities, you can expand your application to new horizons:

- Implement **real-time subtitles, translations, word-detection, sentiment analysis, profanity filter**, etc. in your video conferences.
- Add a **summary generator** to your video conference app, that can extract the most important parts of the conversation to be shared with the participants.
- Build a 1-to-1 **virtual assistant** that can speak naturally with your users, using the latest Text-To-Speech AI models.
- Implement **object detection** in your live-streaming app, to detect and track objects in real-time in the video feed.
</div>
</div>

<div class="ov-usecase ov-usecase--flip" data-sal="slide-up" markdown>
<div class="ov-usecase__media" markdown>
![OpenVidu robotics use case](../assets/images/platform/getting-started/robotics-light.svg#only-light){ .skip-gallery loading=lazy }
![OpenVidu robotics use case](../assets/images/platform/getting-started/robotics-dark.svg#only-dark){ .skip-gallery loading=lazy }
</div>
<div markdown>
### Robotics and embedded systems

The future lies in the integration of cameras and sensors in all kinds of devices, everywhere: industry, homes, public spaces, emergency services... OpenVidu can be used to receive and process video and audio streams from these devices, and doing so in real-time. For example:

- A **security system** to receive the feed of IP cameras and sending an alert when detecting a person.
- A **drone control system** to receive the video feed from each drone camera and securely record it. Any other sensor reading could also be sent to be synchronized later with the recorded video feed.
- A **real-time translation app** that uses the latest AI models to provide high-quality translations of spoken language in real time.
</div>
</div>

</div>

</section>

<section class="ov-section" markdown>

<h2 class="ov-h2" id="openvidu-application-architecture">OpenVidu application architecture</h2>

<p class="ov-lead">Every OpenVidu application consists of 3 main components.</p>

<div class="ov-figure" data-sal="slide-up" markdown>
![OpenVidu app architecture](../assets/images/platform/getting-started/openvidu-app-architecture-light.svg#only-light){ .control-height loading=lazy }
![OpenVidu app architecture](../assets/images/platform/getting-started/openvidu-app-architecture-dark.svg#only-dark){ .control-height loading=lazy }
</div>

<div class="ov-grid ov-grid--3" data-sal="slide-up" markdown>
<div class="ov-card" markdown>
### Your OpenVidu deployment

Provides all the necessary infrastructure for streaming real-time audio and video. It is built upon **LiveKit server** and **mediasoup server**, but it can usually be treated as a black box where its internal aspects are not important: you just deploy it and connect your application to it. It can be a single server or a cluster, deployed on premises or in your cloud provider.
</div>
<div class="ov-card" markdown>
### Your Application client

Runs in your user devices and interacts with the OpenVidu server through any **LiveKit client SDK**. As OpenVidu server is 100% compatible with LiveKit protocol, you can integrate any LiveKit client SDK in your Application client. Your users will join rooms as participants to send and receive real-time audio and video tracks. It needs a token generated by the Application server to join a room.
</div>
<div class="ov-card" markdown>
### Your Application server

Interacts with the OpenVidu deployment through any **LiveKit server SDK**. As OpenVidu server is 100% compatible with LiveKit protocol, you can integrate any LiveKit server SDK in your application server. At a minimum, it is responsible for the generation of tokens for the Application client to join a room. But you can implement your own business logic managing rooms, participants and tracks from the safety of your Application server.
</div>
</div>

</section>

<section class="ov-section" markdown>

<h2 class="ov-h2" id="basic-concepts">Basic concepts</h2>

<p class="ov-lead">With these three concepts you can build any kind of real-time application you can think of.</p>

<div class="ov-grid ov-grid--3" data-sal="slide-up" markdown>
<div class="ov-card" markdown>
### Room

A Room is a virtual space where Participants can connect to send and receive media Tracks. Two Participants can only communicate if they are connected to the same Room.
</div>
<div class="ov-card" markdown>
### Participant

A Participant is a user connected to a specific Room. Each Participant can publish as many video and audio Tracks as needed, and subscribe to any other Participant's Tracks, as long as they are connected to the same Room.
</div>
<div class="ov-card" markdown>
### Track

A Track is a data flow of audio or video. Participants create them from a local media source (a webcam, a microphone, a screen share) and publish them into a Room. Other Participants of the same Room can subscribe to them.
</div>
</div>

<p class="ov-lead ov-lead--after">The figure below shows two simple examples.</p>

<div class="ov-grid ov-grid--2" data-sal="slide-up" markdown>
<div class="ov-figure" markdown>
![Basic concepts](../assets/images/platform/getting-started/basic-concepts-1-light.svg#only-light){ loading=lazy }
![Basic concepts](../assets/images/platform/getting-started/basic-concepts-1-dark.svg#only-dark){ loading=lazy }
/// caption
Room "Daily meeting" has 2 Participants: "Alice" is publishing Track "Webcam" and "Mic" and is receiving Track "Screen" from "Bob". "Bob" is publishing Track "Screen" and receiving Tracks "Webcam" and "Mic" from "Alice".
///
</div>
<div class="ov-figure" markdown>
![Basic concepts](../assets/images/platform/getting-started/basic-concepts-2-light.svg#only-light){ loading=lazy }
![Basic concepts](../assets/images/platform/getting-started/basic-concepts-2-dark.svg#only-dark){ loading=lazy }
/// caption
Room "Remote support" has 3 Participants: Participant "Dan" is not publishing any Track, but receiving all Tracks in the Room. Participant "Erin" is only receiving Track "Mic" from Participant "Carol", but not Track "Screen".
///
</div>
</div>

### Other concepts { .ov-h3 }

<p class="ov-lead" markdown="span">Apart from these basic building blocks, there are other concepts that will be typically used in your OpenVidu application. All of them are just special types of [Participants](#participant) that connect to Rooms to perform specific tasks:</p>

<div class="ov-grid ov-grid--3" data-sal="slide-up" markdown>
<div class="ov-card" markdown>
### Egress

A process that exports media out of a Room. It is a special type of Participant that only subscribes to Tracks. It allows recording tracks to a file or streaming them to an external destination (via HLS or RTMP).
</div>
<div class="ov-card" markdown>
### Ingress

A process that imports media into a Room. It is a special type of Participant that only publishes Tracks. It allows bringing external media sources into a Room, such as an MP4 file, an IP camera or a RTMP stream.
</div>
<div class="ov-card" markdown>
### Agents

A process that performs AI-driven operations to the media of a Room. It is a special type of Participant that can both subscribe and publish Tracks, analyzing and/or modifying them in between. It allows implementing any AI task you can imagine: real-time subtitles, translations, object detection, AI voice bots, etc.
</div>
</div>

</section>

<section class="ov-section" markdown>

<h2 class="ov-h2" id="openvidu-editions">OpenVidu Editions</h2>

<p class="ov-lead">OpenVidu is available in two editions. You can start with OpenVidu Community and upgrade to OpenVidu Pro when needed.</p>

<div class="ov-grid ov-grid--2" data-sal="slide-up" markdown>
<div class="ov-card" markdown>
<span class="ov-tag ov-tag--community">COMMUNITY</span>

### [OpenVidu COMMUNITY](../pricing.md#openvidu-community)

Free to use. It is a single-server deployment and provides a custom LiveKit distribution with Egress, Ingress, S3 storage and monitoring. Ideal for development and testing, but also for medium-scale production deployments. You can host hundreds of simultaneous participants in your rooms by running OpenVidu Community in a sufficiently powerful server!
</div>
<div class="ov-card" markdown>
<span class="ov-tag ov-tag--pro">PRO</span>

### [OpenVidu PRO](../pricing.md#openvidu-pro)

OpenVidu commercial edition. It is a multi-server deployment with all the features of OpenVidu Community plus 2x performance, scalability, fault tolerance and improved monitoring and observability. Ideal for large-scale production deployments with heavy traffic that require the highest standards.
</div>
</div>

<div class="ov-figure ov-figure--table" data-sal="slide-up" markdown>

| Type of deployment        | **OpenVidu**<br>**Local (development)**{ .nowrap }         | **OpenVidu**<br>**Single Node**{ .nowrap } | **OpenVidu**<br>**Elastic**{ .nowrap } | **OpenVidu**<br>**High Availability**{ .nowrap } |
| ------------------------- | ------------------------------------ | -------------------- | ---------------- | -------------------------- |
| **OpenVidu Edition**          | **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } **PRO**{ .openvidu-tag .openvidu-pro-tag } | **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } **PRO**{ .openvidu-tag .openvidu-pro-tag } | **PRO**{ .openvidu-tag .openvidu-pro-tag } | **PRO**{ .openvidu-tag .openvidu-pro-tag } |
| **Suitability**               | For local development in your laptop | For applications with medium user load | For applications with dynamic user load that require scalability | For applications where both scalability and fault tolerance are critical |
| **Features**                  | Friendly Docker Compose setup with Redis, Egress, Ingress, S3 storage and observability. With automatic certificate management to test across devices in your network | **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } Custom LiveKit distribution with Redis, Egress, Ingress, S3 storage and observability.<br><br>**PRO**{ .openvidu-tag .openvidu-pro-tag } Same features but adding **2x performance** and **advanced observability**. | Same benefits as OpenVidu Single Node plus **2x performance**, **advanced observability** and **scalability** | Same benefits as OpenVidu Elastic plus **fault tolerance** |
| **Number of servers**         | Your laptop | 1 Node | 1 Master Node +<br><span class="nowrap">N Media Nodes</span> | 4 Master Nodes +<br><span class="nowrap">N Media Nodes</span> |
| **Installation instructions** | [Install](./self-hosting/local.md){ .md-button } | [Install](./self-hosting/single-node/index.md){ .md-button } | [Install](./self-hosting/elastic/index.md){ .md-button } | [Install](./self-hosting/ha/index.md){ .md-button } |

</div>

</section>

<section class="ov-section ov-closing" data-sal="slide-up" markdown>
<div class="ov-closing__panel" markdown>
<h2 class="ov-closing__title">Build your first app.</h2>
<div class="ov-closing__actions" markdown>
[Tutorials in 8 languages](./tutorials/application-server/index.md){ .ov-btn .ov-btn--lg .ov-btn--platform title="Build your first app with the OpenVidu Platform tutorials" }
[Run OpenVidu locally](./self-hosting/local.md){ .ov-btn .ov-btn--lg .ov-btn--outline }
</div>
[Or talk to an expert](../support/index.md){ .ov-closing__link }
</div>

<p class="ov-compare" markdown="span">Need a ready-made video calling app instead? Check out [OpenVidu Meet](../meet/index.md). Not sure which one fits? [Compare Meet vs Platform](../openvidu-meet-vs-openvidu-platform.md).</p>

</section>

</div>
