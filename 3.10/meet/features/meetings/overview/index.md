# Meetings

A **meeting** is a temporary session within a [room](https://openvidu.io/latest/meet/features/rooms/overview/index.md) where participants join in real time to communicate, share content and collaborate. Unlike rooms, which are persistent, a room can host many meetings over time.

- **It starts** when the first participant presses the join button.
- **It ends** 20 seconds after the last participant leaves, or as soon as it is ended for everyone. A participant who joins within those 20 seconds enters the same meeting.
- **One at a time**: a room holds a single meeting at any moment.

## How to join a meeting

A meeting starts as soon as a member opens a valid **room access link** and presses the join button into an empty room. How access to a room is granted, and how to copy and share its links, is covered in [Room Access](https://openvidu.io/latest/meet/features/rooms/access/index.md).

OpenVidu Meet users can also join directly from the "Rooms" page:

## In this section

Features marked **Per room** are turned on or off from the room configuration wizard when [creating or editing a room](https://openvidu.io/latest/meet/features/rooms/management/#create-rooms). **Deployment** marks a feature that needs extra setup in your OpenVidu deployment. The rest are always available during a meeting.

### Join and configure

- [Meeting lifecycle](https://openvidu.io/latest/meet/features/meetings/lifecycle/index.md): the views a member goes through, from opening an access link until the meeting ends.
- [Meeting configuration](https://openvidu.io/latest/meet/features/meetings/configuration/index.md): participant and duration limits, and whether participants join with microphone and camera on.
- [Locked Room](https://openvidu.io/latest/meet/features/meetings/locked-room/index.md): participants ask to join and wait until a moderator admits or rejects them. **Per room.**

### Moderate

- [Meeting Moderation](https://openvidu.io/latest/meet/features/meetings/moderation/index.md): mute participants' microphone, camera or screen share, and remove them from the meeting.
- [Role Management](https://openvidu.io/latest/meet/features/meetings/role-management/index.md): promote participants to moderator during a meeting, or demote them back.

### Participate

- [Raise Hand](https://openvidu.io/latest/meet/features/meetings/raise-hand/index.md): ask for a turn, with a queue everyone sees and moderators can lower. **Per room.**
- [Reactions](https://openvidu.io/latest/meet/features/meetings/reactions/index.md): react with an emoji that everyone sees for a few seconds. **Per room.**
- [Live Captions](https://openvidu.io/latest/meet/features/meetings/live-captions/index.md): real-time speech-to-text transcription. **Deployment.**
- [Virtual Background](https://openvidu.io/latest/meet/features/meetings/virtual-background/index.md): blur or replace the camera background. **Per room.**
- [Smart Layout](https://openvidu.io/latest/meet/features/meetings/smart-layout/index.md): a layout that adapts to the number of active participants.

### Broadcast and protect

- [Live Broadcast](https://openvidu.io/latest/meet/features/meetings/live-broadcast/index.md): stream the meeting live to YouTube, Twitch or any RTMP server. **Per room.**
- [E2E Encryption](https://openvidu.io/latest/meet/features/meetings/e2e-encryption/index.md): end-to-end encrypted audio, video and chat. **Per room.**
