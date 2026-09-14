# Stable AeST growth–Weyl memory R2d — full-history RHS variational audit

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This declaration is fixed after the completed R2c post-data checkpoint and before any R2d result is generated.

## Parent chain

Immediate formal parent:

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_GLOBAL_NORMALIZATION_MISMATCH_CERTIFIED`.

R2c post-data checkpoint commit:

`23af2c6f1abbedfa63c7e41d4cb7fc0aaf36424c`.

R2b remains formally

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED`

and cannot be reclassified by R2d.

## Motivation

R2c increased the source-grid target-k forcing samples from 123 to 489 while the variational G/L vectors converged at the approximately 1e-3 level. Nevertheless, the finite-eta/reference-to-variational amplitude factors remained tightly clustered near 0.5.

The densified source-grid traces retained the same temporal support:

- tau_min_source = 5174.717262978337
- tau_max_source = 14151.626616283856.

Thus R2c ruled out sparse sampling density inside the source interval, but it did not test forcing before the first CLASS source-grid time. The physical finite-eta memory term is evaluated in `perturbations_derivs()` throughout perturbation integration.

R2d tests the prospective hypothesis that missing early-history forcing causes the global source-grid variational normalization mismatch.

## Frozen physical regime

Use exactly:

- tau H0 = 10
- memory_order = 20
- physical aest_eta = 0 for variational probes
- tol_perturbations_integration = 3e-8
- k_h in {0.09875, 0.16125, 0.19500}
- z = [6,5,4,3,2,1.5,1,0.5,0.2]
- growth observable D_m = CLASS d_m
- Weyl observable W = phi+psi
- stable residual chi = Q*s
- unchanged physical finite-memory closure.

The finite-eta reference remains frozen from completed R2:

G_ref = 0.5 [G_eta=0.005 + G_eta=0.01]
L_ref = 0.5 [L_eta=0.005 + L_eta=0.01].

No new finite-eta reference may be selected after R2d results are seen.

## Full-history forcing trace

Add a diagnostic-only trace hook inside the existing physical memory block of `perturbations_derivs()`.

At eta=0 and before multiplication by `aest_eta`, record the actual raw first-order forcing already present in the physical equation:

F_eta(k,tau) = -a Q B_chi,raw / (2 K_B).

The trace must use the same in-block `Bchi_aest` value that the physical closure subsequently multiplies by `aest_eta`. R2d must not reconstruct B_chi independently from a separate formula.

The hook may be restricted to the target k through a diagnostic environment variable. It must not alter any state derivative.

Raw adaptive-RHS trace rows may contain repeated (k,tau) evaluations. Exact duplicate (k,tau) rows are averaged, the final table is sorted by tau, and duplicate-force spread is reported. No smoothing, fitted rescaling, or posthoc amplitude correction is permitted.

## Full-history coverage

For every anchor require the normalized RHS trace to extend substantially earlier than the R2c source-grid trace:

- tau_min_RHS <= 0.25 * tau_min_source
- tau_max_RHS >= 0.995 * tau_max_source
- unique target-k tau count > 489
- all force values finite.

These are coverage requirements, not physics gates.

## Overlap trace consistency

On the common temporal interval [tau_min_source,tau_max_source], compare the direct RHS forcing table with the already completed R2c dense source-grid forcing table at sampling 0.005.

Interpolate the RHS table to the R2c source-grid tau values and define

E_force = relL2(F_RHS,F_source),
C_force = cosine(F_RHS,F_source).

Require for all three anchors:

E_force <= 0.02 and C_force >= 0.999.

This tests that the new full-history hook measures the same forcing where both traces overlap.

## Signed variational probes

Use each full-history eta=0 forcing table with the existing external-force diagnostic mechanism.

For every anchor run lambda = +30,-30,+10,-10.

For X in {D_m,W}, define

T_X(lambda) = [X(+lambda)-X(-lambda)]/(2 lambda),
G(lambda)=T_D/D_0,
L(lambda)=T_W/W_0,
R(lambda)=L(lambda)-G(lambda).

The primary full-history estimate is lambda=30.

## Patch neutrality

The eta=0 trace baseline must reproduce the frozen unforced stable transfer solution with relL2 <=2e-5 for both D_m and W at every anchor.

## Metrics

Amplifier consistency:

E_lambda_X = relL2(X_10,X_30),
C_lambda_X = cosine(X_10,X_30), X in {G,L}.

Absolute normalization:

E_abs_X = relL2(X_30,X_ref),
C_abs_X = cosine(X_30,X_ref),
A_X = ||X_ref|| / max(||X_30||,tiny).

Full-history common-mode statistic:

B_30 = ||L_30-G_30|| / max(||G_30||,||L_30||,tiny).

Residual reproducibility diagnostic:

E_R = relL2(R_10,R_30),
C_R = cosine(R_10,R_30).

## Gates

### R2D-G1 provenance and parent lock

Require:
- this pre-data commit and R2c post-data commit are ancestors of HEAD;
- R2c classification is exactly `STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_GLOBAL_NORMALIZATION_MISMATCH_CERTIFIED`;
- R2b remains `STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED`;
- R1c remains `STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED`;
- stable host remains `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED`;
- physical memory closure and stable chi=Q*s remain unchanged.

### R2D-G2 full-history coverage

All three anchors satisfy the coverage requirements above.

### R2D-G3 overlap force consistency and patch neutrality

All three anchors satisfy E_force <=0.02, C_force >=0.999, and eta=0 D_m/W neutrality <=2e-5.

### R2D-G4 full-history amplifier consistency

For all three anchors and both G,L:

E_lambda <=0.02 and C_lambda >=0.999.

### R2D-G5 absolute normalization

A strict normalized anchor satisfies for both G and L:

E_abs <=0.05,
C_abs >=0.999,
0.95 <= A <=1.05.

A loose normalized anchor satisfies:

E_abs <=0.10,
C_abs >=0.995,
0.90 <= A <=1.10.

Require at least 2/3 strict and all three loose.

### R2D-G6 full-history common-mode bound

Require B_30 <=0.01 at all three anchors.

This gate licenses only a one-percent full-history common-mode bound. It does not license equality at the observed numerical B_30 value.

### R2D-G7 resolved full-history separation

This gate is evaluated only if G5 passes and G6 fails.

A resolved-separation anchor requires:

B_30 >0.01,
E_R <=0.20,
C_R >=0.95.

Require at least 2/3 anchors to satisfy all three conditions.

### R2D-G8 persistent coherent normalization mismatch

This gate is evaluated only if G2--G4 pass and G5 fails.

For every anchor and both G,L require:

C_abs >=0.999,
E_abs >0.10,

and A_G and A_L agree within 2% relative. Also require max(A)/min(A) <=1.10 across all six amplitude factors.

This gate certifies that extending the forcing history does not remove the global normalization mismatch. It does not permit posthoc rescaling.

## Classification priority

1. G1 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_INCOMPLETE`
2. G2 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_HISTORY_COVERAGE_FAIL`
3. G3 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_TRACE_CONSISTENCY_FAIL`
4. G4 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_VARIATIONAL_TANGENT_FAIL`
5. G5 pass and G6 pass: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_FULL_HISTORY_COMMON_MODE_CERTIFIED`
6. G5 pass and G6 fail and G7 pass: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_FULL_HISTORY_SEPARATION_CERTIFIED`
7. G5 fail and G8 pass: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_NON_HISTORY_NORMALIZATION_MISMATCH_CERTIFIED`
8. otherwise: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_FULL_HISTORY_UNRESOLVED`

## Interpretation lock

`FULL_HISTORY_COMMON_MODE_CERTIFIED` licenses the statement that the absolutely normalized full-history first-order stable-AeST memory response is common-mode between CLASS total matter and Weyl response to the preregistered one-percent bound in the locked tau H0=10 regime.

`FULL_HISTORY_SEPARATION_CERTIFIED` licenses a positive full-history growth–Weyl separation only within this stable-AeST regime and only at the tested anchors/redshifts.

`NON_HISTORY_NORMALIZATION_MISMATCH_CERTIFIED` rules out missing source-grid history as the explanation of the global factor mismatch and requires a deeper source-equation / parameter-semantics audit.

No outcome may retroactively change R1, R1b, R2, R2a, R2b, or R2c. No outcome licenses observational detection, permanent elasticity loss, or a fundamental new-physics claim.
