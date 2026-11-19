# GE19 — Exact composite aether-stress evolution and cancellation of the direct Einstein forcing

19 November 2026. One **new action-consistent reduced analytic identity**, checked independently by symbolic simplification (zero residual). No CLASS, DES, parameter sweep, real observed data, or full-physics certificate.

**Classification: RESTRICTED_X_E_COMPOSITE_STRESS_IDENTITY_PASS / INITIAL_STRESS_SOURCE_SECOND_JET_PASS / FULL_PHYSICAL_PRIMORDIAL_WARD_AND_WEYL_OPEN / PHYSICS_BLOCK.**

## 1. Source-locked reduced starting equations

Use the **original GE05/GE06/NL0B reduced scalar** proper-time equations, with a>0, Q != 0, KB != 0, k>0, c_a²=K_Q/(Q K_QQ), C=2-KB and Qdot/Q=-3H c_a². Let X=chi/Q and
\`\`\`math
F=\Delta_A+\frac{k^2}{3a^2R_A}(K_B E_A+C QX)
=-\frac{\Omega_s}{R_A}+\frac{k^2}{3a^2R_A}
(K_B E_A+C QX-2\Phi)
\`\`\`
where the second equality **assumes** the correct full total-source Einstein Hamiltonian/momentum constraint. The exact reduced action equations derived previously are
\`\`\`math
\dot X=E_A+c_a^2F,
\quad
\dot E_A=-HE_A+\frac{Q}{K_B}
[(K_Q-C(H+Q-3Hc_a^2))X-Cc_a^2F-\eta B_\chi/4].
\`\`\`
The last equation has the original **one-quarter** source, not the historical v019j half-source.

Define the gauge-invariant reduced scalar stress combination
\`\`\`math
S_A:=K_BE_A+C\chi=K_BE_A+C Q X.
\`\`\`
It is exactly the part entering the original action density source as \`-k² S_A/(3a²)\` and the original intrinsic nonadiabatic pressure \`delta P_nad,A = c_a²k² S_A/(3a²)\`. It is **not** itself the full Weyl observable.

## 2. Exact first-order composite identity

Differentiate using KB,C constant:
\`\`\`math
\dot S_A=K_B\dot E_A+C(\dot Q X+Q\dot X).
\`\`\`
Substitute the previous equations and \`Qdot=-3H c_a² Q\` and collect terms. The explicit \`+CQ c_a²F\` from C Q Xdot cancels the \`-CQ c_a²F\` from K_B Edot. All other \`c_a² X\` terms cancel. Thus
\`\`\`math
\boxed{\dot S_A=(C Q-K_B H)E_A+[K_Q-C(H+Q)]\chi-\frac{\eta Q}{4}B_\chi.}\tag{1}
\`\`\`
The direct external/Einstein forcing F disappears **exactly** from this composite equation, irrespective of F time dependence. This does **not** decouple the physical standard species, which affect \`chi,E_A\` indirectly and participate in the full Einstein constraints. The composite equation is a constrained algebraic identity **within the reduced action model**, not full 3+1 action-to-production CLASS proof.

## 3. Selected initial-state corollary and second coefficient

At a regular finite t_i, impose the *specific* reset/preparation \`chi_i=E_i=q_{j,i}=dot q_{j,i}=0\`. Then Bchi_i=0, so
\`\`\`math
\boxed{S_A(t_i)=0,\quad \dot S_A(t_i)=0.}\tag{2}
\`\`\`
For a regular prescribed F_i, \`Xdot_i=c_a,i² F_i\`, \`Edot_i=-Q_i C c_a,i² F_i/K_B\`, \`chidot_i=Q_i c_a,i² F_i\`, and, as qdot_i=0,
\`\`\`math
\dot B_{\chi,i}=W_b \dot\chi_i,\quad W_b=\sum_jw_j.
\`\`\`
Differentiating (1) and using the above gives
\`\`\`math
\boxed{
\ddot S_A(t_i)
=Q_i c_{a,i}^2F_i
\left[K_{Q,i}-\frac{2C Q_i}{K_B}-\frac{\eta Q_i W_b}{4}\right].
}\tag{3}
\`\`\`
Proof is a direct exact symbolic substitution, using 1+C/K_B=2/K_B from C=2-K_B. Therefore \`S_A(t_i+h)=\tfrac12\ddot S_{A,i}h²+O(h³)\` unless the bracket vanishes. The first eta term at this order is the **instantaneous elastic/stiffness** bath contribution, not an isolated retarded history-only signal. Under the selected q=p=0 state, the delayed oscillator displacement begins at higher orders. Do not use (3) to claim delayed gravitational memory or an observable detection.

For the same special initial conditions the intrinsic AeST nonadiabatic pressure \`delta P_nad,A = c_a² k²S_A/(3a²)\` starts at order h² if the coefficient is nonzero and the background is regular. This is a stress/pressure statement, **not** a universal early-time physical Weyl h exponent.

## 4. Initial-condition scope and cosmological meaning

The finite-reset t_i initial condition is **not** universal. If the bath has been driven from an earlier t0, q_j(t_i) and p_j(t_i) are generically nonzero, hence Bchi_i and dot S_i need not vanish. The exact retarded state-transport theorem from 19 November must be honored when changing numerical start/checkpoint. Likewise the genuine radiation-era finite-k growing adiabatic mode may have chi_i and E_i nonzero at subleading orders.

The key scientific distinction is that the composite aether stress combination **removes direct F forcing by an action-derived cancellation**. Any purported full CLASS reduction of the same action should reproduce this combination **on the appropriate physical constraint surface**, including aether/scalar Ward and all standard species. If the constructed production operator does not, its full physical Weyl predictions cannot be certified.

## 5. Decision

This closes a specific action-level cancellation test and provides a concrete algebraic identity for the already planned single full-physics acceptance gate. It **does not** solve the complete primordial Frobenius eigenproblem or certify a physical delayed-only Weyl transfer. The next necessary work is joint finite-k physical initial-state selection with the full all-species hierarchy, and a full-action source-equivalence check that preserves (1). No repeated local Taylor campaigns, new calibration or observational residual fits are justified from this result alone.

## Existing proofs used
- [Exact reduced X/E Einstein source bridge](ge19_20261119_exact_driven_X_E_constrained_source_bridge.md)
- [Original reduced action equations](ge19_20261114_noether_constraint_and_eta0_retarded_branch_theorems.md)
- [Action density/pressure dictionary](ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md)
- [Retarded history transport](ge19_20261119_retarded_history_transport_no_finite_reset.md)
- [Primordial finite-k scope](../ge19/physics_gate/frozen_exp_superhorizon_growing_mode_20261111.py)
