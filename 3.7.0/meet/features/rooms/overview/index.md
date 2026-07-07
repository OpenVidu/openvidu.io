# Rooms

A **Room** is a persistent virtual space designed to host one or more [meetings](https://openvidu.io/3.7.0/meet/features/meetings/overview/index.md) in OpenVidu Meet. Think of it as a physical conference room — customizable with a name, appearance, and security settings.

## What is a Room

Rooms are the entry point to OpenVidu Meet. Every video call happens inside a room, and every room provides the configuration and access controls that govern the meetings that take place in it.

### Key principles

- Create a room first, then start meetings within it.
- One room can host just one meeting at a time, but it can be reused for multiple meetings over time.
- Every room has a **room link**. Users connecting to this link will either start a new meeting (if none is active) or join the ongoing meeting.

## Creation & Management

Administrators can create, edit, list and delete rooms from the **Rooms** page in OpenVidu Meet.

- [Create Rooms](https://openvidu.io/3.7.0/meet/features/rooms/creation-management/#create-rooms) — set a name and configure recording, access control and features at creation time.
- [Edit Rooms](https://openvidu.io/3.7.0/meet/features/rooms/creation-management/#edit-rooms) — modify any room setting while no meeting is active.
- [List Rooms](https://openvidu.io/3.7.0/meet/features/rooms/creation-management/#list-rooms) — browse all rooms, start meetings, access recordings and share links.
- [Delete Rooms](https://openvidu.io/3.7.0/meet/features/rooms/creation-management/#delete-rooms) — remove rooms manually or schedule automatic deletion.

## Room Configuration

Each room can be configured independently to match your branding and access requirements.

- [Room Appearance](https://openvidu.io/3.7.0/meet/features/rooms/appearance/index.md) — customise the color scheme of the meeting view.
- [Room Access](https://openvidu.io/3.7.0/meet/features/rooms/access/index.md) — manage room links per participant role and administrator credentials.

## Room REST API

Every possible action against a room can be done through the [OpenVidu Meet REST API](https://openvidu.io/3.7.0/meet/embedded/reference/rest-api/index.md):

| Operation          | HTTP Method | Reference                                                                                            |
| ------------------ | ----------- | ---------------------------------------------------------------------------------------------------- |
| Create a room      | POST        | [Reference](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/createRoom)       |
| Get a room         | GET         | [Reference](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/getRoom)          |
| Get all rooms      | GET         | [Reference](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/getRooms)         |
| Delete a room      | DELETE      | [Reference](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/deleteRoom)       |
| Bulk delete rooms  | DELETE      | [Reference](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/bulkDeleteRooms)  |
| Get room config    | GET         | [Reference](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/getRoomConfig)    |
| Update room config | PUT         | [Reference](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/updateRoomConfig) |
