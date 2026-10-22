#include "output.h"
// #include "../assets/custom_fonts.h"
#include <fonts.h>
#include <zephyr/kernel.h>

#include "layout.h"

// Where the icons are. On the left screen (the central) the widget is the USB icon, and the
// Bluetooth icons keep their distance from it; on the right screen (the peripheral) it is the
// Bluetooth icon. With the OLED layout off these are all zero and nothing moves.
#if !IS_ENABLED(CONFIG_ZMK_SPLIT) || IS_ENABLED(CONFIG_ZMK_SPLIT_ROLE_CENTRAL)
#define OUTPUT_SHOWN LAYOUT_SHOWN(L_OUTPUT)
#define OUTPUT_DX                                                                                  \
    (LAYOUT_X(L_OUTPUT, CONFIG_NICE_OLED_WIDGET_OUTPUT_USB_CUSTOM_X) -                             \
     CONFIG_NICE_OLED_WIDGET_OUTPUT_USB_CUSTOM_X)
#define OUTPUT_DY                                                                                  \
    (LAYOUT_Y(L_OUTPUT, CONFIG_NICE_OLED_WIDGET_OUTPUT_USB_CUSTOM_Y) -                             \
     CONFIG_NICE_OLED_WIDGET_OUTPUT_USB_CUSTOM_Y)
#else
#define OUTPUT_SHOWN LAYOUT_SHOWN(R_LINK)
#define OUTPUT_DX                                                                                  \
    (LAYOUT_X(R_LINK, CONFIG_NICE_OLED_WIDGET_OUTPUT_BT_CUSTOM_X) -                                \
     CONFIG_NICE_OLED_WIDGET_OUTPUT_BT_CUSTOM_X)
#define OUTPUT_DY                                                                                  \
    (LAYOUT_Y(R_LINK, CONFIG_NICE_OLED_WIDGET_OUTPUT_BT_CUSTOM_Y) -                                \
     CONFIG_NICE_OLED_WIDGET_OUTPUT_BT_CUSTOM_Y)
#endif

LV_IMG_DECLARE(bt_no_signal);
LV_IMG_DECLARE(bt_unbonded);
LV_IMG_DECLARE(bt);
LV_IMG_DECLARE(usb);

#if !IS_ENABLED(CONFIG_ZMK_SPLIT) || IS_ENABLED(CONFIG_ZMK_SPLIT_ROLE_CENTRAL)
static void draw_usb_connected(lv_obj_t *canvas) {
    lv_draw_image_dsc_t img_dsc;
    lv_draw_image_dsc_init(&img_dsc);

    canvas_draw_img(canvas, CONFIG_NICE_OLED_WIDGET_OUTPUT_USB_CUSTOM_X + OUTPUT_DX, CONFIG_NICE_OLED_WIDGET_OUTPUT_USB_CUSTOM_Y + OUTPUT_DY, &usb, &img_dsc);
}

static void draw_ble_unbonded(lv_obj_t *canvas) {
    lv_draw_image_dsc_t img_dsc;
    lv_draw_image_dsc_init(&img_dsc);

    canvas_draw_img(canvas, CONFIG_NICE_OLED_WIDGET_OUTPUT_BT_UNBONDED_CUSTOM_X + OUTPUT_DX, CONFIG_NICE_OLED_WIDGET_OUTPUT_BT_UNBONDED_CUSTOM_Y + OUTPUT_DY, &bt_unbonded, &img_dsc);
}
#endif

static void draw_ble_disconnected(lv_obj_t *canvas) {
    lv_draw_image_dsc_t img_dsc;
    lv_draw_image_dsc_init(&img_dsc);

    canvas_draw_img(canvas, CONFIG_NICE_OLED_WIDGET_OUTPUT_BT_CUSTOM_X + OUTPUT_DX, CONFIG_NICE_OLED_WIDGET_OUTPUT_BT_CUSTOM_Y + OUTPUT_DY, &bt_no_signal, &img_dsc);
}

static void draw_ble_connected(lv_obj_t *canvas) {
    lv_draw_image_dsc_t img_dsc;
    lv_draw_image_dsc_init(&img_dsc);

    canvas_draw_img(canvas, CONFIG_NICE_OLED_WIDGET_OUTPUT_BT_CUSTOM_X + OUTPUT_DX, CONFIG_NICE_OLED_WIDGET_OUTPUT_BT_CUSTOM_Y + OUTPUT_DY, &bt, &img_dsc);
}

void draw_output_status(lv_obj_t *canvas, const struct status_state *state) {
    if (!OUTPUT_SHOWN) {
        return;
    }

#if IS_ENABLED(CONFIG_NICE_EPAPER_ON) &&                                                           \
    !IS_ENABLED(CONFIG_NICE_OLED_WIDGET_CENTRAL_SHOW_BATTERY_PERIPHERAL_ALL)
    lv_draw_label_dsc_t label_dsc;
    init_label_dsc(&label_dsc, LVGL_FOREGROUND, &pixel_operator_mono_16, LV_TEXT_ALIGN_LEFT);
    canvas_draw_text(canvas, 0, 1, 25, &label_dsc, "SIG");

#if IS_ENABLED(CONFIG_NICE_OLED_WIDGET_OUTPUT_BACKGROUND)
    lv_draw_rect_dsc_t rect_white_dsc;
    init_rect_dsc(&rect_white_dsc, LVGL_FOREGROUND);
    canvas_draw_rect(canvas, 43, 0, 24, 15, &rect_white_dsc);
#endif

#else

#if IS_ENABLED(CONFIG_NICE_OLED_WIDGET_OUTPUT_BACKGROUND)
    lv_draw_rect_dsc_t rect_white_dsc;
    init_rect_dsc(&rect_white_dsc, LVGL_FOREGROUND);
    canvas_draw_rect(canvas, -3 + OUTPUT_DX, 32 + OUTPUT_DY, 24, 15, &rect_white_dsc);
#endif

#endif // CONFIG_NICE_EPAPER_ON

#if !IS_ENABLED(CONFIG_ZMK_SPLIT) || IS_ENABLED(CONFIG_ZMK_SPLIT_ROLE_CENTRAL)
    switch (state->selected_endpoint.transport) {
    case ZMK_TRANSPORT_USB:
        draw_usb_connected(canvas);
        break;

    case ZMK_TRANSPORT_BLE:
    case ZMK_TRANSPORT_NONE:
    default:
        // ZMK main reports ZMK_TRANSPORT_NONE while no transport is ready (USB not
        // enumerated and the active BLE profile not connected). Draw the state of the
        // active BLE profile (unbonded / no signal) instead of leaving the slot blank.
        if (state->active_profile_bonded) {
            if (state->active_profile_connected) {
                draw_ble_connected(canvas);
            } else {
                draw_ble_disconnected(canvas);
            }
        } else {
            draw_ble_unbonded(canvas);
        }
        break;
    }
#else
    if (state->connected) {
        draw_ble_connected(canvas);
    } else {
        draw_ble_disconnected(canvas);
    }
#endif
}
