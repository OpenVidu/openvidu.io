---
draft: false
date: 2026-07-01
slug: cheapest-cloud-for-self-hosted-webrtc
description: A practical 2026 guide to what it really costs to self-host a WebRTC video platform on AWS, Azure, GCP, Oracle Cloud and DigitalOcean — and why bandwidth, not compute, is the number that decides your bill.
categories:
  - Comparison
  - Technology
tags:
  - WebRTC
  - Self-hosting
  - Cloud
  - Cost
  - Bandwidth
authors:
  - sergio
hide:
  - navigation
  - search-bar
  - version-selector
---

# Self-hosting a video platform in 2026: why bandwidth, not compute, decides your cloud bill

![Cost to send 1 GB of egress out to the internet, by cloud provider](/assets/images/blog/cheapest-cloud-webrtc/egress-cost-light.svg#only-light)
![Cost to send 1 GB of egress out to the internet, by cloud provider](/assets/images/blog/cheapest-cloud-webrtc/egress-cost-dark.svg#only-dark)

When people think about the cost of running their own video platform, they almost always think about the server: how many CPUs, how much RAM, how big a machine they'll need to handle all those calls. It feels like the scary number.

It usually isn't. On every major cloud, the machine that powers a real-time video server is surprisingly affordable. The number that actually moves your bill up or down is something most people never look at until the invoice arrives: **bandwidth**, specifically the *egress* — the data your server sends out to your users.

The good news is that once you understand this, self-hosting becomes very predictable. And if you pick the right provider, it stays genuinely cheap even as you grow. This post walks through where the money really goes, backed by real measurements we took on live deployments across the five big clouds.

<!-- more -->

!!! abstract "TL;DR"
    - Running a single video server idle costs roughly **$48–$150/month** on any major cloud. Compute is not the problem.
    - The dominant cost of a video platform is **egress** (data sent out to users). A media server just forwards packets, so the *amount* of data is set by your software and is nearly identical on every cloud — only the **price per GB** changes.
    - That price varies by more than **10×**: **Oracle Cloud** ($0.0085/GB after 10 TB free) and **DigitalOcean** ($0.01/GB after ~5 TB bundled) are the cheapest by a wide margin. **AWS, Azure and Google Cloud** charge $0.087–$0.12/GB.
    - Watch out for **Google Cloud's free tier: just 1 GB/month** of VM egress, versus 100 GB on AWS and Azure.
    - Pick a bandwidth-friendly cloud and your video platform is cheap and predictable. That's the whole game.

## Compute is the small, boring part of the bill

Let's get the server out of the way first, because it's the part everyone worries about and the part that matters least.

A media server for real-time video doesn't need a huge machine. A modest instance with 4 vCPUs is plenty to get started. Here's roughly what that costs, running 24/7 with no traffic at all, across the five clouds we tested:

| Cloud | 4-vCPU instance | Idle cost (≈ / month) |
|---|---|---|
| **DigitalOcean** | s-4vcpu-8gb | **~$48** |
| **Oracle Cloud** | VM.Standard.E4.Flex | **~$79** |
| **Google Cloud** | e2-standard-4 | **~$100** |
| **Microsoft Azure** | Standard_B4ms | **~$130** |
| **AWS** | c5.xlarge | **~$150** |

*(Compute prices vary by region and with committed-use discounts; these are ballpark on-demand figures for US/EU regions.)*

There's a spread here, sure — the most expensive is about 3× the cheapest — but every one of these numbers is small. You could run a real video server around the clock for the price of a streaming subscription or two. **Idle, a video platform is cheap everywhere.**

So if compute is this affordable, why do people tell horror stories about cloud video bills? Because they were looking at the wrong line item.

## The real cost driver: bandwidth

Here's the thing about a video call. Your server isn't doing heavy math on the video — a Selective Forwarding Unit (SFU), the kind of media server used by virtually every modern platform, doesn't re-encode anything. It just **receives each participant's stream once and forwards copies to everyone else in the room**. Think of it as a very fast traffic controller, not a video-processing factory.

That has two big consequences for your bill:

- **Incoming data (ingress) is free.** On all five clouds, data flowing *into* your server costs nothing. So all those uploaded camera streams? Free to receive.
- **Outgoing data (egress) is where you pay.** Every copy the server forwards to a participant travels *out* to the internet, and every cloud charges for that by the gigabyte.

Now here's the insight that ties the whole post together. Because the SFU is just forwarding, **the amount of data it sends is determined by your software and the call itself — not by which cloud you're on.** We measured this directly: the same load on live deployments in three different clouds produced almost identical egress (within about 5% of each other). The cloud doesn't change *how much* data leaves. It only changes *what you pay per gigabyte*.

!!! tip "The one idea to take away"
    On a video platform, the volume of data you send is fixed by your app. The only thing a cloud provider controls is the **price per GB of egress**. So your provider choice is, almost entirely, a bet on bandwidth pricing.

If you want to go deeper on *why* that traffic exists and how a client's network can force even more of it through your server, we wrote a whole post on [how client networks affect experience and cost](/blog/2026/04/30/how-client-networks-affect-qoe-and-costs/).

## So how much data does a video call actually move?

To turn "egress is the cost" into real numbers, you need to know how many gigabytes a busy server actually pushes out. So we measured it on live deployments.

A single media node carrying a modest load — 25 people in a room, with the server barely breaking a sweat at under 35% CPU — sent out about **25 GB per hour**. That's the *floor*: it was measured with low-resolution test video, and real HD calls push that several times higher.

That number surprises almost everyone (it surprised us — it was over 20× what a naive back-of-the-envelope estimate had predicted). But it's also empowering, because now you can estimate your own costs. A few reference points from our measurements:

- **~25 GB/hour** per node under a light, everyday load (25 participants).
- One 4-vCPU node comfortably handles **~180–200 participants** before it needs help — the SFU is remarkably CPU-efficient because it never transcodes.
- Under near-maximum load, that same node can push **~105 GB/hour**.

The takeaway isn't "video is expensive." It's that **a little bandwidth math goes a long way**, and one small node serves a lot of people. One more thing worth knowing: when a participant's firewall is too strict for a direct connection, their media has to be *relayed*, which routes even more traffic through your infrastructure — we cover that in our post on [TURN and connectivity](/blog/2026/06/09/turn-key-considerations/).

## The bandwidth price list — this is the whole game

Now the part that actually decides your bill. Here's what each cloud charges to send data out to the internet, plus how much they give you for free every month. All figures are for US/EU regions in 2026.

| Cloud | Free egress each month | Price after that (first tier) |
|---|---|---|
| **Oracle Cloud** | **10 TB** | **$0.0085 / GB** |
| **DigitalOcean** | **~5 TB** (bundled with each droplet, pooled) | **$0.01 / GB** |
| **Microsoft Azure** | 100 GB | $0.087 / GB |
| **AWS** | 100 GB | $0.09 / GB |
| **Google Cloud** | **1 GB** ⚠️ | $0.12 / GB |

Look at that price column. There's a **10–14× gap** between the two cheapest and the three most expensive. Since we established that the *volume* is the same everywhere, this table alone essentially ranks the clouds for a video workload.

A few things worth calling out:

- **Oracle and DigitalOcean are in a different league.** Oracle gives you a very generous 10 TB free every month and then charges less than a penny per GB — the lowest published rate of any major cloud. DigitalOcean bundles several terabytes into the flat price of each server and charges just a cent per GB after that.
- **Mind Google Cloud's free tier.** AWS and Azure both include 100 GB of free egress per month. Google Cloud includes just **1 GB** of VM egress — effectively nothing for a video workload. The "100 GB free" you may have heard about is a separate Cloud Storage allowance, not server bandwidth. It's an easy trap to fall into.
- **The big three do get cheaper at huge volume.** AWS, Azure and Google Cloud step their price down as you send more — AWS and Azure reach ~$0.05/GB above 150 TB, and Google Cloud bottoms out around $0.08/GB. Oracle and DigitalOcean are simply flat. But as we'll see, even with those discounts the big three stay far more expensive for video.

!!! note "Two small caveats before you quote these numbers"
    Prices depend on **region** — the figures above are for North America and Europe, which are the cheapest zones; Asia, Oceania and especially South America cost more. And a couple of providers bill in **GiB** rather than GB — a GiB is about 7% *larger*, so those per-GB rates cover a touch more data than they look. Treat all of this as very close approximations, not accountant-grade precision.

## What it actually costs per month

Let's put the server and the bandwidth together. Here's the monthly cost of one media node at three levels of use: sitting idle; a realistic everyday workload — roughly 8 hours of meetings on weekdays, which at our measured ~25 GB/h floor works out to about 4.5 TB of egress a month; and, as a deliberately extreme upper bound, a single node pinned near maximum load every hour of every day (~78 TB).

![Monthly bill for one media node at a realistic workload, by cloud](/assets/images/blog/cheapest-cloud-webrtc/monthly-cost-light.svg#only-light)
![Monthly bill for one media node at a realistic workload, by cloud](/assets/images/blog/cheapest-cloud-webrtc/monthly-cost-dark.svg#only-dark)

| Cloud | Idle | Realistic month (~4.5 TB) | Flat out 24/7 (~78 TB) |
|---|---|---|---|
| **DigitalOcean** | ~$48 | **~$48** | ~$780 |
| **Oracle Cloud** | ~$79 | **~$79** | ~$660 |
| **Microsoft Azure** | ~$130 | ~$510 | ~$6,300 |
| **AWS** | ~$150 | ~$550 | ~$6,400 |
| **Google Cloud** | ~$100 | ~$605 | ~$6,650 |

The realistic column is the one to focus on, and it tells a happy story. At everyday usage, **Oracle and DigitalOcean pay literally nothing for bandwidth** — that 4.5 TB fits inside their free allowance — so the whole bill is just the server: around **$48–$79 a month**. That's it. A production-capable video node for less than a hundred dollars.

The other three jump to several hundred dollars for the *exact same workload*, purely because of egress. Not because the servers are worse — because their bandwidth is priced for a different kind of workload.

And the scary-looking last column? That's a deliberately extreme scenario: one server slammed at near-peak load 24 hours a day, 30 days a month — something almost no real deployment does, because traffic ebbs and flows. Even in that worst case, **Oracle (~$660) and DigitalOcean (~$780) stay in the hundreds**, while the big three climb into the thousands. The lesson isn't "be afraid" — it's "the cloud you pick sets the ceiling, so pick well."

## Reading the table: who wins, and the honest caveats

If you're optimizing for the cost of a video platform specifically, **Oracle Cloud and DigitalOcean are the clear winners**, and it's not close. Their egress model — huge free allowance, then a flat sub-cent-ish rate — is simply built for high-bandwidth workloads.

But let's be fair, because it's not the whole story:

- **DigitalOcean has no ARM instances.** If you specifically want to run on ARM (for price/performance reasons), it's not an option there today — the other four all offer ARM instances if you want them.
- **AWS, Azure and Google Cloud aren't "bad."** They're expensive *for raw video egress*, but they're often chosen for excellent reasons: an ecosystem your team already knows, global region coverage, deep managed services, and enterprise agreements with **committed-use bandwidth discounts** that can cut those egress rates substantially at scale. If you're already all-in on one of them, that gravity is real.
- **These are list prices.** Negotiated contracts, reserved instances and savings plans change the compute (and sometimes egress) side meaningfully.

In other words: the ranking above is the right starting point, but the "best" cloud is the one that fits your whole situation. For a greenfield, bandwidth-heavy video project where cost is the priority, though, Oracle or DigitalOcean will save you a remarkable amount of money.

## Keeping the bill small, whatever cloud you pick

Bandwidth pricing sets your ceiling. How you run the platform sets how close you get to it. A few principles keep costs low on *any* provider:

- **Don't pay for idle capacity.** A video server costs almost nothing when it's not doing anything (remember: idle is compute-only). The waste comes from running lots of servers around the clock when your traffic is bursty. Autoscaling — adding nodes when demand rises and, crucially, removing them when it falls — is what keeps a real deployment cheap. Scaling *down* is the harder and more valuable half; we dug into it in [the scale-in problem in videoconferences](/blog/2026/05/26/scale-in-problem-in-videoconferences/).
- **A little goes a long way.** Because one modest node serves ~180–200 participants, most platforms need far fewer machines than they expect. You grow by adding nodes only when you actually need them — the full journey from a single server to a fault-tolerant cluster is laid out in [the architecture of scale](/blog/2026/06/02/scalability-in-videoconferencing-systems/).
- **Estimate before you commit.** Now that you know a busy node moves ~25 GB/hour (a floor), you can multiply by your expected usage and drop it into the price table above to forecast your bill within a comfortable margin — *before* you sign up for anything.

## Conclusion: it's cheaper than you think

If there's one myth this post exists to bust, it's that self-hosting a video platform is inherently expensive. It isn't. The server is cheap. What makes cloud video bills explode is bandwidth pricing — and that's a solvable problem, because the amount of data is fixed by your software and the price per GB is something you get to choose when you pick a provider.

Pick a bandwidth-friendly cloud like Oracle or DigitalOcean, run a couple of right-sized nodes, and scale them with your traffic, and a capable video platform costs tens of dollars a month at everyday usage — fully under your control, with no per-minute meter running against you.

The numbers in this post come from real deployments we ran across all five clouds using **[OpenVidu](https://openvidu.io/)**, our open-source stack for self-hosting real-time video. If you'd like to see these costs on your own infrastructure, you can stand up a deployment on any of these providers — starting from a single server and growing to a high-availability cluster — with the same tooling. The [self-hosting deployment guides](../../docs/self-hosting/deployment-types.md) are the place to start.

Curious what it costs *you*? Spin one up, run your own numbers, and let the bandwidth math do the talking.
