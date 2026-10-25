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


def ellipse(pic, cx, cy, rx, ry, fill=False, value=1):
    """An ellipse, as a one-pixel outline or filled."""
    mask = shape(pic.shape[0])
    for y in range(max(0, int(cy - ry - 2)), min(pic.shape[0], int(cy + ry + 3))):
        for x in range(max(0, int(cx - rx - 2)), min(WIDTH, int(cx + rx + 3))):
            if math.hypot((x - cx) / rx, (y - cy) / ry) <= 1.0:
                mask[y, x] = True
    pic[mask if fill else edge_of(mask)] = value


def coffee():
    """A cup of coffee with steam, on its saucer."""
    height = 64
    pic = blank(height)
    cx = 15.5

    # The steam: three wisps that wave, and fade into dots as they go up
    for x0, phase, top in ((10.0, 0.0, 9), (16.0, 1.7, 4), (22.0, 3.3, 11)):
        for y in range(top, 29):
            if y < top + 6 and y % 2:
                continue
            put(pic, int(round(x0 + 2.0 * math.sin(y / 2.6 + phase))), y)

    # The handle goes first: the cup hides the half that is inside it
    ring(pic, 26, 41, 3.6, thickness=0.6)

    def half_width(y):
        return 9.5 - (y - 33) * 3.5 / 19.0

    for y in range(34, 54):
        hw = half_width(y)
        for x in range(int(cx - hw), int(cx + hw) + 2):
            put(pic, x, y, 0)
    # The rim and the coffee in it
    ellipse(pic, cx, 33, 9.5, 2.4)
    for y in range(31, 36):
        for x in range(WIDTH):
            e = math.hypot((x - cx) / 8.3, (y - 33) / 1.6)
            if e <= 1.0 and lit(0.55, x, y):
                put(pic, x, y)
    # The sides and the bottom of the cup
    for y in range(34, 53):
        hw = half_width(y)
        put(pic, int(round(cx - hw)), y)
        put(pic, int(round(cx + hw - 1)), y)
    hline(pic, 9, 22, 52)
    hline(pic, 10, 21, 53)
    # Two bands and the name
    for x in range(8, 24, 2):
        put(pic, x, 37)
        put(pic, x, 49)
    text(pic, 10, 41, "ZMK")
    # The saucer
    ellipse(pic, cx, 55.5, 13.5, 2.6)
    ellipse(pic, cx, 55.5, 8.0, 1.2)
    hline(pic, 10, 21, 59)
    return pic


def cactus():
    """A saguaro cactus in the desert, with the sun low over the dunes."""
    height = 64
    pic = blank(height)

    # The sun: a disc with rays
    disc(pic, 24, 10, 4.3)
    for k in range(8):
        a = k * TAU / 8
        line(pic, 24 + 6.6 * math.cos(a), 10 + 6.6 * math.sin(a), 24 + 9.2 * math.cos(a), 10 + 9.2 * math.sin(a))

    # The dunes behind: a line, and a nearer one with horizontal strokes
    for x in range(WIDTH):
        far = 47 + int(round(2.0 * math.sin(x / 6.0 + 1.0)))
        put(pic, x, far)

    mask = shape(height)

    def block(x0, y0, x1, y1):
        mask[y0 : y1 + 1, x0 : x1 + 1] = True

    block(12, 27, 18, 57)
    block(13, 25, 17, 26)
    block(14, 24, 16, 24)
    # The left arm: it comes out sideways and goes up
    block(6, 38, 12, 42)
    block(5, 30, 9, 37)
    block(6, 28, 8, 29)
    # The right arm
    block(18, 33, 24, 37)
    block(22, 24, 26, 32)
    block(23, 22, 25, 23)
    pic[mask] = 0
    pic[edge_of(mask)] = 1
    # The ribs of the trunk and of the arms, in dashes
    for y in range(28, 56):
        if y % 4 != 3:
            put(pic, 15, y)
    for y in range(31, 37):
        if y % 4 != 3:
            put(pic, 7, y)
    for y in range(25, 32):
        if y % 4 != 3:
            put(pic, 24, y)
    # The spines
    for x, y in ((10, 30), (4, 33), (11, 46), (20, 29), (27, 28), (10, 52), (21, 42), (26, 34)):
        put(pic, x, y)

    # The ground
    for x in range(WIDTH):
        top = 57 + int(round(1.4 * math.sin(x / 4.5)))
        for y in range(top, height):
            pic[y, x] = 0
        put(pic, x, top)
        if x % 2 == 0:
            put(pic, x, top + 3)
        if x % 3 == 1:
            put(pic, x, top + 5)
    # A stone
    for x, y in ((3, 58), (4, 58), (5, 58), (4, 57)):
        put(pic, x, y)
    return pic


def lighthouse():
    """A lighthouse on its rock, sweeping the night with its beam."""
    height = 128
    pic = blank(height)
    rng = Rng(61)
    cx = 15.5

    # Stars, and the moon
    for _ in range(16):
        x, y = rng.integers(0, WIDTH), rng.integers(0, 26)
        if math.hypot(x - 25, y - 9) < 9:
            continue
        put(pic, x, y)
    for y in range(2, 18):
        for x in range(16, 32):
            if math.hypot(x - 25, y - 9) <= 6.2 and math.hypot(x - 27.6, y - 7.6) > 5.4:
                put(pic, x, y)

    # The beams: wedges of dots on both sides of the lantern
    for side in (-1, 1):
        for x in range(1, 12):
            reach = x * 0.62
            for y in range(int(41 - reach), int(41 + reach) + 1):
                px = int(round(cx + side * (4.5 + x)))
                if 0 <= px < WIDTH and abs(y - 41) <= reach and lit(0.28, px, y):
                    put(pic, px, y)
        line(pic, cx + side * 5, 41, cx + side * 16, 34, dotted=True)
        line(pic, cx + side * 5, 41, cx + side * 16, 48, dotted=True)

    # The lantern: a roof, the glass with the light in it, the gallery
    for dy in range(0, 8):
        half = 1 + dy * 0.9
        hline(pic, int(round(cx - half)), int(round(cx + half)), 31 + dy)
    disc(pic, cx, 29.5, 1.2)
    rect(pic, 11, 39, 10, 6)
    disc(pic, cx, 42, 2.2)
    rect(pic, 8, 45, 16, 2, fill=True)

    # The tower: a cone with bands that are solid and bands that are open
    for y in range(47, 109):
        hw = 5.0 + (y - 47) * 4.0 / 61.0
        left, right = int(round(cx - hw)), int(round(cx + hw - 1))
        band = (y - 47) // 9
        for x in range(left, right + 1):
            if band % 2 == 0 and lit(0.8, x, y):
                put(pic, x, y)
        put(pic, left, y)
        put(pic, right, y)
        if (y - 47) % 9 == 0:
            hline(pic, left, right, y)
    # Windows and the door
    for y in (56, 74, 92):
        rect(pic, 14, y, 4, 4, fill=True, value=0)
        rect(pic, 14, y, 4, 4)
    rect(pic, 13, 99, 6, 10, fill=True, value=0)
    rect(pic, 13, 99, 6, 10)
    put(pic, 17, 104)

    # The rock
    for y in range(108, 124):
        hw = 7.0 + (y - 108) * 0.85 + 1.5 * math.sin(y * 1.3)
        for x in range(int(cx - hw), int(cx + hw) + 1):
            if 0 <= x < WIDTH:
                pic[y, x] = 0
        put(pic, int(round(cx - hw)), y)
        put(pic, int(round(cx + hw)), y)
        for x in range(int(cx - hw) + 1, int(cx + hw)):
            if 0 <= x < WIDTH and lit(0.45, x, y):
                put(pic, x, y)
    # The sea
    for k, base in enumerate((114, 119, 124)):
        for x in range(WIDTH):
            y = base + int(round(1.2 * math.sin(x / 2.4 + k * 1.7)))
            if abs(x - cx) > 7.0 + (base - 108) * 0.85 + 2 and (x + k) % 3:
                put(pic, x, y)
    hline(pic, 0, WIDTH - 1, 127)
    return pic


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


def robot():
    """A friendly robot with an antenna."""
    height = 64
    pic = blank(height)
    # The antenna
    vline(pic, 15, 4, 9)
    vline(pic, 16, 4, 9)
    disc(pic, 15.5, 3.2, 2.2)
    # The head, with the ears
    rect(pic, 8, 10, 16, 13)
    rect(pic, 5, 14, 3, 6, fill=True)
    rect(pic, 24, 14, 3, 6, fill=True)
    rect(pic, 11, 14, 4, 4, fill=True)
    rect(pic, 17, 14, 4, 4, fill=True)
    put(pic, 12, 15, 0)
    put(pic, 18, 15, 0)
    for x in range(11, 21, 2):
        put(pic, x, 20)
    # The neck
    rect(pic, 13, 23, 6, 3)
    # The body, with a panel on the chest
    rect(pic, 6, 26, 20, 19)
    rect(pic, 10, 30, 12, 8)
    for x in (12, 15, 18):
        rect(pic, x, 32, 2, 2, fill=True)
    hline(pic, 12, 19, 36)
    # The arms and the hands
    rect(pic, 1, 27, 4, 13)
    rect(pic, 27, 27, 4, 13)
    disc(pic, 2.5, 42, 2.4)
    disc(pic, 28.5, 42, 2.4)
    # The legs and the feet
    rect(pic, 9, 45, 5, 10)
    rect(pic, 18, 45, 5, 10)
    rect(pic, 6, 55, 9, 5, fill=True)
    rect(pic, 17, 55, 9, 5, fill=True)
    hline(pic, 0, 31, 62)
    for x in range(1, 31, 4):
        put(pic, x, 63)
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


def castle():
    """A castle with two towers and a keep, under the moon."""
    height = 64
    pic = blank(height)
    rng = Rng(3)
    for _ in range(10):
        put(pic, rng.integers(0, WIDTH), rng.integers(0, 14))
    for y in range(2, 11):
        for x in range(22, 32):
            if math.hypot(x - 27, y - 6) <= 3.8 and math.hypot(x - 29.2, y - 4.8) > 3.2:
                put(pic, x, y)

    def battlements(x0, x1, y):
        """Merlons: blocks of two with a gap of two, three rows high."""
        for x in range(x0, x1 + 1):
            if ((x - x0) // 2) % 2 == 0:
                vline(pic, x, y - 2, y)

    def bricks(x0, x1, y0, y1, step=4):
        for y in range(y0, y1, step):
            for x in range(x0 + 1, x1, 2):
                put(pic, x, y)

    # The keep, behind the wall
    rect(pic, 11, 22, 10, 22)
    battlements(11, 20, 21)
    bricks(11, 20, 27, 43)
    rect(pic, 14, 26, 4, 5)
    rect(pic, 15, 24, 2, 2, fill=True)
    vline(pic, 15, 8, 20)
    for k in range(5):
        hline(pic, 16, 16 + 4 - k, 8 + k)
    # The wall with its gate
    rect(pic, 6, 40, 20, 18)
    battlements(6, 25, 39)
    bricks(6, 25, 44, 57)
    for y in range(47, 58):
        hw = 3.0 if y > 50 else math.sqrt(max(0.0, 9.0 - (50 - y) ** 2))
        for x in range(int(round(16 - hw)), int(round(16 + hw)) + 1):
            put(pic, x, y, 0)
        put(pic, int(round(16 - hw)) - 1, y)
        put(pic, int(round(16 + hw)), y)
    # The grid of the gate
    for x in range(14, 19, 2):
        for y in range(50, 57, 2):
            put(pic, x, y)
    # The towers, with a pointed roof and a flag
    for x0, x1 in ((1, 8), (23, 30)):
        rect(pic, x0, 30, x1 - x0 + 1, 28)
        battlements(x0, x1, 29)
        bricks(x0, x1, 35, 57)
        mid = (x0 + x1) // 2
        vline(pic, mid, 35, 39)
        vline(pic, mid + 1, 35, 39)
        # The pointed roof sits above the battlements
        for dy in range(0, 9):
            half = 4.4 * dy / 8.0
            left, right = int(round(mid + 0.5 - half)), int(round(mid + 0.5 + half))
            if dy in (0, 8):
                hline(pic, left, right, 20 + dy)
            else:
                put(pic, left, 20 + dy)
                put(pic, right, 20 + dy)
        vline(pic, mid, 13, 19)
        hline(pic, mid + 1, mid + 3, 14)
        hline(pic, mid + 1, mid + 2, 15)
        put(pic, mid + 1, 16)
    # The ground
    hline(pic, 0, WIDTH - 1, 58)
    for x in range(WIDTH):
        for y in range(59, height):
            if lit(0.4, x, y):
                put(pic, x, y)
    return pic


def tree():
    """A big tree on a hill, with apples, a hollow and a pair of birds."""
    height = 128
    pic = blank(height)
    mask = shape(height)

    def add_disc(cx, cy, r):
        for y in range(max(0, int(cy - r - 1)), min(height, int(cy + r + 2))):
            for x in range(max(0, int(cx - r - 1)), min(WIDTH, int(cx + r + 2))):
                if math.hypot(x - cx, y - cy) <= r:
                    mask[y, x] = True

    # Birds
    for bx, by in ((6, 9), (24, 17)):
        line(pic, bx - 3, by - 1, bx, by + 1)
        line(pic, bx, by + 1, bx + 3, by - 1)
    # The crown: a heap of discs
    for cx, cy, r in ((16, 30, 10.5), (8, 38, 7.5), (24, 38, 7.5), (12, 49, 8.5), (21, 49, 8.5), (16, 41, 10.5), (6, 49, 5.5), (26, 49, 5.5)):
        add_disc(cx, cy, r)
    rng = Rng(12)
    for y in range(height):
        for x in range(WIDTH):
            if mask[y, x] and lit(0.32, x, y):
                pic[y, x] = 1
    # Gaps in the foliage
    for _ in range(26):
        x, y = rng.integers(2, 30), rng.integers(22, 58)
        if mask[y, x]:
            put(pic, x, y, 0)
    pic[edge_of(mask)] = 1
    # Apples: a ring with a dark middle
    for x, y in ((10, 33), (21, 29), (16, 45), (6, 44), (25, 45), (12, 54), (22, 54)):
        disc(pic, x, y, 1.6, 0)
        ring(pic, x, y, 1.6, thickness=0.5)
    # The trunk, wider at the bottom where the roots start
    top, bottom = 56, 114
    for y in range(top, bottom):
        hw = 4.6 + max(0.0, y - 94) * 0.33
        left, right = int(round(15.5 - hw)), int(round(15.5 + hw))
        for x in range(left, right + 1):
            pic[y, x] = 0
        put(pic, left, y)
        put(pic, right, y)
        # Bark: dashes that follow the trunk
        for k, off in enumerate((-0.45, 0.0, 0.5)):
            if (y + k * 3) % 8 < 5:
                put(pic, int(round(15.5 + off * hw)) + (1 if k == 1 else 0), y)
    # The hollow
    ellipse(pic, 16, 80, 3.2, 4.4, fill=True, value=0)
    ellipse(pic, 16, 80, 3.2, 4.4)
    ellipse(pic, 16, 81, 1.8, 2.6, fill=True)
    # The hill and the roots, and tufts of grass
    for x in range(WIDTH):
        ground = 112 + int(round(2.0 * math.sin(x / 5.0 + 0.5) - 0.07 * abs(x - 15.5)))
        for y in range(ground, height):
            pic[y, x] = 0
        put(pic, x, ground)
        for y in range(ground + 3, height, 3):
            if (x + y) % 2 == 0:
                put(pic, x, y)
    for x in (3, 8, 24, 29):
        put(pic, x, 109)
        put(pic, x - 1, 108)
        put(pic, x + 1, 108)
    # Leaves that fall
    for x, y in ((4, 70), (27, 76), (7, 92), (25, 100), (3, 82)):
        put(pic, x, y)
        put(pic, x + 1, y + 1)
    return pic


def skull():
    """A skull with crossed bones."""
    height = 64
    pic = blank(height)
    # The bones: two thick diagonals with a knob at each end
    for a, b in (((4, 40), (27, 59)), ((27, 40), (4, 59))):
        for dx, dy in ((0, 0), (0, 1)):
            line(pic, a[0] + dx, a[1] + dy, b[0] + dx, b[1] + dy)
        for end in (a, b):
            disc(pic, end[0], end[1] + 0.5, 2.2)
    # The skull: the cranium and the jaw in one piece
    disc(pic, 15.5, 19, 11.0)
    rect(pic, 9, 24, 14, 13, fill=True)
    for x in range(WIDTH):
        for y in range(34, 40):
            pic[y, x] = pic[y, x] if y < 37 else pic[y, x]
    # Eyes, nose and teeth: dark
    disc(pic, 11.5, 20, 3.4, 0)
    disc(pic, 20.5, 20, 3.4, 0)
    for dy, half in enumerate((0, 1, 1)):
        hline(pic, 15 - half, 16 + half, 26 + dy, 0)
    for x in (12, 14, 17, 19):
        vline(pic, x, 31, 36, 0)
    hline(pic, 10, 21, 30, 0)
    # A highlight on the forehead
    for x, y in ((9, 11), (10, 10), (11, 9), (12, 9)):
        put(pic, x, y, 0)
    return pic


def sword():
    """A long sword with a gem in the guard."""
    height = 128
    pic = blank(height)
    cx = 15.5
    rng = Rng(40)
    # The blade: a point, two faces (one lit, one in shade) and the groove between them
    for y in range(6, 89):
        hw = min(3.4, 0.5 + (y - 6) * 0.3)
        left, right = int(round(cx - hw)), int(round(cx + hw - 1))
        for x in range(left, right + 1):
            if x < 15:
                put(pic, x, y)
            elif lit(0.45, x, y):
                put(pic, x, y)
        put(pic, left, y)
        put(pic, right, y)
        if 24 <= y <= 80:
            put(pic, 15, y, 0)
    hline(pic, 13, 18, 88)
    # The guard, with the ends that turn up
    rect(pic, 4, 89, 24, 4, fill=True)
    for x0, x1 in ((3, 5), (26, 28)):
        rect(pic, x0, 86, x1 - x0 + 1, 3, fill=True)
    rect(pic, 14, 90, 4, 2, fill=True, value=0)
    # The grip, wrapped
    for y in range(93, 113):
        for x in range(14, 18):
            if (y - 93) % 3 == 1 or lit(0.5, x, y):
                put(pic, x, y)
    vline(pic, 13, 93, 112)
    vline(pic, 18, 93, 112)
    # The pommel
    disc(pic, cx, 117, 4.0)
    disc(pic, cx, 117, 1.4, 0)
    # Sparkles around the blade: four-point stars
    for x, y, r in ((24, 16, 3), (7, 34, 2), (23, 56, 2), (8, 72, 3)):
        hline(pic, x - r, x + r, y)
        vline(pic, x, y - r, y + r)
    for _ in range(14):
        x, y = rng.integers(0, WIDTH), rng.integers(0, 84)
        if abs(x - cx) > 6:
            put(pic, x, y)
    return pic


def triangle(pic, p0, p1, p2, fill=True, value=1):
    """A triangle, filled or only its three sides."""
    if not fill:
        line(pic, *p0, *p1, value)
        line(pic, *p1, *p2, value)
        line(pic, *p2, *p0, value)
        return
    (x0, y0), (x1, y1), (x2, y2) = p0, p1, p2
    for y in range(max(0, int(min(y0, y1, y2))), min(pic.shape[0], int(max(y0, y1, y2)) + 1)):
        for x in range(WIDTH):
            d0 = (x - x1) * (y0 - y1) - (x0 - x1) * (y - y1)
            d1 = (x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)
            d2 = (x - x0) * (y2 - y0) - (x2 - x0) * (y - y0)
            if (d0 >= 0 and d1 >= 0 and d2 >= 0) or (d0 <= 0 and d1 <= 0 and d2 <= 0):
                put(pic, x, y, value)


def key():
    """An old key with a three-lobed bow."""
    height = 64
    pic = blank(height)
    cx = 15.5
    # The bow: a disc with three round holes
    disc(pic, cx, 13, 10.5)
    for hx, hy in ((15.5, 8.5), (11.0, 16.0), (20.0, 16.0)):
        disc(pic, hx, hy, 2.7, 0)
    # The collar and the shaft
    rect(pic, 11, 24, 10, 3, fill=True)
    rect(pic, 13, 27, 6, 31)
    for y in range(28, 57):
        for x in (14, 17):
            if lit(0.4, x, y):
                put(pic, x, y)
    rect(pic, 12, 32, 8, 2, fill=True)
    hline(pic, 14, 17, 58)
    # The bit: two teeth with notches
    rect(pic, 19, 44, 8, 5, fill=True)
    rect(pic, 19, 52, 6, 5, fill=True)
    for x, y in ((22, 44), (23, 44), (24, 46), (25, 48), (21, 52), (22, 52)):
        put(pic, x, y, 0)
    return pic


def antenna():
    """A radio tower sending its signal out."""
    height = 128
    pic = blank(height)
    cx = 15.5
    top, bottom = 24, 123

    def half(y):
        return 1.5 + (y - top) * 10.5 / (bottom - top)

    for side in (-1, 1):
        line(pic, cx + side * half(top), top, cx + side * half(bottom), bottom)
    levels = list(range(top + 8, bottom + 1, 13))
    for y0, y1 in zip(levels, levels[1:]):
        hline(pic, int(round(cx - half(y0))), int(round(cx + half(y0))), y0)
        line(pic, cx - half(y0), y0, cx + half(y1), y1)
        line(pic, cx + half(y0), y0, cx - half(y1), y1)
    hline(pic, int(round(cx - half(levels[-1]))), int(round(cx + half(levels[-1]))), levels[-1])
    # The mast and the light on top
    vline(pic, 15, 13, top)
    vline(pic, 16, 13, top)
    disc(pic, cx, 10.5, 2.4)
    # The signal: arcs on both sides, further and further away
    for r in (6.0, 10.0, 14.0):
        for i in range(-12, 13):
            a = 0.8 * i / 12.0
            for side in (-1, 1):
                px = int(round(cx + side * r * math.cos(a)))
                py = int(round(10.5 + r * math.sin(a)))
                if (i + (3 if r > 7 else 0)) % 3 != 2:
                    put(pic, px, py)
    # The base
    rect(pic, 6, 124, 20, 3, fill=True)
    hline(pic, 0, WIDTH - 1, 127)
    return pic


def potion():
    """A round flask with a bubbling potion and a heart."""
    height = 64
    pic = blank(height)
    cx, cy, r = 15.5, 45.0, 12.5
    # The cork and the lip
    rect(pic, 12, 4, 8, 6)
    for y in range(5, 9):
        for x in range(13, 19):
            if lit(0.4, x, y):
                put(pic, x, y)
    rect(pic, 10, 10, 12, 3, fill=True)
    # The neck and the body
    neck_half = 4.6
    meet = cy - math.sqrt(r * r - neck_half * neck_half)
    vline(pic, int(round(cx - neck_half)), 13, int(meet))
    vline(pic, int(round(cx + neck_half)) - 1, 13, int(meet))
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(WIDTH):
            d = math.hypot(x - cx, y - cy)
            if abs(d - r) <= 0.55 and (y > meet or abs(x - cx) > neck_half + 1):
                put(pic, x, y)
    # The potion: dots, with a wavy top
    for y in range(int(cy - r), int(cy + r) + 1):
        for x in range(WIDTH):
            if math.hypot(x - cx, y - cy) < r - 1.0:
                surface = 41 + 1.3 * math.sin(x / 2.1)
                if y >= surface and lit(0.62, x, y):
                    put(pic, x, y)
                if abs(y - surface) < 0.6:
                    put(pic, x, y)
    # Bubbles rising from the liquid
    for bx, by, br in ((12, 36, 1.6), (19, 33, 1.2), (14, 28, 1.0)):
        ring(pic, bx, by, br, thickness=0.5)
    # A heart in the liquid, dark
    heart_rows = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."]
    for j, row in enumerate(heart_rows):
        for i, ch in enumerate(row):
            if ch == "#":
                put(pic, 12 + i, 44 + j, 0)
    # A glint on the glass, and sparkles around
    for x, y in ((9, 40), (8, 42), (8, 44)):
        put(pic, x, y)
    for x, y, rr in ((26, 22, 2), (4, 25, 2), (27, 56, 1)):
        hline(pic, x - rr, x + rr, y)
        vline(pic, x, y - rr, y + rr)
    hline(pic, 4, 27, 62)
    return pic


def sailboat():
    """A sailboat on the waves, with the sun and a gull."""
    height = 64
    pic = blank(height)
    disc(pic, 25, 9, 4.0)
    for k in range(8):
        a = k * TAU / 8
        line(pic, 25 + 5.6 * math.cos(a), 9 + 5.6 * math.sin(a), 25 + 7.6 * math.cos(a), 9 + 7.6 * math.sin(a))
    line(pic, 3, 13, 6, 15)
    line(pic, 6, 15, 9, 13)
    cx = 15
    vline(pic, cx, 12, 42)
    # The main sail: its edge and horizontal seams
    for y in range(13, 39):
        right = cx + 1 + (y - 13) * (27 - cx - 1) / 25.0
        for x in range(cx + 1, int(round(right)) + 1):
            if y % 3 == 0 or x == int(round(right)) or y == 38:
                put(pic, x, y)
    # The small sail in front
    for y in range(19, 39):
        left = cx - 1 - (y - 19) * (cx - 1 - 4) / 19.0
        for x in range(int(round(left)), cx):
            if y % 3 == 1 or x == int(round(left)) or y == 38:
                put(pic, x, y)
    # The flag
    for k in range(4):
        hline(pic, cx + 1, cx + 4 - k, 10 + k)
    # The hull, with portholes
    for y in range(41, 47):
        inset = (y - 41) * 0.9
        hline(pic, int(round(5 + inset)), int(round(26 - inset)), y)
    for x in (11, 15, 19):
        put(pic, x, 43, 0)
    # The waves
    for k, base in enumerate((50, 55, 60)):
        for x in range(WIDTH):
            y = base + int(round(1.4 * math.sin(x / 2.2 + k * 2.1)))
            if (x + k) % 4 != 3:
                put(pic, x, y)
    return pic


def compass():
    """A compass rose inside two rings."""
    height = 32
    pic = blank(height)
    cx = cy = 15.5
    ring(pic, cx, cy, 14.5, thickness=0.5)
    ring(pic, cx, cy, 12.2, thickness=0.4)
    # Marks between the rings
    for k in range(24):
        a = k * TAU / 24
        if k % 6:
            put(pic, int(round(cx + 13.4 * math.cos(a))), int(round(cy + 13.4 * math.sin(a))))
    # The four short points, then the four long ones
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        tip = (cx + 7.5 * math.cos(a), cy + 7.5 * math.sin(a))
        b0 = (cx + 2.2 * math.cos(a - math.pi / 2), cy + 2.2 * math.sin(a - math.pi / 2))
        b1 = (cx + 2.2 * math.cos(a + math.pi / 2), cy + 2.2 * math.sin(a + math.pi / 2))
        triangle(pic, tip, b0, b1, fill=False)
    for k in range(4):
        a = k * math.pi / 2
        tip = (cx + 11.2 * math.cos(a), cy + 11.2 * math.sin(a))
        b0 = (cx + 3.0 * math.cos(a - math.pi / 2), cy + 3.0 * math.sin(a - math.pi / 2))
        b1 = (cx + 3.0 * math.cos(a + math.pi / 2), cy + 3.0 * math.sin(a + math.pi / 2))
        triangle(pic, tip, b0, b1, fill=(k == 3))
    disc(pic, cx, cy, 1.6, 0)
    put(pic, 15, 15)
    return pic


def crown():
    """A crown with five points and jewels."""
    height = 32
    pic = blank(height)
    points = [(3, 21), (3, 9), (9.5, 16), (15.5, 5), (21.5, 16), (28, 9), (28, 21)]
    for p, q in zip(points, points[1:]):
        line(pic, *p, *q)
    # The points are filled with dots, from the zigzag down to the band
    for x in range(4, 28):
        top = 21
        for (xa, ya), (xb, yb) in zip(points[1:], points[2:]):
            if xa <= x <= xb:
                top = ya + (yb - ya) * (x - xa) / (xb - xa)
        for y in range(int(top) + 2, 21):
            if lit(0.32, x, y):
                put(pic, x, y)
    # The band and its jewels
    rect(pic, 3, 21, 26, 7)
    hline(pic, 3, 28, 23)
    for jx in (8, 15, 23):
        disc(pic, jx + 0.5, 25.5, 1.7, 0)
        put(pic, jx, 25)
    # Balls on the tips
    for tx, ty, tr in ((3.5, 8, 1.8), (15.5, 3.5, 2.2), (27.5, 8, 1.8)):
        disc(pic, tx, ty, tr)
    # Sparkles
    for x, y in ((1, 3), (30, 3), (8, 4), (23, 6)):
        put(pic, x, y)
    return pic


def cassette():
    """An audio cassette, with its label and its two reels."""
    height = 32
    pic = blank(height)
    rect(pic, 1, 5, 30, 22)
    # The label, with its name and two lines
    rect(pic, 4, 8, 24, 9)
    text(pic, 6, 10, "MIX")
    hline(pic, 19, 25, 11)
    hline(pic, 19, 25, 14)
    # The window with the two reels
    rect(pic, 8, 18, 16, 6)
    for rx in (12, 20):
        ring(pic, rx, 20.5, 2.3, thickness=0.5)
        put(pic, rx, 20)
        put(pic, rx, 21)
    line(pic, 12, 23, 20, 23)
    # The screws in the corners, and the foot
    for x, y in ((3, 7), (28, 7), (3, 25), (28, 25)):
        put(pic, x, y, 0)
    line(pic, 7, 27, 9, 24)
    line(pic, 24, 27, 22, 24)
    for x in (12, 19):
        put(pic, x, 25)
    return pic


def floppy():
    """A floppy disk, with its metal shutter and its label."""
    height = 32
    pic = blank(height)
    # The body, with the top right corner cut
    line(pic, 2, 2, 25, 2)
    line(pic, 25, 2, 29, 6)
    line(pic, 29, 6, 29, 29)
    line(pic, 29, 29, 2, 29)
    line(pic, 2, 29, 2, 2)
    # The shutter, with its slot
    rect(pic, 9, 2, 14, 9, fill=True)
    rect(pic, 17, 4, 4, 5, fill=True, value=0)
    # The label: a dotted line and the name
    rect(pic, 6, 15, 20, 14)
    for x in range(8, 24, 2):
        put(pic, x, 17)
    text(pic, 10, 21, "ZMK")
    put(pic, 4, 27)
    return pic


def phases():
    """The eight phases of the moon, one above the other."""
    height = 128
    pic = blank(height)
    cx, r = 15.5, 6.2
    craters = [(-2, -2), (2, 1), (-1, 3), (3, -3)]
    for k in range(8):
        cy = 8.5 + 15.5 * k
        phase = k / 8.0
        waxing = phase < 0.5
        for y in range(int(cy - r) - 1, int(cy + r) + 2):
            for x in range(int(cx - r) - 2, int(cx + r) + 3):
                dy = y - cy
                dx = x - cx
                if math.hypot(dx, dy) > r:
                    continue
                span = math.sqrt(max(r * r - dy * dy, 0.01))
                u = dx / span
                if waxing:
                    on = u > math.cos(TAU * phase)
                else:
                    on = u < -math.cos(TAU * phase)
                if on:
                    put(pic, x, y)
        for dx, dy in craters:
            px, py = int(round(cx + dx)), int(round(cy + dy))
            if 0 <= px < WIDTH and pic[py, px] and 0 < k < 7 and abs(k - 4) < 4:
                put(pic, px, py, 0)
        # The whole edge, so the part in the shade is also seen
        for i in range(60):
            a = TAU * i / 60
            if i % 2 == 0:
                put(pic, int(round(cx + r * math.cos(a))), int(round(cy + r * math.sin(a))))
    return pic


def mushroom():
    """A red-cap mushroom with a face, as in the old games."""
    height = 32
    pic = blank(height)
    cx = 15.5
    for y in range(3, 20):
        for x in range(WIDTH):
            if math.hypot((x - cx) / 14.5, (y - 19.5) / 16.0) <= 1.0:
                put(pic, x, y)
    for sx, sy, sr in ((8.5, 12.0, 2.9), (23.0, 11.5, 3.2), (15.5, 7.0, 2.2), (15.5, 15.5, 2.0)):
        disc(pic, sx, sy, sr, 0)
    rect(pic, 3, 20, 26, 2, fill=True)
    # The stalk, with two dark eyes that have a glint
    rect(pic, 10, 22, 12, 9, fill=True)
    rect(pic, 13, 24, 2, 4, fill=True, value=0)
    rect(pic, 17, 24, 2, 4, fill=True, value=0)
    put(pic, 13, 24)
    put(pic, 17, 24)
    hline(pic, 4, 27, 31)
    return pic


STILLS = {
    "coffee": coffee,
    "cactus": cactus,
    "lighthouse": lighthouse,
    "moon_cat": moon_cat,
    "robot": robot,
    "planet": planet,
    "castle": castle,
    "tree": tree,
    "skull": skull,
    "sword": sword,
    "key": key,
    "antenna": antenna,
    "potion": potion,
    "sailboat": sailboat,
    "compass": compass,
    "crown": crown,
    "cassette": cassette,
    "floppy": floppy,
    "phases": phases,
    "mushroom": mushroom,
}
