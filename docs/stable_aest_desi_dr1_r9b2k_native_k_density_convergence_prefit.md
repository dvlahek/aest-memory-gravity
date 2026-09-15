# Stable AeST DESI DR1 R9b2k native-k density convergence — preregistration

## Motivation

R9b2j Repair01 is frozen as `STABLE_AEST_DESI_DR1_R9B2J_CROSS_OPERATOR_FAIL`. Its signed response is converged with respect to the 4096/8192/16384 integration grid and independently stable between `epsilon=0.025` and `epsilon=0.05`, but linear and PCHIP reconstruction of the signed response between the 108 actual CLASS transfer nodes differs materially (`E ~ 0.322`, `C ~ 0.9805`).

R9b2k tests only the remaining unresolved numerical question: does the signed response become reconstruction-independent when the *actual CLASS transfer sampling* is refined?

No historical failure is reclassified. No R9b2j threshold is relaxed.

## Frozen physical setup

The physical/model setup is unchanged from R9b2j Repair01:

- corrected stable-AeST CLASS source and full live epoch mode;
- six DESI ShapeFit effective redshifts used in the R9b chain;
- `tau_H0 = {10, 5, 2.5, 1.25}`;
- `eta = {0, +0.025, -0.025, +0.05, -0.05}`;
- `tol_perturbations_integration = 3e-8`;
- memory order 20 and the same memory source topology;
- `P_k_max_h/Mpc = 5`;
- output `mPk,mTk,vTk`;
- no nonlinear correction, no lensing, no `k_output_values`;
- source-state `Pdd` and `Ptt` constructed from the same baryon+CDM transfer state and primordial prefactor as R9b2f--R9b2j;
- no `pk_lin`, `pk_cb_lin`, local `v/d`, clipping, or extrapolation outside the retained transfer support in the growth response.

The signed central response remains formed before integration,

`D_P = [P(+epsilon)-P(-epsilon)]/(2 epsilon)`.

The primary response operator remains linear interpolation of signed `D_P` in `ln(k)` to 8192 bounded nodes followed by Simpson integration. The independent control remains PCHIP interpolation of signed `D_P` in `ln(k)` to 8192 bounded nodes followed by Simpson integration.

The derivative gate remains exactly `E <= 0.05` and `C >= 0.995`, with nonzero tangent norm.

## Frozen native-k density tiers

The corrected-CLASS historical dense baseline used

- `k_per_decade_for_pk = 80`
- `k_per_decade_for_bao = 560`.

R9b2k freezes two actual solver-density tiers before the new result is observed:

- D1 historical dense: `(80, 560)`;
- D2 two-times dense: `(160, 1120)`.

D1 is evaluated at `tau_H0=10` for all five eta values. D2 is evaluated for all four tau values and all five eta values. Thus the new campaign contains 25 process-isolated CLASS cases. Every case is checkpointed and reusable after validation.

The old DEFAULT/108-node R9b2j result is retained only as a frozen lower-density diagnostic reference. It is not a pass criterion for D1 or D2.

## Stage A gates

### K1 — provenance

Require the frozen R9b2j Repair01 result and postdata commit, the R9b2j/R9b2i ancestry locks, corrected source topology, and the exact local Repair01 JSON SHA256.

### K2 — actual native-grid refinement and health

For each central pair used at a given density, require identical finite monotone native `k` arrays across `eta=0,+epsilon,-epsilon`, positive finite `Pdd/Ptt`, and support containing the sigma8 window.

At every target redshift for `tau=10`, require the actual retained native node count to satisfy

`n_k(D2) > n_k(D1) > 108`.

The measured node counts and support endpoints are recorded. The gate depends on actual returned nodes, not only on input parameters.

### K3 — D2 eta=0 closure and tau invariance

Using the D2 primary bounded extraction, require the existing value-level gate `<= 5e-3` for eta=0 `sigma8_dd` versus CLASS internal sigma8 and for source-state `f` versus the frozen internal growth proxy. Require eta=0 variation across tau `<= 5e-3` for `sigma8_dd`, `sigma8_tt`, and `f`.

### K4 — D2 epsilon consistency

For each tau, require both the linear and PCHIP D2 response operators independently to satisfy the unchanged derivative gate between primary (`epsilon=0.025`) and control (`epsilon=0.05`) tangents.

### K5 — actual native-density convergence

At `tau_H0=10`, compare D1 and D2 response tangents separately for each operator and each epsilon. Each D1-vs-D2 comparison must satisfy `E <= 0.05`, `C >= 0.995`, with nonzero norms.

This is the decisive solver-node convergence test. Interpolation-grid refinement alone cannot satisfy this gate.

### K6 — D2 cross-operator agreement

For every tau and both epsilon values, compare D2 linear and D2 PCHIP response tangents. Every comparison must satisfy the unchanged `E <= 0.05`, `C >= 0.995` gate with nonzero norms.

If K6 fails, the direct-velocity ShapeFit response remains numerically unresolved. No operator may be selected postdata and no DESI projection is licensed from this chain.

## Conditional Stage B — corrected DESI ShapeFit projection

Official DESI DR1 ShapeFit data are loaded only if K1--K6 all pass.

ShapeFit geometry and shape scalars are then constructed from the D2 saved source state and background metadata. `Ap` and `m` use the same bounded source-state `Pdd`; the R9b2k path may not call CLASS `pk_cb_lin`.

The 24-vector tangent contains the same `qiso/qap/df/dm` construction and the same official DESI ordering/covariance as the frozen R9b chain. The D2 linear-8192 response is the preregistered primary tangent and D2 PCHIP-8192 is the independent control.

Require:

1. finite corrected 24-vectors;
2. primary epsilon consistency `E <= 0.05`, `C >= 0.995` for every tau;
3. primary/control full-vector agreement `E <= 0.05`, `C >= 0.995` for every tau and both epsilon values;
4. positive finite nuisance-projected Fisher information and projection idempotence `<= 1e-8`;
5. matched-filter and GLS eta estimates agree to the existing numerical identity tolerance.

The nuisance columns remain the frozen global `df` scale and global `dm` offset. The physical interval remains `0 <= eta <= 0.05`.

## Classification

PASS:

`STABLE_AEST_DESI_DR1_R9B2K_NATIVE_K_DENSITY_SHAPEFIT_CERTIFIED`

Ordered Stage-A failure classes:

- `STABLE_AEST_DESI_DR1_R9B2K_PROVENANCE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2K_NATIVE_GRID_REFINEMENT_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2K_ETA0_CLOSURE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2K_EPSILON_CONSISTENCY_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2K_NATIVE_DENSITY_CONVERGENCE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2K_CROSS_OPERATOR_FAIL`

Conditional Stage-B failures are separately labeled DESI provenance, ShapeFit vector, full-tangent, projection, or GLS failures.

A PASS licenses reporting of the corrected compressed DESI DR1 ShapeFit projection as a numerical/data result. It does not by itself license an observational detection claim, a full-EFT modified-gravity claim, or a tau bound.
