# NL1C6D2N corrected Exp normalization impact result

## Status

GitHub Actions run `34407314848` completed successfully on branch `v053-exp-normalization-corrected` at repository head `1ed13a3524dd3554279b444a6017dad363f38c42`.

The corrected CLASS baseline remains

`NL1C6D2N_CORRECTED_CLASS_BASELINE_R1_PASS`.

This document records the descriptive old-vs-corrected no-refit impact diagnostic. No similarity PASS/FAIL threshold was preregistered, so the impact comparison itself is not assigned a new physical PASS/FAIL classification.

## Corrected baseline health

All inherited R1 checks passed:

- B1 provenance: PASS.
- B2 corrected Exp background charge reconstruction: PASS, charge relative spread `6.357325297863e-15`.
- B3 baryon continuity: PASS, maximum normalized residual `1.188688787789e-06`.
- B4 finite linear trajectory: PASS.
- B5 dense/native closure: PASS, `d_b=1.354865426787e-07`, `t_b=3.299820175703e-07`.
- B6 TT/TE/EE finite spectrum health: PASS.

## Directly comparable background and spectra

The historical factor-2 Exp model was regenerated from the same pinned CLASS commit and patch stack, with identical cosmological/AeST parameters and no refit.

Relative L2 differences are:

- background `H`: `2.7403037469507506e-15`;
- background effective-dark density `rho_cdm`: `6.7150578503607606e-15`;
- TT, ell 2..2500: `2.6403517084529535e-04`;
- TE, ell 2..2500: `1.6452386657532847e-06`;
- EE, ell 2..2500: `6.873200407897351e-07`.

Thus the no-refit background is numerically unchanged to machine precision, while the primary CMB spectra change only weakly at the baseline level.

## Grid-aligned transfer diagnostic

The preregistered grid-aligned diagnostic uses bilinear interpolation on the common native `(k_h,z)` domain, no extrapolation, `0.2 <= z <= 6.0`, and reports the conservative maximum of the two interpolation directions.

The resulting relative L2 differences are:

- `d_b`: `1.850770009805024`;
- `t_b`: `2.8203959047719405`;
- `d_m`: `2.872281029489328`;
- `phi`: `0.1144124068326145`;
- `psi`: `0.11442758323608428`.

The maximum grid-aligned transfer difference is `2.872281029489328`.

These differences remain order unity after grid alignment and therefore are not an artefact of the small native-grid mismatch seen in the raw element-wise comparison.

## Rerun decision

Because the corrected Exp normalization defines a new covariant model revision and materially changes the CLASS perturbation trajectories, every later result that consumes a CLASS-derived baryon/matter/metric source from the historical factor-2 model must be regenerated for the corrected model.

Required corrected-model reruns:

1. baryonic source freeze (`NL1C5B`-equivalent corrected source block);
2. D2A matter-sector audit using the corrected source;
3. nonlinear full-J reclosure tests that consume the baryonic source, including the strongest R3/D2 path used for the current decision chain;
4. memory/tangent calculations whose forcing depends on the corrected `chi/Q` or matter/metric trajectory;
5. observational likelihood tests only after a corrected memory/tangent baseline exists.

Not required to rerun merely because of the Exp normalization revision:

- D1A action/canonical/static identities;
- D1B Minkowski scalar-mode regression;
- D1CDE manufactured quasistatic/high-gradient regressions;
- pure full-J interpolation/operator identities that do not consume a CLASS source;
- historical R/R2/R3 solver-repair attempts as historical records.

The historical results remain unchanged and retain their original classifications. They are not valid as corrected-model source-dependent predictions.

## Interpretation

The normalization correction has almost no effect on the fitted background at the same parameters and only a small direct effect on TT/TE/EE, but it materially changes the linear perturbation state that feeds the baryonic-source and memory sectors. The next scientifically valid step is therefore a fresh corrected baryonic-source freeze, not an observational refit and not a repetition of the entire historical numerical repair sequence.
