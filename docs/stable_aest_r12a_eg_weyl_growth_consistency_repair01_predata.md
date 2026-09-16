# Stable AeST R12a Repair01 — provenance-lock correction (pre-data)

Date: 2026-09-16
Branch: `fullj-evolving-weyl-bridge`

## Trigger

The first R12a runner invocation terminated before any CLASS science calculation with

`fatal: Not a valid commit name d9e2e0e6da65126a81d02f32e65f83410bc8cc7c`

and

`STABLE_AEST_R12A_LOCK_FAIL lock=d9e2e0e6da65126a81d02f32e65f83410bc8cc7c`.

No R12a transfer case, GR control, response tangent, or science quantity was evaluated.

## Root cause

The original R12a preregistration accidentally recorded a non-existent R11a Repair02 postdata SHA:

`d9e2e0e6da65126a81d02f32e65f83410bc8cc7c`.

The authoritative R11a Repair02 postdata commit on this branch is:

`84c4ba550ce3b262c78c69054056ab2778014677`

with commit message

`Freeze certified R11a Repair02 kSZ pairwise-velocity result`.

That commit contains `docs/stable_aest_ksz_r11a_dense_resolution_repair02_postdata.md`, freezes the classification

`STABLE_AEST_KSZ_R11A_REPAIR02_DENSE_RESOLUTION_CERTIFIED`,

and records the same frozen R11a Repair02 JSON SHA256 already required by R12a:

`f5166409be08edc93e739b2b901bd183a2a588325eb6c71eb0ad0e8a82d2b4a1`.

Therefore this is a provenance-pointer typo, not a change in the parent result.

## Allowed repair

Repair01 changes only the R11a Repair02 ancestry lock used by R12a:

- invalid: `d9e2e0e6da65126a81d02f32e65f83410bc8cc7c`
- corrected: `84c4ba550ce3b262c78c69054056ab2778014677`.

The original R12a preregistration remains frozen and is not rewritten.

No other R12a quantity may change. In particular, Repair01 preserves exactly:

- `tau H0 = [10, 5, 2.5, 1.25]`;
- `eta = [0, +0.025, -0.025, +0.05, -0.05]`;
- `k = [0.03, 0.05, 0.08, 0.10, 0.15, 0.20] h/Mpc`;
- the six frozen redshifts;
- the transfer-level `E_G` definition and sign convention;
- cubic-spline primary and PCHIP control interpolation;
- G1 through G8 thresholds;
- the R8a2 and R10a parent locks;
- all frozen artifact hashes;
- the prohibition on smoothing, clipping, extrapolation, and post-data scale selection.

The repaired implementation must import the frozen original R12a implementation and override only `R11A_R02_POSTDATA_LOCK` before calling its unchanged `main()` function.

## Classification discipline

The historical first invocation is a technical lock failure only. It is not an R12a science FAIL and does not evaluate any R12a gate beyond the shell-level ancestry precheck.

The next run is the first permitted R12a science evaluation under the corrected authoritative parent pointer.
