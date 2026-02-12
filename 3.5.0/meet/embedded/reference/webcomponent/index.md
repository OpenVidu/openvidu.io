# Web Component

OpenVidu Meet's Web Component allows embedding the refined, well-crafted OpenVidu Meet interface directly into your application. It offers **attributes** to customize the videoconferencing experience, exposes **commands** for programmatic control, and emits **events** for integration with your own application's logic.

## Installation

Include the following script in your HTML:

```html
<script src="https://{{ your-openvidu-deployment-domain }}/v1/openvidu-meet.js"></script>
```

## Usage

Add the `<openvidu-meet>` tag to your HTML. This will embed OpenVidu Meet interface into your application:

```html
<openvidu-meet room-url="{{ my-room-url }}"></openvidu-meet>
```

The only required attribute is **`room-url`**, which determines the room to join. Different instances of the web component using the same room URL will access the same meeting.

Info

You can get a room's URL programmatically from your application's backend: properties `moderatorUrl` and `speakerUrl` of object [MeetRoom](https://openvidu.io/3.5.0/meet/embedded/reference/api.html#/schemas/MeetRoom) .

## API Reference

### Attributes

Declare attributes in the component to customize the meeting for your user.

| Attribute              | Description                                                                                                     | Required                                                             |
| ---------------------- | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `room-url`             | The OpenVidu Meet room URL to connect to (moderator or speaker url)                                             | Yes (This attribute is required unless `recording-url` is provided.) |
| `recording-url`        | The URL of a recording to view.                                                                                 | Yes (This attribute is required unless `room-url` is provided.)      |
| `participant-name`     | Display name for the local participant.                                                                         | No                                                                   |
| `e2ee-key`             | Secret key for end-to-end encryption (E2EE). If provided, the participant will join the meeting using E2EE key. | No                                                                   |
| `leave-redirect-url`   | URL to redirect to when leaving the meeting. Redirection occurs after the **`CLOSED` event** fires.             | No                                                                   |
| `show-only-recordings` | Whether to show only recordings instead of live meetings.                                                       | No                                                                   |

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

| Method                                 | Command           | Description                                              | Parameters                      | Access Level |
| -------------------------------------- | ----------------- | -------------------------------------------------------- | ------------------------------- | ------------ |
| `endMeeting()`                         | `endMeeting`      | Ends the current meeting for all participants.           | -                               | Moderator    |
| `leaveRoom()`                          | `leaveRoom`       | Disconnects the local participant from the current room. | -                               | All          |
| `kickParticipant(participantIdentity)` | `kickParticipant` | Kicks a participant from the meeting.                    | • `participantIdentity`: string | Moderator    |

Invoke commands using JavaScript:

```javascript
const openviduMeet = document.querySelector('openvidu-meet');
openviduMeet.leaveRoom();
```

### Events

The OpenVidu Meet component emits events that you can listen to in your application.

| Event    | Description                                               | Payload                                                                                             |
| -------- | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `joined` | Event emitted when the local participant joins the room.  | `{      "roomId": "string",     "participantIdentity": "string" }`                                  |
| `left`   | Event emitted when the local participant leaves the room. | `{      "roomId": "string",     "participantIdentity": "string",     "reason": "LeftEventReason" }` |
| `closed` | Event emitted when the application is closed.             | -                                                                                                   |

Listen to events using JavaScript event listeners:

```javascript
const openviduMeet = document.querySelector('openvidu-meet');

openviduMeet.addEventListener('JOINED', (event) => {
    console.log('The local participant has joined the room!', event);
});
```

You can also use the API `on` | `once` | `off`:

```javascript
const openviduMeet = document.querySelector('openvidu-meet');

openviduMeet.on('JOINED', (event) => {
    console.log('The local participant has joined the room!', event);
});

openviduMeet.once('LEFT', (event) => {
    console.log('The local participant has left the room!', event);
});
```
