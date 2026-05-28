---
title: Meetings in OpenVidu Meet
description: Learn what a meeting is in OpenVidu Meet and how to join one.
tags:
  - setupcustomgallery
---

# Meetings

A **Meeting** is a temporary session within a [room](../rooms/overview.md) where participants join in real-time to communicate, share content, and collaborate. It starts when the first participant connects and ends when the last one leaves — or when a moderator explicitly closes it.

## What is a Meeting

Every meeting takes place inside a room. Unlike rooms (which are persistent), a meeting only exists while at least one participant is connected. The same room can host many meetings over time, one at a time.

## How to join a meeting

A meeting starts as soon as a participant opens a valid **room link** into an empty room. You can learn everything about room links [here](../rooms/access.md#room-links).

Users with access to OpenVidu Meet can join a meeting directly from the "Rooms" page:

<a class="glightbox" href="../../../../assets/videos/meet/join-meeting.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery7"><video class="round-corners" src="../../../../assets/videos/meet/join-meeting.mp4" loading="lazy" defer muted playsinline autoplay loop async></video></a>

!!! info
    Doing this simply opens a new tab with a `Moderator` room link.

Users can also copy a room link and share it with external participants:

<a class="glightbox" href="../../../../assets/videos/meet/share-room-link.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery8"><video class="round-corners" src="../../../../assets/videos/meet/share-room-link.mp4" loading="lazy" defer muted playsinline autoplay loop async></video></a>

## Meeting lifecycle

From the moment a participant opens a room link until the meeting ends, they move through a series of views. See [Meeting lifecycle](lifecycle.md) for a full description of the Join, Device, Meeting, Recording and End views.

## Meeting features

OpenVidu Meet provides a set of built-in features that enhance accessibility and collaboration during a live session:

- [Live Captions](live-captions.md) — real-time speech-to-text transcription powered by the OpenVidu Speech Processing Agent.
- [Smart Layout](smart-layout.md) — dynamic layout that adapts automatically to the number of active participants.
- [Role Management](role-management.md) — Moderator and Speaker roles with per-room assignment via room links, and runtime role changes.
- [E2E Encryption](e2e-encryption.md) — end-to-end encrypted audio, video and chat so only participants can decrypt the content.
- [Virtual Background](virtual-background.md) — blur or replace the camera background before or during a meeting.
