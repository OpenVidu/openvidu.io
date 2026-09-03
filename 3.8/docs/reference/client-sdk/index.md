# Client SDK

The client SDK is what runs in your **application client**:

- A browser
- A mobile app
- A desktop app
- IoT and robotic devices

It represents one participant inside a Room. It connects with an [access token](https://openvidu.io/3.8/docs/reference/access-tokens/index.md), publishes camera, microphone or screen, subscribes to what others publish, and raises events as the Room changes around it.

OpenVidu is API-compatible with LiveKit, so the LiveKit client SDKs work unchanged: JavaScript, React, Swift, Android, Flutter, React Native, Unity and more. This page documents the model they all share.

Info

This page presents examples and snippets using the **LiveKit JavaScript SDK**, but the concepts are common to every other LiveKit client SDK. Visit the reference for your own SDK for exact method names and argument shapes.

- [JavaScript](https://docs.livekit.io/reference/client-sdk-js/)
- [Swift](https://docs.livekit.io/reference/client-sdk-swift/documentation/livekit/)
- [Android](https://docs.livekit.io/reference/client-sdk-android/index.html)
- [Flutter](https://docs.livekit.io/reference/client-sdk-flutter/livekit_client/)
- [React Native](https://htmlpreview.github.io/?https://raw.githubusercontent.com/livekit/client-sdk-react-native/main/docs/modules.html)
- [Unity](https://livekit.github.io/client-sdk-unity/api/LiveKit.html)
- [Unity (WebGL)](https://livekit.github.io/client-sdk-unity-web/api/LiveKit.html)
- [Node.js](https://docs.livekit.io/reference/client-sdk-node/)
- [Rust](https://docs.rs/livekit/latest/livekit/)
- [C++](https://docs.livekit.io/reference/client-sdk-cpp/)
- [Python](https://docs.livekit.io/reference/python/livekit/rtc/index.html)
- [Go](https://github.com/livekit/server-sdk-go)
- [ESP32](https://livekit.github.io/client-sdk-esp32/)

Visit the LiveKit docs for the complete client-side documentation, and for the exact signatures of your own SDK:

[**LiveKit docs**](https://docs.livekit.io/reference/#livekit-sdks)

The tutorials build a complete application client in different frameworks:

[**Application client tutorials**](https://openvidu.io/3.8/docs/tutorials/application-client/index.md)

## Connecting to a Room

Connecting a Participant to a Room can be as simple as this:

```javascript
import { Room, RoomEvent } from "livekit-client";

const room = new Room(); // (1)!

room.on(RoomEvent.ParticipantConnected, (participant) => { // (2)!
  console.log(`Participant ${participant.identity} connected`);
});

await room.connect(OPENVIDU_URL, token); // (3)!

await room.localParticipant.enableCameraAndMicrophone(); // (4)!
```

1. Create the `Room` object. It represents this participant's session, and nothing happens on the network yet.
1. Register Room event handlers. Usually the best place to do this is before connecting to avoid missing events.
1. Connect to the Room. `OPENVIDU_URL` is your deployment's WebSocket endpoint: `ws://localhost:7880` for a [local deployment](https://openvidu.io/3.8/docs/self-hosting/local/index.md), `wss://your-domain` in production. The token comes from your application server, see [access tokens](https://openvidu.io/3.8/docs/reference/access-tokens/index.md).
1. Publish the camera and the microphone of the device, so the other participants can subscribe to them.

### Disconnect from a Room

```typescript
await room.disconnect();
```

This will stop all local tracks, unpublish them, and close the connection to the Room. The server will remove this participant from the Room, notify the disconnected participant with a `Disconnected` event, and notify everyone else with a `ParticipantDisconnected` event.

The `Disconnected` event (for the local participant) and `ParticipantDisconnected` event (for remote participants) carry a [`DisconnectReason`](https://docs.livekit.io/reference/client-sdk-js/enums/DisconnectReason.html) . You can handle them separately in your UI if you need:

| Reason                                                                | Meaning                                                                 |
| --------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `CLIENT_INITIATED`                                                    | You called `disconnect()`                                               |
| `DUPLICATE_IDENTITY`                                                  | Someone connected with the same identity and displaced this participant |
| `PARTICIPANT_REMOVED`                                                 | Your backend called `RemoveParticipant`                                 |
| `ROOM_DELETED`                                                        | Your backend called `DeleteRoom`                                        |
| `ROOM_CLOSED`                                                         | The Room closed                                                         |
| `SERVER_SHUTDOWN`                                                     | The server went down                                                    |
| `JOIN_FAILURE`                                                        | The connection never completed                                          |
| `CONNECTION_TIMEOUT` / `MEDIA_FAILURE` / `SIGNAL_CLOSE`               | Network-level failures                                                  |
| `USER_UNAVAILABLE` / `USER_REJECTED` / `MIGRATION` / `STATE_MISMATCH` | Less common; see the SDK for the full set                               |

### Reconnection

When the connection to the server is interrupted, for example because the user moves from WiFi to cellular or a Media Node fails, the client reconnects on its own. There are two mechanisms:

- **Resume**: the client re-establishes the signalling connection and performs an [ICE restart](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Session_lifetime#ice_restart) on the existing session. The participant stays in the Room, tracks are not republished and no `Reconnecting` event is emitted. Users may notice a pause of a few seconds in the video. This is the usual case.
- **Full reconnect**: used when an ICE restart is not possible or does not succeed. The client rejoins the Room from scratch. It takes longer and it is noticeable to every participant, so a `Reconnecting` event is emitted for the application to reflect the state in its UI.

A full reconnect emits this sequence of events:

1. `ParticipantDisconnected` for every other participant in the Room.
1. `LocalTrackUnpublished` for each of your tracks that was unpublished.
1. `Reconnecting`.
1. The client rejoins the Room.
1. `Reconnected`.
1. `ParticipantConnected` for everyone currently in the Room.
1. `LocalTrackPublished` as your tracks are republished.

This is equivalent to every participant leaving the Room and joining it again, so any state the application built from those events is rebuilt.

Some notes:

- A `ConnectionQualityChanged` event with value `lost` is emitted before `Reconnecting` or `Disconnected`. It is the earliest signal that the connection is failing.
- A `reconnecting` state does not mean the Room is over for the participant. In an [Elastic or High Availability deployment](https://openvidu.io/3.8/docs/self-hosting/production-ready/fault-tolerance/index.md), a Media Node failure is recovered by rebuilding the Room on a healthy node in a few seconds.
- Reconnecting does not require a new token. The client uses the token that OpenVidu refreshed while it was connected, so the application server is not involved. See [token lifecycle](https://openvidu.io/3.8/docs/reference/access-tokens/#token-lifecycle).
- A participant that leaves without calling `disconnect()`, because the tab was closed or the process was killed, is automatically removed from the Room after 15 seconds.

## Tracks

### Publish a Track

You can directly publish the default camera and microphone of the device using methods `setCameraEnabled` and `setMicrophoneEnabled` of the `LocalParticipant` object:

```typescript
// Publish a video track from the default camera
await room.localParticipant.setCameraEnabled(true);
// Publish an audio track from the default microphone
await room.localParticipant.setMicrophoneEnabled(true);
```

It is also possible to publish both of them at the same time using method `LocalParticipant.enableCameraAndMicrophone`, which has the advantage of showing a single permission dialog to the user:

```typescript
// Publish both default video and audio tracks triggering a single permission dialog
await room.localParticipant.enableCameraAndMicrophone();
```

To craft a custom Track, you can use the `LocalParticipant.createTracks` method and publish them with `LocalParticipant.publishTrack`:

```typescript
const tracks = await room.localParticipant.createTracks({
  audio: {
    deviceId: "default",
    autoGainControl: true,
    echoCancellation: true,
    noiseSuppression: true,
  },
  video: {
    deviceId: "frontcamera",
    facingMode: "user",
  },
});
await Promise.all([
    room.localParticipant.publishTrack(tracks[0]),
    room.localParticipant.publishTrack(tracks[1]),
]);
```

Three behaviours are worth knowing before wiring a UI to them:

- **Muting is not unpublishing.** A muted track stops sending data but stays published, and everyone in the Room receives `TrackMuted`. Unpublishing removes the publication altogether, and only then do the others get `TrackUnpublished`.
- **Unpublishing does not release the device by itself.** The camera light stays on unless the local track is also stopped.
- **The token decides what may be published.** The `canPublishSources` grant can allow the camera and the microphone but not the screen, and revoking `canPublish` while connected unpublishes everything that Participant had published. See [video grants](https://openvidu.io/3.8/docs/reference/access-tokens/#video-grants).

### Mute/Unmute a Track

To mute the default camera and microphone Tracks:

```typescript
await room.localParticipant.setCameraEnabled(false);
await room.localParticipant.setMicrophoneEnabled(false);
```

To mute/unmute a custom Track:

```typescript
// Mute the track
await track.mute();

// Unmute the track
await track.unmute();
```

Muting stops sending the Track's data to the server, but it remains published. Every participant in the Room is notified with the `TrackMuted` and `TrackUnmuted` events, so your UI can reflect who is muted.

### Unpublish a Track

To completely stop sending a Track to the Room, you must unpublish it:

```typescript
await room.localParticipant.unpublishTrack(track, true);
```

The second boolean parameter indicates if the local Track should be stopped. This usually means freeing the device capturing it (switching off the camera LED, for example).

> [LiveKit reference docs](https://docs.livekit.io/reference/client-sdk-js/classes/LocalParticipant.html#unpublishTrack)

### Subscribe to a Track

By default a Participant subscribes to every Track published in the Room. Each one arrives as a `TrackSubscribed` event, which is where the media is attached to the UI:

```typescript
room.on(RoomEvent.TrackSubscribed, (track, publication, participant) => {
  const element = track.attach(); // Returns an HTMLVideoElement or HTMLAudioElement
  document.getElementById("participants").appendChild(element);
});

room.on(RoomEvent.TrackUnsubscribed, (track) => {
  track.detach().forEach((element) => element.remove());
});
```

In a Room with many Participants, each viewer usually needs only a few Tracks. Connect with `autoSubscribe: false` and subscribe explicitly:

```typescript
await room.connect(wsUrl, token, { autoSubscribe: false });

// Tracks published while connected
room.on(RoomEvent.TrackPublished, (publication) => {
  publication.setSubscribed(true);
});

// Tracks already published when connecting
room.remoteParticipants.forEach((participant) => {
  participant.trackPublications.forEach((publication) => {
    publication.setSubscribed(true);
  });
});
```

To stop receiving the media of a Track without unsubscribing from it, for example while its tile is hidden, disable the publication instead. It is cheaper than unsubscribing and subscribing again:

```typescript
publication.setEnabled(false);
```

### Screen Sharing

To quickly publish a screen sharing Track:

```typescript
await room.localParticipant.setScreenShareEnabled(true);
```

You can also create custom screen tracks, for example capturing the audio of the screen and fine-tuning the video capture options (checkout the [ScreenShareCaptureOptions](https://docs.livekit.io/reference/client-sdk-js/interfaces/ScreenShareCaptureOptions.html) interface for detailed information):

```typescript
const screenTracks = await room.localParticipant.createScreenTracks({
  audio: true,
  contentHint: "detail",
  preferCurrentTab: true,
  video: {
    displaySurface: "window",
  },
});
await Promise.all([
  room.localParticipant.publishTrack(screenTracks[0]),
  room.localParticipant.publishTrack(screenTracks[1]),
]);
```

Sharing the audio of the screen only works in some browsers, and only for a browser tab: the user must additionally tick the "Share tab audio" checkbox in the browser's own dialog. When audio is not shared, `createScreenTracks` returns the video track alone, so do not assume two tracks.

### Virtual Background

It is possible to apply a virtual background to video tracks. In this way you can blur the background or replace it with an image.

SDK support

Virtual backgrounds are only supported in the JavaScript SDK (blur and background image) and the Swift SDK (only blur: [BackgroundBlurVideoProcessor](https://docs.livekit.io/reference/client-sdk-swift/documentation/livekit/backgroundblurvideoprocessor/) ).

It is necessary to install an additional dependency to use this feature:

```bash
npm add @livekit/track-processors
```

A single `BackgroundProcessor` covers both effects, and it can switch between them on the fly:

```typescript
import { BackgroundProcessor, supportsBackgroundProcessors } from "@livekit/track-processors";

if (!supportsBackgroundProcessors()) {
  throw new Error("This browser does not support background processors");
}

const videoTrack = await createLocalVideoTrack();

// Blur the background. blurRadius defaults to 10
const processor = BackgroundProcessor({ mode: "background-blur", blurRadius: 10 });

// Or replace it with an image
// const processor = BackgroundProcessor({ mode: "virtual-background", imagePath: "https://picsum.photos/400" });

await videoTrack.setProcessor(processor);
await room.localParticipant.publishTrack(videoTrack);
```

Toggling the effect without visual artifacts

Calling `setProcessor()` and `stopProcessor()` on demand produces a visible glitch while the pipeline is rebuilt. Instead, attach the processor once in `disabled` mode and switch modes on it:

```typescript
const processor = BackgroundProcessor({ mode: "disabled" });
await videoTrack.setProcessor(processor);

await processor.switchTo({ mode: "background-blur", blurRadius: 10 });
await processor.switchTo({ mode: "disabled" });
```

The same package processes audio tracks, and is the starting point for writing your own processor:

> [GitHub Repository](https://github.com/livekit/track-processors-js)

### Bandwidth optimizations

Participants of the same Room rarely have the same bandwidth, the same screen size or the same layout. These are the mechanisms that adapt the media to each of them, and all of them are configured in the client SDK:

- **Simulcast**: the publisher encodes the same video track several times, at different resolutions and bitrates, and sends all of them. The server then forwards to each subscriber the layer that best fits its bandwidth and its requested resolution, upgrading it again when conditions improve. It is **enabled by default**.
- **SVC (Scalable Video Coding)**: an alternative to simulcast available with the VP9 and AV1 codecs, where a single stream already contains several spatial and temporal layers. It is more efficient than simulcast, because the higher layers reuse the information of the lower ones, and switching between layers is immediate. It is **enabled by default** when publishing with VP9 or AV1.
- **Dynacast**: the publisher stops encoding and sending the layers that no subscriber is consuming. If everyone is subscribed to a low resolution layer, high-resolution layers are not sent at all. It is **disabled by default**.
- **Adaptive stream**: the subscriber requests the layer that matches the size of the HTML element where the track is rendered, and pauses the track entirely while that element is not visible. This prevents downloading a 1080p layer to display it in a 150x150 tile. It is **disabled by default**.

Adaptive stream in JavaScript

Adaptive stream needs to know the size and the visibility of the element rendering each track. In JavaScript this only works if the track is attached with `track.attach()`. If the media element is managed manually, adaptive stream has no effect.

All of them can be configured when creating the `Room`:

```typescript
const room = new Room({
  adaptiveStream: true, // (1)!
  dynacast: true, // (2)!
  publishDefaults: {
    simulcast: true, // (3)!
    videoCodec: "vp9", // (4)!
  },
});
```

1. Subscriber side. Requests the layer that matches the size of the element rendering each Track, and pauses the Track while the element is not visible. Defaults to `false`.
1. Publisher side. Stops sending the layers that nobody is consuming. Defaults to `false`.
1. Publisher side. Publishes several versions of each video Track. Defaults to `true`: set it to `false` to publish a single encoding.
1. Using `vp9` or `av1` activates SVC, with three spatial and temporal layers. Defaults to `true` when those codecs are used.

## Send data and share state

Participants can exchange data through the Room in several ways, each one designed for a different pattern:

| To do this                                                  | Use                                                       | Delivery                             |
| ----------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------ |
| Send chat messages or LLM responses                         | [Text streams](#text-and-files)                           | Reliable, any size                   |
| Send files, images or any binary data                       | [Byte streams](#text-and-files)                           | Reliable, any size                   |
| Call a method on another participant and await its response | [RPC](#remote-procedure-calls)                            | Reliable, request/response           |
| Stream continuous data, such as sensors or telemetry        | [Data tracks](#continuous-data)                           | Lossy, continuous                    |
| Share state that every participant must see                 | [Participant attributes and Room metadata](#shared-state) | Synchronized by the server           |
| Control the delivery of individual packets yourself         | [Data packets](#data-packets)                             | Reliable or lossy, 15 KiB per packet |

### Text and files

Text and byte streams are the right default for messages. They chunk the payload for you, so there is no size limit, and they are routed by a topic that the receiver registers a handler for:

```typescript
// Sender
await room.localParticipant.sendText("Hello!", { topic: "chat" });

// Receiver, registered before the stream arrives
room.registerTextStreamHandler("chat", async (reader, participantInfo) => {
  console.log(`Message from ${participantInfo.identity}:`, await reader.readAll());
});
```

Files travel the same way with `sendFile` and `registerByteStreamHandler`, which additionally report progress.

```typescript
// Sender
const file = (document.getElementById("file") as HTMLInputElement).files[0];
await room.localParticipant.sendFile(file, {
  mimeType: file.type,
  topic: "my-files",
  onProgress: (progress) => console.log(`Sending: ${Math.ceil(progress * 100)}%`),
});

// Receiver
room.registerByteStreamHandler("my-files", async (reader, participantInfo) => {
  reader.onProgress = (progress) => console.log(`Receiving: ${Math.ceil(progress * 100)}%`);
  const file = new Blob(await reader.readAll(), { type: reader.info.mimeType });
  console.log(`Received ${reader.info.name} from ${participantInfo.identity}`);
});
```

Two things to keep in mind: a participant that joins after a stream was opened does not receive it, and OpenVidu does not persist any message. Storing history is up to your application.

> [LiveKit reference docs](https://docs.livekit.io/transport/data/text-streams/)

### Remote procedure calls

RPC is the option when you need an answer back. A participant registers a method, and any other participant in the Room can invoke it:

```typescript
// Callee
room.registerRpcMethod("greet", async (data) => `Hello, ${data.callerIdentity}!`);

// Caller
const response = await room.localParticipant.performRpc({
  destinationIdentity: "my-participant",
  method: "greet",
  payload: "Hi!",
});
```

> [LiveKit reference docs](https://docs.livekit.io/transport/data/rpc/)

### Continuous data

Data tracks carry a continuous flow of frames, sending each one only once and dropping whatever cannot be delivered in time. This suits telemetry, robot control and game state, where the newest value matters more than a complete history. They behave like media tracks: they are published, subscribed to individually, and participants that join later see them.

```typescript
const track = await room.localParticipant.publishDataTrack({ name: "my_sensor_data" });
```

> [LiveKit reference docs](https://docs.livekit.io/transport/data/data-tracks/)

### Shared state

Room metadata and participant attributes are not messages but state: the server stores them and synchronizes them to everyone, including participants that connect later.

- **Room metadata** is a single string for the whole Room. Only your application server can set it, with [`CreateRoom`](https://openvidu.io/3.8/docs/reference/room-service-api/#rooms) or [`UpdateRoomMetadata`](https://openvidu.io/3.8/docs/reference/room-service-api/#rooms). Clients read `room.metadata` and listen for event `RoomMetadataChanged`.
- **Participant attributes** are a key-value store, so a single key can be updated without resending the rest. **Participant metadata** is the single-string equivalent. Both can be given an initial value in the [access token](https://openvidu.io/3.8/docs/reference/access-tokens/index.md), so they are available the moment the participant connects, and a participant can change its own if its token carries grant [`canUpdateOwnMetadata`](https://openvidu.io/3.8/docs/reference/access-tokens/#video-grants).

```typescript
console.log(room.metadata); // Room metadata, set from your application server

room.localParticipant.setAttributes({ handRaised: "true" }); // Needs canUpdateOwnMetadata

room.on(RoomEvent.ParticipantAttributesChanged, (changed, participant) => {
  console.log("New attributes for", participant.identity, changed);
});
```

Metadata is limited to 512 KiB and attributes to 64 KiB across all keys. Neither is meant for frequent updates: more than one every few seconds is a sign you want data packets or a data track instead.

> [LiveKit reference docs](https://docs.livekit.io/transport/data/state/)

### Data packets

Data packets are the low-level API the options above are built on. Reach for them when you want to control each packet yourself:

```typescript
// Sender
const data = new TextEncoder().encode(JSON.stringify({ some: "data" }));
room.localParticipant.publishData(data, {
  reliable: true,
  topic: "chat",
  destinationIdentities: ["my-participant"],
});

// Receiver
room.on(RoomEvent.DataReceived, (payload, participant, kind, topic) => {
  console.log("Received data from", participant.identity, new TextDecoder().decode(payload));
});
```

Reliable packets are retransmitted and delivered in order; lossy packets are sent once. Each packet holds up to 15 KiB, and your application server can publish them too with [`SendData`](https://openvidu.io/3.8/docs/reference/room-service-api/#data).

## Room events

Handlers are registered on the Room with `room.on(...)`. These are the events of the [`RoomEvent`](https://docs.livekit.io/reference/client-sdk-js/enums/RoomEvent.html) enum, grouped by what they tell you.

Participants emit their own [`ParticipantEvent`](https://docs.livekit.io/reference/client-sdk-js/enums/ParticipantEvent.html) events for the subset that concerns them, so you can listen per participant instead of filtering Room-wide events. The last column of each table says where an event is emitted, including the few that exist only on the Participant.

### Connection lifecycle

| Event                    | Fires when                                                                                                                | Triggered by |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------- | ------------ |
| `SignalConnected`        | The signalling connection is established. Tracks can already be published, before media is fully ready                    | Room         |
| `Connected`              | The Room is connected and usable                                                                                          | Room         |
| `Reconnecting`           | The connection dropped and is being re-established                                                                        | Room         |
| `SignalReconnecting`     | The signalling connection specifically is reconnecting                                                                    | Room         |
| `Reconnected`            | Recovery succeeded                                                                                                        | Room         |
| `Disconnected`           | The Room ended for this participant. The handler receives a [`DisconnectReason`](#disconnect-from-a-room)                 | Room         |
| `ConnectionStateChanged` | Any transition between the [ConnectionStates](https://docs.livekit.io/reference/client-sdk-js/enums/ConnectionState.html) | Room         |

### Participants and Room state

| Event                                              | Fires when                                                                                                                                                    | Triggered by      |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| `ParticipantConnected` / `ParticipantDisconnected` | Someone joins or leaves **after** you did. Neither fires for participants already in the Room when you connect                                                | Room              |
| `ParticipantActive`                                | A participant is fully connected and ready to send and receive data messages. `ParticipantConnected` only says they are in the Room                           | Room, Participant |
| `ActiveSpeakersChanged`                            | The set of speaking participants changes. Ordered by audio level, loudest first, and it includes you                                                          | Room              |
| `IsSpeakingChanged`                                | One participant started or stopped speaking. The per-participant counterpart of `ActiveSpeakersChanged`, handy to drive a speaking indicator on a single tile | Participant       |
| `ParticipantMetadataChanged`                       | A participant's metadata changed                                                                                                                              | Room, Participant |
| `ParticipantNameChanged`                           | A participant's display name changed                                                                                                                          | Room, Participant |
| `ParticipantAttributesChanged`                     | A participant's attributes changed                                                                                                                            | Room, Participant |
| `RoomMetadataChanged`                              | The Room's own metadata changed, after your application server called `UpdateRoomMetadata`                                                                    | Room              |
| `ParticipantPermissionsChanged`                    | A participant's permissions changed, for example after your backend called `UpdateParticipant`                                                                | Room, Participant |
| `ParticipantEncryptionStatusChanged`               | A participant's end-to-end encryption status changed                                                                                                          | Room              |

### Track events

| Event                                                                   | Fires when                                                                                                                                  | Triggered by      |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| `TrackPublished` / `TrackUnpublished`                                   | A remote participant starts or stops publishing, **after** you joined. Publishing is not subscribing: it only reports the state of the Room | Room, Participant |
| `TrackSubscribed` / `TrackUnsubscribed`                                 | You start or stop receiving a remote track. **This is where you attach media to your UI**                                                   | Room, Participant |
| `TrackSubscriptionFailed`                                               | Subscribing failed                                                                                                                          | Room, Participant |
| `LocalTrackPublished` / `LocalTrackUnpublished`                         | Your own track went live or stopped. The unpublish also fires when the user ends a screen share from the browser's own bar                  | Room, Participant |
| `DataTrackPublished` / `DataTrackUnpublished`                           | A remote participant published or unpublished a [data track](#continuous-data)                                                              | Room              |
| `LocalDataTrackPublished` / `LocalDataTrackUnpublished`                 | Your own data track went live or stopped                                                                                                    | Room              |
| `LocalTrackSubscribed`                                                  | The first remote participant subscribed to one of your published tracks                                                                     | Room, Participant |
| `TrackMuted` / `TrackUnmuted`                                           | Any track was muted or unmuted, local or remote                                                                                             | Room, Participant |
| `TrackStreamStateChanged`                                               | The server started or stopped delivering a subscribed track, typically under bandwidth pressure                                             | Room, Participant |
| `TrackSubscriptionPermissionChanged` / `TrackSubscriptionStatusChanged` | Your permission or status for a subscription changed. Revoking permission unsubscribes the track; granting it raises `TrackSubscribed`      | Room, Participant |
| `LocalAudioSilenceDetected`                                             | Your microphone is publishing silence, usually a muted or wrong device                                                                      | Room              |
| `LocalTrackCpuConstrained` / `TrackCpuConstrained`                      | One of your local video tracks is limited by CPU. Lower its capture resolution to recover quality                                           | Participant       |

### Data and messaging

| Event                   | Fires when                                                                                                                            | Triggered by      |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| `DataReceived`          | A data message arrived, from a participant or from your backend's `SendData`                                                          | Room, Participant |
| `ChatMessage`           | A chat message arrived                                                                                                                | Room, Participant |
| `TranscriptionReceived` | A transcription segment arrived. This is how [live captions](https://openvidu.io/3.8/docs/ai/live-captions/index.md) reach the client | Room, Participant |

### Quality, devices and diagnostics

| Event                                                       | Fires when                                                                                                                                                            | Triggered by      |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| `ConnectionQualityChanged`                                  | A participant's connection quality rating changed: `excellent`, `good`, `poor` or `lost`                                                                              | Room, Participant |
| `MediaDevicesError`                                         | Acquiring a camera or microphone failed, usually because the user denied permission                                                                                   | Room, Participant |
| `MediaDevicesChanged`                                       | The available cameras or microphones changed, for example a headset was plugged in                                                                                    | Room              |
| `ActiveDeviceChanged`                                       | The device in use changed, in response to your call to `switchActiveDevice()`                                                                                         | Room              |
| `AudioPlaybackStatusChanged` / `VideoPlaybackStatusChanged` | Autoplay was allowed or blocked by the browser. **Handle these**: browsers block autoplay until a user gesture, and this is what tells you to show an "unmute" button | Room              |
| `RecordingStatusChanged`                                    | The Room started or stopped being recorded. Use it to show a recording indicator                                                                                      | Room              |
| `EncryptionError`                                           | End-to-end encryption failed                                                                                                                                          | Room              |

## Related

- [Application client tutorials](https://openvidu.io/3.8/docs/tutorials/application-client/index.md): complete application clients in different frameworks.
- [Access tokens reference](https://openvidu.io/3.8/docs/reference/access-tokens/index.md): what a participant is allowed to do inside a Room.
- [Room Service API reference](https://openvidu.io/3.8/docs/reference/room-service-api/index.md): the same Room, managed from your application server.
- [UI Components](https://openvidu.io/3.8/docs/ui-components/angular-components/index.md): prebuilt components, if you would rather not wire events by hand.
