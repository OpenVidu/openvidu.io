This section compares OpenVidu to other videoconference/streaming solutions, to better understand what it is, what it is not, and what advantages and disadvantages it may have over them.

## OpenVidu vs LiveKit

First of all, and perhaps the most obvious question, how does OpenVidu differ from LiveKit, and what kind of relationship is there between them? This can be answer with four simple points:

- OpenVidu is a **fork of LiveKit**. It is 100% compatible with LiveKit: any application built for LiveKit is compatible with OpenVidu.
- OpenVidu is a **superset of LiveKit**. It provides all of the open source features of LiveKit and supports all of its SDKs, but it also extends LiveKit with extra features, APIs and internal enhancements, most notably integration with [mediasoup](https://mediasoup.org/){target="\_blank"}.
- OpenVidu is a **production-ready self-hosted solution**. It offers an easy deployment process to self-host a high performance, fault tolerant, scalable and observable cluster. OpenVidu provides an interactive installer that manages all of the complexities, so you can quickly host a production deployment that would otherwise require advanced devops/SRE expertise.
- OpenVidu is a **support team** for self-hosted deployments. The OpenVidu team is made up of real-time experts with over a decade of experience in the field. We specialize in customer support and are always ready to help you bring your ideas to life.

<figure markdown>
  ![OpenVidu vs LiveKit](../assets/images/openvidu-vs-livekit.svg){ .mkdocs-img }
  <figcaption>OpenVidu is a custom fork of LiveKit, 100% compatible in terms of its API and SDKs, with the power of mediasoup at its core. This and other integrations provide improved performance, new features and facilitate the deployment and management of your cluster.</figcaption>
</figure>

LiveKit comes in two flavors: [LiveKit Open Source](https://github.com/livekit/livekit){target="\_blank"} and [LiveKit Cloud](https://docs.livekit.io/home/cloud/){target="\_blank"}.

### OpenVidu <span class="openvidu-tag openvidu-community-tag" style="font-size: .8em">COMMUNITY</span> vs LiveKit Open Source

LiveKit Open Source is probably the most advanced and feature-rich open source WebRTC stack available today. It has a simple but very versatile API design, and has a large collection of SDKs to integrate into your application on both the frontend and backend. Regardless of your technology stack, there is sure to be a LiveKit Open Source SDK available for you! This is why OpenVidu is fully compatible with LiveKit protocols. You can use any LiveKit SDK to build your application, and it will work seamlessly with an OpenVidu deployment.

What does OpenVidu Community bring over LiveKit Open Source?

With OpenVidu Community you get a handful of features on top of LiveKit Open Source that will help with the development of your application:

- **Egress and Ingress services already integrated with a Redis instance**: LiveKit allows you to export media from a Room (for example recording it) or import media into a Room (for example ingesting a video file), using [Egress](https://docs.livekit.io/realtime/egress/overview/){target="_blank"} and [Ingress](https://docs.livekit.io/realtime/ingress/overview/){target="_blank"} services respectively. These modules are independent of LiveKit Server and must be correctly configured and connected via a shared Redis. When running OpenVidu Community you will have all these services properly integrated, so you can focus on developing your app without worrying about anything else.
- **S3 compatible storage for Egress recordings**: OpenVidu Community comes with an S3 compatible storage already configured to store [Egress](https://docs.livekit.io/realtime/egress/overview/){target="_blank"} recordings ([Minio](https://min.io/){target="_blank"}).
- **Administration dashboard to monitor your Rooms**: OpenVidu comes with an administration dashboard that allows you to monitor the status of your Rooms. Not only in real time, but also historically: the number of participants, the number of published tracks, Egress and Ingress processes... This is a great tool to have when developing your app, as it can help spotting issues and debugging your application's logic. [See more](./self-hosting/production-ready/observability/openvidu-dashboard.md).
- **OpenVidu Call**: a fully-fledged videoconference application that you can customize and adapt to your needs. [See more](./openvidu-call/index.md).
- **Powerful and easy to use local development environment**: OpenVidu provides a Docker Compose based deployment designed for development and testing devices on your local network. It comes with automatic certificate management that makes it easy to test mobile devices in your LAN. [See more](./self-hosting/local.md#accessing-your-local-deployment-from-other-devices-on-your-network).

### OpenVidu <span class="openvidu-tag openvidu-pro-tag" style="font-size: .8em">PRO</span> vs LiveKit Open Source

Deploying LiveKit Open Source in production requires devops/SRE experience to operate your own network of media servers, load balance between them, maintain high uptime and monitor the health of your deployment. OpenVidu Pro makes this an easy process, hiding most of the complexities of such an advanced deployment. With OpenVidu Pro you can self-host a fault-tolerant, scalable and observable cluster, while doubling the original LiveKit Open Source performance to handle twice as many media streams with the same hardware.

### OpenVidu <span class="openvidu-tag openvidu-pro-tag" style="font-size: .8em">PRO</span> vs LiveKit Cloud

LiveKit Cloud is the official SaaS solution for LiveKit. They manage the infrastructure, with a pricing model based on the total bandwidth consumed by your application. It offers certain advantages over LiveKit Open Source:

- Analytics and telemetry dashboard. LiveKit Open Source does not export any metrics or logs out-of-the-box.
- Massive Rooms for livestreams, where a theoretically unlimited number of viewers can be established for published tracks. In LiveKit Open Source one Room must fit in a single server. LiveKit Cloud overcomes this limitation with a mesh architecture where one media server can connect to other media servers to distribute the load.

Where does OpenVidu Pro stand in relation to LiveKit Cloud? **OpenVidu Pro aims to deliver the same advanced benefits as LiveKit Cloud, but as a self-hosted solution**. We intend to provide a performant, fault tolerant, scalable and observable cluster that is easy to deploy, configure and administrate in your own infrastructure. For now, OpenVidu Pro brings:

- OpenVidu Pro provides a complete observability stack with Grafana, Loki, Promtail and Mimir, as well as OpenVidu Dashboard to visualize the data. [See more](./self-hosting/production-ready/observability/index.md).
- We are currently working on supporting the same scalability as LiveKit Cloud to support big videoconferences and massive live streams. [See more](./self-hosting/production-ready/scalability.md#big-videoconferences-and-massive-live-streams-working-on-it).

## OpenVidu vs SaaS solutions

This includes many services like [Agora](https://www.agora.io/){target="\_blank"}, [GetStream](https://getstream.io/){target="\_blank"}, [Daily](https://www.daily.co/){target="\_blank"}, [Vonage](https://www.vonage.com/communications-apis/video/){target="\_blank"}, [Jitsi as a Service](https://jaas.8x8.vc/#/){target="\_blank"}, [Whereby](https://whereby.com/){target="\_blank"}, [Zoom SDK](https://developers.zoom.us/docs/video-sdk/){target="\_blank"}, [Dolby Millicast](https://dolby.io/){target="\_blank"}, [Amazon Chime SDK](https://aws.amazon.com/chime/chime-sdk/){target="\_blank"}.

The main difference between OpenVidu and these services is who owns the infrastructure, and where your users' data flows. All these SaaS solutions provide:

- A public endpoint that your application connects to, so all media is routed through their servers.
- Different sets of SDKs to integrate with your application. Some more complete than others, and maybe some low-code options.
- A pricing model usually based on one of this two options: minutes-per-participant or total GBs of bandwidth consumed.

Using a SaaS provider is a great option for some use cases, but not all. **OpenVidu is designed to be self-hosted**. This allows you to have full control over your infrastructure and data, taking the most out of your own resources and complying with the most strict regulations. While having the best features provided by SaaS: scalability, fault tolerance, observability. See [Production ready](self-hosting/production-ready/index.md) for more information.

## OpenVidu vs SFUs

This includes projects such as [Kurento](https://kurento.openvidu.io/){target="\_blank"}, [mediasoup](https://mediasoup.org/){target="\_blank"}, [Pion](https://pion.ly/){target="\_blank"}, [Janus](https://janus.conf.meetecho.com/){target="\_blank"}, [Jitsi Videobridge](https://jitsi.org/jitsi-videobridge/){target="\_blank"} or [Medooze](https://github.com/medooze/media-server){target="\_blank"}.

These are all media servers. More specifically, they fall under the umbrella of the so-called **SFUs** (Selective Forwarding Units): they are able to receive media streams from different clients and *selectively forward* them to other clients, usually without transcoding or mixing the media.

SFUs are generally low-level tools. Using them directly to implement real-time applications requires a deep understanding of signaling protocols, codecs, networking and other low-level concepts. **OpenVidu is a higher-level abstraction compared to SFUs**. It internally uses SFUs to rely the media streams (more specifically [Pion](https://pion.ly/){target="\_blank"} and [mediasoup](https://mediasoup.org/){target="\_blank"}), but hides all complexities to offer a simpler way to develop videoconferencing and live streaming applications.

## OpenVidu vs mediasoup

[mediasoup](https://mediasoup.org/){target="\_blank"} is a [WebRTC SFU](#openvidu-vs-sfus). It is a minimalist media server with a super low level API that allows building custom real-time applications. Compared to other SFUs, mediasoup is well known for its outstanding performance.

OpenVidu uses mediasoup internally to transmit media streams. We have embedded mediasoup as the WebRTC engine right at the core of LiveKit Open Source, which allows OpenVidu to offer the fantastic APIs and SDKs of LiveKit while providing the cutting-edge performance of mediasoup. Learn more about mediasoup integration in section [Performance](./self-hosting/production-ready/performance.md).

## OpenVidu vs Microsoft Teams, Google Meet, Zoom

All these well-known video conferencing tools are final applications that provide little to no customization at all. They are proprietary, closed-source apps designed to be used as-is, and they are not intended to be integrated into other systems.

OpenVidu is inherently different, as it provides a set of APIs and SDKs to integrate real-time video capabilities into your own application. In other words: **with OpenVidu you can easily build your own custom Microsoft Teams, Google Meet or Zoom-like application.** See [Use cases](getting-started.md#use-cases) for some examples of what you can build with OpenVidu.
