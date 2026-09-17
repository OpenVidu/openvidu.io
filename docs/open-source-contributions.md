---
title: "Open source contributions to LiveKit and mediasoup"
description: "OpenVidu's merged pull requests in LiveKit, mediasoup, pion and coturn: 37 fixes in the WebRTC stack our platform is built on, each one verifiable on GitHub."
hide:
  - feedback
  - path
  - navigation
  - toc
  - footer
  - search-bar
  - version-selector
---

# Open source contributions

OpenVidu is built on **[LiveKit :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/livekit){:target="_blank"}** and
**[mediasoup :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/versatica/mediasoup){:target="_blank"}**, which run on top of
**[pion :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/pion/webrtc){:target="_blank"}**, and every deployment ships
**[coturn :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/coturn/coturn){:target="_blank"}**. When we hit a bug in any of them, we fix it where
it belongs: upstream, in the project itself, for everyone using it.

That is not a claim you have to take on trust. It is a commit record, and you can read all of it.

<div class="grid cards" markdown>

- **56** pull requests opened in the projects we depend on
- **37** of them merged
- **2019 → today**, continuously
- **10** bugs we reported upstream and then fixed ourselves

</div>

## Where the fixes landed

### LiveKit

The SFU, the protocol and the SDKs OpenVidu 3 builds on.

| Pull request | What it fixed |
|---|---|
| [livekit#2401 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/livekit/pull/2401){:target="_blank"} | A race condition in `Participant.updateState`, in the SFU participant path |
| [livekit#3735 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/livekit/pull/3735){:target="_blank"} | The server was overwriting the sender identity on data packets from hidden participants |
| [livekit#4838 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/livekit/pull/4838){:target="_blank"} | Participants subscribing late never received a connection-quality update |
| [livekit#3382 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/livekit/pull/3382){:target="_blank"} | Boolean settings passed as environment variables were silently ignored |
| [livekit#1815 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/livekit/pull/1815){:target="_blank"} | `--bind` now applies to the RTC ports, not only the HTTP listener |
| [protocol#1371 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/protocol/pull/1371){:target="_blank"} | Unblocked C# and Ruby code generation from the protocol definitions |
| [client-sdk-js#1872 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/client-sdk-js/pull/1872){:target="_blank"} | A race between the `LocalTrackSubscribed` signal and `publishTrack` completion |
| [client-sdk-js#1720 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/client-sdk-js/pull/1720){:target="_blank"} | A memory leak in end-to-end encrypted rooms from unthrottled decryption errors |
| [client-sdk-js#1723 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/client-sdk-js/pull/1723){:target="_blank"} | `EncryptionError` now tells you which participant failed |
| [client-sdk-js#1729 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/client-sdk-js/pull/1729){:target="_blank"} | Encryption worker errors were being swallowed instead of rejecting their promises |
| [client-sdk-js#901 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/client-sdk-js/pull/901){:target="_blank"} | `livekit-client` 1.14.0 would not build in Angular applications |
| [egress#550 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/egress/pull/550){:target="_blank"} | Recording backups failed when the output path contained subdirectories |
| [agents#4111 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/agents/pull/4111){:target="_blank"} | Migrated the AWS speech-to-text plugin off an unmaintained SDK |
| [server-sdk-kotlin#108 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/server-sdk-kotlin/pull/108){:target="_blank"} | `updateIngress` was wiping the participant identity |
| [track-processors-js#127 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/track-processors-js/pull/127){:target="_blank"} | Background processing froze in hidden browser tabs |
| [track-processors-js#114 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/track-processors-js/pull/114){:target="_blank"} | The new `switchTo` API was unreachable because a wrapper was not exported |
| [track-processors-js#20 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/track-processors-js/pull/20){:target="_blank"} | The background-blur processor loaded the wrong WebAssembly path |
| [client-sdk-js#900 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/client-sdk-js/pull/900){:target="_blank"} | A wrong parameter type in the published API documentation for `TrackSubscriptionPermissionChanged` |
| [agents#4702 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/agents/pull/4702){:target="_blank"} | A wrong `timestamp` parameter in the Spitch speech-to-text plugin |
| [track-processors-js#86 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/track-processors-js/pull/86){:target="_blank"} | Consumers had to add the `dom-mediacapture-transform` types themselves |
| [track-processors-js#83 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/track-processors-js/pull/83){:target="_blank"} | A malformed repository field in the published package metadata |
| [livekit#4840 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/livekit/pull/4840){:target="_blank"} | Our own revert of #4838, once the maintainers pointed at a cleaner fix |

### mediasoup

The other media engine OpenVidu builds on, and the Go client our integration uses.

| Pull request | What it fixed |
|---|---|
| [mediasoup#695 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/versatica/mediasoup/pull/695){:target="_blank"} | Installing a prebuilt worker no longer requires Make and Python |
| [mediasoup#750 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/versatica/mediasoup/pull/750){:target="_blank"} | Worker error messages were printed unreadably |
| [mediasoup#688 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/versatica/mediasoup/pull/688){:target="_blank"} | Silenced a misleading worker log line for RTX RTCP packets |
| [mediasoup-website#6 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/versatica/mediasoup-website/pull/6){:target="_blank"} | Corrected the FFmpeg example in the official documentation |
| [mediasoup-go#83 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jiyeyuran/mediasoup-go/pull/83){:target="_blank"} | Two data races in the library's worker-close and transport-connect paths |
| [mediasoup-go#26 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jiyeyuran/mediasoup-go/pull/26){:target="_blank"} | H.264 packetization-mode 0 was indistinguishable from "unset" |
| [mediasoup-go#25 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jiyeyuran/mediasoup-go/pull/25){:target="_blank"} | A pointer was compared instead of its value, so profile matching was wrong |
| [mediasoup-go#27 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jiyeyuran/mediasoup-go/pull/27){:target="_blank"} | A payload type of 0 was emitted where the field should have been omitted |
| [mediasoup-go#78 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/jiyeyuran/mediasoup-go/pull/78){:target="_blank"} | De-flaked the asynchronous router tests |

### pion

The Go WebRTC stack underneath LiveKit. Two layers below our own code.

| Pull request | What it fixed |
|---|---|
| [webrtc#3009 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/pion/webrtc/pull/3009){:target="_blank"} | A deadlock in `DataChannel.DetachWithDeadline` caused by a missing mutex unlock |
| [webrtc#2840 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/pion/webrtc/pull/2840){:target="_blank"} | Simulcast stream order was non-deterministic because SDP parsing iterated a map |
| [webrtc#3473 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/pion/webrtc/pull/3473){:target="_blank"} | A flaky test that panicked after completion |

### Deployment dependencies

| Pull request | What it fixed |
|---|---|
| [coturn#1839 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/coturn/coturn/pull/1839){:target="_blank"} | Restored RFC 3489 STUN compatibility, broken in every coturn since 4.7.0 |
| [coturn#753 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/coturn/coturn/pull/753){:target="_blank"} | Replaced a flaky HTTP lookup for external IP discovery with DNS |
| [caddy-storage-redis#26 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/pberkel/caddy-storage-redis/pull/26){:target="_blank"} | Redis Sentinel deployments can now authenticate |

## We report bugs, then fix them

Ten bugs follow the same pattern: an OpenVidu engineer hit it in production, reported it upstream
with a reproduction, and then wrote the patch that closed it.

| The report | The fix |
|---|---|
| [pion/webrtc#3005 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/pion/webrtc/issues/3005){:target="_blank"} — possible deadlock in `DetachWithDeadline` | [#3009 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/pion/webrtc/pull/3009){:target="_blank"} |
| [pion/webrtc#2838 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/pion/webrtc/issues/2838){:target="_blank"} — undefined iteration order parsing SDP stream ids | [#2840 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/pion/webrtc/pull/2840){:target="_blank"} |
| [client-sdk-js#1878 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/client-sdk-js/issues/1878){:target="_blank"} — race between subscribe and publish | [#1872 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/client-sdk-js/pull/1872){:target="_blank"} |
| [client-sdk-js#1722 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/client-sdk-js/issues/1722){:target="_blank"} — encryption errors not attributable | [#1723 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/client-sdk-js/pull/1723){:target="_blank"} |
| [client-sdk-js#893 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/client-sdk-js/issues/893){:target="_blank"} — broken in Angular | [#901 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/client-sdk-js/pull/901){:target="_blank"} |
| [mediasoup#694 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/versatica/mediasoup/issues/694){:target="_blank"} — prebuilt worker still needs a toolchain | [#695 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/versatica/mediasoup/pull/695){:target="_blank"} |
| [server-sdk-kotlin#107 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/server-sdk-kotlin/issues/107){:target="_blank"} — ingress identity wiped | [#108 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/server-sdk-kotlin/pull/108){:target="_blank"} |
| [track-processors-js#116 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/track-processors-js/issues/116){:target="_blank"} — wrapper not exported | [#114 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/track-processors-js/pull/114){:target="_blank"} |
| [livekit#1876 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/livekit/issues/1876){:target="_blank"} — cannot assign requested address | [#1815 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/livekit/pull/1815){:target="_blank"} |
| [egress#549 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/egress/issues/549){:target="_blank"} — backup errors with subdirectories | [#550 :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/egress/pull/550){:target="_blank"} |

Alongside these, 33 issues in total have been filed upstream, including RTCP specification
discussions with the mediasoup maintainers and operational failure modes found by running Egress at
scale.

## Not everything merges, and that is normal

Of the 56 pull requests, 19 have not been merged. Seven we withdrew ourselves, because a maintainer
pointed at a cleaner fix or our own follow-up superseded them. Seven were closed by a maintainer who
had already solved the problem another way, each with a stated reason. Five are open, waiting for
review.

None was turned down as out of scope or unwelcome.

## Check it yourself

Every row above links to a public pull request. To reproduce the whole list rather than trust ours,
the [GitHub CLI :fontawesome-solid-external-link:{.external-link-icon}](https://cli.github.com/){:target="_blank"} will do it in one command per person:

```bash
gh search prs --author pabloFuente --owner livekit --owner versatica --owner pion \
  --limit 100 --json url,title,state,repository,createdAt
```

The engineers behind these contributions are Pablo Fuente, Juan Navarro, Carlos Santos, Carlos Ruiz
and Juan Carlos Moreno. You will find them on the [about us](about-us.md) page, and in the history of
the projects above.

<div class="second-slogan" markdown>

## Build on a stack we help maintain

Whichever product you pick, it runs on media servers whose bugs we fix rather than work around.
**OpenVidu Meet** is the finished application you deploy and brand. **OpenVidu Platform** gives you
the SDKs and the low-level control.

<div class="home-buttons" markdown="span">
[Deploy Meet in minutes](meet/index.md){ .md-button .md-button--primary .home-meet-button title="Get started with OpenVidu Meet" }
[Start building with the SDKs](docs/index.md){ .md-button .home-platform-button title="Build with OpenVidu Platform SDKs" }
</div>

Not sure which fits? [Compare Meet vs Platform](openvidu-meet-vs-openvidu-platform.md)
{ .home-under-cta }

</div>
