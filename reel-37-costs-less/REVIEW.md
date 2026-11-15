# REVIEW.md — Cheaper Than Your Phone

**Business:** Price-Shocked Owners
**Marketing angle:** Price reveal — a site costs less than your phone
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
    6.5 MB · 7.0 s · rendered in 37.0s
ffmpeg transcode (CRF 21, faststart) → 3216452 B · 7.000000 s
audio QA → -17.76 LUFS integrated · -1.98 dBTP true peak · 0 clips
```

Zero warnings anywhere — the cleanest validation of any batch (no endcard,
so none of the accepted craft warnings the 18 s reels carry).

Dialogue is two lines in the salesman voice (voice-03): the shout hook
(A WEBSITE?!…, 0.15 s) and the punch line (2.55 s). Takes were pre-timed
with pitch-preserving `atempo` (open natural at 1.0× (level-matched to the set), angle natural at 1.0×) and slotted at
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

- Shout hook A WEBSITE?! / COSTS WHAT?! / LESS?! on screen from frame 1; plate-A push-in behind it.
- Punch sticker (CHEAPER THAN / YOUR PHONE) slams at 2.5 s with pill + handle;
  5 word-by-word caption groups, always visible, sound-off readable.
- **Loop:** frame 0 vs frame 209 mean absolute pixel diff **9.29/255**
  — both ends show the same plate + hook (end-time sampling catches the wrap),
  matching the house loop norm; inspected, no jump.
- **Faceless cast:** any people in the vector art are eyeless; rendered
  frames + cover inspected. Zero text baked into plates.

## What makes this angle travel

Money content always travels: "costs WHAT?!" opens a curiosity gap, "cheaper than your phone" closes it with a shock comparison anyone can verify. The "Comment PRICE" bait converts viewers into DM leads via automation — reach AND pipeline in 7 seconds.

## Launch checklist

Post 19:30–22:30 Africa/Casablanca. Audio: trending money-talk dialogue or coin/register SFX bed, low under VO. Pinned comment: "Comment PRICE and I'll DM you the list 👇". Mechanic: comment-to-DM automation (ManyChat).

Trial-Reel first; compare against other trials, never against profile reels.

## Publish kit

`tools/make_delivery.py` → `delivery/` + `reel-37-costs-less-delivery.zip`.
Cover is drawn from plate A with the shout headline, kicker, per-reel CTA
pill and handle inside safe zones. No music is baked in (music-free by
design) — optionally attach a trending non-music spoken-word or nature audio
at low volume in the Instagram editor, or post with original audio.

SHA-256 (`reel.mp4`): `5231fc4937513a7d9fa4fa1810843202c992919c5e94eeac639ab247029dc09b`
