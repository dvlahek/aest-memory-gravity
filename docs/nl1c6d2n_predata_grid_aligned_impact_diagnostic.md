# NL1C6D2N pre-data: grid-aligned old-vs-corrected impact diagnostic

## Purpose

The first no-refit old-vs-corrected comparison is descriptive and directly compares transfer arrays. The two CLASS runs have identical array shapes but slightly different native transfer grids (`k_native_h` and `z_native`), so direct element-wise transfer-field L2 differences are not accepted as physical impact estimates.

This diagnostic is frozen before any grid-aligned transfer result is evaluated.

## Frozen inputs

- Historical factor-2 Exp normalization, regenerated from the same pinned CLASS commit and patch stack.
- Corrected Exp normalization on branch `v053-exp-normalization-corrected`.
- Identical cosmological and AeST parameters; no refit.
- Memory disabled and `eta=0`.
- Existing NPZ exports from the same workflow run.

## Alignment rule

For each transfer field `d_b`, `t_b`, `d_m`, `phi`, and `psi`:

1. Detect whether the stored transfer array is `(nk,nz)` or `(nz,nk)` from the lengths of `k_native_h` and `z_native`; no guessed orientation is allowed.
2. Sort each model's k and z axes monotonically.
3. Restrict to the common rectangular domain in k and z.
4. Restrict redshift further to `0.2 <= z <= 6.0`.
5. Bilinearly interpolate the historical field to the corrected grid points inside the common domain and compute relative L2.
6. Independently bilinearly interpolate the corrected field to the historical grid points in the same common domain and compute relative L2.
7. Report both directional values and the conservative symmetric value `max(old_to_corrected, corrected_to_old)`.

No similarity PASS/FAIL threshold is defined. The result is descriptive only.

## Controls

- Interpolation is linear (`scipy.interpolate.RegularGridInterpolator`) with no extrapolation.
- The number of common k and z samples must each be at least 8, otherwise the diagnostic aborts.
- Background H and rho and CMB TT/TE/EE values from the previous comparison are retained as directly comparable controls; they are not reinterpreted by the grid alignment.
- Historical results remain historical; this diagnostic does not reclassify prior runs.
- No cosmological refit, memory, likelihood, nonlinear branch selection, or NL1C7 is performed.

## Interpretation

Only the grid-aligned transfer metrics may be used to decide which cosmology-dependent stages require rerunning. The prior raw element-wise transfer metrics remain recorded but are not used for that decision.
