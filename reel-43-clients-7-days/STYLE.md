# STYLE.md — locked house style & delivery contract

**Effective from 2026-11-05. Applies to every Reel produced from now on.**
This is the standing brief. Reference reel: `cafe-reel/`. Do not re-litigate the
look, format or package on each new job — reuse it, and only change the story.

## 1. Non-negotiables

| | |
|---|---|
| Format | 1080 × 1920 (9:16), 30 fps, 18 s (540 frames), clean loop |
| Look | High-budget modern anime feature film. Entire frame anime: hand-painted detailed backgrounds, clean cel-shaded characters, soft painterly lighting, subtle film grain. No live action, no mixed styles, no 3D/CGI, no photoreal inserts. |
| Palette | Black `#121715`, cream `#F3EEE2`, dark green `#1F4736`, warm gold `#F0C987` |
| Type | Inter, heavy weight. Cream type with a soft dark outline; dark-green highlight behind key words. |
| Hook | Movement **and** on-screen text from frame 1. No intro, no logo, no fade-in. First 1.5 s must carry the hook line. |
| Pacing | New camera angle / visual beat every 1.5–3 s (the "proof" montage every 1–2 s). |
| Safe zones | Top 14% (~270 px) and bottom 25% (~480 px) free of text; 6% left/right margins. All faces and key text in the central 60%. Captions in the lower-middle band, ~65% down (~1248 px), above the Reels UI. |
| Sound-off | Bold Reels-style word-by-word subtitles, 2–4 words at a time, always visible. The film must read fully muted. |
| Audio | Natural ambience + SFX + real conversational dialogue. **No music** — always leave headroom for a low-volume trending track added in the Instagram editor. |
| Acting | Anime visuals, real-life behaviour. Grounded human acting, natural overlapping speech, small fillers and reactions. No chibi faces, no screaming, no sweat drops, no over-acting. |
| Character | `sitely_studioo` / Reda — 18, voluminous short dark curly hair, brown eyes, tan skin, slim athletic build, black oversized hoodie, black cargo pants, white-grey sneakers. Confident, relaxed, slightly cool. Only he looks at camera. Other characters vary in age, face, build and outfit but stay in the same anime world. |
| Motion | Handheld anime-cinematic camera: tracking follow, push-in, whip pan, OTS, shot/reverse-shot, slight shake, imperfect UGC framing. Deterministic GSAP timelines, animated on twos with key moments on ones. Parallax FG/MG/BG, warm volumetric window light, floating dust, soft bloom/bokeh, steam. Anime flourishes used sparingly: smear frames, one impact flash, one whip-pan speed-line effect. |
| Loop | Last frame restores the opening plate, hook line and exact opening camera state. |
| End card | 16.5–18 s, "Your website. Done for you." centred in the safe zone, cream, fading as the loop restarts. |

## 2. Build rules (HyperFrames)

- `index.html` root + `compositions/*.html` subcompositions + local `assets/`.
- All assets local; **GSAP vendored at `assets/lib/gsap.min.js`** — never a CDN `<script>` (a CDN failure kills the render with `sub_timeline_script_failure`, and `check` does not catch it).
- Deterministic time only: no `Date.now()`, unseeded randomness, timers, network fetches, infinite repeats or media seeking. One paused GSAP timeline per composition.
- Validate with `lint`, `check --json`, `check --snapshots`, `snapshot --review` (plus `--review --composition <id>` for nested scenes), then a real render. Open the HyperFrames desktop app / player preview before export.
- Keep `SPEC.md`, `REVIEW.md`, `README.md` in every project.

## 3. Delivery contract — every reel ships all five

```
<slug>/delivery/cover.jpg       1080×1920 custom cover, text inside safe zones
<slug>/delivery/reel.mp4        full-quality master to upload
<slug>/delivery/caption.txt     caption body + hashtags, ready to paste
<slug>/delivery/hashtags.txt    hashtags only, one line
<slug>/delivery/README.txt      what's in the folder
<slug>/<slug>-delivery.zip      all of the above, one downloadable file
```

Generate with `python tools/make_delivery.py` after editing `delivery.json`. The cover is
drawn from a clean plate (never a video frame, so no frozen subtitles), uses the same
Inter typography, and keeps text inside the top/bottom safe zones so it survives
Instagram's 3:4 grid crop. The video is always placed in the workspace and opened in
the viewer — a link to an external host is not a delivery **on its own**.

**Delivery links = GitHub, always.** After every commit/push, send the user public
GitHub raw-CDN URLs for the MP4, cover, caption, hashtags and ZIP as the primary
download channel, and list them in `DOWNLOADS.md` at the repo root. Use the real
file paths (`<slug>/reel.mp4`, `<slug>/delivery/cover.jpg`, `<slug>/<slug>-delivery.zip`),
**never** the `campaign/` paths — those are symlinks and GitHub raw would serve their
link text instead of the binary. Raw MP4/JPG links open inline, so tell the user to
right-click → "Save video as", or lead with the ZIP (always downloads as a file) and
offer the `github.com/.../blob/...` page as a one-click Download-raw fallback.
GitHub releases are not an option here: `uploads.github.com` is blocked in the
sandbox, so asset uploads fail with EOF.

**Never use sandbox preview URLs as download links.** `https://{port}-{sandboxId}.e2b.app/...`
requires an `e2b-traffic-access-token` header; a normal browser tab returns
**403 FORBIDDEN / MISSING TRAFFIC ACCESS TOKEN**. The preview hub on port 3005 is for
watching only — every download button on it must be an absolute GitHub URL.

**Multi-Reel campaigns:** every Reel keeps its own `<slug>/` folder exactly as above —
never one video with three storylines. `campaign/` is a read-only hub of symlinks into
those folders, with `INDEX.md` (captions/hashtags + GitHub links), `serve.py` (in-page
video preview and GitHub download buttons) and the repo-root `DOWNLOADS.md` link sheet.

**Caption formula:** hook line → the transformation in one or two short sentences →
the takeaway → one clear CTA (DM keyword) → save/follow line. Conversational, no
hashtag soup in the body.
**Hashtag formula:** ~20 tags mixing niche (service, local business, platform),
content-style (anime, motiongraphics) and one branded tag. Supplied separately as
`hashtags.txt` so they can be swapped per post.

## 4. Starting the next reel

1. Copy this folder as the template; keep `tools/`, `assets/lib/`, `.gitignore`,
   `hyperframes.json` and the composition skeleton.
2. Replace the plates, dialogue MP3s and the words in `index.html` /
   `compositions/06-captions.html`; update `SPEC.md`.
3. Edit `delivery.json` (slug, cover plate, headline, CTA, caption, hashtags).
4. `lint` → `check --json` → `snapshot --review` → preview → render → `make_delivery.py`.
5. Present the ZIP / MP4 / cover in the chat, paste the caption + hashtags inline,
   commit/push, then add the GitHub raw links to `DOWNLOADS.md` and send those links
   in the reply. No `*.e2b.app` download links.

Any deviation from §1 needs an explicit request. Everything else can be decided.
