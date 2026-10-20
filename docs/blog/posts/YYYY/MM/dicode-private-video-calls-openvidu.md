---
title: How Dicode built private video calls on OpenVidu
draft: false
date:
  created: 2026-10-20
slug: dicode-private-video-calls-openvidu
description: How Finnish software house Dicode built private, embeddable video calls for non-profit organizations on OpenVidu, with data kept under its own control.
cover_image: poster-light.webp
categories:
  - Success story
  - Vertical
tags:
  - WebRTC
  - Self-hosted
  - Privacy
  - GDPR
  - Embedded video
  - Non-profit
  - Migration
authors:
  - patxi
---

# How Dicode built private video calls on OpenVidu

![Dicode and OpenVidu customer success story](/assets/images/blog/YYYY/MM/dicode-private-video-calls-openvidu/poster-light.webp#only-light "Dicode + OpenVidu"){ .round-corners }
![Dicode and OpenVidu customer success story](/assets/images/blog/YYYY/MM/dicode-private-video-calls-openvidu/poster-dark.webp#only-dark "Dicode + OpenVidu"){ .round-corners }

What do you build when your clients hold confidential conversations, and "just use Teams" isn't an answer you can give them? That's the question [Dicode :fontawesome-solid-external-link:{.external-link-icon}](https://dicode.fi/){:target="_blank"}, a software company from Tampere, Finland, faced when it set out to give non-profit organizations video calls that are easy to join and keep their data private.

We talked to the team at Dicode, led by CEO **Janne Sikiö**, about the product they built on OpenVidu: why privacy and EU data residency drove the choice, how they handle large audiences, what the move from OpenVidu 2 to OpenVidu 3 took, and where they want to go next with recordings and AI.

<!-- more -->

## What is Dicode?

Dicode has been building custom software for its clients since 2002, from resource management and inventory systems to product configurators and health surveys. Video calls are part of that work too, and they live in two places at once:

> "We currently use OpenVidu both for our clients and internally. For our clients, we have developed a product that we customize to meet each client's specific needs. Internally, we use a version built on the same foundation, with some modifications to suit our own requirements."

The client side of that product has a clear audience:

> "At present, our OpenVidu-based solution is used by clients operating in the non-profit sector."

Two of those clients are the [Finnish Rheumatism Association (Suomen Reumaliitto) :fontawesome-solid-external-link:{.external-link-icon}](https://reumaliitto.fi/en/about-us/){:target="_blank"} and the [Organisation for Respiratory Health in Finland (Hengitysliitto) :fontawesome-solid-external-link:{.external-link-icon}](https://www.hengitysliitto.fi/en/){:target="_blank"}. Both are patient and health organizations, and that context explains a lot about the decisions that follow.

## Auditorium rooms for large groups

We asked who joins these calls and how many people Dicode handles at peak. The team kept the numbers private, for a good reason:

> "We prefer not to share precise figures, as we want to protect our clients' confidential information."

What they did share is one of the most interesting features they built on top of OpenVidu:

> "However, we have developed functionality that allows clients to set up auditorium rooms for large groups. These rooms can accommodate many listeners, while only a limited number of participants have permission to share video and audio. The remaining participants can listen in."

This is a pattern every organization running member events, lectures or peer-support sessions eventually needs. A handful of speakers publish audio and video, and everyone else subscribes. Because OpenVidu lets you decide per participant who may publish and who may only listen, an auditorium is a matter of handing out the right permissions rather than running a separate webinar tool. If you're designing something similar, our post on [access models for video conferencing apps](/blog/posts/2026/07/video-conferencing-permissions.md) walks through the options.

## Why not Teams?

Many of Dicode's clients already had a videoconferencing tool on every desk. It wasn't enough:

> "Many of our clients use Teams, but we ruled it out as a technical platform for our own solution. We evaluated several alternatives, and OpenVidu's APIs seemed to offer the best fit for our customization requirements."

That's the build-vs-buy question in its usual form. A meeting app you can't change is fine for internal calls. It stops working when the video call has to live inside your own product, with your own user experience, tailored to each client.

## Privacy first: why Dicode chose OpenVidu

When we asked what drove the decision, privacy came first:

> "Privacy was one of our most important selection criteria. We wanted a solution that could be run on our own servers if needed, ensuring that data would not be exposed to external parties. GDPR compliance and the requirement to keep data traffic within the EU also influenced our decision."

This is where self-hosting earns its place. When you run the media server yourself, you decide which country and which data center the audio and video go through. No third party sits in the middle of the call. For organizations handling health-related conversations, that's often the deciding factor rather than a nice extra. OpenVidu supports a range of [deployment types](/docs/self-hosting/deployment-types.md), from a single server to a multi-node cluster in your cloud of choice or on premises.

## Integration, and the move from 2.x to 3.x

We asked how the integration went and what was hardest. The team was candid:

> "The initial setup and integration went relatively smoothly. We encountered more challenges when migrating from version 2.x to version 3.x.
>
> We have also faced some challenges when adapting existing functionality to work in our own way. In some cases, this has required us to reimplement quite a few things to achieve the desired changes. However, we have not encountered any major technical issues."

On deployment and versions:

> "We maintain our own version for development, but our current client-facing solution is cloud-based to support scalability.
>
> As mentioned earlier, migrating from version 2.x to version 3.x required some effort. We are currently using version 3.7.0."

That's honest feedback, and we appreciate it. OpenVidu 3 is a deep change from OpenVidu 2, so a migration takes real work. We keep investing in making it easier: OpenVidu 3.9 alone brought a batch of fixes to the OpenVidu 2 compatibility module, covering recordings, broadcasts and IP cameras. The [release notes](/docs/releases.md) list what changed in each version.

## What matters most: embedding, data control and scale

We asked which OpenVidu capabilities matter most to Dicode's use case:

> "The most important features are the ability to embed video calls directly into our own user interface and to retain control over our data. Scalability is also a major advantage."

And on which edition they run:

> "We use the PRO edition because, at the time we made our decision, it offered automatic scaling."

That combination maps directly onto a [multi-node elastic deployment](/docs/self-hosting/elastic/index.md). The application keeps its own interface, the data stays on infrastructure Dicode controls, and media servers scale up and down with demand instead of being sized for the busiest day of the year.

## The result: calls that are easy to join

Ask a product team what success looks like and you'll hear about features. Ask the people joining the calls and you hear about friction. Dicode's clients care about the second:

> "From our clients' perspective, joining video calls is much easier than it would be with a solution such as Teams.
>
> Ease of use, a clear and intuitive interface, and strong privacy are important to our clients. Our solution also enables them to hold confidential video calls through our service."

For a patient organization, that's the whole point. A member joining a support session shouldn't have to install software, create an account or work through a complicated interface. And what they say in that session should stay private.

## Documentation and examples

On the developer experience side, Dicode's verdict was short:

> "We have been satisfied with the documentation and example implementations provided by OpenVidu."

## What's next: recordings and AI summaries, without giving up privacy

We asked what the team plans to build next. Recordings and AI summaries are on the list, with one condition:

> "We have considered adding call recording and generating summaries of conversations as potential future features.
>
> In this case, however, we would need to be confident that the AI model being used would not expose data to external parties. Privacy is a key concern for us."

That condition is reasonable, and it can be met. OpenVidu's [Live Captions service](/docs/ai/live-captions.md#local-providers) supports local speech-to-text providers, Vosk and Sherpa, that run on premises next to your OpenVidu deployment, so audio never leaves your infrastructure. Our post on [building a transcriber and summarizer agent](/blog/posts/2026/08/transcriber-summarizer-agent.md) shows the same idea in code, with offline Vosk transcription as one of the options.

## Dicode's advice for teams in the same spot

We closed by asking what Dicode would tell a software team that needs to add video calls to a custom application for a client:

> "If you have the freedom to choose the platform for your video calling solution, OpenVidu is a very good option. It’s easy to use, quick to implement, and there seems to be a strong commitment to continued support in the future.
>
> It also provides a foundation for maintaining control over your own data, keeping it in your hands rather than having to worry about large technology companies using it as training material for AI models."

## Key takeaways

- **Privacy can decide the platform.** For Dicode, being able to run on their own servers, comply with GDPR and keep data traffic within the EU was a core requirement, not a feature to add later.
- **A general meeting tool isn't a product foundation.** Teams works for internal meetings, but Dicode needed APIs it could customize for each client.
- **Large audiences don't need a separate tool.** Auditorium rooms, with a few speakers and many listeners, come down to per-participant permissions.
- **Ease of joining is a feature.** Dicode's clients notice how simple it is to get into a call, and that's what they compare against Teams.
- **Major version migrations take real effort.** Dicode's honest feedback on the 2.x to 3.x move is exactly the kind of input that shapes our work on the compatibility path.
- **AI has to respect the same privacy rules.** Recordings and summaries are on Dicode's roadmap, provided the models don't expose data, and local speech-to-text makes that possible.

## Building private video calls into your own product?

If you're a software team building video into a custom application, with your own interface and strict rules about where the data goes, [OpenVidu Platform](/docs/index.md) gives you the SDKs and APIs Dicode built on, self-hosted on infrastructure you choose. Start with the [deployment types](/docs/self-hosting/deployment-types.md) to find the setup that fits your scale and your privacy requirements.

Want a ready-made videoconferencing module you can embed instead of building one? That's [OpenVidu Meet Embedded](/meet/embedded/intro.md). Not sure which fits your case? The [Meet vs Platform comparison](/openvidu-meet-vs-openvidu-platform.md) helps you decide.

!!! tip "Thinking about your own success story?"
    We're always happy to talk to teams building real-time features. If you're an OpenVidu user with a story like this one, [get in touch](/support/index.md): we'll do the writing, you get the visibility and the backlinks.

*Our thanks to Janne Sikiö and the Dicode team for sharing their experience.*
