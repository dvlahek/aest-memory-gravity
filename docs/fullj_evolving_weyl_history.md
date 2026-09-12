# Full-J evolving Weyl project history — locked chain through stochastic tagged-mode POC

This file records the active reproducibility chain for the evolving-Weyl branch. It is intentionally chronological and preserves all historical PASS/FAIL classifications. No historical result is reinterpreted here.

## Static/full-J foundation

- Full-J phase robustness PASS: `741894f68fd498f924869cfd6e7a1274237abf9c`.
- Full-J Jacobian/node-coupling line: result lock ancestor `8b6655d...` and static Weyl closure result `d0701d...`.
- Static fixed-a identity `W=2 Phi` was validated only in its static scope.
- Local static Weyl covariance result: `e01ed934...`.

## Evolving FLRW Weyl bridge

- Evolving bridge pre-data: `b98d30ae88b6f1e63c9ba79f6813a98786d9caea`.
- R1B Euler identity PASS: `6e3f8735712c3bb21eab5578e08c13f27d604ba0`.
- R2 pre-data: `d59529f429719ab29fdd24669e9a4f27dfa54388`.
- R2 implementation chain: `67e0aee157bdffa3fef52f4b4c32e905893098e4`, runner head `970b5fd1612e52aa3adff98d6d0b0a6084a40cf7`.
- Locked evolving R2 bridge PASS: `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`.

R2 established an action-derived one-way/triangular evolving Weyl reconstruction with direct evolution of `(delta_A,Theta_A)`, linear CLASS agreement at a few `1e-6`, static full-J recovery, and machine-precision metric constraints. Canonical nonlinear trajectories remain externally forced by the corrected CLASS metric and do not receive reconstructed nonlinear metric feedback.

## Deterministic and stochastic covariance line

- Deterministic evolving covariance diagnostic corrected lock: `87434c21866241b1b35588ec88e93e99a6f5db1` — PASS as a completion-sensitivity diagnostic, not a cosmological ensemble.
- Gaussian 1D stochastic ensemble pre-data: `ad0b42694183d71b3ea1cab1eb1775c6456268c6`.
- Gaussian 1D stochastic ensemble result PASS: `05e38b273f91eb04b7b4c8753731017d0ed839c1`.
- Frozen Gaussian coefficient seed: `20260912`.
- Frozen coefficient SHA256: `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`.

## 3D geometry and constitutive closure

- 3D lattice-shell geometry POC result PASS: `ca6a102196055e27dc2b31379285bfc7aea1a35b`.
- 3D saturated constitutive closure result PASS: `f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f`.
- The central stochastic/broadband branch validated the saturated approximation `div[(1+j) grad chi] ~= 2 lap chi` to high precision in the tested regime.

## Isotropic transfer nodes and zero-safe phase audit

- Historical six-node transfer result FAIL: `b7bb0aef90ec935821f4dc1a63db0d79966a15f8`, caused only by the original local relative-imaginary metric near a transfer zero.
- R1 zero-safe phase audit PASS: `20679c5274e936037c226904d40c9d6779b00a49`.
- This licensed the six direct isotropic transfer/power nodes and real-transfer projection, but not a continuous radial power spectrum.

## Dense radial isolated-mode campaigns

### Original total-transfer interpolation

- Pre-data: `82cfb13a782aea71e0a8e3a7433f9729f47c048a`.
- Implementation: `eb36597fc4e9955cb13694b0a9ec1af1c9fd42ed` plus technical runtime repairs.
- Locked result FAIL: `55495cc968082f1cf6638785f7609c787971835c`.

Direct 21-node R2 solutions were finite, constraint-clean and phase-clean, but PCHIP interpolation of the full signed transfer did not satisfy holdout/refinement convergence, especially at low redshift around radial zero/oscillation structure.

### CLASS-residual interpolation

- Pre-data: `3aada0bdcd350f58ddcdf37aa45c4a8a574cb1db`.
- Implementation: `f1df593128110510478ae54fe9c6179e1c33dc42`.
- Runtime/provenance and dense-k64 infrastructure culminated in runner head `c113cda37a79c68dc78ba1f32e8ed3a3926e1bba` before the completed science run.
- Locked completed residual-R2 result FAIL: `4d87865a8e45985388dfab2b9d8922faa9290f7f`.

The residual construction improved observable power accuracy substantially, but the frozen milestone still failed because: (i) two low-k isolated single-mode holdouts left the saturated constitutive regime, (ii) transfer holdout error slightly exceeded its 3% gate, and (iii) refinement of the isolated-mode residual transfer was not monotonic. Total tagged/observable-like power quantities were substantially more stable than the signed isolated transfer.

## Same-environment cardinality audit

- Pre-data: `76d2b923935278317022ab6ef5d036769b91500b`.
- Implementation: `6e179e7eacb0adbc4857a2efe2664c2a34e560c3`.
- Runner: `806c7f350579fd0f4040676b9ff2ba06c6abed54`.
- Locked PASS: `df182a828b3c140fba22f1f5d58414ec41017e7b`.

Six old K2 nodes rerun inside the same 41-history dense-k64 CLASS environment reproduced the 21-history results exactly to stored precision: transfer, power, CLASS reference and saturation differences were all zero. This excludes 21-versus-41 CLASS history cardinality/state plumbing as the source of the jagged isolated-mode radial structure.

## Stochastic-background tagged-mode POC

- Pre-data: `bb478329717575e7e6f73096b0e9c00930b2cd87`.
- Implementation: `0ca032c90e86ae84134e9cb61333ba203f707430`.
- Runner: `8f70d2adec2391a9b8637548dd77c36a3f46a635`.
- Locked PASS: `aff670fa8551163f5cde2b5146e0e5840d53b424`.

Frozen setup: three Gaussian backgrounds (`0,1,2`), targets `k/h={0.0375,0.10,0.175} Mpc^-1`, symmetric amplitudes `epsilon={0.10,0.05}`, both signs, 36 nonlinear R2 integrations.

Main result:

- 36/36 runs finite and constraint-clean.
- `broadband_saturation_max = 4.731066674148239e-05`.
- `epsilon_consistency_median = 5.214054686491488e-15`.
- `epsilon_consistency_max = 1.2944515507279873e-08`.
- `primary_max_scatter_over_rms = 8.793934553894611e-07`.
- `tagged_power_identity_relative_residual = 7.646310444953125e-21`.

The previously anomalous isolated `k/h=0.0375` node, with isolated-mode saturation residual near `0.20`, is deeply saturated on all three broadband Gaussian backgrounds at roughly `4.1e-05` to `4.4e-05`. The symmetric tagged response is effectively invariant under halving epsilon.

Interpretation lock: the isolated finite-amplitude single-mode transfer is not an adequate nonlinear continuum object. The physically motivated next object is the directional tangent/tagged response around a broadband stochastic background.

## Current scope after the tagged POC

True/tested:

- `STOCHASTIC_BROADBAND_TAGGED_RESPONSE_POC_TESTED=True`
- `STOCHASTIC_BROADBAND_LOWK_SATURATION_TESTED=True`
- dense CLASS cardinality artefact excluded.

Still false/unlicensed:

- `STOCHASTIC_TAGGED_RADIAL_CONTINUUM_LICENSED=False`
- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

## Next milestone

The next bounded milestone is a preregistered stochastic tagged radial convergence campaign over `0.03 <= k/h <= 0.20 Mpc^-1`, using common-random Gaussian backgrounds and symmetric tagging, with explicit radial refinement, background convergence, saturation, phase, solver and tagged-power gates. Only a PASS of that milestone may license a bounded tagged radial continuum for subsequent Weyl-power/LOS work.