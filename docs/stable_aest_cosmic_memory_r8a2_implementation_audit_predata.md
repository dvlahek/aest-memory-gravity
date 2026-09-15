# Stable AeST cosmic memory R8a2 — implementation audit before first result

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

Pre-data lock:

`e01db75882717b7f2e230d634ff8f930604d8011`

Implementation head before any R8a2 result:

`cc56de041c756153295d4a3f58343830d974e99b`

Diff from preregistration contains exactly two added implementation files:

- `fullj_weyl/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.py`
- `fullj_weyl/run_local_stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.sh`

No R8a, R7a, R5b, source-patch, threshold, or historical result file was modified after the R8a2 preregistration.

The frozen tau grid remains `[10.0, 5.0, 2.5, 1.25]`; nominal derivative epsilons remain `0.025` and `0.05`; nominal tolerance remains `3e-8`; tight eta-zero controls use `1e-8`.

The implementation uses each same-tau nominal eta-zero solution to normalize its derivative, gates eta-zero precision only through same-tau nominal-versus-tight controls (`E <= 1e-7`, `C >= 0.99999999`), and records cross-tau eta-zero differences as non-gating diagnostics.

No amplitude monotonicity or preferred tau value gates PASS.
