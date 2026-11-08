# REVIEW.md — Losing Is Expensive

**Business:** El Fuego Tacos
**Marketing angle:** Objection crusher — losing customers costs more than a site
**Reviewed:** 2026-11-08 · HyperFrames CLI 0.9.13
**Deliverable:** `reel.mp4` — 1080 × 1920, 30 fps, 18.000 s / 540 frames, H.264 + AAC stereo

## Validation

```text
npx hyperframes lint  . --json   → ok true · 0 errors · 0 warnings · 7 files
npx hyperframes check . --json   → ok true · browserSkipped false
    lint / runtime / layout / motion / contrast / audio : 0 errors, 0 warnings
    craft: 0 errors, 2 warnings (see below)
npx hyperframes check . --snapshots --json → ok true · 5 frames (1/5/9/13/17 s)
npx hyperframes render . -o reel.raw.mp4 -f 30 -q looks --workers 2 → exit 0
    44.8 MB · 18.0 s · rendered in 2m 6.2s
ffmpeg transcode (CRF 21, faststart) → 13925749 B · 18.000000 s
audio QA → -16.67 LUFS integrated · -2.91 dBTP true peak · 0 clips
```

Two accepted `craft / line_unread` warnings on the end card (house spec fixes
that card at 16.5–18 s; documented in `STYLE.md`).

Dialogue is five lines, four in the salesman voice (voice-03): the shout hook
(NO!…, 0.15–3.00 s), the angle line (3.05–8.05 s), and the house benefit
+ CTA texts (takes reused from Reels 09–13). The "thanks" line stays the
customer voice (voice-00). Takes were pre-timed with pitch-preserving `atempo`
(max 1.31×; one short shout kept natural at 1.0×) and slotted at
gapless-decoded length. Two hooks were re-recorded shorter after pace QA so
nothing exceeds the natural-energy ceiling. The hook text holds the full
first 3 s at 110 px per the explicit request.

## Visual QA

All 18 seconds were pulled from the *rendered MP4* (t = 0.5–17.5 s) and inspected
as a contact sheet, plus the 5 `check --snapshots` frames:

- Shout hook NO! / NO! / NOOO!! on screen for the full first 3 s; no intro or fade-in.
- 17 word-by-word caption groups, always visible and inside the
  lower-middle safe band; sound-off readable throughout.
- Taco truck menu with combo prices + ORDER NOW; phone mini-site; lock screen +
  notification toast with the story-specific time (9:33).
- Selfie CTA, "Your website. Done for you." end card, loop-back to the exact
  opening plate + hook line.
- **Loop:** frame 0 vs frame 539 mean absolute pixel diff **6.91/255**.
- Snapshot capture again blanked the 9 s phone frame on every Reel this run;
  the rendered MP4s all show the full site + caption (transient capture race).

## What makes this angle create the need

"Too expensive" dies on arithmetic: one lost customer a week costs more than a site all year. The viewer counts their own walkaways, then sees orders arriving while they cook. The CTA asks for a free mockup by DM, so the need converts
immediately.

## Publish kit

`tools/make_delivery.py` → `delivery/` + `reel-18-losing-expensive-delivery.zip`.
Cover is drawn from the clean establish plate with the shout headline, kicker,
CTA pill and handle inside safe zones. No music is baked in — add a low-volume
trending track in the Instagram editor and set the cover JPG as the Reel cover.

SHA-256 (`reel.mp4`): `edfaeb3b06e3a79045242f57c160d0b750ca2887e3192b88b42c305c61d71e61`
