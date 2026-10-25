/* The little of LVGL that widgets/pixel_shift.c uses, for the host test (harness.c has the
 * functions: they only write down what they were asked). */
#pragma once

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef struct lv_obj_s {
    int id;
} lv_obj_t;

typedef struct {
    uint8_t luminance;
} lv_color_t;

typedef struct lv_timer_s lv_timer_t;
typedef void (*lv_timer_cb_t)(lv_timer_t *timer);

typedef int lv_align_t;
#define LV_ALIGN_TOP_LEFT 1
#define LV_OPA_COVER 255

void lv_obj_align(lv_obj_t *obj, lv_align_t align, int32_t x_ofs, int32_t y_ofs);
void lv_obj_set_style_bg_color(lv_obj_t *obj, lv_color_t color, uint32_t selector);
void lv_obj_set_style_bg_opa(lv_obj_t *obj, uint8_t opa, uint32_t selector);
void lv_obj_set_style_border_width(lv_obj_t *obj, int32_t width, uint32_t selector);
void lv_obj_set_style_radius(lv_obj_t *obj, int32_t radius, uint32_t selector);
lv_timer_t *lv_timer_create(lv_timer_cb_t cb, uint32_t period, void *user_data);
