# Node

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/master/application-server/node){ .md-button target=\_blank }

This is a minimal server application built for Node with [Express](https://expressjs.com/){:target="\_blank"} that allows:

- Generating LiveKit tokens on demand for any [application client](../application-client/index.md).
- Receiving LiveKit [webhook events](https://docs.livekit.io/realtime/server/webhooks/){target=\_blank}.

It internally uses [LiveKit JS SDK](https://docs.livekit.io/server-sdk-js){:target="\_blank"}.

## Running this application

Download the tutorial code:

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git
```

--8<-- "docs/docs/tutorials/shared/node.md"

!!! info

    You can run any [Application Client](../application-client/index.md) to test against this server right away.

## Understanding the code

The application is a simple Express app with a single file `index.js` that exports two endpoints:

- `/token` : generate a token for a given Room name and Participant name.
- `/webhook` : receive LiveKit webhook events.

Let's see the code of the `index.js` file:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/node/index.js#L1-L14' target='_blank'>index.js</a>" linenums="1"
import "dotenv/config";
import express from "express";
import cors from "cors";
import { AccessToken, WebhookReceiver } from "livekit-server-sdk"; // (1)!

const SERVER_PORT = process.env.SERVER_PORT || 6080; // (2)!
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY || "devkey"; // (3)!
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET || "secret"; // (4)!

const app = express(); // (5)!

app.use(cors()); // (6)!
app.use(express.json()); // (7)!
app.use(express.raw({ type: "application/webhook+json" })); // (8)!
```

1. Import `AccessToken` from `livekit-server-sdk`.
2. The port where the application will be listening.
3. The API key of LiveKit Server.
4. The API secret of LiveKit Server.
5. Initialize the Express application.
6. Enable CORS support.
7. Enable JSON body parsing for the `/token` endpoint.
8. Enable raw body parsing for the `/webhook` endpoint.

The `index.js` file imports the required dependencies and loads the necessary environment variables:

- `SERVER_PORT`: the port where the application will be listening.
- `LIVEKIT_API_KEY`: the API key of LiveKit Server.
- `LIVEKIT_API_SECRET`: the API secret of LiveKit Server.

It also initializes the `WebhookReceiver` object that will help validating and decoding incoming [webhook events](https://docs.livekit.io/realtime/server/webhooks/){target=\_blank}.

Finally the `express` application is initialized. CORS is allowed, JSON body parsing is enabled for the `/token` endpoint and raw body parsing is enabled for the `/webhook` endpoint.

---

#### Create token

The endpoint `/token` accepts `POST` requests with a payload of type `application/json`, containing the following fields:

- `roomName`: the name of the Room where the user wants to connect.
- `participantName`: the name of the participant that wants to connect to the Room.

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/node/index.js#L16-L31' target='_blank'>index.js</a>" linenums="16"
app.post("/token", async (req, res) => {
  const roomName = req.body.roomName;
  const participantName = req.body.participantName;

  if (!roomName || !participantName) {
    res.status(400).json({ errorMessage: "roomName and participantName are required" });
    return;
  }

  const at = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, { // (1)!
    identity: participantName,
  });
  at.addGrant({ roomJoin: true, room: roomName }); // (2)!
  const token = await at.toJwt(); // (3)!
  res.json({ token }); // (4)!
});
```

1. A new `AccessToken` is created providing the `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` and setting the participant's identity.
2. We set the video grants in the AccessToken. `roomJoin` allows the user to join a room and `room` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/realtime/concepts/authentication/#Video-grant){:target="\_blank"}.
3. We convert the AccessToken to a JWT token.
4. Finally, the token is sent back to the client.

The endpoint first obtains the `roomName` and `participantName` parameters from the request body. If they are not available, it returns a `400` error.

If required fields are available, a new JWT token is created. For that we use the [LiveKit JS SDK](https://docs.livekit.io/server-sdk-js){:target="\_blank"}:

1. A new `AccessToken` is created providing the `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` and setting the participant's identity.
2. We set the video grants in the AccessToken. `roomJoin` allows the user to join a room and `room` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/realtime/concepts/authentication/#Video-grant){:target="\_blank"}.
3. We convert the AccessToken to a JWT token.
4. Finally, the token is sent back to the client.

---

#### Receive webhook

The endpoint `/webhook` accepts `POST` requests with a payload of type `application/webhook+json`. This is the endpoint where LiveKit Server will send [webhook events](https://docs.livekit.io/realtime/server/webhooks/#Events){:target="\_blank"}.

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/node/index.js#L33-L49' target='_blank'>index.js</a>" linenums="33"
const webhookReceiver = new WebhookReceiver( // (1)!
  LIVEKIT_API_KEY,
  LIVEKIT_API_SECRET
);

app.post("/webhook", async (req, res) => {
  try {
    const event = await webhookReceiver.receive(
      req.body, // (2)!
      req.get("Authorization") // (3)!
    );
    console.log(event); // (4)!
  } catch (error) {
    console.error("Error validating webhook event", error);
  }
  res.status(200).send();
});
```

1. Initialize the WebhookReceiver using the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`. It will help validating and decoding incoming [webhook events](https://docs.livekit.io/realtime/server/webhooks/){target=\_blank}.
2. The body of the HTTP request.
3. The `Authorization` header of the HTTP request.
4. Consume the event as you whish.

First of all we initialize the `WebhookReceiver` using the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`. This object will validate and decode the incoming webhook events.

The endpoint receives the incoming webhook with the async method `WebhookReceiver#receive`. It takes the body and the `Authorization` header of the request. If everything is correct, you can do whatever you want with the event (in this case, we just log it).

Remember to return a `200` OK response at the end to let LiveKit Server know that the webhook was received correctly.

<br>