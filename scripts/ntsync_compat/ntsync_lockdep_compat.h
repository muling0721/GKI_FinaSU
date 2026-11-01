/* SPDX-License-Identifier: GPL-2.0-only */
/*
 * ntsync_lockdep_compat.h - lockdep glue for pre-v5.13 kernels
 *
 * drivers/misc/ntsync.c relies on the generic assertion API introduced by
 * the v5.13 lockdep rework:
 *
 *   lockdep_assert(cond)
 *   LOCK_STATE_UNKNOWN / LOCK_STATE_NOT_HELD / LOCK_STATE_HELD
 *
 * The upstream platform patch backports that rework wholesale, but its
 * include/linux/lockdep.h hunk also expects lockdep_assert_none_held_once(),
 * which does not exist before v5.13. On 5.10 the hunk is rejected while
 * kernel/locking/lockdep.c is patched anyway, leaving a tree that cannot
 * compile.
 *
 * This header provides only the two symbols the driver actually uses, so old
 * kernels keep their core locking code untouched. Semantics match upstream:
 * lockdep_is_held() reports 1/0 (or -1 when lockdep is disabled), therefore
 * "!= LOCK_STATE_NOT_HELD" keeps the upstream meaning in every case.
 */
#ifndef _NTSYNC_LOCKDEP_COMPAT_H
#define _NTSYNC_LOCKDEP_COMPAT_H

#include <linux/bug.h>
#include <linux/lockdep.h>

#ifndef LOCK_STATE_NOT_HELD
#define LOCK_STATE_UNKNOWN	(-1)
#define LOCK_STATE_NOT_HELD	0
#define LOCK_STATE_HELD		1
#endif

#ifndef lockdep_assert
#ifdef CONFIG_LOCKDEP
#define lockdep_assert(cond)	do { WARN_ON(debug_locks && !(cond)); } while (0)
#else
#define lockdep_assert(cond)	do { } while (0)
#endif
#endif

#endif /* _NTSYNC_LOCKDEP_COMPAT_H */
