# GE19 — Covariant gauge-invariant memory strain versus Noether/Ward redundancy: the physical primordial selection decision

**22 November 2026 | physics-first, no new numerical or symbolic-gate campaigns.**

**Decision:** the hidden instantaneous stress-null displacement is **not a pure gauge perturbation** (it changes a first-order gauge-invariant AeST scalar–aether strain and, for finite eta, the quadratic NL0B bath potential), but it is **not certified to be an allowed regular cosmological initial mode**. Moreover, the full diffeomorphism Noether/Ward identity is **dependent** on the complete Einstein, aether, auxiliary, multiplier and matter Euler equations on their common solution: Ward cannot be treated as an *additional independent algebraic initial-condition row*. This refines the exact last obstruction and corrects the imprecise prior phrasing "Ward will select epsilon."

## 1. Actual original covariant fields, independent of CLASS source assignments

The source [original NL0B covariant candidate](nl0b_predata_covariant_memory_completion.md) is built from \`g_{\mu\nu},A_\mu,\phi,U_{j\mu}\`, with
\`\`\`math
h_\mu{}^\nu=\delta_\mu{}^\nu+A_\mu A^\nu,\quad
X_\mu=h_\mu{}^\nu\nabla_\nu\phi,\quad A^\mu U_{j\mu}=0,
\`\`\`
and original quadratic fixed positive bath
\`\`\`math
L_{\rm bath}^{(2)}=\frac{\eta a^3}{4}\sum_j
\left[\dot q_j^2-
\left(\omega_jq_j-\sqrt{w_j}\frac{k\chi}{a}\right)^2\right],\quad
\chi=\varphi+Q\alpha_A .
\`\`\`
The [original GE06 directional 3+1 longitudinal action generator](../ge06/analytic_aest_directional_source_generator.py), [LW30 metric constraints](../ge19/lw30_exact_adm_hamiltonian_momentum_constraints_20261110.py), [LW31 spatial shear](../ge19/lw31_action_spatial_traceless_shear_20261110.py), [LW32 multiplier elimination](../ge19/lw32_covariant_aether_auxiliary_multiplier_elimination_20261110.py), and [LW33 reduced scalar-current off-shell decomposition](ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md) are the precise source layers available today. They are **not** together a certified full 3+1 Einstein–AeST–NL0B+all-species physical primordial Cauchy matrix.

## 2. Gauge test: chi and the auxiliary first-order perturbations are gauge invariant

On the unperturbed FLRW background
\`\`\`math
\bar A_\mu=(-1,0,0,0),\qquad \dot{\bar\phi}=Q(t)\ne0,\qquad
\bar U_{j\mu}=0,\qquad \bar X_\mu=0 .
\`\`\`
Under an arbitrary infinitesimal temporal diffeomorphism \`xi^\mu=(T(t,x),0,0,0)\`, the Lie derivatives of the *same* original background fields yield, in an active convention,
\`\`\`math
\delta_\xi\varphi=QT,\quad
\delta_\xi A_i=-\partial_iT\quad
(\delta_\xi\alpha_A=-T),\quad
\delta_\xi\Psi=\dot T,\quad
\delta_\xi U_{j\mu}=0 .
\`\`\`
Consequently
\`\`\`math
\boxed{\delta_\xi\chi=QT+Q(-T)=0,\qquad
\delta_\xi E_A=\partial_t(-T)+\dot T=0,\qquad
\delta_\xi U_{j\mu}=0.}
\`\`\`
Pure spatial diffeomorphisms also leave the first-order \`chi\` invariant because the original FLRW background scalar is spatially homogeneous and the original spatial aether vanishes. More invariantly, \`X_\mu^{(1)}\` is gauge invariant by the Stewart–Walker background-zero rule: the background \`\bar X_\mu=0\`, so its first-order Lie-gauge variation vanishes.

At finite \`k\ne0\` the stress-map kernel previously proved from the original action,
\`\`\`math
\delta\chi=\epsilon,\quad
\delta E_A=-\frac{2-K_B}{K_B}\epsilon,\quad
\delta(\delta Q)=\delta\varphi=0,
\quad
\delta S_A=K_B\delta E_A+(2-K_B)\delta\chi=0,
\`\`\`
therefore **cannot be obtained from a pure gauge time shift** when \`epsilon\ne0\`. It is a distinguishable *candidate* longitudinal perturbation in the restricted reduced fields, although full constraint and regular-mode selection may still exclude it. Non-gauge does not automatically mean allowed propagating physical degree of freedom.

## 3. Quadratic action discriminant with the *same* auxiliary coordinates

Take two initial states at a fixed regular \`a_i>0\`, same metric/ordinary species and scalar density/phase, same bath \`q_j=\dot q_j=0\`, with one state having \`chi_i=0\` and the second displaced by \`delta chi_i=epsilon\ne0\` along the stress-null direction. From the **original unchanged NL0B quadratic action**, the isolated bath Lagrangian density changes by
\`\`\`math
\boxed{
\Delta L_{\rm bath}^{(2)}
=-\frac{\eta a_i k^2}{4}\left(\sum_jw_j\right)\epsilon^2
=-\frac{\eta a_i k^2W_b}{4}\epsilon^2 .
}\tag{1}
\`\`\`
This is an **action-level, nonzero quadratic potential** for \`eta>0,k\ne0,W_b>0\`; its positive potential magnitude is \`eta a_i k²W_b epsilon²/4\`. It is entirely compatible with **zero first-order direct NL0B Einstein stress** about a relaxed zero-bath FLRW background: a quadratic action term does not contribute a background-times-linear bath stress when the background gradients vanish.

Caveats: (1) is the *isolated bath* contribution, not a full second-order gravitational Hamiltonian or a stability theorem; both the AeST and Einstein action pieces and gravitational constraints must be treated jointly for physical energy. If the background auxiliary coordinates are instead adjusted to their instantaneous minimum, the specific potential shift changes; here the comparison deliberately fixes the same \`q_j\`. At \`eta=0\` the auxiliary action degenerates; no claim of eta=0 auxiliary uniqueness is made. 

Together the gauge test and (1) establish more than a formal stress-map rank deficiency: the candidate displacement has nonzero covariantly built scalar–aether strain and can carry a genuine auxiliary restoring source. **They still do not prove the displacement lies on the regular primordial Einstein–AeST–NL0B solution manifold.**

## 4. Exact Noether dependency: Ward cannot independently select the missing epsilon

Let \`\mathcal E_g^{\mu\nu}\`, \`\mathcal E_\phi\`, \`\mathcal E_A^\mu\`, \`\mathcal E_{U_j}^\mu\` and all multiplier/matter Euler expressions be the variational derivatives of the **full, diffeomorphism-invariant candidate action** (not the historical truncated CLASS code). Diffeomorphism invariance yields the off-shell identity, with the same normalization as the original [14 Nov full Noether derivation](ge19_20261114_noether_constraint_and_eta0_retarded_branch_theorems.md):
\`\`\`math
\nabla_\mu\mathcal E_g^{\mu}{}_{\nu}
=\mathcal E_\phi\,\nabla_\nu\phi+
\sum_{V=A,U_j}\left[
\mathcal E_V^\mu(\nabla_\nu V_\mu-\nabla_\mu V_\nu)
-V_\nu\nabla_\mu\mathcal E_V^\mu
\right]
+\sum_\lambda\mathcal E_\lambda\nabla_\nu\lambda
+\mathcal N_\nu(\mathrm{matter},\mathcal E_{\rm matter}) .
\`\`\`
Linearize about an on-shell FLRW background with \`\dot{\bar\phi}=Q\ne0\`. **Once the complete metric, all aether/auxiliary/multiplier, and all matter Euler equations hold at linear order**, the time component gives
\`\`\`math
\boxed{Q\,\mathcal E_\phi^{(1)}=0\quad\Longrightarrow\quad
\mathcal E_\phi^{(1)}=0.}\tag{2}
\`\`\`
Therefore \`\mathcal E_\phi\`/Ward is **not an additional independent equation for the initial mode** after the other complete on-shell equations. Adding it as a new independent algebraic initial-condition constraint would double-count an equation identity. It remains an indispensable **implementation/source consistency check**: LW33 shows that the historical CLASS \`gamma=1/2\` source fails the original reduced scalar current while original \`gamma=1/4\` is compatible, conditional on the matching original dictionary. This implementation failure does not imply a new physical degree of freedom or a new algebraic constraint.

Note the logical direction is one-way: the partial *lapse/momentum/shear and reduced fluid equations* now implemented are not proven equal to the full set of Euler equations; hence they do NOT yet guarantee the original scalar Ward equation or complete Noether closure. But if the full action Euler system is constructed, Ward is a dependent row and **cannot alone decide** whether the stress-null \`epsilon\` is a regular growing or independent isocurvature mode.

## 5. Exact physical decision still required, with a corrected target

At fixed \`k\ne0\` form the complete initial-value/regularity problem from the **unreduced or exactly constraint-eliminated** original quadratic Einstein–AeST–NL0B action, including photon–baryon and neutrino hierarchy. Impose:

- lapse/shift/metric Hamiltonian, momentum, spatial trace and traceless shear with all ordinary species, not only first-order proxy stress;
- scalar/aether and multiplier Euler evolution with original quarter bath force, correct phase/velocity/density dictionary and no hidden half-source switch;
- common adiabatic growing condition on all constituents and a physical early-time regularity criterion on gauge-invariant stress/curvature, not boundedness of a single reduced coordinate;
- genuinely retarded no-independent-bath mode from the physical past, not arbitrary zeroing of \`q_j,p_j\` at a saved finite time;
- check the derived scalar Ward/Noether identity as a **residual** of this full system, not a new independent equation.

Then **count the dimension** of the regular, adiabatic, fully constrained solution space **modulo diffeomorphism**. If one growing curvature amplitude remains, compute its uniquely normalized \`X_2,S_2\` and physical delayed Weyl. If extra modes remain, identify their independent (iso)curvature data and observational amplitude priors; if none remain, the candidate as posed is incompatible with a regular adiabatic initial state. This is a genuine physics outcome in each case, not a PASS-number exercise.

**Current classification: GAUGE_INVARIANT_STRESS_NULL_CANDIDATE_AND_NOETHER_ROW_DEPENDENCE_PROVED / FULL_PHYSICAL_PRIMORDIAL_MODE_NOT_SELECTED / WARD_NOT_AN_INDEPENDENT_SELECTOR / FULL_PHYSICS_GO=FALSE / DES_DETECTION=FALSE.**

**Reproducibility and provenance.** All displayed identities are direct Lie-derivative, action-quadratic and off-shell Noether consequences of the original source-locked covariant and reduced action. Their short symbolic arithmetic was rechecked independently. No new numerical scan, parameter choice, or source-code patch is needed for these mathematical statements; the genuine next computation is the actual complete physical initial-value constraint/kinetic matrix, not another local identity counter.
