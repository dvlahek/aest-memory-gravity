# NL1C7B5 — pre-data conservative integral initial-data construction

## Status

Pre-data / pre-implementation preregistration.

NL1C7B5 is a new project-level initial-data construction track.

It is **not** Repair19c5 and it does not reopen the finite-difference Gauss-Newton repair sequence.

Its parent scientific boundary is the frozen Repair19c4 result:

`NL1C7B4_REPAIR19C4_NO_MATERIAL_POST_FIRST_STEP_DERIVATIVE_WINDOW`.

Repair19c4 result-freeze commit:

`4237da31c972fc961a2f7c961450a529652baa51`.

Repair19c4 execution HEAD:

`f00638497add00d93b5adec3a4f80cb50f1c06b7`.

Repair19c4 result JSON SHA-256:

`a5a7416cd93120f543dbe0f8a70ddc735e9704212d7db5266de87980fe768c18`.

Repair19c4 established that the frozen post-first-step `3-point, abs_step=3e-6` Jacobian already has worst-case directional mismatch approximately `5.04e-5`, well inside the frozen `1e-3` fidelity criterion. No materially better finite-difference scale was identified.

Therefore NL1C7B5 changes the **constraint construction formulation**, not the physical variables, thresholds or derivative-scale policy.

## Scientific problem

The exact B4 constraints are evaluated in the frozen code as sums of terms of the form

`S_H(r) - d_r F_H(r) = 0`

and

`S_M(r) - d_r F_M(r) = 0`.

The current differential evaluator computes the radial derivative with the frozen ninth-order local differentiation matrix and then subtracts terms that can be individually much larger than the remaining residual.

Repair19c4 showed that after the first physical correction the requested Newton updates can fall to approximately `1e-12--1e-9`, while the independent derivative itself remains stable. At that scale the predicted residual cancellation is not realized by the exact pointwise state-to-residual evaluation.

NL1C7B5 tests a single alternative construction:

solve the same constraints in conservative cell-integrated form,

`F(r_{i+1}) - F(r_i) - integral_{r_i}^{r_{i+1}} S(r) dr = 0`,

while retaining the original differential B4 evaluator as the only final science certification.

If this construction produces a state that passes the unchanged differential `1e-7` constraint gate on both grids, the eta=0 initial-data bottleneck is resolved without introducing a new physical field.

If it does not, NL1C7B5 terminates without a solver-repair sequence.

## Frozen physics

Unchanged from Repair19c4:

- `eta=0`;
- canonical source branch: Simple;
- `beta=1`;
- frozen density-Q-completed parent state;
- frozen AeST functions and coefficients;
- frozen signs;
- frozen matter fields;
- frozen scalar/aether fields;
- frozen radial domains;
- frozen source dictionary;
- no branch-specific refit.

The only adjustable physical state pair remains

`L = L_parent exp(y_L)`

and

`R_t = R_t,parent + q_Rt (a H R_s)`.

No third physical field is introduced.

The exact gauge remains

`Y4=0`

and

`Qmean=0`.

The orthonormal Helmert representation certified in Repair19b1/19c is retained exactly.

## Frozen domain

Exactly six canonical lambda=1 parent cases:

- scales `5, 10, 20 h^-1 Mpc`;
- `Nr=256,512`;
- Simple branch;
- beta=1;
- `a_i=0.02`;
- `delta0=1e-3`;
- radial coordinate `x in [0,8]`.

No lambda continuation is used.

No multistart is used.

No alternate source branch is used.

## Conservative source/flux decomposition

For each frozen state, reconstruct the exact B4 Hamiltonian and momentum terms before the radial derivative is applied.

Define total local sources and radial fluxes so that the existing B4 differential numerators satisfy

`numH = S_H - D F_H`

and

`numM = S_M - D F_M`,

with exactly the same lambdified source functions, AeST terms, K-sector terms, dust terms, background terms and center treatment as the frozen differential evaluator.

Every individual radial flux contribution uses the same frozen regular-center prescription already present in B4:

`F_H(0)=0`

and

`F_M(0)=0`

after the existing center assignments.

No algebraic simplification of the physical source functions is permitted.

## G1 — exact decomposition identity

Before any nonlinear construction, require on all six frozen parent states that the reconstructed

`S_H-D F_H`

and

`S_M-D F_M`

match the unmodified B4 `numH` and `numM`.

For each block require abs-or-rel agreement `<=1e-12` elementwise away from the analytically regular center.

Failure is an implementation failure and terminates NL1C7B5 before solving.

## Frozen cell quadrature

The B4 radial grid is uniform.

For every cell `[r_i,r_{i+1}]`, approximate the source integral by integrating the degree-8 Lagrange interpolant through exactly nine neighboring radial nodes.

For cell index `i=0,...,n-2`, choose the nine-node stencil with

`start = min(max(i-4,0), n-9)`

and node indices

`start,...,start+8`.

The quadrature weights are computed deterministically from the exact polynomial moment equations on the physical radial coordinates.

No quadrature order or stencil is selected from result quality.

## Conservative cell residual

For every cell define

`C_H,i = F_H(r_{i+1}) - F_H(r_i) - sum_j w_ij S_H(r_j)`

and

`C_M,i = F_M(r_{i+1}) - F_M(r_i) - sum_j w_ij S_M(r_j)`.

The constructor uses fixed parent-based normalization.

For the frozen parent state define

`d_H,i = |F_H,i+1| + |F_H,i| + sum_j |w_ij S_H,j| + floor_H`

and analogously `d_M,i`.

Use

`floor_H = 1e-14 max_i(d_H,i without floor)`

and analogously for momentum.

The nonlinear construction residual is

`C = [C_H/d_H, C_M/d_M]`.

The denominators remain fixed at their parent values throughout the solve.

They are construction scales only and do not replace the original B4 science metric.

## Frozen nonlinear coordinates

Use the exact orthonormal gauge basis `B_orth`.

The nonlinear unknown is the reduced coordinate vector `z`.

Physical corrections are

`x = B_orth z`

with

`x=(y_L,q_Rt)`.

Thus `Y4=0` and `Qmean=0` hold algebraically at every trial state.

Start only from

`z=0`.

No warm start from a Repair19c intermediate state is permitted.

## Frozen construction Jacobian

The constructor uses one fixed numerical Jacobian policy:

- physical-coordinate method: `3-point`;
- explicit physical-coordinate `abs_step=3e-6`;
- local half-band `16` sparsity around the cell right-node index in both physical field blocks;
- reduced Jacobian formed as
  `J_z = J_x B_orth`.

This derivative policy is not selected in NL1C7B5.

It is inherited from Repair19c2 and retained because Repair19c4 independently showed that the same `3e-6` physical-coordinate derivative is already inside a stable post-first-step derivative window.

No alternative finite-difference step is evaluated.

## Frozen nonlinear driver

Use exactly one constructor:

`scipy.optimize.least_squares`

with

- method `trf`;
- loss `linear`;
- explicit callable frozen Jacobian defined above;
- start `z=0`;
- `ftol=1e-12`;
- `xtol=1e-12`;
- `gtol=1e-12`;
- `max_nfev=200`;
- `x_scale='jac'`.

No second solver is permitted.

No restart is permitted.

No trust-region setting may be changed after execution.

No multistart, line-search replacement, continuation, damping sweep or post-run tolerance change is permitted.

Solver success/status is recorded but is not by itself a science PASS.

## Frozen safety boundary

For every returned state require:

- all physical arrays finite;
- `L>0`;
- `max |y_L| <=0.5`;
- `max |q_Rt| <=0.5`;
- exact-Q normalized reconstruction error `<=1e-12`;
- `|Y4|<=1e-12`;
- `|Qmean|<=1e-12`;
- every nonprojection field bitwise frozen.

Failure is a construction failure.

## Primary science certification

The returned state is evaluated by the **unmodified original B4 differential constraint evaluator**.

This is the decisive gate.

On every one of the six scale/grid cases require

`max epsilon_H <=1e-7`

and

`max epsilon_M <=1e-7`.

The center is treated exactly as in historical B4.

No cell-integrated residual can substitute for this criterion.

No radial point may be removed.

No threshold may be relaxed.

## Two-grid control

For each physical scale compare the dimensionless correction amplitude

`C = sqrt(RMS[(delta L/a)^2] + RMS[(delta R_t/(a H R_s))^2])`

between Nr=256 and Nr=512.

Retain the historical symmetric ratio criterion

`max(C256,C512)/min(C256,C512) <=2.0`.

This is a control on the constructed state, not a replacement for exact constraints.

## Conservative residual reporting

For every returned state report:

- maximum and RMS normalized conservative H cell residual;
- maximum and RMS normalized conservative M cell residual;
- solver status and termination message;
- number of function and Jacobian evaluations;
- reduced and physical correction norms.

These values are descriptive.

The final science classification is controlled by the original differential B4 residuals and frozen integrity gates.

## Output rule

A corrected-state NPZ may be written only if all six cases satisfy:

- provenance/decomposition integrity;
- safety/gauge/Q/field-freeze integrity;
- original differential B4 H and M `<=1e-7`;
- two-grid correction-amplitude control.

The NPZ must contain all six constructed states and exact provenance metadata.

If any science gate fails, no state NPZ is written.

## Gates

### B5_G1 — frozen provenance

Require exact Repair19c4 result-freeze ancestry and frozen parent input hashes.

### B5_G2 — conservative decomposition identity

Require exact source/flux reconstruction of the original B4 differential numerators under the `1e-12` abs-or-rel rule.

### B5_G3 — orthonormal gauge representation

Require the inherited Helmert basis to satisfy the same gauge and orthonormality tolerances as Repair19c4.

### B5_G4 — complete conservative construction

Require exactly one deterministic construction attempt for all six frozen cases with the preregistered driver and no fallback.

### B5_G5 — safety, exact-Q, gauge and field freeze

Require all returned states to satisfy the frozen integrity limits.

### B5_G6 — original differential exact constraints

Require all six returned states to satisfy

`max epsilon_H <=1e-7`

and

`max epsilon_M <=1e-7`

under the unmodified B4 evaluator.

### B5_G7 — two-grid correction control

Require the historical symmetric correction-amplitude ratio `<=2.0` for all three physical scales.

### B5_G8 — output integrity

Write and validate the six-state NPZ if and only if all preceding science gates pass.

If any science gate fails, require the NPZ to be absent.

### B5_G9 — claim boundary

NL1C7B5 must not:

- change eta;
- change a source function;
- change a coefficient or sign;
- add a physical field;
- change the parent density-Q bridge;
- change Simple/beta=1;
- change the historical `1e-7` differential threshold;
- remove radial points;
- fit a boundary value after looking at results;
- run time evolution;
- make a finite-eta claim;
- make an observational claim;
- relabel Repair19c3 or Repair19c4;
- launch a follow-up solver-tuning sequence inside B5.

## Terminal classifications

Implementation/provenance/decomposition failure:

`NL1C7B5_CONSERVATIVE_INITIAL_DATA_IMPLEMENTATION_FAIL`.

Complete constructor but returned state violates safety/gauge/Q/field-freeze:

`NL1C7B5_CONSERVATIVE_INITIAL_DATA_CONSTRUCTION_FAIL`.

Complete safe construction but one or more original differential H/M constraints remain above `1e-7`:

`NL1C7B5_CONSERVATIVE_DIFFERENTIAL_CERTIFICATION_FAIL`.

Differential constraints pass but historical two-grid correction control fails:

`NL1C7B5_CONSERVATIVE_TWO_GRID_CONTROL_FAIL`.

Full certification:

`NL1C7B5_CONSERVATIVE_INITIAL_DATA_CERTIFIED`.

## Project decision boundary

If and only if NL1C7B5 reaches

`NL1C7B5_CONSERVATIVE_INITIAL_DATA_CERTIFIED`,

the six-state NPZ may be used as the initial-data input to the already preregistered eta=0 short-time spherical evolution gate.

No additional nonlinear initial-data solver repair is needed or licensed before that evolution attempt.

If NL1C7B5 reaches a non-PASS science classification, B5 terminates.

A non-PASS does not by itself prove physical nonexistence of an exact `(L,R_t)` state. It does show that both:

1. pointwise differential finite-difference Gauss-Newton construction, and
2. the preregistered conservative cell-integrated construction

failed to produce an exact B4-certified state under the frozen two-field ansatz and double-precision numerical framework.

At that point the project must choose between a genuinely different numerical representation, such as higher-precision or analytically reduced constraint evaluation, and reassessment of the physical initial-data ansatz.

It must not continue with a B5a/B5b sequence of solver-parameter repairs.
