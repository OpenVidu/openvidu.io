---
title: "OpenVidu server API reference"
description: "Every room and participant operation your backend can call, the grant each one requires, and how the API is authenticated."
---

# Room Service API

The Room Service API is what your **application server** uses to manage Rooms from the outside: create and delete them, list who is in them, mute a track, remove a participant, push data into a Room. It is the counterpart to the [client SDKs](client-sdk.md), which act from *inside* a Room as a participant.

The API is **Twirp-based HTTP** (plain `POST` requests with a JSON body) so any language can call it. OpenVidu is API-compatible with LiveKit, so any LiveKit server SDK can be used to manage Rooms. Visit the LiveKit docs for a complete reference of the Room Service API:

[:octicons-arrow-right-24: **LiveKit docs** :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/){:target="_blank"}

## Calling the API

Each server SDK exposes the same operations through a RoomService client, built with your deployment URL, API key and API secret. The SDK signs an [access token](./access-tokens.md) with the administrative grants of each operation for you, so a server-side token never leaves your backend. For example, removing a participant:

=== ":simple-nodedotjs:{.icon .lg-icon .tab-icon} Node.js"

    Using [LiveKit Node SDK :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/server-sdk-js/){:target="_blank"}

    ```javascript
    import { RoomServiceClient } from 'livekit-server-sdk';

    const roomClient = new RoomServiceClient('https://my-openvidu-host', 'api-key', 'api-secret');

    await roomClient.removeParticipant('my-room', 'my-participant');
    ```

=== ":simple-goland:{.icon .lg-icon .tab-icon} Go"

    Using [LiveKit Go SDK :fontawesome-solid-external-link:{.external-link-icon}](https://pkg.go.dev/github.com/livekit/server-sdk-go/v2){:target="_blank"}

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

=== ":simple-ruby:{.icon .lg-icon .tab-icon} Ruby"

    Using [LiveKit Ruby SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/server-sdk-ruby){:target="_blank"}

    ```ruby
    require 'livekit'

    roomClient = LiveKit::RoomServiceClient.new("https://my-openvidu-host", api_key: "api-key", api_secret: "api-secret")

    roomClient.remove_participant(room: "my-room", identity: "my-participant")
    ```

=== ":fontawesome-brands-java:{.icon .lg-icon .tab-icon} Java"

    Using [LiveKit Kotlin SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/server-sdk-kotlin){:target="_blank"}

    ```java
    import io.livekit.server.RoomServiceClient;

    RoomServiceClient roomClient = RoomServiceClient.createClient("https://my-openvidu-host", "api-key", "api-secret");

    roomClient.removeParticipant("my-room", "my-participant").execute();
    ```

=== ":fontawesome-brands-python:{.icon .lg-icon .tab-icon} Python"

    Using [LiveKit Python SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/python-sdks){:target="_blank"}

    ```python
    from livekit.api import LiveKitAPI, RoomParticipantIdentity

    lkapi = LiveKitAPI(
        url="https://my-openvidu-host", api_key="api-key", api_secret="api-secret"
    )
    await lkapi.room.remove_participant(
        RoomParticipantIdentity(room="my-room", identity="my-participant")
    )
    ```

=== ":simple-rust:{.icon .lg-icon .tab-icon} Rust"

    Using [LiveKit Rust SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/rust-sdks){:target="_blank"}

    ```rust
    use livekit_api::services::room::RoomClient;

    let room_client = RoomClient::with_api_key(
        "https://my-openvidu-host",
        "api-key",
        "api-secret",
    );
    room_client.remove_participant("my-room", "my-participant").await?;
    ```

=== ":simple-php:{.icon .lg-icon .tab-icon} PHP"

    Using [LiveKit PHP SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/agence104/livekit-server-sdk-php){:target="_blank"}

    ```php
    <?php
    use Agence104\LiveKit\RoomServiceClient;

    $room_client = new RoomServiceClient("https://my-openvidu-host", "api-key", "api-secret");

    $room_client->removeParticipant("my-room", "my-participant");
    ```

=== ":simple-dotnet:{.icon .lg-icon .tab-icon} .NET"

    Using [LiveKit .NET SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/pabloFuente/livekit-server-sdk-dotnet){:target="_blank"}

    ```csharp
    using Livekit.Server.Sdk.Dotnet;

    var roomClient = new RoomServiceClient("https://my-openvidu-host", "api-key", "api-secret");

    await roomClient.RemoveParticipant(new RoomParticipantIdentity
    {
        Room = "my-room",
        Identity = "my-participant",
    });
    ```

=== ":material-api:{.icon .lg-icon .tab-icon} Server API"

    If your backend technology does not have its own SDK, you have two options:

    1. Call the Room Service API directly. Every operation is a POST to `/twirp/livekit.RoomService/<Operation>`, with `Content-Type: application/json` and an [access token](./access-tokens.md) in the `Authorization` header. Parameters travel in a JSON body, accepted in both `snake_case` and `camelCase`, and operations that take none receive `{}`. The [Egress](./egress.md) and [Ingress](./ingress.md) modules expose their own services the same way, at `/twirp/livekit.Egress/` and `/twirp/livekit.Ingress/`:

        ```bash
        curl -X POST 'https://my-openvidu-host/twirp/livekit.RoomService/RemoveParticipant' \
          -H 'Authorization: Bearer <TOKEN>' \
          -H 'Content-Type: application/json' \
          -d '{
                "room": "my-room",
                "identity": "my-participant"
              }'
        ```

    2. Use the [livekit-cli :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/home/cli/cli-setup/){:target="_blank"}:

        ```bash
        export LIVEKIT_URL=https://my-openvidu-host
        export LIVEKIT_API_KEY=api-key
        export LIVEKIT_API_SECRET=api-secret

        lk room participants remove --room my-room --identity my-participant
        ```

You can check out the type definitions for the responses in the [LiveKit reference docs :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#types){:target="_blank"}.

For example, `ListParticipants` operation returns a list of [`ParticipantInfo` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#participantinfo){:target="_blank"} objects:

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

<div class="nowrap-first-column" markdown>

| Operation | Grant | Return type | What it does |
| --- | --- | --- | --- |
| [`CreateRoom` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#createroom){:target="_blank"} | `roomCreate` | [`Room` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#room){:target="_blank"} | Creates a Room with explicit settings. This operation is optional, as Rooms can be created automatically the first time a participant connects to it |
| [`ListRooms` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#listrooms){:target="_blank"} | `roomList` | List of [`Room` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#room){:target="_blank"} | Lists the Rooms currently active on the server |
| [`DeleteRoom` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#deleteroom){:target="_blank"} | `roomCreate` | Empty | Deletes a Room, disconnecting every participant in it in the process |
| [`UpdateRoomMetadata` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#updateroommetadata){:target="_blank"} | `roomAdmin` | [`Room` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#room){:target="_blank"} | Replaces the Room's metadata. The change is broadcast to every participant |

</div>

### Participants

<div class="nowrap-first-column" markdown>

| Operation | Grant | Return type | What it does |
| --- | --- | --- | --- |
| [`ListParticipants` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#listparticipants){:target="_blank"} | `roomAdmin` | List of [`ParticipantInfo` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#participantinfo){:target="_blank"} | Lists the participants in a Room |
| [`GetParticipant` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#getparticipant){:target="_blank"} | `roomAdmin` | [`ParticipantInfo` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#participantinfo){:target="_blank"} | Returns one participant by identity |
| [`RemoveParticipant` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#removeparticipant){:target="_blank"} | `roomAdmin` | Empty | Disconnects a participant. They can reconnect with a valid token. To keep them out, stop issuing tokens |
| [`UpdateParticipant` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#updateparticipant){:target="_blank"} | `roomAdmin` | [`ParticipantInfo` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#participantinfo){:target="_blank"} | Changes a participant's metadata, name, attributes or permissions. Broadcast to the Room |
| [`MutePublishedTrack` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#mutepublishedtrack){:target="_blank"} | `roomAdmin` | [`TrackInfo` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#trackinfo){:target="_blank"} | Mutes or unmutes one of a participant's published tracks. Remote unmute additionally requires `room.enable_remote_unmute: true` in [`livekit.yaml`](../self-hosting/configuration/reference.md#livekityaml) |
| [`UpdateSubscriptions` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#updatesubscriptions){:target="_blank"} | `roomAdmin` | Empty | Subscribes or unsubscribes a participant to specific tracks, from the server side |

</div>

### Data

<div class="nowrap-first-column" markdown>

| Operation | Grant | Return type | What it does |
| --- | --- | --- | --- |
| [`SendData` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#senddata){:target="_blank"} | `roomAdmin` | Empty | Sends a data message over the data channel, with reliable or lossy delivery and an optional `topic`. Empty `destinationIdentities` sends it to the whole Room |
| `PerformRpc` | `roomAdmin` | The `payload` string returned by the participant | Invokes an RPC method that a participant has registered with its client SDK. Visit [RPC :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/transport/data/rpc/){:target="_blank"} to learn more |

</div>

## Choosing between the server API and the client SDK

Some operations exist on both sides. A participant can mute its own microphone from the client SDK, and your application server can mute that same track with `MutePublishedTrack`. What separates the two surfaces is not what they can do, but **who they can do it to**:

- The **client SDK** acts on **itself**. A participant publishes and mutes its own tracks, updates its own metadata, and leaves the Room. It can never reach another participant, and its authority is limited to what its access token grants.
- The **Room Service API** acts on **anyone**, from outside the Room. It mutes any track, disconnects any participant, changes the Room itself, and works even when nobody is connected yet. It provides an administrative and moderation control plane of Rooms, directly from your application server.

Each side can do things the other cannot:

<div class="nowrap-first-column" markdown>

| Action | Client SDK | Room Service API |
| --- | --- | --- |
| Publish and unpublish tracks | Its own tracks | No direct operation, but revoking `canPublish` with `UpdateParticipant` unpublishes them |
| Mute a track | Its own tracks | Any participant's tracks |
| Update participant metadata | Its own, with `canUpdateOwnMetadata` token grant | Any participant's |
| Update Room metadata | Not available | Yes |
| Disconnect a participant | Itself, by leaving | Any participant |
| Create a Room | Implicitly, by connecting to a Room that does not exist yet | Explicitly, with settings |
| Delete a Room | Not available | Yes |
| Change what a participant subscribes to | Its own subscriptions | Any participant's subscriptions |
| Send data messages | Yes | Yes |

</div>

The same split holds beyond this API. [Egress](./egress.md) and [Ingress](./ingress.md) are server-side services as well, so a participant cannot start a recording or pull in an external stream on its own. See [_Manage Rooms_ > _From your application server_](../developing-your-openvidu-app/how-to.md#from-your-application-server) for a list of every operation that only exists on the server side.

## Related

- [Access tokens reference](./access-tokens.md): the access token grants in detail
- [How to develop your OpenVidu app](../developing-your-openvidu-app/how-to.md): the cheat sheet of common operations, client-side and server-side
- [Application server tutorials](../tutorials/application-server/index.md): complete servers in nine languages
- [Client SDK reference](./client-sdk.md): the same Room, seen from inside
