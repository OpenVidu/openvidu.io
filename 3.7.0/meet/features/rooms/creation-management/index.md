# Creation & Management

## Create Rooms

OpenVidu Meet internal users with permissions to create and manage rooms can create a new room directly from the **"Rooms"** page in the OpenVidu Meet console. Each room requires a name and can be customized with Advanced Setup options:

- Set up an [auto-deletion date](#room-auto-deletion) and configure [auto-deletion policies](#room-auto-deletion-policies).
- Enable/disable features like recording, chat, virtual backgrounds, and E2EE (end-to-end encryption).
- Configure default permissions for each role (`Moderator` and `Speaker`).
- Enable/disable anonymous access for each role.

\[[](../../../../assets/videos/meet/meet-rooms-dark.mp4#only-dark)\](https://openvidu.io/3.7.0/assets/videos/meet/meet-rooms-dark.mp4) \[[](../../../../assets/videos/meet/meet-rooms-light.mp4#only-light)\](https://openvidu.io/3.7.0/assets/videos/meet/meet-rooms-light.mp4)

Info

Learn more about OpenVidu Meet internal users and their permissions in [OpenVidu Meet internal users](https://openvidu.io/3.7.0/meet/features/rooms/access/#openvidu-meet-internal-users).

## Edit Rooms

Modify room settings anytime from the **Rooms** page, as long as no meeting is currently active. You can update:

- The room name.
- The [auto-deletion date](#room-auto-deletion) and [auto-deletion policies](#room-auto-deletion-policies).
- Enable/disable features like recording, chat, virtual backgrounds, and E2EE (end-to-end encryption).
- Default permissions for each role (`Moderator` and `Speaker`).
- Anonymous access settings for each role.

## List Rooms

The **Rooms** page lists every available room and lets administrators:

- Start a meeting in a room.
- [Edit room settings](#edit-rooms) anytime (if no meeting is active).
- [Delete rooms](#delete-rooms) individually or in bulk.
- Access recordings.
- Share [room links](https://openvidu.io/3.7.0/meet/features/rooms/access/#room-links) with different permissions.

\[[](../../../../assets/videos/meet/room-actions-dark.mp4#only-dark)\](https://openvidu.io/3.7.0/assets/videos/meet/room-actions-dark.mp4) \[[](../../../../assets/videos/meet/room-actions-light.mp4#only-light)\](https://openvidu.io/3.7.0/assets/videos/meet/room-actions-light.mp4)

## Delete Rooms

Rooms can be deleted individually or in bulk from the **Rooms** page. Deleting a room removes it and all associated data.

### Room auto-deletion

Rooms can be configured with an **auto-deletion date**. You can set this date when [creating](#create-rooms) or [editing a room](#edit-rooms). This helps keeping OpenVidu Meet clean and organized, avoiding clutter from old rooms that are no longer needed.

### Room auto-deletion policies

When the auto-deletion date is reached, the room will be deleted. The **Auto-deletion policies** determine how to handle active meetings and stored recordings when attempting to delete the room:

- **Active meetings policy**
  - `Force`: the meeting will be immediately ended without waiting for participants to leave, and the room will be deleted.
  - `When meeting ends`: the room will be deleted after the active meeting ends.
- **Recordings policy**
  - `Force`: the room and all its recordings will be deleted.
  - `Close`: the room will be closed instead of deleted, maintaining its recordings.
