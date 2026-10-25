#pragma once

#include <lvgl.h>

/**
 * Anti burn-in for the OLED: the pixel shift of the display settings of zmk-rgb-matrix
 * (CONFIG_KEYPAW_DISPLAY_SETTINGS; KP_DISPLAY_SHIFT, KP_DISPLAY_SHIFT_EVERY_S and
 * KP_DISPLAY_SHIFT_PX, which ZMK Studio edits).
 *
 * An OLED that shows the same picture for hours ages the lit pixels faster than the dark ones.
 * With the shift on, everything on the screen (the widgets, and the animation or image) moves
 * one pixel, every KP_DISPLAY_SHIFT_EVERY_S seconds, along a short walk (kp_display_shift_offset():
 * up to KP_DISPLAY_SHIFT_PX pixels to each side), so the edges of the text and of the picture
 * do not stay on the same pixels. What is pushed out of the screen on one side is lost for a
 * while, and a margin of the background color opens on the other.
 *
 * `canvas` is the canvas of the status screen and `container` the object it lies in: the canvas is
 * the one that moves, inside the container, so the widgets that are its children move with it.
 * `background` is the color of the screen (the margin that opens when the canvas moves is of this
 * color). Call it once, after the canvas has its buffer. It sets a timer of LVGL that looks at
 * the settings every second, so that a change in ZMK Studio counts at once (the shift off puts
 * the canvas back in its place).
 */
void pixel_shift_init(lv_obj_t *container, lv_obj_t *canvas, lv_color_t background);
