# GE02 nonlinear elastic-source tau crossover — implementation lock

## Status

Implementation locked before the first GE02 execution.

GE02 is the first physics-first nonlinear continuation of the gravitational-elasticity interpretation.

It does not reopen or repair B4-B8.

## Theory provenance

Dependencies:

- `NL0B_COVARIANT_MEMORY_COMPLETION_PASS`;
- `NL1C4_EXPANDING_MEMORY_SOURCE_TRAJECTORY_PASS`.

The nonlinear source diagnostics are inherited unchanged from NL1C4:

`B_x=X-sum_j w_j partial_x z_j`

and

`rhohat_mem=(1/4) sum_j w_j [
 (partial_x z_{j,xi}/r_j)^2
 +(partial_x z_j-X)^2
]`.

The second quantity is quadratic in the finite-amplitude action variables and is the normalized eta-derivative coefficient of the direct metric-energy source on the finite reference.

## Frozen v0.77 reference

Workflow run:

`34315590099`.

Artifact ID:

`10090367181`.

Artifact digest:

`sha256:24b97e5738eb07be4f12d433ff5f9fe22249e199e186d5617aca5dc81f748378`.

Trace:

`v076_v077_base_trace.dat`.

No observational data are used.

## Preregistration

Commit:

`a4ad4d5a8e6bb38d23f5f6e937091b0ca030d105`.

File:

`ge02/predata_nonlinear_elastic_source_tau_crossover.json`.

Frozen blob:

`cc427e0c4941db75bd792c930fab851580bfae08`.

## Implementation

Commit:

`c809863aaed93490b48e652e3fea8057585561eb`.

File:

`ge02/nonlinear_elastic_source_tau_crossover.py`.

Frozen blob:

`52636cdb2e8a7d6ea31287052fc72292d859bd0e`.

The implementation imports the already frozen NL1C4 source calculator and changes only the global physical timescale `tauH0` between independently evaluated locked cases.

No NL1C4 equation or source definition is edited.

## Frozen tau grid

`tau H0={0.1,0.3,0.5,0.7,1.0,3.0,10.0}`.

Same analytic Maxwell crossover grid as GE01.

## Frozen finite-amplitude reference

- `k_h={0.03,0.05,0.08,0.10,0.15,0.20} h/Mpc`;
- exact integer modes `{3,5,8,10,15,20}`;
- fixed phases `{0.13,0.71,1.29,2.03,2.77,3.41}`;
- native times only;
- evaluation window `0.2<=z<=1.5`.

## Frozen numerical controls

Quadrature:

- control 512;
- primary 1024.

Spatial:

- Nx=256;
- Nx=512.

For every tau require:

- exact retained-artifact provenance;
- requested-k relative miss <= `1e-12`;
- common native-grid relative mismatch <= `1e-12`;
- at least eight native evaluation times;
- real-space X-rms reconstruction relative error <= `1e-10`;
- quadrature B-rms maximum pointwise relative difference <= `1e-2`;
- quadrature rhohat maximum pointwise relative difference <= `1e-2`;
- spatial B-rms maximum pointwise relative difference <= `5e-3`;
- spatial rhohat maximum pointwise relative difference <= `5e-3`;
- all outputs finite;
- B-rms positive at every evaluation time;
- rhohat positive at every evaluation time.

No monotonicity gate is imposed.

## Classification

Full control at all seven tau values:

`GE02_NONLINEAR_ELASTIC_SOURCE_TAU_CROSSOVER_PASS`.

Otherwise:

`GE02_NONLINEAR_ELASTIC_SOURCE_TAU_CROSSOVER_FAIL`.

## Claim boundary

GE02 is nonlinear at the finite-amplitude source/stress level.

It is not:

- a self-consistent finite-eta nonlinear evolution;
- a collapse trajectory;
- a halo prediction;
- a splashback prediction;
- an observational result.

Those stronger claims remain gated by later self-gravitating evolution.

## Anti-tuning

After this lock do not alter:

- tau grid;
- retained mode set;
- phases;
- quadrature orders;
- spatial resolutions;
- redshift window;
- action-source definitions;
- numerical gates.

Any later finite-eta evolution must be separately preregistered.
