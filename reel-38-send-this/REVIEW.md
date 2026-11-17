# REVIEW.md — Send This To Him

**Business:** Friends With No Site
**Marketing angle:** Send-to-friend — the share that saves a business
**Reviewed:** 2026-11-15 · HyperFrames CLI 0.9.13
**Deliverable:** `reel.mp4` — 1080 × 1920, 30 fps, 7.000 s / 210 frames, H.264 + AAC stereo
**Format:** 7-second viral loop machine (standalone builder, not the 18 s template)

## Validation

```text
npx hyperframes lint  . --json   → ok true · 0 errors · 0 warnings · 6 files
npx hyperframes check . --json   → ok true · browserSkipped false
    lint / runtime / layout / motion / contrast / audio / craft : 0 errors, 0 warnings
npx hyperframes check . --snapshots --json → ok true · 5 frames (0.389/1.944/3.5/5.056/6.611 s)
npx hyperframes render . -o reel.raw.mp4 -f 30 -q looks --workers 2 → exit 0
    6.1 MB · 7.0 s · rendered in 34.0s
ffmpeg transcode (CRF 21, faststart) → 2762319 B · 7.000000 s
audio QA → -17.24 LUFS integrated · -3.11 dBTP true peak · 0 clips
```

Zero warnings anywhere — the cleanest validation of any batch (no endcard,
so none of the accepted craft warnings the 18 s reels carry).

Dialogue is two lines in the salesman voice (voice-03): the shout hook
(SEND THIS?!…, 0.15 s) and the punch line (2.55 s). Takes were pre-timed
with pitch-preserving `atempo` (open natural at 1.0×, angle natural at 1.0×) and slotted at
gapless-decoded length at 1.0×. The hook text holds from frame 1.

This batch drops the duo for style purity (the viral-native look carries no
anime faces) and runs **music-free by design**: VO + foley SFX only (whip
hits on the hook slam + punch entrance, ping sting on the loop hold, room
tone). PUNCH FX package: hook shake + highlight re-punch, flash frames on
the hook slam / punch entrance / loop sting, speed-line rush into the punch,
caption highlight zoom-punches.

Loop engineering: 03-loop holds plate A frozen at the exact frame-0
cam/shake state + the hook scrim, captions hidden, FX at rest.

## Visual QA

All 7 seconds were pulled from the *rendered MP4* (t = 0.5–6.5 s) and inspected
as a contact sheet, plus the 5 `check --snapshots` frames:

- Shout hook SEND THIS?! / TO HIM?! / NOW?! on screen from frame 1; plate-A push-in behind it.
- Punch sticker (SEND IT / NOW) slams at 2.5 s with pill + handle;
  6 word-by-word caption groups, always visible, sound-off readable.
- **Loop:** frame 0 vs frame 209 mean absolute pixel diff **7.07/255**
  — both ends show the same plate + hook (end-time sampling catches the wrap),
  matching the house loop norm; inspected, no jump.
- **Faceless cast:** any people in the vector art are eyeless; rendered
  frames + cover inspected. Zero text baked into plates.

## What makes this angle travel

This reel IS its own distribution strategy: it directly instructs the viewer's thumb ("send this to him") at the exact moment they picture one specific friend. Sends per reach is the #1 non-follower signal in 2026 — this is pure signal engineering with a transformation flash as the reward.

## Launch checklist

Post 12:30–14:00 + push to Stories with a question sticker. Audio: trending spoken clip, low under VO. Pinned comment: "Sent it? 📩". Mechanic: pure DM sends — seed by sending it to 5 friends yourself in hour one.

Trial-Reel first; compare against other trials, never against profile reels.

## Publish kit

`tools/make_delivery.py` → `delivery/` + `reel-38-send-this-delivery.zip`.
Cover is drawn from plate A with the shout headline, kicker, per-reel CTA
pill and handle inside safe zones. No music is baked in (music-free by
design) — optionally attach a trending non-music spoken-word or nature audio
at low volume in the Instagram editor, or post with original audio.

SHA-256 (`reel.mp4`): `8c64afa2db5cf82673be508c8ad9447516cc09dac01041ad37d12cde4edbabe5`
