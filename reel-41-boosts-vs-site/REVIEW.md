# REVIEW.md — Boosts vs Site

**Business:** Boost Burners
**Marketing angle:** Price proof — two boosts die in a day, a site sells forever
**Reviewed:** 2026-11-16 · HyperFrames CLI 0.9.13
**Deliverable:** `reel.mp4` — 1080 × 1920, 30 fps, 7.000 s / 210 frames, H.264 + AAC stereo
**Format:** 7-second SILENT client magnet (kinetic text, no voice, no music)

## Validation

```text
npx hyperframes lint  . --json   → ok true · 0 errors · 0 warnings · 6 files
npx hyperframes check . --json   → ok true · browserSkipped false
    lint / runtime / layout / motion / contrast / audio / craft : 0 errors, 0 warnings
npx hyperframes check . --snapshots --json → ok true · 5 frames (0.389/1.944/3.5/5.056/6.611 s)
npx hyperframes render . -o reel.raw.mp4 -f 30 -q looks --workers 2 → exit 0
    8.7 MB · 7.0 s · rendered in 1m 2.7s
ffmpeg transcode (CRF 21, faststart) → 3627684 B · 7.000000 s
audio QA → -29.07 LUFS integrated · -7.68 dBTP true peak · 0 clips (SFX-only mix)
```

Zero warnings anywhere. (Handle pill was made fully opaque during this batch
after a contrast warning on bright plates; re-validated clean.)

Voice: none — silent kinetic reel by decision (no founder voice available,
no TTS: removes the suspected 1.7 s scroll-killer). The script lives in the
timed captions: the shout hook (2 BOOSTS?!…, 0.15 s) and the punch line
(2.55 s), word-by-word with highlight zoom-punches. Audio bed is foley SFX
only: whip hits on the hook slam + punch entrance, click on the pill pop,
ping sting on the loop hold, room tone. No music (halal policy).

PUNCH FX package: hook shake + highlight re-punch, flash frames on the hook
slam / punch entrance / loop sting, speed-line rush into the punch. No duo
(style purity). Loop engineering: 03-loop holds plate A frozen at the exact
frame-0 cam/shake state + the hook scrim, captions hidden, FX at rest.

## Visual QA

All 7 seconds were pulled from the *rendered MP4* (t = 0.5–6.5 s) and inspected
as a contact sheet, plus the 5 `check --snapshots` frames:

- Shout hook 2 BOOSTS?! / OR A SITE?! / FOREVER?! on screen from frame 1; plate-A push-in behind it.
- Punch sticker (PAY ONCE / SELL DAILY) slams at 2.5 s with pill + handle;
  5 word-by-word caption groups carry the full script sound-off.
- **Loop:** frame 0 vs frame 209 mean absolute pixel diff **8.61/255**
  — both ends show the same plate + hook (end-time sampling catches the wrap),
  matching the house loop norm; inspected, no jump.
- **Faceless cast:** any people in the vector art are eyeless; rendered
  frames + cover inspected. Zero text baked into plates.

## What makes this angle travel (and convert)

A forced choice ("two boosts or a site?") with a hated loser (burning money) and forever upside: the viewer does the math themselves, which persuades harder than any claim. Money comparisons travel; "Comment PRICE" captures the demand.

## Launch checklist

Post 19:30–22:30 Africa/Casablanca. Audio: trending money-talk dialogue, low. Pinned comment: "Comment PRICE and I'll DM you the list 👇". Mechanic: comment-to-DM automation.

Trial-Reel first; compare against other trials, never against profile reels.

## Publish kit

`tools/make_delivery.py` → `delivery/` + `reel-41-boosts-vs-site-delivery.zip`.
Cover is drawn from plate A with the shout headline, kicker, per-reel CTA
pill and handle inside safe zones. No music is baked in (music-free by
design) — optionally attach a trending non-music spoken-word or nature audio
at low volume in the Instagram editor, or post with original audio.

SHA-256 (`reel.mp4`): `b8034875e60b3daa67f0023b5697335a64e9875a16fc2a4bf81aefba79babbb6`
