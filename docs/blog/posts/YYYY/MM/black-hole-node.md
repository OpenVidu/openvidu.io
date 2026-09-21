---
title: "Bug stories #1: The Black Hole Node"
draft: false
date: 2026-09-21
slug: black-hole-node
description: How a single full disk turned OpenVidu's CPU-based egress placement into a black hole that swallowed every recording, traced with the platform's built-in observability.
cover_image: poster-dark.png
categories:
  - OpenVidu Platform
tags:
  - WebRTC
  - Observability
  - Egress
  - Grafana
  - LiveKit
  - Recording
authors:
  - carlosRuiz
---

# Bug stories #1: The Black Hole Node

![The Black Hole Node: one full disk swallowed every recording in the cluster](/assets/images/blog/YYYY/MM/black-hole-node/poster-dark.png#only-dark){ .round-corners loading=lazy }
![The Black Hole Node: one full disk swallowed every recording in the cluster](/assets/images/blog/YYYY/MM/black-hole-node/poster-light.png#only-light){ .round-corners loading=lazy }

OpenVidu records media from its rooms and distributes the load across multiple Media Nodes. Distributing the load is already hard enough, and recording on top adds one more problem. In systems as complex as WebRTC, it's easy to overlook second-order effects: components that work on their own but, when combined, break in ways you never anticipated.

What we didn't expect was that this distribution policy, combined with a disk limit nobody had accounted for, could break the recording capability of an entire cluster. That was the bug we ran into.

This post describes how this policy, intended to prevent cluster overload, actually fulfilled its purpose while inadvertently breaking the recording service.

<!-- more -->

## Recordings failing for no apparent reason

In an OpenVidu cluster, we observed that, at a certain point, a huge share of Egress recordings (close to 100%) began failing. Your first instinct might be a spike in demand, but the metrics suggested otherwise: CPU usage was stable, and Media Nodes had plenty of headroom.

When CPU metrics don't indicate an overload, it's time to dig into the logs. OpenVidu deploys Grafana alongside the cluster, with container logs streamed into Loki, segmented by Media Node and service. Since the failures were specific to Egress recordings, we filtered for that service to inspect the failed attempts.

The status was identical across the board: `EGRESS_FAILED`, and every `egress_ended` webhook carried the same reason:

![Recordings returning as EGRESS_FAILED](/assets/images/blog/YYYY/MM/black-hole-node/discover-egress-failed.png){ .round-corners loading=lazy }

`"error": "No space left on the resource."`: the issue was disk space. Recordings are first written to a temporary directory before being uploaded to external storage; if that directory fills up, the write operation fails. The strange part wasn't the failure itself, but its scale: it wasn't just a few isolated recordings failing. Nearly the entire cluster was affected.

At first glance, it seemed as if all Media Nodes had run out of disk space simultaneously. However, that would be a massive coincidence. Before assuming the worst, we needed to pinpoint exactly where this was happening: in how many Media Nodes, and in which ones.

The webhook tells you that a recording failed and why, but it doesn't specify which Media Node hosted the Egress. In an OpenVidu cluster, that could be any of them. We pivoted from the Room logs to the Egress containers themselves, grouped by Media Node. The results were unexpected:

![The failing Egresses all run on the same Media Node](/assets/images/blog/YYYY/MM/black-hole-node/discover-node.png){ .round-corners loading=lazy }

All failures originated from a single source: one Media Node with a full disk, where Egress processes repeatedly died while attempting to write to the filesystem. The rest of the Media Nodes had plenty of space, and recordings weren't even reaching the healthy ones.

In other words, it wasn't a cluster-wide issue; **it was a single Media Node running out of disk**, yet almost every recording in the cluster kept getting routed to it, only to fail there. This only makes sense if the Egress dispatcher was actively routing work to the one Media Node that couldn't record.

## The root cause: the emptiest node was the broken one

So, why would the distribution algorithm pick that specific Media Node? This is where it gets counterintuitive.

When a Track, participant, or Room needs recording, OpenVidu decides which Media Node's Egress will execute it. The default strategy is `cpuload`: each Egress instance scores itself based on its available CPU, and the request is routed to the highest scorer, which is the least loaded node. On paper, distributing by CPU is entirely reasonable.

However, a full disk completely subverts this logic:

1. The Media Node with the full disk cannot start any recording: every Egress assigned to it dies almost instantly the moment it touches the disk.
2. Because it never maintains a running recording, it always reports zero active Egresses.
3. A Media Node with zero active Egresses reports maximum free CPU, giving it the highest possible `cpuload` score.
4. The dispatcher, doing exactly what it was told, sees the Media Node as the most available and sends it the next recording. It fails, leaving the Media Node idle once more, and the cycle continues as it wins the next assignment too...

![The loop that makes the node with the full disk win all the recordings](/assets/images/blog/YYYY/MM/black-hole-node/bug-cycle-dark.png#only-dark){ .round-corners loading=lazy }
![The loop that makes the node with the full disk win all the recordings](/assets/images/blog/YYYY/MM/black-hole-node/bug-cycle-light.png#only-light){ .round-corners loading=lazy }

The broken Media Node had become a black hole: **the more it failed, the more idle it appeared, and the more work it attracted**. The healthy Media Nodes, fully capable of recording, sat there doing nothing.

The underlying problem is the signal used for load balancing. Free CPU indicates if a Media Node is idle, not if it is capable of recording. A Media Node that fails instantly consumes almost no CPU: the more broken it is, the more available it appears. By looking only at CPU, a Media Node without disk space always wins exactly when it is the worst possible candidate. We needed to look at something else.

## The fix

The fix addresses this directly: checking disk availability before accepting a task. The Egress monitor now checks the recording directory; if free space falls below `min_disk_space_mb` (512 MB by default), it rejects the request with a clear reason instead of accepting it and dying mid-pipeline. A Media Node that cannot record now steps aside instead of swallowing the work.

With the fix applied to the same cluster, and the disk still full, the affected Media Node now rejects each request and explains why:

![The full Media Node rejecting recordings with reason: disk](/assets/images/blog/YYYY/MM/black-hole-node/after-node1-rejects.png){ .round-corners loading=lazy }

```
WARN egress  can not accept request
  { "total": 16, "availableDiskMB": 5, "minDiskSpaceMB": 512,
    "canAccept": false, "reason": "disk", "error": "not enough disk space" }
```

Because the full node steps aside, the dispatcher routes the recordings to the healthy Media Nodes, where they complete without issue.

The following diagram illustrates the entire lifecycle: from how the bug dragged almost all recordings toward the full Media Node, to how that same Media Node behaves now with the fix in place.

![The journey of the bug and the behavior of the full node with the fix](/assets/images/blog/YYYY/MM/black-hole-node/bug-phases-dark.png#only-dark){ .round-corners loading=lazy }
![The journey of the bug and the behavior of the full node with the fix](/assets/images/blog/YYYY/MM/black-hole-node/bug-phases-light.png#only-light){ .round-corners loading=lazy }

## Conclusions

Two takeaways, one for each half of the story.

First: recording WebRTC involves many moving parts, and a full disk was just one of them. **The real failure wasn't the disk itself, but how three components that worked fine on their own fit together**: real-time recording, the temporary storage directory, and load-based distribution.

Second: **data is only as good as your ability to interpret it**. The metrics said the cluster was healthy, and they were right, but they weren't telling the whole truth. The cause was hidden in the logs, on a single Media Node, repeating itself. This is why observability is a core part of the platform: so that when an unforeseen failure occurs, you have the tools to trace it all the way back to its source.

This bug was fixed in OpenVidu 3.6.0. If you are on that version or later, you won't run into it. We are sharing this because it is exactly the kind of second-order failure you learn the most from: invisible in metrics, capable of taking down an entire cluster's recording capability, and only revealing itself when you know where to look.

## Learn more

- [Observability in OpenVidu](/docs/self-hosting/production-ready/observability/index.md): the Dashboard and Grafana stack every deployment ships with, and the logs and metrics we followed to trace this.
- [How Egress is balanced across Media Nodes](/docs/self-hosting/production-ready/scalability.md#load-balancing-strategies-across-media-nodes): the `cpuload` and `binpack` allocation strategies, and the eligibility check every new Egress request goes through.
- [Troubleshooting recordings](/docs/troubleshooting/recording.md): recordings that fail or return a 503, including the [no disk space free](/docs/troubleshooting/recording.md#no-disk-space-free) case behind this story.
