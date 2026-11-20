# GE19 — Regular radiation-era proxy coefficients for the physical aether and a retarded bath

20 November 2026. A **controlled leading-order analytic proxy**, not the full finite-k Einstein–AeST–NL0B growing mode, a numerical CLASS run or a DES prediction.

**Classification: RADIATION_TEST_FLUID_REGULAR_PROXY_X_TAU4_E_TAU3_BATH_Q_TAU7_DELAYED_TAU8 / FULL_PHYSICS_AND_OBSERVABILITY_BLOCK.**

## 1. Precise approximation and source

Start from the *already derived* original reduced action equations in the conformal-time form,
\`\`\`math
X'=a(E_A+c_a^2F),\qquad
E_A'+\mathcal H E_A=\frac{aQ}{K_B}\left[
(K_Q-C(H+Q-3Hc_a^2))X-Cc_a^2F-\eta B_\chi/4\right],
\quad X=\chi/Q.
\`\`\`
The auxiliary equation is
\`\`\`math
q_j''+2\mathcal H q_j'+a^2\omega_j^2q_j
=a k\omega_j\sqrt{w_j}\,\chi.
\`\`\`
Here prime is d/d conformal tau, H is cosmic H, \`mathcal H=aH\`, and the original quarter E-source is retained.

Use a radiation-dominated leading background \`a=A tau\`, \`mathcal H=1/tau\`, \`K_Q=I_0/(A^3 tau^3)\`, with positive constants A,K_B,I_0. To obtain explicit coefficients, **freeze the slowly varying** early-background Q and \`c=c_a²\` locally at the retained leading order and neglect their logarithmic derivatives relative to 1/tau. This is an asymptotic leading-in-slow-variation proxy and **not an exact homogeneous Exp K(Q) background**, since the actual Qdot/Q=-3H c. Any exact asymptotic coefficient at tau->0 must use the actual running functions Q(tau),c(tau) and justify uniform remainders.

Insert the *already derived separate-test-fluid dustlike radiation+neutrino* comoving source at leading \`rho_A/rho_r\`, \`c_a²\`, \`(k tau)^2\`:
\`\`\`math
F(\tau)=f k²\tau² + \ldots,\qquad
f=-\frac{15+4R_\nu}{40}\Psi_0.
\`\`\`
Replacing the full Einstein-constrained F by this dustlike source is the key unverified physical approximation. Drop the AeST feedback on the radiation/neutrinos, higher powers in k tau, the evolution of their full Boltzmann hierarchy and all bath/eta corrections to the zeroth-order aether solution.

## 2. Leading regular aether state

Require the regular branch with \`X(0)=E_A(0)=0\` in the formal radiation approximation, excluding nonregular aether homogeneous electric solutions. The first source equation yields at leading order
\`\`\`math
\boxed{X(\tau)=\frac{A c f k²}{4}\tau^4+\text{subleading}
=-\frac{A c(15+4R_\nu)}{160}\Psi_0k²\tau^4+\cdots.}\tag{1}
\`\`\`
The leading E-source comes from \`aQ K_Q X/K_B\sim\tau²\` (the \`-C c F\` and \`-CHX\` terms enter one higher tau power). Thus, using \`(tau E_A)'=\tau(E_A'+E_A/tau)\`,
\`\`\`math
\boxed{E_A(\tau)=\frac{Q I_0 c f k²}{16A K_B}\tau³+\text{subleading}
=-\frac{QI_0 c(15+4R_\nu)}{640 A K_B}\Psi_0k²\tau³+\cdots.}\tag{2}
\`\`\`
Consistency check: substituting \`X=x_4 tau^4\`, \`E=e_3 tau^3\` into the first equation leaves a residual \`-I_0Qcfk² tau^4/(16K_B)\`, i.e. one higher power than the leading \`tau^3\`. In the E equation the \`tau²\` coefficient cancels exactly, while the remaining residual begins at \`tau³\`. This is an algebraic leading-order balance, not a fully converged solution or full growing eigenvector.

The formal aether homogeneous leading system has a regularity problem: with \`F=0\` and dropping lower-order terms, \`X'=A\tau E\`, \`E'+E/\tau\approx (QI_0/(A²K_B\tau²))X\`. Eliminating E gives \`X''\approx(QI_0/(A K_B\tau))X\`. Dominant indicial exponents of the associated regular-singular approximation are 0 and 1, but E≈X'/(A tau) and the logarithmic correction to the constant X branch yield singular electric behavior. Bounded electric-field boundary excludes both nonzero homogeneous amplitudes in this local leading approximation. This does not constitute classification of all coupled physical isocurvature modes.

## 3. First regular forced bath coefficient

Choose the *primordial* no-free-bath branch \`q_j(0)=q_j'(0)=0\` in this formal proxy, as a physically declared condition, not a theorem forced by regularity. Since \`chi=QX\sim Q(A c f k²/4)\tau^4\`, the source for mode j begins at \`A Q (A c f k²/4) k omega_j sqrt(w_j) tau^5\`. The leading oscillator operator on \`q_j=b_7 tau^7\` is
\`\`\`math
q_j''+(2/\tau)q_j'=7(7+1)b_7\tau^5=56b_7\tau^5.
\`\`\`
Therefore,
\`\`\`math
\boxed{
q_j(\tau)=\frac{A²Q c f k³\omega_j\sqrt{w_j}}{224}\tau^7
+\text{subleading}.
}\tag{3}
\`\`\`
The bath's \`a²\omega_j²q_j\` contribution is \`O(\tau^9)\`, four powers higher than the retained leading drive at \`O(\tau^5)\`; the leading source residual vanishes. This is a direct algebraic check of the proposed coefficient, not a new numerical computation.

For \`M_2=\sum_j w_j\omega_j²\`, the total bath stress force separates exactly as
\`\`\`math
B_\chi=W_b\chi-\frac{a}{k}\sum_j\omega_j\sqrt{w_j}\,q_j,
\qquad W_b=\sum_jw_j.
\`\`\`
The leading history-only term is
\`\`\`math
\boxed{
B_{\chi,\mathrm{delayed}}(\tau)
=-\frac{A³ Q c f k² M_2}{224}\tau^8
+\text{subleading}.
}\tag{4}
\`\`\`
Thus the *instantaneous* \`W_b chi\` begins at \`O(tau^4)\`, while the *accumulated retarded displacement* begins at \`O(tau^8)\` for this chosen regular early branch. This is an early-time separation only: it does not bound or define the late-time lensing amplitude.

## 4. Boundaries of the inference

1. The fixed-coefficient proxy is not an exact Exp cosmological solution, because Q and c run slowly with log(a). The displayed coefficients are leading in the explicitly stated frozen-slow-variation approximation. No uniform time/remainder bounds for the exact Exp background are certified.
2. The radiation/neutrino comoving source comes from *test dustlike AeST*. Full Einstein–AeST–NL0B, neutrino shear feedback and exact order-by-order finite-k growing physical mode have not been solved. The physical initial mode may carry additional subleading E and chi corrections, change the leading coefficient and permit other regular modes.
3. No-free-bath at the **primordial boundary** is a chosen branch, not a constraint at arbitrary later numerical checkpoints; retarded history must be transported, not zero-reset.
4. These are coefficients of the **eta=0 source/bath** proxy. A real eta tangent requires the original normalized quarter action response, all scalar/aether Ward equations and the induced metric/ordinary-species perturbations.
5. Neither (1)-(4) certifies the late-time physical delayed Weyl observable, a DES Y3 sensitivity, nor detection.

## 5. Decision

The proxy now supplies explicit nonzero finite-time initial coefficients \`X~tau4\`, \`E~tau3\`, \`q~tau7\`, \`B_delayed~tau8\` instead of an arbitrary finite-time reset. This is a **substantive controlled early-time initial-state example**, not a license to declare PHYSICS_GO or feed these coefficients directly into the observed DES likelihood. The next decisive action remains full original-action plus all-species mode validation on this finite-k state and a source-normalized delayed-only Weyl transfer with tested start-time invariance.

## Frozen sources
- [Original reduced X/E system](ge19_20261119_exact_driven_X_E_constrained_source_bridge.md)
- [Radiation-neutrino leading dustlike source](../ge19/physics_gate/radiation_neutrino_delta_source_20261111.py)
- [Previous conditional primordial regularity](ge19_20261120_conditional_radiation_regular_X_E_primordial_boundary.md)
- [Finite-boundary retarded history transport](ge19_20261119_retarded_history_transport_no_finite_reset.md)
- [Original reduced scalar and bath action](ge19_20261114_noether_constraint_and_eta0_retarded_branch_theorems.md)
