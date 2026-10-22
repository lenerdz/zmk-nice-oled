#include "picture.h"

#include <stddef.h>

struct geometry {
    /* The displayed picture */
    int dw;
    int dh;
    /* The upright one */
    int uw;
    int uh;
    /* The piece that shows, in the upright picture */
    int cx;
    int cy;
    int cw;
    int ch;
};

static int min_int(int a, int b) { return a < b ? a : b; }
static int max_int(int a, int b) { return a > b ? a : b; }

static void geometry_of(const struct picture_src *src, const struct picture_view *view,
                        struct geometry *g) {
    const int turned = (view->rot & 3) & 1;

    // A quarter of a turn swaps the sides. The displayed picture has the sides of the stored one
    // turned by `rot`, and the upright one has them the other way round.
    g->dw = turned ? src->h : src->w;
    g->dh = turned ? src->w : src->h;
    g->uw = g->dh;
    g->uh = g->dw;

    if (view->crop_w == 0 || view->crop_h == 0) {
        g->cx = 0;
        g->cy = 0;
        g->cw = g->uw;
        g->ch = g->uh;
        return;
    }

    g->cx = min_int((int)view->crop_x, g->uw - 1);
    g->cy = min_int((int)view->crop_y, g->uh - 1);
    g->cw = min_int((int)view->crop_w, g->uw - g->cx);
    g->ch = min_int((int)view->crop_h, g->uh - g->cy);
}

void picture_upright_size(const struct picture_src *src, uint8_t rot, int *w, int *h) {
    const struct picture_view view = {.rot = rot};
    struct geometry g;

    geometry_of(src, &view, &g);
    *w = g.uw;
    *h = g.uh;
}

/** The pixel (i, j) of the stored picture: 1 is lit. */
static int stored_bit(const struct picture_src *src, int i, int j) {
    return (src->bits[j * src->stride + (i >> 3)] >> (7 - (i & 7))) & 1;
}

/**
 * The pixel (a, b) of the displayed picture. The displayed picture is the stored one turned
 * `rot` quarter turns clockwise, so the pixel (i, j) of the stored one lands on
 *
 *   rot 0  (a, b) = (i, j)
 *   rot 1  (a, b) = (h - 1 - j, i)
 *   rot 2  (a, b) = (w - 1 - i, h - 1 - j)
 *   rot 3  (a, b) = (j, w - 1 - i)
 *
 * (w and h are the columns and the rows of the stored picture), and the pixel (a, b) of the
 * displayed one comes from the pixel of the stored one that lands there, which is what the cases
 * below read.
 */
static int displayed_bit(const struct picture_src *src, int rot, int a, int b) {
    switch (rot) {
    case 1:
        return stored_bit(src, b, src->h - 1 - a);
    case 2:
        return stored_bit(src, src->w - 1 - a, src->h - 1 - b);
    case 3:
        return stored_bit(src, src->w - 1 - b, a);
    default:
        return stored_bit(src, a, b);
    }
}

void picture_blit(uint8_t *dst, int dst_w, int dst_h, int dst_stride, int x, int y,
                  const struct picture_src *src, const struct picture_view *view, uint8_t fg,
                  uint8_t bg) {
    if (dst == NULL || src == NULL || view == NULL || src->bits == NULL || src->w == 0 ||
        src->h == 0) {
        return;
    }

    struct geometry g;
    geometry_of(src, view, &g);

    // The piece of the upright picture (u, v) is the piece of the displayed one with
    // a = dw - 1 - v and b = u: the upright picture is the displayed one turned a quarter of a
    // turn counterclockwise.
    int a0 = g.dw - g.cy - g.ch;
    int a1 = g.dw - g.cy;
    int b0 = g.cx;
    int b1 = g.cx + g.cw;

    // Only what falls on the canvas
    a0 = max_int(a0, -x);
    a1 = min_int(a1, dst_w - x);
    b0 = max_int(b0, -y);
    b1 = min_int(b1, dst_h - y);

    const int rot = view->rot & 3;
    const int middle = ((int)fg + (int)bg) / 2;
    const int lit_is_low = fg < bg;

    for (int b = b0; b < b1; b++) {
        uint8_t *row = dst + (size_t)(y + b) * (size_t)dst_stride + x;

        for (int a = a0; a < a1; a++) {
            if (!displayed_bit(src, rot, a, b)) {
                continue;
            }

            if (view->mix == PICTURE_MIX_INVERT) {
                const int was_lit = lit_is_low ? row[a] <= middle : row[a] > middle;
                row[a] = was_lit ? bg : fg;
            } else {
                row[a] = fg;
            }
        }
    }
}
