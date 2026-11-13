---
title: "OpenVidu Dashboard: live monitoring and usage analytics"
description: "Watch rooms, participants, tracks, egresses and ingresses live, and analyze the usage and quality of an OpenVidu deployment over time."
---

# OpenVidu Dashboard

OpenVidu Dashboard is a web application for the **administrators** of an OpenVidu deployment. It answers two kinds of questions: what is happening **right now** (which rooms are open, who is connected, which recordings are running) and what happened **over time** (how much the deployment is used, how well calls went, what failed and why). It is included by default in any [OpenVidu deployment](../../deployment-types.md) and reads the [analytics data](#analytics-data) that OpenVidu Server stores in MongoDB.

| | **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } | **PRO**{ .openvidu-tag .openvidu-pro-tag } |
| --- | :---: | :---: |
| [Overview](#overview) of the deployment, live | :material-check: | :material-check: |
| [Analytics](#analytics) of rooms, participants, clients, data transferred, egress and ingress | :material-check: | :material-check: |
| Lists of [Rooms](#rooms), [Participants](#participants), [Agents](#agents), [Egress](#egress) and [Ingress](#ingress) | :material-check: | :material-check: |
| [Exports](#exporting-data) of every list (CSV) and every Analytics section (Excel) | :material-check: | :material-check: |
| Quality, diagnostics and top rooms analytics | | :material-check: |
| Details of each Room, Participant, Track, Egress and Ingress | | :material-check: |
| [Media nodes](#media-nodes) and per-node figures in Elastic and High Availability deployments | | :material-check: |

In OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }, the **PRO**{ .openvidu-tag .openvidu-pro-tag } pages and cards stay visible but locked, with a short explanation of what they show.

## Access

Go to `https://your.domain/dashboard/` and **log in** with the admin credentials of your deployment: `DASHBOARD_ADMIN_USERNAME` and `DASHBOARD_ADMIN_PASSWORD` in `openvidu.env`. A session lasts while it is used and expires after 7 days without use.

![OpenVidu Dashboard login page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/login-light.png#only-light){ .round-corners loading=lazy }
![OpenVidu Dashboard login page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/login-dark.png#only-dark){ .round-corners loading=lazy }

## Finding your way around

The side menu holds one entry per page, and the header holds the controls that every page shares. They all work the same way everywhere, so what you learn on one page applies to the rest.

**The time range drives every list and chart.** Pick it once in the header (a preset from the last hour to the last 90 days, the current month, or a custom range) and it follows you from page to page. The same picker chooses the time zone in which every time is shown: the browser's, UTC or any other. When the range starts before the data of a page is [retained](#retention), the picker says so.

**Live pages refresh on their own**, every 10 seconds by default. The control next to the range picker changes the interval or turns it off, and refreshing pauses while the browser tab is hidden. The label next to the title of a live page tells you how far to trust what you see: **LIVE** while data keeps arriving, **paused** while auto-refresh is off, and **stale** when OpenVidu Server has stopped writing data. If no analytics data arrives for over a minute, a banner says so on every page, whatever the auto-refresh setting.

**Search takes you straight to an entity.** Press `/` or click the search box in the header and type a name, an identity or an identifier. An exact identifier (the SID of a Room, Participant or Track, or the ID of an Egress or Ingress) opens that entity whatever its age; any other text lists the rooms, participants, egresses and ingresses whose name starts with it. Every list also has its own search box, which follows the same rule.

**What you see is in the URL.** The time range, time zone, filters, sort order and page of every view are part of its address. Copy the URL to share exactly what you are looking at with a colleague, bookmark a view you check often (a preset such as "last 24 hours" stays relative), and use the browser's **Back** button to return to a list as you left it.

A few details are common to every page:

- An :material-information-outline: icon next to a figure, chart or column explains what it counts. Hover it, focus it with the keyboard or tap it.
- Identifiers have a copy button, and every Room, Participant, Egress and Ingress links to its details.
- Tables let you choose their columns, and several of them can be sorted by duration, end time or other figures. Sorting by those figures is offered for ranges of up to 7 days (24 hours for participant sessions).
- The theme is light or dark, following the operating system by default.
- The bottom of the side menu shows the OpenVidu version and edition, with a link to this documentation.

![Search results grouped by resource in OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/search-light.png#only-light){ .round-corners loading=lazy }
![Search results grouped by resource in OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/search-dark.png#only-dark){ .round-corners loading=lazy }

## Overview

The landing page answers "what is happening right now?" at a glance, and it is the place to start when something looks wrong.

The counters at the top show the **active rooms**, the **participants** connected, how many of them are **publishers**, and the **egresses**, **ingresses** and **agents** running at this moment. Each counter opens its list already filtered to what is live. Below them, **Today** sums up the day so far: rooms, participant sessions, minutes, egresses and ingresses since midnight in your time zone.

The **Data pipeline** card tells you whether the dashboard itself can be trusted: it shows when OpenVidu Server last wrote analytics data, or when it stopped, and the progress of a data migration while one runs. If some active rooms or participants have stopped sending statistics, a notice under the counters says how many, because they may no longer be there.

**Recent rooms** lists the last rooms created, with links to the active ones and to the whole list. In Elastic and High Availability deployments, the **By node** table shows the state of each [media node](#media-nodes).

![Overview page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/overview-light.png#only-light){ .round-corners loading=lazy }
![Overview page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/overview-dark.png#only-dark){ .round-corners loading=lazy }

## Analytics

The Analytics page shows how the deployment is used over the selected time range. Use it to follow growth, to size your infrastructure against the busiest moments, and to compare one period with another. Charts are drawn in buckets from 5 minutes to 1 day; the granularity is chosen for you from the range, and you can change it. This page does not refresh on its own: it loads when you open it and when you press the refresh button.

A row of figures summarizes the range: rooms created, participant sessions, unique identities, data transferred, connection success, egresses and ingresses. Below it, each section looks at one subject:

- **Rooms**: the most rooms open at once and the rooms created over time, their average size and duration, and three views of the rooms that ended in the range. **Room topology** classifies them by their shape, from how many participants were connected at once and how many of them were sending audio or video: 1:1 calls, 1:N sessions with a single sender (a webinar, a class), N:M sessions with several senders (a meeting), and rooms that stayed empty, had a single participant or had nobody publishing. **Room size** groups them by the most participants connected at once, and **Recorded rooms** tells which share of them was recorded.
- **Participants**: the most participants connected at once, participant sessions over time, unique identities per day, sessions by kind, and the share of sessions that managed to connect.
- **Client breakdowns**: the SDK, operating system, browser and connection type of the participants.
- **Data transferred**: the data sent to the server and from the server to the participants.
- **Egress** and **Ingress**: how many ran at once, how many started, how the egresses ended (completed, failed, aborted) and their types.

A participant may join a room several times with the same identity. Each connection is a **participant session**, and **unique identities** counts the distinct identities among them. All these figures count regular participants only: the egress, ingress and agent sessions that join rooms as participants are counted apart, as **services**.

![Analytics page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics-light.png#only-light){ .round-corners loading=lazy }
![Analytics page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics-dark.png#only-dark){ .round-corners loading=lazy }

OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag } adds three sections:

- **Quality**: the average quality score (MOS) over time, drawn over the Excellent, Good, Poor and Lost bands, with the number of poor and lost samples. A drop here is the cue to look at the rooms of that moment.
- **Diagnostics**: why participants disconnected, why rooms ended, failed subscriptions over time, and the API calls and errors of each method. It tells apart a network problem of your users from a problem in your application.
- **Top rooms**: the rooms of the range with most unique identities, longest duration, most data transferred or worst quality, each linking to its details.

<div class="grid-container" markdown>

<div class="grid-50" markdown>
![Quality section of the Analytics page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics-quality-light.png#only-light){ .round-corners loading=lazy }
![Quality section of the Analytics page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics-quality-dark.png#only-dark){ .round-corners loading=lazy }
</div>

<div class="grid-50" markdown>
![Diagnostics section of the Analytics page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics-diagnostics-light.png#only-light){ .round-corners loading=lazy }
![Diagnostics section of the Analytics page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics-diagnostics-dark.png#only-dark){ .round-corners loading=lazy }
</div>

</div>

## Rooms

The Rooms page lists the rooms that started in the selected time range, active and closed, and refreshes live. The figures above the table say how many rooms and participants are active now, and how many rooms and participant sessions the range holds.

Filter the list by status, search a room by the start of its name or by its SID, and keep only the rooms that used egress, ingress or agents. Each row shows the room's status, start and end, duration, unique identities, active participants, data transferred and the services it used. Sort by start, end, duration, unique identities or active participants to find, for example, the longest or the busiest rooms of the week.

![Rooms page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/rooms-light.png#only-light){ .round-corners loading=lazy }
![Rooms page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/rooms-dark.png#only-dark){ .round-corners loading=lazy }

### Room details

!!! info "This view is part of OpenVidu [**PRO**{ .openvidu-tag .openvidu-pro-tag }](../../../../pricing.md#openvidu-pro) edition."

The page of a room tells its whole story. The header shows its status, its topology (1:1, 1:N, N:M...), whether it was recorded, and when and why it ended. The figures below sum it up: duration, participants (with the most connected at once), unique identities, data transferred, connection success, average quality and services.

Three charts cover the life of the room: **active participants**, **bitrate** and **quality**. Joins, leaves, aborted connections and the start and end of each egress are marked on them, so you can relate a drop in quality or bitrate to what was happening in the room at that moment.

The rest of the page lists what took part in the room: its **participants** grouped by identity, its **egresses** and **ingress sessions**, the **timeline of events** (filterable by type and by participant, each event with its full content) and its configuration and metadata. The page keeps refreshing while the room is active.

<div class="grid-container" markdown>

<div class="grid-50" markdown>
![Room details page with charts](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/room-light.png#only-light){ .round-corners loading=lazy }
![Room details page with charts](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/room-dark.png#only-dark){ .round-corners loading=lazy }
</div>

<div class="grid-50" markdown>
![Events timeline of the room details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/room-timeline-light.png#only-light){ .round-corners loading=lazy }
![Events timeline of the room details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/room-timeline-dark.png#only-dark){ .round-corners loading=lazy }
</div>

</div>

## Participants

The Participants page lists participant sessions over the selected time range. Search by the start of an identity or by SID, and filter by kind (regular participants by default, or agent, egress and ingress sessions), by status, by room, or keep only the publishers. Each row shows the session's room, kind, status, join and leave times, duration and what it published (camera, microphone, screen).

The figures above the table show the participants active now, the services active now and the sessions of the range.

![Participants page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/participants-light.png#only-light){ .round-corners loading=lazy }
![Participants page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/participants-dark.png#only-dark){ .round-corners loading=lazy }

### Participant details

!!! info "This view is part of OpenVidu [**PRO**{ .openvidu-tag .openvidu-pro-tag }](../../../../pricing.md#openvidu-pro) edition."

The page of a participant session shows what that person experienced. The figures give its duration, data transferred, quality and how many times the connection had to be resumed. Two cards describe the **client** (SDK, operating system, browser, device, network) and the **connection** (type, time to connect and, once it ended, the reason of the disconnection).

The charts follow the session over time: **quality**, **bitrate**, **round-trip time**, **jitter** and **packets lost**. Below them are the **tracks it published** and the **tracks it subscribed to**, the other sessions of the same identity (in this room or in any room), and the timeline of its events.

Selecting a published track opens the **track panel**: its source, codec, resolution and simulcast layers, the statistics of each layer, its subscribers, and charts of bitrate, loss, jitter, round-trip time and quality of that track alone.

<div class="grid-container" markdown>

<div class="grid-50" markdown>
![Participant details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/participant-light.png#only-light){ .round-corners loading=lazy }
![Participant details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/participant-dark.png#only-dark){ .round-corners loading=lazy }
</div>

<div class="grid-50" markdown>
![Track panel of the participant details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/participant-track-light.png#only-light){ .round-corners loading=lazy }
![Track panel of the participant details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/participant-track-dark.png#only-dark){ .round-corners loading=lazy }
</div>

</div>

## Agents

The Agents page lists the sessions of [agent](../../../ai/openvidu-agents/overview.md) participants in the selected time range, with their room, status and duration, a live counter of the agents connected now and the number of agent sessions in the range. Agents join rooms as participants of kind Agent, so their sessions also appear in the Participants page when filtering by that kind.

![Agents page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/agents-light.png#only-light){ .round-corners loading=lazy }
![Agents page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/agents-dark.png#only-dark){ .round-corners loading=lazy }

## Egress

The Egress page lists the egresses started in the selected time range and refreshes live, so it is the place to follow a recording or a stream while it runs. The figures above the table show the egresses active now, those started and failed in the range, and the total duration.

Search by the start of a room name or by egress ID, and filter by type (room composite, web, participant, track composite or track) and by status. Each row shows the egress's room, type, status, start, end, duration and outputs, and failed egresses are flagged. Sort by end time or duration to find the longest ones.

![Egress page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/egress-light.png#only-light){ .round-corners loading=lazy }
![Egress page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/egress-dark.png#only-dark){ .round-corners loading=lazy }

### Egress details

!!! info "This view is part of OpenVidu [**PRO**{ .openvidu-tag .openvidu-pro-tag }](../../../../pricing.md#openvidu-pro) edition."

The page of an egress shows, while it runs and after it ends: its error, if any, with an explanation when the egress was lost with its node; its **outputs** (files, streams, segments or images) with their location, duration and size; the **timeline of its status changes**; a summary of the **request** that started it (layout, preset, recorded participant and tracks...), with the full request available on demand; and its events. Credentials in URLs and storage settings are never shown.

![Egress details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/egress-detail-light.png#only-light){ .round-corners loading=lazy }
![Egress details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/egress-detail-dark.png#only-dark){ .round-corners loading=lazy }

## Ingress

The Ingress page lists the ingresses with activity in the selected time range: those created in it, those that streamed in it, and those publishing now. An ingress is a reusable input, and each stream published to it is one **session**. The figures above the table show the ingresses publishing now, the ingresses and sessions of the range and their total duration.

Search by the start of a name or by ID, and filter by input type (RTMP, WHIP or URL) and status. Each row shows the ingress's input type, room, status, creation time, total duration, number of sessions and last session.

![Ingress page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/ingress-light.png#only-light){ .round-corners loading=lazy }
![Ingress page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/ingress-dark.png#only-dark){ .round-corners loading=lazy }

### Ingress details

!!! info "This view is part of OpenVidu [**PRO**{ .openvidu-tag .openvidu-pro-tag }](../../../../pricing.md#openvidu-pro) edition."

The page of an ingress shows its last error, if any; its definition; and each of its **sessions**, with the participant it published as, its room, its video and audio details and its error. An RTSP camera pulled by a URL ingress reads **URL (RTSP)**. Stream keys and credentials in URLs are never shown.

![Ingress details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/ingress-detail-light.png#only-light){ .round-corners loading=lazy }
![Ingress details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/ingress-detail-dark.png#only-dark){ .round-corners loading=lazy }

## Media nodes

!!! info "These views are part of OpenVidu [**PRO**{ .openvidu-tag .openvidu-pro-tag }](../../../../pricing.md#openvidu-pro) edition, in [Elastic](../../deployment-types.md#openvidu-elastic) and [High Availability](../../deployment-types.md#openvidu-high-availability) deployments."

In deployments with several media nodes, the dashboard tells you what each of them is doing and lets you look at any figure for one node alone. A media node is named after its private IP address (`media-node-10-0-0-1`) and keeps that name when its OpenVidu Server restarts.

The **Media nodes** page lists every media node with its IP, RTC engine, version, state, active rooms and participants, and how many times its server restarted. A node is **alive** while its analytics data keeps arriving, **draining** while it waits for its rooms to end before it stops, **not reporting** when its data stopped arriving without a clean stop, and **stopped** once it was shut down. The figures above the table tell how many nodes are reporting and how many rooms OpenVidu Server had to close itself because their node disappeared, which points to crashes.

The page of a media node shows its recent activity (rooms, participant sessions, minutes, data transferred and connection success), the rooms it hosts or hosted, and the history of its servers: when each one started and stopped, and whether it stopped cleanly.

<div class="grid-container" markdown>

<div class="grid-50" markdown>
![Media nodes page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/media-nodes-light.png#only-light){ .round-corners loading=lazy }
![Media nodes page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/media-nodes-dark.png#only-dark){ .round-corners loading=lazy }
</div>

<div class="grid-50" markdown>
![Media node details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/media-node-light.png#only-light){ .round-corners loading=lazy }
![Media node details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/media-node-dark.png#only-dark){ .round-corners loading=lazy }
</div>

</div>

The rest of the dashboard follows the media nodes too:

- The Overview shows the **By node** table, with the state of each media node.
- The Analytics page has a **Scope** selector, to see every section for all nodes or for a single one. Egress and ingress are counted for the whole deployment only.
- The Rooms page has a **Node** filter and column, and the details of rooms and participants name their media node. Every media node name links to its page.

## Exporting data

Every list and every Analytics section can be taken out of the dashboard, to work on it in a spreadsheet or to feed a report:

- **Export CSV**, in the toolbar of each list (Rooms, Participants, Agents, Egress and Ingress), downloads what the list shows: the same time range, search, filters and sort order, across all its pages and not only the one on screen. An export holds up to 10,000 rows; when the list has more, the dashboard says so and you can narrow the range or the filters to export the rest.
- **Export XLSX**, in the header of each Analytics section, saves an Excel workbook with the data of its charts: one sheet per time resolution, one per breakdown, and an Info sheet with the range, time zone and scope of the export.
- In OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }, the Participants section of a [room's page](#room-details) exports its **attendance** as CSV: one row per identity, with the total time it spent in the room.

!!! warning
    An exported file is no longer protected by the login of the dashboard. It may hold participant identities and names, so share it with the same care as the dashboard's credentials.

## Common tasks

### Investigating a room with problems

!!! info "This workflow uses views of OpenVidu [**PRO**{ .openvidu-tag .openvidu-pro-tag }](../../../../pricing.md#openvidu-pro) edition."

1. Find the room: type its name or SID in the search box, or open the Rooms page and filter the time range in which the problem happened.
2. In the room's page, look at the **Quality** and **Bitrate** charts around the time of the problem. The markers show who joined or left and which egress started at that moment.
3. In the **Participants** section, the Quality column points at the sessions that went worst. Open the one that had the problem.
4. The participant's page tells whether the cause was on their side: the client and network they used, the connection type, how many times the connection was resumed, and the packet loss, jitter and round-trip time over time.
5. If only one track was affected, open it from **Published tracks** to see its layers and the statistics of each of its subscribers.
6. The **events timeline** of the room or the participant gives the exact sequence: connection aborted, track unpublished, disconnect reason.

### Following an egress

1. Open the Egress page. An egress that has just been requested appears within seconds, and its status changes as it progresses.
2. Filter by room or search the room's name to see every egress of a session, or filter by the **Failed** status to review what went wrong in the range.
3. In OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }, open the egress to see where its outputs were stored and their size, the time of each status change and, if it failed, its error.

### Comparing two periods

1. Open the Analytics page and select the first period with the range picker.
2. Copy the URL, or export the sections you are interested in.
3. Select the second period. With both URLs open in two browser tabs you can compare them side by side, and with the exported workbooks you can chart them together.

## Deployments using mediasoup

OpenVidu Server reports no media statistics when it runs with the [mediasoup](../performance.md#limitations) RTC engine: there are no figures of data transferred, bitrate or quality for the rooms and participants of those media nodes. Everything else (rooms, participants, tracks, events, egresses and ingresses) is reported as with Pion.

The dashboard keeps those figures and charts in place and marks them with a :material-alert-outline: icon that explains why they are empty, dimming them when there is no data at all. On the Analytics page and on the page of a media node, the icon tells whether none or only some of the servers of the range reported media statistics. In the Media nodes page, the **RTC engine** column tells which engine each media node runs.

## Settings

- **Preferences**: theme, default time zone, default time range, rows per page and auto-refresh interval. They are stored in the browser.
- **About**: the OpenVidu version and edition, the progress of a data migration while it runs, the retention in effect for each class of data and the storage each collection uses.

![About tab of the Settings page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/settings-about-light.png#only-light){ .round-corners loading=lazy }
![About tab of the Settings page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/settings-about-dark.png#only-dark){ .round-corners loading=lazy }

## Analytics data

OpenVidu Server writes the analytics data the dashboard shows to MongoDB, in its `openvidu` database:

- **Rooms, participant sessions, tracks, subscriptions, egresses, ingresses and ingress sessions**, updated as their events arrive.
- **Events** as emitted by OpenVidu Server, for the timelines.
- **Statistics** every 30 seconds: quality score, bytes, packets, loss, jitter and round-trip time. OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } stores them per participant and direction; OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag } stores them per track, which the track panel needs.
- **Rollups** every 5 minutes, hour and day, which the Analytics page and the Overview read.

Credentials such as TURN passwords, storage keys, stream keys or tokens in URLs are never stored. Client IP addresses are stored only when `anonymize_ip` is set to `false`, and room and participant metadata only when `store_metadata` is enabled.

When the end of a room, participant session, egress or ingress session never arrives (for example, because a node crashed), OpenVidu Server closes it itself with an estimated end time: participants within about two minutes, and rooms once the cluster has given up on their node. The dashboard marks these entities as estimated.

The first start of OpenVidu Server 3.10 or later on a deployment upgraded from a previous version migrates its analytics data in the background, while new data is written as usual. The dashboard shows the progress of the migration in a banner, in the Overview and in Settings.

### Retention

Each class of data is kept for its own time, after which MongoDB deletes it:

| Data | Default | `livekit.yaml` key |
| --- | --- | --- |
| Events | 7 days | `openvidu.analytics.retention.events` |
| Statistics | 7 days | `openvidu.analytics.retention.stats` |
| Closed tracks and subscriptions | 7 days | `openvidu.analytics.retention.tracks` |
| Closed rooms, participant sessions, egresses and ingresses | 90 days | `openvidu.analytics.retention.entities` |
| 5-minute rollups | 7 days | `openvidu.analytics.retention.rollups_5min` |
| Hourly rollups | 400 days | `openvidu.analytics.retention.rollups_hourly` |
| Daily rollups | Forever | `openvidu.analytics.retention.rollups_daily` |

The details of a room or participant show their charts, events and tracks only while that data is retained, and say so when it is not; the Analytics page keeps showing the figures of that time from the rollups.

## Configuration

- The analytics data (retention, stored detail, privacy options) is configured in the `openvidu.analytics` section of `livekit.yaml`: see [Analytics settings](../../configuration/reference.md#analytics-settings).
- The dashboard service has its own optional settings in `dashboard.env`: see [`dashboard.env`](../../configuration/reference.md#dashboardenv).

[Changing configuration](../../configuration/changing-config.md) explains where these files are and how to apply a change.
