---
title: Meetings in OpenVidu Meet
description: Learn what a meeting is in OpenVidu Meet and how to join one.
tags:
    - setupcustomgallery
---

# Meetings

A **Meeting** is a temporary session within a [room](../rooms/overview.md) where participants join in real-time to communicate, share content, and collaborate. It starts when the first participant connects and ends when the last one leaves — or when a moderator explicitly closes it. Unlike rooms (which are persistent), a meeting only exists while at least one participant is connected, and the same room can host many meetings over time, one at a time.

!!! info

    Meetings are a **runtime** concept: they are not created, edited or deleted like other resources, and there is no dedicated REST API for them — a meeting simply begins when someone joins a room and ends when everyone leaves. To control meetings, manage their [room](../rooms/overview.md) (its [access](../rooms/access.md), features and [recording](../recordings/overview.md)).

## How to join a meeting

A meeting starts as soon as a participant opens a valid **room access link** and presses the join button into an empty room. You can learn everything about how access to a room is granted in [Room Access](../rooms/access.md).

Users with access to OpenVidu Meet can join a meeting directly from the "Rooms" page:

<a class="glightbox" href="../../../../assets/videos/meet/join-meeting.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery7"><video class="round-corners" src="../../../../assets/videos/meet/join-meeting.mp4" loading="lazy" defer muted playsinline autoplay loop async></video></a>

Users can also copy a room access link and share it with guests:

<a class="glightbox" href="../../../../assets/videos/meet/share-room-link.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery8"><video class="round-corners" src="../../../../assets/videos/meet/share-room-link.mp4" loading="lazy" defer muted playsinline autoplay loop async></video></a>

## In this section

- [Meeting lifecycle](lifecycle.md) — the series of views a participant moves through, from opening a room access link until the meeting ends: Lobby, Device, Meeting, Recording and End.
- [Live Captions](live-captions.md) — real-time speech-to-text transcription powered by the OpenVidu Speech Processing Agent.
- [Smart Layout](smart-layout.md) — dynamic layout that adapts automatically to the number of active participants.
- [Role Management](role-management.md) — promote participants to Moderator during a meeting to give them special permissions, or demote them back to their original permissions.
- [E2E Encryption](e2e-encryption.md) — end-to-end encrypted audio, video and chat so only participants can decrypt the content.
- [Virtual Background](virtual-background.md) — blur or replace the camera background before or during a meeting.
