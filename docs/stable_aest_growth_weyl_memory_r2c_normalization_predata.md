# Stable AeST growth–Weyl memory R2c — source-grid normalization audit

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This declaration is fixed after the completed R2b result and its post-data checkpoint, and before any R2c result is generated.

## Parent chain

Immediate parent:

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED`.

R2b post-data checkpoint commit:

`35913eb794d7427431e5f5050f05a71ecfbccbbe`.

Historical R2 and R2a remain unchanged and R2b cannot be reclassified by this audit.

## Motivation

R2b certified a one-percent common-mode bound between the first-order CLASS total-matter and Weyl memory responses, but a posthoc cross-method comparison found an absolute normalization discrepancy. The lambda=30 R2b variational tangents have essentially the same redshift shape as the finite-eta R2 tangents, while their amplitudes are approximately 2.02--2.05 times larger.

R2b freezes the eta=0 memory forcing on the native CLASS source grid. The completed trace contains only 26 time samples at each target k, after which the external variational probe linearly interpolates the frozen table. The physical finite-eta closure is evaluated during perturbation integration rather than through this sparse table.

R2c tests source-grid interpolation as the normalization mechanism. It does not test a new physical model.

## Frozen physical regime

Use exactly the R2b physical regime:

- tau H0 = 10
- memory_order = 20
- physical aest_eta = 0 for variational probes
- tol_perturbations_integration = 3e-8
- k_h in {0.09875, 0.16125, 0.19500}
- z = [6,5,4,3,2,1.5,1,0.5,0.2]
- growth observable D_m = CLASS d_m
- Weyl observable W = phi+psi
- stable residual chi=Q*s
- unchanged finite-bath physical closure.

The finite-eta reference is frozen from the already completed R2 parent at eta=0.005 and eta=0.01. No new finite-eta reference may be selected after R2c results are seen.

## Source-grid densification

Use CLASS precision parameter

`perturb_sampling_stepsize`

at two prospectively fixed dense levels:

- s1 = 0.02
- s2 = 0.005.

For each anchor and each level, run an eta=0 trace and normalize the resulting force table exactly as in R2b. Record the target-k sample count. The s2 force table must contain more target-k samples than s1, and s1 must contain more than the completed R2b coarse trace count of 26.

No physical perturbation equation is changed by the sampling-step parameter.

## Variational probes

At both s1 and s2 use signed lambda=+30,-30 probes with the corresponding frozen force table.

At s2 additionally use lambda=+10,-10 as an amplifier-consistency control.

For X in {D_m,W}, define

T_X(lambda,s) = [X(+lambda,s)-X(-lambda,s)]/(2 lambda),
G(lambda,s)=T_D/D_0(s),
L(lambda,s)=T_W/W_0(s).

The primary dense estimate is lambda=30 at s2.

## Frozen finite-eta reference

For each anchor define

G_ref = 0.5 [G_eta=0.005 + G_eta=0.01],
L_ref = 0.5 [L_eta=0.005 + L_eta=0.01],

using the already existing R2 arrays.

For X in {G,L} define

E_abs_X(s) = relL2(X_30(s), X_ref),
C_X(s) = cosine(X_30(s), X_ref),
A_X(s) = ||X_ref|| / max(||X_30(s)||,tiny).

A correctly normalized dense variational tangent should have A_X close to one. The posthoc R2b coarse result has A_X approximately 0.49 and is diagnostic only.

## Source-grid convergence

For X in {G,L}, define

E_grid_X = relL2(X_30(s1), X_30(s2)),
C_grid_X = cosine(X_30(s1), X_30(s2)).

## Dense amplifier consistency

At s2 define

E_lambda_X = relL2(X_10(s2), X_30(s2)),
C_lambda_X = cosine(X_10(s2), X_30(s2)).

## Patch neutrality

At each dense sampling level, lambda=0 must reproduce the corresponding unforced stable eta=0 transfer solution with relL2 <=2e-5 for D_m and W at each anchor. It is sufficient to run one lambda=0 baseline per anchor and sampling level; the trace run may serve as that baseline if it stores the same transfer vectors.

## Gates

### R2C-G1 provenance and parent lock

Require:
- this pre-data commit is an ancestor of HEAD;
- R2b post-data commit `35913eb794d7427431e5f5050f05a71ecfbccbbe` is an ancestor of HEAD;
- R2b classification is exactly `STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED`;
- R1c remains `STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED`;
- stable host remains `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED`;
- source keeps stable chi=Q*s and the unchanged physical order-20 closure.

### R2C-G2 source-grid densification

For all three anchors:
- both force tables are finite and valid;
- s1 target-k sample count > 26;
- s2 target-k sample count > s1 target-k sample count.

### R2C-G3 patch neutrality

All dense lambda=0 controls satisfy relL2 <=2e-5 for D_m and W.

### R2C-G4 dense amplifier consistency

At s2 all three anchors must satisfy, for both G and L,

E_lambda <= 0.02 and C_lambda >= 0.999.

### R2C-G5 source-grid convergence

A strict anchor satisfies for both G and L

E_grid <= 0.05 and C_grid >= 0.999.

A loose anchor satisfies

E_grid <= 0.10 and C_grid >= 0.995.

Require at least 2/3 strict and all three loose.

### R2C-G6 absolute normalization

A strict normalized anchor satisfies for both G and L at s2

E_abs <= 0.05,
C >= 0.999,
0.95 <= A <= 1.05.

A loose normalized anchor satisfies

E_abs <= 0.10,
C >= 0.995,
0.90 <= A <= 1.10.

Require at least 2/3 strict and all three loose for normalization certification.

### R2C-G7 coherent normalization mismatch

This gate is evaluated only if G2--G5 pass and G6 fails.

A coherent mismatch anchor requires for both G and L at s2:

C >= 0.999,
E_abs > 0.10,

and the G/L amplitude factors A_G and A_L agree within 2% relative.

Require all three anchors to satisfy this condition and require the six A values to have max/min <=1.10.

This gate identifies a stable global normalization mismatch; it does not license an ad hoc rescaling.

## Classification priority

1. G1 fail:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_INCOMPLETE`
2. G2 fail:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_DENSIFICATION_FAIL`
3. G3 fail:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_PATCH_NEUTRALITY_FAIL`
4. G4 fail:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_VARIATIONAL_TANGENT_FAIL`
5. G5 fail:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_GRID_CONVERGENCE_FAIL`
6. G6 pass:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_ABSOLUTE_NORMALIZATION_CERTIFIED`
7. G6 fail and G7 pass:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_GLOBAL_NORMALIZATION_MISMATCH_CERTIFIED`
8. otherwise:
   `STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_NORMALIZATION_UNRESOLVED`

## Interpretation lock

`ABSOLUTE_NORMALIZATION_CERTIFIED` licenses use of the dense variational G and L vectors as numerically validated first-order eta tangents in later stable-AeST analysis.

`GLOBAL_NORMALIZATION_MISMATCH_CERTIFIED` establishes that source-grid densification does not remove a coherent absolute scaling mismatch despite matching temporal shape. It requires a separate source-equation normalization audit and does not permit posthoc rescaling.

No R2c outcome may reclassify R2b. The R2b one-percent common-mode bound remains its formal result.

No R2c outcome licenses a positive growth-Weyl separation, observational detection, permanent elasticity loss, or fundamental new-physics claim.
