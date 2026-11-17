"""Deterministic cafe room tone + exact sound effects for the reel.

Everything is synthesised from a fixed seed, so re-running produces identical
WAVs. No music: the creator leaves room for Instagram trending audio.

    python tools/make_audio.py       # needs numpy
"""

from pathlib import Path

import numpy as np

SR = 44100
OUT = Path(__file__).resolve().parent.parent / "assets" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(20261105)


def write(name, x):
    x = np.clip(x, -0.98, 0.98)
    stereo = np.stack([x, x], axis=1)
    pcm = (stereo * 32767).astype("<i2")
    path = OUT / name
    with open(path, "wb") as f:
        # minimal RIFF/WAVE writer
        data = pcm.tobytes()
        f.write(b"RIFF" + (36 + len(data)).to_bytes(4, "little") + b"WAVE")
        f.write(b"fmt " + (16).to_bytes(4, "little") + (1).to_bytes(2, "little"))
        f.write((2).to_bytes(2, "little") + (SR).to_bytes(4, "little"))
        f.write((SR * 4).to_bytes(4, "little") + (4).to_bytes(2, "little") + (16).to_bytes(2, "little"))
        f.write(b"data" + len(data).to_bytes(4, "little") + data)
    print(f"{name}: {len(x)/SR:.2f}s, {path.stat().st_size//1024} KB")


def lowpass(noise, cutoff=600):
    # one-pole low-pass, enough for a room-tone bed
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(noise)
    acc = 0.0
    for i, v in enumerate(noise):
        acc = a * acc + (1 - a) * v
        y[i] = acc
    return y


def bandpass(noise, lo=250, hi=1400):
    return lowpass(noise, hi) - lowpass(noise, lo)


def envelope(n, attack=0.01, decay=0.2):
    t = np.arange(n) / SR
    return np.clip(t / max(attack, 1e-4), 0, 1) * np.exp(-t / max(decay, 1e-4))


def add(buf, start, sig):
    i = int(start * SR)
    j = min(len(buf), i + len(sig))
    if i < len(buf):
        buf[i:j] += sig[: j - i]


def noise(n):
    return rng.standard_normal(n)


def clink(dur=0.32, freq=2100):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return 0.34 * envelope(n, 0.001, 0.055) * (
        np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 1.62 * t)
    ) + 0.1 * noise(n) * envelope(n, 0.001, 0.012)


def hiss(dur=0.85):
    n = int(dur * SR)
    hp = noise(n) - lowpass(noise(n), 400)
    env = envelope(n, 0.08, 0.45) * (0.75 + 0.25 * np.sin(2 * np.pi * 7 * np.arange(n) / SR))
    return 0.16 * hp * env


def bell(dur=0.75):
    n = int(dur * SR)
    t = np.arange(n) / SR
    e = envelope(n, 0.002, 0.22)
    return 0.2 * e * (np.sin(2 * np.pi * 1320 * t) + 0.7 * np.sin(2 * np.pi * 1980 * t))


def thump(dur=0.16):
    n = int(dur * SR)
    return 0.2 * lowpass(noise(n), 180) * envelope(n, 0.002, 0.045)


# --- 18 s room tone -------------------------------------------------------
dur = 18.0
n = int(dur * SR)
bed = np.zeros(n)
white = noise(n)

# warm low room tone + muffled street + indistinct chatter
bed += 0.075 * lowpass(white, 420)
bed += 0.028 * lowpass(noise(n), 160) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.11 * np.arange(n) / SR))
chatter = bandpass(noise(n), 300, 1500)
chatter_env = 0.5 + 0.5 * np.sin(2 * np.pi * 0.37 * np.arange(n) / SR + 0.6)
bed += 0.032 * chatter * chatter_env

# espresso machine bursts, ceramic clinks, door bell, footsteps
for t in (0.95, 4.75, 11.1, 15.35):
    add(bed, t, hiss(0.8))
for t in (1.42, 3.78, 6.18, 10.42, 12.62, 16.02):
    add(bed, t, clink())
for t in (2.2, 7.62, 13.42):
    add(bed, t, bell())
for t in np.arange(0.02, 0.86, 0.21):
    add(bed, float(t), thump())

bed *= 0.92
fade = np.minimum(1, np.minimum(np.arange(n) / (0.15 * SR), (n - np.arange(n)) / (0.25 * SR)))
write("cafe-ambience.wav", bed * fade)

# --- exact effects, one file per visible action ---------------------------
sfx = np.zeros(int(0.9 * SR))
for t in np.arange(0.0, 0.85, 0.21):
    add(sfx, float(t), thump())
write("sfx-footsteps.wav", sfx)

n = int(0.24 * SR)
t = np.arange(n) / SR
click = 0.5 * (noise(n) - lowpass(noise(n), 900)) * envelope(n, 0.001, 0.012)
click += 0.22 * np.sin(2 * np.pi * 920 * t) * envelope(n, 0.001, 0.02)
write("sfx-laptop.wav", click)

n = int(0.62 * SR)
t = np.arange(n) / SR
ping = 0.3 * np.sin(2 * np.pi * 988 * t) * envelope(n, 0.002, 0.14)
ping += 0.2 * np.sin(2 * np.pi * 1318 * t) * envelope(n, 0.002, 0.19) * (t > 0.075)
write("sfx-ping.wav", ping)

n = int(0.34 * SR)
cup = clink(0.34, 1850) * 0.9
cup += 0.16 * lowpass(noise(n), 240) * envelope(n, 0.001, 0.035)
write("sfx-cup.wav", cup)

n = int(0.3 * SR)
t = np.arange(n) / SR
whip = bandpass(noise(n), 200, 3400) * np.sin(np.pi * t / (n / SR)) ** 1.6
write("sfx-whip.wav", 0.24 * whip)

n = int(0.44 * SR)
cloth = bandpass(noise(n), 900, 4200) * envelope(n, 0.03, 0.16)
write("sfx-cloth.wav", 0.16 * cloth)
