# Stable AeST DESI DR1 R9b2d k-grid inheritance audit preregistration

## Purpose

R9b2c ended as the historical theory-only failure

`STABLE_AEST_DESI_DR1_R9B2C_NATIVE_AEST_STATE_FAIL`.

Post-result code inspection found a concrete configuration asymmetry. The Stable-AeST R5b/R9 parameter path inherits the old spectral-fringe forensic builder, whose corrected CLASS baseline explicitly sets

- `k_per_decade_for_pk = 80.0`
- `k_per_decade_for_bao = 560.0`.

The underlying v0.63 physical parameter set does not set these keys. R9b2c correspondingly produced approximately 864 AeST k nodes but only approximately 108 nodes in its ordinary GR control.

R9b2d tests only if this inherited dense-k forensic configuration is responsible for the eta=0 transfer/source-state pathology. It is a theory-only A/B configuration-isolation test. No DESI data vector, covariance, likelihood, derivative, matched filter, eta preference, or tau constraint is evaluated.

## Frozen provenance

Required ancestors:

- R9b2c post-result record: `7c4cc8a0a9f2a59a91cbb288a157f880d630f309`
- R9b2c preregistration: `1e999d87c1158ee7be764e6055164d75a179b059`
- R9b2c implementation: `cb15af792b6d2deca3c495a47f75238986e85c00`
- R9b2b postdata: `3101581468bc8a5b85eb2b34c33df22418f1ce88`
- R9b2a postdata: `00d06aa140fc8e9097be3df62ecd6013f0c8b312`
- corrected CLASS parent remains `e85808324f51fc694d12e3ed7439552a3c3f9540`.

Historical classifications remain unchanged, including

- `STABLE_AEST_DESI_DR1_R9B2_CENTRAL_DERIVATIVE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2A_SERIALIZATION_FREE_EXTRACTION_UNRESOLVED`
- `STABLE_AEST_DESI_DR1_R9B2B_AEST_ETA0_CLOSURE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2C_NATIVE_AEST_STATE_FAIL`.

## Frozen theory coordinates and physics

Use the same six redshifts, only as theory coordinates:

- 0.29536404346937617
- 0.5096288678782911
- 0.7057956472488681
- 0.9185851971138159
- 1.3170658832980264
- 1.4905017757527006.

Stable AeST settings are frozen to

- `eta = 0`
- `tau_H0 = 10`
- `aest_memory_order = 20`
- `tol_perturbations_integration = 3e-8`
- `output = mPk,mTk,vTk`
- `P_k_max_h/Mpc = 5`
- `z_max_pk >= 2.3`
- no nonlinear correction
- no lensing
- no `k_output_values` request
- same corrected/stable-chi CLASS source and executable used by R9b2b/c.

No physical AeST parameter may differ between the A/B variants.

## Frozen A/B variants

### Variant DENSE

Start from the exact R5b eta=0 parameter constructor and preserve the inherited spectral-fringe precision settings:

- `k_per_decade_for_pk = 80.0`
- `k_per_decade_for_bao = 560.0`.

Remove only output requests already removed in R9b2b/c (`k_output_values`, `l_max_scalars`, nonlinear/lensing where applicable) and set the common transfer-output settings above.

### Variant DEFAULT

Start from an exact copy of DENSE and remove only

- `k_per_decade_for_pk`
- `k_per_decade_for_bao`.

No other parameter is changed. CLASS therefore uses its normal/default k sampling.

### GR controls

For each of DENSE and DEFAULT, run an otherwise identical control with

- `aest_enabled = no`
- `aest_memory_enabled = no`
- `aest_eta = 0`.

The GR controls test that the sampling change by itself does not create a material physical-observable shift.

## Frozen extraction

Use the same source-consistent extraction already validated in pure GR by R9b2b:

- read `d_b,d_cdm,t_b,t_cdm` from `get_transfer(z, output_format="class")`
- `d_cb = f_b d_b + f_c d_cdm`
- `v_b = -t_b/Hconf`, `v_cdm = -t_cdm/Hconf`
- `v_cb = f_b v_b + f_c v_cdm`
- `P_dd = C(k) d_cb^2`
- `P_tt = C(k) v_cb^2`
- compute `sigma8_dd`, `sigma8_tt`
- compute `f_source = sigma8_tt/sigma8_dd` only after integration.

Forbidden inside the extraction:

- `pk_lin`
- `pk_cb_lin`
- local `v_cb/d_cb`
- changing or filtering individual suspicious k points.

For each model also record the k-node count from `get_transfer_and_k_and_z(...)` over the same k support. The node count is diagnostic only and is not itself a physical observable.

## Frozen gates

Set `REL_GATE = 5e-3`, inherited from the validated GR adapter and R9b2b/c. Set `MATERIAL_GATE = 5e-2`, inherited from the earlier localization audits.

### D1 — provenance and configuration-isolation gate

PASS if all frozen ancestors exist and the implementation verifies that DENSE and DEFAULT differ only in the two k-sampling keys, with DENSE exactly `80/560` and DEFAULT omitting both.

### D2 — node-count separation gate

PASS if AeST DENSE has at least four times as many transfer/Fourier k nodes as AeST DEFAULT over the common support.

The factor-four gate is intentionally weaker than the already observed approximately eightfold difference and is frozen before the run.

### D3 — GR sampling invariance gate

At all six redshifts, PASS if DENSE-GR versus DEFAULT-GR relative differences in each of

- `sigma8_dd`
- `sigma8_tt`
- `f_source`

are <= `5e-3`, and both variants are finite and physical:

- `0.1 < sigma8_dd < 2`
- `0.05 < f_source < 2`.

### D4 — DEFAULT AeST eta=0 closure gate

PASS if at all six redshifts DEFAULT AeST has

- finite positive spectra
- `0.1 < sigma8_dd < 2`
- `0.05 < f_source < 2`
- relative difference `sigma8_dd` versus CLASS internal `sigma(8,z,h_units=True)` <= `5e-3`
- relative difference `f_source` versus the historical internal growth proxy `effective_f_sigma8/sigma8` <= `5e-3`.

The internal growth proxy is only a closure control and is not adopted as a DESI observable definition.

### D5 — DENSE pathology reproduction gate

PASS if DENSE AeST reproduces a material pathology while DEFAULT AeST satisfies D4. Material pathology is defined before the run as at least one of:

- a DENSE point violates `0.1 < sigma8_dd < 2`
- a DENSE point violates `0.05 < f_source < 2`
- max relative DENSE-vs-DEFAULT difference in `sigma8_dd` or `f_source` >= `5e-2`.

### D6 — internal-solution invariance gate

PASS if DENSE and DEFAULT AeST internal observables are themselves stable at all six redshifts:

- relative internal `sigma(8,z)` difference <= `5e-3`
- relative internal `effective_f_sigma8/sigma8` difference <= `5e-3`.

This separates a transfer/output-grid defect from a material change in the integrated physical solution.

## Classification

If D1-D6 all pass:

`STABLE_AEST_DESI_DR1_R9B2D_DENSE_K_FORENSIC_INHERITANCE_DEFECT_CERTIFIED`

If provenance/configuration isolation fails:

`STABLE_AEST_DESI_DR1_R9B2D_CONFIGURATION_ISOLATION_FAIL`

If node-count separation is absent:

`STABLE_AEST_DESI_DR1_R9B2D_KGRID_SEPARATION_NOT_REPRODUCED`

If GR is sampling-sensitive:

`STABLE_AEST_DESI_DR1_R9B2D_GR_KGRID_CONTROL_FAIL`

If DEFAULT AeST remains pathological:

`STABLE_AEST_DESI_DR1_R9B2D_DEFAULT_GRID_AEST_UNRESOLVED`

If DENSE does not materially reproduce the pathology after DEFAULT passes:

`STABLE_AEST_DESI_DR1_R9B2D_DENSE_GRID_CAUSE_NOT_REPRODUCED`

If internal AeST observables materially change with sampling:

`STABLE_AEST_DESI_DR1_R9B2D_INTERNAL_SOLUTION_KGRID_SENSITIVE`

Technical exceptions use

`STABLE_AEST_DESI_DR1_R9B2D_RUN_FAIL`.

## Interpretation policy

A certified DENSE-k inheritance defect would localize the R9b2b/c pathology to a debugging precision configuration accidentally inherited by the observational parameter constructor. It would not reclassify any historical FAIL and would not itself license a DESI detection claim.

After certification, a separately preregistered science projection may use the physical/default-grid parameter construction, provided it changes no physical parameter, DESI vector/covariance, nuisance model, eta/tau grid, or likelihood threshold.

If DEFAULT remains pathological, the dense-k hypothesis is falsified and the next diagnostic must move below the transfer/Fourier layer to raw `get_perturbations()` solver histories. No DESI likelihood is run in that case.
