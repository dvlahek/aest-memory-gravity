# Stable AeST DESI DR1 R9b2h derivative-stable bounded quadrature preregistration

## Purpose

R9b2f certified a high-k extrapolation defect in the historical direct-velocity sigma8 construction. R9b2g then validated the bounded-support extraction at the value level over all 20 frozen `(tau,eta)` cases, but failed the frozen central-derivative amplitude criterion when the bounded cosmoprimo interpolator was differentiated.

R9b2g is retained as

`STABLE_AEST_DESI_DR1_R9B2G_CENTRAL_DERIVATIVE_FAIL`.

Post-result analysis of the independent bounded log-linear values already stored by R9b2g showed that the same central finite differences satisfy the original derivative gate. This observation is diagnostic only and does not reclassify R9b2g.

R9b2h is a theory-only audit designed before any corrected DESI likelihood evaluation. It tests if the very small eta derivative is stable under bounded quadrature resolution, a second shape-preserving interpolation operator, and an extension of the actual CLASS k support.

No DESI data vector, covariance, likelihood, eta preference, or tau constraint is loaded or evaluated.

## Frozen provenance

Required ancestors:

- R9b2g postdata: `68ca78bcea41a18af46ec4ccf6e30ddf78f64471`
- R9b2g preregistration: `2ea44eb92319fc6c2a3273dc91254e14dc797e35`
- R9b2g implementation: `ca8b788a40bc5de1649f53ff4cfe7ace5aa1500b`
- R9b2f postdata: `b569aebc41efc841755f5fcec63b91092c192ba3`
- corrected CLASS parent remains `e85808324f51fc694d12e3ed7439552a3c3f9540`.

Completed R9b2g artifact hashes are frozen as:

- JSON SHA-256 `2e2be7821088b8bbe2f152d8ee03cc950d3d4270d4725286dd0e976a522f4d34`
- science log SHA-256 `eb75011d498aeabe7e8282114b4d2eb3d10901e994363aa70b3116f7ff625cb3`
- full-runner SHA-256 `c56662b54ce1bad1293ea53bb7ff120cf211df48a54dd4be13474cd64e7c21cc`.

Historical classifications remain unchanged.

## Frozen physical setup

Primary grid:

- `tau_H0 = {10,5,2.5,1.25}`
- `eta = {0,+0.025,-0.025,+0.05,-0.05}`
- `tol_perturbations_integration = 3e-8`
- `aest_memory_order = 20`
- DEFAULT CLASS k sampling: no `k_per_decade_for_pk`, no `k_per_decade_for_bao`
- no `k_output_values`
- `output = mPk,mTk,vTk`
- no nonlinear correction
- no lensing
- same corrected/stable-chi CLASS source as R9b2f/g.

Primary support uses `P_k_max_h/Mpc = 5`.

Frozen theory coordinates are the same six effective redshifts used throughout R9b:

`{0.29536404346937617, 0.5096288678782911, 0.7057956472488681, 0.9185851971138159, 1.3170658832980264, 1.4905017757527006}`.

The source-state construction is unchanged:

- `d_cb = f_b d_b + f_c d_cdm`
- `v_cb = -(f_b t_b + f_c t_cdm)/Hconf`
- `P_dd = C(k) d_cb^2`
- `P_tt = C(k) v_cb^2`.

No `pk_lin`, `pk_cb_lin`, local `v/d`, point clipping, outlier rejection, or spectral extrapolation is allowed.

## Frozen bounded quadratures

All quadratures integrate only between the first and last actual finite CLASS transfer nodes.

### Q1 — log-linear, 4096

Interpolate `log P` linearly in `log k` onto 4096 equally spaced log-k points and integrate

`sigma8^2 = 1/(2 pi^2) int dlnk k^3 P(k) W_TH(8k)^2`

with Simpson integration.

### Q2 — log-linear, 8192

Same as Q1 with 8192 samples. This is the primary candidate extraction if R9b2h passes.

### Q3 — log-linear, 16384

Same as Q1 with 16384 samples.

### Q4 — log-P PCHIP, 8192

Use SciPy `PchipInterpolator(log k, log P, extrapolate=False)` on the same 8192-point log-k grid and Simpson-integrate the same top-hat variance. No extrapolation is permitted.

All four operators are applied separately to Pdd and Ptt, then `f = sigma8_tt/sigma8_dd`.

## Frozen higher-support control

At `tau_H0=10` only, rerun the same five eta values with

- `P_k_max_h/Mpc = 10`
- `P_k_max_h/Mpc = 20`.

Use Q2 only for this support-convergence control. No other parameter changes.

## Frozen derivative definitions

For every method and tau:

`T_primary = [f(+0.025)-f(-0.025)] / 0.05`

`T_control = [f(+0.05)-f(-0.05)] / 0.10`.

The tangent is the six-redshift vector.

Use the same historical consistency measures:

- `E(A,B) = ||A-B|| / max(||A||,||B||)`
- `C(A,B) = cosine(A,B)`.

Frozen derivative gate remains

- `E <= 0.05`
- `C >= 0.995`.

The threshold is not relaxed from R9b/R9b2g.

## Gates

### H1 — provenance and construction

PASS if all frozen ancestors and R9b2g artifact hash/classification checks pass and the implementation contains no forbidden extrapolation or proxy construction.

### H2 — finite physicality

For Q1-Q4 over all 20 primary cases and all six redshifts:

- finite positive sigma8_dd and sigma8_tt
- `0.1 < sigma8_dd < 2`
- `0.05 < f < 2`.

### H3 — log-linear resolution convergence

Across all 20 primary cases and six redshifts, maximum relative differences must satisfy

- Q1 vs Q2 <= `1e-4`
- Q2 vs Q3 <= `1e-4`

for each of `sigma8_dd`, `sigma8_tt`, and `f`.

### H4 — shape-preserving quadrature agreement

Across all 20 primary cases and six redshifts, Q2 vs Q4 relative differences must be <= `5e-3` for each of `sigma8_dd`, `sigma8_tt`, and `f`.

### H5 — within-method derivative consistency

For each tau, both Q2 and Q4 independently must satisfy

- primary/control `E <= 0.05`
- primary/control `C >= 0.995`
- primary tangent norm > `1e-12`.

### H6 — cross-method tangent agreement

For each tau, Q2 and Q4 tangents must agree for both finite-difference scales:

- `E(Q2,Q4) <= 0.05`
- `C(Q2,Q4) >= 0.995`.

### H7 — actual k-support convergence

At tau=10 for all five eta values, Q2 results must satisfy

- max relative `f`, `sigma8_dd`, `sigma8_tt` difference between KMAX=5 and KMAX=20 <= `5e-3`
- max relative difference between KMAX=10 and KMAX=20 <= `5e-3`.

In addition, at KMAX=10 and KMAX=20 the tau=10 primary/control derivative must independently satisfy `E <= 0.05`, `C >= 0.995`, and the KMAX=5 primary and control tangents must agree with KMAX=20 at `E <= 0.05`, `C >= 0.995`.

## Classification

If H1-H7 all pass:

`STABLE_AEST_DESI_DR1_R9B2H_DERIVATIVE_STABLE_BOUNDED_QUADRATURE_VALIDATED`

Ordered failures:

- `STABLE_AEST_DESI_DR1_R9B2H_PROVENANCE_OR_CONSTRUCTION_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2H_FINITE_PHYSICALITY_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2H_RESOLUTION_CONVERGENCE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2H_QUADRATURE_AGREEMENT_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2H_WITHIN_METHOD_DERIVATIVE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2H_CROSS_METHOD_DERIVATIVE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2H_KSUPPORT_CONVERGENCE_FAIL`
- technical exceptions: `STABLE_AEST_DESI_DR1_R9B2H_RUN_FAIL`.

## Interpretation policy

PASS licenses only a separately preregistered corrected ShapeFit **theory extraction** using Q2 (bounded log-linear 8192). It does not reclassify historical FAILs and does not itself constitute DESI evidence.

Only after R9b2h PASS may a corrected DESI projection be preregistered. That projection must keep the official DESI vector/covariance, nuisance model, eta/tau grid, and likelihood thresholds unchanged from the historical R9b/R9b2 program.
