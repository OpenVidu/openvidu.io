---
title: Recording creation & management in OpenVidu Meet
description: Start, stop, list, share, download and delete recordings in OpenVidu Meet.
tags:
  - setupcustomgallery
---

# Creation & Management

## Start / Stop recording

Recordings must be started by a participant with the `canRecord` permission in the meeting view (see [Role Management](../meetings/role-management.md)).

<a class="glightbox" href="../../../../assets/videos/meet/start-recording.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="../../../../assets/videos/meet/start-recording.mp4" loading="lazy" defer muted playsinline autoplay loop async></video></a>

While the recording is active, all participants in the meeting will see an indicator in the bottom left corner.

<a class="glightbox" href="../../../../assets/images/meet/recordings/recording-indicator.png" data-type="image" data-desc-position="bottom" data-gallery="gallery2"><img src="../../../../assets/images/meet/recordings/recording-indicator.png" loading="lazy"/></a>

To stop the recording, a participant with the `canRecord` permission must simply click the **"Stop recording"** button. The recording will be automatically saved in the OpenVidu Meet server.

<a class="glightbox" href="../../../../assets/images/meet/recordings/stop-recording.png" data-type="image" data-desc-position="bottom" data-gallery="gallery3"><img src="../../../../assets/images/meet/recordings/stop-recording.png" loading="lazy"/></a>

## List Recordings

OpenVidu Meet console can be used to manage all recordings from the "Recordings" page. It is possible to see all recordings, play them, download them, delete them, and share them via a link:

<a class="glightbox" href="../../../../assets/images/meet/recordings/recording-page.png" data-type="image" data-desc-position="bottom" data-gallery="gallery5"><img src="../../../../assets/images/meet/recordings/recording-page.png" loading="lazy" class="round-corners"/></a>

By default, recordings share the same access permissions as their rooms. Whenever a user uses a room link to join a meeting, they will also have the possibility of accessing the list of its previous recordings (if any):

<a class="glightbox" href="../../../../assets/images/meet/recordings/join-view-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery10"><img src="../../../../assets/images/meet/recordings/join-view-dark.png#only-dark" loading="lazy" class="control-height round-corners"/></a>
<a class="glightbox" href="../../../../assets/images/meet/recordings/join-view-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery10"><img src="../../../../assets/images/meet/recordings/join-view-light.png#only-light" loading="lazy" class="control-height round-corners"/></a>

The recording list shows every recording of that particular room:

<a class="glightbox" href="../../../../assets/images/meet/recordings/recording-list-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery11"><img src="../../../../assets/images/meet/recordings/recording-list-dark.png#only-dark" loading="lazy" class="control-height round-corners"/></a>
<a class="glightbox" href="../../../../assets/images/meet/recordings/recording-list-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery11"><img src="../../../../assets/images/meet/recordings/recording-list-light.png#only-light" loading="lazy" class="control-height round-corners"/></a>

Participants can also open the list of recordings for that room directly from the meeting view:

<a class="glightbox" href="../../../../assets/videos/meet/recording-while-meeting.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery6"><video class="round-corners" src="../../../../assets/videos/meet/recording-while-meeting.mp4" defer muted playsinline autoplay loop async></video></a>

The recording view allows playing the video, downloading it or creating a [shareable link](#share-download):

<a class="glightbox" href="../../../../assets/images/meet/recordings/recording-detail.png" data-type="image" data-desc-position="bottom" data-gallery="gallery7"><img src="../../../../assets/images/meet/recordings/recording-detail.png" loading="lazy" class="round-corners"/></a>

### Access permissions for recordings

When [creating a new room](../rooms/creation-management.md#create-rooms), you can define who is allowed to access and manage the recordings generated within that room. This access control system helps ensure privacy, security, and proper role-based permissions for recorded meetings.

<a class="glightbox" href="../../../../assets/images/meet/recordings/recording-access-control.png" data-type="image" data-desc-position="bottom" data-gallery="gallery8"><img src="../../../../assets/images/meet/recordings/recording-access-control.png" loading="lazy" class="round-corners"/></a>

#### Available access options

* **Only admin**
  Restricts access to recordings exclusively to OpenVidu Meet administrators. This option provides the highest level of security and is ideal for sensitive meetings. Administrators always retain access to recordings from any room.

* **Admin and moderators**
  Grants recording access to administrators and participants assigned the **Moderator** role. This configuration allows trusted meeting leaders to review or manage recordings while maintaining controlled access.

* **Admin, moderators, and speakers** *(default)*
  Allows administrators, moderators, and participants with the **Speaker** role to access recordings. This default setting offers a balanced approach, promoting collaboration while still enforcing role-based permissions.

!!! info
    Participants with role "Speaker" may only **play** recordings. Administrators and participants with role "Moderator" can also **delete** them.

## Share & Download

Specific recordings can be shared through a link:

- Users can generate a shareable link from the recording list.

    <a class="glightbox" href="../../../../assets/videos/meet/share-recording-from-recording-list.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery6"><video class="round-corners" src="../../../../assets/videos/meet/share-recording-from-recording-list.mp4" defer muted playsinline autoplay loop async></video></a>

- Users can generate a shareable link from the recording view.

    <a class="glightbox" href="../../../../assets/videos/meet/share-recording.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery7"><video class="round-corners" src="../../../../assets/videos/meet/share-recording.mp4" defer muted playsinline autoplay loop async></video></a>

- From OpenVidu Meet console it is possible to generate shareable links for any recording.

    <a class="glightbox" href="../../../../assets/videos/meet/meet-recording-share-dark.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery8"><video class="round-corners" src="../../../../assets/videos/meet/meet-recording-share-dark.mp4" defer muted playsinline autoplay loop async></video></a>

Recordings can also be **downloaded** from the recording view and from the "Recordings" page, as well as from the [REST API](index.md#recording-rest-api).

## Delete Recordings

Recordings can be deleted individually or in bulk from the "Recordings" page in OpenVidu Meet console, as well as from the recording view (if the user has the required permissions). Recordings can also be deleted through the [REST API](index.md#recording-rest-api).

!!! info
    Only administrators and participants with role "Moderator" can delete recordings. See [Access permissions for recordings](#access-permissions-for-recordings).
