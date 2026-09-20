# GE11 Repair01 precision-key binding — implementation lock

## Status

Implementation locked before the first GE11 Repair01 execution.

Historical GE11 remains:

`GE11_DENSE_LOCAL_JET_FIXED_REFINEMENT_FAIL`.

Historical GE09 remains FAIL and GE10 remains PASS.

## Parent freeze

GE11 result-freeze commit:

`ebca1a3828d6280a008946b4a64c1c102bd724e3`.

Artifact:

- workflow run `35495077694`;
- artifact ID `10600443147`;
- digest
  `sha256:cfacfd970606accfcc7fc816ca0d754c4fc87321d1e793f1e0b1b7d90cbbf9d6`.

## Repair01 preregistration

Commit:

`89d39bf9cd015d90cb76d60cf9a0ed324066a385`.

File:

`ge11/repair01_predata_precision_key_binding.json`.

Frozen blob:

`24fabf77ee957f2cbc825dc987ed38d3d40a6923`.

## Corrected fixed precision files

R1:

- commit `d6c65f47581be4afd2c86ca03a2a9cbea137aef4`;
- file `ge11/pre/R1_repair01.pre`;
- blob `7497e1a88cc15352641fcaacf7652ed6d6fb03f8`;
- `tol_perturbations_integration=2.5e-8`;
- `perturbations_sampling_stepsize=0.00125`.

R2:

- commit `60e41a22f292c2300ce586c7e5c1419c7f29970e`;
- file `ge11/pre/R2_repair01.pre`;
- blob `63c3be3891a9b4178b179a3f728e72245ea63934`;
- `tol_perturbations_integration=1.25e-8`;
- `perturbations_sampling_stepsize=0.000625`.

The numerical values are identical to frozen GE11.

Only the precision-key names are corrected.

## Repair01 implementation

Commit:

`c60b7b28614080ff531b757e39308c5a40ecaa78`.

File:

`ge11/repair01_dense_local_jet_fixed_refinement.py`.

Frozen blob:

`778e6a617af9f9584e4c1107f4c24bda561e6022`.

## Pinned CLASS precision identity

Pinned CLASS commit:

`e85808324f51fc694d12e3ed7439552a3c3f9540`.

Required active precision fields from `include/precisions.h`:

- `tol_perturbations_integration`;
- `perturbations_sampling_stepsize`.

Repair01 must fail at implementation level if these names are absent.

The obsolete singular names must be absent from both Repair01 precision files.

## Runtime identity gate

The R1 and R2 dense accepted-step traces must have different SHA-256 hashes.

If they are identical, classify:

`GE11_REPAIR01_PRECISION_BINDING_IMPLEMENTATION_FAIL`.

This gate exists only to confirm that the two corrected fixed precision levels are actually reaching the runtime.

## Frozen science representation and gates

Unchanged from GE11:

- six frozen k modes;
- `0.2<=z<=1.5`;
- 64 common uniform ln(a) nodes;
- CubicHermiteSpline for derivative-aware fields using fresh RHS/(aH);
- PCHIP for algebraic/background fields;
- every-second accepted-step internal control;
- complete 15-entry GE06 local jet;
- analytic Fourier spatial derivatives.

Single-level gates remain:

- dense trace versus official CLASS perturbation tables <= `1e-12`;
- at least 16 accepted points per k;
- exactly 64 common nodes;
- source-grid state validation <= `1e-4`;
- primary/decimated global relative L2 <= `5e-4`;
- primary/decimated pointwise abs-or-rel <= `2e-3`;
- pt identity <= `1e-12`;
- finite jet entries.

Refinement gates remain numerically unchanged.

Historical p3 terminology is replaced only by the more accurate
`historical runtime reference`.

## Terminal classifications

- `GE11_REPAIR01_DENSE_LOCAL_JET_FIXED_REFINEMENT_PASS`;
- `GE11_REPAIR01_DENSE_LOCAL_JET_FIXED_REFINEMENT_FAIL`;
- `GE11_REPAIR01_PRECISION_BINDING_IMPLEMENTATION_FAIL`.

## Project boundary

Even PASS certifies only the complete GE06 first-order local jet under this corrected fixed precision binding.

Historical GE09 and GE11 remain unchanged.

GE08 Repair01 standard-matter incompleteness remains active, so Repair01 PASS still does not by itself license `Z20`.
