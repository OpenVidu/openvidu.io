# Meeting lifecycle

Meetings consist of different views, shown to participants in sequence from the moment they open a room link until the meeting ends.

## Join view

This is the first view participants see when accessing a room link. It allows setting a nickname before joining the meeting. If the participant has the required permissions, they can also access the [Recording view](#recording-view) of this room from here.

## Device view

This view allows participants tuning their microphone and camera before joining the meeting, as well as setting a [virtual background](https://openvidu.io/3.7.0/meet/features/meetings/virtual-background/index.md).

\[[](../../../../assets/videos/meet/device-view-dark.mp4#only-dark)\](https://openvidu.io/3.7.0/assets/videos/meet/device-view-dark.mp4) \[[](../../../../assets/videos/meet/device-view-light.mp4#only-light)\](https://openvidu.io/3.7.0/assets/videos/meet/device-view-light.mp4)

## Meeting view

The Meeting View is the central interface where all participants can see, hear, and interact with each other in real time. It features a [smart, dynamic layout](https://openvidu.io/3.7.0/meet/features/meetings/smart-layout/index.md) that automatically adapts to the number of active participants, ensuring an optimal viewing experience at all times.

## Recording view

This view allows to manage the recording of the meeting while it is active. Participants with the required permissions can review, play, download, delete, and share the recording via a link.

Info

Recordings can also be accessed from the "Recordings" page in OpenVidu Meet, even after the meeting has ended. See [List Recordings](https://openvidu.io/3.7.0/meet/features/recordings/creation-management/#list-recordings).

## End view

This view is shown to a participant when the meeting ends, at least for that participant. It informs about the specific reason why the meeting ended (an administrator ended it, the participant was evicted from the meeting, etc.).
