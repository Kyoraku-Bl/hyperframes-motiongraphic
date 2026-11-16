# REVIEW.md — Dead Page to Machine

**Business:** Silent Sellers
**Marketing angle:** Transformation — dead page to booking machine in 48 hours
**Reviewed:** 2026-11-16 · HyperFrames CLI 0.9.13
**Deliverable:** `reel.mp4` — 1080 × 1920, 30 fps, 7.000 s / 210 frames, H.264 + AAC stereo
**Format:** 7-second client magnet with urgent salesman VO (buy-now copy)

## Validation

```text
npx hyperframes lint  . --json   → ok true · 0 errors · 0 warnings · 6 files
npx hyperframes check . --json   → ok true · browserSkipped false
    lint / runtime / layout / motion / contrast / audio / craft : 0 errors, 0 warnings
npx hyperframes check . --snapshots --json → ok true · 5 frames (0.389/1.944/3.5/5.056/6.611 s)
npx hyperframes render . -o reel.raw.mp4 -f 30 -q looks --workers 2 → exit 0
    9.6 MB · 7.0 s · rendered in 38.2s
ffmpeg transcode (CRF 21, faststart) → 4021983 B · 7.000000 s
audio QA → -17.30 LUFS integrated · -3.49 dBTP true peak · 0 clips
```

Zero warnings anywhere.

Dialogue is two urgent lines in the salesman voice (voice-03): the shout
hook (DEAD PAGE?!…, 0.15 s) and the buy-now close (2.55 s, "now / today /
right now" urgency + direct CTA). Takes were pre-timed with
pitch-preserving `atempo` (open 1.02×, angle natural at 1.0×) and slotted at gapless-decoded
length at 1.0×. Captions are synced verbatim to the VO. The hook text holds
from frame 1.

PUNCH FX package: hook shake + highlight re-punch, flash frames on the hook
slam / punch entrance / loop sting, speed-line rush into the punch, caption
highlight zoom-punches, whip-hit SFX under the hook slam + punch entrance,
ping sting on the loop hold. No duo (style purity), no music (halal policy:
VO + foley SFX only). Loop engineering: 03-loop holds plate A frozen at the
exact frame-0 cam/shake state + the hook scrim, captions hidden, FX at rest.

## Visual QA

All 7 seconds were pulled from the *rendered MP4* (t = 0.5–6.5 s) and inspected
as a contact sheet, plus the 5 `check --snapshots` frames:

- Shout hook DEAD PAGE?! / TO MACHINE?! / 48 HOURS?! on screen from frame 1; plate-A push-in behind it.
- Punch sticker (BEFORE / AFTER) slams at 2.5 s with pill + handle;
  5 word-by-word caption groups, always visible, sound-off readable.
- **Loop:** frame 0 vs frame 209 mean absolute pixel diff **9.91/255**
  — both ends show the same plate + hook (end-time sampling catches the wrap),
  matching the house loop norm; inspected, no jump.
- **Faceless cast:** any people in the vector art are eyeless; rendered
  frames + cover inspected. Zero text baked into plates.

## What makes this angle travel (and convert)

Before/after is the most shared shape on business Instagram: the brain can't resist a transformation, and "48 hours" makes it feel achievable rather than fantasy. The salesman's "DM FLIP now" converts the envy directly into project inquiries.

## Launch checklist

Post 12:30–14:00 Africa/Casablanca. Audio: trending transformation dialogue, low under VO. Pinned comment: "DM me 'FLIP' and I'll flip yours 👇". Mechanic: saves + before/after shares.

Trial-Reel first; compare against other trials, never against profile reels.

## Publish kit

`tools/make_delivery.py` → `delivery/` + `reel-40-dead-machine-delivery.zip`.
Cover is drawn from plate A with the shout headline, kicker, per-reel CTA
pill and handle inside safe zones. No music is baked in (music-free by
design) — optionally attach a trending non-music spoken-word or nature audio
at low volume under the voiceover in the Instagram editor.

SHA-256 (`reel.mp4`): `03732c71b4d837f22e81d3b23d4835eb65d99d5635d0443b0ea7386c719343cc`
