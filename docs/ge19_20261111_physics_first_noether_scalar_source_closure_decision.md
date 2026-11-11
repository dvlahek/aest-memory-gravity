# GE19 — one physics-first closure decision: scalar Euler is discriminating; Einstein constraint checks alone are not

**11 November 2026 | Research decision, not a new LW step**  
**Status:** \`REDUCED_LINEAR_SCALAR_QUARTER_COMPATIBILITY_PROVEN / FULL_ACTION_TO_CLASS_PRODUCTION_OPEN / NO_DES_OBSERVATION\`.

This note integrates only source-anchored original action/equation evidence, the genuine researcher LW33 WSL results, the independently collected one-point positive-eta candidate outputs and a direct general diffeomorphism Ward derivation. It does **not** run CLASS, re-fit DES, establish the full linear operator, re-label an old PASS or claim an observational detection.

## 1. Scientific question and exact action

The goal is **not** simply to enforce numerical preservation of the CLASS Einstein constraints. It is to determine whether the original covariant *AeST+NL0B* equations produce exactly the **same scalar/aether/metric/effective-fluid evolution** as one specified CLASS implementation with physical source \(\eta\).

The published AeST action starts with
\[
S_A=\frac1{16\pi\widetilde G}\int d^4x\sqrt{-g}\,
\left[R-\frac{K_B}2F_{\mu\nu}F^{\mu\nu}
+2(2-K_B)J^\mu\nabla_\mu\phi
-(2-K_B)\mathcal Y-\mathcal F(\mathcal Y,\mathcal Q)
-\lambda(A^\mu A_\mu+1)\right]+S_m[g],
\]
where \(\mathcal Q=A^\mu\nabla_\mu\phi\), \(X_\mu=(g_\mu{}^\nu+A_\mu A^\nu)\nabla_\nu\phi\), \(\mathcal Y=X^2\). The frozen NL0B addition is
\[
S_{\rm bath}=\frac1{16\pi\widetilde G}\int d^4x\sqrt{-g}\,
\frac14\sum_j\Big[(\mathscr D_A U_j)^2-
(\omega_j U_j-\sqrt{\eta w_j}\,X)^2\Big]
+\int\sqrt{-g}\sum_j \mu_j(A^\mu U_{j\mu}),
\]
with the projected derivative and the unit-timelike/aether-orthogonal constraints. This auxiliary-vector action is the **selected completion**, not a claim of unique completion; no observed residual determined its normalization. In the locked small-\(\mathcal Y\) sector \(\mathcal J(\mathcal Y)\sim\mathcal Y^{3/2}\) contributes only starting at cubic field order and does not introduce a new quadratic linear-scalar action term on FLRW.

The published AeST references establish the baseline theory, not the validity of the **new** NL0B/CLASS coefficient:
- C. Skordis and T. Złośnik, *Phys. Rev. Lett.* **127**, 161302 (2021), DOI 10.1103/PhysRevLett.127.161302.
- M. Bataki, C. Skordis and T. Zlosnik, *Phys. Rev. D* **110**, 044015 (2024), DOI 10.1103/PhysRevD.110.044015; full AeST 3+1 Hamiltonian and constraints **without claiming a proof of this particular NL0B CLASS bridge**.

## 2. Exact diffeomorphism Noether identity: what it genuinely ensures

Use a definite convention for the **total action**, including metric, aether, scalar, all auxiliary covectors, Lagrange-multiplier scalars and minimally coupled matter fields:
\[
\delta S=\int d^4x\sqrt{-g}\left[
\frac12\mathcal E_g^{\mu\nu}\delta g_{\mu\nu}
+\mathcal E_A^\mu\delta A_\mu+\mathcal E_\phi\delta\phi
+\sum_j\mathcal E_{U_j}^\mu\delta U_{j\mu}
+\mathcal E_\lambda\delta\lambda+
\sum_j\mathcal E_{\mu_j}\delta\mu_j+
\text{matter Euler terms}\right].
\]
(The normalization of the Einstein equation is **built into** \(\mathcal E_g\); no separate numerical \(8\pi G\) factor is silently assumed.) For an infinitesimal compactly supported diffeomorphism \(\xi\), the geometric Lie variations are
\[
\delta_\xi g_{\mu\nu}=2\nabla_{(\mu}\xi_{\nu)},\quad
\delta_\xi A_\mu=\xi^\rho\nabla_\rho A_\mu+A_\rho\nabla_\mu\xi^\rho,\quad
\delta_\xi U_{j\mu}=\xi^\rho\nabla_\rho U_{j\mu}+U_{j\rho}\nabla_\mu\xi^\rho,
\]
and \(\delta_\xi\phi=\xi^\rho\nabla_\rho\phi\), with the same scalar transformation for \(\lambda,\mu_j\).

Integrating by parts **once**, with no field equations imposed, gives the off-shell identity
\[
\boxed{\begin{aligned}
\nabla_\mu\mathcal E_g^\mu{}_\nu={}&
\mathcal E_\phi\nabla_\nu\phi
+\mathcal E_A^\rho(\nabla_\nu A_\rho-\nabla_\rho A_\nu)
-A_\nu\nabla_\rho\mathcal E_A^\rho\\
&+\sum_j\big[
\mathcal E_{U_j}^\rho(\nabla_\nu U_{j\rho}-\nabla_\rho U_{j\nu})
-U_{j\nu}\nabla_\rho\mathcal E_{U_j}^\rho
\big]\\
&+\mathcal E_\lambda\nabla_\nu\lambda+
\sum_j\mathcal E_{\mu_j}\nabla_\nu\mu_j
+\mathcal I_\nu^{\rm matter}.
\end{aligned}}\tag{N}
\]
Here \(\mathcal I_\nu^{\rm matter}\) denotes the analogous Euler terms from the chosen matter variables (zero on the matter field equations). This identity is a direct consequence of covariance, **independent of the numeric coefficient** of the source in an unrelated, possibly inconsistent effective-fluid ODE.

**Conditional consequence:** on *all* true metric, aether, auxiliary, multiplier and matter Euler equations, Eq. (N) yields \(\mathcal E_\phi\nabla_\nu\phi=0\). On a regular FLRW branch with \(Q=\dot{\bar\phi}\ne0\), the time component then implies the scalar Euler equation. Thus the scalar field equation is not an additional independent on-shell degree of freedom **when the full original action equations are actually enforced**. This does *not* mean that any arbitrary modified CLASS E equation is therefore action-equivalent.

**Important limit:** the covariant Noether identity alone does not demonstrate that the **implemented** CLASS time evolution reproduces \(\mathcal E_g=\mathcal E_A=\mathcal E_U=0\). Continuum Hamiltonian/momentum propagation is a consequence **once those full equations hold**, but numerical propagation on an incompletely matched effective-fluid implementation is not a proof of the missing action equivalence.

## 3. The actual restricted linear scalar equations already derived from the fixed action

For a scalar Fourier mode \(k>0\) on homogeneous/isotropic FLRW, rotate \(k\) along the longitudinal coframe axis. Keep independent lapse, shift, longitudinal/transverse spatial scale, scalar \(\varphi\), aether rapidity and longitudinal bath amplitude in the quadratic action **before imposing Newtonian gauge**. The projected covariant bath derivative reduces to the original GE05 longitudinal amplitude derivative on this sector. LW30–LW32 are consistent with this constrained algebraic reduction, but it is not a complete proof of all production CLASS approximation branches.

With proper cosmic time \(t\), \(H=\dot a/a\), \(C=2-K_B\), define
\[
E_A=\dot\alpha+\Psi,\quad\chi=\varphi+Q\alpha,\quad
\delta Q=\dot\varphi-Q\Psi,
\]
\[
D_A^{\rm action}=\tfrac13\left[
QK_{QQ}\delta Q-\frac{k^2}{a^2}(K_BE_A+C\chi)\right],
\qquad
T_A=\tfrac{QK_Q}{3}\frac{k^2\varphi}{aQ}.
\]
The original **restricted AeST-only** metric rows are (LW30/31)
\[
\mathcal C_H^{A}=\frac{k^2}{a^2}\Phi+3H(\dot\Phi+H\Psi)+\frac32D_A^{\rm action}=0,
\]
\[
\mathcal C_M^{A}=\dot\Phi+H\Psi-\frac{3aT_A}{2k^2}=0,\qquad
\mathcal C_{\rm shear}^{A}=\Phi-\Psi=0\quad(k\ne0),
\]
where the last equality holds only **without** ordinary-species anisotropic stress. In the full observed cosmology, minimally coupled baryons/photons/neutrinos add their density/momentum/shear contributions, and the **total spatial Einstein trace equation** and their perturbation feedback must be matched with the same conventions.

The original restricted scalar charge \(J_\phi\) is
\[
J_\phi^t=2a^3K_{QQ}\delta Q-6a^3K_Q\Phi,\qquad
J_\phi^x=ika[2C(E_A-\chi)+2K_Q\alpha-\eta B_\chi/2],
\]
\[
\mathscr S_\phi=\dot J_\phi^t-ak^2[2C(E_A-\chi)+2K_Q\alpha-\eta B_\chi/2].
\]
The normalized action-projected aether row is
\[
\boxed{K_B(\dot E_A+HE_A)=K_Q\chi-
C[\dot\chi-QE_A+(H+Q)\chi]-\frac{\eta Q}{4}B_\chi.}\tag{E}
\]
The historical frozen v019j CLASS row instead inserts \(-\eta QB_\chi/2\) in Eq. (E)'s right-hand side, while keeping the old fluid and phase dictionaries unchanged.

## 4. The decisive conditional proposition: the scalar charge tests the source factor

Introduce independent residuals \(R_D,R_E,R_\chi,R_{\rm geo},R_\rho\) exactly as defined in [LW33](ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md); \(R_\rho=D_A-D_A^{\rm action}\), and \(R_E\) uses an arbitrary putative source coefficient \(\gamma\), not just 1/4 or 1/2. The already executed exact original reduced-model identity is
\[
\boxed{\begin{aligned}
\mathscr S_\phi={}&\frac{6a^3}{Q}R_D
+\frac{2ak^2K_B}{Q}R_E
+\frac{2ak^2C}{Q}R_\chi
+\frac{2ak^2K_Q}{Q}R_{\rm geo}\\
&-\frac{6a^3}{Q}\dot R_\rho
-\frac{18a^3H}{Q}R_\rho
+\frac{a\eta k^2B_\chi}{2}(1-4\gamma).
\end{aligned}}\tag{S}
\]

**Proposition (strictly restricted scope).** Assume a regular, nonzero \(a,Q,k,\eta,B_\chi\), the above original quadratic scalar action and *unchanged* action-to-CLASS dictionaries, and \(R_D=R_E=R_\chi=R_{\rm geo}=R_\rho=\dot R_\rho=0\). Then \(\mathscr S_\phi=0\) **if and only if** \(\gamma=1/4\). For the frozen historical half source,
\[
\boxed{\left.\mathscr S_\phi\right|_{\gamma=1/2}=-a\eta k^2B_\chi/2\ne0.}
\]
**Proof:** substitute the stated residuals into (S); under the stated nonzero conditions its final factor is zero iff \(1-4\gamma=0\). No metric/shear/Noether assumption is used to erase the source term, and there is no appeal to a data fit. This is a **mathematical proposition about the fixed reduced action/dictionary**; it is not a newly executed computation or a full unreduced multi-species theorem.

## 5. Why a PASS of Einstein constraint propagation would be insufficient

The frozen CLASS effective-fluid energy and momentum equations give (LW15, in conformal time)
\[
J_D^{\rm code}=D_A'+3\mathcal H(D_A+P_A)+T_A-3R_A\Phi'=0,
\]
\[
J_T^{\rm code}=T_A'+4\mathcal H T_A-k^2P_A-k^2R_A\Psi=0.
\]
These identities are true *for any injected aether E force*, because their derivation uses only the original constructed density/velocity rows; no \(E_A'\) action equation enters them.

**Therefore:**
- Passing \(\mathcal C_H,\mathcal C_M\) and a generic Bianchi/CLASS fluid-Ward check is **necessary but not discriminating** for \(\gamma\). An arbitrary injected E source can satisfy those implemented conservation forms while violating \(\mathscr S_\phi=0\) of the specified action.
- Checking **only** the quarter C-source literal anchor, \(\eta=0\) byte-identity or finite-\(\eta\) native Weyl difference is also **not discriminating** for full action correctness.
- One **real** source-to-theory acceptance must independently reconcile (E) and (S) with the complete constrained metric/effective-fluid **including the spatial trace, scalar/aether/auxiliary Euler and all active ordinary species**, with correct initial-value and gauge mapping. Algebraically imposed fluid conservation is **not** a substitute for the scalar Euler equation.
- At that point a **single** time-resolved direct scalar-charge/Einstein-constraint residual trace on the versioned candidate could provide an implementation check; a perfect constraint trace by itself still would not establish that the action-to-code map was correct.

The mathematical Noether identity (N) **explains why** all these equations must be compatible in the true theory. It does not license artificially adding a density/velocity term to cancel the half-source residual, nor independently prove that quarter is the only possible full covariant effective-fluid representation.

## 6. What is complete, what is still missing, and the one honest decision

| Required physics | Evidence | Decision |
|---|---|---|
| Original linear scalar positive bath, projector and local source Hessian | NL0B, GE05, LW25/LW29 | **Supported** within restricted scalar sector |
| Unit timelike aether and auxiliary covector normal elimination | LW32 regular branch | **Supported** for algebraic multipliers |
| Hamiltonian/momentum and traceless scalar spatial Einstein rows | LW30/LW31 | **Restricted action PASS** |
| Complete off-shell scalar charge/CLASS residual identity | Original researcher LW33 WSL (19/19, 7 locks) | **Restricted exact PASS; quarter necessary** |
| General covariance/Ward identity of covariant action | (N), geometric derivation in this note | **Formal continuum identity**, not code equivalence |
| Fully independent spatial Einstein **trace**, all-species field feedback, original auxiliary/matter Euler-to-C-row map and gauge/IC branches | No combined original action-to-CLASS demonstration | **OPEN** |
| Physical source-normalized, causal \(\partial_\eta P_{d_mW}(k,z)\) | Native CLASS outputs alone do not establish | **BLOCK** |
| Real DES Y3 \(\gamma_t\) including line-of-sight, bias/IA/photo-z/covariance | No verified full forward/likelihood | **BLOCK / no detection** |

The archived action-quarter code candidate indeed compiles, agrees exactly with historical code for \(\eta=0\), and produces distinct tiny native \(d_m,\Phi,\Psi\) for \(\eta=.01,z=.5\). **The signed 49-node k signal is jagged with many sign reversals, and simple factor-two source-to-response scaling is unsupported.** This must **not** be called a converged physical memory prediction without an independent error estimate. Its small apparent amplitude does not settle theory normalization or survey sensitivity.

**Next step is a theory decision, not a numerical sweep:** construct one joint action-derived **spatial Einstein trace + scalar/aether/auxiliary effective-fluid and matter-source map** with all explicit \(\eta\) terms, and compare it to the actual CLASS state evolution. A contradiction is legitimate \`PHYSICS_BLOCK\`; a complete all-rows equivalence allows only the **separate quarter candidate** to advance to a bounded physical transfer calculation. At present the evidence supports \`PHYSICS_BLOCK\`, with the restricted source-normalization proposition as a self-contained potential theoretical result.

No extra LW34/LW35 scripts, no new CLASS jobs or GitHub Actions, no DES tuning.

## Primary repository evidence

- [Original AeST action](nl0_equation_audit.md), [fixed NL0B](nl0b_predata_covariant_memory_completion.md), [NL0C Y branch](nl0c_y_sector_weakly_nonlinear_result.md)
- [LW15 implemented-fluid Ward insufficiency](ge19_lw15_effective_fluid_consistency_vs_covariant_action_noether_2026-11-10.md)
- [LW29 kinetic factor-two normalization](ge19_lw29_covariant_3d_quadratic_action_normalization_and_nl0b_erratum_2026-11-10.md)
- [LW30 ADM Hamiltonian and momentum](ge19_lw30_original_gr_aest_adm_scalar_constraints_class_bridge_2026-11-10.md)
- [LW31 traceless spatial Einstein](ge19_lw31_original_action_spatial_traceless_Einstein_shear_2026-11-10.md)
- [LW32 multiplier elimination](ge19_lw32_covariant_unit_aether_auxiliary_multiplier_exact_elimination_2026-11-10.md)
- [LW33 complete reduced off-shell scalar identity](ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md)
- [2026-11-10 integrated scalar-mode embedding](ge19_single_scalar_3plus1_embedding_and_candidate_source_2026-11-10.md)
- [P0 physical source equivalence issue](https://github.com/dvlahek/aest-memory-gravity/issues/2)
