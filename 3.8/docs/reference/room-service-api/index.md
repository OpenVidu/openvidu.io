# Room Service API

The Room Service API is what your **application server** uses to manage Rooms from the outside: create and delete them, list who is in them, mute a track, remove a participant, push data into a Room. It is the counterpart to the [client SDKs](https://openvidu.io/3.8/docs/reference/client-sdk/index.md), which act from *inside* a Room as a participant.

The API is **Twirp-based HTTP** (plain `POST` requests with a JSON body) so any language can call it. OpenVidu is API-compatible with LiveKit, so any LiveKit server SDK can be used to manage Rooms. Visit the LiveKit docs for a complete reference of the Room Service API:

[**LiveKit docs**](https://docs.livekit.io/reference/other/roomservice-api/)

## Calling the API

Each server SDK exposes the same operations through a RoomService client, built with your deployment URL, API key and API secret. The SDK signs an [access token](https://openvidu.io/3.8/docs/reference/access-tokens/index.md) with the administrative grants of each operation for you, so a server-side token never leaves your backend. For example, removing a participant:

**Node.js**

Using [LiveKit Node SDK](https://docs.livekit.io/server-sdk-js/)

```javascript
import { RoomServiceClient } from 'livekit-server-sdk';

const roomClient = new RoomServiceClient('https://my-openvidu-host', 'api-key', 'api-secret');

await roomClient.removeParticipant('my-room', 'my-participant');
```

**Go**

Using [LiveKit Go SDK](https://pkg.go.dev/github.com/livekit/server-sdk-go/v2)

```go
import (
  "context"

  lksdk "github.com/livekit/server-sdk-go/v2"
  livekit "github.com/livekit/protocol/livekit"
)

roomClient := lksdk.NewRoomServiceClient("https://my-openvidu-host", "api-key", "api-secret")

_, err := roomClient.RemoveParticipant(context.Background(), &livekit.RoomParticipantIdentity{
    Room:     "my-room",
    Identity: "my-participant",
})
```

**Ruby**

Using [LiveKit Ruby SDK](https://github.com/livekit/server-sdk-ruby)

```ruby
require 'livekit'

roomClient = LiveKit::RoomServiceClient.new("https://my-openvidu-host", api_key: "api-key", api_secret: "api-secret")

roomClient.remove_participant(room: "my-room", identity: "my-participant")
```

**Java**

Using [LiveKit Kotlin SDK](https://github.com/livekit/server-sdk-kotlin)

```java
import io.livekit.server.RoomServiceClient;

RoomServiceClient roomClient = RoomServiceClient.createClient("https://my-openvidu-host", "api-key", "api-secret");

roomClient.removeParticipant("my-room", "my-participant").execute();
```

**Python**

Using [LiveKit Python SDK](https://github.com/livekit/python-sdks)

```python
from livekit.api import LiveKitAPI, RoomParticipantIdentity

lkapi = LiveKitAPI(
    url="https://my-openvidu-host", api_key="api-key", api_secret="api-secret"
)
await lkapi.room.remove_participant(
    RoomParticipantIdentity(room="my-room", identity="my-participant")
)
```

**Rust**

Using [LiveKit Rust SDK](https://github.com/livekit/rust-sdks)

```rust
use livekit_api::services::room::RoomClient;

let room_client = RoomClient::with_api_key(
    "https://my-openvidu-host",
    "api-key",
    "api-secret",
);
room_client.remove_participant("my-room", "my-participant").await?;
```

**PHP**

Using [LiveKit PHP SDK](https://github.com/agence104/livekit-server-sdk-php)

```php
<?php
use Agence104\LiveKit\RoomServiceClient;

$room_client = new RoomServiceClient("https://my-openvidu-host", "api-key", "api-secret");

$room_client->removeParticipant("my-room", "my-participant");
```

**.NET**

Using [LiveKit .NET SDK](https://github.com/pabloFuente/livekit-server-sdk-dotnet)

```csharp
using Livekit.Server.Sdk.Dotnet;

var roomClient = new RoomServiceClient("https://my-openvidu-host", "api-key", "api-secret");

await roomClient.RemoveParticipant(new RoomParticipantIdentity
{
    Room = "my-room",
    Identity = "my-participant",
});
```

**Server API**

If your backend technology does not have its own SDK, you have two options:

1. Call the Room Service API directly. Every operation is a POST to `/twirp/livekit.RoomService/<Operation>`, with `Content-Type: application/json` and an [access token](https://openvidu.io/3.8/docs/reference/access-tokens/index.md) in the `Authorization` header. Parameters travel in a JSON body, accepted in both `snake_case` and `camelCase`, and operations that take none receive `{}`. The [Egress](https://openvidu.io/3.8/docs/reference/egress/index.md) and [Ingress](https://openvidu.io/3.8/docs/reference/ingress/index.md) modules expose their own services the same way, at `/twirp/livekit.Egress/` and `/twirp/livekit.Ingress/`:

   ```bash
   curl -X POST 'https://my-openvidu-host/twirp/livekit.RoomService/RemoveParticipant' \
     -H 'Authorization: Bearer <TOKEN>' \
     -H 'Content-Type: application/json' \
     -d '{
           "room": "my-room",
           "identity": "my-participant"
         }'
   ```

1. Use the [livekit-cli](https://docs.livekit.io/home/cli/cli-setup/) :

   ```bash
   export LIVEKIT_URL=https://my-openvidu-host
   export LIVEKIT_API_KEY=api-key
   export LIVEKIT_API_SECRET=api-secret

   lk room participants remove --room my-room --identity my-participant
   ```

You can check out the type definitions for the responses in the [LiveKit reference docs](https://docs.livekit.io/reference/other/roomservice-api/#types) .

For example, `ListParticipants` operation returns a list of [`ParticipantInfo`](https://docs.livekit.io/reference/other/roomservice-api/#participantinfo) objects:

```json
{
  "participants": [
    {
      "sid": "PA_x7bK2mQ9pLwR",
      "identity": "my-participant",
      "name": "My Participant",
      "state": "ACTIVE",
      "joined_at": 1724501200,
      "permissions": {
        "can_publish": true
      },
      "isPublisher": true
    }
  ]
}
```

## Operations

Every operation includes:

- A link to the LiveKit docs for the exact request and response shapes.
- The access token grant required to call it (although LiveKit server SDKs automatically handle this for you).
- The return type, if any, and a link to its definition in the LiveKit docs.
- A short description of what the operation does.

### Rooms

| Operation                                                                                           | Grant        | Return type                                                                     | What it does                                                                                                                                         |
| --------------------------------------------------------------------------------------------------- | ------------ | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`CreateRoom`](https://docs.livekit.io/reference/other/roomservice-api/#createroom)                 | `roomCreate` | [`Room`](https://docs.livekit.io/reference/other/roomservice-api/#room)         | Creates a Room with explicit settings. This operation is optional, as Rooms can be created automatically the first time a participant connects to it |
| [`ListRooms`](https://docs.livekit.io/reference/other/roomservice-api/#listrooms)                   | `roomList`   | List of [`Room`](https://docs.livekit.io/reference/other/roomservice-api/#room) | Lists the Rooms currently active on the server                                                                                                       |
| [`DeleteRoom`](https://docs.livekit.io/reference/other/roomservice-api/#deleteroom)                 | `roomCreate` | Empty                                                                           | Deletes a Room, disconnecting every participant in it in the process                                                                                 |
| [`UpdateRoomMetadata`](https://docs.livekit.io/reference/other/roomservice-api/#updateroommetadata) | `roomAdmin`  | [`Room`](https://docs.livekit.io/reference/other/roomservice-api/#room)         | Replaces the Room's metadata. The change is broadcast to every participant                                                                           |

### Participants

| Operation                                                                                             | Grant       | Return type                                                                                           | What it does                                                                                                                                                                                                                        |
| ----------------------------------------------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`ListParticipants`](https://docs.livekit.io/reference/other/roomservice-api/#listparticipants)       | `roomAdmin` | List of [`ParticipantInfo`](https://docs.livekit.io/reference/other/roomservice-api/#participantinfo) | Lists the participants in a Room                                                                                                                                                                                                    |
| [`GetParticipant`](https://docs.livekit.io/reference/other/roomservice-api/#getparticipant)           | `roomAdmin` | [`ParticipantInfo`](https://docs.livekit.io/reference/other/roomservice-api/#participantinfo)         | Returns one participant by identity                                                                                                                                                                                                 |
| [`RemoveParticipant`](https://docs.livekit.io/reference/other/roomservice-api/#removeparticipant)     | `roomAdmin` | Empty                                                                                                 | Disconnects a participant. They can reconnect with a valid token. To keep them out, stop issuing tokens                                                                                                                             |
| [`UpdateParticipant`](https://docs.livekit.io/reference/other/roomservice-api/#updateparticipant)     | `roomAdmin` | [`ParticipantInfo`](https://docs.livekit.io/reference/other/roomservice-api/#participantinfo)         | Changes a participant's metadata, name, attributes or permissions. Broadcast to the Room                                                                                                                                            |
| [`MutePublishedTrack`](https://docs.livekit.io/reference/other/roomservice-api/#mutepublishedtrack)   | `roomAdmin` | [`TrackInfo`](https://docs.livekit.io/reference/other/roomservice-api/#trackinfo)                     | Mutes or unmutes one of a participant's published tracks. Remote unmute additionally requires `room.enable_remote_unmute: true` in [`livekit.yaml`](https://openvidu.io/3.8/docs/self-hosting/configuration/reference/#livekityaml) |
| [`UpdateSubscriptions`](https://docs.livekit.io/reference/other/roomservice-api/#updatesubscriptions) | `roomAdmin` | Empty                                                                                                 | Subscribes or unsubscribes a participant to specific tracks, from the server side                                                                                                                                                   |

### Data

| Operation                                                                       | Grant       | Return type                                      | What it does                                                                                                                                                  |
| ------------------------------------------------------------------------------- | ----------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`SendData`](https://docs.livekit.io/reference/other/roomservice-api/#senddata) | `roomAdmin` | Empty                                            | Sends a data message over the data channel, with reliable or lossy delivery and an optional `topic`. Empty `destinationIdentities` sends it to the whole Room |
| `PerformRpc`                                                                    | `roomAdmin` | The `payload` string returned by the participant | Invokes an RPC method that a participant has registered with its client SDK. Visit [RPC](https://docs.livekit.io/transport/data/rpc/) to learn more           |

## Choosing between the server API and the client SDK

Some operations exist on both sides. A participant can mute its own microphone from the client SDK, and your application server can mute that same track with `MutePublishedTrack`. What separates the two surfaces is not what they can do, but **who they can do it to**:

- The **client SDK** acts on **itself**. A participant publishes and mutes its own tracks, updates its own metadata, and leaves the Room. It can never reach another participant, and its authority is limited to what its access token grants.
- The **Room Service API** acts on **anyone**, from outside the Room. It mutes any track, disconnects any participant, changes the Room itself, and works even when nobody is connected yet. It provides an administrative and moderation control plane of Rooms, directly from your application server.

Each side can do things the other cannot:

| Action                                  | Client SDK                                                  | Room Service API                                                                         |
| --------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Publish and unpublish tracks            | Its own tracks                                              | No direct operation, but revoking `canPublish` with `UpdateParticipant` unpublishes them |
| Mute a track                            | Its own tracks                                              | Any participant's tracks                                                                 |
| Update participant metadata             | Its own, with `canUpdateOwnMetadata` token grant            | Any participant's                                                                        |
| Update Room metadata                    | Not available                                               | Yes                                                                                      |
| Disconnect a participant                | Itself, by leaving                                          | Any participant                                                                          |
| Create a Room                           | Implicitly, by connecting to a Room that does not exist yet | Explicitly, with settings                                                                |
| Delete a Room                           | Not available                                               | Yes                                                                                      |
| Change what a participant subscribes to | Its own subscriptions                                       | Any participant's subscriptions                                                          |
| Send data messages                      | Yes                                                         | Yes                                                                                      |

The same split holds beyond this API. [Egress](https://openvidu.io/3.8/docs/reference/egress/index.md) and [Ingress](https://openvidu.io/3.8/docs/reference/ingress/index.md) are server-side services as well, so a participant cannot start a recording or pull in an external stream on its own. See [*Common operations* > *From your application server*](https://openvidu.io/3.8/docs/build-your-app/common-operations/#from-your-application-server) for a list of every operation that only exists on the server side.

## Related

- [Access tokens reference](https://openvidu.io/3.8/docs/reference/access-tokens/index.md): the access token grants in detail
- [Common operations](https://openvidu.io/3.8/docs/build-your-app/common-operations/index.md): the cheat sheet of every operation, client-side and server-side
- [Application server tutorials](https://openvidu.io/3.8/docs/tutorials/application-server/index.md): complete servers in nine languages
- [Client SDK reference](https://openvidu.io/3.8/docs/reference/client-sdk/index.md): the same Room, seen from inside
