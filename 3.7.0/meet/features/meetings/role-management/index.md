# Role Management

Participants in a meeting are assigned a role that determines their default set of permissions. The role is determined by the [room access link](https://openvidu.io/3.7.0/meet/features/rooms/access/#getting-room-access-links) used to join.

## Predefined roles

### Moderator

Grants full meeting permissions by default:

- **Meeting management**: end the meeting for all participants
- **Recording control** (`canRecord`): start/stop recordings, retrieve and delete recordings
- **Participant management** (`canMakeModerator`): promote other participants to moderator; (`canShareAccessLinks`): share room access links; kick participants
- **Media publishing**: publish video, audio, and share screen
- **Communication**: send chat messages, change virtual background

### Speaker

Grants basic participation permissions by default:

- **Media publishing**: publish video, audio, and share screen
- **Communication**: send chat messages, change virtual background

Info

The default permissions for `Moderator` and `Speaker` roles can be customized per room when [creating](https://openvidu.io/3.7.0/meet/features/rooms/creation-management/#create-rooms) or [editing](https://openvidu.io/3.7.0/meet/features/rooms/creation-management/#edit-rooms) it. For the complete list of available permissions, see the [REST API](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/schemas/MeetPermissions) .

## Promoting participants to moderator

During an active meeting, participants with the `canMakeModerator` permission can promote or demote other participants from the **"Participants"** side panel:

When a participant is promoted to moderator:

- They receive all permissions associated with the `Moderator` role.
- The promotion applies only to the current session and does not modify their configured permissions.
- The promotion can be undone by demoting the participant back to their original role.
