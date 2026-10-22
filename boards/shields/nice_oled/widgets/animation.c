#include "animation.h"
#if !IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_SMART_BATTERY)
#include <stdlib.h>
#include <zephyr/kernel.h>

#include "layout.h"

LV_IMG_DECLARE(crystal_01);
LV_IMG_DECLARE(crystal_02);
LV_IMG_DECLARE(crystal_03);
LV_IMG_DECLARE(crystal_04);
LV_IMG_DECLARE(crystal_05);
LV_IMG_DECLARE(crystal_06);
LV_IMG_DECLARE(crystal_07);
LV_IMG_DECLARE(crystal_08);
LV_IMG_DECLARE(crystal_09);
LV_IMG_DECLARE(crystal_10);
LV_IMG_DECLARE(crystal_11);
LV_IMG_DECLARE(crystal_12);
LV_IMG_DECLARE(crystal_13);
LV_IMG_DECLARE(crystal_14);
LV_IMG_DECLARE(crystal_15);
LV_IMG_DECLARE(crystal_16);

const lv_img_dsc_t *crystal_imgs[] = {
    &crystal_01, &crystal_02, &crystal_03, &crystal_04, &crystal_05, &crystal_06,
    &crystal_07, &crystal_08, &crystal_09, &crystal_10, &crystal_11, &crystal_12,
    &crystal_13, &crystal_14, &crystal_15, &crystal_16,
};

#if IS_ENABLED(CONFIG_KEYPAW_OLED_LAYOUT)
// The OLED layout picks the animation (or image) while the keyboard runs: all of them are built
// in (see CMakeLists.txt), each with its list of frames.

LV_IMG_DECLARE(head_00);
LV_IMG_DECLARE(head_01);
LV_IMG_DECLARE(head_02);
LV_IMG_DECLARE(head_03);
LV_IMG_DECLARE(head_04);
LV_IMG_DECLARE(head_05);
LV_IMG_DECLARE(head_06);
LV_IMG_DECLARE(head_07);
LV_IMG_DECLARE(head_08);
LV_IMG_DECLARE(head_09);
LV_IMG_DECLARE(head_10);
LV_IMG_DECLARE(head_11);
LV_IMG_DECLARE(head_12);
LV_IMG_DECLARE(head_13);
LV_IMG_DECLARE(head_14);
LV_IMG_DECLARE(head_15);

const lv_img_dsc_t *head_imgs[] = {
    &head_00, &head_01, &head_02, &head_03,
    &head_04, &head_05, &head_06, &head_07,
    &head_08, &head_09, &head_10, &head_11,
    &head_12, &head_13, &head_14, &head_15,
};

LV_IMG_DECLARE(cat_0);
LV_IMG_DECLARE(cat_1);
LV_IMG_DECLARE(cat_2);
LV_IMG_DECLARE(cat_3);
LV_IMG_DECLARE(cat_4);
LV_IMG_DECLARE(cat_5);
LV_IMG_DECLARE(cat_6);
LV_IMG_DECLARE(cat_7);

const lv_img_dsc_t *cat_imgs[] = {
    &cat_0, &cat_1, &cat_2, &cat_3,
    &cat_4, &cat_5, &cat_6, &cat_7,
};

LV_IMG_DECLARE(spaceman_00);
LV_IMG_DECLARE(spaceman_01);
LV_IMG_DECLARE(spaceman_02);
LV_IMG_DECLARE(spaceman_03);
LV_IMG_DECLARE(spaceman_04);
LV_IMG_DECLARE(spaceman_05);
LV_IMG_DECLARE(spaceman_06);
LV_IMG_DECLARE(spaceman_07);
LV_IMG_DECLARE(spaceman_08);
LV_IMG_DECLARE(spaceman_09);
LV_IMG_DECLARE(spaceman_10);
LV_IMG_DECLARE(spaceman_11);
LV_IMG_DECLARE(spaceman_12);
LV_IMG_DECLARE(spaceman_13);
LV_IMG_DECLARE(spaceman_14);
LV_IMG_DECLARE(spaceman_15);
LV_IMG_DECLARE(spaceman_16);
LV_IMG_DECLARE(spaceman_17);
LV_IMG_DECLARE(spaceman_18);
LV_IMG_DECLARE(spaceman_19);

const lv_img_dsc_t *spaceman_imgs[] = {
    &spaceman_00, &spaceman_01, &spaceman_02, &spaceman_03,
    &spaceman_04, &spaceman_05, &spaceman_06, &spaceman_07,
    &spaceman_08, &spaceman_09, &spaceman_10, &spaceman_11,
    &spaceman_12, &spaceman_13, &spaceman_14, &spaceman_15,
    &spaceman_16, &spaceman_17, &spaceman_18, &spaceman_19,
};

LV_IMG_DECLARE(pokemon_00);
LV_IMG_DECLARE(pokemon_01);
LV_IMG_DECLARE(pokemon_02);
LV_IMG_DECLARE(pokemon_03);
LV_IMG_DECLARE(pokemon_04);
LV_IMG_DECLARE(pokemon_05);
LV_IMG_DECLARE(pokemon_06);
LV_IMG_DECLARE(pokemon_07);
LV_IMG_DECLARE(pokemon_08);
LV_IMG_DECLARE(pokemon_09);
LV_IMG_DECLARE(pokemon_10);
LV_IMG_DECLARE(pokemon_11);
LV_IMG_DECLARE(pokemon_12);
LV_IMG_DECLARE(pokemon_13);
LV_IMG_DECLARE(pokemon_14);
LV_IMG_DECLARE(pokemon_15);
LV_IMG_DECLARE(pokemon_16);
LV_IMG_DECLARE(pokemon_17);
LV_IMG_DECLARE(pokemon_18);
LV_IMG_DECLARE(pokemon_19);
LV_IMG_DECLARE(pokemon_20);
LV_IMG_DECLARE(pokemon_21);
LV_IMG_DECLARE(pokemon_22);
LV_IMG_DECLARE(pokemon_23);
LV_IMG_DECLARE(pokemon_24);
LV_IMG_DECLARE(pokemon_25);
LV_IMG_DECLARE(pokemon_26);
LV_IMG_DECLARE(pokemon_27);
LV_IMG_DECLARE(pokemon_28);
LV_IMG_DECLARE(pokemon_29);
LV_IMG_DECLARE(pokemon_30);
LV_IMG_DECLARE(pokemon_31);
LV_IMG_DECLARE(pokemon_32);
LV_IMG_DECLARE(pokemon_33);
LV_IMG_DECLARE(pokemon_34);
LV_IMG_DECLARE(pokemon_35);
LV_IMG_DECLARE(pokemon_36);
LV_IMG_DECLARE(pokemon_37);
LV_IMG_DECLARE(pokemon_38);
LV_IMG_DECLARE(pokemon_39);
LV_IMG_DECLARE(pokemon_40);
LV_IMG_DECLARE(pokemon_41);
LV_IMG_DECLARE(pokemon_42);
LV_IMG_DECLARE(pokemon_43);
LV_IMG_DECLARE(pokemon_44);
LV_IMG_DECLARE(pokemon_45);
LV_IMG_DECLARE(pokemon_46);
LV_IMG_DECLARE(pokemon_47);

const lv_img_dsc_t *pokemon_imgs[] = {
    &pokemon_00, &pokemon_01, &pokemon_02, &pokemon_03,
    &pokemon_04, &pokemon_05, &pokemon_06, &pokemon_07,
    &pokemon_08, &pokemon_09, &pokemon_10, &pokemon_11,
    &pokemon_12, &pokemon_13, &pokemon_14, &pokemon_15,
    &pokemon_16, &pokemon_17, &pokemon_18, &pokemon_19,
    &pokemon_20, &pokemon_21, &pokemon_22, &pokemon_23,
    &pokemon_24, &pokemon_25, &pokemon_26, &pokemon_27,
    &pokemon_28, &pokemon_29, &pokemon_30, &pokemon_31,
    &pokemon_32, &pokemon_33, &pokemon_34, &pokemon_35,
    &pokemon_36, &pokemon_37, &pokemon_38, &pokemon_39,
    &pokemon_40, &pokemon_41, &pokemon_42, &pokemon_43,
    &pokemon_44, &pokemon_45, &pokemon_46, &pokemon_47,
};

LV_IMG_DECLARE(vim);
LV_IMG_DECLARE(vip_marcos);

#elif IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL)
#if IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_HEAD)

LV_IMG_DECLARE(head_00);
LV_IMG_DECLARE(head_01);
LV_IMG_DECLARE(head_02);
LV_IMG_DECLARE(head_03);
LV_IMG_DECLARE(head_04);
LV_IMG_DECLARE(head_05);
LV_IMG_DECLARE(head_06);
LV_IMG_DECLARE(head_07);
LV_IMG_DECLARE(head_08);
LV_IMG_DECLARE(head_09);
LV_IMG_DECLARE(head_10);
LV_IMG_DECLARE(head_11);
LV_IMG_DECLARE(head_12);
LV_IMG_DECLARE(head_13);
LV_IMG_DECLARE(head_14);
LV_IMG_DECLARE(head_15);

const lv_img_dsc_t *head_imgs[] = {&head_00, &head_01, &head_02, &head_03, &head_04, &head_05,
                                   &head_06, &head_07, &head_08, &head_09, &head_10, &head_11,
                                   &head_12, &head_13, &head_14, &head_15};

#elif IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_CAT)
LV_IMG_DECLARE(cat_0);
LV_IMG_DECLARE(cat_1);
LV_IMG_DECLARE(cat_2);
LV_IMG_DECLARE(cat_3);
LV_IMG_DECLARE(cat_4);
LV_IMG_DECLARE(cat_5);
LV_IMG_DECLARE(cat_6);
LV_IMG_DECLARE(cat_7);

const lv_img_dsc_t *cat_imgs[] = {&cat_0, &cat_1, &cat_2, &cat_3, &cat_4, &cat_5, &cat_6, &cat_7};

#elif IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_SPACEMAN)

LV_IMG_DECLARE(spaceman_00);
LV_IMG_DECLARE(spaceman_01);
LV_IMG_DECLARE(spaceman_02);
LV_IMG_DECLARE(spaceman_03);
LV_IMG_DECLARE(spaceman_04);
LV_IMG_DECLARE(spaceman_05);
LV_IMG_DECLARE(spaceman_06);
LV_IMG_DECLARE(spaceman_07);
LV_IMG_DECLARE(spaceman_08);
LV_IMG_DECLARE(spaceman_09);
LV_IMG_DECLARE(spaceman_10);
LV_IMG_DECLARE(spaceman_11);
LV_IMG_DECLARE(spaceman_12);
LV_IMG_DECLARE(spaceman_13);
LV_IMG_DECLARE(spaceman_14);
LV_IMG_DECLARE(spaceman_15);
LV_IMG_DECLARE(spaceman_16);
LV_IMG_DECLARE(spaceman_17);
LV_IMG_DECLARE(spaceman_18);
LV_IMG_DECLARE(spaceman_19);

const lv_img_dsc_t *spaceman_imgs[] = {&spaceman_00, &spaceman_01, &spaceman_02, &spaceman_03,
                                       &spaceman_04, &spaceman_05, &spaceman_06, &spaceman_07,
                                       &spaceman_08, &spaceman_09, &spaceman_10, &spaceman_11,
                                       &spaceman_12, &spaceman_13, &spaceman_14, &spaceman_15,
                                       &spaceman_16, &spaceman_17, &spaceman_18, &spaceman_19};

#elif IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_POKEMON)
LV_IMG_DECLARE(pokemon_00);
LV_IMG_DECLARE(pokemon_01);
LV_IMG_DECLARE(pokemon_02);
LV_IMG_DECLARE(pokemon_03);
LV_IMG_DECLARE(pokemon_04);
LV_IMG_DECLARE(pokemon_05);
LV_IMG_DECLARE(pokemon_06);
LV_IMG_DECLARE(pokemon_07);
LV_IMG_DECLARE(pokemon_08);
LV_IMG_DECLARE(pokemon_09);
LV_IMG_DECLARE(pokemon_10);
LV_IMG_DECLARE(pokemon_11);
LV_IMG_DECLARE(pokemon_12);
LV_IMG_DECLARE(pokemon_13);
LV_IMG_DECLARE(pokemon_14);
LV_IMG_DECLARE(pokemon_15);
LV_IMG_DECLARE(pokemon_16);
LV_IMG_DECLARE(pokemon_17);
LV_IMG_DECLARE(pokemon_18);
LV_IMG_DECLARE(pokemon_19);
LV_IMG_DECLARE(pokemon_20);
LV_IMG_DECLARE(pokemon_21);
LV_IMG_DECLARE(pokemon_22);
LV_IMG_DECLARE(pokemon_23);
LV_IMG_DECLARE(pokemon_24);
LV_IMG_DECLARE(pokemon_25);
LV_IMG_DECLARE(pokemon_26);
LV_IMG_DECLARE(pokemon_27);
LV_IMG_DECLARE(pokemon_28);
LV_IMG_DECLARE(pokemon_29);
LV_IMG_DECLARE(pokemon_30);
LV_IMG_DECLARE(pokemon_31);
LV_IMG_DECLARE(pokemon_32);
LV_IMG_DECLARE(pokemon_33);
LV_IMG_DECLARE(pokemon_34);
LV_IMG_DECLARE(pokemon_35);
LV_IMG_DECLARE(pokemon_36);
LV_IMG_DECLARE(pokemon_37);
LV_IMG_DECLARE(pokemon_38);
LV_IMG_DECLARE(pokemon_39);
LV_IMG_DECLARE(pokemon_40);
LV_IMG_DECLARE(pokemon_41);
LV_IMG_DECLARE(pokemon_42);
LV_IMG_DECLARE(pokemon_43);
LV_IMG_DECLARE(pokemon_44);
LV_IMG_DECLARE(pokemon_45);
LV_IMG_DECLARE(pokemon_46);
LV_IMG_DECLARE(pokemon_47);

const lv_img_dsc_t *pokemon_imgs[] = {
    &pokemon_00, &pokemon_01, &pokemon_02, &pokemon_03, &pokemon_04, &pokemon_05, &pokemon_06,
    &pokemon_07, &pokemon_08, &pokemon_09, &pokemon_10, &pokemon_11, &pokemon_12, &pokemon_13,
    &pokemon_14, &pokemon_15, &pokemon_16, &pokemon_17, &pokemon_18, &pokemon_19, &pokemon_20,
    &pokemon_21, &pokemon_22, &pokemon_23, &pokemon_24, &pokemon_25, &pokemon_26, &pokemon_27,
    &pokemon_28, &pokemon_29, &pokemon_30, &pokemon_31, &pokemon_32, &pokemon_33, &pokemon_34,
    &pokemon_35, &pokemon_36, &pokemon_37, &pokemon_38, &pokemon_39, &pokemon_40, &pokemon_41,
    &pokemon_42, &pokemon_43, &pokemon_44, &pokemon_45, &pokemon_46, &pokemon_47};
#else
#endif
#else // IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL)
      // IS_ENABLED(CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL)

#if IS_ENABLED(CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL_VIM)
LV_IMG_DECLARE(vim);
#define FIXED_IMAGE_VIM &vim

#elif IS_ENABLED(CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL_VIP_MARCOS)
LV_IMG_DECLARE(vip_marcos);
#define FIXED_IMAGE_VIP_MARCOS &vip_marcos

#else

LV_IMG_DECLARE(vim);
#define FIXED_IMAGE_1 &vim

#endif

#endif // IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL)
       // IS_ENABLED(CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL)

#if IS_ENABLED(CONFIG_KEYPAW_OLED_LAYOUT)

// One entry per value of KP_OLED_R_ANIM_KIND (enum kp_oled_anim_kind of zmk-rgb-matrix)
struct anim_def {
    const lv_img_dsc_t **frames;
    // 1 is a still image
    uint8_t count;
    // One cycle, as the animation is made for (the build's own animation takes
    // CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_MS instead)
    uint16_t ms;
};

static const lv_img_dsc_t *vim_imgs[] = {&vim};
static const lv_img_dsc_t *vip_marcos_imgs[] = {&vip_marcos};

static const struct anim_def anims[KP_OLED_ANIM_KIND_COUNT] = {
    [KP_OLED_ANIM_CRYSTAL] = {crystal_imgs, ARRAY_SIZE(crystal_imgs), 960},
    [KP_OLED_ANIM_CAT] = {cat_imgs, ARRAY_SIZE(cat_imgs), 960},
    [KP_OLED_ANIM_HEAD] = {head_imgs, ARRAY_SIZE(head_imgs), 4800},
    [KP_OLED_ANIM_SPACEMAN] = {spaceman_imgs, ARRAY_SIZE(spaceman_imgs), 4800},
    [KP_OLED_ANIM_POKEMON] = {pokemon_imgs, ARRAY_SIZE(pokemon_imgs), 10000},
    [KP_OLED_ANIM_VIM] = {vim_imgs, ARRAY_SIZE(vim_imgs), 0},
    [KP_OLED_ANIM_VIP_MARCOS] = {vip_marcos_imgs, ARRAY_SIZE(vip_marcos_imgs), 0},
};

static lv_obj_t *art;
// What art shows now: the kind (-1 before the first time, and while it is hidden) and its cycle
static int applied_kind = -1;
static uint32_t applied_ms;

// The cycle the setting asks for: 0 is the time of the animation, and a time that is asked for
// is not shorter than 100 ms
static uint32_t cycle_ms(int kind, int32_t asked) {
    if (asked > 0) {
        return MAX((uint32_t)asked, 100U);
    }

#ifdef CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_MS
    // The animation that the build chose keeps the time that the build set
    if (kind == kp_display_setting_default(KP_OLED_R_ANIM_KIND)) {
        return CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_MS;
    }
#endif

    return anims[kind].ms;
}

void animation_apply(void) {
    if (art == NULL) {
        return;
    }

    if (!LAYOUT_SHOWN(R_ANIM)) {
        // Nothing to see: stop it, so that it does not keep LVGL busy for nobody
        lv_anim_delete(art, NULL);
        lv_obj_add_flag(art, LV_OBJ_FLAG_HIDDEN);
        applied_kind = -1;
        return;
    }

    lv_obj_remove_flag(art, LV_OBJ_FLAG_HIDDEN);
    lv_obj_align(art, LV_ALIGN_TOP_LEFT,
                 LAYOUT_X(R_ANIM, CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_CUSTOM_X),
                 LAYOUT_Y(R_ANIM, CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_CUSTOM_Y));

    int kind = (int)kp_display_setting_get(KP_OLED_R_ANIM_KIND);
    if (kind < 0 || kind >= KP_OLED_ANIM_KIND_COUNT) {
        kind = (int)kp_display_setting_default(KP_OLED_R_ANIM_KIND);
    }

    const struct anim_def *def = &anims[kind];
    const uint32_t ms =
        def->count > 1 ? cycle_ms(kind, kp_display_setting_get(KP_OLED_R_ANIM_MS)) : 0;

    if (kind == applied_kind && ms == applied_ms) {
        return;
    }

    // Stop what runs before the source changes: it steps through the old list of frames
    lv_anim_delete(art, NULL);

    if (def->count > 1) {
        lv_animimg_set_src(art, (const void **)def->frames, def->count);
        lv_animimg_set_duration(art, ms);
        lv_animimg_set_repeat_count(art, LV_ANIM_REPEAT_INFINITE);
        lv_animimg_start(art);
    } else {
        lv_image_set_src(art, def->frames[0]);
    }

    applied_kind = kind;
    applied_ms = ms;
}

void draw_animation(lv_obj_t *canvas, struct zmk_widget_screen *widget) {
    art = lv_animimg_create(canvas);
    animation_apply();
}

#else // IS_ENABLED(CONFIG_KEYPAW_OLED_LAYOUT)

void draw_animation(lv_obj_t *canvas, struct zmk_widget_screen *widget) {
    lv_obj_t *art = lv_animimg_create(canvas);

#if IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL)
    lv_obj_center(art);

#if IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_HEAD)
    lv_animimg_set_src(art, (const void **)head_imgs, 16);
#elif IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_CAT)
    lv_animimg_set_src(art, (const void **)cat_imgs, 8);
#elif IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_SPACEMAN)
    lv_animimg_set_src(art, (const void **)spaceman_imgs, 20);
#elif IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_POKEMON)
    lv_animimg_set_src(art, (const void **)pokemon_imgs, 48);
#else
    lv_animimg_set_src(art, (const void **)crystal_imgs, 16);
#endif
    lv_animimg_set_duration(art, CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_MS);
    lv_animimg_set_repeat_count(art, LV_ANIM_REPEAT_INFINITE);
    lv_animimg_start(art);

#else // IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL)
      // IS_ENABLED(CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL)

#if IS_ENABLED(CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL_VIM)
    lv_img_set_src(art, FIXED_IMAGE_VIM);
#elif IS_ENABLED(CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL_VIP_MARCOS)
    lv_img_set_src(art, FIXED_IMAGE_VIP_MARCOS);
#else
    int length = sizeof(crystal_imgs) / sizeof(crystal_imgs[0]);
    srand(k_uptime_get_32());
    int random_index = rand() % length;

    lv_img_set_src(art, crystal_imgs[random_index]);
#endif

#endif // IS_ENABLED(CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL)
       // IS_ENABLED(CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL)

    if (art) {
        lv_obj_align(art, LV_ALIGN_TOP_LEFT, CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_CUSTOM_X, CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_CUSTOM_Y);
    }
}

#endif // IS_ENABLED(CONFIG_KEYPAW_OLED_LAYOUT)
#endif
