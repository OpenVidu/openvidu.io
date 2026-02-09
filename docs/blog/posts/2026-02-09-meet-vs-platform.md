---
draft: true
date: 2026-02-09
categories:
  - Features Meet Platform
authors:
  - patxi
hide:
  - navigation
  - search-bar
  - version-selector
---

# Levels of Abstraction in Real-Time Video: Choosing the Right Self-Hosted Solution in 2026

## Why Abstraction Matters

People are diverse, and that’s what makes life interesting. However, in the world of real-time communications (RTC), this diversity means that different users require entirely different levels of abstraction to get the job done.

### The High-Level Consumer (Plug-and-Play)

Think of your kid’s teacher. They need a videoconferencing system that simply works out of the box. For them, success is a stable connection where media handling, signaling, and device management happen invisibly in the background. At this level, abstraction is at its highest: the complexity is hidden behind a 'Join Meeting' button.
 
### The Specialized Producer (Advanced Control)

On the other hand, a broadcaster or a live-event producer operates at a much deeper level. They don't just need a stream; they need a media engine. Their workflow requires:

* Compositing: Merging multiple camera feeds into a single view.
* Computer Vision: Identifying players on a field in real-time.
* Overlays: Dynamically injecting data, graphics, or text onto the video frames.

## Finding the Sweet Spot: Meet vs. Platform

Choosing the right level of abstraction is a delicate balancing act. If the abstraction is too high, you lose the granular control essential for innovation. If it’s too low, you risk spending months reinventing the wheel—building infrastructure instead of delivering value.

To solve this dilemma, we’ve evolved. We are splitting the ecosystem into two distinct products, both maintaining the production-ready quality and reliability our community expects from OpenVidu:

### OpenVidu Meet: The Power of Integration

**OpenVidu Meet** is a production-ready, self-hosted videoconferencing application designed for **rapid deployment**. It is the ideal choice when you need a robust, feature-rich meeting experience that can be seamlessly embedded into your existing telehealth, e-learning, or CRM platform.

While it works out of the box, it remains highly flexible on the outside, allowing for deep UI customization and branding. Its core features include:

* **Collaboration Tools**: Screen sharing, chat, and recording.
* **Privacy & Tech**: Virtual backgrounds and End-to-End Encryption (E2EE).
* **Identity**: Full UI white-labeling and branding.

### OpenVidu Platform: The Developer’s Canvas

**OpenVidu Platform** is a powerful, self-hosted infrastructure that provides the **APIs and SDKs** necessary to build specialized real-time video experiences. It is designed for developers who need total sovereignty over the media flow.

Rather than being limited by "rooms," the Platform gives you the building blocks to manipulate media at its core. It offers:

* **Granular Control**: Low-level WebRTC SDKs for any language and full management of audio/video/data tracks.
* **Advanced Routing**: Total control over media ingestion and telephony (PSTN/SIP) integration.
* **AI-Ready**: Direct hooks for real-time AI processing and media analysis.

**The Key Difference**: > **OpenVidu Meet** is built around the concepts of **Rooms & Meetings**, whereas **OpenVidu Platform** is built around the fundamental concepts of **Audio & Video Tracks**.

## Conclusion: Strategy over Complexity

The choice between a high-level application and a low-level infrastructure depends entirely on where you want to focus your engineering efforts.

* **Choose OpenVidu Meet** if your goal is to provide a world-class communication experience today, without the overhead of managing complex media pipelines. It allows you to focus on your business logic while we handle the meeting dynamics.

* **Choose OpenVidu Platform** if you are pushing the boundaries of what’s possible with media—whether that’s building the next big broadcasting tool, integrating complex AI workflows, or requiring surgical control over every single data track.

At the end of the day, abstraction is about **freedom**: the freedom to choose how much of the 'under-the-hood' complexity you want to own, and how much you want to delegate to a reliable partner.

The best way to understand these levels of abstraction is to see them in action. Whether you are ready to embed a full-featured meeting room or you want to start routing raw media tracks, our documentation has everything you need to get started.

👉 Explore the [OpenVidu Documentation](https://openvidu.io/)


**Versión antigua:**

# Choosing the correct abstraction for managing your real-time video in 2026

## User context (abstraction levels in real-time communications)

People are very different from each other. And that makes life pretty much interesting. However, this means as well that different people do have different needs from the point of view of real-time communications.


Your kid's teacher at school, for instance, may need a videoconference system that works out of the box, without worrying much about how media is handled and devices are connected to their respective streaming channels.


A broadcaster, may need a media system that is able to compose different videos from different cameras, recognize objects in the images (like players in a play field), or over impress images and text on the video. 

## Different users, different solutions

That's why we decided to split OpenVidu into two different products: OpenVidu Meet and OpenVidu Platform. Both with the quality and production readiness you are looking for, and our users are acustomed to in OpenVidu.

**OpenVidu Meet** is a production-ready, self-hosted videoconferencing application that can be **easily embedded** to bring video calls to your telehealth, e-learning, team collaboration, customer support, or any other application in need of videoconferencing. It is fully customizable on the outside (i.e., the UI), and it provides features such as:

* Screen sharing
* Recording
* Chat
* Virtual backgrounds
* End-to-end encryption
* UI customization
* Branding

**OpenVidu Platform** is a production-ready and self-hosted solution which provides a set of **APIs and SDKs** that simplifies building real-time video applications. It brings developers total flexibility and control to build custom applications that requires managing real-time media. It provides:

* Low-level WebRTC SDKs for any language
* Full control over audio/video/data streaming
* Full control over media ingestion
* Telephony integration
* AI integrations

OpenVidu Meet application is built around the concepts of rooms & meetings, while OpenVidu Platform is built around the concepts of audio & video tracks.

## Conclusions