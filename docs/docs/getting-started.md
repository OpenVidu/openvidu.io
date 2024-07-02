## What is OpenVidu?

OpenVidu is a platform that allows you to implement real-time applications. You can build your brand new OpenVidu app from scratch, but it is also very easy to integrate OpenVidu in your already existing application.

OpenVidu is based on WebRTC technology and allows developing any kind of use case you can imagine: one-to-one calls, video conference rooms, massive live streaming events, management and processing of drones and camera feeds...

OpenVidu is built on the best open source technologies: [LiveKit](https://livekit.io){target="\_blank"}, from which it inherits all its amazing SDKs to integrate it into your front-end and back-end applications, and [mediasoup](https://mediasoup.org){target="\_blank"}, from which it inherits the best performance and optimization for media routing.


<figure markdown>
  ![OpenVidu vs LiveKit](../assets/images/openvidu-stack-dark.svg#only-dark){ .mkdocs-img .do-not-include-in-gallery }
  ![OpenVidu vs LiveKit](../assets/images/openvidu-stack-light.svg#only-light){ .mkdocs-img .do-not-include-in-gallery }
  <figcaption style="max-width: 27rem">OpenVidu is a custom fork of LiveKit, 100% compatible in terms of its API and SDKs, with the power of mediasoup at its core. This and other integrations provide improved performance, new features and facilitate the deployment and management of your self-hosted, production-grade cluster.</figcaption>
</figure>

## Use cases

OpenVidu is a super versatile platform that can be used to build just about any kind of real-time application you can think of. Most common use cases can be classified into one of the following categories:

### Video conferencing

<div style="display: flex; align-items: center; flex-flow: row wrap; justify-content: center;" markdown>

<div class="grid-35 tablet-grid-35">
<img class="do-not-include-in-gallery use-case-img" alt="OpenVidu videoconference use case" src="../../assets/images/getting-started/videoconference.svg" />
</div>

<div class="grid-65 tablet-grid-65" markdown>
Video conferencing rooms are virtual spaces where two or more users can send video and audio and interact with each other in real-time. They can scale in size, from a simple 1-to-1 call to a massive video conference with thousands of participants. For example:

- A 1-to-1 **video-call center** to attend your customers face to face.
- An **e-health application** where doctors can treat their patients directly from it, in a private and secure manner using end-to-end encryption.
- A **banking application** where customers may sign a contract, live and recording the call as proof of it.
- A **webinar platform** where speakers can give their talks to large audiences, with the possibility of viewers temporarily turning their cameras to ask questions.
</div>

</div>

### Live streaming

<div style="display: flex; align-items: center; flex-flow: row wrap; justify-content: center;" markdown>

<div class="grid-65 tablet-grid-65" markdown>
Live streaming applications allow one publisher to broadcast video to many viewers. It can be a single video feed, multiple video feeds (webcam and screen share) or there could be even multiple publishers. The general rule is that the ratio of viewers to publishers is very high, in the order of thousands.

Ultra-low latency live streaming (below 300ms) allows for actual real-time interaction between the viewers and the publishers. This differs from traditional live streaming platforms where the latency is usually in the order of seconds. In this way you can build applications like:

- A **TEDx-like application**, where a speaker can give a talk to a massive audience of thousands of viewers, which may communicate through a chat. Real time subtitles and translations can be added to the stream.
- An application to **stream sport events**, where viewers can switch between different cameras to watch the game from different angles to increase fan engagement.
- A **global live auction platform** where the auctioneer can be seen by the bidders in real-time with sub-second latency all around the world.
</div>

<div class="grid-35 tablet-grid-35">
<img class="do-not-include-in-gallery use-case-img" alt="OpenVidu livestream use case" src="../../assets/images/getting-started/livestream.svg" />
</div>

</div>

### Robotics and embedded systems

<div style="display: flex; align-items: center; flex-flow: row wrap; justify-content: center;" markdown>

<div class="grid-40 tablet-grid-40">
<img class="do-not-include-in-gallery use-case-img" alt="OpenVidu robotics use case" src="../../assets/images/getting-started/robotics.svg" />
</div>

<div class="grid-60 tablet-grid-60" markdown>
The future lies in the integration of cameras and sensors in all kinds of devices, everywhere: industry, homes, public spaces, emergency services... OpenVidu can be used to receive and process video and audio streams from these devices, and doing so in real-time. For example:

- A **security system** to receive the feed of IP cameras and sending an alert when detecting a person.
- A **drone control system** to receive the video feed from each drone camera and securely record it. Any other sensor reading could also be sent to be synchronized later with the recorded video feed.
- A **real-time translation app** that uses the latest AI models to provide high-quality translations of spoken language in real time.
</div>

</div>

## OpenVidu application architecture

<figure markdown>
  ![OpenVidu app architecture](../assets/images/getting-started/openvidu-app-achitecture.drawio.svg)
</figure>

Any OpenVidu application has 3 different parts:

- **Your OpenVidu deployment**: provides all the necessary infrastructure for streaming real-time audio and video. It is built upon **LiveKit server** and **mediasoup server**. It can usually be treated as a black box in which its internal aspects are not important: you just deploy it and connect your application to it. It can be a single server or a cluster, deployed on premises or in your cloud provider.
- **Your Application client**: runs in your user devices and interacts with the OpenVidu server through any **LiveKit client SDK**. As OpenVidu server is 100% compatible with LiveKit protocol, you can integrate any LiveKit client SDK in your Application client. Your users will join rooms as participants to send and receive real-time audio and video tracks. It needs a token generated by the Application server to join a room.
- **Your Application server**: interacts with the OpenVidu deployment through any **LiveKit server SDK**. As OpenVidu server is 100% compatible with LiveKit protocol, you can integrate any LiveKit server SDK in your application server. At a minimum, it is responsible for the generation of tokens for the Application client to join a room. But you can implement your own business logic managing rooms, participants and tracks from the safety of your Application server.

## Basic concepts

### Room

A Room is a virtual space where Participants can connect to send and receive media Tracks. Two Participants can only communicate if they are connected to the same Room.

### Participant

A Participant is a user connected to a specific Room. Each Participant can publish as many video and audio Tracks as needed, and subscribe to any other Participant's Tracks, as long as they are connected to the same Room.

### Track

A Track is a data flow of audio or video. Participants create them from a local media source (a webcam, a microphone, a screen share) and publish them into a Room. Other Participants of the same Room can subscribe to them.

With these three concepts you can build any kind of real-time application you can think of. The figure below shows two simple examples.

<div style="display: flex; align-items: start; justify-content: center;" markdown>

<div class="grid-45 tablet-grid-45" markdown>
<figure markdown>
  ![Basic concepts](../assets/images/getting-started/basic-concepts-1.svg){.basic-concepts-img-1}
  <figcaption style="margin-top: 3em">Room "Daily meeting" has 2 Participants: "Alice" is publishing Track "Webcam" and "Mic" and is receiving Track "Screen" from "Bob". "Bob" is publishing Track "Screen" and receiving Tracks "Webcam" and "Mic" from "Alice".</figcaption>
</figure>
</div>

<div class="grid-55 tablet-grid-55" markdown>
<figure markdown>
  ![Basic concepts](../assets/images/getting-started/basic-concepts-2.svg){.basic-concepts-img-2}
   <figcaption>Room "Remote support" has 3 Participants: Participant "Dan" is not publishing any Track, but receiving all Tracks in the Room. Participant "Erin" is only receiving Track "Mic" from Participant "Carol", but not Track "Screen".</figcaption>
</figure>
</div>

</div>

## OpenVidu Editions

OpenVidu is available in two editions:

- **OpenVidu** <a href="/pricing#openvidu-community"><span class="openvidu-tag openvidu-community-tag">COMMUNITY</span></a>: free to use. It is a single-server deployment and provides a custom LiveKit distribution with Egress, Ingress, S3 storage and monitoring. Ideal for development and testing, but also for medium-scale production deployments. You can host hundreds of simultaneous participants in your rooms by running OpenVidu Community in a sufficiently powerful server!
- **OpenVidu** <a href="/pricing#openvidu-pro"><span class="openvidu-tag openvidu-pro-tag">PRO</span></a>: OpenVidu commercial edition. It is a multi-server deployment with all the features of OpenVidu Community plus 2x performance, scalability, fault tolerance and improved monitoring and observability. Ideal for large-scale production deployments with heavy traffic that require the highest standards. You can start with OpenVidu Community and upgrade to OpenVidu Pro when needed.

<br>

| Type of deployment        | <a href="/docs/self-hosting/deployment-types/#openvidu-local-development"><strong>OpenVidu<br><span class="no-break">Local (development)</span></strong>         | <a href="/docs/self-hosting/deployment-types/#openvidu-single-node"><strong>OpenVidu<br><span class="no-break">Single Node</span></strong></a> | <a href="/docs/self-hosting/deployment-types/#openvidu-elastic"><strong>OpenVidu<br><span class="no-break">Elastic</span></strong></a> | <a href="/docs/self-hosting/deployment-types/#openvidu-high-availability"><strong>OpenVidu<br><span class="no-break">High Availability</span></strong></a> |
| ------------------------- | ------------------------------------ | -------------------- | ---------------- | -------------------------- |
| **OpenVidu Edition**          | <span class="openvidu-tag openvidu-community-tag">COMMUNITY</span> <span class="openvidu-tag openvidu-pro-tag">PRO</span> | <span class="openvidu-tag openvidu-community-tag">COMMUNITY</span> | <span class="openvidu-tag openvidu-pro-tag">PRO</span> | <span class="openvidu-tag openvidu-pro-tag">PRO</span> |
| **Suitability**               | For local development in your laptop | For applications with medium user load | For applications with dynamic user load that require scalability | For applications where both scalability and fault tolerance are critical |
| **Features**                  | Friendly Docker Compose setup with Redis, Egress, Ingress, S3 storage and observability. With automatic certificate management to test across devices in your network | Custom LiveKit distribution with Redis, Egress, Ingress, S3 storage and observability | Same benefits as OpenVidu Single Node plus **2x performance**, **scalability** and **advanced observability** | Same benefits as OpenVidu Single Node and OpenVidu Elastic plus **fault tolerance** |
| **Number of servers**         | Your laptop | 1 Node | 1 Master Node +<br><span class="no-break">N Media Nodes</span> | 4 Master Nodes +<br><span class="no-break">N Media Nodes</span> |
| **Installation instructions** | [Install](./self-hosting/local.md){ .md-button } | [Install](./self-hosting/single-node/index.md){ .md-button } | [Install](./self-hosting/elastic/index.md){ .md-button } | [Install](./self-hosting/ha/index.md){ .md-button } |
