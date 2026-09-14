# Stable AeST observable projection R5a — local-eta tangent pre-data declaration

Date: 2026-09-14

## Parent result

R5a is a post-R5 follow-up. The historical parent classification remains exactly

`STABLE_AEST_OBSERVABLE_PROJECTION_R5_ETA_SCALING_FAIL`.

R5 post-data lock: `7e02d7789c7478f56c1c63b7fa94ca59192d4ac4`.

R5a does not reclassify R5 or any R1–R4 result.

## Scientific question

Does a reproducible first-order observable tangent exist locally near eta=0 even though the response-amplified eta=10 projection failed the R5 eta-scaling gate?

The test is restricted to the same three linear integrated observables:

- total-matter sigma8(z),
- effective f sigma8(z),
- linear CMB lensing convergence C_L^{kappa kappa} derived from raw CLASS C_L^{phi phi}.

This remains an observable-projection test, not a likelihood or detection claim.

## Frozen source/model

Identical to R5:

- CLASS/AeST parent head `e85808324f51fc694d12e3ed7439552a3c3f9540`,
- stable-chi residual patch,
- one physical memory multiplier and one physical closure,
- zero diagnostic external-force injections in `perturbations_derivs`,
- tau H0 = 10,
- memory order = 20,
- no nonlinear/Halofit correction,
- growth redshifts z = [0.2, 0.5, 1.0, 1.5, 2.0],
- lensing multipoles 40 <= L <= 2000,
- P_k_max_h/Mpc = 5,
- l_max_scalars >= 2000.

Observable definitions are exactly those frozen in R5.

## Local physical eta scan

Nominal tolerance: 3e-8.

Physical eta values:

`eta = [0, 0.1, 0.25, 0.5]`.

No signed diagnostic amplifier is permitted.

For each observable vector X,

`T_X(eta) = [X(eta)-X(0)]/[eta X(0)]`.

The primary local comparison is T(0.1) versus T(0.25). A secondary local-range comparison is T(0.25) versus T(0.5).

## Precision control

A separate tighter pair at tolerance 1e-8 is frozen for eta=0 and eta=0.1.

This directly tests the smallest-eta tangent used for certification.

## Gates

### R5a-G1 provenance/parent

PASS iff the R5 post-data lock is an ancestor and the parent R5 JSON has the exact classification `STABLE_AEST_OBSERVABLE_PROJECTION_R5_ETA_SCALING_FAIL`.

### R5a-G2 source topology

PASS iff the disposable source has the stable-chi marker, exactly one physical eta multiplier, exactly one physical memory closure, and zero diagnostic external-force injections in `perturbations_derivs`.

### R5a-G3 finite observable runs

PASS iff all four nominal eta runs and both tight-control runs complete with finite positive sigma8(z), finite effective f sigma8(z), and finite positive C_L^{kappa kappa} on the frozen domains.

### R5a-G4 smallest-eta precision stability

For each observable compare nominal T_X(0.1) to tight-control T_X(0.1).

PASS per observable iff relative vector-L2 error <= 0.10 and cosine >= 0.995.

G4 PASS iff all three observables pass.

### R5a-G5 local eta-tangent consistency

For each observable require both:

- T_X(0.1) versus T_X(0.25): relative vector-L2 error <= 0.10 and cosine >= 0.995,
- T_X(0.25) versus T_X(0.5): relative vector-L2 error <= 0.10 and cosine >= 0.995.

G5 PASS iff all three observables pass both comparisons.

### R5a-G6 resolved local response

PASS iff G4 and G5 pass and all nominal T_X(0.1) vectors are finite with nonzero L2 norm.

No sign is preregistered.

## Classification priority

1. `STABLE_AEST_OBSERVABLE_PROJECTION_R5A_INCOMPLETE`
2. `STABLE_AEST_OBSERVABLE_PROJECTION_R5A_SOURCE_TOPOLOGY_FAIL`
3. `STABLE_AEST_OBSERVABLE_PROJECTION_R5A_RUN_FAIL`
4. `STABLE_AEST_OBSERVABLE_PROJECTION_R5A_PRECISION_UNRESOLVED`
5. `STABLE_AEST_OBSERVABLE_PROJECTION_R5A_LOCAL_ETA_SCALING_FAIL`
6. `STABLE_AEST_OBSERVABLE_PROJECTION_R5A_RESPONSE_UNRESOLVED`
7. if G1–G6 pass: `STABLE_AEST_OBSERVABLE_PROJECTION_R5A_LOCAL_TANGENT_CERTIFIED`.

## Claim discipline

A PASS licenses only a reproducible local first-order projection of the stable-AeST memory response into sigma8, effective f sigma8, and linear CMB lensing convergence in the locked tau-H0=10 setup.

It does not license any observational likelihood, detection, parameter bound, ACT/DESI/RSD preference, or positive growth–Weyl separation claim.
