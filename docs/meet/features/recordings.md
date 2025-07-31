---
title: Recordings
tags:
  - setupcustomgallery
---

# Recordings

## Room recording settings

Rooms can be configured with different recording settings. You can setup these settings when [creating a new room](./rooms-and-meetings.md#creating-a-room) or [editing an existing room](./rooms-and-meetings.md#editing-a-room).

- **Allow Recording / No recording**: whether to allow recording the room or not.
- **Recording Access Control**: who can access the recordings of the room. See section below [Access permissions for recordings](#access-permissions-for-recordings).

<a class="glightbox" href="../../../assets/images/meet/recordings/room-recording-settings.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="../../../assets/images/meet/recordings/room-recording-settings.png" loading="lazy" class="control-height"/></a>

## Recording a meeting

Recordings must be started by a participant with role "Moderator" in the meeting view. All participants in the meeting will see a recording indicator.

<a class="glightbox" href="../../../assets/videos/meet/start-recording.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery2"><video class="round-corners" src="../../../assets/videos/meet/start-recording.mp4" loading="lazy" defer muted playsinline autoplay loop async></video></a>

To stop the recording, a participant with role "Moderator" must simply click the "Stop recording" button. The recording will be automatically saved in the OpenVidu Meet server.

<a class="glightbox" href="../../../assets/images/meet/recordings/stop-recording.png" data-type="image" data-desc-position="bottom" data-gallery="gallery3"><img src="../../../assets/images/meet/recordings/stop-recording.png" loading="lazy"/></a>

## Managing recordings

You can manage all recordings from the "Recordings" page in OpenVidu Meet. Here you can see all recordings, play them, download them, delete them, and share them via a link:

<a class="glightbox" href="../../../assets/images/meet/recordings/recording-page.png" data-type="image" data-desc-position="bottom" data-gallery="gallery4"><img src="../../../assets/images/meet/recordings/recording-page.png" loading="lazy"/></a>

Participants with the requried permissions can also open in a new tab the "Recording" page directly from the meeting view:

<a class="glightbox" href="../../../assets/videos/meet/recording-while-meeting.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery5"><video class="round-corners" src="../../../assets/videos/meet/recording-while-meeting.mp4" defer muted playsinline autoplay loop async></video></a>

!!! info
    Recordings can also be managed programmatically via the [OpenVidu Meet REST API](../../assets/htmls/rest-api.html#/operations/getRecordings){:target="_blank"}.

## Access permissions for recordings

You can set specific access permissions for recordings **at room level**. Whether [creating a new room](./rooms-and-meetings.md#creating-a-room) or [editing the settings of an existing room](./rooms-and-meetings.md#editing-a-room), you can configure who may access its recordings:

<a class="glightbox" href="../../../assets/images/meet/recordings/recording-access-control.png" data-type="image" data-desc-position="bottom" data-gallery="gallery6"><img src="../../../assets/images/meet/recordings/recording-access-control.png" loading="lazy"/></a>

Available options are:

- **Only admin**: only administrators of OpenVidu Meet will have access to the recordings of this room. Administrators can always access recordings of any room.
- **Admin and moderators**: administrators and any participant of the meeting with "Moderator" role will have access to the recordings of this room.
- **Admin, moderators and speakers**: administrators and any participant of the meeting with "Moderator" or "Speaker" role will have access to the recordings of this room.

### Sharing recordings via link

Users with sufficient permissions can generate a link to a recording. This link can be made public or require authentication:

1. From the "Recordings" page, click on the "More Actions" button ( :material-dots-vertical: ) and "Share link" action ( :material-share-variant: ).
2. Choose the access type:
      - **Public Access**: anyone with the link can see the recording.
      - **Private Access**: only users [authenticated in OpenVidu Meet](./users-and-permissions.md#authentication-when-accessing-openvidu-meet) can see the recording.
3. Click "Generate Shareable Link" to create the link and share it.

<a class="glightbox" href="../../../assets/videos/meet/meet-recording-share-dark.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery7"><video class="round-corners" src="../../../assets/videos/meet/meet-recording-share-dark.mp4#only-dark" defer muted playsinline autoplay loop async></video></a>
<a class="glightbox" href="../../../assets/videos/meet/meet-recording-share-light.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery7"><video class="round-corners" src="../../../assets/videos/meet/meet-recording-share-light.mp4#only-light" defer muted playsinline autoplay loop async></video></a>