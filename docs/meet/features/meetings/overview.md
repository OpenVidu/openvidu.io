---
title: "Meetings in OpenVidu Meet"
description: "What a meeting is in OpenVidu Meet: the live session held inside a room, when it starts and ends, and how participants join one."
page_features:
  - lazyvideo
---

# Meetings

A **meeting** is a temporary session within a [room](../rooms/overview.md) where participants join in real time to communicate, share content and collaborate. Unlike rooms, which are persistent, a room can host many meetings over time.

- **It starts** when the first participant presses the join button.
- **It ends** 20 seconds after the last participant leaves, or as soon as it is ended for everyone. A participant who joins within those 20 seconds enters the same meeting.
- **One at a time**: a room holds a single meeting at any moment.

## How to join a meeting

A meeting starts as soon as a member opens a valid **room access link** and presses the join button into an empty room. How access to a room is granted, and how to copy and share its links, is covered in [Room Access](../rooms/access.md).

OpenVidu Meet users can also join directly from the "Rooms" page:

<a class="glightbox" href="/assets/videos/meet/meetings/overview/access-room-dark.mp4" data-type="video" data-gallery="dark"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/overview/access-room-dark.mp4#only-dark" preload="none" muted playsinline loop></video></a>
<a class="glightbox" href="/assets/videos/meet/meetings/overview/access-room-light.mp4" data-type="video" data-gallery="light"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/overview/access-room-light.mp4#only-light" preload="none" muted playsinline loop></video></a>

## In this section

Features marked **Per room** are turned on or off from the room configuration wizard when [creating or editing a room](../rooms/management.md#create-rooms). **Deployment** marks a feature that needs extra setup in your OpenVidu deployment. The rest are always available during a meeting.

### Join and configure

- [Meeting lifecycle](lifecycle.md): the views a member goes through, from opening an access link until the meeting ends.
- [Meeting configuration](configuration.md): participant and duration limits, and whether participants join with microphone and camera on.
- [Locked Room](locked-room.md): participants ask to join and wait until a moderator admits or rejects them. **Per room.**

### Moderate

- [Meeting Moderation](moderation.md): mute participants' microphone, camera or screen share, and remove them from the meeting.
- [Role Management](role-management.md): promote participants to moderator during a meeting, or demote them back.

### Participate

- [Raise Hand](raise-hand.md): ask for a turn, with a queue everyone sees and moderators can lower. **Per room.**
- [Reactions](reactions.md): react with an emoji that everyone sees for a few seconds. **Per room.**
- [Live Captions](live-captions.md): real-time speech-to-text transcription. **Deployment.**
- [Virtual Background](virtual-background.md): blur or replace the camera background. **Per room.**
- [Smart Layout](smart-layout.md): a layout that adapts to the number of active participants.

### Broadcast and protect

- [Live Broadcast](live-broadcast.md): stream the meeting live to YouTube, Twitch or any RTMP server. **Per room.**
- [E2E Encryption](e2e-encryption.md): end-to-end encrypted audio, video and chat. **Per room.**
