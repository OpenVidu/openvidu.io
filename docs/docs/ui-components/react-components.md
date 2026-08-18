---
title: "React Components for OpenVidu apps"
description: "Build real-time audio and video UIs in React with the LiveKit-compatible React components, hooks and contexts shipped with OpenVidu."
---

# React Components

## Introduction

React Components are the simplest way to create real-time audio/video applications with React. There's no need to manage state or low level events, React Components from LiveKit handle all the complexity for you.

## Featured Components

A curated set of components that we believe are essential and serve as a solid foundation for most applications.

<div class="grid cards three-cols" markdown>
-   __LiveKitRoom__

    ---

	It provides the Room context to all its children, serving as the root component of your application, and also exposes the Room state through a React context.

	---

	[:octicons-arrow-right-24: See Reference](https://docs.livekit.io/reference/components/react/component/livekitroom/){:target="_blank"}

-   __RoomAudioRenderer__

    ---

	It manages remote participants' audio tracks and ensures that microphones and screen sharing are audible. It also provides a way to control the volume of each participant.

	---

    [:octicons-arrow-right-24: See Reference](https://docs.livekit.io/reference/components/react/component/roomaudiorenderer/){:target="_blank"}


-   __TrackLoop__

    ---

	Provides an easy way to loop through all participant camera and screen tracks. For each track, TrackLoop creates a TrackRefContext that you can use to render the track.

	---

    [:octicons-arrow-right-24: See Reference](https://docs.livekit.io/reference/components/react/component/trackloop/){:target="_blank"}

</div>

## Prefabricated Components

Prefabricated are constructed using components and enhanced with additional functionalities, unique styles, and practical defaults. They are designed for immediate use and are not meant to be extended.

<div class="grid three-cols" markdown="span">

[AudioConference](https://docs.livekit.io/reference/components/react/component/audioconference/){ .card .no-shadow target="_blank" }
[Chat](https://docs.livekit.io/reference/components/react/component/chat/){ .card .no-shadow target="_blank" }
[ControlBar](https://docs.livekit.io/reference/components/react/component/controlbar/){ .card .no-shadow target="_blank" }
[MediaDeviceMenu](https://docs.livekit.io/reference/components/react/component/mediadevicemenu/){ .card .no-shadow target="_blank" }
[PreJoin](https://docs.livekit.io/reference/components/react/component/prejoin/){ .card .no-shadow target="_blank" }
[VideoConference](https://docs.livekit.io/reference/components/react/component/videoconference/){ .card .no-shadow target="_blank" }

</div>

## Contexts

Contexts are used to allow child components to access parent state without having to pass it down the component tree via props

<div class="grid three-cols" markdown="span">

[Participant](https://docs.livekit.io/reference/components/react/component/participantcontext/){ .card .no-shadow target="_blank" }
[Room](https://docs.livekit.io/reference/components/react/component/roomcontext/){ .card .no-shadow target="_blank" }
[Chat](https://github.com/livekit/components-js/blob/main/packages/react/src/context/chat-context.ts){ .card .no-shadow target="_blank" }
[Feature](https://github.com/livekit/components-js/blob/main/packages/react/src/context/feature-context.ts){ .card .no-shadow target="_blank" }
[Layout](https://docs.livekit.io/reference/components/react/component/layoutcontext/){ .card .no-shadow target="_blank" }
[Pin](https://github.com/livekit/components-js/blob/main/packages/react/src/context/pin-context.ts){ .card .no-shadow target="_blank" }
[TrackRef](https://docs.livekit.io/reference/components/react/component/trackrefcontext/){ .card .no-shadow target="_blank" }

</div>

## Hooks

Hooks are functions that let you use state and other React features without writing a class. They are functions that let you “hook into” React state and lifecycle features from function components.

React Components provides a set of hooks that you can use to interact with the components and the underlying LiveKit client.

[:octicons-arrow-right-24: See Reference](https://github.com/livekit/components-js/tree/main/packages/react/src/hooks){:target="_blank"}

## Applications

A practical example showcases the potential of React Components is the production-ready flagship application, [**LiveKit Meet** :fontawesome-solid-external-link:{.external-link-icon}](https://meet.livekit.io/){:target="_blank"}. This application is built using React Components and demonstrates the power and flexibility of the library.

## References

- [React Components :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/components/react/){:target="_blank"}
