# GE19 Repair07 componentwise-backward-error constraint monitor lock

## Status

**IMPLEMENTATION LOCKED BEFORE REPAIR07 SCIENCE EXECUTION**

Repair06 remains historically frozen as

`GE19_REPAIR06_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`.

It is not relabeled.

## Repair06 result freeze

Commit:

`670990858ea38c56dbad1402eb360b7152d01350`

File:

`docs/ge19_repair06_reduced_h1_result_freeze.md`

Blob:

`db1097ff22a4df3212d6d9e78a2219e0dd1daa6c`

Frozen local science JSON / inner FULL-log:

- SHA256 `8371a22d19e2b0ce4eb57684e6c48b7ae2124fdea225da22093613f01c3a73e9`
- 46036 bytes

Frozen outer runner log:

- SHA256 `ff3766076330e7638796b987cd6e7c37dfde30d5f2e0195c6c33963faf06a867`
- 47976 bytes

## Repair07 preregistration

Primary prereg commit:

`ec93b9ebe23a5a5f0af3611c3291eb53fc55d777`

File:

`ge19/repair07_predata_row_scaled_constraint_monitors.json`

Blob:

`2fbe567620009096b9789738c25e42ce372615a3`

Pre-result amendment:

`d9e47705e98f22e36bd0a5fd53212962f1f67cc3`

File:

`ge19/repair07_predata_amendment01_componentwise_backward_error_scale.json`

Blob:

`05fa5ac42b3c182876893762163dd699fe299333`

The amendment tightens the denominator before any Repair07 science result from a loose operator norm bound to the componentwise backward-error scale.

## Final implementation

Final audited implementation commit:

`b129b1cebac4fb1d36060e4bef2a580eeb0e3b1f`

File:

`ge19/repair07_window_retarded_reduced_h3_z20_particular.py`

Blob:

`e34d28a2062c748f48bc82fa928844b02631de25`

Only the shift/anisotropy monitor normalization and associated diagnostics differ scientifically from Repair06.

The following remain frozen/source-identical under the executable audit:

- stable GE06 generator construction;
- stable background reconstruction;
- GE15/GE18 reference bridge;
- `main_and_constraints`;
- canonical/Noether operator matrices;
- initial canonical state construction;
- source interpolation;
- zero source construction;
- Radau-IIA integrator;
- H3 source construction;
- linear operator;
- collocation matrix utility.

All physical constants, grids, modes, C values, beta values and thresholds are unchanged.

## Final executable prelock audit

Workflow:

`.github/workflows/ge19-repair07-prelock-audit.yml`

Blob:

`3fb848eb344dcac9d9fd7dadb6d0e9c9962a6dd9`

GitHub Actions run:

`35538954732`

Job:

`106152969159`

Audited HEAD:

`b129b1cebac4fb1d36060e4bef2a580eeb0e3b1f`

Conclusion:

`success`

Terminal marker:

`GE19_REPAIR07_PRELOCK_AUDIT_PASS`

Static GE19 prelock audit on the same HEAD:

- run `35538954954`;
- conclusion `success`.

## Frozen monitor definition

For a scalar constraint row `C`, state/local vector `w`, and source `s`:

`r = C @ w - s`

and

`scale = max(|C@w|, |s|, sum_i |C_i w_i|, TINY)`.

The gate metric is

`|r| / scale`.

This is a componentwise backward error.

It is cancellation-safe but does not hide genuine same-sign violations.

The historical Repair06 piece-normalized monitor is still reported diagnostically and is not used for PASS/FAIL.

## Prelock falsification controls

A genuine same-sign violation with old piece metric `2.0` gives the new metric exactly

`1.0`.

An exact cancellation gives

`0.0`.

A near-cancellation residual of

`2.842170943040401e-14`

against actual contributions of approximately `2` gives

`1.4210854715202206e-14`.

Thus the Repair07 metric can distinguish an actual O(1) constraint defect from roundoff near a zero constraint.

Stable GE06 benign equivalence on final prelock:

- c1: `8.242856821646169e-16`;
- c2: `7.939971560854226e-16`;
- all outputs finite.

Physical c1/c2 probes remain finite.

## Unchanged Stage-A gates

- linear-system residual <= `1e-8`;
- shift constraint backward error <= `1e-6`;
- anisotropy constraint backward error <= `1e-6`;
- primary64/control32 state relative L2 <= `5e-3`;
- initial dynamic match abs-or-rel <= `1e-10`;
- all outputs finite.

No threshold was relaxed.

## Unchanged Stage-B gates

All frozen Repair06/GE19 Stage-B thresholds remain unchanged.

## Interpretation rule

If Repair07 Stage A passes while the historical piece-normalized diagnostics remain near 2 and 1, Repair06 is retained as historical FAIL and Repair07 establishes that the old failure was caused by an ill-conditioned monitor denominator.

If the new shift or anisotropy backward error remains above `1e-6`, this is not to be normalized away. It is then a genuine constraint-closure problem requiring a new preregistered repair.

## Claim boundary

Even a Repair07 full PASS licenses only the frozen reduced-matter, low-mode, window-retarded H3 particular coefficient in the formal epsilon->0 hierarchy.

It does not establish finite eta, finite physical-amplitude nonlinear evolution, collapse, lensing, or observational detection.
