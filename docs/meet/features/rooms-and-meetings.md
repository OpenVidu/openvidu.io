---
title: Rooms and meetings in OpenVidu Meet
description: Understand the difference between rooms and meetings in OpenVidu Meet, and learn how to
tags:
  - setupcustomgallery
---

# Rooms and meetings in OpenVidu Meet

Understanding **Rooms** and **Meetings** is essential to getting the most out of OpenVidu Meet. These core concepts define how users interact and how video calls are organized.


## Room vs meeting

- **Room**: A persistent virtual space designed to host one or more meetings. Think of it as a physical conference room—customizable with a name, appearance, and security settings.
- **Meeting**: A temporary session within a room where users join in real-time to communicate, share content, and collaborate. It's like a scheduled event in a conference room.


### Key principles

- Create a room first, then start meetings within it.
- One room can host just one meeting at a time, but it can be reused for multiple meetings over time.
- Every room has different **access links**, each with specific permissions.
- Users pressing the "Join" button after accessing a room will either start a new meeting (if none is active) or join the ongoing meeting.

## Rooms

### Creating a room

OpenVidu Meet internal users with permissions to create and manage rooms can create a new room directly from the "Rooms" page in OpenVidu Meet console. Each room requires a name and can be customized with Advanced Setup options:

- Set up an [auto-deletion date](#room-auto-deletion) and configure [auto-deletion policies](#room-auto-deletion-policies).
- Enable/disable features like recording, chat, virtual backgrounds, and E2EE (end-to-end encryption).
- Configure permissions for each role (moderator and speaker).
- Enable/disable anonymous access for each role.

<a class="glightbox" href="../../../assets/videos/meet/meet-rooms-dark.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="../../../assets/videos/meet/meet-rooms-dark.mp4#only-dark" loading="lazy" defer muted playsinline autoplay loop async></video></a>
<a class="glightbox" href="../../../assets/videos/meet/meet-rooms-light.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="../../../assets/videos/meet/meet-rooms-light.mp4#only-light" loading="lazy" defer muted playsinline autoplay loop async></video></a>

!!! info
    Learn more about OpenVidu Meet internal users and their permissions in [OpenVidu Meet internal users](users-and-permissions.md#openvidu-meet-internal-users).

All OpenVidu Meet internal users can access rooms they are members of, as well as their associated recordings, from the **Rooms** page. Additionally, users with permissions to manage rooms can:

- Share room access links with different permissions (see [Users and permissions](users-and-permissions.md)).
- Edit room settings (if no meeting is active).
- Delete rooms individually or in bulk.

<a class="glightbox" href="../../../assets/videos/meet/room-actions-dark.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="../../../assets/videos/meet/room-actions-dark.mp4#only-dark" loading="lazy" defer muted playsinline autoplay loop async></video></a>
<a class="glightbox" href="../../../assets/videos/meet/room-actions-light.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="../../../assets/videos/meet/room-actions-light.mp4#only-light" loading="lazy" defer muted playsinline autoplay loop async></video></a>

### Editing a room

Modify room settings anytime from the **Rooms** page if no meeting is active. You can:

- Enable/disable features like recording, chat, virtual backgrounds, and E2EE (end-to-end encryption).
- Configure permissions for each role (moderator and speaker).
- Enable/disable anonymous access for each role.

<a class="glightbox" href="../../../assets/images/meet/rooms-and-meetings/edit-room.png" data-type="image" data-desc-position="bottom" data-gallery="gallery3"><img src="../../../assets/images/meet/rooms-and-meetings/edit-room.png" loading="lazy" class="control-height round-corners"/></a>

### Deleting a room

Rooms can be deleted individually or in bulk from the **Rooms** page. Deleting a room removes it and all associated data.

<a class="glightbox" href="../../../assets/images/meet/rooms-and-meetings/delete-room.png" data-type="image" data-desc-position="bottom" data-gallery="gallery5"><img src="../../../assets/images/meet/rooms-and-meetings/delete-room.png" loading="lazy" class="round-corners"/></a>

#### Room auto-deletion

Rooms can be configured with an **auto-deletion date**. You can set this date when [creating a room](#creating-a-room). This helps keeping OpenVidu Meet clean and organized, avoiding clutter from old rooms that are no longer needed.

<a class="glightbox" href="../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery3"><img src="../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-dark.png#only-dark" loading="lazy" class="control-height round-corners"/></a>
<a class="glightbox" href="../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery3"><img src="../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-light.png#only-light" loading="lazy" class="control-height round-corners"/></a>

#### Room auto-deletion policies

When the auto-deletion date is reached, the room will be processed to be deleted. The **Auto-deletion policies** determine how to handle active meetings and stored recordings when attempting to delete the room:

- **Active meetings policy**
    - `Force`: the meeting will be immediately ended without waiting for participants to leave, and the room will be deleted.
    - `When meeting ends`: the room will be deleted after the active meeting ends.
- **Recordings policy**
    - `Force`: the room and all its recordings will be deleted.
    - `Close`: the room will be closed instead of deleted, maintaining its recordings.

<a class="glightbox" href="../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-policies-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery3"><img src="../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-policies-dark.png#only-dark" loading="lazy" class="control-height round-corners"/></a>
<a class="glightbox" href="../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-policies-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery3"><img src="../../../assets/images/meet/rooms-and-meetings/room-auto-deletion-policies-light.png#only-light" loading="lazy" class="control-height round-corners"/></a>


### Room access links

There are two types of **room access links** that grant access to them:

- **Anonymous access links**: Predefined URLs that allow external users to access a room without identification, with permissions associated to a specific role (Moderator or Speaker). These links can be shared with any user, as long as anonymous access for that role is not explicitly disabled.
- **Room member links**: Custom URLs associated with a specific user with personalized permissions. For external users, each member has a unique URL that should be delivered only to them. For OpenVidu Meet internal users, the URL is the same for all members of the room, and membership is determined by their authenticated user account.

See [Users and permissions](users-and-permissions.md) for detailed information about users, roles, permissions, and how to create room members.

#### Getting room access links

##### From the "Rooms" page

OpenVidu Meet internal users with permissions to manage rooms can share anonymous room access links for each role from the "Rooms" page.

<a class="glightbox" href="../../../assets/videos/meet/share-room-link.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery8"><video class="round-corners" src="../../../assets/videos/meet/share-room-link.mp4" loading="lazy" defer muted playsinline autoplay loop async></video></a>

##### From an active meeting

Participants with the `canShareAccessLinks` permission can share room access links from the active meeting view.

<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/share-room-link.png" data-type="image" data-desc-position="bottom" data-gallery="gallery5"><img src="../../../assets/images/meet/users-and-permissions/share-room-link.png" loading="lazy" class="round-corners"/></a>

!!! info
    Links copied from the meeting view will always grant anonymous access to the room with `Speaker` role. If necessary, particiapnts with the `canMakeModerator` permission can promote other participants to `Moderator` during the meeting. See [Promoting participants to moderator](users-and-permissions.md#promoting-participants-to-moderator) for more information.

##### From the REST API

Anonymous access links are available in properties `anonymous.moderator.accessUrl` and `anonymous.speaker.accessUrl` of object [MeetRoom :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/schemas/MeetRoom){:target="_blank"}.

The room owner and internal user members can access the room through the general authenticated access URL available in property `accessUrl` of [MeetRoom :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/schemas/MeetRoom){:target="_blank"}. For external user members, each member has their own unique access URL available in property `accessUrl` of each [MeetRoomMember :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/schemas/MeetRoomMember){:target="_blank"} object. See [Room members](users-and-permissions.md#room-members) for more information.

### Room visual customization

Rooms can be customized to fit your branding needs. As for now, you can setup the color scheme of your rooms from the "Configuration" page.

<a class="glightbox" href="../../../assets/images/meet/rooms-and-meetings/visual-customization-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery14"><img src="../../../assets/images/meet/rooms-and-meetings/visual-customization-dark.png#only-dark" loading="lazy" class="control-height round-corners"/></a>
<a class="glightbox" href="../../../assets/images/meet/rooms-and-meetings/visual-customization-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery14"><img src="../../../assets/images/meet/rooms-and-meetings/visual-customization-light.png#only-light" loading="lazy" class="control-height round-corners"/></a>

You can set separately the color of:

- **Main background**: background color of the meeting view.
- **Main controls**: colors for the main control buttons (mic, camera, etc.)
- **Secondary elements**: colors for logos, icons, borders and subtle details.
- **Highlights & accents**: colors for active states and highlighted items.
- **Panels & dialogs**: background color for side panels and dialog boxes.

You can also choose between a light and a dark background style, to ensure the displayed text is always readable after applying your color scheme.

### Room REST API

Every possible action against a room can be done through [OpenVidu Meet REST API](../embedded/reference/rest-api.md):

| Operation | HTTP Method | Reference |
|-----------|-------------|-----------|
| Create a room | POST | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/createRoom){:target="_blank"} |
| Get all rooms | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRooms){:target="_blank"} |
| Bulk delete rooms | DELETE | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/bulkDeleteRooms){:target="_blank"} |
| Get a room | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRoom){:target="_blank"} |
| Delete a room | DELETE | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/deleteRoom){:target="_blank"} |
| Get room config | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRoomConfig){:target="_blank"} |
| Update room config | PUT | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/updateRoomConfig){:target="_blank"} |
| Update roles permissions for a room | PUT | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/updateRoomRoles){:target="_blank"} |
| Update anonymous access config for a room | PUT | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/updateRoomAnonymous){:target="_blank"} |
| Update room status | PUT | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/updateRoomStatus){:target="_blank"} |
| Add a member to a room | POST | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/addRoomMember){:target="_blank"} |
| Get all members of a room | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRoomMembers){:target="_blank"} |
| Get a room member | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRoomMember){:target="_blank"} |
| Update a room member | PUT | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/updateRoomMember){:target="_blank"} |
| Delete a room member | DELETE | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/deleteRoomMember){:target="_blank"} |

## Meetings

### Starting a meeting

A meeting will start as soon as a user accesses an empty room using a valid **room access link** and presses then "Join" button. You can learn everything about room access links [here](#room-access-links).

OpenVidu Meet internal users can access rooms directly from the "Rooms" page:

<a class="glightbox" href="../../../assets/videos/meet/join-meeting.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery7"><video class="round-corners" src="../../../assets/videos/meet/join-meeting.mp4" loading="lazy" defer muted playsinline autoplay loop async></video></a>

They can also copy an anonymous room access link and share it with external users:

<a class="glightbox" href="../../../assets/videos/meet/share-room-link.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery8"><video class="round-corners" src="../../../assets/videos/meet/share-room-link.mp4" loading="lazy" defer muted playsinline autoplay loop async></video></a>

### Meeting Lifecycle

Meetings consist of different views:

#### Join view

This is the first view users see when accessing a room. It allows setting a nickname before joining the meeting. If the user has the required permissions, they can also access the [Recording view](#recording-view) of this room from here.

<a class="glightbox" href="../../../assets/images/meet/rooms-and-meetings/join-view-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery9"><img src="../../../assets/images/meet/rooms-and-meetings/join-view-dark.png#only-dark" loading="lazy" class="control-height round-corners"/></a>
<a class="glightbox" href="../../../assets/images/meet/rooms-and-meetings/join-view-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery9"><img src="../../../assets/images/meet/rooms-and-meetings/join-view-light.png#only-light" loading="lazy" class="control-height round-corners"/></a>

#### Device view

This view allows users tuning their microphone and camera before joining the meeting, as well as setting a virtual background.

<a class="glightbox" href="../../../assets/videos/meet/device-view-dark.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery10"><video class="round-corners" src="../../../assets/videos/meet/device-view-dark.mp4#only-dark" loading="lazy" defer muted playsinline autoplay loop async></video></a>
<a class="glightbox" href="../../../assets/videos/meet/device-view-light.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery10"><video class="round-corners" src="../../../assets/videos/meet/device-view-light.mp4#only-light" loading="lazy" defer muted playsinline autoplay loop async></video></a>

#### Meeting view

This is the main view of the meeting, where participants can interact with each other.

<a class="glightbox" href="../../../assets/images/meet/rooms-and-meetings/room-view.png" data-type="image" data-desc-position="bottom" data-gallery="gallery11"><img src="../../../assets/images/meet/rooms-and-meetings/room-view.png" loading="lazy" class="round-corners"/></a>

#### Recording view

This view allows to manage all recordings of the room. Users with the required permissions can review, play, download, delete, and share each recording via a link.

<a class="glightbox" href="../../../assets/images/meet/rooms-and-meetings/recording-view-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery12"><img src="../../../assets/images/meet/rooms-and-meetings/recording-view-dark.png#only-dark" loading="lazy" class="control-height round-corners"/></a>
<a class="glightbox" href="../../../assets/images/meet/rooms-and-meetings/recording-view-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery12"><img src="../../../assets/images/meet/rooms-and-meetings/recording-view-light.png#only-light" loading="lazy" class="control-height round-corners"/></a>

!!! info
    Recordings can also be accessed from the "Recordings" page in OpenVidu Meet console. See [Managing recordings](./recordings.md#managing-recordings).

#### End view

This view is shown to a participant when the meeting ends, at least for that participant. It informs about the specific reason why the meeting ended (a moderator ended it, the participant was kicked from the meeting, etc.).

<a class="glightbox" href="../../../assets/images/meet/rooms-and-meetings/end-view-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery13"><img src="../../../assets/images/meet/rooms-and-meetings/end-view-dark.png#only-dark" loading="lazy" class="control-height round-corners"/></a>
<a class="glightbox" href="../../../assets/images/meet/rooms-and-meetings/end-view-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery13"><img src="../../../assets/images/meet/rooms-and-meetings/end-view-light.png#only-light" loading="lazy" class="control-height round-corners"/></a>