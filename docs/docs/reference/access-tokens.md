---
title: "OpenVidu access tokens reference"
description: "Every claim and video grant an OpenVidu access token carries, how your application server signs one, and how long it stays valid."
---

# Access tokens

A client never authenticates against OpenVidu directly. It connects to a Room with an **access token**: a JWT that **your application server** signs with your deployment's API secret. The token says who the participant is and what they are allowed to do, and OpenVidu enforces exactly that.

OpenVidu is API-compatible with LiveKit, so any LiveKit server SDK mints valid OpenVidu tokens. The tutorials show a working token endpoint in nine languages:

[:octicons-arrow-right-24: Application server tutorials](../tutorials/application-server/index.md)

!!! warning "The API secret never leaves your server"

    Anyone holding the secret can mint a token with any identity and any permission. Keep it in your application server's environment, never in a browser or mobile bundle, and never return it from an endpoint.

## API key and secret

Tokens are signed with the key pair configured in your deployment:

| Parameter | Where it lives |
| --- | --- |
| `LIVEKIT_API_KEY` | `openvidu.env` — see the [configuration reference](../self-hosting/configuration/reference.md) |
| `LIVEKIT_API_SECRET` | `openvidu.env` — same file |

A [local deployment](../self-hosting/local.md) starts with the development pair `devkey` / `secret`, which is why every tutorial falls back to those values. Any real deployment generates its own.

## Anatomy of a token

The token is a JWT signed with **HS256** using your API secret. Alongside the grants below, OpenVidu sets three standard JWT claims:

| Claim | Value |
| --- | --- |
| `iss` | Your API key — this is how the server knows which secret to verify with |
| `sub` | The participant identity |
| `nbf` / `exp` | Not-before and expiry. Validity defaults to **6 hours** when you don't set it explicitly |

The expiry only bounds how long the token can be *used to connect*. A participant already in a Room is not disconnected when their token expires.

### Token claims

| Claim | Type | What it does |
| --- | --- | --- |
| `identity` | string | Unique identifier of the participant inside the Room. Two connections with the same identity in the same Room conflict — the newer one displaces the older |
| `name` | string | Display name. Unlike `identity`, it needs not be unique |
| `metadata` | string | Opaque application data attached to the participant, delivered to every other participant in the Room. A JSON string is the usual choice |
| `attributes` | map of string to string | Key/value data attached to the participant, individually updatable during the Room |
| `video` | object | The video grants — the permission set, detailed below |
| `sha256` | string | Base64 SHA-256 of a request body, used to bind a token to a specific payload. This is the mechanism behind [webhook validation](./webhooks.md) |
| `roomConfig` | object | Configuration applied to the Room if this token is the one that creates it |
| `roomPreset` | string | Name of a server-side preset to apply to the Room instead of an inline `roomConfig` |
| `kind` | string | Participant kind, used to distinguish agents and other non-human participants from regular users |

The claim set also carries grants for surfaces outside OpenVidu's supported feature set (SIP telephony among them). Consult your server SDK's API documentation for those.

### Video grants

The `video` claim is where permissions live. Every field is optional; anything you omit is simply not granted, except where noted.

| Grant | Type | Effect |
| --- | --- | --- |
| `roomJoin` | boolean | Allows joining a Room. **Required for a participant token** |
| `room` | string | The Room name this token is valid for. Set it together with `roomJoin` |
| `canPublish` | boolean | Allows publishing tracks. **Defaults to allowed** when the field is absent — set it to `false` explicitly for a viewer-only participant |
| `canSubscribe` | boolean | Allows subscribing to other participants' tracks. Also defaults to allowed |
| `canPublishData` | boolean | Allows sending data messages. Also defaults to allowed |
| `canPublishSources` | array of string | Restricts publishing to specific track sources, e.g. only the camera and microphone but not screen share |
| `canUpdateOwnMetadata` | boolean | Allows the participant to change its own `name`, `metadata` and `attributes` from the client |
| `canSubscribeMetrics` | boolean | Allows the participant to receive metrics |
| `hidden` | boolean | The participant is present but invisible to others — it does not appear in their participant lists |
| `recorder` | boolean | Marks the participant as a recorder. Used by Egress, which joins the Room to record it |
| `agent` | boolean | Marks the participant as an agent |
| `roomCreate` | boolean | Server-side permission: create and delete Rooms |
| `roomList` | boolean | Server-side permission: list Rooms |
| `roomAdmin` | boolean | Server-side permission: administer the Room named in `room` — remove participants, mute tracks, update metadata |
| `roomRecord` | boolean | Server-side permission: start and stop Egress |
| `ingressAdmin` | boolean | Server-side permission: manage Ingress |
| `canManageAgentSession` | boolean | Allows managing agent sessions |
| `destinationRoom` | string | Target Room for moving a participant between Rooms |

The last group are **server-side** grants. A token your backend uses to call the API needs those; a token you hand to a browser should not carry them.

## Minting a token

The canonical shape, with the Node.js server SDK:

```javascript
import { AccessToken } from "livekit-server-sdk";

const at = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
  identity: participantName,
});
at.addGrant({ roomJoin: true, room: roomName });
const token = await at.toJwt();
```

That is the smallest useful token: this participant, this Room, publish and subscribe allowed by default.

A viewer who may watch but not publish:

```javascript
const at = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
  identity: viewerName,
});
at.addGrant({
  roomJoin: true,
  room: roomName,
  canPublish: false,
  canPublishData: false,
});
```

And a token for your own backend to administer a Room, which grants no join at all:

```javascript
const at = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET);
at.addGrant({ roomAdmin: true, room: roomName });
```

Equivalent code for Go, Ruby, Java, Python, Rust, PHP and .NET is in the [application server tutorials](../tutorials/application-server/index.md), each one a complete working server.

## Designing your permission model

Access tokens are the whole authorization surface: OpenVidu has no notion of your users, so **your** rules decide what each token carries. Two habits worth keeping:

- **Authenticate before you mint.** The token endpoint must be behind your own login. An open `/token` endpoint lets anyone join any Room under any name.
- **Mint the narrowest token that works.** Scope it to one Room, set `canPublish: false` for audiences, and keep the server-side grants out of client tokens.

For the operations these permissions gate — creating Rooms, muting, removing participants, recording — see [How to develop your OpenVidu application](../developing-your-openvidu-app/how-to.md).

## Related

- [Webhooks reference](./webhooks.md) — the events your backend receives, verified with the same key pair
- [Configuration reference](../self-hosting/configuration/reference.md) — `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`
- Your server SDK's API documentation, for the exact builder methods in your language
