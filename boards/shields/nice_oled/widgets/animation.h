#pragma once

#include <lvgl.h>
#include "util.h"
#include "screen_peripheral.h"

void draw_animation(lv_obj_t *canvas, struct zmk_widget_screen *widget);

#if IS_ENABLED(CONFIG_KEYPAW_OLED_LAYOUT) &&                                                       \
    !IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_SMART_BATTERY)
/**
 * Puts the animation (or image) in line with the OLED layout settings: drawn or not, which one and
 * how long a cycle takes (where it is, how it is turned, which piece of it shows and how it mixes
 * with the widgets are read at every draw). Call it from the display work queue.
 **/
void animation_apply(void);

/**
 * Puts the frame of the picture that is playing on the canvas, after the widgets were drawn and the
 * canvas was turned for the panel: turned, cropped and mixed as the settings say. Call it at the
 * end of every draw of the canvas.
 **/
void animation_composite(lv_obj_t *canvas);
#endif
