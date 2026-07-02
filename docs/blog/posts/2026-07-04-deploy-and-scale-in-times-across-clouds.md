---
draft: false
date: 2026-07-04
slug: deploy-and-scale-in-times-across-clouds
description: A follow-up to our scale-in post — real measured deploy times across AWS, Azure, GCP, Oracle Cloud and DigitalOcean, and what it really takes to safely scale a self-hosted WebRTC video platform back down.
categories:
  - Technology
  - Research
tags:
  - DevOps
  - Cloud Infrastructure
  - Autoscaling
  - Scale-In
  - Benchmarks
authors:
  - sergio
hide:
  - navigation
  - search-bar
  - version-selector
---

# Scaling up is fast, scaling down is slow: we timed five clouds — one took 14 minutes just to decide, another never did

![Time to a working deployment, by cloud and deployment type](/assets/images/blog/scale-in-times/deploy-times-light.svg#only-light)
![Time to a working deployment, by cloud and deployment type](/assets/images/blog/scale-in-times/deploy-times-dark.svg#only-dark)

A few weeks ago we argued that [scaling *up* is easy and scaling *down* is the real hard part](/blog/2026/05/26/scale-in-problem-in-videoconferences/) of running a real-time video platform. You can't just kill a media node that has live meetings on it — you have to *drain* it first, and each cloud gives you a different, awkward set of primitives to do that safely.

That post made the argument. This one brings the receipts.

We built a tool, **ov-cloud-tester**, that deploys the same self-hosted video stack on all five major clouds — AWS, Azure, Google Cloud, Oracle Cloud and DigitalOcean — in every topology (single node, elastic, high-availability), drives real WebRTC load at it, and puts a stopwatch on every phase: how long to stand up, how long to add a node under load, and — the interesting one — how long to *safely take a node away* again. The numbers confirm the thesis and then some: standing up is fast and boringly predictable, while scaling back down is slow, wildly cloud-dependent, and on one cloud it didn't happen at all within our window.

<!-- more -->

!!! abstract "TL;DR"
    - **Deploying is fast:** a single node is ready in **4–12 minutes** across all five clouds; DigitalOcean is quickest (~4 min), Oracle slowest (~12 min).
    - **A full HA cluster is where clouds diverge hard:** GCP is ready in **~6.5 min**, while AWS takes **~27.5 min** — a 4× spread, most of it DNS propagation baked into readiness.
    - **Scaling in is dominated by one thing: how long the cloud takes to even *decide* to remove a node.** We measured **up to ~14.5 minutes** just for that decision on GCP.
    - **AWS didn't scale in at all** within our 10-minute window — CPU well under target, the cluster plainly over-provisioned, and the Auto Scaling Group simply hadn't acted. With default cooldowns, "elastic" can quietly mean "fixed-size, but still paying."
    - **GCP and DigitalOcean are mirror images:** GCP scales out fast (~3.5–4 min) but marks nodes for removal slowly; DigitalOcean scales out slowly (~9–10.5 min) but marks them fast (~2.5–3.5 min).
    - **Actually removing a drained node is trivial** — ~35 seconds once it's empty. The cost of scaling in is the *decision* plus the *deliberate* graceful drain, never the teardown.

## The claim we're testing

Quick recap, because this is a direct sequel. A media node is **stateful** in the most unforgiving way: every participant holds a live WebRTC connection pinned to that specific machine, with its own ICE candidates, DTLS keys and SRTP state. There is no transparent session migration. Kill a node anyway and you get the forty-people-mid-sentence problem from last time — every live call on it drops at once, with no retry and no rewind. So when the autoscaler decides the cluster is over-provisioned and wants to remove a node, you cannot just terminate it — you have to mark it as *draining*, stop sending it new rooms, wait for the meetings already on it to end, and only *then* let the cloud reclaim the machine.

Every cloud implements the interception differently (AWS lifecycle hooks, Azure runbooks, GCP scale-out-only MIGs plus a scheduled function, DigitalOcean external functions). We covered the *mechanisms* in the [previous post](/blog/2026/05/26/scale-in-problem-in-videoconferences/). What we never had were the *timings*. Now we do.

## How we measured it

Every run is a real deployment — real Terraform / CloudFormation / ARM, real VMs, real OpenVidu — torn down cleanly afterwards. The tool records the duration of each atomic phase from its own logs, so the numbers are wall-clock times a real operator would experience, not estimates.

Two things worth defining up front, because they're where the interesting numbers live:

- **Time to ready** = `deploy` (all cloud resources created) **+** `wait-ready` (the deployment's real endpoint starts answering over HTTP). We report the *sum*, because the clouds split the work differently — AWS folds the software install into the deploy step, while others finish provisioning quickly and then spend minutes booting and installing before the endpoint answers. Only the sum is a fair comparison.
- **Scale-in phases.** Under a fixed synthetic load (5 rooms with 15 publishers and 80 subscribers, generated with the LiveKit `lk` CLI) we push a media node past a **50% CPU** autoscaling threshold and then measure three distinct, cloud-comparable phases:

    1. **Scale-out** — from a node crossing `>50%` CPU to a *new* node being registered and ready.
    2. **Mark latency** — from CPU dropping back `<50%` to the autoscaler actually *marking* a node for removal.
    3. **Drain-death** — from the marked node having no rooms left to it actually being removed.

    Between phases 2 and 3 there's a deliberate **graceful-drain hold** (default 20 minutes) where the marked node keeps serving its last meeting. That hold is a *policy choice*, not a cloud limitation, so we exclude it from the three phases above — which makes those three directly comparable across providers.

One honest caveat before the numbers: we have complete, live scale-in measurements for **GCP and DigitalOcean** (elastic and HA). AWS we'll get to — it produced a genuinely interesting result. Azure and Oracle scale-in timings aren't measured live yet, so we won't invent them; where they appear it's the mechanism, not a stopwatch.

## Scaling up: fast and boringly predictable

Here's how long it took to go from "go" to a deployment answering requests, per cloud and topology:

| Topology | AWS | Azure | GCP | Oracle | DigitalOcean |
|---|---|---|---|---|---|
| **Single node** | 7m30s | 7m32s | 6m27s | 12m10s | **4m03s** ⚡ |
| **Elastic** | 6m30s | 8m45s | **5m10s** ⚡ | 9m32s | 9m13s |
| **High availability** | **27m35s** 🔴 | 21m45s | **6m29s** ⚡ | 12m56s | 9m02s |

The single-node story is unremarkable in the best way: every cloud gets you a working server in single-digit-to-low-double-digit minutes. DigitalOcean is the sprinter (~4 min and it also tears down in seconds); Oracle is the tortoise (~12 min — its VMs provision in about 40 seconds, but the software then takes 11+ minutes to come up healthy). Nothing here will surprise or hurt you.

**High availability is where the clouds stop agreeing.** GCP stands up a full HA cluster in ~6.5 minutes — faster than it took some clouds to deploy a *single node*. AWS, at the other extreme, took ~27.5 minutes. Most of that AWS penalty isn't compute: it's the Route 53 alias to the load balancer taking ~15 minutes to propagate, so the endpoint returns NXDOMAIN until DNS catches up, and readiness has to wait it out. It's a real delay a real operator hits on first deploy — but it's a DNS artifact, not GCP being "4× better at servers."

!!! tip "Takeaway 1"
    Deployment time is a solved problem — but "time to *ready*" is not the same as "time to provision." The gap between them (software boot, DNS propagation, health checks) is where the minutes hide, and it varies more by cloud than the raw infrastructure does.

## Scaling down: where the minutes actually go

Now the part the previous post was really about. When load drops and the cluster wants to shrink, how long does it take — and where does the time go?

![Where the minutes go when scaling in: scale-out vs mark-for-removal vs drain-death](/assets/images/blog/scale-in-times/scale-in-phases-light.svg#only-light)
![Where the minutes go when scaling in: scale-out vs mark-for-removal vs drain-death](/assets/images/blog/scale-in-times/scale-in-phases-dark.svg#only-dark)

| Cloud · topology | Scale-out<br>(add a node) | Mark latency<br>(decide to remove) | Drain-death<br>(remove empty node) |
|---|---|---|---|
| **GCP** · elastic | 3m32s | **6m44s** | 38s |
| **GCP** · HA | 4m12s | **12m02s** | 40s |
| **DigitalOcean** · elastic | **9m08s** | 2m32s | 33s |
| **DigitalOcean** · HA | **10m25s** | 3m34s | 33s |

Three things jump out.

**First: removing a drained node is trivial — about 35 seconds, on both clouds, in every topology.** Once a node is empty, tearing it down is a non-event. So when people worry that "scaling in is slow," the teardown is never the culprit.

**Second: the expensive phase is the *decision* — the mark latency.** This is the time between "load has clearly dropped" and "the autoscaler has committed to removing a node." On GCP it ran from **6m44s up to 12m02s** depending on topology, and across repeated runs we saw it swing as high as **14m36s**. That's a quarter of an hour where you're knowingly over-provisioned, paying for a node the system already agrees it doesn't need, before any graceful drain even begins.

**Third: GCP and DigitalOcean are near-perfect mirror images.**

- **GCP** scales *out* fast (~3.5–4 min — its Managed Instance Group reacts quickly) but is *slow to mark* a node for removal.
- **DigitalOcean** is the exact opposite: *slow to scale out* (~9–10.5 min — it has no native autoscaling group, so it provisions droplets from scratch) but *fast to mark* (~2.5–3.5 min).

Neither cloud is "fast at scaling." Each is fast at one direction and slow at the other. If your traffic is bursty and you care about reacting quickly to *drops* (to save money), DigitalOcean's decision loop wins; if you care about reacting quickly to *spikes* (to protect quality), GCP's does. There is no free lunch, and the shape of that trade-off is a property of the cloud's autoscaler, not of your software.

!!! tip "Takeaway 2"
    Scaling in is almost entirely *mark latency* + a *deliberate* drain hold. The teardown is instant; the drain is a safety policy you choose. The number that actually varies between clouds — and that you can't control — is how long the provider takes to *decide*.

## The AWS surprise: it didn't scale in at all

AWS deserves its own paragraph, because it produced the most instructive result of the whole campaign. Scaling *out* worked exactly as expected: under load, a second node registered in about 3m42s, rooms seeded onto it, all good. But when we dropped the load and waited for the Auto Scaling Group to mark a node for removal… it didn't. Not within our 10-minute observation window. CPU was well under the 50% target, the cluster was plainly over-provisioned, and the ASG simply hadn't acted yet.

We're deliberately not turning this into "AWS can't scale in." The [previous post](/blog/2026/05/26/scale-in-problem-in-videoconferences/) explains why AWS's lifecycle-hook mechanism is actually the *cleanest* of the four once it does fire. This is about **latency**: ASG scale-in is governed by cooldowns and alarm-evaluation periods that, with conservative defaults, can easily exceed ten minutes before a termination decision is even made. It's the same lesson GCP's 14-minute mark latency teaches, in a more extreme form — the *decision* to scale in is slow and provider-controlled, and if you don't tune it, "elastic" quietly becomes "fixed-size, but you're still paying for the extra node."

## Why the clouds differ this much

None of this is random. Scale-out is a simple additive operation, so every cloud does it in minutes. Scale-in is a *destructive* operation against a live system, so every cloud wraps it in caution — and each expresses that caution through a different control loop:

- **GCP** — a scheduled Cloud Function (`*/5`) compares actual vs recommended MIG size and removes the excess; per-node cron then triggers the graceful shutdown. Fast to grow, slow and spiky to decide to shrink.
- **DigitalOcean** — an external function polls demand on a `*/2–*/4` cron and flags droplets to drain. Slow to grow, fast to decide to shrink.
- **AWS** — native ASG lifecycle hooks: the cleanest interception once triggered, but gated behind cooldowns and alarm periods that make the *decision* slow by default.
- **Azure** — VMSS instance protection plus an Automation Account runbook; the previous post cited Azure's documented up-to-5-minute latency before the graceful shutdown even begins.
- **Oracle** — instance-pool detach driven by the same threshold logic.

The pattern underneath all of them: **the graceful drain is under your control and is uniform (~35s teardown, plus whatever hold you configure), but the mark-for-removal decision belongs to the cloud, and that's where the double-digit-minute surprises live.**

## What to actually do about it

A few practical conclusions we'd stand behind:

- **Budget for scale-in latency, and measure it on *your* cloud.** "The autoscaler will handle it" hides a 2-to-15-minute decision delay that differs several-fold between providers. That delay is money — every minute a marked-but-not-removed node lives is a minute you're paying for capacity you don't need.
- **Don't assume symmetric scaling.** The cloud that adds nodes fastest is often the slowest to remove them. Pick based on whether spikes or lulls dominate your traffic.
- **Tune the decision, not the drain.** The graceful-drain hold is a safety feature — keep it generous enough to outlast a real meeting. The lever worth tuning for cost is the provider's scale-in cooldown / cron / evaluation period, which is what actually gates the decision.
- **"Time to ready" ≠ "time to provision."** Especially for HA, plan around DNS propagation and health-check windows, not just VM boot time.

## Conclusion: the asymmetry is real, and now it has numbers

Our earlier claim was that scaling down is the hard direction. The stopwatch agrees. Standing up a deployment is fast and predictable everywhere (minutes, single node; a bit more for HA). Adding a node under load is fast too. But *removing* one safely is slow, and almost all of that slowness is the cloud taking its time to *decide* — up to ~14.5 minutes on GCP, and beyond our window entirely on AWS with default settings — while the actual graceful teardown is a uniform ~35 seconds.

The good news for anyone running a real-time platform: none of these delays have to translate into a broken meeting or a runaway bill. The drain itself is safe by construction, and the decision latency is tunable once you know it's there. In [OpenVidu](https://openvidu.io/), graceful scale-in ships configured out of the box on every supported cloud, so a scale-down event never interrupts a live room — the numbers in this post came from exercising exactly that machinery, on all five clouds, over and over.

If you want to see it on your own infrastructure — or just run your own stopwatch — start with the [self-hosting deployment guides](../../docs/self-hosting/deployment-types.md) and pick the topology that fits your traffic.

The cloud is happy to scale you up in a hurry. Scaling you back down is the part worth measuring.
