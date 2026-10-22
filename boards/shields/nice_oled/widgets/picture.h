#pragma once

/**
 * A picture of the right screen (an animation frame or a still image: 1 bit per pixel) put on the
 * canvas after the canvas was turned for the panel, as the OLED layout settings of zmk-rgb-matrix
 * say: which way it is turned, which piece of it shows, and how it mixes with the widgets that are
 * already on the canvas.
 *
 * Plain C, with no LVGL and no Zephyr, so that tests/picture/test_picture.py runs it on a PC.
 *
 * The pictures of the shield are stored turned a quarter of a turn clockwise (the canvas is
 * rotated by 270 degrees, that is a quarter of a turn counterclockwise, before the panel gets it),
 * and the canvas that this code draws on is the turned one: 160 pixels wide and 68 tall, of which
 * the panel shows the 128 x 32 at the top left. So three pictures are talked about here:
 *
 *   stored      the pixels of the file (struct picture_src), w columns by h rows
 *   upright     the picture as it is looked at when the keyboard is on the desk: the stored one
 *               turned a quarter of a turn counterclockwise, h columns by w rows, and then turned
 *               by `rot` quarter turns clockwise (the settings talk about this one: the crop is a
 *               piece of it)
 *   displayed   the upright one turned a quarter of a turn clockwise again: what is put on the
 *               canvas, with its top left corner at (x, y)
 *
 * With rot 0 the displayed picture is the stored one.
 **/

#include <stdint.h>

/** How a lit pixel of the picture mixes with what is on the canvas. */
enum picture_mix {
    /** The pixel is lit, whatever was there: widgets and picture add up. */
    PICTURE_MIX_ADD = 0,
    /** The pixel flips what was there: a widget over the picture shows in reverse. */
    PICTURE_MIX_INVERT = 1,
};

/** The pixels of a stored picture. */
struct picture_src {
    /** The first row; the leftmost pixel of a row is the most significant bit of its first byte. */
    const uint8_t *bits;
    /** Columns and rows of the stored picture. */
    uint16_t w;
    uint16_t h;
    /** Bytes of a row. */
    uint16_t stride;
};

/** What the settings say about the picture. */
struct picture_view {
    /** Quarter turns clockwise, 0 to 3 (more is taken modulo 4). */
    uint8_t rot;
    /**
     * The piece of the upright picture that shows. A width or a height of 0 is all of it; what
     * goes past the picture is cut off.
     */
    uint16_t crop_x;
    uint16_t crop_y;
    uint16_t crop_w;
    uint16_t crop_h;
    /** A value of enum picture_mix. */
    uint8_t mix;
};

/** The size of the upright picture: what the crop is a piece of. */
void picture_upright_size(const struct picture_src *src, uint8_t rot, int *w, int *h);

/**
 * Puts the lit pixels of the piece of the picture that shows on a canvas of 8 bits per pixel.
 *
 *   dst, dst_w, dst_h, dst_stride  the canvas: pixels, columns, rows, bytes of a row
 *   x, y                           where the top left corner of the displayed picture is (the
 *                                  whole of it, not only the piece); what falls outside the
 *                                  canvas is not drawn
 *   fg, bg                         the value of a lit pixel and the one of an unlit pixel of the
 *                                  canvas (0 and 255 with the ink in black, the other way round
 *                                  with CONFIG_NICE_OLED_WIDGET_INVERTED)
 *
 * The unlit pixels of the picture do not touch the canvas.
 **/
void picture_blit(uint8_t *dst, int dst_w, int dst_h, int dst_stride, int x, int y,
                  const struct picture_src *src, const struct picture_view *view, uint8_t fg,
                  uint8_t bg);
