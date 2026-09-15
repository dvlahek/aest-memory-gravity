# Stable AeST DESI DR1 R9b2d k-grid inheritance post-result record

## Historical classification

R9b2d completed with

`STABLE_AEST_DESI_DR1_R9B2D_DEFAULT_GRID_AEST_UNRESOLVED`

and `EXIT=1`.

This is a completed theory-only diagnostic. No DESI data vector, covariance, likelihood, eta preference, matched filter, or tau constraint was evaluated. No earlier R9b/R9b2/R9b2a/R9b2b/R9b2c result is reclassified.

## Locked parent state

- R9b2d preregistration: `bb15759f23246d3b7af734ff7f7cb2052f44d651`
- R9b2d implementation: `a18020d3b307294b742614edc75a5ed28d7a91e8`
- R9b2d runner: `6fe8fe0f9e01cb77763ae20e2311a232d9b789cc`
- R9b2c postdata: `7c4cc8a0a9f2a59a91cbb288a157f880d630f309`

## Local artifact hashes

The completed local artifacts supplied after the run have SHA256 digests:

- `stable_aest_desi_dr1_r9b2d_kgrid_inheritance.json`: `54db5acc49d4099d1173aa029a58e02cdac0e844c03aa72d95fa08b86a6f70df`
- `stable_aest_desi_dr1_r9b2d_kgrid_inheritance.log`: `63d2df9addf4024056671a6013e64d0f6fe840af2eb0bb95819e5c7c2167b72e`
- `stable_aest_desi_dr1_r9b2d_kgrid_inheritance_FULL_runner.log`: `484440cf05c3cba4d1500812ac6dbd60bae2e5c55e2963edd35f74b856dd38f4`

The JSON is a local generated artifact and is identified here by hash rather than treated as a repository source file.

## Frozen gate result

- `R9B2D_D1_provenance_and_configuration_isolation = true`
- `R9B2D_D2_node_count_separation = true`
- `R9B2D_D3_GR_sampling_invariance = true`
- `R9B2D_D4_DEFAULT_AeST_eta0_closure = false`
- `R9B2D_D5_DENSE_pathology_reproduction = false`
- `R9B2D_D6_internal_solution_invariance = true`

The inherited dense-grid settings therefore materially change where and how the pathology appears, but they are **not** its root cause: the normal/default CLASS grid remains pathological in the AeST velocity/source extraction.

## Quantitative result

The inherited dense grid has 864 transfer/Fourier k nodes, while the DEFAULT grid has 108, giving the preregistered eightfold separation:

`node_ratio_dense_over_default = 8.0`.

The GR controls are essentially sampling invariant:

- max relative `sigma8_dd` dense/default: `2.541798588617514e-07`
- max relative `sigma8_tt` dense/default: `2.392073600341683e-07`
- max relative `f` dense/default: `1.993830553092911e-08`.

The AeST internal observables are also stable under the sampling change:

- max relative internal `sigma8`: `1.1080178912511883e-06`
- max relative internal growth proxy: `4.898983663058511e-06`.

Thus the physical/integrated eta=0 solution is insensitive to DENSE versus DEFAULT sampling at the frozen tolerance.

## DEFAULT-grid AeST failure pattern

The DEFAULT grid largely repairs the density-source extraction but not the velocity-source extraction.

At the six frozen redshifts, DEFAULT AeST gives approximately:

| z | sigma8_dd_source | sigma8_internal | sigma8_tt_source | f_source | internal growth proxy |
|---:|---:|---:|---:|---:|---:|
| 0.295364043 | 0.702365 | 0.699359 | 1.2489e3 | 1.7782e3 | 0.681054 |
| 0.509628868 | 0.628804 | 0.626100 | 1.0626e7 | 1.6899e7 | 0.762888 |
| 0.705795647 | 0.570906 | 0.568441 | 50.7579 | 88.9075 | 0.818263 |
| 0.918585197 | 0.517225 | 0.514983 | 0.445383 | 0.861102 | 0.862176 |
| 1.317065883 | 0.437351 | 0.435444 | 0.399363 | 0.913142 | 0.914300 |
| 1.490501776 | 0.409229 | 0.407441 | 0.379721 | 0.927893 | 0.929020 |

The maximum DEFAULT density-source versus internal-sigma8 relative difference is only `0.0043692413021709465`, inside the frozen 0.5% density closure gate. The maximum DEFAULT velocity-derived growth mismatch is `0.9999999548560244`, causing D4 to fail.

Hence the unresolved pathology is now strongly concentrated in the transfer/output velocity sector (`t_b`, `t_cdm`, or their mapping into the output table), not in the integrated density growth observable.

## Interpretation

R9b2d falsifies the hypothesis that the inherited `k_per_decade_for_pk=80` and `k_per_decade_for_bao=560` forensic settings are the sole cause of the DESI extraction failure.

The settings do affect the manifestation of the pathology. For example, the DENSE configuration can move the failure between density and velocity channels and between redshifts. However, removing both settings does not restore a healthy AeST velocity-source spectrum.

The next diagnostic must therefore move below the transfer/Fourier output layer to raw `get_perturbations()` solver histories at fixed requested physical k modes. The critical test is raw `theta_b/theta_cdm` history versus transfer-table `t_b/t_cdm` at the same k and redshift, while independently checking baryon/CDM continuity and internal-observable invariance. No DESI likelihood is licensed before that closure is resolved.
