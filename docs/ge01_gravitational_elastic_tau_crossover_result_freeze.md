# GE01 gravitational elastic tau crossover — result freeze

## Status

Frozen first locked GE01 science execution.

Terminal classification:

`GE01_GRAVITATIONAL_ELASTIC_TAU_CROSSOVER_PASS`.

GitHub Actions run:

`35470092536`.

Execution HEAD:

`fbf0d9e67e985c45672a5d864aae15030c68acb4`.

Artifact:

- ID: `10593415777`;
- name: `results_bundle_ge01_gravitational_elastic_tau_crossover`;
- ZIP SHA-256:
  `2608ba2ad5b49f300ae65f214898071e21411e76ef68726d583c8344bad12ca8`.

## Frozen output hashes

Result JSON:

- bytes: `10087`;
- SHA-256:
  `efac42437ed2d1331e67d569861ac614391a03597f84961ff9530e514fb7df78`.

Result NPZ:

- bytes: `4129400`;
- SHA-256:
  `3420b2873c670b95e0d25bdd71bf74d7180a4580d156d74603e312ef8dfc9b40`.

## Gate result

Every preregistered numerical gate passes:

- all forcing-resolution controls pass;
- eta=0 baseline state is identical across tau values;
- both tangent amplitudes satisfy the locked linearity controls for every tau;
- all reported values are finite.

Thus GE01 is a valid theory-only tau-response map.

## Linear native-state response

For

`tau H0={0.1,0.3,0.5,0.7,1,3,10}`

the native total-matter tangent L2 norms are

`{10710.2565,14948.4037,16228.9262,16846.0198,17339.6919,18165.8660,18473.4932}`.

Relative to the historical `tau H0=10` response:

`{0.57976,0.80918,0.87850,0.91190,0.93863,0.98335,1.00000}`.

The response norm increases monotonically with tau.

The tangent shape is already extremely stable across tau:

- cosine to the tauH0=10 consensus is `0.9996386` even at tauH0=0.1;
- it exceeds `0.99999` by tauH0=1.

Thus tau mainly changes the amplitude of the trusted linear state direction over this window rather than rotating it strongly in native state space.

## Relation to the analytic Maxwell proxy

At H=H0, the simple local growing-mode proxy

`K=A/(1+A)`

with

`A=tau H0 sqrt[f(f+3)]`

predicts a relaxed-to-elastic crossover around `tau H0~0.5--1`.

The full CLASS/AeST response shows the same qualitative transition but reaches the historical plateau relatively quickly.

At `tau H0=1`, the native tangent norm is already

`0.93863`

of the tauH0=10 response.

At `tau H0=3`, it is

`0.98335`.

Therefore the historical tauH0=10 setting is indeed an almost saturated elastic-response control.

## Claim boundary

GE01 certifies a numerically controlled eta=0 native matter-state tangent map across the frozen tau grid.

It does not establish:

- finite physical eta;
- observational preference;
- a nonlinear evolution;
- halo/collapse effects;
- a likelihood result.

## Project interpretation

GE01 provides the linear state-level counterpart to GE02.

Together they show that both:

- the certified linear matter-state tangent;
- the finite-amplitude nonlinear action-source response;

move smoothly from the relaxed regime toward a common high-tau elastic plateau.

This supports the gravitational Maxwell-viscoelastic interpretation of the frozen NL0B memory sector without changing any historical classification.
