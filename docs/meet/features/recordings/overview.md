---
title: Recordings in OpenVidu Meet
description: Overview of how recordings work in OpenVidu Meet.
tags:
  - setupcustomgallery
---

# Recordings

OpenVidu Meet can record [meetings](../meetings/overview.md) and store them on the server so they can be played back, shared and downloaded at any time — even after the meeting has ended.

## How recordings work

Recordings are always associated with the [room](../rooms/overview.md) where they were generated. Who can retrieve and delete them is governed by [room member permissions](#access-permissions-for-recordings), and they can be opened both from within the room and from the global "Recordings" page of the OpenVidu Meet app.

### Key principles

- Recordings are started during an **active meeting** by a participant with the `canRecord` permission — from the app or the [REST API](management.md#start-stop-recording).
- A room must have recording enabled in its [configuration](configuration.md#enabling-recordings) to allow starting recordings.
- Recordings persist even after the meeting ends and can be managed independently from the "Recordings" page.
- Access to a recording (retrieve and delete) is governed by [room member permissions](#access-permissions-for-recordings).

## Access permissions for recordings { #access-permissions-for-recordings }

Who can retrieve and delete a room's recordings is governed by **[room member permissions](../room-members/overview.md)**, not by a room-wide setting:

- **`canRetrieveRecordings`** — list, play and download the room's recordings.
- **`canDeleteRecordings`** — delete the room's recordings.

By default, these permissions are assigned per role as follows:

| Role | Retrieve recordings | Delete recordings |
|------|:---:|:---:|
| **Moderator** | ✔ | ✔ |
| **Speaker** | ✔ | ✘ |

You can change these defaults per room (when [creating or editing](../rooms/management.md#create-rooms) it) or per member (with [custom permissions](../room-members/management.md#add-a-member)). In addition, **admins** can retrieve and delete the recordings of **any** room, and a **room owner** always has full access to the recordings of their own rooms.

## In this section

- [Creation & Management](management.md) — start and stop recordings during a meeting, browse, play, share, download and delete them, and the equivalent REST API operations.
- [Recording configuration](configuration.md) — enable recording per room and choose its layout, encoding and anonymous sharing.
