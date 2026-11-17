# REVIEW.md — The Big Client

**Business:** Atlas Woodworks
**Marketing angle:** Legitimacy gate — a website makes you credible to bigger clients
**Reviewed:** 2026-11-06 · HyperFrames CLI 0.9.13
**Deliverable:** `reel.mp4` — 1080 × 1920, 30 fps, 18.000 s / 540 frames, H.264 + AAC stereo

## Validation

```text
npx hyperframes lint  . --json   → ok true · 0 errors · 0 warnings · 7 files
npx hyperframes check . --json   → ok true · browserSkipped false
    lint / runtime / layout / motion / contrast / audio : 0 errors, 0 warnings
    craft: 0 errors, 2 warnings (see below)
npx hyperframes check . --snapshots --json → ok true · 5 frames (1/5/9/13/17 s)
npx hyperframes render . -o reel.raw.mp4 -f 30 -q looks --workers 2 → exit 0
    45.8 MB · 18.0 s · rendered in 1m 49.9s
ffmpeg transcode (CRF 21, faststart) → 13292762 B · 18.000000 s
audio QA → -16.89 LUFS integrated · -2.10 dBTP true peak · 0 clips
```

`check` still emits two `craft / line_unread` warnings on the end card
(`"Your website."` 0.94 s, `"Done for you."` 0.87 s), both under the CLI's generic
2.00 s closing-line rule. The house spec fixes that card at 16.5–18 s and requires
the loop-back to begin before 18 s, so the exact wording and timing were kept —
an accepted spec-vs-heuristic trade-off, documented in `STYLE.md`.

Dialogue is five lines: the hook (THE BIG CLIENT…) and the angle
line are fresh takes pre-timed with pitch-preserving `atempo` to their windows
(angle window widened to 6.65 s), with slots set to the gapless-decoded MP3
length at 1.0× so `clip_media_fit` stays silent; the remaining three lines are
the house VO.

## Visual QA

All 18 seconds were pulled from the *rendered MP4* (t = 0.5–17.5 s) and inspected
as a contact sheet, plus the 5 `check --snapshots` frames:

- Hook THE BIG CLIENT / SAID YES / THEN: YOUR SITE? from frame 1; no intro or fade-in.
- 20 word-by-word caption groups, always visible and inside the
  lower-middle safe band; sound-off readable throughout.
- Woodwork portfolio with build prices + ENQUIRE NOW; phone mini-site; lock screen +
  notification toast with the story-specific time (4:18).
- Selfie CTA, "Your website. Done for you." end card, loop-back to the exact
  opening plate + hook line.
- **Loop:** frame 0 vs frame 539 mean absolute pixel diff **7.68/255**,
  in the same band as Reels 01–03 (8.23 / 8.13 / 9.38) — residual is
  deterministic grain/flicker, not a composition jump.
- One `check --snapshots` pass captured a blank phone screen at 9 s on two
  Reels; the rerun and the rendered MP4 both show the full site + caption, so
  it was a transient capture race, not a content defect.

## What makes this angle create the need

Forty desks, one email, zero reply after "what is your website?". The viewer sees that big clients do not doubt the craft — they doubt what they cannot forward to their boss. A website is not just a finder, it is a credential that unlocks bigger cheques. The CTA asks for a free mockup by DM, so the need converts
immediately.

## Publish kit

`tools/make_delivery.py` → `delivery/` (`cover.jpg`, `caption.txt`,
`hashtags.txt`, `README.txt`, `reel.mp4` link) + `reel-08-the-big-client-delivery.zip`.
Cover is drawn from the clean establish plate with the hook headline, kicker,
CTA pill and handle inside safe zones. No music is baked in — add a low-volume
trending track in the Instagram editor and set the cover JPG as the Reel cover.

SHA-256 (`reel.mp4`): `ab4f3829956f678a08a5cd6516c28c33a7daab4b6ad9720f09345a175bb93663`
