# REVIEW.md — A PDF in 2026?!

**Business:** Café Verona
**Marketing angle:** Menu friction — a broken PDF menu sends diners next door
**Reviewed:** 2026-11-13 · HyperFrames CLI 0.9.13
**Deliverable:** `reel.mp4` — 1080 × 1920, 30 fps, 18.000 s / 540 frames, H.264 + AAC stereo

## Validation

```text
npx hyperframes lint  . --json   → ok true · 0 errors · 0 warnings · 7 files
npx hyperframes check . --json   → ok true · browserSkipped false
    lint / runtime / layout / motion / contrast / audio : 0 errors, 0 warnings
    craft: 0 errors, 2 warnings (see below)
npx hyperframes check . --snapshots --json → ok true · 5 frames (1/5/9/13/17 s)
npx hyperframes render . -o reel.raw.mp4 -f 30 -q looks --workers 2 → exit 0
    41.6 MB · 18.0 s · rendered in 2m 55.1s
ffmpeg transcode (CRF 21, faststart) → 13261965 B · 18.000000 s
audio QA → -16.85 LUFS integrated · -1.78 dBTP true peak · 0 clips
```

Two accepted `craft / line_unread` warnings on the end card (house spec fixes
that card at 16.5–18 s; documented in `STYLE.md`).

Dialogue is five lines, four in the salesman voice (voice-03): the shout hook
(A PDF?!…, 0.15–3.00 s), the angle line (3.05–8.05 s), and the house benefit
+ CTA texts (takes reused from Reels 09–13). The "thanks" line stays the
customer voice (voice-00). Takes were pre-timed with pitch-preserving `atempo`
(open 1.15×, angle 1.08×) and slotted at gapless-decoded length.
The hook text holds the full first 3 s at 110 px per the explicit request.

This batch keeps the PUNCH FX package (hook text shake + highlight re-punch,
flash frames on the hook slam / angle entrance / CTA entrance / endcard slam,
a speed-line rush into the CTA, an endblock power-slam, caption highlight
zoom-punches, whip-hit SFX under the hook + CTA) and the attached duo:
sitely_studioo (salesman) pops with the shout, Salma (happy client) pops on
the thanks beat, and both ride the CTA + cover. Duo portraits are shared
ungraded so the faces stay identical in every Reel.

## Visual QA

All 18 seconds were pulled from the *rendered MP4* (t = 0.5–17.5 s) and inspected
as a contact sheet, plus the 5 `check --snapshots` frames:

- Shout hook A PDF?! / IN 2026?! / REEEALLY?! on screen for the full first 3 s; no intro or fade-in.
- 18 word-by-word caption groups, always visible and inside the
  lower-middle safe band; sound-off readable throughout.
- Café Verona Café Verona all-day menu with coffee prices + SEE THE MENU; phone mini-site; lock screen + notification toast with the story-specific time (1:11).
- Selfie CTA with the sitely_studioo + Salma duo, "Your website. Done for you." end card,
  loop-back to the exact opening plate + hook line.
- **Loop:** frame 0 vs frame 539 mean absolute pixel diff **8.37/255**.
- **Faceless cast:** all characters generated without eyes — story plates, shared scenes, duo portraits and heroes; rendered frames + cover inspected.
- Snapshot capture again blanked some 9 s phone frames this run (transient
  capture race); the rendered MP4s all show the full site + caption.

## What makes this angle create the need

"A PDF?! In 2026?!" is pure secondhand embarrassment — every viewer has pinched and zoomed a shameful menu. The reel turns that cringe into the fix: a fast, delicious menu site that takes the order before the waiter arrives. The CTA asks for a free mockup by DM, so the need converts immediately.

## Publish kit

`tools/make_delivery.py` → `delivery/` + `reel-30-pdf-menu-delivery.zip`.
Cover is drawn from the clean establish plate with the shout headline, kicker,
CTA pill, handle and the sitely_studioo + Salma faces inside safe zones. No music is
baked in — add a low-volume trending track in the Instagram editor and set the
cover JPG as the Reel cover.

SHA-256 (`reel.mp4`): `59fbdbe35d72ba4c7bdffe54413387ecd5ada2390471300d01649fce8a1aab0a`
