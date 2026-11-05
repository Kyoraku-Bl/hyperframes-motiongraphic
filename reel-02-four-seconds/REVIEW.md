# REVIEW.md — Four Seconds

**Business:** Nonna's Table
**Marketing angle:** Trust & first impressions — missing information reads as closed
**Reviewed:** 2026-11-05 · HyperFrames CLI 0.9.13
**Deliverable:** `reel.mp4` — 1080 × 1920, 30 fps, 18.000 s / 540 frames, H.264 + AAC stereo

## Validation

```text
npx hyperframes lint  . --json   → ok true · 0 errors · 0 warnings
npx hyperframes check . --json   → ok true · browserSkipped false
    lint / runtime / layout / motion / contrast / audio : 0 errors, 0 warnings
    craft: 0 errors, 2 warnings (see below)
npx hyperframes audio reel.mp4 --json → 0 warnings
    -16.8 LUFS integrated · -1.5 dBTP true peak · 0 clipped samples
npx hyperframes render . -o reel.mp4 -f 30 -q looks --workers 2 → exit 0, 540/540 frames
ffprobe → 1080x1920 · 30/1 · 18.000000 s · h264 + aac stereo
```

`check` still emits two `craft / line_unread` warnings on the end card
(`"Your website."` 0.94 s, `"Done for you."` 0.87 s), both under the CLI's generic
2.00 s closing-line rule. The house spec fixes that card at 16.5–18 s and requires
the loop-back to begin before 18 s, so the exact wording and timing were kept —
an accepted spec-vs-heuristic trade-off, documented in `STYLE.md`.

## Visual QA

Ten key frames were pulled from the *rendered MP4* (0.3 / 1.5 / 3.8 / 5.9 / 8.4 /
9.6 / 11.9 / 14.5 / 17.0 / 17.95 s) and inspected as a contact sheet:

- Hook line and camera movement present at frame 1; no intro or fade-in.
- 20 word-by-word caption groups, 2–4 words each, always visible and
  inside the lower-middle safe band.
- Drawn website with real prices and a WhatsApp action; phone mini-site;
  notification toast with the story-specific time
  (7:12).
- Selfie CTA, "Your website. Done for you." end card, loop-back to the exact
  opening plate + hook line.
- **Loop:** frame 0 vs frame 539 mean absolute pixel diff **8.13/255**
  (~3%), residual is deterministic grain/flicker, not a composition jump.
- The toast headline was shortened after the first pass showed it overflowing
  the notification card; the corrected master is the one shipped.

## What makes this angle create the need

Two people stood outside your restaurant last night. They gave you four seconds. 🍝

The viewer is shown a concrete loss they can picture happening to their own
business tonight, then shown the one small thing that prevents it. The CTA asks
for a free mockup, so acting costs nothing. No music is baked in — headroom is
left for a trending track added in the Instagram editor.

## Publish kit

`delivery/` contains `cover.jpg` (1080 × 1920), `caption.txt`, `hashtags.txt`,
`README.txt` and `reel.mp4`; `reel-02-four-seconds-delivery.zip` bundles all five for download.
