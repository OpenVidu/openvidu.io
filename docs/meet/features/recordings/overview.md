---
title: Recordings in OpenVidu Meet
description: Overview of how recordings work in OpenVidu Meet.
tags:
  - setupcustomgallery
---

# Recordings

OpenVidu Meet can record [meetings](../meetings/overview.md) and store them on the server so they can be played back, shared and downloaded at any time — even after the meeting has ended.

## Overview

Recordings are always associated with the [room](../rooms/overview.md) where they were generated. They inherit the room's access permissions by default and are accessible both from within the room and from the global "Recordings" page of the OpenVidu Meet console.

### Key principles

- Recordings can only be started by a participant with `Moderator` role.
- A room must have recording enabled in its [configuration](../rooms/create.md) to allow starting recordings.
- Recordings persist after the meeting ends and can be managed independently from the "Recordings" page.
- Each recording inherits the [access permissions](list.md#access-permissions-for-recordings) defined in its room.

## Creation & Management

Moderators start and stop recordings during a live meeting. Afterwards, anyone with the right permissions can browse, share, download or delete them.

- [Start / Stop recording](start-stop.md) — how a Moderator starts and stops a recording during a meeting.
- [List Recordings](list.md) — browse all recordings from the console or from the room's join view, including access permission rules.
- [Share & Download](share-download.md) — generate shareable links or download recording files.
- [Delete Recordings](delete.md) — remove recordings individually or in bulk.

## Recording configuration

Recording behaviour can be tuned per room at creation time or when editing a room.

- [Recording layouts](layouts.md) — choose between Grid, Speaker and Single Speaker layouts.
- [Recording resolution](resolution.md) — configure the resolution to balance quality and storage.

## Recording REST API

Recordings can be managed via the [OpenVidu Meet REST API](../../embedded/reference/rest-api.md):

| Operation | HTTP Method | Reference |
|-----------|-------------|-----------|
| Get recording | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRecording){:target="_blank"} |
| Get all recordings | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRecordings){:target="_blank"} |
| Delete recording | DELETE | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/deleteRecording){:target="_blank"} |
| Bulk delete recordings | DELETE | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/bulkDeleteRecordings){:target="_blank"} |
| Download recordings | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/downloadRecordings){:target="_blank"} |
| Get recording media | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRecordingMedia){:target="_blank"} |
| Get recording URL | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRecordingUrl){:target="_blank"} |
