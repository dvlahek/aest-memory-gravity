# NL1C5BC corrected Exp baryon-source freeze result

## Classification

`NL1C5BC_CORRECTED_BARYON_SOURCE_FREEZE_PASS`

GitHub Actions run: `34408385173`.

Repository branch: `v053-exp-normalization-corrected`.
Run head: `07439a4a8975f24bc6fa9fa805b3bcc9e9ad649f`.

## Frozen result

All preregistered C1-C5 gates passed:

- C1 corrected CLASS provenance: PASS.
- C2 `d_b` and `d_m` existence/finite checks: PASS.
- C3 all six requested modes `[0.03,0.05,0.08,0.10,0.15,0.20] h/Mpc` were hit exactly; maximum relative miss `0`.
- C4 time coverage: 8 native redshift samples in `0.2 <= z <= 1.5`; PASS.
- C5 duplicate extraction: identical shapes and exactly zero reported mismatch for `k`, `z`, `d_b`, and `d_m`; PASS.

The source freeze used the corrected Exp-normalization CLASS model with memory disabled and `eta=0`. No observational likelihood, cosmological refit, nonlinear branch selection, or memory forcing was used.

## Interpretation

This PASS freezes the corrected-model baryonic source. Historical NL1C5B remains unchanged and must not be reused as the physical baryonic source for the corrected model. This result licenses corrected-model D2A matter-sector validation and corrected source-dependent full-J reclosure tests. It does not by itself license memory/likelihood claims or NL1C7.
