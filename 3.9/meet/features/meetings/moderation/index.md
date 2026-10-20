# Meeting moderation

The **Participants** panel of the [Meeting view](https://openvidu.io/3.9/meet/features/meetings/lifecycle/#meeting-view) lists everyone in the meeting, with the current state of their **microphone**, **camera** and **screen share**. Participants with the right [permissions](https://openvidu.io/3.9/meet/features/rooms/access/#predefined-roles) act on the others from there:

- **Mute** another participant's microphone, turn off their camera or stop their screen share, one device at a time (`participantMute` permission).
- **Turn off for everyone**: mute every microphone, turn off every camera or stop every screen share at once (`participantMute` permission).
- **Remove** a participant from the meeting (`participantKick` permission).
- **Promote** a participant to moderator, or demote them back (`participantPromote` permission). See [Role Management](https://openvidu.io/3.9/meet/features/meetings/role-management/index.md).

## Muting participants

Muting only ever turns a device **off**: a moderator can never turn on somebody else's microphone or camera. The affected participant is told that a moderator turned off one of their devices, and may turn it back on at any time. Moderators cannot be muted, and turning off a device for everyone leaves the moderators alone.

`participantMute` is granted by default to the `Moderator` [predefined role](https://openvidu.io/3.9/meet/features/rooms/access/#predefined-roles) of every room created from OpenVidu Meet 3.9.0 on. Rooms and room members that existed before start without it, so it has to be granted explicitly in the room's role permissions or in the member's [custom permissions](https://openvidu.io/3.9/meet/features/room-members/management/#edit-a-member).

## Removing participants

A participant with the `participantKick` permission can **remove** any other participant from the meeting. The removed participant is taken to the [End view](https://openvidu.io/3.9/meet/features/meetings/lifecycle/#end-view), which tells them they were removed, and the [`participantLeft` webhook](https://openvidu.io/3.9/meet/embedded/reference/webhooks/index.md) reports `participant_kicked` as the reason.

## From your application

When OpenVidu Meet is [embedded](https://openvidu.io/3.9/meet/embedded/intro/index.md), the same actions are available to the host application as the `participantMute`, `participantMuteAll`, `participantKick` and `meetingEnd` [commands](https://openvidu.io/3.9/meet/embedded/reference/webcomponent/#commands) of the Web Component and the iframe. They act on behalf of the local participant, so they require that participant to hold the corresponding permission.

## REST API reference

Live meetings can be read and moderated from your backend with the [Meetings REST API](https://openvidu.io/3.9/meet/embedded/reference/rest-api/index.md). Reading a meeting or its participants requires the `meetingRead` permission, and each moderation action the permission named above; a request authenticated with the API key is not subject to them.

| Operation                   | HTTP Method | Reference                                                                                               |
| --------------------------- | ----------- | ------------------------------------------------------------------------------------------------------- |
| Get a live meeting          | GET         | [Reference](https://openvidu.io/3.9/meet/embedded/reference/api.html#/operations/meetingGet)            |
| End a meeting               | DELETE      | [Reference](https://openvidu.io/3.9/meet/embedded/reference/api.html#/operations/meetingEnd)            |
| List participants           | GET         | [Reference](https://openvidu.io/3.9/meet/embedded/reference/api.html#/operations/participantList)       |
| Get a participant           | GET         | [Reference](https://openvidu.io/3.9/meet/embedded/reference/api.html#/operations/participantGet)        |
| Kick a participant          | DELETE      | [Reference](https://openvidu.io/3.9/meet/embedded/reference/api.html#/operations/participantKick)       |
| Mute a participant          | PUT         | [Reference](https://openvidu.io/3.9/meet/embedded/reference/api.html#/operations/participantMute)       |
| Mute all participants       | PUT         | [Reference](https://openvidu.io/3.9/meet/embedded/reference/api.html#/operations/participantMuteAll)    |
| Update a participant's role | PUT         | [Reference](https://openvidu.io/3.9/meet/embedded/reference/api.html#/operations/participantRoleUpdate) |
