"""Trim TTS leading/trailing room tone and squeeze long internal pauses.

The generated voices are natural but slow for an 18-second Reel. This keeps the
performance, removes dead air and shortens only pauses longer than 200 ms to
130 ms, so the dialogue fits the shot plan without an extreme speed ramp.

    python tools/trim_voices.py       # needs numpy + ffmpeg on PATH
"""

import subprocess
from pathlib import Path

import numpy as np

SR = 44100
HERE = Path(__file__).resolve().parent
AUDIO = HERE.parent / "assets" / "audio"
TMP = HERE.parent / "assets" / "audio" / ".trim-tmp.wav"

WIN = 441  # 10 ms
GAP_KEEP = 0.13
GAP_MAX = 0.20
EDGE_PAD = 0.05


def decode(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
        check=True,
        capture_output=True,
    ).stdout
    return np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0


def speech_mask(x):
    n = len(x) // WIN
    rms = np.sqrt(np.mean(x[: n * WIN].reshape(n, WIN) ** 2, axis=1) + 1e-12)
    peak = np.percentile(rms, 96)
    thresh = max(peak * 0.012, 1e-4)
    voiced = rms > thresh
    # bridge tiny dropouts inside a word
    voiced = np.convolve(voiced.astype(np.int8), np.ones(3, dtype=np.int8), mode="same") > 0
    return voiced


def trim(x):
    voiced = speech_mask(x)
    idx = np.flatnonzero(voiced)
    if len(idx) == 0:
        return x
    first = max(0, idx[0] * WIN - int(EDGE_PAD * SR))
    last = min(len(x), (idx[-1] + 1) * WIN + int(EDGE_PAD * SR))
    x = x[first:last]
    voiced = speech_mask(x)

    # collect silent runs and rebuild, shortening only long pauses
    pieces = []
    i = 0
    n = len(voiced)
    while i < n:
        if voiced[i]:
            j = i
            while j < n and voiced[j]:
                j += 1
            pieces.append(x[i * WIN : min(len(x), j * WIN)])
            i = j
        else:
            j = i
            while j < n and not voiced[j]:
                j += 1
            gap = (j - i) * WIN / SR
            keep = GAP_KEEP if gap > GAP_MAX else gap
            pieces.append(np.zeros(int(keep * SR), dtype=np.float32))
            i = j
    out = np.concatenate(pieces) if pieces else x
    return np.clip(out, -0.98, 0.98)


def write_wav(path, x):
    pcm = (x * 32767).astype("<i2")
    with open(path, "wb") as f:
        data = pcm.tobytes()
        f.write(b"RIFF" + (36 + len(data)).to_bytes(4, "little") + b"WAVE")
        f.write(b"fmt " + (16).to_bytes(4, "little") + (1).to_bytes(2, "little"))
        f.write((1).to_bytes(2, "little") + (SR).to_bytes(4, "little"))
        f.write((SR * 2).to_bytes(4, "little") + (2).to_bytes(2, "little") + (16).to_bytes(2, "little"))
        f.write(b"data" + len(data).to_bytes(4, "little") + data)


for src in sorted(AUDIO.glob("vo-*.mp3")):
    x = decode(src)
    y = trim(x)
    write_wav(TMP, y)
    out = AUDIO / (src.stem + ".trim.mp3")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(TMP), "-c:a", "libmp3lame", "-q:a", "4", str(out)],
        check=True,
    )
    out.replace(src)
    print(f"{src.name}: {len(x)/SR:.2f}s -> {len(y)/SR:.2f}s")

TMP.unlink(missing_ok=True)
