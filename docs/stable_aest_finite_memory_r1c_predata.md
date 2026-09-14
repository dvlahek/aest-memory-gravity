# Stable AeST finite-memory R1c — long-relaxation held-out certification

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This declaration is fixed before any R1c result is inspected.

## Parent chain

The numerical host remains the certified stable-residual AeST implementation with

    s = a theta/k^2 + alpha,
    chi = Q s,

and numerical parent

    FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED.

The immediate physics parent is

    STABLE_AEST_FINITE_MEMORY_R1B_ETA_TANGENT_FAIL.

R1b remains a historical FAIL. Its post-data result showed a clean split: all three tau H0=10 cells had eta-tangent consistency and tight-tolerance reproducibility, while all three tau H0=1 cells did not. R1c tests only the numerically resolved long-relaxation regime and does not reclassify tau H0=1.

## Question

Does the matched-bath first-order Weyl memory tangent at tau H0=10 generalize to held-out k anchors and remain consistent under an independent positive-bath discretization?

## Frozen physics and numerics

No physical source equation may be changed relative to R1/R1b.

Use the existing positive finite Drude bath with

    aest_memory_enabled = yes,
    tau H0 = 10,
    chi = Q s,
    E_rhs -> E_rhs - Q B_chi/2.

Fix

    tol_perturbations_integration = 3e-8.

Use two existing bath orders:

    aest_memory_order in {16,20}.

No solver, cosmological, initial-condition, k-serialization, or observable-extractor setting may otherwise change.

## Held-out anchors

Use exactly

    k_h in {0.09875, 0.16125, 0.19500}.

These were not the three primary R1b anchors and therefore act as held-out scale tests.

## Couplings

For each k and bath order run

    eta in {0, 0.005, 0.01}.

The matched response is

    Delta^M_W(eta;order) = W(eta;order)-W(0;order),

and tangent estimate

    Q_W(eta;order) = Delta^M_W(eta;order)/eta.

## Metrics

For each k and order define eta-linearity

    E_eta = relL2(Q_W(0.005), Q_W(0.01)).

For each k at eta=0.01 define bath-order agreement

    E_order = relL2(Q_W(order=16), Q_W(order=20)),

and cosine similarity between those tangent vectors.

Define matched response amplitude

    A^M_W = ||Delta^M_W(0.01)|| / max(||W(0)||,tiny).

All retained observables W, delta_cdm, alpha, E, and s must remain finite.

## Gates

### R1C-G1 provenance and parent lock

Require this pre-data commit to be an ancestor of HEAD, R1b parent JSON classification to be `STABLE_AEST_FINITE_MEMORY_R1B_ETA_TANGENT_FAIL`, stable-host parent to remain certified, the R1b post-data note to be an ancestor, and source audit to confirm unchanged stable chi and finite-bath equations with both orders available.

### R1C-G2 numerical regularity

All 18 runs (3 k x 2 orders x 3 eta) must complete with finite retained observables.

### R1C-G3 held-out eta-tangent consistency

For all six k/order cells require

    E_eta <= 0.05,

with at least 5/6 satisfying

    E_eta <= 0.02.

### R1C-G4 bath-order tangent consistency

For eta=0.01 require at least 2/3 held-out k anchors to satisfy

    E_order <= 0.10
    cosine >= 0.99,

with all three satisfying

    E_order <= 0.20
    cosine >= 0.95.

### R1C-G5 resolved nonzero response

At eta=0.01 require nonzero finite tangent norm in all six k/order cells and

    A^M_W >= 1e-12

in at least 5/6 cells.

## Classification priority

1. G1 fail: `STABLE_AEST_FINITE_MEMORY_R1C_INCOMPLETE`
2. G2 fail: `STABLE_AEST_FINITE_MEMORY_R1C_NUMERICAL_FAIL`
3. G3 fail: `STABLE_AEST_FINITE_MEMORY_R1C_ETA_TANGENT_FAIL`
4. G4 fail: `STABLE_AEST_FINITE_MEMORY_R1C_BATH_ORDER_FAIL`
5. G5 fail: `STABLE_AEST_FINITE_MEMORY_R1C_RESPONSE_UNRESOLVED`
6. all pass: `STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED`

## Interpretation lock

A PASS establishes only that the tau H0=10 matched-bath first-order Weyl memory tangent is numerically resolved across held-out k anchors and robust to the two existing finite-bath discretizations.

A PASS licenses a subsequent stable-AeST growth–Weyl comparison against the host-independent MCMG first-moment relation in this certified long-relaxation regime.

A PASS does not reclassify R1 or R1b, does not certify tau H0=1, and does not establish observational detection, permanent loss of elasticity, or new physics.
