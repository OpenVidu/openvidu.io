---
title: "Raise hand in OpenVidu Meet"
description: "Participants raise their hand to ask for a turn in an OpenVidu Meet meeting, everyone sees the queue, and moderators lower hands."
page_features:
  - lazyvideo
---

# Raise Hand

Participants **raise their hand** to ask for a turn without interrupting whoever is speaking. Raised hands form a **queue**, ordered by the moment each hand went up, and every participant sees the same queue.

## Raising your hand { #raising-your-hand }

Click the **Raise hand** button in the toolbar, or press the `R` key anywhere outside a text field. Click it or press `R` again to lower your hand. On phones, the button is in the **More options** menu.

Your camera tile is highlighted and shows your place in the queue. When a hand ahead of yours goes down, your place moves up.

<a class="glightbox" href="/assets/videos/meet/meetings/raise-hand/raise-hand-dark.mp4" data-type="video" data-gallery="dark"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/raise-hand/raise-hand-dark.mp4#only-dark" preload="none" muted playsinline loop></video></a>
<a class="glightbox" href="/assets/videos/meet/meetings/raise-hand/raise-hand-light.mp4" data-type="video" data-gallery="light"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/raise-hand/raise-hand-light.mp4#only-light" preload="none" muted playsinline loop></video></a>

## Following the queue { #following-the-queue }

Every participant sees who is waiting and in which order:

- The **camera tile** of each raised hand is highlighted and shows its place in the queue.
- The **status rail** at the top of the meeting counts the raised hands, including those of participants that [Smart Layout](smart-layout.md) keeps off the grid. Clicking it opens the **Participants** panel.
- The **Participants** panel lists the raised hands first, in queue order, with a hand on their avatar.

Participants who can [lower hands](#lowering-hands) also hear a sound and get a notice when a hand goes up. The hands raised while that notice is on screen are gathered into it, as in "David and 2 more raised their hand", so many hands going up at once never pile up notices.

<a class="glightbox" href="/assets/videos/meet/meetings/raise-hand/hand-notice-dark.mp4" data-type="video" data-gallery="dark"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/raise-hand/hand-notice-dark.mp4#only-dark" preload="none" muted playsinline loop></video></a>
<a class="glightbox" href="/assets/videos/meet/meetings/raise-hand/hand-notice-light.mp4" data-type="video" data-gallery="light"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/raise-hand/hand-notice-light.mp4#only-light" preload="none" muted playsinline loop></video></a>

## Lowering other participants' hands { #lowering-hands }

A participant with the `participantHandLower` permission lowers the hands of the others, from the **Participants** panel:

- **Lower hand** in the menu of a participant whose hand is raised. The notice of a single hand offers the same action.
- **Lower all hands** in the **Raised hands** section at the top of the panel.

The participant is told that a moderator lowered their hand.

<a class="glightbox" href="/assets/videos/meet/meetings/raise-hand/lower-hands-dark.mp4" data-type="video" data-gallery="dark"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/raise-hand/lower-hands-dark.mp4#only-dark" preload="none" muted playsinline loop></video></a>
<a class="glightbox" href="/assets/videos/meet/meetings/raise-hand/lower-hands-light.mp4" data-type="video" data-gallery="light"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/raise-hand/lower-hands-light.mp4#only-light" preload="none" muted playsinline loop></video></a>

`participantHandLower` is granted by default to the `Moderator` [predefined role](../rooms/access.md#predefined-roles) of every room created from OpenVidu Meet 3.10.0 on. Rooms and room members that existed before start without it, so it has to be granted explicitly in the room's role permissions or in the member's [custom permissions](../room-members/management.md#edit-a-member).

## Enable or disable raise hand for a room { #enable-or-disable }

Raise hand is enabled by default when a room is [created](../rooms/management.md#create-rooms), whether through the UI or the [REST API :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/createRoom){:target="_blank"}. It can be turned off per room from the **Features** section of the **Meeting** step of the room configuration wizard, using the **Raise hand** toggle, or with the room config `raiseHand.enabled`. In a room with raise hand turned off, the button is not shown and every attempt to raise a hand is rejected.

![Room wizard step with the raise hand toggle](../../../assets/images/meet/meetings/raise-hand/room-wizard-hand-dark.webp#only-dark){ .control-height .round-corners loading=lazy }
![Room wizard step with the raise hand toggle](../../../assets/images/meet/meetings/raise-hand/room-wizard-hand-light.webp#only-light){ .control-height .round-corners loading=lazy }

## From your application { #embedded }

When OpenVidu Meet is [embedded](../../embedded/intro.md), the host application raises and lowers hands with the `participantHandRaise`, `participantHandLower` and `participantHandLowerAll` [commands](../../embedded/reference/webcomponent.md#commands) of the Web Component and the iframe. They act on behalf of the local participant: lowering another participant's hand, or every hand, requires the `participantHandLower` permission. The `participantHandChanged` [event](../../embedded/reference/webcomponent.md#events) tells the host every time a hand goes up or down, with its place in the queue and who lowered it.

## REST API reference { #rest-api-reference }

Hands can also be raised and lowered from your backend with the [Meetings REST API](../../embedded/reference/rest-api.md). A request authenticated with a room member token acts as that participant: anyone can raise or lower their own hand, while lowering someone else's requires `participantHandLower`. A request authenticated with the API key can lower any hand, but raise none, since only its owner raises a hand. The participants of a meeting report whether their hand is raised and since when, and the [`participantHandChanged` webhook :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/webhooks/participantHandChangedWebhook){:target="_blank"} reports every change.

| Operation           | HTTP Method | Reference                                                                                                                                                   |
| ------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Raise or lower hand | PUT         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/participantHandUpdate){:target="_blank"}   |
| Lower all hands     | PUT         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/participantHandLowerAll){:target="_blank"} |
| List participants   | GET         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/participantList){:target="_blank"}         |
