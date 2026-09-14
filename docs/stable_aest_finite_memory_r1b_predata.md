# Stable AeST finite-memory R1b — matched-bath tangent pre-data declaration

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This declaration is fixed before any R1b run is inspected.

## Parent chain

The numerical host remains the certified stable-residual AeST implementation

    s = a theta/k^2 + alpha,
    chi = Q s,

with parent numerical milestone

    FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED.

The immediate physics parent is the completed R1 classification

    STABLE_AEST_FINITE_MEMORY_R1_ETA_SMOOTHNESS_FAIL.

R1 remains a historical FAIL and is not reclassified by R1b.

R1 established that the finite-bath extension is numerically regular and that the eta=0 memory-enabled system reproduces the memory-off host within its locked regression tolerance. Post-data inspection showed that the absolute finite-eta response measured against the memory-off run is of the same order as the solver offset induced by integrating the enlarged bath state vector. Therefore R1b tests the coupling response with a matched bath baseline at the same relaxation time.

## Question

After subtracting the matched `memory_enabled=yes, eta=0` solution at the same `tau H0`, does the stable AeST finite-bath sector exhibit a reproducible first-order Weyl response whose tangent is stable across eta and numerical tolerance, and whose tangent depends on the bath relaxation time?

R1b is a numerical/host-level memory certification test. It contains no likelihood, parameter fit, observational claim, permanent-elasticity-loss claim, or new-physics claim.

## Frozen physics

No physical source equation may be changed relative to R1.

Use the existing positive finite Drude bath with

    aest_memory_enabled = yes,
    aest_memory_order = 16,
    E_rhs -> E_rhs - Q B_chi/2,
    chi = Q s.

No new source patch is permitted.

## Anchors and redshifts

Use exactly

    k_h in {0.10000, 0.16500, 0.19750}

with the same direct/R3 serialized tokens as R1.

Use

    z = [6,5,4,3,2,1.5,1,0.5,0.2].

## Relaxation times and couplings

Use

    tau H0 in {1, 10}

and the existing R1 finite-coupling values

    eta in {0.0025, 0.005, 0.01}.

The primary R1 finite-eta histories at

    tol_perturbations_integration = 1e-7

are frozen parent data and must be reused rather than regenerated.

For R1b, obtain a matched eta=0 bath baseline at `1e-7` for each `(k,tau)`. The already existing R1 eta=0, tau=10 result may be reused only after exact metadata/provenance checks; tau=1 eta=0 must be generated.

For independent tight-tolerance confirmation, run only

    eta in {0, 0.01}

for both tau values at

    tol_perturbations_integration = 3e-8.

Thus the expensive full eta scan is not repeated at the tight tolerance.

## Matched-bath response

For each observable X define

    Delta^M_X(eta,tau) = X(eta,tau) - X(0,tau),

where both terms have `aest_memory_enabled=yes`, the same tau, order, k token, tolerance, and all other numerical settings.

For eta>0 define the vector tangent estimate

    Q_W(eta,tau) = Delta^M_W(eta,tau) / eta.

The normalization used in relative comparisons is always the larger L2 norm of the two compared vectors, with a tiny denominator guard.

## Primary eta-tangent consistency

At the primary tolerance `1e-7`, define for each `(k,tau)`

    E_25_50 = relL2(Q_W(0.0025,tau), Q_W(0.005,tau)),
    E_50_100 = relL2(Q_W(0.005,tau), Q_W(0.01,tau)).

This tests the response itself, not its offset from a memory-off solver trajectory.

## Tight-tolerance tangent confirmation

At eta=0.01 define

    Q_W^P(tau) = [W_1e-7(0.01,tau)-W_1e-7(0,tau)]/0.01,
    Q_W^T(tau) = [W_3e-8(0.01,tau)-W_3e-8(0,tau)]/0.01.

Define

    C_tol = relL2(Q_W^P, Q_W^T).

Also compute their cosine similarity when both tangent norms are nonzero.

## Relaxation-time dependence

At each k use the tight-tolerance eta=0.01 tangent estimates and define

    T_tau = relL2(Q_W^T(tau=10), Q_W^T(tau=1)).

This quantity compares matched-bath coupling tangents, not raw trajectories.

## Gates

### R1B-G1 provenance and parent lock

Require:

- this pre-data commit is an ancestor of HEAD;
- the parent R1 JSON exists and has classification `STABLE_AEST_FINITE_MEMORY_R1_ETA_SMOOTHNESS_FAIL`;
- the stable-host parent remains `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED`;
- the R1 post-data mechanism note is an ancestor;
- the R1 NPZ contains all frozen primary finite-eta histories required by this protocol;
- the stable source still contains `chi=Q*s` and the unchanged finite-bath closure;
- no new physical source patch is used.

### R1B-G2 matched eta=0 regularity

All new eta=0 matched-bath runs at both tolerances and both tau values must complete with finite W, delta_cdm, alpha, E, and s histories.

At the primary tolerance, the reused/generated eta=0, tau=10 trajectory must reproduce the R1 eta=0, tau=10 trajectory with W relL2 <= 2e-5 at every anchor.

### R1B-G3 primary eta-tangent consistency

Across the six `(k,tau)` cells require at least 5/6 cells to satisfy

    max(E_25_50, E_50_100) <= 0.05

and all six to satisfy

    max(E_25_50, E_50_100) <= 0.10.

### R1B-G4 tight-tolerance tangent reproducibility

For eta=0.01 require at least 5/6 `(k,tau)` cells to satisfy

    C_tol <= 0.10

and cosine similarity >= 0.99,

with all six satisfying

    C_tol <= 0.20

and cosine similarity >= 0.95.

If either tangent norm is numerically zero, the cell fails this gate.

### R1B-G5 nonzero matched coupling response

At eta=0.01 and tight tolerance require a finite, nonzero matched tangent norm at all six `(k,tau)` cells.

Additionally require the matched response amplitude relative to the matched eta=0 Weyl norm,

    A^M_W = ||Delta^M_W|| / max(||W(0,tau)||,tiny),

be >= 1e-12 in at least 4/6 cells.

This threshold is intentionally below the raw solver-offset scale because R1b tests paired differential reproducibility directly through G4.

### R1B-G6 relaxation-time dependence of the matched tangent

Using the tight-tolerance eta=0.01 tangents, require

    T_tau >= 0.02

for at least 2/3 k anchors.

The remaining anchor must be finite. This is the finite-relaxation gate.

## Classification priority

1. G1 fail: `STABLE_AEST_FINITE_MEMORY_R1B_INCOMPLETE`
2. G2 fail: `STABLE_AEST_FINITE_MEMORY_R1B_MATCHED_BASELINE_FAIL`
3. G3 fail: `STABLE_AEST_FINITE_MEMORY_R1B_ETA_TANGENT_FAIL`
4. G4 fail: `STABLE_AEST_FINITE_MEMORY_R1B_TOLERANCE_FAIL`
5. G5 fail: `STABLE_AEST_FINITE_MEMORY_R1B_RESPONSE_UNRESOLVED`
6. G6 fail: `STABLE_AEST_FINITE_MEMORY_R1B_RELAXATION_TIME_FAIL`
7. all pass: `STABLE_AEST_FINITE_MEMORY_R1B_MATCHED_TANGENT_CERTIFIED`

## Interpretation lock

A PASS establishes that the already-implemented finite-bath sector on the stable AeST host has a numerically reproducible matched-bath first-order Weyl response and that this response depends on the relaxation time.

A PASS licenses a later growth–Weyl memory comparison with the host-independent MCMG first-moment relation.

A PASS does not reclassify R1 or any historical AeST result and does not establish observational detection, permanent loss of elasticity, or new physics.
