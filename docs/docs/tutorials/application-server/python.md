# Python

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/master/application-server/python){ .md-button target=\_blank }

This is a minimal server application built for Python with [Flask](https://flask.palletsprojects.com/){:target="\_blank"} that allows:

- Generating LiveKit tokens on demand for any [application client](../application-client/index.md).
- Receiving LiveKit [webhook events](https://docs.livekit.io/realtime/server/webhooks/){target=\_blank}.

It internally uses [LiveKit Python SDK](https://github.com/livekit/python-sdks){:target="\_blank"}.

## Running this application

Download the tutorial code:

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git
```

--8<-- "docs/docs/tutorials/shared/python.md"

!!! info

    You can run any [Application Client](../application-client/index.md) to test against this server right away.

## Understanding the code

The application is a simple Flask app with a single file `app.py` that exports two endpoints:

- `/token` : generate a token for a given Room name and Participant name.
- `/webhook` : receive LiveKit webhook events.

Let's see the code of the `app.py` file:

```python title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/python/app.py#L1-L15' target='_blank'>app.py</a>" linenums="1"
import os
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from livekit.api import AccessToken, VideoGrants, TokenVerifier, WebhookReceiver # (1)!

load_dotenv() # (2)!

SERVER_PORT = os.environ.get("SERVER_PORT", 6080) # (3)!
LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY", "devkey") # (4)!
LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET", "secret") # (5)!

app = Flask(__name__) # (6)!

CORS(app) # (7)!
```

1. Import all necessary dependencies from `livekit` library
2. Load environment variables from `.env` file
3. The port where the application will be listening
4. The API key of LiveKit Server
5. The API secret of LiveKit Server
6. Initialize the Flask application
7. Enable CORS support

The `app.py` file imports the required dependencies and loads the necessary environment variables from `.env` file using `dotenv` library:

- `SERVER_PORT`: the port where the application will be listening.
- `LIVEKIT_API_KEY`: the API key of LiveKit Server.
- `LIVEKIT_API_SECRET`: the API secret of LiveKit Server.

Finally the `Flask` application is initialized and CORS support is enabled.

---

#### Create token

The endpoint `/token` accepts `POST` requests with a payload of type `application/json`, containing the following fields:

- `roomName`: the name of the Room where the user wants to connect.
- `participantName`: the name of the participant that wants to connect to the Room.

```python title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/python/app.py#L18-L31' target='_blank'>app.py</a>" linenums="18"
@app.post("/token")
def create_token():
    room_name = request.json.get("roomName")
    participant_name = request.json.get("participantName")

    if not room_name or not participant_name:
        return {"errorMessage": "roomName and participantName are required"}, 400

    token = (
        AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET) # (1)!
        .with_identity(participant_name) # (2)!
        .with_grants(api.VideoGrants(room_join=True, room=room_name)) # (3)!
    )
    return {"token": token.to_jwt()} # (4)!
```

1. A new `AccessToken` is created providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.
2. We set participant's identity in the AccessToken.
3. We set the video grants in the AccessToken. `room_join` allows the user to join a room and `room` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/realtime/concepts/authentication/#Video-grant){:target="\_blank"}.
4. Finally, we convert the AccessToken to a JWT token and send it back to the client.

The endpoint first obtains the `roomName` and `participantName` parameters from the request body. If they are not available, it returns a `400` error.

If required fields are available, a new JWT token is created. For that we use the [LiveKit Python SDK](https://github.com/livekit/python-sdks){:target="\_blank"}:

1. A new `AccessToken` is created providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.
2. We set participant's identity in the AccessToken.
3. We set the video grants in the AccessToken. `room_join` allows the user to join a room and `room` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/realtime/concepts/authentication/#Video-grant){:target="\_blank"}.
4. Finally, we convert the AccessToken to a JWT token and send it back to the client.

---

#### Receive webhook

The endpoint `/webhook` accepts `POST` requests with a payload of type `application/webhook+json`. This is the endpoint where LiveKit Server will send [webhook events](https://docs.livekit.io/realtime/server/webhooks/#Events){:target="\_blank"}.

```python title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/python/app.py#L34-L51' target='_blank'>app.py</a>" linenums="34"
token_verifier = TokenVerifier(LIVEKIT_API_KEY, LIVEKIT_API_SECRET) # (1)!
webhook_receiver = WebhookReceiver(token_verifier) # (2)!


@app.post("/webhook")
def receive_webhook():
    auth_token = request.headers.get("Authorization") # (3)!

    if not auth_token:
        return "Authorization header is required", 401

    try:
        event = webhook_receiver.receive(request.data.decode("utf-8"), auth_token) # (4)!
        print("LiveKit Webhook:", event) # (5)!
        return "ok"
    except:
        print("Authorization header is not valid")
        return "Authorization header is not valid", 401
```

1. Initialize a `TokenVerifier` using the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.
2. Initialize a `WebhookReceiver` using the `TokenVerifier`. It will help validating and decoding incoming [webhook events](https://docs.livekit.io/realtime/server/webhooks/){target=\_blank}.
3. Get the 'Authorization' header from the HTTP request.
4. Obtain the webhook event using the `WebhookReceiver#receive` method. It expects the raw body of the request and the 'Authorization' header.
5. Consume the event as you whish.

First of all, we need a `WebhookReceiver` for validating and decoding incoming webhook events. We initialize it with a `TokenVerifier` built with the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.

Inside the `receive_webhook` handler we:

1. Get the `Authorization` header from the HTTP request.
2. Obtain the webhook event using the `WebhookReceiver#receive` method. It expects the raw body of the request and the `Authorization` header. In this way, we can validate the event to confirm it is actually coming from our LiveKit Server.
3. If everything is ok, you can consume the event as you whish (in this case, we just log it).

<br>