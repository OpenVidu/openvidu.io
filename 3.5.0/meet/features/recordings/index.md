# Recordings

## Recording a meeting

Recordings must be started by a participant with role "Moderator" in the meeting view (see [Participant roles in a room](https://openvidu.io/3.5.0/meet/features/users-and-permissions/#participant-roles-in-a-room)).

\[[](../../../assets/videos/meet/start-recording.mp4)\](https://openvidu.io/3.5.0/assets/videos/meet/start-recording.mp4)

While the recording is active, all participants in the meeting will see an indicator in the bottom left corner.

To stop the recording, a participant with role "Moderator" must simply click the "Stop recording" button. The recording will be automatically saved in the OpenVidu Meet server.

## Viewing recordings

By default, recordings share the same access permissions as their rooms. Whenever a user uses a room link to join a meeting, they will also have the possibility of accessing the list of its previous recordings (if any):

The recording list shows every recording of that particular room:

Participants can also open the list of recordings for that room directly from the meeting view:

\[[](../../../assets/videos/meet/recording-while-meeting.mp4)\](https://openvidu.io/3.5.0/assets/videos/meet/recording-while-meeting.mp4)

The recording view allows playing the video, downloading it or creating a [shareable link](#sharing-recordings-via-link):

### Access permissions for recordings

When [creating a new room](https://openvidu.io/3.5.0/meet/features/rooms-and-meetings/#creating-a-room) you can configure who may access its recordings:

Available options are:

- **Only admin**: only administrators of OpenVidu Meet will have access to the recordings of this room. Administrators can always access recordings of any room.
- **Admin and moderators**: administrators and any participant of the meeting with "Moderator" role will have access to the recordings of this room.
- **Admin, moderators and speakers**: this is the default value. Administrators and any participant of the meeting with "Moderator" or "Speaker" role will have access to the recordings of this room.

Info

Participants with role "Speaker" may only **play** recordings. Administrators and participants with role "Moderator" can also **delete** them.

### Sharing recordings via link

Specific recordings can be shared through a link:

- Users can generate a shareable link from the recording list.

  \[[](../../../assets/videos/meet/share-recording-from-recording-list.mp4)\](https://openvidu.io/3.5.0/assets/videos/meet/share-recording-from-recording-list.mp4)

- Users can generate a shareable link from the recording view.

  \[[](../../../assets/videos/meet/share-recording.mp4)\](https://openvidu.io/3.5.0/assets/videos/meet/share-recording.mp4)

- From OpenVidu Meet console it is possible to generate shareable links for any recording.

  \[[](../../../assets/videos/meet/meet-recording-share-dark.mp4)\](https://openvidu.io/3.5.0/assets/videos/meet/meet-recording-share-dark.mp4)

## Room recording settings

Rooms can be configured with different recording settings. You can set up these settings when [creating a new room](https://openvidu.io/3.5.0/meet/features/rooms-and-meetings/#creating-a-room) or [editing an existing room](https://openvidu.io/3.5.0/meet/features/rooms-and-meetings/#editing-a-room).

- **Allow Recording / No recording**: whether to allow recording the room or not.
- **Recording Access Control**: who can access the recordings of the room. See [Access permissions for viewing recordings](#access-permissions-for-viewing-recordings).

## Managing recordings

OpenVidu Meet console can be used to manage all recordings from the "Recordings" page. It is possible to see all recordings, play them, download them, delete them, and share them via a link:

## Recording REST API

Recordings can be managed via the [OpenVidu Meet REST API](https://openvidu.io/3.5.0/meet/embedded/reference/rest-api/index.md):

| Operation              | HTTP Method | Reference                                                                                                |
| ---------------------- | ----------- | -------------------------------------------------------------------------------------------------------- |
| Get recording          | GET         | [Reference](https://openvidu.io/3.5.0/meet/embedded/reference/api.html#/operations/getRecording)         |
| Get all recordings     | GET         | [Reference](https://openvidu.io/3.5.0/meet/embedded/reference/api.html#/operations/getRecordings)        |
| Delete recording       | DELETE      | [Reference](https://openvidu.io/3.5.0/meet/embedded/reference/api.html#/operations/deleteRecording)      |
| Bulk delete recordings | DELETE      | [Reference](https://openvidu.io/3.5.0/meet/embedded/reference/api.html#/operations/bulkDeleteRecordings) |
| Download recordings    | GET         | [Reference](https://openvidu.io/3.5.0/meet/embedded/reference/api.html#/operations/downloadRecordings)   |
| Get recording media    | GET         | [Reference](https://openvidu.io/3.5.0/meet/embedded/reference/api.html#/operations/getRecordingMedia)    |
| Get recording URL      | GET         | [Reference](https://openvidu.io/3.5.0/meet/embedded/reference/api.html#/operations/getRecordingUrl)      |
