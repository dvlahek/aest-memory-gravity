# GE02 nonlinear elastic-source tau crossover — result freeze

## Status

Frozen first locked GE02 execution.

Terminal classification:

`GE02_NONLINEAR_ELASTIC_SOURCE_TAU_CROSSOVER_PASS`.

GitHub Actions run:

`35470926045`.

Execution head:

`318e9167a64140ab2fe6c111c40aff7f44d64db0`.

Artifact:

- ID: `10592418646`;
- name: `results_bundle_ge02_nonlinear_elastic_source_tau_crossover`;
- ZIP SHA-256:
  `61c72e6cd66fc27427f15fbe7d0c9e1410096b82b99ebcd8368194f8348bc100`.

## Frozen output hashes

Result JSON:

- bytes: `10325`;
- SHA-256:
  `4fe77a183b9a45891446b53fa4afbdded0c8145d75f3acf4db7a6e033fa520d0`.

Result log:

- bytes: `10325`;
- SHA-256:
  `4fe77a183b9a45891446b53fa4afbdded0c8145d75f3acf4db7a6e033fa520d0`.

Result NPZ:

- bytes: `2126`;
- SHA-256:
  `94d650d24382ff025b79e33bc0e34d965c765a7bd8b0425fed1df4aa3cf76a6f`.

Artifact metadata JSON:

- bytes: `835`;
- SHA-256:
  `78fc8a9c0f80359e3910525bd40596b6620fb9eadae2e79d6dfa4b77e0e9feac`.

## Gate result

Every locked GE02 gate passes:

- retained v0.77 artifact digest exact;
- all six k modes exact to the frozen tolerance;
- common native grid exact;
- all seven tau cases pass the NL1C4 numerical/action-source controls;
- all reported quantities finite;
- no finite eta, observation, likelihood, halo or collapse input.

The native history has 24 points and the requested-k and common-grid mismatches are both exactly zero.

## Nonlinear action-source result

The action-derived restoring-force norm increases monotonically over the preregistered tau grid.

For

`tau H0={0.1,0.3,0.5,0.7,1,3,10}`

the time-window L2 norms of `B_rms` are

`{7.82151e-20, 1.39385e-19, 1.62989e-19, 1.75317e-19, 1.85645e-19, 2.03880e-19, 2.10976e-19}`.

Relative to the historical `tau H0=10` response, these are

`{0.37073,0.66067,0.77255,0.83098,0.87993,0.96637,1.00000}`.

Thus most of the transition from relaxed to unrelaxed response occurs below `tau H0~1`, and `tau H0=3` is already close to the unrelaxed plateau.

## Quadratic elastic-energy source

The action-derived finite-amplitude metric-energy coefficient

`rhohat_mem=(1/4) sum_j w_j[(partial_x z_{j,xi}/r_j)^2+(partial_x z_j-X)^2]`

also increases monotonically over the preregistered tau grid.

Its time-window L2 norms are

`{1.89202e-39, 3.52362e-39, 4.18795e-39, 4.54303e-39, 4.84485e-39, 5.38773e-39, 5.60245e-39}`.

Relative to the historical `tau H0=10` case:

`{0.33771,0.62894,0.74752,0.81090,0.86477,0.96167,1.00000}`.

The peak of `rhohat_mem` occurs at the latest frozen native evaluation time in every tau case,

`z=0.24761975466101416`.

This is descriptive and is not used as a gate.

## Numerical controls

The real-space X-rms reconstruction error is

`3.15197e-16`

for every tau case.

Worst quadrature and spatial controls remain far inside their frozen gates.

Across all seven tau values:

- B-rms quadrature mismatch is at most `1.22578e-5` against a `1e-2` limit;
- rhohat quadrature mismatch is at most `1.63531e-7` against a `1e-2` limit;
- B-rms spatial mismatch is below `4.70e-16` against a `5e-3` limit;
- rhohat spatial mismatch is below `8.37e-16` against a `5e-3` limit.

## Physical interpretation

GE02 establishes that the already certified NL0B finite-amplitude action sources show a smooth Maxwell-like timescale transition.

The nonlinear restoring-force source and the quadratic stored-energy source are both substantially suppressed in the relaxed `tau H0<<1` regime and approach a common unrelaxed plateau as tau increases.

The historical `tau H0=10` choice therefore probes an almost saturated elastic regime, not the primary relaxation crossover.

This provides a nonlinear source-level counterpart to the analytic Maxwell interpretation.

## Claim boundary

GE02 is nonlinear at the finite-amplitude source/stress level.

It does not establish:

- a self-consistent finite-eta nonlinear trajectory;
- a collapse or turnaround prediction;
- a halo/splashback observable;
- an observational detection.

Those stronger claims require the memory source to backreact on the nonlinear physical state.

## Licensed continuation

GE02 licenses a separately preregistered **nonlinear-background eta-tangent response**.

The target should solve the linearized physical equations about a finite-amplitude nonlinear memory-off reference,

`D E0[Z0] Z_eta = -M[Z0,q0]`,

using the action-derived source blocks already certified by NL1C3A/NL1C5/NL1C6.

The continuation must not introduce finite physical eta before the nonlinear-background tangent is numerically controlled.
