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

!!! info
	You can get a room's URL programmatically from your application's backend: properties `moderatorUrl` and `speakerUrl` of object [MeetRoom](../../../assets/htmls/rest-api.html#/schemas/MeetRoom){:target="_blank"}.

## API Reference

### Attributes

Declare attributes in the component to customize the meeting for your user. For example:

```html
<openvidu-meet
	room-url="{{ my-room-url }}"
	participant-name="John Doe"
	leave-redirect-url="https://meeting.end.url/"
></openvidu-meet>
```

--8<-- "shared/meet/webcomponent-attributes.md"

### Commands

The OpenVidu Meet component exposes a set of commands that allow you to control the room from your application's logic.

```javascript
const openviduMeet = document.querySelector('openvidu-meet');
openviduMeet.leaveRoom();
```

--8<-- "shared/meet/webcomponent-commands.md"

### Events

The OpenVidu Meet component emits events that you can listen to in your application using standard JavaScript:

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

--8<-- "shared/meet/webcomponent-events.md"

## Examples

TODO: INCLUDE EXAMPLES HERE

- Basic Example
- Advanced Example with Customization
- Listen for events and handle them accordingly.
- Sending commands to the component.
