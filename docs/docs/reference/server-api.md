---
title: "OpenVidu server API reference"
description: "Every room and participant operation your backend can call, the grant each one requires, and how the API is authenticated."
---

# Server API

The server API is what your **application server** uses to manage rooms from the outside: create and delete them, list who is in them, mute a track, remove a participant, push data into a room. It is the counterpart to the client SDKs, which act from *inside* a room as a participant.

The API is **Twirp-based HTTP** — plain `POST` requests with a JSON or protobuf body — so any language can call it, and OpenVidu's server SDKs wrap it for you.

## Authentication

Same [access token](./access-tokens.md) mechanism as a participant, with different grants. A server-side token carries no `roomJoin`; it carries the administrative grants for the operations it needs, and it never leaves your backend.

```javascript
const at = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET);
at.addGrant({ roomAdmin: true, room: "my-room" });
```

The server SDKs mint this token for you when you construct a client with your key and secret.

## Operations

Every operation states the grant it requires. `roomAdmin` is scoped: it applies to the room named in the token's `room` claim.

### Rooms

| Operation | Grant | What it does |
| --- | --- | --- |
| `CreateRoom` | `roomCreate` | Creates a room with explicit settings. **Optional** — a room is created automatically the first time a client connects to it. Use it when you need to set options up front, such as auto-egress or an empty-room timeout |
| `ListRooms` | `roomList` | Lists the rooms currently active on the server |
| `DeleteRoom` | `roomCreate` | Deletes a room **and disconnects everyone in it** |
| `UpdateRoomMetadata` | `roomAdmin` | Replaces the room's metadata. The change is broadcast to every participant |

### Participants

| Operation | Grant | What it does |
| --- | --- | --- |
| `ListParticipants` | `roomAdmin` | Lists the participants in a room |
| `GetParticipant` | `roomAdmin` | Returns one participant by identity |
| `RemoveParticipant` | `roomAdmin` | Disconnects a participant. They can reconnect with a valid token — to keep them out, stop issuing tokens |
| `UpdateParticipant` | `roomAdmin` | Changes a participant's metadata, name or permissions. Broadcast to the room |
| `MutePublishedTrack` | `roomAdmin` | Mutes or unmutes one of a participant's published tracks |
| `UpdateSubscriptions` | `roomAdmin` | Subscribes or unsubscribes a participant to specific tracks, from the server side |

### Data

| Operation | Grant | What it does |
| --- | --- | --- |
| `SendData` | `roomAdmin` | Sends a data message over the data channel to a room, or to specific participants in it |
| `PerformRpc` | `roomAdmin` | Invokes an RPC method a participant has registered |

### Not available when self-hosting

| Operation | |
| --- | --- |
| `ForwardParticipant` | Forwards a participant's tracks into another room |
| `MoveParticipant` | Moves a participant from one room to another |

Both are marked **cloud-only** in the protocol and are not part of a self-hosted deployment, OpenVidu's included. They would also require the `destinationRoom` grant. Listed here so their absence is not a surprise.

## Choosing between the server API and the client SDK

Both can mute a track or update metadata, and the difference is who is acting:

- **Server API** — your backend acting on the room from outside, with administrative authority. Nobody has to be connected for it to work. This is where moderation belongs: your backend already knows which of your users is a moderator, and the client cannot forge it.
- **Client SDK** — a participant acting within the limits its own token grants. A participant with `canUpdateOwnMetadata` can change its own metadata; it cannot mute someone else unless your backend does it for them.

The practical pattern for a "mute everyone" button: the client calls **your** endpoint, your endpoint checks that this user is a moderator, and then calls `MutePublishedTrack`.

## Related

- [Access tokens reference](./access-tokens.md) — the grants above, in detail
- [How to develop your OpenVidu app](../developing-your-openvidu-app/how-to.md) — worked snippets for the common operations
- [Application server tutorials](../tutorials/application-server/index.md) — complete servers in nine languages
- [Client SDK reference](./client-sdk.md) — the same room, seen from inside
- Your server SDK's API documentation, for exact method names and argument shapes in your language
