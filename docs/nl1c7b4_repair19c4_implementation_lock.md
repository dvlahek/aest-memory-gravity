# NL1C7B4 Repair19c4 — implementation lock

## Status

Locked after implementation and before any Repair19c4 execution.

Repair19c4 is the single terminal post-first-step derivative-scale diagnostic licensed by the Repair19c3 result freeze.

No Repair19c4 diagnostic output has been inspected before this lock.

## Frozen Repair19c3 parent

- result-freeze commit:
  `b15eee7f15a5ef4dbb2c87050f4a55983d688d88`
- result-freeze blob:
  `f2f9bd8eb10efa5424cc0e0710b7c4941aa673c4`
- execution HEAD:
  `8317c38c1f6f3df18dcb4106c9b81f7bc543ceaa`
- result JSON SHA-256:
  `aa19480ce4d41f649368f192f27d85b823e0247aa6f9bcc9eb7a9d23b60ac5b0`
- classification:
  `NL1C7B4_REPAIR19C3_SELECTED_JACOBIAN_NONLINEAR_CLOSURE_FAIL`
- implementation blob:
  `08985f1ee334f038a7125cc239fb6b8929d428af`.

Repair19c3 remains a frozen science FAIL and is not relabelled.

## Preregistration

Initial preregistration commit:

`3ad5a4e1a9118d26a3c12d5b806f3afeeed6d52d`.

A pre-implementation dimensional clarification was committed before any implementation or execution:

`77a0b4977ee921d0693ad14880f38e5822d505a4`.

Frozen preregistration file:

`docs/nl1c7b4_repair19c4_predata_post_first_step_derivative_scale_diagnostic.md`

with final blob:

`b9ca6d74c862fca6c67b1522648701f32b7e46e8`.

The clarification distinguishes:

- normalized reduced direction `v_z`;
- physical image `v_x=B_orth v_z`.

Directional exact secants use `v_x`; reduced Jacobian actions use `v_z`.

No candidate, threshold, ranking rule or interpretation boundary changed in that clarification.

## Implementation

Final implementation commit:

`5bddba7183d4d0d549bc195d9aa95e5cb105b356`.

Implementation file:

`nl1c7b/initial_constraint_certification_repair19c4.py`

with frozen blob:

`f9965d55af274e601268b41ce325a540e881165d`.

The immediately preceding implementation commit was

`46697e7725b8a6f573475570864fa7a767444bd2`.

The final pre-lock change only hardened the completeness check so candidate directional actions must be finite even if the independent Richardson reference does not resolve. It did not change any scientific metric or candidate rule.

## Frozen domain

Exactly six lambda=1 canonical cases:

- eta=0;
- Simple branch;
- beta=1;
- scales 5, 10 and 20 h^-1 Mpc;
- Nr=256 and Nr=512.

No virtual-amplitude sweep is run.

No alternate source-dictionary branch is run.

## Frozen first state

Each case exactly reconstructs the Repair19c3 parent and reproduces the first accepted Repair19c3 step using:

- grouped half-band-16 physical-coordinate Jacobian;
- `3-point`;
- `abs_step=3e-6`;
- orthonormal `Y4=0,Qmean=0` basis;
- direct GELSY solve;
- unchanged Repair19c3 Armijo/backtracking rule.

The resulting state is `x1`.

No post-step candidate can redefine `x1`.

## Frozen diagnostic direction

At `x1`, the Repair19c3 control Jacobian `3-point, abs_step=3e-6` produces exactly one direct GELSY correction.

From this correction define:

- `dx2_control=B_orth dz2_control`;
- `n2=||dx2_control||_2`;
- `v_z=dz2_control/n2`;
- `v_x=B_orth v_z`.

Thus `||v_x||_2=1`.

Every candidate is evaluated on this same frozen direction.

## Frozen exact directional-reference sweep

Directional amplitudes:

`1e-5, 3e-6, 1e-6, 3e-7, 1e-7, 3e-8, 1e-8, 3e-9, 1e-9`.

For every amplitude the implementation evaluates exact symmetric full- and half-step residuals and forms the preregistered Richardson estimate.

A stable adjacent reference pair requires both:

- full-vector relative change `<=5e-4`;
- momentum-block relative change `<=5e-4`.

The first stable pair in descending-amplitude order is selected.

Its smaller-amplitude Richardson estimate is the case reference.

No post-run reference amplitude substitution is allowed.

## Frozen candidate Jacobians

Method is fixed:

`3-point`.

Absolute physical-coordinate steps:

- `1e-5`
- `3e-6`
- `1e-6`
- `3e-7`
- `1e-7`
- `3e-8`
- `1e-8`
- `3e-9`
- `1e-9`.

The `3e-6` candidate is the Repair19c3 control.

Candidate action is evaluated as

`J_orth v_z`.

Candidate selection never uses exact nonlinear one-step closure performance.

## Frozen global selection rule

A global candidate is selected only if all six directional references resolve.

Aggregate every candidate across all six cases and minimize lexicographically:

1. maximum full directional-action mismatch;
2. maximum momentum directional-action mismatch;
3. median full directional-action mismatch;
4. median momentum directional-action mismatch;
5. larger absolute step on an exact tie.

## Frozen material-window criterion

A material new derivative window is identified only if:

1. all six directional references resolve;
2. selected maximum full mismatch is `<=1e-3`;
3. selected maximum momentum mismatch is `<=1e-3`;
4. selected step differs from the `3e-6` control;
5. selected maximum full mismatch is at least fivefold smaller than the control maximum full mismatch;
6. the `3e-6` control does not already satisfy both `1e-3` mismatch bounds.

No threshold may change after execution.

## Frozen one-step cross-check

For all 9 candidates x 6 cases, exactly one direct post-first-step GELSY correction is attempted and exactly one full physical trial is evaluated.

These 54 probes are descriptive only.

They cannot select a candidate.

No post-`x1` line search is run.

No third Newton correction is run.

## Frozen outputs and classification

No state NPZ may be written.

Allowed terminal classes:

- `NL1C7B4_REPAIR19C4_IMPLEMENTATION_FAIL`
- `NL1C7B4_REPAIR19C4_POST_FIRST_STEP_DERIVATIVE_WINDOW_IDENTIFIED`
- `NL1C7B4_REPAIR19C4_NO_MATERIAL_POST_FIRST_STEP_DERIVATIVE_WINDOW`.

Only the second class licenses one final separately preregistered nonlinear closure execution.

The third class terminates finite-difference Gauss-Newton solver repair.

Neither scientific outcome establishes physical infeasibility of the `(L,R_t)` ansatz.

## Frozen imported blobs

- Repair19c3:
  `08985f1ee334f038a7125cc239fb6b8929d428af`
- Repair19c:
  `f27ed8b39c1351e27d4f3b43b195ff4423e04c76`
- Repair19a:
  `3322ed5cb6ed36471b5d700966d9a3fba646d2d8`
- Repair18a:
  `767199e8ab620f5d6dabd50d0efde9828f22048b`
- Repair16:
  `fbd7d24f748fc398638d4eea4b7707801161e52a`
- Repair01:
  `253a0ae2a19a597f06358704ea276c9005973af3`
- Repair09:
  `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- base B4:
  `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08:
  `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- C7A reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`.

No implementation file, candidate set, finite-difference method, amplitude list, reference rule, selection rule, material-window criterion, physical field, source, coefficient, sign, eta, branch, historical threshold, radial point set or interpretation boundary may change after the first Repair19c4 execution.
