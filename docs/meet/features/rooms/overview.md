---
title: Rooms in OpenVidu Meet
description: Understand what a room is in OpenVidu Meet and how it relates to meetings.
tags:
  - setupcustomgallery
---

# Rooms

A **Room** is a persistent virtual space designed to host one or more [meetings](../meetings/overview.md) in OpenVidu Meet. Think of it as a physical conference room — customizable with a name, appearance, and security settings.

## What is a Room

Rooms are the entry point to OpenVidu Meet. Every video call happens inside a room, and every room provides the configuration and access controls that govern the meetings that take place in it.

### Key principles

- Create a room first, then start meetings within it.
- One room can host just one meeting at a time, but it can be reused for multiple meetings over time.
- Every room has a **room link**. Users connecting to this link will either start a new meeting (if none is active) or join the ongoing meeting.

## Creation & Management

Administrators can create, edit, list and delete rooms from the **Rooms** page in OpenVidu Meet.

- [Create Rooms](creation-management.md#create-rooms) — set a name and configure recording, access control and features at creation time.
- [Edit Rooms](creation-management.md#edit-rooms) — modify any room setting while no meeting is active.
- [List Rooms](creation-management.md#list-rooms) — browse all rooms, start meetings, access recordings and share links.
- [Delete Rooms](creation-management.md#delete-rooms) — remove rooms manually or schedule automatic deletion.

## Room Configuration

Each room can be configured independently to match your branding and access requirements.

- [Room Appearance](appearance.md) — customise the color scheme of the meeting view.
- [Room Access](access.md) — manage room links per participant role and administrator credentials.

## Room REST API

Every possible action against a room can be done through the [OpenVidu Meet REST API](../../embedded/reference/rest-api.md):

| Operation | HTTP Method | Reference |
|-----------|-------------|-----------|
| Create a room | POST | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/createRoom){:target="_blank"} |
| Get a room | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRoom){:target="_blank"} |
| Get all rooms | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRooms){:target="_blank"} |
| Delete a room | DELETE | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/deleteRoom){:target="_blank"} |
| Bulk delete rooms | DELETE | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/bulkDeleteRooms){:target="_blank"} |
| Get room config | GET | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRoomConfig){:target="_blank"} |
| Update room config | PUT | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/updateRoomConfig){:target="_blank"} |
