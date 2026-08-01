---
title: "OpenVidu client SDK reference"
description: "How an OpenVidu client connects, publishes and subscribes, with every room event, track source and connection state it can observe."
---

# Client SDK

The client SDK is what runs in your **application client** — browser, mobile app or desktop — and represents one participant inside a room. It connects with an [access token](./access-tokens.md), publishes camera, microphone or screen, subscribes to what others publish, and raises events as the room changes around it.

OpenVidu is API-compatible with LiveKit, so the LiveKit client SDKs work unchanged: JavaScript, React, Swift, Android, Flutter, React Native, Unity and more. This page documents the model they share. **For exact method signatures in your language, use that SDK's own API documentation** — the names below are from the JavaScript SDK, the concepts are common to all of them.

The [application client tutorials](../tutorials/application-client/index.md) build a complete application in eight of them.

## Connecting

Four steps, in this order:

```javascript
import { Room, RoomEvent } from "livekit-client";

const room = new Room();                                    // 1. create
room.on(RoomEvent.TrackSubscribed, (track) => {             // 2. subscribe to events
  document.body.appendChild(track.attach());                //    BEFORE connecting
});
await room.connect(OPENVIDU_URL, token);                    // 3. connect
await room.localParticipant.enableCameraAndMicrophone();    // 4. publish
```

Register handlers **before** `connect`. Tracks that already exist in the room are delivered as `TrackSubscribed` events during connection, and a handler attached afterwards misses them — this is the single most common reason a participant sees nobody who was already there.

The URL is your deployment's WebSocket endpoint: `ws://localhost:7880` for a [local deployment](../self-hosting/local.md), `wss://your-domain` in production. The token comes from your application server; see [access tokens](./access-tokens.md).

## Room events

Handlers registered with `room.on(...)`. Grouped by what they tell you:

### Connection lifecycle

| Event | Fires when |
| --- | --- |
| `SignalConnected` | The signalling connection is established, before media is ready |
| `Connected` | The room is connected and usable |
| `Reconnecting` | The connection dropped and is being re-established |
| `SignalReconnecting` | The signalling connection specifically is reconnecting |
| `Reconnected` | Recovery succeeded |
| `Disconnected` | The room ended for this participant. The handler receives a reason — see below |
| `ConnectionStateChanged` | Any transition between the states below |
| `MediaDevicesError` | Acquiring a camera or microphone failed |

### Participants

| Event | Fires when |
| --- | --- |
| `ParticipantConnected` / `ParticipantDisconnected` | Someone joins or leaves |
| `ActiveSpeakersChanged` | The set of speaking participants changes |
| `ParticipantMetadataChanged` | A participant's metadata changed |
| `ParticipantNameChanged` | A participant's display name changed |
| `ParticipantAttributesChanged` | A participant's attributes changed |
| `ParticipantPermissionsChanged` | A participant's permissions changed — for example after your backend called `UpdateParticipant` |
| `ParticipantEncryptionStatusChanged` | A participant's end-to-end encryption status changed |
| `RoomMetadataChanged` | The room's own metadata changed |

### Tracks

| Event | Fires when |
| --- | --- |
| `TrackPublished` / `TrackUnpublished` | A remote participant starts or stops publishing |
| `TrackSubscribed` / `TrackUnsubscribed` | You start or stop receiving a remote track. **This is where you attach media to your UI** |
| `TrackSubscriptionFailed` | Subscribing failed |
| `LocalTrackPublished` / `LocalTrackUnpublished` | Your own track went live or stopped |
| `LocalTrackSubscribed` | Your own published track was confirmed subscribed |
| `TrackMuted` / `TrackUnmuted` | Any track was muted or unmuted, local or remote |
| `TrackStreamStateChanged` | The server started or stopped delivering a subscribed track, typically under bandwidth pressure |
| `TrackSubscriptionPermissionChanged` / `TrackSubscriptionStatusChanged` | Your permission or status for a subscription changed |
| `LocalAudioSilenceDetected` | Your microphone is publishing silence — usually a muted or wrong device |

### Data and messaging

| Event | Fires when |
| --- | --- |
| `DataReceived` | A data message arrived, from a participant or from your backend's `SendData` |
| `ChatMessage` | A chat message arrived |
| `TranscriptionReceived` | A transcription segment arrived — this is how [live captions](../ai/live-captions.md) reach the client |
| `SipDTMFReceived` | A DTMF tone arrived |

### Quality, devices and diagnostics

| Event | Fires when |
| --- | --- |
| `ConnectionQualityChanged` | A participant's connection quality rating changed |
| `MetricsReceived` | Metrics arrived |
| `MediaDevicesChanged` | The available cameras or microphones changed — a headset was plugged in |
| `ActiveDeviceChanged` | The device in use changed |
| `AudioPlaybackStatusChanged` / `VideoPlaybackStatusChanged` | Autoplay was allowed or blocked by the browser. **Handle these**: browsers block autoplay until a user gesture, and this is what tells you to show an "unmute" button |
| `RecordingStatusChanged` | The room started or stopped being recorded — use it to show a recording indicator |
| `DCBufferStatusChanged` | The data channel buffer became congested or recovered |
| `EncryptionError` | End-to-end encryption failed |

Participants also emit their own events for the subset that concerns them, so you can listen per participant instead of filtering room-wide events.

## Connection states

`room.state`, and the payload of `ConnectionStateChanged`:

| State | |
| --- | --- |
| `disconnected` | Not connected |
| `connecting` | Connection in progress |
| `connected` | Connected |
| `reconnecting` | Recovering a dropped connection. Media is interrupted; the SDK is retrying |

Reconnection is automatic. A brief `reconnecting` is normal on a network change — for instance a Media Node failure in an [Elastic or High Availability deployment](../self-hosting/production-ready/fault-tolerance.md), where the room is rebuilt on a healthy node in about five seconds. Show a "reconnecting" indicator rather than tearing the call down.

### Why a room ended

`Disconnected` carries a reason. The ones worth handling separately:

| Reason | Meaning |
| --- | --- |
| `CLIENT_INITIATED` | You called `disconnect()` |
| `DUPLICATE_IDENTITY` | Someone connected with the same identity and displaced this participant |
| `PARTICIPANT_REMOVED` | Your backend called `RemoveParticipant` |
| `ROOM_DELETED` | Your backend called `DeleteRoom` |
| `ROOM_CLOSED` | The room closed |
| `SERVER_SHUTDOWN` | The server went down |
| `JOIN_FAILURE` | The connection never completed |
| `CONNECTION_TIMEOUT` / `MEDIA_FAILURE` / `SIGNAL_CLOSE` | Network-level failures |
| `USER_UNAVAILABLE` / `USER_REJECTED` / `MIGRATION` / `STATE_MISMATCH` | Less common; see the SDK for the full set |

`DUPLICATE_IDENTITY` is the one that surprises people: identities must be unique within a room, so reusing one — a user opening a second tab — disconnects the first.

## Tracks

### Sources

Every track declares what it is, which is how you tell a camera from a screen share without inspecting the media:

| Source | |
| --- | --- |
| `camera` | |
| `microphone` | |
| `screen_share` | |
| `screen_share_audio` | Audio captured alongside a screen share |
| `unknown` | |

Track **kind** is separate and simpler: `audio`, `video` or `unknown`.

The `canPublishSources` grant restricts which of these a participant may publish — a token that allows camera and microphone but not screen share. See [video grants](./access-tokens.md#video-grants).

### Publishing and subscribing

`enableCameraAndMicrophone()` is the shortcut used in most examples. Under it are per-track methods for publishing a specific device, a screen share, or a track you created yourself — from a canvas, a file, or a processing pipeline.

Subscription is automatic by default: you receive `TrackSubscribed` for every track published in the room. Two ways to change that:

- From the **client**, disable automatic subscription and subscribe selectively — the usual approach for a large room where each viewer only needs a few streams.
- From your **backend**, with [`UpdateSubscriptions`](./server-api.md#participants) — when the decision is yours to make rather than the participant's.

Attach a subscribed track to your UI with `track.attach()`, which returns a media element, and `track.detach()` when it goes away.

## Related

- [Application client tutorials](../tutorials/application-client/index.md) — complete applications in eight frameworks
- [Access tokens reference](./access-tokens.md) — what a participant is allowed to do
- [Server API reference](./server-api.md) — the same room, managed from your backend
- [UI Components](../ui-components/angular-components.md) — prebuilt components, if you would rather not wire events by hand
- Your client SDK's API documentation, for exact signatures in your language
