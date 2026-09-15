# Stable AeST cosmic memory R8a — post-data record

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Historical classification

R8a remains formally classified as

`STABLE_AEST_COSMIC_MEMORY_R8A_RUN_FAIL`.

This classification is not changed by later follow-up work.

## What completed

All 20 frozen tau/eta runs completed, were finite, and were domain-positive on the preregistered grid

`tau H0 = [10.0, 5.0, 2.5, 1.25]`

with

`eta = [0, +/-0.025, +/-0.05]`.

Source topology and parent provenance passed.

## Why G3 failed

The preregistered R8A-G3 required eta-zero observables at every tau to match the tau10 eta-zero baseline at

`E <= 1e-10` and `C >= 0.9999999999`.

The actual eta-zero differences were tiny but exceeded the frozen `1e-10` relative-error threshold. The largest observed baseline relative error was of order `1.6e-9` (effective f sigma8), while all corresponding cosines were numerically unity.

Thus the formal failure is caused by an over-strict cross-tau eta-zero numerical-identity gate. Because G3 is earlier in the preregistered gate hierarchy, R8a did not license reporting tau-dependent derivative amplitudes or shapes from this run.

## Interpretation discipline

This post-data record does not alter the R8a preregistration and does not reclassify R8a.

No tau-amplitude or tau-shape science claim is licensed from R8a itself.

A separate follow-up must use a precision-qualified baseline rule fixed before its own results. The follow-up should normalize each derivative by its own same-tau eta-zero baseline and test eta-zero numerical precision with nominal-versus-tight integration tolerance, instead of requiring cross-tau auxiliary-bath trajectories to agree at `1e-10`.
