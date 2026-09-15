# Stable AeST DESI DR1 R9b2e raw-solver velocity-closure post-result record

## Historical technical pre-run

The first R9b2e invocation ended before any diagnostic physics result because the implementation incorrectly required each `get_perturbations()` scalar-history dictionary to carry an explicit k field. The local CLASS interface instead returns scalar histories in the frozen `k_output_values` order, as already used by the earlier NL1C6D2A audit.

The pre-repair technical output is retained as

`STABLE_AEST_DESI_DR1_R9B2E_RUN_FAIL`

with `diagnostic_complete=false` and `science_evaluated=false`. It is not a scientific R9b2e result.

## Repair01

Repair01 changed only the requested-mode identity mapping:

`history[i] <-> K_H[i]`

with an exact `len(histories)==len(K_H)` check. No physical parameter, requested k mode, redshift, CLASS source, interpolation method, threshold, or E1-E7 rule changed.

Repair preregistration: `28e98f6490ab02a979461b150af972898156d1fa`.
Repair implementation: `02c95668f655afe96c9351b573c020cb1f241acb`.
Repair runner: `793248884e4c5fbba52943716d54135ec05f55f7`.

## Completed diagnostic result

The completed repaired run is retained as

`STABLE_AEST_DESI_DR1_R9B2E_VELOCITY_MAPPING_DEFECT_NOT_LOCALIZED`.

Observed gates:

- E1 provenance / requested-mode identity: PASS
- E2 `k_output_values` internal-solution invariance: PASS
- E3 GR raw-history -> transfer closure: PASS
- E4 AeST raw continuity and finiteness: PASS
- E5 AeST raw-history -> transfer density closure: PASS
- E6 AeST material velocity discrepancy localization: FAIL
- E7 cubic/PCHIP raw interpolation robustness: PASS

Key completed-run metrics:

- AeST cubic raw -> transfer closure:
  - `d_b = 2.3493681008257841e-07`
  - `d_cdm = 1.1405778450066722e-06`
  - `t_b = 7.931923827246499e-07`
  - `t_cdm = 4.372769841992576e-06`
- AeST PCHIP raw -> transfer closure:
  - `d_b = 2.569829182286799e-07`
  - `d_cdm = 1.1456296283709382e-06`
  - `t_b = 8.133487311013249e-07`
  - `t_cdm = 4.379309942394284e-06`
- AeST raw continuity maxima:
  - baryons `4.645947998781224e-10`
  - CDM `6.683771101991995e-08`
- worst individual tested AeST velocity raw/transfer discrepancy:
  - `1.83651101686433e-05`
  - field `t_cdm`
  - `k_h = 2.0`
  - `z = 0.5096288678782911`
- cubic-vs-PCHIP raw-state discrepancy <= `6.493044319400316e-08`
- `k_output_values` internal-solution changes:
  - sigma8 `7.267526815855335e-07`
  - growth proxy `4.6359265276222805e-06`.

Therefore the raw AeST perturbation histories are finite and continuity-consistent over the 24 requested modes, and transfer values at those same requested modes agree with raw solver histories to a few parts in 10^6. The preregistered hypothesis of a material raw-history -> transfer velocity mapping defect is falsified on the tested modes.

Completed local artifact hashes supplied after Repair01:

- JSON SHA-256: `3deb9cf8b946f56727b4f10af70dababefda2b31098e1039b15ac21d03c5d255`
- science log SHA-256: `1660340934a84066b9b1887939a6fa5a9215cf5b0ee6334cf96ec419b0b159be`
- repair full-runner log SHA-256: `ab0e1dfe531757d3e133c9ea08d52306896fc61a99b14765fd0adb1982d6b26c`.

## Post-result localization

R9b2d and R9b2e do not sample the same k set. R9b2d source-state sigma8 uses the entire ordinary CLASS transfer grid (108 k nodes in the DEFAULT case, extending to about `4.18 h/Mpc`). R9b2e explicitly requested 24 logarithmically spaced modes only over `0.02 <= k/h <= 2.0` and verified those modes individually.

Thus R9b2e does not test all automatic transfer-grid nodes that enter the pathological R9b2d `sigma8_tt` integration. A sparse or narrow set of rogue automatic-grid nodes can remain completely consistent with the R9b2e result.

A separate local reconstruction from the completed R9b2e JSON also checked the previously suspected generic high-k extrapolation mechanism on the 24 healthy modes. Using the source-state shape `P_tt ~ k^(n_s-4) t_cb^2`, extending the healthy 24-mode spectrum from `k=2` to `100 h/Mpc` changes the reconstructed sigma8_tt only at the few-per-mille level. This does not support generic high-k extrapolation as a sufficient explanation for the historical factors of 10^2-10^7.

## Consequence

The next theory-only diagnostic must inspect every automatic DEFAULT transfer-grid node, identify which nodes dominate the pathological velocity variance, and then re-evaluate those exact k values as explicit `k_output_values` raw solver modes. No DESI data or likelihood is licensed before that full-grid node-identity test is resolved.
