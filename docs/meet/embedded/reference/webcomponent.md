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
	You can get a room's URL programmatically from your application's backend: properties `moderatorUrl` and `speakerUrl` of object [MeetRoom :fontawesome-solid-external-link:{.external-link-icon}](../../../assets/htmls/rest-api.html#/schemas/MeetRoom){:target="_blank"}.

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

#### Passing attributes to a direct link or iframe

If you are using a direct link or an iframe to embed OpenVidu Meet instead of using the web component, you can pass the [same attributes](#attributes) as query parameters in the room URL. For example, if your room URL is ...

`http://my.domain.com/room/MyRoom-abcdef?secret=12345`{.code-margin-left}

... to pass attribute `participant-name` ...

<code class="code-margin-left">http://my.domain.com/room/MyRoom-abcdef?secret=12345<strong class="accent-code">&participant-name=Alice</strong></code>

This is what it would look like when using a URL or an iframe:

=== "Using a URL"

	```html
	<a href="http://my.domain.com/room/MyRoom-abcdef?secret=12345&participant-name=Alice">Join Room</a>
	```

=== "Using an iframe"

	```html
	<iframe
		src="http://my.domain.com/room/MyRoom-abcdef?secret=12345&participant-name=Alice"
		allow="camera; microphone; display-capture; fullscreen; autoplay; compute-pressure;"
		width="100%" height="100%">
	</iframe>
	```

### Commands

The OpenVidu Meet component exposes a set of commands that allow you to control the room from your application's logic.

```javascript
const openviduMeet = document.querySelector('openvidu-meet');
openviduMeet.leaveRoom();
```

--8<-- "shared/meet/webcomponent-commands.md"

#### Sending commands to an iframe

If you are using an iframe to embed OpenVidu Meet, you can still use the same commands by accessing the iframe's content window. For example:

```javascript
const iframe = document.querySelector('iframe');
iframe.contentWindow.postMessage({ command: 'leaveRoom' }, '*');
```

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

#### Receiving events from an iframe

If you are using an iframe to embed OpenVidu Meet, you can still listen for events by accessing the iframe's content window. For example:

```javascript
const iframe = document.querySelector('iframe');
iframe.contentWindow.addEventListener('message', (message) => {
	if (message.event === 'JOINED') {
		console.log('The local participant has joined the room!', message.payload);
	}
	if (message.event === 'LEFT') {
		console.log('The local participant has left the room!', message.payload);
	}
});
```
