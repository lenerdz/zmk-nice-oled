"""The second batch of animations of make_pictures.py (kinds 26 to 45): each function returns the
frames (upright, 32 pixels wide) of a loop that closes by itself: the last frame is followed by the
first one. Nothing here uses random numbers from numpy (see Rng in pixels.py)."""
import math

import numpy as np

from animations import noise
from pixels import (
    BAYER8,
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
    sprite,
    text,
    vline,
)

TAU = 2 * math.pi


def triangle_wave(u, low, high):
    """A value that goes back and forth between low and high as u grows (a ball between two walls)."""
    span = high - low
    d = (u - low) % (2 * span)
    return low + (d if d <= span else 2 * span - d)


def fill_triangle(pic, p0, p1, p2, value=1):
    """A filled triangle; the points are (x, y)."""
    xs, ys = [p[0] for p in (p0, p1, p2)], [p[1] for p in (p0, p1, p2)]

    def side(a, b, x, y):
        return (b[0] - a[0]) * (y - a[1]) - (b[1] - a[1]) * (x - a[0])

    for y in range(int(math.floor(min(ys))), int(math.ceil(max(ys))) + 1):
        for x in range(int(math.floor(min(xs))), int(math.ceil(max(xs))) + 1):
            s0, s1, s2 = side(p0, p1, x, y), side(p1, p2, x, y), side(p2, p0, x, y)
            if (s0 >= 0 and s1 >= 0 and s2 >= 0) or (s0 <= 0 and s1 <= 0 and s2 <= 0):
                put(pic, x, y, value)


def rotated(pic, angle, cx, cy):
    """The picture turned by an angle (radians, clockwise) about a point, by sampling four points
    of every pixel: a pixel is lit when two of them land on a lit pixel."""
    h, w = pic.shape
    out = blank(h, w)
    cos, sin = math.cos(angle), math.sin(angle)
    for y in range(h):
        for x in range(w):
            hits = 0
            for dy in (0.25, 0.75):
                for dx in (0.25, 0.75):
                    px, py = x + dx - 0.5 - cx, y + dy - 0.5 - cy
                    sx = cx + px * cos + py * sin
                    sy = cy - px * sin + py * cos
                    ix, iy = int(math.floor(sx + 0.5)), int(math.floor(sy + 0.5))
                    if 0 <= ix < w and 0 <= iy < h and pic[iy, ix]:
                        hits += 1
            if hits >= 2:
                out[y, x] = 1
    return out


# ------------------------------------------------------------------------------------------------


def waterfall():
    """Water that falls over a ledge between two cliffs, with mist and a pool that ripples."""
    frames_count, height, period = 16, 128, 32
    lip, pool, c = 14, 106, 15.5
    rng = Rng(41)

    def banks(y):
        """The x of the left and of the right bank at a row: a river that narrows towards the ledge,
        and a fall that widens as it goes down."""
        spread = 7.0 * (lip - y) / lip if y < lip else (y - lip) * 0.075
        return 9.0 - spread, 22.0 + spread

    # The rock of the cliffs, with strata: the same in every frame
    rock = blank(height)
    for y in range(height):
        left, right = banks(y)
        for x in range(WIDTH):
            if x < int(round(left)) - 1 or x > int(round(right)) + 1:
                # Chunks of 2 x 3 pixels, which look more like stone than a dither does
                if noise(x // 2, y // 3, 7) < 0.3:
                    rock[y, x] = 1
    for y in range(8, 104, 9):
        left, right = banks(y)
        for x0, x1 in ((0, int(round(left)) - 3), (int(round(right)) + 3, WIDTH - 1)):
            if x1 - x0 >= 3:
                start = x0 + rng.integers(0, max(1, x1 - x0 - 2))
                hline(rock, start, min(x1, start + rng.integers(3, 8)), y + rng.integers(0, 3))

    # The streams of the fall: a position across it (-1 to 1), how fast, and where the dashes are
    strands = []
    for i in range(12):
        strands.append(
            dict(
                rel=-0.92 + 1.84 * i / 11.0 + 0.03 * (rng.random() - 0.5),
                speed=2 if i % 3 == 1 else 1,
                off=rng.integers(0, period),
                first=rng.integers(7, 14),
                second=rng.integers(5, 10),
                gap=rng.integers(15, 20),
                wide=(i % 4 == 0),
            )
        )
    drops = [(rng.integers(6, 26), rng.integers(-6, 7), rng.integers(6, 15), rng.random()) for _ in range(9)]

    out = []
    for t in range(frames_count):
        pic = rock.copy()
        for y in range(height):
            left, right = banks(y)
            x0, x1 = int(round(left)), int(round(right))
            # The water is dark between the bright strands; the cliffs end in a bright edge
            for x in range(x0, x1 + 1):
                pic[y, x] = 0
            put(pic, x0 - 1, y, 1)
            put(pic, x1 + 1, y, 1)
            if y < lip:
                for x in range(x0, x1 + 1):
                    if ((y - 2 * t) % 8 < 2) and ((x + ((y - 2 * t) // 8 % 2) * 2) % 5 < 3):
                        put(pic, x, y)
            elif y < pool:
                half = (right - left) / 2.0
                for s in strands:
                    pos = (y - 2 * s["speed"] * t - s["off"]) % period
                    if pos < s["first"] or s["gap"] <= pos < s["gap"] + s["second"]:
                        x = int(round(c + s["rel"] * (half - 0.5)))
                        put(pic, x, y)
                        if s["wide"]:
                            put(pic, x + 1, y)

        # Foam at the ledge
        for y in range(lip, lip + 3):
            left, right = banks(y)
            for x in range(int(round(left)), int(round(right)) + 1):
                if (x + t + y) % 4 < 3:
                    pic[y, x] = 1

        # The mist that rises where the water lands
        for y in range(88, pool + 4):
            for x in range(3, 29):
                density = 0.7 * (1 - abs(x - c) / 14.0) * (1 - (pool + 2 - y) / 20.0)
                if density > 0 and noise(x // 2, y // 2, t) < density and lit(0.75, x, y, BAYER8):
                    put(pic, x, y)

        # The pool: waves that go sideways, and rings from where the water lands
        for y in range(pool + 4, height):
            for x in range(WIDTH):
                pic[y, x] = 0
        for k, row in enumerate((pool + 6, pool + 10, pool + 14, pool + 18)):
            direction = 1 if k % 2 == 0 else -1
            for x in range(WIDTH):
                if (x + direction * t) % 8 < 5:
                    put(pic, x, row)
        for k in range(3):
            u = (k / 3.0 + t / frames_count) % 1.0
            rx, ry = 3.0 + 15.0 * u, 0.9 + 2.6 * u
            for y in range(pool - 3, height):
                for x in range(WIDTH):
                    d = math.hypot((x - c) / rx, (y - (pool + 3)) / ry)
                    if abs(d - 1.0) < 0.2 and lit(1.0 - u * 0.8, x, y):
                        put(pic, x, y)

        # Drops thrown up by the water that lands
        for x0, vx, rise, phase in drops:
            u = (phase + t / frames_count) % 1.0
            x = x0 + vx * u
            y = pool + 2 - rise * 4 * u * (1 - u)
            put(pic, int(round(x)), int(round(y)))
            if u < 0.5:
                put(pic, int(round(x)), int(round(y)) + 1)
        out.append(pic)
    return out


def lava():
    """A lava lamp: blobs of wax that rise, stretch and sink again in a glass with a base."""
    frames_count, height, c = 16, 128, 15.5
    rng = Rng(52)

    def half_width(y):
        if y <= 96:
            return 5.0 + 7.0 * ((y - 6) / 90.0) ** 0.9
        return 12.0 - (y - 96) * 0.25

    blobs = []
    for i in range(7):
        blobs.append(
            dict(
                x=3.5 * math.sin(i * 2.1),
                ax=1.5 + 2.5 * rng.random(),
                y=18 + 12.5 * i,
                ay=10.0 + 8.0 * rng.random(),
                k=1 + (i % 2),
                ph=rng.random(),
                phx=rng.random(),
                r=3.2 + 2.2 * rng.random() + (0.6 if i % 3 == 0 else 0.0),
            )
        )

    out = []
    for t in range(frames_count):
        pic = blank(height)
        u = t / frames_count
        centers = [
            (
                c + b["x"] + b["ax"] * math.sin(TAU * (u + b["phx"])),
                b["y"] + b["ay"] * math.sin(TAU * (b["k"] * u + b["ph"])),
                b["r"],
            )
            for b in blobs
        ]
        for y in range(6, 105):
            hw = half_width(y)
            for x in range(WIDTH):
                if abs(x - c) > hw - 1.2:
                    continue
                field = 0.0
                for bx, by, r in centers:
                    field += r * r / ((x - bx) ** 2 + 1.6 * (y - by) ** 2 / 2.0 + 0.4)
                # The wax that rests at the bottom of the glass
                field += max(0.0, (y - 90) / 11.0) ** 1.6
                if field > 1.0:
                    put(pic, x, y)
                elif field > 0.72 and lit((field - 0.72) / 0.28, x, y):
                    put(pic, x, y)

        # The glass
        for y in range(6, 105):
            hw = half_width(y)
            put(pic, int(round(c - hw)), y)
            put(pic, int(round(c + hw)), y)
        hline(pic, int(round(c - half_width(105))), int(round(c + half_width(105))), 105)
        # The cap, and the base
        rect(pic, 10, 0, 12, 5)
        hline(pic, 12, 19, 5)
        for y in range(106, 128):
            left = 8 - (y - 106) * 5.0 / 21.0
            put(pic, int(round(left)), y)
            put(pic, int(round(31 - left)), y)
        hline(pic, 8, 23, 106)
        hline(pic, 7, 24, 107)
        hline(pic, 3, 28, 127)
        hline(pic, 5, 26, 118)
        for x in range(9, 23, 3):
            put(pic, x, 112)
        out.append(pic)
    return out


def lightning():
    """A storm: a cloud, slanting rain, and two bolts that flash one after the other."""
    frames_count, height = 16, 64
    rng = Rng(63)

    cloud = [(7, 8, 6.0), (14, 5, 7.0), (22, 8, 6.2), (11, 11, 5.2), (19, 12, 5.0), (27, 11, 4.0), (3, 12, 3.5)]

    def in_cloud(x, y):
        return any(math.hypot(x - cx, y - cy) <= r for cx, cy, r in cloud)

    shape = blank(height)
    for y in range(0, 22):
        for x in range(WIDTH):
            if in_cloud(x, y):
                shape[y, x] = 1
    edge = blank(height)
    for y in range(0, 22):
        for x in range(WIDTH):
            if shape[y, x]:
                around = [
                    shape[y + dy, x + dx] if 0 <= x + dx < WIDTH and 0 <= y + dy < height else 0
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                ]
                if min(around) == 0 and (y > 0):
                    edge[y, x] = 1

    def bolt(x0, seed):
        r = Rng(seed)
        points = [(x0, 14)]
        x, y = float(x0), 14.0
        while y < 58:
            y += r.integers(4, 8)
            x += r.integers(-5, 6)
            x = min(max(x, 3), 28)
            points.append((x, min(y, 59)))
        return points

    bolts = {3: bolt(11, 5), 4: bolt(11, 5), 5: bolt(11, 5), 10: bolt(21, 9), 11: bolt(21, 9), 12: bolt(21, 9)}
    rain = [(rng.integers(0, WIDTH), rng.integers(0, height)) for _ in range(46)]

    out = []
    for t in range(frames_count):
        pic = blank(height)
        flash = t in (4, 11)
        if flash:
            for y in range(height):
                for x in range(WIDTH):
                    if lit(0.1, x, y):
                        put(pic, x, y)

        for x0, y0 in rain:
            y = (y0 + 4 * t) % height
            x = (x0 - 2 * t) % WIDTH
            line(pic, x, y, x - 1, y - 2)

        for y in range(0, 22):
            for x in range(WIDTH):
                if shape[y, x]:
                    # Lighter on top, darker underneath
                    body = lit(0.62 - 0.027 * y, x, y, BAYER8)
                    pic[y, x] = 1 if (edge[y, x] or flash or body) else 0
        # The underside of the cloud
        for x in range(2, 30):
            if lit(0.5, x, 17) and shape[16, x]:
                put(pic, x, 17)

        if t in bolts:
            pts = bolts[t]
            thick = t in (3, 4, 10, 11)
            for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
                line(pic, xa, ya, xb, yb)
                if thick:
                    line(pic, xa + 1, ya, xb + 1, yb)
            # A branch
            if len(pts) > 3:
                bx, by = pts[2]
                line(pic, bx, by, bx + (6 if bx < 16 else -6), by + 7)
            # Where it lands
            lx, ly = pts[-1]
            for dx in (-3, -2, 2, 3):
                put(pic, int(lx) + dx, 61)
        hline(pic, 0, 31, 63)
        out.append(pic)
    return out


def snow():
    """Snow that falls past a pine tree on a hill, under a moon."""
    frames_count, height = 24, 64
    rng = Rng(74)

    flakes = []
    for i in range(34):
        flakes.append(
            dict(
                x=rng.integers(0, WIDTH),
                y=rng.integers(0, height),
                speed=1 if i % 3 else 2,
                sway=1.0 + 2.0 * rng.random(),
                phase=rng.random(),
                near=(i % 3 == 0),
            )
        )

    cx = 12
    # (the top of the layer, the bottom, half of its width at the bottom)
    layers = [(14, 25, 6), (20, 33, 8), (27, 42, 10), (34, 51, 12)]

    def draw_flake(pic, f, t):
        y = (f["y"] + f["speed"] * t * height / frames_count) % height
        x = f["x"] + f["sway"] * math.sin(TAU * (f["phase"] + t / frames_count))
        xi, yi = int(round(x)), int(round(y))
        put(pic, xi, yi)
        if f["near"]:
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                put(pic, xi + dx, yi + dy)

    out = []
    for t in range(frames_count):
        pic = blank(height)
        # The moon: a crescent
        for y in range(1, 16):
            for x in range(18, 32):
                if math.hypot(x - 25, y - 8) <= 5.6 and math.hypot(x - 27.4, y - 6.6) > 4.8:
                    put(pic, x, y)

        # The snow that is far away is behind the tree, the near snow in front of it
        for f in flakes:
            if not f["near"]:
                draw_flake(pic, f, t)

        # The tree: every layer clears what is behind it, then has its edges and a little snow
        for top, base, half in layers:
            fill_triangle(pic, (cx, top), (cx - half, base), (cx + half, base), 0)
        for top, base, half in layers:
            line(pic, cx, top, cx - half, base)
            line(pic, cx, top, cx + half, base)
            # The lower edge has a notch for every branch
            for k in range(-half, half + 1, 3):
                put(pic, cx + k, base)
                put(pic, cx + k + 1, base - 1)
            # The snow on the top of the layer
            for k in range(-2, 3):
                put(pic, cx + k, top + 3 + abs(k) // 2)
        rect(pic, cx - 1, 51, 3, 6, fill=True)
        # A star on the top
        for dx, dy in ((0, 12), (0, 11), (-1, 12), (1, 12), (0, 13)):
            put(pic, cx + dx, dy)

        for f in flakes:
            if f["near"]:
                draw_flake(pic, f, t)

        # The hill, with a drift
        for x in range(WIDTH):
            top = 56 + int(round(1.8 * math.sin(TAU * x / 32.0 + 1.0)))
            put(pic, x, top)
            for y in range(top + 1, height):
                if noise(x // 2, y, 5) < 0.28:
                    put(pic, x, y)
        out.append(pic)
    return out


def jellyfish():
    """A jellyfish that pulses, with tentacles that wave, and a few specks that float up."""
    frames_count, height, c = 16, 64, 15.5
    rng = Rng(85)
    specks = [(rng.integers(1, 31), rng.integers(0, 32)) for _ in range(5)]

    out = []
    for t in range(frames_count):
        u = t / frames_count
        pulse = math.sin(TAU * u)
        cy = 21.0 + 1.5 * math.sin(TAU * u + 1.2)
        rx, ry = 10.5 + 1.8 * pulse, 8.0 - 1.4 * pulse

        pic = blank(height)
        # The bell: the upper half of an ellipse, shaded, with a rim
        for y in range(int(cy - ry) - 1, int(cy) + 2):
            for x in range(WIDTH):
                d = math.hypot((x - c) / rx, (y - cy) / ry)
                if y <= cy + 0.5 and d <= 1.0:
                    edge = d > 1.0 - 1.15 / min(rx, ry)
                    if edge or lit(0.34 + 0.2 * (1 - d), x, y):
                        put(pic, x, y)
        # Arcs inside the bell
        for scale in (0.62, 0.3):
            for x in range(WIDTH):
                inner = 1 - ((x - c) / (rx * scale)) ** 2
                if inner > 0:
                    put(pic, x, int(round(cy - ry * scale * math.sqrt(inner) * 0.9)))
        # The rim under the bell, scalloped
        for x in range(int(c - rx), int(c + rx) + 1):
            put(pic, x, int(round(cy + 0.5 + 0.8 * math.cos((x - c) * TAU / 4.2))))

        # Long tentacles and short thick arms
        for i in range(6):
            x0 = c + (i - 2.5) * rx * 0.34
            length = 30 if i % 2 == 0 else 20
            prev = None
            for k in range(length):
                y = cy + 1.5 + k
                amplitude = 3.2 * min(1.0, k / 12.0)
                x = x0 + amplitude * math.sin(TAU * (k / 11.0 - u + i / 7.0))
                if prev is not None:
                    line(pic, prev[0], prev[1], x, y, dotted=(i % 2 == 1))
                prev = (x, y)
        for x, y0 in specks:
            for y in ((y0 - 2 * t) % 64, (y0 + 32 - 2 * t) % 64):
                put(pic, x, y)
        out.append(pic)
    return out


# Tetris: a piece is the cells of its rotations, as (column, row) offsets
PIECES = {
    "I": [[(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 1), (1, 1), (2, 1), (3, 1)]],
    "O": [[(0, 0), (1, 0), (0, 1), (1, 1)]],
    "T": [[(1, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (2, 1), (1, 2)],
          [(0, 1), (1, 1), (2, 1), (1, 2)], [(1, 0), (0, 1), (1, 1), (1, 2)]],
    "L": [[(0, 0), (0, 1), (0, 2), (1, 2)], [(0, 1), (1, 1), (2, 1), (0, 2)],
          [(0, 0), (1, 0), (1, 1), (1, 2)], [(2, 0), (0, 1), (1, 1), (2, 1)]],
    "S": [[(1, 0), (2, 0), (0, 1), (1, 1)], [(0, 0), (0, 1), (1, 1), (1, 2)]],
    "Z": [[(0, 0), (1, 0), (1, 1), (2, 1)], [(1, 0), (0, 1), (1, 1), (0, 2)]],
}  # fmt: skip


def tetris():
    """Pieces that fall down a board of eight columns, turning on the way, like a screen saver of
    the game (they pass each other and leave at the bottom)."""
    frames_count, cols, rows, fall = 20, 8, 16, 20
    rng = Rng(96)
    names = list(PIECES)

    def cells(piece, t):
        shape, x0, phase, turns = piece
        step = (t - phase) % fall
        row = step - 4
        rotation = sum(1 for turn in turns if step >= turn) % len(PIECES[shape])
        return {(x0 + cx, row + cy) for cx, cy in PIECES[shape][rotation]}

    chosen = None
    for _attempt in range(4000):
        pieces = []
        for k in range(6):
            shape = names[rng.integers(0, len(names))]
            turns = sorted({rng.integers(3, 17) for _ in range(rng.integers(0, 3))})
            span = [max(cx for cx, _ in rot) + 1 for rot in PIECES[shape]]
            x0 = rng.integers(0, cols - max(span) + 1)
            pieces.append((shape, x0, (k * 3 + rng.integers(0, 2)) % fall, turns))
        ok = True
        for t in range(fall):
            seen = set()
            for p in pieces:
                here = cells(p, t)
                if any(not (0 <= cx < cols) for cx, _ in here) or seen & here:
                    ok = False
                    break
                seen |= here
            if not ok:
                break
        if ok:
            chosen = pieces
            break
    if chosen is None:
        raise SystemExit("tetris: no arrangement of pieces without a collision")

    out = []
    for t in range(frames_count):
        pic = blank(rows * 4)
        taken = set()
        for p in chosen:
            for cx, cy in cells(p, t):
                if 0 <= cy < rows:
                    rect(pic, cx * 4, cy * 4, 3, 3, fill=True)
                    taken.add((cx, cy))
        # A dot in the middle of every cell that is empty: the grid of the well
        for cx in range(cols):
            for cy in range(rows):
                if (cx, cy) not in taken:
                    put(pic, cx * 4 + 1, cy * 4 + 1)
        out.append(pic)
    return out


def pong():
    """A game of pong played from top to bottom: two paddles that follow the ball, the net, and the
    score."""
    frames_count, height = 24, 64
    out = []

    def position(t):
        x = triangle_wave(2.0 + 54.0 * t / frames_count + 9.0, 2.0, 29.0)
        y = triangle_wave(6.0 + 102.0 * t / frames_count + 20.0, 6.0, 57.0)
        return x, y

    for t in range(frames_count):
        pic = blank(height)
        bx, by = position(t)
        for x in range(0, 32, 4):
            hline(pic, x, x + 1, 31)
        text(pic, 2, 23, "03")
        text(pic, 2, 36, "07")
        # The paddles follow the ball, a little behind it
        for y in (2, 60):
            centre = 15.5 + (position(t - 2)[0] - 15.5) * 0.85
            x0 = int(round(centre - 4.5))
            x0 = min(max(x0, 0), 23)
            rect(pic, x0, y, 9, 2, fill=True)
        # The ball, and where it was
        for k, size in ((1, 1), (2, 1)):
            px, py = position(t - k)
            if k == 2:
                put(pic, int(round(px)), int(round(py)))
            else:
                rect(pic, int(round(px)), int(round(py)), 1, 1, fill=True)
        rect(pic, int(round(bx)) - 1, int(round(by)) - 1, 3, 3, fill=True)
        out.append(pic)
    return out


INVADER_SQUID = [
    ["...##...", "..####..", ".######.", "##.##.##", "########", "..#..#..", ".#.##.#.", "#.#..#.#"],
    ["...##...", "..####..", ".######.", "##.##.##", "########", ".#.##.#.", "#......#", ".#....#."],
]
INVADER_CRAB = [
    ["..#..#..", "...##...", "..####..", ".##..##.", "########", "#.####.#", "#.#..#.#", "...##..."],
    ["..#..#..", "#..##..#", "#.####.#", "###..###", "########", ".######.", "..#..#..", ".#....#."],
]
INVADER_OCTOPUS = [
    ["..####..", ".######.", "########", "##.##.##", "########", "..#..#..", ".#.##.#.", "##....##"],
    ["..####..", ".######.", "########", "##.##.##", "########", ".##..##.", "##.##.##", ".#....#."],
]
INVADER_BURST = ["#..##..#", ".#.##.#.", "..####..", "###..###", "###..###", "..####..", ".#.##.#.", "#..##..#"]


def invaders():
    """A formation of aliens that marches from side to side, a cannon that shoots one down, and
    a saucer that crosses the top."""
    frames_count, height = 8, 64
    out = []
    kinds = [INVADER_SQUID, INVADER_CRAB, INVADER_CRAB, INVADER_OCTOPUS]
    shifts = [0, 1, 2, 3, 4, 3, 2, 1]
    for t in range(frames_count):
        pic = blank(height)
        # The saucer: it needs 8 frames to cross the top, 5 pixels at a time
        ux = (5 * t + 24) % 40 - 8
        sprite(pic, ux, 0, ["..####..", ".######.", "##.##.##", ".#....#."])
        for row, art in enumerate(kinds):
            for col in range(3):
                x = shifts[t] + 10 * col
                y = 6 + 9 * row
                if row == 3 and col == 1 and t >= 2:
                    # The one the cannon hits: it bursts, and is gone until the loop starts again
                    if t < 4:
                        sprite(pic, x, y, INVADER_BURST)
                    continue
                sprite(pic, x, y, art[t % 2])
        # The shields
        for x in (2, 10, 18, 26):
            sprite(pic, x, 48, [".###.", "#####", "##.##"])
        # The cannon and its shot
        sprite(pic, 13, 56, ["...#...", "..###..", "#######"])
        shot = 54 - 7 * t
        if t < 2:
            vline(pic, 16, shot, shot + 2)
        hline(pic, 0, 31, 63)
        out.append(pic)
    return out


def pac_man(pic, cx, cy, mouth, r=4.5):
    """A disc with a wedge cut out, looking to the right; the wedge is `mouth` radians to each side."""
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            dx, dy = x - cx, y - cy
            if math.hypot(dx, dy) <= r + 0.2 and not (dx > 0 and abs(math.atan2(dy, dx)) < mouth):
                put(pic, x, y)


def ghost(pic, x0, y0, frame, scared=False):
    """A ghost of 9 x 9 pixels with a wavy hem; a scared one is an outline with a wavy mouth."""
    body = blank(9, 9)
    for y in range(9):
        for x in range(9):
            if y <= 4:
                inside = math.hypot(x - 4, y - 4) <= 4.5
            else:
                inside = True
            if y == 8:
                inside = (x + frame) % 2 == 0
            if inside:
                body[y, x] = 1
    for y in range(9):
        for x in range(9):
            if not body[y, x]:
                continue
            if scared:
                around = [
                    body[y + dy, x + dx] if 0 <= x + dx < 9 and 0 <= y + dy < 9 else 0
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                ]
                if min(around) == 0:
                    put(pic, x0 + x, y0 + y)
            else:
                put(pic, x0 + x, y0 + y)
    if scared:
        for x in range(1, 8):
            put(pic, x0 + x, y0 + (6 if x % 2 else 7))
        put(pic, x0 + 3, y0 + 3)
        put(pic, x0 + 5, y0 + 3)
    else:
        # The eyes: a hole with a pupil that looks forward
        for ex in (2, 5):
            for dy in (3, 4):
                put(pic, x0 + ex, y0 + dy, 0)
                put(pic, x0 + ex + 1, y0 + dy, 0)
            put(pic, x0 + ex + 1, y0 + 4)


def pacman():
    """Pac-Man eats a row of dots chasing a scared ghost, and a ghost chases him on the next row."""
    frames_count, size = 16, 32
    length = 62
    out = []
    for t in range(frames_count):
        pic = blank(size)
        # The first row: the dots, Pac-Man behind a scared ghost
        head = -9 + length * t / frames_count
        pac_x = head - 21
        ghost_x = head - 9
        for k in range(8):
            dx = 3 + 4 * k
            if dx > pac_x + 5.5:
                put(pic, dx, 7)
        mouth = (0.0, 0.5, 0.9, 0.5)[t % 4]
        pac_man(pic, pac_x + 4, 7, mouth)
        ghost(pic, int(round(ghost_x)), 3, t % 2, scared=True)

        # The second row: a ghost behind Pac-Man, half a loop later
        head2 = -9 + length * ((t + 8) % frames_count) / frames_count
        pac2_x = head2 - 9
        ghost2_x = head2 - 21
        pac_man(pic, pac2_x + 4, 24, (0.0, 0.5, 0.9, 0.5)[(t + 2) % 4])
        ghost(pic, int(round(ghost2_x)), 20, t % 2)
        # Both rows are on a floor
        hline(pic, 0, 31, 13)
        hline(pic, 0, 31, 30)
        out.append(pic)
    return out


def life_cells(rows):
    """The (row, column) of the live cells of a pattern written as strings."""
    return [(y, x) for y, line_ in enumerate(rows) for x, ch in enumerate(line_) if ch == "#"]


LIFE_PATTERNS = {
    "pulsar": [
        "..###...###..", ".............", "#....#.#....#", "#....#.#....#", "#....#.#....#",
        "..###...###..", ".............", "..###...###..", "#....#.#....#", "#....#.#....#",
        "#....#.#....#", ".............", "..###...###..",
    ],
    "penta": ["..#....#..", "##.####.##", "..#....#.."],
    "toad": [".###", "###."],
    "beacon": ["##..", "##..", "..##", "..##"],
    "blinker": ["###"],
    "block": ["##", "##"],
    "beehive": [".##.", "#..#", ".##."],
    "boat": ["##.", "#.#", ".#."],
    "loaf": [".##.", "#..#", ".#.#", "..#."],
}  # fmt: skip


def life():
    """Conway's Game of Life on a small field: a pulsar (period 3), a pentadecathlon (period 15),
    a toad, a beacon and blinkers (period 2), and some still lifes. All of them are back where
    they started after 30 generations, which is the loop."""
    frames_count, rows, cols = 30, 64, 32
    board = np.zeros((rows, cols), dtype=np.uint8)

    def place(name, y, x, turned=False):
        pattern = LIFE_PATTERNS[name]
        if turned:
            pattern = ["".join(row[i] for row in pattern) for i in range(len(pattern[0]))]
        for dy, dx in life_cells(pattern):
            board[y + dy, x + dx] = 1

    # Every pattern is at least two empty cells from the others, whatever phase it is in: that is
    # what keeps them from touching each other (the board wraps around at the edges)
    place("pulsar", 2, 1)
    place("penta", 22, 6, turned=True)
    place("pulsar", 38, 1)
    place("penta", 57, 3)
    place("toad", 4, 21)
    place("beacon", 10, 25)
    place("blinker", 17, 21)
    place("block", 17, 27)
    place("beehive", 23, 21)
    place("boat", 28, 27)
    place("penta", 36, 22, turned=True)
    place("blinker", 52, 22)
    place("loaf", 56, 26)

    def step(b):
        n = sum(np.roll(np.roll(b, dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dx or dy)
        return ((n == 3) | ((b == 1) & (n == 2))).astype(np.uint8)

    generations = [board]
    for _ in range(frames_count):
        generations.append(step(generations[-1]))
    if not np.array_equal(generations[0], generations[frames_count]):
        raise SystemExit("life: the field is not back where it started after 30 generations")
    return generations[:frames_count]


def plasma():
    """The plasma of the old demos: waves that add up, drawn with an ordered dither."""
    frames_count, height = 24, 64
    out = []
    for t in range(frames_count):
        a = TAU * t / frames_count
        pic = blank(height)
        for y in range(height):
            for x in range(WIDTH):
                v = (
                    math.sin(x / 4.6 + a)
                    + math.sin(y / 5.7 - a)
                    + math.sin((x + y) / 7.3 + 2 * a)
                    + math.sin(math.hypot(x - 15.5, y - 32.0) / 4.2 - a)
                ) / 4.0
                # Stretched so there are solid areas and bare ones, not just a uniform grey
                if lit(0.5 + 1.15 * v, x, y, BAYER8):
                    put(pic, x, y)
        out.append(pic)
    return out


def spiral():
    """A spiral with three arms that turns, inside a ring."""
    frames_count, size, c = 16, 32, 15.5
    out = []
    for t in range(frames_count):
        pic = blank(size)
        for y in range(size):
            for x in range(size):
                r = math.hypot(x - c, y - c)
                if r > 14.6:
                    continue
                angle = math.atan2(y - c, x - c) / TAU
                phase = (3 * angle + r * 0.115 - t / frames_count) % 1.0
                if phase < 0.5:
                    put(pic, x, y)
        ring(pic, c, c, 15.0, 1, 0.45)
        disc(pic, c, c, 1.6, 0)
        out.append(pic)
    return out


def newton():
    """Newton's cradle: the ball on one side swings in, the one on the other side swings out and
    back, and the first one answers. Four frames for each quarter of the cycle, a step of more than
    a pixel each, so no two frames in a row are alike."""
    frames_count, size = 16, 32
    out = []
    string = 16.0
    reach = 5.0
    for t in range(frames_count):
        quarter, k = divmod(t, 4)
        shift = [0.0] * 5
        if quarter == 0:
            shift[0] = -reach * (1 - k / 4)
        elif quarter == 1:
            shift[4] = reach * (k / 4)
        elif quarter == 2:
            shift[4] = reach * (1 - k / 4)
        else:
            shift[0] = -reach * (k / 4)
        pic = blank(size)
        hline(pic, 0, 31, 3)
        hline(pic, 0, 31, 4)
        vline(pic, 0, 3, 29)
        vline(pic, 31, 3, 29)
        hline(pic, 0, 31, 29)
        hline(pic, 0, 31, 30)
        for i in range(5):
            x0 = 8 + 4 * i
            angle = math.asin(shift[i] / string)
            bx = x0 + string * math.sin(angle)
            by = 5.0 + string * math.cos(angle)
            cx, cy = int(round(bx)), int(round(by))
            line(pic, x0, 5, cx, cy - 1)
            # A ball of 3 x 3 pixels
            rect(pic, cx - 1, cy - 1, 3, 3, fill=True)
        out.append(pic)
    return out


def gear_mask(size, cx, cy, teeth, root, tip, turn, spokes_dots):
    """A gear as an array: a ring with square teeth, a hub and spokes (or dots), turned by `turn`."""
    mask = blank(size, size)
    for y in range(size):
        for x in range(size):
            dx, dy = x - cx, y - cy
            r = math.hypot(dx, dy)
            if r > tip + 0.6:
                continue
            phase = (teeth * (math.atan2(dy, dx) - turn) / TAU) % 1.0
            outer = tip if phase < 0.5 else root
            if root - 1.9 <= r <= outer + 0.3:
                mask[y, x] = 1
            if r <= 1.3:
                mask[y, x] = 1
    # Spokes
    for k in range(spokes_dots):
        a = turn + TAU * k / spokes_dots
        for r in np.arange(1.3, root - 1.5, 0.4):
            put(mask, int(round(cx + r * math.cos(a))), int(round(cy + r * math.sin(a))))
    return mask


def gears():
    """Two gears that mesh and turn."""
    frames_count, size = 12, 32
    teeth_a, teeth_b = 10, 7
    root_a, tip_a = 7.0, 9.0
    root_b, tip_b = 4.7, 6.7
    ca = (11.0, 11.0)
    distance = root_a + root_b + 1.0
    cb = (ca[0] + distance * math.cos(math.pi / 4), ca[1] + distance * math.sin(math.pi / 4))

    # Where the second gear starts so that the teeth of the two fit: the phase with the fewest
    # lit pixels shared at the point where they touch
    best = None
    for k in range(64):
        base_b = TAU * k / 64 / teeth_b
        a0 = gear_mask(size, *ca, teeth_a, root_a, tip_a, 0.0, 5)
        b0 = gear_mask(size, *cb, teeth_b, root_b, tip_b, base_b, 0)
        shared = int((a0 & b0).sum())
        if best is None or shared < best[0]:
            best = (shared, base_b)
    base_b = best[1]

    out = []
    for t in range(frames_count):
        # Two pitches of the first gear in a cycle: 72 degrees, and the second one turns the other
        # way by the same arc of its teeth
        turn_a = TAU * (2.0 / teeth_a) * t / frames_count
        turn_b = base_b - TAU * (2.0 / teeth_b) * t / frames_count
        pic = gear_mask(size, *ca, teeth_a, root_a, tip_a, turn_a, 5)
        pic |= gear_mask(size, *cb, teeth_b, root_b, tip_b, turn_b, 0)
        out.append(pic)
    return out


def hourglass():
    """An hourglass: the sand runs down through the neck and, at the end of every cycle, the glass
    turns over end to end (squeezed like a card that flips, so it never leaves the picture). The
    glass is the same upside down, so the last frame of the flip is the first frame again."""
    drain, flip = 16, 4
    height = 64
    cx, cy = 15.5, 31.5

    def half_width(d):
        if d < 2.0:
            return 1.0
        return 1.0 + 9.8 * ((d - 2.0) / 23.5) ** 0.7

    glass = blank(height)
    inside = np.zeros((height, WIDTH), dtype=bool)
    rect(glass, 3, 2, 26, 3, fill=True)
    rect(glass, 3, 59, 26, 3, fill=True)
    vline(glass, 3, 5, 58)
    vline(glass, 28, 5, 58)
    for y in range(5, 59):
        w = half_width(min(abs(y - cy), 25.5))
        for x in range(WIDTH):
            ax = abs(x - cx)
            if ax <= w - 0.5:
                inside[y, x] = True
            elif ax <= w + 0.5:
                glass[y, x] = 1

    def mound(x):
        return max(0.0, 1.0 - abs(x - cx) / 9.0)

    def state(q, k=0, stream=True):
        """The glass with the fraction q of the sand still in the upper bulb."""
        pic = glass.copy()
        p = 1.0 - q
        dip = 12.0 * q * (1.0 - q)
        heap = 12.0 * p * (1.0 - p)
        for y in range(5, 59):
            for x in range(WIDTH):
                if not inside[y, x]:
                    continue
                if y < 32:
                    if y >= 5.0 + 27.0 * (1.0 - q) + dip * mound(x):
                        pic[y, x] = 1
                elif y >= 59.0 - 27.0 * p - heap * mound(x):
                    pic[y, x] = 1
        if stream and 0.0 < q:
            floor = int(math.ceil(59.0 - 27.0 * p - heap * mound(15)))
            for y in range(28, min(floor, 59)):
                if 29 <= y <= 34 or (y + k) % 2 == 0:
                    put(pic, 15, y)
                if 29 <= y <= 34:
                    put(pic, 16, y)
        return pic

    out = [state(1.0 - k / drain, k) for k in range(drain)]
    end = state(0.0, stream=False)
    for j in range(1, flip + 1):
        c = math.cos(math.pi * j / (flip + 1))
        pic = blank(height)
        for y in range(height):
            src = int(round(cy + (y - cy) / c))
            if 0 <= src < height:
                pic[y] = end[src]
        out.append(pic)
    return out


def windmill():
    """A windmill whose sails turn (a quarter turn per cycle, since the four are alike) under
    clouds that drift across and come back around."""
    frames_count, height = 16, 64
    hub = (15.5, 24.0)
    sail_length, sail_width = 14.0, 3.6
    out = []

    def cloud(pic, x, y):
        disc(pic, x + 3, y + 3, 2.6)
        disc(pic, x + 7.5, y + 2, 3.3)
        disc(pic, x + 12, y + 3.2, 2.6)
        rect(pic, x + 3, y + 3, 10, 3, fill=True)

    def span(y):
        """The left and right edge of the roof and of the tower at row y."""
        if 19 <= y <= 28:
            half = 5.5 * (y - 19) / 9.0
            return 15.5 - half, 15.5 + half
        if 28 < y <= 58:
            grow = 5.0 * (y - 28) / 30.0
            return 10.5 - grow, 20.5 + grow
        return None

    for t in range(frames_count):
        pic = blank(height)
        for base_x, base_y in ((2, 1), (4, 44)):
            for wrap in (0, -32):
                cloud(pic, (base_x + 2 * t) % 32 + wrap, base_y)
        # The tower hides what is behind it
        for y in range(19, 59):
            edges = span(y)
            if edges:
                for x in range(int(edges[0]) - 1, int(edges[1]) + 2):
                    put(pic, x, y, 0)
        for y in range(19, 59):
            edges = span(y)
            if edges:
                put(pic, int(round(edges[0])), y)
                put(pic, int(round(edges[1])), y)
                if y in (36, 44, 52):
                    for x in range(int(round(edges[0])) + 1, int(round(edges[1])), 2):
                        put(pic, x, y)
        hline(pic, 10, 21, 28)
        rect(pic, 14, 33, 4, 4)
        rect(pic, 13, 50, 6, 9)
        # The sails
        base = math.pi / 8 + (TAU / 4) * t / frames_count
        for k in range(4):
            a = base + k * TAU / 4
            dx, dy = math.cos(a), math.sin(a)
            px, py = -dy, dx

            def at(r, s):
                return hub[0] + r * dx + s * px, hub[1] + r * dy + s * py

            line(pic, *at(2, 0), *at(sail_length, 0))
            line(pic, *at(sail_length, 0), *at(sail_length, sail_width))
            line(pic, *at(sail_length, sail_width), *at(5, sail_width))
            line(pic, *at(5, sail_width), *at(5, 0))
            for r in (8.5, 11.5):
                line(pic, *at(r, 0), *at(r, sail_width))
        disc(pic, *hub, 1.8)
        # The ground
        for x in range(WIDTH):
            top = 58 + int(round(1.5 * math.sin(x / 4.0)))
            put(pic, x, top)
            for y in range(top + 1, height):
                if lit(0.45, x, y):
                    put(pic, x, y)
        out.append(pic)
    return out


def hash01(n):
    """A repeatable number between 0 and 1 for n (no state, so frames can be drawn in any order)."""
    return (math.sin(n * 12.9898 + 4.1414) * 43758.5453) % 1.0


def fireworks():
    """Rockets that rise and burst into sparks that fall; three bursts take turns, so there is
    always something going off."""
    frames_count, height = 24, 64
    # Each burst: where it goes off, the frame its rocket takes off, and how far the sparks reach
    bursts = [(11, 17, 0, 13.0), (21, 29, 8, 12.0), (13, 43, 16, 10.0)]
    heights = [6, 9, 5, 8, 4, 7, 9, 5]
    out = []

    def reach_at(reach, rho):
        return reach * (1.0 - (1.0 - rho / 12.0) ** 2)

    for t in range(frames_count):
        pic = blank(height)
        for index, (bx, by, start, reach) in enumerate(bursts):
            tau = (t - start) % frames_count
            if tau < 8:
                y = int(round(62.0 - (62.0 - by) * min(1.0, tau / 7.0)))
                for trail in (0, 2, 4):
                    put(pic, bx, y + trail)
                continue
            rho = tau - 8
            if rho > 11:
                continue
            if rho == 0:
                disc(pic, bx, by, 2.0)
            for ring_index, (count, scale, twist) in enumerate(((20, 1.0, 0.0), (12, 0.55, 0.4))):
                for i in range(count):
                    seed = index * 100 + ring_index * 40 + i
                    a = TAU * (i + twist) / count + 0.25 * (hash01(seed) - 0.5)
                    f = scale * (0.8 + 0.35 * hash01(seed + 500))
                    # The sparks go out one by one near the end
                    if rho >= 9 and (i + rho) % 2:
                        continue
                    if rho >= 6 and (i + rho) % 3 == 0:
                        continue
                    for step in ((0, 1) if 0 < rho < 5 else (0,)):
                        r = reach_at(reach, rho - step) * f
                        x = bx + r * math.cos(a)
                        y = by + r * math.sin(a) * 0.9 + 0.06 * (rho - step) ** 2
                        put(pic, int(round(x)), int(round(y)))
        # The town in the dark, along the bottom
        for column, h in enumerate(heights):
            x0 = column * 4
            hline(pic, x0, x0 + 3, height - h)
            for x in range(x0, x0 + 4):
                for y in range(height - h + 1, height):
                    if lit(0.5, x, y):
                        put(pic, x, y)
        out.append(pic)
    return out


def ufo():
    """A flying saucer that hovers over a field and lifts a cow in its beam, then puts it back."""
    frames_count, height = 16, 64
    cx = 15.5
    stars = [(3, 4), (27, 6), (8, 12), (23, 15), (4, 25), (28, 30), (6, 40), (26, 46), (29, 55), (2, 52)]
    out = []
    for t in range(frames_count):
        phase = TAU * t / frames_count
        pic = blank(height)
        for i, (x, y) in enumerate(stars):
            if (t + i) % 4 < 3:
                put(pic, x, y)
        y0 = 17 + int(round(math.sin(phase)))
        # The beam: a cone of dots that run up towards the saucer
        for y in range(y0 + 3, 58):
            half = 4.0 + (y - y0 - 3) * 0.17
            for x in range(int(cx - half - 1), int(cx + half + 2)):
                if abs(x - cx) <= half and lit(0.38, x, y + t // 2):
                    put(pic, x, y)
        line(pic, cx - 4.5, y0 + 3, cx - 11.5, 58, dotted=True)
        line(pic, cx + 4.5, y0 + 3, cx + 11.5, 58, dotted=True)
        # The cow, 0 on the ground and 1 at the top of the beam
        lift = 0.5 - 0.5 * math.cos(phase)
        cow_y = int(round(53 - 22 * lift))
        cow_x = 11 + int(round(math.sin(phase * 3)))
        rect(pic, cow_x - 1, cow_y - 2, 12, 9, fill=True, value=0)
        rect(pic, cow_x + 1, cow_y + 1, 6, 3, fill=True)
        rect(pic, cow_x + 7, cow_y, 3, 3, fill=True)
        put(pic, cow_x + 9, cow_y - 1)
        vline(pic, cow_x, cow_y + 1, cow_y + 2)
        for leg in (1, 3, 5, 6):
            vline(pic, cow_x + leg, cow_y + 4, cow_y + 5)
        put(pic, cow_x + 3, cow_y + 2, 0)
        put(pic, cow_x + 5, cow_y + 1, 0)
        # The saucer: a dome with its little pilot over a flat body with lights that blink
        for y in range(y0 - 4, y0 + 5):
            for x in range(WIDTH):
                if ((x - cx) / 13.2) ** 2 + ((y - y0) / 3.4) ** 2 <= 1.0:
                    put(pic, x, y)
        for y in range(y0 - 8, y0 - 2):
            for x in range(WIDTH):
                e = ((x - cx) / 6.2) ** 2 + ((y - (y0 - 2)) / 5.6) ** 2
                if 0.55 <= e <= 1.0:
                    put(pic, x, y)
        rect(pic, 14, y0 - 5, 3, 2, fill=True)
        for i, x in enumerate((6, 11, 16, 20, 25)):
            if (i + t) % 2:
                put(pic, x, y0, 0)
        # The ground
        hline(pic, 0, 31, 58)
        for x in range(WIDTH):
            for y in range(59, height):
                if lit(0.4, x, y):
                    put(pic, x, y)
        out.append(pic)
    return out


def eye():
    """An eye that looks around in a figure of eight and blinks once per cycle."""
    frames_count, size = 24, 32
    cx, cy, rx, hmax = 15.5, 16.0, 14.5, 10.0
    out = []
    for t in range(frames_count):
        phase = TAU * t / frames_count
        gx, gy = 5.0 * math.sin(phase), 2.5 * math.sin(2 * phase)
        openness = {11: 0.55, 12: 0.1, 13: 0.45}.get(t, 1.0)
        heights = []
        for x in range(size):
            s = 1.0 - ((x - cx) / rx) ** 2
            heights.append(hmax * openness * s if s > 0 else -1.0)
        pic = blank(size)
        ups, downs = [], []
        for x in range(size):
            if heights[x] < 0:
                ups.append(None)
                downs.append(None)
                continue
            ups.append(int(round(cy - heights[x])))
            downs.append(int(round(cy + heights[x])))
        for x in range(size):
            if ups[x] is None:
                continue
            put(pic, x, ups[x])
            put(pic, x, downs[x])
            if x > 0 and ups[x - 1] is not None:
                vline(pic, x, ups[x - 1], ups[x])
                vline(pic, x, downs[x - 1], downs[x])
        if openness > 0.9:
            for x in (4, 9, 15, 21, 26):
                step = -1 if x < 15 else 1
                line(pic, x, ups[x], x + step * 2, ups[x] - 3)
        # The iris and the pupil, only where the eyelids are open
        ix, iy = cx + gx, cy + gy
        inside = blank(size)
        for x in range(size):
            if heights[x] < 0:
                continue
            for y in range(size):
                if abs(y - cy) < heights[x] - 0.4:
                    inside[y, x] = 1
        for y in range(size):
            for x in range(size):
                if not inside[y, x]:
                    continue
                d = math.hypot(x - ix, y - iy)
                if abs(d - 6.3) <= 0.6 or d <= 3.0:
                    pic[y, x] = 1
        for dx, dy in ((-1, -1), (0, -1)):
            gx_, gy_ = int(round(ix)) - 1 + dx, int(round(iy)) - 1 + dy
            if 0 <= gx_ < size and 0 <= gy_ < size and inside[gy_, gx_]:
                pic[gy_, gx_] = 0
        out.append(pic)
    return out


def keywave():
    """A wave of key presses that sweeps across a field of keycaps."""
    frames_count, height = 24, 64
    cols, rows, pitch = 5, 10, 6
    out = []
    for t in range(frames_count):
        pic = blank(height)
        for r in range(rows):
            for c in range(cols):
                x, y = 1 + c * pitch, 2 + r * pitch
                u = (t - 1.6 * (r + c)) % frames_count
                if u < 2.4:
                    rect(pic, x, y, 5, 5, fill=True)
                else:
                    rect(pic, x, y, 5, 5)
                    if u < 4.8:
                        # Half way down: the outline with a dot in the middle
                        put(pic, x + 2, y + 2)
                for cx_, cy_ in ((x, y), (x + 4, y), (x, y + 4), (x + 4, y + 4)):
                    put(pic, cx_, cy_, 0)
        out.append(pic)
    return out


# name -> (function, milliseconds of one cycle)
ANIMATIONS = {
    "waterfall": (waterfall, 1600),
    "lava": (lava, 3200),
    "lightning": (lightning, 1600),
    "snow": (snow, 2400),
    "jellyfish": (jellyfish, 1600),
    "tetris": (tetris, 2000),
    "pong": (pong, 1500),
    "invaders": (invaders, 1600),
    "pacman": (pacman, 1600),
    "life": (life, 3000),
    "plasma": (plasma, 2400),
    "spiral": (spiral, 1600),
    "newton": (newton, 1600),
    "gears": (gears, 1000),
    "hourglass": (hourglass, 2000),
    "windmill": (windmill, 1600),
    "fireworks": (fireworks, 2400),
    "ufo": (ufo, 1600),
    "eye": (eye, 2400),
    "keywave": (keywave, 2400),
}
