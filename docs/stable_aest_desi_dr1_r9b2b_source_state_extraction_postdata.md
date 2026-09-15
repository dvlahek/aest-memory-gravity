# Stable AeST DESI DR1 R9b2b source-state extraction post-result record

## Historical classification

Retain unchanged:

`STABLE_AEST_DESI_DR1_R9B2B_AEST_ETA0_CLOSURE_FAIL`

R9b2b was theory-only. No DESI data vector, covariance, likelihood, eta preference, or tau constraint was evaluated.

The repair01 wrapper only replaced an invalid byte-SHA provenance check for the local R9b2a JSON with the already locked semantic parent checks. It changed no physics, source equation, redshift, tau, threshold, interpolation, or R9b2b science gate.

## Artifact hashes

Uploaded completed artifacts:

- `stable_aest_desi_dr1_r9b2b_source_state_extraction.json`: SHA-256 `bc0013a70a1e13ef925efc39b57f8810d7c5bab80091eed1ba4407bc1862314e`, 24877 bytes
- `stable_aest_desi_dr1_r9b2b_source_state_extraction.log`: SHA-256 `756225120d12f9c8d1a82b17dab5cc0056cf95e094d79309b7bd40cc23d2e74f`, 4863 bytes
- `stable_aest_desi_dr1_r9b2b_source_state_extraction_FULL_runner.log`: SHA-256 `f13ba3293f2f4cc4f861fd1476371f77d80c36c6dc660620ef1ea570cdb91b98`, 5989 bytes

The local R9b2a parent SHA printed by repair01 was
`e6eabb125925348f7bcae63db92e86a47c394f0861c8bff51452e7ef37565086`.

## Gates

- `R9B2B_B1_provenance_and_historical_lock = true`
- `R9B2B_B2_source_state_construction = true`
- `R9B2B_B3_pure_GR_benchmark = true`
- `R9B2B_B4_AeST_eta0_source_internal_consistency = false`
- `R9B2B_B5_eta0_tau_invariance = true`
- `R9B2B_B6_pathological_point_removal = false`

Therefore the source-consistent DESI follow-up is not licensed by R9b2b.

## Clean GR control

The source-state construction

`P_dd = C(k) d_cb^2`

`P_tt = C(k) v_cb^2`

with no `pk_lin`, no `pk_cb_lin`, and no local `v_cb/d_cb` ratio reproduces the locked GR adapter extremely well:

- max relative `f` difference vs locked CLASS adapter: `1.7712822347997615e-07`
- max relative `f` difference vs locked CAMB: `4.067555296812559e-05`
- max relative `sigma8_dd` difference vs locked CLASS adapter: `3.4521423909594334e-05`
- max relative `sigma8_tt` difference vs locked CLASS adapter: `3.4344301769484965e-05`

All are far below the frozen `5e-3` gate.

## AeST eta=0 failure pattern

At `tau_H0=10`, the off-native `get_transfer(z)` source state gives:

| z | sigma8_dd source | sigma8_tt source | f_source | internal sigma8 | internal growth proxy |
|---:|---:|---:|---:|---:|---:|
| 0.295364043 | 4.6442525e7 | 48.4435 | 1.0431e-6 | 0.699359 | 0.681053 |
| 0.509628868 | 0.628804 | 76.3090 | 121.356 | 0.626101 | 0.762884 |
| 0.705795647 | 0.570906 | 502.851 | 880.794 | 0.568442 | 0.818265 |
| 0.918585197 | 0.517224 | 2.348467e6 | 4.540519e6 | 0.514983 | 0.862176 |
| 1.317065883 | 0.437351 | 0.399363 | 0.913142 | 0.435444 | 0.914301 |
| 1.490501776 | 0.409229 | 0.379721 | 0.927893 | 0.407441 | 0.929021 |

Thus the density state itself is pathological at the first redshift, while at the next three problematic redshifts the density RMS is normal but the velocity state is catastrophically large. The last two redshifts are healthy.

## Tau invariance of the pathology

The pathological values are effectively identical for `tau_H0={10,5,2.5,1.25}` at eta=0:

- max relative tau variation in `f_source`: `1.131039355633761e-08`
- max relative tau variation in `sigma8_dd_source`: `1.1678474244667484e-08`
- max relative tau variation in `sigma8_tt_source`: `3.6808077133616175e-10`

This strongly disfavors the memory-relaxation parameter as the origin of the failure.

## Interpretation

R9b2b eliminates the mixed `pk_lin`/transfer construction and the local `v/d` ratio as necessary causes of the pathology. Since the pure-GR source-state construction is clean, but the AeST-enabled eta=0 `get_transfer(z)` source state fails at isolated requested redshifts and is almost exactly tau-invariant, the next unresolved layer is the off-native AeST transfer-state interpolation itself.

This is consistent with the preserved v0.78 result that native source and Fourier matter power close at common native `(k,tau)` nodes while large discrepancies can appear at off-native times because of distinct CLASS time-interpolation operators.

R9b2b does not by itself prove that the native AeST velocity state is healthy. That must be tested directly before any further DESI science projection.

## Licensed next step

A separately preregistered theory-only audit may:

1. read the full native transfer table with `get_transfer_and_k_and_z(...)`;
2. verify finite/physical native density and velocity states;
3. interpolate the raw native state variables `d_b,d_cdm,t_b,t_cdm` to the six frozen DESI effective redshifts using a predeclared external interpolation in scale factor;
4. compare that result with both GR benchmarks/internal integrated observables and the pathological direct `get_transfer(z)` path.

No historical FAIL is reclassified by such a follow-up.
