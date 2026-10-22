#pragma once

#include <lvgl.h>
#include "util.h"
#include "screen_peripheral.h"

void draw_animation(lv_obj_t *canvas, struct zmk_widget_screen *widget);

#if IS_ENABLED(CONFIG_KEYPAW_OLED_LAYOUT) &&                                                       \
    !IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_SMART_BATTERY)
/**
 * Puts the animation (or image) in line with the OLED layout settings: drawn or not, where, which
 * one and how long a cycle takes. Call it from the display work queue.
 **/
void animation_apply(void);
#endif
