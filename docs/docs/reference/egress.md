---
title: "OpenVidu Egress reference"
description: "Export media out of an OpenVidu Room with Egress: recording and streaming types, output formats, storage targets and the Egress lifecycle."
---

# Egress

**Egress** exports media out of a Room. Recording a meeting to MP4, streaming it to RTMP, producing HLS segments, capturing periodic thumbnails: all of it is Egress. Your application server starts and stops Egress through the API; the Egress service joins the Room as a hidden participant of kind `EGRESS` and subscribes only to the tracks it needs.

OpenVidu ships Egress already wired to the bundled S3-compatible storage, so a recording has somewhere to land with no extra setup.

For working examples, see the [recording tutorials](../tutorials/advanced-features/index.md).

## Egress types

Five request types, each starting a different kind of export:

| Type | SDK method | What it produces |
| --- | --- | --- |
| **Room Composite** | [`StartRoomCompositeEgress` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#startroomcompositeegress){:target="_blank"} | One output with every participant composited in a layout. The usual choice for "record the meeting". It follows the Room, stopping on its own when the Room ends |
| **Web** | [`StartWebEgress` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#startwebegress){:target="_blank"} | One output from an arbitrary web page URL, rather than from a Room. Nothing stops it but you |
| **Participant** | [`StartParticipantEgress` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/transport/media/ingress-egress/egress/participant/){:target="_blank"} | One output per participant, identified by `identity`. It waits for them to publish, copes with tracks being muted or unpublished, and stops when they leave. Set `screen_share` to capture their screen share instead of their camera |
| **Track Composite** | [`StartTrackCompositeEgress` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#starttrackcompositeegress){:target="_blank"} | One output combining a chosen audio track and video track, selected by track id. Both must already be published when the Egress starts |
| **Track** | [`StartTrackEgress` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#starttrackegress){:target="_blank"} | One output per individual track, written without transcoding |

!!! warning "Egress and transcoding"

    Egress is a heavy operation. It consumes lots of CPU, many orders of magnitude more CPU cycles than the rooms themselves. **Track Egress** is the only type that does not transcode: it directly dumps the published track to the server as-is. Use it if possible to reduce hardware requirements.

## Starting an Egress

Egress are started by making a request to the [Egress API :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/){:target="_blank"} from your application server. Requests to the Egress API require a token with the [`roomRecord` grant](./access-tokens.md#video-grants) (any LiveKit server SDK automatically generates it from your `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`).

The example below records `"my-room"` to an MP4 file. The output carries no explicit upload target, so OpenVidu sends it to the bundled MinIO S3 storage:

=== ":simple-nodedotjs:{.icon .lg-icon .tab-icon} Node.js"

    Using [LiveKit Node SDK :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/server-sdk-js/){:target="_blank"}

    ```javascript
    import { EgressClient, EncodedFileOutput, EncodedFileType } from 'livekit-server-sdk';

    const egressClient = new EgressClient('https://my-openvidu-host', 'api-key', 'api-secret');

    const fileOutput = new EncodedFileOutput({
      fileType: EncodedFileType.MP4,
      filepath: 'my-room-recording.mp4'
    });

    const egressInfo = await egressClient.startRoomCompositeEgress('my-room', { file: fileOutput }, { layout: 'grid' });
    ```

=== ":simple-goland:{.icon .lg-icon .tab-icon} Go"

    Using [LiveKit Go SDK :fontawesome-solid-external-link:{.external-link-icon}](https://pkg.go.dev/github.com/livekit/server-sdk-go/v2){:target="_blank"}

    ```go
    import (
      "context"

      livekit "github.com/livekit/protocol/livekit"
      lksdk "github.com/livekit/server-sdk-go/v2"
    )

    egressClient := lksdk.NewEgressClient("https://my-openvidu-host", "api-key", "api-secret")

    egressInfo, err := egressClient.StartRoomCompositeEgress(context.Background(), &livekit.RoomCompositeEgressRequest{
        RoomName: "my-room",
        Layout:   "grid",
        FileOutputs: []*livekit.EncodedFileOutput{{
            FileType: livekit.EncodedFileType_MP4,
            Filepath: "my-room-recording.mp4",
        }},
    })
    ```

=== ":simple-ruby:{.icon .lg-icon .tab-icon} Ruby"

    Using [LiveKit Ruby SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/server-sdk-ruby){:target="_blank"}

    ```ruby
    require 'livekit'

    egress_client = LiveKit::EgressServiceClient.new("https://my-openvidu-host", api_key: "api-key", api_secret: "api-secret")

    output = LiveKit::Proto::EncodedFileOutput.new(
      file_type: LiveKit::Proto::EncodedFileType::MP4,
      filepath: "my-room-recording.mp4"
    )
    egress_info = egress_client.start_room_composite_egress("my-room", output, layout: "grid")
    ```

=== ":fontawesome-brands-java:{.icon .lg-icon .tab-icon} Java"

    Using [LiveKit Kotlin SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/server-sdk-kotlin){:target="_blank"}

    ```java
    import io.livekit.server.EgressServiceClient;
    import livekit.LivekitEgress;

    EgressServiceClient egressClient = EgressServiceClient.createClient("https://my-openvidu-host", "api-key", "api-secret");

    LivekitEgress.EncodedFileOutput fileOutput = LivekitEgress.EncodedFileOutput.newBuilder()
            .setFileType(LivekitEgress.EncodedFileType.MP4)
            .setFilepath("my-room-recording.mp4")
            .build();

    LivekitEgress.EgressInfo egressInfo = egressClient
            .startRoomCompositeEgress("my-room", fileOutput, "grid")
            .execute().body();
    ```

=== ":fontawesome-brands-python:{.icon .lg-icon .tab-icon} Python"

    Using [LiveKit Python SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/python-sdks){:target="_blank"}

    ```python
    from livekit import api

    lkapi = api.LiveKitAPI(
        url="https://my-openvidu-host", api_key="api-key", api_secret="api-secret"
    )
    egress_info = await lkapi.egress.start_room_composite_egress(
        api.RoomCompositeEgressRequest(
            room_name="my-room",
            layout="grid",
            file_outputs=[api.EncodedFileOutput(
                file_type=api.EncodedFileType.MP4,
                filepath="my-room-recording.mp4",
            )],
        )
    )
    ```

=== ":simple-rust:{.icon .lg-icon .tab-icon} Rust"

    Using [LiveKit Rust SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/rust-sdks){:target="_blank"}

    ```rust
    use livekit_api::services::egress::{EgressClient, EgressOutput, RoomCompositeOptions};
    use livekit_protocol as proto;

    let egress_client = EgressClient::with_api_key(
        "https://my-openvidu-host",
        "api-key",
        "api-secret",
    );

    let file_output = proto::EncodedFileOutput {
        file_type: proto::EncodedFileType::Mp4 as i32,
        filepath: "my-room-recording.mp4".to_string(),
        ..Default::default()
    };

    let egress_info = egress_client.start_room_composite_egress(
        "my-room",
        vec![EgressOutput::File(file_output)],
        RoomCompositeOptions {
            layout: "grid".to_string(),
            ..Default::default()
        },
    ).await?;
    ```

=== ":simple-php:{.icon .lg-icon .tab-icon} PHP"

    Using [LiveKit PHP SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/agence104/livekit-server-sdk-php){:target="_blank"}

    ```php
    <?php
    use Agence104\LiveKit\EgressServiceClient;
    use Livekit\EncodedFileOutput;
    use Livekit\EncodedFileType;

    $egressClient = new EgressServiceClient("https://my-openvidu-host", "api-key", "api-secret");

    $fileOutput = new EncodedFileOutput([
        'file_type' => EncodedFileType::MP4,
        'filepath' => 'my-room-recording.mp4',
    ]);
    $egressInfo = $egressClient->startRoomCompositeEgress('my-room', 'grid', $fileOutput);
    ```

=== ":simple-dotnet:{.icon .lg-icon .tab-icon} .NET"

    Using [LiveKit .NET SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/pabloFuente/livekit-server-sdk-dotnet){:target="_blank"}

    ```csharp
    using Livekit.Server.Sdk.Dotnet;

    var egressClient = new EgressServiceClient("https://my-openvidu-host", "api-key", "api-secret");

    var request = new RoomCompositeEgressRequest { RoomName = "my-room", Layout = "grid" };
    request.FileOutputs.Add(new EncodedFileOutput
    {
        FileType = EncodedFileType.Mp4,
        Filepath = "my-room-recording.mp4",
    });
    EgressInfo egressInfo = await egressClient.StartRoomCompositeEgress(request);
    ```

=== ":material-api:{.icon .lg-icon .tab-icon} Server API"

    If your backend technology does not have its own SDK, you have two options:

    1. Call the [Egress API :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/){:target="_blank"} directly. `StartRoomCompositeEgress` is a POST to `/twirp/livekit.Egress/StartRoomCompositeEgress`, authenticated with a token carrying the [`roomRecord` grant](./access-tokens.md#video-grants):

        ```bash
        curl -X POST 'https://my-openvidu-host/twirp/livekit.Egress/StartRoomCompositeEgress' \
          -H 'Authorization: Bearer <TOKEN>' \
          -H 'Content-Type: application/json' \
          -d '{
                "room_name": "my-room",
                "layout": "grid",
                "file_outputs": [
                  { "file_type": "MP4", "filepath": "my-room-recording.mp4" }
                ]
              }'
        ```

    2. Use the [livekit-cli :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/intro/basics/cli/){:target="_blank"}:

        Create a file at `egress.json` with the following content:

        ```json
        {
          "room_name": "my-room",
          "layout": "grid",
          "file_outputs": [
            {
              "file_type": "MP4",
              "filepath": "my-room-recording.mp4"
            }
          ]
        }
        ```

        Then run the following commands:

        ```bash
        export LIVEKIT_URL=https://my-openvidu-host
        export LIVEKIT_API_KEY=api-key
        export LIVEKIT_API_SECRET=api-secret

        lk egress start --type room-composite egress.json
        ```

## Outputs

Egress can write to files, push RTMP and SRT streams, generate HLS segments and capture still images (thumbnails).

A transcoded Egress encodes once and fans out, so a single request can write a file, push a stream and generate thumbnails at the same time. Which outputs are available depends on the type of egress:

| Egress type | File | HLS segments | RTMP / SRT stream | Images | WebSocket |
| --- | :---: | :---: | :---: | :---: | :---: |
| Room Composite, Web, Participant, Track Composite | ✅ | ✅ | ✅ | ✅ | |
| Track | ✅ (pass-through, as published) | | | | ✅ (audio only) |

Set one or more of these fields on the start egress request:

<div class="nowrap-first-column" markdown>

| Field | Produces | Type |
| --- | --- | --- |
| `file_outputs` | A single media file | [`EncodedFileOutput` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#encodedfileoutput){:target="_blank"} |
| `stream_outputs` | A live stream pushed to one or more URLs | [`StreamOutput` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#streamoutput){:target="_blank"} |
| `segment_outputs` | Segmented output plus a playlist (HLS) | [`SegmentedFileOutput` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#segmentedfileoutput){:target="_blank"} |
| `image_outputs` | Still images captured at an interval. You can use it to generate thumbnails | [`ImageOutput` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#imageoutput){:target="_blank"} |

</div>

Each list holds a single item: one Egress cannot write two files, but it can write a file *and* HLS segments *and* a stream. Track Egress is the exception, taking neither these lists nor encoding options, just a `file` ([`DirectFileOutput` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#directfileoutput){:target="_blank"}) or a `websocket_url`.

Because Track Egress never transcodes, the container follows the codec the track was published with: MP4 for H.264, WebM for VP8 and Ogg for Opus. With a `websocket_url` instead of a file, an audio track is streamed to a server of yours as raw `pcm_s16le` binary frames, with JSON text frames such as `{"muted": true}` reporting track events. The connection closes when the track is unpublished.

### Filenames

When outputting to files (`file_outputs`, `segment_outputs` or `image_outputs`), you can customize the path and filename using `filepath` and `filename_prefix` fields.

Both accept template variables, though not every variable makes sense for every Egress type:

<div class="nowrap-first-column" markdown>

| Variable | Value | Available in |
| --- | --- | --- |
| `{room_name}` | Name of the Room | Room Composite, Participant, Track Composite, Track |
| `{room_id}` | Unique id of the Room | Room Composite, Participant, Track Composite, Track |
| `{time}` | Timestamp of when the recording started | Room Composite, Web, Participant, Track Composite, Track |
| `{publisher_identity}` | Identity of the participant publishing the track | Participant, Track Composite, Track |
| `{track_id}` | Unique id of the track | Track |
| `{track_type}` | `audio` or `video` | Track |
| `{track_source}` | Source of the track, such as `camera` or `microphone` | Track |

</div>

Two notes:

- With no filename, you get `{room_name}-{time}`.
- A value ending in `/` is treated as a directory, and the default filename is appended inside it.

Some examples of how the template variables are expanded:

<div class="nowrap-first-column" markdown>

| Requested filename | Resulting filename |
| --- | --- |
| `""` | `my-room-2026-08-24T173012.mp4` |
| `"recordings/"` | `recordings/my-room-2026-08-24T173012.mp4` |
| `"{room_name}/{time}"` | `my-room/2026-08-24T173012.mp4` |
| `"{track_type}_{publisher_identity}.mp4"` | `audio_my-participant.mp4` |
| `"{track_source}-{track_id}"` | `microphone-TR_VCa8sTgxQpMv.ogg` |

</div>

### Streams

Stream outputs push RTMP or SRT. URLs can be added to and removed from a running Egress with [`UpdateStream` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#updatestream){:target="_blank"}. To start an Egress that will only stream later, include a `StreamOutput` with the right `protocol` and an empty `urls` list.

!!! warning
    RTMP and SRT streaming is very sensitive to long distances. Locate your ingest endpoints close to the servers running your Egress for best results.

## Encoding

All Egress types that require transcoding (Room Composite, Web, Participant, Track Composite) can define their resolution, framerate, codecs, bitrates and more. When calling the start Egress operation, you can set encoding options in two ways:

- Using a preset: field `preset` of type [`EncodingOptionsPreset` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#encodingoptionspreset){:target="_blank"}.
- Explicitly: field `advanced` of type [`EncodingOptions` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#encodingoptions){:target="_blank"}.

For example, this starts a Room Composite Egress recording to an MP4 file with the `H264_720P_30` preset:

=== ":simple-nodedotjs:{.icon .lg-icon .tab-icon} Node.js"

    Using [LiveKit Node SDK :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/server-sdk-js/){:target="_blank"}

    ```javascript
    import { EgressClient, EncodedFileOutput, EncodedFileType, EncodingOptionsPreset } from 'livekit-server-sdk';

    const egressClient = new EgressClient('https://my-openvidu-host', 'api-key', 'api-secret');

    const fileOutput = new EncodedFileOutput({
      fileType: EncodedFileType.MP4,
      filepath: 'my-room-recording.mp4'
    });

    const egressInfo = await egressClient.startRoomCompositeEgress('my-room', { file: fileOutput }, {
      layout: 'grid',
      encodingOptions: EncodingOptionsPreset.H264_720P_30
    });
    ```

=== ":simple-goland:{.icon .lg-icon .tab-icon} Go"

    Using [LiveKit Go SDK :fontawesome-solid-external-link:{.external-link-icon}](https://pkg.go.dev/github.com/livekit/server-sdk-go/v2){:target="_blank"}

    ```go
    import (
      "context"

      livekit "github.com/livekit/protocol/livekit"
      lksdk "github.com/livekit/server-sdk-go/v2"
    )

    egressClient := lksdk.NewEgressClient("https://my-openvidu-host", "api-key", "api-secret")

    egressInfo, err := egressClient.StartRoomCompositeEgress(context.Background(), &livekit.RoomCompositeEgressRequest{
        RoomName: "my-room",
        Layout:   "grid",
        Options: &livekit.RoomCompositeEgressRequest_Preset{
            Preset: livekit.EncodingOptionsPreset_H264_720P_30,
        },
        FileOutputs: []*livekit.EncodedFileOutput{{
            FileType: livekit.EncodedFileType_MP4,
            Filepath: "my-room-recording.mp4",
        }},
    })
    ```

=== ":simple-ruby:{.icon .lg-icon .tab-icon} Ruby"

    Using [LiveKit Ruby SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/server-sdk-ruby){:target="_blank"}

    ```ruby
    require 'livekit'

    egress_client = LiveKit::EgressServiceClient.new("https://my-openvidu-host", api_key: "api-key", api_secret: "api-secret")

    output = LiveKit::Proto::EncodedFileOutput.new(
      file_type: LiveKit::Proto::EncodedFileType::MP4,
      filepath: "my-room-recording.mp4"
    )
    egress_info = egress_client.start_room_composite_egress(
      "my-room",
      output,
      layout: "grid",
      preset: LiveKit::Proto::EncodingOptionsPreset::H264_720P_30
    )
    ```

=== ":fontawesome-brands-java:{.icon .lg-icon .tab-icon} Java"

    Using [LiveKit Kotlin SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/server-sdk-kotlin){:target="_blank"}

    ```java
    import io.livekit.server.EgressServiceClient;
    import livekit.LivekitEgress;

    EgressServiceClient egressClient = EgressServiceClient.createClient("https://my-openvidu-host", "api-key", "api-secret");

    LivekitEgress.EncodedFileOutput fileOutput = LivekitEgress.EncodedFileOutput.newBuilder()
            .setFileType(LivekitEgress.EncodedFileType.MP4)
            .setFilepath("my-room-recording.mp4")
            .build();

    LivekitEgress.EgressInfo egressInfo = egressClient
            .startRoomCompositeEgress("my-room", fileOutput, "grid",
                    LivekitEgress.EncodingOptionsPreset.H264_720P_30)
            .execute().body();
    ```

=== ":fontawesome-brands-python:{.icon .lg-icon .tab-icon} Python"

    Using [LiveKit Python SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/python-sdks){:target="_blank"}

    ```python
    from livekit import api

    lkapi = api.LiveKitAPI(
        url="https://my-openvidu-host", api_key="api-key", api_secret="api-secret"
    )
    egress_info = await lkapi.egress.start_room_composite_egress(
        api.RoomCompositeEgressRequest(
            room_name="my-room",
            layout="grid",
            preset=api.EncodingOptionsPreset.H264_720P_30,
            file_outputs=[api.EncodedFileOutput(
                file_type=api.EncodedFileType.MP4,
                filepath="my-room-recording.mp4",
            )],
        )
    )
    ```

=== ":simple-rust:{.icon .lg-icon .tab-icon} Rust"

    Using [LiveKit Rust SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/rust-sdks){:target="_blank"}

    The Rust SDK does not expose presets. Set the equivalent explicit encoding options instead.

    ```rust
    use livekit_api::services::egress::encoding::EncodingOptions;
    use livekit_api::services::egress::{EgressClient, EgressOutput, RoomCompositeOptions};
    use livekit_protocol as proto;

    let egress_client = EgressClient::with_api_key(
        "https://my-openvidu-host",
        "api-key",
        "api-secret",
    );

    let file_output = proto::EncodedFileOutput {
        file_type: proto::EncodedFileType::Mp4 as i32,
        filepath: "my-room-recording.mp4".to_string(),
        ..Default::default()
    };

    let egress_info = egress_client.start_room_composite_egress(
        "my-room",
        vec![EgressOutput::File(file_output)],
        RoomCompositeOptions {
            layout: "grid".to_string(),
            encoding: EncodingOptions {
                width: 1280,
                height: 720,
                framerate: 30,
                video_bitrate: 3000,
                ..Default::default()
            },
            ..Default::default()
        },
    ).await?;
    ```

=== ":simple-php:{.icon .lg-icon .tab-icon} PHP"

    Using [LiveKit PHP SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/agence104/livekit-server-sdk-php){:target="_blank"}

    ```php
    <?php
    use Agence104\LiveKit\EgressServiceClient;
    use Livekit\EncodedFileOutput;
    use Livekit\EncodedFileType;
    use Livekit\EncodingOptionsPreset;

    $egressClient = new EgressServiceClient("https://my-openvidu-host", "api-key", "api-secret");

    $fileOutput = new EncodedFileOutput([
        'file_type' => EncodedFileType::MP4,
        'filepath' => 'my-room-recording.mp4',
    ]);
    $egressInfo = $egressClient->startRoomCompositeEgress(
        'my-room',
        'grid',
        $fileOutput,
        EncodingOptionsPreset::H264_720P_30
    );
    ```

=== ":simple-dotnet:{.icon .lg-icon .tab-icon} .NET"

    Using [LiveKit .NET SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/pabloFuente/livekit-server-sdk-dotnet){:target="_blank"}

    ```csharp
    using Livekit.Server.Sdk.Dotnet;

    var egressClient = new EgressServiceClient("https://my-openvidu-host", "api-key", "api-secret");

    var request = new RoomCompositeEgressRequest
    {
        RoomName = "my-room",
        Layout = "grid",
        Preset = EncodingOptionsPreset.H264720P30,
    };
    request.FileOutputs.Add(new EncodedFileOutput
    {
        FileType = EncodedFileType.Mp4,
        Filepath = "my-room-recording.mp4",
    });
    EgressInfo egressInfo = await egressClient.StartRoomCompositeEgress(request);
    ```

=== ":material-api:{.icon .lg-icon .tab-icon} Server API"

    If your backend technology does not have its own SDK, you have two options:

    1. Call the [Egress API :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/){:target="_blank"} directly. `StartRoomCompositeEgress` is a POST to `/twirp/livekit.Egress/StartRoomCompositeEgress`, authenticated with a token carrying the [`roomRecord` grant](./access-tokens.md#video-grants):

        ```bash
        curl -X POST 'https://my-openvidu-host/twirp/livekit.Egress/StartRoomCompositeEgress' \
          -H 'Authorization: Bearer <TOKEN>' \
          -H 'Content-Type: application/json' \
          -d '{
                "room_name": "my-room",
                "layout": "grid",
                "preset": "H264_720P_30",
                "file_outputs": [
                  { "file_type": "MP4", "filepath": "my-room-recording.mp4" }
                ]
              }'
        ```

    2. Use the [livekit-cli :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/intro/basics/cli/){:target="_blank"}:

        Create a file at `egress.json` with the following content:

        ```json
        {
          "room_name": "my-room",
          "layout": "grid",
          "preset": "H264_720P_30",
          "file_outputs": [
            {
              "file_type": "MP4",
              "filepath": "my-room-recording.mp4"
            }
          ]
        }
        ```

        Then run the following commands:

        ```bash
        export LIVEKIT_URL=https://my-openvidu-host
        export LIVEKIT_API_KEY=api-key
        export LIVEKIT_API_SECRET=api-secret

        lk egress start --type room-composite egress.json
        ```

## Where the output goes

You can send Egress output to any S3-compatible service, Google Cloud Storage, Azure Blob Storage or Alibaba Cloud OSS:

<div class="nowrap-first-column" markdown>

| Target | Type |
| --- | --- |
| `s3` | [`S3Upload` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#s3upload){:target="_blank"} |
| `gcp` | [`GCPUpload` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#gcpupload){:target="_blank"} |
| `azure` | [`AzureBlobUpload` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#azureblobupload){:target="_blank"} |
| `aliOSS` | [`AliOSSUpload` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#aliossupload){:target="_blank"} |

</div>

For example, this sends a Room Composite recording to an Azure Blob Storage container:

=== ":simple-nodedotjs:{.icon .lg-icon .tab-icon} Node.js"

    Using [LiveKit Node SDK :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/server-sdk-js/){:target="_blank"}

    ```javascript
    import { EgressClient, EncodedFileOutput, EncodedFileType, AzureBlobUpload } from 'livekit-server-sdk';

    const egressClient = new EgressClient('https://my-openvidu-host', 'api-key', 'api-secret');

    const fileOutput = new EncodedFileOutput({
      fileType: EncodedFileType.MP4,
      filepath: 'my-room-recording.mp4',
      output: {
        case: 'azure',
        value: new AzureBlobUpload({
          accountName: 'my-storage-account',
          accountKey: 'my-account-key',
          containerName: 'my-container'
        })
      }
    });

    const egressInfo = await egressClient.startRoomCompositeEgress('my-room', { file: fileOutput }, { layout: 'grid' });
    ```

=== ":simple-goland:{.icon .lg-icon .tab-icon} Go"

    Using [LiveKit Go SDK :fontawesome-solid-external-link:{.external-link-icon}](https://pkg.go.dev/github.com/livekit/server-sdk-go/v2){:target="_blank"}

    ```go
    import (
      "context"

      livekit "github.com/livekit/protocol/livekit"
      lksdk "github.com/livekit/server-sdk-go/v2"
    )

    egressClient := lksdk.NewEgressClient("https://my-openvidu-host", "api-key", "api-secret")

    egressInfo, err := egressClient.StartRoomCompositeEgress(context.Background(), &livekit.RoomCompositeEgressRequest{
        RoomName: "my-room",
        Layout:   "grid",
        FileOutputs: []*livekit.EncodedFileOutput{{
            FileType: livekit.EncodedFileType_MP4,
            Filepath: "my-room-recording.mp4",
            Output: &livekit.EncodedFileOutput_Azure{
                Azure: &livekit.AzureBlobUpload{
                    AccountName:   "my-storage-account",
                    AccountKey:    "my-account-key",
                    ContainerName: "my-container",
                },
            },
        }},
    })
    ```

=== ":simple-ruby:{.icon .lg-icon .tab-icon} Ruby"

    Using [LiveKit Ruby SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/server-sdk-ruby){:target="_blank"}

    ```ruby
    require 'livekit'

    egress_client = LiveKit::EgressServiceClient.new("https://my-openvidu-host", api_key: "api-key", api_secret: "api-secret")

    output = LiveKit::Proto::EncodedFileOutput.new(
      file_type: LiveKit::Proto::EncodedFileType::MP4,
      filepath: "my-room-recording.mp4",
      azure: LiveKit::Proto::AzureBlobUpload.new(
        account_name: "my-storage-account",
        account_key: "my-account-key",
        container_name: "my-container"
      )
    )
    egress_info = egress_client.start_room_composite_egress("my-room", output, layout: "grid")
    ```

=== ":fontawesome-brands-java:{.icon .lg-icon .tab-icon} Java"

    Using [LiveKit Kotlin SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/server-sdk-kotlin){:target="_blank"}

    ```java
    import io.livekit.server.EgressServiceClient;
    import livekit.LivekitEgress;

    EgressServiceClient egressClient = EgressServiceClient.createClient("https://my-openvidu-host", "api-key", "api-secret");

    LivekitEgress.EncodedFileOutput fileOutput = LivekitEgress.EncodedFileOutput.newBuilder()
            .setFileType(LivekitEgress.EncodedFileType.MP4)
            .setFilepath("my-room-recording.mp4")
            .setAzure(LivekitEgress.AzureBlobUpload.newBuilder()
                    .setAccountName("my-storage-account")
                    .setAccountKey("my-account-key")
                    .setContainerName("my-container")
                    .build())
            .build();

    LivekitEgress.EgressInfo egressInfo = egressClient
            .startRoomCompositeEgress("my-room", fileOutput, "grid")
            .execute().body();
    ```

=== ":fontawesome-brands-python:{.icon .lg-icon .tab-icon} Python"

    Using [LiveKit Python SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/python-sdks){:target="_blank"}

    ```python
    from livekit import api

    lkapi = api.LiveKitAPI(
        url="https://my-openvidu-host", api_key="api-key", api_secret="api-secret"
    )
    egress_info = await lkapi.egress.start_room_composite_egress(
        api.RoomCompositeEgressRequest(
            room_name="my-room",
            layout="grid",
            file_outputs=[api.EncodedFileOutput(
                file_type=api.EncodedFileType.MP4,
                filepath="my-room-recording.mp4",
                azure=api.AzureBlobUpload(
                    account_name="my-storage-account",
                    account_key="my-account-key",
                    container_name="my-container",
                ),
            )],
        )
    )
    ```

=== ":simple-rust:{.icon .lg-icon .tab-icon} Rust"

    Using [LiveKit Rust SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/rust-sdks){:target="_blank"}

    ```rust
    use livekit_api::services::egress::{EgressClient, EgressOutput, RoomCompositeOptions};
    use livekit_protocol as proto;

    let egress_client = EgressClient::with_api_key(
        "https://my-openvidu-host",
        "api-key",
        "api-secret",
    );

    let file_output = proto::EncodedFileOutput {
        file_type: proto::EncodedFileType::Mp4 as i32,
        filepath: "my-room-recording.mp4".to_string(),
        output: Some(proto::encoded_file_output::Output::Azure(proto::AzureBlobUpload {
            account_name: "my-storage-account".to_string(),
            account_key: "my-account-key".to_string(),
            container_name: "my-container".to_string(),
        })),
        ..Default::default()
    };

    let egress_info = egress_client.start_room_composite_egress(
        "my-room",
        vec![EgressOutput::File(file_output)],
        RoomCompositeOptions { layout: "grid".to_string(), ..Default::default() },
    ).await?;
    ```

=== ":simple-php:{.icon .lg-icon .tab-icon} PHP"

    Using [LiveKit PHP SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/agence104/livekit-server-sdk-php){:target="_blank"}

    ```php
    <?php
    use Agence104\LiveKit\EgressServiceClient;
    use Livekit\AzureBlobUpload;
    use Livekit\EncodedFileOutput;
    use Livekit\EncodedFileType;

    $egressClient = new EgressServiceClient("https://my-openvidu-host", "api-key", "api-secret");

    $fileOutput = new EncodedFileOutput([
        'file_type' => EncodedFileType::MP4,
        'filepath' => 'my-room-recording.mp4',
        'azure' => new AzureBlobUpload([
            'account_name' => 'my-storage-account',
            'account_key' => 'my-account-key',
            'container_name' => 'my-container',
        ]),
    ]);
    $egressInfo = $egressClient->startRoomCompositeEgress('my-room', 'grid', $fileOutput);
    ```

=== ":simple-dotnet:{.icon .lg-icon .tab-icon} .NET"

    Using [LiveKit .NET SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/pabloFuente/livekit-server-sdk-dotnet){:target="_blank"}

    ```csharp
    using Livekit.Server.Sdk.Dotnet;

    var egressClient = new EgressServiceClient("https://my-openvidu-host", "api-key", "api-secret");

    var request = new RoomCompositeEgressRequest { RoomName = "my-room", Layout = "grid" };
    request.FileOutputs.Add(new EncodedFileOutput
    {
        FileType = EncodedFileType.Mp4,
        Filepath = "my-room-recording.mp4",
        Azure = new AzureBlobUpload
        {
            AccountName = "my-storage-account",
            AccountKey = "my-account-key",
            ContainerName = "my-container",
        },
    });
    EgressInfo egressInfo = await egressClient.StartRoomCompositeEgress(request);
    ```

=== ":material-api:{.icon .lg-icon .tab-icon} Server API"

    If your backend technology does not have its own SDK, you have two options:

    1. Call the [Egress API :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/){:target="_blank"} directly. `StartRoomCompositeEgress` is a POST to `/twirp/livekit.Egress/StartRoomCompositeEgress`, authenticated with a token carrying the [`roomRecord` grant](./access-tokens.md#video-grants):

        ```bash
        curl -X POST 'https://my-openvidu-host/twirp/livekit.Egress/StartRoomCompositeEgress' \
          -H 'Authorization: Bearer <TOKEN>' \
          -H 'Content-Type: application/json' \
          -d '{
                "room_name": "my-room",
                "layout": "grid",
                "file_outputs": [
                  {
                    "file_type": "MP4",
                    "filepath": "my-room-recording.mp4",
                    "azure": {
                      "account_name": "my-storage-account",
                      "account_key": "my-account-key",
                      "container_name": "my-container"
                    }
                  }
                ]
              }'
        ```

    2. Use the [livekit-cli :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/intro/basics/cli/){:target="_blank"}:

        Create a file at `egress.json` with the following content:

        ```json
        {
          "room_name": "my-room",
          "layout": "grid",
          "file_outputs": [
            {
              "file_type": "MP4",
              "filepath": "my-room-recording.mp4",
              "azure": {
                "account_name": "my-storage-account",
                "account_key": "my-account-key",
                "container_name": "my-container"
              }
            }
          ]
        }
        ```

        Then run the following commands:

        ```bash
        export LIVEKIT_URL=https://my-openvidu-host
        export LIVEKIT_API_KEY=api-key
        export LIVEKIT_API_SECRET=api-secret

        lk egress start --type room-composite egress.json
        ```

!!! tip "Output files may survive crashes"

    If the Egress process crashes, the output is not necessarily lost: OpenVidu keeps a copy on the node's disk. Visit [Recovering Egress from node failures](../self-hosting/production-ready/fault-tolerance.md#recovering-egress-from-node-failures) for how to retrieve it.

## Layouts and custom templates

A Room Composite Egress records a web page rendered in a headless Chrome instance, which is what makes the output look like your application instead of a grid of raw tracks. The `layout` field of the start request chooses between the built-in layouts: `grid`, `speaker` and `single-speaker`. Add a `-light` suffix (`grid-light`) for a white background. [`UpdateLayout` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#updatelayout){:target="_blank"} changes it while the Egress runs.

A custom template is a web application you host and point `custom_base_url` at, so a Room Composite Egress records your view instead of a built-in layout. Visit the [LiveKit docs :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/transport/media/ingress-egress/egress/custom-template/){:target="_blank"} for the full specification.

## Audio-only and video-only egress

When starting a **Room Composite Egress** or a **Web Egress**, you can set `audio_only` parameter to true to generate an output with no video at all: one audio file with every participant of the Room mixed into it. The opposite parameter `video_only` drops the audio instead.

This is not just a matter of what ends up in the file. An audio-only Egress skips the browser compositor and the video encoder, which is where nearly all of the CPU cost of an Egress lives.

!!! warning

    For `audio_only` to actually skip the video pipeline, leave `layout` and `custom_base_url` unset. Setting either of them routes the recording through the compositor anyway.

If `audio_only` is set, parameter `audio_mixing` of type [`AudioMixing` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#audiomixing){:target="_blank"} defines how the audio of the participants is combined:

<div class="nowrap-first-column" markdown>

| Mode | Result |
| --- | --- |
| `DEFAULT_MIXING` | Every participant mixed together. This is the default |
| `DUAL_CHANNEL_AGENT` | AI Agent audio in the left channel, every other participant in the right channel |
| `DUAL_CHANNEL_ALTERNATE` | Each new audio track alternates between the left and right channels |

</div>

## Auto Egress

A Room can record itself from the moment it is created, with no call to the Egress API at all. Pass an `egress` configuration when calling method [CreateRoom :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#createroom){:target="_blank"}. This `egress` configuration is an object of type [RoomEgress :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#roomegress){:target="_blank"}, and lets you record the Room with Room Composite Egress or Track Egress.

!!! tip
    You can also include the same `egress` field in the `roomConfig` claim of [access tokens](./access-tokens.md#token-claims), in case you are letting participants create Rooms when they join.

Automatic recordings fail silently, since no API call of yours returns their error. [Enable webhooks](../self-hosting/how-to-guides/enable-webhooks.md) and watch `egress_ended`, and see [Troubleshoot OpenVidu recordings](../troubleshooting/recording.md) when auto egress does not produce the expected output.

## Egress lifecycle

### Managing a running Egress

The operations that **start** an Egress are the ones listed under [Egress types](#egress-types), one per type. Once an Egress is running, four more operations act on it, all of them identifying it by its `egress_id`:

<div class="nowrap-first-column" markdown>

| Operation | What it does |
| --- | --- |
| [`ListEgress` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#listegress){:target="_blank"} | Lists Egress, optionally filtered by Room or to only the active ones |
| [`StopEgress` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#stopegress){:target="_blank"} | Stops an Egress before it ends on its own |
| [`UpdateLayout` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#updatelayout){:target="_blank"} | Changes the layout of a running Room Composite Egress |
| [`UpdateStream` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#updatestream){:target="_blank"} | Adds or removes stream URLs on a running Egress |

</div>

### EgressInfo

Every one of those operations returns an [`EgressInfo` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#egressinfo){:target="_blank"}, and so does every Egress webhook. It is the complete state of an Egress at that moment:

```json
{
  "egressId": "EG_AbCdEfGhIjKl",
  "roomId": "RM_GmENxWJemFqL",
  "roomName": "my-room",
  "status": "EGRESS_COMPLETE",
  "startedAt": "1755678000000000000",
  "endedAt": "1755681600000000000",
  "fileResults": [
    {
      "filename": "my-room-recording.mp4",
      "location": "https://my-s3-endpoint/my-bucket/my-room-recording.mp4",
      "size": "104857600",
      "duration": "3600000000000"
    }
  ],
  "backupStorageUsed": false
}
```

The fields that matter most while an application is running:

- `egressId`: the identifier every operation above takes.
- `status`: where the Egress is in its lifecycle. See [below](#status).
- `startedAt`, `endedAt` and `updatedAt`: timestamps in **nanoseconds** (divide by 1,000,000 for milliseconds).
- `fileResults`, `streamResults`, `segmentResults` and `imageResults`: one entry per output, carrying the final location, size and duration of what was produced.
- `error`, `errorCode` and `details`: populated when something went wrong.
- `backupStorageUsed`: the output was written to the node's disk instead of the upload target.

### Webhooks

Rather than polling `ListEgress`, let OpenVidu tell you. Three [webhook events](./webhooks.md#events) track an Egress, and all of them carry the full `egressInfo`:

<div class="nowrap-first-column" markdown>

| Event | Fires when |
| --- | --- |
| `egress_started` | The Egress has begun recording or streaming |
| `egress_updated` | Its state changed while running |
| `egress_ended` | It finished, successfully or not |

</div>

### Status

<div class="nowrap-first-column" markdown>

| Status | Meaning |
| --- | --- |
| `EGRESS_STARTING` | Accepted, not yet producing output |
| `EGRESS_ACTIVE` | Running |
| `EGRESS_ENDING` | Shutting down: the output is being finalized and uploaded |
| `EGRESS_COMPLETE` | Finished successfully |
| `EGRESS_FAILED` | Finished with an error. Check `error` and `error_code` |
| `EGRESS_ABORTED` | Ended before producing any output |
| `EGRESS_LIMIT_REACHED` | Stopped because a configured limit was hit |

</div>

**A recording is only complete at `EGRESS_COMPLETE`.** Until then the file may not exist at its final location, and its `location` may not be final either. This is why an application waits for the `egress_ended` webhook rather than acting on the `EgressInfo` returned by `StopEgress`, which reports `EGRESS_ENDING`.

## Related

- [Recording tutorials](../tutorials/advanced-features/index.md): Egress in a working application, with S3 and Azure variants.
- [Configure external S3](../self-hosting/how-to-guides/external-s3.md): sending recordings to your own bucket.
- [Troubleshoot OpenVidu recordings](../troubleshooting/recording.md): missing recordings, 503s, CPU pressure.
- [Access tokens reference](./access-tokens.md): the `roomRecord` grant gates these operations.
- [Webhooks reference](./webhooks.md): the Egress events and their payloads.
- [Ingress reference](./ingress.md): media in the other direction.
