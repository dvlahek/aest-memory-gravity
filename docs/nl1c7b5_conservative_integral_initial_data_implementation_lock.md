# NL1C7B5 — conservative integral initial-data implementation lock

## Status

Implementation locked before the first NL1C7B5 construction run.

NL1C7B5 is a project-level numerical reformulation of the frozen eta=0 initial constraints.

It is not Repair19c5 and it does not reopen finite-difference step-scale tuning.

## Parent scientific boundary

Repair19c4 result freeze:

- commit:
  `4237da31c972fc961a2f7c961450a529652baa51`
- blob:
  `cd36b4d3d457b22a63054b78b9930c02ca117a37`
- execution HEAD:
  `f00638497add00d93b5adec3a4f80cb50f1c06b7`
- result JSON SHA-256:
  `a5a7416cd93120f543dbe0f8a70ddc735e9704212d7db5266de87980fe768c18`
- classification:
  `NL1C7B4_REPAIR19C4_NO_MATERIAL_POST_FIRST_STEP_DERIVATIVE_WINDOW`.

The Repair19c finite-difference Gauss-Newton repair track remains closed.

## Preregistration

Preregistration commit:

`13a1e33cc170688441fe979a277c3826952de5e0`.

Preregistration file:

`docs/nl1c7b5_predata_conservative_integral_initial_data.md`

with frozen blob:

`f03e657c5f3ec3eebd4cffef65083dc789182103`.

No preregistered physics, threshold, candidate policy, solver setting, quadrature order or stopping boundary changed after this commit.

## Implementation

Initial implementation commit:

`78f6d490f929113aafbc14a8b55ea6503ab9d0a2`.

Final implementation commit:

`f166dadd74f6df8931707eeb9bdcf567d1f0d4bb`.

Implementation file:

`nl1c7b/conservative_integral_initial_data_b5.py`

with frozen blob:

`6f94be113ef8cabe7459a8a920d8005f5b212a6c`.

The only change between the initial and final implementation commits caches the frozen radial derivative matrix once per case. It changes runtime only, not the numerical formula or scientific rule.

## Frozen physical state

Unchanged:

- eta=0;
- Simple source branch;
- beta=1;
- density-Q-completed parent;
- projection fields only:
  - L
  - R_t;
- state map:
  - `L=L_parent exp(y_L)`
  - `R_t=R_t,parent+q_Rt(a H R_s)`;
- exact gauge:
  - `Y4=0`
  - `Qmean=0`;
- all nonprojection fields frozen.

No additional physical field is permitted.

## Frozen cases

Exactly:

- scales 5, 10, 20 h^-1 Mpc;
- Nr=256,512;
- lambda=1 physical parent only.

Total:

6 construction cases.

No continuation, multistart or alternate branch is permitted.

## Frozen conservative decomposition

The implementation reconstructs the same B4 exact source terms as

`numH=S_H-D F_H`

and

`numM=S_M-D F_M`.

The decomposition uses the unchanged B4 lambdified source functions and the same regular-center flux assignments.

Before construction, all six parent states must reproduce the original B4 numerators under the preregistered elementwise abs-or-rel `1e-12` rule.

## Frozen cell balance

For cell `[r_i,r_{i+1}]`:

`C_H,i=F_H[i+1]-F_H[i]-sum_j w_ij S_H[j]`

and analogously for momentum.

The weights integrate the degree-8 Lagrange interpolant through the frozen nine-node local stencil

`start=min(max(i-4,0),n-9)`.

Parent-based cell normalization is fixed before each solve and never updated.

## Frozen coordinates and start

Use the certified orthonormal Helmert basis.

The solver variable is reduced `z`.

Physical correction:

`x=B_orth z`.

Only start:

`z=0`.

No Repair19c intermediate state is used as a warm start.

## Frozen Jacobian

Exactly:

- `3-point`;
- physical-coordinate `abs_step=3e-6`;
- half-band 16 conservative cell sparsity;
- `J_z=J_x B_orth`.

No alternative step is evaluated.

## Frozen nonlinear driver

Exactly one driver:

`scipy.optimize.least_squares`

with:

- method `trf`;
- loss `linear`;
- `ftol=1e-12`;
- `xtol=1e-12`;
- `gtol=1e-12`;
- `max_nfev=200`;
- `x_scale='jac'`.

No fallback, restart, continuation, multistart or parameter sweep is permitted.

## Frozen final certification

The conservative objective is a construction device only.

A state is science-certified only by the **unchanged original differential B4 evaluator**.

Every one of six cases must satisfy:

`max epsilon_H <=1e-7`

and

`max epsilon_M <=1e-7`.

No radial point may be removed.

The original threshold may not change.

## Frozen safety and integrity

Require:

- finite state;
- L>0;
- max |y_L| <=0.5;
- max |q_Rt| <=0.5;
- exact-Q error <=1e-12;
- |Y4| <=1e-12;
- |Qmean| <=1e-12;
- every nonprojection field bitwise frozen;
- source/flux differential reconstruction remains consistent.

## Frozen two-grid control

For each scale retain the historical correction-amplitude rule:

`max(C256,C512)/min(C256,C512) <=2.0`.

## Frozen output rule

A six-state NPZ may exist only after a full science PASS.

Any non-PASS outcome must leave the state NPZ absent.

## Allowed classifications

- `NL1C7B5_CONSERVATIVE_INITIAL_DATA_IMPLEMENTATION_FAIL`
- `NL1C7B5_CONSERVATIVE_INITIAL_DATA_CONSTRUCTION_FAIL`
- `NL1C7B5_CONSERVATIVE_DIFFERENTIAL_CERTIFICATION_FAIL`
- `NL1C7B5_CONSERVATIVE_TWO_GRID_CONTROL_FAIL`
- `NL1C7B5_CONSERVATIVE_INITIAL_DATA_CERTIFIED`.

Only the final class licenses the already preregistered eta=0 short-time evolution gate.

A non-PASS does not establish physical nonexistence of the two-field ansatz.

No B5a/B5b solver-parameter repair sequence is licensed.

## Frozen imported code blobs

- Repair02 helper:
  `eff076ec9a511f64bc693dc48b07b2ce26cfbaeb`
- Repair19 gauge:
  `2532094b518dfc2990fa0d77d8123d793b0107b3`
- Repair19a orthonormal basis:
  `3322ed5cb6ed36471b5d700966d9a3fba646d2d8`
- Repair19c shared constants:
  `f27ed8b39c1351e27d4f3b43b195ff4423e04c76`
- Repair18a exact evaluator/projection:
  `767199e8ab620f5d6dabd50d0efde9828f22048b`
- Repair16 parent-state reconstruction:
  `fbd7d24f748fc398638d4eea4b7707801161e52a`
- Repair01 frozen non-K source builder:
  `253a0ae2a19a597f06358704ea276c9005973af3`
- Repair09 Q/background helper:
  `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- base B4:
  `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08 scalar identity helper:
  `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- C7A reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`.

No locked file or scientific criterion may change after the first B5 execution.
