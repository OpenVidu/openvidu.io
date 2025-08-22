---
title: Users and permissions
tags:
  - setupcustomgallery
---

# Users and permissions

## OpenVidu Meet authentication

!! ATENCION !!

PENDIENTE DE IMPLEMENTAR

!! ATENCION !!

OpenVidu Meet is by default protected with a **username and password** randomly generated after the installation. Users will be required those credentials when connecting to OpenVidu Meet.

<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/login-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="../../../assets/images/meet/users-and-permissions/login-dark.png#only-dark" loading="lazy" class="control-height"/></a>
<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/login-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="../../../assets/images/meet/users-and-permissions/login-light.png#only-light" loading="lazy" class="control-height"/></a>

The location of the credentials depends on the environment of the deployment:

=== "Local (development)"

=== "On Premises"

=== "AWS"

=== "Azure"

### Modify OpenVidu Meet authentication

!! ATENCION !!

PENDIENTE DE MEJORAR: qué es el concepto de "admin" user? El cambio de contraseña maestra debería ser más seguro.

!! ATENCION !!

Once logged in, you can modify the authentication method to access OpenVidu Meet from the **"User & Permissions"** view:

<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/change-authentication.png" data-type="image" data-desc-position="bottom" data-gallery="gallery2"><img src="../../../assets/images/meet/users-and-permissions/change-authentication.png" loading="lazy"/></a>

!!! info
    The only authentication method currently offered by OpenVidu Meet is a single **username and password**, but we are working on adding support for multi-user credentials and OAuth.

## User authentication when joining a meeting

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

## Participant roles in a meeting

Participants in a meeting can have different roles, which grant different permissions. The role of a participant is determined by the room link used to join the meeting. See [Room links](./rooms-and-meetings.md#room-links) for more information.

Available roles are:

- **Moderator**: grants permissions to end the meeting, start/stop recordings, share room links and manage participants. Also grants permissions of `Speaker` and `Viewer` roles.
- **Speaker**: grants permissions to share their camera, microphone and screen. Also grants permissions of `Viewer` role.
- **Viewer** **:hammer:`(COMING SOON)`:hammer:**: can only watch the meeting without participating.

### Changing participant roles during a meeting

Participants with `Moderator` role can upgrade or downgrade other participants' roles during the meeting from the "Participants" side panel:

<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/upgrade-role.png" data-type="image" data-desc-position="bottom" data-gallery="gallery5"><img src="../../../assets/images/meet/users-and-permissions/upgrade-role.png" loading="lazy"/></a>

### Fine-grained participant permissions **:hammer: [COMING SOON] :hammer:**

Predefined participant roles such as `Moderator`, `Speaker` or `Viewer` provide a coarse-grained permission model, which is enough for most use cases. However, OpenVidu Meet will also allow creating room links with fine-grained permissions. This way, you can give specific permissions to specific participants (such as the ability to share the screen, to use the chat...). Stay tuned for future updates!