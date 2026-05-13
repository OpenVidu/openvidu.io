# Iframe

Embed OpenVidu Meet directly into your application using a traditional HTML iframe. This approach is perfect for applications that cannot use [OpenVidu Meet Web Component](https://openvidu.io/3.4.1/meet/embedded/reference/webcomponent/index.md) or need a simple integration method.

## Usage

Embed OpenVidu Meet by adding an iframe to your HTML with the room URL and required permissions:

```html
<iframe
    src="https://your-meet-domain.com/room/MyRoom-abcdef?secret=12345"
    allow="camera; microphone; display-capture; fullscreen; autoplay; compute-pressure;"
    width="100%" height="100%">
</iframe>
```

### Required iframe attributes

- **`src`**: The room URL to join
- **`allow`**: Permissions required for the meeting to work properly:
  - `camera`: Access to the camera
  - `microphone`: Access to the microphone
  - `display-capture`: Screen sharing capability
  - `fullscreen`: Full screen mode
  - `autoplay`: Media autoplay
  - `compute-pressure`: Device performance monitoring

Info

You can get room URLs programmatically from your backend using the [REST API](https://openvidu.io/3.4.1/meet/embedded/reference/api.html#/schemas/MeetRoom) properties `moderatorUrl` or `speakerUrl`.

## API Reference

### Attributes

Info

The iframe accepts the same **attributes** as the OpenVidu Meet Web Component. See [Web Component Attributes](https://openvidu.io/3.4.1/meet/embedded/reference/webcomponent/#attributes) for the full list and descriptions.

Customize the **participant name** and meeting redirect by adding attributes as query parameters in the iframe src URL.

```html
<iframe
    src="https://your-meet-domain.com/room/MyRoom-abcdef?secret=12345&participant-name=John&leave-redirect-url=https://meeting.end.url/"
    allow="camera; microphone; display-capture; fullscreen; autoplay; compute-pressure;"
    width="100%" height="100%">
</iframe>
```

### Commands

Info

The iframe accepts the same **commands** as the OpenVidu Meet Web Component. See [Web Component Commands](https://openvidu.io/3.4.1/meet/embedded/reference/webcomponent/#commands) for the full list and descriptions.

Control the meeting programmatically by sending commands via `postMessage` to the iframe's content window:

```javascript
const iframe = document.querySelector('iframe');
const targetOrigin = '*'; // Replace with your actual domain
iframe.contentWindow.postMessage({ command: 'leaveRoom' }, targetOrigin);
```

### Events

Info

The iframe emits the same **events** as the OpenVidu Meet Web Component. See [Web Component Events](https://openvidu.io/3.4.1/meet/embedded/reference/webcomponent/#events) for the full list and descriptions.

Listen to meeting events by monitoring messages from the iframe:

```javascript
const iframe = document.querySelector('iframe');

window.addEventListener('message', (event) => {
    // Verify the event origin for security
    if (event.origin !== 'https://your-meet-domain.com') return;

    const message = event.data;

    if (!message || !message.event) {
        return;
    }

    console.log('Received event from iframe:', message.event, message.payload);
});
```
