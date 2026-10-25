#!/usr/bin/env python3
"""Tests of the pictures that scripts/pictures/make_pictures.py makes for the right screen: the
files in the repository are what the script makes, the C files are what the shield reads (a
compiler reads the same bytes that a parser of the text does, and they turn back into the
pictures the script drew), and the list is consistent.

    python tests/picture/test_generated.py

needs numpy and Pillow, and a C compiler: `cc`, or the one of the `ziglang` package
(`python -m ziglang cc`) when there is none.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SHIELD = ROOT / "boards" / "shields" / "nice_oled"
sys.path.insert(0, str(ROOT / "scripts" / "pictures"))

import make_pictures as mp  # noqa: E402

# The order of the pictures is the number of the kind that the keyboard saves in its memory, from
# FIRST_KIND on. This is what exists: it only grows at the end, a name is never moved or removed
# (kinds 7 to 25 are the first batch, 26 to 65 the second). A name stays in the list when its
# picture is taken out (RETIRED): the kind keeps its number
KINDS = """
equalizer radar heartbeat rain cube atom helix warp sonar bounce flame
mountains skyline circuit alien heart keyboard pulsar rocket
waterfall lava lightning snow jellyfish tetris pong invaders pacman life plasma spiral newton
gears hourglass windmill fireworks ufo eye keywave
coffee cactus lighthouse moon_cat robot planet castle tree skull sword key antenna potion
sailboat compass crown cassette floppy phases mushroom
""".split()

# The still images that are left, and the ones that were taken out (22 of the 28 that the
# generator drew; vim and vip_marcos, the two of zmk-nice-oled, are retired in the module too)
STILLS_LEFT = ["mountains", "skyline", "circuit", "keyboard", "moon_cat", "planet"]
RETIRED = """
alien heart pulsar rocket
coffee cactus lighthouse robot castle tree skull sword key antenna potion
sailboat compass crown cassette floppy phases mushroom
""".split()

STUB = """\
#ifndef LVGL_STUB_H
#define LVGL_STUB_H
#include <stddef.h>
#include <stdint.h>
#define LV_COLOR_FORMAT_I1 1
typedef struct {
    struct { uint32_t cf; uint32_t w; uint32_t h; } header;
    uint32_t data_size;
    const uint8_t *data;
} lv_img_dsc_t;
#define LV_IMG_DECLARE(name) extern const lv_img_dsc_t name;
#define ARRAY_SIZE(a) (sizeof(a) / sizeof((a)[0]))
#endif
"""

DUMP = """\
#include <stdio.h>
#include <lvgl.h>
#include "pictures.h"

#define DUMP(KIND, prefix, ms) \\
    for (size_t i = 0; i < ARRAY_SIZE(prefix##_imgs); i++) { \\
        const lv_img_dsc_t *d = prefix##_imgs[i]; \\
        printf("%s %zu %u %u %u %u %u ", #KIND, i, (unsigned)(ms), (unsigned)ARRAY_SIZE(prefix##_imgs), \\
               (unsigned)d->header.w, (unsigned)d->header.h, (unsigned)d->data_size); \\
        for (uint32_t k = 0; k < d->data_size; k++) { \\
            printf("%02x", d->data[k]); \\
        } \\
        printf("\\n"); \\
    }

int main(void) {
    PICTURES(DUMP)
    return 0;
}
"""


def compiler():
    cc = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if cc:
        return [cc]
    return [sys.executable, "-m", "ziglang", "cc"]


def upright_of(stored):
    """The picture as the app shows it: convert.py turns PIL's counterclockwise quarter turn."""
    h, w = stored.shape
    img = Image.new("L", (w, h), 0)
    img.putdata([255 if v else 0 for v in stored.reshape(-1)])
    return (np.array(img.rotate(90, expand=True)) > 0).astype(np.uint8)


def parse_c(path):
    """The images of a C file of the shield, read from its text: name -> (w, h, data_size, bytes
    of both branches of the palette and the pixels)."""
    text = Path(path).read_text(encoding="utf-8")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    arrays = {}
    for m in re.finditer(r"uint8_t\s+(\w+)\[\]\s*=\s*\{(.*?)\};", text, re.S):
        body = "\n".join(l for l in m.group(2).splitlines() if not l.strip().startswith("#"))
        arrays[m.group(1)] = bytes(int(x, 16) for x in re.findall(r"0x([0-9a-fA-F]{2})", body))
    images = {}
    for m in re.finditer(r"const\s+lv_img_dsc_t\s+(\w+)\s*=\s*\{(.*?)\};", text, re.S):
        body = m.group(2)
        images[m.group(1)] = (
            int(re.search(r"\.header\.w\s*=\s*(\d+)", body).group(1)),
            int(re.search(r"\.header\.h\s*=\s*(\d+)", body).group(1)),
            int(re.search(r"\.data_size\s*=\s*(\d+)", body).group(1)),
            arrays[re.search(r"\.data\s*=\s*(\w+)", body).group(1)],
        )
    return images


def rows_of(pixels, w, h):
    stride = (w + 7) // 8
    rows = np.zeros((h, w), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            rows[y, x] = (pixels[y * stride + x // 8] >> (7 - x % 8)) & 1
    return rows


class GeneratedPictures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.all_frames = mp.outputs()
        # What has a picture (a retired kind has none: no frames, no file)
        cls.live = [(entry, frames) for entry, frames in cls.all_frames if frames]
        cls.manifest = json.loads(Path(mp.MANIFEST).read_text(encoding="utf-8"))
        cls.kind_of = {p["name"]: p["kind"] for p in cls.manifest["pictures"]}
        cls.kind_of.update({r["name"]: r["kind"] for r in cls.manifest["retired"]})

    def test_the_files_are_what_the_script_makes(self):
        for path, text in self.files.items():
            current = Path(path).read_text(encoding="utf-8").replace("\r\n", "\n")
            self.assertEqual(current, text, f"{path}: run make_pictures.py --write")

    def test_no_stray_files(self):
        known = {Path(p).name for p in self.files if Path(p).parent == Path(mp.ASSETS)}
        found = {p.name for p in Path(mp.ASSETS).iterdir()}
        self.assertEqual(found, known)

    def test_every_picture_is_32_pixels_wide_and_not_empty(self):
        for entry, frames in self.all_frames:
            for i, frame in enumerate(frames):
                self.assertEqual(frame.shape[1], 32, entry[0])
                lit = int(frame.sum())
                self.assertGreater(lit, 8, f"{entry[0]} frame {i} is almost empty")
                self.assertLess(lit, frame.size * 0.9, f"{entry[0]} frame {i} is almost full")

    def test_animations_move_and_stills_are_one_picture(self):
        for entry, frames in self.all_frames:
            name, kind, _fn, ms = entry
            if kind == "retired":
                self.assertEqual(frames, [], name)
                self.assertEqual(ms, 0, name)
                continue
            if kind == "still":
                self.assertEqual(len(frames), 1, name)
                self.assertEqual(ms, 0, name)
                continue
            self.assertGreaterEqual(len(frames), 8, name)
            self.assertGreaterEqual(ms // len(frames), 20, f"{name}: a frame under 20 ms")
            for i in range(len(frames)):
                nxt = frames[(i + 1) % len(frames)]
                self.assertFalse(np.array_equal(frames[i], nxt), f"{name}: frame {i} and the next are equal")

    def test_the_kinds_that_exist_never_change_and_a_new_picture_goes_at_the_end(self):
        names = [entry[0] for entry, _frames in self.all_frames]
        self.assertEqual(names[: len(KINDS)], KINDS)
        self.assertEqual(mp.FIRST_KIND, 7)
        self.assertEqual(self.kind_of["flame"], 17)
        self.assertEqual(self.kind_of["rocket"], 25)
        self.assertEqual(self.kind_of["waterfall"], 26)
        self.assertEqual(self.kind_of["mushroom"], 65)
        self.assertEqual(self.manifest["kind_count"], 66)
        for forbidden in mp.NICE_OLED_KINDS:
            self.assertNotIn(forbidden, names)

    def test_only_six_still_images_are_left_and_the_others_are_retired_with_their_numbers(self):
        stills = [entry[0] for entry, _frames in self.live if entry[1] == "still"]
        self.assertEqual(stills, STILLS_LEFT)
        retired = [entry[0] for entry, frames in self.all_frames if entry[1] == "retired"]
        self.assertEqual(retired, RETIRED)
        self.assertEqual([r["name"] for r in self.manifest["retired"]], RETIRED)
        # a retired kind keeps the place and the name of its picture, and the ones that stay do
        # not move
        for name, kind in {
            "mountains": 18,
            "skyline": 19,
            "circuit": 20,
            "alien": 21,
            "heart": 22,
            "keyboard": 23,
            "pulsar": 24,
            "rocket": 25,
            "coffee": 46,
            "moon_cat": 49,
            "robot": 50,
            "planet": 51,
            "castle": 52,
            "mushroom": 65,
        }.items():
            self.assertEqual(self.kind_of[name], kind, name)
        for r in self.manifest["retired"]:
            self.assertEqual(r["enum"], "KP_OLED_ANIM_" + r["name"].upper())
            # no file is left for it
            self.assertFalse((Path(mp.ASSETS) / f"{r['name']}.c").exists(), r["name"])

    def test_the_kinds_are_numbered_in_order_after_the_ones_of_nice_oled(self):
        # the pictures that exist and the retired ones together are every kind, in order
        every = sorted(self.kind_of.values())
        self.assertEqual(every, list(range(mp.FIRST_KIND, mp.FIRST_KIND + len(every))))
        self.assertEqual(self.manifest["kind_count"], mp.FIRST_KIND + len(every))
        kinds = [p["kind"] for p in self.manifest["pictures"]]
        self.assertEqual(kinds, sorted(kinds))
        names = [p["name"] for p in self.manifest["pictures"]] + [r["name"] for r in self.manifest["retired"]]
        self.assertEqual(len(names), len(set(names)))
        # the sizes of the manifest are the ones of the pictures
        for p, (entry, frames) in zip(self.manifest["pictures"], self.live):
            self.assertEqual(p["name"], entry[0])
            self.assertEqual((p["frames"], p["width"], p["height"]), (len(frames), 32, frames[0].shape[0]))

    def test_the_text_of_the_c_files_turns_back_into_the_pictures(self):
        for entry, frames in self.live:
            images = parse_c(Path(mp.ASSETS) / f"{entry[0]}.c")
            self.assertEqual(len(images), len(frames), entry[0])
            for i, frame in enumerate(frames):
                name = mp.c_name(entry[0], i, frames)
                w, h, size, data = images[name]
                stride = (w + 7) // 8
                # what is stored is the picture turned a quarter of a turn clockwise
                self.assertEqual((w, h), (frame.shape[0], frame.shape[1]), name)
                self.assertEqual(size, 8 + stride * h, name)
                self.assertEqual(len(data), 16 + stride * h, name)
                stored = rows_of(data[16:], w, h)
                self.assertTrue(np.array_equal(upright_of(stored), frame), f"{name} does not turn back")

    def test_a_compiler_reads_the_same_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "lvgl.h").write_text(STUB)
            (tmp / "dump.c").write_text(DUMP)
            sources = sorted(str(p) for p in Path(mp.ASSETS).glob("*.c"))
            dumps = {}
            for inverted in (0, 1):
                exe = tmp / f"dump{inverted}.exe"
                subprocess.run(
                    compiler()
                    + [
                        "-Wall",
                        "-Werror",
                        f"-DCONFIG_NICE_OLED_WIDGET_INVERTED={inverted}",
                        f"-I{tmp}",
                        f"-I{SHIELD / 'widgets'}",
                        "-o",
                        str(exe),
                        str(tmp / "dump.c"),
                    ]
                    + sources,
                    check=True,
                )
                out = subprocess.run([str(exe)], check=True, capture_output=True, text=True).stdout
                dumps[inverted] = [line.split() for line in out.splitlines()]

        by_kind = {}
        for fields in dumps[0]:
            by_kind.setdefault(fields[0], []).append(fields)
        # a retired kind has no row in PICTURES(X)
        self.assertEqual(list(by_kind), [e[0].upper() for e, _ in self.live])

        for (entry, frames), (kind, rows) in zip(self.live, by_kind.items()):
            self.assertEqual(len(rows), len(frames), kind)
            for i, fields in enumerate(rows):
                _kind, index, ms, count, w, h, size, hexdata = fields
                self.assertEqual((int(index), int(ms), int(count)), (i, entry[3], len(frames)), kind)
                data = bytes.fromhex(hexdata)
                self.assertEqual(len(data), int(size), kind)
                self.assertEqual(int(size), 8 + ((int(w) + 7) // 8) * int(h), kind)
                self.assertEqual(data[:8], bytes([0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0xFF]), kind)
                stored = rows_of(data[8:], int(w), int(h))
                self.assertTrue(np.array_equal(upright_of(stored), frames[i]), f"{kind} frame {i}")

        # the build that is inverted has the other palette, and the same pixels
        for plain, inverted in zip(dumps[0], dumps[1]):
            a, b = bytes.fromhex(plain[7]), bytes.fromhex(inverted[7])
            self.assertEqual(b[:8], bytes([0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]))
            self.assertEqual(a[8:], b[8:])


if __name__ == "__main__":
    unittest.main(verbosity=2)
