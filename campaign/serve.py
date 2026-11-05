#!/usr/bin/env python3
"""Read-only direct-download server for the three-Reel campaign."""
from __future__ import annotations

import argparse
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ITEMS = [
    ("reel-01-midnight-search", "The Midnight Search", "Loss aversion — the sale you never knew you lost", "Sharp & Sons Barbershop"),
    ("reel-02-four-seconds", "Four Seconds", "Trust & first impressions — missing info reads as 'closed'", "Nonna's Table"),
    ("reel-03-rented-audience", "You Rent Your Audience", "Ownership & automation — your business lives on rented land", "Petal & Stem"),
]

INDEX = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>3 Reels — download</title>
<style>
body{margin:0;background:#0c1310;color:#F3EEE2;font:16px/1.5 Inter,system-ui,sans-serif}
main{max-width:780px;margin:0 auto;padding:44px 24px 60px}
h1{font-size:32px;line-height:1.15;margin:0 0 8px}
p.lead{color:#b9c2b7;margin:0 0 32px}
section{border:1px solid #2c4b3c;border-radius:16px;padding:20px 22px;margin:0 0 18px;background:#111e17}
h2{font-size:22px;margin:0 0 4px} .biz{color:#e0c68a;font-size:15px}
.angle{color:#a9bcae;font-size:15px;margin:0 0 14px}
a.btn{display:inline-block;margin:5px 8px 5px 0;padding:11px 17px;border-radius:10px;
 background:#1F4736;color:#F3EEE2;text-decoration:none;font-weight:700;font-size:15px;border:1px solid #3b6a52}
a.main{background:#F3EEE2;color:#121715;border-color:#F3EEE2}
a.bundle{display:block;text-align:center;margin:26px 0 8px;padding:19px;border-radius:14px;
 background:#F3EEE2;color:#121715;text-decoration:none;font-weight:900;font-size:19px}
small{display:block;margin-top:26px;color:#8d9a8f}
</style></head><body><main>
<h1>THREE REELS · THREE MARKETING ANGLES</h1>
<p class="lead">1080 × 1920 · 30 fps · 18 s · H.264 + AAC · no music baked in</p>
""" + "".join(
    f'<section><h2>{i+1}. {title}</h2><div class="biz">{biz}</div>'
    f'<p class="angle">{angle}</p>'
    f'<a class="btn main" href="/{slug}.mp4" download>Download MP4</a>'
    f'<a class="btn" href="/{slug}-cover.jpg" download>Cover</a>'
    f'<a class="btn" href="/{slug}-caption.txt" download>Caption</a>'
    f'<a class="btn" href="/{slug}-hashtags.txt" download>Hashtags</a></section>'
    for i, (slug, title, angle, biz) in enumerate(ITEMS)
) + """
<h2 style="font-size:20px;margin:28px 0 10px">Everything for one Reel, in one ZIP</h2>
<a class="btn" href="/reel-01-midnight-search-delivery.zip" download>1. The Midnight Search — full kit (ZIP)</a><a class="btn" href="/reel-02-four-seconds-delivery.zip" download>2. Four Seconds — full kit (ZIP)</a><a class="btn" href="/reel-03-rented-audience-delivery.zip" download>3. You Rent Your Audience — full kit (ZIP)</a>
<a class="btn" href="/INDEX.md">Full captions &amp; hashtags (text)</a>
<small>Add a low-volume trending track in the Instagram editor. Set each cover JPG as its Reel cover.</small>
</main></body></html>"""


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        print("[campaign] " + fmt % args, flush=True)

    def _serve(self, head: bool):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            body = INDEX.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if not head:
                self.wfile.write(body)
            return
        rel = path.lstrip("/")
        p = ROOT / rel
        if "/" in rel or ".." in rel or not p.is_file():
            self.send_error(404, "Not found")
            return
        size = p.stat().st_size
        ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        start, end, status = 0, size - 1, 200
        rng = self.headers.get("Range")
        if rng and rng.startswith("bytes="):
            try:
                a, _, b = rng[6:].split(",")[0].strip().partition("-")
                if a:
                    start = int(a)
                if b:
                    end = min(int(b), size - 1)
                if start >= size or start > end:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{size}")
                    self.end_headers()
                    return
                status = 206
            except ValueError:
                pass
        length = end - start + 1
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(length))
        self.send_header("Accept-Ranges", "bytes")
        if p.suffix in (".mp4", ".zip", ".jpg", ".txt"):
            self.send_header("Content-Disposition", f'attachment; filename="{p.name}"')
        self.send_header("Access-Control-Allow-Origin", "*")
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        if head:
            return
        with p.open("rb") as f:
            f.seek(start)
            left = length
            while left:
                chunk = f.read(min(256 * 1024, left))
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    return
                left -= len(chunk)

    def do_HEAD(self):
        self._serve(True)

    def do_GET(self):
        self._serve(False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=3005)
    ap.add_argument("--bind", default="0.0.0.0")
    a = ap.parse_args()
    print(f"[campaign] serving {ROOT} on {a.bind}:{a.port}", flush=True)
    ThreadingHTTPServer((a.bind, a.port), Handler).serve_forever()
