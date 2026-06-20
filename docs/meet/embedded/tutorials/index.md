---
title: OpenVidu Meet Tutorials
description: Learn how to build a video conferencing application by easily integrating OpenVidu Meet into your web application.
---

# OpenVidu Meet Tutorials

OpenVidu Meet offers a robust and adaptable way to add video conferencing to your projects. These tutorials walk you through integrating it into your web application, step by step, using a small **Node.js and Express** backend and a plain **HTML/CSS/JavaScript** frontend.

!!! tip "Read them in order"

    The tutorials are **progressive**: each one builds on the previous tutorial, adding a new capability on top of the same application. If you are getting started with OpenVidu Meet, we recommend following them in order, from top to bottom.

## Integration

Different ways to integrate OpenVidu Meet into your own application:

- **[Direct Link](./integration/direct-link.md)**: redirect your users to the OpenVidu Meet interface through a direct URL. The simplest integration, with no embedding.
- **[WebComponent](./integration/webcomponent.md)**: embed the meeting directly inside your application with the `<openvidu-meet>` WebComponent.
- **[WebComponent Commands & Events](./integration/webcomponent-advanced.md)**: drive the embedded WebComponent programmatically through commands and react to meeting events.

!!! info "What about the iframe?"

    There is no dedicated tutorial for the iframe integration because it is essentially the same as the WebComponent: the WebComponent is a thin wrapper around an iframe that exposes the same capabilities through a friendlier API. If you prefer to embed OpenVidu Meet using a raw iframe, see the [iframe reference](../reference/iframe.md).

## Access

Different ways individuals can access a room:

- **[Anonymous Access](./access/anonymous-access.md)**: shared `moderator` or `speaker` links that anyone can use to access a room without identifying themselves.
- **[Identified Guests](./access/identified-guests.md)**: room members with a fixed name and a unique, revocable access link, with no account required.
- **[Users](./access/users.md)**: OpenVidu Meet accounts added to a room as members, who access the room by logging in with their own credentials.

## Advanced features

Server-side capabilities to get the most out of OpenVidu Meet:

- **[Recordings](./advanced-features/recordings.md)**: list, play and delete the recordings of your meetings.
- **[Webhooks](./advanced-features/webhooks.md)**: receive real-time notifications about room and recording events.
