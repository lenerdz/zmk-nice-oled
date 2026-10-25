#!/usr/bin/env python3
"""Host-test boards/shields/nice_oled/widgets/pixel_shift.c, the anti burn-in of the screens: the
canvas of the status screen moves one pixel every KP_DISPLAY_SHIFT_EVERY_S seconds along the
walk of kp_display_shift_offset() (zmk-rgb-matrix), when KP_DISPLAY_SHIFT is on.

The code of the shield is compiled as it is, with a few stubs for LVGL and Zephyr (stubs/) that
write down what they are asked, and the real zmk/display_settings.h of zmk-rgb-matrix, which is
looked for in the folder in the environment variable KEYPAW_RGB_MATRIX_DIR (a checkout of
lenerdz/zmk-rgb-matrix) or next to this repository (../zmk-rgb-matrix); without it the test is
skipped.

    python tests/pixel_shift/test_pixel_shift.py

needs a C compiler: `cc`, or the one of the `ziglang` package (`python -m ziglang cc`) when there
is none.
"""
import ctypes
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WIDGETS = ROOT / "boards" / "shields" / "nice_oled" / "widgets"

# The ids of enum kp_display_setting_id that the shift uses
SHIFT, SHIFT_EVERY_S, SHIFT_PX = 11, 12, 13


def module_dir():
    asked = os.environ.get("KEYPAW_RGB_MATRIX_DIR")
    for candidate in ([Path(asked)] if asked else []) + [ROOT.parent / "zmk-rgb-matrix"]:
        if (candidate / "include" / "zmk" / "display_settings.h").is_file():
            return candidate
    return None


def compiler():
    cc = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if cc:
        return [cc]
    return [sys.executable, "-m", "ziglang", "cc"]


def build(directory, module):
    suffix = ".dll" if os.name == "nt" else ".so"
    library = Path(directory) / ("pixel_shift" + suffix)
    subprocess.run(
        compiler()
        + [
            "-shared",
            "-O1",
            "-Wall",
            "-Werror",
            "-fPIC",
            f"-I{HERE / 'stubs'}",
            f"-I{WIDGETS}",
            f"-I{module / 'include'}",
            "-o",
            str(library),
            str(HERE / "harness.c"),
        ],
        check=True,
    )
    lib = ctypes.CDLL(str(library))
    lib.t_set.argtypes = [ctypes.c_int, ctypes.c_int32]
    lib.t_time.argtypes = [ctypes.c_int64]
    lib.t_init.argtypes = [ctypes.c_uint8]
    lib.t_timer_period.restype = ctypes.c_uint32
    lib.t_x.restype = ctypes.c_int32
    lib.t_y.restype = ctypes.c_int32
    lib.t_style_border.restype = ctypes.c_int32
    lib.t_style_radius.restype = ctypes.c_int32
    lib.t_expected.argtypes = [
        ctypes.c_uint32,
        ctypes.c_int32,
        ctypes.POINTER(ctypes.c_int32),
        ctypes.POINTER(ctypes.c_int32),
    ]
    return lib


class PixelShift(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        module = module_dir()
        if module is None:
            raise unittest.SkipTest("no zmk-rgb-matrix checkout (set KEYPAW_RGB_MATRIX_DIR)")
        cls.tmp = tempfile.mkdtemp()
        cls.lib = build(cls.tmp, module)

    @classmethod
    def tearDownClass(cls):
        # The library stays loaded on Windows: removing the folder may fail, and does not matter
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def setUp(self):
        self.lib.t_reset()
        self.lib.t_init(0xFF)

    def expected(self, step, px):
        dx, dy = ctypes.c_int32(), ctypes.c_int32()
        self.lib.t_expected(step, px, ctypes.byref(dx), ctypes.byref(dy))
        return dx.value, dy.value

    def at(self):
        return self.lib.t_x(), self.lib.t_y()

    def look(self, ms):
        """The timer of LVGL fires at `ms`."""
        self.lib.t_time(ms)
        self.lib.t_poll()

    def turn_on(self, every_s=10, px=2, at_ms=1000):
        self.lib.t_set(SHIFT, 1)
        self.lib.t_set(SHIFT_EVERY_S, every_s)
        self.lib.t_set(SHIFT_PX, px)
        self.look(at_ms)

    def test_init_sets_one_timer_of_a_second_and_the_container_shows_the_background(self):
        self.assertEqual(self.lib.t_timers(), 1)
        self.assertEqual(self.lib.t_timer_period(), 1000)
        # the container: the color it was given, opaque, no border, square
        self.assertTrue(self.lib.t_styles_on_container())
        self.assertEqual(self.lib.t_style_bg(), 0xFF)
        self.assertEqual(self.lib.t_style_opa(), 255)
        self.assertEqual(self.lib.t_style_border(), 0)
        self.assertEqual(self.lib.t_style_radius(), 0)
        # and the canvas was not moved
        self.assertEqual(self.lib.t_aligns(), 0)

    def test_the_background_is_the_one_the_screen_passes(self):
        self.lib.t_reset()
        self.lib.t_init(0x00)
        self.assertEqual(self.lib.t_style_bg(), 0x00)

    def test_off_never_moves_the_canvas(self):
        for ms in range(0, 3_600_000, 7_000):
            self.look(ms)
        self.assertEqual(self.lib.t_aligns(), 0)

    def test_the_first_step_comes_after_a_whole_time(self):
        self.turn_on(every_s=10, px=2, at_ms=5000)
        self.assertEqual(self.lib.t_aligns(), 0)
        for ms in range(6000, 15000, 1000):
            self.look(ms)
        self.assertEqual(self.lib.t_aligns(), 0, "it moved before 10 s went by")
        self.look(15000)
        self.assertEqual(self.lib.t_aligns(), 1)
        self.assertEqual(self.at(), self.expected(1, 2))
        self.assertTrue(self.lib.t_align_is_canvas_top_left())
        # and the next one 10 s after
        self.look(24000)
        self.assertEqual(self.lib.t_aligns(), 1)
        self.look(25000)
        self.assertEqual(self.lib.t_aligns(), 2)
        self.assertEqual(self.at(), self.expected(2, 2))

    def test_the_canvas_walks_one_pixel_at_a_time_and_stays_within_the_pixels(self):
        px = 3
        self.turn_on(every_s=10, px=px, at_ms=0)
        previous = (0, 0)
        positions = {previous}
        for n in range(1, 400):
            self.look(n * 10_000)
            now = self.at()
            self.assertLessEqual(abs(now[0]), px)
            self.assertLessEqual(abs(now[1]), px)
            self.assertEqual(abs(now[0] - previous[0]) + abs(now[1] - previous[1]), 1, f"step {n}")
            self.assertEqual(now, self.expected(n, px), f"step {n}")
            positions.add(now)
            previous = now
        # every square of the walk had its turn
        self.assertEqual(len(positions), (2 * px + 1) ** 2)

    def test_nothing_is_drawn_again_when_nothing_changed(self):
        self.turn_on(every_s=10, px=2, at_ms=0)
        self.look(10_000)
        count = self.lib.t_aligns()
        for ms in range(11_000, 20_000, 1000):
            self.look(ms)
        self.assertEqual(self.lib.t_aligns(), count)

    def test_a_late_look_takes_one_step_and_does_not_jump(self):
        self.turn_on(every_s=10, px=2, at_ms=0)
        self.look(10_000)
        self.assertEqual(self.at(), self.expected(1, 2))
        # the keyboard was busy for 95 s
        self.look(105_000)
        self.assertEqual(self.at(), self.expected(2, 2))
        self.assertEqual(self.lib.t_aligns(), 2)
        # the next one is 10 s after the late look
        self.look(114_000)
        self.assertEqual(self.lib.t_aligns(), 2)
        self.look(115_000)
        self.assertEqual(self.at(), self.expected(3, 2))

    def test_turning_it_off_puts_the_canvas_back_and_turning_it_on_starts_over(self):
        self.turn_on(every_s=10, px=2, at_ms=0)
        for n in range(1, 6):
            self.look(n * 10_000)
        self.assertNotEqual(self.at(), (0, 0))

        self.lib.t_set(SHIFT, 0)
        self.look(60_000)
        self.assertEqual(self.at(), (0, 0))
        count = self.lib.t_aligns()
        self.look(61_000)
        self.assertEqual(self.lib.t_aligns(), count, "it was put back once, not at every look")

        # on again: a whole time before the first step, and the walk starts from the beginning
        self.lib.t_set(SHIFT, 1)
        self.look(100_000)
        self.assertEqual(self.lib.t_aligns(), count)
        self.look(109_000)
        self.assertEqual(self.lib.t_aligns(), count)
        self.look(110_000)
        self.assertEqual(self.at(), self.expected(1, 2))

    def test_a_smaller_distance_counts_at_the_next_look(self):
        self.turn_on(every_s=10, px=4, at_ms=0)
        for n in range(1, 14):
            self.look(n * 10_000)
        x, y = self.at()
        self.assertEqual((x, y), self.expected(13, 4))

        self.lib.t_set(SHIFT_PX, 1)
        self.look(130_000 + 1000)
        self.assertEqual(self.at(), self.expected(13, 1))
        self.assertLessEqual(max(abs(self.lib.t_x()), abs(self.lib.t_y())), 1)

        # no distance: the canvas is where it started
        self.lib.t_set(SHIFT_PX, 0)
        self.look(130_000 + 2000)
        self.assertEqual(self.at(), (0, 0))

    def test_a_time_of_zero_never_moves_it(self):
        self.turn_on(every_s=0, px=2, at_ms=0)
        for n in range(1, 50):
            self.look(n * 100_000)
        self.assertEqual(self.lib.t_aligns(), 0)

    def test_a_new_time_counts_from_the_last_step(self):
        self.turn_on(every_s=60, px=2, at_ms=0)
        self.look(60_000)
        self.assertEqual(self.lib.t_aligns(), 1)
        # the time becomes 5 s: the next step is 5 s after the last one
        self.lib.t_set(SHIFT_EVERY_S, 5)
        self.look(64_000)
        self.assertEqual(self.lib.t_aligns(), 1)
        self.look(65_000)
        self.assertEqual(self.lib.t_aligns(), 2)
        self.assertEqual(self.at(), self.expected(2, 2))


if __name__ == "__main__":
    unittest.main(verbosity=2)
