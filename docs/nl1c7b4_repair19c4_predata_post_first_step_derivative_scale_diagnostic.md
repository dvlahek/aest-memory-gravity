# NL1C7B4 Repair19c4 — pre-data post-first-step derivative-scale diagnostic

## Status

Pre-data / pre-run terminal diagnostic preregistration.

Repair19c3 is frozen as

`NL1C7B4_REPAIR19C3_SELECTED_JACOBIAN_NONLINEAR_CLOSURE_FAIL`

at result-freeze commit

`b15eee7f15a5ef4dbb2c87050f4a55983d688d88`.

Frozen Repair19c3 result JSON:

- bytes: `258335`
- SHA-256:
  `aa19480ce4d41f649368f192f27d85b823e0247aa6f9bcc9eb7a9d23b60ac5b0`.

Repair19c3 execution HEAD:

`8317c38c1f6f3df18dcb4106c9b81f7bc543ceaa`.

Frozen Repair19c3 implementation blob:

`08985f1ee334f038a7125cc239fb6b8929d428af`.

Repair19c4 is the single post-first-step derivative-scale diagnostic licensed by the Repair19c3 result freeze.

It is not a nonlinear closure repair and it does not modify the physical model.

## Scientific question

After the first accepted Repair19c3 Gauss-Newton step, is the remaining momentum-dominated stagnation caused by loss of local finite-difference Jacobian fidelity at the frozen post-step probe `abs_step=3e-6`?

The diagnostic asks a narrower question than Repair19c3.

Repair19c3 established a large scale separation:

- first accepted physical correction approximately `1e-5--1e-4`;
- next requested corrections approximately `1e-9--1e-11`, then frequently `1e-12--1e-13`;
- finite-difference probe fixed at `3e-6`.

That scale separation alone does not prove that `3e-6` is inaccurate. Repair19c4 therefore measures derivative fidelity directly at the post-first-step state.

## Frozen physics and state

Unchanged from Repair19c3:

- `eta=0`;
- canonical branch: Simple, beta=1;
- physical projection variables:
  `(y_L,q_Rt)`;
- exact state map:
  `L=L_parent exp(y_L)`;
  `R_t=R_t,parent+q_Rt(a H R_s)`;
- exact orthonormal Helmert representation of:
  `Y4=0`;
  `Qmean=0`;
- all nonprojection fields frozen;
- no direct modification of Q, alpha, phi, matter, source dictionaries, coefficients or signs;
- same residual map and radial point sets;
- same historical exact thresholds.

No new physical field is introduced.

## Frozen domain

Exactly the six lambda=1 canonical cases:

- scales `5,10,20 h^-1 Mpc`;
- `Nr=256,512`;
- Simple branch;
- beta=1.

No virtual-amplitude sweep and no alternate-branch retest is performed.

## Frozen first accepted state

For every case:

1. reconstruct the exact Repair19c3 parent state;
2. construct the Repair19c2-selected Jacobian:
   - method `3-point`;
   - explicit physical-coordinate `abs_step=3e-6`;
3. form the same reduced orthonormal Jacobian;
4. solve the same GELSY system with the same cutoff;
5. reproduce the frozen Repair19c3 first full accepted step.

Call the resulting correction state `x1`.

Require abs-or-rel `1e-10` reproduction of the frozen Repair19c3 lambda=1 first-step controls:

- returned rank;
- predicted relative residual;
- max |y_L|;
- max |q_Rt|;
- exact full-step frozen-denominator residual ratio.

No candidate post-step Jacobian may redefine `x1`.

## Frozen post-first-step diagnostic direction

At `x1`, construct the Repair19c3 control Jacobian using:

- `3-point`;
- `abs_step=3e-6`;
- the same grouped half-band-16 physical-coordinate sparsity;
- the same orthonormal basis.

Solve exactly one GELSY linear system for the post-first-step correction.

Let the resulting reduced correction be `dz2_control` and physical correction be

`dx2_control = B_orth dz2_control`.

Define the normalization

`n2 = ||dx2_control||_2`.

Define the frozen reduced diagnostic direction

`v_z = dz2_control / n2`

and its physical image

`v_x = B_orth v_z = dx2_control / n2`.

Thus `||v_x||_2=1`.

If `dx2_control` is non-finite or `n2=0`, the diagnostic fails implementation integrity for that case.

Candidate Jacobians may not redefine either direction.

This reduced/physical pair is an implementation clarification committed before any Repair19c4 implementation or execution. It changes no candidate, threshold, metric or selection rule.

## Independent symmetric directional reference

At `x1`, evaluate the exact frozen-denominator residual along the frozen unit physical direction `v_x`.

Directional amplitudes are fixed to:

`1e-5, 3e-6, 1e-6, 3e-7, 1e-7, 3e-8, 1e-8, 3e-9, 1e-9`.

For each amplitude `s`, evaluate:

- `F(x1+s v_x)`;
- `F(x1-s v_x)`;
- `F(x1+(s/2)v_x)`;
- `F(x1-(s/2)v_x)`.

Define

`D1(s)=[F(x1+s v_x)-F(x1-s v_x)]/(2s)`

and

`Dhalf(s)=[F(x1+(s/2)v_x)-F(x1-(s/2)v_x)]/s`.

Define the Richardson directional estimate

`Dref(s)=[4 Dhalf(s)-D1(s)]/3`.

For every `s` record:

- full-vector norm;
- H-block norm;
- M-block norm;
- Richardson correction size;
- exact-Q error;
- Y4;
- Qmean;
- field-freeze invariant.

## Deterministic reference-window rule

For adjacent listed amplitudes `s_i > s_{i+1}`, define

`r_i = ||Dref(s_i)-Dref(s_{i+1})|| / max(||Dref(s_{i+1})||,tiny)`

and the corresponding momentum-block quantity `r_i^M`.

A stable directional-reference pair requires simultaneously

- `r_i <= 5e-4`;
- `r_i^M <= 5e-4`.

For each case choose the stable adjacent pair with the largest amplitudes.

The smaller-amplitude member of that pair is the case reference `Dstar`.

If no stable adjacent pair exists for a case, that case has no resolved directional reference.

The threshold `5e-4` is frozen before execution. It is comparable to the largest Richardson-reference instability already observed in Repair19c2 (`3.383564090978392e-4`) and is not adjustable after the run.

## Candidate post-step Jacobians

The finite-difference method remains fixed:

`3-point`.

Evaluate explicit absolute physical-coordinate steps:

- `1e-5`;
- `3e-6`;
- `1e-6`;
- `3e-7`;
- `1e-7`;
- `3e-8`;
- `1e-8`;
- `3e-9`;
- `1e-9`.

The `3e-6` candidate is the frozen Repair19c3 control.

No relative-step fallback is permitted.

For candidate reduced Jacobian `J_cand`, evaluate only its action on the frozen reduced direction:

`A_cand = J_cand v_z`.

This is algebraically the same directional action as the corresponding physical-coordinate Jacobian acting on `v_x`.

If a case has a resolved `Dstar`, define:

`m = ||A_cand-Dstar|| / max(||Dstar||,tiny)`.

Also record H-block and M-block mismatches separately.

## Deterministic candidate ranking

A global post-first-step candidate may be selected only if all six cases have resolved directional references.

For every candidate aggregate across all six cases:

- maximum full directional mismatch;
- median full directional mismatch;
- maximum momentum-block mismatch;
- median momentum-block mismatch.

Select exactly one candidate by lexicographic minimization of:

1. maximum full directional mismatch;
2. maximum momentum-block mismatch;
3. median full directional mismatch;
4. median momentum-block mismatch;
5. larger absolute step before smaller absolute step in an exact tie.

The exact nonlinear residual after a candidate step does not enter candidate selection.

## Material derivative-window criterion

A numerically meaningful post-first-step derivative window is declared only if all of the following hold:

1. all six cases have resolved directional references;
2. the selected candidate has maximum full mismatch `<=1e-3`;
3. the selected candidate has maximum momentum mismatch `<=1e-3`;
4. if the selected candidate is not the `3e-6` control, its maximum full mismatch is at most one fifth of the control maximum full mismatch;
5. if the `3e-6` control itself already satisfies both `1e-3` mismatch bounds, Repair19c4 does not attribute Repair19c3 stagnation to a post-first-step finite-difference scale error.

Criterion 4 requires at least a fivefold aggregate fidelity improvement before a different post-step finite-difference scale can license one final nonlinear closure execution.

No threshold may be relaxed after execution.

## Single-step descriptive cross-check

For every candidate and every case, independently solve exactly one post-first-step GELSY linear system at `x1` using that candidate Jacobian.

Evaluate exactly one full physical trial step from `x1`.

Record:

- returned rank;
- predicted relative residual;
- exact frozen-denominator residual ratio;
- exact moving-denominator max epsilon_H;
- exact moving-denominator max epsilon_M;
- physical correction L2 norm;
- max |delta y_L|;
- max |delta q_Rt|;
- exact-Q error;
- Y4;
- Qmean;
- field-freeze invariant.

These quantities are descriptive only.

They do not select the candidate and they do not change the material derivative-window criterion.

No line search is run.

No third Newton step is run.

## Gates

### R19C4_G1 — exact frozen provenance

Require exact Repair19c3 classification, result JSON SHA-256, result-freeze commit, execution HEAD, implementation blob and inherited parent provenance.

Repair19c3 remains frozen as science FAIL.

### R19C4_G2 — exact first-step reproduction

Require all six lambda=1 first accepted states to reproduce the frozen Repair19c3 controls under abs-or-rel `1e-10`.

### R19C4_G3 — exact gauge, Q and field freeze at x1

Require:

- exact-Q reconstruction error `<=1e-12`;
- |Y4| `<=1e-12`;
- |Qmean| `<=1e-12`;
- every nonprojection field bitwise frozen.

### R19C4_G4 — complete directional-reference sweep

Require all preregistered directional residual evaluations to complete and all stored diagnostic quantities to be finite.

A numerically unresolved derivative reference is a scientific diagnostic outcome, not an implementation failure, provided the residual evaluations themselves are finite and provenance/invariants hold.

### R19C4_G5 — deterministic reference-window evaluation

Require the frozen stable-pair rule to be evaluated exactly for all six cases.

No post-run replacement reference amplitude is permitted.

### R19C4_G6 — complete candidate Jacobian audit

Require all nine candidate Jacobians for all six cases to be constructed with exactly the frozen method, explicit absolute steps and grouped sparsity rule.

Require all finite candidate-action mismatch values to be recorded.

### R19C4_G7 — deterministic candidate selection

If and only if all six references resolve, require exactly one global candidate selected by the frozen lexicographic rule.

If any reference is unresolved, no candidate is licensed for later solver use.

### R19C4_G8 — complete single-step descriptive cross-check

Require all 54 candidate/case one-step probes to be attempted and their outcomes retained.

No closure criterion is imposed on these probes.

### R19C4_G9 — claim boundary

Repair19c4 must not:

- run a nonlinear iteration beyond the frozen first state and one candidate post-step probe;
- run line search;
- certify a corrected state;
- write a state NPZ;
- change the physical projection pair;
- add a field;
- modify Y4/Qmean;
- alter any source, coefficient, sign, eta, branch, historical threshold or radial point set;
- tune candidate selection from exact nonlinear closure;
- run time evolution;
- make an observational claim;
- relabel any historical result.

## Terminal classifications

Implementation/provenance failure:

`NL1C7B4_REPAIR19C4_IMPLEMENTATION_FAIL`.

Complete characterization with a material new derivative window:

`NL1C7B4_REPAIR19C4_POST_FIRST_STEP_DERIVATIVE_WINDOW_IDENTIFIED`.

Complete characterization without a material new derivative window:

`NL1C7B4_REPAIR19C4_NO_MATERIAL_POST_FIRST_STEP_DERIVATIVE_WINDOW`.

## Project decision boundary

Repair19c4 is the end of post-first-step derivative-scale diagnosis.

If and only if Repair19c4 identifies a material new derivative window, one final separately preregistered nonlinear closure execution is licensed.

That final execution may use exactly:

- `3-point, abs_step=3e-6` for the first Jacobian at the parent state;
- the single Repair19c4-selected global `3-point` post-first-step absolute step for every later Jacobian.

No adaptive rule, additional candidate, trust region, LM damping, multistart, alternate driver, threshold change or further derivative tuning is licensed.

If Repair19c4 finds no material new derivative window, the finite-difference Gauss-Newton solver-repair track terminates.

That outcome does not prove that no exact solution exists in the physical `(L,R_t)` ansatz. It means that the present double-precision finite-difference projection route has exhausted its preregistered numerical justification.

Observational/data-side infrastructure may continue independently, but no result may be presented as a tested finite-eta AeST prediction until the required eta=0 evolution and finite-eta observable gates are satisfied.
