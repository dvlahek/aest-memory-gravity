# NL1C6D2AC corrected baryon matter-sector audit result

## Classification

`NL1C6D2AC_CORRECTED_BARYON_MATTER_SECTOR_AUDIT_PASS`

GitHub Actions run: `34436438650`.
Run head: `37c404324865c201b5caf635f6a8055637255edd`.
Branch: `v053-exp-normalization-corrected`.

## Frozen gate results

- A1 corrected source identity: PASS. Fresh corrected CLASS and regenerated NL1C5BC source have zero reported mismatch in `k`, `z`, `d_b`, and `d_m`.
- A2 Newtonian-gauge baryon continuity: PASS. Maximum normalized L2 residual across six modes is `1.114877014563e-06`, versus the preregistered `2e-3` gate.
- A3 dense/native closure: PASS. Maximum `d_b` relative L2 is `1.582957008794e-07`; maximum `t_b` relative L2 is `4.310593390133e-07`, both below `2e-4`.
- A4 convention/scope: PASS. CLASS `theta_b` is used directly as the Newtonian-gauge velocity divergence in `delta_b' + theta_b - 3 phi' = 0`, with no added scale-factor redefinition. Memory, likelihood, refit, nonlinear full-J evolution, and branch selection were absent.

## Interpretation

The corrected Exp-normalization model now has a certified corrected baryonic density and velocity source consistent with its own CLASS perturbation dynamics. Historical D2A remains unchanged. This PASS licenses corrected source-dependent full-J static/reclosure testing, but not memory/likelihood claims or NL1C7 by itself.
