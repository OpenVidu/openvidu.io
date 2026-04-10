---
draft: true
date: 2026-02-09
cover_image: 2026-02-09-meet-vs-platform-3.png
categories:
  - OpenVidu Meet features
  - OpenVidu Platform features
authors:
  - patxi
hide:
  - navigation
  - search-bar
  - version-selector
---

# Choosing the right level of abstraction in self-hosted WebRTC solutions in 2026: OpenVidu Meet vs OpenVidu Platform

![OpenVidu Meet vs OpenVidu Platform](/assets/images/blog/meet-vs-platform/meet-vs-platform2.png)

In this blog post we explore how different levels of abstraction are needed in the WebRTC arena, and which choices do you have when using the OpenVidu WebRTC ecosystem. 

## Why Abstraction Matters

People are diverse, and that’s what makes life interesting. In the world of real-time communications (RTC), diversity means that different users require entirely different levels of abstraction to get the job done, from a "batteries included" scalable meeting application, to an extremely customizable media processing pipeline with access to low-level media SDKs and APIs. 

<!-- more -->

### The High-Level Consumer (Plug-and-Play)

Think of your kid’s teachers, for instance. They need a videoconferencing system that simply works out of the box. For them, success is a stable connection where media handling, signaling, and device management happen invisibly in the background. At this level, abstraction is at its highest: the complexity is hidden behind a 'Join Meeting' button.
 
### The Specialized Producer (Advanced Control)

On the other hand, a broadcaster or a live-event producer operates at a much deeper level. They don't just need a stream; they need a media engine. Their workflow requires:

* Compositing: Merging multiple camera feeds into a single view.
* Computer Vision: Identifying players on a field in real-time.
* Overlays: Dynamically injecting data, graphics, or text onto the video frames.

## Finding the Sweet Spot: Meet vs. Platform

Choosing the right level of abstraction is a delicate balancing act. If the abstraction is too high, you lose the granular control essential for innovation, but you make your life easier by hiding the complexity of the system. If it’s too low, you risk spending months reinventing the wheel—building infrastructure instead of delivering value, but you are in full control of what happens under-the-hood. 

At OpenVidu, we are aware of this dilemma, and we’ve evolved. We are splitting the ecosystem into two distinct products, OpenVidu Meet and OpenVidu Platform, both maintaining the production-ready quality and reliability our community expects from OpenVidu.

### OpenVidu Meet: The Power of Integration

**OpenVidu Meet** is a production-ready, self-hosted videoconferencing application designed for **rapid deployment**. It is the ideal choice when you need a robust, feature-rich meeting experience that can be seamlessly embedded into your existing telehealth, e-learning, or CRM platform.

While it works out of the box, it remains highly flexible on the outside, allowing for deep UI customization and branding. Its core features include:

* **Collaboration Tools**: Screen sharing, chat, and recording.
* **Privacy & Tech**: Virtual backgrounds and End-to-End Encryption (E2EE).
* **Identity**: Full UI white-labeling and branding.

![OpenVidu Meet screenshot](/assets/images/blog/meet-vs-platform/webcomponent-meeting.png)

### OpenVidu Platform: The Developer’s Canvas

**OpenVidu Platform** is a production-ready, powerful, and self-hosted infrastructure that provides the **APIs and SDKs** necessary to build specialized real-time video experiences. It is designed for developers who need total sovereignty over the media flow.

Rather than being limited by "rooms", the Platform gives you the building blocks to manipulate media at its core. It offers:

* **Granular Control**: Low-level WebRTC SDKs for any language providing developers full management of audio/video/data tracks.
* **Advanced Routing**: Total control over media ingestion and telephony (PSTN/SIP) integration.
* **AI-Ready**: Direct hooks for real-time AI processing and media analysis.

![OpenVidu Platform screenshot](/assets/images/blog/meet-vs-platform/ov-platform.png)

**The Key Difference** > **OpenVidu Meet** is built around the concepts of **Rooms & Meetings**, whereas **OpenVidu Platform** is built around the fundamental concepts of **Audio & Video Tracks**.

## Conclusion: Strategy over Complexity

The choice between a high-level application and a low-level infrastructure depends entirely on where you want to focus your engineering efforts.

* **Choose OpenVidu Meet** if your goal is to provide a world-class communication experience today, without the overhead of managing complex media pipelines. It allows you to focus on your business logic while we handle the meeting dynamics.

* **Choose OpenVidu Platform** if you are pushing the boundaries of what’s possible with media and you require total control over every single media track.

At the end of the day, abstraction is about **freedom**: the freedom to choose how much of the 'under-the-hood' complexity you want to own, and how much you want to delegate to a reliable partner.

The best way to understand these levels of abstraction is to see them in action. Whether you are ready to embed a full-featured meeting room or you want to start routing raw media tracks, our documentation has everything you need to get started.

👉 Explore the [OpenVidu Documentation](https://openvidu.io/)
