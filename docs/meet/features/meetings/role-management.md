---
title: Role Management in OpenVidu Meet
description: Promote participants to Moderator during an OpenVidu Meet meeting to grant them full moderator permissions, and demote them back to their original permissions.
tags:
    - setupcustomgallery
---

# Role Management

Every participant enters a meeting with a set of permissions inherited from their [room member](../room-members/overview.md):

- **Users** and **identified guests** start with the permissions of their **base role** (`Moderator` or `Speaker`), which can be fine-tuned **independently for each member** with [custom permissions](../room-members/management.md#add-a-member).
- **Anonymous guests** can only join through the [shared `Moderator` or `Speaker` link](../rooms/access.md#anonymous-access), so they always have the **default permissions of that role** and cannot be customized.

During a live meeting these permissions are not fixed. Participants with the `canMakeModerator` permission can **promote** other participants to moderator and **demote** them back, all from the **"Participants"** side panel.

!!! info
    `canMakeModerator` is one of the permissions the `Moderator` [predefined role](../rooms/access.md#predefined-roles) grants by default. For the complete list of permissions, see the [MeetPermissions :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/schemas/MeetPermissions){:target="\_blank"} schema.

## Promoting participants to moderator { #promoting-participants-to-moderator }

A participant with the `canMakeModerator` permission can promote any other participant whose permissions are **lower than the full set of moderator permissions**. The promotion grants that participant **all the moderator permissions they were missing**.

<a class="glightbox" href="../../../../assets/images/meet/users-and-permissions/upgrade-role.png" data-type="image" data-desc-position="bottom" data-gallery="gallery5"><img src="../../../../assets/images/meet/users-and-permissions/upgrade-role.png" loading="lazy"/></a>

The promotion is **temporary** and scoped to the ongoing meeting:

- It does **not** modify the member's configured base role or custom permissions.
- As soon as the promoted participant leaves the meeting — **including refreshing the browser** — the extra permissions are dropped and they return to their **original permissions**.

## Demoting participants { #demoting-participants }

A participant with the `canMakeModerator` permission can also **demote** a promoted participant at any time, reverting them to the **original permissions** they joined the meeting with.

Because demoting only undoes a previous promotion, it has no effect on participants who already held the full set of moderator permissions when they joined.

!!! warning
    A **promoted** moderator cannot demote an **original** moderator — a participant who already had moderator permissions when they joined, rather than being promoted during the meeting. This prevents temporarily-promoted moderators from stripping permissions from the participants who were moderators from the start.
