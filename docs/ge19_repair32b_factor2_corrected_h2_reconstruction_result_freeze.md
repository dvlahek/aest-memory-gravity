# GE19 Repair32B factor-two corrected reduced H2/Z11 reconstruction — result freeze

## Status

Classification:

`GE19_REPAIR32B_FACTOR2_CORRECTED_REDUCED_H2_Z11_RECONSTRUCTION_PASS`.

This validates the corrected H2 reconstruction only.

By preregistration:
- `Z11_certified = false`;
- `H4_Z21_licensed = false`.

No H4/Z21 solve, finite physical eta, or observational claim was made.

## Local output provenance

JSON:
- SHA-256: `226dd2a2a0e86ddccc39a62d833960bdf9d5a9af038ad3bf225bbbf69d0b95cf`
- bytes: `68434`

NPZ:
- SHA-256: `5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327`
- bytes: `1082578`

FULL log:
- SHA-256: `226dd2a2a0e86ddccc39a62d833960bdf9d5a9af038ad3bf225bbbf69d0b95cf`
- bytes: `68434`

Runner log:
- SHA-256: `1d88f93bb304d27f1c458e8c5b65cad795631a6875963e672c9c5c97a895310a`
- bytes: `70726`

The JSON and FULL log are byte-identical.

## Exact H2 equation

Repair32B uses the exact Repair32A dictionary:

`L_GE06 Z11 = -2 M1_GE05[Z10,q10]`.

Dictionary:
- `GE05_M1_to_GE06_raw_residual_scale = 2`;
- `fitted_normalization_used = false`.

Thus:
- aether source: `+Q a^3 B10`;
- scalar source: `-a^2 partial_x(B10)`;
- direct metric M1 source: zero;
- dust M1 source: zero.

## Reconstruction validation

All Repair32B validation gates PASS.

Key controls:

- B10 Nt128/Nt64 relative L2:
  `1.5452075499280114e-05`;
- linear-system relative L2 residual:
  `4.500763888743939e-16`;
- inherited dynamic-boundary abs-or-rel:
  `1.7462031549538564e-21`;
- full six-field global Nt128/Nt64 relative L2:
  `2.556265819451129e-04`;
- dynamic S,u,varphi,T global Nt128/Nt64 relative L2:
  `2.5562658185082605e-04`;
- reduced chi11 vs Repair29B R2 parent relative L2 max:
  `3.551143432738103e-04`;
- chi11 C-envelope relative L2 max:
  `2.5827438644493813e-04`.

Per-C chi11 parent closure:
- C_min: `1.0609116944188875e-04`;
- C_star: `9.716652083790403e-05`;
- C_max: `3.551143432738103e-04`.

This closes the historical Repair30 ~0.404 chi11 discrepancy by roughly three orders of magnitude.

## Historical Repair30 monitors

The following remain report-only exactly as preregistered:

- componentwise shift backward error:
  `0.9401687948604716`;
- anisotropy backward error:
  `2.1568055433880993e-16`;
- max-per-field Nt128/Nt64 state relative L2:
  `0.9628829383983947`.

Repair31 already diagnosed the large shift value as a local denominator/cancellation pathology and the large state value as domination by the near-zero algebraic dust-density coordinate.

Repair32B did not alter or relax these historical monitors.

## Interpretation

The exact factor-two GE05-to-GE06 raw-residual dictionary derived in Repair32A is sufficient to restore agreement between the independently constructed reduced H2 state and the certified Repair29B R2 eta tangent.

This is a reconstruction result, not yet the final Z11 certificate.

## Next licensed step

Repair32C must be artifact-only.

It may:
- read the frozen Repair32B JSON/NPZ;
- reconstruct the unchanged reduced operator from frozen GE15/Repair13 parents;
- re-evaluate global state precision, chi11 parent closure, main-equation residuals, and constraints with the Repair31-motivated global operator-scale normalization.

It must not:
- reintegrate H2;
- change the factor two;
- relax Repair32B reconstruction gates;
- relabel Repair30/31/32A;
- solve H4/Z21 before Z11 certification.

## Canonical status

**Repair32B = reconstruction PASS. The factor-two corrected H2 state is validated. Reduced Z11 remains NOT CERTIFIED until Repair32C. H4/Z21 remains BLOCKED until Repair32C PASS.**
