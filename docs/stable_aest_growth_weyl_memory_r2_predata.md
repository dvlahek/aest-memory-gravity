# Stable AeST growth-Weyl memory R2 — pre-data declaration

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This declaration is fixed before any R2 growth-Weyl result is inspected.

## Parent chain

The required physics parent is

    STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED

with

    long_relaxation_growth_Weyl_followup_licensed = true.

The certified host remains

    FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED.

Historical R1 and R1b FAIL classifications remain unchanged. R2 cannot reclassify any historical result.

## Question

In the numerically certified long-relaxation AeST memory branch, does causal memory produce a reproducible differential response between total-matter growth and the Weyl potential, with a response that is enhanced toward late times and coherent across k?

R2 is the first physics-level bridge test after host certification. It does not yet test quantitative agreement with the host-independent MCMG first-moment formula. That comparison is reserved for R3 if R2 passes.

## Frozen physical and numerical regime

No physical source equation may be changed relative to R1c.

Use

    tau H0 = 10,
    aest_memory_order = 20,
    tol_perturbations_integration = 3e-8,
    aest_memory_enabled = yes.

Use exactly

    eta in {0, 0.005, 0.01}

and exactly the R1c held-out certified anchors

    k_h in {0.09875, 0.16125, 0.19500}.

Use

    z = [6,5,4,3,2,1.5,1,0.5,0.2].

No ACT/SPT likelihood, nonlinear correction, parameter fitting, or observational inference is part of R2.

## Observable basis

R2 must not use the internal AeST `delta_cdm` history as the final growth observable.

Use the standard CLASS scalar transfer output in CLASS normalization. For every requested redshift retrieve the transfer dictionary and require the fields

    d_m,
    phi,
    psi.

The total-matter growth observable is

    D_m(k,z) = d_m(k,z).

The Weyl observable in the same transfer basis is

    W(k,z) = phi(k,z) + psi(k,z).

For each requested k, evaluate the transfer fields at the exact requested k_h by deterministic interpolation in log k on the returned positive CLASS transfer grid. The same interpolation algorithm and returned-k convention must be used for eta=0, 0.005, and 0.01. Extrapolation is forbidden.

The eta=0 and eta>0 runs must have compatible returned transfer k domains at every z.

## Matched fractional tangents

For eta>0 define the total-matter tangent

    G_eta(k,z) = [D_m(eta,k,z)-D_m(0,k,z)] / [eta D_m(0,k,z)]

and the Weyl tangent

    L_eta(k,z) = [W(eta,k,z)-W(0,k,z)] / [eta W(0,k,z)].

The central R2 quantity is the growth-Weyl separation

    R_eta(k,z) = L_eta(k,z) - G_eta(k,z).

All retained eta=0 denominators must be finite and nonzero on the locked redshift grid.

For vector comparisons use

    rel(a,b) = ||a-b||_2 / max(||a||_2,||b||_2,tiny).

## Tangent consistency

For each k define

    E_G = rel(G_0.005, G_0.01),
    E_L = rel(L_0.005, L_0.01),
    E_R = rel(R_0.005, R_0.01).

A strict tangent cell satisfies

    E_G <= 0.10,
    E_L <= 0.10,
    E_R <= 0.15.

A loose tangent cell satisfies

    E_G <= 0.25,
    E_L <= 0.25,
    E_R <= 0.30.

## Resolved growth-Weyl separation

At eta=0.01 define the separation signal

    S_R = ||R_0.01||_2.

Use the eta-tangent disagreement as an internal numerical/noise proxy

    N_R = ||R_0.005 - R_0.01||_2.

Define

    Q_sep = S_R / max(N_R,tiny).

This is deliberately scale-adaptive because the certified AeST memory response is very small in absolute amplitude.

## Late-time activation

For eta=0.01 define

    A_hi = RMS(|R| over z in {6,5,4,3}),
    A_lo = RMS(|R| over z in {1,0.5,0.2}),
    F_late = A_lo / max(A_hi,tiny).

This tests the physical pattern already motivated by the host-independent memory theory: the differential memory response should be weak during the near-matter-dominated regime and enhanced at late times.

## Cross-k temporal coherence

For each k take the late/intermediate vector

    r_k = R_0.01(z in {2,1.5,1,0.5,0.2}).

If its z=0.2 value is nonzero, align its overall sign by multiplying with sign[R_0.01(z=0.2)] and normalize it to unit L2 norm. Compute all three pairwise cosines between these sign-aligned vectors.

This gate tests a common redshift-response shape without imposing that the physical amplitude or raw sign must be identical at every k.

## Gates

### R2-G1 provenance and certified-parent lock

Require:

- this pre-data commit is an ancestor of HEAD;
- the R1c JSON exists and has classification `STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED`;
- R1c has `long_relaxation_growth_Weyl_followup_licensed=true`;
- the stable-host parent remains `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED`;
- the R1c post-data milestone and the project-history checkpoint through R1c are ancestors of HEAD;
- the stable source still contains `chi=Q*s` and the unchanged finite-bath closure;
- no new physical source patch is used.

### R2-G2 transfer-basis validity

All nine `(k,eta)` runs must complete and provide finite transfer fields `d_m`, `phi`, and `psi` at all nine requested redshifts.

Require:

- positive monotone transfer-k grids;
- requested k lies inside every returned k domain;
- no interpolation extrapolation;
- finite interpolated `D_m` and `W`;
- nonzero eta=0 `D_m` and `W` at every retained point.

### R2-G3 matched tangent reproducibility

Require at least 2/3 k anchors to satisfy the strict tangent-cell criteria and all three to satisfy the loose criteria.

### R2-G4 resolved growth-Weyl separation

Require all three anchors to have finite nonzero `S_R`.

Require

    Q_sep >= 3

for at least 2/3 anchors and

    Q_sep >= 1

for all three anchors.

### R2-G5 late-time activation

Require

    F_late >= 2

for at least 2/3 anchors and

    F_late >= 1

for all three anchors.

### R2-G6 cross-k temporal coherence

Require the three sign-aligned late/intermediate response vectors to be finite and nonzero and require

    min pairwise cosine >= 0.75.

## Classification priority

1. G1 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2_INCOMPLETE`
2. G2 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2_TRANSFER_BASIS_FAIL`
3. G3 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2_TANGENT_FAIL`
4. G4 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2_SEPARATION_UNRESOLVED`
5. G5 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2_LATE_ACTIVATION_FAIL`
6. G6 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2_CROSS_K_COHERENCE_FAIL`
7. all gates pass: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2_SEPARATION_PASS`

## Interpretation lock

A PASS establishes only that, in the already-certified AeST long-relaxation branch, finite causal memory produces a numerically reproducible differential response between CLASS total-matter growth and the Weyl potential, that this separation is resolved relative to its eta-tangent inconsistency, becomes stronger toward late times, and has a coherent temporal shape across the tested k range.

A PASS licenses R3: quantitative comparison of the AeST growth-Weyl separation shape with the host-independent MCMG first-moment relation.

A PASS does not establish the MCMG relation itself, observational detection, permanent loss of gravitational elasticity, or a fundamental new-physics claim.