# Pre-data declaration: stochastic tagged same-k box-doubling audit

## Purpose

The locked stochastic tagged power-lattice campaign completed the full `Delta k/h=0.005 Mpc^-1` power lattice and then tested preregistered half-lattice nodes in a doubled periodic box. The frozen power-lattice milestone failed only the half-lattice interpolation-accuracy and unresolved-spike gates; solver health, metric constraints, broadband saturation, tagged algebra, and B2->B4 background convergence all passed.

Because exact half-lattice representation requires changing the periodic embedding from `kF/h=0.005, NX=256` to `kF/h=0.0025, NX=512`, the observed half-lattice discrepancy is not yet uniquely attributable to finer radial structure. This bounded audit tests the same physical k modes in both embeddings before any finer radial continuum claim is made.

This is a pre-data declaration. Nodes, backgrounds, geometry, thresholds, and classification are fixed before the new doubled-box same-k results are inspected.

## Required locked ancestry

- evolving R2 bridge PASS: `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`
- Gaussian 1D stochastic ensemble PASS: `05e38b273f91eb04b7b4c8753731017d0ed839c1`
- 3D saturated closure PASS: `f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f`
- tagged-mode POC PASS: `aff670fa8551163f5cde2b5146e0e5840d53b424`
- response-kernel POC PASS: `2a5f884a50b7b30b90ddff01721914626dbde20f`
- power-lattice FAIL result: `b1a66aaa6e1a37919c8287908995ee2aea79eb4e`
- history addendum through power-lattice FAIL: `1edb8309fa978a1a832ca324ff8bf2dc0a6cc59d`

Historical FAIL/PASS classifications remain unchanged.

## Frozen setup

Physics/stochastic setup is unchanged:

- reference member: `sigma=0`, `kind=simple`, `beta0=1`
- Gaussian seed `20260912`
- coefficient SHA256 `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`
- backgrounds `B2={0,1}`
- symmetric tag amplitude `epsilon=0.05`
- redshifts `z={6,5,4,3,2,1.5,1,0.5,0.2}`
- `NSTEP=4096`
- triangular one-way R2 trajectory remains unchanged.

Locked reference responses are the B2 per-background Stage-A responses in `results/fullj_stochastic_tagged_power_lattice.npz` on geometry A:

- `kF_A/h=0.005 Mpc^-1`
- `NX_A=256`
- `box_A=2*pi/(kF_A*h)`.

Audit reruns use geometry B:

- `kF_B/h=0.0025 Mpc^-1`
- `NX_B=512`
- `box_B=2*pi/(kF_B*h)`.

The physical real-space spacing is identical between A and B.

## Frozen audit nodes

Use exactly eight shared lattice nodes:

`K_audit/h={0.030,0.060,0.095,0.100,0.120,0.160,0.195,0.200} Mpc^-1`.

These cover both boundaries, a low/mid control, the strongest late-time half-lattice failure region near `0.095-0.100`, the additional problematic region near `0.120`, the high-curvature region near `0.160`, and the high-k late-time region near `0.195-0.200`.

All eight are exact integer harmonics in both geometry A and geometry B.

Cost: `8 nodes x 2 backgrounds x 2 signs = 32` new R2 integrations, all on geometry B. Geometry-A references are reused immutably from the locked power-lattice NPZ.

## Comparison quantities

For every background, node, and redshift recover the symmetric tagged response in geometry B with the same normalization used in the locked tagged campaigns.

Compare new geometry-B response `T_B` with locked geometry-A response `T_A` at identical `(background,k,z)`.

Power is `P=|T|^2`.

Report:

- global response relative L2 over `B2 x K_audit x z`
- maximum per-k response relative L2
- maximum per-z response relative L2
- global power relative L2
- maximum per-k power relative L2
- maximum per-z power relative L2
- maximum pointwise symmetric relative response difference
- maximum pointwise symmetric relative power difference.

The pointwise symmetric relative difference is `|a-b|/max(|a|,|b|, floor)`, with floor `1e-12` times the global maximum magnitude of the corresponding locked quantity. This prevents zero crossings from producing meaningless ratios.

## Frozen gates

### BD-G1 provenance and identity

All required ancestry, coefficient hash, audit nodes, backgrounds, epsilon, NSTEP, and geometries must match this declaration exactly. The local locked power-lattice JSON must preserve classification `FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_FAIL`, with PL-G1 through PL-G5 true and PL-G6/PL-G7 false.

### BD-G2 solver/constraint health

All 32 new doubled-box runs finite. Across all new runs:

- canonical residual `<=1e-10`
- Hamiltonian, momentum and shear constraints each `<=1e-8`.

### BD-G3 broadband saturated closure

Across all new runs/checkpoints:

`epsilon_sat <= 2e-2`.

### BD-G4 same-k response invariance

Require:

- global response relative L2 `<=1e-4`
- maximum per-k response relative L2 `<=5e-4`
- maximum per-z response relative L2 `<=5e-4`
- maximum zero-safe pointwise response difference `<=2e-3`.

### BD-G5 same-k power invariance

Require:

- global power relative L2 `<=2e-4`
- maximum per-k power relative L2 `<=1e-3`
- maximum per-z power relative L2 `<=1e-3`
- maximum zero-safe pointwise power difference `<=4e-3`.

## Classification

PASS only if BD-G1 through BD-G5 all pass:

`FULLJ_STOCHASTIC_TAGGED_BOX_DOUBLING_AUDIT_PASS`.

Otherwise:

`FULLJ_STOCHASTIC_TAGGED_BOX_DOUBLING_AUDIT_FAIL`.

Use `INCOMPLETE` only if provenance/runtime/local locked artifacts prevent the frozen diagnostic from executing.

## Scope

A PASS licenses only:

- `STOCHASTIC_TAGGED_BOX_DOUBLING_INVARIANCE_TESTED=True`
- interpretation that the Stage-A/Stage-B box change is excluded as the source of the previously observed half-lattice power discrepancy within the tested bounded branch.

A PASS does not change the historical power-lattice FAIL and does not by itself license a continuous power spectrum.

If PASS, the next bounded step is a finer/adaptive radial power representation using the directly identified half-lattice structure. If FAIL, resolve periodic-embedding dependence before any radial-continuum refinement.

Keep false regardless of outcome:

- `STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED=False`
- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`.
