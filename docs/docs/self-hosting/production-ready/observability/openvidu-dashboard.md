---
title: "OpenVidu Dashboard: live monitoring and usage analytics"
description: "Watch rooms, participants, tracks, egresses and ingresses live, and analyze the usage and quality of an OpenVidu deployment over time."
---

# OpenVidu Dashboard

OpenVidu Dashboard is a web application that gives **OpenVidu administrators** **real-time monitoring** and **usage analytics** of the **Rooms**, **Participants**, **Tracks**, **Egresses** and **Ingresses** of a deployment. It is included by default in any [OpenVidu deployment](../../deployment-types.md) and reads the analytics data that OpenVidu Server stores in MongoDB.

| | **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } | **PRO**{ .openvidu-tag .openvidu-pro-tag } |
| --- | :---: | :---: |
| [Overview](#overview) with live counters | :material-check: | :material-check: |
| [Analytics](#analytics) of rooms, participants, clients, bandwidth and egresses, with CSV export | :material-check: | :material-check: |
| Lists of [Rooms](#rooms), [Participants](#participants), [Egresses](#egress) and [Ingresses](#ingress) | :material-check: | :material-check: |
| Per-node breakdown in the Overview and Analytics | | :material-check: |
| Quality, failures, ingress and top rooms analytics | | :material-check: |
| Details of each Room, Participant, Track, Egress and Ingress | | :material-check: |
| [Agents](#agents) page | | :material-check: |

In OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }, the **PRO**{ .openvidu-tag .openvidu-pro-tag } views and cards are visible but locked, with a short explanation of what they show.

## Access

Go to `https://your.domain/dashboard/` and **log in** with the admin credentials of your deployment: `DASHBOARD_ADMIN_USERNAME` and `DASHBOARD_ADMIN_PASSWORD` in `openvidu.env`. A session lasts while it is used and expires after 7 days without use.

![OpenVidu Dashboard login page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/login-light.png#only-light){ .round-corners loading=lazy }
![OpenVidu Dashboard login page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/login-dark.png#only-dark){ .round-corners loading=lazy }

## Navigating the dashboard

Every page shares the same header and the same rules:

- **Time range**: the selector in the header applies to every page. It offers presets from the last hour to the last 90 days, the current month and a custom range, in the browser's time zone or in UTC.
- **Auto-refresh**: pages showing live data refresh every 10 seconds by default. You can choose another period or turn it off; refreshing pauses while the browser tab is hidden.
- **Search**: press `/` or click the search box. Typing an exact identifier (a Room, Participant, Track, Egress or Ingress SID) opens its details; any other text finds rooms, participants, egresses and ingresses whose name starts with it.
- **Shareable views**: the time range, filters, sort order and page of every list live in the URL. Copy the URL to share exactly what you see; the browser's **Back** button restores the previous view.
- **Identifiers** have a copy button, and every Room, Participant, Egress and Ingress links to its details.
- **Theme**: light and dark themes, following the operating system by default.
- **Version**: the bottom of the side menu shows the OpenVidu version and edition, with a link to this documentation.

![Search results grouped by resource in OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/search-light.png#only-light){ .round-corners loading=lazy }
![Search results grouped by resource in OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/search-dark.png#only-dark){ .round-corners loading=lazy }

## Overview

The landing page answers "what is happening right now":

- **Live counters** of active rooms, participants, publishers, services (egress, ingress and agent sessions), egresses, ingresses and agents, each linking to its list.
- **Today**: rooms, participants, minutes, egresses and ingresses since midnight.
- **Data pipeline**: time of the last data written by OpenVidu Server, how many nodes are reporting, and the progress of a [data migration](#upgrading-from-previous-versions) while it runs.
- **Recent rooms**: the last rooms created.
- **By node** **PRO**{ .openvidu-tag .openvidu-pro-tag }: version, region, state, rooms and participants of each node.

A warning appears when no analytics data has been written for a while, or when some entities have stopped receiving statistics.

![Overview page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/overview-light.png#only-light){ .round-corners loading=lazy }
![Overview page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/overview-dark.png#only-dark){ .round-corners loading=lazy }

## Analytics

Charts and figures over the selected time range, with a granularity from 5 minutes to 1 day (automatic by default). Every section exports its data as CSV.

- **Summary**: rooms created, participant sessions, unique identities, connection success rate, bandwidth, egresses and API error rate.
- **Rooms**: rooms created and ended, average room size and duration.
- **Participants**: participants joined and aborted, connection success rate and sessions by kind.
- **Clients**: SDK, operating system, browser and connection type of the participants.
- **Bandwidth**: upstream and downstream traffic.
- **Egress**: egresses started, ended and failed, by type.

**PRO**{ .openvidu-tag .openvidu-pro-tag } adds:

- **Quality**: the average quality score (MOS) over time, drawn over the Excellent, Good, Poor and Lost bands.
- **Failures**: disconnection reasons, room end reasons, subscription failures and API calls and errors by method.
- **Ingress**: ingress sessions and failures by input type.
- **Top rooms**: the rooms with most participants, longest duration, most bandwidth or worst quality.
- **Scope**: any of the above for the whole cluster or for a single node, chosen in the page header.

![Analytics page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics-light.png#only-light){ .round-corners loading=lazy }
![Analytics page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics-dark.png#only-dark){ .round-corners loading=lazy }

<div class="grid-container" markdown>

<div class="grid-50" markdown>
![Quality section of the Analytics page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics-quality-light.png#only-light){ .round-corners loading=lazy }
![Quality section of the Analytics page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics-quality-dark.png#only-dark){ .round-corners loading=lazy }
</div>

<div class="grid-50" markdown>
![Failures section of the Analytics page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics-failures-light.png#only-light){ .round-corners loading=lazy }
![Failures section of the Analytics page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics-failures-dark.png#only-dark){ .round-corners loading=lazy }
</div>

</div>

## Rooms

Active and closed rooms of the selected time range, with counters of active rooms, rooms in range, participant sessions and active participants. Filter by status, search by name prefix or SID, and filter the rooms that used egress, ingress or agents. The table shows each room's status, start and end time, duration, participants, bandwidth, features and node.

![Rooms page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/rooms-light.png#only-light){ .round-corners loading=lazy }
![Rooms page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/rooms-dark.png#only-dark){ .round-corners loading=lazy }

### Room details

!!! info "This view is part of OpenVidu [**PRO**{ .openvidu-tag .openvidu-pro-tag }](../../../../pricing.md#openvidu-pro) edition."

Everything about one room: duration, participants, connection success, bandwidth, egresses and quality; charts of active participants, bandwidth and quality with the room's events marked on them; its participants grouped by identity; its egresses and ingress sessions; the timeline of events, filterable by type, with the full content of each event; and its configuration. The page keeps refreshing while the room is active.

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

Search participant sessions by identity prefix or SID over the selected time range, and filter them by kind (standard participants by default, or agent, egress and ingress sessions), status and room. The table shows each session's room, kind, status, join and leave time, duration, client and connection type.

A participant may connect to a room several times with the same identity: each connection is a **participant session**, with its own SID. Participant counts across the dashboard include standard participants only; agent, egress and ingress sessions are counted apart as **services**.

![Participants page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/participants-light.png#only-light){ .round-corners loading=lazy }
![Participants page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/participants-dark.png#only-dark){ .round-corners loading=lazy }

### Participant details

!!! info "This view is part of OpenVidu [**PRO**{ .openvidu-tag .openvidu-pro-tag }](../../../../pricing.md#openvidu-pro) edition."

One participant session: quality, duration, bandwidth, connection time and reconnections; client (SDK, operating system, browser, device, network) and connection details; charts of quality, bitrate, round-trip time, jitter and packet loss; the tracks it published and subscribed to; the other sessions of the same identity; and the timeline of its events.

Selecting a published track opens the **track panel**: source, codec, dimensions and simulcast layers, publish statistics per layer, subscribers, and charts of bandwidth, loss, jitter, round-trip time and quality of that track.

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

!!! info "This view is part of OpenVidu [**PRO**{ .openvidu-tag .openvidu-pro-tag }](../../../../pricing.md#openvidu-pro) edition."

The sessions of [agent](../../../ai/openvidu-agents/overview.md) participants in the selected time range, with their status, room, duration, SDK and node, and a live counter of the agents connected now. In **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }, the agents counter of the Overview and the agent filters of the Rooms and Participants pages are available.

![Agents page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/agents-light.png#only-light){ .round-corners loading=lazy }
![Agents page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/agents-dark.png#only-dark){ .round-corners loading=lazy }

## Egress

Egresses of the selected time range, with counters of active, started and failed egresses and the time recorded. Filter by status, type and room, or search by ID. The table shows each egress's room, type, status, start time, duration and outputs, and flags the failed ones.

![Egress page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/egress-light.png#only-light){ .round-corners loading=lazy }
![Egress page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/egress-dark.png#only-dark){ .round-corners loading=lazy }

### Egress details

!!! info "This view is part of OpenVidu [**PRO**{ .openvidu-tag .openvidu-pro-tag }](../../../../pricing.md#openvidu-pro) edition."

One egress: the participant it records, if any; its error, if any; its outputs (files, streams, segments or images) with their location and size; the timeline of its status changes; a summary of the request that started it (layout, preset, recorded tracks...) followed by the full request; and its events. Credentials in URLs and storage settings are never shown.

![Egress details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/egress-detail-light.png#only-light){ .round-corners loading=lazy }
![Egress details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/egress-detail-dark.png#only-dark){ .round-corners loading=lazy }

## Ingress

Ingresses with activity in the selected time range, with their counters. Filter by status and input type (RTMP, WHIP or URL), or search by name or ID. The table shows each ingress's input type, room, status, number of sessions, total duration, creation time and last session.

![Ingress page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/ingress-light.png#only-light){ .round-corners loading=lazy }
![Ingress page of OpenVidu Dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/ingress-dark.png#only-dark){ .round-corners loading=lazy }

### Ingress details

!!! info "This view is part of OpenVidu [**PRO**{ .openvidu-tag .openvidu-pro-tag }](../../../../pricing.md#openvidu-pro) edition."

One ingress: its last error, its definition, each of its sessions with the participant it published as, its room and its video and audio details, and its events. An RTSP camera pulled by a URL ingress reads **URL (RTSP)**. Stream keys and credentials in URLs are never shown.

![Ingress details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/ingress-detail-light.png#only-light){ .round-corners loading=lazy }
![Ingress details page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/ingress-detail-dark.png#only-dark){ .round-corners loading=lazy }

## Settings

- **Preferences**: theme, time zone, default time range, rows per page and auto-refresh period. They are stored in the browser.
- **About**: the OpenVidu version and edition, the progress of a data migration while it runs, the retention in effect and the storage used by each collection.

![About tab of the Settings page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/settings-about-light.png#only-light){ .round-corners loading=lazy }
![About tab of the Settings page](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/settings-about-dark.png#only-dark){ .round-corners loading=lazy }

## Analytics data

OpenVidu Server writes the analytics data the dashboard shows to MongoDB, in its `openvidu` database:

- **Rooms, participant sessions, tracks, subscriptions, egresses, ingresses and ingress sessions**, updated as their events arrive.
- **Events** as emitted by OpenVidu Server, for the timelines.
- **Statistics** every 30 seconds: quality score, bytes, packets, loss, jitter and round-trip time. OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } stores them per participant and direction; OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag } stores them per track, which the track panel needs.
- **Rollups** every 5 minutes, hour and day, which the Analytics page and the Overview read.

Credentials such as TURN passwords, storage keys, stream keys or tokens in URLs are never stored. Client IP addresses are stored unless `anonymize_ip` is enabled, and room and participant metadata only when `store_metadata` is enabled.

When the end of a room, participant session, egress or ingress session never arrives (for example, because a node crashed), OpenVidu Server closes it within about two minutes with an estimated end time. The dashboard marks these entities as closed by the server.

### Retention

Each class of data is kept for its own time, after which MongoDB deletes it:

| Data | Default | `livekit.yaml` key |
| --- | --- | --- |
| Events | 7 days | `openvidu.analytics.retention.events` |
| Statistics and 5-minute rollups | 7 days | `openvidu.analytics.retention.stats` |
| Closed tracks and subscriptions | 7 days | `openvidu.analytics.retention.tracks` |
| Closed rooms, participant sessions, egresses and ingresses | 90 days | `openvidu.analytics.retention.entities` |
| Hourly rollups | 400 days | `openvidu.analytics.retention.rollups_hourly` |
| Daily rollups | Forever | |

The details of a room or participant show charts and tracks only while their statistics and tracks are retained; the Analytics page keeps showing their figures from the rollups. See [Analytics settings](../../configuration/reference.md#analytics-settings) for these and the other `openvidu.analytics` keys, and [Changing configuration](../../configuration/changing-config.md) to apply them.

## Upgrading from previous versions

- **Data migration**: the first start of OpenVidu Server after the upgrade migrates the existing analytics data in the background, while live data is written as usual. The dashboard shows its progress in a banner, in the Overview and in Settings. The previous `events` collection is renamed `legacy_events` and kept until its data expires.
- **Retention**: `openvidu.analytics.expiration` is deprecated. If it is still set and no `retention` key is, it sets the retention of events and statistics; replace it with the `retention` keys above.
- **Credentials**: the dashboard no longer starts without `ADMIN_USERNAME` and `ADMIN_PASSWORD` in its environment, which every OpenVidu installation already sets from `openvidu.env`.
- **Containers**: the dashboard runs as the user with uid 1000. Configuration, license or certificate files mounted into its container must be readable by that user.

## Advanced configuration

The dashboard container reads its environment from `dashboard.env` in the configuration directory of the deployment (see [Changing configuration](../../configuration/changing-config.md)). These variables are optional:

| Variable | Default | Description |
| --- | --- | --- |
| `LOG_LEVEL` | `info` | `error`, `warn`, `info`, `http`, `verbose` or `debug`. |
| `DATABASE_TLS_CA_FILE` | | Path, inside the container, to the PEM file of a private certificate authority for the MongoDB connection. It enables TLS. |
| `DASHBOARD_JWT_SECRET` | Generated once and stored in MongoDB | Key that signs the session tokens, at least 32 bytes. Set the same value in every dashboard of a cluster to share sessions without MongoDB. |
| `DASHBOARD_REFRESH_TOKEN_TTL` | `604800` | Seconds a session lasts without use. |
| `DASHBOARD_COOKIE_SECURE` | `auto` | Whether the session cookie requires HTTPS: `auto` (when the request is HTTPS), `true` or `false`. |
| `DASHBOARD_TRUST_PROXY` | Private networks | Proxies whose `X-Forwarded-*` headers are trusted: `false`, a number of hops, or a comma-separated list of addresses and CIDR ranges. |
| `DASHBOARD_LIST_TOTAL_MAX_RANGE` | `7d` | Longest time range for which lists count their total number of items. |
