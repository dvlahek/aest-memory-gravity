# Stable AeST observable projection R5a — pre-result implementation audit

Date: 2026-09-14

This audit was recorded after R5a implementation and before any R5a science result.

## Locked provenance

- R5a preregistration lock: `d728b9629866da83182f5324988dea659eb61f0d`.
- R5 post-data lock: `7e02d7789c7478f56c1c63b7fa94ca59192d4ac4`.
- Required historical parent classification: `STABLE_AEST_OBSERVABLE_PROJECTION_R5_ETA_SCALING_FAIL`.
- Frozen CLASS/AeST parent head: `e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Branch-diff audit

The implementation diff from the preregistration commit contains only two newly added executable files:

- `fullj_weyl/stable_aest_observable_projection_r5a_local_eta.py`,
- `fullj_weyl/run_local_stable_aest_observable_projection_r5a_local_eta.sh`.

No R4 or R5 historical science code is modified by R5a.

## Anti-stale audit

The R5a driver uses only the frozen local eta scan

`eta = [0, 0.1, 0.25, 0.5]`

at nominal tolerance `3e-8`, with the separate tighter pair

`eta = [0, 0.1]`

at tolerance `1e-8`.

The driver contains no R5 `nominal_e10` or `tight_e10` run labels and no R4 parent lock/JSON dependency.

The runner contains a mandatory runtime anti-stale assertion that checks the exact preregistration lock, R5 post-data lock, R5 historical classification, local eta scan, and tight eta=0.1 control before any CLASS build or science run.

## Fresh-source audit

R5a does not reuse the R4 or R5 mutable CLASS build tree. The runner always:

1. starts from the frozen parent referenced by `results/nl1c6d2n_corrected_class_densek64_env.sh`,
2. checks exact CLASS head and `aest_memory.c` SHA,
3. copies it into a new disposable `...stablechi_r5asource` tree,
4. applies only the certified stable-chi patch,
5. requires exactly one dormant historical diagnostic external-force hook and removes exactly that line in the disposable source,
6. verifies one physical `Bchi_aest *= pba->aest_eta;` multiplier,
7. verifies one physical `E_rhs_aest -= 0.5*Q_aest*Bchi_aest;` closure,
8. verifies zero diagnostic external-force injections after neutralization,
9. builds a separate R5a Python target.

All diagnostic forcing environment variables are explicitly unset before the science run.

## Observable and gate audit

R5a directly computes the same observables frozen in R5:

- `Class.sigma(8.0,z,h_units=True)`,
- `Class.effective_f_sigma8(z,z_step=0.1)`,
- raw CLASS `C_L^{phi phi}` converted to `C_L^{kappa kappa}` for `40 <= L <= 2000`.

The driver separately evaluates:

- G4: nominal-vs-tight precision stability of `T(0.1)`,
- G5: local eta consistency `T(0.1)` vs `T(0.25)` and `T(0.25)` vs `T(0.5)`,
- G6: finite nonzero local response conditional on G4 and G5.

Unlike the historical R5 implementation, R5a does not set G5 false merely because G4 failed; precision and local-eta consistency are computed independently and classification priority is applied afterwards.

## Status

Implementation audit: PASS.

No R5a science result existed at the time of this audit.
