---
title: "3 ways to integrate video conferencing into your app"
draft: false
date: 2026-09-04
slug: integrate-video-conferencing-into-your-app
description: "Three ways to add video conferencing to your app with OpenVidu, from embedding OpenVidu Meet to Angular Components and low-level SDKs, with code for each."
cover_image: poster-light.webp
categories:
  - OpenVidu Meet
  - OpenVidu Platform
tags:
  - Angular
  - WebRTC
  - WebComponent
  - Embedded video
  - LiveKit
  - Video Conferencing
  - UI components
authors:
  - juanCarlos
---

# 3 ways to integrate video conferencing into your app with OpenVidu

![Three stacked integration levels, from embedding OpenVidu Meet to Angular Components to low-level SDKs, all running on one self-hosted OpenVidu deployment](/assets/images/blog/YYYY/MM/integrate-video-conferencing-into-your-app/poster-light.webp#only-light "Three ways to integrate video conferencing with OpenVidu")
![Three stacked integration levels, from embedding OpenVidu Meet to Angular Components to low-level SDKs, all running on one self-hosted OpenVidu deployment](/assets/images/blog/YYYY/MM/integrate-video-conferencing-into-your-app/poster-dark.webp#only-dark "Three ways to integrate video conferencing with OpenVidu")

Sooner or later the ticket lands on your board: *"Add video calls to the app"*. The WebRTC part is a solved problem. The question that actually shapes the project is a different one: **how much of the meeting do you want to own?** The buttons, the layout, the media tracks themselves? Or just a `<div>` where a meeting shows up?

There are three ways to integrate video conferencing into your app with OpenVidu, and all of them run on the same self-hosted deployment. You can embed <a href="/meet/embedded/intro/">OpenVidu Meet</a>, a finished meeting UI, with one HTML tag. You can assemble your own meeting screen from <a href="/docs/ui-components/angular-components/">Angular Components</a>. Or you can go down to the <a href="/docs/">OpenVidu Platform</a> SDKs and handle every audio and video track yourself.

<!-- more -->

This post walks through the three, with working code for each, so you can pick the level that fits your product instead of the one you stumbled into.

## One question, three answers

Here is the map before the details. Each level trades control for speed, and the three stack on top of each other: OpenVidu Meet is built with Angular Components, and Angular Components are built on the same client SDK you would use at the lowest level. Whichever one you pick, the media flows through your own OpenVidu deployment.

| | Embed OpenVidu Meet | Angular Components | Low-level SDKs |
|---|---|---|---|
| **What you write** | One HTML tag and a REST call | An Angular template built from prebuilt components | Everything: connection, tracks, layout |
| **What you get** | The complete OpenVidu Meet UI: chat, recording, screen share, virtual backgrounds, captions, E2EE | A working meeting screen you adapt, extend or replace piece by piece | A Room object and its tracks |
| **Customization** | Colors, per-room features, permissions | Any component: toolbar, layout, streams, panels, CSS variables | Unlimited |
| **Platforms** | Web | Angular web apps | Browsers, iOS, Android, Flutter, React Native, Unity... |
| **Product** | [OpenVidu Meet](/meet/index.md) | [OpenVidu Platform](/docs/index.md) | [OpenVidu Platform](/docs/index.md) |

None of this changes what you pay. Both products work in OpenVidu COMMUNITY and OpenVidu PRO, and the [pricing](/pricing.md) depends on the deployment, not on how you integrate.

For the code, we will use one scenario throughout: a **support desk** app where an agent clicks *Start call* and a customer joins. Angular on the front end, Node.js on the back end. Angular is the framework where all three levels are first-party OpenVidu territory; the section near the end covers other frameworks.

## Level 1: embed OpenVidu Meet

This is the fastest path. OpenVidu Meet is a complete video conferencing application, and [OpenVidu Meet Embedded](/meet/embedded/intro.md) puts that application inside yours. On the client you have three ways to show a room: a [direct link](/meet/embedded/reference/direct-link.md), an [iframe](/meet/embedded/reference/iframe.md) or the [`<openvidu-meet>` Web Component](/meet/embedded/reference/webcomponent.md). On the server you have a [REST API](/meet/embedded/reference/rest-api.md) to manage rooms, members, recordings and users, and [webhooks](/meet/embedded/reference/webhooks.md) to react to what happens in them.

### Create the room from your backend

Rooms are created with one authenticated request. The API key comes from the "Embedded" page of the OpenVidu Meet app, and the [local OpenVidu Meet deployment](/meet/deployment/local.md) ships with `meet-api-key` preconfigured. The `config` object toggles the features of this particular room:

```bash
npm install express cors
```

```javascript title="server.js"
import express from "express";
import cors from "cors";

const MEET_URL = process.env.OV_MEET_SERVER_URL || "http://localhost:9080/meet";
const MEET_API_KEY = process.env.OV_MEET_API_KEY || "meet-api-key";

const app = express();
app.use(cors());
app.use(express.json());

app.post("/meetings", async (req, res) => {
  const response = await fetch(`${MEET_URL}/api/v1/rooms`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-API-KEY": MEET_API_KEY },
    body: JSON.stringify({
      roomName: req.body.roomName,
      config: {
        chat: { enabled: true },
        recording: { enabled: false },
        virtualBackground: { enabled: true },
      },
    }),
  });
  const room = await response.json();

  // The moderator link is for your agent; the speaker link goes to the customer
  res.json({
    moderatorUrl: room.access.anonymous.moderator.url,
    speakerUrl: room.access.anonymous.speaker.url,
  });
});

app.listen(6080, () => console.log("Backend on http://localhost:6080"));
```

Both servers in this post use ES modules, so set `"type": "module"` in your `package.json`. The response carries the room's **access links**. Which link you hand to whom decides the role and identity a participant gets: shared anonymous links for moderators and speakers, a login-protected link for OpenVidu Meet users, or a personal link per identified guest. The [Room Access](/meet/features/rooms/access.md) page has the full model, and we covered how to map it to your own users in [3 access models for video conferencing apps](/blog/posts/2026/07/video-conferencing-permissions.md).

### Drop the meeting into your Angular template

Load the Web Component bundle from your deployment once, in `index.html`:

```html title="index.html"
<script src="http://localhost:9080/meet/v1/openvidu-meet.js"></script>
```

Then use `<openvidu-meet>` like any other element. Angular needs `CUSTOM_ELEMENTS_SCHEMA` to accept the unknown tag, and the rest is attribute and event bindings:

```typescript title="meeting.component.ts"
import { Component, CUSTOM_ELEMENTS_SCHEMA, ElementRef, signal, viewChild } from "@angular/core";

@Component({
  selector: "app-meeting",
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  template: `
    @if (roomUrl(); as url) {
      <openvidu-meet
        #meet
        [attr.room-url]="url"
        participant-name="Alice (support)"
        (joined)="onJoined($event)"
        (closed)="roomUrl.set(null)"
      ></openvidu-meet>
      <button (click)="endCall()">End call for everyone</button>
    } @else {
      <button (click)="startCall()">Start call</button>
    }
  `,
})
export class MeetingComponent {
  roomUrl = signal<string | null>(null);
  meet = viewChild<ElementRef<any>>("meet");

  async startCall() {
    const res = await fetch("http://localhost:6080/meetings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ roomName: "Ticket #4821" }),
    });
    const { moderatorUrl } = await res.json();
    this.roomUrl.set(moderatorUrl);
  }

  onJoined(event: Event) {
    const { roomId, participantIdentity } = (event as CustomEvent).detail;
    console.log(`${participantIdentity} joined ${roomId}`);
  }

  endCall() {
    this.meet()?.nativeElement.endMeeting();
  }
}
```

That is the whole integration. The component emits `joined`, `left` and `closed` events, and exposes `leaveRoom()`, `endMeeting()` and `kickParticipant()` as commands, so your app knows what is going on and can act on it. If you cannot use a Web Component, the iframe accepts the same attributes and speaks the same commands and events through `postMessage`. And if you do not need the meeting inside your page at all, the direct link opens the full OpenVidu Meet UI in its own tab, with `leave-redirect-url` to bring the user back.

### What you can customize today, and what is coming

Let's be precise here, because this is where expectations matter. Today, OpenVidu Meet Embedded lets you shape the meeting in these ways:

- **Colors.** Five color slots (main background, main controls, secondary elements, highlights and accents, panels and dialogs) plus a light or dark base. Admins set them from the "Configuration" page, and they apply globally to every room.
- **Features per room.** Chat, captions, virtual backgrounds, end-to-end encryption and recording, with the recording layout, from the room wizard or the `config` object you saw above. The API additionally exposes the recording encoding. Note that an encrypted room cannot be recorded.
- **Access and permissions.** Anonymous links per role, registered users, identified guests, and per-member permission overrides on top of the `Moderator` and `Speaker` roles.
- **Per-participant attributes.** The display name, an E2EE key, a redirect URL on leave, and a recordings-only view.
- **Language.** The interface is translated into ten languages and follows the user's browser.

What you cannot do yet is reshape the meeting UI itself: replace the toolbar, restyle one room differently from another, or place your own components inside the meeting view. More branding and customization options are on the roadmap, and it is an area we are actively working on. If you need that level of control today, keep reading: it is exactly what the next level gives you.

!!! tip "Pick this level when"
    Your use case is a video conferencing one (telehealth, e-learning, customer support, team collaboration), you want recording, chat and screen sharing without building them, and your brand is served by your colors on a proven UI. This is the path we took in [Building a video-enabled CRM with an AI agent](/blog/posts/2026/07/building-a-video-enabled-crm-with-an-ai-agent.md).

## Level 2: Angular Components

One rung down sits the library OpenVidu Meet itself is built with. [Angular Components](/docs/ui-components/angular-components.md) gives you a `<ov-videoconference>` element that renders a complete meeting, plus the ability to adapt, extend or replace any part of it. You get a working screen in minutes and then work on your customizations from there.

The backend changes at this level. You are no longer talking to OpenVidu Meet but to OpenVidu directly, through the LiveKit-compatible server SDK, and the one thing your server must do is mint [access tokens](/docs/reference/access-tokens.md). This same server also serves Level 3:

```bash
npm install express cors livekit-server-sdk
```

```javascript title="server.js"
import express from "express";
import cors from "cors";
import { AccessToken } from "livekit-server-sdk";

const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY || "devkey";
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET || "secret";

const app = express();
app.use(cors());
app.use(express.json());

app.post("/token", async (req, res) => {
  const { roomName, participantName } = req.body;
  const at = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, { identity: participantName });
  at.addGrant({ roomJoin: true, room: roomName });
  res.json({ token: await at.toJwt() });
});

app.listen(6080, () => console.log("Token server on http://localhost:6080"));
```

### Render a meeting

Install the library and its Angular Material dependency, then register it at bootstrap:

```bash
ng add @angular/material
npm install openvidu-components-angular
```

```typescript title="main.ts"
import { bootstrapApplication } from "@angular/platform-browser";
import { importProvidersFrom } from "@angular/core";
import { provideAnimations } from "@angular/platform-browser/animations";
import { OpenViduComponentsModule, OpenViduComponentsConfig } from "openvidu-components-angular";
import { AppComponent } from "./app/app.component";

const config: OpenViduComponentsConfig = { production: true };

bootstrapApplication(AppComponent, {
  providers: [importProvidersFrom(OpenViduComponentsModule.forRoot(config)), provideAnimations()],
});
```

The component asks you for a token when the participant is ready to join. You fetch it from your server and hand it back:

```typescript title="meeting.component.ts"
import { Component } from "@angular/core";
import { OpenViduComponentsModule } from "openvidu-components-angular";

@Component({
  selector: "app-meeting",
  imports: [OpenViduComponentsModule],
  template: `
    <ov-videoconference
      [token]="token"
      [livekitUrl]="LIVEKIT_URL"
      (onTokenRequested)="onTokenRequested($event)"
    ></ov-videoconference>
  `,
})
export class MeetingComponent {
  LIVEKIT_URL = "ws://localhost:7880";
  token!: string;

  async onTokenRequested(participantName: string) {
    const res = await fetch("http://localhost:6080/token", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ roomName: "ticket-4821", participantName }),
    });
    this.token = (await res.json()).token;
  }
}
```

With that you have a prejoin page, a toolbar, a responsive layout, chat, participants and activities panels, screen sharing and the recording controls. Only recording needs a backend hook: the component emits `onRecordingStartRequested` and `onRecordingStopRequested`, and your server starts and stops the Egress, as the [recording tutorial](/docs/tutorials/advanced-features/recording-basic-s3.md) shows. Everything else works with no wiring.

### Make it yours

Customization works at three depths, and you can mix them:

- **CSS variables** for the look. Redefine `--ov-background-color`, `--ov-primary-action-color`, `--ov-accent-action-color`, the border radio and the rest in your global stylesheet, and every component follows.
- **Inputs** for behavior. Attribute directives on `<ov-videoconference>` such as `[prejoin]`, `[participantName]`, `[minimal]` or `[toolbarChatPanelButton]` show, hide and preconfigure parts of the UI.
- **Structural directives** for structure. Put your own markup inside the component with `*ovToolbar`, `*ovLayout`, `*ovStream`, `*ovPanel`, `*ovChatPanel`, `*ovParticipantsPanel` or `*ovAdditionalPanels`, and it replaces the default one while the library keeps managing the room for you.

Our support desk wants to replace the default toolbar with a minimal one: microphone, camera and a "ticket" button. That is one structural directive and one injected service. If you only want to add a button next to the default controls, `*ovToolbarAdditionalButtons` does that without replacing anything:

```typescript title="meeting.component.ts"
import { Component } from "@angular/core";
import { OpenViduComponentsModule, ParticipantService } from "openvidu-components-angular";

@Component({
  selector: "app-meeting",
  imports: [OpenViduComponentsModule],
  template: `
    <ov-videoconference
      [token]="token"
      [livekitUrl]="LIVEKIT_URL"
      (onTokenRequested)="onTokenRequested($event)"
      (onParticipantLeft)="backToTicket()"
    >
      <div *ovToolbar class="support-toolbar">
        <button (click)="toggleMic()">Mic</button>
        <button (click)="toggleCamera()">Camera</button>
        <button (click)="openTicket()">Ticket #4821</button>
      </div>
    </ov-videoconference>
  `,
})
export class MeetingComponent {
  constructor(private participants: ParticipantService) {}

  async toggleMic() {
    await this.participants.setMicrophoneEnabled(!this.participants.isMyMicrophoneEnabled());
  }

  async toggleCamera() {
    await this.participants.setCameraEnabled(!this.participants.isMyCameraEnabled());
  }

  // token, LIVEKIT_URL and onTokenRequested() as in the previous snippet;
  // openTicket() and backToTicket() navigate within your app
}
```

Every piece you do not replace keeps working and keeps receiving improvements with each OpenVidu release. The [Angular Components tutorials](/docs/tutorials/angular-components/index.md) walk through each directive one at a time: custom toolbar, extra buttons, custom layout, custom stream, custom panels, an admin dashboard and more.

!!! tip "Pick this level when"
    You want your own meeting screen inside an Angular app, you want it working this week, and you would rather customize a proven UI than write one. It is also the natural next step when Level 1 stops being enough.

## Level 3: low-level SDKs

At the bottom of the stack there is no UI at all, just a `Room` and its tracks. OpenVidu is a fork of LiveKit that keeps 100% API compatibility, so any [LiveKit client SDK :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/){:target="_blank"} works unchanged against your deployment. For a browser that is `livekit-client`:

```bash
npm install livekit-client
```

The token server from Level 2 is all the backend you need. Your client asks for a token, connects, publishes camera and microphone, and renders whatever tracks other participants publish. Here is the whole loop in Angular, with signals holding the state:

```typescript title="meeting.component.ts"
import { Component, signal } from "@angular/core";
import { LocalVideoTrack, RemoteTrack, Room, RoomEvent, Track } from "livekit-client";
import { TrackViewComponent } from "./track-view.component";

@Component({
  selector: "app-meeting",
  imports: [TrackViewComponent],
  template: `
    @if (localTrack(); as track) {
      <track-view [track]="track" />
    }
    @for (remote of remoteTracks(); track remote.sid) {
      <track-view [track]="remote" />
    }
    <button (click)="join()">Join</button>
    <button (click)="leave()">Leave</button>
  `,
})
export class MeetingComponent {
  private room?: Room;
  localTrack = signal<LocalVideoTrack | undefined>(undefined);
  remoteTracks = signal<RemoteTrack[]>([]);

  async join() {
    const room = new Room();
    this.room = room;

    room.on(RoomEvent.TrackSubscribed, (track) => {
      this.remoteTracks.update((tracks) => [...tracks, track]);
    });
    room.on(RoomEvent.TrackUnsubscribed, (track) => {
      this.remoteTracks.update((tracks) => tracks.filter((t) => t.sid !== track.sid));
    });

    const token = await this.getToken("ticket-4821", "Alice");
    await room.connect("ws://localhost:7880", token);
    await room.localParticipant.enableCameraAndMicrophone();

    const camera = room.localParticipant.getTrackPublication(Track.Source.Camera);
    this.localTrack.set(camera?.videoTrack);
  }

  async leave() {
    await this.room?.disconnect();
    this.localTrack.set(undefined);
    this.remoteTracks.set([]);
  }

  private async getToken(roomName: string, participantName: string) {
    const res = await fetch("http://localhost:6080/token", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ roomName, participantName }),
    });
    return (await res.json()).token as string;
  }
}
```

Rendering a track means attaching it to a `<video>` or `<audio>` element. A small component takes care of both kinds and detaches on destroy:

```typescript title="track-view.component.ts"
import { AfterViewInit, Component, ElementRef, OnDestroy, input, viewChild } from "@angular/core";
import { Track } from "livekit-client";

@Component({
  selector: "track-view",
  template: `
    @if (track().kind === Track.Kind.Video) {
      <video #media autoplay playsinline></video>
    } @else {
      <audio #media autoplay></audio>
    }
  `,
})
export class TrackViewComponent implements AfterViewInit, OnDestroy {
  protected readonly Track = Track;
  track = input.required<Track>();
  media = viewChild.required<ElementRef<HTMLMediaElement>>("media");

  ngAfterViewInit() {
    this.track().attach(this.media().nativeElement);
  }

  ngOnDestroy() {
    this.track().detach();
  }
}
```

Notice what is *not* here: no prejoin page, no toolbar, no layout, no chat. You decide whether a participant publishes or only subscribes, which tracks to render and where, what a "mute" button does. The four operations every client performs, connecting with a token, publishing tracks, subscribing to tracks and muting them, are the same across every SDK, and the [client SDK reference](/docs/reference/client-sdk.md) documents the shared model.

Two things open up at this level that the other two do not offer. First, **platforms**: the same code shape works in iOS, Android, Flutter, React Native, Unity and even embedded devices, and the [application client tutorials](/docs/tutorials/application-client/index.md) cover eight platforms, from plain JavaScript to Android and iOS. Second, **use cases beyond meetings**: live streaming to thousands of viewers, ingesting IP cameras or RTMP feeds, server-side recording with custom layouts, telephony, and AI agents that join a room as participants. OpenVidu Meet and Angular Components are built around rooms and meetings; the SDKs are built around tracks.

!!! tip "Pick this level when"
    Your UI is not a meeting grid, you need native mobile or desktop clients, you need control over codecs, bitrates and subscriptions, or video conferencing is only one part of a larger real-time product.

## Not on Angular?

The three levels exist for other stacks too, with one honest caveat in the middle:

- **Level 1** is framework-agnostic. `<openvidu-meet>` is a standard custom element, so it drops into React, Vue, Svelte or a server-rendered page the same way. In React it is one line: `<openvidu-meet room-url={roomUrl} />`. The iframe and the direct link cover everything else, including apps that cannot load third-party scripts.
- **Level 2** in React means LiveKit's own [React Components](/docs/ui-components/react-components.md), which our docs list under UI Components. `<LiveKitRoom>` with a `<VideoConference>` inside gets you a prebuilt meeting, and hooks and contexts let you build your own. It is a solid library, but it is LiveKit's, not ours, so the theming, the directive-style slots and the "OpenVidu Meet is built with this" story apply to Angular only.
- **Level 3** has tutorials for JavaScript, React, Angular, Vue, Electron, Ionic, Android and iOS on the client, and Node.js, Go, Ruby, Java, Python, Rust, PHP and .NET for the [token server](/docs/tutorials/application-server/index.md). Any client works with any server.

## Which level should you pick?

If you are still torn about how to integrate video conferencing into your app, three rules of thumb from the projects we have seen:

- **Start as high as your requirements allow.** If a meeting with chat, recording and screen sharing is what your users need, Level 1 gets you there in an afternoon and keeps you on OpenVidu Meet's release train for free. You can always move down later; nobody moves up.
- **Move down when the UI, not the media, is the blocker.** The moment you need a toolbar button that does not exist or a layout Meet does not have, Level 2 gives you exactly that without touching a single track.
- **Go to the bottom when the product is not a meeting.** Live streaming, robotics, AI pipelines and native apps are Level 3 by definition, and there the SDKs are a feature, not a cost.

You do not have to choose once for the whole product either. Both products share a deployment, so a telehealth platform can embed OpenVidu Meet for consultations and use the SDKs for a one-way waiting-room stream. The [Meet vs Platform comparison](/openvidu-meet-vs-openvidu-platform.md) has the side-by-side table, and [OpenVidu Meet vs OpenVidu Platform in 2026](/blog/posts/2026/06/meet-vs-platform.md) goes deeper into why we split the two products in the first place.

## Need more than this?

**Try all three against one OpenVidu Local deployment this afternoon.** [OpenVidu Local](/docs/self-hosting/local.md) is a `git clone` and a `docker compose up`, and it ships both the LiveKit-compatible API on port 7880, with the `devkey` and `secret` credentials the snippets above use, and OpenVidu Meet on port 9080. The developer page at `http://localhost:7880` lists every service with its credentials. Point the three snippets at it and feel the difference yourself. Then go deeper:

- [OpenVidu Meet Embedded step-by-step guide](/meet/embedded/step-by-step-guide.md) and the progressive [Meet tutorials](/meet/embedded/tutorials/index.md), from direct links to webhooks.
- [Angular Components tutorials](/docs/tutorials/angular-components/index.md), one per customizable piece.
- [Build your app](/docs/build-your-app/index.md) and the [Getting started](/docs/getting-started.md) page for the SDK path.
- [Deployment types](/docs/self-hosting/deployment-types.md) when you are ready to leave `localhost`: Single Node, Elastic or High Availability, on your servers or any major cloud.
