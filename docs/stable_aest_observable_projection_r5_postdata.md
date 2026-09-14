# Stable AeST observable projection R5 — post-data record

Date: 2026-09-14

## Frozen parent and preregistration

R5 pre-data lock: `773ee8b0ab1d41dc1737eaf53f1961ea2f644bde`.

Parent R4 classification: `STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SINGLE_AMPLITUDE_MODE_CERTIFIED`.

R5 does not alter or reinterpret any historical R1–R4 classification.

## Formal R5 classification

`STABLE_AEST_OBSERVABLE_PROJECTION_R5_ETA_SCALING_FAIL`

Runner exit: 1.

This is a completed science classification, not a technical pre-result failure.

## Completed runs and source topology

All five preregistered physical runs completed finite and positive:

- nominal eta=0, tolerance 3e-8,
- nominal eta=1, tolerance 3e-8,
- nominal eta=10, tolerance 3e-8,
- tight eta=0, tolerance 1e-8,
- tight eta=10, tolerance 1e-8.

The disposable source passed the single-channel audit: stable-chi marker present, one physical eta multiplier, one physical memory closure, and zero diagnostic external-force injections in `perturbations_derivs`.

## Formal gates

- G1 provenance/parent lock: PASS.
- G2 single-channel source topology: PASS.
- G3 finite observable runs: PASS.
- G4 physical-eta tangent consistency: FAIL.
- G5 precision stability: formally FALSE because the implementation gates G5 on G4, even though the standalone nominal-vs-tight precision metrics pass for all three observables by a large margin.
- G6 resolved observable response: formally FALSE because the implementation gates G6 on G5.

No R5 observable-projection claim is licensed.

## Eta-scaling result

The preregistered comparison of `T_X(1)` and `T_X(10)` gives:

- sigma8: E = 0.11266478285032307, C = 0.9975324205333668 — FAIL strict eta consistency.
- effective f sigma8: E = 0.04409864896301453, C = 0.999083853374621 — PASS strict eta consistency individually.
- C_L^{kappa kappa}: E = 0.9426180983451122, C = 0.40925964658412195 — strong FAIL.

Therefore eta=10 is not licensed as a first-order observable amplifier in this setup.

## Precision-control result

Standalone nominal-vs-tight eta=10 tangent comparisons are extremely stable:

- sigma8: E = 2.299142795935231e-7, C = 0.9999999999999748.
- effective f sigma8: E = 7.050909885178742e-7, C = 0.9999999999998969.
- C_L^{kappa kappa}: E = 1.7994033046348887e-7, C = 0.9999999999999988.

Thus the R5 failure is not attributable to the tested perturbation-tolerance change from 3e-8 to 1e-8.

## Response magnitudes at eta=10

The eta=10 tangent vectors are finite and nonzero:

- sigma8: norm = 1.11687216104434e-6, max = 1.058105293844844e-6.
- effective f sigma8: norm = 7.169273211422456e-6, max = 6.371480404930432e-6.
- C_L^{kappa kappa}: norm = 3.8922480442403875e-4, max = 2.1967794435129492e-5.

These nonzero vectors do not by themselves license a first-order observable response because G4 failed.

## Post-data interpretation

R5 rejects the specific preregistered assumption that eta=10 can be used as a response-amplified first-order proxy simultaneously for sigma8, effective f sigma8, and linear CMB lensing convergence.

The result does not reject the R4 single-amplitude mode on its tested transfer-function domain. R4 used eta=0.005 and 0.01 on stable k anchors around 0.1–0.2 h/Mpc. R5 instead projects over integrated observables, especially CMB lensing, which mixes a much broader range of scales and times.

The excellent nominal-vs-tight agreement indicates that the observed eta dependence is not explained by the tested integration-tolerance floor. The appropriate follow-up is a separately preregistered small-eta observable scan near eta=0, rather than a larger eta amplifier.

No ACT, DESI, RSD, CMB-lensing likelihood, observational detection, parameter bound, or positive growth–Weyl separation claim is licensed by R5.
