# React Components

## Introduction

React Components are the simplest way to create real-time audio/video applications with React. There's no need to manage state or low level events, React Components from LiveKit handle all the complexity for you.

## Featured Components

A curated set of components that we believe are essential and serve as a solid foundation for most applications.

- **LiveKitRoom**

  ______________________________________________________________________

  It provides the Room context to all its children, serving as the root component of your application, and also exposes the Room state through a React context.

  ______________________________________________________________________

  [See Reference](https://docs.livekit.io/reference/components/react/component/livekitroom/)

- **RoomAudioRenderer**

  ______________________________________________________________________

  It manages remote participants' audio tracks and ensures that microphones and screen sharing are audible. It also provides a way to control the volume of each participant.

  ______________________________________________________________________

  [See Reference](https://docs.livekit.io/reference/components/react/component/roomaudiorenderer/)

- **TrackLoop**

  ______________________________________________________________________

  Provides an easy way to loop through all participant camera and screen tracks. For each track, TrackLoop creates a TrackRefContext that you can use to render the track.

  ______________________________________________________________________

  [See Reference](https://docs.livekit.io/reference/components/react/component/trackloop/)

## Prefabricated Components

Prefabricated are constructed using components and enhanced with additional functionalities, unique styles, and practical defaults. They are designed for immediate use and are not meant to be extended.

[AudioConference](https://docs.livekit.io/reference/components/react/component/audioconference/) [Chat](https://docs.livekit.io/reference/components/react/component/chat/) [ControlBar](https://docs.livekit.io/reference/components/react/component/controlbar/) [MediaDeviceMenu](https://docs.livekit.io/reference/components/react/component/mediadevicemenu/) [PreJoin](https://docs.livekit.io/reference/components/react/component/prejoin/) [VideoConference](https://docs.livekit.io/reference/components/react/component/videoconference/)

## Contexts

Contexts are used to allow child components to access parent state without having to pass it down the component tree via props

[Participant](https://docs.livekit.io/reference/components/react/component/participantcontext/) [Room](https://docs.livekit.io/reference/components/react/component/roomcontext/) [Chat](https://github.com/livekit/components-js/blob/main/packages/react/src/context/chat-context.ts) [Feature](https://github.com/livekit/components-js/blob/main/packages/react/src/context/feature-context.ts) [Layout](https://docs.livekit.io/reference/components/react/component/layoutcontext/) [Pin](https://github.com/livekit/components-js/blob/main/packages/react/src/context/pin-context.ts) [TrackRef](https://docs.livekit.io/reference/components/react/component/trackrefcontext/)

## Hooks

Hooks are functions that let you use state and other React features without writing a class. They are functions that let you “hook into” React state and lifecycle features from function components.

React Components provides a set of hooks that you can use to interact with the components and the underlying LiveKit client.

[See Reference](https://github.com/livekit/components-js/tree/main/packages/react/src/hooks)

## Applications

A practical example showcases the potential of React Components is the production-ready flagship application, [**LiveKit Meet**](https://meet.livekit.io/) . This application is built using React Components and demonstrates the power and flexibility of the library.

## References

- [React Components](https://docs.livekit.io/reference/components/react/)
