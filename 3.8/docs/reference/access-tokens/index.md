# Access tokens

Any client requires an **access token** to connect to a Room in OpenVidu. The token is a JWT signed with your deployment's API secret, generated securely by your **application server**. It carries the participant's identity, display name, metadata, and permissions.

OpenVidu is API-compatible with LiveKit, so any LiveKit server SDK can generate valid OpenVidu tokens. Visit the LiveKit docs for a complete reference of token claims and grants:

[**LiveKit docs**](https://docs.livekit.io/frontends/reference/tokens-grants/)

The tutorials show a working token endpoint in different languages:

[**Application server tutorials**](https://openvidu.io/3.8/docs/tutorials/application-server/index.md)

## API key and API secret

Tokens are signed with the key pair configured in your OpenVidu deployment:

| Parameter            | Where it lives                                                                                                                |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `LIVEKIT_API_KEY`    | `openvidu.env`: see the [configuration reference](https://openvidu.io/3.8/docs/self-hosting/configuration/reference/index.md) |
| `LIVEKIT_API_SECRET` | `openvidu.env`: same file                                                                                                     |

Two notes:

- An [OpenVidu local deployment](https://openvidu.io/3.8/docs/self-hosting/local/index.md) starts with the development pair `LIVEKIT_API_KEY=devkey` and `LIVEKIT_API_SECRET=secret`.
- Any production OpenVidu deployment must keep its API key and secret private. Always keep those values in your application server's environment, never in a browser or mobile bundle.

## Anatomy of a token

The token is a JWT signed with HS256 using your API secret. Its payload says who the participant is, what they are allowed to do, and for how long the token is valid.

Some notes:

- A participant already in a Room is not disconnected when their token expires.
- Tokens are verified with one minute of leeway on `nbf` and `exp`, which absorbs a small clock difference between your application server and your OpenVidu deployment.
- An already issued token cannot be revoked. See [token lifecycle](#token-lifecycle) below for what that means in practice.

### Token claims

Decoded, the payload of a typical participant token looks like this:

```json
{
  "iss": "APIM6JLn2DGzDON",
  "sub": "my-participant",
  "nbf": 1787240258,
  "exp": 1787261858,
  "identity": "my-participant",
  "name": "My Participant",
  "video": {
    "roomJoin": true,
    "room": "my-room",
    "canPublish": true,
    "canSubscribe": true
  },
  "metadata": "{\"role\":\"speaker\"}",
  "attributes": {
    "lang": "en"
  }
}
```

| Claim        | Type                       | What it does                                                                                                                                                                                                                                                                               |
| ------------ | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `iss`        | string                     | Your API key. This is how the server knows which secret to verify with                                                                                                                                                                                                                     |
| `sub`        | string                     | Standard JWT subject. Same value as `identity`                                                                                                                                                                                                                                             |
| `nbf`        | number                     | Not-before time. The token cannot be used to connect before it                                                                                                                                                                                                                             |
| `exp`        | number                     | Expiry time. The token cannot be used to connect after it. By default 6 hours from the time the token is created                                                                                                                                                                           |
| `identity`   | string                     | Unique identifier of the participant inside the Room. Two participants with the same identity in the same Room conflict: the newer one evicts the older                                                                                                                                    |
| `name`       | string                     | Participant display name                                                                                                                                                                                                                                                                   |
| `metadata`   | string                     | Participant metadata                                                                                                                                                                                                                                                                       |
| `attributes` | key/value pairs of strings | Key/value data attached to the participant, individually updatable during the Room                                                                                                                                                                                                         |
| `video`      | object                     | The video grants: the permission set in the room for this participant (see [Video grants](#video-grants))                                                                                                                                                                                  |
| `roomConfig` | object                     | Configuration applied to the Room if this token is the one that creates it. Among other things it allows automatically dispatching agents and recording rooms. See the type definition for [RoomConfiguration](https://docs.livekit.io/reference/other/roomservice-api/#roomconfiguration) |

### Video grants

The `video` claim is where permissions live. Every field is optional; anything you omit is simply not granted, except where noted.

| Grant                  | Type            | Effect                                                                                                                                                         |
| ---------------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `roomCreate`           | boolean         | Allows creating and deleting Rooms                                                                                                                             |
| `roomList`             | boolean         | Allows listintg Rooms                                                                                                                                          |
| `roomJoin`             | boolean         | Allows joining a Room as a participant                                                                                                                         |
| `roomAdmin`            | boolean         | Allows moderating a Room. This is generally a server-side permission (remove participants, mute tracks, update participant permissions... )                    |
| `room`                 | string          | The Room name this token is valid for. Required when setting `roomJoin`or `roomAdmin`                                                                          |
| `roomRecord`           | boolean         | Allows calling the [Egress API](https://openvidu.io/3.8/docs/reference/egress/index.md). This is generally a server-side permission                            |
| `ingressAdmin`         | boolean         | Allows calling the [Ingress API](https://openvidu.io/3.8/docs/reference/ingress/index.md). This is generally a server-side permission                          |
| `canPublish`           | boolean         | Allows publishing tracks. **Defaults to true** when the field is absent. Set it to `false` explicitly for a viewer-only participant                            |
| `canSubscribe`         | boolean         | Allows subscribing to other participants' tracks. **Defaults to true** when the field is absent. Set it to `false` explicitly for a publisher-only participant |
| `canPublishData`       | boolean         | Allows sending data messages. **Defaults to true** when the field is absent                                                                                    |
| `canPublishSources`    | array of string | Restricts publishing to specific track sources: `camera`, `microphone`, `screen_share`, `screen_share_audio`. Requires `canPublish`                            |
| `canUpdateOwnMetadata` | boolean         | Allows the participant to change its own `name`, `metadata` and `attributes` from the client side                                                              |
| `hidden`               | boolean         | The participant is present but invisible to others. It does not appear in their participant lists                                                              |

## Generating a token

**Node.js**

- Using [LiveKit Node SDK](https://docs.livekit.io/server-sdk-js/) .
- For a working example run the [Node.js tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/node/index.md).

```javascript
import { AccessToken } from 'livekit-server-sdk';

const at = new AccessToken('api-key', 'api-secret', {
  identity: 'my-participant',
  name: 'My Participant',
});
at.addGrant({
  roomJoin: true,
  room: 'my-room',
  canPublish: true,
  canPublishData: false,
});
const token = await at.toJwt();
```

**Go**

- Using [LiveKit Go SDK](https://pkg.go.dev/github.com/livekit/server-sdk-go/v2) .
- For a working example run the [Go tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/go/index.md).

```go
import "github.com/livekit/protocol/auth"

canPublish := true
canPublishData := false

at := auth.NewAccessToken("api-key", "api-secret").
    SetIdentity("my-participant").
    SetName("My Participant").
    SetVideoGrant(&auth.VideoGrant{
        RoomJoin:       true,
        Room:           "my-room",
        CanPublish:     &canPublish,
        CanPublishData: &canPublishData,
    })
token, err := at.ToJWT()
```

**Ruby**

- Using [LiveKit Ruby SDK](https://github.com/livekit/server-sdk-ruby) .
- For a working example run the [Ruby tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/ruby/index.md).

```ruby
require 'livekit'

token = LiveKit::AccessToken.new(api_key: 'api-key', api_secret: 'api-secret')
token.identity = 'my-participant'
token.name = 'My Participant'
token.add_grant(
  roomJoin: true,
  room: 'my-room',
  canPublish: true,
  canPublishData: false
)
jwt = token.to_jwt
```

**Java**

- Using [LiveKit Kotlin SDK](https://github.com/livekit/server-sdk-kotlin) .
- For a working example run the [Java tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/java/index.md).

```java
import io.livekit.server.*;

AccessToken token = new AccessToken("api-key", "api-secret");
token.setIdentity("my-participant");
token.setName("My Participant");
token.addGrants(
    new RoomJoin(true),
    new RoomName("my-room"),
    new CanPublish(true),
    new CanPublishData(false)
);
String jwt = token.toJwt();
```

**Python**

- Using [LiveKit Python SDK](https://github.com/livekit/python-sdks) .
- For a working example run the [Python tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/python/index.md).

```python
from livekit.api import AccessToken, VideoGrants

token = (
    AccessToken("api-key", "api-secret")
    .with_identity("my-participant")
    .with_name("My Participant")
    .with_grants(
        VideoGrants(
            room_join=True,
            room="my-room",
            can_publish=True,
            can_publish_data=False,
        )
    )
    .to_jwt()
)
```

**Rust**

- Using [LiveKit Rust SDK](https://github.com/livekit/rust-sdks) .
- For a working example run the [Rust tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/rust/index.md).

```rust
use livekit_api::access_token::{AccessToken, VideoGrants};

let token = AccessToken::with_api_key("api-key", "api-secret")
    .with_identity("my-participant")
    .with_name("My Participant")
    .with_grants(VideoGrants {
        room_join: true,
        room: "my-room".to_string(),
        can_publish: true,
        can_publish_data: false,
        ..Default::default()
    })
    .to_jwt()?;
```

**PHP**

- Using [LiveKit PHP SDK](https://github.com/agence104/livekit-server-sdk-php) .
- For a working example run the [PHP tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/php/index.md).

```php
<?php
use Agence104\LiveKit\AccessToken;
use Agence104\LiveKit\AccessTokenOptions;
use Agence104\LiveKit\VideoGrant;

$options = (new AccessTokenOptions())
    ->setIdentity('my-participant')
    ->setName('My Participant');
$grant = (new VideoGrant())
    ->setRoomJoin()
    ->setRoomName('my-room')
    ->setCanPublish(TRUE)
    ->setCanPublishData(FALSE);
$jwt = (new AccessToken('api-key', 'api-secret'))
    ->init($options)
    ->setGrant($grant)
    ->toJwt();
```

**.NET**

- Using [LiveKit .NET SDK](https://github.com/pabloFuente/livekit-server-sdk-dotnet) .
- For a working example run the [.NET tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/dotnet/index.md).

```csharp
using Livekit.Server.Sdk.Dotnet;

var token = new AccessToken("api-key", "api-secret")
    .WithIdentity("my-participant")
    .WithName("My Participant")
    .WithGrants(new VideoGrants
    {
        RoomJoin = true,
        Room = "my-room",
        CanPublish = true,
        CanPublishData = false,
    });
string jwt = token.ToJwt();
```

**CLI**

Using the [LiveKit CLI](https://docs.livekit.io/home/cli/cli-setup/)

```bash
export LIVEKIT_API_KEY=api-key
export LIVEKIT_API_SECRET=api-secret

lk token create \
  --identity my-participant \
  --room my-room \
  --join \
  --valid-for 1h
```

Each [application server tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/index.md) is a complete working server built around exactly this code.

## Token lifecycle

### Token refresh

OpenVidu keeps issuing refreshed tokens to participants while they are connected to a Room:

- Refreshed tokens let a client recover from a dropped connection without asking your backend for a new token.
- Each refreshed token is rebuilt from the participant's current claims, so it always carries the permissions in effect at that moment.
- Any change to the participant's name, metadata, attributes or permissions ([`UpdateParticipant`](https://openvidu.io/3.8/docs/reference/room-service-api/#participants)) triggers a refresh immediately.

The refreshed token exchange is invisible to your application: the client SDK replaces the token it holds in memory and raises no event for it, and your backend is not involved.

### Revocation

An issued token cannot be revoked. Neither [`RemoveParticipant`](https://openvidu.io/3.8/docs/reference/room-service-api/#participants) nor narrowing a participant's grants invalidates a token that is already out: it stays usable to connect until it expires on its own.

Two habits follow from that:

- Keep token lifetimes short. The 6 hour default is generous for a token whose only job is to connect once.
- Do not generate a new token for a participant you just removed.

### Updating token permissions

[`UpdateParticipant`](https://openvidu.io/3.8/docs/reference/room-service-api/#participants) applies new permissions to an already-connected participant without a reconnect, for example promoting a viewer to speaker:

- The client observes a [`ParticipantPermissionsChanged`](https://openvidu.io/3.8/docs/reference/client-sdk/#participants-and-room-state) event.
- Revoking [`canPublish` video grant](#video-grants) automatically unpublishes every track that participant had published.

## Designing your permission model

Access tokens are the whole authorization surface: OpenVidu Platform has no notion of your users, so **your** rules decide what each token carries. Two habits worth keeping when generating tokens for your clients:

- **Authenticate before you generate.** The token endpoint must be behind your own login. An open `/token` endpoint lets anyone join any Room under any name.
- **Generate the narrowest token that works.** Scope it to one Room, set `canPublish: false` for viewers, and keep administration grants out of client tokens.

For server-side operations run from your application server, all LiveKit server SDKs automatically generate a token with the required grants for each operation. Visit the [Room Service API reference](https://openvidu.io/3.8/docs/reference/room-service-api/index.md), [Egress API reference](https://openvidu.io/3.8/docs/reference/egress/index.md) and [Ingress API reference](https://openvidu.io/3.8/docs/reference/ingress/index.md) for further information.
