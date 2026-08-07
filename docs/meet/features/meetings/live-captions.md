---
title: "Live captions in OpenVidu Meet"
description: "Turn on real-time speech-to-text captions in an OpenVidu Meet meeting to make it accessible, and choose the language each participant reads."
keywords: OpenVidu Meet, live captions, speech to text, real-time transcription, video conferencing accessibility, speech processing agent
tags:
    - setupcustomgallery
---

# Live Captions

OpenVidu Meet includes a built-in **Live Captions** feature that turns speech into text in real-time. This is a powerful tool for making your meetings more accessible to hearing-impaired participants, helping participants in noisy environments, and assisting non-native speakers.

## How to Enable Live Captions in OpenVidu Meet

!!! warning "Local Meet Deployment Limitation"

    Live Captions are **not available** in local Meet deployments. You must use either the [OpenVidu Local deployment](../../../docs/self-hosting/local.md) or an [OpenVidu production deployment](../../../docs/self-hosting/deployment-types.md) to enable this feature.

### 1. Connect to your OpenVidu deployment

SSH into an OpenVidu Node and navigate to your OpenVidu deployment directory.

--8<-- "shared/self-hosting/common/ssh-openvidu-deployment.md"

### 2. Enable the Speech Processing Agent

Modify file `agent-speech-processing.yaml` to enable the Live Captions Service with `processing: manual`:

```yaml
docker_image: docker.io/openvidu/agent-speech-processing-vosk:3.8.0

enabled: true # (1)!

live_captions:
    processing: manual # (2)!
```

1. Set `enabled` to `true` to activate the Speech Processing Agent.
2. Set **processing** to `manual`; participants will activate captions on demand via a toolbar button.

!!! info

    By default, the Speech Processing Agent uses a local Vosk model for speech-to-text transcription.

    For a more advanced setup, consider using a cloud-based provider. See [Cloud providers](../../../docs/ai/live-captions.md#cloud-providers) for more information.

!!! warning "Default language is English"

    The Speech Processing Agent uses **English** for speech-to-text transcription by default. To use a different language, you must configure a different Vosk model. See [Vosk models configuration](../../../docs/ai/live-captions.md#vosk) for details on changing the language model.

### 3. Enable Captions in OpenVidu Meet configuration

Edit the `meet.env` file and ensure the following configuration variable is set:

```
MEET_CAPTIONS_ENABLED=true
```

### 4. Restart OpenVidu

Apply your changes by restarting OpenVidu. This ensures the system recognizes the new live captioning capabilities.

--8<-- "shared/self-hosting/common/restart-openvidu-deployment.md"

### 5. Enable/Disable Captions for specific Rooms

Captions are enabled by default when a room is [created](../rooms/management.md#create-rooms), whether through the UI or the [REST API :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/createRoom){:target="_blank"}. This behavior can be overridden to enable or disable captions on a per-room basis from the **Room Features** step of the room configuration wizard, using the **Captions** toggle.

<a class="glightbox" href="/assets/images/meet/meetings/live-captions/room-wizard-captions-dark.webp" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="/assets/images/meet/meetings/live-captions/room-wizard-captions-dark.webp#only-dark" loading="lazy" class="round-corners" alt="Room wizard step enabling live captions for the room"/></a>
<a class="glightbox" href="/assets/images/meet/meetings/live-captions/room-wizard-captions-light.webp" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="/assets/images/meet/meetings/live-captions/room-wizard-captions-light.webp#only-light" loading="lazy" class="round-corners" alt="Room wizard step enabling live captions for the room"/></a>

## Using Live Captions in a Meeting

Once live captions are enabled for a room, any participant can turn them on during the meeting by clicking the **captions button** in the toolbar. Captions then appear instantly at the bottom of the screen as participants speak, with no additional configuration required. The interface is designed to be easy to read without blocking the video feed.

<a class="glightbox" href="/assets/videos/meet/meetings/live-captions/enable-captions-dark.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="/assets/videos/meet/meetings/live-captions/enable-captions-dark.mp4#only-dark" loading="lazy" defer muted playsinline autoplay loop async></video></a>
<a class="glightbox" href="/assets/videos/meet/meetings/live-captions/enable-captions-light.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="/assets/videos/meet/meetings/live-captions/enable-captions-light.mp4#only-light" loading="lazy" defer muted playsinline autoplay loop async></video></a>
