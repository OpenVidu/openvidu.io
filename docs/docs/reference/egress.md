---
title: "OpenVidu Egress reference"
description: "Export media out of an OpenVidu Room: every Egress type, output format, encoding preset, storage target and status value."
---

# Egress

**Egress** exports media out of a Room. Recording a meeting to MP4, streaming it to RTMP, producing HLS segments, capturing periodic thumbnails — all of it is Egress. Your application server starts and stops Egress through the API; the Egress service joins the Room as a hidden participant and does the work.

OpenVidu ships Egress already wired to the bundled S3-compatible storage, so a recording has somewhere to land with no extra setup. That is one of the things OpenVidu adds over a bare LiveKit install.

For a worked application — start a recording, list them, serve them back — see the [recording tutorials](../tutorials/advanced-features/index.md).

## Egress types

Five request types, each starting a different kind of export:

| Type | SDK method | What it produces |
| --- | --- | --- |
| **Room Composite** | `StartRoomCompositeEgress` | One output with every participant composited in a layout. The usual choice for "record the meeting" |
| **Web** | `StartWebEgress` | One output from an arbitrary web page URL, rather than from a Room |
| **Participant** | `StartParticipantEgress` | One output per participant, identified by `identity` |
| **Track Composite** | `StartTrackCompositeEgress` | One output combining a chosen audio track and video track |
| **Track** | `StartTrackEgress` | One output per individual track, written without transcoding |

### Request fields

Room Composite, Web, Participant and Track Composite share the same output and encoding fields, and differ in what identifies the source:

| Request | Source fields |
| --- | --- |
| Room Composite | `room_name`, `layout`, `audio_only`, `video_only`, `audio_mixing`, `custom_base_url` |
| Web | `url`, `audio_only`, `video_only`, `await_start_signal` |
| Participant | `room_name`, `identity`, `screen_share` |
| Track Composite | `room_name`, `audio_track_id`, `video_track_id` |
| Track | `room_name`, `track_id` |

`audio_mixing` on Room Composite takes `DEFAULT_MIXING`, `DUAL_CHANNEL_AGENT` or `DUAL_CHANNEL_ALTERNATE`, for putting different speakers on separate channels.

**Track Egress is the exception.** It does not transcode, so it takes neither encoding options nor the output lists below — just one of `file` (a `DirectFileOutput`) or `websocket_url`.

## Outputs

Every other type accepts four output lists, and you can populate more than one in a single request — the same Egress can write a file *and* push a stream:

| Output list | Type | Produces |
| --- | --- | --- |
| `file_outputs` | `EncodedFileOutput` | A single media file |
| `stream_outputs` | `StreamOutput` | A live stream pushed to one or more URLs |
| `segment_outputs` | `SegmentedFileOutput` | Segmented output plus a playlist — HLS |
| `image_outputs` | `ImageOutput` | Still images captured at an interval |

!!! warning "Use the plural fields"

    Each request also has singular `file`, `stream` and `segments` fields. They are **deprecated** in favour of the lists above. Some SDKs still expose the singular form as a convenience — the recording tutorials in these docs pass `file` — but new code should prefer the lists.

### File output

`EncodedFileOutput` takes a `file_type`, a `filepath`, `disable_manifest`, and exactly one upload target.

| `file_type` | Notes |
| --- | --- |
| `DEFAULT_FILETYPE` | Chosen from the codecs in use |
| `MP4` | |
| `OGG` | |
| `MP3` | |

`DirectFileOutput`, used only by Track Egress, is the same minus `file_type` — the track is written in whatever codec it was published with.

### Stream output

`StreamOutput` takes a `protocol` and a list of `urls`:

| `protocol` | |
| --- | --- |
| `DEFAULT_PROTOCOL` | Chosen from the URLs given |
| `RTMP` | |
| `SRT` | |
| `WEBSOCKET` | |

URLs can be added to and removed from a running stream Egress with `UpdateStream`.

### Segmented output

`SegmentedFileOutput` produces HLS:

| Field | Notes |
| --- | --- |
| `protocol` | `DEFAULT_SEGMENTED_FILE_PROTOCOL` or `HLS_PROTOCOL` |
| `filename_prefix` | Prefix for the segment files |
| `playlist_name` | Playlist file name |
| `live_playlist_name` | A second, live playlist. Disabled unless set |
| `segment_duration` | Seconds per segment |
| `filename_suffix` | `INDEX` (default) or `TIMESTAMP` |
| `disable_manifest` | Skip uploading the manifest file |

### Image output

`ImageOutput` captures stills: `capture_interval` in seconds (required), optional `width` and `height` (default to the track's), `filename_prefix`, `image_codec`, `disable_manifest`, and a `filename_suffix` of `IMAGE_SUFFIX_INDEX`, `IMAGE_SUFFIX_TIMESTAMP` or `IMAGE_SUFFIX_NONE_OVERWRITE` — the last one keeps overwriting a single file, which is what you want for a "current thumbnail".

## Encoding

Pick a preset or specify options. Presets:

| Preset | Resolution | FPS | Video bitrate |
| --- | --- | --- | --- |
| `H264_720P_30` | 1280×720 | 30 | 3000 kbps |
| `H264_720P_60` | 1280×720 | 60 | 4500 kbps |
| `H264_1080P_30` | 1920×1080 | 30 | 4500 kbps |
| `H264_1080P_60` | 1920×1080 | 60 | 6000 kbps |
| `PORTRAIT_H264_720P_30` | 720×1280 | 30 | 3000 kbps |
| `PORTRAIT_H264_720P_60` | 720×1280 | 60 | 4500 kbps |
| `PORTRAIT_H264_1080P_30` | 1080×1920 | 30 | 4500 kbps |
| `PORTRAIT_H264_1080P_60` | 1080×1920 | 60 | 6000 kbps |

All presets encode H.264 MAIN video with OPUS audio. For anything else, set `advanced` (`EncodingOptions`) instead:

| Field | Default |
| --- | --- |
| `width` / `height` | 1920 × 1080 |
| `depth` | 24 |
| `framerate` | 30 |
| `audio_codec` | `OPUS` |
| `audio_bitrate` | 128 |
| `audio_frequency` | 44100 |
| `video_codec` | `H264_MAIN` |
| `video_bitrate` | 4500 |
| `key_frame_interval` | 4 s for streaming; the segment duration for segmented output; the encoder's default for files |

## Where the output goes

Each file, segment and image output carries exactly one upload target:

| Target | Key fields |
| --- | --- |
| `s3` | `access_key`, `secret`, `region`, `endpoint`, `bucket`, `force_path_style`, plus optional `session_token`, `assume_role_arn`, `metadata`, `tagging`, `content_disposition` and a `proxy` |
| `gcp` | `credentials` (a service-account JSON), `bucket`, `proxy` |
| `azure` | `account_name`, `account_key`, `container_name` |
| `aliOSS` | `access_key`, `secret`, `region`, `endpoint`, `bucket` |

In OpenVidu the S3 target is the default path: deployments bundle a MinIO instance that Egress is already configured against. To send recordings elsewhere instead, see [Configure external S3](../self-hosting/how-to-guides/external-s3.md).

!!! tip "Output files survive a node failure"

    If the Media Node running an Egress crashes, the output is not necessarily lost: OpenVidu keeps a copy on the node's disk, and `EgressInfo.backup_storage_used` tells you when that fallback was taken. [Recovering Egress from node failures](../self-hosting/production-ready/fault-tolerance.md#recovering-egress-from-node-failures) has the paths and the caveats.

## EgressInfo

Returned by every Egress call, and delivered on the [Egress webhooks](./webhooks.md#events):

| Field | Notes |
| --- | --- |
| `egress_id` | Identifier to stop or look up this Egress |
| `room_id` / `room_name` | The Room being exported |
| `status` | See below |
| `started_at` / `ended_at` / `updated_at` | **Nanosecond** timestamps — the recording tutorials divide by 1,000,000 to get milliseconds |
| `file_results` | One `FileInfo` per file: `filename`, `location`, `size`, `duration` and more |
| `stream_results` | One `StreamInfo` per stream URL |
| `segment_results` | One `SegmentsInfo` per segmented output |
| `image_results` | One `ImagesInfo` per image output |
| `error` / `error_code` / `details` | Populated when something went wrong |
| `manifest_location` | Location of the uploaded manifest, unless disabled |
| `backup_storage_used` | Whether the output was written to backup storage instead of the upload target |
| `retry_count` | How many times this Egress was retried |
| `source_type` | `EGRESS_SOURCE_TYPE_WEB` or `EGRESS_SOURCE_TYPE_SDK` |

The request that started it is echoed back in a `oneof`: `room_composite`, `web`, `participant`, `track_composite` or `track`.

### Status

| Status | Meaning |
| --- | --- |
| `EGRESS_STARTING` | Accepted, not yet producing output |
| `EGRESS_ACTIVE` | Running |
| `EGRESS_ENDING` | Stopping — finalizing and uploading |
| `EGRESS_COMPLETE` | Finished successfully |
| `EGRESS_FAILED` | Finished with an error; check `error` and `error_code` |
| `EGRESS_ABORTED` | Ended before producing output |
| `EGRESS_LIMIT_REACHED` | Stopped because a configured limit was hit |

**A recording is only complete at `EGRESS_COMPLETE`.** Until then the file may not exist at its final location. This is why applications key off the `egress_ended` webhook rather than the response to `StopEgress`.

## Lifecycle and webhooks

Three webhook events track an Egress, each carrying the full `egressInfo`:

| Event | Fires |
| --- | --- |
| `egress_started` | The export has begun |
| `egress_updated` | Its state changed while running |
| `egress_ended` | It finished, successfully or not |

`egress_ended` is the one that matters to most applications: it is where the final file location and the terminal status arrive. See the [webhooks reference](./webhooks.md).

## Other operations

| Operation | Purpose |
| --- | --- |
| `ListEgress` | List Egress, optionally filtered by Room or active state |
| `StopEgress` | Stop one by `egress_id` |
| `UpdateLayout` | Change the layout of a running Room Composite Egress |
| `UpdateStream` | Add or remove stream URLs on a running Egress |

## Related

- [Recording tutorials](../tutorials/advanced-features/index.md) — Egress in a working application, with S3 and Azure variants
- [Configure external S3](../self-hosting/how-to-guides/external-s3.md) — sending recordings to your own bucket
- [Troubleshoot OpenVidu recordings](../troubleshooting/recording.md) — missing recordings, 503s, CPU pressure
- [Webhooks reference](./webhooks.md) — the Egress events and their payloads
- [Ingress reference](./ingress.md) — media in the other direction
