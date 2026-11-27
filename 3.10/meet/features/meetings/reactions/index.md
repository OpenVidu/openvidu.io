# Reactions

Participants **react** with an emoji to show how they feel without speaking or writing in the chat: a thumbs up to agree, a confused face when something is not clear, applause at the end of a talk. A reaction shows for **10 seconds** and then fades away, so whoever leads the meeting reads the room at a glance.

## Sending a reaction

Hover over the **Reactions** button in the toolbar, right after [**Raise hand**](https://openvidu.io/3.10/meet/features/meetings/raise-hand/index.md), and pick one of the eight reactions: 👍 👎 😀 🙁 😕 😮 👏 ❤️. From the keyboard, press `E` anywhere outside a text field to open the picker, and then a number from `1` to `8` to send the reaction in that place. In a meeting embedded with the Web Component, these keys work once you have clicked inside the meeting, not while you are using the rest of the page. On phones, the reactions are in the **More options** menu.

Your reaction shows on your own camera tile, and the button wears it with a ring that empties as its time runs out. A new reaction replaces the previous one and starts its time over.

## Reading the reactions

Every participant sees each reaction on the **camera tile** of whoever sent it, and counted in the **status rail** at the top of the meeting, the most common first. The rail also counts the reactions of participants that [Smart Layout](https://openvidu.io/3.10/meet/features/meetings/smart-layout/index.md) keeps off the grid, so a class answering a question can be read in one place. On phones, the rail keeps the one or two most common reactions and its **⋯** menu lists them all.

Clicking the counts opens the **Participants** panel, where each reaction takes the place of the participant's avatar.

> **Note**
>
> Reactions are not stored: a participant who joins the meeting does not see the reactions sent before, and reactions do not appear in [recordings](https://openvidu.io/3.10/meet/features/recordings/overview/index.md).

## Who can react

Sending reactions requires the `participantSendReaction` permission. Seeing the reactions of others is never restricted. The permission is granted by default to the `Moderator` and `Speaker` [predefined roles](https://openvidu.io/3.10/meet/features/rooms/access/#predefined-roles). It can be revoked in the room's role permissions or in a member's [custom permissions](https://openvidu.io/3.10/meet/features/room-members/management/#edit-a-member), which hides the **Reactions** button for those participants.

## Enable or disable reactions for a room

Reactions are enabled by default when a room is [created](https://openvidu.io/3.10/meet/features/rooms/management/#create-rooms), whether through the UI or the [REST API](https://openvidu.io/3.10/meet/embedded/reference/api.html#/operations/roomCreate) . They can be turned off per room from the **Features** section of the **Meeting** step of the room configuration wizard, using the **Reactions** toggle, or with the room config `reactions.enabled`. In a room with reactions turned off, the button is not shown and every reaction is rejected.

## From your application

When OpenVidu Meet is [embedded](https://openvidu.io/3.10/meet/embedded/intro/index.md), the host application sends a reaction on behalf of the local participant with the `participantSendReaction` [command](https://openvidu.io/3.10/meet/embedded/reference/webcomponent/#commands) of the Web Component and the iframe. The `participantReactionSent` [event](https://openvidu.io/3.10/meet/embedded/reference/webcomponent/#events) tells the host about every reaction sent in the meeting, the local participant's included, with who sent it.

Both name each reaction with a plain string: the [Unicode CLDR short name](https://unicode.org/emoji/charts/full-emoji-list.html) of its emoji, in snake_case. The host application compares and stores these values without writing any emoji in its code, and shows each reaction with the emoji or icon of its choice.

| Reaction | Value                    |
| -------- | ------------------------ |
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

openviduMeet.participantSendReaction('thumbs_up');

openviduMeet.on('participantReactionSent', (event) => {
    if (event.reaction === 'thumbs_up') {
        console.log(`${event.participant.participantName} agrees`);
    }
});
```
