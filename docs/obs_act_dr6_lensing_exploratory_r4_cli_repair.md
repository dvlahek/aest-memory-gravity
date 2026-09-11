# ACT DR6 exploratory lensing R4 — CLASS CLI/output-path technical repair

Date: 2026-09-11

Status: frozen after R3 returned INCOMPLETE and before any R4 ACT likelihood output.

## Historical status

The original exploratory scan and R1–R3 remain `ACT_DR6_LENSING_EXPLORATORY_SCAN_INCOMPLETE`. R3 established that `classy.raw_cl()` returned non-finite `pp` values at every physical multipole L=2..4000 already for the memory-disabled eta=0 reference. No ACT likelihood point was produced by those runs.

D2C6H remains a formal FAIL. Therefore every R4 result remains exploratory and `OBSERVATIONAL_CLAIM_LICENSED=False`.

## Technical diagnosis and frozen repair

The historical v0.62 ACT DR6 lensing implementation did not obtain the lensing spectrum through `classy.raw_cl()`. It ran the pinned CLASS executable with the high-precision file `v019p/pre/p3.pre`, requested `output=tCl,pCl,lCl`, and read the CLASS `_cl.dat` file. Its phi-phi column was converted to raw convergence power before multiplication by the official ACT binning matrix.

R4 restores exactly this CLASS execution/output path while retaining the current finite-memory implementation and the already frozen R1–R3 observational scope.

This is a technical output-path repair only. It does not change the AeST equations, memory closure, background cosmology, ACT data selection, eta values, or likelihood covariance.

## Frozen model and likelihood

- upstream CLASS SHA: `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- current zero-safe finite-memory patch chain, including tau-H0 memory implementation, memory order 39, eta=0 passive decoupling and current sparse-k support;
- fixed cosmology: the same `v063.START` values used by R1–R3;
- `K_B=0.0665`;
- `tau H0=1`;
- memory order 39;
- eta grid: `{0,1/256,1/128,1/64,1/32,1/16,1/8}`;
- `l_max_scalars=4000`;
- `output=tCl,pCl,lCl`;
- `lensing=yes`;
- `non linear=halofit` (exploratory, as already frozen);
- precision file `v019p/pre/p3.pre`;
- ACT DR6 likelihood package `act_dr6_lenslike==1.2.1`, data v1.2;
- variant `act_baseline`;
- `lens_only=True`;
- primary-CMB likelihood corrections disabled;
- `trim_lmax=2998`, so the official ACT matrix uses L=0..2999.

No cosmological or nuisance parameter is refit.

## Frozen spectrum extraction

From CLASS `_cl.dat` in class-format ordering, file column 5 is `D_L^{phi phi}=L(L+1)C_L^{phi phi}/(2 pi)` for `output=tCl,pCl,lCl`.

R4 constructs

`C_L^{kappa kappa} = (pi/2) L(L+1) D_L^{phi phi}`.

All values inside the ACT-required support L<=2999 must be finite. No non-finite value inside that support may be masked or interpolated. Values above ACT support are diagnostic only.

The official likelihood is evaluated directly as

`b = binmat_act @ Ckk[:n_theory]`,
`chi2 = (data-b)^T cinv (data-b)`.

## Eta=0 technical regression

Before the eta scan, run:

1. memory disabled, eta=0;
2. memory enabled, eta=0.

Both spectra must be finite over ACT support and have relative L2 difference <=1e-8 over L=2..2999. Failure leaves R4 INCOMPLETE.

## Output

For each frozen eta value report fixed-cosmology ACT DR6 lensing chi2 and `delta_chi2_vs_eta0`. Report the best discrete grid point only as exploratory.

Complete label:
`ACT_DR6_LENSING_EXPLORATORY_R4_COMPLETE`

Incomplete label:
`ACT_DR6_LENSING_EXPLORATORY_R4_INCOMPLETE`

A COMPLETE result is not a detection, posterior, final bound, or licensed observational claim.