/* The one function of Zephyr that widgets/pixel_shift.c uses, for the host test (harness.c has the
 * clock). */
#pragma once

#include <stdint.h>

int64_t k_uptime_get(void);
