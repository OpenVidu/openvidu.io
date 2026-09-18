# Role Management

Every participant joins a meeting with a different set of permissions:

- **Users** and **identified guests** have by default the permissions of their **base role** (`Moderator` or `Speaker`), which can be fine-tuned **independently for each member** with [custom permissions](https://openvidu.io/3.8/meet/features/room-members/management/#add-a-member).
- **Anonymous guests** can only join through the [shared `Moderator` or `Speaker` link](https://openvidu.io/3.8/meet/features/rooms/access/#anonymous-access), so they always have the [predefined permissions of that role](https://openvidu.io/3.8/meet/features/rooms/access/#predefined-roles) and cannot be customized.

During a meeting, these permissions are not fixed. Participants with the `canMakeModerator` permission can **promote** other participants to moderator or **demote** them back to their original permissions.

Info

`canMakeModerator` is one of the permissions the `Moderator` [predefined role](https://openvidu.io/3.8/meet/features/rooms/access/#predefined-roles) grants by default. For the complete list of permissions, see the [MeetPermissions](https://openvidu.io/3.8/meet/embedded/reference/api.html#/schemas/MeetPermissions) schema.

## Promoting participants to moderator

A participant with the `canMakeModerator` permission can **promote to moderator** any other participant whose permissions are **lower** than the full set of `Moderator` predefined role permissions. The promotion grants that participant all the moderator permissions they were missing.

Participant menu with the option to promote to moderator

The promotion is **temporary** and scoped to the ongoing meeting:

- It does **not** modify the member's configured base role or custom permissions.
- As soon as the promoted participant leaves the meeting — **including refreshing the browser** — the extra permissions are dropped and they return to their **original permissions**.

## Demoting participants

A participant with the `canMakeModerator` permission can also **demote** a promoted participant at any time, reverting them to the **original permissions** they joined the meeting with.

Participant menu with the option to demote a moderator

Info

A **promoted** moderator cannot demote an **original** moderator — a participant who already had moderator permissions when they joined, rather than being promoted during the meeting. This prevents temporarily-promoted moderators from stripping permissions from the participants who were moderators from the start.
