# GE19 Repair39 frozen-source stage-interpolation localization — implementation lock

## Status

Repair39 is frozen before its first local diagnostic execution.

Repair39 is diagnostic only. It cannot relabel Repair37 or Repair38, certify
Z21, alter the frozen `1e-6` science target, or license lensing.

Its sole purpose is to test whether the remaining Repair38 shift floor depends
materially on the off-node source-at-stage interpolation rule.

## Frozen Repair38 parent

Valid diagnostic freeze:

`docs/ge19_repair38_valid_diagnostic_pchip_or_other_floor_freeze.md`.

Freeze commit:

`ada593c99c7bc217313b1f7c8ff99504f13e8d10`.

Freeze blob:

`040af5dcb90070d05e3ab7e98623a4e03aa25009`.

Frozen Repair38 artifacts:

- JSON/FULL SHA-256:
  `08dd95c614118c66e37349e2b8d058e85163812fed77c9b048e0ce57e339e5dd`;
- NPZ SHA-256:
  `aff63771c1800b0db236cd020cf0d2772f6d9a0fd0328573d055392f2c60da67`;
- outer runner SHA-256:
  `6e6b4477528ca63858a14f2fecf7bd2183498739b4c6a4d8db2d4cf3ba10dd16`.

Frozen Repair38 route:

`PCHIP_OR_OTHER_FLOOR_REMAINS`.

## Frozen preregistration

File:

`ge19/repair39_predata_frozen_source_stage_interpolation_localization.json`.

Preregistration commit:

`87aff396a2a8505b50001a1a5169a3167477e1f7`.

Blob:

`7f289263768e0eb1e3a9af47ecc6b10f71f0065a`.

## Frozen implementation

File:

`ge19/repair39_frozen_source_stage_interpolation_localization.py`.

Implementation commit:

`0ae58cc9c71c7afac85654b30a85162d27d79f4f`.

Blob:

`91e65251198983205394196893b862f08dd2a585`.

Repair39 loads, rather than reconstructs:

- Repair37 Nt128 total H4 main source nodes;
- Repair37 Nt128 total H4 constraint-source nodes;
- Repair37 projected p0;
- Repair37 shift-scale arrays defining the active mask;
- Repair38 factor2/factor4 propagated outputs defining the frozen numerical
  reference scale.

No GE06/GE07 Q source, DY2 source, memory source or Lambda mixed source is
recomputed.

## Only varied numerical control

The fixed internal propagation is Repair38 endpoint-safe two-stage Radau IIA
with four internal substeps per frozen Nt128 interval.

Only the off-node source-at-stage interpolation varies:

1. `PCHIP` — exact Repair07/Repair38 baseline;
2. `CUBIC_SPLINE` — scipy CubicSpline, not-a-knot, extrapolate=False;
3. `AKIMA` — scipy Akima1DInterpolator, extrapolate=False.

Real and imaginary parts are interpolated separately. Main and constraint
sources use the same method.

Every method must reproduce the original frozen source nodes within relative
L2 <= `1e-12`.

## PCHIP reproduction rule

Before any interpolation sensitivity is interpreted, Repair39 PCHIP factor4
must reproduce frozen Repair38 substep4:

- Z21 global relative L2 <= `1e-11`;
- active shift-metric relative L2 <= `1e-10`;
- frozen active sample count exactly `23850`;
- all outputs finite.

A failure is an implementation failure, not a diagnostic result.

## Frozen diagnostic scale

The reference numerical scale is not tuned from Repair39 output.

It is the already frozen Repair38 PCHIP factor2-to-factor4 change in the same
active shift-metric field.

For each independent interpolant, Repair39 computes:

`R = RMS(m_alt - m_PCHIP4) / RMS(m_PCHIP4 - m_PCHIP2)`.

Routing is frozen as follows:

- `STAGE_SOURCE_REPRESENTATION_DEPENDENCE_CONFIRMED` if at least one
  independent interpolant has `R >= 4`;
- `STAGE_SOURCE_REPRESENTATION_INVARIANT_OTHER_FLOOR` if both independent
  interpolants have `R <= 1`;
- otherwise
  `MIXED_STAGE_REPRESENTATION_SENSITIVITY`.

Alternative Linf/RMS values and whether an alternative is below `1e-6` are
report-only. No interpolant is declared physically preferred inside Repair39.

## Dedicated prelock

Workflow:

`.github/workflows/ge19-repair39-prelock-audit.yml`.

Workflow commit:

`9bcfdd4d9d93d7739079c3034bc7b9fe7dd32ac0`.

Workflow blob:

`2470783b6cd3307c8d03922ebe9391cc82ebbd6b`.

Run:

`35870448283`.

Job:

`107212831905`.

Conclusion:

`success`.

The prelock verifies the frozen-node interpolation-only contract, PCHIP
baseline identity, fixed factor4 Repair38 propagation, frozen source/p0
loading, absence of H4 source builders, and the preregistered routing.

## Claim boundary

Repair39 cannot certify Z21, finite eta, full-species nonlinear cosmology,
lensing or any observational signal.

Repair39 cannot relabel Repair37 or Repair38.

It is a source-at-stage numerical localization test only.
