---
title: "OpenVidu Platform webhooks reference"
description: "Every webhook event OpenVidu sends, the JSON payload it carries, and how to verify a request before your backend acts on it."
---

# Webhooks

Webhooks are how your application server learns what happened in a Room without polling. OpenVidu POSTs a signed JSON event to the URLs you configure, as Rooms start and finish, participants come and go, tracks are published, and Egress or Ingress processes change state.

To turn them on, see [Enable OpenVidu webhooks](../self-hosting/how-to-guides/enable-webhooks.md). This page is the reference for what arrives once they are on.

## Events

| Event | Fires when | Carries |
| --- | --- | --- |
| `room_started` | A Room is created — the first participant joins, or your backend creates it explicitly | `room` |
| `room_finished` | A Room ends and is removed from the server | `room` |
| `participant_joined` | A participant finishes connecting to a Room | `room`, `participant` |
| `participant_left` | A participant disconnects | `room`, `participant` |
| `participant_connection_aborted` | A participant's connection attempt did not complete | `room`, `participant` |
| `track_published` | A participant starts publishing a track | `room`, `participant`, `track` |
| `track_unpublished` | A participant stops publishing a track | `room`, `participant`, `track` |
| `egress_started` | An Egress process begins — a recording or stream export | `egressInfo` |
| `egress_updated` | An Egress process changes state while running | `egressInfo` |
| `egress_ended` | An Egress process finishes, successfully or not | `egressInfo` |
| `ingress_started` | An Ingress process begins — media imported into a Room | `ingressInfo` |
| `ingress_ended` | An Ingress process finishes | `ingressInfo` |

`egress_ended` is the one most applications care about: it is the point at which a recording file is complete and its final location is known. The [recording tutorials](../tutorials/advanced-features/index.md) build on exactly that event.

## Payload

The body is a JSON object. Field names are lowerCamelCase, and only the fields relevant to the event are populated:

| Field | Type | Notes |
| --- | --- | --- |
| `event` | string | One of the event names above |
| `id` | string | Unique id of this event |
| `createdAt` | int64 | Unix timestamp, in seconds, of when the event was created |
| `room` | object | Room information: `sid`, `name`, `numParticipants`, `creationTime` and the rest of the Room's fields |
| `participant` | object | Participant information: `sid`, `identity`, `name`, `state`, `metadata`, `attributes`, permissions |
| `track` | object | Track information: `sid`, `type`, `source`, `muted`, dimensions and codec details |
| `egressInfo` | object | Egress process information, including its `egressId`, `roomName`, `status` and the resulting file or stream outputs |
| `ingressInfo` | object | Ingress process information, including its `ingressId`, `roomName` and state |
| `numDropped` | int32 | How many events were dropped since the last successful delivery to this URL. Anything other than `0` means your endpoint missed events |

A minimal `egress_ended` handler therefore reads:

```javascript
const { event, egressInfo } = webhookEvent;
if (event === "egress_ended") {
  // egressInfo.status tells you whether it completed or failed
}
```

!!! tip "`numDropped` is your delivery health signal"

    Webhooks are delivered on a best-effort basis: OpenVidu retries a failing endpoint, but events can still be dropped if your server stays unavailable. Log `numDropped` and alert on it — a non-zero value is the only notice you get that your application's view of the Rooms is incomplete.

## Delivery

| | |
| --- | --- |
| Method | `POST` |
| `content-type` | `application/webhook+json` |
| `Authorization` | A JWT signed with your API secret, valid for 5 minutes |
| Body | The JSON event, exactly as described above |

The unusual content type is deliberate: it stops a framework from parsing the body as ordinary JSON before you have verified the signature.

## Validating an event

**Never act on an unverified webhook.** Your endpoint is a public URL, so anyone can POST to it; the signature is what distinguishes a real event from a forgery.

The `Authorization` header carries a JWT whose `sha256` claim is the base64-encoded SHA-256 of the **raw request body**. Verifying means:

1. Verify the JWT's signature with your `LIVEKIT_API_SECRET`.
2. Hash the raw body with SHA-256, base64-encode it, and compare against the token's `sha256` claim.

The server SDKs do both for you. In Node.js:

```javascript
import { WebhookReceiver } from "livekit-server-sdk";

const webhookReceiver = new WebhookReceiver(LIVEKIT_API_KEY, LIVEKIT_API_SECRET);

app.post("/livekit/webhook", async (req, res) => {
  try {
    const event = await webhookReceiver.receive(req.body, req.get("Authorization"));
    // event is verified — safe to act on
  } catch (error) {
    console.error("Error validating webhook event", error);
  }
  res.status(200).send();
});
```

Two things that break validation, both easy to hit:

- **Parsing the body first.** The hash is over the exact bytes received. If a JSON body parser has already turned the body into an object, re-serializing it will not reproduce those bytes. Register a raw body parser for this route only — in Express, `express.raw({ type: "application/webhook+json" })`.
- **Reverse proxies that rewrite the body.** Anything that re-encodes or pretty-prints JSON on the way in invalidates the hash.

Every [application server tutorial](../tutorials/application-server/index.md) ships a working, validated webhook endpoint in its language.

## Developing against a remote deployment

Your local machine is not reachable from your OpenVidu deployment, so webhooks sent to `localhost` never arrive. Expose your local server with a tunnel and configure that public URL instead — see [Send webhooks to a local application server](../self-hosting/how-to-guides/enable-webhooks.md#send-webhooks-to-a-local-application-server).

## Related

- [Enable OpenVidu webhooks](../self-hosting/how-to-guides/enable-webhooks.md) — configuring `webhook.urls` in `livekit.yaml`
- [Access tokens reference](./access-tokens.md) — the same key pair, used in the other direction
- [Recording tutorials](../tutorials/advanced-features/index.md) — `egress_ended` in a working application
- OpenVidu Meet sends its own, higher-level webhooks. If you are embedding Meet rather than building on Platform, see the [OpenVidu Meet webhooks reference](../../meet/embedded/reference/webhooks.md)
