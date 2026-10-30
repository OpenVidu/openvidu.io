---
title: "Meeting moderation in OpenVidu Meet"
description: "Mute a participant's microphone, camera or screen share, or everyone's at once, and remove participants from an OpenVidu Meet meeting."
---

# Meeting moderation

The **Participants** panel of the [Meeting view](lifecycle.md#meeting-view) lists everyone in the meeting, with the current state of their **microphone**, **camera** and **screen share**. Participants with the right [permissions](../rooms/access.md#predefined-roles) act on the others from there:

- **Mute** another participant's microphone, turn off their camera or stop their screen share, one device at a time (`participantMute` permission).
- **Turn off for everyone**: mute every microphone, turn off every camera or stop every screen share at once (`participantMute` permission).
- **Lower** a participant's raised hand, or every raised hand at once (`participantHandLower` permission). See [Raise Hand](raise-hand.md#lowering-hands).
- **Remove** a participant from the meeting (`participantKick` permission).
- **Promote** a participant to moderator, or demote them back (`participantPromote` permission). See [Role Management](role-management.md).

![Participants panel with the media state and moderation controls of every participant](../../../assets/images/meet/meetings/moderation/participants-panel-dark.png#only-dark){ .round-corners loading=lazy }
![Participants panel with the media state and moderation controls of every participant](../../../assets/images/meet/meetings/moderation/participants-panel-light.png#only-light){ .round-corners loading=lazy }

## Muting participants { #muting-participants }

Muting only ever turns a device **off**: a moderator can never turn on somebody else's microphone or camera. The affected participant is told that a moderator turned off one of their devices, and may turn it back on at any time. Moderators cannot be muted, and turning off a device for everyone leaves the moderators alone.

`participantMute` is granted by default to the `Moderator` [predefined role](../rooms/access.md#predefined-roles) of every room created. Rooms and room members that existed before start without it, so it has to be granted explicitly in the room's role permissions or in the member's [custom permissions](../room-members/management.md#edit-a-member).

## Removing participants { #removing-participants }

A participant with the `participantKick` permission can **remove** other participants from the meeting. The Participants panel offers **Remove from meeting** for every participant who is not a moderator in their own right, and for every participant promoted to moderator during the meeting, but never for original moderators, the room owner or administrators. The [REST API](#rest-api-reference) and the `participantKick` [command](#embedded) can remove any participant. The removed participant is taken to the [End view](lifecycle.md#end-view), which tells them they were removed, and both the [`participantLeft` webhook](../../embedded/reference/webhooks.md) and the `participantLeft` [embedded event](../../embedded/reference/webcomponent.md#events) report `participant_kicked` as the reason.

Removing a participant does not take away their access to the room: with the same link, room member record or user account they can join the meeting again at once. To keep someone out, revoke that access: delete their [room member](../room-members/management.md) record, or disable the [access link](../rooms/access.md) they entered with. Access links can only be changed while no meeting is running, so a participant who entered through an anonymous link can join again until the meeting ends.

## From your application { #embedded }

When OpenVidu Meet is [embedded](../../embedded/intro.md), the same actions are available to the host application as the `participantMute`, `participantMuteAll`, `participantKick` and `meetingEnd` [commands](../../embedded/reference/webcomponent.md#commands) of the Web Component and the iframe. They act on behalf of the local participant, so they require that participant to hold the corresponding permission.

## REST API reference { #rest-api-reference }

Live meetings can be read and moderated from your backend with the [Meetings REST API](../../embedded/reference/rest-api.md). Reading a meeting or its participants requires the `meetingRead` permission, and each moderation action the permission named above; a request authenticated with the API key is not subject to them.

| Operation                   | HTTP Method | Reference                                                                                                                                                    |
| --------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Get a live meeting          | GET         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/meetingGet){:target="_blank"}             |
| End a meeting               | DELETE      | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/meetingEnd){:target="_blank"}             |
| List participants           | GET         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/participantList){:target="_blank"}        |
| Get a participant           | GET         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/participantGet){:target="_blank"}         |
| Kick a participant          | DELETE      | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/participantKick){:target="_blank"}        |
| Mute a participant          | PUT         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/participantMute){:target="_blank"}        |
| Mute all participants       | PUT         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/participantMuteAll){:target="_blank"}     |
| Update a participant's role | PUT         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/participantRoleUpdate){:target="_blank"}  |
