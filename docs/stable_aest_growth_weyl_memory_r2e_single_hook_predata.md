# Stable AeST growth–Weyl memory R2e — single-hook normalization audit

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This declaration is fixed after the completed R2d result and its post-data checkpoint, and before any R2e corrected signed-probe result is generated.

## Parent chain

Immediate formal parent:

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_NON_HISTORY_NORMALIZATION_MISMATCH_CERTIFIED`.

R2d post-data checkpoint commit:

`d2589759cda81a590008c184cc2b061eada3ee28`.

Historical R2b, R2c, and R2d classifications remain unchanged and cannot be retroactively reclassified by R2e.

## Pre-result source forensic observation

After R2d completed, the exact external variational-force statement was counted in the generated R2d `perturbations.c`:

```c
dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);
dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);
```

The local audit returned `HOOK_COUNT=2` on consecutive source lines.

The historical v0.19w parent already installs one external variational-force hook. The later stable-R2b wrapper reused the historical runtime helper but inserted the same external-force statement again. Thus the completed R2b/R2c/R2d diagnostic variational equation received the frozen forcing twice, while the physical finite-eta memory closure contains one copy of the eta-dependent source.

This is a concrete implementation defect in the diagnostic variational probe, not a change to the physical AeST memory equations.

The previously observed normalization factors

`A = ||X_ref|| / ||X_variational||`

lie near 0.5. A duplicated external forcing predicts that removing exactly one duplicate copy should halve the variational tangent and move `A` from approximately 0.5 to approximately 1 without changing its shape.

## Frozen physical regime

Use exactly the already certified stable-AeST regime:

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

The frozen finite-eta reference remains the completed R2 reference:

G_ref = 0.5 [G_eta=0.005 + G_eta=0.01]
L_ref = 0.5 [L_eta=0.005 + L_eta=0.01].

No finite-eta reference may be changed after R2e results are seen.

## Allowed implementation correction

The stable variational patcher may be changed only so that the exact statement

```c
dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);
```

is present exactly once in the final diagnostic CLASS source.

If one historical hook is already present, it must be reused. If no hook is present, one may be installed. More than one hook is a source-audit failure.

No coefficient, sign, physical memory equation, bath equation, observable definition, lambda value, finite-eta reference, or science threshold may be changed.

## Frozen forcing tables

R2e reuses the already generated full-history, full-CLASS-k-grid forcing tables from the completed R2d run:

- `results/stable_aest_growth_weyl_memory_r2d_work/rhs_force_0p09875.dat`
- `results/stable_aest_growth_weyl_memory_r2d_work/rhs_force_0p16125.dat`
- `results/stable_aest_growth_weyl_memory_r2d_work/rhs_force_0p19500.dat`

These tables were generated at physical eta=0 from the direct in-block physical RHS forcing before eta multiplication. R2e must not regenerate, smooth, rescale, or otherwise alter them.

The completed R2d overlap test already established that the direct RHS forcing and the dense source-grid forcing agree on their common interval at about 1e-5 relative L2 with cosine effectively one. R2e does not reopen that result.

## Signed probes

For each anchor run lambda = +30,-30,+10,-10 using the frozen R2d full-history forcing table and the corrected single-hook diagnostic CLASS source.

Also run a lambda=0 baseline for each anchor.

For X in {D_m,W} define

T_X(lambda) = [X(+lambda)-X(-lambda)]/(2 lambda),
G(lambda)=T_D/D_0,
L(lambda)=T_W/W_0,
R(lambda)=L(lambda)-G(lambda).

The primary corrected estimate is lambda=30.

## Metrics

Amplifier consistency:

E_lambda_X = relL2(X_10,X_30),
C_lambda_X = cosine(X_10,X_30).

Absolute normalization:

E_abs_X = relL2(X_30,X_ref),
C_abs_X = cosine(X_30,X_ref),
A_X = ||X_ref|| / max(||X_30||,tiny).

Duplicate-hook correction factor relative to completed R2d:

S_X = ||X_R2d,30|| / max(||X_R2e,30||,tiny),
C_old_new_X = cosine(X_R2d,30,X_R2e,30).

A pure duplicate-hook correction predicts S_X approximately 2 and C_old_new_X approximately 1.

Corrected common-mode statistic:

B_30 = ||L_30-G_30|| / max(||G_30||,||L_30||,tiny).

Residual reproducibility diagnostic:

E_R = relL2(R_10,R_30),
C_R = cosine(R_10,R_30).

## Gates

### R2E-G1 provenance and parent lock

Require:
- this pre-data commit and the R2d post-data commit are ancestors of HEAD;
- R2d classification is exactly `STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_NON_HISTORY_NORMALIZATION_MISMATCH_CERTIFIED`;
- R2c remains `STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_GLOBAL_NORMALIZATION_MISMATCH_CERTIFIED`;
- R2b remains `STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED`;
- R1c remains `STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED`;
- stable host remains `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED`.

### R2E-G2 single-hook source correction

Require in the final diagnostic CLASS source:
- exactly one external variational-force hook;
- stable chi=Q*s remains present;
- exactly one physical `Bchi_aest *= aest_eta` multiplication;
- exactly one physical `E_rhs_aest -= 0.5*Q_aest*Bchi_aest` closure;
- runtime external-force helper remains exactly one definition.

### R2E-G3 patch neutrality

For every anchor the corrected lambda=0 baseline must reproduce the frozen R2 eta=0 D_m and W vectors with relL2 <= 2e-5.

### R2E-G4 corrected amplifier consistency

For all three anchors and both G,L require

E_lambda <= 0.02 and C_lambda >= 0.999.

### R2E-G5 duplicate-hook causal normalization

A strict anchor requires for both G and L:

E_abs <= 0.05,
C_abs >= 0.999,
0.95 <= A <= 1.05,
1.95 <= S <= 2.05,
C_old_new >= 0.999.

A loose anchor requires:

E_abs <= 0.10,
C_abs >= 0.995,
0.90 <= A <= 1.10,
1.90 <= S <= 2.10,
C_old_new >= 0.995.

Require at least 2/3 strict and all three loose.

Passing G5 certifies that the duplicate diagnostic external-force hook caused the approximately factor-two absolute-normalization mismatch.

### R2E-G6 corrected common-mode bound

Require B_30 <= 0.01 at all three anchors.

This licenses only the one-percent bound, not exact equality at the observed B_30 value.

### R2E-G7 resolved corrected separation

Evaluate only if G5 passes and G6 fails. A resolved anchor requires

B_30 > 0.01,
E_R <= 0.20,
C_R >= 0.95.

Require at least 2/3 resolved anchors.

## Classification priority

1. G1 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_INCOMPLETE`
2. G2 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_SOURCE_FAIL`
3. G3 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_PATCH_NEUTRALITY_FAIL`
4. G4 fail: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_VARIATIONAL_TANGENT_FAIL`
5. G5 pass and G6 pass: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_ABSOLUTE_COMMON_MODE_CERTIFIED`
6. G5 pass and G6 fail and G7 pass: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_ABSOLUTE_SEPARATION_CERTIFIED`
7. G5 pass otherwise: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_NORMALIZATION_CERTIFIED`
8. otherwise: `STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_NORMALIZATION_UNRESOLVED`

## Interpretation lock

`SINGLE_HOOK_ABSOLUTE_COMMON_MODE_CERTIFIED` licenses the statement that, after removal of the duplicated diagnostic forcing hook, the absolutely normalized full-history first-order stable-AeST memory response agrees with the finite-eta derivative and is common-mode between CLASS total matter and Weyl response to the preregistered one-percent bound in the locked tau H0=10 regime.

It also identifies the duplicate diagnostic hook as the source of the historical approximately factor-two variational-normalization discrepancy.

`SINGLE_HOOK_ABSOLUTE_SEPARATION_CERTIFIED` licenses a positive corrected growth-Weyl separation only within the tested stable-AeST regime and anchors/redshifts.

No R2e outcome may retroactively alter the historical R1, R1b, R2, R2a, R2b, R2c, or R2d classifications. R2e distinguishes a diagnostic implementation defect from the physical memory model.

No outcome licenses observational detection, permanent elasticity loss, or a fundamental new-physics claim.
