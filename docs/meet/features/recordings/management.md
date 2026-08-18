---
title: "Recording management in OpenVidu Meet"
description: "Start and stop recordings, then list, play, share, download and delete them, from the OpenVidu Meet application or the Recordings REST API."
page_features:
  - lazyvideo
---

# Creation & Management

## Start / Stop recording

Recordings are started from the meeting view by a participant with the `canRecord` permission (see [Predefined roles](../rooms/access.md#predefined-roles)). The room must have recording [enabled in its configuration](configuration.md#enabling-recordings).

<a class="glightbox" href="/assets/videos/meet/recordings/management/start-recording-dark.mp4" data-type="video" data-desc-position="bottom" data-gallery="dark"><video class="round-corners lazy-video" src="/assets/videos/meet/recordings/management/start-recording-dark.mp4#only-dark" preload="none" muted playsinline loop></video></a>
<a class="glightbox" href="/assets/videos/meet/recordings/management/start-recording-light.mp4" data-type="video" data-desc-position="bottom" data-gallery="light"><video class="round-corners lazy-video" src="/assets/videos/meet/recordings/management/start-recording-light.mp4#only-light" preload="none" muted playsinline loop></video></a>

While the recording is active, all participants in the meeting will see an indicator in the bottom left corner.

![Recording indicator shown to participants during the meeting](../../../assets/images/meet/recordings/management/recording-indicator-dark.png#only-dark){ loading=lazy }
![Recording indicator shown to participants during the meeting](../../../assets/images/meet/recordings/management/recording-indicator-light.png#only-light){ loading=lazy }

To stop the recording, a participant with the `canRecord` permission must simply click the **"Stop recording"** button. The recording is then automatically saved on the OpenVidu Meet server.

![Stop recording button in the meeting toolbar](../../../assets/images/meet/recordings/management/stop-recording-dark.png#only-dark){ loading=lazy }
![Stop recording button in the meeting toolbar](../../../assets/images/meet/recordings/management/stop-recording-light.png#only-light){ loading=lazy }

!!! info "Starting and stopping recordings via REST API"
    Recordings can also be started and stopped with the [REST API](#rest-api-reference). There must be an **active meeting** in the target room — starting a recording in a room with no ongoing meeting returns an error. When starting a recording via the API, you may also **override** the room's default [layout](configuration.md#recording-layouts) and [encoding](configuration.md#recording-encoding) for that specific recording.

## Managing recordings { #managing-recordings }

A saved recording can be **listed**, **played**, **shared**, **downloaded** and **deleted** (individually or in bulk). All of these actions are available — subject to your [recording permissions](overview.md#recording-permissions) — from any of the places where recordings appear in the app:

- The general **"Recordings"** page, which lists every recording you can access.

![Recordings page listing every accessible recording](../../../assets/images/meet/recordings/management/recording-list-dark.png#only-dark){ .round-corners loading=lazy }
![Recordings page listing every accessible recording](../../../assets/images/meet/recordings/management/recording-list-light.png#only-light){ .round-corners loading=lazy }

- The **detail recording page** — accessed from the general "Recordings" page when clicking a recording — which shows the recording's metadata and a player displaying it.

![Recording detail page with metadata and actions](../../../assets/images/meet/recordings/management/recording-detail-dark.png#only-dark){ .round-corners loading=lazy }
![Recording detail page with metadata and actions](../../../assets/images/meet/recordings/management/recording-detail-light.png#only-light){ .round-corners loading=lazy }

- The **"Recordings"** tab of a [room's detail page](../rooms/management.md#room-details), listing that single room's recordings.

![Recordings tab of a room's detail page](../../../assets/images/meet/rooms/management/room-details-dark.png#only-dark){ .round-corners loading=lazy }
![Recordings tab of a room's detail page](../../../assets/images/meet/rooms/management/room-details-light.png#only-light){ .round-corners loading=lazy }

- The [**room recordings view**](../meetings/lifecycle.md#recordings-view), reachable from within a meeting (and from the lobby view before joining).

![Recordings view listing the recordings of the room](../../../assets/images/meet/recordings/management/room-recordings-dark.png#only-dark){ .round-corners loading=lazy }
![Recordings view listing the recordings of the room](../../../assets/images/meet/recordings/management/room-recordings-light.png#only-light){ .round-corners loading=lazy }

- The **display recording view** — accessed when clicking the play button for a recording — which displays the recording.

![Recording playback view](../../../assets/images/meet/recordings/management/recording-display-dark.png#only-dark){ .round-corners loading=lazy }
![Recording playback view](../../../assets/images/meet/recordings/management/recording-display-light.png#only-light){ .round-corners loading=lazy }

### Sharing recordings { #sharing-recordings }

When you create a shareable link for a recording, you choose **who can access it**:

- **OpenVidu Meet users**: any logged-in OpenVidu Meet user can view the recording — even if they have no recording permissions in that room, or no access to the room at all.
- **Anyone**: any individual with the link can view it without logging in. This option is available only when the room has [anonymous recording sharing](configuration.md#anonymous-recording-sharing) enabled.

<a class="glightbox" href="/assets/videos/meet/recordings/management/share-recording-dark.mp4" data-type="video" data-desc-position="bottom" data-gallery="dark"><video class="round-corners lazy-video" src="/assets/videos/meet/recordings/management/share-recording-dark.mp4#only-dark" preload="none" muted playsinline loop></video></a>
<a class="glightbox" href="/assets/videos/meet/recordings/management/share-recording-light.mp4" data-type="video" data-desc-position="bottom" data-gallery="light"><video class="round-corners lazy-video" src="/assets/videos/meet/recordings/management/share-recording-light.mp4#only-light" preload="none" muted playsinline loop></video></a>

## REST API reference { #rest-api-reference }

All of these operations can also be performed programmatically with the [OpenVidu Meet REST API](../../embedded/reference/rest-api.md). See the [REST API specification :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html){:target="_blank"} for the full list of available endpoints, request bodies and response schemas.

| Operation | HTTP Method | Reference |
|-----------|-------------|-----------|
| Start a recording | POST | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/startRecording){:target="_blank"} |
| Stop a recording | POST | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/stopRecording){:target="_blank"} |
| Get all recordings | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRecordings){:target="_blank"} |
| Download recordings | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/downloadRecordings){:target="_blank"} |
| Bulk delete recordings | DELETE | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/bulkDeleteRecordings){:target="_blank"} |
| Get a recording | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRecording){:target="_blank"} |
| Delete a recording | DELETE | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/deleteRecording){:target="_blank"} |
| Get recording media | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRecordingMedia){:target="_blank"} |
| Get recording URL | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRecordingUrl){:target="_blank"} |
