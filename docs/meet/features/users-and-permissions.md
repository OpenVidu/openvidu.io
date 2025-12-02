---
title: Users and permissions
tags:
  - setupcustomgallery
---

# Users and permissions

## OpenVidu Meet internal users

OpenVidu Meet has an internal user management system that controls access to the OpenVidu Meet console and the ability to create and manage rooms. Internal users are identified by a `userId` and can be assigned one of three roles.

### Root administrator

The root administrator is a special user with the fixed `userId` **`admin`**. This user has full control over OpenVidu Meet and cannot be deleted. The root administrator password is set during installation:

- In **local deployments**: the password is always **`admin`**.
- In **production deployments**: the password is specified during installation (or randomly generated if not provided).

These credentials are required when accessing the OpenVidu Meet console:

<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/login-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="../../../assets/images/meet/users-and-permissions/login-dark.png#only-dark" loading="lazy" class="control-height round-corners"/></a>
<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/login-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="../../../assets/images/meet/users-and-permissions/login-light.png#only-light" loading="lazy" class="control-height round-corners"/></a>

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
        If you [modify the administrator password](#changing-credentials), this value will no longer be valid.

=== "AWS"

    In the Secrets Manager of the CloudFormation stack, in secret **`MEET_INITIAL_ADMIN_PASSWORD`**

    !!! warning
        If you [modify the administrator password](#changing-credentials), this value will no longer be valid.

=== "Azure"

    In the Azure Key Vault, in secret **`MEET_INITIAL_ADMIN_PASSWORD`**

    !!! warning
        If you [modify the administrator password](#changing-credentials), this value will no longer be valid.

### Internal user roles

Internal users can have one of the following roles:

| Role | Description | Permissions |
|------|-------------|-------------|
| **admin** | Administrator | Full control over OpenVidu Meet, including user management, room creation and management for all rooms, and system configuration |
| **user** | Regular user | Can create and manage their own rooms, assign room members, and configure room settings |
| **room_member** | Room member only | Can only access rooms where they have been explicitly added as a member; cannot create or manage rooms |

### Managing internal users from the console

Internal users with the **admin** role can manage other internal users from the OpenVidu Meet console in the **"Users & Permissions"** view. From there, administrators can:

- **Create new users**: Add new internal users with a `userId`, name, password, and role.
<!-- - **Modify existing users**: Change user passwords and roles. -->
- **Delete users**: Remove internal users from the system.

!!! info
    The root administrator (**`admin`**) cannot be deleted, but its password can be changed.

### Changing credentials

Users credentials can be modified from the **"Users & Permissions"** view:

<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/change-authentication.png" data-type="image" data-desc-position="bottom" data-gallery="gallery2"><img src="../../../assets/images/meet/users-and-permissions/change-authentication.png" loading="lazy"/></a>

## Room members

Room members are specific individuals (internal users or external users) with personalized access to a room. There are two ways users can access a room: as **anonymous users** using anonymous room access links, or as **explicit room members** with customized permissions.

### Anonymous access vs. explicit room members

| Access Type | How it works | Use case |
|-------------|--------------|----------|
| **Anonymous access** | Any user can access by using the predefined anonymous `Moderator` or `Speaker` room access links. Users are assigned standard role permissions (either full `Moderator` or basic `Speaker` permissions). Anonymous access can be enabled or disabled per role when creating or updating a room. | Quick meetings, public rooms, or scenarios where you don't need to track specific individuals. |
| **Explicit room members** | Specific individuals are added as room members with personalized URLs and custom permissions. Each member has a fixed name and tailored access. | Controlled access, pre-defined names, custom permissions, and the ability to revoke access for specific individuals. |

### Internal users as room members vs. external users

When creating a room member, you can designate them as either an **internal user** (someone with an OpenVidu Meet `userId`) or an **external user** (someone without an OpenVidu Meet account). The key differences are:

| Aspect | Internal users | External users |
|--------|----------------|----------------|
| **Identification** | Identified by their OpenVidu Meet `userId` | Identified by a generated `ext-XXX` ID |
| **Access URL** | All internal user room members share the same access URL for the room. They are identified through authentication. | Each external user receives a unique access URL that must not be shared |
| **Authentication** | Must authenticate with their OpenVidu Meet credentials when accessing the room | No authentication required; access is granted via the unique URL |
| **Use case** | For team members, employees, or regular collaborators with OpenVidu Meet accounts | For guests, clients, or one-time participants without OpenVidu Meet accounts |

### Creating room members

Room members can be created via the [REST API :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/addRoomMember){:target="_blank"}. When creating a member, you specify:

- **User type**: Whether the member is an internal user (provide `userId`) or an external user (provide `name`).
- **Base role**: Either `moderator` or `speaker`, which defines the initial set of permissions.
- **Custom permissions**: Optional overrides to grant or restrict specific capabilities beyond the base role.

The API returns a member object containing:

- **Member ID**: The unique identifier for this room member.
- **Name**: The fixed name that will be displayed in the meeting.
- **Access URL**: The URL to access the room (shared for internal users, unique for external users).
- **Permissions**: The final set of permissions assigned to the member.

### Managing room members

Room members can be managed through the REST API:

- **List all members**: [GET /rooms/:roomId/members :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRoomMembers){:target="_blank"}
- **Retrieve member information**: [GET /rooms/:roomId/members/:memberId :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRoomMember){:target="_blank"}
- **Update member permissions**: [PATCH /rooms/:roomId/members/:memberId :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/updateRoomMember){:target="_blank"}
- **Delete a member**: [DELETE /rooms/:roomId/members/:memberId :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/deleteRoomMember){:target="_blank"}

!!! warning
    When a room member is deleted, their access is immediately revoked. If they are currently in an active meeting, they will be expelled from it.

## Predefined roles and permissions

### Room Owner

The **Room Owner** is the internal user who created the room. The owner always has full permissions within the room, regardless of any custom permission configurations. The owner role cannot be changed or removed.

When a room is created through the [REST API :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/createRoom){:target="_blank"}, the owner will be the root administrator (**`admin`**).

### Anonymous access roles

Users accessing a room through anonymous access links are assigned one of these predefined roles:

#### Moderator

Grants full permissions by default including:

- **Meeting management**: end the meeting for all participants
- **Recording control**: start/stop recordings, retrieve and delete recordings
- **Participant management**: share access links, promote other participants, kick participants
- **Media publishing**: publish video, audio, and share screen
- **Communication**: send chat messages, change virtual background

#### Speaker

Grants basic participation permissions by default:

- **Media publishing**: publish video, audio, and share screen
- **Communication**: send chat messages, change virtual background

!!! info
    The default permissions for `Moderator` and `Speaker` roles can be customized when creating or updating a room. For the complete list of available permissions and their descriptions, see the [REST API :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/schemas/MeetPermissions){:target="_blank"}.

## Managing participants during meetings

During an active meeting, participants with appropriate permissions can manage other participants in real-time. These changes are temporary and only affect the current session.

### Promoting participants to moderator

Participants with the `canMakeModerator` permission can promote other participants to the moderator role from the "Participants" side panel:

<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/upgrade-role.png" data-type="image" data-desc-position="bottom" data-gallery="gallery5"><img src="../../../assets/images/meet/users-and-permissions/upgrade-role.png" loading="lazy"/></a>

When a participant is promoted to moderator:

- They receive all permissions associated with the `Moderator` role.
- The promotion applies only to the current session and does not modify their configured permissions.
- The promotion can be undone by demoting the participant back to their original permissions.
