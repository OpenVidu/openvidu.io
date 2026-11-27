# Creation & Management

## Start / Stop recording

Recordings are started from the meeting view by a participant with the `recordingControl` permission (see [Predefined roles](https://openvidu.io/latest/meet/features/rooms/access/#predefined-roles)). The room must have recording [enabled in its configuration](https://openvidu.io/latest/meet/features/recordings/configuration/#enabling-recordings). A room can also be configured to start recording **automatically** when a participant joins: see [Recording trigger](https://openvidu.io/latest/meet/features/recordings/configuration/#recording-trigger).

Every participant is notified when the recording starts and when it stops, and while it is active a **REC** indicator with the elapsed time is shown in the status rail above the meeting layout. The **Activities** panel shows the state of the recording and holds its controls.

To stop the recording, a participant with the `recordingControl` permission must simply click the **"Stop recording"** button, in the toolbar or in the recording panel. The recording is then automatically saved on the OpenVidu Meet server. The button is available as soon as the recording has been requested, so a recording that is still starting can be cancelled before it captures anything.

> **Starting and stopping recordings from outside the meeting view**
>
> Recordings can also be started and stopped, in an **active meeting** only (starting one in a room with no ongoing meeting returns an error), through:
>
> - The [REST API](#rest-api-reference), which can also **override** the room's default [layout](https://openvidu.io/latest/meet/features/recordings/configuration/#recording-layouts) and [encoding](https://openvidu.io/latest/meet/features/recordings/configuration/#recording-encoding) for that recording.
> - The `recordingStart` and `recordingStop` [commands](https://openvidu.io/latest/meet/embedded/reference/webcomponent/#commands) of an [embedded](https://openvidu.io/latest/meet/embedded/intro/index.md) application, which require the local participant to hold the `recordingControl` permission. The progress of the recording is reported by the `recordingStarted`, `recordingUpdated` and `recordingEnded` [events](https://openvidu.io/latest/meet/embedded/reference/webcomponent/#events).
>
> As in the app, the start is refused in a room with recording disabled or with an automatic [recording trigger](https://openvidu.io/latest/meet/features/recordings/configuration/#recording-trigger).

## Managing recordings

A saved recording can be **listed**, **played**, **shared**, **downloaded** and **deleted** (individually or in bulk). All of these actions are available — subject to your [recording permissions](https://openvidu.io/latest/meet/features/recordings/overview/#recording-permissions) — from any of the places where recordings appear in the app:

- The general **"Recordings"** page, which lists every recording you can access. Above the list it shows how many of them there are in total, in progress, complete and failed, and selecting one of those figures filters the list by its statuses. The list can also be filtered by one or several statuses.

- The **detail recording page** — accessed from the general "Recordings" page when clicking a recording — which shows the recording's metadata and a player displaying it.

- The **"Recordings"** tab of a [room's detail page](https://openvidu.io/latest/meet/features/rooms/management/#room-details), listing that single room's recordings.

- The [**room recordings view**](https://openvidu.io/latest/meet/features/meetings/lifecycle/#recordings-view), reachable from within a meeting (and from the Join view).

- The **display recording view** — accessed when clicking the play button for a recording — which displays the recording.

### Sharing recordings

When you create a shareable link for a recording, you choose **who can access it**:

- **OpenVidu Meet users**: any logged-in OpenVidu Meet user can view the recording — even if they have no recording permissions in that room, or no access to the room at all.
- **Anyone**: any individual with the link can view it without logging in. This option is available only when the room has [anonymous recording sharing](https://openvidu.io/latest/meet/features/recordings/configuration/#anonymous-recording-sharing) enabled.

A link offers the download only when the person who created it holds the download permission. A link created without it plays the recording but does not offer to download it.

## REST API reference

All of these operations can also be performed programmatically with the [OpenVidu Meet REST API](https://openvidu.io/latest/meet/embedded/reference/rest-api/index.md). See the [REST API specification](https://openvidu.io/latest/meet/embedded/reference/api.html) for the full list of available endpoints, request bodies and response schemas.

| Operation              | HTTP Method | Reference                                                                                                |
| ---------------------- | ----------- | -------------------------------------------------------------------------------------------------------- |
| Start a recording      | POST        | [Reference](https://openvidu.io/latest/meet/embedded/reference/api.html#/operations/recordingStart)        |
| Stop a recording       | POST        | [Reference](https://openvidu.io/latest/meet/embedded/reference/api.html#/operations/recordingStop)         |
| Get all recordings     | GET         | [Reference](https://openvidu.io/latest/meet/embedded/reference/api.html#/operations/recordingList)         |
| Download recordings    | GET         | [Reference](https://openvidu.io/latest/meet/embedded/reference/api.html#/operations/recordingBulkDownload) |
| Bulk delete recordings | DELETE      | [Reference](https://openvidu.io/latest/meet/embedded/reference/api.html#/operations/recordingBulkDelete)   |
| Get a recording        | GET         | [Reference](https://openvidu.io/latest/meet/embedded/reference/api.html#/operations/recordingGet)          |
| Delete a recording     | DELETE      | [Reference](https://openvidu.io/latest/meet/embedded/reference/api.html#/operations/recordingDelete)       |
| Get recording media    | GET         | [Reference](https://openvidu.io/latest/meet/embedded/reference/api.html#/operations/recordingGetMedia)     |
| Download a recording   | GET         | [Reference](https://openvidu.io/latest/meet/embedded/reference/api.html#/operations/recordingDownload)     |
| Get recording URL      | GET         | [Reference](https://openvidu.io/latest/meet/embedded/reference/api.html#/operations/recordingGetUrl)       |
