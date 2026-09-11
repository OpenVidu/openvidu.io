---
title: "Meeting configuration in OpenVidu Meet"
description: "Cap how many participants a meeting admits and how long it lasts, and choose whether participants join with the microphone and camera on."
---

# Meeting configuration

A few settings of a [room](../rooms/overview.md) shape every meeting held in it. They are configured in the **Meeting Features** step of the room wizard when [creating](../rooms/management.md#create-rooms) or [editing](../rooms/management.md#edit-rooms) the room, or through the `config` object of the room via the [REST API](../rooms/management.md#rest-api-reference):

- A [participant limit](#participant-limit).
- A [duration limit](#duration-limit).
- The [initial state of the microphone and the camera](#initial-device-state) of every participant.

![Meeting Features step of the room configuration wizard](../../../assets/images/meet/meetings/configuration/room-wizard-meeting-features-dark.png#only-dark){ .round-corners loading=lazy }
![Meeting Features step of the room configuration wizard](../../../assets/images/meet/meetings/configuration/room-wizard-meeting-features-light.png#only-light){ .round-corners loading=lazy }

!!! info
    The same step toggles the in-meeting features that have their own page: [End-to-End Encryption](e2e-encryption.md), [Live Captions](live-captions.md), chat and [Virtual Backgrounds](virtual-background.md).

## Participant limit { #participant-limit }

The **participant limit** caps how many participants may be in the meeting at the same time, from 1 to 30. Once it is reached, anyone else trying to join is told the meeting is full. Leave it empty for no limit.

Via the REST API it is the `config.maxParticipants` property of the room configuration; `null` lifts the limit. The limit is read when the meeting starts, so changing it does not affect a meeting already in progress.

## Duration limit { #duration-limit }

The **duration limit** ends the meeting automatically after the given number of minutes, from 1 to 1440 (one day), exactly as if a moderator had ended it for everyone. Leave it empty for unlimited meetings.

As the end approaches, participants see the time remaining in the status rail of the [Meeting view](lifecycle.md#meeting-view) and are warned that the meeting is about to end. When the meeting ends, the [End view](lifecycle.md#end-view) tells them the meeting reached its maximum duration.

Via the REST API it is the `config.maxDurationMinutes` property of the room configuration; `null` lifts the limit. The end time is fixed when the meeting starts and can be read with the [Meetings REST API :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/meetingGet){:target="_blank"}. An integration can tell the two kinds of end apart: the [`meetingEnded` webhook :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/webhooks/meetingEndedWebhook){:target="_blank"} carries `reason: max_duration_reached`, and the `meetingLeft` [event](../../embedded/reference/webcomponent.md#events) of an embedded meeting carries `reason: meeting_ended_by_duration_limit`.

## Initial device state { #initial-device-state }

**Microphone on when joining** and **Camera on when joining** decide whether participants join the meeting with the device active. Both are on by default.

This is an initial state, not a restriction: a participant can turn the device on or off at any time during the meeting. To prevent a participant from publishing audio or video, deny the `mediaPublishAudio` or `mediaPublishVideo` [permission](../rooms/access.md#predefined-roles) instead; a denied permission always wins over the initial state.

Via the REST API these are the `config.initialAudioActive` and `config.initialVideoActive` properties of the room configuration. When OpenVidu Meet is [embedded](../../embedded/intro.md), the `initial-audio-active` and `initial-video-active` [attributes](../../embedded/reference/webcomponent.md#attributes) of the Web Component take precedence over the room's setting whenever they are set.

## REST API reference { #rest-api-reference }

All of these settings live in the room configuration, managed with the [OpenVidu Meet REST API](../../embedded/reference/rest-api.md). Their exact ranges and defaults are documented in the [MeetRoomConfig :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/schemas/MeetRoomConfig){:target="_blank"} schema.

| Operation          | HTTP Method | Reference                                                                                                                                             |
| ------------------ | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Get room config    | GET         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRoomConfig){:target="_blank"}    |
| Update room config | PUT         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/updateRoomConfig){:target="_blank"} |
