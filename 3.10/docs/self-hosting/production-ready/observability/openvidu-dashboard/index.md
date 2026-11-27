# OpenVidu Dashboard

OpenVidu Dashboard is a web application for the **administrators** of an OpenVidu deployment. It answers two kinds of questions: what is happening **right now** (which rooms are open, who is connected, which recordings are running) and what happened **over time** (how much the deployment is used, how well calls went, what failed and why). It is included by default in any [OpenVidu deployment](https://openvidu.io/3.10/docs/self-hosting/deployment-types/index.md) and reads the [analytics data](#analytics-data) that OpenVidu Server stores in MongoDB.

|                                                                                                                       | **COMMUNITY** | **PRO** |
| --------------------------------------------------------------------------------------------------------------------- | ------------- | ------- |
| [Overview](#overview) of the deployment, live                                                                         |               |         |
| [Analytics](#analytics) of rooms, participants, clients, data transferred, egress and ingress                         |               |         |
| Lists of [Rooms](#rooms), [Participants](#participants), [Agents](#agents), [Egress](#egress) and [Ingress](#ingress) |               |         |
| [Exports](#exporting-data) of every list (CSV) and every Analytics section (Excel)                                    |               |         |
| Quality, diagnostics and top rooms analytics                                                                          |               |         |
| Details of each Room, Participant, Track, Egress and Ingress                                                          |               |         |
| [Media nodes](#media-nodes) and per-node figures in Elastic and High Availability deployments                         |               |         |

In OpenVidu **COMMUNITY**, the **PRO** pages and cards stay visible but locked, with a short explanation of what they show.

## Access

Go to `https://your.domain/dashboard/` and **log in** with the admin credentials of your deployment: `DASHBOARD_ADMIN_USERNAME` and `DASHBOARD_ADMIN_PASSWORD` in `openvidu.env`. A session lasts while it is used and expires after 7 days without use. That time, the log level and the other optional settings of the dashboard service are in [`dashboard.env`](https://openvidu.io/3.10/docs/self-hosting/configuration/reference/#dashboardenv).

## Finding your way around

The side menu holds one entry per page, and the header holds the controls that every page shares. They all work the same way everywhere, so what you learn on one page applies to the rest.

**The time range drives every list and chart.** Pick it once in the header (a preset from the last hour to the last 90 days, the current month, or a custom range) and it follows you from page to page. The same picker chooses the time zone in which every time is shown: the browser's, UTC or any other. When the range starts before the data of a page is [retained](#retention), the picker says so.

**Live pages refresh on their own**, every 10 seconds by default. The control next to the range picker changes the interval or turns it off, and refreshing pauses while the browser tab is hidden. The label next to the title of a live page tells you how far to trust what you see: **LIVE** while data keeps arriving, **paused** while auto-refresh is off, and **stale** when OpenVidu Server has stopped writing data. If no analytics data arrives for over a minute, a banner says so on every page, whatever the auto-refresh setting.

**Search takes you straight to an entity.** Press `/` or click the search box in the header and type a name, an identity or an identifier. An exact identifier (the SID of a Room, Participant or Track, or the ID of an Egress or Ingress) opens that entity whatever its age, and any other text lists the rooms, participants, egresses and ingresses whose name starts with it. Every list also has its own search box, which follows the same rule.

**What you see is in the URL.** The time range, time zone, filters, sort order and page of every view are part of its address. Copy the URL to share exactly what you are looking at with a colleague, bookmark a view you check often (a preset such as "last 24 hours" stays relative), and use the browser's **Back** button to return to a list as you left it.

A few details are common to every page:

- An icon next to a figure, chart or column explains what it counts. Hover it, focus it with the keyboard or tap it.
- Identifiers have a copy button, and every Room, Participant, Egress, Ingress and [media node](#media-nodes) links to its details.
- Tables let you choose their columns, and several of them can be sorted by duration, end time or other figures. Sorting by those figures is offered for ranges of up to 7 days (24 hours for participant sessions).
- The theme is light or dark, following the operating system by default.
- The bottom of the side menu shows the OpenVidu version and edition, with a link to this documentation.

## Overview

The landing page answers "what is happening right now?" at a glance, and it is the place to start when something looks wrong.

The counters at the top show the **active rooms**, the **participants** connected, how many of them are **publishers**, and the **egresses**, **ingresses** and **agents** running at this moment. Each counter opens its list already filtered to what is live. Below them, **Today** sums up the day so far: rooms, participant sessions, minutes, egresses and ingresses since midnight in your time zone.

The **Data pipeline** card tells you whether the dashboard itself can be trusted: it shows when OpenVidu Server last wrote analytics data, or when it stopped, and the progress of a data migration while one runs. If some active rooms or participants have stopped sending statistics, a notice under the counters says how many, because they may no longer be there.

**Recent rooms** lists the last rooms created, with links to the active ones and to the whole list. In Elastic and High Availability deployments, the **By node** table shows the state of each [media node](#media-nodes).

## Analytics

The Analytics page shows how the deployment is used over the selected time range. Use it to follow growth, to size your infrastructure against the busiest moments, and to compare one period with another. Charts are drawn in buckets from 5 minutes to 1 day. The dashboard chooses the granularity from the range, and you can change it. This page does not refresh on its own: it loads when you open it and when you press the refresh button.

A row of figures summarizes the range: rooms created, participant sessions, unique identities, data transferred, connection success, egresses and ingresses. Below it, each section looks at one subject:

- **Rooms**: the most rooms open at once and the rooms created over time, their average size and duration, and three views of the rooms that ended in the range. **Room topology** classifies them by their shape, from how many participants were connected at once and how many of them were sending audio or video: 1:1 calls, 1:N sessions with a single sender (a webinar, a class), N:M sessions with several senders (a meeting), and rooms that stayed empty, had a single participant or had nobody publishing. **Room size** groups them by the most participants connected at once, and **Recorded rooms** tells which share of them was recorded.
- **Participants**: the most participants connected at once, participant sessions over time, unique identities per day, sessions by kind, and the share of sessions that managed to connect.
- **Client breakdowns**: the SDK, operating system, browser and connection type of the participants.
- **Data transferred**: the data sent to the server and from the server to the participants.
- **Egress** and **Ingress**: how many ran at once, how many started, how the egresses ended (completed, failed, aborted) and their types.

A participant may join a room several times with the same identity. Each connection is a **participant session**, and **unique identities** counts the distinct identities among them. All these figures count regular participants only: the egress, ingress and agent sessions that join rooms as participants are counted apart, as **services**.

OpenVidu **PRO** adds three sections:

- **Quality**: the average quality score (MOS) over time, drawn over the Excellent, Good, Poor and Lost bands, with the number of poor and lost samples. A drop here is the cue to look at the rooms of that moment.
- **Diagnostics**: why participants disconnected, why rooms ended, failed subscriptions over time, and the API calls and errors of each method. It tells apart a network problem of your users from a problem in your application.
- **Top rooms**: the rooms of the range with most unique identities, longest duration, most data transferred or worst quality, each linking to its details.

In Elastic and High Availability deployments, it also adds a **Scope** selector to the header, to see every section for all nodes or for a single [media node](#media-nodes). Egress and ingress are always counted for the whole deployment.

## Rooms

The Rooms page lists the rooms that started in the selected time range, active and closed, and refreshes live. The figures above the table say how many rooms and participants are active now, and how many rooms and participant sessions the range holds.

Filter the list by status, search a room by the start of its name or by its SID, and keep only the rooms that used egress, ingress or agents. Each row shows the room's status, start and end, duration, unique identities, active participants, data transferred and the services it used. Sort by start, end, duration, unique identities or active participants to find, for example, the longest or the busiest rooms of the week. In OpenVidu **PRO** Elastic and High Availability deployments, a **Node** filter and column show the rooms of each [media node](#media-nodes).

### Room details

> **This view is part of OpenVidu PRO edition.**

The page of a room tells its whole story. The header shows its status, its topology (1:1, 1:N, N:M...), whether it was recorded, and when and why it ended. In Elastic and High Availability deployments, it also names the media node that hosted the room. The figures below sum it up: duration, participants (with the most connected at once), unique identities, data transferred, connection success, average quality and services.

Three charts cover the life of the room: **active participants**, **bitrate** and **quality**. Joins, leaves, aborted connections and the start and end of each egress are marked on them, so you can relate a drop in quality or bitrate to what was happening in the room at that moment.

The rest of the page lists what took part in the room: its **participants** grouped by identity, its **egresses** and **ingress sessions**, the **timeline of events** (filterable by type and by participant, each event with its full content) and its configuration and metadata. The page keeps refreshing while the room is active.

## Participants

The Participants page lists participant sessions over the selected time range. Search by the start of an identity or by SID, and filter by kind (regular participants by default, or agent, egress and ingress sessions), by status, by room, or keep only the publishers. Each row shows the session's room, kind, status, join and leave times, duration and what it published (camera, microphone, screen).

The figures above the table show the participants active now, the services active now and the sessions of the range.

### Participant details

> **This view is part of OpenVidu PRO edition.**

The page of a participant session shows what that person experienced. The header names its room and, in Elastic and High Availability deployments, its media node. The figures give its duration, data transferred, quality and how many times the connection had to be resumed. Two cards describe the **client** (SDK, operating system, browser, device, network) and the **connection** (type, time to connect and, once it ended, the reason of the disconnection).

The charts follow the session over time: **quality**, **bitrate**, **round-trip time**, **jitter** and **packets lost**. Below them are the **tracks it published** and the **tracks it subscribed to**, the other sessions of the same identity (in this room or in any room), and the timeline of its events.

Selecting a published track opens the **track panel**: its source, codec, resolution and simulcast layers, the statistics of each layer, its subscribers, and charts of bitrate, loss, jitter, round-trip time and quality of that track alone.

## Agents

The Agents page lists the sessions of agent participants in the selected time range, with their agent name, room, status and duration, a live counter of the agents connected now and the number of agent sessions in the range. The agents of the official collection of [OpenVidu agents](https://openvidu.io/3.10/docs/ai/openvidu-agents/overview/index.md) carry an **OpenVidu** tag, and the **Origin** filter keeps only them or only third-party agents. Agents join rooms as participants of kind Agent, so their sessions also appear in the Participants page when filtering by that kind.

## Egress

The Egress page lists the egresses started in the selected time range and refreshes live, so it is the place to follow a recording or a stream while it runs. The figures above the table show the egresses active now, those started and failed in the range, and the total duration.

Search by the start of a room name or by egress ID, and filter by type (room composite, web, participant, track composite or track) and by status. Each row shows the egress's room, type, status, start, end, duration and outputs, and failed egresses are flagged. Sort by end time or duration to find the longest ones.

### Egress details

> **This view is part of OpenVidu PRO edition.**

The page of an egress follows it while it runs and keeps its record once it ends. If the egress failed, the page shows its error, with an explanation when it was lost together with its node. The **outputs** are the files, streams, segments or images it produced, with their location, duration and size, and the **timeline of its status changes** tells when it reached each status. A summary of the **request** that started it gives its layout, preset, recorded participant and tracks, and the full request is available on demand. The page also lists the events of the egress. Credentials in URLs and storage settings are never shown.

## Ingress

The Ingress page lists the ingresses with activity in the selected time range: those created in it, those that streamed in it, and those publishing now. An ingress is a reusable input, and each stream published to it is one **session**. The figures above the table show the ingresses publishing now, the ingresses and sessions of the range and their total duration.

Search by the start of a name or by ID, and filter by input type (RTMP, WHIP or URL) and status. Each row shows the ingress's input type, room, status, creation time, total duration, number of sessions and last session.

### Ingress details

> **This view is part of OpenVidu PRO edition.**

The page of an ingress shows its definition, its events and, if it has one, its last error. Each of its **sessions** is listed with the participant it published as, its room, its video and audio details and the error it ended with, if any. An RTSP camera pulled by a URL ingress reads **URL (RTSP)**. Stream keys and credentials in URLs are never shown.

## Media nodes

> **These views are part of OpenVidu PRO edition, in Elastic and High Availability deployments.**

In deployments with several media nodes, the dashboard tells you what each of them is doing and lets you look at any figure for one node alone. A media node is named after its private IP address (`media-node-10-0-0-1`) and keeps that name when its OpenVidu Server restarts.

The **Media nodes** page lists every media node with its IP, RTC engine, version, state, active rooms and participants, and how many times its server restarted. A node is **alive** while its analytics data keeps arriving, **draining** while it waits for its rooms to end before it stops, **not reporting** when its data stopped arriving without a clean stop, and **stopped** once it was shut down. The figures above the table tell how many nodes are reporting and how many rooms OpenVidu Server had to close itself because their node disappeared, which points to crashes.

### Media node details

The page of a media node shows its state, its IP, RTC engine and version, and counts its active rooms and participants, the rooms OpenVidu Server had to close itself and the restarts of its server. A card sums up its recent activity: rooms, participant sessions, minutes, data transferred and connection success over the last 24 hours, or over the 24 hours before it stopped, with a link to the Analytics page scoped to that node.

Below them, the **Rooms** section lists the rooms the node hosts or hosted, and the **Servers** section tells the history of its servers: when each one started and stopped, and whether it stopped cleanly.

## Exporting data

Every list and every Analytics section can be taken out of the dashboard, to work on it in a spreadsheet or to feed a report:

- **Export CSV**, in the toolbar of each list (Rooms, Participants, Agents, Egress and Ingress), downloads what the list shows: the same time range, search, filters and sort order, across all its pages and not only the one on screen. An export holds up to 10,000 rows. When the list has more, the dashboard says so and you can narrow the range or the filters to export the rest.
- **Export XLSX**, in the header of each Analytics section, saves an Excel workbook with the data of its charts: one sheet per time resolution, one per breakdown, and an Info sheet with the range, time zone and scope of the export.
- In OpenVidu **PRO**, the Participants section of a [room's page](#room-details) exports its **attendance** as CSV: one row per identity, with the total time it spent in the room.

> **Warning**
>
> An exported file is no longer protected by the login of the dashboard. It may hold participant identities and names, so share it with the same care as the dashboard's credentials.

## Common tasks

### Investigating a room with problems

> **This workflow uses views of OpenVidu PRO edition.**

1. Find the room: type its name or SID in the search box, or open the Rooms page and filter the time range in which the problem happened.
1. In the room's page, look at the **Quality** and **Bitrate** charts around the time of the problem. The markers show who joined or left and which egress started at that moment.
1. In the **Participants** section, the Quality column points at the sessions that went worst. Open the one that had the problem.
1. The participant's page tells whether the cause was on their side: the client and network they used, the connection type, how many times the connection was resumed, and the packet loss, jitter and round-trip time over time.
1. If only one track was affected, open it from **Published tracks** to see its layers and the statistics of each of its subscribers.
1. The **events timeline** of the room or the participant gives the exact sequence: connection aborted, track unpublished, disconnect reason.

### Following an egress

1. Open the Egress page. An egress that has just been requested appears within seconds, and its status changes as it progresses.
1. Filter by room or search the room's name to see every egress of a session, or filter by the **Failed** status to review what went wrong in the range.
1. In OpenVidu **PRO**, open the egress to see where its outputs were stored and their size, the time of each status change and, if it failed, its error.

### Comparing two periods

1. Open the Analytics page and select the first period with the range picker.
1. Copy the URL, or export the sections you are interested in.
1. Select the second period. With both URLs open in two browser tabs you can compare them side by side, and with the exported workbooks you can chart them together.

## Settings

- **Preferences**: theme, default time zone, default time range, rows per page and auto-refresh interval. They are stored in the browser.
- **Data**: the retention of each class of data, the collections that hold it, and their documents and size. While a class has not reached its retention yet, the tab estimates the size it will take once it does. It also shows the progress of a data migration while it runs and, after an upgrade from a version before 3.10, the analytics data of that version while OpenVidu Server keeps it for a rollback. Each class has a delete button, and the one of the **Total** row deletes them all: see [Deleting analytics data](#deleting-analytics-data).

## Analytics data

OpenVidu Server writes the analytics data the dashboard shows to MongoDB, in its `openvidu` database. What it stores and for how long is configured in the `openvidu.analytics` section of `livekit.yaml`: see [Analytics settings](https://openvidu.io/3.10/docs/self-hosting/configuration/reference/#analytics-settings), and [Changing configuration](https://openvidu.io/3.10/docs/self-hosting/configuration/changing-config/index.md) to apply a change. OpenVidu Server stores:

- **Rooms, participant sessions, tracks, subscriptions, egresses, ingresses and ingress sessions**, updated as their events arrive.
- **Events** as emitted by OpenVidu Server, for the timelines.
- **Statistics** every 30 seconds: quality score, bytes, packets, loss, jitter and round-trip time. OpenVidu **COMMUNITY** stores them per participant and direction, and OpenVidu **PRO** per track, which the track panel needs.
- **Rollups** every 5 minutes, hour and day, which the Analytics page and the Overview read.

Credentials such as TURN passwords, storage keys, stream keys or tokens in URLs are never stored. Client IP addresses are stored only when `anonymize_ip` is set to `false`, and room and participant metadata only when `store_metadata` is enabled. The analytics data kept from a version before 3.10 is the exception: see [Personal data](#personal-data).

When the end of a room, participant session, egress or ingress session never arrives (for example, because a node crashed), OpenVidu Server closes it itself with an estimated end time: participants within about two minutes, and rooms once the cluster has given up on their node. The dashboard marks these entities as estimated.

The first start of OpenVidu Server 3.10 or later on a deployment upgraded from a previous version migrates its analytics data in the background, while new data is written as usual. The dashboard shows the progress of the migration in a banner, in the Overview and in Settings.

After the migration, OpenVidu Server keeps the analytics data of the previous version, the `legacy_events` and `stats` collections, so that a rollback to that version still finds it. That data keeps expiring with its own retention (32 days with the installers up to 3.9), and once the date shown in the **Data** tab of [Settings](#settings) has passed, OpenVidu Server removes both collections and frees their disk space. You can also drop them earlier from the **Data** tab of Settings, as explained in [Deleting analytics data](#deleting-analytics-data).

### Retention

Each class of data is kept for its own time, after which MongoDB deletes it:

| Data                                                       | Default  | `livekit.yaml` key                            |
| ---------------------------------------------------------- | -------- | --------------------------------------------- |
| Events                                                     | 7 days   | `openvidu.analytics.retention.events`         |
| Statistics                                                 | 7 days   | `openvidu.analytics.retention.stats`          |
| Closed tracks and subscriptions                            | 7 days   | `openvidu.analytics.retention.tracks`         |
| Closed rooms, participant sessions, egresses and ingresses | 90 days  | `openvidu.analytics.retention.entities`       |
| 5-minute rollups                                           | 7 days   | `openvidu.analytics.retention.rollups_5min`   |
| Hourly rollups                                             | 400 days | `openvidu.analytics.retention.rollups_hourly` |
| Daily rollups                                              | Forever  | `openvidu.analytics.retention.rollups_daily`  |

The details of a room or participant show their charts, events and tracks only while that data is retained, and say so when it is not. The Analytics page keeps showing the figures of that time from the rollups.

The **Data** tab of [Settings](#settings) shows how much space each class takes and, while a class has not reached its retention yet, estimates its size at full retention from the data so far, which helps to size each retention. A new `entities` or `tracks` retention applies to what closes after the restart, while the other classes follow the new value at once.

### Deleting analytics data

The **Data** tab of [Settings](#settings) deletes the stored data of a class before its retention does, to make room for new data or to start again from a clean history. Each class has its delete button, and the one of the **Total** row deletes every class at once. A confirmation dialog says what the deletion removes and what it keeps:

| Class                              | What its deletion removes                                                                                                                |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Events                             | The events of rooms, participant sessions, egresses and ingresses that have ended. Their records stay, with empty timelines.             |
| Stats                              | The statistics of the sessions and tracks that have ended. Their charts become empty, and the Analytics page keeps its figures.          |
| Tracks and subscriptions           | The tracks and subscriptions that have ended, with the statistics stored per track.                                                      |
| Entities                           | The rooms, participant sessions, egresses and ingress sessions that have ended, with their events, statistics, tracks and subscriptions. |
| 5-minute, hourly and daily rollups | The rollups before the previous 5 minutes, hour or day. The Analytics charts that read them become empty for that time.                  |

Every deletion keeps the data of the rooms in progress, the data that ended in the last 5 minutes, the latest rollups, the ingresses that were not deleted and the records of the media nodes. A deletion cannot be undone.

A deletion runs in the background, in batches that leave room for the writes of OpenVidu Server, and only one runs at a time. It goes on if you close the browser: the tab shows its progress, and a banner on the other pages says it is running. Once it ends, the tab shows when each class was deleted. If the dashboard stops in the middle of a deletion, the deletion is marked as interrupted and what it deleted stays deleted: start it again to finish.

In OpenVidu **PRO**, once a deletion ends, the details of a room, participant session, track, egress or ingress whose events, statistics, tracks or subscriptions it removed say so above the empty timeline, charts or tracks section, with the date the deletion finished and a link to the **Data** tab, so that an empty section is not taken for a room without activity.

After an upgrade from a version before 3.10, the **Legacy data** row deletes the analytics data that OpenVidu Server keeps for a rollback, before its date. Its two collections are dropped and their disk space is freed at once, and a rollback to the previous version finds no analytics data. The dialog of the **Total** row offers to delete it as well.

OpenVidu deployments include MongoDB 8.0. With an [external MongoDB](https://openvidu.io/3.10/docs/self-hosting/how-to-guides/external-mongodb/index.md), deleting statistics needs MongoDB 7.0 or later, because they are stored in a time-series collection.

#### Freeing disk space

Deleting documents does not make the database files smaller. MongoDB keeps the space they used inside each collection and reuses it for new data of that collection, so the disk usage stops growing until new data fills that space. About a minute after a deletion, the **Data** tab shows under each deleted class how much space MongoDB keeps free for new data.

To give that space back to the operating system, run the MongoDB `compact` command on the collections of the deleted classes, which the **Data** tab lists under each class. `compact` rewrites a collection and loads the disk while it runs, so run it at a quiet time.

Connect to MongoDB with `mongosh` from a machine that reaches port 20000 of the node that runs it:

```bash
docker run --rm -it --network host mongo:8.0 mongosh \
    "mongodb://<MONGO_ADMIN_USERNAME>:<MONGO_ADMIN_PASSWORD>@<NODE_IP>:20000/openvidu?authSource=admin&directConnection=true"
```

Replace the placeholders with values from your deployment. `<MONGO_ADMIN_USERNAME>` and `<MONGO_ADMIN_PASSWORD>` are the MongoDB admin credentials in the `openvidu.env` file, and `<NODE_IP>` is the IP address of the node, as explained below for each deployment.

Then estimate how much space each collection would give back, and compact it. For example, for the `events` collection:

```javascript
db.runCommand({ compact: "events", dryRun: true, force: true })  // estimatedBytesFreed
db.runCommand({ compact: "events", force: true })                // bytesFreed
```

Repeat it for each collection of the deleted classes. The statistics collection, `track_stats`, takes the same form.

**Single Node**

`<NODE_IP>` is the IP address of the OpenVidu node. MongoDB runs there as a replica set with a single member, its primary, and `compact` needs `force: true` to run on a primary.

**Elastic**

`<NODE_IP>` is the IP address of the master node. MongoDB runs there as a replica set with a single member, its primary, and `compact` needs `force: true` to run on a primary.

**High Availability**

MongoDB runs as a replica set with a member on each master node, and `compact` only applies to the member you are connected to. Compact the members one by one, setting `<NODE_IP>` to the IP address of each master node:

1. Connect to each secondary member and compact its collections without `force: true`. `rs.status()` tells which member is the primary.
1. Connect to the primary member and run `rs.stepDown()`, so that another member becomes the primary.
1. Connect again to that former primary, now a secondary, and compact its collections without `force: true`.

**External MongoDB**

Follow the procedure of your MongoDB provider to compact collections or to reclaim disk space.

### Personal data

The analytics data describes the people who use your applications, so the MongoDB of your deployment holds personal data about them. OpenVidu does not receive any of it: it stays in your deployment, and you decide how long it is kept and who can see it. If your organization keeps a record of the personal data it processes, or tells its users what it stores about them, this section lists what to include.

| Data                           | What it holds about a person                                                                                                                                                                                                  | Kept by default             |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| Participant sessions           | Identity and name, room name, join and leave times, how the session ended, region, connection type (UDP, TCP or TURN), SDK, operating system, browser and device model with their versions, and the quality of the connection | 90 days                     |
| Rooms                          | The room name, which your application chooses and may contain the name of a person or a customer                                                                                                                              | 90 days                     |
| Egresses                       | The room name, the identity of the recorded participant if there is one, and the file names and storage paths of the outputs, which often contain the room name                                                               | 90 days                     |
| Ingresses and ingress sessions | The ingress name, the room name, and the identity and name of the participant the ingress publishes as                                                                                                                        | 90 days                     |
| Tracks and subscriptions       | The identity of each publisher, and which participants received each track and when                                                                                                                                           | 7 days                      |
| Events                         | The identity, the room name and the content of each event                                                                                                                                                                     | 7 days                      |
| Statistics                     | Connection quality every 30 seconds, linked to a participant session                                                                                                                                                          | 7 days                      |
| Rollups                        | Counts and totals only, such as the number of participants or of distinct identities in a day. They name no one                                                                                                               | 7 days, 400 days or forever |

**Identities and names come from your application.** OpenVidu stores the identity and name that your application gives each participant. With OpenVidu Meet, the name is the one the participant joins with, and the identity is the member or user ID of the room member when it has one, or otherwise a value made from the name. In your own application, prefer an opaque ID as the identity rather than an email address or an employee number: the dashboard works just as well, and it stores less about each person.

**Two settings store more.** With `anonymize_ip: false`, each participant's IP address is stored as well. With `store_metadata: true`, the metadata and attributes your application sets on rooms and participants are stored as they are, whatever they contain. Both are off by default.

**Shortening the retention.** Each [retention](#retention) can be shortened in `livekit.yaml`. Participant sessions and the other entities are kept for at least 2 days, which OpenVidu Server needs to count the distinct identities of each day. A shorter `entities` or `tracks` retention applies only to what closes after the restart: to remove older data at once, delete it from the **Data** tab of [Settings](#settings).

**One person's data.** The **Data** tab deletes a class of data up to the current time, for everyone. To find or delete the data of one person, for example to answer a request from that person, connect with `mongosh` as explained in [Freeing disk space](#freeing-disk-space) and run the following with the identity they had in your application. In a High Availability deployment, connect to the primary member: `rs.status()` tells which one it is.

```javascript
const identity = "<IDENTITY>";
const closed = { expiresAt: { $ne: null } };
const sids = db.participants.distinct("_id", { identity });
const closedSids = db.participants.distinct("_id", { ...closed, identity });
const activeSids = db.participants.distinct("_id", { identity, expiresAt: null });

// Where an egress request can name the person: in events under "payload.egress.request", in egresses under "rawRequest"
const requestPaths = ["participant.identity",
  "egress.source.media.video.participant_video.identity", "egress.source.media.audio.routes.match.participant_identity",
  "replay.source.media.video.participant_video.identity", "replay.source.media.audio.routes.match.participant_identity"];
const events = { $or: [{ participantSid: { $in: sids } },
  ...["identity", "payload.participant.identity", "payload.publisher.identity", "payload.ingress.participant_identity",
    ...requestPaths.map((path) => "payload.egress.request." + path)].map((path) => ({ [path]: identity }))] };
const egresses = { $or: [{ "request.participantIdentity": identity },
  ...requestPaths.map((path) => ({ ["rawRequest." + path]: identity }))] };

// List what is stored about this identity
db.participants.find({ identity });
db.tracks.find({ participantSid: { $in: sids } });
db.track_subscriptions.find({ $or: [{ subscriberSid: { $in: sids } }, { publisherSid: { $in: sids } }] });
db.events.find(events);
db.egresses.find(egresses);
db.ingresses.find({ participantIdentity: identity });
db.ingress_sessions.find({ participantIdentity: identity });
db.rooms.find({ "internal.identities": identity }, { name: 1, createdAt: 1 });

// Delete it, except what belongs to something still in progress: a session, a recording or an ingress
const inProgress = [
  { participantSid: { $in: activeSids } },
  { "payload.publisher.sid": { $in: activeSids } },
  { egressId: { $in: db.egresses.distinct("_id", { expiresAt: null }) } },
  { ingressSessionId: { $in: db.ingress_sessions.distinct("_id", { expiresAt: null }) } },
  { ingressSessionId: null, ingressId: { $in: db.ingresses.distinct("_id", { expiresAt: null }) } }
];
db.events.deleteMany({ $and: [events, { $nor: inProgress }] });
db.track_stats.deleteMany({ "meta.participantSid": { $in: closedSids } });
db.track_subscriptions.deleteMany({ $and: [closed, { $or: [{ subscriberSid: { $in: closedSids } }, { publisherSid: { $in: closedSids } }] }] });
db.tracks.deleteMany({ ...closed, participantSid: { $in: closedSids } });
db.egresses.deleteMany({ $and: [closed, egresses] });
db.ingress_sessions.deleteMany({ ...closed, participantIdentity: identity });
db.ingresses.deleteMany({ ...closed, participantIdentity: identity });
db.participants.deleteMany({ ...closed, identity });
// Rooms keep their counts: the identity is replaced by an anonymous value, except where the person is still connected
db.rooms.updateMany(
  { "internal.identities": identity, _id: { $nin: db.participants.distinct("roomSid", { identity, expiresAt: null }) } },
  { $set: { "internal.identities.$": "deleted-" + new ObjectId() } });

// Data of a version before 3.10, kept for some days after an upgrade to roll back (legacy_events and stats)
const legacySids = [...new Set([...sids, ...db.legacy_events.distinct("participant.sid", { "participant.identity": identity })])];
db.legacy_events.deleteMany({ $or: [
  { participant_id: { $in: legacySids } }, { "participant.sid": { $in: legacySids } }, { "webhook.participant_id": { $in: legacySids } },
  ...["participant.identity", "publisher.identity", "ingress.participant_identity", "webhook.participant_identity",
    "egress.Request.Participant.identity"].map((path) => ({ [path]: identity }))] });
db.getCollection("stats").deleteMany({ participant_id: { $in: legacySids } });
```

The script keeps what belongs to something still in progress: a session the person is still connected to, or a recording or an ingress that is still running. Run it again once they have ended.

Rooms are not deleted, because they hold data about everyone who took part. The script lists the rooms the person took part in and replaces their identity in them with an anonymous value, so the counts of those rooms stay right. The room name stays as it is: if it contains the person's name, look for it with `db.rooms.find({ nameLower: /<name>/ })`. The rollups keep their counts, which name no one.

After an upgrade from a version before 3.10, the script also deletes the person's data that OpenVidu Server keeps from that version for a rollback.

**Who can see it.** Anyone with the dashboard's administrator credentials can see every room and participant session that is retained and export it. The dashboard has a single administrator account and does not log who viewed or exported what, so share those credentials only with the people who need them.

**Copies that retention does not reach.** Retention and deletions act on the MongoDB of your deployment only. They do not reach:

- the files exported from the dashboard (see [Exporting data](#exporting-data));
- backups or snapshots of your MongoDB or its disks;
- the analytics data of a version before 3.10, which OpenVidu Server keeps for a rollback after an upgrade. It was written before `anonymize_ip` applied to it, so it may contain client IP addresses. Delete it from the **Legacy data** row of the **Data** tab once you no longer need to roll back.

With an [external MongoDB](https://openvidu.io/3.10/docs/self-hosting/how-to-guides/external-mongodb/index.md), the data is stored by whoever runs that database.

None of this data is sent to OpenVidu.
