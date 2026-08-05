---
name: video-recording
description: >
  Record a looping demo video of an app that embeds OpenVidu Meet, with two
  synthetic camera feeds (e.g. a "user" and a "client") so the meeting looks
  real without any physical webcams. Covers injecting stock/video-file cameras
  into OpenVidu Meet via getUserMedia override, driving the join through the
  real browser, and compositing the final loop with ffmpeg. Use when producing
  marketing/demo footage of an embedded-meeting flow. Triggers: "record a demo
  video", "fake the camera feeds", "two people in the meeting", "loop video for
  the blog post".
---

# Recording an embedded-meeting demo with injected camera feeds

Produce a short looping MP4 of a two-person OpenVidu Meet call embedded in an
app, where **both participants' cameras are pre-recorded clips** rather than
real webcams. The reference output is the video of the
`building-a-video-enabled-crm-with-an-ai-agent` post: sign in → open an issue →
click **Join** → a live two-way meeting inside the app, ~10 s, looping.

## The core idea

OpenVidu Meet takes whatever `navigator.mediaDevices.getUserMedia()` returns.
Override that function **before the Meet app runs** and hand it a `MediaStream`
built from a `<canvas>` you paint video frames onto. Meet publishes it over
WebRTC as if it were a real camera. Do this once per browser session, one clip
per "person".

## Do not use these approaches

Each has been tried and fails; use the fix instead.

1. **Do not feed a `<video>` element or blob straight into `captureStream()`.**
   Inside the Meet page a `<video src=blob:...>` (or an `http://` src) never
   leaves `readyState 0` and the join hangs on "Preparing room…", while
   `fetch()` of the same URL succeeds — it is the media element decode path,
   not the network. **Instead:** decode frames out-of-band and cycle them on a
   canvas (below).
2. **Do not drive the join with Playwright, headless Chrome, headless-shell or
   snap Chromium.** The media pipeline stalls pre-network regardless of sandbox,
   GPU, WebGL, virtual-background or wait time. **Instead:** drive the join in
   the user's **real Chrome** via the `claude-in-chrome` extension. Headless
   Playwright is still the right tool for the static lead-up screenshots.
3. **Do not leave the second participant in a background tab.** Chrome stops
   compositing hidden tabs, so its canvas `captureStream` goes **black**.
   **Instead:** give it its own **visible** window — drag the tab out, small but
   neither minimized nor covered.
4. **Do not click the Meet prejoin by coordinates.** It is flaky and depends on
   device-pixel scaling. **Instead:** submit the name form and click Join via
   in-page JS that pierces shadow DOM (below).
5. **Do not reschedule into the same room.** The CRM verifies a cached room with
   a GET that races the async DELETE. **Instead:** `DELETE` the room, poll until
   it returns 404, then schedule.

## The frame-cycling fake camera

Extract the clip to JPEGs, load them as `ImageBitmap`s in the page, and paint
them onto a canvas on a timer. `canvas.captureStream()` on that canvas is a
rock-solid video track.

Pre-extract frames (per clip), served over a tiny CORS+range HTTP server:

```bash
ffmpeg -y -i clip.mp4 -vf "fps=12,scale=640:360" -q:v 6 frames/f_%03d.jpg
# serve frames/ over http with CORS + Range (a threaded Python server works)
```

Inject before the Meet app loads (run in the page via the extension's
`javascript_tool`, immediately after navigating to the room URL):

```js
(async () => {
  const N = 114; // number of frames
  const urls = Array.from({length: N}, (_, i) =>
    `http://localhost:8899/frames/f_${String(i+1).padStart(3,'0')}.jpg`);
  const bitmaps = [];
  for (let i = 0; i < N; i += 20) {                     // load in chunks
    const chunk = await Promise.all(urls.slice(i, i+20).map(
      async u => createImageBitmap(await (await fetch(u)).blob())));
    bitmaps.push(...chunk);
  }
  const canvas = document.createElement('canvas');
  canvas.width = 640; canvas.height = 360;
  const ctx = canvas.getContext('2d');
  let idx = 0;
  setInterval(() => {                                    // ~12 fps
    ctx.drawImage(bitmaps[idx], 0, 0, 640, 360);
    idx = (idx + 1) % bitmaps.length;
  }, 83);
  const silentAudio = () => {                            // Meet wants an audio track
    const ac = new AudioContext(), osc = ac.createOscillator(),
          g = ac.createGain(), d = ac.createMediaStreamDestination();
    g.gain.value = 0.0001; osc.connect(g).connect(d); osc.start();
    return d.stream.getAudioTracks()[0];
  };
  navigator.mediaDevices.getUserMedia = async (c = {}) => {
    const s = new MediaStream();
    if (c.video) s.addTrack(canvas.captureStream(30).getVideoTracks()[0]);
    if (c.audio) s.addTrack(silentAudio());
    return s;
  };
  navigator.mediaDevices.enumerateDevices = async () => [
    { kind:'videoinput', deviceId:'stock-cam', groupId:'g1', label:'Stock Camera', getCapabilities(){return {}}, toJSON(){return this} },
    { kind:'audioinput', deviceId:'stock-mic', groupId:'g1', label:'Stock Microphone', getCapabilities(){return {}}, toJSON(){return this} },
  ];
})();
```

Submit the Meet prejoin reliably from JS (pierces shadow DOM):

```js
const findAll = (sel) => { const o=[]; const w=r=>{o.push(...r.querySelectorAll(sel));
  for (const e of r.querySelectorAll('*')) if (e.shadowRoot) w(e.shadowRoot);}; w(document); return o; };
const input = findAll('input').find(i => i.offsetParent);
const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
setter.call(input, 'John Doe');
input.dispatchEvent(new Event('input', { bubbles: true }));
input.dispatchEvent(new Event('change', { bubbles: true }));
await new Promise(r => setTimeout(r, 300));
findAll('button').find(b => b.offsetParent && b.textContent.trim() === 'Join Meeting').click();
```

## Full procedure

1. **Bring up the stack** — the demo app lives in its own repo, not this one
   (the CRM demo starts with its `deploy/up.sh`) — and seed demo data (user,
   client, issue, a *future* meeting so the **Join** button shows).
2. **Source the clips** — Pexels works well (front-facing, calm, office
   setting; avoid side profiles, big arm-waving, and over-the-shoulder shots
   that read as in-person). Extract each to JPEG frames.
3. **Second participant (the "client")**: in real Chrome, open the client's
   member access URL, inject their fake camera, submit the prejoin. Then
   **pop the tab into its own visible window** so its canvas keeps painting.
4. **Recorded participant (the "user")**: in a second tab/window, inject their
   fake camera, then walk the app: sign in → issue → **Join** → prejoin →
   join. This tab is the one you record.
5. **Capture** — the extension's `gif_creator` records a frame per action, so
   the *meeting* portion is not smooth. Use it only to confirm the flow;
   rebuild the meeting segment with ffmpeg (next).

## Compositing the smooth meeting segment (ffmpeg)

Take one real screenshot of the embedded meeting as a static **plate** (real
CRM chrome, sidebar, toolbar), then overlay each clip into its tile rectangle
and draw name-label chips. Tile rects are measured from the plate.

```bash
# label chips (ImageMagick handles text cleanly; ffmpeg drawtext is fiddly)
convert -background "rgba(0,0,0,0.6)" -fill white -font DejaVu-Sans-Bold \
  -pointsize 12 -gravity center -size 98x21 caption:"Joanna Doe" label-main.png
convert -background "rgba(0,0,0,0.6)" -fill white -font DejaVu-Sans-Bold \
  -pointsize 12 -gravity center -size 92x20 caption:"Alex Ramírez" label-self.png

# plate + main clip (big tile) + self-view clip (corner) + labels
ffmpeg -y -loop 1 -t 8 -i meeting-plate.png \
  -stream_loop -1 -t 8 -ss 3 -i main.mp4 \
  -stream_loop -1 -t 8 -ss 2 -i selfview.mp4 \
  -i label-main.png -i label-self.png \
  -filter_complex "\
    [1:v]scale=1019:569,setsar=1[j];\
    [2:v]scale=175:98,setsar=1[a];\
    [0:v][j]overlay=303:119[b1];\
    [b1][a]overlay=1158:590[b2];\
    [b2][3:v]overlay=305:121[b3];\
    [b3][4:v]overlay=1160:592,crop=1512:798:0:0[out]" \
  -map "[out]" -r 30 -c:v libx264 -crf 22 -preset medium -pix_fmt yuv420p \
  meeting-segment.mp4
```

Notes:
- Overlaying the main clip covers the plate's baked-in person and label, so the
  label chip you draw on top is what shows — this is how you **rename** a
  participant without re-recording (e.g. relabel to match a woman's clip).
- `crop=W:H:0:0` fixes "height not divisible by 2" from odd screenshot sizes.
- `-ss` into each clip skips awkward openings (a wave, a hand near the face).

## Assembling the final loop

Lead-up screens are static UI — capture them crisply with **headless
Playwright** at the exact video resolution (1512×798), one still per screen.
Turn each still into a short clip, then concat with the meeting segment:

```bash
mk() { ffmpeg -y -loop 1 -t "$2" -i "$1" \
  -vf "scale=1512:798,setsar=1,format=yuv420p" -r 30 \
  -c:v libx264 -crf 22 -preset medium "$3"; }
mk 01-login.png   1.1 s1.mp4
mk 02-clients.png 0.9 s2.mp4
mk 03-issues.png  0.9 s3.mp4
mk 04-issue.png   1.4 s4.mp4
ffmpeg -y -t 5.5 -i meeting-segment.mp4 -r 30 -c:v libx264 -crf 22 s5.mp4

printf "file 's1.mp4'\nfile 's2.mp4'\nfile 's3.mp4'\nfile 's4.mp4'\nfile 's5.mp4'\n" > concat.txt
ffmpeg -y -f concat -safe 0 -i concat.txt \
  -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p -movflags +faststart \
  crm-meet-demo.mp4
```

Embed in the post right after the `<!-- more -->` excerpt marker:

```html
<video autoplay muted loop playsinline width="100%" style="border-radius:10px;">
  <source src="/assets/images/blog/YYYY/MM/<slug>/crm-meet-demo.mp4" type="video/mp4">
</video>
```

(`YYYY/MM/<slug>` is the post's asset folder — the literal placeholder on a
draft, the real year/month once published; see the `blog-write` skill.)

## Honesty / caption

The participants are stock footage, not real customers — say so in the caption
("participant video is stock footage"). Don't imply the faces are real users.

## Gotchas checklist

- [ ] Meeting needs a *future* date for the Join button to appear.
- [ ] Second participant in its **own visible window** (else black tile).
- [ ] Inject the fake camera **after** navigating to the room, **before** join.
- [ ] Fresh room per take: DELETE + poll for 404 before rescheduling.
- [ ] Same output filename across re-records → hard-refresh (Ctrl-Shift-R) to
      beat the browser/CDN cache when reviewing.
