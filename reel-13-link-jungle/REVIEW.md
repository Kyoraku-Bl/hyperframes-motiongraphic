# REVIEW.md — The Link Jungle

**Business:** Retro Rack Thrift
**Marketing angle:** Link chaos — five bio links, zero clarity
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
    43.3 MB · 18.0 s · rendered in 1m 59.6s
ffmpeg transcode (CRF 21, faststart) → 13138217 B · 18.000000 s
audio QA → -16.69 LUFS integrated · -1.70 dBTP true peak · 0 clips
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

- Shout hook STOP! / LOOK AT / THIS! on screen for the full first 3 s; no intro or fade-in.
- 17 word-by-word caption groups, always visible and inside the
  lower-middle safe band; sound-off readable throughout.
- Thrift shop with vintage prices + SHOP NOW; phone mini-site; lock screen +
  notification toast with the story-specific time (5:41).
- Selfie CTA, "Your website. Done for you." end card, loop-back to the exact
  opening plate + hook line.
- **Loop:** frame 0 vs frame 539 mean absolute pixel diff **7.43/255**,
  in the same band as Reels 01–08 — residual is deterministic grain/flicker.
- Snapshot capture again blanked the 9 s phone frame on some Reels; the
  rendered MP4s all show the full site + caption (transient capture race).

## What makes this angle create the need

WhatsApp here, a form there, prices somewhere else: buyers get lost and leave, because confused people do not buy. The viewer sees their own link jungle, then one home where everything ends in one tap. The CTA asks for a free mockup by DM, so the need converts
immediately.

## Publish kit

`tools/make_delivery.py` → `delivery/` + `reel-13-link-jungle-delivery.zip`.
Cover is drawn from the clean establish plate with the shout headline, kicker,
CTA pill and handle inside safe zones. No music is baked in — add a low-volume
trending track in the Instagram editor and set the cover JPG as the Reel cover.

SHA-256 (`reel.mp4`): `e96b3ab8e2f476365933f6b85c5750a832043db1efce2b23b00726998498fe20`
