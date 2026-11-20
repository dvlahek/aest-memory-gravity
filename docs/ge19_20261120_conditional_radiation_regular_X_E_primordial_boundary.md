# GE19 — Conditional radiation-era regularity selects X(0)=E(0)=0, but does not set finite-time chi_i

20 November 2026. Physics-first **asymptotic initial-mode selection**, not another finite-start Taylor-onset lemma, CLASS integration or DES fit.

**Classification: CONDITIONAL_REDUCED_RADIATION_REGULARITY_LEADING_BOUNDARY_PASS / FINITE_K_SUBLEADING_PRIMORDIAL_MODE_UNSOLVED / FULL_PHYSICAL_WEYL_BLOCK.**

## 1. Original action-consistent reduced system

The previously derived original restricted action scalar/aether system in cosmic time is
\`\`\`math
\dot X=E_A+c_a^2 F,\quad X=\chi/Q,\quad
\frac{d}{dt}(aE_A)=
\frac{aQ}{K_B}\left[
\{K_Q-C(H+Q-3Hc_a^2)\}X
-Cc_a^2F-\frac{\eta}{4}B_\chi
\right].
\tag{1}
\`\`\`
This uses the original one-quarter E source. F is the all-species Einstein-constrained source **conditional** on the action-to-total-stress dictionary and a correctly propagated growing radiation solution. Bath mode histories are **not reset** at an arbitrary finite checkpoint.

## 2. Assumptions explicitly needed for the primordial t->0 limit

Work on a formal early radiation-dominated branch \`a(t)=A t^{1/2}(1+o(1))\`, \`H(t)=1/(2t)+o(1/t)\`, \`K_Q=I0/a³\` with I0>0, K_B>0 and constant C=2-K_B. The frozen Exp K(Q) satisfies Q(t)>Q0>0, and Q grows no faster than logarithmic power as a->0 (roughly sqrt(log 1/a) at the extremely remote formal limit); therefore Q is slowly varying and \`t^{1/2}Q(t)->0\`. **Q must NOT be described as strictly constant at mathematical t->0.** The physical model may cease to be valid before this idealized limit and requires a physical onset boundary.

Assume the bounded physical scalar/electric branch with \`X(t)\` finite limit, \`E_A(t)\` bounded, \`c_a² F(t)\` bounded and with the remaining contributions \`aQ C(H+Q-3Hc_a²)X\`, \`aQ c_a²F\`, \`aQ Bchi\` locally integrable near 0. In particular do not permit a finely tuned bath or other-species term of order KQ X that cancels the leading scalar driving. For a standard regular radiation adiabatic mode, \`Omega_s=O(k²/a²)\` at finite k in superhorizon scaling, \`R_A=QK_Q/3=O(Q/a³)\`, suggesting \`F=O(k² a/Q)\` if metric and aether terms are regular. This is an expected hierarchy, not yet certified from the complete action+Boltzmann evolution.

The auxiliary state must follow a declared primordial retarded boundary, not an arbitrary numerical reset. Its existence as t->0 is an independent physical question.

## 3. Leading boundary exclusion of a nonzero constant X

Since aE_A->0 for bounded E_A, integrate (1) near zero. If \`lim_{t->0}X(t)=X_0 !=0\`, the source \`a Q K_Q X /K_B\` behaves as
\`\`\`math
a Q K_Q X/K_B
=\frac{I_0 Q X}{K_B a²}
\sim \frac{I_0 X_0}{K_B A²}\,\frac{Q(t)}{t}.
\`\`\`
As Q(t)>=Q0>0, its primitive diverges logarithmically or more strongly. All the other source terms are locally integrable by assumption, so there is no bounded-E solution with a finite nonzero limit X_0. Therefore
\`\`\`math
\boxed{\lim_{t\to0^+}X(t)=0.}\tag{2}
\`\`\`
For a constant-Q toy approximation this logarithmic primitive yields an E_A branch proportional to \`t^{-1/2} log t\`; in the **actual** Exp asymptotic, Q has slow logarithmic growth, so that expression is only illustrative, not its exact asymptotic profile.

## 4. Bounded electric field must itself vanish at the boundary

With X(0)=0 and both E_A, c_a²F bounded, the first equation gives X(t)=O(t). Insert in the integrated electric equation and use Q(t) at most polylogarithmic:
\`\`\`math
\frac{d}{dt}(a E_A)
=O(Q(t))+ O(Q(t)t^{1/2})+\text{integrable force terms}.
\`\`\`
If the integrated remaining forcing additionally obeys \`a(t)^{-1}\int_0^t a(s)Q(s)c_a²(s)F(s)ds ->0\` and the analogous retarded bath term (true for the stated bounded source and any bath B growing no faster than a logarithmic power), then
\`\`\`math
\boxed{\lim_{t\to0^+}E_A(t)=0.}\tag{3}
\`\`\`
The original homogeneous integration constant in \`aE_A\` must be zero to achieve a bounded E_A branch. Under the specified modest source regularity this is a leading primordial boundary selection, not a statement that E_A or chi are **exactly** zero at finite t_i>0.

## 5. Consequences for the finite-k physical adiabatic mode

- This restricted **conditional** regularity argument can exclude a nonzero constant X and divergent aether-electric homogeneous branch at the idealized t->0 boundary.
- It does **not** solve the finite-k next-to-leading growing mode, the possible physical isocurvature branches, whether the primordial bath state exists in the t->0 limit, or the complete Einstein–AeST–NL0B Ward/CLASS equivalence.
- Neither \`chi(t_i)=0\` nor \`E_A(t_i)=0\` at the finite CLASS numerical start follows from (2)-(3). Nor may all q_j/p_j be reset at an arbitrary later checkpoint. The earlier h5/h6 local metric estimates remain special finite-start examples, not physical universal late-time predictions.
- The real all-species photon/neutrino hierarchy must determine the *subleading* physical amplitudes at fixed finite k, transport the bath and verify the full scalar charge as well as Einstein constraints.

**Decision:** this meaningfully narrows the admissible **leading** regular primordial branch in the reduced action; it is not enough for \`PHYSICS_GO\`, and no DES sensitivity or detection can be inferred. The next actionable task is one complete finite-k radiation Frobenius initial-state solution and action-to-CLASS source consistency, not another local Taylor or numerical sweep.

## Sources
- [Reduced X/E joint equations](ge19_20261119_exact_driven_X_E_constrained_source_bridge.md)
- [Composite aether stress identity](ge19_20261119_composite_aether_stress_direct_source_cancellation.md)
- [Finite-start bath history transport](ge19_20261119_retarded_history_transport_no_finite_reset.md)
- [Original background Exp primordial source](../ge19/physics_gate/frozen_exp_superhorizon_growing_mode_20261111.py)
- [Full all-species primordial mode limitations](ge19_20261111_all_species_Einstein_operator_and_adiabatic_IC_block.md)
- [Return to DES single gate](ge19_20261119_observability_return_single_gate_decision.md)
