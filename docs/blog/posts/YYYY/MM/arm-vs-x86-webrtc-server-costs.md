---
title: "ARM vs x86 for WebRTC servers: participants per node on 3 clouds"
draft: false
date: 2026-09-15
slug: arm-vs-x86-webrtc-server-costs
description: "We deployed OpenVidu 3.8 on matching ARM and x86 instances in AWS, Google Cloud and Oracle Cloud and measured how many participants each node holds per dollar."
cover_image: participants-per-node-light.png
categories:
  - Comparison
  - Research
tags:
  - ARM
  - x86
  - Cloud Infrastructure
  - Benchmarks
  - Self-hosted
  - WebRTC
  - Cloud costs
authors:
  - sergio
---

# ARM or x86 for a WebRTC media server? Participants per node measured on three clouds

![Participants per node at 80% CPU, ARM vs x86, on AWS, Google Cloud and Oracle Cloud](/assets/images/blog/YYYY/MM/arm-vs-x86-webrtc-server-costs/participants-per-node-light.png#only-light "ARM vs x86: participants per OpenVidu node"){ .round-corners }
![Participants per node at 80% CPU, ARM vs x86, on AWS, Google Cloud and Oracle Cloud](/assets/images/blog/YYYY/MM/arm-vs-x86-webrtc-server-costs/participants-per-node-dark.png#only-dark "ARM vs x86: participants per OpenVidu node"){ .round-corners }

Every cloud price list says the same thing: the ARM instance is cheaper than the x86 one next to it. What it doesn't say is whether an ARM vCPU forwards as many RTP packets as an x86 vCPU, and for an SFU that is the whole question. We couldn't find a number for this, so we produced one: the same OpenVidu 3.8 single node, load generator and ramp on matching ARM and x86 instances in AWS, Google Cloud and Oracle Cloud, counting participants until the CPU runs out.

<!-- more -->

!!! abstract "What's in this post"
    Nine 4-vCPU nodes, four ARM and five x86, loaded with `lk load-test` until 85% CPU. For each one:
    participants per node, compute cost per participant-hour, and what hit its limit first. "ARM"
    turns out to be two very different things, and RAM mattered more than we expected.

The short version: on AWS, Graviton3 matches Intel per dollar and Graviton4 beats every x86 option we tried. The Ampere Altra cores behind Google's `t2a` and Oracle's `A1` are a generation behind and the price doesn't make up for it.

## Why the price list doesn't answer the question

AWS, Spain region (eu-south-2), September 2026 on-demand, 4 vCPUs and 8 GB in every case: `c7g.xlarge` (Graviton3) $0.155/hour, `c8g.xlarge` (Graviton4) $0.171, `c7i.xlarge` (Intel Sapphire Rapids) $0.192, `c7a.xlarge` (AMD Genoa) $0.220. Graviton3 is 19% cheaper than Intel and 30% cheaper than AMD. Three things make that number insufficient.

**A vCPU is not a vCPU.** On Intel instances a vCPU is one hardware thread: 4 vCPUs are 2 physical cores with SMT. On Graviton, on Ampere and also on AWS's `c7a` and GCP's `t2d`, a vCPU is a full core. "4 vCPUs vs 4 vCPUs" between `c7g` and `c7i` is 4 cores against 2 cores with hyper-threading. `lscpu` on each node confirms it (`Thread(s) per core: 1` vs `2`).

**Oracle bills per OCPU, and an OCPU is not constant either.** On the AMD shapes (E4, E5) one OCPU is a core with two threads, 2 vCPUs. On the Ampere shapes one OCPU is one core, one thread. "A1 with 4 OCPUs" against "E4 with 4 OCPUs" is a 4-vCPU machine against an 8-vCPU one. We sized everything by vCPU.

**Compute is the small part of the bill under load.** A busy media node pushes hundreds of gigabytes of video per hour, and on AWS, GCP or Azure that egress is 80-95% of the monthly cost. So the useful metric is **participants per node per dollar**, and it has to be measured.

## Setup

**Nodes.** OpenVidu 3.8.0 Single Node, Community edition, installed with the official templates for each cloud (the ones the [self-hosting docs](/docs/self-hosting/deployment-types.md) link to). Nothing was changed for ARM: since OpenVidu 3.5 every image is published for `linux/amd64` and `linux/arm64` and the installer picks the architecture of the host. The only parameter that differed between an ARM run and its x86 twin was the instance type.

Every node has 4 vCPUs and 8 GB of RAM where the cloud offers that combination; GCP's `standard-4` shapes come with 16 GB, which turns out to matter.

| Cloud | ARM nodes | x86 nodes | Region |
|---|---|---|---|
| AWS | c7g.xlarge (Graviton3), c8g.xlarge (Graviton4) | c7i.xlarge (Intel Sapphire Rapids), c7a.xlarge (AMD Genoa) | eu-south-2 |
| Google Cloud | t2a-standard-4 (Ampere Altra) | t2d-standard-4 (AMD Milan) | europe-west4 |
| Oracle Cloud | A1.Flex 4 OCPU (Ampere Altra) | E4.Flex 2 OCPU (AMD Milan), E5.Flex 2 OCPU (AMD Genoa) | eu-madrid-1 |

Azure is absent because our subscription has a zero quota on every Dpsv5 (ARM) and Dsv5 (x86) family and the quota request was refused. Google's Axion (`c4a`) had no quota either, and Oracle's AmpereOne `A2` returned a 404 on every launch. Those three are pending.

**Load.** [LiveKit CLI :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/livekit-cli){:target="_blank"} 2.18 running on a separate 8-vCPU x86 VM in the same region as the node under test, so the generator never competes for the node's CPU and traffic stays inside the cloud. One "room" is one process:

```bash
lk load-test --url wss://<node-domain>/ --api-key <key> --api-secret <secret> \
  --room ovarm-r1 --video-publishers 10 --subscribers 30 \
  --video-resolution medium --video-codec vp8 --duration 7200s
```

Each subscriber receives six of the ten tracks at about 1.6 Mbps, so a room is roughly 180 forwarded streams and 40 participants. We started one more room every 120 seconds, sampled the node every 5 seconds from `/proc/stat` (busy = total minus idle and iowait, steal recorded separately) and `/proc/meminfo`, and took the mean of the last 60 seconds of each step. The ramp stopped at 85% CPU.

This measures the SFU path only; recording (headless Chrome plus ffmpeg) and AI agents are out of scope.

## Results

The headline number is the participant count at which the node reaches 80% CPU, roughly where an autoscaler should already have added a node. CPU grows close to linearly with rooms on every machine, so the ranking is the same at 50% or 70%.

| Cloud | Instance | CPU | Arch | 4 vCPU are | $/h | Participants at 80% CPU | $ per 1,000 participant-hours |
|---|---|---|---|---|---|---|---|
| AWS | `c7g.xlarge` | Graviton3 (Neoverse V1) | ARM | 4 cores | $0.155 | **1,032** | $0.150 |
| AWS | `c8g.xlarge` | Graviton4 (Neoverse V2) | ARM | 4 cores | $0.171 | **1,493\*** | $0.114 |
| AWS | `c7i.xlarge` | Intel Xeon 8488C (Sapphire Rapids) | x86 | 2 cores × 2 threads | $0.192 | **1,258\*** | $0.152 |
| AWS | `c7a.xlarge` | AMD EPYC 9R14 (Genoa) | x86 | 4 cores | $0.220 | **1,307\*** | $0.168 |
| Google Cloud | `t2a-standard-4` | Ampere Altra (Neoverse N1) | ARM | 4 cores | $0.162 | **662** | $0.244 |
| Google Cloud | `t2d-standard-4` | AMD EPYC 7B13 (Milan) | x86 | 4 cores | $0.186 | **1,006** | $0.185 |
| Oracle Cloud | `A1.Flex, 4 OCPU` | Ampere Altra (Neoverse N1) | ARM | 4 cores | $0.052 | **346** | $0.150 |
| Oracle Cloud | `E4.Flex, 2 OCPU` | AMD EPYC 7J13 (Milan) | x86 | 2 cores × 2 threads | $0.062 | **426** | $0.145 |
| Oracle Cloud | `E5.Flex, 2 OCPU` | AMD EPYC 9J14 (Genoa) | x86 | 2 cores × 2 threads | $0.076 | **751** | $0.101 |

\* Three AWS nodes (`c7i`, `c7a`, `c8g`) never reached 80% CPU: at around 1,150 participants connections started failing with the CPU between 60% and 72%. The cause is memory. The OpenVidu server uses about **6 MB of RAM per connected participant** (1.3 GB idle, 7.4 GB at 1,080 participants, the same slope on every node) and these are 8 GB machines, so the faster CPUs hit the RAM ceiling first; the 16 GB `t2d` went past 1,000 participants with room to spare. The asterisked values are least-squares extrapolations of the last six valid steps; read them as ±10%.

What the table says:

- **Graviton3 holds 18-21% fewer participants than the Intel and AMD instances of its generation and costs 19-30% less.** Per dollar that is a tie with Intel ($0.150 vs $0.152 per thousand participant-hours) and a win over AMD. Graviton4 holds 45% more participants than Graviton3 for 10% more money, more than either x86 option, and is the cheapest compute per participant on AWS by a wide margin.
- **Ampere Altra is where the discount evaporates.** Google's `t2a` holds 34% fewer participants than its AMD sibling `t2d` while costing only 13% less, so the x86 machine is 24% cheaper per participant. Oracle's `A1` holds 19% fewer than the `E4` with the same vCPU count and lands at the same cost per participant; the newer `E5` does 2.2× the work of the `A1` for 1.5× the price.
- **Steal time appeared only on Oracle.** All three Oracle shapes, ARM and AMD alike, reported 13-19% steal at the top of the ramp; AWS and GCP reported zero. That explains part of Oracle's low absolute numbers despite reasonable per-dollar figures.
- **Media quality was constant.** Every subscriber received its tracks at ~1.6 Mbps with zero packet loss until the stop condition, on every architecture.

## Cost per participant

Hourly price divided by participants at 80% CPU gives the compute cost of keeping a thousand participants in calls for one hour:

![Compute cost per 1,000 participant-hours at 80% CPU, ARM vs x86, by cloud](/assets/images/blog/YYYY/MM/arm-vs-x86-webrtc-server-costs/cost-per-participant-light.png#only-light "Compute cost per 1,000 participant-hours"){ .round-corners loading=lazy }
![Compute cost per 1,000 participant-hours at 80% CPU, ARM vs x86, by cloud](/assets/images/blog/YYYY/MM/arm-vs-x86-webrtc-server-costs/cost-per-participant-dark.png#only-dark "Compute cost per 1,000 participant-hours"){ .round-corners loading=lazy }

The two cheapest are on opposite architectures: Oracle's x86 `E5` ($0.101) and AWS's ARM Graviton4 ($0.114). The most expensive is Google's ARM `t2a` ($0.244), 32% above the `t2d` on the same cloud.

For scale: a thousand participants cost $0.10 to $0.24 per hour in compute on any of these machines. In our test they also pushed about 1.3 Gbps out of the node, close to 0.6 TB per hour, and at AWS list prices that single hour of egress costs more than two weeks of Graviton4 compute running around the clock. The architecture decision moves the compute line only; the cloud and its egress pricing move the bill.

## What to watch for

None of the ARM deployments needed a manual step, and deploy times were within about a minute of the x86 twins. The problems are elsewhere.

**Quotas.** ARM families have their own quotas and a new account often starts at zero: our Azure subscription could not get a single Dpsv5 core and Google's Axion family did not appear in our quota list. Oracle's `A1` is known for "out of capacity" errors in busy regions. Check quotas before planning a fleet around a family.

**Instance names the template recognises.** The templates pick the arm64 image by prefix: `t4g`, `c6g`, `c7g`, `c8g`, `m7g`, `r7g` on AWS; `t2a`, `c4a`, `n4a` on GCP; `VM.Standard.A1/A2` on Oracle; sizes with a `p` in the name (`D4pls_v5`) on Azure. An unknown family gets an x86 image and does not boot. Burstable families (`t4g`, Azure `B`) run on CPU credits and are not suitable for sustained SFU load.

**RAM before CPU on fast chips.** About 6 MB per participant, regardless of architecture, so an 8 GB node tops out near 1,150 participants and Graviton4, Sapphire Rapids and Genoa all get there with CPU to spare. Pair a fast 4-vCPU instance with 16 GB (`m`-family on AWS, `standard` rather than `highcpu` on GCP, more `instanceMemory` on Oracle Flex shapes).

**Mixed clusters.** In OpenVidu Elastic and High Availability the master and the media nodes are sized independently and can run different architectures: an x86 master with an ARM media-node fleet is where the per-node saving multiplies.

## Conclusions

- **On AWS, Graviton.** Graviton3 matches Intel per dollar and beats AMD; Graviton4 beats everything measured here, with 45% more participants than Graviton3 for 10% more money. `c8g` is the media-node instance to pick.
- **On GCP and Oracle, x86 today.** Ampere Altra is a generation behind and a 13-16% discount does not cover a 19-54% gap in participants. `t2d` is cheaper per participant than `t2a`, and `E5` is far cheaper than `A1`. `A1` remains a reasonable choice when absolute price matters more than density: $0.052/hour for 346 participants.
- **Compare per participant, not per vCPU.** A vCPU is a core on Graviton, Ampere, `c7a` and `t2d`, and a thread on Intel and on Oracle's AMD shapes. The two-core `c7i` came within 4% of the four-core `c7a`; CPU generation predicts more than core count.

The compute cost of a participant-hour varies 2.4× between the best and the worst instance measured ($0.10 to $0.24 per thousand). The architecture label alone does not tell you which end you are on; the CPU generation does.

## Need more than this? { #need-more-than-this }

Everything here is a stock OpenVidu 3.8 Community single node and can be reproduced with the same templates and `lk`. To go further:

- [Deployment types](/docs/self-hosting/deployment-types.md) — when a single node stops being enough, and how Elastic and High Availability split the master and media tiers.
- The single-node install guides for [AWS](/docs/self-hosting/single-node/aws/install.md), [GCP](/docs/self-hosting/single-node/gcp/install.md) and [Oracle Cloud](/docs/self-hosting/single-node/oracle/install.md) — the instance type is a parameter; every ARM family in this post works out of the box.
- [Performance](/docs/self-hosting/production-ready/performance.md) — why OpenVidu's media server (mediasoup instead of Pion) forwards about twice the media of stock LiveKit on the same hardware.
- [Deploy OpenVidu on Hetzner in 15 minutes](/blog/posts/2026/08/deploy-openvidu-hetzner.md) — the cheapest way to try a single node.
