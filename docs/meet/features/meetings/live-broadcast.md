---
title: "Live broadcast in OpenVidu Meet"
description: "Stream an OpenVidu Meet meeting live to YouTube, Twitch or any RTMP server, to up to five destinations at once, each one started and stopped on its own."
page_features:
  - lazyvideo
---

# Live Broadcast

A meeting can be **streamed live** to an audience outside it, on YouTube, Twitch, Facebook or any RTMP server, without a separate streaming tool. Webinars, town halls and classes reach everyone who follows the channel while the meeting goes on as usual for its participants.

A meeting streams to up to **five destinations** at once. Each destination is its own **broadcast**: it starts, goes live, and stops or fails without touching the others, so a channel that drops its connection never takes the rest of the broadcast with it.

## Default destinations of a room { #room-destinations }

Live broadcast is turned on per room from the **Live broadcast** step of the room configuration wizard, when [creating](../rooms/management.md#create-rooms) or [editing](../rooms/management.md#edit-rooms) a room. The **Allow live broadcast** toggle needs at least one **default destination**: the channels the room's meetings go live to.

Each destination has a **name** and the **stream URL** the platform gives you, of the form `rtmp://host/app/key` or `rtmps://host/app/key`, stream key included. The wizard recognises the URLs of YouTube, Facebook, Instagram, X, Vimeo, Twitch and Kick, and shows each destination with its platform's logo. A room saves up to five destinations, each with its own stream key: two destinations with the same stream key are rejected, even on different servers.

**Stream keys stay hidden once saved**: the wizard, the REST API and every event show a destination URL with its stream key replaced by `********`. To change only the name of a destination, leave its URL as it is and the saved stream key is kept; to change the key, paste the full URL again.

The same step chooses the **layout** of the stream, with the same options as [recordings](../recordings/configuration.md): a grid of every participant, the active speaker with the others below, or the active speaker alone.

![Live broadcast step of the room wizard with two default destinations](../../../assets/images/meet/meetings/live-broadcast/room-wizard-broadcast-dark.webp#only-dark){ .round-corners loading=lazy }
![Live broadcast step of the room wizard with two default destinations](../../../assets/images/meet/meetings/live-broadcast/room-wizard-broadcast-light.webp#only-light){ .round-corners loading=lazy }

!!! info "Server upload"

    Every destination is a separate stream sent from your OpenVidu deployment, about **3 Mbps of upload each** at 720p. The wizard and the meeting show the estimate for the destinations chosen. Live broadcast runs on the deployment's egress service, the one that also produces [recordings](../recordings/overview.md), so the egress host needs outbound access to the RTMP servers.

## Going live { #going-live }

The **Live broadcast** activity sits in the **Activities** panel of the meeting, next to [recording](../recordings/overview.md). It lists the room's destinations under **Stream to**, all of them selected. Clear the ones this meeting should leave out and press **Go live**: each selected destination starts its own broadcast.

<a class="glightbox" href="/assets/videos/meet/meetings/live-broadcast/go-live-dark.mp4" data-type="video" data-gallery="dark"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/live-broadcast/go-live-dark.mp4#only-dark" preload="none" muted playsinline loop></video></a>
<a class="glightbox" href="/assets/videos/meet/meetings/live-broadcast/go-live-light.mp4" data-type="video" data-gallery="light"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/live-broadcast/go-live-light.mp4#only-light" preload="none" muted playsinline loop></video></a>

The **More options** menu of the toolbar offers **Start live broadcast** and **Stop live broadcast** too, which go live to every room destination or stop every broadcast at once.

A meeting goes live only while someone shares audio or video. Each destination shows **Connecting…** until the platform receives the meeting, and then **Live**. Every participant gets a notice when the meeting goes live and when the broadcast ends, and the status rail at the top of the meeting shows a **LIVE** mark for as long as the meeting is broadcast, with the time on air since the first destination received it. Clicking the mark opens the activity.

<a class="glightbox" href="/assets/videos/meet/meetings/live-broadcast/live-mark-dark.mp4" data-type="video" data-gallery="dark"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/live-broadcast/live-mark-dark.mp4#only-dark" preload="none" muted playsinline loop></video></a>
<a class="glightbox" href="/assets/videos/meet/meetings/live-broadcast/live-mark-light.mp4" data-type="video" data-gallery="light"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/live-broadcast/live-mark-light.mp4#only-light" preload="none" muted playsinline loop></video></a>

## Controlling each destination { #controlling-each-destination }

While the meeting is live, every destination is controlled on its own from the activity:

- **Stop** one destination: its broadcast ends at once and the others go on.
- **Start** a destination that was left out, or one stopped before: it starts a new broadcast while the others go on.
- **Retry** a destination that **failed**, for example because the platform rejected its stream key or lost the connection. The activity shows why it failed.
- **Stop broadcast** ends every broadcast of the meeting.

<a class="glightbox" href="/assets/videos/meet/meetings/live-broadcast/control-destinations-dark.mp4" data-type="video" data-gallery="dark"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/live-broadcast/control-destinations-dark.mp4#only-dark" preload="none" muted playsinline loop></video></a>
<a class="glightbox" href="/assets/videos/meet/meetings/live-broadcast/control-destinations-light.mp4" data-type="video" data-gallery="light"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/live-broadcast/control-destinations-light.mp4#only-light" preload="none" muted playsinline loop></video></a>

**Add destination** streams the meeting to a URL the room does not have, for this meeting only: give it a name and paste its full stream URL. It is never saved in the room, and only the browser that added it knows its stream key, so it can be started again only from there.

A broadcast never outlives its meeting: when the meeting ends, every broadcast ends with it.

## Who can go live { #who-can-go-live }

Two [room member permissions](../room-members/overview.md#permissions) control live broadcast:

- **`broadcastControl`** (**Go live**): start and stop the broadcasts of the room's destinations, all of them or only some.
- **`broadcastAddDestinations`** (**Add destinations**): stream the meeting to a destination the room does not have.

Both are granted by default to the `Moderator` [predefined role](../rooms/access.md#predefined-roles) and not to the `Speaker` role. They are independent, so a room can let its moderators choose among vetted channels without allowing them to stream anywhere else. Without `broadcastControl`, a participant sees the activity and the **LIVE** mark but cannot start or stop anything.

!!! warning "Not available with end-to-end encryption"

    A room with [end-to-end encryption](e2e-encryption.md) cannot be broadcast: the server cannot decrypt the meeting to stream it. Turning live broadcast on turns encryption off for the room, and the other way round.

## From your application { #embedded }

When OpenVidu Meet is [embedded](../../embedded/intro.md), the host application controls the broadcasts on behalf of the local participant with the `broadcastStart` and `broadcastStop` [commands](../../embedded/reference/webcomponent.md#commands) of the Web Component and the iframe. Without options, `broadcastStart` goes live to every room destination the meeting is not streaming to yet, and `broadcastStop` stops every broadcast. The `broadcastStarted`, `broadcastUpdated` and `broadcastEnded` [events](../../embedded/reference/webcomponent.md#events) report each broadcast of the meeting, whoever started it.

```javascript
const openviduMeet = document.querySelector('openvidu-meet');

openviduMeet.broadcastStart();

openviduMeet.on('broadcastUpdated', (event) => {
	if (event.status === 'active') {
		console.log(`Live on ${event.name}`);
	}
});
```

A backend controls the broadcasts of any room with the [REST API :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/broadcastStart){:target="_blank"}, shaped like the recordings one: start the broadcasts of a room, list them, read or stop one by its `broadcastId`, or stop several at once. The [`broadcastStarted`, `broadcastUpdated` and `broadcastEnded` webhooks](../../embedded/reference/webhooks.md) report each broadcast as it starts, goes live and ends, with its final status: `complete`, `failed` with the reason, or `aborted` when no media reached its destination. The meeting info says whether a broadcast is in progress with `broadcastActive`.
