# GE04 DY2 spectral convergence characterization — implementation lock

## Status

Implementation locked before first GE04 execution.

GE04 is a numerical characterization study of the already frozen GE03/NL1B2 cross-source.

It does not alter or relabel the frozen GE03 FAIL.

## Parent result

GE03 classification:

`GE03_WEAKLY_NONLINEAR_Y_MEMORY_CROSS_SOURCE_FAIL`.

GE03 frozen failure gate:

`Nx256_vs_Nx512_low_mode_DY2_relative_L2_max`.

Observed GE03 value:

`1.1665436252484428e-3`.

Frozen GE03 limit:

`5e-4`.

## Preregistration

Commit:

`248fdbe5ec381509363b52e33c536b683fb3ba3d`.

File:

`ge04/predata_dy2_spectral_convergence.json`.

Frozen blob:

`7d85c3374e6099a64a8869e0f4ca9d1e00df81ba`.

## Implementation

Commit:

`82e354f9a4fa791dcc00ece14d697a74c4ae216d`.

File:

`ge04/dy2_spectral_convergence.py`.

Frozen blob:

`c96812aca5d73b0fd0e61625b62c7022a4930a96`.

## Frozen science content

Same retained v0.77 artifact and GE03 field reconstruction.

Same:

- `chi10`;
- four-lambda consensus `chi11`;
- six signal-band modes;
- frozen phases;
- native `0.2<=z<=1.5` window;
- `beta0={1,0.5,0.1}`;
- exact NL1B2 directional derivative;
- FFT derivative;
- 2/3 nonlinear-flux dealiasing.

## Frozen resolution ladder

`N={128,256,512,1024,2048,4096}`.

Low-mode comparison:

`m=0..32`.

Reference resolution:

`N=4096`.

Pairwise errors:

`E_N=||DY2_N-DY2_2N||/max(||DY2_N||,||DY2_2N||)`.

Convergence fit:

`log E_N = c - p log N`

over

`N={256,512,1024,2048}`.

## Gates

Require:

- exact retained artifact provenance;
- requested-k mismatch <= `1e-12`;
- common native-grid mismatch <= `1e-12`;
- four-lambda chi11 relative-L2 affinity <= `5e-3`;
- four-lambda cosine >= `0.9999`;
- analytic versus finite-difference DY2 at N=4096 <= `1e-4`;
- beta0 scaling error <= `1e-12`;
- pairwise errors decrease monotonically from N=256;
- N1024 versus N2048 low-mode relative error <= `5e-4`;
- fitted convergence order `p>=0.5` for every native time and beta0;
- all outputs finite.

## Classification

Full characterization control:

`GE04_DY2_SPECTRAL_CONVERGENCE_PASS`.

Otherwise:

`GE04_DY2_SPECTRAL_CONVERGENCE_FAIL`.

## Claim boundary

GE04 can identify a numerically adequate representation for a later N2 state solve.

It cannot:

- relabel GE03;
- solve `Z21`;
- introduce finite eta;
- establish collapse, halo, lensing or observational claims.

## Anti-tuning

After this lock do not change:

- resolution ladder;
- low-mode range;
- convergence-fit definition;
- N1024/N2048 threshold;
- convergence-order threshold;
- field reconstruction;
- artifact;
- beta set;
- finite-difference step;
- numerical gates.
