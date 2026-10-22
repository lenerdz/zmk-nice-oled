"""Small drawing helpers for the pictures of make_pictures.py.

A picture is an array of rows: pic[y][x] is 1 for a lit pixel (what the OLED shows lit is the
ink of the shield, a set bit of the LVGL image). Pictures are upright, as the screen is looked at,
and 32 pixels wide, the width of the panel of the Corne.
"""
import math

import numpy as np

WIDTH = 32

def _bayer(n):
    """The ordered dither matrix of n x n cells (n a power of two), values 0 to n * n - 1."""
    if n == 1:
        return np.array([[0]])
    m = _bayer(n // 2)
    return np.block([[4 * m, 4 * m + 2], [4 * m + 3, 4 * m + 1]])


# Ordered dither: a value from 0 to 1 is lit where it is above the threshold of the cell
BAYER4 = (_bayer(4) + 0.5) / 16.0
BAYER8 = (_bayer(8) + 0.5) / 64.0


class Rng:
    """A small generator of numbers (xorshift32), so that the pictures are the same whatever the
    version of numpy: the same seed always gives the same pictures."""

    def __init__(self, seed):
        self.state = ((seed * 2654435761) ^ 0x9E3779B9) & 0xFFFFFFFF or 1
        for _ in range(4):
            self._next()

    def _next(self):
        x = self.state
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= x >> 17
        x ^= (x << 5) & 0xFFFFFFFF
        self.state = x
        return x

    def random(self):
        """A number from 0 up to, and not including, 1."""
        return self._next() / 4294967296.0

    def integers(self, low, high=None):
        """A whole number from low up to, and not including, high."""
        if high is None:
            low, high = 0, low
        return low + int(self.random() * (high - low))


def blank(height, width=WIDTH):
    return np.zeros((height, width), dtype=np.uint8)


def put(pic, x, y, value=1):
    if 0 <= x < pic.shape[1] and 0 <= y < pic.shape[0]:
        pic[y, x] = value


def hline(pic, x0, x1, y, value=1):
    for x in range(min(x0, x1), max(x0, x1) + 1):
        put(pic, x, y, value)


def vline(pic, x, y0, y1, value=1):
    for y in range(min(y0, y1), max(y0, y1) + 1):
        put(pic, x, y, value)


def line(pic, x0, y0, x1, y1, value=1, dotted=False):
    """Bresenham; a dotted line lights every other pixel."""
    x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    step = 0
    while True:
        if not dotted or step % 2 == 0:
            put(pic, x0, y0, value)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
        step += 1


def rect(pic, x, y, w, h, fill=False, value=1):
    if fill:
        for yy in range(y, y + h):
            hline(pic, x, x + w - 1, yy, value)
    else:
        hline(pic, x, x + w - 1, y, value)
        hline(pic, x, x + w - 1, y + h - 1, value)
        vline(pic, x, y, y + h - 1, value)
        vline(pic, x + w - 1, y, y + h - 1, value)


def disc(pic, cx, cy, r, value=1):
    """A filled circle; the centre may be between two pixels (15.5)."""
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + 0.25:
                put(pic, x, y, value)


def ring(pic, cx, cy, r, value=1, thickness=0.5):
    for y in range(int(cy - r - 2), int(cy + r + 3)):
        for x in range(int(cx - r - 2), int(cx + r + 3)):
            if abs(math.hypot(x - cx, y - cy) - r) <= thickness:
                put(pic, x, y, value)


def lit(density, x, y, matrix=BAYER4):
    """Whether the pixel of an area with this density (0 to 1) is lit: ordered dither."""
    return density > matrix[y % matrix.shape[0], x % matrix.shape[1]]


def fill_dither(pic, x0, y0, x1, y1, density, matrix=BAYER4):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if lit(density, x, y, matrix):
                put(pic, x, y)


# A font of 3 x 5 pixels for the few letters the pictures write
FONT3X5 = {
    "A": ["010", "101", "111", "101", "101"],
    "B": ["110", "101", "110", "101", "110"],
    "C": ["011", "100", "100", "100", "011"],
    "D": ["110", "101", "101", "101", "110"],
    "E": ["111", "100", "110", "100", "111"],
    "F": ["111", "100", "110", "100", "100"],
    "G": ["011", "100", "101", "101", "011"],
    "H": ["101", "101", "111", "101", "101"],
    "I": ["111", "010", "010", "010", "111"],
    "K": ["101", "101", "110", "101", "101"],
    "L": ["100", "100", "100", "100", "111"],
    "M": ["101", "111", "111", "101", "101"],
    "N": ["110", "101", "101", "101", "101"],
    "O": ["010", "101", "101", "101", "010"],
    "P": ["110", "101", "110", "100", "100"],
    "R": ["110", "101", "110", "101", "101"],
    "S": ["011", "100", "010", "001", "110"],
    "T": ["111", "010", "010", "010", "010"],
    "U": ["101", "101", "101", "101", "111"],
    "V": ["101", "101", "101", "101", "010"],
    "W": ["101", "101", "111", "111", "101"],
    "X": ["101", "101", "010", "101", "101"],
    "Y": ["101", "101", "010", "010", "010"],
    "Z": ["111", "001", "010", "100", "111"],
    "0": ["111", "101", "101", "101", "111"],
    "1": ["010", "110", "010", "010", "111"],
    "2": ["110", "001", "010", "100", "111"],
    "3": ["110", "001", "010", "001", "110"],
    "4": ["101", "101", "111", "001", "001"],
    "5": ["111", "100", "110", "001", "110"],
    "6": ["011", "100", "111", "101", "111"],
    "7": ["111", "001", "010", "010", "010"],
    "8": ["111", "101", "111", "101", "111"],
    "9": ["111", "101", "111", "001", "110"],
    " ": ["000"] * 5,
}


def text(pic, x, y, string, spacing=1):
    for ch in string:
        glyph = FONT3X5.get(ch.upper(), FONT3X5[" "])
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                if bit == "1":
                    put(pic, x + col, y + row)
        x += 3 + spacing
    return x


def sprite(pic, x, y, rows, scale=1, value=1):
    """Draws a sprite given as strings ('#' lit), each pixel scale x scale."""
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == "#":
                for dy in range(scale):
                    for dx in range(scale):
                        put(pic, x + i * scale + dx, y + j * scale + dy, value)
            elif ch == "." or ch == " ":
                pass
