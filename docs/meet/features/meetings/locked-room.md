---
title: "Locked room in OpenVidu Meet"
description: "Make participants ask to join a locked room and wait until a moderator admits or rejects them, from OpenVidu Meet, the REST API or your own application."
---

# Locked Room

In a **locked room**, participants do not enter the meeting directly: they **ask to join** and wait until someone with permission **admits** or **rejects** them. It suits classes, consultations and public meetings, where the host wants to see who is asking before letting anyone in.

## Locking a room { #locking-a-room }

Rooms are unlocked by default. Lock a room from the **Locked room** section of the **Room Access** step of the room configuration wizard. An optional **message**, up to 500 characters, is shown to everyone who waits: use it to say what the meeting is or when it starts.

![Room Access step of the room wizard with the locked room turned on and a message for the participants who wait](../../../assets/images/meet/meetings/locked-room/room-wizard-locked-room-dark.webp#only-dark){ .control-height .round-corners loading=lazy }
![Room Access step of the room wizard with the locked room turned on and a message for the participants who wait](../../../assets/images/meet/meetings/locked-room/room-wizard-locked-room-light.webp#only-light){ .control-height .round-corners loading=lazy }

With the REST API, the lock is the `lock` property of the room's [access settings](../rooms/access.md), sent to [`roomUpdateAccess` :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/roomUpdateAccess){:target="_blank"} or [`roomCreate` :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/roomCreate){:target="_blank"}. A `message` of `null` removes it:

```json
{ "access": { "lock": { "enabled": true, "message": "The class starts at 10:00. We will let you in shortly." } } }
```

- The lock changes only while **no meeting is running**, like every access setting.
- Changing it **invalidates the room member tokens** issued before: whoever held one opens the room again, and waits if it is now locked.
- **Unlocking** the room lets everyone waiting in.

## Who waits { #who-waits }

Two independent [permissions](../rooms/access.md#predefined-roles) decide it:

| Permission                | Name in the interface | What it allows                                     |
| ------------------------- | --------------------- | -------------------------------------------------- |
| `accessBypassLock`        | Join a locked room    | Joining directly, without asking.                  |
| `waitingParticipantAdmin` | Admit participants    | Seeing who waits, and admitting or rejecting them. |

The `Moderator` role has both by default and the `Speaker` role neither, so speakers wait. Admins and the room owner never wait. A participant with `waitingParticipantAdmin` but without `accessBypassLock` waits like anyone else, and admits the others once inside.

The usual join checks (closed room, disabled link, `meetingJoin`) run before anyone waits. The [participant limit](configuration.md#participant-limit) is checked when the participant is let in.

## Waiting to be let in { #participant-view }

In the [Join view](lifecycle.md#join-view), the button of a participant who has to wait reads **Ask to join**. Pressing it starts the wait at once, without the [Device view](lifecycle.md#device-view).

![Join view of a locked room, with the Ask to join button](../../../assets/images/meet/meetings/locked-room/join-ask-dark.webp#only-dark){ .control-height .round-corners loading=lazy }
![Join view of a locked room, with the Ask to join button](../../../assets/images/meet/meetings/locked-room/join-ask-light.webp#only-light){ .control-height .round-corners loading=lazy }

While waiting, the participant sees how long they have waited, the room's message, whether the meeting has started, a **Stop waiting** button and a camera preview to set up their camera, microphone and [virtual background](virtual-background.md). They see nothing of the others who wait. Once admitted, they join **without reloading the page**, with the devices they chose.

![Waiting view showing the time waited, the room message and the camera preview](../../../assets/images/meet/meetings/locked-room/waiting-screen-dark.webp#only-dark){ .control-height .round-corners loading=lazy }
![Waiting view showing the time waited, the room message and the camera preview](../../../assets/images/meet/meetings/locked-room/waiting-screen-light.webp#only-light){ .control-height .round-corners loading=lazy }

When the wait ends without a place, the view says why: they were **rejected**, they **lost their place**, the **meeting ended**, the room was **closed**, they **stopped waiting**, or **too many people are waiting** (100 at most). Most of these offer **Ask to join again**, which starts a new wait: nobody is blocked.

![The "You weren't let in" view of a participant whom a moderator rejected](../../../assets/images/meet/meetings/locked-room/rejected-dark.webp#only-dark){ .control-height .round-corners loading=lazy }
![The "You weren't let in" view of a participant whom a moderator rejected](../../../assets/images/meet/meetings/locked-room/rejected-light.webp#only-light){ .control-height .round-corners loading=lazy }

### Keeping a place { #keeping-a-place }

A wait lasts while the participant's page stays connected:

- A connection lost for **less than about a minute** keeps the place.
- **Closing, reloading or leaving the page** ends the wait at once. A reload asks to join again on its own, as a new wait.
- Asking again from **another tab or device** ends the earlier wait.

A page that never manages to connect shows a connection error instead: see the [troubleshooting note](../../deployment/basic.md#troubleshooting).

## Admitting and rejecting { #admitting-and-rejecting }

Participants with `waitingParticipantAdmin` see who waits, live. Nobody else in the meeting does.

![Participants panel of a moderator with the Waiting to join section, each participant with their avatar, the free places and the status rail chip](../../../assets/images/meet/meetings/locked-room/admit-panel-dark.webp#only-dark){ .control-height .round-corners loading=lazy }
![Participants panel of a moderator with the Waiting to join section, each participant with their avatar, the free places and the status rail chip](../../../assets/images/meet/meetings/locked-room/admit-panel-light.webp#only-light){ .control-height .round-corners loading=lazy }

- The **Waiting to join** section of the **Participants** panel lists them, each with **Deny** and **Admit**, and the free places when the room has a participant limit. A **Shared link** label marks those who asked with a shared room link, where anyone can type any name.
- From two waiting, **Deny all** and **Admit all** act on everyone. **Admit all** admits all of them or nobody, so it is disabled while more wait than places are free.
- A chip in the **status rail** counts who waits, and a **notification** announces each new request while the panel is closed.

![Notification below the status rail announcing a participant who asks to join, with their avatar, Deny and Admit](../../../assets/images/meet/meetings/locked-room/knock-notice-dark.webp#only-dark){ .round-corners loading=lazy }
![Notification below the status rail announcing a participant who asks to join, with their avatar, Deny and Admit](../../../assets/images/meet/meetings/locked-room/knock-notice-light.webp#only-light){ .round-corners loading=lazy }

Participants can wait before any meeting runs; the first one admitted starts it when they join. A meeting that empties keeps its waiting participants for the next one. Only **ending the meeting** for everyone ends their waits.

### Capacity { #capacity }

- The free places are the participant limit minus the participants in the meeting and those admitted who have not joined yet. An admission not used within a minute is lost, and frees its place.
- Two moderators admitting at once never both take the last place.
- An admitted participant who finds the meeting full when joining goes back to waiting.
- Unlocking a room where more wait than fit lets in whoever connects first; the others see "Meeting full".

## Acting on a locked room { #who-acts }

In a locked room, a **room member token** acts on the meeting (reads it, moderates it, controls recordings and broadcasts, admits) only if its holder was let in. A token obtained without joining keeps only the recording permissions and `roomShareAccessLinks`, so a waiting participant cannot admit anyone, themselves included. A backend acting on its own uses the [API key](../../embedded/reference/rest-api.md#generate-an-api-key), which keeps full access.

!!! warning "`externalId` and `metadata` prove nothing"

    They are whatever the participant's client sent. To admit automatically, trust the `type` (`user`, `identified_guest` or `anonymous`) and the `participantIdentity` of a member or user, which the server derives from their account or personal link.

!!! warning "A leaked link can keep the waiting list full"

    Anyone with a shared link can open up to 100 waits. The remedy is to **end the meeting** and disable the leaked [access link](../rooms/access.md).

## From your application { #embedded }

When OpenVidu Meet is [embedded](../../embedded/intro.md), the host application uses the [commands](../../embedded/reference/webcomponent.md#commands) and [events](../../embedded/reference/webcomponent.md#events) of the Web Component and the iframe:

- **For those who admit** (holding `waitingParticipantAdmin`, in the meeting): the `waitingParticipantAdmit`, `waitingParticipantAdmitAll`, `waitingParticipantReject` and `waitingParticipantRejectAll` commands, and the `waitingParticipantKnocked` (a new request), `waitingParticipantListUpdated` (the whole list) and `waitingParticipantStatusChanged` (how each wait changed, whoever changed it) events.
- **For the participant who waits**: `waitingParticipantStatusChanged` reports their own wait, and `meetingJoined` confirms the admission. `meetingLeave` stops the wait.

A host page with a Content Security Policy must allow the WebSocket connection to OpenVidu Meet: see [Content Security Policy](../../embedded/reference/webcomponent.md#content-security-policy).

## REST API and webhooks { #rest-api-reference }

A backend runs a locked room with the [Meetings REST API](../../embedded/reference/rest-api.md), under `/api/v1/meetings/{roomId}/waiting-participants`. These operations require `waitingParticipantAdmin` and work whether or not a meeting is running.

| Operation                          | HTTP Method | Reference                                                                                                                                                         |
| ---------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| List the waiting participants      | GET         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/waitingParticipantList){:target="_blank"}         |
| Get a waiting participant          | GET         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/waitingParticipantGet){:target="_blank"}          |
| Admit a waiting participant        | POST        | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/waitingParticipantAdmit){:target="_blank"}        |
| Admit all the waiting participants | POST        | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/waitingParticipantAdmitAll){:target="_blank"}     |
| Reject a waiting participant       | DELETE      | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/waitingParticipantReject){:target="_blank"}       |
| Bulk reject waiting participants   | DELETE      | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/waitingParticipantBulkReject){:target="_blank"} |

### Webhooks { #webhooks }

- [`waitingParticipantKnocked` :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/webhooks/waitingParticipantKnockedWebhook){:target="_blank"}: a participant asked to join.
- [`waitingParticipantStatusChanged` :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/webhooks/waitingParticipantStatusChangedWebhook){:target="_blank"}: a wait changed, one per participant. Its `status` is `admitted`, `rejected`, `left`, `expired`, `meeting_ended`, `room_closed`, or `waiting` for an admitted participant who found the meeting full. `origin` tells who caused it, and `reason` adds why when needed.

```json
{
  "creationDate": 1620000012000,
  "event": "waitingParticipantStatusChanged",
  "data": {
    "roomId": "room-123",
    "roomName": "room",
    "participant": {
      "participantIdentity": "ana-a1b2c3",
      "participantName": "Ana",
      "type": "anonymous",
      "knockDate": 1620000000000
    },
    "status": "admitted",
    "origin": "moderator"
  }
}
```

`admitted` is not the join: the `participantJoined` webhook confirms it. The time waited is `creationDate` minus `knockDate`.
