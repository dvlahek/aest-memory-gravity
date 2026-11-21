# GE19 — Radiation-era finite-k NLO source and a strict-dust memory-onset condition

**2026-11-21 — physics-first, no CLASS rerun, no DES fit.** A reproducible next-order derivation after researcher WSL confirmation of the previous **31/31** coupled leading \`O(y_m)\` photon–baryon–neutrino–AeST-like seed. The researcher's original [31-gate JSON](../results/ge19_physical_baryon_Exp_leading_seed_20261121_r1.json) and [log](../results/ge19_physical_baryon_Exp_leading_seed_20261121_r1.log) have been archived **byte-exactly** with original Git blobs \`917d316a6b1c80bfca41ab0c06b985a01d4f6ccb\` and \`e30e86434847cfc9df1a26ffc7cd3a8b0fb70dda\`, respectively. The old result stays strictly leading \`k\tau\to0\`.

The **new** source-locked script [radiation_neutrino_finite_k_NLO_memory_source_20261121.py](../ge19/physics_gate/radiation_neutrino_finite_k_NLO_memory_source_20261121.py) checks 37 exact symbolic identities. The algebra was independently evaluated in a local SymPy prototype **37/37 PASS**; canonical researcher WSL source-locked run is pending.

**Classification: RADIATION_ONLY_NLO_NEUTRINO_HIERARCHY_AND_DUSTLIKE_TEST_AEST_SOURCE_PASS / FULL_COUPLED_O(y_m(k\tau)^2)_AND_ACTION_WARD_OPEN / GRAVITATIONAL_MEMORY_OBSERVATION_NOT_ESTABLISHED.**

## 1. Full first gradient correction in exactly radiation-dominated Einstein–Boltzmann theory

This subsection temporarily takes \`y_A=y_b=0\` in the *metric/background*, retaining a **non-gravitating pressureless AeST-like test fluid** to find the first regular source seed. It includes self-gravitating photons and collisionless massless neutrinos with \`R_\nu=\rho_\nu/\rho_r\`, and no neutrino masses or baryon loading at this order. \`x=k\tau\ll1\`, \`\mathcal H=1/\tau\`, \`a²\rho_r=1/\tau²\` in the existing normalized Einstein convention; \`P=\Psi_0\`.

Write \`\Phi=(1+2R_\nu/5)P+\Phi_2 x²+\cdots\`, \`\Psi=P+\Psi_2x²+\cdots\`. Solving the Einstein Hamiltonian, momentum, shear and spatial trace equations **jointly with the neutrino Boltzmann hierarchy** yields
\`\`\`math
\boxed{\frac{\Phi_2}{P}=-\frac{56R_\nu^2+580R_\nu+525}{630(2R_\nu+25)}},\qquad
\boxed{\frac{\Psi_2}{P}=\frac{56R_\nu^2+10R_\nu-525}{630(2R_\nu+25)}}.
\`\`\`
The neutrino anisotropic stress has \`\sigma_\nu=(P/15)x²+\sigma_{\nu,4}x⁴+\cdots\`, and its \`x⁴\` coefficient is **needed** because the Einstein shear relation divides \`\sigma_\nu\` by \`k²\tau²=x²\`. Keeping only the \`x²\` neutrino quadrupole would produce an incorrect \`\Phi_2-\Psi_2\`. In Ma–Bertschinger Newtonian gauge:
\`\`\`math
\boxed{\frac{\sigma_{\nu,4}}{P}=-\frac{56R_\nu+295}{1890(2R_\nu+25)}},\qquad
\boxed{F_{\nu3}=\frac{2P}{105}\,x³+\cdots.}
\`\`\`
The explicitly audited hierarchy is
\`\`\`math
\delta_\nu'=-4\theta_\nu/3+4\Phi',\quad
\theta_\nu'=k²(\delta_\nu/4+\Psi-\sigma_\nu),\quad
\sigma_\nu'=4\theta_\nu/15-3kF_{\nu3}/10,\quad
F_{\nu3}'=6k\sigma_\nu/7+O(k^5\tau^4).
\`\`\`
The photon hierarchy at this order has \`\sigma_\gamma=0\` (tight-coupled radiation), and the test-AeST-like dust uses \`\delta_A'=-\theta_A+3\Phi'\`, \`\theta_A'+\mathcal H\theta_A=k²\Psi\`. This is the standard collisionless-neutrino linear framework of Ma & Bertschinger (1995), astro-ph/9506072; no claim of a novel neutrino perturbation law.

Independent checks include the Einstein **spatial trace WITH the correct \`+k²(\Phi-\Psi)/3\` slip term** and the independent time/momentum constraints. All corresponding coefficients through the claimed order vanish.

## 2. The first explicit comoving AeST-like matter source

The regular pressureless test matter has
\`\`\`math
\delta_A=-\frac32P+\left(3\Phi_2-\frac14P\right)x²+\cdots,\quad
\theta_A=k²\tau\left(\frac12P+\frac{\Psi_2}{4}x²\right)+\cdots.
\`\`\`
Therefore the **comoving**, not the raw, density perturbation is
\`\`\`math
\boxed{
\Delta_A=\delta_A+\frac{3\mathcal H\theta_A}{k²}
=-\frac{15+4R_\nu}{40}P(k\tau)²+O((k\tau)^4).
}
\`\`\`
This **independently reconstructs** the previously archived coefficient from the full NLO radiation hierarchy, not a new full AeST pressureful result. For illustrative \`R_\nu=0.41\`, the coefficient is \`-0.416 P\`. Standard photon and neutrino comoving contrasts are **different** at this order:
\`\`\`math
\Delta_\gamma=-\frac{2(4R_\nu+15)}{45}P(k\tau)^2+\cdots,\qquad
\Delta_\nu=-\frac{2(4R_\nu+17)}{45}P(k\tau)^2+\cdots.
\`\`\`
Their weighted sum exactly satisfies the full radiation comoving Einstein constraint
\`\`\`math
(1-R_\nu)\Delta_\gamma+R_\nu\Delta_\nu
=-\frac23(1+2R_\nu/5)P(k\tau)^2+O((k\tau)^4).
\`\`\`

**Scope boundary:** this is \`O((k\tau)^2)\` **at zero matter fraction**. The prior 31-gate result is \`O(y_m)\` **at leading gradient order**. These two calculations are independent edges of a *double expansion*; their yet-unknown **mixed** \`O(y_m(k\tau)^2)\` coefficients, baryon loading, pressureful AeST scalar/aether eigenvector and full Ward identity must not be silently imported from either edge.

## 3. Important original-action selection rule: finite comoving density does not guarantee memory

From the previously source-locked original reduced action, \`X=\chi/Q\`, \`E=E_A\`, \`C=2-K_B\`, \`c=c_a^2\`:
\`\`\`math
\dot X=E+cF,\qquad
\dot E=-HE+\frac{Q}{K_B}
\left[\{K_Q-C(H+Q-3Hc)\}X-CcF-\frac{\eta}{4}B_\chi\right],
\`\`\`
\`\`\`math
F=\Delta_A+\frac{k²}{3a²R_A}(K_BE+CQX),\quad
B_\chi=W_b QX-\frac{a}{k}\sum_j\omega_j\sqrt{w_j}q_j,
\quad
\ddot q_j+3H\dot q_j+\omega_j²q_j=\omega_j\sqrt{w_j}kQX/a.
\`\`\`
At any regular initial point with **selected** no-independent-mode values \`X=E=q_j=\dot q_j=0\`, the *immediate* forcing is **exactly**
\`\`\`math
\boxed{\dot X=c\,\Delta_A,\qquad
\dot E=-\frac{CQc}{K_B}\Delta_A.}
\`\`\`
Thus \`Delta_A\ne0\` is **necessary for this density-driven source but not sufficient for nonzero memory**. In the **strict formal dust limit** \`c=0\`, the zero longitudinal/scalar/auxiliary state is an invariant solution of the restricted system for any externally supplied \`Delta_A\`; no bath memory is excited *from these zero states*. This does **NOT** establish that the full finite-\`k\` original action requires those zero initial X/E, that the c→0 limit of the Exp action is nonsingular, or that all AeST modes have zero memory. Independent scalar/aether initial modes could alter the conclusion.

For our frozen Exp background, \`0<c_a²\le3.5355e-14\` **globally**, but this bound **cannot** simply be transferred to \`W_{1,\rm delayed}\` because other coefficients can grow, perturbation ratios can be singular, the primordial interval is long, and the initial physical eigenvector has not been selected.

**This is the decisive risk as well as an opportunity:** the original theory requires a physically derived finite-\`k\` initial scalar/aether mode; assuming a freely excited memory mode could manufacture a signal, while assuming it vanishes without the Ward/Frobenius derivation could erase a real one. The previously derived small historical \`W_{1,\rm delayed}=-1.2006039315857457\times10^{-10}\` at \`k=0.06732117, z=0.5\` stays a **provisional CLASS implementation tangent**, not a physical GR-versus-memory measurement.

## 4. Single next action

Solve **the mixed finite-\`k\` coupled Einstein–AeST–photon–baryon–neutrino initial-value problem** with both expansions active, and the original scalar/aether Ward, rather than more numerical source sweeps:
1. freeze the original Exp background, \`R_A=QK_Q/3\`, the actual radiation/particle contents and the original quarter bath source;
2. derive regular finite-\`k\` Newtonian/Cauchy primordial seed in \`(\Phi,\Psi,\delta_i,\theta_i,\sigma_\nu,X,E_A,q_j,\dot q_j)\`, showing \`O(y_m(k\tau)^2)\` compatibility with all constraints and adiabatic entropy;
3. use exactly this initial eigenvector and retarded no-free-bath choice to propagate the physical \`W_{1,\rm delayed}\`;
4. only if physical/Ward gates pass, return to predeclared DES Y3 MagLim4 × Source4 geometry. Do not tune to improve an expected faint signal.

**FULL_PHYSICS_GO = FALSE; DES_DETECTION = FALSE.**

## References
- Ma, C.-P. and Bertschinger, E. (1995). *Astrophys. J.* 455, 7–25. https://arxiv.org/abs/astro-ph/9506072
- [Researcher-verified leading baryon/Exp symbolic seed](../results/ge19_physical_baryon_Exp_leading_seed_20261121_r1.json)
- [Original exact reduced scalar/aether driven operator](ge19_20261119_exact_driven_X_E_constrained_source_bridge.md)
- [Earlier 31-gate baryon/Exp physics priority](ge19_20261121_universal_baryon_Exp_physics_priority.md)
