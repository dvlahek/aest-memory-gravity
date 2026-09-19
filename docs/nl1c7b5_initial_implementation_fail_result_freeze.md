# NL1C7B5 — initial implementation-fail result freeze

## Status

Frozen first locked NL1C7B5 execution.

Classification:

`NL1C7B5_CONSERVATIVE_INITIAL_DATA_IMPLEMENTATION_FAIL`.

Execution HEAD:

`7806749a5d28c63887cd0207e366e858cdaf8c99`.

The first execution began with

`NL1C7B5_CONSERVATIVE_INITIAL_DATA_LOCK_PASS`.

This result is an implementation failure before any conservative nonlinear construction completed. It is not a science failure of the conservative formulation and it is not evidence against the frozen physical `(L,R_t)` ansatz.

## Frozen output hashes

Result JSON:

- bytes: `9018`
- SHA-256:
  `6f59e45621d4895ee8fbb4ce125943fcd2939a534a7266fbebae4759190f79bc`.

Evaluator log:

- bytes: `9464`
- SHA-256:
  `6a444f6c7ca9abf6afd54fc43d9fcecf4f2389afc3993c3a472dec6c1577bd50`.

Full runner log:

- bytes: `11707`
- SHA-256:
  `620f0ff3615eaa4ab08edde945e1b3e96729088e170eaaf8f3b5e05a35445a7e`.

No state NPZ was written.

## Gate result

PASS:

- B5_G1 frozen provenance;
- B5_G2 conservative decomposition identity;
- B5_G3 orthonormal gauge representation;
- B5_G8 output integrity;
- B5_G9 claim boundary.

FAIL:

- B5_G4 complete conservative construction;
- B5_G5 safety/Q/gauge/field freeze;
- B5_G6 original differential exact constraints;
- B5_G7 two-grid correction control.

The latter gates were not reached scientifically because the nonlinear driver rejected the initial residual before the first solve step.

## Exact failure signature

All six frozen cases fail identically at the initial point with

`ValueError: Residuals are not finite in the initial point.`

Cases:

- scale 5, Nr=256;
- scale 5, Nr=512;
- scale 10, Nr=256;
- scale 10, Nr=512;
- scale 20, Nr=256;
- scale 20, Nr=512.

No case reports a solver status, function-evaluation count or returned physical correction.

Therefore the failure is upstream of nonlinear optimization.

## Provenance and decomposition controls

All six parent states reproduce the frozen B4 values exactly.

The reconstructed conservative source/flux decomposition reproduces the original B4 differential numerators on all preregistered noncenter points.

Thus the failure is not caused by:

- parent-state drift;
- source-dictionary drift;
- wrong gauge basis;
- changed physics;
- changed differential constraint equations.

## Localized implementation cause

The frozen B4 differential evaluator permits removable coordinate singularities in raw lambdified source expressions at the analytic center `r=0`.

The historical differential science residual does not use the center as a physical proof point.

The first NL1C7B5 implementation reused the raw center source inside the nine-node conservative cell quadrature.

The log shows raw forms such as

`L R^2(-2 R_t^2/R^2 - 4 L_t R_t/(L R)) + L R^2(4 R_t^2/R^2 + 8 L_t R_t/(L R))`

and

`L R^2(4 R_r R_t/R^2 + 4 L_r R_t/(L R) + 4 L_t R_r/(L R))`

which generate floating-point `0/0` warnings at `R=0`.

These are removable center singularities.

For a regular spherical center,

- `R(0)=0`;
- `R_t(0)=0`;
- `L_r(0)=0`;
- regular scalar quantities remain finite.

The first displayed Hamiltonian source simplifies to terms proportional to `R_t^2` and `R R_t`, so its regular center limit is zero.

The displayed momentum source simplifies to terms proportional to `R_t`, `R L_r R_t` or `R`, so its regular center limit is also zero.

The remaining frozen source terms carry the same regular spherical-volume/radial factors and have zero total local source at the analytic center.

Therefore the nonfinite initial conservative residual is an implementation representation bug: the constructor used undefined raw `0/0` floating-point values instead of the analytic regular-center source limit.

## Licensed implementation repair

Exactly one implementation-only repair is licensed:

- retain every frozen B5 physical equation, variable, quadrature stencil, quadrature weight, normalization, Jacobian rule, solver setting, threshold and output rule;
- after assembling the total local source arrays, set only
  - `S_H[0]=0`;
  - `S_M[0]=0`;
- retain the already frozen center flux values
  - `F_H[0]=0`;
  - `F_M[0]=0`;
- do not modify any noncenter value.

The repair must additionally verify that:

1. all conservative parent residuals are finite before entering `least_squares`;
2. the original noncenter B4 decomposition identity remains unchanged;
3. no new center fit, extrapolation, smoothing or free parameter is introduced.

This is a representation completion for the analytic regular center, not a solver-parameter repair.

The frozen first run remains classified as an implementation FAIL and must not be relabelled.
