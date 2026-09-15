# Stable AeST DESI DR1 R9b2f full-grid rogue-node audit preregistration

## Purpose

R9b2e completed after Repair01 as

`STABLE_AEST_DESI_DR1_R9B2E_VELOCITY_MAPPING_DEFECT_NOT_LOCALIZED`.

The repaired R9b2e result showed finite continuity-consistent raw AeST histories and raw-history -> transfer closure at 24 explicitly requested modes over `0.02 <= k/h <= 2.0`. This falsifies a material velocity mapping defect on those tested modes.

However, R9b2d's pathological source-state sigma8 uses the entire automatic DEFAULT CLASS transfer grid: about 108 nodes extending to about `4.18 h/Mpc`. The sparse requested-mode audit therefore does not test all automatic-grid nodes entering the pathological variance integral.

R9b2f is a theory-only full-grid localization audit. It asks one narrow question: is the R9b2d velocity pathology produced by (i) power-spectrum extrapolation, (ii) interpolation between otherwise healthy full-grid nodes, or (iii) one or more automatic CLASS transfer-grid nodes that do not reproduce when the same k values are evaluated as explicit raw solver modes?

No DESI data vector, covariance, residual, likelihood, eta preference, or tau constraint is loaded or evaluated.

## Frozen provenance

Required ancestors:

- R9b2e post-result record: `f1f2bfd032065360ec7a18c080403d6e39f54dc7`
- R9b2e Repair01 preregistration: `28e98f6490ab02a979461b150af972898156d1fa`
- R9b2e Repair01 implementation: `02c95668f655afe96c9351b573c020cb1f241acb`
- R9b2e Repair01 runner: `793248884e4c5fbba52943716d54135ec05f55f7`
- R9b2d post-result record: `6b26243f78b477f7d4040c6499085faf05e8ffac`
- corrected CLASS parent remains `e85808324f51fc694d12e3ed7439552a3c3f9540`.

Completed R9b2e JSON SHA-256 is frozen as

`3deb9cf8b946f56727b4f10af70dababefda2b31098e1039b15ac21d03c5d255`.

Its classification is frozen as

`STABLE_AEST_DESI_DR1_R9B2E_VELOCITY_MAPPING_DEFECT_NOT_LOCALIZED`.

Historical R9b/R9b2/R9b2a/R9b2b/R9b2c/R9b2d/R9b2e classifications remain unchanged.

## Frozen physical setup

Use only

- `eta = 0`
- `tau_H0 = 10`
- `aest_memory_order = 20`
- `tol_perturbations_integration = 3e-8`
- `output = mPk,mTk,vTk`
- `P_k_max_h/Mpc = 5`
- `z_max_pk >= 2.3`
- no nonlinear correction
- no lensing
- DEFAULT CLASS k sampling: remove `k_per_decade_for_pk` and `k_per_decade_for_bao`
- same corrected/stable-chi CLASS source used by R9b2d/e.

Use the same six theory coordinates:

`z = {0.29536404346937617, 0.5096288678782911, 0.7057956472488681, 0.9185851971138159, 1.3170658832980264, 1.4905017757527006}`.

## Stage A — complete automatic transfer grid

Run one eta=0, tau=10 DEFAULT-grid model with no `k_output_values`.

At each frozen z, read every finite common node of

- `k (h/Mpc)`
- `d_b`, `d_cdm`
- `t_b`, `t_cdm`.

Construct

- `d_cb = f_b d_b + f_c d_cdm`
- `v_cb = -(f_b t_b + f_c t_cdm)/Hconf`
- `P_dd = C(k) d_cb^2`
- `P_tt = C(k) v_cb^2`

with the same primordial prefactor used by R9b2b/d.

For each z compute sigma8_dd and sigma8_tt by three frozen methods:

1. `COSMO_DEFAULT`: current R9b2b/d `PowerSpectrumInterpolator1D(k, P).sigma8()` defaults.
2. `COSMO_BOUNDED`: the same interpolator but with extrapolation bounds fixed to the actual first/last CLASS transfer nodes.
3. `LOGLINEAR_BOUNDED`: direct Simpson integration over 8192 equally spaced log-k samples between the actual first/last transfer nodes, with linear interpolation of `log(P)` versus `log(k)` and no extrapolation.

The direct bounded integral is

`sigma8^2 = 1/(2 pi^2) int dlnk k^3 P(k) W_TH(8k)^2`.

No transfer point may be removed, clipped, Winsorized, or manually filtered.

## Frozen candidate-node selection

Candidate selection is diagnostic and deterministic.

For each z and each automatic grid node, define the non-negative node contribution proxy

`Q_i = Delta(ln k)_i * k_i^3 * P_tt(k_i) * W_TH(8 k_i)^2`,

where interior `Delta(ln k)_i = 0.5 [ln(k_{i+1}) - ln(k_{i-1})]` and endpoint widths are one-sided.

For every node index define

`S_i = max_z Q_i / sum_j Q_j`.

Select the eight node indices with largest `S_i`. Add each selected node's immediate automatic-grid neighbors `i-1` and `i+1` when present. Deduplicate and preserve ascending k order. This yields at most 24 exact candidate k values.

The selection rule is frozen before the run and does not use DESI data or any expected growth proxy.

## Stage B — exact-k raw solver rerun

Run the identical physical model again, now adding `k_output_values` equal to the exact Stage-A candidate physical wavenumbers (`k = h k_h`) serialized with 17 significant digits.

Require the number of scalar raw histories returned by `get_perturbations()` to equal the number of requested candidate modes. Map history `i` to candidate `i` by the same ordered convention certified operationally in R9b2e Repair01.

At each frozen z:

- interpolate raw `theta_b` and `theta_cdm` histories in scale factor using PCHIP;
- read transfer `t_b,t_cdm` from the exact-k rerun;
- compare raw rerun -> rerun transfer;
- compare original automatic-grid Stage-A transfer -> exact-k rerun transfer at the same frozen k.

Also compare internal `sigma(8,z)` and `effective_f_sigma8/sigma8` between Stage A and Stage B.

## Frozen thresholds

- `REL_GATE = 5e-3` for healthy source/internal closure and internal-solution invariance.
- `RAW_TRANSFER_GATE = 2e-4`, inherited from R9b2e primary raw->transfer closure.
- `MATERIAL_GATE = 5e-2` for localization of a material post-processing or automatic-grid discrepancy.

Relative point discrepancies in velocity use denominator

`max(|x|, |y|, 1e-12 * max_k |t_cb|)`

at the corresponding z to avoid meaningless division by an exact velocity zero.

## Frozen interpretation logic

First require the historical pathology to reproduce in `COSMO_DEFAULT`: at least one z has `f_source > 2` or relative difference from the internal growth proxy >= 0.05.

Then classify the mechanism in this fixed priority:

1. **High-k extrapolation defect** if `COSMO_DEFAULT` is pathological but `COSMO_BOUNDED` is healthy at all six z and differs materially (>=0.05) from `COSMO_DEFAULT` at at least one z.

   Classification:
   `STABLE_AEST_DESI_DR1_R9B2F_HIGH_K_EXTRAPOLATION_DEFECT_CERTIFIED`

2. **Power interpolation defect** if `COSMO_BOUNDED` remains pathological but `LOGLINEAR_BOUNDED` is healthy at all six z and differs materially (>=0.05) from `COSMO_BOUNDED` at at least one z.

   Classification:
   `STABLE_AEST_DESI_DR1_R9B2F_POWER_INTERPOLATION_DEFECT_CERTIFIED`

3. **Automatic-grid rogue-node defect** if `LOGLINEAR_BOUNDED` remains pathological, the candidate exact-k rerun has raw->rerun-transfer closure <= `2e-4`, internal observables remain invariant <= `5e-3`, and Stage-A automatic-grid velocity differs from the exact-k rerun by >= `5e-2` at at least one candidate `(k,z)`.

   Classification:
   `STABLE_AEST_DESI_DR1_R9B2F_AUTOMATIC_KGRID_ROGUE_NODE_DEFECT_CERTIFIED`

4. Otherwise:

   `STABLE_AEST_DESI_DR1_R9B2F_FULL_GRID_PATHOLOGY_UNRESOLVED`.

Technical/provenance failures use dedicated `...PROVENANCE_FAIL` or `...RUN_FAIL` classifications and are not scientific results.

## Interpretation policy

A certified R9b2f defect localizes only the numerical post-processing/output mechanism. It does not reclassify any historical FAIL and does not license a DESI science rerun by itself. A later science projection requires a separately preregistered extraction path that avoids the certified defect without changing physical parameters, DESI inputs, eta/tau grid, nuisance model, or likelihood thresholds.
