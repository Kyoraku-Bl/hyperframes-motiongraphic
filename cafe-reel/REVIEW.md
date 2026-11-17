# REVIEW.md — QA record

**Project:** `cafe-reel/` — "THIS CAFÉ IS LOSING CUSTOMERS EVERY DAY"
**Reviewed:** 2026-11-05 · HyperFrames CLI 0.9.13
**Deliverable:** `reel.mp4` — 1080 × 1920, 30 fps, 18.000 s / 540 frames, H.264 + AAC stereo, 12.7 MB

## 1. Format & timeline

| Requirement | Result |
|---|---|
| 1080 × 1920 (9:16) | ✅ `ffprobe` 1080 × 1920 |
| 30 fps | ✅ `r_frame_rate 30/1`, 540 frames rendered and encoded |
| Exactly 18 s | ✅ `duration 18.000000` |
| Hook from frame 1 | ✅ headline is on screen at t=0 (no intro/fade/logo); `snapshot` at 0.3 s confirms |
| New angle every 1.5–3 s | ✅ 15 timed shot clips across 4 host compositions; shot 3 cuts every ~1.15 s |
| Clean loop | ✅ frame 539 restores plate 01 + the hook line + the exact t=0 camera transform (`translate(-53px,12px) scale(1.16)`). Measured frame-0 vs frame-539 mean absolute pixel diff **8.02/255 (3.1%)** — residual is deterministic grain/flicker/dust and the hook-word pop, not a composition jump |
| Sound-off readable | ✅ 17 word-by-word caption groups cover 0.15–16.50 s plus the end card; every reviewed beat shows a caption |
| Safe zones | ✅ headline at y≈302, captions at y≈1148, end card at y≈800; top 270 px / bottom 480 px stay clear of text, faces within the central 60% |

`npx hyperframes timeline . --json` → `duration: 18`, graphics + captions + audio tracks parse cleanly.

## 2. Validation commands and results

```text
npx hyperframes lint  . --json   → ok true · 0 errors · 0 warnings · 0 info · 7 files scanned
npx hyperframes check . --json   → ok true · browserSkipped false
    lint      0 errors / 0 warnings
    runtime   0 / 0        layout   0 / 0        motion   0 / 0
    contrast  0 / 0        audio    0 / 0
    craft     0 errors / 2 warnings   (see §5)
npx hyperframes audio reel.mp4 --json → 0 warnings
    -16.9 LUFS integrated · -15.8 LUFS short-term max
    -1.4 dBTP true peak · 0 clipped samples
    signal from 0.19 s to 17.77 s (final 0.27 s is the room-tone fade-out)
npx hyperframes render . -o reel.mp4 -f 30 -q looks --workers 2 → exit 0, 540/540 frames
```

`npx hyperframes check . --snapshots --json` → `ok true`, five contrast-pass PNGs saved
at 1 / 5 / 9 / 13 / 17 s, no finding files. The 17 s frame confirms the cream end card
centred in the safe zone over a darkened plate.

`npx hyperframes usage --json` returns `status: unknown / unsupported_harness` in this
sandbox; no quota/telemetry data is available here.

### Render-safety fix
The first render failed with `sub_timeline_script_failure`: the root HTML loaded GSAP
from `cdn.jsdelivr.net` and the browser reported `ERR_CONNECTION_CLOSED`, leaving all
seven timelines unbuilt. GSAP 3.15.0 is now vendored at `assets/lib/gsap.min.js` and
every `<script src>` is local. `check --json` succeeded even before this fix, so both
lint/check **and** a real render were required to catch it.

## 3. Visual review

`npx hyperframes snapshot . --review` produced the beat sheet, phone-width sheet and
five-frame seam strips. Because the project uses nested subcompositions, the CLI asked
for per-composition review; all five were run and inspected:

```text
snapshot . --review --composition hook   | pitch | proof | cta | fx
```

- **hook (0–3 s):** tracking plate → sidestep → spin-to-camera; headline from frame 1;
  barista line and eyebrow-raise beat read clearly; owner staring at his phone is present.
- **pitch (3–8 s):** OTS with crossed arms, laptop turn, drawn website with `$4.50 /
  $5.00 / $6.50` prices, food photos and green WhatsApp order button; push-in on the
  worried owner; lean-back smile. Hero text was moved to a top cream gradient with dark
  type and the pastry image re-cropped (`object-position: 50% 88%`) after the first
  pass showed it washed out.
- **proof (8–13 s):** phone mini-site, `NEW ORDER` lock-screen toast with ping,
  handoff/crowd, handshake-into-hug. Overlay coordinates were measured against the
  plates so the site sits inside the drawn phone screen.
- **cta (13–18 s):** selfie angle with owner/crowd behind, end card, loop-back frame.
- **fx (0–18 s):** grain, flicker, bloom, dust, vignette, two smear frames, one impact
  flash, whip-pan speed lines, steam. All deterministic GSAP, no randomness/timers.

Three plates (`04-owner`, `07-phone-web`, `10-hug`) were generated with cream/black
letterbox margins. These were removed with mirrored, defocus-edged extensions and the
seams inpainted, so the drawn phone/UI overlays stayed aligned. All 13 plates are now
full-bleed 1080 × 1920 (except the deliberate horizontal pastry strip).

## 4. Sound

- 18 s café room tone (espresso, chatter, door bell, muffled street) at low volume.
- Six placed SFX: footsteps, laptop, whip, notification ping, ceramic cup, cloth.
- Eight trimmed dialogue MP3s, three distinct natural voices, consistent lead voice
  across all four shots; leading/trailing room tone and long internal pauses trimmed by
  `tools/trim_voices.py`.
- **No music**, by instruction — headroom is left for a low-volume trending track in
  the Instagram editor. Every line is captioned.

## 5. Accepted warnings / known limits

1. **Two `craft / line_unread` warnings** on the end card: `"Your website."` (0.94 s)
   and `"Done for you."` (0.86 s) are below the CLI's generic 2.00 s closing-line rule.
   The user's script explicitly places that text at 16.5–18 s and requires the loop-back
   to start before 18 s, so the exact wording and timing were kept. This is a deliberate
   spec-vs-heuristic trade-off, not an oversight.
2. **Animation fidelity.** This is an *editable HTML composition* built from 13 painted
   plates animated with deterministic GSAP camera moves, cuts, parallax, smear frames
   and overlay UI. It is not a frame-by-frame 2D animation: per-frame redraw effects
   such as true heel-to-toe gait cycles, lip-sync, blinking, breathing and hoodie/hair
   settle are *implied* by plate selection, cut timing and camera weight rather than
   literally drawn. Meeting the brief's "high-budget feature animation" acting note at
   face value would require a hand-drawn/AI-video character animation pass. Everything
   else (style consistency, framing, pacing, captions, sound) is implemented as asked.
3. **Character likeness** was driven by crops of the supplied reference sheet
   (`assets/ref/`); the plates match the dark curly hair, black oversized hoodie, cargo
   pants, white-grey sneakers, tan skin and brown eyes, but they are stylised renditions,
   not a pixel trace of the sheet.
4. Render used screenshot capture (software GL); the CLI noted this is the slower path,
   but all 540 frames were captured and the artifact validated.

## 6. Preview / export gate

The composition is open in the lightweight HyperFrames player (live preview on
`0.0.0.0:3003`) and can be opened in the **HyperFrames desktop app** by pointing it at
`cafe-reel/`. No CDN, no network fetch and no runtime timer are used, so the preview and
the render are identical. The MP4 was exported after the preview was verified, under the
user's "if I don't reply, feel free to finish everything and export the Reel" instruction.
