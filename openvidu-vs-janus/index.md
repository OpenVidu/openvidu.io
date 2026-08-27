# OpenVidu vs Janus

**Janus isn't a competing platform** — it's a general-purpose, plugin-based WebRTC gateway from Meetecho, comparable in spirit to [mediasoup](https://openvidu.io/openvidu-vs-mediasoup/index.md) but broader in scope: its plugins cover conferencing, SIP gateways, streaming and more, not conferencing rooms alone. If you're evaluating "build directly on Janus" against "use OpenVidu," here's exactly what Janus leaves for you to build yourself, and what OpenVidu already built on its own stack.

[Get started with Platform](https://openvidu.io/latest/docs/index.md) [Compare with a full platform instead](https://openvidu.io/openvidu-vs-jitsi/index.md)

## What Janus gives you

Janus follows a **core-plus-plugins** design: the core handles WebRTC session setup and JSON message exchange with browsers, while server-side plugins implement everything else. Its own docs are explicit that the core provides *"no functionality per se other than implementing the means to set up a WebRTC media communication."*

That said, Janus ships more out of the box than a bare media engine:

- The **VideoRoom plugin** provides an actual multistream SFU room concept — closer to a room primitive than mediasoup's raw Workers/Routers/Transports, though still far short of a full platform (see below).
- Multiple transport bindings are bundled: REST/HTTP, WebSockets, RabbitMQ, MQTT and Unix sockets.
- An **Admin/Monitor API**, authenticated via JWT or HTTP Basic Auth, for inspecting sessions and handles at the media level.
- Recording at the plugin level: VideoRoom can dump raw per-user audio/video tracks to `.mjr` files.

## What you'd still build yourself

- **No application-level authentication.** The Admin/Monitor API has its own auth, but nothing protects your actual conferencing rooms — that's your signaling layer's job to build.
- **No managed recording pipeline.** VideoRoom's `.mjr` dumps are raw per-track files; turning them into a normal video file needs the separate `janus-pp-rec` post-processing tool, run by you.
- **No S3 or other managed storage** for whatever recordings you produce.
- **No admin dashboard.** The Admin/Monitor API is programmatic only — third-party community dashboards exist, but nothing official ships with the project.
- **No official native mobile SDKs.** Only community-maintained wrappers are available for iOS and Android.
- **No cross-instance clustering.** Each Janus instance is standalone; running several behind a single conferencing experience is your own load-balancing and signaling design.
- **A copyleft license to account for.** Janus is GPL v3, worth checking against your own project's licensing model before you build on it (Meetecho also sells a commercial license if GPL doesn't fit).

## OpenVidu already built all of this — on top of its own stack

|                    | **OpenVidu**                                                                                                                                | **Janus**                                             |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| License            | Apache 2.0**COMMUNITY** / commercial**PRO**                                                                                                 | GPL v3 (commercial license available)                 |
| Room/session model | [Bundled](https://openvidu.io/latest/docs/reference/room-service-api/#rooms)                                                                   | Basic, via the VideoRoom plugin only                  |
| Authentication     | [JWT tokens with grants](https://openvidu.io/latest/docs/reference/access-tokens/#video-grants), bundled                                       | Not provided for application rooms                    |
| Recording (Egress) | [Bundled](https://openvidu.io/latest/docs/reference/egress/index.md), S3-compatible storage                                                    | Raw `.mjr` dumps, manual post-processing              |
| Server/REST API    | Full [server API](https://openvidu.io/latest/docs/reference/room-service-api/index.md)                                                         | Admin/Monitor API only (session-level, not app-level) |
| Webhooks           | Bundled [event set](https://openvidu.io/latest/docs/reference/webhooks/#events)                                                                | None                                                  |
| Dashboard          | [OpenVidu Dashboard](https://openvidu.io/latest/docs/self-hosting/production-ready/observability/openvidu-dashboard/index.md)                  | None official                                         |
| Client SDKs        | [8 SDKs, including native Android and iOS](https://openvidu.io/latest/docs/tutorials/application-client/index.md)                              | Community-maintained only                             |
| Clustering         | [One-click automated deployment](https://openvidu.io/latest/docs/self-hosting/deployment-types/index.md) with autoscaling on 5 cloud providers | Your own orchestration across standalone instances    |

## When raw Janus is still the right call

To be fair about it: Janus's plugin ecosystem reaches further than conferencing rooms alone — SIP gateway integrations (although that's also possible through [LiveKit's SIP API](https://docs.livekit.io/reference/telephony/sip-api/) ), one-to-many streaming, and other topologies its plugins already cover. Teams building one of those use cases, or something custom enough that a room-centric platform like OpenVidu doesn't fit, get real value from working directly with Janus's core-plus-plugins design.

For those specific cases, building on Janus is the right call, as long as you accept the GPL licensing and the list above as work you're signing up to own. For most teams building a standard real-time video application, that's a lot of platform to build on top of a gateway, when OpenVidu already ships it.

## Frequently asked questions

### Is Janus a competitor to OpenVidu?

Not directly — Janus is a general-purpose WebRTC gateway, not a finished platform. Its VideoRoom plugin provides a basic multistream SFU room, but signaling design, authentication, managed recording, a REST API and a dashboard are left for the integrating application to build. OpenVidu is a full platform where all of that is already built.

### Does OpenVidu use Janus?

No. OpenVidu is a fork of LiveKit that uses Pion or mediasoup as its media engine, not Janus. Janus is an independent project from Meetecho with its own plugin architecture.

### What license is Janus released under?

Janus is released under the GNU GPL v3, with a commercial license available from Meetecho for teams that don't want GPL's copyleft obligations. This is a real practical difference from OpenVidu **COMMUNITY**'s Apache 2.0 license, worth checking against your own project's licensing requirements before you build on it.

### Can I use Janus directly instead of a platform?

Yes, and for teams building something beyond a standard video-conferencing room — a custom SIP gateway, a broadcast/streaming topology, or another use case covered by Janus's plugin ecosystem — it can be the right call. Go in aware of the scope: you're also taking on authentication, room persistence beyond VideoRoom's basics, managed recording, a REST API, a dashboard, and native mobile SDKs yourself.

[Start with a tutorial](https://openvidu.io/latest/docs/tutorials/application-server/index.md)

## Weighing a DIY Janus build against a ready platform?

Tell us what you are building and we will help you scope the tradeoffs.

[Talk to an expert](https://openvidu.io/support/#talk-to-an-expert)
