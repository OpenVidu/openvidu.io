---
title: "OpenVidu 3.8.0 release notes"
draft: false
date: 2026-07-09
slug: release-380
description: "OpenVidu 3.8.0 is out: user accounts, role-based access and fine-grained room members in Meet, plus a mediasoup overhaul and tighter TURN security."
categories:
    - Release
tags:
    - WebRTC
    - mediasoup
    - Security
    - Self-hosted
    - Video Conferencing
authors:
    - pabloFuente
hide:
    - navigation
    - search-bar
    - version-selector
---

# OpenVidu 3.8.0 is now available

OpenVidu 3.8.0 brings a major step forward for both OpenVidu Platform and OpenVidu Meet.

On the **OpenVidu Platform** side, the standout change is a complete mediasoup overhaul: RTX, DTX, AV1/VP9/H264 codecs and SVC are now fully supported, bringing mediasoup on par with Pion in terms of features while delivering a 2x performance boost. This release also tightens TURN security and improves the robustness of deployments across all supported clouds.

On the **OpenVidu Meet** side, this release introduces real user accounts with role-based access and fine-grained, per-person room permissions, turning the previous "share a link" model into a complete access control system. It also comes with a redesigned application, now fully translated into 10 languages, and a range of improvements to the in-meeting experience.

Continue reading for the complete release notes of both products.

<!-- more -->

## OpenVidu Platform

- **mediasoup updates**: all restrictions on using [mediasoup as the RTC engine](https://openvidu.io/3.8/docs/self-hosting/production-ready/performance/#about-mediasoup-integration) have been addressed. Previous versions of mediasoup had [several limitations](https://openvidu.io/3.7/docs/self-hosting/production-ready/performance/#limitations) that prevented OpenVidu from fully leveraging its capabilities. These have now all been resolved, making mediasoup comparable to Pion in terms of features while delivering the 2x performance boost. Below is the complete list of mediasoup-related improvements:
    - Upgrade mediasoup from v3.19.19 to **v3.19.21** ([changes :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/versatica/mediasoup/compare/3.19.19...3.19.21){:target="_blank"}).
    - [**ConnectionQuality** :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/intro/basics/rooms-participants-tracks/webhooks-events/#connection-quality){:target="_blank"} events now available in mediasoup.
    - **Screen Share simulcast greatly improved**: layer selection was buggy when screens became static, causing low-quality layers to always take precedence once the screen started moving again. The result was low-resolution screen sharing that was barely legible. This has now been fixed, and simulcast layer selection properly chooses high-quality layers as long as each participant's network bandwidth allows it.
    - **RTX support**: mediasoup now fully supports RTX, the retransmission mechanism that mitigates packet loss in media traffic. This greatly improves video behavior in poor network conditions.
    - **DTX support**: mediasoup now fully implements DTX (Discontinuous Transmission) for Opus audio. This is an important optimization that reduces the audio bitrate when participants are not speaking. It saves up to 90% of the bitrate during silence periods, without affecting speech quality once they start speaking again.
    - Support for **H264**, **VP9**, and **AV1** video codecs: previous versions of mediasoup forced the VP8 video codec due to certain limitations. These issues have now been resolved, so the remaining codecs are allowed.
    - **SVC** in AV1 and VP9: now that mediasoup supports the AV1 and VP9 codecs, SVC (Scalable Video Coding) is also available. SVC is a modern approach to multi-layered video encoding, where a single stream is encoded in multiple qualities and the server forwards only the layers each consumer needs. It is more efficient than simulcast, since the sender encodes just once instead of producing several independent streams.
- **Deployment improvements**:
    - Fixed several race conditions in the deployment process that could end up in a broken deployment.
    - Fixed a rare config synchronization problem caused by a Redis timeout in OpenVidu Elastic and OpenVidu High Availability deployments.
    - If no domain is defined for the OpenVidu deployment, the public IP is now used as the domain instead of [sslip.io :fontawesome-solid-external-link:{.external-link-icon}](https://sslip.io/){:target="_blank"}.
    - The Promtail service of OpenVidu's [observability stack](https://openvidu.io/3.8/docs/self-hosting/production-ready/observability/) has been replaced by [Alloy :fontawesome-solid-external-link:{.external-link-icon}](https://grafana.com/docs/alloy/latest/){:target="_blank"}. Promtail has been deprecated and Alloy is now the recommended log collector for OpenVidu deployments.
    - **Oracle Deployment**: scale-in implemented for OpenVidu Elastic and OpenVidu High Availability. See [Custom scale-in strategy](https://openvidu.io/3.8/docs/self-hosting/elastic/oracle/install/#custom-scale-in-strategy) for OpenVidu Elastic in Oracle and [Custom scale-in strategy](https://openvidu.io/3.8/docs/self-hosting/ha/oracle/install/#custom-scale-in-strategy) for OpenVidu High Availability in Oracle.
    - **GCP Deployment**: there was a bug in the cron job that triggered the graceful shutdown of the same Media Node multiple times, ultimately causing a forced shutdown of OpenVidu services without waiting for rooms to finish. GCP now properly waits for rooms to finish before shutting down the Media Node. See commit [#82ae32b :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/OpenVidu/openvidu/commit/82ae32b9fe0865192faaeb8d1a96151a96b2f969){:target="_blank"}.
    - **Azure Deployment**: fixed a bug in the High Availability deployment that could cause a failed Media Node to never be deleted and re-deployed. See commit [#99d7660 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/OpenVidu/openvidu/commit/99d76604053219119c8fd15ca23a2d4d0a6fcb3b){:target="_blank"}.
- **Improved TURN security**: OpenVidu now blocks all private IPs when relaying traffic through the TURN server, except for the known private IPs of each node. On startup, the OpenVidu cluster automatically configures itself, auto-discovering the private IP of each node and allowing private TURN relay traffic only between those specific IPs. This happens automatically, with no need for manual whitelisting. It improves the overall security of the deployment and prevents TURN-relay-abuse attacks. You can learn all about TURN server security here: [TURN server security](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/turn-security/).
- **Speech Processing agent**: important fixes to the memory management of [Speech Processing agents](https://openvidu.io/3.8/docs/ai/openvidu-agents/speech-processing-agent/). Previously, the agent could enter a memory-consumption loop without freeing memory, which could ultimately cause a memory shortage on the node hosting it. Multiple memory leaks have been addressed, improving the stability of the agent when running for long periods.
- **LiveKit stack updated to v1.12.0**: OpenVidu is now based on LiveKit v1.12.0. See the complete list of changes from the previous supported version here: [v1.9.12 vs v1.12.0 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/livekit/compare/v1.9.12...v1.12.0){:target="_blank"}.
- New configuration property **`advertise_internal_ip`** available in [`livekit.yaml`](https://openvidu.io/3.8/docs/self-hosting/configuration/reference/#livekityaml) to enable announcing the private IP in ICE host candidates when `use_external_ip` is true. This allows clients to connect to the OpenVidu deployment from both private and public networks.
- **Fixed nil pointer dereference** in OpenVidu Server that could cause an unexpected crash of the service ([Issue 8 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/OpenVidu/openvidu-livekit/issues/8){:target="_blank"}).
- **openvidu-browser-v2compatibility**: method [Stream.reconnect :fontawesome-solid-external-link:{.external-link-icon}](https://docs.openvidu.io/en/stable/api/openvidu-browser/classes/Stream.html#reconnect){:target="_blank"} of OpenVidu v2 API is now wired up to work in OpenVidu v3. You can learn more about updating your OpenVidu v2 web application to work against an OpenVidu v3 deployment in the [OpenVidu v2 compatibility guide :fontawesome-solid-external-link:{.external-link-icon}](https://docs.openvidu.io/en/stable/openvidu3/#2-update-your-application){:target="_blank"}.

## OpenVidu Meet

- **Users and role-based accounts**: OpenVidu Meet now lets you register multiple users and assign each one a role that controls what they can do in the application. There are three roles — `admin` (full control over all users, rooms, members, recordings and system configuration), `room_manager` (can create and manage their own rooms) and `room_member` (can only access rooms where they are a member). Learn more in the [Users](https://openvidu.io/3.8/meet/features/users/overview/) feature.
- **Room members with fine-grained access**: you can now grant access to a room to specific individuals — either registered [users](https://openvidu.io/3.8/meet/features/users/overview/) or [identified guests](https://openvidu.io/3.8/meet/features/room-members/overview/) (people without an account who each receive a unique personal access link). Every member is added with a base role (`Moderator` or `Speaker`) whose default permissions can be customized individually, per member. See the [Room Members](https://openvidu.io/3.8/meet/features/room-members/overview/) feature for the complete picture.
- **Customizable default role permissions per room**: the default permissions of the `Moderator` and `Speaker` roles can now be customized when [creating](https://openvidu.io/3.8/meet/features/rooms/management/#create-rooms) or [editing](https://openvidu.io/3.8/meet/features/rooms/management/#edit-rooms) a room, letting you tailor what each role can do on a per-room basis.
- **Per-room anonymous access control**: anonymous access can now be disabled per role for individual rooms. You can independently enable or disable the `Moderator` and `Speaker` [shared anonymous access links](https://openvidu.io/3.8/meet/features/rooms/access/#anonymous-access) when creating or editing a room.
- **Improved room creation wizard**: the room wizard has been redesigned to guide you through the full room setup, including access configuration, role permissions and room members, all in one place.
- **Redesigned OpenVidu Meet app**: the application has been expanded with new pages and forms to manage everything from the UI — a user list, a user profile page, a room details page (showing the room's recordings and members), a recording details page, and dedicated forms for creating users and adding members.
- **Full internationalization (i18n)**: OpenVidu Meet is now fully translated, with support for 10 languages: Chinese, English, German, Spanish, French, Hindi, Italian, Japanese, Dutch and Portuguese. The interface automatically adapts to the user's language.
- **New filters for rooms and recordings**: additional filtering options have been added to the rooms and recordings lists, making it easier to find what you are looking for.
- **New `show-recording` WebComponent attribute**: the [OpenVidu Meet WebComponent](https://openvidu.io/3.8/meet/embedded/reference/webcomponent/) now accepts a `show-recording` attribute to embed the recording playback view. Unlike the existing `recording-url` attribute, `show-recording` takes a recording identifier alongside the room `room-url` and inherits the permissions from the room URL, offering a simpler alternative to display a specific recording.
- **Meeting experience improvements**: several enhancements to the in-meeting experience:
    - **Network quality indicator**: a network quality indicator is now displayed for each participant, both on the participant's video tile and in the Participants panel, giving a clear view of individual connection quality at a glance.
    - **New status indicators in the Participants panel**: the Participants panel now shows a set of per-participant status indicators — a **speaking** indicator that highlights who is currently talking, plus indicators for participants who have their **microphone muted**, their **camera turned off**, or are **sharing their screen**.
    - **Flexible self-view**: the self-view video (your own camera preview) can now be resized independently to better fit your preferences, and it stays independent from the meeting layout as more participants join, so it no longer gets rearranged with everyone else.
    - **Manual zoom for screen sharing**: when viewing a shared screen, participants can now manually zoom in and out to customize the view and focus on the details that matter to them.
    - **Categorized virtual backgrounds**: the [virtual backgrounds](https://openvidu.io/3.8/meet/features/meetings/virtual-background/) have been updated and are now organized into categories (such as _Professional_, _Home Office_ and _Creative_), making it easier to browse and pick the right background.
    - **Improved live captions performance**: the live captions agent has been optimized, delivering faster and more reliable real-time captions during meetings. Learn more about [Live captions](https://openvidu.io/3.8/meet/features/meetings/live-captions/).

### Breaking changes

All breaking changes in this release are related to the [REST API](https://openvidu.io/3.8/meet/embedded/reference/rest-api/):

- **Anonymous access links moved in the room object**: the `moderatorUrl` and `speakerUrl` properties of the room response have been moved to `access.anonymous.moderator.url` and `access.anonymous.speaker.url` respectively. Update any integration that reads the anonymous access links from the [MeetRoom :fontawesome-solid-external-link:{.external-link-icon}](https://openvidu.io/3.8/meet/embedded/reference/api.html#/schemas/MeetRoom){:target="_blank"} object accordingly.
- **Recording access replaced by per-member permissions**: the room configuration property `config.recording.allowAccessTo` has been removed. Access to a room's recordings is now governed by fine-grained [room member permissions](https://openvidu.io/3.8/meet/features/recordings/overview/#recording-permissions): `canRetrieveRecordings` (list, play and download recordings) and `canDeleteRecordings` (delete recordings). **Admins** always retain full access to any recording (retrieve and delete), regardless of these permissions. By default, the `Moderator` role has both permissions and the `Speaker` role has only `canRetrieveRecordings`. To reproduce the behavior of the removed property, adjust the default permissions of the `Moderator` and `Speaker` roles when [creating](https://openvidu.io/3.8/meet/features/rooms/management/#create-rooms) or [editing](https://openvidu.io/3.8/meet/features/rooms/management/#edit-rooms) the room:
    - **`admin`** (previously only admins could retrieve and delete recordings): disable both `canRetrieveRecordings` and `canDeleteRecordings` for the `Moderator` and `Speaker` roles. Admins keep full access regardless.
    - **`admin_moderator`** (previously only admins and moderators could retrieve and delete recordings): keep `canRetrieveRecordings` and `canDeleteRecordings` enabled for `Moderator`, and disable both for `Speaker`.
    - **`admin_moderator_speaker`** (previously everyone could retrieve recordings, but only admins and moderators could delete them): this is exactly the new default, so no change is needed — `Moderator` keeps both permissions and `Speaker` keeps only `canRetrieveRecordings`.
- **Rooms API no longer returns `config` by default**: endpoints that return a room object (or an array of rooms) no longer include the `config` property in the response by default. To include it, request it explicitly using the `extraFields=config` query parameter or the `X-ExtraFields` HTTP header.

