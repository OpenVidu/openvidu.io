# Getting started

By the end of this page you will have a video room running entirely on your own machine: OpenVidu in Docker, a small server minting access tokens, and a browser page publishing and subscribing to media. About ten minutes, no account and no cloud.

That is the whole shape of an OpenVidu application, and it does not change when you go to production — only the URL and the credentials do.

- **OpenVidu deployment**

  ______________________________________________________________________

  Routes the media. You run it: locally now, on your own infrastructure later.

- **Your application server**

  ______________________________________________________________________

  Signs an access token for each participant. The one piece nobody else can do for you, because it is where your authorization rules live.

- **Your application client**

  ______________________________________________________________________

  Connects to a room with that token and publishes camera and microphone.

Prerequisites

[Docker and Docker Compose](https://docs.docker.com/get-started/get-docker/) , and [Node.js](https://nodejs.org/) for the example server on this page. The [application server tutorials](https://openvidu.io/3.8/docs/tutorials/application-server/index.md) cover eight other languages.

## 1. Run OpenVidu locally

1. Download OpenVidu

   ```bash
   git clone https://github.com/OpenVidu/openvidu-local-deployment -b 3.8.0
   ```

1. Configure the local deployment

   **Windows**

   ```powershell
   cd openvidu-local-deployment/community
   .\configure_lan_private_ip_windows.bat
   ```

   **macOS**

   ```bash
   cd openvidu-local-deployment/community
   ./configure_lan_private_ip_macos.sh
   ```

   **Linux**

   ```bash
   cd openvidu-local-deployment/community
   ./configure_lan_private_ip_linux.sh
   ```

1. Run OpenVidu

   ```bash
   docker compose up
   ```

Once it is up, open <http://localhost:7880>. That page lists every service in the deployment along with its credentials, and it is where you will find:

- **OpenVidu API** — `ws://localhost:7880`, the URL your client connects to.
- **API key / secret** — `devkey` / `secret` in the local deployment.
- [**OpenVidu Dashboard**](http://localhost:7880/dashboard) — watch rooms, participants and tracks appear as you build.

Keep the dashboard open in a tab. It is the fastest way to see whether something worked.

For what else the local deployment gives you — including testing from a phone on the same network with real certificates — see [OpenVidu Local installation](https://openvidu.io/3.8/docs/self-hosting/local/index.md).

## 2. Mint an access token

A client cannot connect to a room with a URL alone: it needs an **access token**, a JWT signed with your API secret that says who the participant is and what they may do. Your application server issues it, which is also where you decide who is allowed into which room.

Create a folder, install the server SDK, and save this as `server.js`:

```bash
npm install livekit-server-sdk express cors
```

server.js

```javascript
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

The API secret stays on the server

Never ship it to a browser or a mobile app. Anyone holding it can mint a token for any identity with any permission. Here it is hardcoded because `devkey`/`secret` are throwaway local credentials — in production read them from the environment.

## 3. Join from the browser

Save this as `index.html` next to your server, and serve it however you like — `npx serve` will do:

index.html

```html
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

Now look at the [dashboard](http://localhost:7880/dashboard): one room, two participants, four tracks.

Nothing appears?

- **No video and no error** — the browser blocked camera access. Check the permission prompt; `enableCameraAndMicrophone` fails silently in some browsers when denied.
- **The token request fails** — the token server is not running, or CORS is blocking it. The server above enables CORS for everything, which is fine locally and not fine in production.
- **Connection fails** — confirm `docker compose up` is still running and <http://localhost:7880> answers.
- **It works in one tab but not two** — some browsers only hand the camera to one tab at a time. Try one normal tab and one incognito window.

## Where to go next

- **Build the server properly**

  ______________________________________________________________________

  The same token endpoint plus webhook handling, as a complete working project in nine languages.

  [Application server tutorials](https://openvidu.io/3.8/docs/tutorials/application-server/index.md)

- **Build the client properly**

  ______________________________________________________________________

  React, Angular, Vue, Electron, Ionic, Android and iOS, each a full application rather than a page of script.

  [Application client tutorials](https://openvidu.io/3.8/docs/tutorials/application-client/index.md)

- **Look things up**

  ______________________________________________________________________

  Every operation at a glance — tokens, room management, recording, screen sharing — each one linking to its reference page.

  [Common operations](https://openvidu.io/3.8/docs/build-your-app/common-operations/index.md)

- **Go to production**

  ______________________________________________________________________

  Single Node, Elastic or High Availability, on your own servers or any major cloud.

  [Deployment types](https://openvidu.io/3.8/docs/self-hosting/deployment-types/index.md)

Prefer a finished video conferencing application over building one? [OpenVidu Meet](https://openvidu.io/3.8/meet/index.md) is ready to deploy and embed, and the [comparison](https://openvidu.io/openvidu-meet-vs-openvidu-platform/index.md) shows which of the two fits your project.
