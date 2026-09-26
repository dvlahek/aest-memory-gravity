# GE19 H4F3d14 — actual original R1 source-weighted GE05 bath phase partition: independent archive freeze

**Date:** 2026-09-26. **Physical local classification:** `GE19_H4F3D14_ACTUAL_ORIGINAL_R1_SOURCE_WEIGHTED_PHASE_BATH_DIAGNOSTIC_PASS_ONSHELL_OPEN`. **Independent postrun classification:** `GE19_H4F3D14_ACTUAL_ORIGINAL_R1_SOURCE_WEIGHTED_PHASE_BATH_INDEPENDENT_ARCHIVE_AUDIT_PASS_ONSHELL_OPEN`. No GE05 first-order bath on-shell, no full H4 Noether, no Z21 or lensing claim.

## Immutable actual physical inputs and archive

Four original user-local D14 files independently hashed and checked against the original local runner:

| Actual uploaded file | SHA-256 | Bytes |
| --- | --- | ---: |
| `ge19_h4f3d14_actual_original_r1_source_weighted_phase_bath.json` | `8d8244cf810447c96df82f6ece6c161a4dd0553f707e3a698ed0b29f37ff3c6e` | 290019 |
| `ge19_h4f3d14_actual_original_r1_source_weighted_phase_bath.npz` | `f79d87f10dc1561ef2c61997b7952d62d85eda6674abaa015e5d38e161b55c48` | 31955470 |
| `ge19_h4f3d14_actual_original_r1_source_weighted_phase_bath_FULL.log` | `8d8244cf810447c96df82f6ece6c161a4dd0553f707e3a698ed0b29f37ff3c6e` | 290019 |
| `ge19_H4F3D14_LOCAL_runner.log` | `497871f79c0969f619287d215e532bdc235e08a263bec48958054dc6b3c96586` | 2512 |

JSON and FULL log are identical by bytes. Original runner reports exact original code, Repair26 R1 accepted-step 26,643,162-byte trace SHA, and actual D13 JSON/NPZ SHA PASS. Original D13 actual SHA256 values were independently verified against the separately mounted original D13 physical bytes: JSON `2b4dfbd30ec6466292e0dcf62eeed8b723555d1890a127a5e0a6ff761d2ebe76` and NPZ `1608fe98dd924b2b235ecf0f8fce768f2f3a2fa4a2854de04a56fe622ad3df89`. The raw original Repair26 R1 trace is SHA-gated on the user-local runner and driver and was not independently repropagated in this postrun archive audit.

Original D14 actual NPZ stores **746 distinct finite arrays**, all original `C_min,C_star,C_max × Nt128,Nt64 × Nq2048,Nq1024` cases, both original one-sided interval endpoints, and the original six positive spatial modes `[3,5,8,10,15,20]` plus their signed negative-frequency conjugates. The D14 output `m0..40` is the signed convolution of this original six-input-mode parent. It is **not** the full `m0..64` Nyquist bath archive.

## Independent source/phase/D13 reconstruction checks

The five preregistered phase bins `[0,.25), [.25,.5), [.5,1), [1,pi), [pi,infinity)` form an exact partition for all **1,751,040** original node-interval phase entries in twelve physical C/Nt/Nq cases. Their independently counted populations exactly match each saved JSON row. Both sides' saved phase arrays match exact original D13 actual physical phase arrays.

The 12 sampled FD4 signed W arrays match original D13 bitwise. Independently summing all five signed complex W bins in original `m0..40` for both sides and all cases reconstructs the frozen actual D13 signed parent with maximum relative discrepancies:

| Independently reconstructed original source | Maximum relative difference |
| --- | ---: |
| Original one-sided signed interval ODE W | `4.666416083264566e-16` |
| Original sampled FD4 derivative-defect signed W | `5.150113272825773e-16` |
| Original sampled FD4 signed W | `4.4297659348837253e-16` |
| Per-bin `W_FD4 = W_ODE + W_defect` | `4.1685390616065405e-16` |

The conservative per-frequency-node signed-pair absolute-sum envelope majorizes each saved complex bin component, with numerical excess no greater than `4.544e-28` absolute. The original JSON's separately reported full-source relative identity can be as high as `2.874240521458319e-14` because it normalizes a cancellation-sensitive residual differently; this is still an **algebraic machine identity**, not a physical bath-on-shell residual. The original FD4 m0 coefficient reaches at most `3.2202159546123623e-24` absolute; no exact zero or all-sector Ward claim is inferred.

## Actual phase-weighted physics: high-frequency interval ODE differs from FD4

At original `C_star,Nt128,Nq2048`, the unweighted original interval phase exceeds `pi` for `0.5432609498%` of node-interval pairs, with maximum `961.031376`. This unweighted population is **not** the source-weighted bath contribution. Using the actual saved signed W and conservative unsigned source-pair envelopes, the fraction `||unsigned W_bin||_2 / ||sum_bins unsigned W_bin||_2` at `phase >= pi` is:

| Original source-weighted quantity | Left | Right |
| --- | ---: | ---: |
| Original one-sided interval ODE | `1.883603607e-7` | `1.957263738e-7` |
| Original sampled FD4 derivative defect | `5.208835857e-4` | `4.822060897e-4` |
| Original sampled FD4 total | `0.01460932802` | `0.01459704721` |

The corresponding original **left signed** whole W L2 norms are interval ODE `1.4132200209806873e-12`, FD4 derivative defect `1.3664519122854888e-12` and final sampled FD4 `4.8422385381524534e-14`. The near cancellation inflates the relative high-phase share of sampled FD4, even though the high-phase source-weighted *interval ODE* W is tiny on this frozen discretization.

Across both sides and all twelve C/Nt/Nq original cohorts, the phase >= pi conservative unsigned W-bin/total-envelope norm ratio spans `1.51714e-7..1.64316e-6` for the original interval ODE, `4.80693e-4..1.44684e-3` for the sampled derivative defect, and `0.0145388..0.0195537` for the sampled FD4 total. These are descriptions of the frozen **discrete signed Ward parent**, NOT bounds on continuous-time GE05 per-node EOM error or on the full all-sector action Ward residual.

## Why separate Nq phase-bin quadrature can look unstable

The actual original sampled FD4 signed W changes by up to `0.01354770743` relative under original Nq2048 vs Nq1024 quadrature. At primary `C_star,Nt128`, the difference is `6.569599692967569e-16` absolute L2 or `0.01349759228` relative. For the *phase >= pi subset* of this same case, the original **signed interval ODE W** Nq difference is only `7.593873261767442e-20` absolute but `0.2852753` relative to its extremely small high-phase bin, and the high-phase FD4 signed bin changes `0.7871515` relative. In the original `C_star,Nt64` control, the high-phase FD4 bin relative change is `0.5644919`.

A hard phase-bin mask changes its set of quadrature nodes between nonnested original quadrature orders. These large **individual-bin relative differences** are therefore not standalone quadrature error bars. The full original signed interval ODE total had already matched Nq2048/1024 at <=`7.661e-8` relative in D13, but its two sampled FD4 cancellation components and the discontinuous phase partitions require a separate continuous-time and quadrature error argument. Neither ignoring the high-frequency nodes nor substituting the small total FD4 residual for the true first-order GE05 EOM is justified.

## Source-first next stage and immutable stop

The scientifically relevant next D15 task is an **original-action continuous-time R1 interpolation/propagation defect and cancellation-aware total signed bath error budget**. The original Repair24 interval propagator is exact for its *piecewise frozen* `h_mid=tau sqrt(H_i H_{i+1})` and linearly interpolated `X10`; its D13 endpoint Euler residual is proportional to `H_endpoint-h_mid/tau`. Thus small discrete signed W and a small high-phase bin do not alone certify the true variable-H and variable-drive continuous GE05 bath EOM. D15 must retain the original action, original R1 dense/history input, all original modes and phase weights, and distinguish numerical ODE/forcing interpolation errors from on-shell residuals without selecting physics from lensing or any observable.

The complete original action/Noether boundary contribution `E_i00 ∂χ F_i21`, `a E_L21 + L21 E_L00 - b21 E_b00` remains uncomputed. Original Repair37 SCIENCE_FAIL and archived original D10 FAIL are immutable. **`GE05_bath_first_order_on_shell_certified=false`; `actual_all_sector_H4_Ward_certified=false`; `Z21_certified=false`; `lensing_licensed=false`.**

Machine audit: `ge19/h4f3d14_actual_original_r1_source_weighted_phase_bath_independent_archive_audit.json`, Git blob `3f7acc17aee24c6b776578ef2b654a40b2db6af0`.
