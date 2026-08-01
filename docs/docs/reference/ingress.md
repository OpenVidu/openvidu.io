---
title: "OpenVidu Ingress reference"
description: "Bring external media into an OpenVidu Room: input types, transcoding options, encoding presets and every Ingress state value."
---

# Ingress

**Ingress** brings media from outside into a Room. A streamer pushing RTMP from OBS, a WHIP endpoint publishing over WebRTC, a video file pulled from a URL, an IP camera — Ingress transcodes what arrives (or relays it untouched) and publishes it as a participant, so everyone in the Room subscribes to it like any other track.

Your application server creates an Ingress up front. The API returns a URL and, where relevant, a stream key; whoever is broadcasting points their encoder at those.

## Input types

| Input | What it is |
| --- | --- |
| `RTMP_INPUT` | OpenVidu exposes an RTMP endpoint. The broadcaster pushes to the returned `rtmp://` URL using the returned `stream_key`. Always transcoded |
| `WHIP_INPUT` | OpenVidu exposes a WHIP endpoint, so the broadcaster publishes over WebRTC. The only input that can skip transcoding |
| `URL_INPUT` | OpenVidu **pulls** from a URL you supply, rather than waiting to be pushed to. Used for media files and HLS streams |

!!! tip "IP cameras"

    RTSP cameras are ingested through `URL_INPUT`, passing the camera's `rtsp://` URL. There is a worked example in eight languages under [IP Cameras](../developing-your-openvidu-app/how-to.md#ip-cameras).

## Creating an Ingress

| Field | Notes |
| --- | --- |
| `input_type` | One of the three above |
| `url` | Where to pull media from. `URL_INPUT` only |
| `name` | Your own label for this Ingress |
| `room_name` | The Room to publish into |
| `participant_identity` | Identity the Ingress publishes as. Same uniqueness rules as any [participant identity](./access-tokens.md#token-claims) |
| `participant_name` | Display name |
| `participant_metadata` | Metadata attached to the publishing participant |
| `enable_transcoding` | See below |
| `audio` | `IngressAudioOptions` — track name, source, and a preset or explicit options |
| `video` | `IngressVideoOptions` — same shape |
| `enabled` | Defaults to `true`; set `false` to reject new connection attempts without deleting the Ingress |

### Transcoding

`enable_transcoding` decides whether media is re-encoded on the way in or relayed as it arrives.

- **RTMP and URL inputs are always transcoded.** RTMP arrives as a single non-simulcast stream that has to be re-encoded to be useful in a Room.
- **WHIP can skip it, and does by default.** WHIP is already WebRTC, so relaying it straight through avoids a transcode. That is the lowest-latency path into a Room, at the cost of the layers a transcode would produce.

An older `bypass_transcoding` field does the same job and is deprecated; use `enable_transcoding`.

### Audio and video options

Each of `audio` and `video` carries a track `name`, a `source`, and **either** a preset **or** explicit encoding options.

Audio presets:

| Preset | Codec |
| --- | --- |
| `OPUS_STEREO_96KBPS` | OPUS, 2 channels, 96 kbps |
| `OPUS_MONO_64KBS` | OPUS, 1 channel, 64 kbps |

Video presets — all H.264, with the layer count deciding whether subscribers get simulcast:

| Preset | Resolution | FPS | Main-layer bitrate | Layers |
| --- | --- | --- | --- | --- |
| `H264_720P_30FPS_3_LAYERS` | 1280×720 | 30 | 1900 kbps | 3 |
| `H264_1080P_30FPS_3_LAYERS` | 1920×1080 | 30 | 3500 kbps | 3 |
| `H264_540P_25FPS_2_LAYERS` | 960×540 | 25 | 1000 kbps | 2 |
| `H264_720P_30FPS_1_LAYER` | 1280×720 | 30 | 1900 kbps | 1 |
| `H264_1080P_30FPS_1_LAYER` | 1920×1080 | 30 | 3500 kbps | 1 |
| `H264_720P_30FPS_3_LAYERS_HIGH_MOTION` | 1280×720 | 30 | 2500 kbps | 3 |
| `H264_1080P_30FPS_3_LAYERS_HIGH_MOTION` | 1920×1080 | 30 | 4500 kbps | 3 |
| `H264_540P_25FPS_2_LAYERS_HIGH_MOTION` | 960×540 | 25 | 1300 kbps | 2 |
| `H264_720P_30FPS_1_LAYER_HIGH_MOTION` | 1280×720 | 30 | 2500 kbps | 1 |
| `H264_1080P_30FPS_1_LAYER_HIGH_MOTION` | 1920×1080 | 30 | 4500 kbps | 1 |

The `HIGH_MOTION` variants spend more bitrate at the same resolution. Reach for them when the source is hard to encode — sport, gameplay, anything with constant movement — and for a static presentation or a talking head, don't.

## IngressInfo

| Field | Notes |
| --- | --- |
| `ingress_id` | Identifier for update, delete and lookup |
| `name` | Your label |
| `stream_key` | Secret the broadcaster authenticates with. Treat it like a credential |
| `url` | Where to push to, or pull from: `rtmp://` for RTMP, the WHIP endpoint for WHIP, your own URL for `URL_INPUT` |
| `input_type` | The input in use |
| `enable_transcoding` | Whether media is re-encoded |
| `audio` / `video` | The options in effect |
| `room_name` | Destination Room |
| `participant_identity` / `participant_name` / `participant_metadata` | How the Ingress appears in the Room |
| `reusable` | Whether the endpoint accepts a new session after one ends — true for RTMP, which is what lets a broadcaster reconnect to the same URL |
| `enabled` | Whether new connections are accepted |
| `state` | Current state, below |

### State

`IngressState.status`:

| Status | Meaning |
| --- | --- |
| `ENDPOINT_INACTIVE` | Created, nothing connected yet |
| `ENDPOINT_BUFFERING` | Media is arriving and being buffered |
| `ENDPOINT_PUBLISHING` | Publishing into the Room |
| `ENDPOINT_ERROR` | Failed — `error` says why |
| `ENDPOINT_COMPLETE` | The session finished |

Alongside `status`, the state carries `error`, `room_id`, `started_at`, `ended_at`, `updated_at`, `resource_id`, the published `tracks`, and a description of what is actually arriving:

| | Fields |
| --- | --- |
| `video` (`InputVideoState`) | `mime_type`, `average_bitrate`, `width`, `height`, `framerate` |
| `audio` (`InputAudioState`) | `mime_type`, `average_bitrate`, `channels`, `sample_rate` |

Those two are the first place to look when a stream connects but looks wrong: they report what the broadcaster is really sending, as opposed to what they think they configured.

## Other operations

| Operation | Purpose |
| --- | --- |
| `CreateIngress` | Create one and get back its URL and stream key |
| `UpdateIngress` | Change an existing Ingress — Room, participant details, options, `enabled` |
| `ListIngress` | List them, filtered by Room or by id |
| `DeleteIngress` | Remove one |

## Webhooks

| Event | Fires |
| --- | --- |
| `ingress_started` | The Ingress began publishing |
| `ingress_ended` | It stopped |

Both carry the full `ingressInfo`, so `state.error` is where a failed ingest explains itself. See the [webhooks reference](./webhooks.md).

Note that an Ingress publishing into a Room also produces ordinary participant and track events — a `participant_joined` for the Ingress participant, and `track_published` per track.

## Related

- [IP Cameras](../developing-your-openvidu-app/how-to.md#ip-cameras) — RTSP ingest in eight languages
- [Stream ingestion](../developing-your-openvidu-app/how-to.md#stream-ingestion) — choosing between the input types
- [Access tokens reference](./access-tokens.md) — the `ingressAdmin` grant gates these operations
- [Webhooks reference](./webhooks.md) — the Ingress events and their payloads
- [Egress reference](./egress.md) — media in the other direction
