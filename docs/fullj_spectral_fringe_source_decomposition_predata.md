# Pre-data: common-geometry spectral-fringe source decomposition

## Purpose

The interleaved same-geometry audit is formally classified

`FULLJ_STOCHASTIC_TAGGED_SPECTRAL_FRINGE_GEOMETRY_CERTIFIED`.

It established that the six parent/interleaved responses are invariant when rerun in the same `kF/h=0.00125`, `NX=1024` geometry as the nine source-localization nodes. Together with the preceding source-localization audit, the selected sharp responses are stable to timestep refinement, tag-amplitude refinement, same-k box doubling, and the exact saturated scalar-current surrogate.

The remaining mechanistic ambiguity is now source attribution. The tagged total Weyl response is

`T[W_total] = T[W_CLASS] + T[W_corr]`,

where `W_CLASS` is the corrected-CLASS Weyl field embedded with the same tagged basis and `W_corr` is the reconstructed effective-fluid/metric correction. The nine source-localization nodes already store both terms, but the six interleaved nodes do not. This audit fills only those missing component responses in the already certified common geometry.

No radial interpolation threshold is relaxed. No physical-fringe or observational claim is licensed by this diagnostic alone.

## Locked ancestry and local inputs

Required result locks:

- physical-k metric-projection repair PASS: `20151ab785e923de20d720f3fdd8890576b6cc05`
- quarter-lattice formal FAIL: `c1dd14b2d15fcd48519c328eb4906ef5d1b265b4`
- source-localization saturated-mode PASS: `86ab13ffa1048860731f65348074ede1b469c644`
- interleaved geometry certification: `73fb42d64e61d69820d31a9c9f71c8d536b2376e`

Frozen source-localization NPZ SHA256:

`f18aaa614fa72ccbb0e63a10e7bb49c51bd69b15e806ac7ba69e0f61b52ffa91`.

Frozen interleaved geometry NPZ SHA256:

`1a69f04e43a7e6837dead23a837ed40dcb46ed4e753f65a64abf7f4a4fdfce39`.

Gaussian coefficient SHA256 remains

`9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`.

## Frozen targets and geometry

Only the six interleaved nodes missing source decomposition are rerun:

`k/h = {0.1000, 0.1025, 0.1625, 0.1650, 0.1950, 0.1975}`.

Setup:

- `bg=0`
- `epsilon=0.05`
- both tag signs
- `NSTEP=4096`
- `kF/h=0.00125`
- `NX=1024`
- physical metric-projection cutoff `0 < |k|/h <= 0.32`
- reference nonlinear member `sigma=0`, `kind=simple`, `beta0=1.0`.

Total new integrations: `6 x 2 = 12`.

## Stored component responses

For each signed pair store the same components as the source-localization audit:

- `W_total`
- `W_CLASS`
- `W_corr`
- `delta_A`
- `Theta_A`
- `alpha`
- `chi`
- `P_chi`
- `S`
- `E`.

Merge the six new component responses with the nine locked source-localization nodes to form a 15-node common-geometry component profile in three five-point windows.

## Diagnostics

For each component and redshift, form the three within-window centered second differences

`D2 X_i = X_{i+1} - 2 X_i + X_{i-1}`

at the three interior points of each five-node window. The concatenated `D2` vector measures the sharp interleaved spectral structure without fitting a continuous interpolant.

At `z=0.2`, define

- `C_CLASS = corr(Re D2 W_CLASS, Re D2 W_total)`
- `E_CLASS = ||D2 W_total - D2 W_CLASS|| / max(||D2 W_total||, tiny)`
- `F_corr = ||D2 W_corr|| / max(||D2 W_total||, tiny)`.

The exact identity `D2 W_total = D2 W_CLASS + D2 W_corr` is also audited.

## Gates

### SD-G1 — provenance and frozen setup

Require all result locks, exact NPZ hashes, exact coefficient hash, physical-k repair active, exact six targets, and exactly 12 planned integrations.

### SD-G2 — numerical health and response reproduction

Require all 12/12 runs finite with

- canonical residual `<=1e-10`
- each metric-constraint residual `<=1e-8`
- broadband saturation `<=2e-2`.

The new `W_total` responses must reproduce the frozen interleaved-geometry NPZ with

- global relative L2 `<=1e-8`
- per-k relative L2 max `<=3e-8`.

### SD-G3 — decomposition identity

Require

- global relative residual of `T[W_total] - T[W_CLASS] - T[W_corr]` `<=1e-12`
- global relative residual of the corresponding merged `D2` identity `<=1e-12`.

### SD-G4 — source attribution at late time

This is a classification diagnostic, not a PASS/FAIL physics threshold.

Classify `CORRECTED_CLASS_LINEAR_SECTOR_DOMINATED` if all are true at `z=0.2`:

- `C_CLASS >= 0.95`
- `E_CLASS <= 0.30`
- `F_corr <= 0.30`.

Classify `INTERNAL_CORRECTION_REQUIRED` if numerical/provenance gates pass but the above three conditions are not all satisfied.

These thresholds are fixed before the missing six component responses are computed.

## Classification

If SD-G1 through SD-G3 pass and the SD-G4 corrected-CLASS conditions pass:

`FULLJ_SPECTRAL_FRINGE_SOURCE_DECOMPOSITION_CORRECTED_CLASS_LINEAR_SECTOR_DOMINATED`.

If SD-G1 through SD-G3 pass but the SD-G4 conditions do not all pass:

`FULLJ_SPECTRAL_FRINGE_SOURCE_DECOMPOSITION_INTERNAL_CORRECTION_REQUIRED`.

If provenance is valid but SD-G2 or SD-G3 fails:

`FULLJ_SPECTRAL_FRINGE_SOURCE_DECOMPOSITION_NUMERICAL_CONTROL_FAIL`.

If required provenance/input is missing:

`FULLJ_SPECTRAL_FRINGE_SOURCE_DECOMPOSITION_INCOMPLETE`.

## Decision after the audit

- If `CORRECTED_CLASS_LINEAR_SECTOR_DOMINATED`, do not call the fringes a nonlinear constitutive discovery. Audit the corrected-CLASS linear AeST sector directly in continuous k and compare against a GR/control calculation before assigning physical novelty.
- If `INTERNAL_CORRECTION_REQUIRED`, derive the Fourier-reduced saturated elastic mode and preregister held-out node/lobe predictions from the internal correction sector.
- In either case, do not resume blind radial grid halving.
