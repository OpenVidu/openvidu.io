---
title: "Get started with OpenVidu Platform"
description: "Run OpenVidu on your machine, mint an access token from a server and join a room from the browser, in about ten minutes."
---

# Getting started

By the end of this page you will have a video room running entirely on your own machine: OpenVidu in Docker, a small server minting access tokens, and a browser page publishing and subscribing to media. About ten minutes, no account and no cloud.

That is the whole shape of an OpenVidu application, and it does not change when you go to production — only the URL and the credentials do.

<div class="grid cards" markdown>

-   :material-server:{ .lg .middle } **OpenVidu deployment**

    ---

    Routes the media. You run it: locally now, on your own infrastructure later.

-   :material-key:{ .lg .middle } **Your application server**

    ---

    Signs an access token for each participant. The one piece nobody else can do for you, because it is where your authorization rules live.

-   :material-monitor-cellphone:{ .lg .middle } **Your application client**

    ---

    Connects to a room with that token and publishes camera and microphone.

</div>

!!! info "Prerequisites"

    [Docker and Docker Compose :fontawesome-solid-external-link:{.external-link-icon}](https://docs.docker.com/get-started/get-docker/){:target="_blank"}, and [Node.js :fontawesome-solid-external-link:{.external-link-icon}](https://nodejs.org/){:target="_blank"} for the example server on this page. The [application server tutorials](./tutorials/application-server/index.md) cover eight other languages.

## 1. Run OpenVidu locally

--8<-- "tutorials/run-openvidu-locally.md"

Once it is up, open [http://localhost:7880](http://localhost:7880){:target="_blank"}. That page lists every service in the deployment along with its credentials, and it is where you will find:

- **OpenVidu API** — `ws://localhost:7880`, the URL your client connects to.
- **API key / secret** — `devkey` / `secret` in the local deployment.
- [**OpenVidu Dashboard**](http://localhost:7880/dashboard){:target="_blank"} — watch rooms, participants and tracks appear as you build.

Keep the dashboard open in a tab. It is the fastest way to see whether something worked.

For what else the local deployment gives you — including testing from a phone on the same network with real certificates — see [OpenVidu Local installation](./self-hosting/local.md).

## 2. Mint an access token

A client cannot connect to a room with a URL alone: it needs an **access token**, a JWT signed with your API secret that says who the participant is and what they may do. Your application server issues it, which is also where you decide who is allowed into which room.

Create a folder, install the server SDK, and save this as `server.js`:

```bash
npm install livekit-server-sdk express cors
```

```javascript title="server.js"
import express from "express";
import cors from "cors";
import { AccessToken } from "livekit-server-sdk";

const app = express();
app.use(cors());
app.use(express.json());

app.post("/token", async (req, res) => {
  const { roomName, participantName } = req.body;

  const at = new AccessToken("devkey", "secret", { identity: participantName });
  at.addGrant({ roomJoin: true, room: roomName });

  res.json({ token: await at.toJwt() });
});

app.listen(6080, () => console.log("Token server on http://localhost:6080"));
```

```bash
node server.js
```

`roomJoin` and `room` are the only grants this token needs. Publishing and subscribing are allowed unless you turn them off, so a viewer-only participant is the case that needs extra work, not this one.

!!! danger "The API secret stays on the server"

    Never ship it to a browser or a mobile app. Anyone holding it can mint a token for any identity with any permission. Here it is hardcoded because `devkey`/`secret` are throwaway local credentials — in production read them from the environment.

## 3. Join from the browser

Save this as `index.html` next to your server, and serve it however you like — `npx serve` will do:

```html title="index.html"
<!DOCTYPE html>
<html>
  <body>
    <button onclick="join()">Join</button>
    <div id="videos"></div>

    <script type="module">
      import { Room, RoomEvent } from "https://cdn.jsdelivr.net/npm/livekit-client/+esm";

      window.join = async () => {
        const participantName = "user-" + Math.floor(Math.random() * 1000);

        const res = await fetch("http://localhost:6080/token", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ roomName: "my-first-room", participantName }),
        });
        const { token } = await res.json();

        const room = new Room();

        room.on(RoomEvent.TrackSubscribed, (track) => {
          document.getElementById("videos").appendChild(track.attach());
        });

        await room.connect("ws://localhost:7880", token);
        await room.localParticipant.enableCameraAndMicrophone();

        room.localParticipant.videoTrackPublications.forEach((pub) => {
          document.getElementById("videos").appendChild(pub.track.attach());
        });
      };
    </script>
  </body>
</html>
```

Three things are happening: the page asks **your** server for a token, connects to OpenVidu with it, and attaches every track it receives to the page. `TrackSubscribed` fires once per remote track, which is how other participants appear.

## 4. See media flow

Open the page in **two browser tabs** and click Join in both. Each tab publishes its own camera and subscribes to the other's — that is a real two-participant room, with the media routed by the OpenVidu running on your machine.

Now look at the [dashboard](http://localhost:7880/dashboard){:target="_blank"}: one room, two participants, four tracks.

??? question "Nothing appears?"

    - **No video and no error** — the browser blocked camera access. Check the permission prompt; `enableCameraAndMicrophone` fails silently in some browsers when denied.
    - **The token request fails** — the token server is not running, or CORS is blocking it. The server above enables CORS for everything, which is fine locally and not fine in production.
    - **Connection fails** — confirm `docker compose up` is still running and [http://localhost:7880](http://localhost:7880){:target="_blank"} answers.
    - **It works in one tab but not two** — some browsers only hand the camera to one tab at a time. Try one normal tab and one incognito window.

## Where to go next

<div class="grid cards" markdown>

-   **Build the server properly**

    ---

    The same token endpoint plus webhook handling, as a complete working project in nine languages.

    [:octicons-arrow-right-24: Application server tutorials](./tutorials/application-server/index.md)

-   **Build the client properly**

    ---

    React, Angular, Vue, Electron, Ionic, Android and iOS, each a full application rather than a page of script.

    [:octicons-arrow-right-24: Application client tutorials](./tutorials/application-client/index.md)

-   **Look things up**

    ---

    Permissions, room management, recording, screen sharing and the rest, as a cheat sheet.

    [:octicons-arrow-right-24: How to develop your OpenVidu app](./developing-your-openvidu-app/how-to.md)

-   **Go to production**

    ---

    Single Node, Elastic or High Availability, on your own servers or any major cloud.

    [:octicons-arrow-right-24: Deployment types](./self-hosting/deployment-types.md)

</div>

Prefer a finished video conferencing application over building one? [OpenVidu Meet](../meet/index.md) is ready to deploy and embed, and the [comparison](../openvidu-meet-vs-openvidu-platform.md) shows which of the two fits your project.
