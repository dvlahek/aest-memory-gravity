# GE11 fixed dense local-jet refinement — implementation lock

## Status

Implementation locked before first GE11 execution.

Historical GE09 remains FAIL.

GE11 is a new fixed refinement track licensed by GE10.

## Preregistration

Commit:

`9bb36f3e07b4f9c3f65567200f581c94bc4e7b1b`.

File:

`ge11/predata_dense_local_jet_fixed_refinement.json`.

Frozen blob:

`10516af16f0b39c1dcd94cf6ee8b6f84e9ff40a0`.

## Fixed precision files

R1:

- commit `fd4c6596aafbac4af91f68292a8d3cee202e31c2`;
- file `ge11/pre/R1.pre`;
- blob `2f6446c7e4fb2cf59f6145bfdc85be2b96be8c1a`;
- `tol_perturb_integration=2.5e-8`;
- `perturb_sampling_stepsize=0.00125`.

R2:

- commit `167054ece0f5772fa7f19d545795f3171613221e`;
- file `ge11/pre/R2.pre`;
- blob `1f886429d480f2167df07235533c55be4a5f1330`;
- `tol_perturb_integration=1.25e-8`;
- `perturb_sampling_stepsize=0.000625`.

No third level is licensed by the first GE11 outcome.

## Implementation

Commit:

`d087289a9be3348e65f528211ab6c5fa9518c670`.

File:

`ge11/dense_local_jet_fixed_refinement.py`.

Frozen blob:

`be3e57829e961079bd20467c8ca0f34a4b1d1316`.

Frozen imported GE09 driver:

- file `ge09/repair01_dense_accepted_step_local_jet_bridge.py`;
- blob `509fa9d7bb323034bbf77b26792f35e1cc2ff7c7`.

GE10 result freeze:

- blob `9a410cef15bc873f24972a3e92136d1aff76d753`.

## Frozen representation

Unchanged from GE09:

- six k modes;
- `0.2<=z<=1.5`;
- 64 common uniform ln(a) nodes;
- CubicHermiteSpline for derivative-aware fields using fresh RHS/(aH);
- PCHIP for algebraic/background fields;
- every-second endpoint internal control;
- complete 15-entry GE06 jet;
- analytic Fourier spatial derivatives.

## Per-level frozen gates

For both R1 and R2:

- dense trace versus official CLASS perturbation tables <= `1e-12`;
- at least 16 accepted points per k;
- exactly 64 common nodes;
- source-grid state validation <= `1e-4`;
- primary/decimated global jet relative L2 <= `5e-4`;
- primary/decimated pointwise abs-or-rel <= `2e-3`;
- pt identity <= `1e-12`;
- finite jet entries.

## Refinement gates

Require:

- R1 accepted point count per k >= frozen p3;
- R2 accepted point count per k >= R1;
- R1 max ln(a) gap per k <= frozen p3;
- R2 max ln(a) gap per k <= R1;
- R2 source-validation maximum <= R1;
- R1/R2 complete-jet global relative L2 <= `5e-4`;
- R1/R2 complete-jet pointwise abs-or-rel <= `2e-3`.

## Terminal classifications

- `GE11_DENSE_LOCAL_JET_FIXED_REFINEMENT_PASS`;
- `GE11_DENSE_LOCAL_JET_FIXED_REFINEMENT_FAIL`.

## Project boundary

PASS certifies the complete GE06 first-order local jet **under GE11**.

It does not relabel historical GE09.

GE08 Repair01 standard-matter incompleteness remains active, therefore even GE11 PASS does not license Z20.

No adaptive/tolerance sequence is licensed after the first GE11 execution.
