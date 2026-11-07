# REVIEW.md — Stop the DM Pile-Up

**Business:** Lina's Boutique
**Marketing angle:** DM overload — slow replies send buyers elsewhere
**Reviewed:** 2026-11-07 · HyperFrames CLI 0.9.13
**Deliverable:** `reel.mp4` — 1080 × 1920, 30 fps, 18.000 s / 540 frames, H.264 + AAC stereo

## Validation

```text
npx hyperframes lint  . --json   → ok true · 0 errors · 0 warnings · 7 files
npx hyperframes check . --json   → ok true · browserSkipped false
    lint / runtime / layout / motion / contrast / audio : 0 errors, 0 warnings
    craft: 0 errors, 2 warnings (see below)
npx hyperframes check . --snapshots --json → ok true · 5 frames (1/5/9/13/17 s)
npx hyperframes render . -o reel.raw.mp4 -f 30 -q looks --workers 2 → exit 0
    43.4 MB · 18.0 s · rendered in 2m 0.4s
ffmpeg transcode (CRF 21, faststart) → 13096368 B · 18.000000 s
audio QA → -16.71 LUFS integrated · -1.76 dBTP true peak · 0 clips
```

Two accepted `craft / line_unread` warnings on the end card (house spec fixes
that card at 16.5–18 s; documented in `STYLE.md`).

Dialogue is five lines, four in the salesman voice (voice-03): the shout hook
(STOP!…, 0.15–3.00 s), the angle line (3.05–8.05 s), and the house benefit
+ CTA texts re-recorded so the whole pitch stays in one convincing voice. The
"thanks" line stays the customer voice (voice-00). Takes were pre-timed with
pitch-preserving `atempo` (max 1.29×; two short shouts kept natural at 1.0×
with a trailing beat) and slotted at gapless-decoded length, so
`clip_media_fit` stays silent. The hook text was extended to the full first
3 s at 110 px per the explicit request.

## Visual QA

All 18 seconds were pulled from the *rendered MP4* (t = 0.5–17.5 s) and inspected
as a contact sheet, plus the 5 `check --snapshots` frames:

- Shout hook STOP! / STOP! / STOP! on screen for the full first 3 s; no intro or fade-in.
- 18 word-by-word caption groups, always visible and inside the
  lower-middle safe band; sound-off readable throughout.
- Boutique site with dress prices + SHOP NOW; phone mini-site; lock screen +
  notification toast with the story-specific time (9:12).
- Selfie CTA, "Your website. Done for you." end card, loop-back to the exact
  opening plate + hook line.
- **Loop:** frame 0 vs frame 539 mean absolute pixel diff **6.72/255**,
  in the same band as Reels 01–08 — residual is deterministic grain/flicker.
- Snapshot capture again blanked the 9 s phone frame on some Reels; the
  rendered MP4s all show the full site + caption (transient capture race).

## What makes this angle create the need

Every "price please" waits hours in the DMs while buyers tap away to faster shops. The viewer feels their own inbox chaos, then sees the fix: prices shown, orders taken, money collected — day and night, even asleep. The CTA asks for a free mockup by DM, so the need converts
immediately.

## Publish kit

`tools/make_delivery.py` → `delivery/` + `reel-09-dm-pileup-delivery.zip`.
Cover is drawn from the clean establish plate with the shout headline, kicker,
CTA pill and handle inside safe zones. No music is baked in — add a low-volume
trending track in the Instagram editor and set the cover JPG as the Reel cover.

SHA-256 (`reel.mp4`): `646988ce3d78f8b5a7d05202fdcd079f53d31ed3832d1015510e79ee9e5bf443`
