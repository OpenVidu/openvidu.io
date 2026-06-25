---
title: Users in OpenVidu Meet
description: Users in OpenVidu Meet - account roles (admin, room_manager, room_member), the root administrator, and how users relate to room access.
tags:
    - setupcustomgallery
---

# Users

OpenVidu Meet has a built-in user management system that controls access to the OpenVidu Meet app. **Users** are accounts identified by a `userId` and protected by a password. Each user is assigned a **role** that determines what they can do.

## User roles

Every user has one of the following roles:

| Role | Description | Permissions |
| --- | --- | --- |
| **admin** | Administrator | Full control over OpenVidu Meet: create and manage **all** [users](management.md), [rooms](../rooms/overview.md), [room members](../room-members/overview.md) and [recordings](../recordings/overview.md). Can also change the system configuration — [room appearance](../rooms/management.md#room-appearance), [webhook configuration](../../embedded/reference/webhooks.md) and [API key](../../embedded/reference/rest-api.md#generate-an-api-key). |
| **room_manager** | Room manager | Can create and manage **their own** rooms, including their configuration, members and recordings. Can also access rooms — and their recordings, depending on their [member permissions](../room-members/overview.md#permissions) — where they are a member, or that are [open to all users](../rooms/access.md#member-access-links). |
| **room_member** | Room member | Can only access rooms — and their recordings, depending on their [member permissions](../room-members/overview.md#permissions) — where they are a member, or that are open to all users. Cannot create or manage rooms. |

!!! info

    Roles control what a user can do in OpenVidu Meet as an account. The permissions a member has in a room are a separate concept. See [Room Members](../room-members/overview.md) for more information on how member permissions work.

## Root administrator { #root-administrator }

The root administrator is a special user with the fixed `userId` **`admin`**. This user has full control over OpenVidu Meet and **cannot be deleted**. Its password is set during installation:

- In **local deployments**: the password is always **`admin`**.
- In **production deployments**: the password is specified during installation (or randomly generated if not provided).

These credentials are required to access the OpenVidu Meet app, at least for the first time, to create other users and manage the system:

<a class="glightbox" href="../../../../assets/images/meet/users-and-permissions/login-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="../../../../assets/images/meet/users-and-permissions/login-dark.png#only-dark" loading="lazy" class="control-height round-corners"/></a>
<a class="glightbox" href="../../../../assets/images/meet/users-and-permissions/login-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="../../../../assets/images/meet/users-and-permissions/login-light.png#only-light" loading="lazy" class="control-height round-corners"/></a>

The location of the initial administrator password depends on the deployment environment:

=== "Local (Demo)"

    Credentials are always username **`admin`** and password **`admin`**.

=== "On Premises"

    Credentials will be logged at the end of the installation process:

    ```
    OpenVidu Meet is available at:

        URL: https://<YOUR_DOMAIN>
        Credentials:
          - User: admin
          - Password: XXXXXXX
    ```

    !!! warning
        If you [change the administrator password](management.md#changing-credentials), this value will no longer be valid.

=== "AWS"

    In the Secrets Manager of the CloudFormation stack, in secret **`MEET_INITIAL_ADMIN_PASSWORD`**

    !!! warning
        If you [change the administrator password](management.md#changing-credentials), this value will no longer be valid.

=== "Azure"

    In the Azure Key Vault, in secret **`MEET_INITIAL_ADMIN_PASSWORD`**

    !!! warning
        If you [change the administrator password](management.md#changing-credentials), this value will no longer be valid.

## How users access rooms

Users do not get access to a room just by having an account. Access works as follows:

- **Admins** and the **room owner** always have full access to a room, with all permissions granted.
- A user added as a [member](../room-members/overview.md) of a room can access it through the **room's user access link**, logging in with their credentials.
- If a room is configured to be **accessible to all users**, any user can join — even without being an explicit member — with `Speaker` permissions.

See [Room Access](../rooms/access.md) for the complete picture of how access to a room is granted.

## In this section

- [Creation & Management](management.md) — create users, update their role, reset passwords and delete users from the OpenVidu Meet app (admins only), change your own password, and the equivalent REST API operations.
