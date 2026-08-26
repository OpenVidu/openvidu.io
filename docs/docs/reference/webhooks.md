---
title: "OpenVidu Platform webhooks reference"
description: "Every webhook event OpenVidu sends, the JSON payload it carries, and how to verify a request before your backend acts on it."
---

# Webhooks

Webhooks allow your application server to be notified of events of Rooms, Egress and Ingress without the need of polling. OpenVidu POSTs a signed JSON event to the URLs you configure, as Rooms start and finish, participants come and go, tracks are published, and Egress or Ingress processes change state.

To turn webhooks on, see [Enable OpenVidu webhooks](../self-hosting/how-to-guides/enable-webhooks.md). This page is the reference for what arrives once they are on.

OpenVidu is API-compatible with LiveKit, so all LiveKit webhook events are supported. Visit the LiveKit docs for a complete reference of webhook management:

[:octicons-arrow-right-24: **LiveKit docs**](https://docs.livekit.io/intro/basics/rooms-participants-tracks/webhooks-events/#managing-webhooks){:target="_blank"}



## Events

| Event | Fires when | Payload that carries |
| --- | --- | --- |
| `room_started` | A Room is created, either by the first participant joining or by your backend creating it explicitly | `room` |
| `room_finished` | A Room ends, either because your backend deleted it or because the departure timeout elapsed after the last participant left | `room` |
| `participant_joined` | A participant finishes connecting to a Room | `room`, `participant` |
| `participant_left` | A participant disconnects | `room`, `participant` |
| `participant_connection_aborted` | A participant's connection attempt did not complete | `room`, `participant` |
| `track_published` | A participant starts publishing a track | `room`, `participant`, `track` |
| `track_unpublished` | A participant stops publishing a track | `room`, `participant`, `track` |
| `egress_started` | An Egress process begins (a recording or stream export) | `egressInfo` |
| `egress_updated` | An Egress process changes state while running | `egressInfo` |
| `egress_ended` | An Egress process finishes, successfully or not | `egressInfo` |
| `ingress_started` | An Ingress process begins (media imported into a Room) | `ingressInfo` |
| `ingress_ended` | An Ingress process finishes | `ingressInfo` |

## Payload

The body is a JSON object with lowerCamelCase field names. A `participant_joined` event looks like this:

```json
{
  "event": "participant_joined",
  "id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "createdAt": "1755648000",
  "room": {
    "sid": "RM_GmENxWJemFqL",
    "name": "my-room",
    "creationTime": "1755647990",
    "numParticipants": 2
  },
  "participant": {
    "sid": "PA_dRnCwpBTgKe8",
    "identity": "my-participant",
    "name": "My Participant",
    "state": "ACTIVE"
  }
}
```

Only the fields relevant to the event are populated:

<div class="nowrap-first-column" markdown>

| Field | Type | Notes |
| --- | --- | --- |
| `event` | string | One of the [event names above](#events) |
| `id` | string | Unique id of this event |
| `createdAt` | int64 | Unix timestamp, in seconds, of when the event was created |
| `room` | object | Room information. Visit the official LiveKit documentation ([Room :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#room){:target="_blank"}) for details |
| `participant` | object | Participant information. Visit the official LiveKit documentation ([ParticipantInfo :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#participantinfo){:target="_blank"}) for details |
| `track` | object | Track information. Visit the official LiveKit documentation ([TrackInfo :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#trackinfo){:target="_blank"}) for details |
| `egressInfo` | object | Egress process information. Visit the official LiveKit documentation ([EgressInfo :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#egressinfo){:target="_blank"}) for details |
| `ingressInfo` | object | Ingress process information. Visit the official LiveKit documentation ([IngressInfo :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/ingress/api/#ingressinfo){:target="_blank"}) for details |
| `numDropped` | int64 | The number of events that were dropped before this one. This acts as your delivery health signal: a non-zero value indicates that your application server has missed some events |

</div>

## Delivery

| | |
| --- | --- |
| HTTP method | `POST` |
| `content-type` | `application/webhook+json` |
| `Authorization` | A JWT signed with your API secret. Use it to [verify the event](#receiving-and-validating-webhook-events) |
| Body | The [payload](#payload) of the event, in JSON format |

!!! note
    - Events are always delivered in order: a newer event is sent only after the older ones have been delivered (or abandoned).
    - There is no guarantee of delivery. OpenVidu retries failed deliveries with exponential backoff, but if your endpoint is down for a long time or consistently returns errors, events will be abandoned.

## Receiving and validating webhook events

**Never act on an unverified webhook.** Your endpoint is a public URL, so anyone can POST to it; the signature is what distinguishes a real event from a forgery.

Verifying means:

1. Verify the JWT's signature with your `LIVEKIT_API_SECRET`.
2. Hash the raw body with SHA-256, base64-encode it, and compare against the token's `sha256` claim.

The LiveKit server SDKs do both for you:

=== ":simple-nodedotjs:{.icon .lg-icon .tab-icon} Node.js"

    - Using [LiveKit Node SDK :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/server-sdk-js/){:target="_blank"}.
    - For a working example run the [Node.js tutorial](../tutorials/application-server/node.md).

    ```javascript
    import express from "express";
    import { WebhookReceiver } from "livekit-server-sdk";

    const webhookReceiver = new WebhookReceiver("api-key", "api-secret");

    // The receiver needs the raw body, not parsed JSON
    app.use(express.raw({ type: "application/webhook+json" }));

    app.post("/livekit/webhook", async (req, res) => {
      try {
        const event = await webhookReceiver.receive(req.body, req.get("Authorization"));
        // event is verified: safe to act on
      } catch (error) {
        console.error("Error validating webhook event", error);
      }
      res.status(200).send();
    });
    ```

=== ":simple-goland:{.icon .lg-icon .tab-icon} Go"

    - Using [LiveKit Go SDK :fontawesome-solid-external-link:{.external-link-icon}](https://pkg.go.dev/github.com/livekit/server-sdk-go/v2){:target="_blank"}.
    - For a working example run the [Go tutorial](../tutorials/application-server/go.md).

    ```go
    import (
        "net/http"

        "github.com/livekit/protocol/auth"
        "github.com/livekit/protocol/webhook"
    )

    func receiveWebhook(w http.ResponseWriter, r *http.Request) {
        authProvider := auth.NewSimpleKeyProvider("api-key", "api-secret")
        event, err := webhook.ReceiveWebhookEvent(r, authProvider)
        if err != nil {
            http.Error(w, "Error validating webhook event", http.StatusUnauthorized)
            return
        }
        // event is verified: safe to act on
        w.WriteHeader(http.StatusOK)
    }
    ```

=== ":simple-ruby:{.icon .lg-icon .tab-icon} Ruby"

    - Using [LiveKit Ruby SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/server-sdk-ruby){:target="_blank"}.
    - For a working example run the [Ruby tutorial](../tutorials/application-server/ruby.md).

    The Ruby SDK has no `WebhookReceiver` class. Verify the `Authorization` header with `LiveKit::TokenVerifier`, compare the body hash against the token's `sha256` claim, then parse the body yourself:

    ```ruby
    require 'livekit'
    require 'json'
    require 'digest'

    post '/livekit/webhook' do
      token_verifier = LiveKit::TokenVerifier.new(api_key: 'api-key', api_secret: 'api-secret')
      begin
        body = request.body.read
        claims = token_verifier.verify(request.env['HTTP_AUTHORIZATION'])
        halt 401, "Webhook body hash mismatch" if claims.sha256 != Digest::SHA256.base64digest(body)
        event = JSON.parse(body)
        # event is verified: safe to act on
      rescue => e
        halt 401, "Error validating webhook event: #{e}"
      end
    end
    ```

=== ":fontawesome-brands-java:{.icon .lg-icon .tab-icon} Java"

    - Using [LiveKit Kotlin SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/server-sdk-kotlin){:target="_blank"}.
    - For a working example run the [Java tutorial](../tutorials/application-server/java.md).

    ```java
    import io.livekit.server.WebhookReceiver;
    import livekit.LivekitWebhook.WebhookEvent;

    WebhookReceiver webhookReceiver = new WebhookReceiver("api-key", "api-secret");

    // body is the raw request body as a String
    // authHeader is the value of the "Authorization" header
    WebhookEvent event = webhookReceiver.receive(body, authHeader);
    // event is verified: safe to act on (receive throws if it is not valid)
    ```

=== ":fontawesome-brands-python:{.icon .lg-icon .tab-icon} Python"

    - Using [LiveKit Python SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/python-sdks){:target="_blank"}.
    - For a working example run the [Python tutorial](../tutorials/application-server/python.md).

    ```python
    from livekit.api import TokenVerifier, WebhookReceiver

    token_verifier = TokenVerifier("api-key", "api-secret")
    webhook_receiver = WebhookReceiver(token_verifier)

    @app.post("/livekit/webhook")
    def receive_webhook():
        auth_token = request.headers.get("Authorization")
        try:
            event = webhook_receiver.receive(request.data.decode("utf-8"), auth_token)
            # event is verified: safe to act on
            return "ok"
        except Exception:
            return "Error validating webhook event", 401
    ```

=== ":simple-rust:{.icon .lg-icon .tab-icon} Rust"

    - Using [LiveKit Rust SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/rust-sdks){:target="_blank"}.
    - For a working example run the [Rust tutorial](../tutorials/application-server/rust.md).

    ```rust
    use livekit_api::access_token::TokenVerifier;
    use livekit_api::webhooks::WebhookReceiver;

    async fn receive_webhook(headers: HeaderMap, body: String) -> StatusCode {
        let token_verifier = TokenVerifier::with_api_key("api-key", "api-secret");
        let webhook_receiver = WebhookReceiver::new(token_verifier);

        let auth_header = headers
            .get("Authorization")
            .and_then(|v| v.to_str().ok())
            .unwrap_or("");

        match webhook_receiver.receive(&body, auth_header) {
            Ok(event) => {
                // event is verified: safe to act on
                println!("LiveKit Webhook: {:?}", event);
                StatusCode::OK
            }
            Err(_) => StatusCode::UNAUTHORIZED,
        }
    }
    ```

=== ":simple-php:{.icon .lg-icon .tab-icon} PHP"

    - Using [LiveKit PHP SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/agence104/livekit-server-sdk-php){:target="_blank"}.
    - For a working example run the [PHP tutorial](../tutorials/application-server/php.md).

    ```php
    <?php
    use Agence104\LiveKit\WebhookReceiver;

    $webhookReceiver = new WebhookReceiver("api-key", "api-secret");

    $body = file_get_contents("php://input");
    $authHeader = getallheaders()["Authorization"];

    try {
        $event = $webhookReceiver->receive($body, $authHeader);
        // event is verified: safe to act on
    } catch (Exception $e) {
        http_response_code(401);
    }
    ```

=== ":simple-dotnet:{.icon .lg-icon .tab-icon} .NET"

    - Using [LiveKit .NET SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/pabloFuente/livekit-server-sdk-dotnet){:target="_blank"}.
    - For a working example run the [.NET tutorial](../tutorials/application-server/dotnet.md).

    ```csharp
    using Livekit.Server.Sdk.Dotnet;

    var webhookReceiver = new WebhookReceiver("api-key", "api-secret");

    app.MapPost("/livekit/webhook", async (HttpRequest request) =>
    {
        string body = await new StreamReader(request.Body).ReadToEndAsync();
        string authHeader = request.Headers["Authorization"].FirstOrDefault();
        try
        {
            WebhookEvent webhookEvent = webhookReceiver.Receive(body, authHeader);
            // event is verified: safe to act on
            return Results.Ok();
        }
        catch (Exception)
        {
            return Results.Unauthorized();
        }
    });
    ```

!!! tip "Each [application server tutorial](../tutorials/application-server/index.md) ships a working, validated webhook endpoint in its language."

## Developing against a remote deployment

Your local machine is not reachable from your OpenVidu deployment, so webhooks sent to `localhost` never arrive. Expose your local server with a tunnel and configure that public URL instead — see [Send webhooks to a local application server](../self-hosting/how-to-guides/enable-webhooks.md#send-webhooks-to-a-local-application-server).

## Related

- [Enable OpenVidu webhooks](../self-hosting/how-to-guides/enable-webhooks.md): configuring `webhook.urls` in `livekit.yaml`.
- [Access tokens reference](./access-tokens.md): the same key pair, used in the other direction.
- [Egress reference](./egress.md) and [Ingress reference](./ingress.md): the objects `egressInfo` and `ingressInfo` carry.
- [Recording tutorial](../tutorials/advanced-features/recording-advanced-s3.md#handling-webhook-events): egress webhook events in a real application server.
- **OpenVidu Meet** sends its own, higher-level webhooks. If you are embedding Meet rather than building on Platform, see the [OpenVidu Meet webhooks reference](../../meet/embedded/reference/webhooks.md).
