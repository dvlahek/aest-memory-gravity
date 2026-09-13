# Pre-data: interleaved same-geometry spectral-fringe audit

## Purpose

The preregistered source-localization audit is classified

`FULLJ_STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_SATURATED_MODE_SUPPORTED`.

Time-step, tag-amplitude and same-k doubled-box controls all pass, and the exact saturated scalar-current surrogate reproduces the local tagged response at approximately `1e-7` power accuracy. The candidate sharp structure is therefore stable at the tested center wavenumbers and does not require the small residual nonlinear constitutive term.

A remaining confound must be removed before interpreting the earlier power spikes as spectral node/lobe structure: the strongest apparent spikes were defined by interleaving quarter-offset points computed in `kF/h=0.00125, NX=1024` with parent `0.0025`/`0.005` points inherited from coarser geometries. The present audit reruns the parent near-node wavenumbers in the same quarter-grid geometry. It is a same-physical-k geometry certification, not another radial-refinement campaign.

No historical FAIL is reclassified and no observational scope is licensed.

## Locked ancestry

- physical-k metric-projection repair PASS result: `20151ab785e923de20d720f3fdd8890576b6cc05`
- repaired power-lattice regression FAIL result: `9f5218629901643574373e32c84d137c9cda2494`
- quarter-lattice FAIL result: `c1dd14b2d15fcd48519c328eb4906ef5d1b265b4`
- spike source-localization implementation/runner ancestry through `a1b7305cef99f5a61a2af49101cc875a5de0fdc3`
- spectral-fringe working-hypothesis note: `1dcafa0643fa99e5de527dcb4a66589814ec6301`
- source-localization formal result lock: `86ab13ffa1048860731f65348074ede1b469c644`

Frozen result hashes:

- source-localization NPZ SHA256: `f18aaa614fa72ccbb0e63a10e7bb49c51bd69b15e806ac7ba69e0f61b52ffa91`
- repaired-regression NPZ SHA256: `83fb7462ec970bfef953e3804d11a81fd5843745347fe77c318c9e39b8e6e82d`
- Gaussian coefficient SHA256: `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`

## Frozen same-k targets

Six parent near-node wavenumbers are selected because they are the coarse-grid neighbors that defined the strongest earlier apparent spike/node contrasts:

- W1: `{0.1000, 0.1025}`
- W2: `{0.1625, 0.1650}`
- W3: `{0.1950, 0.1975}`

All six are exact Fourier modes in the common geometry

- `kF/h = 0.00125`
- `NX = 1024`
- `NSTEP = 4096`
- `epsilon = 0.05`
- physical metric-projection cutoff `0 < |k|/h <= 0.32`.

Only frozen Gaussian background `bg=0` is used. The completed quarter and source-localization audits already show negligible B0/B1 dependence, so this is not a stochastic-convergence test.

Both tag signs are run. Total new integrations: `6 x 2 = 12`.

## Frozen reference response

For each physical target `k`, the reference response is the already locked repaired parent response from `fullj_stochastic_tagged_power_lattice_kmask_regression.npz`:

- use `response_hybrid_B2[bg=0]` for nodes on the `0.005` lattice;
- use `response_half_new[bg=0]` for nodes on the selected `0.0025` half lattice.

No interpolation is used in this audit. Every comparison is direct at identical physical `k`.

## Gates

### IG-G1 — provenance and exact setup

Require all locked ancestry, exact NPZ hashes, exact Gaussian coefficient hash, validated physical-k mask with original-R2 identity, exact six targets, exact common geometry, and exactly 12 planned integrations.

### IG-G2 — numerical health

Require all 12/12 runs finite, canonical residual `<=1e-10`, Hamiltonian/momentum/shear residuals each `<=1e-8`, and broadband saturation `<=2e-2`.

### IG-G3 — same-k interleaved geometry invariance

Compare the new common-geometry tagged response with the frozen repaired parent response at the same six physical `k` values. Require

- tagged-response global relative L2 `<=1e-4`,
- tagged-power global relative L2 `<=2e-4`,
- per-k tagged-response relative L2 max `<=3e-4`.

These are the same same-k tolerances used in the source-localization doubled-box control.

### IG-G4 — common-geometry profile construction

Require that the new six responses and the already locked nine quarter-offset source-localization responses are all finite and can be merged into the exact 15-node local profile without duplicate/ambiguous physical `k` values.

The detailed node/lobe pattern is stored descriptively and is not itself a preregistered PASS criterion because these windows were selected post hoc from the previously observed structure.

## Classification

If IG-G1 through IG-G4 all pass, classify

`FULLJ_STOCHASTIC_TAGGED_SPECTRAL_FRINGE_GEOMETRY_CERTIFIED`.

If provenance is valid but IG-G2 or IG-G3 fails, classify

`FULLJ_STOCHASTIC_TAGGED_SPECTRAL_FRINGE_GEOMETRY_FAIL`.

If frozen inputs are incomplete, classify

`FULLJ_STOCHASTIC_TAGGED_SPECTRAL_FRINGE_GEOMETRY_INCOMPLETE`.

A PASS certifies only that the interleaved local signed-transfer profile is not an artifact of mixing the tested box geometries. It does not yet establish a physical dispersion law, continuous power, lensing, ACT use, or an observational claim.

## Decision after PASS

A PASS ends geometry forensics for these local windows. The next milestone is not further real-space grid halving. It is a Fourier-reduced saturated elastic-mode solver with arbitrary continuous `k`, followed by preregistered held-out predictions of signed-transfer node/lobe locations against the full tagged solver.
