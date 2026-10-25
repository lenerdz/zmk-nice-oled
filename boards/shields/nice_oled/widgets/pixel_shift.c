#include "pixel_shift.h"

#include <zephyr/kernel.h>

#include <zmk/display_settings.h>

// How often the settings are looked at. It is not the time between two steps of the shift (that is
// KP_DISPLAY_SHIFT_EVERY_S): it is how soon a change in ZMK Studio counts.
#define POLL_MS 1000

// The canvas that moves
static lv_obj_t *shifted;
// How many steps of the walk were taken since the shift was turned on
static uint32_t step;
// When the walk last took a step (k_uptime_get()), or when the shift was turned on
static int64_t last_step_at;
// Whether the shift is on (as the last look at the settings saw it)
static bool running;
// Where the canvas is now, from its place
static int32_t offset_x;
static int32_t offset_y;

static void place(int32_t dx, int32_t dy) {
    if (shifted == NULL || (dx == offset_x && dy == offset_y)) {
        return;
    }

    offset_x = dx;
    offset_y = dy;
    lv_obj_align(shifted, LV_ALIGN_TOP_LEFT, dx, dy);
}

static void poll_cb(lv_timer_t *timer) {
    if (kp_display_setting_get(KP_DISPLAY_SHIFT) == 0) {
        // Off: the canvas goes back to its place, and the walk starts again when it is turned on
        running = false;
        place(0, 0);
        return;
    }

    const int64_t now = k_uptime_get();
    if (!running) {
        // Just turned on: a whole time before the first step, so that turning it on does not
        // move the screen under the eyes at once
        running = true;
        step = 0;
        last_step_at = now;
    }

    const int64_t every_ms = (int64_t)kp_display_setting_get(KP_DISPLAY_SHIFT_EVERY_S) * 1000;
    if (every_ms > 0 && now - last_step_at >= every_ms) {
        // One step, never more: a late look (the keyboard was busy) does not make the screen
        // jump over the squares of the walk
        step++;
        last_step_at = now;
    }

    int32_t dx;
    int32_t dy;
    kp_display_shift_offset(step, (int32_t)kp_display_setting_get(KP_DISPLAY_SHIFT_PX), &dx, &dy);
    place(dx, dy);
}

void pixel_shift_init(lv_obj_t *container, lv_obj_t *canvas, lv_color_t background) {
    shifted = canvas;

    // When the canvas moves, the container shows where it left: the background of the screen,
    // with nothing around it. (Until now the canvas covered all of it, so how the container
    // looked did not matter.)
    lv_obj_set_style_bg_color(container, background, 0);
    lv_obj_set_style_bg_opa(container, LV_OPA_COVER, 0);
    lv_obj_set_style_border_width(container, 0, 0);
    lv_obj_set_style_radius(container, 0, 0);

    lv_timer_create(poll_cb, POLL_MS, NULL);
}
