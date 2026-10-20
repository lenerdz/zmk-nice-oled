#include "led_toast.h"

#include <ctype.h>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>

#include <fonts.h>
#include <zephyr/kernel.h>
#include <zephyr/sys/util.h>

/**
 * The labels. Every text is ASCII (the 8 pixel font has no accents), and every line has to fit
 * LED_TOAST_LINE_LEN - 1 characters: 8 characters of 4 pixels fill the 32 pixel wide screen.
 **/

#if IS_ENABLED(CONFIG_NICE_OLED_WIDGET_LED_TOAST_LANGUAGE_PT_BR)
#define TXT_EFFECT "EFEITO"
#define TXT_EFFECT_SHORT "EFX"
#define TXT_LIGHTS "LUZES"
#define TXT_ON "LIGADAS"
#define TXT_OFF "APAGADAS"
#define TXT_BRIGHTNESS "BRILHO"
#define TXT_HUE "MATIZ"
#define TXT_SATURATION "SATUR."
#define TXT_PERIOD "CICLO"
#define TXT_RESET "RESET"
#else
#define TXT_EFFECT "EFFECT"
#define TXT_EFFECT_SHORT "FX"
#define TXT_LIGHTS "LIGHTS"
#define TXT_ON "ON"
#define TXT_OFF "OFF"
#define TXT_BRIGHTNESS "BRIGHT"
#define TXT_HUE "HUE"
#define TXT_SATURATION "SATUR."
#define TXT_PERIOD "PERIOD"
#define TXT_RESET "RESET"
#endif

BUILD_ASSERT(sizeof(TXT_EFFECT " 9") <= LED_TOAST_LINE_LEN, "TXT_EFFECT does not fit in a line");
BUILD_ASSERT(sizeof(TXT_EFFECT_SHORT " 99") <= LED_TOAST_LINE_LEN,
             "TXT_EFFECT_SHORT does not fit in a line");
BUILD_ASSERT(sizeof(TXT_LIGHTS) <= LED_TOAST_LINE_LEN, "TXT_LIGHTS does not fit in a line");
BUILD_ASSERT(sizeof(TXT_ON) <= LED_TOAST_LINE_LEN, "TXT_ON does not fit in a line");
BUILD_ASSERT(sizeof(TXT_OFF) <= LED_TOAST_LINE_LEN, "TXT_OFF does not fit in a line");
BUILD_ASSERT(sizeof(TXT_BRIGHTNESS) <= LED_TOAST_LINE_LEN,
             "TXT_BRIGHTNESS does not fit in a line");
BUILD_ASSERT(sizeof(TXT_HUE) <= LED_TOAST_LINE_LEN, "TXT_HUE does not fit in a line");
BUILD_ASSERT(sizeof(TXT_SATURATION) <= LED_TOAST_LINE_LEN,
             "TXT_SATURATION does not fit in a line");
BUILD_ASSERT(sizeof(TXT_PERIOD) <= LED_TOAST_LINE_LEN, "TXT_PERIOD does not fit in a line");
BUILD_ASSERT(sizeof(TXT_RESET) <= LED_TOAST_LINE_LEN, "TXT_RESET does not fit in a line");

/** The font is 7 pixels tall: 8 pixels between lines leave one blank row. */
#define LED_TOAST_LINE_PITCH 8
/** 8 characters of 4 pixels. */
#define LED_TOAST_LINE_WIDTH 32

/** Writes `fmt` into a line, cutting what does not fit. */
static void put_linef(char dst[LED_TOAST_LINE_LEN], const char *fmt, ...)
    __attribute__((format(printf, 2, 3)));

static void put_linef(char dst[LED_TOAST_LINE_LEN], const char *fmt, ...) {
    char text[24];
    va_list args;

    va_start(args, fmt);
    vsnprintf(text, sizeof(text), fmt, args);
    va_end(args);

    snprintf(dst, LED_TOAST_LINE_LEN, "%s", text);
}

static void put_uppercase(char dst[LED_TOAST_LINE_LEN], const char *src) {
    size_t i = 0;

    for (; src != NULL && src[i] != '\0' && i < LED_TOAST_LINE_LEN - 1; i++) {
        dst[i] = (char)toupper((unsigned char)src[i]);
    }
    dst[i] = '\0';
}

void led_toast_format(const struct zmk_rgb_matrix_changed *ev, char line1[LED_TOAST_LINE_LEN],
                      char line2[LED_TOAST_LINE_LEN]) {
    switch (ev->kind) {
    case ZMK_RGB_MATRIX_CHANGE_EFFECT: {
        // The number is what the user counts on the keys (1 based); the name tells what it is
        const unsigned int number = (unsigned int)ev->effect + 1U;

        put_linef(line1, "%s %u", number < 10U ? TXT_EFFECT : TXT_EFFECT_SHORT, number);
        put_uppercase(line2, ev->effect_name);
        break;
    }
    case ZMK_RGB_MATRIX_CHANGE_POWER:
        put_linef(line1, "%s", TXT_LIGHTS);
        put_linef(line2, "%s", ev->on ? TXT_ON : TXT_OFF);
        break;
    case ZMK_RGB_MATRIX_CHANGE_BRIGHTNESS:
        put_linef(line1, "%s", TXT_BRIGHTNESS);
        put_linef(line2, "%u%%", (unsigned int)ev->brightness);
        break;
    case ZMK_RGB_MATRIX_CHANGE_HUE:
        put_linef(line1, "%s", TXT_HUE);
        put_linef(line2, "%u deg", (unsigned int)ev->hue);
        break;
    case ZMK_RGB_MATRIX_CHANGE_SATURATION:
        put_linef(line1, "%s", TXT_SATURATION);
        put_linef(line2, "%u%%", (unsigned int)ev->saturation);
        break;
    case ZMK_RGB_MATRIX_CHANGE_PERIOD:
        put_linef(line1, "%s", TXT_PERIOD);
        put_linef(line2, "%u ms", (unsigned int)ev->period_ms);
        break;
    case ZMK_RGB_MATRIX_CHANGE_RESET:
        put_linef(line1, "%s", TXT_LIGHTS);
        put_linef(line2, "%s", TXT_RESET);
        break;
    default:
        put_linef(line1, "%s", TXT_LIGHTS);
        put_linef(line2, "%s", "");
        break;
    }
}

void draw_led_toast(lv_obj_t *canvas, const struct status_state *state) {
    if (!state->toast_active) {
        return;
    }

    lv_draw_label_dsc_t label_dsc;
    init_label_dsc(&label_dsc, LVGL_FOREGROUND, &pixel_operator_mono_8, LV_TEXT_ALIGN_LEFT);

    // x, y, width, dsc, text
    canvas_draw_text(canvas, CONFIG_NICE_OLED_WIDGET_LED_TOAST_CUSTOM_X,
                     CONFIG_NICE_OLED_WIDGET_LED_TOAST_CUSTOM_Y, LED_TOAST_LINE_WIDTH, &label_dsc,
                     state->toast_line1);
    canvas_draw_text(canvas, CONFIG_NICE_OLED_WIDGET_LED_TOAST_CUSTOM_X,
                     CONFIG_NICE_OLED_WIDGET_LED_TOAST_CUSTOM_Y + LED_TOAST_LINE_PITCH,
                     LED_TOAST_LINE_WIDTH, &label_dsc, state->toast_line2);
}
