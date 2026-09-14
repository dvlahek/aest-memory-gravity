# Stable AeST growth–Weyl memory R2a — eta-leverage separation audit

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This declaration is fixed after the completed R2 result and before any R2a run is inspected.

## Parent chain

The immediate parent is the completed R2 classification

    STABLE_AEST_GROWTH_WEYL_MEMORY_R2_TANGENT_FAIL.

R2 remains a historical FAIL and is not reclassified by R2a.

The certified finite-memory parent remains

    STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED

in the branch

    tau H0 = 10,
    memory_order = 20.

## Motivation

R2 showed that the separate CLASS total-matter and Weyl tangents are individually reproducible between eta=0.005 and eta=0.01, while their small difference

    R_eta = L_eta - G_eta

is not. Post-data inspection showed that G and L are nearly common-mode and that at k_h=0.195 the absolute fractional separation `eta R_eta` is almost unchanged when eta doubles from 0.005 to 0.01. This is consistent with a differential numerical floor being amplified by division by eta.

R2a therefore increases the positive-coupling lever arm while independently checking the largest coupling at a tighter integration tolerance.

## Question

Does the small CLASS total-matter/Weyl differential response become a reproducible first-order separation when eta is increased within a still-perturbative regime, or does it remain unresolved/floor-like while the individual G and L responses remain smooth?

R2a is a numerical-resolution audit of the R2 separation residual. It does not test the MCMG first-moment relation.

## Frozen physics

No physical source equation may be changed.

Use

    aest_memory_enabled = yes,
    tau H0 = 10,
    aest_memory_order = 20.

Use exactly

    k_h in {0.09875, 0.16125, 0.19500}

and the same CLASS transfer observables as R2:

    D_m = d_m,
    W = phi + psi.

Use the same redshift grid

    z = [6,5,4,3,2,1.5,1,0.5,0.2].

Use the same deterministic PCHIP interpolation in log k_h with no extrapolation.

## Primary eta-leverage runs

At

    tol_perturbations_integration = 3e-8

use

    eta in {0, 0.01, 0.02, 0.04}.

The completed R2 eta=0 and eta=0.01 transfer histories may be reused after exact metadata/provenance checks. The eta=0.02 and eta=0.04 runs are new.

## Tight confirmation

At

    tol_perturbations_integration = 1e-8

run only

    eta in {0, 0.04}

for all three k anchors.

Thus R2a requires 12 new CLASS runs when the reusable R2 parent data are available.

## Matched responses

For every eta>0 define

    G_eta = [D_m(eta)-D_m(0)]/[eta D_m(0)],
    L_eta = [W(eta)-W(0)]/[eta W(0)],
    R_eta = L_eta - G_eta.

Also define the undivided differential response

    P_eta = eta R_eta
          = [W(eta)-W(0)]/W(0) - [D_m(eta)-D_m(0)]/D_m(0).

In an exact smooth first-order separation, R_eta should approach an eta-independent vector and P_eta should scale approximately in proportion to eta. An eta-independent P_eta over increasing eta is instead a floor-like signature.

For vector comparisons use

    rel(a,b) = ||a-b||_2 / max(||a||_2,||b||_2,tiny).

## Extended individual-response linearity

For each k compare the primary tangents at eta=0.01, 0.02 and 0.04.

Define

    E_G_12 = rel(G_0.01,G_0.02),
    E_G_24 = rel(G_0.02,G_0.04),
    E_L_12 = rel(L_0.01,L_0.02),
    E_L_24 = rel(L_0.02,L_0.04).

A strict cell satisfies all four errors <= 0.05.
A loose cell satisfies all four errors <= 0.10.

## High-leverage separation resolution

For each k define

    E_R_hi = rel(R_0.02,R_0.04),
    Q_hi = ||R_0.04|| / max(||R_0.02-R_0.04||,tiny).

A resolved high-leverage cell requires

    E_R_hi <= 0.20
    and
    Q_hi >= 3.

A loose cell requires

    E_R_hi <= 0.35
    and
    Q_hi >= 1.

## Floor-like eta scaling diagnostic

For each k define

    C_P_12 = rel(P_0.01,P_0.02),
    C_P_24 = rel(P_0.02,P_0.04),

and the corresponding vector cosines.

A floor-like cell satisfies

    max(C_P_12,C_P_24) <= 0.20

and both cosines >= 0.95.

This diagnostic is only interpreted if the separate G and L tangents pass their linearity gate and the R separation itself is not resolved.

## Tight-tolerance confirmation at eta=0.04

At each k construct G_0.04, L_0.04 and R_0.04 independently at tolerances 3e-8 and 1e-8.

Define

    C_G_tol = rel(G_3e-8,G_1e-8),
    C_L_tol = rel(L_3e-8,L_1e-8),
    C_R_tol = rel(R_3e-8,R_1e-8),

plus cosine(R_3e-8,R_1e-8).

Require the individual physical responses to satisfy

    C_G_tol <= 0.05,
    C_L_tol <= 0.05

for all three anchors.

A tight-resolved separation cell additionally requires

    C_R_tol <= 0.25
    and cosine >= 0.95.

## Gates and outcome logic

### R2A-G1 provenance and parent lock

Require:

- this pre-data commit is an ancestor of HEAD;
- R2 JSON exists with classification `STABLE_AEST_GROWTH_WEYL_MEMORY_R2_TANGENT_FAIL`;
- R2 post-data note is an ancestor of HEAD;
- R1c remains `STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED`;
- the stable host remains `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED`;
- the source still contains the same stable `chi=Q*s` finite-bath implementation;
- no physical source patch is introduced.

### R2A-G2 transfer-basis and numerical regularity

All reused/new runs must provide finite `d_m`, `phi`, and `psi` on the locked redshift/k domain with no extrapolation.

### R2A-G3 extended G/L linearity

Require at least 2/3 anchors to satisfy the strict individual-response criteria and all three to satisfy the loose criteria.

### R2A-G4 high-leverage separation resolution

Require at least 2/3 anchors to satisfy the resolved high-leverage criteria and all three to satisfy the loose criteria.

### R2A-G5 tight individual-response reproducibility

Require C_G_tol <= 0.05 and C_L_tol <= 0.05 at all three anchors.

### R2A-G6 tight separation reproducibility

Require at least 2/3 anchors to satisfy the tight-resolved separation criterion, with all three finite.

### R2A-D1 floor-like eta scaling

Count the anchors satisfying the floor-like P_eta criterion. This is a diagnostic classification branch, not a prerequisite for a resolved-separation PASS.

## Classification priority

1. G1 fail:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_INCOMPLETE`
2. G2 fail:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_TRANSFER_FAIL`
3. G3 fail:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_INDIVIDUAL_NONLINEAR`
4. G3,G4,G5,G6 all pass:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_SEPARATION_RESOLVED`
5. G3 and G5 pass, G4 or G6 fail, and at least 2/3 anchors satisfy D1:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_DIFFERENTIAL_FLOOR_SUPPORTED`
6. otherwise:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_SEPARATION_UNRESOLVED`

## Interpretation lock

`SEPARATION_RESOLVED` licenses an R3 comparison of the resolved AeST growth-Weyl separation shape with the MCMG first-moment relation.

`DIFFERENTIAL_FLOOR_SUPPORTED` means that the individual total-matter and Weyl memory responses are smooth and reproducible but their difference behaves like an eta-independent differential floor over the tested lever arm. In that outcome the correct scientific statement is a common-mode memory response to the achieved numerical bound, not a detected growth-Weyl lag.

`SEPARATION_UNRESOLVED` means the available lever arm and precision are insufficient to distinguish a physical separation from the numerical floor.

No R2a outcome licenses observational detection, permanent elasticity loss, or a fundamental new-physics claim by itself.
