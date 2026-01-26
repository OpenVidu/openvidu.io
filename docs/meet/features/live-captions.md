---
title: How to Enable Live Captions in OpenVidu Meet | Real-time Transcription Guide
description: Learn how to enable and use live captions in OpenVidu Meet to improve meeting accessibility with real-time speech-to-text transcriptions.
keywords: OpenVidu Meet, live captions, speech to text, real-time transcription, video conferencing accessibility, speech processing agent
---

# Live Captions in OpenVidu Meet

OpenVidu Meet includes a built-in **Live Captions** feature that turns speech into text in real-time. This is a powerful tool for making your meetings more accessible to hearing-impaired users, helping participants in noisy environments, and assisting non-native speakers.

By following this guide, you will learn how to set up the **Speech Processing Agent** and activate captions for your video calls.

---

## How to Enable Live Captions

### Step 1: Deploy OpenVidu with Caption Support

Live captions require a specific deployment configuration. You must deploy OpenVidu with the specialized [Speech Processing Agent](../../docs/ai/openvidu-agents/speech-processing-agent.md) configuration.

### 1. Deploy with Speech Support

To use captions, you must deploy OpenVidu with the specialized [Speech Processing Agent](../../docs/ai/openvidu-agents/speech-processing-agent.md) configuration.
!!!warning
	OpenVidu Meet requires that the Speech Processing Agent is deployed in `manual` mode.

### 2. Activate the Meet Caption Variable

After the Speech Processing Agent is configured, you need to turn the feature "On" in the OpenVidu Meet settings.

- **Action:** Set the following environment variable in your configuration:
  `MEET_CAPTIONS_ENABLED=true`

### 3. Restart OpenVidu Meet

Apply your changes by restarting the OpenVidu Meet service. This ensures the system recognizes the new live captioning capabilities.

### 4. Enable Captions for Specific Rooms

You have total control over which meetings use captions. You can enable them in two ways:

- **Via the Interface:** When creating a room in the **OpenVidu Meet UI**, simply toggle the "Captions" switch to **ON**.

[Photo of the Room Creation Interface with Captions Toggle]

- **Via the API:** If you are an advanced user, set the `captions` property to `true` when using the [OpenVidu REST API](../embedded/reference/api.html#/operations/createRoom).

---

## 🎙️ Using Live Captions in a Meeting

Once the meeting starts, the experience is seamless:

- **Automatic Transcription:** Captions appear instantly at the bottom of the screen as participants speak.
- **User Friendly:** No extra clicks are needed from the participants—the text appears automatically if the room was configured for captions.
- **Clear Visibility:** The interface is designed to be easy to read without blocking the video feed.

[Screenshot of Live Captions in Action]


