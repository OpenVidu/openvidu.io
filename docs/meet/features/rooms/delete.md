---
title: Delete Rooms in OpenVidu Meet
description: Delete rooms manually or schedule auto-deletion to keep OpenVidu Meet clean.
tags:
  - setupcustomgallery
---

# Delete Rooms

Rooms can be deleted individually or in bulk from the **Rooms** page. Deleting a room removes it and all associated data.

<a class="glightbox" href="../../../../assets/images/meet/rooms-and-meetings/delete-room.png" data-type="image" data-desc-position="bottom" data-gallery="gallery5"><img src="../../../../assets/images/meet/rooms-and-meetings/delete-room.png" loading="lazy" class="round-corners"/></a>

## Room auto-deletion

Rooms can be configured with an **auto-deletion date**. You can set this date when [creating](create.md) or [editing a room](edit.md). This helps keeping OpenVidu Meet clean and organized, avoiding clutter from old rooms that are no longer needed.

<a class="glightbox" href="../../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery3"><img src="../../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-dark.png#only-dark" loading="lazy" class="control-height round-corners"/></a>
<a class="glightbox" href="../../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery3"><img src="../../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-light.png#only-light" loading="lazy" class="control-height round-corners"/></a>

## Room auto-deletion policies

When the auto-deletion date is reached, the room will be deleted. The **Auto-deletion policies** determine how to handle active meetings and stored recordings when attempting to delete the room:

- **Active meetings policy**
    - `Force`: the meeting will be immediately ended without waiting for participants to leave, and the room will be deleted.
    - `When meeting ends`: the room will be deleted after the active meeting ends.
- **Recordings policy**
    - `Force`: the room and all its recordings will be deleted.
    - `Close`: the room will be closed instead of deleted, maintaining its recordings.

<a class="glightbox" href="../../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-policies-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery3"><img src="../../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-policies-dark.png#only-dark" loading="lazy" class="control-height round-corners"/></a>
<a class="glightbox" href="../../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-policies-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery3"><img src="../../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-policies-light.png#only-light" loading="lazy" class="control-height round-corners"/></a>
