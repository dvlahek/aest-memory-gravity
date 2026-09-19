# NL1C7B4 Repair19b1 — pre-data orthonormal direct linear feasibility certification

## Status

Pre-data / pre-run diagnostic preregistration.

Repair19b is frozen as

`NL1C7B4_REPAIR19B_IMPLEMENTATION_FAIL`

at result-freeze commit

`cdc50f56d31f8a0007a80fe7fcaee98e687fe867`.

Frozen Repair19b result JSON:

- bytes: `33646`
- SHA-256:
  `d177394b45e19ac2bca739d4ff256694c5df65e9331276e3c1b1466f4fbe5929`.

Repair19b1 does not relabel Repair19b.

## Scientific question

Does the preregistered orthonormal Y4=0/Qmean=0 coordinate representation admit a direct linear correction with residual below the unchanged Repair19a threshold in all six canonical cases, and does that establish that Repair19a's LSMR result was an iterative-solver stagnation rather than a residual-space incompatibility?

This is a narrower residual-space question than Repair19b.

## Why Repair19b requires a separate repair

Repair19b required all chain and orth direct solves to report full reduced-column rank and required physical correction vectors to agree across coordinate bases and LAPACK drivers.

Those conditions are not invariant under numerical rank truncation of a near-singular operator.

The orthonormal basis was already preregistered before Repair19b as the conditioning-stable representation.

Repair19b1 therefore keeps:

- the same physical Y4=0/Qmean=0 subspace;
- the same residual;
- the same grouped two-point Jacobian;
- the same six cases;
- the same direct LAPACK drivers;
- the same `1e-6` linear-feasibility threshold.

It changes only the diagnostic question from numerical-vector/rank identity to residual-space feasibility in the predeclared orthonormal representation.

## Frozen domain

Exactly six canonical lambda=1 cases:

- eta=0
- Y=Simple
- beta=1
- scales=5,10,20 h^-1 Mpc
- Nr=256,512.

## Frozen orthonormal representation

Use exactly the Repair19a/Repair19b Helmert basis:

- first-four-node Helmert contrasts for the inner y_L constraint block;
- identity on remaining y_L coordinates;
- global Helmert mean-zero q_Rt basis.

Require:

- `G B_orth=0` to `1e-12`;
- `B_orth^T B_orth=I` to `1e-12`;
- condition number = 1 to abs-or-rel `1e-12`.

No chain-basis solve enters a science gate.

The frozen chain payload is reproduced only as a conditioning control.

## Frozen direct solvers

Recompute the same orth reduced matrix

`J_orth = J_x B_orth`

from the same grouped two-point Repair18a Jacobian.

Solve with both:

- SciPy `lstsq(..., lapack_driver='gelsd')`
- SciPy `lstsq(..., lapack_driver='gelsy')`

with

`cond=max(J_orth.shape)*eps_float64`.

No full-rank requirement is imposed.

Returned numerical rank is recorded descriptively.

## Frozen feasibility criterion

For every case and both direct drivers require:

`||F0 + J_orth dz||_2 / max(||F0||_2,tiny) <= 1e-6`.

This is exactly the Repair19a/Repair19b linear-feasibility threshold.

No nonlinear B4 threshold is changed or evaluated.

## Frozen gauge criterion

For every direct correction require:

- `|Y4| <= 1e-12`
- `|Qmean| <= 1e-12`.

## Frozen LSMR stagnation criterion

Use the frozen Repair19a orth-basis LSMR residual for the same case.

For both direct drivers require:

`r_LSMR / max(r_direct,tiny) >= 1e3`.

The ratio is residual-space only.

No physical correction-vector agreement is required.

## Frozen reproduction requirement

Repair19b1 must reproduce the frozen Repair19b orth payload before assigning a science PASS.

For every scale/grid/driver reproduce to abs-or-rel `1e-12`:

- initial residual L2;
- final residual L2;
- relative final residual;
- returned numerical rank;
- max |y_L|;
- max |q_Rt|;
- Y4 residual;
- Qmean residual.

## Gates

### R19B1_G1 — exact frozen provenance

Require exact hashes/classes for Repair19b and all imported parents.

Repair19b remains IMPLEMENTATION_FAIL.

### R19B1_G2 — exact orthonormal basis reproduction

Require exact frozen Repair19b orth basis audit at both grids.

### R19B1_G3 — exact Repair19b orth payload reproduction

Require all six cases and both direct drivers to reproduce the frozen Repair19b orth payload under the rule above.

### R19B1_G4 — finite direct orth solves

Require all 12 orth direct solves finite.

No numerical full-rank requirement.

### R19B1_G5 — orth direct residual-space feasibility

Require all 12 orth direct solves to satisfy the unchanged `1e-6` relative residual threshold.

### R19B1_G6 — exact gauge satisfaction

Require all 12 orth direct corrections to satisfy the frozen Y4/Qmean limits.

### R19B1_G7 — LSMR stagnation identified

Require the frozen Repair19a orth LSMR residual to exceed each corresponding direct residual by at least `1e3`.

### R19B1_G8 — chain conditioning control retained

Require exact reproduction of the frozen Repair19b chain basis condition numbers:

- Nr=256: `162.33598862000716`
- Nr=512: `325.3116790240505`.

No chain residual/rank/vector criterion is used for PASS.

### R19B1_G9 — claim boundary

Repair19b1 must not:

- run nonlinear least squares;
- evaluate or accept a nonlinear corrected state;
- write an NPZ;
- modify any parent state;
- change Y4/Qmean;
- add a physical field;
- alter sources, coefficients, signs, eta, branch, radial points, or historical thresholds;
- remove any case;
- run time evolution;
- make an observational claim;
- relabel Repair19, Repair19a, or Repair19b.

## Terminal classifications

If G1-G4, G6, G8, or G9 fail:

`NL1C7B4_REPAIR19B1_IMPLEMENTATION_FAIL`.

Else if G5 fails:

`NL1C7B4_REPAIR19B1_ORTHONORMAL_DIRECT_LINEAR_INFEASIBILITY`.

Else if G7 fails:

`NL1C7B4_REPAIR19B1_LSMR_STAGNATION_NOT_ESTABLISHED`.

Else:

`NL1C7B4_REPAIR19B1_ORTHONORMAL_DIRECT_LINEAR_FEASIBILITY_LSMR_STAGNATION_PASS`.

## Interpretation boundary

A PASS certifies only:

1. the same frozen gauge-fixed linearized problem is residual-space feasible in the orthonormal representation under both direct LAPACK drivers;
2. Repair19a's LSMR solve was grossly underconverged relative to those direct solves.

It does not certify nonlinear exact B4 closure.

Only after this certification may a separately preregistered nonlinear solver use the orthonormal gauge-fixed subspace and a deterministic direct rank-revealing Gauss-Newton/Newton step.
