---
title: "Waiting room in OpenVidu Meet"
description: "Hold participants in a waiting room until a moderator admits or rejects them, from the OpenVidu Meet interface, the REST API or your own application."
---

# Waiting Room

In a room with the **waiting room** on, a participant who asks to join does not enter the meeting. They wait, and someone with the right permission **admits** or **denies** them. It suits classes, consultations and public meetings, where the host wants to see who is asking before letting anyone in.

## Turning it on { #turning-it-on }

The waiting room is off by default. Turn it on per room from the **Waiting room** section of the **Room Access** step of the room configuration wizard, or with the room config `waitingRoom.enabled`. In the same section, an optional **message** of up to 500 characters is shown to everyone while they wait. Use it to say what the meeting is or when it starts.

![Room Access step of the room wizard with the waiting room turned on and a message for the participants who wait](../../../assets/images/meet/meetings/waiting-room/room-wizard-waiting-room-dark.webp#only-dark){ .control-height .round-corners loading=lazy }
![Room Access step of the room wizard with the waiting room turned on and a message for the participants who wait](../../../assets/images/meet/meetings/waiting-room/room-wizard-waiting-room-light.webp#only-light){ .control-height .round-corners loading=lazy }

Via the REST API, `waitingRoom` takes `enabled` and an optional `message`. Sending `message` as `null` removes it:

```json
{ "config": { "waitingRoom": { "enabled": true, "message": "The class starts at 10:00. We will let you in shortly." } } }
```

- Like the rest of the room config, the waiting room can only be changed while **no meeting is running**. A meeting has no switch to turn it off.
- Turning it on **invalidates the room member tokens** issued before. Whoever held one opens the room again and waits like everyone else.
- Turning it off lets everyone waiting in. See [Capacity](#capacity) for what happens when more people wait than the meeting can take.
- With the waiting room off, nothing changes: everyone joins directly.

## Who waits and who does not { #who-waits }

Two [permissions](../rooms/access.md#predefined-roles) decide it. They are independent of each other:

| Permission          | Name in the interface | What it allows                                                                 |
| ------------------- | --------------------- | ------------------------------------------------------------------------------ |
| `waitingRoomBypass` | Join without waiting  | Joining the meeting directly, without asking.                                  |
| `waitingRoomAdmin`  | Admit participants    | Seeing who waits, and admitting or rejecting them, from the meeting or an API. |

Both are granted by default to the `Moderator` [predefined role](../rooms/access.md#predefined-roles) of every room, including the rooms created before this feature existed, and to the room members with that role. The `Speaker` role has neither, so speakers wait. Both can be revoked or granted to other participants in the room's role permissions or in the member's [custom permissions](../room-members/management.md#edit-a-member). The wizard groups them under **Waiting room**.

- A participant with `waitingRoomAdmin` but without `waitingRoomBypass` waits like anyone else. Once they are let in, they admit the others.
- **Admins** and the **room owner** have every permission, so they never wait.
- A participant who gains `waitingRoomBypass` while waiting keeps waiting until someone admits them.
- The usual checks of a join run before anyone waits: a closed room, a disabled link or a missing `meetingJoin` permission never reach the waiting room. Only the [participant limit](configuration.md#participant-limit) is checked later, when the participant is let in.

## What the participant sees { #participant-view }

### Asking to join { #asking-to-join }

In the [Join view](lifecycle.md#join-view), the button of a participant who would wait reads **Ask to join**. Pressing it puts them in line at once, and they skip the [Device view](lifecycle.md#device-view): the waiting view is where they prepare their camera and microphone. A participant who joins without waiting sees **Join Meeting** and the Device view as usual.

![Join view of a room with a waiting room, with the Ask to join button](../../../assets/images/meet/meetings/waiting-room/join-ask-dark.webp#only-dark){ .control-height .round-corners loading=lazy }
![Join view of a room with a waiting room, with the Ask to join button](../../../assets/images/meet/meetings/waiting-room/join-ask-light.webp#only-light){ .control-height .round-corners loading=lazy }

If the waiting room is turned on while someone is in the Device view, pressing join takes them to the waiting view with the devices they chose.

### The waiting view { #waiting-view }

While they wait, participants see:

- Their **position in line**, such as "You're 2nd in line".
- How long they have waited, in whole minutes from the first minute on.
- The room's **message**, if there is one.
- A **camera preview** with the device controls, to set up the camera, the microphone and the [virtual background](virtual-background.md) while they wait.
- "The meeting hasn't started yet", while no meeting is running in the room.
- A **Leave waiting room** button.

![Waiting view showing the position in line, the time waited, the room message and the camera preview](../../../assets/images/meet/meetings/waiting-room/waiting-screen-dark.webp#only-dark){ .control-height .round-corners loading=lazy }
![Waiting view showing the position in line, the time waited, the room message and the camera preview](../../../assets/images/meet/meetings/waiting-room/waiting-screen-light.webp#only-light){ .control-height .round-corners loading=lazy }

All of it updates live. The position and whether the meeting has started can lag by up to about 20 seconds. Screen readers announce position changes politely, at most once every 10 seconds, and announce the admission or the end of the wait at once.

When a moderator admits them, the participant joins the meeting **without reloading the page**, with the name and the devices they had in the waiting view. A participant admitted while their page is in a background tab joins with the microphone off.

### When the wait ends without a place { #outcomes }

The view says why the wait ended:

| What happened                                    | What the participant sees                                                              |
| ------------------------------------------------ | -------------------------------------------------------------------------------------- |
| A moderator denied them                          | "You weren't let in", with **Ask to join again**, disabled for the next 15 seconds.     |
| They lost their place                            | "You lost your place", with **Ask to join again**. See [Keeping a place](#keeping-a-place). |
| They asked again from another tab or device      | The earlier page says "You lost your place": the new request is the one that waits.     |
| The meeting was ended for everyone               | A message that the meeting has ended.                                                  |
| The room was closed or deleted                   | The same error view as a closed room without the waiting room.                          |
| They pressed **Leave waiting room**              | A message that they left.                                                              |
| 100 participants were already waiting            | "The waiting room is full", with **Ask to join again**. See [Capacity](#capacity).       |

![The "You weren't let in" view of a participant whom a moderator denied](../../../assets/images/meet/meetings/waiting-room/rejected-dark.webp#only-dark){ .control-height .round-corners loading=lazy }
![The "You weren't let in" view of a participant whom a moderator denied](../../../assets/images/meet/meetings/waiting-room/rejected-light.webp#only-light){ .control-height .round-corners loading=lazy }

In an [embedded](../../embedded/intro.md) meeting, these views offer the same dismiss button as the [End view](lifecycle.md#end-view): pressing it emits `embeddedCloseRequested` to the host application.

**Ask to join again** starts a new wait at the end of the line. Every request to join is a new wait: a participant who asks again, from another tab or another device, goes to the end of the line, and their earlier wait ends. A reload while waiting is not a request to join again: see [Keeping a place](#keeping-a-place). Nobody is blocked: a denied participant can ask again as many times as they like.

### Keeping a place { #keeping-a-place }

A place in line belongs to the participant's **live connection** to OpenVidu Meet, and it is kept only while the page stays connected.

- A short loss of connection is fine. The participant keeps their place if the connection is back within about a minute.
- About a **minute without connection** loses the place, whatever the cause: the network, a closed tab, a phone that suspends the page, or a host application that removes the embedded element or iframe.
- A **reload** continues the same wait: the participant returns to the waiting screen with the same place and identity, without asking again. The page remembers the wait of its tab, so another tab asks to join again. A participant who was admitted and reloads the page after joining also asks again at the end of the line.
- **Leave waiting room** ends the wait at once, even while the connection is down.

A page that never manages to connect shows the connection error screen instead of "You lost your place". That points to a network that blocks WebSockets: see the [troubleshooting note](../../deployment/basic.md#troubleshooting).

## Admitting and rejecting { #admitting-and-rejecting }

Participants with `waitingRoomAdmin` see who waits, live, from the moment each one presses **Ask to join**. Everyone else in the meeting sees nothing of it.

![Participants panel of a moderator with the Waiting to join section, the free places and the status rail chip](../../../assets/images/meet/meetings/waiting-room/admit-panel-dark.webp#only-dark){ .control-height .round-corners loading=lazy }
![Participants panel of a moderator with the Waiting to join section, the free places and the status rail chip](../../../assets/images/meet/meetings/waiting-room/admit-panel-light.webp#only-light){ .control-height .round-corners loading=lazy }

- A **Waiting to join** section at the top of the **Participants** panel lists the participants in arrival order, each with **Admit** and **Deny**. Under a [participant limit](configuration.md#participant-limit), it also shows the free places, such as "2 places left".
- A **Shared link** label marks the participants who asked with a shared link of the room: anyone with the link can type any name, so the label tells them apart from an account or a personal link. When two rows share a name, each shows the time it asked to join.
- From two waiting, **Deny all** rejects everyone waiting, after a confirmation, and **Admit N** admits the first N in line that fit in the free places.
- The **status rail** at the top of the meeting shows a chip with the number waiting, such as "3 waiting to join".
- While the panel is closed, a **notification** below the rail names each participant who starts waiting, with **Deny** and **Admit**. Several are gathered into one with the number waiting and a **View** button, and joining a meeting where people already wait shows one gathered notification. Opening the panel dismisses it. It never takes the keyboard focus.

![Notification below the status rail announcing a participant who asks to join, with Deny and Admit](../../../assets/images/meet/meetings/waiting-room/knock-notice-dark.webp#only-dark){ .round-corners loading=lazy }
![Notification below the status rail announcing a participant who asks to join, with Deny and Admit](../../../assets/images/meet/meetings/waiting-room/knock-notice-light.webp#only-light){ .round-corners loading=lazy }

A participant who is **admitted** joins the meeting. One who is **denied** is told they weren't let in. Denying everyone rejects whoever waits when the request arrives, and whoever asks afterwards waits as usual. There is no block list, and no way to send a participant back to the line.

The room stays `open` while participants wait: asking to join does not start the meeting, reserve a name or take a place in it. The first participant admitted into a room with no meeting running starts it when they join. Participants can wait before any meeting runs: a moderator who joins sees them, and a backend can also admit them [with the API key](#who-acts). A meeting that empties, because its last participants left or lost their connection, does not end the waits: those waiting keep their place for the next meeting. Only ending the meeting for everyone, or reaching its duration limit, ends them.

## Capacity { #capacity }

The waiting room works with the room's [participant limit](configuration.md#participant-limit):

- A meeting at its limit still lets participants wait.
- The **free places** are the participant limit minus the participants in the meeting minus the participants admitted who have not joined yet.
- **Admitted participants count as taken places until they join**, a minute at most. An admission that is not used within a minute is lost: the waiter sees "You lost your place" and asks again, and the place is free again for the next admission.
- Two moderators admitting at the same time cannot both take the last place. One succeeds, and the other is told there is no room.
- Admitting named participants who outnumber the free places admits nobody. **Admitting everyone waiting** admits the first in line, up to the free places, and the rest keep their place.
- A participant who is admitted but finds the meeting full when they ask for their join, because someone with `waitingRoomBypass` took the place meanwhile, goes back to their place in line.
- **Turning the waiting room off** while more participants wait than the meeting can take lets in whoever connects first, not the first in line. The others see "Meeting full".
- A participant is **listed as soon as they ask**, before their waiting view connects. One who never opens it, such as a script or a tab closed at once, shows for 15 to 20 seconds and then disappears.
- The waiting list holds up to **100 participants**. One more asking to join sees "The waiting room is full".

## Acting on a meeting behind a waiting room { #who-acts }

In a room with the waiting room on, a **room member token** acts on the meeting only if its holder was let in, which means the token carries a participant identity, as the token of an admitted participant or of a holder of `waitingRoomBypass` does. Acting on the meeting covers reading it and its participants, ending it, moderating it, controlling recordings and broadcasts, and admitting or rejecting.

A token obtained without joining keeps only the recording permissions (`recordingList`, `recordingPlay`, `recordingDownload`, `recordingDelete`) and `roomShareAccessLinks`. So a participant who waits cannot read the meeting, list its participants or admit anyone, themselves included, whatever their permissions.

A **host application acting for itself**, such as a dashboard or an admission backend, uses the [API key](../../embedded/reference/rest-api.md#generate-an-api-key), which keeps its full access.

## Security notes { #security }

!!! warning "`externalId` and `metadata` prove nothing"

    The `externalId` and `metadata` of a waiting participant are what their own client sent. Anyone with a shared link can send any value, so they are never a proof of identity. A backend that admits on its own identifies waiters by `type` and by the `participantIdentity` of a member or user, which the server derives from their personal link or account.

    | `type`             | How the participant asked to join      |
    | ------------------ | -------------------------------------- |
    | `user`             | With their own OpenVidu Meet account.  |
    | `identified_guest` | With their personal member link.       |
    | `anonymous`        | With a shared link of the room.        |

!!! warning "A leaked link can keep the waiting room full"

    Whoever holds a shared link of the room can open up to 100 waits and keep each one alive, so real participants see "The waiting room is full". **Deny all** only clears the line until they ask again. During a meeting, the waiting room cannot be turned off and an access link cannot be changed. The remedy is to **end the meeting** and then disable the leaked [access link](../rooms/access.md).

## From your application { #embedded }

When OpenVidu Meet is [embedded](../../embedded/intro.md), the host application drives the waiting room with the [commands](../../embedded/reference/webcomponent.md#commands) and [events](../../embedded/reference/webcomponent.md#events) of the Web Component and the iframe.

**For the participants who admit.** They act on behalf of the local participant, who must hold `waitingRoomAdmin` and be in the meeting:

- `participantWaitingAdmit` and `participantWaitingReject` take an optional `participantIdentities` list. With identities, they act on exactly those participants, all or none. Without it, they act on everyone waiting: `participantWaitingAdmit` admits the first in line up to the free places, and `participantWaitingReject` rejects everyone waiting when the command runs. An empty list is refused.
- `participantKnocked` fires once for each participant who starts waiting while the local participant is in the meeting. The participants already waiting when the element joined, and a participant back in line after an admission that failed, arrive in `waitingRoomUpdated` instead.
- `waitingRoomUpdated` carries the whole list, `participants` and `availablePlaces`, once after joining and again every time it changes.

**For the participant who waits.** The host of a waiting participant receives `participantWaitingChanged` with the `participant`, the same object the webhooks carry, the `status` and, while waiting, the `queuePosition`, starting at 1. The `waiting` status repeats every time the position changes. The other statuses are the ones in the [webhook table](#webhooks), each with the `origin` of the change when the meeting knows it.

- `meetingJoined`, not `admitted`, is what confirms the join. A join that finds the meeting full after `admitted` raises no waiting room event.
- A waiting participant never produces `meetingLeft`: their host learns how the wait ended from `participantWaitingChanged`.
- While waiting, `mediaToggleAudio` and `mediaToggleVideo` act on the preview, and `meetingLeave` leaves the waiting room and reports `left`.
- Removing the element or the iframe while the participant waits is not a leave: the place is lost after about a minute and reported as `expired`.
- With an iframe, the host waits for `participantWaitingChanged` with `left` after posting `meetingLeave` before removing the iframe: the command is handled in a later task of the page, so an iframe removed right away never delivers it and the wait ends a minute later as `expired`.

A host page with a Content Security Policy must also allow the WebSocket connection to OpenVidu Meet: see [Content Security Policy](../../embedded/reference/webcomponent.md#content-security-policy).

## REST API and webhooks { #rest-api-reference }

The waiting room can also be run from your backend with the [Meetings REST API](../../embedded/reference/rest-api.md). Unlike the other meeting operations, these three answer whether or not a meeting is running, since participants wait before the first one starts it. They require `waitingRoomAdmin`, and a request authenticated with the API key is not subject to it. A room member token needs its holder to have been let in, as [explained above](#who-acts).

| Operation                          | HTTP Method | Reference                                                                                                                                                  |
| ---------------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| List the participants waiting      | GET         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/participantWaitingList){:target="_blank"}             |
| Admit waiting participants         | POST        | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/participantWaitingAdmit){:target="_blank"}            |
| Reject waiting participants        | POST        | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/participantWaitingReject){:target="_blank"}           |

- `participantWaitingList` answers `participants`, those waiting in arrival order, each with its `participantIdentity`, `participantName`, `type`, `knockDate` and, when the client sent them, `externalId` and `metadata`. It also answers `availablePlaces`, the free places, or `null` when the room has no participant limit.
- `participantWaitingAdmit` and `participantWaitingReject` take `participantIdentities`, from 1 to 100 distinct identities, or no `participantIdentities` for everyone waiting. An empty or repeated list is a `422`, never read as everyone. A decision on named participants applies to all of them or to none: it answers `404`, naming the first identity that no longer waits, and `participantWaitingAdmit` also answers `409` when they outnumber the free places. Both answer the participants decided on.
- With the waiting room off, `participantWaitingList` answers an empty list, a decision on named participants answers `404`, and a decision on everyone waiting answers an empty list of participants.

### Webhooks { #webhooks }

Two [webhooks](../../embedded/reference/webhooks.md) report the waiting room:

- The [`participantKnocked` webhook :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/webhooks/participantKnockedWebhook){:target="_blank"} is sent once for each wait, when the participant asks to join and before their waiting view connects. A participant who never connects therefore produces a `participantKnocked` and, about 20 seconds later, an `expired` status.
- The [`participantWaitingChanged` webhook :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/webhooks/participantWaitingChangedWebhook){:target="_blank"} is sent for each later change of the wait, one per participant, also when a decision covers everyone waiting. It carries the participant, a `status` and the `origin` of the change.

| `status`        | What happened                                                                             |
| --------------- | ----------------------------------------------------------------------------------------- |
| `waiting`       | An admitted participant went back to their place because the meeting was full.            |
| `admitted`      | A moderator admitted the participant, or the waiting room was turned off.                 |
| `rejected`      | A moderator rejected the participant.                                                     |
| `left`          | The participant left the waiting room, or asked again, which starts a new wait.           |
| `expired`       | The participant lost their place, or an admission was not used within a minute.           |
| `meeting_ended` | The meeting was ended for everyone, or reached its duration limit, while they waited.     |
| `room_closed`   | The room was closed or deleted while they waited.                                         |

`admitted` is not the join: the `participantJoined` webhook, with the same `participantIdentity`, confirms it. The `origin` is `participant`, `moderator` or `system`.

```json
{
  "creationDate": 1620000012000,
  "event": "participantWaitingChanged",
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

The time a participant waited is the `creationDate` of the event minus the `knockDate` of the participant. Webhooks are **not stored**: one is lost if the OpenVidu Meet replica sending it stops, may be repeated by the retries and arrives in no guaranteed order. The `knockDate` of the participant and the `creationDate` of the event order them.
