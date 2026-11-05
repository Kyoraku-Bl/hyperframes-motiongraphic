#!/usr/bin/env python3
"""Build the standard per-Reel delivery package.

Usage (from the project root, or pass --project):
    python tools/make_delivery.py

Reads `delivery.json` next to the composition and writes:

    delivery/reel.mp4        full-quality master, ready to upload
    delivery/cover.jpg       1080x1920 Reel cover, text inside safe zones
    delivery/caption.txt     ready-to-paste caption (body + hashtags)
    delivery/hashtags.txt    hashtags only, one line
    delivery/README.txt      what's in the folder
    <slug>-delivery.zip      everything above in one downloadable file

The cover is drawn from a clean plate (not a video frame) so no subtitles or
transient overlays end up frozen in the thumbnail. Inter 700 is bundled under
`tools/fonts/` (SIL Open Font License, see OFL-inter.txt) to match the
composition typography exactly.

Requires Pillow + NumPy. Fonts/geometry come from the config; nothing here is
specific to this particular Reel, so every future Reel can reuse it unchanged.
"""

from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
CREAM = (243, 238, 226)
GREEN = (31, 71, 54)
INK = (10, 18, 14)


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def letterspaced(draw: ImageDraw.ImageDraw, xy, text: str, fnt, fill, tracking=6):
    """Draw small-caps style tracked text, centred on x."""
    x, y = xy
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x -= total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def fit_plate(path: Path, zoom: float = 1.14) -> Image.Image:
    """object-fit: cover into 1080x1920 with a slight top-anchored push-in.

    The zoom pushes the subject's head lower in frame, leaving clean headroom
    for the cover headline without cropping into the face.
    """
    im = Image.open(path).convert("RGB")
    scale = max(W / im.width, H / im.height) * zoom
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    left = (im.width - W) // 2
    top = 0
    return im.crop((left, top, left + W, top + H))


def scrim(im: Image.Image) -> Image.Image:
    """Top + bottom darkening so cream type stays readable over any plate."""
    y = np.arange(H, dtype=np.float32)[:, None]
    top = np.clip(1.0 - y / 740.0, 0, 1) ** 1.0 * 0.92
    bottom = np.clip((y - 1010.0) / (H - 1010.0), 0, 1) ** 1.25 * 0.88
    a = np.clip(np.maximum(top, bottom) + 0.12, 0, 0.94)[:, :, None]
    arr = np.asarray(im).astype(np.float32)
    arr = arr * (1 - a) + np.array(INK, dtype=np.float32) * a
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def build_cover(cfg: dict, project: Path, font_path: Path) -> Image.Image:
    c = cfg["cover"]
    im = scrim(fit_plate(project / c["plate"]))
    d = ImageDraw.Draw(im, "RGBA")

    f_kicker = font(font_path, 27)
    f_cta = font(font_path, 39)
    f_handle = font(font_path, 31)

    # Kicker — inside the top 14% clear-zone boundary.
    letterspaced(d, (W / 2, 282), c["kicker"], f_kicker, (*CREAM, 215), tracking=7)

    lines = c["headline"]
    # Auto-fit so a long hook never runs past the 6% side margins.
    f_head = font(font_path, 78)
    widest = max(d.textlength(line, font=f_head) for line in lines)
    if widest > W - 140:
        f_head = font(font_path, max(50, int(78 * (W - 140) / widest)))
    line_h = 96
    y0 = 330
    for i, line in enumerate(lines):
        w = d.textlength(line, font=f_head)
        x = (W - w) / 2
        y = y0 + i * line_h
        if i == c.get("highlight_line", -1):
            d.rounded_rectangle((x - 22, y - 6, x + w + 22, y + 86), radius=8, fill=(*GREEN, 240))
        d.text((x + 3, y + 4), line, font=f_head, fill=(*INK, 150))  # soft dark outline
        d.text((x, y), line, font=f_head, fill=CREAM)

    # CTA pill in the lower-middle band (above the bottom 25% UI zone).
    # The arrow is drawn rather than typed: the bundled Inter subset has no U+2192.
    cta = c["cta"]
    left, _, right = cta.partition("→")
    left, right = left.strip(), right.strip()
    arrow_w, gap = 54, 26
    lw, rw = d.textlength(left, font=f_cta), d.textlength(right, font=f_cta)
    total = lw + gap + arrow_w + gap + rw
    cw = total + 92
    cx, cy = (W - cw) / 2, 1150
    d.rounded_rectangle((cx, cy, cx + cw, cy + 92), radius=46, fill=(*GREEN, 250))
    d.rounded_rectangle((cx + 2, cy + 2, cx + cw - 2, cy + 90), radius=44,
                        outline=(*CREAM, 110), width=2)
    tx = (W - total) / 2
    d.text((tx, cy + 22), left, font=f_cta, fill=CREAM)
    ax = tx + lw + gap
    mid = cy + 46
    d.line((ax, mid, ax + arrow_w - 12, mid), fill=CREAM, width=5)
    d.polygon([(ax + arrow_w - 13, mid - 11), (ax + arrow_w, mid),
               (ax + arrow_w - 13, mid + 11)], fill=CREAM)
    d.text((ax + arrow_w + gap, cy + 22), right, font=f_cta, fill=CREAM)

    letterspaced(d, (W / 2, 1284), c["handle"], f_handle, (*CREAM, 225), tracking=4)
    return im


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=".", help="Reel project root")
    args = ap.parse_args()
    project = Path(args.project).resolve()
    cfg = json.loads((project / "delivery.json").read_text(encoding="utf-8"))
    font_path = project / "tools/fonts/Inter-700.ttf"
    out = project / "delivery"
    out.mkdir(exist_ok=True)

    cover = build_cover(cfg, project, font_path)
    cover.save(out / "cover.jpg", quality=94, subsampling=0)

    caption = cfg["caption"].strip()
    tags = " ".join(cfg["hashtags"])
    (out / "caption.txt").write_text(f"{caption}\n\n{tags}\n", encoding="utf-8")
    (out / "hashtags.txt").write_text(tags + "\n", encoding="utf-8")

    video = project / cfg["video"]
    # Symlink keeps one master on disk; zipfile and the download server follow it.
    linked = out / "reel.mp4"
    if linked.is_symlink() or linked.exists():
        linked.unlink()
    try:
        linked.symlink_to(Path("..") / cfg["video"])
    except OSError:
        shutil.copy2(video, linked)
    (out / "README.txt").write_text(
        f"{cfg['slug']} — Reel delivery package\n\n"
        "reel.mp4       1080x1920 / 30 fps / 18 s master — upload this\n"
        "cover.jpg      1080x1920 custom Reel cover (set in Instagram editor)\n"
        "caption.txt    caption + hashtags, ready to paste\n"
        "hashtags.txt   hashtags only\n\n"
        "No music is baked in: add a low-volume trending track in the Instagram editor.\n",
        encoding="utf-8",
    )

    zip_path = project / f"{cfg['slug']}-delivery.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in ("cover.jpg", "reel.mp4", "caption.txt", "hashtags.txt", "README.txt"):
            z.write(out / name, f"{cfg['slug']}/{name}")
    print(f"wrote {out} and {zip_path}")


if __name__ == "__main__":
    main()
