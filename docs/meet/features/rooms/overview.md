---
title: Rooms in OpenVidu Meet
description: Understand what a room is in OpenVidu Meet and how it relates to meetings.
tags:
    - setupcustomgallery
---

# Rooms

A **Room** is a persistent virtual space designed to host one or more [meetings](../meetings/overview.md) in OpenVidu Meet. Think of it as a physical conference room, customizable with a name, appearance, and security settings.

Rooms are the entry point to OpenVidu Meet: every video call happens inside a room, and every room provides the configuration and access controls that govern the meetings that take place in it.

## Key principles

- Create a room first, then start meetings within it.
- One room can host just one meeting at a time, but it can be reused for multiple meetings over time.
- Every room has different **access links**. Anyone connecting to these links will either start a new meeting (if none is active) or join the ongoing meeting.

## In this section

- [Creation & Management](management.md) — create, edit, list and delete rooms from the OpenVidu Meet app, configure their features and appearance, and the equivalent REST API operations.
- [Room Access](access.md) — how individuals join a room as [room members](../room-members/overview.md) (anonymous, user and identified-guest access links) and the predefined roles (`Moderator` and `Speaker`).
