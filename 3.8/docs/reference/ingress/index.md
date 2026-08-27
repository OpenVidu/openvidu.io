# Ingress

**Ingress** brings media from outside into a Room. A streamer pushing RTMP from OBS, a WHIP endpoint publishing over WebRTC, a video file pulled from a URL, an IP camera: Ingress takes what arrives, transcodes it (or relays it untouched) and publishes it into the Room as a regular participant, so everyone subscribes to it like any other track.

Your application server creates the Ingress up front. The API returns a URL and, for push inputs, a stream key. Whoever is broadcasting points their encoder at those.

## Input types

| Input        | What it is                                                                                                                                                    |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RTMP_INPUT` | OpenVidu exposes an RTMP endpoint. The broadcaster pushes to the returned `rtmp://` URL using the returned `stream_key`. Always transcoded                    |
| `WHIP_INPUT` | OpenVidu exposes a WHIP endpoint, so the broadcaster publishes over WebRTC. The only input that can skip transcoding                                          |
| `URL_INPUT`  | OpenVidu **pulls** media from a URL you supply, rather than waiting to be pushed to. Supports HLS streams and media files (MP4, MOV, MKV/WebM, OGG, MP3, M4A) |

The full enum is [`IngressInput`](https://docs.livekit.io/reference/other/ingress/api/#ingressinput) .

IP cameras

RTSP cameras are ingested through `URL_INPUT`, passing the camera's `rtsp://` URL. There is a worked example in eight languages under [IP Cameras](https://openvidu.io/3.8/docs/build-your-app/common-operations/#ip-cameras).

### Push and pull workflows

The two families have different lifecycles, and this is the first thing to get right.

A **push** Ingress (`RTMP_INPUT`, `WHIP_INPUT`) waits for the broadcaster:

1. You create the Ingress. It returns a URL and a stream key.
1. Your user configures those in their streaming software and starts streaming.
1. Ingress transcodes the incoming media, or forwards it unchanged when transcoding is disabled.
1. Ingress joins the Room and publishes the media.
1. When the broadcaster disconnects, the Ingress participant leaves the Room. The Ingress itself stays valid in a disconnected state, so the same URL and stream key can be reused for the next session.

A **pull** Ingress (`URL_INPUT`) starts on its own:

1. You create the Ingress, and Ingress immediately starts fetching and transcoding the media.
1. Ingress joins the Room and publishes it.
1. When the media has been fully consumed, or you call `DeleteIngress`, the participant leaves the Room.

## Creating an Ingress

Ingress are created by making a request to the [Ingress API](https://docs.livekit.io/reference/other/ingress/api/) from your application server. Requests to the Ingress API require a token with the [`ingressAdmin` grant](https://openvidu.io/3.8/docs/reference/access-tokens/#video-grants) (any LiveKit server SDK automatically generates it from your `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`).

The example below creates an RTMP Ingress that publishes into `"my-room"`:

**Node.js**

Using [LiveKit Node SDK](https://docs.livekit.io/server-sdk-js/)

```javascript
import { IngressClient, IngressInput } from 'livekit-server-sdk';

const ingressClient = new IngressClient('https://my-openvidu-host', 'api-key', 'api-secret');

const ingress = await ingressClient.createIngress(IngressInput.RTMP_INPUT, {
  name: 'my-ingress',
  roomName: 'my-room',
  participantIdentity: 'my-participant',
  participantName: 'My Participant'
});

// ingress.url and ingress.streamKey are the endpoint the broadcaster pushes to
```

**Go**

Using [LiveKit Go SDK](https://pkg.go.dev/github.com/livekit/server-sdk-go/v2)

```go
import (
  "context"

  livekit "github.com/livekit/protocol/livekit"
  lksdk "github.com/livekit/server-sdk-go/v2"
)

ingressClient := lksdk.NewIngressClient(
    "https://my-openvidu-host",
    "api-key",
    "api-secret",
)

ingressRequest := &livekit.CreateIngressRequest{
    InputType:           livekit.IngressInput_RTMP_INPUT,
    Name:                "my-ingress",
    RoomName:            "my-room",
    ParticipantIdentity: "my-participant",
    ParticipantName:     "My Participant",
}

ingressInfo, err := ingressClient.CreateIngress(context.Background(), ingressRequest)
// ingressInfo.Url and ingressInfo.StreamKey are the endpoint the broadcaster pushes to
```

**Ruby**

Using [LiveKit Ruby SDK](https://github.com/livekit/server-sdk-ruby)

```ruby
require 'livekit'

ingressClient = LiveKit::IngressServiceClient.new("https://my-openvidu-host", api_key: "api-key", api_secret: "api-secret")

response = ingressClient.create_ingress(
  :RTMP_INPUT,
  name: "my-ingress",
  room_name: "my-room",
  participant_identity: "my-participant",
  participant_name: "My Participant"
)
ingressInfo = response.data
# ingressInfo.url and ingressInfo.stream_key are the endpoint the broadcaster pushes to
```

**Java**

Using [LiveKit Kotlin SDK](https://github.com/livekit/server-sdk-kotlin)

```java
import io.livekit.server.IngressServiceClient;
import livekit.LivekitIngress.IngressInfo;
import livekit.LivekitIngress.IngressInput;

IngressServiceClient ingressService = IngressServiceClient.createClient("https://my-openvidu-host", "api-key", "api-secret");

IngressInfo ingressInfo = ingressService.createIngress(
    "my-ingress", // Ingress name
    "my-room", // Room name
    "my-participant", // Ingress participant identity
    "My Participant", // Ingress participant name
    IngressInput.RTMP_INPUT // Ingress input type
).execute().body();

// ingressInfo.getUrl() and ingressInfo.getStreamKey() are the endpoint the broadcaster pushes to
```

**Python**

Using [LiveKit Python SDK](https://github.com/livekit/python-sdks)

```python
from livekit.api import LiveKitAPI, CreateIngressRequest, IngressInput

lkapi = LiveKitAPI(
    url="https://my-openvidu-host", api_key="api-key", api_secret="api-secret"
)
request = CreateIngressRequest(
    input_type=IngressInput.RTMP_INPUT,
    name="my-ingress",
    room_name="my-room",
    participant_identity="my-participant",
    participant_name="My Participant",
)
ingress_info = await lkapi.ingress.create_ingress(request)
# ingress_info.url and ingress_info.stream_key are the endpoint the broadcaster pushes to
```

**Rust**

Using [LiveKit Rust SDK](https://github.com/livekit/rust-sdks)

```rust
use livekit_api::services::ingress::{CreateIngressOptions, IngressClient};
use livekit_protocol::IngressInput;

let ingress_client = IngressClient::with_api_key(
    "https://my-openvidu-host",
    "api-key",
    "api-secret",
);
let ingress_info = ingress_client.create_ingress(
    IngressInput::RtmpInput,
    CreateIngressOptions {
        name: "my-ingress".to_string(),
        room_name: "my-room".to_string(),
        participant_identity: "my-participant".to_string(),
        participant_name: "My Participant".to_string(),
        ..Default::default()
    }).await?;
// ingress_info.url and ingress_info.stream_key are the endpoint the broadcaster pushes to
```

**PHP**

Using [LiveKit PHP SDK](https://github.com/agence104/livekit-server-sdk-php)

```php
<?php
use Agence104\LiveKit\IngressServiceClient;
use Livekit\IngressInput;

$ingressClient = new IngressServiceClient("https://my-openvidu-host", "api-key", "api-secret");
$ingressInfo = $ingressClient->createIngress(
  IngressInput::RTMP_INPUT,
  "my-ingress", // Ingress name
  "my-room", // Room name
  "my-participant", // Ingress participant identity
  "My Participant" // Ingress participant name
);
// $ingressInfo->getUrl() and $ingressInfo->getStreamKey() are the endpoint the broadcaster pushes to
```

**.NET**

Using [LiveKit .NET SDK](https://github.com/pabloFuente/livekit-server-sdk-dotnet)

```csharp
using Livekit.Server.Sdk.Dotnet;

IngressServiceClient ingressClient = new IngressServiceClient(
    "https://my-openvidu-host",
    "api-key",
    "api-secret"
);
var ingressInfo = await ingressClient.CreateIngress(new CreateIngressRequest
{
    InputType = IngressInput.RtmpInput,
    Name = "my-ingress",
    RoomName = "my-room",
    ParticipantIdentity = "my-participant",
    ParticipantName = "My Participant",
});
// ingressInfo.Url and ingressInfo.StreamKey are the endpoint the broadcaster pushes to
```

**Server API**

If your backend technology does not have its own SDK, you have two options:

1. Call the [Server API](https://openvidu.io/3.8/docs/reference/room-service-api/index.md) directly. `CreateIngress` is a POST to `/twirp/livekit.Ingress/CreateIngress`, authenticated with a token carrying the `ingressAdmin` [grant](https://openvidu.io/3.8/docs/reference/access-tokens/#video-grants):

   ```bash
   curl -X POST 'https://my-openvidu-host/twirp/livekit.Ingress/CreateIngress' \
     -H 'Authorization: Bearer <TOKEN>' \
     -H 'Content-Type: application/json' \
     -d '{
           "input_type": "RTMP_INPUT",
           "name": "my-ingress",
           "room_name": "my-room",
           "participant_identity": "my-participant",
           "participant_name": "My Participant"
         }'
   ```

1. Use the [livekit-cli](https://docs.livekit.io/home/cli/cli-setup/) :

   Create a file at `ingress.json` with the following content:

   ```json
   {
     "input_type": "RTMP_INPUT",
     "name": "my-ingress",
     "room_name": "my-room",
     "participant_identity": "my-participant",
     "participant_name": "My Participant"
   }
   ```

   Then run the following commands:

   ```bash
   export LIVEKIT_URL=https://my-openvidu-host
   export LIVEKIT_API_KEY=api-key
   export LIVEKIT_API_SECRET=api-secret

   lk ingress create ingress.json
   ```

The response is an [`IngressInfo`](https://docs.livekit.io/reference/other/ingress/api/#ingressinfo) . For push inputs it carries the `url` and `stream_key` the broadcaster points their encoder at.

These are the fields of the create request:

| Field                  | Notes                                                                                                                                                      |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `input_type`           | One of the three input types above                                                                                                                         |
| `url`                  | Where to pull media from. `URL_INPUT` only                                                                                                                 |
| `name`                 | Your own label for this Ingress                                                                                                                            |
| `room_name`            | The Room to publish into                                                                                                                                   |
| `participant_identity` | Identity the Ingress publishes as. Same uniqueness rules as any [participant identity](https://openvidu.io/3.8/docs/reference/access-tokens/#token-claims) |
| `participant_name`     | Display name of the publishing participant                                                                                                                 |
| `participant_metadata` | Metadata attached to the publishing participant                                                                                                            |
| `enable_transcoding`   | Whether to re-encode the incoming media. See [Transcoding](#transcoding)                                                                                   |
| `audio`                | [`IngressAudioOptions`](https://docs.livekit.io/reference/other/ingress/api/#ingressaudiooptions) : track name, source, and a preset or explicit options   |
| `video`                | [`IngressVideoOptions`](https://docs.livekit.io/reference/other/ingress/api/#ingressvideooptions) : the same, for video                                    |
| `enabled`              | Defaults to `true`. Set it to `false` to reject new connection attempts without deleting the Ingress                                                       |

## Transcoding

Ingress can re-encode incoming media before publishing it, so that every subscriber can consume it. When it transcodes, it publishes simulcast layers by default, which is what lets viewers on poor connections get a lower layer.

Whether it transcodes depends on the input:

- **RTMP and URL inputs are always transcoded.** They arrive as a single non-simulcast stream that has to be re-encoded to be useful in a Room.
- **WHIP forwards media unmodified by default.** WHIP is already WebRTC, so relaying it straight through gives the lowest possible latency. The cost is that the broadcaster's own encoder settings are what every subscriber gets, so it should publish simulcast itself. Set `enable_transcoding` to `true` when it cannot.

### Presets

The simplest way to configure transcoding is a preset, which fixes codec, dimensions, framerate, bitrate and, for video, the whole set of simulcast layers.

Video presets ([`IngressVideoEncodingPreset`](https://docs.livekit.io/reference/other/ingress/api/#ingressvideoencodingpreset) ), all H.264:

| Preset                                  | Resolution | FPS | Main-layer bitrate | Layers |
| --------------------------------------- | ---------- | --- | ------------------ | ------ |
| `H264_720P_30FPS_3_LAYERS`              | 1280×720   | 30  | 1900 kbps          | 3      |
| `H264_1080P_30FPS_3_LAYERS`             | 1920×1080  | 30  | 3500 kbps          | 3      |
| `H264_540P_25FPS_2_LAYERS`              | 960×540    | 25  | 1000 kbps          | 2      |
| `H264_720P_30FPS_1_LAYER`               | 1280×720   | 30  | 1900 kbps          | 1      |
| `H264_1080P_30FPS_1_LAYER`              | 1920×1080  | 30  | 3500 kbps          | 1      |
| `H264_720P_30FPS_3_LAYERS_HIGH_MOTION`  | 1280×720   | 30  | 2500 kbps          | 3      |
| `H264_1080P_30FPS_3_LAYERS_HIGH_MOTION` | 1920×1080  | 30  | 4500 kbps          | 3      |
| `H264_540P_25FPS_2_LAYERS_HIGH_MOTION`  | 960×540    | 25  | 1300 kbps          | 2      |
| `H264_720P_30FPS_1_LAYER_HIGH_MOTION`   | 1280×720   | 30  | 2500 kbps          | 1      |
| `H264_1080P_30FPS_1_LAYER_HIGH_MOTION`  | 1920×1080  | 30  | 4500 kbps          | 1      |

The `HIGH_MOTION` variants spend more bitrate at the same resolution. Reach for them when the source is hard to encode, such as sport or gameplay. For a static presentation or a talking head the standard presets are enough.

Audio presets ([`IngressAudioEncodingPreset`](https://docs.livekit.io/reference/other/ingress/api/#ingressaudioencodingpreset) ):

| Preset               | Codec                     |
| -------------------- | ------------------------- |
| `OPUS_STEREO_96KBPS` | OPUS, 2 channels, 96 kbps |
| `OPUS_MONO_64KBS`    | OPUS, 1 channel, 64 kbps  |

### Custom encoding options

If no preset fits, set explicit options instead of a preset. Note that with custom video options **you define the simulcast layers yourself**: when `layers` is empty, Ingress publishes a single layer plus the usual half and quarter dimensions.

| Options                                                                                                           | Fields                                                                                                       |
| ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [`IngressVideoEncodingOptions`](https://docs.livekit.io/reference/other/ingress/api/#ingressvideoencodingoptions) | `video_codec`, `frame_rate` and `layers`, an array of `VideoLayer` (`quality`, `width`, `height`, `bitrate`) |
| [`IngressAudioEncodingOptions`](https://docs.livekit.io/reference/other/ingress/api/#ingressaudioencodingoptions) | `audio_codec`, `bitrate`, `channels` and `disable_dtx`                                                       |

## Configuring the encoder

Whatever software the broadcaster uses, it needs the same two values from the [`IngressInfo`](https://docs.livekit.io/reference/other/ingress/api/#ingressinfo) : the `url` and the `stream_key`.

- **OBS Studio**: in **Settings > Stream**, pick the `Custom...` service, put the `url` in **Server** and the `stream_key` in **Stream Key**.

- **FFmpeg**: append the stream key to the URL and publish with the `flv` muxer.

  ```bash
  ffmpeg -re -i my-video.mp4 \
    -c:v libx264 -b:v 3M -preset veryfast -profile:v high \
    -c:a libfdk_aac -b:a 128k \
    -f flv "rtmp://my-openvidu-host/x/my-stream-key"
  ```

- **GStreamer**: supports both RTMP (`rtmp2sink`) and WHIP (`whipsink`), the latter requiring the `nicesink`, `webrtcbin` and `whipsink` plugins.

Full command lines for each: [Encoder configuration](https://docs.livekit.io/transport/media/ingress-egress/ingress/encoders/) .

## Ingress lifecycle

### Managing an Ingress

| Operation                                                                             | What it does                                                                                                                    |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| [`CreateIngress`](https://docs.livekit.io/reference/other/ingress/api/#createingress) | Creates one and returns its URL and stream key                                                                                  |
| [`ListIngress`](https://docs.livekit.io/reference/other/ingress/api/#listingress)     | Lists Ingress, filtered by Room or by `ingress_id`                                                                              |
| [`UpdateIngress`](https://docs.livekit.io/reference/other/ingress/api/#updateingress) | Changes an existing Ingress: Room, participant details, options, `enabled`. Only a reusable Ingress (RTMP, WHIP) can be updated |
| [`DeleteIngress`](https://docs.livekit.io/reference/other/ingress/api/#deleteingress) | Removes one, disconnecting it from the Room                                                                                     |

### IngressInfo

Every operation above returns an [`IngressInfo`](https://docs.livekit.io/reference/other/ingress/api/#ingressinfo) , and so does every Ingress webhook. It describes the Ingress and how to connect to it:

```json
{
  "ingressId": "IN_AbCdEfGhIjKl",
  "name": "my-ingress",
  "streamKey": "GHtwLbmMChLR",
  "url": "rtmp://my-openvidu-host:1935/x",
  "inputType": "RTMP_INPUT",
  "enableTranscoding": true,
  "roomName": "my-room",
  "participantIdentity": "my-participant",
  "participantName": "My Participant",
  "reusable": true,
  "enabled": true,
  "state": {
    "status": "ENDPOINT_PUBLISHING",
    "roomId": "RM_GmENxWJemFqL",
    "startedAt": "1755640000000000000"
  }
}
```

The fields that matter most:

- `ingressId`: the identifier every operation above takes.
- `url` and `streamKey`: what the broadcaster configures. Treat the stream key as a credential.
- `reusable`: whether the endpoint accepts a new session after one ends. True for push inputs, which is what lets a broadcaster reconnect to the same URL.
- `state`: describes current endpoint status, errors, and input media state. It is an object of type [`IngressState`](https://docs.livekit.io/reference/other/ingress/api/#ingressstate) and carries the most important information about the media actually arriving for the Ingress endpoint.

### Webhooks

Two [webhook events](https://openvidu.io/3.8/docs/reference/webhooks/#events) track an Ingress, both carrying the full `ingressInfo`:

| Event             | Fires when                                 |
| ----------------- | ------------------------------------------ |
| `ingress_started` | The Ingress began publishing into the Room |
| `ingress_ended`   | It stopped                                 |

An Ingress publishing into a Room also produces ordinary participant and track events: a `participant_joined` for the Ingress participant, and a `track_published` per track.

## Related

- [IP Cameras](https://openvidu.io/3.8/docs/build-your-app/common-operations/#ip-cameras): RTSP ingest in eight languages.
- [Stream ingestion](https://openvidu.io/3.8/docs/build-your-app/common-operations/#stream-ingestion): choosing between the input types.
- [Access tokens reference](https://openvidu.io/3.8/docs/reference/access-tokens/index.md): the `ingressAdmin` grant gates these operations.
- [Webhooks reference](https://openvidu.io/3.8/docs/reference/webhooks/index.md): the Ingress events and their payloads.
- [Egress reference](https://openvidu.io/3.8/docs/reference/egress/index.md): media in the other direction.
