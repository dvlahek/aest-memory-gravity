# GE19 — Noether closure, the one-sided eta=0 retarded derivative and the exact obstruction to a physical Weyl mode

**14 November 2026. Physics-first analytical continuation, zero new CLASS/numerical runs.**

**Result**: Three genuinely mathematical statements are proved within their named assumptions below. No new theorem claiming a full, gauge-invariant physical cosmological memory mode is proved. This document identifies **one explicit remaining proof condition** instead of initiating a new LW/PASS sequence.

## A. Original frozen model and the point of the argument

Use the original restricted GE05/GE06 longitudinal scalar action, positive auxiliary bath and separate quarter-source candidate, retaining the original historical v019j half coefficient as preserved evidence. For a fixed physical k>0, cosmic time t, a>0, H=dot(a)/a, C=2-K_B and \(\chi=\varphi+Q\alpha_A\), take
\[
 \dot\chi=QE_A+Qc_a^2\left[
 \Delta_A-\frac{3H\chi}{Q}
 +\frac{k^2}{3a^2R_A}(K_BE_A+C\chi)\right], \tag{1}
\]
\[
 K_B(\dot E_A+HE_A)=K_Q\chi
 -C\left[\dot\chi-QE_A+(H+Q)\chi\right]
 -\frac{\eta Q}{4}B_\chi, \tag{2}
\]
\[
 \ddot q_j+3H\dot q_j+\omega_j^2q_j
 =\omega_j\sqrt{w_j}\frac{k\chi}{a},
 \quad
 B_\chi=\sum_j\left[w_j\chi-\frac{a\omega_j\sqrt{w_j}}{k}q_j\right].
 \tag{3}
\]
Here \(K_B>0,Q>0,R_A>0,a>0,\omega_j>0,w_j\ge0\). The finite auxiliary initial state is **selected**, \(q_j(t_i)=\dot q_j(t_i)=0\), and is not implied by regularity alone. For the first theorem \(\Delta_A(t)\) is an externally specified regular source, NOT the as-yet-unproven full constrained cosmological operator. The original source coefficient 1/4 is the reduced action normalization, conditional on the established dictionary.

## Theorem A — the physical retarded branch has a well-defined one-sided first derivative at eta=0 despite a degenerate auxiliary action

**Assumptions**: equations (1)–(3) on a finite regular interval [t_i,T]; a,H,Q,K_Q,c_a²,R_A and the prescribed \(\Delta_A\) are continuous and bounded, the denominators in (1)–(3) remain nonzero, and the full normalized initial state of \(\chi,E_A,q_j,\dot q_j\) is independent of eta. Auxiliary Euler equations at eta>0 are divided by their common eta coefficient *before taking the selected continuous limit eta->0+*.

**Claim**: the unique selected solution \(y_\eta(t)=(\chi,E_A,q_1,\dot q_1,\ldots,q_N,\dot q_N)\) has a unique finite, right-sided derivative \(y_1(t)=\left.\partial_\eta y_\eta(t)\right|_{0^+}\) on [t_i,T]. Indeed for the reduced finite-dimensional normalized state,
\[
 \dot y_\eta=(A_0(t)+\eta A_1(t))y_\eta+b(t)\Delta_A(t), \tag{4}
\]
where \(A_1y_\eta\) has **only** the E component
\[
 (A_1y_\eta)_E=-\frac{Q(t)}{4K_B}B_\chi[y_\eta](t).\tag{5}
\]
Thus the map eta -> y_eta is analytic near eta=0 in this selected branch, and
\[
 \dot y_1=A_0y_1+A_1y_0,\qquad y_1(t_i)=0,\qquad
 y_1(t)=\int_{t_i}^{t}U_0(t,s)A_1(s)y_0(s)\,ds. \tag{6}
\]

**Proof**: substitute (1) for \(\dot\chi\) in (2). Every state equation becomes linear in \(y_\eta\), with eta entering only linearly through (3)'s finite \(B_\chi\) expression in the E equation. The original q/p equations have coefficients independent of eta **after normalization**, hence the finite-dimensional matrix formulation (4) holds for eta>0 and admits continuous extension to eta=0 along the selected branch. Uniformly bounded continuous coefficients on [t_i,T] give a unique fundamental matrix. The Peano–Baker series for the inhomogeneous IVP converges uniformly on finite intervals and is analytic in the complex parameter eta locally (indeed the evolution is entire in eta for fixed finite T and bounded coefficients). Differentiating (4) and the eta-independent initial data gives (6). This is a proof of the *one-sided reduced-branch derivative*, not of uniqueness among all possible unnormalized eta=0 action configurations. QED.

**Important obstruction explicitly exposed**: at eta=0 the original oscillator action has vanishing q/p Hessian. Therefore q_j are not uniquely dynamical **if one sets eta exactly to zero in the unnormalized variational principle first**. The limiting branch and the exactly eta=0 variational equations need not have the same solution set. Treating the normalized eta=0 auxiliary equations as physical without specifying continuation from eta>0 would be an unjustified step. The numerical CLASS branch has made this selection, but the full primordial physical theory has not proved it to be uniquely selected.

## Corollary A1 — a nonzero constrained-fluid source directly excites the reduced aether memory channel

Under Theorem A, assume at the starting time
\[
 \chi_i=E_{A,i}=q_{j,i}=\dot q_{j,i}=0,\qquad
 D_i:=Q_i c_{a,i}^2\Delta_{A,i}\ne0,\qquad
 W_b:=\sum_jw_j>0.
\tag{7}
\]
All eta dependence is in the dynamical coupling, not the starting state or prescribed Delta.

Then equations (1)–(3) give \(\dot\chi_{0,i}=D_i\), \(B_{\chi,0}(t_i)=0\) and
\[
 \dot B_{\chi,0}(t_i)=W_bD_i. \tag{8}
\]
In particular the **first strictly nonzero source response** obeys
\[
 \boxed{
 E_{A,1}(t_i+h)=-\frac{Q_iW_bD_i}{8K_B}h^2+O(h^3)
 \quad (h\downarrow0).
 }
 \tag{9}
\]
For nonzero \(Q_i,K_B,W_b,D_i\), the \(\eta\)-derivative of \(E_A\) is therefore nonzero for sufficiently small positive h.

**Proof**: the q/p initial data make the q term and its first derivative vanish at t_i, leaving (8). Because \(y_1(t_i)=0\), equation (6) gives \(\dot y_1(t_i)=A_1(t_i)y_0(t_i)=0\). In the E equation, differentiation in time at t_i then leaves only \(-Q_i\dot B_{\chi,0}(t_i)/(4K_B)\) as its second derivative; all \(A_0y_1\) and initial state derivatives vanish through that order. Taylor's formula yields (9). QED.

**Scope**: \(\Delta_A(t_i)\ne0\) is an explicit hypothesis. It is consistent with the earlier leading finite-k radiation-source expansion
\[
 \Delta_A\simeq-\frac{15+4R_\nu}{40}\Psi_0(k\tau)^2+\cdots,
\tag{10}
\]
when the retained leading term is nonzero, but this is **not** a completed all-species constrained primordial eigenvector. Corollary A1 proves a **local aether response**, not an Einstein-constraint-compatible Weyl mode, and gives no survey sensitivity. Note that an early Taylor onset and a large late-time amplitude are logically different claims.

## Theorem B — the exact diffeomorphism Noether identity identifies the missing full Ward closure

Let the *actual full covariant* action be diffeomorphism invariant and depend on the metric \(g_{\mu\nu}\), scalar \(\phi\), one-form aether \(A_\mu\), one-form auxiliary fields \(U_{j\mu}\), scalar multipliers and minimally coupled matter fields. Define Euler expressions for the **entire action including constraints and Lagrange multipliers**
\[
 {\cal E}_g^{\mu\nu}=\frac{2}{\sqrt{-g}}\frac{\delta S}{\delta g_{\mu\nu}},
 \quad {\cal E}_\phi=\frac{1}{\sqrt{-g}}\frac{\delta S}{\delta\phi},
 \quad {\cal E}_{V}^{\mu}=\frac{1}{\sqrt{-g}}\frac{\delta S}{\delta V_\mu}.
\]
Here \(V\in\{A,U_j\}\). Scalar multiplier and matter Euler terms are denoted \({\cal E}_{\lambda}\) and \({\cal E}_\psi\). This definition is **not** an assumption of the form of a missing NL0B 3+1 Hessian; it is the general covariant identity that any proposed complete action must satisfy.

**Off-shell Noether identity**:
\[
 \boxed{
 \nabla_\mu{\cal E}_g^{\mu}{}_{\nu}
 = {\cal E}_\phi\nabla_\nu\phi
 +\sum_V\left[
 {\cal E}_V^\mu(\nabla_\nu V_\mu-\nabla_\mu V_\nu)
 -V_\nu\nabla_\mu{\cal E}_V^\mu\right]
 +\sum_\lambda{\cal E}_{\lambda}\nabla_\nu\lambda
 +{\cal N}_{\nu}(\psi,{\cal E}_\psi).
 }\tag{11}
\]
The last term is the ordinary matter Euler contribution from the Lie derivative of its fields (for scalar matter it has the same scalar-gradient form; for tensors it includes derivative terms analogous to the V terms).

**Proof**: under an arbitrary compactly supported infinitesimal diffeomorphism generated by \(\xi^\nu\), use
\[
 \delta_\xi g_{\mu\nu}=2\nabla_{(\mu}\xi_{\nu)},\quad
 \delta_\xi\phi=\xi^\nu\nabla_\nu\phi,\quad
 \delta_\xi V_\mu=\xi^\nu\nabla_\nu V_\mu+V_\nu\nabla_\mu\xi^\nu .
\]
Insert the metric and field variational definitions into \(\delta_\xi S=0\), integrate every derivative of \(\xi\) by parts, and use the arbitrariness of \(\xi^\nu\). The metric term gives \(-\nabla_\mu{\cal E}_g^\mu{}_\nu\); each one-form term gives \({\cal E}_V^\mu(\nabla_\nu V_\mu-\nabla_\mu V_\nu)-V_\nu\nabla_\mu{\cal E}_V^\mu\). Collect matter and scalar-multiplier terms. QED.

**Strong consequence**: On a background and perturbation satisfying **the complete** Einstein metric equations, all complete aether/auxiliary Euler equations, all multiplier constraints and all minimally coupled matter Euler equations, identity (11) reduces to \({\cal E}_\phi\nabla_\nu\phi=0\). For the FLRW AeST background \(\dot{\bar\phi}=Q\ne0\), its time component implies
\[
 \boxed{{\cal E}_\phi^{(1)}=0}
 \qquad\text{provided all those other complete linear Euler equations hold.}
 \tag{12}
\]
Thus the scalar Ward/Euler equation is **not an independent extra dynamical condition on an already complete on-shell covariant solution**. However the implication CANNOT be reversed: merely showing the internally constructed CLASS fluid conservation or partial Einstein identities does not demonstrate (12), because the full aether, auxiliary, unit-timelike, multiplier and original scalar dictionary Euler expressions have **not** all been shown to coincide with the implemented code.

For the on-shell FLRW background with \(A_\mu=(-1,0,0,0)\), zero auxiliary background and vanishing background Euler expressions, the **linear time component** under on-shell multiplier/matter/auxiliary conditions reads, in the above sign convention,
\[
 Q\,{\cal E}_\phi^{(1)}
 =\left[\nabla_\mu{\cal E}_g^\mu{}_{0}\right]^{(1)}
 -\left[\nabla_\mu{\cal E}_A^\mu\right]^{(1)} .
 \tag{13}
\]
Equation (13) is an actionable **off-shell residual target** for a future joint action-vs-code proof: if the right-hand side reconstructed independently from the full action vanishes, then the scalar Euler follows. Equation (13) is not to be evaluated from the original CLASS E-row alone; the missing covariant aether multiplier equations are necessary.

## Proposition C — Einstein scalar Hamiltonian constraint is propagated once the full shear and conservation conditions hold

In the already archived total-stress scalar normalization, let \({\cal C}_H\) be the Hamiltonian residual and
\[
 {\cal C}_{\sigma}
 =\Phi-\Psi-\frac{9a^2}{2k^2}S_{\rm shear}
\]
be the shear residual with **all species** contributing. Under background Friedmann equations, total stress continuity/Euler evolution and the appropriate linear spatial Einstein evolution, the previously established exact constrained-source identity is
\[
 \dot{\cal C}_H+3H{\cal C}_H
 =\frac{Hk^2}{a^2}{\cal C}_{\sigma}. \tag{14}
\]
It integrates exactly to
\[
 \boxed{
 {\cal C}_H(t)
 =\left(\frac{a_i}{a(t)}\right)^3{\cal C}_H(t_i)
 +\frac{1}{a(t)^3}\int_{t_i}^t
 a(s)^3\,\frac{H(s)k^2}{a(s)^2}{\cal C}_{\sigma}(s)\,ds .
 }\tag{15}
\]
**Proof**: multiply (14) by a³ and integrate; it is equivalent to the earlier symbolic all-species source/constraint propagation calculation, not a new numeric certification. If shear residual and initial Hamiltonian residual vanish, (15) proves Hamiltonian preservation *within the assumed total stress + metric evolution*. This does NOT by itself prove the independent full AeST scalar Ward or that all actual CLASS approximation maps preserve the same equations.

## Scientific decision / remaining irreducible proof obligation

- **Proved within the reduced action**: existence of the selected retarded bath, analytic \(\eta\to0^+\) tangent despite the unnormalized auxiliary-action degeneracy, and the leading explicit nonzero \(E_{A,1}\) onset **when** \(D_i\ne0\).
- **Proved for any complete covariant action**: the precise diffeomorphism Noether identity (11), and scalar Euler redundancy on a complete on-shell Einstein+aether+auxiliary+matter solution with Q nonzero.
- **Proved conditionally under complete stress/spatial evolution**: homogeneous Einstein Hamiltonian constraint propagation when shear holds.
- **Not proved**: that the actual original full GE05/GE06+NL0B 3+1 variational Hessian and all multiplier variations reduce to the very same state-space operator as the v019+v019j+quarter CLASS code. There is no independently derived physical eta-dependent full radiation-era eigenvector or proof that \(Y_{{\rm ic},1}=0\). The local E response of Corollary A1 and the preliminary native full CLASS \(W_1/W_0=2.6238427503110188\times10^{-8}\) at one fixed k/z are **not** proof of an independent physical gravitational eigenmode or observational detectability.

**The decisive full proof remains one *joint* source-to-operator comparison of the actual full covariant quadratic action and its constrained early-time physical state**, not further separate toy-model PASS statements or numerical scans. In particular, one must establish the identity (13) with full action Euler expressions and show the physical retarded branch lies on the jointly propagated Einstein–AeST constraint manifold. Only then can a gauge-invariant nonzero Weyl overlap be elevated from a source-driven code number to a physical prediction.

### Frozen evidence reviewed

- [Retarded bath action and earlier operator statement](ge19_20261113_retarded_memory_proof_and_full_physics_obstruction.md)
- [Action-to-CLASS source matrix, original LW33 Ward/drift residual](ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md)
- [All species metric and primordial adiabatic source limitation](ge19_20261111_all_species_Einstein_operator_and_adiabatic_IC_block.md)
- [Total-stress constraint-projected analytic operator](../ge19/physics_gate/constraint_projected_joint_operator_20261112.py)
- [Positive bath energy balance and actual radiation forcing](ge19_20261112_retarded_bath_energy_amplification_gate.md)
- [Frozen full CLASS W1 one-point archive](../results/ge19_one_forced_tangent_20261113/GE19_ONE_FORCED_TANGENT_SCREEN.json)
