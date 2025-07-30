---
title: Users and permissions
tags:
  - setupcustomgallery
---

# Users and permissions

OpenVidu Meet offers two different layers of user management and permissions:

- [Authentication when accessing OpenVidu Meet](#authentication-when-accessing-openvidu-meet): how users authenticate to access the OpenVidu Meet application.
- [Authentication when joining a meeting](#authentication-when-joining-a-meeting): how users authenticate to join a specific meeting.

## Authentication when accessing OpenVidu Meet

First of all, OpenVidu Meet is by default protected with a **username and password** randomly generated after the first installation. Only users with valid credentials can access the application:

<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/login.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="../../../assets/images/meet/users-and-permissions/login.png" loading="lazy"/></a>

!!! note
    We will refer as an **administrator** to any user that has access to OpenVidu Meet with valid credentials. Once logged in, users can manage rooms, meetings, recordings and any other OpenVidu Meet feature.

### Changing OpenVidu Meet authentication

Once logged in, you can modify the authentication method to access OpenVidu Meet from the "User & Permissions" view:

<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/change-authentication.png" data-type="image" data-desc-position="bottom" data-gallery="gallery2"><img src="../../../assets/images/meet/users-and-permissions/change-authentication.png" loading="lazy"/></a>

These are the available options to authenticate users when accessing OpenVidu Meet:

- **Single user**: the default option, not recommended for production environments.
- **Multi user**: allows creating multiple username-password pairs.
- **Oauth**: allows authenticating users through an external OAuth provider.
- ...

## Authentication when joining a meeting

Meetings are always accessed through **room links**. There are different types of room links, each granting different permissions to the participants (see [Participant permissions in a meeting](#participant-permissions-in-a-meeting)).

- Administrators can share links for a room from the "Rooms" page.

<a class="glightbox" href="../../../assets/videos/meet/share-room-link-from-console.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery3"><video class="round-corners" src="../../../assets/videos/meet/share-room-link-from-console.mp4" loading="lazy" defer muted playsinline autoplay loop async></video></a>

- Participants with role "Moderator" can share links for ongoing meetings directly from the meeting itself (see [Participant permissions in a meeting](#participant-permissions-in-a-meeting)).

<a class="glightbox" href="../../../assets/videos/meet/meet-share-link.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery4"><video class="round-corners" src="../../../assets/videos/meet/meet-share-link.mp4" loading="lazy" defer muted playsinline autoplay loop async></video></a>

Further authentication can be enforced for users trying to join a meeting using a valid room link. From the "User & Permissions" page, administrators can configure which users must authenticate before joining a meeting:

- **Nobody**: no authentication is required. Anyone with a valid room link can join the meeting.
- **Only moderators**: users joining the meeting through a room link with "Moderator" role must authenticate first.
- **Everybody**: all users joining the meeting must authenticate first.

<a class="glightbox" href="../../../assets/images/meet/users-and-permissions/authentication-to-join-meeting.png" data-type="image" data-desc-position="bottom" data-gallery="gallery5"><img src="../../../assets/images/meet/users-and-permissions/authentication-to-join-meeting.png" loading="lazy"/></a>

## Participant permissions in a meeting

Participants in a meeting can have different permissions. These permissions are defined by the **role** assigned to each participant, which is determined by the room link used to join the meeting.

Available roles are:

- **Moderator**: can end the meeting, start/stop recordings, share room links and manage participants.
- **Speaker**: can share their camera, microphone and screen.
- **Viewer** **:hammer:`(COMING SOON)`:hammer:**: can only watch the meeting without participating.

### Fine-grained participant permissions **:hammer:`(COMING SOON)`:hammer:**

Predefined participant roles provide a coarse-grained permission model, which is enough for most use cases. However, OpenVidu Meet also allows creating room links with fine-grained permissions. This way, you can give specific permissions to specific participants (such as the ability to share the screen, to use the chat...)

...