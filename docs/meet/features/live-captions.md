---
title: How to Enable Live Captions in OpenVidu Meet | Real-time Transcription Guide
description: Learn how to enable and use live captions in OpenVidu Meet to improve meeting accessibility with real-time speech-to-text transcriptions.
keywords: OpenVidu Meet, live captions, speech to text, real-time transcription, video conferencing accessibility, speech processing agent
---

# Live Captions in OpenVidu Meet

OpenVidu Meet includes a built-in **Live Captions** feature that turns speech into text in real-time. This is a powerful tool for making your meetings more accessible to hearing-impaired users, helping participants in noisy environments, and assisting non-native speakers.

## How to Enable Live Captions in OpenVidu Meet

### 1. Enable Live Captions Service in OpenVidu

--8<-- "shared/self-hosting/ssh-openvidu-deployment.md"


Modify file `agent-speech-processing.yaml` to enable the Live Captions Service with `processing: manual`:

```yaml
docker_image: docker.io/openvidu/agent-speech-processing-vosk:3.5.0

enabled: true # (1)!

live_captions:
  processing: manual # (2)!

```

1. Set `enabled` to `true` to activate the Speech Processing Agent.
2. Set **processing** to `manual`; `automatic` processing is not supported for OpenVidu Meet.


!!!info
	The Speech Processing Agent **uses a local Vosk model** for speech-to-text transcription by default. For a more advanced setup, consider using a cloud-based provider. See [Cloud providers](../../docs/ai/live-captions.md#cloud-providers) for more details.

### 2. Enable Captions in OpenVidu Meet configuration

1. SSH into an OpenVidu Node and navigate to the OpenVidu configuration directory.

	--8<-- "shared/self-hosting/ssh-openvidu-deployment.md"

2. Depending on your deployment type, edit **one** of the following files:
	- For **OpenVidu Local (Development)** deployments, edit `docker-compose.yml`.
	- For other deployment types, edit `meet.env`.

3. Ensure the following configuration variable is set:
	```
	MEET_CAPTIONS_ENABLED=true
	```

### 3. Restart OpenVidu

Apply your changes by restarting the OpenVidu. This ensures the system recognizes the new live captioning capabilities.

--8<-- "shared/self-hosting/restart-openvidu-deployment.md"

### 4. Enable/Disable Captions for specific Rooms

Captions are enabled by default when a room is created, whether through the UI or the [REST API](../embedded/reference/api.html#/operations/createRoom). This behavior can be overridden to enable or disable captions on a per-room basis.


---

## 🎙️ Using Live Captions in a Meeting

Once the meeting starts, the experience is seamless:

- **Automatic Transcription:** Captions appear instantly at the bottom of the screen as participants speak.
- **User Friendly:** No extra clicks are needed from the participants—the text appears automatically if the room was configured for captions.
- **Clear Visibility:** The interface is designed to be easy to read without blocking the video feed.

[Screenshot of Live Captions in Action]


