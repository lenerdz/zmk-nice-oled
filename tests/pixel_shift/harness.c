/* Host test of boards/shields/nice_oled/widgets/pixel_shift.c: the code of the shield, compiled as
 * it is (it is included below, so the test can reset its state) with a few stubs for LVGL and
 * Zephyr that write down what they are asked, and the REAL zmk/display_settings.h of
 * zmk-rgb-matrix (the ids of the settings and the walk of the shift). Driven by
 * test_pixel_shift.py through ctypes. */
#include <lvgl.h>
#include <zephyr/kernel.h>

#include <zmk/display_settings.h>

#include "pixel_shift.c"

/* The settings, and the clock */
static int32_t settings[KP_DISPLAY_SETTING_CAP];
static int64_t clock_ms;

int32_t kp_display_setting_get(enum kp_display_setting_id id) { return settings[id]; }
int32_t kp_display_setting_default(enum kp_display_setting_id id) { return 0; }
int64_t k_uptime_get(void) { return clock_ms; }

/* What LVGL was asked */
static lv_obj_t container_obj = {1};
static lv_obj_t canvas_obj = {2};
static lv_timer_cb_t timer_cb;
static uint32_t timer_period;
static int timers;
static int aligns;
static lv_obj_t *align_obj;
static lv_align_t align_mode;
static int32_t align_x;
static int32_t align_y;
static lv_obj_t *style_obj;
static int styles_set;
static uint8_t style_bg;
static uint8_t style_opa;
static int32_t style_border = -1;
static int32_t style_radius = -1;

void lv_obj_align(lv_obj_t *obj, lv_align_t align, int32_t x_ofs, int32_t y_ofs) {
    aligns++;
    align_obj = obj;
    align_mode = align;
    align_x = x_ofs;
    align_y = y_ofs;
}

void lv_obj_set_style_bg_color(lv_obj_t *obj, lv_color_t color, uint32_t selector) {
    style_obj = obj;
    style_bg = color.luminance;
    styles_set++;
}
void lv_obj_set_style_bg_opa(lv_obj_t *obj, uint8_t opa, uint32_t selector) {
    style_opa = opa;
    styles_set++;
}
void lv_obj_set_style_border_width(lv_obj_t *obj, int32_t width, uint32_t selector) {
    style_border = width;
    styles_set++;
}
void lv_obj_set_style_radius(lv_obj_t *obj, int32_t radius, uint32_t selector) {
    style_radius = radius;
    styles_set++;
}

lv_timer_t *lv_timer_create(lv_timer_cb_t cb, uint32_t period, void *user_data) {
    timer_cb = cb;
    timer_period = period;
    timers++;
    return (lv_timer_t *)&timer_cb;
}

/* The test API */
void t_reset(void) {
    for (int i = 0; i < KP_DISPLAY_SETTING_CAP; i++) {
        settings[i] = 0;
    }
    clock_ms = 0;
    shifted = NULL;
    step = 0;
    last_step_at = 0;
    running = false;
    offset_x = 0;
    offset_y = 0;
    timer_cb = NULL;
    timer_period = 0;
    timers = 0;
    aligns = 0;
    align_obj = NULL;
    align_mode = 0;
    align_x = 0;
    align_y = 0;
    style_obj = NULL;
    styles_set = 0;
    style_bg = 0;
    style_opa = 0;
    style_border = -1;
    style_radius = -1;
}

void t_init(uint8_t background) {
    pixel_shift_init(&container_obj, &canvas_obj, (lv_color_t){background});
}
void t_set(int id, int32_t value) { settings[id] = value; }
void t_time(int64_t ms) { clock_ms = ms; }
void t_poll(void) { timer_cb(NULL); }
int t_have_timer(void) { return timer_cb != NULL; }

int t_timers(void) { return timers; }
uint32_t t_timer_period(void) { return timer_period; }
int t_aligns(void) { return aligns; }
int32_t t_x(void) { return align_x; }
int32_t t_y(void) { return align_y; }
int t_align_is_canvas_top_left(void) {
    return align_obj == &canvas_obj && align_mode == LV_ALIGN_TOP_LEFT;
}
int t_styles_on_container(void) { return style_obj == &container_obj; }
int t_styles_set(void) { return styles_set; }
int t_style_bg(void) { return style_bg; }
int t_style_opa(void) { return style_opa; }
int32_t t_style_border(void) { return style_border; }
int32_t t_style_radius(void) { return style_radius; }

void t_expected(uint32_t step_n, int32_t px, int32_t *dx, int32_t *dy) {
    kp_display_shift_offset(step_n, px, dx, dy);
}
