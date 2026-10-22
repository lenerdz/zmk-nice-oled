#pragma once

#include <zephyr/kernel.h>

/**
 * OLED layout
 *
 * With CONFIG_KEYPAW_OLED_LAYOUT (zmk-rgb-matrix) whether a widget is drawn, and where, are
 * settings that ZMK Studio edits (the ids 16 and up of <zmk/display_settings.h>), kept in the flash
 * of each half. Their defaults are the CONFIG_NICE_OLED_WIDGET_*_CUSTOM_X and _Y options of the
 * build, so the screens look the way they did until something is changed.
 *
 * Without the option the macros are the values of the build and nothing is read at run time.
 *
 *   LAYOUT_SHOWN(widget)       true if the widget is drawn
 *   LAYOUT_X(widget, build_x)  its x on the canvas
 *   LAYOUT_Y(widget, build_y)  its y on the canvas
 *
 * `widget` is the name in the ids (L_LAYER for KP_OLED_L_LAYER_SHOW, _X and _Y; R_ for the right
 * screen, L_ for the left one); `build_x` and `build_y` are what the build says.
 **/

#if IS_ENABLED(CONFIG_KEYPAW_OLED_LAYOUT)

#include <zmk/display_settings.h>

#define LAYOUT_SHOWN_(widget) (kp_display_setting_get(KP_OLED_##widget##_SHOW) != 0)
#define LAYOUT_X_(widget, build_x) ((int)kp_display_setting_get(KP_OLED_##widget##_X))
#define LAYOUT_Y_(widget, build_y) ((int)kp_display_setting_get(KP_OLED_##widget##_Y))

#else

#define LAYOUT_SHOWN_(widget) true
#define LAYOUT_X_(widget, build_x) (build_x)
#define LAYOUT_Y_(widget, build_y) (build_y)

#endif

// The second level expands the name first, for a file that picks the widget by half (battery.c)
#define LAYOUT_SHOWN(widget) LAYOUT_SHOWN_(widget)
#define LAYOUT_X(widget, build_x) LAYOUT_X_(widget, build_x)
#define LAYOUT_Y(widget, build_y) LAYOUT_Y_(widget, build_y)
