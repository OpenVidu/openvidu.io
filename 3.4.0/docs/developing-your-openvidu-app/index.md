# Developing your OpenVidu application

Here's a high-level overview of the steps involved in building an OpenVidu application:

1. **Launch an OpenVidu deployment**
1. **Use LiveKit Server SDK in your application server**
1. **Build the UI of your client application**
1. **Deploy OpenVidu and your application**

## 1. Launch an OpenVidu deployment

The quickest way is to use [OpenVidu local deployment](../self-hosting/local/).

If you feel like it, you can directly launch a production-ready deployment on **AWS**, **Azure** or **your own servers**. Check out the different options at [Deployment types](../self-hosting/deployment-types/).

## 2. Use LiveKit Server SDK in your application server

OpenVidu is fully compatibly with LiveKit APIs. This means that any LiveKit Server SDK can be used in your application server.

The only mandatory task to perform in your application server is:

- **Creating access tokens**. Your Participants will only be able to connect to your Rooms by using a valid access token. Visit the official documentation about [Authentication](https://docs.livekit.io/home/get-started/authentication/) to learn how to generate access tokens and which permissions you can assign to them.

There are other optional tasks that you can perform from your application server, depending on your requirements:

- **Manage your Rooms and Participants**: although most of your application logic will be in the frontend, you can also manage the logic of your Rooms and Participants from the security of your application backend. You can list, create, update and destroy Rooms and Participants. This is the official LiveKit documentation with all the available methods of the **[`RoomServiceClient`](https://docs.livekit.io/reference/server/server-apis/#RoomService-APIs)** exposed by the Server API. These methods are also available in all LiveKit Server SDKs.
- **Manage Egress and Ingress**: if your application needs some kind of recording, broadcasting or media ingestion, this operations must all be performed by your application server.
- **Receive Webhook events**: you can also listen to Webhook events in your application backend. In this way you can react to events happening in your Rooms: a Room has started, a Room has finished, a Participant has joined a Room, a Track has been published... Visit the official documentation about [Webhooks](https://docs.livekit.io/home/server/webhooks/) .
- **Publish Tracks from your backend**: this is only for advanced applications that require server-side media publishing. Publishing media from your backend is possible by using [LiveKit CLI](https://github.com/livekit/livekit-cli) , [Python SDK](https://github.com/livekit/python-sdks) , [Go SDK](https://pkg.go.dev/github.com/livekit/server-sdk-go) , [Node.js SDK](https://github.com/livekit/node-sdks) or [Rust SDK](https://github.com/livekit/rust-sdks) .

To get you started, here is a list of all available LiveKit Server SDKs and an application server tutorial using them. These tutorials are all set up to **generate access tokens** and **receive webhook events**, so they are perfect starting points for your application server.

[Node.js Tutorial](../tutorials/application-server/node/)

[Reference Docs](https://docs.livekit.io/server-sdk-js/)

[Go Tutorial](../tutorials/application-server/go/)

[Reference Docs](https://pkg.go.dev/github.com/livekit/server-sdk-go)

[Ruby Tutorial](../tutorials/application-server/ruby/)

[GitHub Repository](https://github.com/livekit/server-sdk-ruby)

[Java Tutorial](../tutorials/application-server/java/)

[GitHub Repository](https://github.com/livekit/server-sdk-kotlin)

[Python Tutorial](../tutorials/application-server/python/)

[GitHub Repository](https://github.com/livekit/python-sdks)

[Rust Tutorial](../tutorials/application-server/rust/)

[Reference Docs](https://docs.rs/livekit-api/latest/livekit_api/index.html)

[PHP Tutorial](../tutorials/application-server/php/)

[GitHub Repository](https://github.com/agence104/livekit-server-sdk-php)

[.NET Tutorial](../tutorials/application-server/dotnet/)

[GitHub Repository](https://github.com/pabloFuente/livekit-server-sdk-dotnet)

If your backend technology does not have its own SDK, you have two different options:

1. Consume the Server API directly: [Reference Docs](https://docs.livekit.io/reference/server/server-apis/)
1. Use the livekit-cli: [GitHub Repository](https://github.com/livekit/livekit-cli)

## 3. Build the UI of your client application

There are two main strategies to build the UI of your client application:

- **Use a high-level UI Components library**: you can use [Angular Components](../ui-components/angular-components/) and [React Components](../ui-components/react-components/) to quickly set up your UI with building blocks that manage the events and state of the Room for you.
- **Use a low-level client SDK**: if you want extensive control and maximum flexibility when designing your UI, use any of the [LiveKit Client SDKs](https://docs.livekit.io/reference/) .

The table below summarizes the key differences between these two strategies to help you make an informed decision:

|                 | UI Components                                                                                                                                                                                                              | Low-level client SDKs                                                                                                                                                          |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **What is it?** | Frontend libraries offering videoconferencing components to build your own application. There are [Angular Components](../ui-components/angular-components/) or [React Components](../ui-components/react-components/)     | Integrate OpenVidu from scratch in your web, mobile or desktop application using [LiveKit Client SDKs](https://docs.livekit.io/reference/)                                     |
| **Pros**        | - Very flexible components: adapt, extend or replace any component - Have your first version running in minutes, work on your customizations from there - Easily keep your client code up to date with the latest features | - Unlimited level of customization: build your own UI from scratch as you please - Available for all client platforms: browsers, iOS, Android, Flutter, React Native, Unity... |
| **Cons**        | - Only available for Angular and React web apps                                                                                                                                                                            | - Higher complexity, although there are plenty of tutorials to smooth the learning curve                                                                                       |
| **Tutorials**   | [Angular Components tutorials](../tutorials/angular-components/)                                                                                                                                                           | [Application client tutorials](../tutorials/application-client/)                                                                                                               |

Whatever strategy you choose to build the UI of your application, most common steps to perform are:

- **Connect to a Room with an access token**: the application client will connect to a Room with an access token generated by your application server. Once connected, the client becomes a Participant of the Room.
- **Publish Tracks to the Room**: the application client may create Tracks of any kind (audio from the microphone, video from the camera device, screen sharing from an application...) and publish them to the Room.
- **Subscribe to Tracks from other Participants**: the application client may receive the Tracks published by other Participants in the Room. It is possible to perform selective subscription, so the client can choose which Tracks to specifically subscribe to.
- **Mute and unmute Tracks**: the application client may mute and unmute its own Tracks, and also may disable the reception of any Track published by other Participants.

Of course, depending on the use case, this may not be necessary for all users, or other additional steps may need to be taken. For example, in a live-streaming application, only presenters will publish Tracks, while all other viewers will only subscribe to them. Or it is possible that users may need exchange messages through a chat. Each specific application will need to refine its use of the UI Components or client SDKs to meet its requirements.

Here is the list of all LiveKit Client SDKs: [LiveKit Client SDKs](https://docs.livekit.io/reference/) . Below is a list of application client tutorials, which are perfect starting points for your client application.

[**JavaScript**](../tutorials/application-client/javascript/)

[**React**](../tutorials/application-client/react/)

[**Angular**](../tutorials/application-client/angular/)

[**Vue**](../tutorials/application-client/vue/)

[**Electron**](../tutorials/application-client/electron/)

[**Ionic**](../tutorials/application-client/ionic/)

[**Android**](../tutorials/application-client/android/)

[**iOS**](../tutorials/application-client/ios/)

## 4. Deploy OpenVidu and your application

You have different options to deploy OpenVidu in a production-ready environment, depending on the level of scalability, fault tolerance and observability you need. See [Deployment types](../self-hosting/deployment-types/) for more information.
