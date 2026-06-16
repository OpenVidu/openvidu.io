---
title: Room member creation & management in OpenVidu Meet
description: Add, edit, list and remove users and identified guests of an OpenVidu Meet room from the app or the Room Members REST API.
tags:
    - setupcustomgallery
---

# Creation & Management

Room members are managed from the **"Room Members"** tab of the [room details page](../rooms/management.md#room-details), or programmatically through the [REST API](#rest-api-reference).

Only two kinds of member are managed here: [users](overview.md#users-vs-identified-guests) and [identified guests](overview.md#users-vs-identified-guests). [Anonymous guests](../rooms/access.md#anonymous-access) cannot be added or listed, since their identity is only known once they join.

## Add a member

From the room's **"Room Members"** tab, click **"Add Member"** and choose the member type:

- **User** — pick an existing [user](../users/overview.md) account. They access the room through the shared [user access link](../rooms/access.md#member-access-links), logging in with their credentials.

    !!! info

          **Admins** and the room **owner** cannot be added as room members — they are already _implicit_ members of the room, with full access and all permissions granted.

- **Identified guest** — type a fixed display name. OpenVidu Meet generates a **unique personal access link** for them, which grants access with no login.

Then choose a **base role** (`Moderator` or `Speaker`) that sets the default [permissions](../rooms/access.md#predefined-roles), and optionally fine-tune them with **custom permissions**.

<a class="glightbox" href="../../../../assets/images/meet/rooms-and-meetings/add-room-member-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery30"><img src="../../../../assets/images/meet/rooms-and-meetings/add-room-member-dark.png#only-dark" loading="lazy" class="control-height round-corners"/></a>
<a class="glightbox" href="../../../../assets/images/meet/rooms-and-meetings/add-room-member-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery30"><img src="../../../../assets/images/meet/rooms-and-meetings/add-room-member-light.png#only-light" loading="lazy" class="control-height round-corners"/></a>

## List & filter members

The **"Room Members"** tab lists the room's users and identified guests, showing each member's name, role and type. You can **search** by name and **filter** by base role or by type (user / identified guest).

<a class="glightbox" href="../../../../assets/images/meet/rooms-and-meetings/room-members-tab-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery31"><img src="../../../../assets/images/meet/rooms-and-meetings/room-members-tab-dark.png#only-dark" loading="lazy" class="round-corners"/></a>
<a class="glightbox" href="../../../../assets/images/meet/rooms-and-meetings/room-members-tab-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery31"><img src="../../../../assets/images/meet/rooms-and-meetings/room-members-tab-light.png#only-light" loading="lazy" class="round-corners"/></a>

## Edit a member

Update a member's **base role** or **custom permissions** from the member list. Changes apply **immediately** — even if the member is currently in a meeting, their permissions are updated on the fly.

## Copy a member's access link

Every member's access link can be copied from the member list:

- **Identified guests** have a **unique personal access link**. Copy it and deliver it privately to the intended individual.
- **Users** do not have a personal link, but their link can also be copied from the member list — it is the shared [user access link](../rooms/access.md#member-access-links) that every user of the room logs in through.

## Remove members

Members can be removed individually or in bulk from the **"Room Members"** tab.

!!! warning

    When a room member is removed, their access is immediately revoked. An identified guest's unique link stops working, and any member currently in an active meeting is expelled from it.

## REST API reference { #rest-api-reference }

All of these operations can also be performed programmatically with the [OpenVidu Meet REST API](../../embedded/reference/rest-api.md). See the [REST API specification :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html){:target="\_blank"} for the full list of available endpoints, request bodies and response schemas.

| Operation           | HTTP Method | Reference                                                                                                                                                  |
| ------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Add a member        | POST        | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/addRoomMember){:target="\_blank"}         |
| List members        | GET         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRoomMembers){:target="\_blank"}        |
| Bulk delete members | DELETE      | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/bulkDeleteRoomMembers){:target="\_blank"} |
| Get a member        | GET         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRoomMember){:target="\_blank"}         |
| Update a member     | PUT         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/updateRoomMember){:target="\_blank"}      |
| Delete a member     | DELETE      | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/deleteRoomMember){:target="\_blank"}      |
