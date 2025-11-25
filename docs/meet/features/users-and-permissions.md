---
title: Users and permissions
tags:
  - setupcustomgallery
---

# Users and permissions

## Participant roles in a room

Participants in a room can have different roles, which grant different permissions. There are two ways to define a participant's role:

1. **Through general room links**: By using the general `Moderator` or `Speaker` room link. See [General room links](./rooms-and-meetings.md#general-room-links) for more information.
2. **Through room members**: By creating a specific member with custom permissions. See [Room members](#room-members) for more information.

### Standard roles

When accessing a room through general room links, participants are assigned one of these standard roles:

#### Moderator

Grants full permissions including:

- Meeting management: end the meeting for all participants
- Recording control: start/stop recordings, retrieve and delete recordings
- Participant management: share room links, promote other participants, kick participants
- Media publishing: publish video, audio, and share screen
- Communication: send chat messages, change virtual background

#### Speaker

Grants basic participation permissions:

- Media publishing: publish video, audio, and share screen
- Communication: send chat messages, change virtual background

### Custom role for room members

When accessing a room through a member-specific URL, the participant is assigned a **Custom** role with a personalized set of permissions. These permissions are defined when the room member is created and can be different from the standard `Moderator` and `Speaker` roles.

### Changing participant roles during a meeting

Participants with `Moderator` role can upgrade or downgrade other participants' roles during the meeting from the "Participants" side panel:

<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/upgrade-role.png" data-type="image" data-desc-position="bottom" data-gallery="gallery5"><img src="../../../assets/images/meet/users-and-permissions/upgrade-role.png" loading="lazy"/></a>

## Room members

Room members are specific individuals with personalized access to a room. Each member has:

- A **fixed participant name** that cannot be changed when joining.
- A **unique access URL** that should not be shared with others.
- **Custom permissions** tailored to their needs, which can be different from standard `Moderator` or `Speaker` roles.

Room members are ideal for scenarios where you need:

- Fine-grained access control for specific users.
- Pre-defined participant names for identification.
- The ability to revoke access to specific individuals without affecting others.

### Creating room members

Room members can only be created via the [REST API :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/addRoomMember){:target="_blank"}. When creating a member, you specify:

- **Participant name**: The fixed name that will be displayed in the meeting.
- **Base role**: Either `moderator` or `speaker`, which defines the initial set of permissions.
- **Custom permissions**: Optional overrides to grant or restrict specific capabilities beyond the base role.

The API returns a member object containing the unique access URL and member ID.

### Managing room members

Room members can be managed through the REST API:

- **Retrieve member information**: [GET /rooms/:roomId/members/:memberId :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/getRoomMember){:target="_blank"}
- **Delete a member**: [DELETE /rooms/:roomId/members/:memberId :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/deleteRoomMember){:target="_blank"}

!!! warning
    When a room member is deleted, their access is immediately revoked. If they are currently in an active meeting, they will be expelled from it.

### Available permissions

Room members can have any combination of the following permissions:

| Permission | Description |
|------------|-------------|
| `canRecord` | Can start/stop recording the meeting |
| `canRetrieveRecordings` | Can list and play recordings |
| `canDeleteRecordings` | Can delete recordings |
| `canShareAccessLinks` | Can share access links to invite others |
| `canMakeModerator` | Can promote other participants to moderator role |
| `canKickParticipants` | Can remove other participants from the meeting |
| `canEndMeeting` | Can end the meeting for all participants |
| `canPublishVideo` | Can publish video in the meeting |
| `canPublishAudio` | Can publish audio in the meeting |
| `canShareScreen` | Can share screen in the meeting |
| `canChat` | Can send chat messages in the meeting |
| `canChangeVirtualBackground` | Can change the virtual background |

When creating a member, you start with a base role (`moderator` or `speaker`) and then override specific permissions as needed. For example, you could create a member with `speaker` base role but grant them `canRecord` permission.

## OpenVidu Meet authentication

OpenVidu Meet is by default protected with an administrator **username and password**. These credentials will be required when accessing OpenVidu Meet console:

<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/login-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="../../../assets/images/meet/users-and-permissions/login-dark.png#only-dark" loading="lazy" class="control-height round-corners"/></a>
<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/login-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="../../../assets/images/meet/users-and-permissions/login-light.png#only-light" loading="lazy" class="control-height round-corners"/></a>

The initial administrator credentials are:

- **Username**: **`admin`**
- **Password**: specified on installation time

The value of the password will be asked on installation. If left empty, a random password will be generated.
The location of the administration password depends on the environment of the deployment:

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
        If you [modify the initial administrator password](#modify-openvidu-meet-authentication), this value will no longer be valid.

=== "AWS"

    In the Secrets Manager of the CloudFormation stack, in secret **`MEET_INITIAL_ADMIN_PASSWORD`**

    !!! warning
        If you [modify the initial administrator password](#modify-openvidu-meet-authentication), this value will no longer be valid.

=== "Azure"

    In the Azure Key Vault, in secret **`MEET_INITIAL_ADMIN_PASSWORD`**

    !!! warning
        If you [modify the initial administrator password](#modify-openvidu-meet-authentication), this value will no longer be valid.

### Modify OpenVidu Meet authentication

Administrator credentials can be modified from the **"User & Permissions"** view:

<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/change-authentication.png" data-type="image" data-desc-position="bottom" data-gallery="gallery2"><img src="../../../assets/images/meet/users-and-permissions/change-authentication.png" loading="lazy"/></a>

<!--## User authentication when joining a meeting

Meetings are always accessed through a **room link**. Room links are unique URLs with random segments difficult to decipher, ensuring a first layer of security: only users that know the link can access the meeting.

!!! info 
    Learn how to obtain room links to be shared here: [Room links](./rooms-and-meetings.md#room-links).

Room links provide a reasonable level of security, but it might not be enough for certain use cases. For this  reason, further authentication can be enforced for users trying to join a meeting using a valid room link. From the **"User & Permissions"** page in OpenVidu Meet, you can configure it:

- **Nobody**: no authentication is required. Anyone with a valid room link can join the meeting.
- **Only moderators**: users joining the meeting through a `Moderator` room link with must authenticate first.
- **Everybody**: all users joining the meeting must authenticate first.

<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/authentication-to-join-meeting.png" data-type="image" data-desc-position="bottom" data-gallery="gallery5"><img src="../../../assets/images/meet/users-and-permissions/authentication-to-join-meeting.png" loading="lazy"/></a>

!!! info
    The only authentication method currently available to enforce when joining a meeting is the OpenVidu Meet **username and password**. Other authentication methods are on the way, including multi-user credentials and OAuth.

-->