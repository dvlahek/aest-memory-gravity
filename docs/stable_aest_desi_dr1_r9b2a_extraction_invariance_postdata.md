# Stable AeST DESI DR1 R9b2a extraction-invariance post-result record

## Status

Historical result retained unchanged:

`STABLE_AEST_DESI_DR1_R9B2A_SERIALIZATION_FREE_EXTRACTION_UNRESOLVED`

The diagnostic completed after the pre-result technical repair that removed the inherited `l_max_scalars` parameter from the transfer-only `mPk,mTk,vTk` output request. The repair changed no science setting, gate, eta/tau point, extraction formula, or classification rule.

R9b2a is theory-only. No DESI data vector or likelihood was evaluated.

## Locked parent state

- R9b2a preregistration: `950b4d37a9a6480e7f8e65d2a5a946230987b09a`
- historical R9b2 postdata: `5f453a296d367556927cfa8e1e86b7ea103a9b52`
- historical R9b2 classification remains `STABLE_AEST_DESI_DR1_R9B2_CENTRAL_DERIVATIVE_FAIL`
- R9b2 velocity adapter remains `STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_VALIDATED`
- R9b2a implementation lock printed by the runner: `c63229f7bc9fe7137b276a5df7bf00ee97ebccb5`
- pre-result transfer-output technical repair: `c969a3cd35b15d9ae1ad575d5972bc058bb001ba`

Historical R9b and R9b2 classifications are not altered by this result.

## Gate result

- `R9B2A_A1_provenance_and_historical_fail_lock = true`
- `R9B2A_A2_internal_output_request_invariance = true`
- `R9B2A_A3_serialization_free_density_consistency = false`
- `R9B2A_A4_serialization_free_direct_velocity_sanity = false`
- `R9B2A_A5_eta0_tau_invariance = true`
- `R9B2A_A6_material_diagnostic_output_contamination = false`

The preregistered contamination hypothesis is therefore **not reproduced**. In particular,

- locked vs no-`k_output_values` `f_direct`: `2.7864309409031372e-11`
- locked vs no-`k_output_values` `sigma8_dd`: `9.273361364189838e-12`
- adjacent-ULP vs locked `f_direct`: `7.604553867600103e-13`
- adjacent-ULP vs locked `sigma8_dd`: `6.767625357145929e-13`
- maximum material-contamination metric: `2.7864309409031372e-11`, far below the frozen `0.05` gate.

The internal quantities are also invariant under the output request:

- internal growth-proxy locked vs no-`k_output_values`: `3.1780409918394666e-13`
- internal sigma8 locked vs no-`k_output_values`: `3.601711200956656e-12`.

At eta=0 the no-`k_output_values` extraction is tau-invariant to high precision:

- maximum tau variation in `f_direct`: `2.001957230312556e-08`
- maximum tau variation in `sigma8_dd`: `5.2706364864387176e-09`.

## Extraction failure pattern

The failure is instead inside the external extraction path.

For `tau_H0=10`, representative points are:

| z | internal sigma8 | external sigma8_dd | external sigma8_tt | f_direct | internal legacy proxy |
|---:|---:|---:|---:|---:|---:|
| 0.295364043 | 0.699359070 | 8.10154308e4 | 3.38964875 | 4.18395448e-5 | 0.681053106 |
| 0.509628868 | 0.626100601 | 7.23072938e12 | 1.95030807e71 | 2.69724943e58 | 0.762883835 |
| 0.705795647 | 0.568441545 | 0.570890958 | 0.466659511 | 0.817423194 | 0.818264548 |
| 0.918585197 | 0.514983075 | 0.517209763 | 3.33693599e7 | 6.45180394e7 | 0.862175923 |
| 1.317065883 | 0.435444345 | 0.437336608 | 0.399350365 | 0.913141863 | 0.914300507 |
| 1.490501776 | 0.407441230 | 0.409214918 | 0.379707631 | 0.927892935 | 0.929020721 |

The same pathological points appear with the locked request, adjacent-ULP request, and no-`k_output_values` request. Hence the R9b2a result excludes the tested diagnostic-output serialization as the cause of this DESI extraction failure.

## Relation to the preserved v0.76-v0.78 numerical audit

This pattern is consistent with the already preserved CLASS-chain diagnosis:

- v0.76 established source-to-Fourier closure at common native nodes to approximately machine precision but found large off-node source-power versus `pk_lin` discrepancies. Its fractional response became ill-conditioned near deep minima where division by very small local `d_m` or `P_m` amplifies finite differences.
- v0.77 avoided that division and certified the native matter-state tangent as lambda-affine.
- v0.78 then certified `V078_TIME_INTERPOLATION_OPERATOR_DISCREPANCY_LOCALIZED`: source-derived matter power and Fourier matter power agree on common native `(k,tau)` nodes, but can disagree strongly at off-native times even at exactly the same native Fourier k nodes. The preserved interpretation explicitly localizes the mismatch to the distinct time-interpolation operators and recommends the certified state/native-source representation for later work.

The R9b2 extraction combines exactly the two operations that those audits warn against: density power from `pk_cb_lin(k,z)` and a transfer-derived ratio `(v_cb/d_cb)^2`. Because the two factors are produced by distinct interpolation paths, the formal cancellation of `d_cb^2` is not numerically protected near transfer minima.

## Consequence

R9b2a does **not** license a serialization-free DESI science rerun. It instead licenses a new theory-only source-consistent extraction closure test.

The next diagnostic must construct both spectra from the same transfer state,

`P_dd(k,z) = C(k) d_cb(k,z)^2`

and

`P_tt(k,z) = C(k) v_cb(k,z)^2`,

with the same primordial prefactor `C(k)`, without calling `pk_cb_lin` inside the construction and without forming `v_cb/d_cb`.

Before any new DESI projection, this source-consistent adapter must reproduce the already validated GR velocity adapter/CAMB benchmark and give finite, physical eta=0 AeST values at all six frozen DESI effective redshifts. No historical result is reclassified by such a follow-up.
