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

The only required attribute is **`room-url`**, which determines the room to access. Different instances of the web component using the same room URL will join the same meeting.

A room URL is a room access link

The **room URL** is simply a [room access link](https://openvidu.io/3.8.0/meet/features/rooms/access/index.md): the URL an individual opens to access a room. The role and identity a participant gets depend on **which** access link you use. This guide and most examples use the **anonymous** moderator/speaker links for simplicity, but a room also has **user** and **identified-guest** links — see [Room Access](https://openvidu.io/3.8.0/meet/features/rooms/access/index.md) for the full picture.

You can obtain a room's access links programmatically from your backend with the [REST API](https://openvidu.io/3.8.0/meet/embedded/reference/rest-api/index.md): the `access.anonymous.moderator.url`, `access.anonymous.speaker.url` and `access.user.url` properties of the [MeetRoom](https://openvidu.io/3.8.0/meet/embedded/reference/api.html#/schemas/MeetRoom) object, or the unique `accessUrl` of an [identified-guest member](https://openvidu.io/3.8.0/meet/features/room-members/overview/#users-vs-identified-guests).

## API Reference

### Attributes

Declare attributes in the component to customize the meeting for your user.

| Attribute              | Description                                                                                                           | Required                                                             |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `room-url`             | The OpenVidu Meet room URL to access to.                                                                              | Yes (This attribute is required unless `recording-url` is provided.) |
| `recording-url`        | The URL of a recording to view.                                                                                       | Yes (This attribute is required unless `room-url` is provided.)      |
| `participant-name`     | Display name for the local participant.                                                                               | No                                                                   |
| `e2ee-key`             | Secret key for end-to-end encryption (E2EE). If provided, the participant will join the meeting using E2EE key.       | No                                                                   |
| `leave-redirect-url`   | URL to redirect to when leaving OpenVidu Meet. Redirection occurs after the **`CLOSED` event** fires.                 | No                                                                   |
| `show-only-recordings` | Whether to show only recordings instead of live meetings.                                                             | No                                                                   |
| `show-recording`       | Identifier of the recording to display. When provided along with `room-url`, the app redirects to the recording view. | No                                                                   |

Example:

```html
<openvidu-meet
    room-url="{{ my-room-url }}"
    participant-name="John Doe"
    leave-redirect-url="https://meeting.end.url/"
></openvidu-meet>
```

### Commands

The OpenVidu Meet component exposes a set of commands that allow you to control the room from your application's logic.

| Method                                 | Command           | Description                                                 | Parameters                      | Access Level |
| -------------------------------------- | ----------------- | ----------------------------------------------------------- | ------------------------------- | ------------ |
| `endMeeting()`                         | `endMeeting`      | Ends the current meeting for all participants.              | -                               | Moderator    |
| `leaveRoom()`                          | `leaveRoom`       | Disconnects the local participant from the current meeting. | -                               | All          |
| `kickParticipant(participantIdentity)` | `kickParticipant` | Kicks a participant from the meeting.                       | • `participantIdentity`: string | Moderator    |

Invoke commands using JavaScript:

```javascript
const openviduMeet = document.querySelector('openvidu-meet');
openviduMeet.leaveRoom();
```

### Events

The OpenVidu Meet component emits events that you can listen to in your application.

| Event    | Description                                                  | Payload                                                                                             |
| -------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| `joined` | Event emitted when the local participant joins the meeting.  | `{      "roomId": "string",     "participantIdentity": "string" }`                                  |
| `left`   | Event emitted when the local participant leaves the meeting. | `{      "roomId": "string",     "participantIdentity": "string",     "reason": "LeftEventReason" }` |
| `closed` | Event emitted when the application is closed.                | -                                                                                                   |

Listen to events using JavaScript event listeners:

```javascript
const openviduMeet = document.querySelector('openvidu-meet');

openviduMeet.addEventListener('joined', (event) => {
    console.log('The local participant has joined the meeting', event.detail);
});
```

You can also use the API `on` | `once` | `off`:

```javascript
const openviduMeet = document.querySelector('openvidu-meet');

openviduMeet.on('joined', (event) => {
    console.log('The local participant has joined the meeting', event);
});

openviduMeet.once('left', (event) => {
    console.log('The local participant has left the meeting', event);
});
```

Accessing the event payload

The way you access the event payload depends on the method you use to listen:

- With the native **`addEventListener`** method, the callback receives a standard [`CustomEvent`](https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent) , so the payload is available in its **`detail`** property (e.g. `event.detail`).
- With the **`on`** | **`once`** | **`off`** API, the callback receives the payload **directly** as its argument (e.g. `event`), without needing to access any `detail` property.
