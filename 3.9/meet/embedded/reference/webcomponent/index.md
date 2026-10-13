# Web Component

OpenVidu Meet's Web Component allows embedding the refined, well-crafted OpenVidu Meet interface directly into your application. It offers **attributes** to customize the videoconferencing experience, exposes **commands** for programmatic control, and emits **events** for integration with your own application's logic.

## Installation

Include the following script in your HTML:

```html
<script src="https://{{ your-domain }}/meet/v1/openvidu-meet.js"></script>
```

## Usage

Add the `<openvidu-meet>` tag to your HTML. This will embed OpenVidu Meet interface into your application:

```html
<openvidu-meet room-url="{{ my-room-url }}"></openvidu-meet>
```

One of **`room-url`** or **`recording-url`** is required: the former determines the room to access, the latter the recording to display. Different instances of the web component using the same room URL will join the same meeting.

> **A room URL is a room access link**
>
> The **room URL** is simply a [room access link](https://openvidu.io/3.9/meet/features/rooms/access/index.md): the URL an individual opens to access a room. The role and identity a participant gets depend on **which** access link you use. This guide and most examples use the **anonymous** moderator/speaker links for simplicity, but a room also has **user** and **identified-guest** links — see [Room Access](https://openvidu.io/3.9/meet/features/rooms/access/index.md) for the full picture.
>
> You can obtain a room's access links programmatically from your backend with the [REST API](https://openvidu.io/3.9/meet/embedded/reference/rest-api/index.md): the `access.anonymous.moderator.url`, `access.anonymous.speaker.url` and `access.user.url` properties of the [MeetRoom](https://openvidu.io/3.9/meet/embedded/reference/api.html#/schemas/MeetRoom) object, or the unique `accessUrl` of an [identified-guest member](https://openvidu.io/3.9/meet/features/room-members/overview/#users-vs-identified-guests).

## API Reference

### Attributes

Declare attributes in the component to customize the meeting for your user.

| Attribute                 | Description                                                                                                                                                                                                                                                                                                                                                                                                                                           | Required                                                             |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `room-url`                | The OpenVidu Meet room URL to access to.                                                                                                                                                                                                                                                                                                                                                                                                              | Yes (This attribute is required unless `recording-url` is provided.) |
| `recording-url`           | The URL of a recording to view.                                                                                                                                                                                                                                                                                                                                                                                                                       | Yes (This attribute is required unless `room-url` is provided.)      |
| `participant-name`        | Display name for the local participant.                                                                                                                                                                                                                                                                                                                                                                                                               | No                                                                   |
| `participant-external-id` | Application-defined identifier for the local participant, so the embedding application can correlate the participant with one of its own users. Up to 64 characters (letters, digits, `_` and `-`). Never interpreted by OpenVidu Meet.                                                                                                                                                                                                               | No                                                                   |
| `participant-metadata`    | Opaque application-defined payload attached to the local participant (JSON is recommended). Up to 2048 bytes (UTF-8). Never interpreted by OpenVidu Meet.                                                                                                                                                                                                                                                                                             | No                                                                   |
| `initial-audio-active`    | Join the meeting with the microphone active. This is the participant's initial state only: they may mute afterwards. Setting it — to either value — **takes precedence over the room's own `config.initialAudioActive`**; leaving it out means "no opinion", so the room's value applies (and `true` when the room has none either). The `mediaPublishAudio` permission is not part of that chain: it is a capability, and a denial always wins.      | No                                                                   |
| `initial-video-active`    | Join the meeting with the camera active. This is the participant's initial state only: they may deactivate it afterwards. Setting it — to either value — **takes precedence over the room's own `config.initialVideoActive`**; leaving it out means "no opinion", so the room's value applies (and `true` when the room has none either). The `mediaPublishVideo` permission is not part of that chain: it is a capability, and a denial always wins. | No                                                                   |
| `e2ee-key`                | Secret key for end-to-end encryption (E2EE). If provided, the participant will join the meeting using E2EE key.                                                                                                                                                                                                                                                                                                                                       | No                                                                   |
| `leave-redirect-url`      | URL to redirect to when leaving OpenVidu Meet. Redirection happens when the participant dismisses the post-meeting, join, error or recording screen, right after the **`embeddedCloseRequested` event** fires.                                                                                                                                                                                                                                        | No                                                                   |
| `show-only-recordings`    | Whether to show only recordings instead of live meetings. Follows the standard HTML boolean-attribute convention: a bare attribute or any value other than `"false"` is `true`; `"false"` and an absent attribute are `false`.                                                                                                                                                                                                                        | No                                                                   |
| `show-recording`          | Identifier of the recording to display. When provided along with `room-url`, the app redirects to the recording view.                                                                                                                                                                                                                                                                                                                                 | No                                                                   |

Example:

```html
<openvidu-meet
    room-url="{{ my-room-url }}"
    participant-name="John Doe"
    participant-external-id="user-42"
    initial-video-active="false"
    leave-redirect-url="https://meeting.end.url/"
></openvidu-meet>
```

> **Identify your own users**
>
> `participant-external-id` and `participant-metadata` are never interpreted by OpenVidu Meet: they travel untouched as the `externalId` and `metadata` properties of every participant payload, in the `participantJoined` / `participantLeft` events and webhooks and in the [Meetings REST API](https://openvidu.io/3.9/meet/embedded/reference/rest-api/index.md), so your backend can correlate a participant with one of its own users.

### Commands

The OpenVidu Meet component exposes a set of commands that allow you to control the room from your application's logic.

| Method                                                                                                                                                                | Description                                                                                                                                                  | Permission          | Restriction                                       |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| `meetingLeave()`                                                                                                                                                      | Disconnects the local participant from the current meeting.                                                                                                  | None                | Requires having joined the meeting                |
| `meetingEnd()`                                                                                                                                                        | Ends the current meeting for all participants.                                                                                                               | `meetingEnd`        | Requires having joined the meeting                |
| `participantKick(     participantIdentity: string )`                                                                                                                  | Kicks a participant from the meeting.                                                                                                                        | `participantKick`   | Requires having joined the meeting                |
| `participantMute(     participantIdentity: string,     media: {         audioActive?: false;         videoActive?: false;         screenShareActive?: false;     } )` | Turns off a participant's microphone, camera or screen share. The participant may turn the device back on.                                                   | `participantMute`   | Requires having joined the meeting                |
| `participantMuteAll(     media: {         audioActive?: false;         videoActive?: false;         screenShareActive?: false;     } )`                               | Turns off the microphone, camera or screen share of every participant except the moderators and the caller. Each participant may turn their devices back on. | `participantMute`   | Requires having joined the meeting                |
| `mediaToggleAudio(active?: boolean)`                                                                                                                                  | Toggles the local participant's microphone, or sets it when `active` is provided.                                                                            | `mediaPublishAudio` | Requires the prejoin screen or an ongoing meeting |
| `mediaToggleVideo(active?: boolean)`                                                                                                                                  | Toggles the local participant's camera, or sets it when `active` is provided.                                                                                | `mediaPublishVideo` | Requires the prejoin screen or an ongoing meeting |
| `mediaToggleScreenShare(active?: boolean)`                                                                                                                            | Toggles the local participant's screen share, or sets it when `active` is provided.                                                                          | `mediaShareScreen`  | Requires having joined the meeting                |
| `endMeeting()`                                                                                                                                                        | **Deprecated** Renamed to `meetingEnd`. Removed in 3.12.0.                                                                                                   | `meetingEnd`        | Requires having joined the meeting                |
| `leaveRoom()`                                                                                                                                                         | **Deprecated** Renamed to `meetingLeave`. Removed in 3.12.0.                                                                                                 | None                | Requires having joined the meeting                |
| `kickParticipant(     participantIdentity: string )`                                                                                                                  | **Deprecated** Renamed to `participantKick`. Removed in 3.12.0.                                                                                              | `participantKick`   | Requires having joined the meeting                |

Invoke commands using JavaScript:

```javascript
const openviduMeet = document.querySelector('openvidu-meet');
openviduMeet.meetingLeave();
```

Commands that take parameters receive them as arguments, in the order listed in the table:

```javascript
openviduMeet.participantMute('participant-identity', { audioActive: false });
openviduMeet.mediaToggleVideo(false);
```

### Events

The OpenVidu Meet component emits events that you can listen to in your application.

| Event                           | Description                                                                                                                                                                                                                                                                                              | Payload                                                                                                                                                 |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `meetingJoined`                 | Event emitted when the local participant joins the meeting.                                                                                                                                                                                                                                              | `{     roomId: string;     participantIdentity: string; }`                                                                                              |
| `meetingLeft`                   | Event emitted when the local participant leaves the meeting.                                                                                                                                                                                                                                             | \`\`\` { roomId: string; participantIdentity: string; reason:                                                                                           |
| `participantJoined`             | Event emitted when a remote participant joins the meeting. Only live transitions are notified: participants already in the meeting when the local one joins are not replayed. The local participant's own join is notified through `meetingJoined` instead.                                              | \`\`\` { roomId: string; participant: { participantIdentity: string; participantName: string; externalId?: string; metadata?: string; role: 'moderator' |
| `participantLeft`               | Event emitted when a remote participant leaves the meeting. The local participant's own departure is notified through `meetingLeft` instead.                                                                                                                                                             | \`\`\` { roomId: string; participant: { participantIdentity: string; participantName: string; externalId?: string; metadata?: string; role: 'moderator' |
| `mediaAudioStatusChanged`       | Event emitted to the local participant when their microphone state changes. Emitted from the prejoin screen onwards, before `meetingJoined`.                                                                                                                                                             | \`\`\` { active: boolean; origin:                                                                                                                       |
| `mediaVideoStatusChanged`       | Event emitted to the local participant when their camera state changes. Emitted from the prejoin screen onwards, before `meetingJoined`.                                                                                                                                                                 | \`\`\` { active: boolean; origin:                                                                                                                       |
| `mediaScreenShareStatusChanged` | Event emitted to the local participant when their screen share state changes. Emitted from the prejoin screen onwards, before `meetingJoined`.                                                                                                                                                           | \`\`\` { active: boolean; origin:                                                                                                                       |
| `embeddedCloseRequested`        | Event emitted when the participant asks to close OpenVidu Meet by dismissing the post-meeting, join, error or recording screen. The host application responds by removing the embedded element or routing the participant elsewhere; the meeting itself may still be running for the other participants. | -                                                                                                                                                       |
| `joined`                        | **Deprecated** Renamed to `meetingJoined`. Removed in 3.12.0.                                                                                                                                                                                                                                            | `{     roomId: string;     participantIdentity: string; }`                                                                                              |
| `left`                          | **Deprecated** Renamed to `meetingLeft`. Removed in 3.12.0.                                                                                                                                                                                                                                              | \`\`\` { roomId: string; participantIdentity: string; reason:                                                                                           |
| `closed`                        | **Deprecated** Renamed to `embeddedCloseRequested`. Removed in 3.12.0.                                                                                                                                                                                                                                   | -                                                                                                                                                       |

Listen to events using JavaScript event listeners:

```javascript
const openviduMeet = document.querySelector('openvidu-meet');

openviduMeet.addEventListener('meetingJoined', (event) => {
    console.log('The local participant has joined the meeting', event.detail);
});
```

You can also use the API `on` | `once` | `off`:

```javascript
const openviduMeet = document.querySelector('openvidu-meet');

openviduMeet.on('meetingJoined', (event) => {
    console.log('The local participant has joined the meeting', event);
});

openviduMeet.on('participantJoined', (event) => {
    console.log(`${event.participant.participantName} has joined the meeting`, event);
});

openviduMeet.once('meetingLeft', (event) => {
    console.log('The local participant has left the meeting', event.reason);
});
```

> **Accessing the event payload**
>
> The way you access the event payload depends on the method you use to listen:
>
> - With the native **`addEventListener`** method, the callback receives a standard [`CustomEvent`](https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent) , so the payload is available in its **`detail`** property (e.g. `event.detail`).
> - With the **`on`** | **`once`** | **`off`** API, the callback receives the payload **directly** as its argument (e.g. `event`), without needing to access any `detail` property.

When the participant asks to close OpenVidu Meet, the component emits `embeddedCloseRequested`: that is the moment to remove it or show one of your own screens. Leaving the meeting does not emit it: `meetingLeft` fires and OpenVidu Meet shows its [End view](https://openvidu.io/3.9/meet/features/meetings/lifecycle/#end-view), and `embeddedCloseRequested` follows when the participant closes that view. The meeting may still be running for everyone else.

```javascript
const openviduMeet = document.querySelector('openvidu-meet');

openviduMeet.once('embeddedCloseRequested', () => {
    openviduMeet.remove();
});
```
