# Rooms

A **Room** is a persistent virtual space designed to host one or more [meetings](https://openvidu.io/3.8.0/meet/features/meetings/overview/index.md) in OpenVidu Meet. Think of it as a physical conference room, customizable with a name, appearance, and security settings.

Rooms are the entry point to OpenVidu Meet: every video call happens inside a room, and every room provides the configuration and access controls that govern the meetings that take place in it.

## Key principles

- Create a room first, then start meetings within it.
- One room can host just one meeting at a time, but it can be reused for multiple meetings over time.
- Every room has different **access links**. Anyone connecting to these links and pressing the join button will either start a new meeting (if none is active) or join the ongoing meeting.

## In this section

- [Creation & Management](https://openvidu.io/3.8.0/meet/features/rooms/management/index.md) — create, edit, list and delete rooms from the OpenVidu Meet app, configure their features and appearance, and the equivalent REST API operations.
- [Room Access](https://openvidu.io/3.8.0/meet/features/rooms/access/index.md) — how individuals access a room as [room members](https://openvidu.io/3.8.0/meet/features/room-members/overview/index.md) (anonymous, user and identified-guest access links) and the predefined roles (`Moderator` and `Speaker`).
