---
title: OpenVidu Meet Features Overview
description: A global picture of OpenVidu Meet features - Rooms, Meetings, Users, Room Members and Recordings - and how they relate.
---

# Features Overview

OpenVidu Meet is organized around a few core concepts. Understanding how they relate gives you the full picture of how the product works, whether you use it out of the box or embed it in your own application.

<div class="grid cards" markdown>

- :material-door-open:{ .lg .middle } **Rooms**

    ***

    A **Room** is a persistent virtual space that hosts meetings. You create and configure rooms (appearance, features, access control) and reuse them over time.

    [:octicons-arrow-right-24: Rooms](rooms/overview.md)

- :material-video:{ .lg .middle } **Meetings**

    ***

    A **Meeting** is the live session that takes place inside a room. It exists only while participants are connected, with features like recording, chat, captions and roles.

    [:octicons-arrow-right-24: Meetings](meetings/overview.md)

- :material-account-key:{ .lg .middle } **Users**

    ***

    **Users** are OpenVidu Meet accounts that log in to the app. Their role — **admin**, **room manager** or **room member** — determines what they can do, from full control of the app to accessing only the rooms they belong to.

    [:octicons-arrow-right-24: Users](users/overview.md)

- :material-account-group:{ .lg .middle } **Room Members**

    ***

    **Room members** are individuals granted access to a specific room. They can be **users** (with an account) or **guests** (identified or anonymous).

    [:octicons-arrow-right-24: Room Members](room-members/overview.md)

- :material-record-rec:{ .lg .middle } **Recordings**

    ***

    **Recordings** capture meetings and are stored on your server. They belong to the room where they were generated and can be played back, shared and downloaded.

    [:octicons-arrow-right-24: Recordings](recordings/overview.md)

</div>

## How it all fits together

- You start by creating a **room**. Each room carries its own configuration: visual [appearance](rooms/management.md#room-appearance), enabled features, recording settings and [access control](rooms/access.md).
- When someone opens a valid room access link and presses the join button, a **meeting** starts (or they join the ongoing one). Meetings are where the real-time communication happens.
- Access to a room is granted to its **room members**, of which there are three kinds (see [Room Members](room-members/overview.md)): **users** (accounts that log in), **identified guests** (a personal link, no login) and **anonymous guests** (a shared link, no login). The links and roles involved are described in [Room Access](rooms/access.md).
- **Users** are OpenVidu Meet accounts. **Room Members** bind users — or guests — to a specific room with a base role and optional custom permissions. Every member becomes a participant of the meetings held in the room.
- During a meeting, participants with appropriate permissions can start **recordings**, which remain available afterwards and inherit the room's access permissions.

!!! info "New to OpenVidu Meet?"

    If you haven't deployed it yet, start with the [Getting started](../getting-started/index.md) guide and try it [locally](../deployment/local.md).
