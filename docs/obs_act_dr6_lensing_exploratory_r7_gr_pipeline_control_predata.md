# ACT DR6 exploratory lensing R7 — GR pipeline control

Date: 2026-09-11

Status: frozen before any R7 ACT likelihood output.

## Motivation

R5 certified a finite linear CLASS lensing baseline and exact memory-on/off regression at eta=0. R6 then started the frozen positive-eta scan, but the first two points returned extremely large ACT DR6 lensing chi-square values. Before assigning any physical interpretation to those R6 values, R7 isolates the CLASS-to-ACT interface with an AeST-off control.

## Single question

Does the identical CLASS -> C_L^{kappa kappa} -> ACT DR6 standalone lensing pipeline return a numerically ordinary finite result when AeST is disabled?

## Frozen execution path

R7 inherits the R6 checkpoint `f4280426267e397af18f066d2c7c0755b7a105fa` and uses:

- upstream CLASS SHA `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- the same current zero-safe finite-memory CLASS source tree and precision file `v019p/pre/p3.pre`;
- the same fixed cosmology as R6;
- `l_max_scalars=4000`;
- `output=tCl,pCl,lCl`;
- `lensing=yes`;
- linear theory only, with no `non linear` entry;
- `aest_enabled=no`;
- no memory parameters used by the GR prediction;
- CLASS executable plus `_cl.dat` extraction.

No cosmological parameter, likelihood option, trimming rule, binning matrix, covariance, or spectrum conversion may be changed after seeing the R7 result.

## Frozen ACT DR6 likelihood

- package `act_dr6_lenslike==1.2.1`;
- official data version `v1.2`;
- variant `act_baseline`;
- `lens_only=True`;
- `like_corrections=False`;
- `trim_lmax=2998`;
- 10 ACT lensing bins.

## Frozen CLASS-to-ACT spectrum conversion

The CLASS-format `_cl.dat` file reports the lensing-potential column as

`D_L^{phi phi} = L(L+1) C_L^{phi phi}/(2 pi)`.

Construct

`C_L^{kappa kappa} = (pi/2) L(L+1) D_L^{phi phi}`.

For every physical multipole `L=2..2999`, the resulting spectrum must be finite and nonzero. No value may be masked, interpolated, clipped, or replaced.

ACT theory and chi-square are computed exactly as in R6:

`binned_theory = binmat_act @ C_L^{kappa kappa}`

`chi2 = (data-binned_theory)^T cinv (data-binned_theory)`.

## R7 completion gates

R7 COMPLETE requires only:

1. the R6 checkpoint and this preregistration are ancestors of the executed code;
2. CLASS completes successfully with `aest_enabled=no`;
3. `C_L^{kappa kappa}` is finite and nonzero for all `L=2..2999`;
4. all 10 binned-theory values and the ACT chi-square are finite.

No numerical chi-square threshold is a preregistered gate. The purpose is diagnostic, not to manufacture a pass/fail around the observed value.

## Outputs

Record:

- ACT chi-square;
- physical-spectrum min/max;
- ACT band centers;
- ACT data bandpowers;
- binned GR theory;
- residuals;
- CLASS log and `_cl.dat`.

Successful execution label:

`ACT_DR6_LENSING_EXPLORATORY_R7_GR_PIPELINE_CONTROL_COMPLETE`

Otherwise:

`ACT_DR6_LENSING_EXPLORATORY_R7_GR_PIPELINE_CONTROL_INCOMPLETE`.

Always:

`OBSERVATIONAL_CLAIM_LICENSED=False`.

## Interpretation rule

R7 does not validate or falsify AeST by itself. A finite GR result comparable in scale to the ACT bandpowers would support the CLASS-to-ACT interface and redirect the R6 anomaly toward the AeST lensing prediction. A similarly pathological GR result would instead indicate that the interface/convention path still requires repair.