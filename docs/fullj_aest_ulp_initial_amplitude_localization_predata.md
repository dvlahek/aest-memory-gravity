# AeST ULP initial-amplitude localization — pre-data declaration

Date: 2026-09-13
Branch: `fullj-evolving-weyl-bridge`
Parent numerical result: `FULLJ_CLASS_FRINGE_AEST_ULP_SENSITIVITY_CERTIFIED`

This follow-up is fixed before inspecting any new full-history result.

## Motivation

The completed ULP forensic audit certified all of the following:

- the serialization effect is localized to the target `k_output_values` token;
- matched GR remains ULP-continuous;
- AeST changes materially under representable-double perturbations of the target k;
- historical R3 is not reclassified and no new-physics claim is licensed.

A post-result inspection of the already-produced sparse-redshift NPZ revealed an additional diagnostic clue: for the most sensitive ULP pairs, the AeST auxiliary fields `alpha_aest` and `E_aest` differ by nearly constant multiplicative factors from z=6 to z=0.2, while `phi+psi` is initially much closer and diverges mainly at later times. The ratio `alpha_aest/E_aest` is nearly unchanged between the paired solutions.

This suggests a discrete AeST amplitude/initialization or k-index-selection branch. It does not yet prove the source of the discontinuity.

## Question

Do adjacent representable k values select different multiplicative amplitudes of the AeST auxiliary sector already at the beginning of the raw perturbation history, while the matched-GR metric sector remains continuous?

## Frozen ULP pairs

Use four actual adjacent-binary64 pairs selected from the completed ULP audit. These span all three spectral windows and were fixed before the present full-history run.

1. k_h = 0.10125
   - bits A = 4589576883704929730
   - bits B = 4589576883704929731

2. k_h = 0.10250
   - bits A = 4589637531396803372
   - bits B = 4589637531396803373

3. k_h = 0.16500
   - bits A = 4592669915990485346
   - bits B = 4592669915990485347

4. k_h = 0.19750
   - bits A = 4593959187948552946
   - bits B = 4593959187948552947

All non-target `k_output_values` tokens remain exactly at the R3/direct 15-digit serialization. `P_k_max_h/Mpc=0.30` remains fixed. No memory term is enabled.

## Frozen runtime provenance

The run must use the same frozen CLASS/AeST runtime as the ULP audit:

- CLASS head `e85808324f51fc694d12e3ed7439552a3c3f9540`
- `source/aest_memory.c` SHA256 `4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f`
- `_MAX_NUMBER_OF_K_FILES_=64`
- `OMP_NUM_THREADS=1`

## Raw-history extraction

For each frozen pair and for AeST-on and matched-GR:

1. run the same target mode list used by the prior ULP audit;
2. select the same positional target history;
3. use the raw CLASS perturbation history rather than the sparse z interpolation;
4. identify the scale-factor array `a`;
5. construct a common log(a) grid of 1024 points over the overlap of the two histories;
6. interpolate only for pairwise comparison on this common grid.

Primary AeST fields:

- `alpha_aest` or fallback `alpha`;
- `E_aest` or fallback `E`;
- `phi`;
- `psi`;
- `W=phi+psi`.

Primary GR controls:

- `phi`;
- `psi`;
- `W=phi+psi`.

The implementation may additionally rank all common one-dimensional numeric history fields, but such ranking is diagnostic only and cannot alter the frozen gates.

## Multiplicative-amplitude diagnostic

For a field X on a pair (A,B), fit the scalar

    c_X = argmin_c ||X_B - c X_A||_2

on the common full-history grid.

Define the multiplicative residual

    r_X = ||X_B - c_X X_A||_2 / ||X_B||_2.

Define the first-point relative discrepancy

    q_X,first = |X_B-X_A| / max(|X_A|,|X_B|,tiny)

at the earliest common grid point.

Define matched-scale disagreement

    d_alphaE = |c_alpha-c_E| / max(|c_alpha|,|c_E|,tiny).

## Gates

### IA_G1 provenance and parent lock

Require:

- completed parent classification `FULLJ_CLASS_FRINGE_AEST_ULP_SENSITIVITY_CERTIFIED`;
- all parent ULP gates true;
- frozen runtime provenance exactly matches the values above;
- all four frozen bit pairs are present in the parent NPZ.

### IA_G2 matched-GR early continuity

For every pair require, at the earliest common history point,

    q_phi,first <= 1e-4,
    q_psi,first <= 1e-4,
    q_W,first   <= 1e-4.

Also require full-history relative L2 for matched-GR W <= 1e-5 for every pair.

### IA_G3 AeST auxiliary material difference at history start

For at least 3 of 4 pairs require both

    q_alpha,first >= 1e-2
    q_E,first     >= 1e-2.

### IA_G4 common multiplicative auxiliary branch

For at least 3 of 4 pairs require

    r_alpha <= 1e-3,
    r_E     <= 1e-3,
    d_alphaE <= 1e-3,

and at least one of

    |c_alpha-1| >= 1e-2
    |c_E-1|     >= 1e-2.

### IA_G5 metric response is delayed relative to auxiliary branch

For at least 3 of 4 pairs require

    q_W,first < min(q_alpha,first, q_E,first)/10.

This gate does not require W to remain small at late times.

## Classification priority

1. If IA_G1 fails:

   `FULLJ_AEST_ULP_INITIAL_AMPLITUDE_LOCALIZATION_INCOMPLETE`

2. If IA_G2 fails:

   `FULLJ_AEST_ULP_GENERIC_EARLY_HISTORY_DISCONTINUITY`

3. If IA_G2 passes and IA_G3-IA_G5 all pass:

   `FULLJ_AEST_ULP_AUXILIARY_AMPLITUDE_BRANCH_CERTIFIED`

4. If IA_G2 and IA_G3 pass but IA_G4 or IA_G5 fails:

   `FULLJ_AEST_ULP_AUXILIARY_EARLY_DIVERGENCE_MIXED`

5. Otherwise:

   `FULLJ_AEST_ULP_LATE_EVOLUTION_DIVERGENCE`

## Source-trace diagnostic

The runner will also save read-only source excerpts from the exact frozen CLASS tree for occurrences of:

- `k_output_values`
- `index_k_output`
- `alpha_aest`
- `E_aest`
- `alpha`
- initialization-related terms in `aest_memory.c` and `perturbations.c`.

These excerpts are diagnostic only. They do not determine the classification.

## Interpretation lock

A certified auxiliary amplitude branch means the ULP effect is already present in the AeST auxiliary sector at the beginning of the available perturbation history and is approximately a multiplicative amplitude selection. It would strongly disfavor a purely late-time unstable-mode explanation.

It would still not identify the exact source-code statement causing the branch and would not license a physical instability or new-physics claim.

Historical R3 remains unchanged. The next licensed step after certification is a source-level initialization/index audit targeted specifically at the AeST auxiliary amplitude path.