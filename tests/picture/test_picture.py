#!/usr/bin/env python3
"""Host-test boards/shields/nice_oled/widgets/picture.c, the code that puts a picture of the
right screen on the canvas turned, cropped and mixed with the widgets.

picture.c is plain C (no LVGL, no Zephyr): it is compiled as it is into a shared library and
called through ctypes. The answers are compared with a model that does not share its index
arithmetic: it turns whole arrays (numpy) the way the settings describe it, and the upright
picture is the one convert.py makes for the app (PIL, a quarter of a turn counterclockwise).

    python tests/picture/test_picture.py

needs numpy and Pillow, and a C compiler: `cc`, or the one of the `ziglang` package
(`python -m ziglang cc`) when there is none.
"""
import ctypes
import os
import random
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "boards" / "shields" / "nice_oled" / "widgets" / "picture.c"

ADD, INVERT = 0, 1


class Src(ctypes.Structure):
    _fields_ = [
        ("bits", ctypes.c_void_p),
        ("w", ctypes.c_uint16),
        ("h", ctypes.c_uint16),
        ("stride", ctypes.c_uint16),
    ]


class View(ctypes.Structure):
    _fields_ = [
        ("rot", ctypes.c_uint8),
        ("crop_x", ctypes.c_uint16),
        ("crop_y", ctypes.c_uint16),
        ("crop_w", ctypes.c_uint16),
        ("crop_h", ctypes.c_uint16),
        ("mix", ctypes.c_uint8),
    ]


def compiler():
    cc = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if cc:
        return [cc]
    return [sys.executable, "-m", "ziglang", "cc"]


def build(directory):
    suffix = ".dll" if os.name == "nt" else ".so"
    library = Path(directory) / ("picture" + suffix)
    command = compiler() + [
        "-shared",
        "-O1",
        "-Wall",
        "-Werror",
        "-fPIC",
        "-o",
        str(library),
        str(SOURCE),
    ]
    subprocess.run(command, check=True)
    lib = ctypes.CDLL(str(library))
    lib.picture_blit.argtypes = [
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.POINTER(Src),
        ctypes.POINTER(View),
        ctypes.c_uint8,
        ctypes.c_uint8,
    ]
    lib.picture_blit.restype = None
    lib.picture_upright_size.argtypes = [
        ctypes.POINTER(Src),
        ctypes.c_uint8,
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
    ]
    lib.picture_upright_size.restype = None
    return lib


def pack(rows):
    """The bytes of a picture, a row after the other, the leftmost pixel in the top bit."""
    h, w = rows.shape
    stride = (w + 7) // 8
    out = bytearray(stride * h)
    for j in range(h):
        for i in range(w):
            if rows[j, i]:
                out[j * stride + i // 8] |= 0x80 >> (i % 8)
    return bytes(out), stride


def upright_of(stored):
    """The picture as the app shows it: convert.py turns PIL's counterclockwise quarter turn."""
    h, w = stored.shape
    img = Image.new("L", (w, h), 0)
    img.putdata([255 if v else 0 for v in stored.reshape(-1)])
    turned = img.rotate(90, expand=True)
    return (np.array(turned) > 0).astype(np.uint8)


def model(stored, rot, crop, x, y, canvas, mix, fg, bg):
    """What picture_blit has to leave on the canvas, by turning arrays instead of indexes."""
    upright = np.rot90(upright_of(stored), -rot)
    uh, uw = upright.shape

    cx, cy, cw, ch = crop
    if cw == 0 or ch == 0:
        cx, cy, cw, ch = 0, 0, uw, uh
    else:
        cx = min(cx, uw - 1)
        cy = min(cy, uh - 1)
        cw = min(cw, uw - cx)
        ch = min(ch, uh - cy)

    # The piece that shows: the lit pixels of the crop, the rest of the upright picture off
    shown = np.zeros_like(upright)
    shown[cy : cy + ch, cx : cx + cw] = upright[cy : cy + ch, cx : cx + cw]

    # Turned back for the canvas
    displayed = np.rot90(shown, -1)

    out = canvas.copy()
    dh, dw = displayed.shape
    lit_is_low = fg < bg
    middle = (fg + bg) // 2
    for b in range(dh):
        for a in range(dw):
            if not displayed[b, a]:
                continue
            px, py = x + a, y + b
            if not (0 <= px < out.shape[1] and 0 <= py < out.shape[0]):
                continue
            if mix == INVERT:
                was_lit = out[py, px] <= middle if lit_is_low else out[py, px] > middle
                out[py, px] = bg if was_lit else fg
            else:
                out[py, px] = fg
    return out


class PictureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.lib = build(cls.directory.name)

    @classmethod
    def tearDownClass(cls):
        if os.name == "nt":
            # Windows does not delete a library that is still loaded
            import _ctypes

            _ctypes.FreeLibrary(cls.lib._handle)
        cls.directory.cleanup()

    def blit(self, stored, rot, crop, x, y, canvas, mix, fg, bg):
        data, stride = pack(stored)
        buffer = ctypes.create_string_buffer(data, len(data))
        src = Src(ctypes.cast(buffer, ctypes.c_void_p), stored.shape[1], stored.shape[0], stride)
        view = View(rot, crop[0], crop[1], crop[2], crop[3], mix)
        h, w = canvas.shape
        flat = ctypes.create_string_buffer(canvas.astype(np.uint8).tobytes(), w * h)
        self.lib.picture_blit(flat, w, h, w, x, y, ctypes.byref(src), ctypes.byref(view), fg, bg)
        return np.frombuffer(flat.raw, dtype=np.uint8).reshape(h, w).copy()

    def check(self, stored, rot, crop, x, y, canvas, mix, fg=0, bg=255):
        got = self.blit(stored, rot, crop, x, y, canvas, mix, fg, bg)
        want = model(stored, rot, crop, x, y, canvas, mix, fg, bg)
        self.assertTrue(
            np.array_equal(got, want),
            f"rot {rot}, crop {crop}, at ({x}, {y}), mix {mix}, fg {fg}\n"
            f"stored\n{stored}\ngot\n{got}\nwant\n{want}",
        )

    def test_the_stored_picture_is_the_one_at_rot_0(self):
        # The pixels of a picture that is not turned and not cropped go where they are stored
        stored = np.zeros((4, 6), dtype=np.uint8)
        stored[0, 0] = stored[1, 5] = stored[3, 2] = 1
        canvas = np.full((10, 12), 255, dtype=np.uint8)
        got = self.blit(stored, 0, (0, 0, 0, 0), 2, 3, canvas, ADD, 0, 255)

        want = canvas.copy()
        want[3 + 0, 2 + 0] = want[3 + 1, 2 + 5] = want[3 + 3, 2 + 2] = 0
        self.assertTrue(np.array_equal(got, want))

    def test_upright_size(self):
        stored = np.zeros((4, 6), dtype=np.uint8)
        data, stride = pack(stored)
        buffer = ctypes.create_string_buffer(data, len(data))
        src = Src(ctypes.cast(buffer, ctypes.c_void_p), 6, 4, stride)
        w, h = ctypes.c_int(), ctypes.c_int()

        # The stored picture is 6 columns by 4 rows: upright it is 4 by 6, and the other way
        # round after a quarter of a turn
        for rot, size in ((0, (4, 6)), (1, (6, 4)), (2, (4, 6)), (3, (6, 4)), (5, (6, 4))):
            self.lib.picture_upright_size(ctypes.byref(src), rot, ctypes.byref(w), ctypes.byref(h))
            self.assertEqual((w.value, h.value), size, rot)

    def test_the_upright_picture_is_the_one_the_app_draws(self):
        # An animation of 69 x 68 stored (the cat): its top right pixel is the top left one
        # upright, and its top left one is the bottom left one
        stored = np.zeros((4, 6), dtype=np.uint8)
        stored[0, 5] = 1
        upright = upright_of(stored)
        self.assertEqual(upright.shape, (6, 4))
        self.assertEqual(upright[0, 0], 1)
        self.assertEqual(int(upright.sum()), 1)

        stored = np.zeros((4, 6), dtype=np.uint8)
        stored[0, 0] = 1
        self.assertEqual(upright_of(stored)[5, 0], 1)

    def test_a_quarter_turn_clockwise_puts_the_upright_top_on_the_right(self):
        # The upright picture is a vertical bar on the left; a quarter turn clockwise puts it
        # at the top, and the pixels get to the canvas as the model says
        upright = np.zeros((6, 4), dtype=np.uint8)
        upright[:, 0] = 1
        # stored = the upright one turned clockwise
        stored = np.rot90(upright, -1).copy()
        self.assertTrue(np.array_equal(upright_of(stored), upright))
        canvas = np.full((12, 12), 255, dtype=np.uint8)
        self.check(stored, 1, (0, 0, 0, 0), 1, 1, canvas, ADD)

    def test_random_pictures(self):
        rng = random.Random(7)
        for _ in range(1500):
            w, h = rng.randint(1, 19), rng.randint(1, 19)
            stored = np.array(
                [[1 if rng.random() < 0.4 else 0 for _ in range(w)] for _ in range(h)],
                dtype=np.uint8,
            )
            cw, ch = rng.randint(8, 30), rng.randint(8, 30)
            if rng.random() < 0.5:
                canvas = np.full((ch, cw), 255, dtype=np.uint8)
            else:
                canvas = np.array(
                    [[rng.choice((0, 255)) for _ in range(cw)] for _ in range(ch)],
                    dtype=np.uint8,
                )

            rot = rng.randint(0, 3)
            if rng.random() < 0.4:
                crop = (0, 0, 0, 0)
            else:
                crop = (
                    rng.randint(0, 22),
                    rng.randint(0, 22),
                    rng.randint(0, 24),
                    rng.randint(0, 24),
                )
            x, y = rng.randint(-25, 30), rng.randint(-25, 30)
            mix = rng.choice((ADD, INVERT))
            # The ink is dark (0 on 255) or light (the build with CONFIG_NICE_OLED_WIDGET_INVERTED)
            fg, bg = rng.choice(((0, 255), (255, 0)))
            if fg == 255:
                canvas = 255 - canvas
            self.check(stored, rot, crop, x, y, canvas, mix, fg, bg)

    def test_nothing_outside_the_canvas_is_touched(self):
        # The canvas is a window of a bigger buffer in the firmware (160 x 160, of which
        # 160 x 68 is drawn on): the rows past the canvas must not change
        stored = np.ones((8, 8), dtype=np.uint8)
        data, stride = pack(stored)
        buffer = ctypes.create_string_buffer(data, len(data))
        src = Src(ctypes.cast(buffer, ctypes.c_void_p), 8, 8, stride)
        view = View(0, 0, 0, 0, 0, ADD)

        width, stride_bytes, rows, canvas_rows = 10, 16, 14, 10
        flat = ctypes.create_string_buffer(b"\x55" * (stride_bytes * rows), stride_bytes * rows)
        self.lib.picture_blit(
            flat, width, canvas_rows, stride_bytes, -4, 6, ctypes.byref(src), ctypes.byref(view), 0, 255
        )
        out = np.frombuffer(flat.raw, dtype=np.uint8).reshape(rows, stride_bytes)

        # Only the 4 columns and the 4 rows that are inside were drawn
        self.assertEqual(int((out == 0).sum()), 16)
        self.assertTrue(np.all(out[:, width:] == 0x55))
        self.assertTrue(np.all(out[canvas_rows:, :] == 0x55))

    def test_bad_arguments_do_nothing(self):
        stored = np.ones((2, 2), dtype=np.uint8)
        data, stride = pack(stored)
        buffer = ctypes.create_string_buffer(data, len(data))
        view = View(0, 0, 0, 0, 0, ADD)
        canvas = ctypes.create_string_buffer(b"\xff" * 16, 16)

        empty = Src(None, 2, 2, stride)
        self.lib.picture_blit(canvas, 4, 4, 4, 0, 0, ctypes.byref(empty), ctypes.byref(view), 0, 255)
        flat = Src(ctypes.cast(buffer, ctypes.c_void_p), 0, 2, stride)
        self.lib.picture_blit(canvas, 4, 4, 4, 0, 0, ctypes.byref(flat), ctypes.byref(view), 0, 255)
        self.assertEqual(canvas.raw, b"\xff" * 16)

    def test_a_crop_that_starts_past_the_picture_keeps_its_last_pixel(self):
        stored = np.ones((3, 5), dtype=np.uint8)
        canvas = np.full((9, 9), 255, dtype=np.uint8)
        # upright 3 x 5: a crop at (50, 50) is the last pixel
        self.check(stored, 0, (50, 50, 4, 4), 1, 1, canvas, ADD)
        got = self.blit(stored, 0, (50, 50, 4, 4), 1, 1, canvas, ADD, 0, 255)
        self.assertEqual(int((got == 0).sum()), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
