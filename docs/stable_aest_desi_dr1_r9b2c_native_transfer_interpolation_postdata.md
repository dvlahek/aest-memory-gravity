# Stable AeST DESI DR1 R9b2c native-transfer interpolation post-result record

## Historical result

R9b2c completed with `EXIT=1` and is retained as the historical theory-only failure

`STABLE_AEST_DESI_DR1_R9B2C_NATIVE_AEST_STATE_FAIL`.

No DESI data vector, covariance, likelihood, eta preference, or tau constraint was evaluated. No earlier R9b/R9b2/R9b2a/R9b2b result is reclassified.

## Locked setup

- R9b2c preregistration: `1e999d87c1158ee7be764e6055164d75a179b059`
- R9b2c implementation: `cb15af792b6d2deca3c495a47f75238986e85c00`
- R9b2c runner: `1a1aac02cdcc6511109098fc8369b219fbd63a21`
- parent R9b2b postdata: `3101581468bc8a5b85eb2b34c33df22418f1ce88`

## Result interpretation

The pure-GR custom native-table interpolation benchmark was healthy, but the AeST-enabled transfer/Fourier table failed its native-state sanity gate already at eta=0. The table returned by `get_transfer_and_k_and_z(...)` contained pathological density and/or velocity amplitudes before interpolation to the six frozen DESI effective redshifts.

The completed run showed approximately 19 transfer redshift nodes in the relevant output table. Its AeST native-health scan reached pathological values of order

- `sigma8_dd_max ~ 1.5e45`
- `f_max ~ 3.6e8`.

The AeST transfer table also contained approximately 864 k nodes, while the matched GR-control transfer table contained approximately 108 k nodes.

Therefore R9b2c does **not** establish an off-native `get_transfer(z)` accessor defect as the sole cause. It localizes the pathology earlier, to the AeST transfer/Fourier output path or to a configuration entering that path. It also does not establish that the underlying ODE perturbation history is pathological, because `get_transfer_and_k_and_z(...)` is itself a transfer/Fourier output product rather than the raw per-mode `get_perturbations()` solver history.

## Newly identified configuration ancestry

Post-result code inspection found that Stable-AeST R5b parameter construction inherits the spectral-fringe forensic parameter builder:

`stable_aest_observable_projection_r5b_derivative_zero.build_params`

→ `aest_ulp_initial_amplitude_localization.make_params`

→ `corrected_class_spectral_fringe_bridge_identity.r3_params`

→ `nl1c6d2n.corrected_class_baseline.build_params`.

The final parent explicitly sets

- `k_per_decade_for_pk = 80.0`
- `k_per_decade_for_bao = 560.0`.

By contrast, the underlying `v063.theory_response_map.class_params()` does not set either parameter and therefore uses the normal CLASS sampling defaults.

The approximately 864-versus-108 k-node difference observed in R9b2c is consistent with this inherited dense-k forensic configuration. This observation is post-result and is not itself a repaired R9b2c result.

## Consequence

Before inspecting raw ODE histories, the smallest theory-only follow-up is an A/B configuration-isolation test at eta=0 and tau_H0=10:

1. exact inherited dense-k R9 parameters, with `k_output_values` removed;
2. identical parameters with only `k_per_decade_for_pk` and `k_per_decade_for_bao` removed so CLASS defaults apply.

The follow-up must use the same CLASS build, same cosmology, same source-state extraction, same six redshifts, and no DESI likelihood. If the normal/default grid is healthy while the inherited dense grid reproduces the pathology, the dense-k forensic inheritance is localized as the relevant output-configuration defect. If both remain pathological, the hypothesis is falsified and the next layer is raw `get_perturbations()` solver-history closure.
