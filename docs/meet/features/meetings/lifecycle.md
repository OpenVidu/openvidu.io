---
title: "Meeting lifecycle in OpenVidu Meet"
description: "The views a participant moves through during an OpenVidu Meet meeting, from the Join and Device views to the Meeting, Recording and End views."
page_features:
  - setupcustomgallery
---

# Meeting lifecycle

Meetings consist of different views, shown to room members in sequence from the moment they open a room access link until the meeting ends.

## Lobby view

This is the first view members see when accessing a room. It allows setting a nickname before joining the meeting. If the member has the required permissions, they can also access the [Recordings view](#recordings-view) of this room from here.

![Lobby view where a member sets a nickname before joining](../../../assets/images/meet/meetings/lifecycle/lobby-view-dark.png#only-dark){ .control-height .round-corners loading=lazy }
![Lobby view where a member sets a nickname before joining](../../../assets/images/meet/meetings/lifecycle/lobby-view-light.png#only-light){ .control-height .round-corners loading=lazy }

## Device view

This view allows members to tune their microphone and camera before joining the meeting, as well as setting a [virtual background](virtual-background.md).

![Device view for tuning microphone, camera and virtual background](../../../assets/images/meet/meetings/lifecycle/device-view-dark.png#only-dark){ .control-height .round-corners loading=lazy }
![Device view for tuning microphone, camera and virtual background](../../../assets/images/meet/meetings/lifecycle/device-view-light.png#only-light){ .control-height .round-corners loading=lazy }

## Meeting view

The Meeting View is the central interface where all participants can see, hear, and interact with each other in real time. It features a [smart, dynamic layout](smart-layout.md) that automatically adapts to the number of active participants, ensuring an optimal viewing experience at all times.

![Meeting view with participant videos and the toolbar](../../../assets/images/meet/meetings/lifecycle/meeting-view-dark.png#only-dark){ .control-height .round-corners loading=lazy }
![Meeting view with participant videos and the toolbar](../../../assets/images/meet/meetings/lifecycle/meeting-view-light.png#only-light){ .control-height .round-corners loading=lazy }

## Recordings view

This view allows to manage all recordings of the room (from the current or past meetings). Members with the required permissions can review, play, download, and delete them, as well as share recordings via a link.

![Recordings view listing the recordings of the room](../../../assets/images/meet/recordings/management/room-recordings-dark.png#only-dark){ .control-height .round-corners loading=lazy }
![Recordings view listing the recordings of the room](../../../assets/images/meet/recordings/management/room-recordings-light.png#only-light){ .control-height .round-corners loading=lazy }

!!! info

    Recordings can also be accessed from the "Recordings" page in OpenVidu Meet. See [Managing recordings](../recordings/management.md#managing-recordings).

## End view

This view is shown to a participant when the meeting ends, at least for that participant. It informs about the specific reason why the meeting ended (a moderator ended it, the participant was kicked from the meeting, etc.).

![End view shown when the meeting ends for a participant](../../../assets/images/meet/meetings/lifecycle/end-view-dark.png#only-dark){ .control-height .round-corners loading=lazy }
![End view shown when the meeting ends for a participant](../../../assets/images/meet/meetings/lifecycle/end-view-light.png#only-light){ .control-height .round-corners loading=lazy }
