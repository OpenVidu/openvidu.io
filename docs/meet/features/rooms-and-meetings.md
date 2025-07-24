## Room vs meeting

It is important to understand these core concepts of OpenVidu Meet:

- A **room** is a persistent virtual space used to host one or more meetings. Its real-world counterpart is a physical conference room in a building: you can lock it, change its appearance, etc.
- A **meeting** is a temporary session that occurs within a room, where participants can join and interact in real-time. Its real-world counterpart is a scheduled event that takes place in that room, where authorized people can join, talk, and share information.

One room can host one meeting at a time, but it can be reused for multiple meetings over time.

## Creating a room

You can create a new room directly from the "Rooms" view in OpenVidu Meet.

<video class="round-corners" src="../../../assets/videos/meet/meet-rooms-dark.mp4#only-dark" defer muted playsinline autoplay loop async></video>

Rooms are configurable in multiple ways:

1. Name them.
2. Set up recording.
3. Change its appearance.
4. ...

!!! note "You can also programmatically create rooms using [OpenVidu Meet REST API](../embedded/reference/rest.md)"

Available rooms are all listed in the "Rooms" view. From there you can:

- Start a meeting in a room.
- Edit the room settings.
- Delete the room.
- Access the room's recordings.
- Share room links with different permissions (see [Users and permissions](users-and-permissions.md)).

<video class="round-corners" src="../../../assets/videos/meet/room-actions.mp4" defer muted playsinline autoplay loop async></video>

### Room auto-deletion

Rooms can be created with an **auto-deletion date**. This helps keeping OpenVidu Meet clean and organized, avoiding clutter from old rooms that are no longer needed.

![Room auto-deletion](../../../assets/images/meet/rooms-and-meetings/room-auto-deletion.png)

## Starting a meeting

A meeting will start as soon as a participant enters the room using a valid **link**.

You can join a meeting directly from the "Rooms" view in OpenVidu Meet:

<video class="round-corners" src="../../../assets/videos/meet/join-meeting.mp4" defer muted playsinline autoplay loop async></video>

Or you can copy the room link and share it with other participants. There are multiple room links, each granting different permissions to the participants (for more information, see [Users and permissions](users-and-permissions.md)):

<video class="round-corners" src="../../../assets/videos/meet/share-room-link.mp4" defer muted playsinline autoplay loop async></video>