# GE19 Repair03 reduced-H1 result — historical FAIL freeze

## Status

The first locked GE19 Repair03 local execution reached Stage A and terminated with

`GE19_REPAIR03_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`.

Historical classification is immutable.

The execution did not construct Z20.

## Local result provenance

Uploaded result files:

- JSON:
  - bytes: `11137`;
  - SHA-256:
    `9dab09eca02a05c85fcb09ebebe64d9428a7bac79e78cd30b60713c3d28dbe37`;
- full log:
  - bytes: `11137`;
  - SHA-256:
    `9dab09eca02a05c85fcb09ebebe64d9428a7bac79e78cd30b60713c3d28dbe37`;
- runner log:
  - bytes: `14918`;
  - SHA-256:
    `a99294ee21678f0a944c5ee023b6d3d3cfc951c280990937293bfbde4548084d`.

## Stable Exp controls

All Repair03 stable-Exp controls passed:

- native I0/background reconstruction passed;
- GE06 benign c1/c2 equivalence was O(1e-15);
- all 7 c1 and all 7 c2 exponential arguments canonicalized exactly to `Zb**2`;
- physical-parameter c1/c2 probe was finite.

Thus the earlier overflow defects were removed.

## Observed Stage-A numbers

Across all three C cases and both 64/32 grids:

- linear-system residual maximum:
  `2.034605278964149e-17`;
- initial dynamic match maximum:
  `1.084689953737024e-17`;
- shift-constraint normalized residual maximum:
  `1.0113389909151673`;
- anisotropy-constraint normalized residual maximum:
  `1.0000000000000002`;
- 64/32 state relative-L2 maximum:
  `0.06444781481790336`.

The failed gates were shift constraint, anisotropy constraint and time-grid convergence.

## Post-run implementation diagnosis

The Stage-A result cannot be interpreted as a valid reduced-H1 physics failure because the active linear-operator wiring is incorrect.

The Repair03 stable GE06 generator signature is

`(aa, adot, Zb, ...)`.

However `linear_operator_batch()` supplies

`bg["Q_action"]`

as the third argument.

The correct argument is

`bg["Z_action"]`.

Numerically, the intended physical coordinate in the frozen window is

`Zb ~= 4.45--4.69`,

while `Q_action` is O(`1e-4`) in Mpc^-1.

Therefore the sparse collocation system solved to O(1e-17) residual is the wrong linear operator. The O(1) independent constraints and 6.4% grid drift are not valid evidence against reduced H1 closure.

## Additional provenance-gate issue

The implementation also added a non-preregistered gate

`GE15_background_mode_mismatch <= 1e-10`.

The observed diagnostic is

`2.14156901519004e-6`.

This quantity compares separately interpolated background traces carried inside different k-mode perturbation files.

It is redundant with and weaker in meaning than the exact/frozen controls already present:

- exact GE15 dense hash;
- GE15 frozen 64-node complete-jet error `0.0`;
- exact GE18 NPZ hash;
- GE15/GE18 metric bridge error `0.0`;
- native conserved-I0 reconstruction errors O(1e-14).

It was not an original GE19 science gate.

A Repair04 may retain this per-k interpolation mismatch as a descriptive diagnostic but remove it from PASS/FAIL provenance.

## Licensed Repair04

Repair04 may change only:

1. the third GE06 argument in the active linear operator from
   `Q_action` to `Z_action`;
2. the non-preregistered per-k interpolated-background mismatch from a provenance gate to a descriptive diagnostic.

Repair04 must not change:

- any Stage-A science threshold;
- any Stage-B science threshold;
- stable Exp reconstruction;
- canonical symbolic generator;
- matter model;
- modes/phases;
- beta0/C values;
- time/spatial grids;
- gauge;
- initial matching prescription;
- window-retarded convention.

## Claim boundary

Repair03 remains a historical FAIL, but its Stage-A constraint/grid numbers are implementation-contaminated and do not establish a physical failure of reduced H1 closure.
