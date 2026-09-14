# Stable AeST growth–Weyl memory R3 — corrected scale-generality audit

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This declaration is fixed after the completed corrected R2e result and its post-data checkpoint, and before any R3 scale-generality result is generated.

## Parent chain

Immediate formal parent:

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_ABSOLUTE_COMMON_MODE_CERTIFIED`.

R2e post-data checkpoint commit:

`c0fe57f73a7785c21b1fecd7455f19148d5f812d`.

Historical R2/R2a/R2b/R2c/R2d classifications remain unchanged.

## Question

R2e established, on three anchors, that after correction of the duplicated diagnostic variational-force hook the absolutely normalized first-order stable-AeST finite-memory response agrees with direct finite-eta differencing and is common-mode between CLASS total-matter growth and Weyl response to the preregistered one-percent bound.

R3 asks if the same common-mode structure persists on additional scales that were already part of the independently validated stable-chi host domain but were not used as the three R2e science anchors.

R3 is a direct physical finite-eta test. Its primary science metrics do not use the diagnostic variational forcing helper.

## Frozen physical regime

Use exactly:

- tau H0 = 10
- memory_order = 20
- tol_perturbations_integration = 3e-8
- physical eta in {0, 0.005, 0.01}
- z = [6,5,4,3,2,1.5,1,0.5,0.2]
- growth observable D_m = CLASS `d_m`
- Weyl observable W = `phi+psi`
- stable residual chi = Q*s
- unchanged physical finite-memory closure.

No diagnostic external-force file or lambda may be active in the R3 science runs.

## Prospectively fixed held-out scale set

Use the seven scales already present in the stable-chi precision-validation domain but not used as the three R2e anchors:

- k_h = 0.10000
- k_h = 0.10125
- k_h = 0.10250
- k_h = 0.10375
- k_h = 0.16500
- k_h = 0.19750
- k_h = 0.19875

The three R2e anchors {0.09875,0.16125,0.19500} are parent references only and are not counted toward the R3 held-out pass fraction.

## Direct finite-eta tangents

For each held-out k and eta in {0.005,0.01}, define

G_eta = [D_m(eta)-D_m(0)]/[eta D_m(0)],
L_eta = [W(eta)-W(0)]/[eta W(0)].

Define individual tangent-consistency metrics

E_G = relL2(G_0.005,G_0.01),
E_L = relL2(L_0.005,L_0.01),
C_G = cosine(G_0.005,G_0.01),
C_L = cosine(L_0.005,L_0.01).

Define the primary eta=0.01 common-mode statistic

B_01 = ||L_0.01-G_0.01|| / max(||G_0.01||,||L_0.01||,tiny),

and the eta=0.005 control

B_005 = ||L_0.005-G_0.005|| / max(||G_0.005||,||L_0.005||,tiny).

The residual itself is not used as an absolute positive-separation observable because the earlier R2/R2a line established that direct differencing of L-G can reach a numerical cancellation floor.

## Late-time activation diagnostic

For X in {G_0.01,L_0.01}, define

F_late(X) = RMS(|X| over z in {1,0.5,0.2}) / max(RMS(|X| over z in {6,5,4}),tiny).

This is a diagnostic of the already observed late activation. It is not required to infer a growth–Weyl separation.

## Gates

### R3-G1 provenance and parent lock

Require:
- this pre-data commit and R2e post-data checkpoint are ancestors of HEAD;
- R2e classification is exactly `STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_ABSOLUTE_COMMON_MODE_CERTIFIED`;
- R1c remains `STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED`;
- stable host remains `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED`;
- stable chi=Q*s and the physical finite-memory closure remain unchanged.

### R3-G2 transfer-basis and finite-run validity

All 21 physical runs must be finite. For every requested redshift and k, `d_m`, `phi`, and `psi` must be present on a valid CLASS transfer basis and the requested k must lie inside the interpolation domain without extrapolation.

### R3-G3 individual finite-eta tangent consistency

A strict scale requires

E_G <= 0.02,
E_L <= 0.02,
C_G >= 0.999,
C_L >= 0.999.

A loose scale requires

E_G <= 0.05,
E_L <= 0.05,
C_G >= 0.995,
C_L >= 0.995.

Require at least 6/7 strict and all seven loose.

### R3-G4 held-out common-mode generality

A strict common-mode scale requires both

B_01 <= 0.01,
B_005 <= 0.01.

A loose common-mode scale requires both

B_01 <= 0.02,
B_005 <= 0.02.

Require at least 6/7 strict and all seven loose.

### R3-G5 nonzero late-time physical response

For every scale require finite nonzero G_0.01 and L_0.01 vector norms.

Additionally require F_late(G_0.01) > 1 and F_late(L_0.01) > 1 for at least 6/7 scales. This gate only establishes that the tested memory response is late-time activated rather than an all-redshift constant numerical offset.

## Classification priority

1. G1 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R3_INCOMPLETE`
2. G2 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R3_TRANSFER_BASIS_FAIL`
3. G3 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R3_TANGENT_GENERALITY_FAIL`
4. G4 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R3_COMMON_MODE_GENERALITY_FAIL`
5. G5 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R3_LATE_RESPONSE_FAIL`
6. all G1--G5 pass: `STABLE_AEST_GROWTH_WEYL_MEMORY_R3_SCALE_GENERALITY_CERTIFIED`

## Interpretation lock

`SCALE_GENERALITY_CERTIFIED` licenses the statement that the direct physical finite-eta stable-AeST response remains common-mode between CLASS total matter and Weyl response to the preregistered one-percent bound on at least six of seven held-out stable-host scales, with all seven inside a two-percent loose bound, in the locked tau H0=10 regime.

It does not license exact equality, a positive growth–Weyl separation, extrapolation outside the tested k/redshift domain, tau H0=1, observational detection, permanent elasticity loss, or a fundamental new-physics claim.

A successful R3 licenses direct observable projection as the next step. A failed R3 requires scale-local mechanism analysis before any observational projection.
