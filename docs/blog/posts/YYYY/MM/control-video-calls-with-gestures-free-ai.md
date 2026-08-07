---
title: "Control your video calls with gestures using free AI"
draft: false
date: 2026-08-06
slug: control-video-calls-with-gestures-free-ai
description: "Control your camera, microphone and hand-raise requests with hand gestures, using MediaPipe in the browser, at no cost and without sending video to the cloud."
cover_image: cover.webp
categories:
  - AI
  - Technology
  - Livekit
tags:
  - MediaPipe
  - Gestures
  - WebRTC
  - Privacy
  - LiveKit
  - Computer Vision
authors:
  - csantosm
hide:
  - navigation
  - search-bar
  - version-selector
---

# Control your video calls with hand gestures, thanks to a free AI from Google

![Hand gesture recognition in a video call, processed in the browser with free AI](/assets/images/blog/YYYY/MM/control-video-calls-with-gestures-free-ai/cover.webp "Control your video call with gestures")

If you're tired of reaching for the cursor to hit the camera icon every time you want to disappear from the meeting, you're in luck. At **OpenVidu** we've built an open-source prototype that lets you control your video call's features with gestures, like an actual tech shaman.

<!-- more -->

## What this demo does

This open-source demo lets you control your own video call with four hand gestures, without touching the keyboard or the mouse.

I'll confess it: you'll feel like Harry Potter on his first day of class...

![OpenVidu gesture control](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXBvdmlnMjF4a2phc3ZnejI1dndsemhuZjR0dzhuNWF4MmZsMG9ydSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/N7aCOnWxcmMSlOy2eH/giphy.gif)

but no, it's not magic. These gestures are recognized in real time with [MediaPipe Gesture Recognizer](https://developers.google.com/edge/mediapipe/solutions/vision/gesture_recognizer){:target="_blank"}, a **free** AI model that runs in the browser itself and lets you detect gestures without sending video to the cloud. We can pair these gestures with real actions in the video call, like turning off the camera, muting the microphone, and so on.

The gestures we've wired up are:

- **✊ Closed fist.** Turns off your camera. Close the fist again and it turns back on.
- **☝️ Index finger raised.** Mutes or unmutes your microphone.
- **✋ Open palm.** Raises your hand — the rest of the room sees a pulsing badge appear on your tile within a second.
- **✌️ Victory sign.** Shows or hides, only in your own view, the hand-tracking skeleton MediaPipe is reading from your hand at that instant.

Each gesture has to be held steady for a period of time (650 ms) for the action to fire, which keeps an unintentional gesture from triggering the action.

## What MediaPipe is

[MediaPipe](https://developers.google.com/edge/mediapipe){:target="_blank"} is Google's family of computer vision models, built to run on your own device instead of on a server.

And no, it's not complex to install and set up. Using it is as straightforward as this:

```ts
import * as vision from '@mediapipe/tasks-vision';

const TASKS_VISION_VERSION = '0.10.14';

const WASM_FILESET_URL = `https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@${TASKS_VISION_VERSION}/wasm`;

const MODEL_URL =
  'https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task';


const fileSet = await vision.FilesetResolver.forVisionTasks(WASM_FILESET_URL);
this.recognizer = await vision.GestureRecognizer.createFromOptions(fileSet, {
  baseOptions: { modelAssetPath: MODEL_URL, delegate: 'GPU' },
  runningMode: 'VIDEO',
  numHands: 1,
  minHandDetectionConfidence: 0.5,
  minHandPresenceConfidence: 0.5,
  minTrackingConfidence: 0.5,
});
```

These models are free and open source. Google maintains and updates them under the Apache 2.0 license, and you can use them in your own project at no cost at all. You can check MediaPipe's privacy policy [here](https://github.com/google-ai-edge/mediapipe#privacy-notice){:target="_blank"}.

MediaPipe isn't the only option, though. If you need more precision or dedicated commercial support instead, [Banuba](https://www.banuba.com/technology/hand-tracking-and-gesture-recognition){:target="_blank"}, a commercial SDK built on its own proprietary neural networks, explicitly marketed for video chats, is worth a look too.

## Wiring gestures up to OpenVidu

Once gesture detection is solved, all that's left is hooking it up to the video call.

There are 4 gestures we've assigned actions to:

1. Turn the camera on/off
2. Mute/unmute the microphone
3. Show/hide the hand-tracking skeleton (only in your own view)
4. Raise/lower the hand

OpenVidu lets us control the camera and microphone with these two simple calls:

```ts
room.localParticipant.setCameraEnabled(false);
room.localParticipant.setMicrophoneEnabled(false);
```

Other participants find out that your camera or microphone are off thanks to OpenVidu's own architecture.

Raising your hand, however, needs to notify the other participants manually, so it's sent as a *participant attribute*:

```ts
room.localParticipant.setAttributes({ handRaised: '1' });
```

The rest of the participants receive it by subscribing to `RoomEvent.ParticipantAttributesChanged`. For someone to be able to write their own attributes, the token server needs to add the `canUpdateOwnMetadata` grant when issuing the token:

```js
at.addGrant({ roomJoin: true, room: roomName, canUpdateOwnMetadata: true });
```

## Problems we ran into, and how we fixed them

The first time I tried the prototype, I did exactly what anyone would do: I closed my fist to turn off the camera.

Brilliant, I thought. The model recognized the gesture perfectly and turned off the camera... What I didn't think about is that by turning off the camera, the model stopped seeing my hand and recognizing any gesture at all.

<figure markdown>
  ![Confused robot gif representing the model losing hand tracking](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2c0OHYyemhvaXZkZDdpb20xZTkxNGNtNnh2bDRqaWNtZjhvdmVtcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/h8HmN0UcEKR0xWnv3R/giphy.gif)
  <figcaption>What the model thought when I tried this</figcaption>
</figure>

The fix is to feed the model from a hidden capture, not from the track that gets published to the room. That way, the AI model keeps seeing your hand exactly the same whether the camera is off or on.

## What this actually costs, in resources

Measuring the resources needed, on a laptop with an integrated GPU, we can see that the AI's cost is very low, and that you don't need a dedicated GPU for it to run in real time:

| Resource | Measured figure |
|---|---|
| Per-frame inference, GPU | ≈ 9.2 ms on average — 11% of the 83 ms budget per cycle at 12 Hz |
| Per-frame inference, CPU (no GPU available) | ≈ 35 ms on average — 3.8× slower than GPU, but still 42% of the budget, comfortably real-time |
| Memory (JS heap) per recognizer instance | ≈ 32 MB |

**You don't need a dedicated GPU.** The GPU delegate uses WebGL2, supported on practically any desktop or mobile browser today, including integrated GPUs from a decade ago.

## Try it in two minutes

**Repository:** [github.com/openvidu-labs/openvidu-gestures](https://github.com/openvidu-labs/openvidu-gestures){:target="_blank"}

You'll need [Node.js](https://nodejs.org/en/download){:target="_blank"} and [OpenVidu Local](/docs/self-hosting/local.md) up and running. Then:

```bash
# Terminal 1 — OpenVidu
git clone https://github.com/OpenVidu/openvidu-local-deployment -b 3.8.0
cd openvidu-local-deployment/community
./configure_lan_private_ip_linux.sh
docker compose up

# Terminal 2 — token server
cd server
npm install
npm start   # serves POST /token on port 6084

# Terminal 3 — client
cd client
npm install
npm run dev
```

Open [`http://localhost:5094`](http://localhost:5094) and start trying out the gestures.

## Where to go from here

Everything in this demo runs on your own machine: MediaPipe never sends a single frame anywhere, and the OpenVidu Local deployment you just spun up runs the call itself on your own infrastructure too. Local AI plus a self-hosted video platform means every byte of video and metadata stays under your control, with no per-minute SaaS bill and no third party watching your calls.

If gesture control isn't what you need but self-hosting your own video infrastructure is, that's exactly what **[OpenVidu](/docs/index.md)** is for: the same LiveKit-compatible core you just used, wrapped in a production-ready platform you can run anywhere, from a one-command local install to a highly available cluster. The [self-hosting docs](/docs/self-hosting/local.md) are the natural next step.
