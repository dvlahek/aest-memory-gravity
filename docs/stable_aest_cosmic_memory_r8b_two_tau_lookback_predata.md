# Stable AeST cosmic memory R8b — two-tau live lookback comparison (pre-data)

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Status before any R8b result

This document preregisters R8b before implementation or inspection of any R8b short-tau lookback result.

Frozen parents:

1. R7a live lookback decomposition at `tau H0 = 10`, formally
   `STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED`,
   post-data lock `86c03e6ba2ee9fcbf33a9d319d12ae778a747881`.
2. R8a2 precision-qualified tau scan, formally
   `STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED`,
   post-data lock `590dbc69e2823f583b157af2297e357991103c47`.

Historical R8a remains `STABLE_AEST_COSMIC_MEMORY_R8A_RUN_FAIL` and is not reclassified.

Frozen parent result hashes:

- R7a JSON SHA256: `94977acfe47f3f58337ce45dd8df982cd04ff6459434ed9780e229623bc92c0b`;
- R7a NPZ SHA256: `cc3e9b70809c44c8154abfc4cd3961d5f785f5cd3b327def2666e39bec789771`;
- R8a2 JSON SHA256: `2d6289c2fbd37bebcb904dade89f64c15a009e5c7454754b39d4dcc72924ca66`;
- R8a2 NPZ SHA256: `c81b2093a88719423e87ff5c180d790a56da6f396c0070858624879c90f26ee1`.

## Scientific question

R7a certified a causal live lookback decomposition at `tau H0 = 10`.
R8a2 certified that the full observable tangent remains reproducible down to `tau H0 = 1.25` and that shortening tau modestly reduces the total tangent norm while preserving most of its shape.

R8b asks:

> How does the causal epoch composition of the observable memory response change between the two certified endpoint relaxation times `tau H0 = 10` and `tau H0 = 1.25`?

The short-tau endpoint `1.25` is selected because it is the shortest tau certified by R8a2. The long-tau endpoint `10` is selected because it is the existing certified R7a lookback parent. No intermediate tau is selected after looking at epoch results.

No direction of temporal redistribution is preregistered. In particular, R8b does not require shorter tau to move the response toward later epochs.

## Frozen model and source construction

Use the same frozen stable-AeST setup as R7a/R8a2:

- CLASS parent `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- certified stable `chi = Q s` residual dynamics;
- memory order 20;
- nominal perturbation tolerance `3e-8`;
- no nonlinear/Halofit;
- no R2d history trace;
- no external tangent replay hook;
- direct physical memory feedback only;
- signed eta permitted only in the disposable diagnostic source for the symmetric derivative;
- R7a live epoch weighting applied only to the physical feedback multiplier.

The final disposable source must contain exactly one physical memory closure and exactly one live epoch multiplier.

## Frozen observables and domains

Exactly the same observable definitions as R7a/R8a2:

- `sigma8(z)`;
- CLASS `effective_f_sigma8(z)`;
- linear `C_L^{kappa kappa}` from raw CLASS `pp`;
- `z = [0.2, 0.5, 1.0, 1.5, 2.0]`;
- `L = 40,...,2000`;
- same `P_k_max_h/Mpc = 5` and canonical R5b initialization setup.

## Frozen tau endpoint and cosmic windows

R8b newly computes the lookback decomposition only at

`tau H0 = 1.25`.

The tau10 lookback reference is the frozen R7a result and is not recomputed.

Use exactly the R7a windows:

- `ancient`: `z >= 10`;
- `intermediate`: `2 <= z < 10`;
- `recent_structure`: `0.5 <= z < 2`;
- `late`: `z < 0.5`.

The windows are complementary and unchanged.

## Frozen run set at tau H0 = 1.25

Nominal tolerance `3e-8`:

- one `full`, `eta=0` baseline;
- `full`, `eta=+0.025` and `eta=-0.025`;
- `full`, `eta=+0.05` and `eta=-0.05`;
- for each of the four epoch modes, `eta=+0.025` and `eta=-0.025`.

Total: 13 cosmology runs.

No tau10 cosmology is rerun inside R8b.

For observable `X`, define at tau1.25

`T_X^full(eps) = [X_full(+eps)-X_full(-eps)]/[2 eps X_0]`,

and

`T_X^i = [X_i(+0.025)-X_i(-0.025)]/[0.05 X_0]`.

The negative-eta branch is only a local derivative diagnostic around eta=0.

## Parent bridges

R8b must bridge its tau1.25 full solution to the frozen R8a2 tau1.25 result.

The R8a2 NPZ arrays used as parent references are:

- `baseline_tau1p25_sigma8`, `baseline_tau1p25_fsigma8`, `baseline_tau1p25_ckk`;
- `T_tau1p25_sigma8_eps025`, `T_tau1p25_fsigma8_eps025`, `T_tau1p25_ckk_eps025`.

The frozen tau10 epoch component references are the R7a NPZ arrays:

- `T_ancient_*`;
- `T_intermediate_*`;
- `T_recent_structure_*`;
- `T_late_*`;
- `T_full025_*`.

## Epoch metrics and two-tau comparison

Only if all certification gates pass, report for tau1.25 and compare with frozen tau10:

For each observable and each epoch:

1. signed projection fraction onto the same-tau full tangent,
   `p_i = (T_i dot T_full)/(T_full dot T_full)`;
2. norm share,
   `n_i = ||T_i|| / sum_j ||T_j||`;
3. cosine of each epoch tangent with the same-tau full tangent;
4. tangent norm;
5. cosine between the tau1.25 epoch tangent and the corresponding frozen tau10 epoch tangent;
6. amplitude ratio `||T_i(1.25)||/||T_i(10)||`.

Also report, descriptively and without gating:

- `Delta p_i = p_i(1.25)-p_i(10)`;
- `Delta n_i = n_i(1.25)-n_i(10)`;
- early signed contribution `p_ancient + p_intermediate`;
- late signed contribution `p_recent_structure + p_late`;
- early/late norm-share sums;
- for `sigma8` and `f sigma8`, signed pointwise fractions at observed `z=0.2`;
- linear-lensing full-tangent zero crossings for tau1.25 compared with the frozen tau10 crossings.

Signed projection fractions are not probabilities and may be negative or exceed one due to cancellation. They must not be clipped or renormalized.

No preregistered gate depends on an epoch becoming larger, smaller, earlier, or later.

## Metrics

For vectors A and B:

- `E = ||A-B|| / max(||A||,||B||)`;
- `C = A.B/(||A|| ||B||)`.

## Preregistered gates

### R8B-G1 provenance and parent lock

PASS iff:

- this preregistration lock, R7a post-data lock, and R8a2 post-data lock are ancestors of implementation HEAD;
- exact R7a/R8a2 JSON and NPZ hashes match the frozen values above;
- R7a classification remains `STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED` with all gates true;
- R8a2 classification remains `STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED` with all gates true;
- historical R8a is not reclassified by R8b.

### R8B-G2 direct physical source topology

PASS iff the fresh disposable source has:

- stable `chi = Q s` dynamics;
- exactly one physical closure `E_rhs_aest -= 0.5*Q_aest*Bchi_aest;`;
- exactly one R7a live epoch multiplier;
- exactly one epoch helper;
- zero external tangent replay hooks in `perturbations_derivs`;
- zero R2d trace hooks in `perturbations_derivs`;
- the signed-eta parser diagnostic repair exactly once.

### R8B-G3 finite runs and tau1.25 baseline bridge

PASS iff all 13 runs are finite/domain-positive and the R8b tau1.25 eta-zero baseline reproduces frozen R8a2 tau1.25 nominal eta-zero for all three observables with

- `E <= 1e-7`;
- `C >= 0.99999999`.

### R8B-G4 tau1.25 full central-derivative consistency

Compare full central tangents from `epsilon=0.025` and `epsilon=0.05`.

PASS iff for each observable:

- `E <= 0.05`;
- `C >= 0.995`.

### R8B-G5 tau1.25 full bridge to R8a2

Compare the R8b tau1.25 full `epsilon=0.025` tangent to frozen R8a2 tau1.25 primary tangent.

PASS iff for each observable:

- `E <= 0.02`;
- `C >= 0.999`.

### R8B-G6 live epoch reconstruction at tau1.25

Let `T_sum = sum_i T_i` over the four frozen epoch windows.

PASS iff, relative to `T_full(0.025)`, for all three observables:

- `E <= 0.02`;
- `C >= 0.999`.

### R8B-G7 resolved epoch components

PASS iff every tau1.25 epoch tangent is finite and has strictly positive vector norm for every observable.

No epoch-dominance or temporal-shift direction is a gate.

## Formal classifications

Priority order:

1. `STABLE_AEST_COSMIC_MEMORY_R8B_INCOMPLETE`
2. `STABLE_AEST_COSMIC_MEMORY_R8B_PARENT_PROVENANCE_FAIL`
3. `STABLE_AEST_COSMIC_MEMORY_R8B_SOURCE_TOPOLOGY_FAIL`
4. `STABLE_AEST_COSMIC_MEMORY_R8B_RUN_OR_BASELINE_FAIL`
5. `STABLE_AEST_COSMIC_MEMORY_R8B_CENTRAL_DERIVATIVE_FAIL`
6. `STABLE_AEST_COSMIC_MEMORY_R8B_R8A2_BRIDGE_FAIL`
7. `STABLE_AEST_COSMIC_MEMORY_R8B_EPOCH_RECONSTRUCTION_FAIL`
8. `STABLE_AEST_COSMIC_MEMORY_R8B_EPOCH_COMPONENT_UNRESOLVED`
9. if G1-G7 pass: `STABLE_AEST_COSMIC_MEMORY_R8B_TWO_TAU_LOOKBACK_CERTIFIED`.

## Licensed interpretation of PASS

A PASS licenses reporting the causal lookback decomposition at `tau H0=1.25` and its measured difference from the already certified `tau H0=10` R7a decomposition, in the locked stable-AeST, order-20, linear-observable regime.

A PASS may support a statement that the temporal weighting is or is not sensitive to an eightfold change in relaxation time, according to the measured epoch metrics.

R8b does not license:

- extrapolation below `tau H0=1.25`;
- a continuous analytic law in tau;
- observational detection or parameter constraints;
- interpreting signed epoch projections as stored-energy probabilities;
- a universal statement about all relativistic memory models;
- irreversible or permanent spacetime memory.
