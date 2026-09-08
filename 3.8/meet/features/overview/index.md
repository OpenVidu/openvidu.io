# Features Overview

OpenVidu Meet is organized around a few core concepts. Understanding how they relate gives you the full picture of how the product works, whether you use it out of the box or embed it in your own application.

- **Rooms**

  ______________________________________________________________________

  A **Room** is a persistent virtual space that hosts meetings. You create and configure rooms (appearance, features, access control) and reuse them over time.

  [Rooms](https://openvidu.io/3.8/meet/features/rooms/overview/index.md)

- **Meetings**

  ______________________________________________________________________

  A **Meeting** is the live session that takes place inside a room. It exists only while participants are connected, with features like recording, chat, captions and roles.

  [Meetings](https://openvidu.io/3.8/meet/features/meetings/overview/index.md)

- **Users**

  ______________________________________________________________________

  **Users** are OpenVidu Meet accounts that log in to the app. Their role — **admin**, **room manager** or **room member** — determines what they can do, from full control of the app to accessing only the rooms they belong to.

  [Users](https://openvidu.io/3.8/meet/features/users/overview/index.md)

- **Room Members**

  ______________________________________________________________________

  **Room members** are individuals granted access to a specific room. They can be **users** (with an account) or **guests** (identified or anonymous).

  [Room Members](https://openvidu.io/3.8/meet/features/room-members/overview/index.md)

- **Recordings**

  ______________________________________________________________________

  **Recordings** capture meetings and are stored on your server. They belong to the room where they were generated and can be played back, shared and downloaded.

  [Recordings](https://openvidu.io/3.8/meet/features/recordings/overview/index.md)

## How it all fits together

- You start by creating a **room**. Each room carries its own configuration: visual [appearance](https://openvidu.io/3.8/meet/features/rooms/management/#room-appearance), enabled features, recording settings and [access control](https://openvidu.io/3.8/meet/features/rooms/access/index.md).
- When someone opens a valid room access link and presses the join button, a **meeting** starts (or they join the ongoing one). Meetings are where the real-time communication happens.
- Access to a room is granted to its **room members**, of which there are three kinds (see [Room Members](https://openvidu.io/3.8/meet/features/room-members/overview/index.md)): **users** (accounts that log in), **identified guests** (a personal link, no login) and **anonymous guests** (a shared link, no login). The links and roles involved are described in [Room Access](https://openvidu.io/3.8/meet/features/rooms/access/index.md).
- **Users** are OpenVidu Meet accounts. **Room Members** bind users — or guests — to a specific room with a base role and optional custom permissions. Every member becomes a participant once they join a meeting held in the room.
- During a meeting, participants with appropriate permissions can start **recordings**, which remain available afterwards and inherit the room's access permissions.

New to OpenVidu Meet?

If you haven't deployed it yet, start with the [Getting started](https://openvidu.io/3.8/meet/getting-started/index.md) guide and try it [locally](https://openvidu.io/3.8/meet/deployment/local/index.md).
