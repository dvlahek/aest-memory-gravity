# GE19 H4F3d6 — first actual physical bath-parent Ward subset result freeze

## Classification and hard claim boundary

**`GE19_H4F3D6_ACTUAL_BATH_PARENT_WARD_SUBSET_PASS_FULL_OPEN`**.

The user supplied all four exact local result files, including the
actual physical NPZ, and the first hash-locked local physical run
passed every preregistered **subset** implementation/provenance gate.
This freezes the independently computed signed per-node normalized
GE05 first-order bath Euler contribution to the H4 mixed Ward ledger
on the actual corrected H3F/H3G/Z11/Repair13/R1 physical grids.

This is **not** an on-shell certificate for the saved physical
bath Euler trajectory, a full all-sector Noether certificate, a
new H4/Z21 science solve, finite-eta evolution, lensing or observation.
There was intentionally no source-only or source+bath Ward smallness
gate, and no ex post facto tolerance or hotspot adjustment.

## Independent uploaded-file provenance

The following local results were uploaded, read directly and
independently hashed, including the previously important binary:

| Original local result | Bytes | Verified SHA-256 |
|---|---:|---|
| `results/ge19_h4f3d6_actual_normalized_bath_parent_ward.json` | 17572 | `4607edde17c6820c85f32c0bbd774d5a58148eb01bfd0c81ce592e8c1b907791` |
| `results/ge19_h4f3d6_actual_normalized_bath_parent_ward.npz` | 1315867 | `17b50c6ee584b2a8886f7114a90ea9396a127172dd9e02976b0e6275fe2fedc0` |
| `results/ge19_h4f3d6_actual_normalized_bath_parent_ward_FULL.log` | 17572 | `4607edde17c6820c85f32c0bbd774d5a58148eb01bfd0c81ce592e8c1b907791` |
| `results/ge19_H4F3D6_LOCAL_runner.log` | 3297 | `74aef76c0d92b41a0e318fa1baeadbf2ecc45274b805e4e4ade16dc351fd3437` |

JSON and FULL log are byte-identical. NPZ was opened
with `allow_pickle=False`, has **32** fields and every numeric
field is finite. Each primary complex Ward field has
shape `(128,41)` and each time-control field
`(64,41)`. The 18 per-(C,beta,Nt) report-only maxima
for W_bath, W_source and W_source+W_bath are exactly
reproduced from the uploaded NPZ: maximum absolute
array-to-JSON diagnostic difference **0.0**.

Local runner markers:

`GE19_H4F3D6_LOCAL_LOCK_PASS`;
`GE19_H4F3D6_LOCAL_PREEXECUTION_PASS`;
`GE19_H4F3D6_H4F3B_SOURCE_INPUT_PASS`;
`GE19_H4F3D6_REPAIR26_R1_INPUT_PASS`;
`GE19_H4F3D6_ACTUAL_CORRECTED_PARENT_INPUT_PASS`;
`GE19_H4F3D6_ACTUAL_BATH_SUBSET_PASS_FULL_NOETHER_OPEN`.

All six recorded subset gates pass; `failed_gates=[]`.
There are 18 actual C × beta × Nt case entries.

## Frozen physical subset diagnostics

- Exact original Repair26 R1 weighted-z10 reconstruction
  against H3G: relative L2 `0.0` across all cases.
- For Nt128, `W_bath` max absolute is
  `1.2240389389117984e-14` (C_min),
  `1.2237907797992256e-14` (C_star) and
  `1.2234786133146418e-14` (C_max).
- Nt128 `W_source+W_bath` max absolute ranges
  `4.4639524882664554e-13` to
  `4.4679309239941164e-13`;
  Nt64 reaches `3.659645217615514e-12`.
- `W_source`, `W_bath` and their sum are
  **report only**, not a zero/ward-closure gate.

**Material unresolved observation:** The separately reported
GE05 physical normalized first-order bath Euler residual

`R_z10=H FD4_x(a^3 v10/tau)+a^3 omega^2(z10-X10)`

has natural-scale relative L2 between
`0.9985018009839012` and
`0.9993411932629498` on the actual Nt128/Nt64
grids, with Nt128 absolute L2 between
`9.269917659808491e-05` and
`9.684778205175287e-05`.
These numbers do not satisfy any asserted on-shell
smallness claim: such a gate was expressly absent.
They may include finite-difference/current
resolution error or a physical-clock/normalization
inconsistency and cannot be interpreted further without
an independent fixed-ODE/current/FD4 consistency test.

In particular, do **not** set the bath Euler term to zero
in a subsequent full Ward proof based solely on this
subset PASS. Conversely, do not label the entire theory
a physical FAIL from the report-only ratio before separating
FD4 discretization error from the frozen R1 trajectory
and the exact action-derived Euler operator.

## Immutable code and parent provenance

Preregistration:
`ge19/h4f3d6_predata_actual_normalized_bath_parent_ward.json`,
blob `d283086a6ae95efd184db570d6c2f9a8aa32ac7c`.

Source:
`ge19/h4f3d6_actual_normalized_bath_parent_ward.py`,
blob `0419145499f5f44e06ba0c96f779c2a604e84ce7`.

Runner:
`ge19/run_local_h4f3d6_actual_normalized_bath_parent_ward.sh`,
blob `3690147a766f276309d628fba9f436df3941deae`.

Earlier manufactured compiler PASS:
`docs/ge19_h4f3d6_bath_convolution_compiler_valid_freeze.md`,
blob `5695cc61be84098787af2cec8585f7daea6ced38`.
Earlier runner static PASS: GitHub run `36128447037`.

Actual frozen H4F3b six-piece source JSON/NPZ
SHA-256: `1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1`
and `787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b`.
H3F, H3G, Repair32B Z11, Repair13 and
Repair26 R1 parent hashes match original pinned inputs.

## Next structurally licensed step

Freeze/preregister a *separate* independent normalized-bath
physical-current/ODE discretization discrepancy audit before
assuming the bath Euler parent is numerically on shell.
It must preserve the frozen Repair24 propagator, R1 full-history
boundary, omega/r/tau normalization and the exact action.
It must compare FD4 `H D_x(a^3 v/tau)` with the
original propagator's physical clock/current derivative
using preregistered grid and error controls, and report all
boundary/interior and node-frequency contributions without
tuning time stencils or removing fast nodes post hoc.

In parallel, full H4F3d still requires independent signed
**nonbath** background/H1/Z11/corrected H3F/H3G parent Euler
and action-boundary contributions, plus the already frozen
canonical operator Ward, on the same actual H4F3b
parent/time representation. A physically justified FD4/FD8
structural truncation budget must be preregistered before
the first full all-sector residual test.

The prior Repair37 H4/Z21 science FAIL and Repair38--44
diagnostics remain immutable. Original active-shift
threshold `1e-6` and matched order `>=2.5` unchanged.
**Full H4 Noether NOT CERTIFIED. Z21 NOT CERTIFIED.
Lensing blocked.**
