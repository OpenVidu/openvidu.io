# Room Members

A **room member** is any individual granted access to a specific [room](https://openvidu.io/3.8/meet/features/rooms/overview/index.md). Every room member joins as a **participant** of the meetings held in that room.

There are three kinds of room member:

- **Users** — individuals with an OpenVidu Meet [account](https://openvidu.io/3.8/meet/features/users/overview/index.md). They access the room through its shared user access link, logging in with their credentials.
- **Identified guests** — individuals without an account, added to the room with a fixed name. Each one accesses the room through their own **unique** personal access link, with no login required.
- **Anonymous guests** — individuals without an account who access the room through a [shared anonymous access link](https://openvidu.io/3.8/meet/features/rooms/access/#anonymous-access), providing a name before joining the meeting.

Info

**Users** and **identified guests** are *explicitly added* to a room, so they can be listed and managed individually. **Anonymous guests** are not: anyone holding a shared anonymous access link can access the room, so they cannot be added, listed or revoked one by one — they only exist once they join a meeting.

## Explicit members vs. anonymous guests

Add **users** or **identified guests** when you need controlled, personalized access; rely on **anonymous guests** for quick, open access.

| Access approach               | How it works                                                                                                                                                                                                                                                                                   | When to use                                                              |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Users & identified guests** | Specific individuals are added to the room, each with a fixed identity, a base role and optional custom permissions. Their access can be revoked individually at any time.                                                                                                                     | Controlled access with predefined identities and per-person permissions. |
| **Anonymous guests**          | Anyone with the room's `Moderator` or `Speaker` [shared anonymous access link](https://openvidu.io/3.8/meet/features/rooms/access/#anonymous-access) can join with that predefined role's permissions. Anonymous access can be enabled or disabled per role when creating or editing the room. | Quick or public meetings where you don't need to track who joins.        |

## Users vs Identified guests

Both are explicitly added to the room, but they differ in how they are identified and how they join:

| Aspect             | Users                                                                                                      | Identified guests                                   |
| ------------------ | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| **Account**        | Require an existing [OpenVidu Meet account](https://openvidu.io/3.8/meet/features/users/overview/index.md) | No account required                                 |
| **Identification** | Identified by their user account                                                                           | Identified by the name given when they were added   |
| **Access link**    | Share the room's single user access link                                                                   | Each gets a **unique** link that must not be shared |
| **Authentication** | Must log in with their credentials                                                                         | None — the unique link grants access directly       |
| **Typical use**    | Team members, employees or regular collaborators                                                           | Guests, clients or one-time participants            |

## Permissions

Every room member has a set of permissions derived from a base role:

- **Anonymous guests** get the role of the [shared anonymous access link](https://openvidu.io/3.8/meet/features/rooms/access/#anonymous-access) they use — `Moderator` or `Speaker` — with that [predefined role's permissions](https://openvidu.io/3.8/meet/features/rooms/access/#predefined-roles).
- **Users and identified guests** are assigned a base role (`Moderator` or `Speaker`) when added to the room, which can be fine-tuned with [custom permissions](https://openvidu.io/3.8/meet/features/room-members/management/#add-a-member).

## In this section

- [Creation & Management](https://openvidu.io/3.8/meet/features/room-members/management/index.md) — add, edit, list and remove the users and identified guests of a room from its **"Room Members"** tab, and the equivalent REST API operations.
