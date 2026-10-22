#include <zephyr/kernel.h>

#include <zephyr/logging/log.h>
LOG_MODULE_DECLARE(zmk, CONFIG_ZMK_LOG_LEVEL);

#include <zmk/battery.h>
#include <zmk/ble.h>
#include <zmk/display.h>
#include <zmk/event_manager.h>
#include <zmk/events/battery_state_changed.h>
#include <zmk/events/split_peripheral_status_changed.h>
#include <zmk/events/usb_conn_state_changed.h>
#include <zmk/split/bluetooth/peripheral.h>
#include <zmk/usb.h>

#include "animation.h"
#include "battery.h"
#include "output.h"
#include "screen_peripheral.h"

#if IS_ENABLED(CONFIG_KEYPAW_OLED_LAYOUT)
#include <zmk/events/display_settings_changed.h>
#endif

#if IS_ENABLED(CONFIG_NICE_OLED_WIDGET_LED_TOAST)
#include <string.h>

#include <zmk/events/rgb_matrix_changed.h>

#include "led_toast.h"

#if IS_ENABLED(CONFIG_KEYPAW_DISPLAY_SETTINGS)
#include <zmk/display_settings.h>
#endif
#endif

static sys_slist_t widgets = SYS_SLIST_STATIC_INIT(&widgets);

/**
 * sleep status
 **/

#if IS_ENABLED(CONFIG_NICE_OLED_SHOW_SLEEP_ART_ON_IDLE) ||                                         \
    IS_ENABLED(CONFIG_NICE_OLED_SHOW_SLEEP_ART_ON_SLEEP)
#include "sleep_status.h"
static struct zmk_widget_sleep_status sleep_status_widget;
#endif

/**
 * luna
 **/

#if IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_WPM)
#include "luna.h"
static struct zmk_widget_luna luna_widget;
#endif

/**
 * Draw canvas
 **/

static void draw_canvas(lv_obj_t *widget, const struct status_state *state) {
    lv_obj_t *canvas = lv_obj_get_child(widget, 0);

    // Draw widgets
    draw_background(canvas);
    draw_output_status(canvas, state);
    draw_battery_status(canvas, state);
#if IS_ENABLED(CONFIG_NICE_OLED_WIDGET_LED_TOAST)
    draw_led_toast(canvas, state);
#endif

    // Rotate for horizontal display
    rotate_canvas(canvas);

#if IS_ENABLED(CONFIG_KEYPAW_OLED_LAYOUT) &&                                                       \
    !IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_SMART_BATTERY)
    // The picture goes on the turned canvas: a lit pixel of it adds to the widgets or flips them
    animation_composite(canvas);
#endif
}

/**
 * Battery status
 **/

static void set_battery_status(struct zmk_widget_screen *widget,
                               struct battery_status_state state) {

#if IS_ENABLED(CONFIG_USB_DEVICE_STACK)
    widget->state.charging = state.usb_present;
#endif /* IS_ENABLED(CONFIG_USB_DEVICE_STACK) */

    widget->state.battery = state.level;

    draw_canvas(widget->obj, &widget->state);

    // draw_animation(widget->obj, widget);

#if IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_SMART_BATTERY)
    if (widget->state.charging) {
        // mostrar
        // lv_obj_clear_flag(widget->obj, LV_OBJ_FLAG_HIDDEN);
        animation_smart_battery_on(widget->obj);

    } else {
        // quitar
        // lv_obj_add_flag(widget->art, LV_OBJ_FLAG_HIDDEN);
        animation_smart_battery_off(widget->obj);
    }
#endif
}

static void battery_status_update_cb(struct battery_status_state state) {
    struct zmk_widget_screen *widget;
    SYS_SLIST_FOR_EACH_CONTAINER(&widgets, widget, node) { set_battery_status(widget, state); }
}

static struct battery_status_state battery_status_get_state(const zmk_event_t *eh) {
    const struct zmk_battery_state_changed *ev = as_zmk_battery_state_changed(eh);

    return (struct battery_status_state){
        .level = (ev != NULL) ? ev->state_of_charge : zmk_battery_state_of_charge(),
#if IS_ENABLED(CONFIG_USB_DEVICE_STACK)
        .usb_present = zmk_usb_is_powered(),
#endif /* IS_ENABLED(CONFIG_USB_DEVICE_STACK) */
    };
}

ZMK_DISPLAY_WIDGET_LISTENER(widget_battery_status, struct battery_status_state,
                            battery_status_update_cb, battery_status_get_state);

ZMK_SUBSCRIPTION(widget_battery_status, zmk_battery_state_changed);
#if IS_ENABLED(CONFIG_USB_DEVICE_STACK)
ZMK_SUBSCRIPTION(widget_battery_status, zmk_usb_conn_state_changed);
#endif /* IS_ENABLED(CONFIG_USB_DEVICE_STACK) */

/**
 * Peripheral status
 **/

static struct peripheral_status_state get_state(const zmk_event_t *_eh) {
    return (struct peripheral_status_state){.connected = zmk_split_bt_peripheral_is_connected()};
}

static void set_connection_status(struct zmk_widget_screen *widget,
                                  struct peripheral_status_state state) {
    widget->state.connected = state.connected;

    draw_canvas(widget->obj, &widget->state);
}

static void output_status_update_cb(struct peripheral_status_state state) {
    struct zmk_widget_screen *widget;
    SYS_SLIST_FOR_EACH_CONTAINER(&widgets, widget, node) { set_connection_status(widget, state); }
}

ZMK_DISPLAY_WIDGET_LISTENER(widget_peripheral_status, struct peripheral_status_state,
                            output_status_update_cb, get_state)
ZMK_SUBSCRIPTION(widget_peripheral_status, zmk_split_peripheral_status_changed);

/**
 * RGB toast
 *
 * For CONFIG_NICE_OLED_WIDGET_LED_TOAST_MS after a light command changed something, show what
 * changed. The state of the display listener keeps only the latest event, which is what a toast
 * wants: a newer change replaces the one on screen and restarts the timer.
 *
 * With CONFIG_KEYPAW_DISPLAY_SETTINGS (zmk-rgb-matrix), the toast can be turned off and its time
 * changed from ZMK Studio; CONFIG_NICE_OLED_WIDGET_LED_TOAST_MS is then only the build without
 * those settings.
 **/

#if IS_ENABLED(CONFIG_NICE_OLED_WIDGET_LED_TOAST)

struct led_toast_state {
    // false for the listener's initial refresh, when nothing has been announced yet
    bool valid;
    char line1[LED_TOAST_LINE_LEN];
    char line2[LED_TOAST_LINE_LEN];
};

static void led_toast_expire_cb(struct k_work *work);
static K_WORK_DELAYABLE_DEFINE(led_toast_expire_work, led_toast_expire_cb);

static void led_toast_show(struct zmk_widget_screen *widget, const struct led_toast_state *toast) {
    widget->state.toast_active = true;
    memcpy(widget->state.toast_line1, toast->line1, sizeof(widget->state.toast_line1));
    memcpy(widget->state.toast_line2, toast->line2, sizeof(widget->state.toast_line2));

    draw_canvas(widget->obj, &widget->state);
}

static void led_toast_update_cb(struct led_toast_state toast) {
    if (!toast.valid) {
        return;
    }

#if IS_ENABLED(CONFIG_KEYPAW_DISPLAY_SETTINGS)
    if (kp_display_setting_get(KP_DISPLAY_TOAST) == 0) {
        return;
    }
    const uint32_t toast_ms = (uint32_t)kp_display_setting_get(KP_DISPLAY_TOAST_MS);
#else
    const uint32_t toast_ms = CONFIG_NICE_OLED_WIDGET_LED_TOAST_MS;
#endif

    struct zmk_widget_screen *widget;
    SYS_SLIST_FOR_EACH_CONTAINER(&widgets, widget, node) { led_toast_show(widget, &toast); }

    k_work_reschedule_for_queue(zmk_display_work_q(), &led_toast_expire_work, K_MSEC(toast_ms));
}

static void led_toast_expire_cb(struct k_work *work) {
    struct zmk_widget_screen *widget;
    SYS_SLIST_FOR_EACH_CONTAINER(&widgets, widget, node) {
        widget->state.toast_active = false;
        draw_canvas(widget->obj, &widget->state);
    }
}

static struct led_toast_state led_toast_get_state(const zmk_event_t *eh) {
    struct led_toast_state toast = {0};

    // The initial refresh passes no event, and the accessor does not accept NULL
    const struct zmk_rgb_matrix_changed *ev = (eh != NULL) ? as_zmk_rgb_matrix_changed(eh) : NULL;
    if (ev != NULL) {
        toast.valid = true;
        led_toast_format(ev, toast.line1, toast.line2);
    }

    return toast;
}

ZMK_DISPLAY_WIDGET_LISTENER(widget_led_toast, struct led_toast_state, led_toast_update_cb,
                            led_toast_get_state)
ZMK_SUBSCRIPTION(widget_led_toast, zmk_rgb_matrix_changed);

#endif /* IS_ENABLED(CONFIG_NICE_OLED_WIDGET_LED_TOAST) */

/**
 * OLED layout
 *
 * With CONFIG_KEYPAW_OLED_LAYOUT (zmk-rgb-matrix), which widgets are drawn and where, and which
 * animation (or image) plays, how fast, turned how and cropped how, are settings that ZMK Studio
 * edits. Every draw function reads them; the animation is not an object of LVGL but a frame that
 * draw_canvas() puts on the canvas last (animation_composite), and animation_apply() puts its timer
 * in line.
 **/

#if IS_ENABLED(CONFIG_KEYPAW_OLED_LAYOUT)
struct oled_layout_state {
    uint8_t unused;
};

void screen_peripheral_redraw(void) {
    struct zmk_widget_screen *widget;
    SYS_SLIST_FOR_EACH_CONTAINER(&widgets, widget, node) {
        draw_canvas(widget->obj, &widget->state);
    }
}

static void oled_layout_update_cb(struct oled_layout_state state) {
#if !IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_SMART_BATTERY)
    animation_apply();
#endif

    screen_peripheral_redraw();
}

static struct oled_layout_state oled_layout_get_state(const zmk_event_t *eh) {
    return (struct oled_layout_state){0};
}

ZMK_DISPLAY_WIDGET_LISTENER(widget_oled_layout, struct oled_layout_state, oled_layout_update_cb,
                            oled_layout_get_state)
ZMK_SUBSCRIPTION(widget_oled_layout, zmk_display_settings_changed);
#endif // IS_ENABLED(CONFIG_KEYPAW_OLED_LAYOUT)

/**
 * Initialization
 **/

int zmk_widget_screen_init(struct zmk_widget_screen *widget, lv_obj_t *parent) {
    widget->obj = lv_obj_create(parent);
    lv_obj_set_size(widget->obj, CANVAS_HEIGHT, CANVAS_WIDTH);

    lv_obj_t *canvas = lv_canvas_create(widget->obj);
    lv_obj_align(canvas, LV_ALIGN_TOP_LEFT, 0, 0);
    lv_canvas_set_buffer(canvas, widget->cbuf, CANVAS_HEIGHT, CANVAS_HEIGHT, LV_COLOR_FORMAT_L8);

    sys_slist_append(&widgets, &widget->node);

#if !IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_SMART_BATTERY)
    draw_animation(canvas, widget);
#endif
    widget_battery_status_init();
    widget_peripheral_status_init();
#if IS_ENABLED(CONFIG_NICE_OLED_WIDGET_LED_TOAST)
    widget_led_toast_init();
#endif
#if IS_ENABLED(CONFIG_KEYPAW_OLED_LAYOUT)
    widget_oled_layout_init();
#endif

#if IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_WPM)
    zmk_widget_luna_init(&luna_widget, canvas);
    lv_obj_align(zmk_widget_luna_obj(&luna_widget), LV_ALIGN_TOP_LEFT, CONFIG_NICE_OLED_WIDGET_LUNA_CUSTOM_X, CONFIG_NICE_OLED_WIDGET_LUNA_CUSTOM_Y);
#endif

#if IS_ENABLED(CONFIG_NICE_OLED_SHOW_SLEEP_ART_ON_IDLE) ||                                         \
    IS_ENABLED(CONFIG_NICE_OLED_SHOW_SLEEP_ART_ON_SLEEP)
    zmk_widget_sleep_status_init(&sleep_status_widget, canvas);
    lv_obj_align(zmk_widget_sleep_status_obj(&sleep_status_widget), LV_ALIGN_TOP_LEFT, CONFIG_NICE_OLED_WIDGET_SLEEP_STATUS_CUSTOM_X, CONFIG_NICE_OLED_WIDGET_SLEEP_STATUS_CUSTOM_Y);
#endif

    return 0;
}

lv_obj_t *zmk_widget_screen_obj(struct zmk_widget_screen *widget) { return widget->obj; }
