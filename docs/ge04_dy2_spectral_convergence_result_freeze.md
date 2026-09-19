# GE04 DY2 spectral convergence characterization — result freeze

## Status

Frozen first locked GE04 execution.

Terminal classification:

`GE04_DY2_SPECTRAL_CONVERGENCE_PASS`.

GitHub Actions run:

`35472879893`.

Execution HEAD:

`b6dc5faee233bf271e6b9c9f0f916ec4fe176e10`.

Artifact:

- ID: `10593716113`;
- name: `results_bundle_ge04_dy2_spectral_convergence`;
- ZIP SHA-256:
  `a62c4016ff5a4e66f725c67571574c2bfd4e66f86b625b5f71e5669f31235337`.

GE03 remains frozen FAIL. GE04 does not relabel it.

## Frozen output hashes

Result JSON:

- bytes: `27449`;
- SHA-256:
  `0982163624922ccdb870332ff6d7053be615a65facd2f29cd0ef8004ab2cb421`.

Result log:

- bytes: `27449`;
- SHA-256:
  `0982163624922ccdb870332ff6d7053be615a65facd2f29cd0ef8004ab2cb421`.

Result NPZ:

- bytes: `1911`;
- SHA-256:
  `5d533dcaceeba64e8d1b2d4ab0437e9cd0409fb577101761628a4a4ccf53a46e`.

Artifact metadata JSON:

- bytes: `835`;
- SHA-256:
  `78fc8a9c0f80359e3910525bd40596b6620fb9eadae2e79d6dfa4b77e0e9feac`.

## Gate result

Every preregistered GE04 gate passes:

- exact retained-artifact provenance;
- requested-k and common-native-grid matching;
- four-lambda `chi11` affinity;
- analytic versus finite-difference `DY2` at N=4096;
- exact beta0 scaling;
- monotone pairwise spatial convergence from N=256;
- N1024 versus N2048 low-mode error <= `5e-4`;
- fitted convergence order >= `0.5`;
- finite outputs;
- no GE03 relabel, finite eta or observational input.

## Convergence result

The maximum N1024 versus N2048 low-mode error over all native times and all beta0 values is

`1.7508778207505268e-5`.

This is almost thirty times smaller than the preregistered `5e-4` gate.

The minimum fitted convergence order over all native times and beta0 values is

`3.097139414077839`.

Thus the nonanalytic cross-source converges approximately third order over the frozen high-resolution ladder.

For beta0=1, representative pairwise errors are nearly time independent:

- N128 vs N256:
  `~1.4629e-2`;
- N256 vs N512:
  `~1.1665e-3`;
- N512 vs N1024:
  `~1.266e-4`;
- N1024 vs N2048:
  `~1.75e-5`;
- N2048 vs N4096:
  `~1.75e-6`.

Therefore the frozen GE03 failure is explained by an under-resolved 256/512 pair for the cusp/nonanalytic `|grad chi|` cross-source.

It is not evidence of a divergent or unstable `DY2` operator.

## Independent derivative control

At N=4096 the analytic directional derivative agrees with the centered finite-difference derivative with maximum relative L2 error

`2.4616604661582814e-9`.

The beta0 scaling error remains

`2.4424906541753446e-16`.

## Physical source pattern

The high-resolution source retains the descriptive GE03 geometry.

For beta0=1,

`||2 DY2||/||2 Y2||`

per unit eta tangent increases from approximately

`0.0148315`

at z=1.38524 to

`0.0972675`

at z=0.24762.

The source cosine remains extremely close to -1 throughout the window.

At the latest frozen native time:

`cos(Y2,DY2)=-0.9999999989431472`.

Thus the memory tangent acts predominantly as an opposing correction to the leading Y-sector nonlinear source on this reference.

This remains a source-level statement.

## Numerical representation decision

For any later N2 weakly nonlinear state solve using this cross-source, use:

- primary spatial representation: `N=1024`;
- control spatial representation: `N=2048`;
- same 2/3 nonlinear-flux dealiasing;
- same low-mode reporting convention.

This decision is now based on a separately preregistered convergence study, not on post-hoc relaxation of GE03.

## Project boundary

GE04 licenses use of the controlled high-resolution `DY2` source representation in a separately preregistered N2 / second-order physical-state eta-tangent calculation.

It does not:

- convert GE03 to PASS;
- solve `Z21`;
- introduce finite eta;
- certify nonlinear collapse;
- establish halo/lensing/observational predictions.
