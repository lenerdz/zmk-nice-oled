#pragma once

#include <lvgl.h>
#include <zmk/events/rgb_matrix_changed.h>

#include "util.h"

/**
 * RGB toast: for a moment after a light command changes something the user can
 * see (effect, on/off, brightness, hue, saturation, animation period or reset),
 * the peripheral screen shows what changed, in two lines of up to
 * LED_TOAST_LINE_LEN - 1 characters.
 */

/**
 * Writes the two lines that announce `ev` (ASCII only, always terminated).
 */
void led_toast_format(const struct zmk_rgb_matrix_changed *ev, char line1[LED_TOAST_LINE_LEN],
                      char line2[LED_TOAST_LINE_LEN]);

/**
 * Draws the two lines of the toast when `state->toast_active`.
 */
void draw_led_toast(lv_obj_t *canvas, const struct status_state *state);
