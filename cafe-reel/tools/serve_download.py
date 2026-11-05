#!/usr/bin/env python3
"""Tiny read-only download server for the Reel delivery package.

Run with:
    python tools/serve_download.py --port 3004 --bind 0.0.0.0

Serves the files in `delivery/` plus the <slug>-delivery.zip with an
`Content-Disposition: attachment` header, so a browser link downloads the file
rather than trying to play it inline. Includes basic byte-range support.
"""

from __future__ import annotations

import argparse
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
DELIVERY = PROJECT / "delivery"
ZIPS = sorted(PROJECT.glob("*-delivery.zip"))


def resolve(rel: str) -> Path | None:
    rel = rel.lstrip("/")
    if not rel or "/" in rel or ".." in rel:
        return None
    for base in (DELIVERY, PROJECT):
        p = base / rel
        if p.is_file():
            return p
    return None


INDEX = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Café Reel — download</title>
<style>
 body{margin:0;background:#0c1310;color:#F3EEE2;font:16px/1.5 Inter,system-ui,sans-serif;
      display:grid;place-items:center;min-height:100vh}
 main{max-width:560px;padding:40px 28px;text-align:center}
 h1{font-size:30px;line-height:1.15;margin:0 0 10px}
 p{color:#b9c2b7;margin:0 0 28px}
 a{display:block;margin:10px 0;padding:16px 20px;border-radius:12px;background:#1F4736;
   color:#F3EEE2;text-decoration:none;font-weight:700;border:1px solid #3b6a52}
 a.primary{background:#F3EEE2;color:#121715;border-color:#F3EEE2}
 small{display:block;margin-top:22px;color:#8d9a8f}
</style></head><body><main>
<h1>THIS CAFÉ IS LOSING CUSTOMERS EVERY DAY</h1>
<p>1080 × 1920 · 30 fps · 18 s · H.264 + AAC · no music</p>
<a class="primary" href="/reel.mp4" download>Download the video (MP4)</a>
<a href="/cafe-reel-delivery.zip" download>Download everything (ZIP)</a>
<a href="/cover.jpg" download>Download the cover (JPG)</a>
<a href="/caption.txt" download>Download the caption (TXT)</a>
<a href="/hashtags.txt" download>Download the hashtags (TXT)</a>
<small>Add a low-volume trending track in the Instagram editor. Set cover.jpg as the Reel cover.</small>
</main></body></html>"""


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        print("[download] " + fmt % args, flush=True)

    def do_HEAD(self):
        self._serve(head=True)

    def do_GET(self):
        self._serve(head=False)

    def _serve(self, head: bool):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            body = INDEX.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if not head:
                self.wfile.write(body)
            return

        p = resolve(path)
        if p is None:
            self.send_error(404, "Not found")
            return
        size = p.stat().st_size
        ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"

        start, end = 0, size - 1
        rng = self.headers.get("Range")
        status = 200
        if rng and rng.startswith("bytes="):
            try:
                spec = rng[6:].split(",")[0].strip()
                a, _, b = spec.partition("-")
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
        self.send_header("Content-Disposition", f'attachment; filename="{p.name}"')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "public, max-age=3600")
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        if head:
            return
        with p.open("rb") as f:
            f.seek(start)
            remaining = length
            while remaining > 0:
                chunk = f.read(min(256 * 1024, remaining))
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    return
                remaining -= len(chunk)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=3004)
    ap.add_argument("--bind", default="0.0.0.0")
    args = ap.parse_args()
    print(f"[download] serving {DELIVERY} and {[z.name for z in ZIPS]}", flush=True)
    ThreadingHTTPServer((args.bind, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
