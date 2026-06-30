# Recordings

OpenVidu Meet can record [meetings](https://openvidu.io/3.7.0/meet/features/meetings/overview/index.md) and store them on the server so they can be played back, shared and downloaded at any time — even after the meeting has ended.

## Overview

Recordings are always associated with the [room](https://openvidu.io/3.7.0/meet/features/rooms/overview/index.md) where they were generated. They inherit the room's access permissions by default and are accessible both from within the room and from the global "Recordings" page of the OpenVidu Meet console.

### Key principles

- Recordings can only be started by a participant with `Moderator` role.
- A room must have recording enabled in its [configuration](https://openvidu.io/3.7.0/meet/features/rooms/creation-management/#create-rooms) to allow starting recordings.
- Recordings persist after the meeting ends and can be managed independently from the "Recordings" page.
- Each recording inherits the [access permissions](https://openvidu.io/3.7.0/meet/features/recordings/creation-management/#access-permissions-for-recordings) defined in its room.

## Creation & Management

Moderators start and stop recordings during a live meeting. Afterwards, anyone with the right permissions can browse, share, download or delete them.

- [Start / Stop recording](https://openvidu.io/3.7.0/meet/features/recordings/creation-management/#start-stop-recording) — how a Moderator starts and stops a recording during a meeting.
- [List Recordings](https://openvidu.io/3.7.0/meet/features/recordings/creation-management/#list-recordings) — browse all recordings from the console or from the room's join view, including access permission rules.
- [Share & Download](https://openvidu.io/3.7.0/meet/features/recordings/creation-management/#share-download) — generate shareable links or download recording files.
- [Delete Recordings](https://openvidu.io/3.7.0/meet/features/recordings/creation-management/#delete-recordings) — remove recordings individually or in bulk.

## Recording configuration

Recording behaviour can be tuned per room at creation time or when editing a room.

- [Recording layouts](https://openvidu.io/3.7.0/meet/features/recordings/configuration/#recording-layouts) — choose between Grid, Speaker and Single Speaker layouts.
- [Recording resolution](https://openvidu.io/3.7.0/meet/features/recordings/configuration/#recording-resolution) — configure the resolution to balance quality and storage.

## Recording REST API

Recordings can be managed via the [OpenVidu Meet REST API](https://openvidu.io/3.7.0/meet/embedded/reference/rest-api/index.md):

| Operation              | HTTP Method | Reference                                                                                                |
| ---------------------- | ----------- | -------------------------------------------------------------------------------------------------------- |
| Get recording          | GET         | [Reference](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/getRecording)         |
| Get all recordings     | GET         | [Reference](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/getRecordings)        |
| Delete recording       | DELETE      | [Reference](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/deleteRecording)      |
| Bulk delete recordings | DELETE      | [Reference](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/bulkDeleteRecordings) |
| Download recordings    | GET         | [Reference](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/downloadRecordings)   |
| Get recording media    | GET         | [Reference](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/getRecordingMedia)    |
| Get recording URL      | GET         | [Reference](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/getRecordingUrl)      |
