# GE19 — Gauge-null theorem and adjoint criterion for physical delayed Weyl memory

19 November 2026. Physics-first continuation. No CLASS, H4/Z21, DES, fitting, or numerical sweeps.

**Classification: RESTRICTED_GAUGE_NULL_PROVED / CONDITIONAL_ADJOINT_HISTORY_OVERLAP_PROVED / FULL_PHYSICAL_NONZERO_WEYL_NOT_PROVED / PHYSICS_BLOCK.**

## 1. Original ingredients and scope

Use the frozen reduced GE05/GE06 longitudinal scalar bath for fixed k>0, eta>0, finite regular FLRW interval, a(t)>0, positive frequencies omega_j>0 and weights w_j>=0, and selected no-free-bath retarded initial conditions q_j(t_i)=dot q_j(t_i)=0. Let chi=varphi+Q alpha_A and E_A=dot alpha_A+Psi. Original auxiliary equations and force:
\`\`\`math
\ddot q_j+3H\dot q_j+\omega_j^2q_j=\omega_j\sqrt{w_j}\frac{k\chi}{a},
\quad B_\chi=\sum_j\left[w_j\chi-\frac{a\omega_j\sqrt{w_j}}{k}q_j\right].
\`\`\`

These are **original reduced-action** statements, not a production CLASS or full 3+1 covariant equivalence claim. No claim that a generic finite-k physical adiabatic growing mode equals the pure-gauge mode.

## 2. Exact pure-diffeomorphism null theorem

On the original FLRW background phi_bar-dot=Q and aether A_mu=(-1,0,0,0), a pure infinitesimal coordinate-time shift T produces (in the documented longitudinal convention)
\`\`\`math
\varphi=Q T,\quad\alpha_A=-T,\quad\Psi=\dot T,\quad
\chi=\varphi+Q\alpha_A=0,\quad E_A=\dot\alpha_A+\Psi=0.
\`\`\`
The auxiliary background is zero, hence its Lie derivative under this diffeomorphism is zero. With retarded zero q/dot q initial conditions and chi=0, the auxiliary forcing vanishes identically. ODE uniqueness yields q_j=0 for every j; therefore
\`\`\`math
\boxed{B_\chi=0,\qquad B_{\chi,\mathrm{delayed}}=0}
\`\`\`
at all times on the finite regular interval. Thus the **reduced-action memory force cannot be excited by the pure coordinate/time-shift perturbation**. This is a necessary gauge-null check. It does not certify full gauge invariance of every implemented CLASS approximation or of the finite-k Weyl observer.

**More general necessary condition:** for the fixed retarded no-free-bath branch, chi_0 identically zero implies q_j,0 identically zero and the history-only bath source identically zero. Hence a nonzero delayed Weyl response requires a nontrivial chi_0 history. The converse is false: an excited chi can still have a zero projected Weyl signal through cancellation.

## 3. The exact adjoint kernel for a *completed* full physical state space

Make the explicit **unverified full-theory assumptions**: the actual unreduced covariant action, multiplier/lapse/shift constraints, all independent Euler equations, full species and correct adiabatic primordial branch define a smooth, constraint-reduced physical state z and eta=0 linear operator A_0(t); the quarter-source tangent can be represented by a physical projected input b_E(t) f(t); the gauge-invariant Weyl output is W_1(T)=ell_W(T) z_1(T); the eta derivative of the physical initial state is held identical in both source-comparison problems; no omitted eta-dependent observer or constraint maps contribute.

Define the **history-only source decomposition** using the same eta=0 background, trajectory, propagator and IC. The difference d(t)=z_1,ret(t)-z_1,inst(t) obeys
\`\`\`math
\dot d=A_0 d+b_E f_{\mathrm{hist}},\qquad d(t_i)=0,
\quad
f_{\mathrm{hist}}(t)=\frac{Q(t)a(t)}{4K_B}
\sum_jw_j\omega_j^2\int_{t_i}^tG_{R,j}(t,u)\frac{\chi_0(u)}{a(u)}\,du.
\`\`\`
The factor a(t) in f_hist is in the conformal-time normalization used for the prior full-physics theorem; if the independent variable is cosmic time, **remove this factor**. More precisely: write \`x\` for the chosen integration variable and define f_hist in the same-time normalization as A_0 and b_E. All formulas below are time-coordinate invariant under consistent conversion \`dx\`, \`A_0\`, and \`b_E f\`.

Let the backward adjoint satisfy
\`\`\`math
-\frac{d}{dx}\lambda(x)=A_0(x)^\mathsf{T}\lambda(x),\qquad
\lambda(X)=\ell_W(X)^\mathsf{T}.
\`\`\`
Then direct integration by parts of d/dx(lambda^T d)=lambda^T b_E f_hist gives
\`\`\`math
\boxed{\delta_h W(X)=\int_{x_i}^X\lambda(x)^\mathsf{T}b_E(x)f_{\mathrm{hist}}(x)\,dx.}\tag{A}
\`\`\`
This is equivalent to the prior forward double-Volterra Green formula, and **does not require** explicit assembly of the full two-time forward propagator once the complete physical A_0 has been established.

For a definite physical cosmological trajectory, a sufficient nonvanishing certificate is an interval with rigorously controlled signed contribution and a bound on contributions from the remainder such that the total signed integral does not include zero. If lambda^T b_E vanishes identically, the full delayed-only Weyl response is zero for every admissible bath history at that observation time. This is a structural obstruction, not a numerical tolerance issue.

The adjoint criterion remains **conditional**: A_0, b_E, the full initial-state derivative, and the observer map are currently not independently derived from the original complete covariant theory.

## 4. Constraint consistency in the fixed project normalization

The previously derived exact Einstein-constraint Weyl expression, *assuming the full total-source constraints hold*, is
\`\`\`math
W=-\frac{3a^2}{2k^2}\left(D_{\rm tot}+\frac{3aH}{k^2}T_{\rm tot}\right)-\frac{9a^2}{4k^2}S_{\rm shear}.
\`\`\`
Under the GE06 restricted stress dictionary it contains the electric entry +(K_B/2) E_A plus additional chi, deltaQ, varphi and ordinary species terms. This exhibits a structural channel, **not** proof of a nonzero constrained physical overlap. The adjoint ell_W must encode this **complete combination**, rather than read off just the E_A coefficient.

### Explicit conditional observability test

1. Derive the same full action's physical A_0 and b_E, including all multiplier and Einstein constraints.
2. Derive the coupled radiation-era finite-k adiabatic growing eigenvector (with the AeST pressureful relation delta_A/(1+w_A)=3 delta_gamma/4), and its eta derivative, with a declared no-free-bath sector.
3. Build the same physical Weyl ell_W from the total stress/shear constraint; verify it annihilates pure gauge perturbations.
4. Prove chi_0 is a genuinely non-gauge, nontrivial driven history for the physical mode; compute or bound the *signed* adjoint overlap (A).
5. Grant PHYSICS_GO only if full action consistency and nonzero history-only projected Weyl output are both established. If the overlap is identically zero or action equations fail, report PHYSICS_BLOCK rather than adjust an observational fit.

## 5. No false damping assertion from a finite positive bath

A finite lossless oscillator bath is passive in the proven static-energy sense, but **passivity does not imply decay**. For a=1, H=0 and a step chi(t)=chi_* for t>=0 with q_j(0)=dot q_j(0)=0, the forced oscillator solution for t>0 is
\`\`\`math
q_j(t)=\frac{\sqrt{w_j}k\chi_*}{\omega_j}(1-\cos\omega_j t),
\qquad B_\chi(t)=\chi_*\sum_jw_j\cos(\omega_j t).
\`\`\`
A finite bath exhibits persistent oscillatory transients; the vanishing zero-frequency steady transfer applies to appropriately prepared stationary/harmonic response, not instantaneous post-step relaxation in a nonexpanding lossless background. This rules out any unsupported claim of irreversible dissipation from the finite-bath passivity proof.

## Decision

**PROVED under fixed restricted-action hypotheses:** pure-gauge time-shift gives identically zero chi, E_A, q and memory force in the selected branch. A nontrivial chi history is necessary but not sufficient for delayed Weyl memory. Finite lossless bath need not dissipate.

**PROVED conditionally for a completed physical operator:** exact adjoint delayed Weyl overlap identity and null criterion.

**OPEN:** full unreduced action and physical constrained operator, finite-k primordial eigenmode, independent source projection, nonzero Weyl overlap, observability. Production PHYSICS_BLOCK remains. No new CLASS campaign.

## Frozen references
- [15 Nov Weyl constraint cancellation identity](ge19_20261115_constraint_eliminated_weyl_memory_cancellation_identity.md)
- [15 Nov delayed transfer double-Volterra condition](ge19_20261115_constrained_delayed_weyl_transfer_proof_gate.md)
- [14 Nov Noether and local retarded theorem](ge19_20261114_noether_constraint_and_eta0_retarded_branch_theorems.md)
- [11 Nov all-species primordial IC defect](ge19_20261111_all_species_Einstein_operator_and_adiabatic_IC_block.md)
- [P0 gate](https://github.com/dvlahek/aest-memory-gravity/issues/2)
