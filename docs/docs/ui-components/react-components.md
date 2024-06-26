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

<div class="grid three-cols">

<a href="https://docs.livekit.io/reference/components/react/component/audioconference/" target="_blank" class="card no-shadow">AudioConference</a>
<a href="https://docs.livekit.io/reference/components/react/component/chat/" target="_blank" class="card no-shadow">Chat</a>
<a href="https://docs.livekit.io/reference/components/react/component/controlbar/" target="_blank" class="card no-shadow">ControlBar</a>
<a href="https://docs.livekit.io/reference/components/react/component/mediadevicemenu/" target="_blank" class="card no-shadow">MediaDeviceMenu</a>
<a href="https://docs.livekit.io/reference/components/react/component/prejoin/" target="_blank" class="card no-shadow">PreJoin</a>
<a href="https://docs.livekit.io/reference/components/react/component/videoconference/" target="_blank" class="card no-shadow">VideoConference</a>

</div>

## Contexts

Contexts are used to allow child components to access parent state without having to pass it down the component tree via props

<div class="grid three-cols">

<a href="https://docs.livekit.io/reference/components/react/component/participantcontext/" target="_blank" class="card no-shadow">Participant</a>
<a href="https://docs.livekit.io/reference/components/react/component/roomcontext/" target="_blank" class="card no-shadow">Room</a>
<a href="https://github.com/livekit/components-js/blob/main/packages/react/src/context/chat-context.ts" target="_blank" class="card no-shadow">Chat</a>
<a href="https://github.com/livekit/components-js/blob/main/packages/react/src/context/feature-context.ts" target="_blank" class="card no-shadow">Feature</a>
<a href="https://docs.livekit.io/reference/components/react/component/layoutcontext/" target="_blank" class="card no-shadow">Layout</a>
<a href="https://github.com/livekit/components-js/blob/main/packages/react/src/context/pin-context.ts" target="_blank" class="card no-shadow">Pin</a>
<a href="https://docs.livekit.io/reference/components/react/component/trackrefcontext/" target="_blank" class="card no-shadow">TrackRef</a>

</div>

## Hooks

Hooks are functions that let you use state and other React features without writing a class. They are functions that let you “hook into” React state and lifecycle features from function components.

React Components provides a set of hooks that you can use to interact with the components and the underlying LiveKit client.

[:octicons-arrow-right-24: See Reference](https://github.com/livekit/components-js/tree/main/packages/react/src/hooks){:target="_blank"}

## Applications

A practical example showcases the potential of React Components is the production-ready flagship application, [**LiveKit Meet**](https://meet.livekit.io/){:target="_blank"}. This application is built using React Components and demonstrates the power and flexibility of the library.

## References

- [React Components](https://docs.livekit.io/reference/components/react/){:target="_blank"}
