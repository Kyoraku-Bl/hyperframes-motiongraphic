# THIS CAFÉ IS LOSING CUSTOMERS EVERY DAY — HyperFrames Reel

An editable, self-contained **HyperFrames HTML composition** for an 18-second vertical
Instagram Reel. No network calls, no runtime dependencies, no music bed.

| | |
|---|---|
| Canvas | 1080 × 1920 (9:16) |
| Frame rate | 30 fps |
| Duration | 18.00 s / 540 frames |
| Output | `reel.mp4` (H.264 + AAC, 13 MB) |
| Timeline | `index.html` + six subcompositions in `compositions/` |
| Docs | `SPEC.md` (build spec), `STORYLINES.md` (story decision), `REVIEW.md` (QA record), `STYLE.md` (locked house style + delivery contract for all future Reels) |
| Publish kit | `delivery/` + `cafe-reel-delivery.zip` — cover, caption, hashtags and the MP4 in one download |

## Open / edit

```bash
# From a checkout that has the HyperFrames CLI available:
npx hyperframes play . --no-open      # lightweight browser player
npx hyperframes preview .             # full HyperFrames desktop app / Studio
```

The project also opens directly in the HyperFrames desktop app: point it at this
`cafe-reel/` folder. Everything the composition needs is local:

- `assets/plates/` — 13 painted anime plates (1080 × 1920 unless noted)
- `assets/audio/` — 7 generated WAV ambience/SFX beds + 8 trimmed dialogue MP3s
- `assets/ref/` — identity crops from the supplied character sheet
- `assets/lib/gsap.min.js` — vendored GSAP 3.15.0 (renders never hit a CDN)

## Editable knobs

`meta.json` declares four composition variables, also visible in the desktop app:
`hook` (headline), `endline` (end card), `handle` (@sitely_studioo), `accent`
(dark green `#1F4736`). Shot timing lives in `index.html` (`data-start` /
`data-duration` on each `.clip`); per-shot animation lives in the matching
`compositions/*.html` GSAP timelines. Subtitle groups are in
`compositions/06-captions.html`; audio placement is in `index.html`.

## Validate / re-export

```bash
npx hyperframes lint . --json
npx hyperframes check . --json
npx hyperframes snapshot . --review
npx hyperframes render . -o reel.mp4 -f 30 -q looks --workers 2
```

Regenerate the sound beds with `/home/user/.pyvenv/bin/python tools/make_audio.py`.
`tools/trim_voices.py` documents the one-time room-tone/pause trim applied to the
generated dialogue MP3s.

## Publish kit

Every Reel ships a cover, caption, hashtags and a downloadable master. Edit
`delivery.json`, then run:

```bash
python tools/make_delivery.py        # needs Pillow + NumPy
```

It writes `delivery/{cover.jpg,reel.mp4,caption.txt,hashtags.txt,README.txt}` and
`cafe-reel-delivery.zip`. The reusable rules are in `STYLE.md`.

## Sound design

Natural café room tone, espresso/chatter/door-bell texture, footsteps, laptop
click, notification ping, ceramic cup on wood, cloth movement — plus eight
natural dialogue performances. **No music**, by design: headroom is left for a
low-volume trending track added in the Instagram editor. Every line is also
captioned, so the Reel reads completely with sound off.
