"""The animations of make_pictures.py: each function returns the frames (upright, 32 pixels
wide) of a loop that closes by itself: the last frame is followed by the first one."""
import math

import numpy as np

from pixels import (
    WIDTH,
    Rng,
    blank,
    disc,
    hline,
    line,
    lit,
    put,
    rect,
    ring,
)

TAU = 2 * math.pi


def noise(x, y, t):
    """A number from 0 to 1 that is the same every time for the same pixel and frame."""
    n = (x * 73856093) ^ (y * 19349663) ^ (t * 83492791)
    n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0


# ------------------------------------------------------------------------------------------------


def equalizer():
    """Eight bars of segments that go up and down, and a mark that falls slowly behind each."""
    frames_count, height, bars = 16, 64, 8
    rng = Rng(11)
    # Every bar moves with two waves: how many times each goes around in one cycle, and its phase
    f = [rng.integers(1, 4) for _ in range(bars)]
    g = [(f[i] + rng.integers(1, 3) - 1) % 3 + 1 for i in range(bars)]
    p = [rng.random() for _ in range(bars)]
    q = [rng.random() for _ in range(bars)]

    levels = np.zeros((frames_count, bars), dtype=int)
    for t in range(frames_count):
        for i in range(bars):
            wave = 0.65 * math.sin(TAU * (f[i] * t / frames_count + p[i])) + 0.35 * math.sin(
                TAU * (g[i] * t / frames_count + q[i])
            )
            levels[t, i] = 1 + int(round((0.5 + 0.5 * wave) * 13))

    out = []
    for t in range(frames_count):
        pic = blank(height)
        for i in range(bars):
            x = 4 * i
            n = levels[t, i]
            for k in range(n):
                rect(pic, x, height - 4 * k - 4, 3, 3, fill=True)
            peak = min(15, max(levels[(t - k) % frames_count, i] for k in range(6)) + 1)
            if peak > n:
                hline(pic, x, x + 2, height - 4 * peak - 3)
        out.append(pic)
    return out


def radar():
    """A sweep with a trail that fades, and three blips that light up as it goes by."""
    frames_count, size, c = 24, 32, 15.5
    blips = [(10.0, math.radians(70)), (5.0, math.radians(200)), (12.0, math.radians(300))]
    out = []
    for t in range(frames_count):
        sweep = TAU * t / frames_count
        pic = blank(size)

        # The outer ring, an inner ring of dots and the cross
        ring(pic, c, c, 14.5)
        for k in range(24):
            u = TAU * k / 24
            put(pic, int(round(c + 7.5 * math.cos(u))), int(round(c + 7.5 * math.sin(u))))
        for i in range(3, 29, 3):
            put(pic, i, 15)
            put(pic, 15, i)

        for y in range(size):
            for x in range(size):
                d = math.hypot(x - c, y - c)
                if d > 14.0:
                    continue
                angle = math.atan2(x - c, -(y - c)) % TAU
                behind = (sweep - angle) % TAU
                if behind < 0.11:
                    put(pic, x, y)
                elif behind < 1.2 and d > 1.5:
                    if lit((1 - behind / 1.2) ** 2.0 * 0.85, x, y):
                        put(pic, x, y)

        for r, a in blips:
            behind = (sweep - a) % TAU
            strength = 1 - behind / (TAU * 0.85)
            if strength > 0.12:
                bx, by = c + r * math.sin(a), c - r * math.cos(a)
                size_px = 3 if strength > 0.55 else 2 if strength > 0.3 else 1
                half = size_px // 2
                for dy in range(size_px):
                    for dx in range(size_px):
                        put(pic, int(round(bx)) - half + dx, int(round(by)) - half + dy)
        out.append(pic)
    return out


def heartbeat():
    """The trace of a heart monitor, scrolling down, fading as it gets old."""
    frames_count, height, period = 16, 64, 32
    shape = [
        (0, 0), (2, 0), (3.5, 2), (5, 0), (8, 0), (9, -3), (11, 11), (13, -6), (14, 0),
        (18, 0), (20, 3), (22, 4), (24, 3), (26, 0), (32, 0),
    ]  # fmt: skip

    def amplitude(y):
        y = y % period
        for (y0, a0), (y1, a1) in zip(shape, shape[1:]):
            if y0 <= y <= y1:
                return a0 + (a1 - a0) * (y - y0) / (y1 - y0) if y1 > y0 else a0
        return 0

    out = []
    for t in range(frames_count):
        shift = 2 * t
        pic = blank(height)
        # a grid of dots
        for y in range(4, height, 8):
            for x in range(4, WIDTH, 8):
                put(pic, x, y)

        previous = None
        for y in range(height):
            x = int(round(12 + amplitude(y - shift)))
            if previous is not None:
                line(pic, previous[0], previous[1], x, y)
            previous = (x, y)

        # The trace fades in the lower part: older, and about to leave
        for y in range(36, height):
            density = (height - 1 - y) / 28.0
            for x in range(WIDTH):
                if pic[y, x] and not lit(density, x, y):
                    pic[y, x] = 0
        out.append(pic)
    return out


def digital_rain():
    """Streaks that fall down the whole screen, bright at the head and flickering behind it."""
    frames_count, height = 32, 128
    rng = Rng(5)
    columns = []
    for c in range(16):
        period, step = [(128, 4), (128, 8), (64, 2), (64, 4)][rng.integers(0, 4)]
        columns.append(
            dict(
                x=1 + 2 * c,
                period=period,
                step=step,
                offset=rng.integers(0, period),
                tail=rng.integers(12, 30),
            )
        )

    out = []
    for t in range(frames_count):
        pic = blank(height)
        for col in columns:
            head = (col["offset"] + col["step"] * t) % col["period"]
            for y in range(height):
                behind = (head - y) % col["period"]
                if behind >= col["tail"]:
                    continue
                if behind == 0:
                    put(pic, col["x"], y)
                    put(pic, col["x"] + 1, y)
                else:
                    strength = (1 - behind / col["tail"]) ** 1.3
                    if strength > noise(col["x"], y, t % frames_count) * 0.9:
                        put(pic, col["x"], y)
        out.append(pic)
    return out


def cube():
    """A wire cube that turns; the edges at the back are dotted."""
    frames_count, size, c = 16, 32, 15.5
    vertices = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    edges = [
        (a, b)
        for a in range(8)
        for b in range(a + 1, 8)
        if sum(p != q for p, q in zip(vertices[a], vertices[b])) == 1
    ]
    tilt = 0.62
    out = []
    for t in range(frames_count):
        # A cube looks the same after a quarter of a turn: that is the loop
        turn = math.pi / 4 + (math.pi / 2) * t / frames_count
        projected = []
        for x, y, z in vertices:
            x1 = x * math.cos(turn) + z * math.sin(turn)
            z1 = -x * math.sin(turn) + z * math.cos(turn)
            y1 = y * math.cos(tilt) - z1 * math.sin(tilt)
            z2 = y * math.sin(tilt) + z1 * math.cos(tilt)
            scale = 8.2 / (1 - z2 / 9.0)
            projected.append((c + x1 * scale, c + y1 * scale, z2))

        pic = blank(size)
        for a, b in edges:
            (xa, ya, za), (xb, yb, zb) = projected[a], projected[b]
            back = (za + zb) / 2 < -0.15
            line(pic, xa, ya, xb, yb, dotted=back)
        for x, y, z in projected:
            if z > 0.3:
                disc(pic, x, y, 1.0)
        out.append(pic)
    return out


def atom():
    """A nucleus with three orbits and an electron on each."""
    frames_count, size, c = 24, 32, 15.5
    out = []
    for t in range(frames_count):
        pic = blank(size)
        disc(pic, c, c, 1.6)
        for y in range(size):
            for x in range(size):
                d = math.hypot(x - c, y - c)
                if 2.6 <= d <= 4.0 and lit(0.35, x, y):
                    put(pic, x, y)

        for k in range(3):
            tilt = math.radians(60 * k)
            for i in range(160):
                u = TAU * i / 160
                ex, ey = 14.0 * math.cos(u), 5.0 * math.sin(u)
                x = c + ex * math.cos(tilt) - ey * math.sin(tilt)
                y = c + ex * math.sin(tilt) + ey * math.cos(tilt)
                if i % 3 == 0:
                    put(pic, int(round(x)), int(round(y)))

            u = TAU * (t / frames_count + k / 3.0)
            ex, ey = 14.0 * math.cos(u), 5.0 * math.sin(u)
            x = c + ex * math.cos(tilt) - ey * math.sin(tilt)
            y = c + ex * math.sin(tilt) + ey * math.cos(tilt)
            disc(pic, x, y, 1.5)
        out.append(pic)
    return out


def helix():
    """The two strands of a DNA helix, turning around its axis, with the rungs between them."""
    frames_count, height = 16, 128
    out = []
    for t in range(frames_count):
        pic = blank(height)
        spin = TAU * t / frames_count
        for y in range(height):
            phase = TAU * y / 32.0 + spin
            xa = 16 + 11.5 * math.sin(phase)
            xb = 16 - 11.5 * math.sin(phase)
            depth = math.cos(phase)

            if y % 6 == 0 and abs(xa - xb) > 5:
                x0, x1 = int(round(min(xa, xb))) + 2, int(round(max(xa, xb))) - 2
                for x in range(x0, x1 + 1):
                    if (x + y // 6) % 2 == 0:
                        put(pic, x, y)

            for x, near in ((xa, depth >= 0), (xb, depth < 0)):
                xi = int(round(x))
                put(pic, xi, y)
                if near:
                    put(pic, xi + 1, y)
                    put(pic, xi - 1 if x < 16 else xi + 2, y)
        out.append(pic)
    return out


def warp():
    """Stars that fly out from the middle, faster and longer as they get near."""
    frames_count, height = 24, 64
    rng = Rng(3)
    stars = [(rng.random() * TAU, rng.random(), rng.integers(1, 3)) for _ in range(46)]
    cx, cy = 15.5, 31.5

    def where(angle, u):
        r = 1.5 + 36.0 * u**2.2
        return cx + r * math.cos(angle), cy + r * math.sin(angle) * 1.0

    out = []
    for t in range(frames_count):
        pic = blank(height)
        for angle, phase, speed in stars:
            u = (phase + speed * t / frames_count) % 1.0
            if u < 0.12:
                continue
            x, y = where(angle, u)
            if u > 0.45:
                x0, y0 = where(angle, u - 0.09)
                line(pic, x0, y0, x, y)
            else:
                put(pic, int(round(x)), int(round(y)))
        out.append(pic)
    return out


def sonar():
    """Rings that spread from the middle and fade."""
    frames_count, size, c = 16, 32, 15.5
    out = []
    for t in range(frames_count):
        pic = blank(size)
        disc(pic, c, c, 1.0)
        for k in range(3):
            u = (k / 3.0 + t / frames_count) % 1.0
            r = 2.0 + 13.5 * u
            # The ring is solid, and breaks up into dots as it fades near the edge
            density = 1.0 if u < 0.5 else 1.0 - ((u - 0.5) / 0.5) ** 1.2
            for y in range(size):
                for x in range(size):
                    if abs(math.hypot(x - c, y - c) - r) <= 0.62 and lit(density, x, y):
                        put(pic, x, y)
        out.append(pic)
    return out


def bounce():
    """A ball that bounces, squashes at the floor and has a shadow."""
    frames_count, height, floor = 24, 64, 57
    out = []
    for t in range(frames_count):
        u = t / frames_count
        rise = 40.0 * 4 * u * (1 - u)
        squash = max(0.0, 4.0 - rise) * 0.55
        rx, ry = 5.0 + squash, 5.0 - squash

        pic = blank(height)
        hline(pic, 2, 29, floor + 1)
        shadow = 4 + int(round(9 * (1 - rise / 40.0)))
        hline(pic, 16 - shadow, 16 + shadow, floor + 3)

        cy = floor - ry - rise
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(8, 25):
                if ((x - 15.5) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                    put(pic, x, y)
        # A shine
        for dx, dy in ((-2, -2), (-1, -2), (-2, -1)):
            put(pic, int(round(15.5 + dx * rx / 5)), int(round(cy + dy * ry / 5)), 0)
        out.append(pic)
    return out


def flame():
    """A fire that flickers."""
    frames_count, height = 16, 64
    out = []
    for t in range(frames_count):
        pic = blank(height)
        for y in range(height):
            # How far up the fire the pixel is (0 at the base, 1 at the tip)
            rise = 1 - y / (height - 1)
            for x in range(WIDTH):
                # The flame sways more the higher it goes, and licks upwards
                sway = 4.2 * rise**1.4 * math.sin(TAU * (rise * 1.3 - t / frames_count))
                lick = math.sin(TAU * (rise * 3.0 - 2 * t / frames_count))
                width = 14.0 * (1 - rise**1.15) ** 0.85
                side = abs(x - 15.5 - sway) / max(width, 0.4)
                heat = ((1 - side**1.4) + 0.3 * lick * rise) * (1 - rise**0.9)
                if heat > 0.0 and lit(min(1.0, heat * 1.5), x, y):
                    put(pic, x, y)
        out.append(pic)
    return out


# name -> (function, milliseconds of one cycle)
ANIMATIONS = {
    "equalizer": (equalizer, 1200),
    "radar": (radar, 2400),
    "heartbeat": (heartbeat, 1600),
    "rain": (digital_rain, 3200),
    "cube": (cube, 1600),
    "atom": (atom, 2400),
    "helix": (helix, 1600),
    "warp": (warp, 2400),
    "sonar": (sonar, 1600),
    "bounce": (bounce, 1200),
    "flame": (flame, 1200),
}
