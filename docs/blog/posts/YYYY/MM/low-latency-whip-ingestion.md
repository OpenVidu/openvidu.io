---
title: 'Low Latency Live Streaming: Ingest WHIP into OpenVidu (Part 2)'
draft: false
date: 2026-09-03
slug: low-latency-whip-ingestion
description: >-
  Push a real stream into an OpenVidu Room over WHIP, from a browser webcam and
  from OBS Studio, and watch it arrive with sub-second delay.
categories:
  - How-to
  - Technology
tags:
  - WebRTC
  - WHIP
  - Live Streaming
  - Low Latency
  - OBS
  - Self-hosted
authors:
  - patxi
---

# Low Latency Live Streaming: Ingest WHIP into OpenVidu (Part 2)

<!-- IMAGE: poster-light.webp / poster-dark.webp — a browser webcam tile and the OBS interface on
     the left, both feeding an arrow labelled "WHIP" into an OpenVidu Room on the right, with a
     viewer's browser coming out of it. Alt: "A browser and OBS Studio pushing video into an
     OpenVidu Room over WHIP". Place immediately below the H1, light and dark variants, and point
     cover_image at the light one. -->

Part 1 of this series argued that if your video has to close a feedback loop with the person watching it, HLS and DASH structurally can't get you there and WebRTC can. That's the theory, and theory is cheap. So let's do the thing itself: take a webcam, push it into a self-hosted <a href="/docs/">OpenVidu Platform</a> Room over WHIP, and watch it come out the other side fast enough to have a conversation through. Then do it again from OBS Studio, which has spoken WHIP natively since version 30 and needs no plugin, no SDK and no code at all.

<!-- more -->

If you haven't read it, [Part 1: WebRTC vs. HLS and DASH](/blog/posts/2026/09/low-latency-live-streaming.md) is where the *why* lives — what counts as low latency, and why a segmented protocol can't reach it. This post is the *how*.

!!! abstract "What you'll build"
    A local loop you can watch yourself: a small Node app that mints WHIP credentials against
    OpenVidu, a browser page that publishes your camera straight over WHIP, an OBS scene that does
    the same thing from a real production tool, and a viewer page that subscribes to the Room. All
    of it runs on your machine with Docker Compose. The code is at
    [openvidu-labs/low-latency-whip-ingestion](https://github.com/openvidu-labs/low-latency-whip-ingestion){:target="_blank"}.

## WHIP, in one paragraph

WebRTC's reputation for being hard is mostly about signaling: the protocol never said how two peers
should exchange their session descriptions, so everyone built their own. **[WHIP](https://datatracker.ietf.org/doc/rfc9725/){:target="_blank"}** (WebRTC-HTTP Ingestion Protocol) ends that argument for the
one-way ingest case, and it is almost comically small. You `POST` your SDP offer to a URL with a
bearer token. The server answers `201 Created` with the SDP answer in the body. That's it — that is
the entire handshake. Everything after it is ordinary WebRTC: SRTP over UDP, ICE for connectivity,
media flowing continuously with nothing batched into segments.

The reason that matters for this series is what *doesn't* happen. There's no manifest to write, no
segment duration to pick, no player buffer to tune. The delay you get is the delay of the network
plus the encoder, which is why this path lands under a second where a chunked one starts at several.

## The demo app

OpenVidu Platform is a self-hosted, [LiveKit](https://livekit.io/){:target="_blank"}-compatible
server, and its Ingress module exposes a WHIP endpoint. There is no OpenVidu-specific ingestion API
to learn: the demo talks to it with LiveKit's own server SDK, exactly as
<a href="/docs/build-your-app/common-operations/#stream-ingestion">OpenVidu's own docs</a> suggest.

The whole backend is two endpoints:

| Endpoint | What it does |
|---|---|
| `POST /api/ingress` | Creates a WHIP ingress on the Room and returns the `url` and `streamKey` an encoder needs |
| `GET /api/viewer-token` | Mints a **subscribe-only** access token so a browser can watch, but never publish |

That asymmetry is the interesting part of the design. The publisher side needs no SDK at all — a
`fetch()` and an `RTCPeerConnection` are enough, which is precisely why OBS can do it too. The
viewer side is a normal WebRTC subscriber, so it uses the client SDK like any other participant in
the Room.

```
Browser webcam ──┐
                 ├── WHIP (HTTP + SDP) ──▶ OpenVidu Room ──▶ WebRTC ──▶ viewer's browser
OBS Studio ──────┘
```

## Get it running

Two stacks: OpenVidu itself, and the demo app that joins its Docker network. The app deliberately
doesn't bundle OpenVidu — you add ingestion to a deployment you don't otherwise control, which is
how it works in real life too.

```bash
git clone https://github.com/openvidu-labs/low-latency-whip-ingestion
cd low-latency-whip-ingestion
make setup                      # clones the OpenVidu Local Deployment, pinned to 3.8.0
cd vendor/openvidu-local-deployment/community && docker compose up -d && cd -
docker compose up -d --build    # the demo app, on port 3000
```

Wait for the `🎉 OpenVidu is ready! 🎉` banner before you carry on — it's eleven containers and the
first boot pulls a lot of images:

```bash
docker compose -f vendor/openvidu-local-deployment/community/docker-compose.yaml logs -f openvidu
```

Then open **<http://localhost:3000>**. There are two things to click: *Publish from your webcam* and
*Watch the stream*. Open them in two tabs and you have the whole loop in front of you.

!!! tip "Watch them side by side"
    Put the publisher tab and the viewer tab next to each other and wave at the camera. What you're
    looking for is that the wave arrives while your hand is still moving. That's the difference this
    series is about, and it's much more convincing than a number.

<!-- IMAGE: screenshot of the two tabs side by side, publisher left, viewer right, both showing the
     same webcam frame. Alt: "The publisher and viewer pages side by side, showing the same frame".
     Place right after this tip. -->

## Publishing from the browser

The browser publisher is about forty lines, and none of them are OpenVidu-specific. That is the
point worth taking away from this section: WHIP is small enough to hand-write, so a web app can
publish into your platform without shipping an SDK at all.

```javascript
const pc = new RTCPeerConnection({ iceServers: [] });

// Send-only: this peer publishes, it never receives.
for (const track of stream.getTracks()) {
  pc.addTransceiver(track, { direction: 'sendonly', streams: [stream] });
}

await pc.setLocalDescription(await pc.createOffer());
await waitForIceGatheringComplete(pc);        // non-trickle: send every candidate at once

const response = await fetch(whipUrl, {
  method: 'POST',
  headers: { 'Content-Type': 'application/sdp', Authorization: `Bearer ${streamKey}` },
  body: pc.localDescription.sdp,
});

await pc.setRemoteDescription({ type: 'answer', sdp: await response.text() });
```

Two details in there are worth a second look.

- **`sendonly` transceivers.** An ingest is one-directional, and saying so in the offer keeps the
  negotiated session honest — the server never has to answer with tracks nobody wants.
- **Waiting for ICE gathering.** WHIP allows trickle ICE, but a single `POST` that already carries
  every candidate is simpler and perfectly fine on a LAN. A production publisher on a flaky network
  would usually trickle instead, to start media sooner.

The `Location` header in the response points at a resource you can `DELETE` to end the session
cleanly. Browsers can only read that header if the server sends
`Access-Control-Expose-Headers: Location`; when it doesn't, closing the peer connection ends the
stream anyway, just less tidily on the server side.

## Publishing from OBS

Here's the part that surprises people: **OBS needs no plugin for this.** WHIP has been a built-in
output since OBS 30, sitting in the same *Service* dropdown as Twitch and YouTube. Everything you
already do in OBS — scenes, overlays, multiple cameras, a green screen — arrives in your OpenVidu
Room over WebRTC.

Generate a set of credentials from the app, either by clicking **Generate WHIP credentials** at
<http://localhost:3000> or with curl:

```bash
curl -s -X POST http://localhost:3000/api/ingress \
  -H 'Content-Type: application/json' \
  -d '{"identity":"obs"}'
```

```json
{
  "roomName": "demo-room",
  "participantIdentity": "obs",
  "url": "http://localhost:7885/w",
  "streamKey": "<a long single-use token>"
}
```

Then, in **Settings → Stream**:

| Field | Value |
|---|---|
| **Service** | `WHIP` |
| **Server** | the `url` from the response |
| **Bearer Token** | the `streamKey` from the response |

**Apply**, then **Start Streaming**, then open
<http://localhost:3000/watch.html>. Your OBS scene is in the Room.

<!-- IMAGE: screenshot of OBS Settings → Stream with Service set to WHIP and the Server/Bearer Token
     fields filled in (token redacted). Alt: "OBS Settings → Stream with the WHIP service selected".
     Place right after this table. -->

### A scene collection to start from

Building the scene by hand every time gets old, so the repo ships one:
[`obs/openvidu-whip-webcam.json`](https://github.com/openvidu-labs/low-latency-whip-ingestion/blob/main/obs/openvidu-whip-webcam.json){:target="_blank"}.
Import it with **Scene Collection → Import** and you get a webcam filling a 720p canvas, a backdrop
behind it, your default microphone, and a virtual-background filter already wired up.

There are three scenes in it, one per operating system, because a capture source's internal id is
platform-specific — `v4l2_input` on Linux, `av_capture_input` on macOS, `dshow_input` on Windows.
Keep the one for your machine and delete the other two.

The collection carries **no stream settings on purpose**. A WHIP token is single-use and yours; it
has no business sitting in a file in a git repository.

### The virtual background

The *Virtual background* filter on the camera is
[obs-backgroundremoval](https://github.com/locaal-ai/obs-backgroundremoval){:target="_blank"}, which
is a plugin rather than something OBS ships. Without it, the collection still imports and the camera
still streams — you just get your real background:

```bash
# Flatpak OBS on Linux; installers for other platforms are on the plugin's releases page
flatpak install flathub com.obsproject.Studio.Plugin.BackgroundRemoval
```

If the filter doesn't appear on the camera after installing it, add it by hand
(**right-click the camera → Filters → + → Background Removal**) — the filter's internal id has
changed between plugin releases. And if you'd rather not add a plugin at all, OBS's built-in
**Chroma Key** does the same job with a green screen for almost no CPU.

!!! note "Segmentation isn't free"
    Background removal runs an inference model on every frame. On a laptop that is also running
    eleven OpenVidu containers, that shows up as a stutter — and it is tempting to blame WHIP for
    it. Drop the camera to 720p, or watch the encoder's frame drops in OBS's stats panel, before you
    go looking for the delay anywhere else.

## Watching it

The viewer is a normal WebRTC subscriber. The app mints it a token that can join and subscribe but
**not** publish, so the page can't accidentally start sending video:

```javascript
const token = new AccessToken(API_KEY, API_SECRET, { identity, ttl: '2h' });
token.addGrant({ room: ROOM_NAME, roomJoin: true, canSubscribe: true, canPublish: false });
```

In the browser, connecting and rendering is two events:

```javascript
const room = new Room();
room.on(RoomEvent.TrackSubscribed, (track) => track.attach(videoElement));
await room.connect(livekitUrl, token);
```

Whatever is publishing into the Room — the browser page, OBS, both at once — shows up here as a
participant with tracks. From OpenVidu's point of view a WHIP ingress *is* a participant, which is
why nothing about the viewer has to know how the media got in.

## Why this path is the low-latency one

One line in the app does more for latency than everything else put together:

```javascript
await ingressClient.createIngress(IngressInput.WHIP_INPUT, {
  roomName: ROOM_NAME,
  participantIdentity: identity,
  enableTranscoding: false,
});
```

With transcoding off, OpenVidu forwards the encoder's own codec, untouched. Nothing decodes and
re-encodes your video on the way through, which is where a good chunk of avoidable delay usually
lives — and the CPU that would have gone into it stays free. It's the default for WHIP ingress in
LiveKit, and the demo sets it explicitly so you can see it rather than discover it in the SDK
source.

The trade is compatibility: if a publisher shows up with a codec the subscribers can't play, nothing
transcodes it into one they can. Turning transcoding on buys that flexibility back and costs you
some of the latency you came here for.

The other knob is on the OBS side. Set the keyframe interval to **1 second** in
**Settings → Output** — a new subscriber can't render anything until a keyframe arrives, so a long
interval shows up as a slow join, not as ongoing delay.

## When it doesn't work

Three things account for most of it:

- **"Could not create ingress. Is the OpenVidu stack up?"** — the app container can't reach
  `http://openvidu:7880`. Check that `docker network inspect openvidu-community` lists both the app
  and the OpenVidu containers.
- **OBS has no `WHIP` under Service.** You're on OBS < 30, or on the Ubuntu 24.04 PPA build, which
  ships without the WebRTC output. The [Flatpak build](https://flathub.org/apps/com.obsproject.Studio){:target="_blank"}
  has it.
- **The second stream never appears.** Each set of credentials is one ingress. Stop streaming,
  generate a fresh set, start again — the old one isn't reused.

## Need more than this?

You now have a stream going into a self-hosted WebRTC platform from a browser and from a real
production encoder, with no transcoding in the path and no proprietary ingest protocol anywhere. The
next post in this series looks outward: which tools out there can already speak WHIP — hardware
encoders, mobile apps, ffmpeg builds, cloud services — and what to do when the one you're stuck with
can't.

To go further:

- [Part 1: WebRTC vs. HLS and DASH](/blog/posts/2026/09/low-latency-live-streaming.md) — why this
  works, if you jumped straight to the code.
- [Stream ingestion](/docs/build-your-app/common-operations.md#stream-ingestion) — WHIP ingest in
  your own app, beyond the demo.
- [OpenVidu Local Deployment](/docs/self-hosting/local.md) — the stack this post runs on, and how to
  take it somewhere that isn't your laptop.
- [OpenVidu Platform](/docs/index.md) — the SDKs and APIs underneath all of it.
