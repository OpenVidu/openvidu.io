# How DynDevice Built Virtual Classrooms Into Its LMS with OpenVidu

What do you do when your product depends on video meetings that happen somewhere else? For years, the trainers using [DynDevice](https://www.dyndevice.com/), the corporate eLearning platform built by [Mega Italia Media](https://www.megaitaliamedia.com/), had to send their learners out of the LMS and into Zoom, Meet, Teams, WebEx or GoToWebinar links to run a live class. It worked — and it fragmented the learning experience every single day.

This post kicks off our series on how engineering teams solve real WebRTC and infrastructure challenges. We interviewed **Matteo Resconi**, IT & Development Area Manager at Mega Italia Media, about the journey from juggling five external meeting tools to one-click virtual classrooms built into their own platform: what they evaluated, why they didn't build on raw WebRTC, and what changed for their team and their users.

## What is DynDevice?

DynDevice is an advanced LMS (Learning Management System) for creating, delivering and managing corporate training, developed by Mega Italia Media, an Italian eLearning company. Live virtual classrooms and webinars are not a nice-to-have in that business — they're the product:

> "Real-time video and audio are absolutely critical to our user experience because live virtual classrooms and webinars are essential components of modern corporate training. High-quality, low-latency communication allows instructors to interact seamlessly with learners, facilitating Q&As, live demonstrations, and collaborative learning directly within our ecosystem."

That last part — *directly within our ecosystem* — is the whole story. Getting there is what this interview is about.

## Life before: five meeting tools and constant context-switching

Before adopting OpenVidu, DynDevice did what most platforms do: lean on whatever web-conferencing tool each customer already had.

> "Our clients and instructors were using external tools like Google Meet, Microsoft Teams, Cisco WebEx, GoToWebinar, and Zoom to conduct their live training sessions."

If you run a platform, you know exactly what that means in practice: learners leaving your app mid-course, instructors managing meeting links by hand, five different UIs none of which carry your brand, and zero integration between the live session and the course data around it. Matteo describes the effect on users bluntly:

> "Previously, learners and instructors had to leave our LMS and juggle third-party apps for live sessions, which created friction and context-switching."

## Build vs buy: the evaluation

The interesting part is what DynDevice considered next. Their first instinct was the same one many engineering teams have:

> "Initially, we evaluated the feasibility of building our own proprietary web-conferencing system from scratch. However, since our core focus is developing and maintaining our DynDevice LMS, we realized that building on raw WebRTC stacks would require an excessively high investment of both time and financial resources."

So the team reframed the question. Not *"can we build this?"* — a good engineering team usually can — but *"should the people who build our LMS spend the next year becoming a real-time media infrastructure team?"* Their answer:

> "We pivoted to looking for a solution that provided an easy and intuitive way to manage the code, while still giving us the flexibility to add all the custom features necessary for our specific use case."

That middle ground — more than a rigid SaaS widget, less than a raw [WebRTC](https://webrtc.org/) stack you assemble yourself — is precisely the gap OpenVidu is designed to fill.

## Why OpenVidu

> "We chose OpenVidu because of the flexibility it offers in terms of deployment, scalability, and customization. The most important factor for us was the ability to extend the core functionalities already built by the OpenVidu team to perfectly fit our specific eLearning environment. It gave us the right balance between a ready-to-use architecture and the freedom to build tailored features on top of it."

Notice what's *not* in that answer: no single killer feature. The decision was architectural — a working videoconferencing core they didn't have to write, plus the freedom to shape it (self-hosted deployment, their own branding, LMS-specific behavior) without fighting the abstraction.

## What stands out to the engineering team

We asked Matteo which parts of the architecture his developers value most day to day. His answer surprised us a little — it wasn't a media feature at all:

> "From a development team's perspective, the observability tools and the cost predictability/analysis stand out the most. Having clear insights into system performance and being able to effectively monitor our infrastructure while keeping costs under control are crucial features for our daily operations."

It makes sense once you run video in production. Features demo well; observability is what lets a small team *operate* real-time infrastructure without a dedicated SRE group — and self-hosting is what makes the cost curve predictable in the first place. If you want to see what this looks like in OpenVidu, start with the [production-ready observability](https://openvidu.io/3.8/docs/self-hosting/production-ready/index.md) documentation.

## The results: faster shipping, one-click classrooms

Two outcomes matter in any build-vs-buy story: what happened to the roadmap, and what happened to the users. On the roadmap side:

> "Integrating OpenVidu significantly accelerated our time-to-market. Instead of spending months wrestling with low-level WebRTC complexities, our team could focus directly on integrating the video capabilities into the DynDevice workflow. The developer experience was excellent; the straightforward architecture and clear documentation made the integration process smooth, allowing us to roll out our custom web-conference module much faster than anticipated."

And on the user side, the friction from the "before" picture is simply gone:

> "With OpenVidu integrated directly into DynDevice, users now enjoy a seamless, all-in-one experience. They can join a live virtual classroom directly from their course dashboard with a single click, without needing to install external plugins or manage separate meeting links."

One click from the course dashboard into a branded virtual classroom — that's the experience that used to require five third-party apps.

## What's next for DynDevice

> "Looking ahead, the integration of AI is certainly on our radar. We believe AI will help both our team and our users by making the web-conferencing experience smoother, more accessible, and easier to manage and moderate."

That maps to where OpenVidu is heading too — real-time [AI agents](https://openvidu.io/3.8/docs/tutorials/ai-services/index.md) that join rooms to caption, translate, summarize or moderate. We suspect this won't be the last conversation we have with the DynDevice team about it.

## Matteo's advice for teams in the same spot

We closed by asking what he'd tell an engineering team struggling to add real-time communication to their product — or drowning while scaling their own WebRTC infrastructure:

> "My main advice would be: don't reinvent the wheel unless your core product is the video infrastructure itself. Building and scaling a raw WebRTC stack is incredibly complex and resource-intensive. If you want to save time and focus on the unique value of your own application, choose a solution like OpenVidu. It abstracts away the heavy lifting while still giving you the control and flexibility needed to build a highly customized user experience."

## Key takeaways

- **Video that lives outside your product is friction you ship every day.** External meeting links break the experience your product is supposed to own — DynDevice's users felt it, and so did their instructors.
- **Build vs buy isn't about capability, it's about focus.** DynDevice could have built on raw WebRTC; they chose to keep their engineers on the LMS and let OpenVidu carry the media stack.
- **The middle ground is real.** Between rigid SaaS meeting tools and raw stacks, a self-hosted, extensible core gave them ready-made architecture *and* room for custom features.
- **Operations decide long-term satisfaction.** The features got them in the door; observability and cost predictability are what the engineering team praises after running it in production.
- **The payoff shows up twice**: months saved on the roadmap, and a one-click, fully branded classroom for every learner.

## Bring virtual classrooms to your own platform

If DynDevice's "before" picture looked uncomfortably familiar, the fastest way out is [**OpenVidu Meet Embedded**](https://openvidu.io/3.8/meet/embedded/intro/index.md): a full-featured, brandable videoconferencing module you embed into your LMS or SaaS with a web component, a REST API and webhooks — self-hosted on your infrastructure, exactly like DynDevice runs theirs.

Need lower-level control instead — custom UIs, media pipelines, your own SDK-driven architecture? That's [OpenVidu Platform](https://openvidu.io/3.8/docs/index.md). Not sure which fits your case? The [Meet vs Platform comparison](https://openvidu.io/openvidu-meet-vs-openvidu-platform/index.md) settles it in five minutes.

Thinking about your own success story?

We're always happy to talk to teams building real-time features. If you're an OpenVidu user with a story like this one, [get in touch](https://openvidu.io/support/index.md) — we'll do the writing, you get the visibility and the backlinks.

*Our thanks to Matteo Resconi and the Mega Italia Media team for sharing their experience.*
