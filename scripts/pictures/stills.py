"""The still images of make_pictures.py: each function returns one upright picture, 32 pixels wide."""
import math

from pixels import (
    WIDTH,
    Rng,
    blank,
    disc,
    hline,
    line,
    put,
    rect,
    ring,
    text,
    vline,
)

TAU = 2 * math.pi


def mountains():
    """A night sky with a moon, and three ridges of mountains."""
    height = 128
    pic = blank(height)
    rng = Rng(21)

    # The stars
    for _ in range(26):
        x, y = rng.integers(0, WIDTH), rng.integers(0, 72)
        if math.hypot(x - 22, y - 20) < 12:
            continue
        put(pic, x, y)
        if rng.random() < 0.18:
            put(pic, x - 1, y)
            put(pic, x + 1, y)
            put(pic, x, y - 1)
            put(pic, x, y + 1)

    # The moon: a crescent
    for y in range(8, 34):
        for x in range(10, 32):
            if math.hypot(x - 22, y - 20) <= 8.4 and math.hypot(x - 25.5, y - 18) > 7.2:
                put(pic, x, y)

    def ridge(base, peaks, slope):
        """The line of a range: the highest of the cones (centre, height) at every column."""
        return [base - max(max(0.0, h - abs(x - c) * slope) for c, h in peaks) for x in range(WIDTH)]

    far = ridge(84, [(5, 13), (19, 19), (33, 12)], 0.9)
    mid = ridge(100, [(-2, 14), (12, 24), (27, 17)], 1.05)
    near = ridge(120, [(7, 24), (24, 31)], 1.15)

    # The far range: the line only
    for x in range(WIDTH):
        if x:
            line(pic, x - 1, int(round(far[x - 1])), x, int(round(far[x])))

    # The middle range: the line, and horizontal strokes below it
    for x in range(WIDTH):
        y = int(round(mid[x]))
        for yy in range(y, height):
            pic[yy, x] = 0
        if x:
            line(pic, x - 1, int(round(mid[x - 1])), x, y)
        for yy in range(y + 3, height - 4, 3):
            put(pic, x, yy)

    # The near range: the line, and a checker below it, that hides what is behind
    for x in range(WIDTH):
        y = int(round(near[x]))
        for yy in range(y, height):
            pic[yy, x] = 0
        for yy in range(y + 1, height):
            if (x + yy) % 2 == 0:
                put(pic, x, yy)
        if x:
            line(pic, x - 1, int(round(near[x - 1])), x, y)

    # Snow on the two peaks of the near range: a lit cap with the line of the peak
    for c, h in ((7, 24), (24, 31)):
        top = int(round(120 - h))
        for dy in range(0, 5):
            for dx in range(-(dy + 1), dy + 2):
                put(pic, c + dx, top + dy)
    return pic


def skyline():
    """A city at night: the windows that are lit, and a few stars."""
    height = 128
    pic = blank(height)
    rng = Rng(8)

    for _ in range(18):
        put(pic, rng.integers(0, WIDTH), rng.integers(0, 50))
    disc(pic, 24, 14, 4.5)
    disc(pic, 22, 12, 4.2, 0)

    x = 0
    blocks = []
    while x < WIDTH:
        w = rng.integers(5, 9)
        w = min(w, WIDTH - x)
        blocks.append((x, w, rng.integers(24, 78)))
        x += w
    # An antenna on the highest one
    tallest = max(blocks, key=lambda b: b[2])

    for bx, bw, bh in blocks:
        top = height - 2 - bh
        rect(pic, bx, top, bw, bh, fill=False)
        for wy in range(top + 3, height - 5, 4):
            for wx in range(bx + 2, bx + bw - 2, 2):
                if rng.random() < 0.55:
                    put(pic, wx, wy)
        if (bx, bw, bh) == tallest:
            mid = bx + bw // 2
            vline(pic, mid, top - 8, top - 1)
            put(pic, mid, top - 9)
            hline(pic, mid - 1, mid + 1, top - 5)

    hline(pic, 0, WIDTH - 1, height - 1)
    return pic


def circuit():
    """The tracks of a circuit board, with a chip."""
    height = 128
    pic = blank(height)

    # The chip, with the pins on both sides and a notch
    rect(pic, 9, 50, 14, 24)
    for y in range(53, 72, 4):
        hline(pic, 5, 8, y)
        hline(pic, 24, 27, y)
    for y in range(51, 54):
        for x in range(12, 21):
            if abs(math.hypot(x - 16, y - 50) - 2.6) <= 0.5:
                put(pic, x, y)
    pic[50, 14:19] = 0
    put(pic, 11, 53)
    text(pic, 11, 60, "ZMK")

    def pad(x, y):
        ring(pic, x, y, 1.5)
        put(pic, x, y, 0)

    def track(points):
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            line(pic, x0, y0, x1, y1)

    # Tracks above the chip
    track([(5, 53), (2, 53), (2, 38), (6, 34), (6, 20), (10, 16), (10, 4)])
    track([(5, 57), (3, 57), (3, 40), (13, 30), (13, 22), (18, 17), (18, 2)])
    track([(5, 61), (4, 61), (4, 41), (24, 21), (24, 8)])
    track([(27, 53), (29, 53), (29, 36), (22, 29), (22, 18), (28, 12), (28, 2)])
    track([(27, 57), (30, 57), (30, 31)])
    # Tracks below the chip
    track([(5, 65), (2, 65), (2, 86), (8, 92), (8, 106), (12, 110), (12, 124)])
    track([(5, 69), (3, 69), (3, 88), (14, 99), (14, 120)])
    track([(27, 61), (30, 61), (30, 84), (24, 90), (24, 104), (20, 108), (20, 124)])
    track([(27, 65), (29, 65), (29, 80), (17, 92), (17, 104)])
    track([(27, 69), (31, 69), (31, 96), (28, 99), (28, 124)])

    for x, y in ((10, 4), (18, 2), (24, 8), (28, 2), (30, 31), (12, 124), (14, 120), (20, 124), (17, 104), (28, 124)):
        pad(x, y)
    for x, y in ((2, 38), (13, 30), (22, 29), (8, 92), (24, 90)):
        put(pic, x, y)
        put(pic, x + 1, y)
        put(pic, x, y + 1)
        put(pic, x + 1, y + 1)
    return pic


def keyboard():
    """The two halves of a Corne, as seen from above."""
    height = 64
    pic = blank(height)
    offsets = [3, 3, 1, 0, 1, 2]

    def half(top, mirrored, pressed):
        keys = []
        for c in range(6):
            x = 1 + 5 * (5 - c if mirrored else c)
            for r in range(3):
                keys.append((x, top + offsets[c] + 5 * r))
        for i in range(3):
            x = 1 + 5 * (2 - i if mirrored else 3 + i)
            keys.append((x, top + 19 + (0 if i == 1 else 1)))
        for n, (x, y) in enumerate(keys):
            rect(pic, x, y, 4, 4)
            if n in pressed:
                rect(pic, x + 1, y + 1, 2, 2, fill=True)

    half(2, False, {2, 4, 9, 13})
    half(40, True, {1, 6, 10, 16})
    # The name, between the two halves
    text(pic, 4, 29, "CORNE")
    hline(pic, 3, 28, 27)
    hline(pic, 3, 28, 35)
    return pic


# None is a still image that was taken out (a retired kind): its place in the list stays reserved,
# so that the kinds of the pictures after it do not move. See make_pictures.py.
STILLS = {
    "mountains": mountains,
    "skyline": skyline,
    "circuit": circuit,
    "alien": None,
    "heart": None,
    "keyboard": keyboard,
    "pulsar": None,
    "rocket": None,
}
