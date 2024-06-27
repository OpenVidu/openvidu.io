---
draft: true
date: 2024-06-20
categories:
  - Release
authors:
  - pabloFuente
hide:
  - navigation
  - toc
---

# OpenVidu 3.0.0 (BETA)

We are proud and excited to introduce the beta version of OpenVidu 3.0.0. This is a major milestone for the project and represents many months of hard work by the entire OpenVidu team. It involves a complete overhaul of OpenVidu's internal technologies, architecture and deployment. All in order to offer the best real-time media solution out there.

Let's take a quick look at everything you need to know about OpenVidu 3.0.0.

<!-- more -->

## What are the reasons for this major release?

At OpenVidu we are always striving to offer the latest technology available to deliver the best results in your real-time applications. We developed [Kurento](https://kurento.openvidu.io/){:target=_blank} more than a decade ago as a powerful SFU, and built OpenVidu on top of it to provide an easy-to-use framework to develop videoconferencing applications. As [Kurento](https://kurento.openvidu.io/){:target=_blank} grew older and some limitations became apparent (mainly related to performance), we decided to evolve OpenVidu to support [mediasoup](https://mediasoup.org/){:target=_blank} instead of Kurento as its internal media server.

And now it is time to take the next big step: we are now integrating [**LiveKit**](https://livekit.io/){:target=_blank} into our stack. LiveKit is a cutting-edge WebRTC stack that is open source and certainly the most popular choice in the community in recent times.

## What has changed?

Being now based on LiveKit's fantastic stack, OpenVidu 3.0.0 incorporates the latest innovations and optimizations in real-time media. Here are some of the most important low-level features that will improve your application performance:

- [Simulcast](https://docs.livekit.io/realtime/client/publish/#Video-simulcast){target="_blank"} for VP8 and H264 video codecs.
- [Scalable Video Coding (SVC)](https://docs.livekit.io/guides/video-codecs/#Supported-codecs){target="_blank"} for VP9 and AV1 video codecs.
- [Dynamic Broadcasting (Dynacast)](https://docs.livekit.io/realtime/client/publish/#Dynamic-broadcasting){target="_blank"} for minimizing bandwidth consumption. It pauses the publication of any video layer that is not being consumed by any subscriber.
- [Adaptive Stream](https://docs.livekit.io/realtime/client/receive/#Adaptive-stream){target="_blank"} for UI-based video quality optimization. It sends to each user the minimum bits needed to display high-quality rendering based on the size of the video player. If a video player is hidden, the video stream is paused. This allows you to scale your application to large video rooms with thousands of users.
- [Audio RED (REDundant Encoding)](https://docs.livekit.io/guides/audio-red){target="_blank"} and [Hi-fi audio](https://docs.livekit.io/guides/hi-fi-audio/){target="_blank"} for crisp, clear, high-quality audio streams.
- [Audio DTX (Discontinuous Transmission)](https://bloggeek.me/webrtcglossary/dtx/){target="_blank"} for detecting silence in audio tracks and reducing their bandwidth.
- [End-To-End Encryption (E2EE)](https://en.wikipedia.org/wiki/End-to-end_encryption){target="_blank"} for the ultimate secure communication.
- [WHIP](https://millicast.medium.com/whip-the-magic-bullet-for-webrtc-media-ingest-57c2b98fb285){target="_blank"} for low-latency media ingestion.

These and many other features will make your real-time application more efficient, performant, reliable, secure and future-proof.

## Updating from OpenVidu 2 to OpenVidu 3

Although this is a major release that involves a complete overhaul of OpenVidu's internal technologies, all OpenVidu 2 Pro/Enterprise users will have available a compatibility module that hopefully will make the transition as seamless as possible, minimizing code changes.

These are the general steps to migrate an application from OpenVidu 2 to OpenVidu 3:

1. Update your application.
2. Deploy OpenVidu 3.
3. Point your server application to your new OpenVidu 3 deployment.

### 1. Update your application

#### For applications using _openvidu-browser.js_ library

This includes any client application built with **JavaScript**, **Angular**, **Vue**, **React**, **React Native**, **Ionic** and **Electron**. Just update:

- Dependency `openvidu-browser` to version 3.0.0 in your package.json.
- Dependency `openvidu-angular` to version 3.0.0 in your package.json, if you use [OpenVidu Components](https://docs.openvidu.io/en/latest/components/){target="_blank"}.
- Dependency `openvidu-react-native-adapter` to version 3.0.0 in your package.json, if you use [React Native](https://docs.openvidu.io/en/latest/tutorials/openvidu-react-native/){target="_blank"}.
- File `openvidu-browser.js` to `openvidu-browser-3.0.0.js` if you are using a [local copy of the library](https://github.com/OpenVidu/openvidu/releases){target="_blank"}.

#### For applications built for native Android or iOS

As OpenVidu 2 did not provide native SDKs for Android or iOS, it is necessary to adapt the application to use the official LiveKit SDKs. We know this may sound like a daunting task, but it is not that hard and we've created this guide to help you through the process:

- [Migrating a native Android app from OpenVidu 2 to OpenVidu 3]()
- [Migrating a native iOS app from OpenVidu 2 to OpenVidu 3]()

### 2. Deploy OpenVidu 3

An OpenVidu 2 deployment is *NOT* directly upgradable to an OpenVidu 3 deployment. You will have to deploy OpenVidu 3 completely from scratch. Just follow the [official instructions](https://openvidu.io/docs/self-hosting/).

### 3. Point your server application to your new OpenVidu 3 deployment

Make sure that your server application is configured to connect to your new OpenVidu 3 deployment.

## Breaking changes

.....

## Roadmap for the future

The OpenVidu team will spend the near future helping with the migration of users coming from OpenVidu 2 (you can write us at [commercial@openvidu.io](mailto:commercial@openvidu.io){target="_blank"} if you need custom support).

As mid-term goals, will be working in supporting a mesh distribution in the media servers, which will allow for massive Rooms in your own infrastructure.
