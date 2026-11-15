# GE19 — Constrained delayed-memory Weyl transfer: exact proof criterion and current obstruction

15 November 2026. Physics-first analytical continuation of the frozen GE05/GE06, 13–14 November retarded theorems. **No CLASS, DES, numerical sweep, or observational fit.**

**Classification: CONDITIONAL_DELAYED_WEYL_TRANSFER_CRITERION_PROVED / FULL_ACTION_OPERATOR_NOT_CERTIFIED / NONZERO_PHYSICAL_WEYL_OVERLAP_NOT_PROVED / PHYSICS_BLOCK.**

## 1. Freeze exactly what has already been proved

The finite retarded auxiliary bath at fixed Fourier mode k>0 obeys
```math
\ddot q_j+3H\dot q_j+\omega_j^2q_j=\omega_j\sqrt{w_j}\,k\chi/a,\qquad
q_j(t_i)=\dot q_j(t_i)=0.
```
The frozen reduced source is
```math
B_\chi(t)=W_b\chi(t)-a(t)\sum_j w_j\omega_j^2\int_{t_i}^t G_{R,j}(t,s)\frac{\chi(s)}{a(s)}\,ds,
\qquad W_b=\sum_j w_j.
```
The reduced aether source at the quarter-action normalization is `-eta Q B_chi/(4 K_B)` in cosmic time. This alone does **not** establish the full constrained Einstein–AeST–NL0B operator, a physical primordial eigenvector, or a gauge-invariant Weyl overlap. The reported native CLASS total W1 is not a delayed-only Weyl measurement.

## 2. A theorem about a *hypothetical completed* full constrained operator

Let z be a complete, gauge-fixed, **constraint-reduced physical scalar state** obtained from the original full quadratic covariant action after (a) lapse/shift and multiplier variation, (b) algebraic elimination, (c) all independent Einstein, aether, scalar, auxiliary and matter Euler conditions, and (d) a physically specified primordial initial-value branch. All of these are hypotheses, not results of this document.

Assume on a finite regular interval the linear eta=0 tangent for the same physical initial-state derivative is
```math
\dot z_1=A_0(t)z_1+b_E(t)f(t),\qquad
f(t)=-\frac{Q(t)}{4K_B} B_{\chi,0}(t).
```
Here `b_E` is the **physical projection of the original action source** after the constraints have been eliminated; it is not automatically a unit vector in an unreduced CLASS state. Let `W_1(t)=\ell_W(t)z_1(t)` denote the correctly normalized gauge-invariant Bardeen Weyl combination, and let `U_0(t,s)` be the propagator of this same physical constrained operator. Suppose `z_1(t_i)` is held fixed between the two *source decompositions*, not fitted separately.

Define the first-order instantaneous comparator by retaining `B_inst=W_b chi_0` in the source, with the *same* background, same eta=0 trajectory, same A0, same bE, same Weyl observable and same z1(ti). This is only a mathematical source decomposition, not a second physical action.

**Theorem (exact delayed-overlap identity).** For any observation time T,
```math
\boxed{\Delta W_{1,\mathrm{hist}}(T)
=\int_{t_i}^{T}\mathcal K_W(T,s)\,
\frac{Q(s)a(s)}{4K_B}
\sum_jw_j\omega_j^2
\int_{t_i}^{s}G_{R,j}(s,u)\frac{\chi_0(u)}{a(u)}\,du\,ds,}
```
where `K_W(T,s)=ell_W(T) U_0(T,s) b_E(s)`. In particular, `Delta W_hist(T) != 0` **if and only if** this signed nested integral is nonzero, under these assumptions. A finite bound follows by taking absolute values and bounding the integrands. Neither positivity of wj nor the nonzero aether local response implies the integral is nonzero, since constraint projection, Green response, and time cancellation can make it vanish.

*Proof:* Differentiating the assumed fully reduced linear system at eta=0 yields a forced linear tangent. Subtract the instantaneous-only tangent equation with identical initial condition. The difference solves `dot(delta z)=A0 delta z + bE[-Q/(4KB)] B_delayed, delta z(ti)=0`. Variation of constants and the retarded auxiliary representation give the stated double Volterra integral. QED.

**Important:** If there is any explicit eta-dependent metric observer normalization, constraint map, initial state, approximation match, or independent direct source, its derivative must be included. The displayed formula cannot be asserted for the historical patched CLASS system without checking these terms.

## 3. Why positivity of the bath does not prove a physical Weyl signal

A passive positive-frequency bath establishes action-level temporal nonlocality; the metric output is governed by the *projected* Green operator `K_W(T,s)`. If `K_W\equiv0` on the relevant source subspace, or if its weighted overlap with the history vanishes for the chosen physical primordial trajectory, the physical Weyl response may be zero. Gauge invariance of W does not guarantee that a given source has nonzero overlap with it.

A physically decisive sufficient condition would be a rigorously derived nonzero leading coefficient in a short-time expansion of the fully reduced **metric** output, or a justified sign-definite interval of the projected kernel together with the source, with no global cancellation at the target time. Such a condition has not been certified for the full model.

## 4. An important initial-condition caveat

For the fixed reduced diagnostic, if chi_i=E_i=q_i=qdot_i=0 and D_i=dot chi_0(ti) != 0, the already proved delayed bath source starts at `-(D_i/6)(sum wj omegaj^2)h^3`, and the delayed part of the reduced aether eta-tangent starts at `(Q_i D_i/(96 KB))(sum wj omegaj^2)h^4`. **Neither order can automatically be transferred to W**, because the Einstein constraints may be algebraic, the physical source projection may vanish, the physical primordial eta-derivative can differ, and the chosen zero-chi initial point is not the jointly derived full radiation-era growing eigenvector.

The original patched AeST effective-fluid state inherits a pressureless CDM density initial condition and gauge transform. The necessary genuine adiabatic relation is `delta_A/(1+w_A)=3 delta_gamma/4`, not the dust formula at general `w_A != 0`. Consistent transformation of both density and velocity plus all species and the true auxiliary branch is needed.

## 5. The single proof obligation before PHYSICS_GO

Starting from the *same* full covariant action, derive the full scalar quadratic Hessian retaining lapse, shift, unit-aether and auxiliary multipliers. After satisfying constraints, give (i) the independent physical state z and its true evolution A0, (ii) the projected source bE including any eta-dependent constraint eliminations, (iii) the gauge-invariant Weyl projector ellW, (iv) the constrained growing adiabatic state and eta-derivative, and (v) a verified nonzero value or analytic nonvanishing certificate for the **delayed-only nested overlap** above, or an explicit obstruction.

The existing restricted LW30–LW33 proofs and general Noether identity are necessary ingredients but do not by themselves supply (i)–(v). The one-quarter source is action-normalized in the restricted scalar dictionary; the historic half-source v019j is retained as historical evidence, not promoted to the physical action.

**Decision:** No claim of a new free physical memory eigenmode or measurable gravitational lensing effect. Continue with a single joint constrained action and primordial-state derivation. If the completed action cancels the delayed-only Weyl projection, report the obstruction rather than tuning the model. No further CLASS/DES campaigns until this proof gate closes.

## Frozen source documents
- [13 November retarded proof](ge19_20261113_retarded_memory_proof_and_full_physics_obstruction.md)
- [14 November Noether and delayed-onset proof](ge19_20261114_noether_constraint_and_eta0_retarded_branch_theorems.md)
- [11 November joint action-to-CLASS matrix](ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md)
- [All-species and primordial IC issue](ge19_20261111_all_species_Einstein_operator_and_adiabatic_IC_block.md)
- [LW32 multiplier-elimination scope](ge19_lw32_covariant_unit_aether_auxiliary_multiplier_exact_elimination_2026-11-10.md)
- [P0 physics issue](https://github.com/dvlahek/aest-memory-gravity/issues/2)
