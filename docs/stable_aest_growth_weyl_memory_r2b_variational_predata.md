# Stable AeST growth–Weyl memory R2b — eta=0 variational separation audit

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This declaration is fixed after the completed R2a result and before any R2b variational result is generated.

## Parent chain

Immediate parent:

    STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_SEPARATION_UNRESOLVED.

Certified physical host/memory parent:

    STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED.

Historical R2 and R2a classifications remain unchanged.

## Motivation

R2 and R2a established that the separate CLASS total-matter and Weyl finite-memory tangents are smooth, but their small difference reaches a differential double-precision floor. Increasing eta to 0.04 and tightening the integration tolerance did not resolve the separation.

The existing finite-bath closure is linear in eta:

    E' = F_0(y) + eta F_mem(y,q),

with

    F_mem = -a Q B_chi,raw/(2 K_B).

At eta=0 the bath state q_0 evolves under the baseline chi but does not feed back into the AeST sector. Therefore F_mem(y_0,q_0) is the exact inhomogeneous forcing of the first-order eta variational equation. R2b uses this forcing directly instead of estimating it by subtracting two nearly identical finite-eta solutions.

The historical v0.19w variational forcing method is reused conceptually, but the trace must use the certified stable residual

    s = a theta/k^2 + alpha,
    chi = Q s.

## Question

When the exact eta=0 memory forcing is frozen and amplified with signed lambda probes, is the first-order total-matter/Weyl separation reproducibly nonzero, or is the variational response common-mode to a quantitative bound?

## Frozen physical regime

Use exactly

    tau H0 = 10,
    memory_order = 20,
    aest_memory_enabled = yes,
    physical aest_eta = 0,
    tol_perturbations_integration = 3e-8.

Use

    k_h in {0.09875, 0.16125, 0.19500}

and

    z = [6,5,4,3,2,1.5,1,0.5,0.2].

Use CLASS transfer observables

    D_m = d_m,
    W = phi + psi,

with the same PCHIP-in-log-k interpolation and no extrapolation as R2/R2a.

No physical memory equation may be changed. The variational patch is diagnostic-only and adds an external frozen source only when explicit environment variables are supplied.

## Exact forcing trace

For each anchor run the stable eta=0 bath trajectory and record on the native CLASS source grid

    F_eta(k,tau) = -a Q B_chi,raw/(2 K_B),

where

    B_chi,raw = sum_j [ w_j chi - sqrt(w_j) (a omega_j/k) q_j ],
    chi = Q s.

Normalize exact duplicate (k,tau) rows by averaging and sort by (k,tau). The force table must contain finite values and at least 8 time samples for the target k.

## Signed variational probes

Keep physical eta=0 and inject

    lambda F_eta(k,tau)

only into the E equation through the diagnostic external-forcing hook.

Use

    lambda in {0, +1, -1, +10, -10, +30, -30}.

Lambda is a numerical amplification parameter, not a physical eta value.

For observable X in {D_m,W}, define symmetric tangent estimates

    T_X(lambda) = [X(+lambda)-X(-lambda)]/(2 lambda).

Define fractional tangents relative to the lambda=0 baseline

    G_lambda = T_D(lambda)/D_0,
    L_lambda = T_W(lambda)/W_0,
    R_lambda = L_lambda-G_lambda.

The primary amplified estimates are lambda=10 and lambda=30. Lambda=1 is a low-amplification diagnostic.

## Patch-neutrality control

The variationally patched lambda=0 run must reproduce the unforced stable eta=0 transfer solution.

For D_m and W require relL2 <= 2e-5 at each anchor.

## Amplification consistency

For each anchor define

    E_G_10_30 = rel(G_10,G_30),
    E_L_10_30 = rel(L_10,L_30).

A strict cell satisfies max(E_G_10_30,E_L_10_30) <= 0.02.
A loose cell satisfies max(...) <= 0.05.

Also report lambda=1 vs lambda=10 errors but do not use them as the primary gate because lambda=1 may remain near the floating-point floor.

## Separation resolution

For each anchor define

    E_R_10_30 = rel(R_10,R_30),
    cos_R_10_30 = cosine(R_10,R_30),
    Q_R = ||R_30|| / max(||R_10-R_30||,tiny).

A resolved separation cell requires

    E_R_10_30 <= 0.20,
    cos_R_10_30 >= 0.95,
    Q_R >= 3.

## Common-mode bound

Define

    B_30 = ||R_30|| / max(||G_30||,||L_30||,tiny).

A common-mode cell requires

    B_30 <= 0.01.

This is a quantitative one-percent bound on the first-order growth/Weyl mismatch over the locked redshift vector. It is not a proof of exact equality.

## Cross-k temporal coherence

For resolved R_30 vectors, allow an overall sign alignment and compute pairwise cosines of the resulting temporal shapes. Report these values. They are supportive diagnostics and are not allowed to override failed within-anchor reproducibility.

## Gates

### R2B-G1 provenance and parent lock

Require:

- this pre-data commit is an ancestor of HEAD;
- the R2a post-data milestone is an ancestor of HEAD;
- R2a classification is `STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_SEPARATION_UNRESOLVED`;
- R1c remains `STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED`;
- stable host remains `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED`;
- source contains stable `chi=Q*s` and unchanged order-20 finite-bath closure.

### R2B-G2 forcing-trace validity

All three force tables must be finite, cover the target k, have monotone time after normalization, and contain at least 8 target-k samples.

### R2B-G3 patch neutrality

Lambda=0 patched runs must reproduce the unforced stable eta=0 D_m and W with relL2 <=2e-5 at all anchors.

### R2B-G4 amplified individual-tangent consistency

Require at least 2/3 anchors strict and all three loose for G and L between lambda=10 and 30.

### R2B-G5 resolved separation

Count anchors satisfying the resolved separation cell criterion.

### R2B-G6 common-mode bound

Count anchors satisfying B_30 <=0.01.

## Classification priority

1. G1 fail:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_INCOMPLETE`
2. G2 fail:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_FORCE_TRACE_FAIL`
3. G3 fail:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_PATCH_NEUTRALITY_FAIL`
4. G4 fail:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_VARIATIONAL_TANGENT_FAIL`
5. at least 2/3 anchors satisfy G5:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_SEPARATION_CERTIFIED`
6. otherwise, all three anchors satisfy G6:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED`
7. otherwise:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_SEPARATION_UNRESOLVED`

## Interpretation lock

`SEPARATION_CERTIFIED` establishes a reproducible first-order AeST total-matter/Weyl memory separation and licenses the MCMG shape bridge.

`COMMON_MODE_BOUND_CERTIFIED` establishes only that the first-order total-matter and Weyl responses agree to within one percent in vector L2 norm over the locked redshift grid. It does not establish exact equality and does not license a positive growth–Weyl lag claim. It would instead provide a model-discriminating null result relative to MCMG.

`SEPARATION_UNRESOLVED` means even the amplified eta=0 variational probe cannot distinguish the differential response from numerical resolution.

No outcome licenses an observational detection, permanent elasticity loss, or a fundamental new-physics claim by itself.
