# Developing your OpenVidu application

Here's a high-level overview of the steps involved in building an OpenVidu application:

1. **Launch an OpenVidu deployment**
2. **Use LiveKit Server SDK in your application server**
3. **Build the UI of your client application**
4. **Deploy OpenVidu and your application**

## 1. Launch an OpenVidu deployment

The quickest way is to use [OpenVidu local deployment](../self-hosting/local.md).

## 2. Use LiveKit Server SDK in your application server

OpenVidu is fully compatibly with LiveKit APIs. This means that any LiveKit Server SDK can be used in your application server.

The only mandatory task to perform in your application server is:

- **Creating access tokens**. Your Participants will only be able to connect to your Rooms by using a valid access token. Visit the official documentation about [Authentication](https://docs.livekit.io/home/get-started/authentication/){target="\_blank"} to learn how to generate access tokens and which permissions you can assign to them.

There are also other optional tasks that you can perform from your application server, depending on your requirements:

- **Manage your Rooms and Participants**: although most of your application logic will be in the frontend, you can also manage the logic of your Rooms and Participants from the security of your application backend. You can list, create, update and destroy Rooms and Participants. This is the official LiveKit documentation with all the available methods of the **[`RoomServiceClient`](https://docs.livekit.io/reference/server/server-apis/#RoomService-APIs){target="\_blank"}** exposed by the Server API. These methods are also available in all LiveKit Server SDKs.
- **Manage Egress and Ingress**: if your application needs some kind of recording, broadcasting or media ingestion, this operations must all be performed by your application server.
- **Receive Webhook events**: you can also listen to Webhook events in your application backend. In this way you can react to events happening in your Rooms: a Room has started, a Room has finished, a Participant has joined a Room, a Track has been published... Visit the official documentation about [Webhooks](https://docs.livekit.io/realtime/server/webhooks/){target="\_blank"}.
- **Publish Tracks from your backend**: this is only for advanced applications that require server-side media publishing. Publishing media from your backend is possible by using [LiveKit CLI](https://github.com/livekit/livekit-cli){target="\_blank"}, [Python SDK](https://github.com/livekit/python-sdks){target="\_blank"}, [Go SDK](https://pkg.go.dev/github.com/livekit/server-sdk-go){target="\_blank"}, [Node SDK](https://github.com/livekit/node-sdks){target="\_blank"} or [Rust SDK](https://github.com/livekit/rust-sdks){target="\_blank"}.

To get you started, here is a list of all available LiveKit Server SDKs and an application server tutorial using them. These tutorials are all set up to **generate access tokens** and **receive webhook events**, so they are perfect starting points for your application server.

=== ":simple-nodedotjs:{.icon .lg-icon .tab-icon} Node"

    [:octicons-arrow-right-24: Node Tutorial](../tutorials/application-server/node.md)

    [:octicons-arrow-right-24: Reference Docs](https://docs.livekit.io/server-sdk-js/){target="\_blank"}

=== ":simple-goland:{.icon .lg-icon .tab-icon} Go"

    [:octicons-arrow-right-24: Go Tutorial](../tutorials/application-server/go.md)

    [:octicons-arrow-right-24: Reference Docs](https://pkg.go.dev/github.com/livekit/server-sdk-go){target="\_blank"}

=== ":simple-ruby:{.icon .lg-icon .tab-icon} Ruby"

    [:octicons-arrow-right-24: Ruby Tutorial](../tutorials/application-server/ruby.md)

    [:octicons-arrow-right-24: GitHub Repository](https://github.com/livekit/server-sdk-ruby){target="\_blank"}

=== ":fontawesome-brands-java:{.icon .lg-icon .tab-icon} Java"

    [:octicons-arrow-right-24: Java Tutorial](../tutorials/application-server/java.md)

    [:octicons-arrow-right-24: GitHub Repository](https://github.com/livekit/server-sdk-kotlin){target="\_blank"}

=== ":simple-python:{.icon .lg-icon .tab-icon} Python"

    [:octicons-arrow-right-24: Python Tutorial](../tutorials/application-server/python.md)

    [:octicons-arrow-right-24: GitHub Repository](https://github.com/livekit/python-sdks){target="\_blank"}

=== ":simple-rust:{.icon .lg-icon .tab-icon} Rust"

    [:octicons-arrow-right-24: Rust Tutorial](../tutorials/application-server/rust.md)

    [:octicons-arrow-right-24: Reference Docs](https://docs.rs/livekit-api/latest/livekit_api/index.html){target="\_blank"}

=== ":simple-php:{.icon .lg-icon .tab-icon} PHP"

    [:octicons-arrow-right-24: PHP Tutorial](../tutorials/application-server/php.md)

    [:octicons-arrow-right-24: GitHub Repository](https://github.com/agence104/livekit-server-sdk-php){target="\_blank"}

=== ":simple-dotnet:{.icon .lg-icon .tab-icon} .NET"

    [:octicons-arrow-right-24: .NET Tutorial](../tutorials/application-server/dotnet.md)

    > There is no .NET SDK for LiveKit available. Visit the tutorial to learn how to create tokens and receive Webhook events directly from your .NET application server.

=== ":material-api:{.icon .lg-icon .tab-icon} Server API"

    If your backend technology does not have its own SDK, you have two different options:
    
    1. Consume the Server API directly: [:octicons-arrow-right-24: Reference Docs](https://docs.livekit.io/reference/server/server-apis/){target="\_blank"}

    2. Use the livekit-cli: [:octicons-arrow-right-24: GitHub Repository](https://github.com/livekit/livekit-cli){target="\_blank"}

## 3. Build the UI of your client application

There are two main strategies to build the UI of your client application:

- **Use a high-level UI Components library**: you can use [Angular Components](../ui-components/angular-components.md) and [React Components](../ui-components/react-components.md) to quickly set up your UI with building blocks that manage the events and state of the Room for you.
- **Use a low-level client SDK**: if you want extensive control and maximum flexibility when designing your UI, use any of the [LiveKit Client SDKs](https://docs.livekit.io/reference/){target="\_blank"}.

The table below summarizes the key differences between these two strategies to help you make an informed decision:

|  | UI Components  | Low-level client SDKs  |
|------|--------------------|----------------------------------------------------------|
| **What is it?** | Frontend libraries offering videoconferencing components to build your own application. There are [Angular Components](../ui-components/angular-components.md) or [React Components](../ui-components/react-components.md) | Integrate OpenVidu from scratch in your web, mobile or desktop application using [LiveKit Client SDKs](https://docs.livekit.io/reference/){target="\_blank"} |
| **Pros** | <ul><li>Very flexible components: adapt, extend or replace any component</li><li>Have your first version running in minutes, work on your customizations from there</li><li>Easily keep your client code up to date with the latest features</li></ul> | <ul><li>Unlimited level of customization: build your own UI from scratch as you please</li><li>Available for all client platforms: browsers, iOS, Android, Flutter, React Native, Unity...</li></ul> |
| **Cons** | <ul><li>Only available for Angular and React web apps</li></ul>                                                                                                                            | <ul><li>Higher complexity, although there are plenty of tutorials to smooth the learning curve</li></ul>                                                                     |
| **Tutorials** | [Angular Components tutorials](../tutorials/angular-components/index.md) | [Application client tutorials](../tutorials/application-client/index.md) |

Whatever strategy you choose to build the UI of your application, most common steps to perform are:

- **Connect to a Room with an access token**: the application client will connect to a Room with an access token generated by your application server. Once connected, the client becomes a Participant of the Room.
- **Publish Tracks to the Room**: the application client may create Tracks of any kind (audio from the microphone, video from the camera device, screen sharing from an application...) and publish them to the Room.
- **Subscribe to Tracks from other Participants**: the application client may receive the Tracks published by other Participants in the Room. It is possible to perform selective subscription, so the client can choose which Tracks to specifically subscribe to.
- **Mute and unmute Tracks**: the application client may mute and unmute its own Tracks, and also may disable the reception of any Track published by other Participants.

Of course, depending on the use case, this may not be necessary for all users, or other additional steps may need to be taken. For example, in a live streaming application, only presenters will publish Tracks, while all other viewers will only subscribe to them. Or it is possible that users may need exchange messages through a chat. Each specific application will need to refine its use of the UI Components or client SDKs to meet its requirements.

Here is the list of all LiveKit Client SDKs: [LiveKit Client SDKs](https://docs.livekit.io/reference/){target="\_blank"}. Below is a list of application client tutorials, which are perfect starting points for your client application. 

<div class="tutorials-container" markdown>

[:simple-javascript:{.icon .lg-icon .tab-icon} **JavaScript**](../tutorials/application-client/javascript.md){ .md-button .md-button--primary .tutorial-link}

[:simple-react:{.icon .lg-icon .tab-icon} **React**](../tutorials/application-client/react.md){ .md-button .md-button--primary .tutorial-link}

[:simple-angular:{.icon .lg-icon .tab-icon} **Angular**](../tutorials/application-client/angular.md){ .md-button .md-button--primary .tutorial-link}

[:simple-vuedotjs:{.icon .lg-icon .tab-icon} **Vue**](../tutorials/application-client/vue.md){ .md-button .md-button--primary .tutorial-link}

[:simple-electron:{.icon .lg-icon .tab-icon} **Electron**](../tutorials/application-client/electron.md){ .md-button .md-button--primary .tutorial-link}

[:simple-ionic:{.icon .lg-icon .tab-icon} **Ionic**](../tutorials/application-client/ionic.md){ .md-button .md-button--primary .tutorial-link}

</div>

## 4. Deploy OpenVidu and your application

You have different options to deploy OpenVidu in a production-ready environment, depending on the level of scalability, fault tolerance and observability you need. See [Deployment types](../self-hosting/deployment-types.md) for more information.