# GE19 — Retarded bath history transport and the finite-start reset obstruction

19 November 2026. Physics-first **initial-state composition theorem** for the exact restricted positive NL0B auxiliary equations. No CLASS/DES runs or observed residuals. This supersedes any interpretation of the finite-start h5/h6 jets as universal cosmological onset.

**Classification: AUXILIARY_HISTORY_COMPOSITION_EXACT / FINITE_START_ZERO_RESET_NOT_PHYSICALLY_INVARIANT / FULL_COSMOLOGICAL_INITIAL_STATE_AND_WEYL_TRANSFER_OPEN / PHYSICS_BLOCK.**

## 1. Exact retarded auxiliary evolution

For each mode at a fixed nonzero Fourier k, on a regular finite cosmological interval, the original selected normalized auxiliary bath obeys
\`\`\`math
\ddot q_j+3H(t)\dot q_j+\omega_j^2 q_j
=f_j(t),\qquad
f_j(t)=\omega_j\sqrt{w_j}\frac{k\chi(t)}{a(t)}.
\`\`\`
Let the homogeneous fundamental matrix for state \`v_j=(q_j,\dot q_j)^T\` be \`U_j(t,s)\` of
\`\`\`math
\frac{d}{dt}v_j =
\begin{pmatrix}0&1\\-\omega_j^2&-3H\end{pmatrix}v_j+
\binom{0}{f_j(t)},\qquad
U_j(t,s)U_j(s,u)=U_j(t,u).
\`\`\`
For a finite initial time t0 and the **selected zero-free-bath state** \`v_j(t0)=0\`,
\`\`\`math
\boxed{v_j(t)=\int_{t_0}^{t}U_j(t,u)\binom{0}{f_j(u)}\,du.}\tag{1}
\`\`\`
With the corresponding scalar retarded kernel \`G_{R,j}(t,u)=[U_j(t,u)]_{1,2}\`, this implies
\`\`\`math
\boxed{q_j(t_i)=\omega_j\sqrt{w_j}k
\int_{t_0}^{t_i}G_{R,j}(t_i,u)\frac{\chi(u)}{a(u)}\,du.}\tag{2}
\`\`\`
And \`dot q_j(t_i)\` uses the second-row, second-column propagator. Generally neither is zero even if both were zero at t0.

## 2. Exact division-of-evolution theorem

For any t0 < ti < T,
\`\`\`math
\boxed{v_j(T)=U_j(T,t_i)v_j(t_i)+
\int_{t_i}^{T}U_j(T,u)\binom{0}{f_j(u)}\,du.}\tag{3}
\`\`\`
Proof: split (1) into [t0,ti] and [ti,T] and use the homogeneous semigroup composition. Consequently changing a computational checkpoint from t0 to ti is **exactly neutral** if and only if the appropriate transported state \`v_j(t_i)\` is carried along (or if the discarded past contribution happens to vanish for the chosen forcing/observer). Setting \`v_j(t_i)=0\` after a nontrivial earlier retarded forcing removes
\`\`\`math
\boxed{\delta v_j(T)=U_j(T,t_i)v_j(t_i)}
\`\`\`
from the solution, where \`delta\` means full-history minus forced-finite-reset at the *same prescribed chi history*. This is a mathematical identity for the forced auxiliary subsystem; when chi backreacts on the metric and aether, changing this initial bath state also changes the later forcing, so this expression alone is NOT the total full coupled metric error.

## 3. Consequences for the bath force and memory-only tangent

The original completed-square reduced bath force is
\`\`\`math
B_\chi(t)=W_b\chi(t)-\frac{a(t)}{k}
\sum_j\omega_j\sqrt{w_j}\,q_j(t).
\`\`\`
At an arbitrary finite ti after prehistory has occurred, the delayed-only term \`B_delayed(ti)\` need not vanish. Thus the h2 or h3 delayed-force Taylor onset and the related h5/h6 reduced metric jets of the **reset-at-ti** calculations cannot be extrapolated as the universal physical beginning of cosmological memory.

The correct first-order eta response about a fixed eta=0 baseline uses the bath history \`q_{j,0}(t)\` carried from the declared primordial retarded branch. Its memory-only E-source in cosmic time is
\`\`\`math
f_{E,\mathrm{hist}}(t)=\frac{Q(t)a(t)}{4K_Bk}\sum_j\omega_j\sqrt{w_j}\,q_{j,0}(t).
\`\`\`
At generic ti this is already nonzero even when the **new post-ti** driving starts from chi_i=0. The entire cosmological field, not just the auxiliary q/p pair, carries a prior eta-dependent response at ti. Therefore one may **not** initialize the metric or AeST first-order tangent to zero at ti and call the resulting fresh transient the complete physical memory contribution; to change the checkpoint one must transport its complete physical constrained first-order state too.

## 4. Primordial selection remains mathematically nontrivial

The no-free-homogeneous-mode condition is **defined at the physical initial boundary** and transported forward. Its equality to zero at finite ti is a valid *choice of finite-epoch preparation*, not a consequence of regularity or cosmological adiabaticity. The true primordial boundary could be a regular limit, a finite physical onset, or an independently justified statistical initial-state prescription. The singular radiation-era limit \`t->0\` requires checking existence and regularity of (1); it is not licensed by mere finite-interval ODE uniqueness.

In the original reduced scalar system X=chi/Q,
\`\`\`math
\dot X=E_A+c_a^2\left[-\frac{\Omega_s}{R_A}+\frac{k^2}{3a^2R_A}(K_B E_A+C Q X-2\Phi)\right],
\`\`\`
the value X(ti) must be inherited from the full physical growing-mode evolution, not independently zeroed. Selecting bath q/p and X/E consistently from one physical boundary is necessary before a late-time Weyl observable can be predicted.

## 5. Single execution consequence for observability

The previously frozen DES Y3 MagLim4 x Source4 geometry remains reusable. A physical memory transfer used there must:
- declare one physical retarded primordial branch and initial boundary;
- verify start-time/checkpoint **invariance by state transport** (full constrained field+all species+q/p+eta tangent), rather than zero-resetting late;
- derive a nonzero late-time delayed-only *physical* Weyl template, with numerical-error control and distinctness against instantaneous rivals;
- pass Asimov nuisance/instantaneous-rival discriminability before examining observed DES shear residuals.

This exact initial-state composition law is an acceptance requirement, not a claim that the finite-start history has been cosmologically calibrated or that DES detection is present. No full initial-mode solver or observed data analysis was performed.

## References
- [Original normalized action and bath dynamics](ge19_20261114_noether_constraint_and_eta0_retarded_branch_theorems.md)
- [General restricted h5/h6 jets](ge19_20261119_general_initial_chi_delayed_weyl_h5_vs_h6.md)
- [Original finite-start time-history proxy limitation](ge19_20261119_primordial_proxy_delayed_metric_source_decision.md)
- [Constrained X/E source operator](ge19_20261119_exact_driven_X_E_constrained_source_bridge.md)
- [Observability return gate](ge19_20261119_observability_return_single_gate_decision.md)
