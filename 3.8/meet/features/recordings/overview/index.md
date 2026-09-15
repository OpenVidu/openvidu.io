# Recordings

OpenVidu Meet can record [meetings](https://openvidu.io/3.8/meet/features/meetings/overview/index.md) and store them on the server so they can be played back, shared and downloaded at any time.

## How recordings work

Recordings are always associated with the [room](https://openvidu.io/3.8/meet/features/rooms/overview/index.md) where they were generated. Who can retrieve and delete them is governed by [room member permissions](#recording-permissions), and they can be opened both from within the room and from the global "Recordings" page of the OpenVidu Meet app.

### Key principles

- Recordings are started during an **active meeting** by a participant with the `canRecord` permission — from the app or the [REST API](https://openvidu.io/3.8/meet/features/recordings/management/#start-stop-recording).
- A room must have recording enabled in its [configuration](https://openvidu.io/3.8/meet/features/recordings/configuration/#enabling-recordings) to allow starting recordings.
- Recordings persist even after the meeting ends and can be managed independently.
- Access to a recording (retrieve and delete) is governed by room member permissions.

## Recording permissions

Who can retrieve and delete a room's recordings is governed by **[room member permissions](https://openvidu.io/3.8/meet/features/room-members/overview/#permissions)**, not by a room-wide setting:

- **`canRetrieveRecordings`** — list, play and download the room's recordings.
- **`canDeleteRecordings`** — delete the room's recordings.

By default, these permissions are assigned per role as follows:

| Role          | Retrieve recordings | Delete recordings |
| ------------- | ------------------- | ----------------- |
| **Moderator** | ✔                   | ✔                 |
| **Speaker**   | ✔                   | ✘                 |

You can change these defaults per room (when [creating](https://openvidu.io/3.8/meet/features/rooms/management/#create-rooms) or [editing](https://openvidu.io/3.8/meet/features/rooms/management/#edit-rooms) it) or per member (with [custom permissions](https://openvidu.io/3.8/meet/features/room-members/management/#add-a-member)). In addition, **admins** can retrieve and delete the recordings of **any** room, and a **room owner** always has full access to the recordings of their own created rooms.

## In this section

- [Creation & Management](https://openvidu.io/3.8/meet/features/recordings/management/index.md) — start and stop recordings during a meeting, browse, play, share, download and delete them, and the equivalent REST API operations.
- [Recording configuration](https://openvidu.io/3.8/meet/features/recordings/configuration/index.md) — enable recording per room and choose its layout, encoding and anonymous sharing.
