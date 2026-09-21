# Gravitational elasticity — nonlinear program

## Purpose

The nonlinear programme is retained, but it is reorganized so that each stage answers one physical question and does not depend prematurely on the blocked B4-B8 cosmological initial-data construction.

The active nonlinear hierarchy is

`nonlinear source -> weakly nonlinear state source -> nonlinear-background eta tangent -> finite eta -> collapse observables`.

## N0 — nonlinear source/stress response

Status: **PASS**.

Dependencies:

- NL0B covariant memory completion PASS;
- NL1C4 expanding action-source trajectory PASS;
- GE02 nonlinear elastic-source tau crossover PASS.

Objects:

- restoring source `B_x`;
- quadratic direct metric-energy coefficient `rhohat_mem`.

Result:

Both increase smoothly from the relaxed regime toward the unrelaxed elastic plateau across the preregistered Maxwell tau grid.

This establishes nonlinear finite-amplitude source physics, but not state backreaction.

## N1 — weakly nonlinear Y-memory cross-source

Target:

`DY2[chi10;chi11]`.

Theory dependency:

`NL1B2_DIRECTIONAL_SECOND_ORDER_ETA_TANGENT_PASS`.

For

`g=grad_phys chi10`

and

`h=grad_phys chi11`,

`DY2 = C_beta div_phys[ |g| h + (g.h/|g|) g ]`

with the bracket set continuously to zero where `|g|=0`.

This is the first direct nonlinear coupling between

- the baseline AeST/MOND Y nonlinearity;
- the certified linear elastic-memory tangent.

Required controls:

1. reconstruct `chi10` and `chi11` from common native accepted-source traces;
2. verify `chi11` lambda affinity;
3. verify the analytic DY2 expression against centered finite differences of the already certified NL1A operator;
4. use two spatial resolutions and 2/3 dealiasing;
5. retain all three co-primary `beta0={1,0.5,0.1}`;
6. no finite eta.

A PASS establishes a controlled weakly nonlinear physical source entering the exact `Z21` hierarchy.

## N2 — second-order physical-state eta tangent

**Current prerequisite status (GE19, 2026-09-21): BLOCKED ON BASELINE Z20 CONSTRAINT CERTIFICATION.**

The prerequisite memory-off hierarchy is now much more advanced than the original programme text:

- Repair13 certifies the self-consistent reduced background and H1/Z10 parent;
- Repair14 constructs the first reduced H3/Z20 particular candidate but fails the second-order shift constraint;
- Repair15 excludes the zero-dynamic-velocity initial convention;
- Repair16 excludes canonical y0=0 as an admissible forced initial state;
- Repair17 certifies existence of the full canonical initial constraint manifold in 714/714 material cases;
- Repair18 certifies a unique reproducible zero-coordinate projected-momentum finite-window boundary in 714/714 material cases;
- Repair19 is locked and ready to rerun H3/Z20 with that boundary and the original Stage-B gates.

Therefore the immediate N2 blocker is **not** source generation, initial-manifold existence or boundary selection. Repair18 closes the boundary problem. The remaining prerequisite is Repair19 H3 propagation itself: the baseline memory-off second-order state `Z20` must satisfy the unchanged propagation, shift, anisotropy and time-grid gates.

No `q20` or `Z21` solve is licensed until a separately frozen H3 run satisfies the unchanged second-order constraint gates.

Persistent GE19 chronology:

`docs/ge19_history.md`.

Target:

`Z21 = partial_eta Z^(2)|_eta=0`.

Frozen equation:

`L Z21 =
 -2 Q(Z10,Z11)
 -2 DY2[Z10;Z11]
 -M1[Z20,q20]
 -M2[(Z10,q10),(Z10,q10)]`.

This is the first stage at which the nonlinear physical state itself, rather than only a source block, is solved.

No finite eta is introduced.

Implementation requirements:

- all source blocks generated from the frozen action;
- independent scalar constraint residual;
- v0.77 first-order tangent recovered when nonlinear sources are disabled;
- NL1A Y operator and N1 DY2 controls re-executed;
- fixed native-state representation, avoiding the historical off-native interpolation ambiguity.

## N3 — nonlinear-background eta tangent

Target:

Given a finite-amplitude memory-off solution `Z0`,

`D E0[Z0] Z_eta = -M[Z0,q0]`.

This is the appropriate first self-consistent strong-nonlinear memory result.

It requires a genuine nonlinear memory-off trajectory.

The existing NL1C6 result provides:

- spherical variational closure;
- retained Hamiltonian and momentum constraints;
- a nonsingular gauge-fixed principal evolution block;
- local solver readiness.

It does not provide the required nonlinear trajectory by itself.

Therefore N3 must not use the NL1C4 finite-amplitude reconstruction as if it were an exact nonlinear solution.

## N4 — finite physical eta

Only after N2/N3 numerical control is established may finite eta be introduced.

Required finite-eta checks:

- eta->0 tangent convergence;
- sign symmetry / small-eta linearity;
- constraint convergence;
- resolution convergence;
- energy and source consistency from the same action;
- no parameter selection using observational outcome.

## N5 — nonlinear observables

Only after finite-eta evolution is controlled:

- collapse time;
- turnaround radius;
- infall velocity;
- splashback radius;
- potential/lensing response;
- halo-scale profile changes.

These are later observables, not current claims.

## Relation to B4-B8

B4-B8 tested one specific route from a CLASS-derived cosmological slice to a fully nonlinear spherical constraint state.

That route is frozen as blocked/failed.

It is not the active definition of nonlinear gravitational elasticity.

The nonlinear programme above can proceed through N1/N2 without solving B4-B8.

A future N3/N4 spherical-collapse calculation will require a valid nonlinear memory-off trajectory and consistent initial data, but by then the physically relevant source structure and tau regime will already be known.

## Decision rule

Do not advance a stage because a solver can be written.

Advance only when the previous stage establishes the physical source/state object that the next stage needs.
