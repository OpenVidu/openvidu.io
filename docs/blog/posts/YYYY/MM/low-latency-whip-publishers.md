---
title: 'Low Latency Live Streaming: WHIP Publishers (Part 3)'
draft: false
date: 2026-09-23
slug: low-latency-whip-publishers
cover_image: poster-light.webp
description: >-
  Seven tools that already publish over WHIP into OpenVidu — a command line, a
  Raspberry Pi, a microcontroller, a phone, a rack encoder and a gateway.
categories:
  - Research
  - Technology
tags:
  - WebRTC
  - WHIP
  - Live streaming
  - Low latency
  - FFmpeg
  - GStreamer
  - Self-hosted
authors:
  - patxi
---

# Low Latency Live Streaming: WHIP Publishers (Part 3)

![Command line, single-board computer, microcontroller, phone, broadcast encoder and gateway all publishing into an OpenVidu Room over WHIP](/assets/images/blog/YYYY/MM/low-latency-whip-publishers/poster-light.webp#only-light "Software and hardware that publishes over WHIP"){ .round-corners }
![Command line, single-board computer, microcontroller, phone, broadcast encoder and gateway all publishing into an OpenVidu Room over WHIP](/assets/images/blog/YYYY/MM/low-latency-whip-publishers/poster-dark.webp#only-dark "Software and hardware that publishes over WHIP"){ .round-corners }

Every time I show someone the WHIP demo from <a href="https://openvidu.io/blog/2026/09/08/low-latency-whip-ingestion/">Part 2</a>, the same question comes back within a minute: "fine, but my camera is an SDI feed in a rack / an ESP32 on a nest box / an SRT link from a contribution encoder — can *that* get in?" The answer is rarely in the marketing copy. So I went through the software and hardware that can actually publish over WHIP today, checked the claims in source where source exists, and pointed the interesting ones at a live <a href="/docs/">OpenVidu Platform</a> deployment to see what really happens.

<!-- more -->

Part 1 argued <a href="https://openvidu.io/blog/2026/09/01/low-latency-live-streaming/">why WebRTC beats HLS and DASH</a> when someone has to act on what they see; part 2 built the loop. This post is the field guide — if your question is still "how do I set any of this up at all", read part 2 first.

**OBS Studio and VDO.Ninja are deliberately missing from the list below.** Both publish WHIP perfectly well; part 2 already spent those two scenarios, so the seven rows here are the ones part 2 does *not* cover.

## First, the gate every one of these has to pass

One constraint decides more than any feature list. OpenVidu's WHIP ingress registers exactly four codecs: video **H.264** and **VP8**, audio **Opus** and **PCMA**. That is the whole set.

![The OpenVidu WHIP codec gate — H.264 and VP8 with Opus pass, AV1 and HEVC are rejected, and PCMA passes the handshake then dies](/assets/images/blog/YYYY/MM/low-latency-whip-publishers/whip-codec-gate-light.svg#only-light "What negotiates over WHIP into OpenVidu"){ loading=lazy }
![The OpenVidu WHIP codec gate — H.264 and VP8 with Opus pass, AV1 and HEVC are rejected, and PCMA passes the handshake then dies](/assets/images/blog/YYYY/MM/low-latency-whip-publishers/whip-codec-gate-dark.svg#only-dark "What negotiates over WHIP into OpenVidu"){ loading=lazy }

Three consequences, all worth knowing before you buy hardware.

**AV1 and HEVC cannot negotiate.** It does not matter that your encoder offers them, or that the box's spec sheet leads with H.265. They are not in the ingress's media engine, so the SDP exchange has nothing to agree on. Set every one of these tools to H.264 or VP8 and move on.

**High-profile H.264 is fine, despite appearances.** The ingress registers H.264 with `profile-level-id=42001f`, which reads as "constrained baseline, level 3.1" and looks like it would exclude every hardware encoder locked to High. It does not. I sent an offer carrying only `profile-level-id=64001f` and got back `201 Created` with `64001f` echoed in the answer — the underlying WebRTC stack matches `fmtp` lines loosely. And because the ingress runs with `bypass_transcoding:true`, what a High-profile encoder sends is what subscribers receive; nothing quietly re-encodes it down.

**Audio means Opus, and PCMA is a trap.** PCMA is registered in the media engine, but the decode path handles only VP8, H.264 and Opus. I published a PCMA-only offer and got `201 Created` with `a=rtpmap:8 PCMA/8000` echoed straight back — and then no media ever arrived. That is the worst failure shape there is: the handshake says yes, the logs look clean, the stream never shows up. A device that can only do G.711 cannot publish audio into OpenVidu over WHIP, and it will not tell you so.

!!! tip "A client with no header support can still authenticate"
    OpenVidu's ingress reads the `Authorization` header and strips a leading `Bearer `, but it also
    exposes `/{app}/{stream_key}` routes for clients that cannot set a header at all. If a box or a
    service only gives you a URL field, put the stream key in the path.

## The seven, and who each one is for

![Seven WHIP publishers grouped by scenario — scripts and servers, devices, people and racks — all pointing at one OpenVidu WHIP ingress](/assets/images/blog/YYYY/MM/low-latency-whip-publishers/whip-publisher-map-light.svg#only-light "Which WHIP publisher fits which scenario"){ loading=lazy }
![Seven WHIP publishers grouped by scenario — scripts and servers, devices, people and racks — all pointing at one OpenVidu WHIP ingress](/assets/images/blog/YYYY/MM/low-latency-whip-publishers/whip-publisher-map-dark.svg#only-dark "Which WHIP publisher fits which scenario"){ loading=lazy }

| Tool | You recognise yourself if… | Licence / price | Watch out for |
|---|---|---|---|
| **FFmpeg ≥ 8.0** | you have a script, a cron job, a file or an RTSP camera, and want no GUI anywhere | LGPL-2.1+ / GPL-2+, free | your distro's build probably has no `whip` muxer |
| **GStreamer `whipclientsink`** | you ship a Linux device — Pi, Jetson, drone companion computer — where the pipeline *is* the product | MPL-2.0 plugin, free | not `whipsink`; that one is deprecated |
| **libpeer** | you write firmware for an ESP32-class camera, with no Linux and no room for GStreamer | MIT, free | video-only in practice; its audio is G.711 |
| **Larix Broadcaster** | you are in the field with a phone, and need WHIP and SRT out at once | closed source; WHIP needs Larix Premium, **$9.99/month** | paid, proprietary, never tested against OpenVidu |
| **Osprey Talon 4K-SC** | you have SDI infrastructure and a rack, and "install OBS on a laptop" is no answer | commercial, **$2,959** | WHIP is the vendor's claim; we tested no unit |
| **Eyevinn `whip-mpegts`** | MPEG-TS or SRT already arrives from a playout system or a contribution link | Apache-2.0, free | no RTMP or RTSP input, no Windows build |
| **ggarber/whip-go** | you publish from your own Go program, or want a CLI to hack on | MIT, free | no tagged release, ever; four `-dev` packages to build |

### FFmpeg ≥ 8.0 — the command line

FFmpeg grew a real WHIP muxer in 8.0 (2025-08-22), and it is the most useful row here because FFmpeg reads *everything*: files, `x11grab`, v4l2 cameras, RTSP, SRT, MPEG-TS. It is the "IP camera into OpenVidu" answer as much as the "play a file" one.

```bash
ffmpeg -re -i input.mp4 \
  -c:v libx264 -profile:v baseline -tune zerolatency -bf 0 -g 30 \
  -c:a libopus -b:a 64k -ar 48000 -ac 2 \
  -f whip -authorization "<streamKey>" "http://localhost:8085/whip"
```

`-authorization` is the muxer's Bearer token. `-bf 0` is not optional: the muxer refuses B-frames outright. And it only ever writes H.264 video and Opus audio, which happens to be exactly what OpenVidu wants — no codec decisions needed on your part.

!!! note "Why it says `Unknown muxer 'whip'` on your machine"
    This is the likeliest thing to go wrong, and it is not your command. The WHIP muxer needs a
    DTLS backend, and in 8.0 that meant **OpenSSL or schannel only**. The FFmpeg that ships with
    Debian and Ubuntu is built against GnuTLS, so on 8.x it has **no `whip` muxer at all**. FFmpeg
    9.0 widened the dependency to include GnuTLS and mbedTLS. Check that first:

    ```bash
    ffmpeg -muxers | grep whip
    ```

    Nothing back means you need a 9.x build, or an 8.x one linked against OpenSSL.

FFmpeg's own documentation still labels the muxer experimental. It works; just don't be surprised by rough edges.

### GStreamer `whipclientsink` — the Pi, the Jetson, the thing you ship

When the pipeline is the product — a Raspberry Pi in an enclosure, a Jetson doing inference on the way past, a companion computer on a drone — GStreamer is the answer, and it has been since 1.24 added `whipclientsink`.

```bash
gst-launch-1.0 -e v4l2src ! videoconvert ! \
  whipclientsink signaller::whip-endpoint="http://localhost:8085/whip" \
                 signaller::auth-token="<streamKey>"
```

`auth-token` goes out as `Authorization: Bearer <token>`, which is exactly what the ingress wants. And because `whipclientsink` is built around `webrtcsink`, you inherit its congestion control — the reason it exists and the reason to prefer it.

!!! warning "Not `whipsink`"
    You will find `whipsink` in older tutorials, and, at the time of writing, in
    [OpenVidu's own Ingress reference](/docs/reference/ingress.md). It was deprecated in favour of
    `whipclientsink` in GStreamer 1.24, and its entire `webrtchttp` plugin was deprecated in 1.28.
    Write new pipelines against `whipclientsink`.

The flip side of a pipeline is that the encoder, the bitrate and the keyframe interval are all your problem. Constrain it to H.264 or VP8 plus Opus and you are inside the gate.

This row is also the honest answer to "which camera speaks WHIP natively?". I looked at Axis, Kiloview, BirdDog, PTZOptics and the drone platforms and found encoder boxes and companion computers — no camera firmware that emits WHIP itself. That device category does not exist yet.

### libpeer — WHIP from a microcontroller

This is the row that surprised me. [libpeer :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/sepfy/libpeer){:target="_blank"} is an MIT-licensed WebRTC stack in C for embedded targets — mbedTLS, libsrtp, usrsctp, FreeRTOS — and it does WHIP signalling, Bearer header included, on an ESP32. If you are building a doorbell, a nest-box camera or a battery-powered field camera, there is no Linux and no GStreamer down there, and this is the only thing here that fits.

Be clear-eyed about it. Its codec enum implements H.264, PCMA and PCMU; VP8, MJPEG and **Opus** are marked "not implemented yet" in the source. Against the gate above, the usable configuration is **video-only H.264** — its audio is exactly the G.711 that negotiates and then dies. There are no tagged releases either, so you pin a commit; the WHIP implementation is minimal (no trickle ICE, no ICE restart); and there is no congestion control worth the name, so a congested uplink degrades rather than adapts.

### Larix Broadcaster — the phone as a field camera

For "someone is standing somewhere with a phone", there is essentially one app. Larix Broadcaster publishes WHIP from iOS and Android, and it sends to several destinations at once — WHIP into your OpenVidu Room and SRT to an archive, simultaneously — which is what makes it interesting rather than merely available.

Two things plainly. It is **closed source**, and **WHIP output sits behind Larix Premium at $9.99/month**. Softvelum lists interop testing with Cloudflare Stream, Dolby.io and its own Nimble Streamer — not with LiveKit or OpenVidu. Its codecs (H.264 + Opus, plus VP8/VP9 on Android) fit the gate, so there is no technical reason it should fail; it is simply not certified.

Dolby's documentation for Larix describes the setup as Settings → Connections → new WebRTC connection, with the endpoint in **URL**, authentication set to **WHIP** and the stream key in **Token**. That is a third party's page, not Softvelum's specification, so treat the field names as a good guess.

### Osprey Talon 4K-SC — the rack

If your video arrives on 12G-SDI or HDMI and lives in a rack, the Talon 4K-SC is the box whose spec sheet lists WHIP alongside RTMP(S), SRT, Zixi, RTSP and RTP — and Opus specifically for the WHIP path.

It is not cheap — **$2,959** at the retailer I checked — and two caveats matter more than the price. First, **WHIP here is the vendor's claim** — I read the spec page, not a unit, and Osprey publishes no firmware release notes, so "WHIP since firmware X" is unanswerable from public sources. The one independent corroboration is PhenixRTS's integration guide, which tells users to set the protocol to "WHIP (Real-Time WebRTC)" and enter an endpoint and a publishing token — so the generic mode, the one that matters for a self-hosted endpoint, does appear to exist. Second, the box also does H.265, and H.265 will not negotiate. Configure it for H.264 and Opus.

### Eyevinn `whip-mpegts` — the gateway

Sometimes the stream already exists and arrives as MPEG-TS over UDP or as an SRT link from a contribution encoder or a playout system. `whip-mpegts` is an Apache-2.0 gateway that takes exactly those inputs and republishes them over WHIP.

```bash
brew install eyevinn/tools/whip-mpegts
```

It fits OpenVidu almost suspiciously well: it targets H.264 or VP8 with Opus, transcodes AAC to Opus automatically, and has `--bypass-video` and `--bypass-audio` flags for true passthrough when the input is already in the right codec. The token goes in `--whipEndpointAuthKey` and is sent as `Authorization: Bearer` on the POST, the PATCH and the DELETE.

The limits: no RTMP and no RTSP input (that is FFmpeg's job), no Windows build, and it is a small project — the bus factor is real. Its sibling `srt-whip-gateway` wraps a web UI around it but has not been tagged since 2023.

### ggarber/whip-go — publishing from your own program

The last row is for when the thing holding the media is a program you wrote. `whip-go` is an MIT-licensed, Pion-based Go library with a CLI on top: it sends the Bearer token on POST, PATCH and DELETE, reads the `Location` header, and does VP8 and H.264.

I built it from `main` and published into a local OpenVidu 3.8.0. It works — the peer connection reached `connected` and OpenVidu recorded a real participant with a real track. Three frictions, all of which I hit:

- **It does not build with `go build` alone.** cgo wants `pkg-config`, `libx264-dev`, `libvpx-dev`, `libx11-dev` and `libxext-dev`, failing once per missing package.
- **Pipe input is hardcoded to 1280×720 I420** and audio to 48 kHz mono s16. Feed it anything else and the frames come out scrambled.
- **It waits on stdin** ("Press 'Enter' to finish"), so under a container or a service manager it reads EOF and exits at once.

```bash
go build
./whip-go -v screen -vc vp8 -t "<streamKey>" http://localhost:8085/whip
```

There is **no tagged release, ever** — last push 2025-06-04. Treat it as reference code you vendor and adapt, not a dependency you pin. With `-vc vp8` it published as described; with `-vc h264` the run died in the encoder on my machine, which I did not chase further.

## The part that is about us: we advertise no TURN

This is a finding about OpenVidu, not about the tools above, and it gets its own heading because it decides whether half of them work on your network.

WHIP lets a server hand back ICE server configuration in `Link` headers. OpenVidu's ingress sends none. The full response to a successful `POST /whip` is `201 Created`, `Content-Type: application/sdp`, an `Etag`, a `Location` and the CORS headers — no `Link` header at all. A client with no ICE configuration of its own, which is most hardware encoders and appliance-style publishers, has nothing to pick up.

What the ingress does instead is put **its own** candidates in the SDP answer: a `typ host` candidate on the container address and several `typ srflx` ones on the machine's public address, so it runs STUN server-side. There are **no `typ relay` candidates**. No TURN appears anywhere in the exchange.

So these clients connect when outbound UDP to the media ports works, and have no fallback when it does not. The honest answer to "will my rack encoder publish from the corporate network?" is *probably — and if the firewall blocks UDP, nothing in the WHIP response will rescue it*.

## The row that isn't here: game streaming

I wanted a gameplay row. There isn't one, and the reason is worth more than the row would have been.

Sunshine, Selkies, neko, Nestri, Epic's Pixel Streaming and Millicast's Unity SDK all speak WebRTC. Every one of them. A code search for "whip" across each of those repositories on 2026-09-23 returned **zero hits** — they each ship their own WebSocket or RTSP-flavoured signalling. WebRTC is the media stack; WHIP is a signalling protocol, and speaking one does not give you the other.

Selkies is the frustrating case: it is a GStreamer application driving `webrtcbin`, so swapping in `whipclientsink` is a plausible weekend fork. Nobody has shipped it.

So gameplay into OpenVidu today means capturing it — with OBS (part 2), or with FFmpeg or GStreamer against a KMS/NVENC source. That is a real answer, and better than pretending Sunshine is one.

One more negative that will save a Home Assistant user an afternoon: **`go2rtc` cannot do this**. Its WHIP support is *ingest* — it receives WHIP, it does not emit it. For an IP camera, the bridge is FFmpeg or GStreamer.

## Need more than this?

Seven ways in, one gate to pass. If your situation is on that list, what remains is part 2's demo app plus one command or one settings screen.

- [Part 1: WebRTC vs. HLS and DASH](/blog/posts/2026/09/low-latency-live-streaming.md) — why sub-second delivery needs a different protocol.
- [Part 2: Ingest WHIP into OpenVidu](/blog/posts/2026/09/low-latency-whip-ingestion.md) — the demo app, the credentials endpoint, the OBS walkthrough.
- [Stream ingestion](/docs/build-your-app/common-operations.md#stream-ingestion) — creating WHIP ingresses from your own backend.
- [Ingress reference](/docs/reference/ingress.md) — every ingress type and option, including when to turn transcoding on.
- [OpenVidu Platform](/docs/index.md) — the self-hosted stack all of this publishes into.
