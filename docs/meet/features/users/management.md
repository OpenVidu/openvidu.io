---
title: User creation & management in OpenVidu Meet
description: Create users, update roles, reset and change passwords, and delete users in OpenVidu Meet from the app or the Users REST API.
tags:
    - setupcustomgallery
---

# Creation & Management

Only **admin** users can manage other users — from the **"Users"** page of the OpenVidu Meet app or programmatically through the [REST API](#rest-api-reference). Any user can change their own password from their profile.

## Create a user

From the **"Users"** page, click **"Create User"** and provide a `userId`, a name and a [role](overview.md#user-roles) (`admin`, `room_manager` or `room_member`). For the **temporary password**, you can either specify one or auto-generate one and then copy it.

!!! info

    The `userId` must be between 5 and 20 characters and contain only lowercase letters, numbers and underscores.

<a class="glightbox" href="/assets/videos/meet/users/management/create-user-dark.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="/assets/videos/meet/users/management/create-user-dark.mp4#only-dark" loading="lazy" defer muted playsinline autoplay loop async></video></a>
<a class="glightbox" href="/assets/videos/meet/users/management/create-user-light.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="/assets/videos/meet/users/management/create-user-light.mp4#only-light" loading="lazy" defer muted playsinline autoplay loop async></video></a>

Send the credentials to the user. On their **first login** they are required to change the temporary password before they can use OpenVidu Meet.

<a class="glightbox" href="/assets/images/meet/users/management/force-change-password-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="/assets/images/meet/users/management/force-change-password-dark.png#only-dark" loading="lazy" class="round-corners"/></a>
<a class="glightbox" href="/assets/images/meet/users/management/force-change-password-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="/assets/images/meet/users/management/force-change-password-light.png#only-light" loading="lazy" class="round-corners"/></a>

## Update a user's role

Change a user's [role](overview.md#user-roles) from the user list at any time. The [root administrator](overview.md#root-administrator) (**`admin`**) and your own account cannot be modified.

<a class="glightbox" href="/assets/videos/meet/users/management/update-user-role-dark.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="/assets/videos/meet/users/management/update-user-role-dark.mp4#only-dark" loading="lazy" defer muted playsinline autoplay loop async></video></a>
<a class="glightbox" href="/assets/videos/meet/users/management/update-user-role-light.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="/assets/videos/meet/users/management/update-user-role-light.mp4#only-light" loading="lazy" defer muted playsinline autoplay loop async></video></a>

## Reset a user's password

Generate a new temporary password for a user from the user list (for example, if they forgot theirs). As with creation, the user must set a new password on their next login.

<a class="glightbox" href="/assets/videos/meet/users/management/reset-user-password-dark.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="/assets/videos/meet/users/management/reset-user-password-dark.mp4#only-dark" loading="lazy" defer muted playsinline autoplay loop async></video></a>
<a class="glightbox" href="/assets/videos/meet/users/management/reset-user-password-light.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="/assets/videos/meet/users/management/reset-user-password-light.mp4#only-light" loading="lazy" defer muted playsinline autoplay loop async></video></a>

## List & filter users

The **"Users"** page lists every user with their role and registration date. You can search by name and filter by role.

<a class="glightbox" href="/assets/images/meet/users/management/users-list-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="/assets/images/meet/users/management/users-list-dark.png#only-dark" loading="lazy" class="round-corners"/></a>
<a class="glightbox" href="/assets/images/meet/users/management/users-list-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="/assets/images/meet/users/management/users-list-light.png#only-light" loading="lazy" class="round-corners"/></a>

Clicking a user opens their **profile page**, which shows the user's details together with buttons for every action you can perform on them: [update their role](#update-a-users-role), [reset their password](#reset-a-users-password) and [delete the user](#delete-users).

<a class="glightbox" href="/assets/images/meet/users/management/profile-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="/assets/images/meet/users/management/profile-dark.png#only-dark" loading="lazy" class="round-corners"/></a>
<a class="glightbox" href="/assets/images/meet/users/management/profile-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="/assets/images/meet/users/management/profile-light.png#only-light" loading="lazy" class="round-corners"/></a>

## Delete users

Users can be deleted individually or in bulk from the **"Users"** page. The root administrator cannot be deleted, and you cannot delete your own account. Deleting a user removes their account and automatically removes them from any room where they were a [member](../room-members/overview.md). In addition:

- If the user **owns rooms**, ownership of those rooms is transferred to the [root administrator](overview.md#root-administrator).
- If the user is **currently in a meeting**, they are kicked from it immediately.

<a class="glightbox" href="/assets/videos/meet/users/management/delete-user-dark.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="/assets/videos/meet/users/management/delete-user-dark.mp4#only-dark" loading="lazy" defer muted playsinline autoplay loop async></video></a>
<a class="glightbox" href="/assets/videos/meet/users/management/delete-user-light.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="/assets/videos/meet/users/management/delete-user-light.mp4#only-light" loading="lazy" defer muted playsinline autoplay loop async></video></a>

## Changing your password { #changing-credentials }

Any user can change their own password from their **Profile** page. You are asked to enter your **current password** and then type the **new password twice** to confirm it. Once changed, the new password is required the next time you log in.

<a class="glightbox" href="/assets/images/meet/users/management/change-password-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="/assets/images/meet/users/management/change-password-dark.png#only-dark" loading="lazy" class="round-corners"/></a>
<a class="glightbox" href="/assets/images/meet/users/management/change-password-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="/assets/images/meet/users/management/change-password-light.png#only-light" loading="lazy" class="round-corners"/></a>

## REST API reference { #rest-api-reference }

All of these operations can also be performed programmatically with the [OpenVidu Meet REST API](../../embedded/reference/rest-api.md). See the [REST API specification :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html){:target="\_blank"} for the full list of available endpoints, request bodies and response schemas.

| Operation               | HTTP Method | Reference                                                                                                                                              |
| ----------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Create a user           | POST        | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/createUser){:target="\_blank"}        |
| List users              | GET         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getUsers){:target="\_blank"}          |
| Bulk delete users       | DELETE      | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/bulkDeleteUsers){:target="\_blank"}   |
| Get a user              | GET         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getUser){:target="\_blank"}           |
| Delete a user           | DELETE      | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/deleteUser){:target="\_blank"}        |
| Reset a user's password | PUT         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/resetUserPassword){:target="\_blank"} |
| Update a user's role    | PUT         | [Reference :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/updateUserRole){:target="\_blank"}    |
