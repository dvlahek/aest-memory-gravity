# NL1C7B4 Repair06 — high-resolution analytic momentum convergence audit

Status: **PRE-DATA / LOCKED BEFORE IMPLEMENTATION**

Parent Repair05 official run: `35225084320`

Parent Repair05 head SHA: `cfb43b99162db1b8cf25621d3de795b42e1e2cf9`

Parent Repair05 artifact: `10498343763`

Parent Repair05 artifact SHA256: `5798127479d0a359b5805aa7bd846caee035e582b0fdb3a08b7cd7ab2dc2e9ce`

Parent Repair05 result freeze commit: `56de1b3bf028dfdbbab2684bde652056561074c1`

## Problem

Repair05 removed the finite-difference tangent ambiguity and found a large analytic first-order momentum residual dominated by the AeST K(Q) sector in all 54 evaluated cases. However, the preregistered 256/512 grid-control gate failed at `R_sigma = 20 h^-1 Mpc`: the relative RMS difference was `0.026137957486093634`, above the unchanged `0.02` limit. Therefore Repair05 was correctly classified as `NL1C7B4_REPAIR05_IMPLEMENTATION_FAIL`, and the large residual was not promoted to a physical leading-order interface mismatch.

Repair06 changes only the radial resolution study. The analytic evaluator, action-derived term decomposition, normalization, thresholds, state reconstruction, background interface, sign conventions, and claim boundary remain frozen from Repair05.

## Frozen evaluator

The primary analytic evaluator is the implementation in

`nl1c7b/initial_constraint_certification_repair05.py`

with blob SHA

`34fd22c73171fce5e32920a94d71d05de61521f6`.

Repair06 must import and reuse the Repair05 analytic functions directly. It may not rederive, refit, reorder by scientific outcome, or modify any physical term.

The following Repair05 constants remain unchanged:

- `PASS_LIMIT = 1e-5`;
- `MISMATCH_FLOOR = 0.1`;
- `ZERO_REL_LIMIT = 1e-12`;
- `ZERO_ABS_FLOOR = 1e-30`;
- `GRID_LIMIT = 2e-2`;
- `BRIDGE_LIMIT = 1e-6`.

No post-result threshold relaxation is allowed.

## Frozen state, background, and cases

The state direction remains exactly the retained C7A Repair01 growing-mode spherical state reconstructed from the same frozen dense trace.

The retained 256-point NPZ remains a provenance/reproduction control and must reproduce with maximum relative L2 error <= `1e-12`.

Primary Repair06 analytic resolutions are:

- `Nr = 512`;
- `Nr = 1024`;
- `Nr = 2048`.

Frozen scales remain `5, 10, 20 h^-1 Mpc`.

All 9 co-primary Y/beta labels remain present:

- Y in `Simple`, `Exponential`, `Sharp`;
- `beta0` in `1.0, 0.5, 0.1`.

This gives `3 scales x 3 resolutions x 9 Y/beta labels = 81` primary analytic rows.

Repair05 established that the eta=0 first-order analytic momentum expression used here is independent of Y family and beta0. Repair06 nevertheless retains all nine labels and evaluates all nine cases at every scale and resolution. No branch or scale may be selected after the result.

## Primary residual

For every non-center radial point, Repair06 uses the unchanged Repair05 quantity

`epsilon_M1 = |sum_i M1_i| / (sum_i |M1_i| + floor)`

with

`floor = 1e-14 * max_r(sum_i |M1_i|)`.

The center is excluded only because the spherical momentum constraint is identically degenerate there. No other radial point may be excluded.

The unchanged scientific regions are:

- analytic linear-interface PASS: `max epsilon_M1 <= 1e-5` in every primary row;
- strong leading-order mismatch: `max epsilon_M1 >= 0.1` in every primary row.

Values between these regions remain diagnostic only.

## Required controls

Repair06 is scientifically interpretable only if every item below passes.

1. Repair05 parent provenance, classification, artifact ID, and artifact digest match exactly.
2. The Repair05 evaluator blob is exactly `34fd22c73171fce5e32920a94d71d05de61521f6`.
3. C7A retained-state reproduction remains <= `1e-12` on the frozen 256-point control.
4. Symbolic Exp K(Q) dictionary identity remains true.
5. Analytic-zero checks for `AeST_E2`, `AeST_EX`, `AeST_X2`, and `AeST_J` pass with the unchanged Repair05 tolerance.
6. E/X bridge controls pass with relative L2 error <= `1e-6` at all three Repair06 resolutions and all three scales.
7. Every reported residual is finite.
8. **Primary 512/1024 grid gate:** for every scale and Y/beta label, the RMS normalized residual must agree to relative difference <= `0.02`, unless both RMS values are below `1e-8`.
9. **Independent high-resolution 1024/2048 safety gate:** the same criterion <= `0.02` must pass for every scale and Y/beta label, unless both RMS values are below `1e-8`.
10. Both adjacent-resolution grid gates are mandatory for scientific interpretation. A failure of either gate gives an implementation/grid-convergence failure; 2048 is not allowed to be ignored after inspection.
11. No state projection, fitted coefficient, sign flip, Y selection, scale selection, radial standard-species insertion, nonlinear evolution, or finite-eta calculation.

For each adjacent pair, Repair06 must report the RMS residual at both resolutions and the relative difference. It must also report the dominant term group at the maximum residual for every primary row.

## Preregistered classifications

- `NL1C7B4_REPAIR06_ANALYTIC_LINEAR_MOMENTUM_INTERFACE_PASS`
  - every implementation/control gate passes and all 81 primary rows satisfy `max epsilon_M1 <= 1e-5`.

- `NL1C7B4_REPAIR06_ANALYTIC_LEADING_ORDER_INTERFACE_MISMATCH`
  - every implementation/control gate, including both 512/1024 and 1024/2048 grid gates, passes and all 81 primary rows satisfy `max epsilon_M1 >= 0.1`.

- `NL1C7B4_REPAIR06_ANALYTIC_LINEAR_MOMENTUM_DIAGNOSTIC_COMPLETE`
  - every implementation/control gate passes but the 81 primary rows do not uniformly occupy either the PASS or strong-mismatch region.

- `NL1C7B4_REPAIR06_IMPLEMENTATION_FAIL`
  - any provenance, evaluator-lock, state-reproduction, symbolic identity, analytic-zero, E/X bridge, finiteness, row-count, or either adjacent-resolution grid-control requirement fails.

## Claim boundary

Repair06 is still a linear identity/convergence audit at eta=0. It does not solve or project the nonlinear initial constraints and does not authorize nonlinear spherical evolution, turnaround, collapse, lensing, SPT, or finite-eta interpretation.

A Repair06 `ANALYTIC_LEADING_ORDER_INTERFACE_MISMATCH` classification would certify only that the large first-order radial momentum mismatch persists under the locked analytic evaluator and two successive radial refinements through `Nr = 2048`. Any repair of that mismatch must then be separately derived and preregistered; no coefficient or sign may be tuned from this audit.