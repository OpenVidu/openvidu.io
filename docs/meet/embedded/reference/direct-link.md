# Direct Link

Redirect users to OpenVidu Meet using simple HTML links. This is the simplest way to integrate OpenVidu Meet into your application - perfect when you want users to join meetings in a new browser tab or window with the polished OpenVidu Meet interface.

## Usage

Create a direct link to an OpenVidu Meet room using a simple HTML anchor tag:

```html
<a href="https://your-domain.com/meet/room/my_room-abcdef?secret=12345">Join Room</a>
```

When users click the link, they'll be redirected to OpenVidu Meet in their browser, ready to join the room.

!!! info "A room URL is a room access link"
    The room URL is a [room access link](../../features/rooms/access.md). The examples use the **anonymous** moderator/speaker links, but a room also has **user** and **identified-guest** links — see [Room Access](../../features/rooms/access.md) for all of them.

    You can get them programmatically from your backend with the [REST API](./api.html#/schemas/MeetRoom){:target="\_blank"}: the `access.anonymous.moderator.url`, `access.anonymous.speaker.url` and `access.user.url` properties of the `MeetRoom` object, or an identified guest's `accessUrl`.

## API Reference

### Attributes

!!! info
	Direct links accept the same **attributes** as the OpenVidu Meet Web Component. See [Web Component Attributes](./webcomponent.md#attributes) for the full list and descriptions.

Customize the meeting by passing attributes as query parameters in the room URL:

```html
<a href="https://your-domain.com/meet/room/my_room-abcdef?secret=12345&participant-name=John&leave-redirect-url=https://meeting.end.url/">
    Join Room as John
</a>
```


### Commands

Direct links do not support programmatic commands since the meeting runs in a separate browser context. If you need to control the meeting programmatically, consider using the [Web Component](./webcomponent.md) or [Iframe](./iframe.md) approaches instead.

### Events

Direct links do not emit events to your application since the meeting runs in a separate browser context. If you need to listen to meeting events, consider using the [Web Component](./webcomponent.md) or [Iframe](./iframe.md) approaches instead.
