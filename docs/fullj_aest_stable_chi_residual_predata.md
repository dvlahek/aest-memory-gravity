# AeST stable chi-residual intervention — pre-data declaration

Date: 2026-09-13
Branch: `fullj-evolving-weyl-bridge`
Post-hoc mechanism note parent: `9e3d8e51fc3013894d071e3d1850177110866287`
Formal parent classification: `FULLJ_AEST_ULP_E_RHS_COMPONENT_DISCONTINUITY`

This declaration is fixed before any stable-residual intervention result is inspected.

## Question

Does the certified adjacent-ULP AeST sensitivity disappear when the gauge-invariant residual

    s = a theta/k^2 + alpha

is evolved directly, instead of being reconstructed by subtraction at every RHS evaluation?

The intervention must be algebraically equivalent to the frozen memory-off AeST equations in exact arithmetic. It is a numerical-variable reformulation, not a new physical term.

No memory term is active:

    aest_memory_enabled = no
    aest_eta = 0.

## Exact residual identity

The frozen source uses

    chi = Q (a theta/k^2 + alpha).

Define

    s = a theta/k^2 + alpha,
    chi = Q s.

The frozen AeST equations include

    theta' = (3 c_a^2 - 1) Hc theta + k^2 Pi/(1+w) + metric_euler,

    alpha' = a(E - psi),
    psi = metric_euler/k^2,

where `Hc=a'/a` is the conformal Hubble rate.

Differentiating `s` and substituting the frozen equations gives the exact identity

    s' = 3 c_a^2 Hc (s-alpha) + a[Pi/(1+w) + E].

The metric-Euler/psi terms cancel analytically. This equation contains no subtraction of the two O(alpha) contributions that define a small chi residual.

## Permitted source intervention

Create a separate diagnostic CLASS/AeST copy from the same frozen runtime used by the parent audit.

The only physical-system change permitted is the addition of one redundant perturbation state `s_aest` satisfying the equation above, with

    s_aest(initial) = 0

because the frozen leading adiabatic initial condition imposes

    alpha = -a theta/k^2,
    E = 0.

In the AeST metric/source and perturbation RHS blocks, replace only

    chi = Q (a theta/k^2 + alpha)

by

    chi = Q s_aest.

All original `delta`, `theta`, `alpha`, and `E` equations remain unchanged. `s_aest` is therefore redundant in exact arithmetic and merely supplies a numerically stable representation of the same residual.

Approximation-switch state copies must also copy `s_aest`. No solver tolerance, precision setting, background equation, physical parameter, memory parameter, requested-k value, or observable extractor may be changed.

## Frozen pathological adjacent-ULP pairs

Use exactly the four parent pairs:

- k_h=0.10125: bits 4589576883704929730 / 4589576883704929731
- k_h=0.10250: bits 4589637531396803372 / 4589637531396803373
- k_h=0.16500: bits 4592669915990485346 / 4592669915990485347
- k_h=0.19750: bits 4593959187948552946 / 4593959187948552947

These are intervention targets, not held-out discovery points.

## Held-out adjacent-ULP anchors

Before results, additionally freeze four anchors that were not used in the parent stable-variable diagnosis:

    k_h in {0.10000, 0.16125, 0.19500, 0.19875}.

At each held-out anchor, take the direct/R3 serialized target token and the immediately next larger positive binary64 value as the adjacent pair. Other requested-k tokens remain the direct/R3 list.

## Calm-control anchors

Use three anchors whose previous serialization endpoint response was small:

    k_h in {0.09875, 0.10250, 0.10375}.

For each calm control compare the stable-residual single-token direct/R3 solution with the unmodified direct/R3 solution at the exact direct/R3 token. This is only a gross-regression guard; the historical unmodified solver is not assumed exact in the cancellation-dominated sector.

## Observables

For every run retain raw histories for

- alpha_aest,
- E_aest,
- phi,
- psi,
- W=phi+psi,
- and the new `s_aest` state when available.

Primary comparison redshifts remain the parent grid

    z = [6,5,4,3,2,1.5,1,0.5,0.2].

Also retain dense raw histories for diagnostic inspection.

## Gates

### SR-G1 provenance and exact reformulation audit

Require:

- frozen parent AeST runtime provenance;
- formal parent classification `FULLJ_AEST_ULP_E_RHS_COMPONENT_DISCONTINUITY`;
- post-hoc mechanism note is an ancestor;
- source patch adds exactly one `s_aest` state;
- `s_aest(initial)=0`;
- source contains the exact locked s' equation;
- both chi construction sites use `chi=Q*s_aest`;
- original delta/theta/alpha/E equations remain byte-identical apart from local variable declarations needed by the patch.

### SR-G2 unmodified-reference reproduction

Before applying the stable-residual intervention, the runner must reproduce the four parent pathological endpoint W histories with the frozen unmodified runtime to relative L2 <=2e-5. This ensures the same problem is being tested.

### SR-G3 calm-control regression

For each calm control, compare the stable-residual solution to the unmodified direct/R3 solution at the exact direct/R3 token.

Require W relative L2 <=5e-3 for at least 2/3 controls and <=2e-2 for all three.

This is deliberately loose enough not to assume the cancellation-dominated representation is the reference truth.

### SR-G4 pathological-pair continuity recovery

For each of the four frozen pathological adjacent-ULP pairs, compute relative L2 differences over the nine locked redshifts for W, alpha, and E.

Require at least 3/4 pairs to satisfy

    W relL2 <= 1e-4

and all four to satisfy

    W relL2 <= 1e-3.

For the same 3/4 passing pairs require

    alpha relL2 <= 1e-3
    E relL2 <= 1e-3.

### SR-G5 material improvement over parent

For each pathological pair define

    improvement = parent_W_relL2 / stable_W_relL2.

Require median improvement >=1e3 and at least 3/4 pairs >=1e2.

### SR-G6 held-out adjacent-ULP continuity

For the four frozen held-out anchors, require at least 3/4 stable-residual adjacent pairs to have

    W relL2 <= 1e-4

and all four <=1e-3.

This is the primary confirmatory generalization gate because the residual intervention was designed after inspecting the original four pairs.

### SR-G7 residual-state consistency

At dense raw-history points where

    |s_aest| >= 1e-8 (|a theta/k^2| + |alpha|),

compare the directly evolved `s_aest` against the algebraic identity `a theta/k^2+alpha`.

Require relative L2 <=1e-4 for at least 3/4 pathological endpoint-A runs in this non-cancellation-dominated subset.

This checks the exact transformation away from the numerically singular subtraction region.

## Classification priority

1. G1 fail:
   `FULLJ_AEST_STABLE_CHI_RESIDUAL_INCOMPLETE`
2. G2 fail:
   `FULLJ_AEST_STABLE_CHI_REFERENCE_MISMATCH`
3. G3 fail:
   `FULLJ_AEST_STABLE_CHI_GROSS_REGRESSION`
4. G1-G3 pass and G4 fails:
   `FULLJ_AEST_STABLE_CHI_PATHOLOGY_PERSISTS`
5. G1-G4 pass and G5 fails:
   `FULLJ_AEST_STABLE_CHI_IMPROVEMENT_INSUFFICIENT`
6. G1-G5 pass and G6 fails:
   `FULLJ_AEST_STABLE_CHI_HELDOUT_CONTINUITY_FAIL`
7. G1-G6 pass and G7 fails:
   `FULLJ_AEST_STABLE_CHI_IDENTITY_CONTROL_FAIL`
8. G1-G7 pass:
   `FULLJ_AEST_STABLE_CHI_RESIDUAL_REFORMULATION_CERTIFIED`

## Interpretation lock

A final PASS establishes that the adjacent-ULP pathology of the frozen memory-off AeST implementation is removed by an algebraically equivalent residual-state reformulation and generalizes to held-out k anchors.

A PASS would support the conclusion that the historical fringe/ULP pathology was dominated by numerical state-coordinate conditioning in the subtraction-defined chi variable, not by a physical unstable mode.

A PASS still does not retroactively reclassify historical R3 and does not license a new-physics claim.

Only after a PASS may the stable-residual AeST implementation be used as a candidate host for renewed finite-memory physics tests and comparison with the host-independent MCMG consistency relation.
