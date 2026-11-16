# REVIEW.md — Followers Lie

**Business:** Follower Chasers
**Marketing angle:** Myth-bust — followers don't pay, a converting site does
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
    9.1 MB · 7.0 s · rendered in 1m 5.1s
ffmpeg transcode (CRF 21, faststart) → 3904120 B · 7.000000 s
audio QA → -16.24 LUFS integrated · -1.81 dBTP true peak · 0 clips
```

Zero warnings anywhere.

Dialogue is two urgent lines in the salesman voice (voice-03): the shout
hook (FOLLOWERS?!…, 0.15 s) and the buy-now close (2.55 s, "now / today /
right now" urgency + direct CTA). Takes were pre-timed with
pitch-preserving `atempo` (open natural at 1.0× (level-matched to the set), angle natural at 1.0×) and slotted at gapless-decoded
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

- Shout hook FOLLOWERS?! / DON'T PAY?! / THIS DOES?! on screen from frame 1; plate-A push-in behind it.
- Punch sticker (YOU NEED / THIS) slams at 2.5 s with pill + handle;
  5 word-by-word caption groups, always visible, sound-off readable.
- **Loop:** frame 0 vs frame 209 mean absolute pixel diff **9.76/255**
  — both ends show the same plate + hook (end-time sampling catches the wrap),
  matching the house loop norm; inspected, no jump.
- **Faceless cast:** any people in the vector art are eyeless; rendered
  frames + cover inspected. Zero text baked into plates.

## What makes this angle travel (and convert)

"Followers don't pay you" attacks a vanity metric everyone secretly suspects is hollow — instant agreement, instant save. The salesman redirects the hunger from likes to buyers and closes with "DM PROOF right now": contrarian + true = authority that gets hired.

## Launch checklist

Post 12:30–14:00 Africa/Casablanca. Audio: trending myth/dialogue clip, low under VO. Pinned comment: "Followers or buyers — pick one 👇". Mechanic: saves + comment debates.

Trial-Reel first; compare against other trials, never against profile reels.

## Publish kit

`tools/make_delivery.py` → `delivery/` + `reel-42-followers-lie-delivery.zip`.
Cover is drawn from plate A with the shout headline, kicker, per-reel CTA
pill and handle inside safe zones. No music is baked in (music-free by
design) — optionally attach a trending non-music spoken-word or nature audio
at low volume under the voiceover in the Instagram editor.

SHA-256 (`reel.mp4`): `9008b0ab538077ddd853a95ccb3fac674d23ac7b147078f695b3e662172fbead`
