# Creation & Management

## Start / Stop recording

Recordings are started from the meeting view by a participant with the `canRecord` permission (see [Predefined roles](https://openvidu.io/3.8/meet/features/rooms/access/#predefined-roles)). The room must have recording [enabled in its configuration](https://openvidu.io/3.8/meet/features/recordings/configuration/#enabling-recordings).

\[[](/assets/videos/meet/recordings/management/start-recording-dark.mp4#only-dark)\](/assets/videos/meet/recordings/management/start-recording-dark.mp4) \[[](/assets/videos/meet/recordings/management/start-recording-light.mp4#only-light)\](/assets/videos/meet/recordings/management/start-recording-light.mp4)

While the recording is active, all participants in the meeting will see an indicator in the bottom left corner.

To stop the recording, a participant with the `canRecord` permission must simply click the **"Stop recording"** button. The recording is then automatically saved on the OpenVidu Meet server.

Starting and stopping recordings via REST API

Recordings can also be started and stopped with the [REST API](#rest-api-reference). There must be an **active meeting** in the target room — starting a recording in a room with no ongoing meeting returns an error. When starting a recording via the API, you may also **override** the room's default [layout](https://openvidu.io/3.8/meet/features/recordings/configuration/#recording-layouts) and [encoding](https://openvidu.io/3.8/meet/features/recordings/configuration/#recording-encoding) for that specific recording.

## Managing recordings

A saved recording can be **listed**, **played**, **shared**, **downloaded** and **deleted** (individually or in bulk). All of these actions are available — subject to your [recording permissions](https://openvidu.io/3.8/meet/features/recordings/overview/#recording-permissions) — from any of the places where recordings appear in the app:

- The general **"Recordings"** page, which lists every recording you can access.

- The **detail recording page** — accessed from the general "Recordings" page when clicking a recording — which shows the recording's metadata and a player displaying it.

- The **"Recordings"** tab of a [room's detail page](https://openvidu.io/3.8/meet/features/rooms/management/#room-details), listing that single room's recordings.

- The [**room recordings view**](https://openvidu.io/3.8/meet/features/meetings/lifecycle/#recordings-view), reachable from within a meeting (and from the lobby view before joining).

- The **display recording view** — accessed when clicking the play button for a recording — which displays the recording.

### Sharing recordings

When you create a shareable link for a recording, you choose **who can access it**:

- **OpenVidu Meet users**: any logged-in OpenVidu Meet user can view the recording — even if they have no recording permissions in that room, or no access to the room at all.
- **Anyone**: any individual with the link can view it without logging in. This option is available only when the room has [anonymous recording sharing](https://openvidu.io/3.8/meet/features/recordings/configuration/#anonymous-recording-sharing) enabled.

\[[](/assets/videos/meet/recordings/management/share-recording-dark.mp4#only-dark)\](/assets/videos/meet/recordings/management/share-recording-dark.mp4) \[[](/assets/videos/meet/recordings/management/share-recording-light.mp4#only-light)\](/assets/videos/meet/recordings/management/share-recording-light.mp4)

## REST API reference

All of these operations can also be performed programmatically with the [OpenVidu Meet REST API](https://openvidu.io/3.8/meet/embedded/reference/rest-api/index.md). See the [REST API specification](https://openvidu.io/3.8/meet/embedded/reference/api.html) for the full list of available endpoints, request bodies and response schemas.

| Operation              | HTTP Method | Reference                                                                                              |
| ---------------------- | ----------- | ------------------------------------------------------------------------------------------------------ |
| Start a recording      | POST        | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/startRecording)       |
| Stop a recording       | POST        | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/stopRecording)        |
| Get all recordings     | GET         | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/getRecordings)        |
| Download recordings    | GET         | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/downloadRecordings)   |
| Bulk delete recordings | DELETE      | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/bulkDeleteRecordings) |
| Get a recording        | GET         | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/getRecording)         |
| Delete a recording     | DELETE      | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/deleteRecording)      |
| Get recording media    | GET         | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/getRecordingMedia)    |
| Get recording URL      | GET         | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/getRecordingUrl)      |
