# Meetings

A **Meeting** is a temporary session within a [room](https://openvidu.io/3.7.0/meet/features/rooms/overview/index.md) where participants join in real-time to communicate, share content, and collaborate. It starts when the first participant connects and ends when the last one leaves — or when a moderator explicitly closes it.

## What is a Meeting

Every meeting takes place inside a room. Unlike rooms (which are persistent), a meeting only exists while at least one participant is connected. The same room can host many meetings over time, one at a time.

## How to join a meeting

A meeting starts as soon as a participant opens a valid **room link** into an empty room. You can learn everything about room links [here](https://openvidu.io/3.7.0/meet/features/rooms/access/#room-links).

Users with access to OpenVidu Meet can join a meeting directly from the "Rooms" page:

\[[](../../../../assets/videos/meet/join-meeting.mp4)\](https://openvidu.io/3.7.0/assets/videos/meet/join-meeting.mp4)

Info

Doing this simply opens a new tab with a `Moderator` room link.

Users can also copy a room link and share it with external participants:

\[[](../../../../assets/videos/meet/share-room-link.mp4)\](https://openvidu.io/3.7.0/assets/videos/meet/share-room-link.mp4)

## Meeting lifecycle

From the moment a participant opens a room link until the meeting ends, they move through a series of views. See [Meeting lifecycle](https://openvidu.io/3.7.0/meet/features/meetings/lifecycle/index.md) for a full description of the Join, Device, Meeting, Recording and End views.

## Meeting features

OpenVidu Meet provides a set of built-in features that enhance accessibility and collaboration during a live session:

- [Live Captions](https://openvidu.io/3.7.0/meet/features/meetings/live-captions/index.md) — real-time speech-to-text transcription powered by the OpenVidu Speech Processing Agent.
- [Smart Layout](https://openvidu.io/3.7.0/meet/features/meetings/smart-layout/index.md) — dynamic layout that adapts automatically to the number of active participants.
- [Role Management](https://openvidu.io/3.7.0/meet/features/meetings/role-management/index.md) — Moderator and Speaker roles with per-room assignment via room links, and runtime role changes.
- [E2E Encryption](https://openvidu.io/3.7.0/meet/features/meetings/e2e-encryption/index.md) — end-to-end encrypted audio, video and chat so only participants can decrypt the content.
- [Virtual Background](https://openvidu.io/3.7.0/meet/features/meetings/virtual-background/index.md) — blur or replace the camera background before or during a meeting.
