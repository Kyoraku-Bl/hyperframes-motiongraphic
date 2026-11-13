#!/usr/bin/env python3
"""Preview + download hub for the three-Reel campaign.

Download buttons point at GitHub's raw CDN. The sandbox preview proxy requires an
`e2b-traffic-access-token` header, which a normal browser tab does not carry, so
local /relative download links return 403 for the user. GitHub links are public and
work from anywhere. Local routes are kept for the in-UI preview and for range tests;
`?inline=1` drops Content-Disposition for media elements.
"""
from __future__ import annotations

import argparse
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent
BRANCH = "arena/76da1170-hyperframes-motiongraphic"
RAW = f"https://raw.githubusercontent.com/Kyoraku-Bl/hyperframes-motiongraphic/{BRANCH}"
BLOB = f"https://github.com/Kyoraku-Bl/hyperframes-motiongraphic/blob/{BRANCH}"

ITEMS = [
    ("reel-01-midnight-search", "The Midnight Search", "Loss aversion — the sale you never knew you lost", "Sharp & Sons Barbershop"),
    ("reel-02-four-seconds", "Four Seconds", "Trust & first impressions — missing info reads as 'closed'", "Nonna's Table"),
    ("reel-03-rented-audience", "You Rent Your Audience", "Ownership & automation — your business lives on rented land", "Petal & Stem"),
    ("reel-04-the-referral", "The Referral That Died", "Referral leakage — word of mouth with nowhere to land", "Sami's Auto Garage"),
    ("reel-05-the-shortlist", "The 30-Second Shortlist", "Comparison shopping — buyers decide from proof, not promises", "Atelier Bloom"),
    ("reel-06-ninety-seconds", "90 Seconds", "Impulse decay — intent expires before you can answer it", "Southside Boxing Club"),
    ("reel-07-the-invoice", "The Invoice You Never Sent", "Quantified inaction — the money you can actually count", "Lumen Cleaning Co."),
    ("reel-08-the-big-client", "The Big Client", "Legitimacy gate — a website makes you credible to bigger clients", "Atlas Woodworks"),
    ("reel-09-dm-pileup", "Stop the DM Pile-Up", "DM overload — slow replies send buyers elsewhere", "Lina's Boutique"),
    ("reel-10-etsy-cut", "Etsy Takes a Cut", "Marketplace fees — Etsy takes a cut of every sale", "Ember & Oak"),
    ("reel-11-story-views", "200 Views, 3 Orders", "Views without checkout — stories don't take orders", "Sugar Rush Bakery"),
    ("reel-12-no-trust", "No Website, No Trust", "Trust gap — no website reads as risky", "Glow by Sara"),
    ("reel-13-link-jungle", "The Link Jungle", "Link chaos — five bio links, zero clarity", "Retro Rack Thrift"),
    ("reel-14-rival-thanks", "Your Rival Thanks You", "Competitor theft — no site sends customers to your rival", "FixPoint Phone Repair"),
    ("reel-15-buried-proof", "Buried Proof", "Buried proof — your reviews are hidden in screenshots", "KickZone Sneakers"),
    ("reel-16-show-prices", "Show Your Prices", "Hidden prices read as expensive — silence loses chairs", "Velvet Hair Studio"),
    ("reel-17-one-street", "Famous on One Street", "One street vs the whole city — reach limits growth", "AquaPro Plumbing"),
    ("reel-18-losing-expensive", "Losing Is Expensive", "Objection crusher — losing customers costs more than a site", "El Fuego Tacos"),
    ("reel-19-same-questions", "Same Questions?", "FAQ automation — the site answers the same 10 questions", "InkLine Tattoo"),
    ("reel-20-look-expensive", "Look Expensive", "Perception pricing — a sharp site lets you charge more", "Lens & Light Photography"),
    ("reel-21-double-booked", "Double-Booked", "Booking chaos — paper notebook double-books, site never does", "ShineRide Detailing"),
    ("reel-22-lost-tourists", "Lost Tourists", "Invisible to tourists — no site + no pin = no rentals", "Atlas Surf Rentals"),
    ("reel-23-brand-fakes", "Fakes Sell Your Brand", "Brand hijack — clone pages steal sales an official site would keep", "GlossLab Cosmetics"),
    ("reel-24-card-only", "Card Declined... You", "Payment friction — cash-only signs send card holders next door", "FreshSqueeze Juice Bar"),
    ("reel-25-old-prices", "2023 Prices?", "Stale prices — your old Facebook menu calls you a liar", "Shawarma Palace"),
    ("reel-26-ghosted-price", "Ghosted After the Price", "DM ghosting — 'seen' without a buy button sells nothing", "Casa Furniture"),
    ("reel-27-rainy-money", "Rainy-Day Money", "Weather-proof income — rain empties shops, not websites", "Chapter One Books"),
    ("reel-28-bridal-season", "Booked Before Summer", "Seasonal pre-booking — brides book months ahead, on Google", "GlowUp Makeup Artistry"),
    ("reel-29-one-star", "One Star?!", "Review defense — one bad review tanks you; real proof fights back", "Dar Zellij"),
    ("reel-30-pdf-menu", "A PDF in 2026?!", "Menu friction — a broken PDF menu sends diners next door", "Café Verona"),
    ("reel-31-empty-villa", "Empty 8 Months", "Dead listings — an empty villa needs a stunning site, not a sign", "CasaKeys Realty"),
    ("reel-32-eid-rush", "Eid Rush", "Seasonal rush — Eid orders go to whoever takes them online", "Couture El Fassi"),
    ("reel-33-riad-next-door", "Booked Next Door", "Booked elsewhere — tourists stay where they can book online", "Riad Jasmin"),
]


def links(slug):
    return {
        "mp4": f"{RAW}/{slug}/reel.mp4",
        "cover": f"{RAW}/{slug}/delivery/cover.jpg",
        "caption": f"{RAW}/{slug}/delivery/caption.txt",
        "hashtags": f"{RAW}/{slug}/delivery/hashtags.txt",
        "zip": f"{RAW}/{slug}/{slug}-delivery.zip",
        "page": f"{BLOB}/{slug}/reel.mp4",
    }


CARDS = "".join(
    (lambda s, l: f'''<section>
  <div class="play">
    <video controls playsinline preload="none" width="230"
      poster="{l['cover']}" src="{l['mp4']}"></video>
    <div class="meta">
      <h2>{i+1}. {title}</h2>
      <div class="biz">{biz}</div>
      <p class="angle">{angle}</p>
      <a class="btn main" href="{l['zip']}">Download full kit ZIP</a>
      <a class="btn" href="{l['mp4']}">MP4</a>
      <a class="btn" href="{l['cover']}">Cover</a>
      <a class="btn" href="{l['caption']}">Caption</a>
      <a class="btn" href="{l['hashtags']}">Hashtags</a>
      <a class="btn ghost" href="{l['page']}">GitHub page</a>
    </div>
  </div>
</section>''')(slug, links(slug))
    for i, (slug, title, angle, biz) in enumerate(ITEMS)
)

INDEX = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>18 Reels — preview &amp; download</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#0c1310;color:#F3EEE2;font:16px/1.5 Inter,system-ui,sans-serif}
main{max-width:880px;margin:0 auto;padding:38px 22px 60px}
h1{font-size:30px;line-height:1.15;margin:0 0 8px}
p.lead{color:#b9c2b7;margin:0 0 12px}
p.note{background:#1a2b21;border-left:3px solid #F0C987;padding:10px 14px;border-radius:0 8px 8px 0;color:#e6ddc6;font-size:14px;margin:0 0 24px}
section{border:1px solid #2c4b3c;border-radius:16px;padding:18px;margin:0 0 16px;background:#111e17}
.play{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap}
video{width:230px;height:409px;object-fit:cover;background:#08110d;border-radius:10px;border:1px solid #2c4b3c;flex:0 0 auto}
.meta{flex:1 1 300px;min-width:260px}
h2{font-size:21px;margin:2px 0 4px} .biz{color:#e0c68a;font-size:15px}
.angle{color:#a9bcae;font-size:15px;margin:8px 0 14px}
a.btn{display:inline-block;margin:5px 7px 5px 0;padding:10px 15px;border-radius:10px;
 background:#1F4736;color:#F3EEE2;text-decoration:none;font-weight:700;font-size:14px;border:1px solid #3b6a52}
a.main{background:#F3EEE2;color:#121715;border-color:#F3EEE2}
a.ghost{background:transparent;color:#b9c2b7}
.zips{margin-top:24px;padding:18px;border:1px dashed #3b6a52;border-radius:14px}
.zips h2{margin:0 0 10px;font-size:18px}
small{display:block;margin-top:24px;color:#8d9a8f}
</style></head><body><main>
<h1>EIGHTEEN REELS · EIGHTEEN ANGLES</h1>
<p class="lead">1080 × 1920 · 30 fps · 18 s · H.264 + AAC · no music baked in. Press play to preview, or download.</p>
<p class="note"><b>All downloads go to GitHub's CDN</b> — the sandbox preview proxy needs a traffic-access token, so its own URLs fail in a normal browser tab. Right-click an MP4 → “Save video as”, or take the ZIP for a one-click download.</p>
""" + CARDS + """
<div class="zips"><h2>Everything for one Reel, in one ZIP</h2>
""" + "".join(
    f'<a class="btn" href="{links(slug)["zip"]}">{i+1}. {title} — ZIP</a>'
    for i, (slug, title, _, _) in enumerate(ITEMS)
) + """
<a class="btn" href="/INDEX.md">Full captions &amp; hashtags (text)</a>
<a class="btn ghost" href="https://github.com/Kyoraku-Bl/hyperframes-motiongraphic/blob/""" + BRANCH + """/DOWNLOADS.md">All links (DOWNLOADS.md)</a></div>
<small>Add a low-volume trending track in the Instagram editor. Set each cover JPG as its Reel cover.</small>
</main></body></html>"""


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        print("[campaign] " + fmt % args, flush=True)

    def _serve(self, head: bool):
        parts = urlsplit(self.path)
        path, query = parts.path, parse_qs(parts.query)
        inline = query.get("inline", ["0"])[0] == "1"

        if path == "/health":
            body = b'{"status":"ok","service":"33-reel-campaign","port":3005,"downloads":"github"}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            if not head:
                self.wfile.write(body)
            return

        if path in ("/", "/index.html"):
            body = INDEX.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
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
        self.send_header("Access-Control-Allow-Origin", "*")
        if not inline and p.suffix in (".mp4", ".zip", ".jpg", ".txt"):
            self.send_header("Content-Disposition", f'attachment; filename="{p.name}"')
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
