# Stable AeST cosmic-memory R7 — lookback decomposition pre-data declaration

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

## Purpose

R7 asks a causal question that is not answered by the previous amplitude and likelihood stages:

> Which cosmic epochs contribute to the present local-memory response of the certified stable-AeST model?

The test is a linear-response decomposition of the already certified `tau H0 = 10` memory channel. It does not modify the physical finite-memory equations and it does not fit observational data.

## Frozen scientific parents

R7 is licensed by three completed checkpoints:

1. corrected single-hook variational normalization:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_ABSOLUTE_COMMON_MODE_CERTIFIED`,
   post-data commit `c0fe57f73a7785c21b1fecd7455f19148d5f812d`;
2. observable derivative-at-zero response:
   `STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_ZERO_CERTIFIED`,
   post-data commit `3242335ece23fbeb743f075a1df1aa70acaab211`;
3. ACT fixed-template projection:
   `STABLE_AEST_ACT_DR6_R6A_FIXED_TEMPLATE_PROJECTION_CERTIFIED`,
   post-data commit `540f8f85c618209abb509e3c9c7dc188698d8e25`.

R7 does not reclassify any historical result.

The frozen R5b result files used for the physical derivative bridge are:

- `results/stable_aest_observable_projection_r5b_derivative_zero.json`, SHA-256 `26ce723e2b7b783fcd19765c9c7f01b6101992a3f09e6ee321299bf148259ca9`;
- `results/stable_aest_observable_projection_r5b_derivative_zero.npz`, SHA-256 `a88f99254bc1a7393e40691d5dc539bb1e1648eae1b892e43b63f593f8e367e1`.

## Frozen physical/numerical regime

Use the same stable-AeST regime as R5b:

- `tau H0 = 10`;
- memory order `20`;
- perturbation integration tolerance `3e-8`;
- physical background memory coupling `eta = 0` during the trace/replay construction;
- canonical initialization anchor `k_h = 0.165` only for the frozen initial-amplitude setup used by R5b;
- no Halofit/nonlinear correction;
- observables:
  - `sigma8(z)` at `z = [0.2, 0.5, 1.0, 1.5, 2.0]`,
  - CLASS `effective_f_sigma8(z)` on the same redshift grid,
  - linear `C_L^{kappa kappa}` for `L = 40,...,2000` from CLASS `raw_cl()['pp']` using `[(L(L+1)/2)^2] C_L^{phiphi}`.

The observable parameter/output construction must otherwise match R5b.

## Frozen first-order forcing

At physical `eta=0`, trace the direct first-order memory forcing before the physical eta multiplication:

`F_eta(k,tau) = -a Q B_chi,raw / (2 K_B)`.

The trace must be produced from the same observable CLASS run used for the R7 baseline and must cover the full k grid required by that run. Use the already validated R2d trace architecture and the corrected R2e single external replay hook.

The final disposable R7 source must contain:

- certified stable `chi = Q s` dynamics;
- exactly one physical `Bchi_aest *= pba->aest_eta;` statement;
- exactly one physical `E_rhs_aest -= 0.5*Q_aest*Bchi_aest;` closure statement;
- exactly one R2d full-history trace call for the direct forcing in `perturbations_derivs`;
- exactly one `dy[index_E] += aest_tangent_external_force(k,tau)` replay hook;
- exactly one runtime definition of `aest_tangent_external_force`.

No diagnostic forcing environment variable may be set during the eta-zero baseline/trace run.

## Cosmic-epoch windows

Map every normalized force-table conformal time to redshift using the background from the same eta-zero CLASS run. The background interpolation must cover the complete normalized force-table time range.

Partition every force-table row into exactly one of four predeclared epochs:

- `ancient`: `z >= 10`;
- `intermediate`: `2 <= z < 10`;
- `recent_structure`: `0.5 <= z < 2`;
- `late`: `z < 0.5`.

Each epoch table must retain the **same complete `(k,tau)` row grid** as the normalized full force table. Rows outside that epoch are retained with force set to zero; rows inside retain the original force exactly. Therefore no k-grid or tau-grid interpolation support is changed by the decomposition.

Require row-by-row

`F_full = F_ancient + F_intermediate + F_recent_structure + F_late`

to relative/scale-aware numerical tolerance `1e-12`.

No epoch-boundary value or contribution threshold may be modified after results are seen.

## Variational replay

Use the corrected single diagnostic hook only. The physical memory term remains at `eta=0`; the external replay is a diagnostic derivative generator, not a second physical memory coupling.

Full-history replay amplitudes:

- `lambda = +30, -30, +10, -10`.

Epoch-window replay amplitudes:

- `lambda = +30, -30` for each of the four windows.

For any observable `X`, define the central full-history fractional tangent

`T_X^full(lambda) = [X(+lambda)-X(-lambda)] / [2 lambda X(0)]`.

For epoch `i`, define

`T_X^i = [X_i(+30)-X_i(-30)] / [60 X(0)]`.

Define the reconstructed tangent

`T_X^sum = sum_i T_X^i`.

## Epoch-contribution metrics

For each observable vector, report without using these values as success thresholds:

1. signed projection fraction

`p_i = (T_i dot T_full) / (T_full dot T_full)`;

2. norm share

`n_i = ||T_i|| / sum_j ||T_j||`;

3. cosine with the full tangent;

4. raw tangent norm.

When reconstruction is successful, `sum_i p_i` should be approximately one. Signed projection fractions may be negative because different epochs may partially cancel; they must not be clipped or converted into probabilities.

For `sigma8` and `f sigma8`, also report the signed epoch fractions at the lowest locked redshift `z=0.2` as a late-time diagnostic. No minimum ancient/high-redshift contribution is preregistered.

## Gates

### R7-G1 provenance and parent lock

PASS iff all three post-data commits above are ancestors of HEAD, the frozen R5b JSON/NPZ SHA-256 values match, and the R5b classification is exactly `STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_ZERO_CERTIFIED` with all its gates true.

### R7-G2 single-hook + full-history source topology

PASS iff the final disposable R7 CLASS source satisfies all source-count requirements listed above and preserves the stable residual dynamics.

### R7-G3 trace and epoch-partition integrity

PASS iff the normalized full force trace is finite, contains more than one k and more than 1000 total unique `(k,tau)` rows, the same-run background covers its complete tau range, every row receives a finite redshift and exactly one epoch assignment, all epoch tables preserve the exact full row grid, and their row-wise sum reconstructs the full force table to `<=1e-12` scale-aware relative error.

### R7-G4 full-replay amplifier consistency

For each of `sigma8`, `f sigma8`, and `C_L^{kappa kappa}`, compare the `lambda=10` and `lambda=30` full-history tangents.

PASS iff for all three observables:

- relative L2 difference `<= 0.05`;
- cosine `>= 0.995`.

### R7-G5 physical derivative bridge

Compare the corrected full-history `lambda=30` tangent with the frozen physical R5b `eta=0.01` derivative-at-zero tangent.

PASS iff for all three observables:

- relative L2 difference `<= 0.10`;
- cosine `>= 0.995`.

This gate verifies that the diagnostic history decomposition is normalized to the already certified physical observable response.

### R7-G6 epoch reconstruction

For each observable compare `T_sum` with the corrected full-history `lambda=30` tangent.

PASS iff for all three observables:

- relative L2 difference `<= 0.02`;
- cosine `>= 0.999`.

No condition is imposed on which epoch dominates.

## Classification priority

1. `STABLE_AEST_COSMIC_MEMORY_R7_INCOMPLETE`
2. `STABLE_AEST_COSMIC_MEMORY_R7_PARENT_PROVENANCE_FAIL`
3. `STABLE_AEST_COSMIC_MEMORY_R7_SOURCE_TOPOLOGY_FAIL`
4. `STABLE_AEST_COSMIC_MEMORY_R7_TRACE_PARTITION_FAIL`
5. `STABLE_AEST_COSMIC_MEMORY_R7_REPLAY_LINEARITY_FAIL`
6. `STABLE_AEST_COSMIC_MEMORY_R7_PHYSICAL_BRIDGE_FAIL`
7. `STABLE_AEST_COSMIC_MEMORY_R7_EPOCH_RECONSTRUCTION_FAIL`
8. if G1-G6 all pass: `STABLE_AEST_COSMIC_MEMORY_R7_LOOKBACK_DECOMPOSITION_CERTIFIED`.

## Claim discipline

A PASS licenses only that the first-order stable-AeST memory response in the frozen `tau H0=10` regime has been causally decomposed into the four predeclared cosmic redshift windows, with the sum reconstructing the full physical derivative response within the preregistered tolerances.

The measured epoch fractions may then be reported as a property of this tested model/regime.

R7 does **not** by itself license:

- a universal statement that gravity remembers the entire age of the Universe;
- a detection of gravitational memory;
- an observational constraint on eta or tau;
- a permanent/irreversible spacetime memory claim;
- a claim that ancient epochs dominate before the measured decomposition is inspected;
- extrapolation from `tau H0=10` to other relaxation times.

A later separately preregistered tau scan is required for relaxation-time generality and amplitude optimization.