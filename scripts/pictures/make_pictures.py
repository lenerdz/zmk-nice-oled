#!/usr/bin/env python3
"""Draws the pictures for the right screen of the Corne that the OLED layout of the lenerdz
fork can pick (the kinds that come after the ones of zmk-nice-oled), and writes them as the
LVGL C files of the shield.

    python scripts/pictures/make_pictures.py                 # list what there is
    python scripts/pictures/make_pictures.py --preview DIR   # PNG sheets to look at, no files written
    python scripts/pictures/make_pictures.py --write         # the C files, pictures.h, pictures.json
    python scripts/pictures/make_pictures.py --check         # fails if the files are not what --write makes
    python scripts/pictures/make_pictures.py --check --module <zmk-rgb-matrix>
                                                             # also: the enum of the module has them

What it makes (all of it under boards/shields/nice_oled):

* assets/pictures/<name>.c: the frames of one picture, in the format of the other assets of the
  shield (LVGL, 1 bit per pixel, a palette of two colors, the same #if for the inverted build).
* widgets/pictures.h: the declarations of the frames, one list of frames per picture and the
  table PICTURES(X) that widgets/animation.c turns into its table of kinds.
* assets/pictures/pictures.json: the list, with the kind number of each (for the app of ZMK
  Studio, and for whoever writes the READMEs).

The pictures are drawn upright, as the screen is looked at, and 32 pixels wide (the panel is
32 pixels wide). The files hold them turned a quarter of a turn clockwise, like the other
pictures of the right screen, because the canvas of the widgets is turned for the panel after it
is drawn: widgets/picture.c puts them on the canvas after that, and turns them back.

The kinds are numbered from FIRST_KIND, in the order of PICTURES below: the pictures of each batch
of BATCHES (its animations, then its stills), the batches one after the other. The number is what
the keyboard saves in its memory: ONLY ADD pictures at the end (a new batch, with its own
animations2-like and stills2-like files), never reorder, and add the same name to
enum kp_oled_anim_kind (include/zmk/display_settings.h of zmk-rgb-matrix) with the same number,
and raise KP_OLED_ANIM_KIND_COUNT. The first batch (animations.py, stills.py) is the kinds 7 to
25, the second (animations2.py, stills2.py) the kinds 26 to 65. A name cannot repeat, and it
cannot be one of the kinds of zmk-nice-oled either (crystal, cat, head, spaceman, pokemon, vim,
vip_marcos), because the enum is made of the names.

A picture is not removed from the list, because that would move the numbers of the ones after
it: its entry in STILLS becomes None. The kind is then retired: it keeps its place and its name
in the enum, no file or frames are made for it, it is not in the table PICTURES(X) of pictures.h
(so widgets/animation.c has an empty entry for it), and pictures.json lists it under "retired".
The module (kp_oled_anim_kind_retired() in display_settings.h) must list it as retired too, so
that the keyboard does not accept it as a setting and forgets one that it had saved; --check
--module tests that.

Needs Python 3 and numpy; --preview also needs Pillow. The drawing does not use random numbers
from numpy, so the pictures do not change with its version.
"""
import argparse
import json
import os
import re
import sys
import textwrap

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import animations  # noqa: E402
import animations2  # noqa: E402
import stills  # noqa: E402
import stills2  # noqa: E402
from pixels import WIDTH  # noqa: E402

SHIELD = os.path.normpath(os.path.join(HERE, "..", "..", "boards", "shields", "nice_oled"))
ASSETS = os.path.join(SHIELD, "assets", "pictures")
HEADER = os.path.join(SHIELD, "widgets", "pictures.h")
MANIFEST = os.path.join(ASSETS, "pictures.json")

# The kind of the first picture here: the module has the kinds before it (KP_OLED_ANIM_CRYSTAL 0
# up to KP_OLED_ANIM_VIP_MARCOS 6)
FIRST_KIND = 7

# The kinds that zmk-nice-oled itself has (KP_OLED_ANIM_CRYSTAL 0 to KP_OLED_ANIM_VIP_MARCOS 6):
# a picture cannot take one of these names
NICE_OLED_KINDS = ("crystal", "cat", "head", "spaceman", "pokemon", "vim", "vip_marcos")

# Batches of pictures, in the order of their kinds; a new batch goes at the end. Each one is the
# table of its animations, (function, milliseconds of one cycle) by name, and the one of its
# stills, a function by name.
BATCHES = [
    (animations.ANIMATIONS, stills.STILLS),  # the kinds 7 to 25
    (animations2.ANIMATIONS, stills2.STILLS),  # the kinds 26 to 65
]

# The order is the number of the kind. A still whose function is None was taken out ("retired"):
# it keeps its number and its name, and nothing is made for it
PICTURES = []
for _animations, _stills in BATCHES:
    for _name, (_fn, _ms) in _animations.items():
        PICTURES.append((_name, "animation", _fn, _ms))
    for _name, _fn in _stills.items():
        PICTURES.append((_name, "still" if _fn is not None else "retired", _fn, 0))

_names = [p[0] for p in PICTURES]
for _name in _names:
    if _names.count(_name) > 1:
        sys.exit(f"{_name}: the name is in two batches")
    if _name in NICE_OLED_KINDS:
        sys.exit(f"{_name}: that is the name of a kind of zmk-nice-oled")


def frames_of(entry):
    """The upright frames of a picture, as arrays of rows of 0 and 1 (none for a retired one)."""
    name, kind, fn, ms = entry
    if kind == "retired":
        return []
    result = fn()
    frames = list(result) if kind == "animation" else [result]
    if not frames:
        sys.exit(f"{name}: no frames")
    shape = frames[0].shape
    for i, frame in enumerate(frames):
        if frame.shape != shape:
            sys.exit(f"{name}: frame {i} is {frame.shape}, the first is {shape}")
        if frame.shape[1] != WIDTH:
            sys.exit(f"{name}: {frame.shape[1]} pixels wide, it has to be {WIDTH}")
        if frame.max() > 1:
            sys.exit(f"{name}: frame {i} has values above 1")
    if shape[0] > 160 or shape[0] < 1:
        sys.exit(f"{name}: {shape[0]} pixels tall (1 to 160)")
    if kind == "still" and len(frames) != 1:
        sys.exit(f"{name}: a still has one frame")
    if kind == "animation" and len(frames) < 2:
        sys.exit(f"{name}: an animation has two frames or more")
    return frames


def stored(frame):
    """What the file holds: the upright picture turned a quarter of a turn clockwise."""
    return np.rot90(frame, -1)


def pack(frame):
    """The bytes of the rows of an array of 0 and 1: 1 bit per pixel, the leftmost in bit 7."""
    h, w = frame.shape
    stride = (w + 7) // 8
    out = bytearray(stride * h)
    for y in range(h):
        for x in range(w):
            if frame[y, x]:
                out[y * stride + x // 8] |= 0x80 >> (x % 8)
    return bytes(out)


def c_name(name, index, frames):
    return f"pic_{name}_{index:02d}" if len(frames) > 1 else f"pic_{name}"


def c_bytes(data):
    lines = []
    for i in range(0, len(data), 16):
        lines.append("  " + ", ".join(f"0x{b:02x}" for b in data[i : i + 16]))
    return ",\n".join(lines)


def c_file(entry, frames):
    name, kind, _fn, _ms = entry
    first = stored(frames[0])
    h, w = first.shape
    out = [
        "/* GENERATED by scripts/pictures/make_pictures.py: do not edit, run the script again. */",
        f"/* {name}: {'an animation of ' + str(len(frames)) + ' frames' if kind == 'animation' else 'a still image'}, "
        f"{frames[0].shape[1]} x {frames[0].shape[0]} pixels as it is looked at (the data is turned "
        f"a quarter of a turn clockwise: {w} x {h}). */",
        "#include <lvgl.h>",
        "",
        "#ifndef LV_ATTRIBUTE_MEM_ALIGN",
        "#define LV_ATTRIBUTE_MEM_ALIGN",
        "#endif",
        "",
    ]
    for i, frame in enumerate(frames):
        cname = c_name(name, i, frames)
        attr = f"LV_ATTRIBUTE_IMG_{cname.upper()}"
        data = pack(stored(frame))
        out += [
            f"#ifndef {attr}",
            f"#define {attr}",
            "#endif",
            "",
            f"static const LV_ATTRIBUTE_MEM_ALIGN {attr} uint8_t {cname}_map[] = {{",
            "#if CONFIG_NICE_OLED_WIDGET_INVERTED",
            "  /*Palette: Idx 0: Black (#if), Idx 1: White (#if)*/",
            "  0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff,",
            "#else",
            "  /*Palette: Idx 0: White (#else), Idx 1: Black (#else)*/",
            "  0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0xff,",
            "#endif",
            "",
            "  /*Pixel data (1 bit per pixel, 0=palette idx 0, 1=palette idx 1)*/",
            c_bytes(data),
            "};",
            "",
            f"const lv_img_dsc_t {cname} = {{",
            "  .header.cf = LV_COLOR_FORMAT_I1,",
            f"  .header.w = {w},",
            f"  .header.h = {h},",
            f"  .data_size = {8 + len(data)},",
            f"  .data = {cname}_map,",
            "};",
            "",
        ]
    return "\n".join(out)


def header_file(all_frames):
    out = [
        "/* GENERATED by scripts/pictures/make_pictures.py: do not edit, run the script again.",
        " *",
        " * The pictures of the right screen that come after the ones of zmk-nice-oled (the OLED",
        " * layout of the lenerdz fork, CONFIG_KEYPAW_OLED_LAYOUT). widgets/animation.c includes this",
        " * file once, and builds its table of kinds from PICTURES(). A retired kind (a picture that",
        " * was taken out) has no frames and no row here: its entry of that table stays empty. */",
        "#ifndef NICE_OLED_PICTURES_H",
        "#define NICE_OLED_PICTURES_H",
        "",
        "#include <lvgl.h>",
        "",
    ]
    for entry, frames in all_frames:
        for i in range(len(frames)):
            out.append(f"LV_IMG_DECLARE({c_name(entry[0], i, frames)});")
        out.append("")
    for entry, frames in all_frames:
        name = entry[0]
        refs = ", ".join(f"&{c_name(name, i, frames)}" for i in range(len(frames)))
        body = textwrap.fill(refs + ",", width=96, initial_indent="    ", subsequent_indent="    ")
        out.append(f"static const lv_img_dsc_t *const pic_{name}_imgs[] = {{\n{body}\n}};")
    out += [
        "",
        "// X(KIND, name, cycle in ms): KIND is the end of the name of KP_OLED_ANIM_<KIND> of",
        "// zmk-rgb-matrix, in the order of the numbers of the kinds",
        "#define PICTURES(X) \\",
    ]
    rows = []
    for entry, frames in all_frames:
        name, _kind, _fn, ms = entry
        rows.append(f"    X({name.upper()}, pic_{name}, {ms})")
    out.append(" \\\n".join(rows))
    out += ["", "#endif /* NICE_OLED_PICTURES_H */", ""]
    return "\n".join(out)


def manifest_file(all_frames):
    pictures = []
    retired = []
    for number, (entry, frames) in enumerate(all_frames):
        name, kind, _fn, ms = entry
        if kind == "retired":
            retired.append(
                {
                    "name": name,
                    "kind": FIRST_KIND + number,
                    "enum": f"KP_OLED_ANIM_{name.upper()}",
                }
            )
            continue
        h, w = frames[0].shape
        pictures.append(
            {
                "name": name,
                "kind": FIRST_KIND + number,
                "enum": f"KP_OLED_ANIM_{name.upper()}",
                "type": kind,
                "frames": len(frames),
                "width": w,
                "height": h,
                "cycle_ms": ms,
                "file": f"assets/pictures/{name}.c",
                "bytes": sum(8 + len(pack(stored(f))) for f in frames),
            }
        )
    return json.dumps(
        {
            "generator": "scripts/pictures/make_pictures.py",
            "first_kind": FIRST_KIND,
            "kind_count": FIRST_KIND + len(all_frames),
            "total_bytes": sum(p["bytes"] for p in pictures),
            "pictures": pictures,
            # Taken out: the kind keeps its number and its name, and there is no picture
            "retired": retired,
        },
        indent=2,
    ) + "\n"


def outputs():
    """path -> text of every file that --write makes."""
    all_frames = [(entry, frames_of(entry)) for entry in PICTURES]
    # A retired picture has no frames, so no file and no row in the header
    live = [(entry, frames) for entry, frames in all_frames if frames]
    files = {os.path.join(ASSETS, f"{entry[0]}.c"): c_file(entry, frames) for entry, frames in live}
    files[HEADER] = header_file(live)
    files[MANIFEST] = manifest_file(all_frames)
    return files, all_frames


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def check_module(module, all_frames):
    """The enum of zmk-rgb-matrix has every picture with its number, and the count."""
    path = os.path.join(module, "include", "zmk", "display_settings.h")
    text = open(path, encoding="utf-8").read()
    body = re.search(r"enum kp_oled_anim_kind\s*\{(.*?)\};", text, re.S).group(1)
    found = {m.group(1): int(m.group(2)) for m in re.finditer(r"(KP_OLED_ANIM_\w+)\s*=\s*(\d+)", body)}
    count = int(re.search(r"#define\s+KP_OLED_ANIM_KIND_COUNT\s+(\d+)", text).group(1))
    problems = []
    for number, (entry, _frames) in enumerate(all_frames):
        want = f"KP_OLED_ANIM_{entry[0].upper()}"
        if found.get(want) != FIRST_KIND + number:
            problems.append(f"{want}: the enum has {found.get(want)}, it has to be {FIRST_KIND + number}")
    if count != FIRST_KIND + len(all_frames):
        problems.append(f"KP_OLED_ANIM_KIND_COUNT is {count}, it has to be {FIRST_KIND + len(all_frames)}")

    # kp_oled_anim_kind_retired(): the kinds that it says are retired are the retired pictures
    # here, plus the two stills that zmk-nice-oled itself had (vim, vip_marcos), and no other
    fn = re.search(r"kp_oled_anim_kind_retired\([^)]*\)\s*\{(.*?)\n\}", text, re.S)
    if fn is None:
        problems.append("kp_oled_anim_kind_retired() is not in the module")
        return problems
    body = fn.group(1)
    said = {found[n] for n in re.findall(r"case\s+(KP_OLED_ANIM_\w+)\s*:", body) if n in found}
    for lo, hi in re.findall(r">=\s*(KP_OLED_ANIM_\w+)\s*&&\s*kind\s*<=\s*(KP_OLED_ANIM_\w+)", body):
        if lo in found and hi in found:
            said |= set(range(found[lo], found[hi] + 1))
    want = {FIRST_KIND + number for number, (entry, _f) in enumerate(all_frames) if entry[1] == "retired"}
    want |= {found["KP_OLED_ANIM_VIM"], found["KP_OLED_ANIM_VIP_MARCOS"]}
    for kind in sorted(want - said):
        problems.append(f"kind {kind} is retired here, kp_oled_anim_kind_retired() does not say so")
    for kind in sorted(said - want):
        problems.append(f"kind {kind} is retired in kp_oled_anim_kind_retired(), it is not here")
    return problems


def preview(directory, all_frames):
    from PIL import Image

    lit, off, back = (0xDF, 0xF1, 0xFF), (4, 7, 12), (40, 50, 70)
    scale, gap = 4, 3
    os.makedirs(directory, exist_ok=True)

    def tile(frame):
        h, w = frame.shape
        img = Image.new("RGB", (w, h), off)
        px = img.load()
        for y in range(h):
            for x in range(w):
                if frame[y, x]:
                    px[x, y] = lit
        return img.resize((w * scale, h * scale), Image.NEAREST)

    still_tiles = []
    for entry, frames in all_frames:
        name = entry[0]
        if not frames:
            # Retired: nothing to look at
            continue
        if len(frames) == 1:
            still_tiles.append(tile(frames[0]))
            continue
        columns = min(8, len(frames))
        rows = (len(frames) + columns - 1) // columns
        h, w = frames[0].shape
        sheet = Image.new("RGB", (columns * (w * scale + gap) + gap, rows * (h * scale + gap) + gap), back)
        for i, frame in enumerate(frames):
            sheet.paste(tile(frame), (gap + (i % columns) * (w * scale + gap), gap + (i // columns) * (h * scale + gap)))
        sheet.save(os.path.join(directory, f"{name}.png"))
        print(f"{name}.png: {len(frames)} frames")

    if still_tiles:
        height = max(t.height for t in still_tiles)
        width = sum(t.width + gap for t in still_tiles) + gap
        sheet = Image.new("RGB", (width, height + 2 * gap), back)
        x = gap
        for t in still_tiles:
            sheet.paste(t, (x, gap))
            x += t.width + gap
        sheet.save(os.path.join(directory, "stills.png"))
        print(f"stills.png: {len(still_tiles)} pictures")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--preview", metavar="DIR", help="write PNG sheets of the pictures to DIR")
    parser.add_argument("--write", action="store_true", help="write the C files, pictures.h and pictures.json")
    parser.add_argument("--check", action="store_true", help="fail if the files are not what --write makes")
    parser.add_argument("--module", metavar="DIR", help="with --check: zmk-rgb-matrix, to check its enum")
    args = parser.parse_args()

    files, all_frames = outputs()

    if args.preview:
        preview(args.preview, all_frames)

    if args.write:
        for path, text in files.items():
            write(path, text)
        # Files of pictures that are not in the list any more
        known = {os.path.basename(p) for p in files}
        for name in sorted(os.listdir(ASSETS)):
            if name.endswith(".c") and name not in known:
                os.remove(os.path.join(ASSETS, name))
                print(f"removed {name}")
        print(f"wrote {len(files)} files")

    if args.check:
        problems = []
        for path, text in files.items():
            try:
                current = open(path, encoding="utf-8", newline="").read().replace("\r\n", "\n")
            except FileNotFoundError:
                problems.append(f"{os.path.relpath(path, SHIELD)} is missing")
                continue
            if current != text:
                problems.append(f"{os.path.relpath(path, SHIELD)} is not what the script makes")
        if args.module:
            problems += check_module(args.module, all_frames)
        for p in problems:
            print("FAIL:", p)
        if problems:
            sys.exit(1)
        print(f"ok: {len(files)} files are what the script makes")

    if not (args.preview or args.write or args.check):
        total = 0
        print(f"{'kind':>4}  {'name':10} {'type':9} {'frames':>6}  {'size':>7}  {'ms':>5}  {'bytes':>6}")
        for number, (entry, frames) in enumerate(all_frames):
            name, kind, _fn, ms = entry
            if not frames:
                print(f"{FIRST_KIND + number:>4}  {name:10} {kind:9}")
                continue
            h, w = frames[0].shape
            size = sum(8 + len(pack(stored(f))) for f in frames)
            total += size
            print(f"{FIRST_KIND + number:>4}  {name:10} {kind:9} {len(frames):>6}  {w:>3}x{h:<3}  {ms:>5}  {size:>6}")
        print(f"{'':>4}  {'total':10} {'':9} {'':>6}  {'':>7}  {'':>5}  {total:>6}")


if __name__ == "__main__":
    main()
