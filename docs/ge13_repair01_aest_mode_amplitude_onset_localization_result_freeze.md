# GE13 Repair01 AeST mode-amplitude onset localization — result freeze

## Status

Frozen first science-reaching GE13 Repair01 execution.

Terminal classification:

`GE13_AEST_MODE_AMPLITUDE_ONSET_LOCALIZED`.

GitHub Actions run:

`35501740049`.

Execution HEAD:

`f70fdf95a05c4461ac7bd37c952e57b401608222`.

Artifact:

- ID: `10601814407`;
- name: `results_bundle_ge13_repair01_aest_mode_amplitude_onset_localization`;
- ZIP SHA-256:
  `dc9513f2b63aec4dbacbaf5af4858dd0b2928a9cf76467a95ff4d0ff6c2cb096`.

## Frozen output hashes

Result JSON:

`ddce8acd113eedb5997d943ae573a84a121173349b46659153f11df4360b7d14`.

Result log:

`ddce8acd113eedb5997d943ae573a84a121173349b46659153f11df4360b7d14`.

Result NPZ:

`45d41ab828ff171507ac17280eaa502343706d50481c0d5b73855f0a3d5726b7`.

GE11 metadata JSON:

`9e41662bc3b62d1717815e5f962fc6600057d86971be78db185be77e6879720e`.

GE12 metadata JSON:

`30bf3e895827af405c30e6092b7e5004e46e832c2479f914a7a4edf25c9b9f92`.

Every locked GE13 diagnostic gate passes.

## Late-time per-k mode structure

For each frozen k mode, the R2/R1 scale of the four AeST internal channels

- `alpha_aest`;
- `E_aest`;
- `chi`;
- `ut_kernel=H alpha-E+psi`

is the same to approximately `1e-7` or better.

For `alpha_aest`, the late-window R2/R1 scales are:

- k_h=0.03: `0.7511674301437334`;
- k_h=0.05: `0.5994608868152181`;
- k_h=0.08: `0.21709096980186046`;
- k_h=0.10: `0.47668729217321115`;
- k_h=0.15: `0.5861929310407155`;
- k_h=0.20: `0.541379012214324`.

After fitting one scale independently for each k, the alpha post-rescaling relative-L2 residuals are only

`1e-8 -- 8e-8`

and the cosines are numerically unity.

Thus the late R1/R2 difference is, mode by mode, overwhelmingly an amplitude difference of the same AeST temporal solution.

It is not a late-time shape divergence.

## Initial agreement

At the first common accepted endpoint the alpha R1/R2 abs-or-rel mismatches are approximately

`3e-22 -- 1e-20`.

Thus the two corrected-precision executions begin on numerically indistinguishable AeST states.

The order-unity late discrepancy is generated during subsequent evolution.

## Departure epochs

The first 0.1% alpha-amplitude departure occurs at:

| k_h [h/Mpc] | a | z | k/(aH) |
|---:|---:|---:|---:|
| 0.03 | 0.0086582 | 114.50 | 14.67 |
| 0.05 | 0.0072586 | 136.77 | 22.32 |
| 0.08 | 0.0027028 | 368.99 | 21.12 |
| 0.10 | 0.0025185 | 396.07 | 25.39 |
| 0.15 | 0.0022277 | 447.89 | 35.58 |
| 0.20 | 0.0019514 | 511.45 | 44.04 |

The first 10% departure occurs at:

| k_h [h/Mpc] | a | z | k/(aH) |
|---:|---:|---:|---:|
| 0.03 | 0.0247147 | 39.46 | 25.04 |
| 0.05 | 0.0198045 | 49.49 | 37.30 |
| 0.08 | 0.0073004 | 135.98 | 35.81 |
| 0.10 | 0.0068806 | 144.34 | 43.41 |
| 0.15 | 0.0062228 | 159.70 | 61.79 |
| 0.20 | 0.0054471 | 182.58 | 76.85 |

Therefore the visible precision-level separation begins well after horizon entry, not at the initial superhorizon state.

The crossing values are strongly k dependent and do not identify one universal horizon-crossing trigger.

## Full-history behavior

Before the departure regime, the R2/R1 scale is numerically unity.

For the highest-k example, the fitted alpha scale evolves approximately as:

- a~5e-5: `0.999999997`;
- a~1.2e-4: `0.999999981`;
- a~2.7e-4: `0.999999489`;
- a~6.3e-4: `0.999982668`;
- a~1.5e-3: `0.999197812`;
- a~3.4e-3: `0.958203`;
- a~8.0e-3: `0.591652`;
- a~1.86e-2: `0.542252`;
- late plateau: `0.541379`.

The same qualitative pattern occurs mode by mode: an initially common branch, rapid amplification/separation, then a time-stable per-k amplitude plateau.

## IC provenance

The frozen v0.19i source still uses only the leading superhorizon adiabatic identities:

`delta_A=(1+w_A)delta_c`;

`alpha_A=-a Theta_A/k^2`;

`E_A=0`.

Equivalently, at leading order,

`chi_i=0`, `E_i=0`.

The v0.19i theory note explicitly leaves finite-gradient terms

`O[(k/H)^2]`

uncertified.

## Interpretation

GE13 excludes several simple explanations for the GE11 failure:

- the corrected R1/R2 runs do not begin from measurably different states;
- the discrepancy is not a late-time interpolation artifact;
- it is not a late-time temporal-shape instability;
- it is not one universal multiplicative normalization across all k.

The observed structure is consistent with a tiny precision-dependent excitation of a scale-dependent AeST homogeneous/isocurvature mode that is amplified after the initial epoch and later dominates the internal AeST amplitude.

This interpretation is not yet a certified physical conclusion.

In particular, GE13 alone does not distinguish:

1. numerical excitation of an existing homogeneous mode because the leading-order IC does not lie exactly on the finite-k regular adiabatic manifold;
2. excitation associated with a CLASS approximation/integration transition;
3. another early-time numerical representation effect.

## Licensed continuation

Do not add R3 or select R1/R2.

The next physics-first step is to derive and independently audit the finite-gradient regular AeST adiabatic initial condition through

`O((k/H)^2)`

using the frozen eta=0 linear equations.

Only after that analytic correction is fixed should a new precision-pair CLASS test be run.

That test should ask if the corrected IC eliminates the per-k amplitude bifurcation.

## Claim boundary

GE13 does not:

- relabel GE11;
- select R1 or R2;
- modify initial conditions;
- claim a physical instability;
- license `Z20`, `Z21` or finite eta.
