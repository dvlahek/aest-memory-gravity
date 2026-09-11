# ACT DR6 exploratory lensing R6 — linear-theory eta scan

Date: 2026-09-11

Status: frozen after R5 PASS and before any R6 ACT eta likelihood output.

## Historical status preserved

R5 returned

`ACT_DR6_LENSING_EXPLORATORY_R5_LINEAR_BASELINE_PASS`

with finite linear CLASS lensing spectra for memory-off eta=0 and memory-on eta=0 over every physical multipole L=2..2999, and exact memory-on/off regression at eta=0.

R4 remains `ACT_DR6_LENSING_EXPLORATORY_R4_INCOMPLETE` because the AeST nonlinear/Halofit lensing interface produced non-finite lensing power. D2C6H remains a formal FAIL. Therefore this R6 stage is explicitly exploratory and `OBSERVATIONAL_CLAIM_LICENSED=False` remains frozen.

R6 does not repair or use the unresolved AeST nonlinear/Halofit lensing interface.

## Purpose

R6 performs the ACT DR6 standalone lensing likelihood scan that R5 licensed, using linear CLASS lensing only. No additional numerical bridge or theory modification is introduced.

The question is purely exploratory: on the frozen current AeST+memory implementation, how does the ACT DR6 standalone lensing chi-square vary over the already declared positive eta grid when the lensing spectrum is evaluated in linear theory?

## Frozen theory and execution path

- upstream CLASS SHA: `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- current zero-safe finite-memory patch chain from `nl1c6d2c6c_r5/setup_zero_safe_class.sh`;
- fixed cosmology identical to R5/R4/v063 START;
- `K_B=0.0665`;
- `tau H0=1`;
- memory order 39;
- `l_max_scalars=4000`;
- `output=tCl,pCl,lCl`;
- `lensing=yes`;
- linear theory only: no `non linear` entry;
- precision file `v019p/pre/p3.pre`;
- CLASS executable + `_cl.dat` extraction;
- no direct R2/H quadratic metric stress is inserted into linear CLASS.

The eta grid is frozen to

`eta = {0, 1/256, 1/128, 1/64, 1/32, 1/16, 1/8}`.

No adaptive refinement or post-data grid change is allowed inside R6.

## Frozen ACT DR6 likelihood

- package `act_dr6_lenslike==1.2.1`;
- official data version `v1.2`;
- variant `act_baseline`;
- `lens_only=True`;
- `like_corrections=False`;
- `trim_lmax=2998`;
- 10 ACT lensing bins.

No primary-CMB likelihood contribution is included.

## Frozen spectrum extraction

Read CLASS `_cl.dat` column 5,

`D_L^{phi phi}=L(L+1) C_L^{phi phi}/(2 pi)`,

and construct

`C_L^{kappa kappa} = (pi/2) L(L+1) D_L^{phi phi}`.

For every eta point, `C_L^{kappa kappa}` must be finite and nonzero at every physical multipole L=2..2999. No non-finite value may be masked, interpolated, clipped or replaced.

ACT chi-square is computed exactly from the official likelihood data arrays:

`binned_theory = binmat_act @ C_L^{kappa kappa}`

and

`chi2 = (data-binned_theory)^T cinv (data-binned_theory)`.

## R6 gates

R6 COMPLETE requires all of:

1. provenance confirms the R5 executed head and this R6 preregistration are ancestors of the executed code;
2. memory-off eta=0 and memory-on eta=0 linear spectra are finite/nonzero on L=2..2999;
3. eta=0 memory-on/off relative L2 spectrum difference is <= `1e-8`;
4. all seven frozen eta points return successfully with finite/nonzero linear `C_L^{kappa kappa}` over L=2..2999;
5. all seven ACT DR6 chi-square values are finite.

No sign, monotonicity, preferred eta, delta-chi-square magnitude or detection threshold is a gate.

## Outputs

Record for each eta:

- eta;
- ACT DR6 chi-square;
- delta chi-square relative to eta=0;
- min/max Ckk;
- relative L2 spectrum shift relative to eta=0.

Save full spectra, binned theory, ACT data vector, bin centers, chi-square and delta-chi-square arrays in NPZ, plus CLASS logs and `_cl.dat` files in the local bundle.

## Classification and interpretation

Successful execution label:

`ACT_DR6_LENSING_EXPLORATORY_R6_LINEAR_ETA_SCAN_COMPLETE`

Otherwise:

`ACT_DR6_LENSING_EXPLORATORY_R6_LINEAR_ETA_SCAN_INCOMPLETE`.

Always:

`OBSERVATIONAL_CLAIM_LICENSED=False`.

R6 may identify an exploratory best grid point or an exploratory trend in ACT DR6 lensing likelihood, but it cannot support a physical ACT constraint or detection because the AeST-specific nonlinear/Halofit lensing interface remains unresolved and D2C6H remains a formal FAIL.