---
title: "Reactions in OpenVidu Meet"
description: "Participants react with an emoji in an OpenVidu Meet meeting, shown for a few seconds on their camera tile, in the participants panel and in the status rail."
page_features:
  - lazyvideo
---

# Reactions

Participants **react** with an emoji to show how they feel without speaking or writing in the chat: a thumbs up to agree, a confused face when something is not clear, applause at the end of a talk. A reaction shows for **10 seconds** and then fades away, so whoever leads the meeting reads the room at a glance.

## Sending a reaction { #sending-a-reaction }

Hover over the **Reactions** button in the toolbar, right after [**Raise hand**](raise-hand.md), and pick one of the eight reactions: 👍 👎 😀 🙁 😕 😮 👏 ❤️. From the keyboard, press `E` anywhere outside a text field to open the picker, and then a number from `1` to `8` to send the reaction in that place. On phones, the reactions are in the **More options** menu.

Your reaction shows on your own camera tile, and the button wears it with a ring that empties as its time runs out. A new reaction replaces the previous one and starts its time over.

<a class="glightbox" href="/assets/videos/meet/meetings/reactions/send-reaction-dark.mp4" data-type="video" data-gallery="dark"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/reactions/send-reaction-dark.mp4#only-dark" preload="none" muted playsinline loop></video></a>
<a class="glightbox" href="/assets/videos/meet/meetings/reactions/send-reaction-light.mp4" data-type="video" data-gallery="light"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/reactions/send-reaction-light.mp4#only-light" preload="none" muted playsinline loop></video></a>

## Reading the reactions { #reading-the-reactions }

Every participant sees each reaction on the **camera tile** of whoever sent it, and counted in the **status rail** at the top of the meeting, the most common first. The rail also counts the reactions of participants that [Smart Layout](smart-layout.md) keeps off the grid, so a class answering a question can be read in one place. On phones, the rail keeps the one or two most common reactions and its **⋯** menu lists them all.

<a class="glightbox" href="/assets/videos/meet/meetings/reactions/reactions-pulse-dark.mp4" data-type="video" data-gallery="dark"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/reactions/reactions-pulse-dark.mp4#only-dark" preload="none" muted playsinline loop></video></a>
<a class="glightbox" href="/assets/videos/meet/meetings/reactions/reactions-pulse-light.mp4" data-type="video" data-gallery="light"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/reactions/reactions-pulse-light.mp4#only-light" preload="none" muted playsinline loop></video></a>

Clicking the counts opens the **Participants** panel, where each reaction takes the place of the participant's avatar.

<a class="glightbox" href="/assets/videos/meet/meetings/reactions/reactions-panel-dark.mp4" data-type="video" data-gallery="dark"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/reactions/reactions-panel-dark.mp4#only-dark" preload="none" muted playsinline loop></video></a>
<a class="glightbox" href="/assets/videos/meet/meetings/reactions/reactions-panel-light.mp4" data-type="video" data-gallery="light"><video class="round-corners lazy-video" src="/assets/videos/meet/meetings/reactions/reactions-panel-light.mp4#only-light" preload="none" muted playsinline loop></video></a>

!!! info "Note"

    Reactions are not stored: a participant who joins the meeting does not see the reactions sent before, and reactions do not appear in [recordings](../recordings/overview.md).

## Who can react { #who-can-react }

Sending reactions requires the `participantReactionSend` permission. Seeing the reactions of others is never restricted. The permission is granted by default to the `Moderator` and `Speaker` [predefined roles](../rooms/access.md#predefined-roles). It can be revoked in the room's role permissions or in a member's [custom permissions](../room-members/management.md#edit-a-member), which hides the **Reactions** button for those participants.

## Enable or disable reactions for a room { #enable-or-disable }

Reactions are enabled by default when a room is [created](../rooms/management.md#create-rooms), whether through the UI or the [REST API :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/createRoom){:target="_blank"}. They can be turned off per room from the **Features** section of the **Meeting** step of the room configuration wizard, using the **Reactions** toggle, or with the room config `reactions.enabled`. In a room with reactions turned off, the button is not shown and every reaction is rejected.

![Room wizard step with the reactions toggle](../../../assets/images/meet/meetings/reactions/room-wizard-reactions-dark.webp#only-dark){ .control-height .round-corners loading=lazy }
![Room wizard step with the reactions toggle](../../../assets/images/meet/meetings/reactions/room-wizard-reactions-light.webp#only-light){ .control-height .round-corners loading=lazy }

## From your application { #embedded }

When OpenVidu Meet is [embedded](../../embedded/intro.md), the host application sends a reaction on behalf of the local participant with the `participantReactionSend` [command](../../embedded/reference/webcomponent.md#commands) of the Web Component and the iframe. The `participantReactionSent` [event](../../embedded/reference/webcomponent.md#events) tells the host about every reaction sent in the meeting, the local participant's included, with who sent it.

Both name each reaction with a plain string: the [Unicode CLDR short name :fontawesome-solid-external-link:{.external-link-icon}](https://unicode.org/emoji/charts/full-emoji-list.html){:target="_blank"} of its emoji, in snake_case. The host application compares and stores these values without writing any emoji in its code, and shows each reaction with the emoji or icon of its choice.

| Reaction | Value                    |
| :------: | ------------------------ |
| 👍       | `thumbs_up`              |
| 👎       | `thumbs_down`            |
| 😀       | `grinning_face`          |
| 🙁       | `slightly_frowning_face` |
| 😕       | `confused_face`          |
| 😮       | `face_with_open_mouth`   |
| 👏       | `clapping_hands`         |
| ❤️       | `red_heart`              |

The values are listed in the order the picker offers them, the same order as the keys `1` to `8`.

```javascript
const openviduMeet = document.querySelector('openvidu-meet');

openviduMeet.participantReactionSend('thumbs_up');

openviduMeet.on('participantReactionSent', (event) => {
	if (event.reaction === 'thumbs_up') {
		console.log(`${event.participant.participantName} agrees`);
	}
});
```
