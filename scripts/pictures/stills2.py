"""The still images of the second batch of make_pictures.py: each function returns one upright
picture, 32 pixels wide. They are added after the first batch (stills.py), so the kinds of the
pictures that exist do not change."""
import math

import numpy as np

from pixels import (
    WIDTH,
    Rng,
    blank,
    disc,
    hline,
    lit,
    put,
    ring,
    vline,
)

TAU = 2 * math.pi


def edge_of(mask):
    """The pixels of a shape (an array of booleans) that touch the outside."""
    padded = np.pad(mask, 1)
    inner = (
        padded[1:-1, 1:-1]
        & padded[:-2, 1:-1]
        & padded[2:, 1:-1]
        & padded[1:-1, :-2]
        & padded[1:-1, 2:]
    )
    return mask & ~inner


def shape(height):
    return np.zeros((height, WIDTH), dtype=bool)


def moon_cat():
    """A cat sitting on a wall in front of the full moon, seen from behind (not called cat: that
    is the name of a kind of zmk-nice-oled)."""
    height = 64
    pic = blank(height)
    rng = Rng(5)
    for _ in range(9):
        put(pic, rng.integers(0, WIDTH), rng.integers(0, 8))
    disc(pic, 16, 25, 13.2)

    mask = shape(height)

    def add_disc(cx, cy, r):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                if 0 <= x < WIDTH and 0 <= y < height and math.hypot(x - cx, y - cy) <= r:
                    mask[y, x] = True

    def add_triangle(p0, p1, p2):
        (x0, y0), (x1, y1), (x2, y2) = p0, p1, p2
        for y in range(int(min(y0, y1, y2)), int(max(y0, y1, y2)) + 1):
            for x in range(WIDTH):
                d0 = (x - x1) * (y0 - y1) - (x0 - x1) * (y - y1)
                d1 = (x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)
                d2 = (x - x0) * (y2 - y0) - (x2 - x0) * (y - y0)
                if (d0 >= 0 and d1 >= 0 and d2 >= 0) or (d0 <= 0 and d1 <= 0 and d2 <= 0):
                    mask[y, x] = True

    add_disc(16, 30, 4.9)
    add_triangle((11.0, 29), (11.2, 21), (15.2, 26))
    add_triangle((21.0, 29), (20.8, 21), (16.8, 26))
    for y in range(33, 53):
        hw = 4.0 + (y - 33) * 0.2 + (1.2 if y > 45 else 0.0)
        for x in range(int(16 - hw), int(16 + hw) + 1):
            mask[y, x] = True
    for k in range(0, 40):
        t = k / 39.0
        add_disc(22.0 + 6.5 * math.sin(t * 1.9), 51 - 15 * t, 1.5)
    # A dark cat with a lit outline
    pic[mask] = 0
    pic[edge_of(mask)] = 1

    # The wall
    hline(pic, 0, WIDTH - 1, 52)
    hline(pic, 0, WIDTH - 1, 63)
    for y, off in ((56, 0), (60, 4)):
        hline(pic, 0, WIDTH - 1, y)
        for x in range(off, WIDTH, 8):
            vline(pic, x, y - 3 if y == 60 else y - 3, y)
    for x in range(2, WIDTH, 8):
        vline(pic, x, 61, 62)
    return pic


def planet():
    """A ringed planet with a small moon, among the stars."""
    height = 64
    pic = blank(height)
    rng = Rng(77)
    for _ in range(20):
        x, y = rng.integers(0, WIDTH), rng.integers(0, height)
        if math.hypot(x - 16, y - 33) < 19:
            continue
        put(pic, x, y)
    cx, cy, r = 16.0, 33.0, 9.5
    # The globe: bands, darker towards the side that is in the shade
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            if math.hypot(x - cx, y - cy) > r:
                continue
            band = int((y - (cy - r)) // 3) % 3
            density = (0.85, 0.5, 0.68)[band] - 0.55 * max(0.0, (x - cx) / r)
            if lit(density, x, y):
                put(pic, x, y)
    ring(pic, cx, cy, r, thickness=0.5)
    # The rings, tilted: the far half goes behind the globe, the near half in front of it
    tilt = -0.36
    for a, b in ((17.5, 4.4), (14.0, 3.4)):
        for i in range(1600):
            th = TAU * i / 1600
            ex, ey = a * math.cos(th), b * math.sin(th)
            x = cx + ex * math.cos(tilt) - ey * math.sin(tilt)
            y = cy + ex * math.sin(tilt) + ey * math.cos(tilt)
            inside = math.hypot(x - cx, y - cy) < r + 0.8
            near = math.sin(th) > 0
            if inside and not near:
                continue
            px, py = int(round(x)), int(round(y))
            if inside:
                put(pic, px, py - 1, 0)
                put(pic, px, py + 1, 0)
            put(pic, px, py)
    # A small moon
    disc(pic, 27, 9, 2.4)
    put(pic, 26, 8, 0)
    return pic


# None is a still image that was taken out (a retired kind): its place in the list stays reserved,
# so that the kinds of the pictures after it do not move. See make_pictures.py.
STILLS = {
    "coffee": None,
    "cactus": None,
    "lighthouse": None,
    "moon_cat": moon_cat,
    "robot": None,
    "planet": planet,
    "castle": None,
    "tree": None,
    "skull": None,
    "sword": None,
    "key": None,
    "antenna": None,
    "potion": None,
    "sailboat": None,
    "compass": None,
    "crown": None,
    "cassette": None,
    "floppy": None,
    "phases": None,
    "mushroom": None,
}
