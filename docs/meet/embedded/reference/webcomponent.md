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

!!! info "A room URL is a room access link"
	The **room URL** is simply a [room access link](../../features/rooms/access.md): the URL an individual opens to access a room. The role and identity a participant gets depend on **which** access link you use. This guide and most examples use the **anonymous** moderator/speaker links for simplicity, but a room also has **user** and **identified-guest** links — see [Room Access](../../features/rooms/access.md) for the full picture.

	You can obtain a room's access links programmatically from your backend with the [REST API](./rest-api.md): the `access.anonymous.moderator.url`, `access.anonymous.speaker.url` and `access.user.url` properties of the [MeetRoom :fontawesome-solid-external-link:{.external-link-icon}](./api.html#/schemas/MeetRoom){:target="_blank"} object, or the unique `accessUrl` of an [identified-guest member](../../features/room-members/overview.md#users-vs-identified-guests).

## API Reference

### Attributes

Declare attributes in the component to customize the meeting for your user.

--8<-- "shared/meet/webcomponent-attributes.md"

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

--8<-- "shared/meet/webcomponent-commands.md"

Invoke commands using JavaScript:

```javascript
const openviduMeet = document.querySelector('openvidu-meet');
openviduMeet.leaveRoom();
```



### Events

The OpenVidu Meet component emits events that you can listen to in your application.

--8<-- "shared/meet/webcomponent-events.md"


Listen to events using JavaScript event listeners:

```javascript
const openviduMeet = document.querySelector('openvidu-meet');

openviduMeet.addEventListener('joined', (event) => {
	console.log('The local participant has joined the meeting!', event);
});
```

You can also use the API `on` | `once` | `off`:

```javascript
const openviduMeet = document.querySelector('openvidu-meet');

openviduMeet.on('joined', (event) => {
	console.log('The local participant has joined the meeting!', event);
});

openviduMeet.once('left', (event) => {
	console.log('The local participant has left the meeting!', event);
});
```


