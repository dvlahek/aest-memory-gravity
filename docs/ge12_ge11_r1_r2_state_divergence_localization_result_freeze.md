# GE12 GE11 R1/R2 state-divergence localization — result freeze

## Status

Frozen first locked GE12 execution.

Terminal classification:

`GE12_GE11_R1_R2_STATE_DIVERGENCE_LOCALIZED`.

GitHub Actions run:

`35500848748`.

Execution HEAD:

`6f79cf9968e8c3d09eaa5c8a179292aec0a37926`.

Artifact:

- ID: `10602610942`;
- name: `results_bundle_ge12_ge11_r1_r2_state_divergence_localization`;
- ZIP SHA-256:
  `2b44a0c38d1a3aadcb05f1ed743560a68817e720dcb4d2cc41fe040d0b409fd9`.

## Frozen output hashes

Result JSON:

- bytes: `29988`;
- SHA-256:
  `a374e3c66dcf7e73591c19acd22ae75a119798d73a222ea9678dac317b12380c`.

Result log:

- bytes: `29988`;
- SHA-256:
  `a374e3c66dcf7e73591c19acd22ae75a119798d73a222ea9678dac317b12380c`.

Result NPZ:

- bytes: `137011`;
- SHA-256:
  `1ec36eb7e253e8fbc543f8fa20f04d269419d2c883b59349a1fb3ffa290041eb`.

Parent artifact metadata JSON:

- bytes: `852`;
- SHA-256:
  `9e41662bc3b62d1717815e5f962fc6600057d86971be78db185be77e6879720e`.

## Gate result

Every locked GE12 diagnostic gate passes:

- exact parent artifact digest;
- exact parent classification;
- exact frozen R1/R2 dense trace hashes;
- exactly 64 common ln(a) nodes;
- reconstructed parent complete-jet global mismatch within `1e-12`;
- reconstructed parent pointwise mismatch within `1e-12`;
- exact derived dictionary identities within `1e-12`;
- all quantities finite.

The frozen parent complete-jet discrepancy is reproduced as:

- global relative L2:
  `0.4588606870438122`
  versus parent
  `0.45886068704381233`;
- pointwise abs-or-rel:
  `0.7829092344800966`
  exactly.

The global reconstruction difference is
`1.1102230246251565e-16`.

## Localization result

The dominant R1/R2 discrepancy is concentrated in the AeST internal/aether-memory state.

Largest raw/derived channel global relative-L2 discrepancies:

- `ut_kernel=H alpha-E+psi`:
  `0.48709984609707435`;
- `E_aest`:
  `0.4870998415154267`;
- `chi`:
  `0.48709981721306234`;
- `alpha_aest`:
  `0.48709981658243034`;
- `u_kernel=alpha_aest`:
  `0.48709981658243034`;
- `alpha_aest_prime_interp`:
  `0.4870998096656848`;
- `E_aest_prime_interp`:
  `0.48709980885396903`.

The corresponding cosines remain high, approximately `0.98478`, so the two precision levels are strongly aligned but not equal.

The baseline metric state is much more stable:

- `psi`: global `0.00428111365`;
- `phi`: global `0.00428110935`.

Background quantities are essentially unchanged:

- `Q`: exactly identical;
- `rho_dark`, `p_dark`, `H/H0`, `cad2_dark`: sub-`1e-6` to sub-`1e-9` global differences.

## Multiplicative-scale diagnostic

For the dominant AeST channels, the global least-squares R2/R1 scale is nearly identical:

- `alpha_aest`: `0.521680347454335`;
- `E_aest`: `0.5216803229837121`;
- `chi`: `0.5216803469168892`;
- `ut_kernel`: `0.5216803189242599`.

Their post-rescaling relative-L2 residuals are all approximately

`0.173798`.

Thus the cross-precision difference is not a pure single global amplitude rescaling, but a common amplitude component dominates the AeST internal channels.

## Time dependence

The best-fit R2/R1 scale for `alpha_aest`, `E_aest` and `chi` is effectively constant across all eight preregistered ln(a) bins.

For example, the `chi` scale remains within approximately

`0.521680304 -- 0.521680354`

over the full frozen redshift window.

Therefore the dominant discrepancy is not a growing temporal drift or a late-time instability.

## Scale dependence

The discrepancy is strongly k dependent.

For `alpha_aest` the per-k global relative-L2 discrepancies over

`k_h={0.03,0.05,0.08,0.10,0.15,0.20} h/Mpc`

are approximately

`{0.24883,0.40054,0.78291,0.52331,0.41381,0.45862}`.

`E_aest` and `chi` follow essentially the same k-dependent pattern.

In contrast, the matter/aether velocity channel `theta_dark` shows a different trend:

`{7.13e-6,4.67e-5,0.0132,0.0301,0.1303,0.5139}`.

The scalar-derived `varphi=Q a theta_dark/k^2` similarly becomes increasingly precision-sensitive toward the highest k.

## Scientific interpretation

GE12 localizes the GE11 Repair01 failure to a scale-dependent first-order AeST state normalization/transfer structure.

The evidence does not support a simple time-growing instability:

- the dominant AeST channel scale is almost time independent;
- metric/background channels remain comparatively stable;
- the discrepancy depends strongly on Fourier scale.

The evidence also does not support a single global multiplicative normalization as a complete explanation because the post-rescaling residual remains about `17.4%` and the per-k discrepancies vary substantially.

No physical instability is claimed.

## Project boundary

GE12 does not:

- relabel GE11 Repair01;
- select R1 or R2;
- license R3;
- change the precision settings;
- alter the GE06 local-jet dictionary;
- license `Z20`;
- establish a physical instability.

A separately preregistered follow-up may diagnose the **per-k multiplicative normalization and phase/shape residual** of the frozen R1/R2 AeST state using only the frozen GE12/GE11 artifacts.

The purpose of such a diagnostic is to distinguish:

1. a k-dependent but time-stable transfer-function normalization shift;
2. a genuine within-k shape/phase change.

No new CLASS execution is required for that localization.
