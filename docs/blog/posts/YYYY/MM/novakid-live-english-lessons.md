---
title: "How Novakid Runs 30 Million Live English Lessons on OpenVidu"
draft: true
date: 2026-08-27
slug: novakid-live-english-lessons
description: "How Novakid migrated from raw Kurento to OpenVidu to power live English lessons for over a million kids, and what changed for their engineering team."
categories:
    - Success story
    - Vertical
tags:
    - WebRTC
    - Self-hosted
    - EdTech
    - Scalability
    - AWS
    - Migration
authors:
    - patxi
hide:
    - navigation
    - search-bar
    - version-selector
---

<!--
🚧 NOT READY TO PUBLISH — pending Novakid's sign-off, per the DynDevice-style promise made in
the outreach email ("you will have full approval over the draft before anything goes live"):

1. Logo/poster image — requested 2026-08-27 11:12, no reply yet. Poster markdown below is a
   placeholder pointing at a file that does not exist.
2. "Novakid" vs. "Novakid School" as the name used throughout — asked 2026-08-27, unconfirmed.
   This draft uses "Novakid" (matches this file's own earlier research note that the internal
   list's "Novakids" is a typo for the singular "Novakid").
3. Consent to credit Andrey (Andrei) Yakimov, DevOps Lead, by name and role — asked 2026-08-27,
   unconfirmed. This draft already uses his name/role per his own answers' signature, but that
   is not the same as consent to publish it.
4. The full draft itself still needs to go back to Novakid for review before anything ships.

See Novakid.md in openvidu-brain's Interviews folder for the full source thread.
-->

# How Novakid Runs 30 Million Live English Lessons on OpenVidu

<!-- 🖼️ PLACEHOLDER: poster image needed before publish (light/dark webp variants) — ideally Novakid's own logo/product screenshot once they send one. -->
![Novakid and OpenVidu customer success story](/assets/images/blog/YYYY/MM/novakid-live-english-lessons/poster-light.webp#only-light "Novakid + OpenVidu")
![Novakid and OpenVidu customer success story](/assets/images/blog/YYYY/MM/novakid-live-english-lessons/poster-dark.webp#only-dark "Novakid + OpenVidu")

Try running a live video product where the users are seven years old. Adults tolerate a frozen frame or a reconnect spinner; a seven-year-old just wanders off, and the parent watching over their shoulder doesn't book a second lesson. That's the bar [Novakid](https://www.novakidschool.com/){:target="_blank"}, an online English school for kids aged 4–12, has run against since 2017. Over a million students, 50+ countries, more than 30 million lessons delivered, and up to 2,300 lessons running at once at peak.

We talked to **Andrei Yakimov**, DevOps Lead at Novakid, about moving their live classroom off a self-managed Kurento deployment and onto OpenVidu: what that migration actually looked like, how they built scheduled autoscaling on top of it, and what broke (and got fixed) along the way.

<!-- more -->

## What is Novakid?

Novakid pairs children with real teachers for live one-on-one and small-group English lessons, wrapped in a gamified classroom: interactive exercises, games and activities run alongside the video the whole time. Andrei is blunt about what that means for the infrastructure underneath it:

> "When your students are young children, the bar is unforgiving: kids won't tolerate frozen video, audio glitches, or reconnection loops the way adults might. A single bad technical experience can ruin a lesson and shake a parent's trust. So for us, video infrastructure isn't a supporting service — it's mission-critical, core infrastructure of the business."

That's the whole story in one paragraph: for most companies, video is a feature. For Novakid, it's the product.

## Life before OpenVidu: running Kurento themselves

Novakid didn't start on OpenVidu. For years, they ran directly on the open-source [Kurento Media Server](https://www.kurento.org/){:target="_blank"}, the same media server OpenVidu itself was originally built around.

> "We built everything around it ourselves: load balancing across media nodes, scaling logic, session recording to S3, video post-processing, and all the operational subtleties that come with running WebRTC media infrastructure at scale. It worked, but it meant we owned a large amount of custom orchestration code that had nothing to do with our actual product — teaching kids English."

That's a familiar shape: the media server itself is only the beginning. Balancing, scaling, recording and monitoring around it are their own engineering project, and Novakid was maintaining all of it on top of an open-source component instead of teaching English.

## Why not build on raw WebRTC, or buy commercial SaaS?

Having already lived through the "build it yourself" path with Kurento, the team knew exactly what that costs. So when it was time to move on, they evaluated both extremes:

> "We had already lived the 'build it yourself on a raw media server' path with Kurento, so we knew exactly what that costs in engineering time. When evaluating the next step, we looked at commercial SaaS top vendors but per-minute/per-participant pricing simply doesn't work at our lesson volume; the economics of self-hosting are dramatically better for a platform running millions of lessons per year. We also looked at LiveKit. In the end, OpenVidu offered the best combination for us: a vendor-managed platform that we still fully control and host ourselves."

That framing, "vendor-managed platform we still fully control and host ourselves," is precisely the middle ground between a raw stack and a metered SaaS API.

## Why OpenVidu

Novakid had already been running Kurento in production, so OpenVidu wasn't unfamiliar territory:

> "It was a natural evolution rather than a leap. Coming from Kurento, OpenVidu was a familiar ecosystem built by a team we already trusted — moving to it meant replacing our homegrown orchestration (balancing, scaling, recording pipelines) with a supported, battle-tested product while keeping the self-hosted model we needed. At the time there weren't many mature self-hosted alternatives, and commercial SaaS pricing was far above our target infrastructure cost."

Novakid started on OpenVidu 2.x (Pro) and has since upgraded to OpenVidu 3 (Pro/Enterprise).

## What stands out to the engineering team

Asked what features of the architecture matter most day to day, Andrei covers deployment and scaling, and adds one honest limitation too:

> "Clean deployment flow via CloudFormation. Standing up or rebuilding a cluster is a well-understood, repeatable process rather than a bespoke project. Customization through AWS ASG launch templates lets us slip in a fresh, patched AMI that rolls out across media nodes without reinstalling the whole platform — that makes routine maintenance boring, in the best possible way. High availability, with multiple master nodes, gives us the fault tolerance a mission-critical service needs."

They also built their own scheduled autoscaling on top of OpenVidu's scaling mechanics:

> "Since we know our lesson schedule in advance, we built scheduled autoscaling on top of OpenVidu's scaling mechanics. The cluster grows before peak teaching hours and shrinks after — we call it the 'breathing' of our infrastructure. It saves us significant money by not holding idle capacity across time zones."

And the honest part:

> "Built-in observability. The bundled monitoring and logging stack has helped us get to the bottom of production issues more than once. One honest piece of feedback: under load it could itself become a bottleneck on the master nodes, and in hindsight we'd recommend moving the observability stack out to dedicated VMs."

## Migrating from v2 to v3: two or three days, not months

Version migrations are usually where infrastructure projects get scary. Not this one:

> "Honestly, it wasn't hard at all — mostly thanks to how we approach migrations. We deploy the new cluster side by side with the old one, route a portion of the traffic to it at the application level, watch how it behaves, and then gradually complete the switchover. The whole process typically fits into two or three days. No big-bang migration, no downtime drama."

A blue-green rollout at the application level, not a maintenance window, is the difference between a migration your users notice and one they don't.

## Tailoring elasticity, and how stable it's actually been

Because Novakid's Lambda-driven autoscaling sits on top of standard AWS building blocks, extending it wasn't a fight:

> "AWS infrastructure is home turf for us, so working with things like Auto Scaling Groups felt natural. We added Lambda functions that monitor our lesson schedule and adjust the number of media nodes ahead of demand. And because OpenVidu's built-in load-balancing mechanisms handle session draining well, scaling down is smooth — media nodes are removed gracefully without disrupting ongoing lessons."

On stability compared to their self-managed Kurento days, Andrei gives real credit both ways:

> "To be fair to Kurento, most of those problems came from the orchestration layer around it — the load balancing, scaling, and recording logic we had built and maintained ourselves. OpenVidu is simply a more mature solution from our point of view, and it brought real gains in stability and fault tolerance. To be honest, we did also hit a few issues inside OpenVidu itself — mostly around MongoDB load from telemetry collection, which at our volumes could overload the master nodes. But the OpenVidu engineers (special thanks to Carlos and Pablo!) helped us resolve them remarkably quickly. That responsiveness is exactly the kind of engineer-to-engineer partnership we mentioned in our earlier answers."

## The developer experience, and what changed for time-to-market

On the infrastructure side, CloudFormation turned deployment from a project into a repeatable step:

> "We can treat OpenVidu largely as a black box — deploy it, scale it, monitor it — and spend our engineering time on the product instead of on media-server plumbing that used to be entirely our responsibility in the Kurento days. A good real-world example: when the business needed us to expand into a new geographic region, we had to stand up a completely new cluster from scratch — and it was remarkably fast."

On the frontend, building on OpenVidu's LiveKit-compatible SDKs shortened the loop between product and engineering:

> "The integration was smooth because OpenVidu lets us build on the LiveKit SDKs, which are very developer-friendly. The APIs are clear, the documentation is practical, and the SDKs handle much of the low-level real-time communication complexity, so we can focus on the classroom UI and the learning experience rather than media plumbing."

## What it changed for students and teachers

> "The most important effect is the one nobody notices: after moving to OpenVidu, overall lesson quality went up and technical failures attributable to the video infrastructure went down noticeably. Our classroom is heavy on interactive content — games, exercises, and shared activities run alongside the live video throughout the lesson — so the video layer has to be a stable foundation that everything else can rely on. With OpenVidu, it is. For teachers, that means fewer interrupted lessons; for kids, it means staying immersed in the lesson instead of waiting for video to recover."

## AI, child safety, and what's next

Novakid already runs AI-powered lesson analytics, but today it's a post-lesson, offline pipeline:

> "We already run AI-powered lesson analytics today, built as separate services downstream of OpenVidu: we take lesson recordings, extract the audio, and analyze that everything in the classroom went well — including sensitive quality signals like teacher tone and classroom conduct. This feeds our teacher operations team and is an important part of quality assurance and child safety on a platform serving young learners."

That's exactly the shape of workload OpenVidu's server-side AI Agents target: running that kind of analysis live, inside the media pipeline, instead of after the fact.

> "That whole pipeline currently runs on recordings, post-lesson. So the direction OpenVidu is taking with server-side AI Agents is genuinely interesting to us — the ability to run this kind of analysis closer to real time, inside the media pipeline itself, is a natural next step we're keeping a close eye on."

## Andrei's advice for teams in the same spot

We closed by asking what he'd tell an engineering team struggling to build or scale real-time communication into their own product:

> "Understand WebRTC — at least in a nutshell. You don't need to implement an SFU, but you need to know what ICE, TURN, and codecs are doing to your traffic, or you'll be debugging blind. Learn to debug actual media streams, and fall in love with `chrome://webrtc-internals` — it will tell you more about a 'bad lesson' than any server log. Invest in monitoring your bottlenecks early: in real-time systems, degradation is gradual and user-visible long before anything crashes. Think about recording storage economics from day one — millions of lessons means petabyte-scale questions about what to keep, at what quality, and for how long. Don't be afraid to experiment: we went from raw Kurento to OpenVidu 2 to OpenVidu 3, and each step was worth it. And build partner-level relationships with your vendors, engineer to engineer — having a direct line to the people who build your media platform is worth more than any SLA document when something strange happens at 2 a.m. in some time zone."

## Key takeaways

- **Running your own media server is its own product.** Kurento was only the starting point; the load balancing, scaling, recording and monitoring Novakid built around it were the real engineering cost.
- **"Vendor-managed but self-hosted" is a real middle ground.** It sits between a raw WebRTC stack and metered SaaS pricing: a supported platform they still fully control and run on their own AWS account.
- **Scheduled autoscaling pays for itself.** Knowing lesson demand in advance lets Novakid's infrastructure "breathe": it scales up before peak hours and back down after, instead of holding idle capacity around the clock.
- **A version migration doesn't have to be scary.** A side-by-side cluster with gradual traffic shifting turned the v2→v3 upgrade into a 2–3 day non-event.
- **Observability is a feature you have to operate, too.** Novakid's honest feedback, that the bundled stack became a bottleneck under load, is exactly the kind of production experience that's worth more than a features list.
- **Engineer-to-engineer support matters when things get strange.** A MongoDB-driven telemetry bottleneck got resolved quickly because Novakid had a direct line to OpenVidu's own engineers, not a ticket queue.

## Building your own live classroom or interactive video product?

If you're weighing the same build-vs-buy-vs-self-host question Novakid faced, [OpenVidu Platform](/docs/index.md) gives you the LiveKit-compatible SDKs, self-hosted control and AWS-native deployment tooling this story is built on. See the [self-hosting deployment types](/docs/self-hosting/deployment-types.md) to find the topology that matches your own scale.

!!! tip "Thinking about your own success story?"
    We're always happy to talk to teams building real-time features. If you're an OpenVidu user with a story like this one, [get in touch](/support.md): we'll do the writing, you get the visibility and the backlinks.

*Our thanks to Andrei Yakimov and the Novakid team for sharing their experience.*
