# OpenVidu Meet Tutorials

OpenVidu Meet offers a robust and adaptable way to add video conferencing to your projects. These tutorials walk you through integrating it into your web application, step by step, using a small **Node.js and Express** backend and a plain **HTML/CSS/JavaScript** frontend.

Read them in order

The tutorials are **progressive**: each one builds on the previous tutorial, adding a new capability on top of the same application. If you are getting started with OpenVidu Meet, we recommend following them in order, from top to bottom.

## Embedding options

Different ways to embed OpenVidu Meet into your own application:

- **[Direct Link](https://openvidu.io/3.8.0/meet/embedded/tutorials/embedding-options/direct-link/index.md)**: redirect your users to the OpenVidu Meet interface through a direct URL. The simplest integration, with no embedding.
- **[WebComponent](https://openvidu.io/3.8.0/meet/embedded/tutorials/embedding-options/webcomponent/index.md)**: embed the meeting directly inside your application with the `<openvidu-meet>` WebComponent.
- **[WebComponent Commands & Events](https://openvidu.io/3.8.0/meet/embedded/tutorials/embedding-options/webcomponent-advanced/index.md)**: drive the embedded WebComponent programmatically through commands and react to meeting events.

What about the iframe?

There is no dedicated tutorial for the iframe integration because it is essentially the same as the WebComponent: the WebComponent is a thin wrapper around an iframe that exposes the same capabilities through a friendlier API. If you prefer to embed OpenVidu Meet using a raw iframe, see the [iframe reference](https://openvidu.io/3.8.0/meet/embedded/reference/iframe/index.md).

## Access

Different ways individuals can access a room:

- **[Anonymous Access](https://openvidu.io/3.8.0/meet/embedded/tutorials/access/anonymous-access/index.md)**: shared `moderator` or `speaker` links that anyone can use to access a room without identifying themselves.
- **[Identified Guests](https://openvidu.io/3.8.0/meet/embedded/tutorials/access/identified-guests/index.md)**: room members with a fixed name and a unique, revocable access link, with no account required.
- **[Users](https://openvidu.io/3.8.0/meet/embedded/tutorials/access/users/index.md)**: OpenVidu Meet accounts added to a room as members, who access the room by logging in with their own credentials.

## Advanced features

Server-side capabilities to get the most out of OpenVidu Meet:

- **[Recordings](https://openvidu.io/3.8.0/meet/embedded/tutorials/advanced-features/recordings/index.md)**: list, play and delete the recordings of your meetings.
- **[Webhooks](https://openvidu.io/3.8.0/meet/embedded/tutorials/advanced-features/webhooks/index.md)**: receive real-time notifications about room and recording events.
