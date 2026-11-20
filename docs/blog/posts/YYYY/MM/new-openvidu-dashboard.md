---
title: Monitor self-hosted video calls with the new OpenVidu Dashboard
draft: false
date:
  created: 2026-11-20
slug: new-openvidu-dashboard
description: >-
  OpenVidu 3.10 ships a rebuilt dashboard to watch rooms, participants and
  recordings live and to analyze usage and call quality over time.
cover_image: poster-light.png
categories:
  - OpenVidu
  - Technology
tags:
  - Observability
  - Monitoring
  - Analytics
  - Self-hosted
  - WebRTC
  - LiveKit
authors:
  - juanCarlos
---

# Monitor self-hosted video calls with the new OpenVidu Dashboard

![Overview page of the new OpenVidu Dashboard, with live counters of rooms, participants, egress, ingress and agents, the figures of the day and the state of each media node](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/poster-light.png#only-light "The new OpenVidu Dashboard"){ .round-corners }
![Overview page of the new OpenVidu Dashboard, with live counters of rooms, participants, egress, ingress and agents, the figures of the day and the state of each media node](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/poster-dark.png#only-dark "The new OpenVidu Dashboard"){ .round-corners }

A user writes to you: "yesterday's call sounded terrible". What can you answer? If you run your own video infrastructure, you are the one who has to find out whether it was their Wi-Fi, your server or your application. And the day your boss asks how much the platform is used, or whether it's time for a bigger machine, you need an answer for that too.

OpenVidu 3.10 comes with a completely rebuilt <a href="/docs/self-hosting/production-ready/observability/openvidu-dashboard/">OpenVidu Dashboard</a> made for those questions. It tells you what is happening in your deployment **right now** and what happened **over time**, down to the packet loss of a single track. In this post we walk through what's new and how to use it.

<!-- more -->

## Why we rebuilt it

The previous dashboard listed rooms, egresses and ingresses from the events OpenVidu Server stored. It was enough to see that a room existed, but not to explain how a call went or how your usage evolved. Long time ranges were slow, too.

So we started from the data. OpenVidu Server 3.10 writes a new analytics model to MongoDB, and the dashboard is built on top of it:

- **Entities kept up to date.** Rooms, participant sessions, tracks, egresses and ingresses are stored as such, updated as their events arrive.
- **Statistics every 30 seconds.** Quality score, bitrate, packet loss, jitter and round-trip time.
- **Rollups.** Counters aggregated every 5 minutes, hour and day, so a 90-day chart loads as fast as a one-hour one.

The dashboard is included in every [OpenVidu deployment](/docs/self-hosting/deployment-types.md), and nothing leaves your infrastructure: the data lives in your own MongoDB.

## Five questions the new dashboard answers

The best way to show a dashboard is to ask it things. These are five questions you will bring to it sooner or later, and where it answers each of them.

### What is happening right now?

The landing page is the **Overview**, the image at the top of this post. Its counters show the active rooms, the participants connected, how many of them publish, and the egresses, ingresses and agents running at this moment. Each counter opens its list already filtered to what is live, and **Today** sums up the day so far.

Live pages refresh on their own, and they are honest about it. The label next to the title reads **LIVE** while data keeps arriving, **paused** if you turned auto-refresh off, and **stale** when the server stopped writing. The **Data pipeline** card says when the last batch of data arrived, so you always know how far to trust what you see.

### How is my deployment used?

The **Analytics** page looks at a whole time range, from the last hour to the last 90 days or any custom range. Use it to follow growth, to size your infrastructure against the busiest moments and to compare one period with another.

![Analytics page of OpenVidu Dashboard, with rooms created, participant sessions, data transferred and the charts of active rooms and room topology](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/analytics-light.png#only-light){ .round-corners loading=lazy }
![Analytics page of OpenVidu Dashboard, with rooms created, participant sessions, data transferred and the charts of active rooms and room topology](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/analytics-dark.png#only-dark){ .round-corners loading=lazy }

A few of the things it answers:

- **How big is my peak?** The most rooms and participants connected at once, which is what your servers have to hold.
- **What kind of application do I really have?** *Room topology* classifies your rooms by shape: 1:1 calls, 1:N sessions with a single sender (a webinar, a class) and N:M meetings. It also tells you how many rooms stayed empty.
- **What do my users connect with?** SDK, operating system, browser and connection type.
- **How much do I record and stream?** Egresses and ingresses over time, and how the egresses ended.

Every section exports its data as an Excel workbook, in case you want to take the numbers to a report.

### Why was that call bad?

Back to the complaint of the introduction. With OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }, every room, participant, track, egress and ingress has its own page, and together they take you from the symptom to the cause.

**1. Find the room.** Press `/` and type its name. The page of a room tells its whole story: three charts follow its active participants, bitrate and quality, with every join, leave and recording marked on them. If quality dropped at 22:41, you see what else happened at 22:41.

![Room details page of OpenVidu Dashboard, with the figures of the room and the chart of active participants with joins and leaves marked](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/room-light.png#only-light){ .round-corners loading=lazy }
![Room details page of OpenVidu Dashboard, with the figures of the room and the chart of active participants with joins and leaves marked](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/room-dark.png#only-dark){ .round-corners loading=lazy }

**2. Open the participant who had the problem.** Their page shows what that person experienced: the browser, device and network they used, the connection type, how many times the connection had to be resumed, and the quality, packet loss, jitter and round-trip time over time.

**3. Go down to the track.** If only their camera froze, open it from the published tracks. The track panel shows its codec, resolution and simulcast layers, and the statistics of each of its subscribers. That is how you tell a bad uplink from one subscriber with a bad downlink.

![Track panel of the participant details page, with the codec, layers, publish statistics and subscribers of a video track](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/participant-track-light.png#only-light){ .round-corners loading=lazy }
![Track panel of the participant details page, with the codec, layers, publish statistics and subscribers of a video track](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/participant-track-dark.png#only-dark){ .round-corners loading=lazy }

And when the question is not about one call but about all of them, the PRO sections of Analytics help. **Quality** draws the average quality score over time, **Top rooms** ranks the rooms of the range with the worst quality, and **Diagnostics** shows why participants disconnected, why rooms ended and which API calls failed.

![Diagnostics section of the Analytics page, with disconnect reasons, room end reasons, subscribe failures and API calls by method](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/analytics-diagnostics-light.png#only-light){ .round-corners loading=lazy }
![Diagnostics section of the Analytics page, with disconnect reasons, room end reasons, subscribe failures and API calls by method](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/analytics-diagnostics-dark.png#only-dark){ .round-corners loading=lazy }

!!! tip "The dashboard and Grafana complement each other"
    The dashboard explains your rooms and your users. When you need to see what the services themselves were doing, OpenVidu also ships a [Grafana stack](/docs/self-hosting/production-ready/observability/grafana-stack.md) with the logs of every service of your deployment.

### Did my recording, stream or agent work?

Rooms are not only people. The services that join them have their own pages:

- **Egress.** The list refreshes live, so you can follow a recording or a stream while it runs. In PRO, the page of an egress shows where its files were stored, their size, when it reached each status and, if it failed, why.
- **Ingress.** An ingress is a reusable input, and each stream published to it is a session, with its video and audio details.
- **Agents.** Every agent session with its agent name, room and duration. Agents from the official collection of [OpenVidu agents](/docs/ai/openvidu-agents/overview.md) carry an **OpenVidu** tag, and a filter separates them from your own.

![Agents page of OpenVidu Dashboard, listing agent sessions with their agent name, the OpenVidu tag, room, status and duration](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/agents-light.png#only-light){ .round-corners loading=lazy }
![Agents page of OpenVidu Dashboard, listing agent sessions with their agent name, the OpenVidu tag, room, status and duration](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/agents-dark.png#only-dark){ .round-corners loading=lazy }

### Is every media node healthy?

In OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag } Elastic and High Availability deployments, rooms are spread over several media nodes, and the dashboard follows them.

![Media nodes page of OpenVidu Dashboard, with the state, version, active rooms and participants of each media node](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/media-nodes-light.png#only-light){ .round-corners loading=lazy }
![Media nodes page of OpenVidu Dashboard, with the state, version, active rooms and participants of each media node](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/media-nodes-dark.png#only-dark){ .round-corners loading=lazy }

The **Media nodes** page tells whether each node is alive, draining before it stops, not reporting or stopped. It also counts the rooms OpenVidu Server had to close itself because their node disappeared, which is the number to watch if you suspect crashes. From there, any figure of the Analytics page can be seen for a single node, and the Rooms list filters by node.

## Small things you will use every day

A tool you open every morning has to be comfortable. These details work the same way on every page:

- **One time range for everything.** Pick it once and it follows you from page to page, in the time zone you choose.
- **What you see is in the URL.** Range, filters, sort order and page. Copy it to share exactly what you are looking at with a colleague, or bookmark the view you check every day.
- **Search that goes straight to the point.** An exact ID opens its room, participant, egress or ingress, however old it is.
- **Exports.** Every list downloads as CSV with the filters you applied, and in PRO a room exports its attendance: who was there and for how long.
- **Explanations where you need them.** An info icon next to each figure says what it counts.
- **Light and dark themes**, as you have seen in the screenshots if you switched the theme of this page 😉

## Your data, your retention

All this data is yours, so you decide how long it lives. Each class has its own retention, configured in `livekit.yaml`:

| Data | Kept by default |
| --- | --- |
| Events, statistics and closed tracks | 7 days |
| Closed rooms, participant sessions, egresses and ingresses | 90 days |
| Hourly rollups | 400 days |
| Daily rollups | Forever |

In practice: the fine detail of a call is there for a week, the list of what happened for three months, and the usage figures for as long as you want. The **Data** tab of Settings shows how much space each class takes and estimates how much it will take once it reaches its retention.

![Data tab of the Settings page, with the retention, documents and size of each class of analytics data](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/settings-data-light.png#only-light){ .round-corners loading=lazy }
![Data tab of the Settings page, with the retention, documents and size of each class of analytics data](/assets/images/blog/YYYY/MM/new-openvidu-dashboard/settings-data-dark.png#only-dark){ .round-corners loading=lazy }

Privacy is the default as well. Client IP addresses are anonymized unless you say otherwise, and credentials such as stream keys, storage keys or tokens in URLs are never stored. The [analytics settings](/docs/self-hosting/configuration/reference.md#analytics-settings) list every option.

## What you get in each edition

| | **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } | **PRO**{ .openvidu-tag .openvidu-pro-tag } |
| --- | :---: | :---: |
| Overview, live | :material-check: | :material-check: |
| Analytics of rooms, participants, clients, data, egress and ingress | :material-check: | :material-check: |
| Lists of rooms, participants, agents, egress and ingress | :material-check: | :material-check: |
| CSV and Excel exports | :material-check: | :material-check: |
| Quality, diagnostics and top rooms analytics | | :material-check: |
| Details of each room, participant, track, egress and ingress | | :material-check: |
| Media nodes and per-node figures | | :material-check: |

In OpenVidu COMMUNITY the PRO pages stay visible but locked, with a short explanation of what they show, so you can see what is there before deciding.

## Upgrading from a previous version

There is nothing to do by hand. The first time OpenVidu Server 3.10 starts on a deployment upgraded from a previous version, it migrates the analytics data you already had in the background, while new data is written as usual. The dashboard shows the progress of the migration until it finishes.

The [release notes](/docs/releases.md) have the details of the upgrade.

## Try it

The best way to judge a dashboard is with your own rooms in it. Deploy OpenVidu 3.10, or upgrade the deployment you already have, and open `https://your.domain/dashboard/`.

[Deploy OpenVidu :fontawesome-solid-arrow-right:](/docs/self-hosting/deployment-types.md){ .md-button .md-button--primary }

If you want the detail pages and the quality analytics, OpenVidu PRO has a [15-day free trial](/pricing.md#openvidu-pro). And the [dashboard documentation](/docs/self-hosting/production-ready/observability/openvidu-dashboard.md) describes every page in depth.

---

*A personal note to finish. This dashboard is my last contribution to OpenVidu: by the time you read this, I will have moved on to a new stage. It has been a pleasure to build this project with such a talented and generous team. I leave the dashboard in the best hands. Thank you all, and see you around!*

*Juan Carlos*
