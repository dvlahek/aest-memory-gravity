# GE19 — Exact original-action X–S subsystem: stress-null initial data are lifted dynamically

**22 November 2026. Physics-first theorem after actual researcher WSL source-locked 13/13 and corrected 17/17.** No CLASS run or numerical scan.

## 0. Frozen experimental evidence

The researcher's source-locked [Exp constrained source JSON](../results/ge19_Exp_constraint_regular_source_20261122_r1.json), SHA-256 \`ed7af989df0c5995e18762f9f78eb19a7dd3a6a3a2dbbcb670f79934a897e8bc\`, and [WSL log](../results/ge19_Exp_constraint_regular_source_20261122_r1.log), SHA-256 \`a169eabb1742269da4bc49cc8ac05976b14c085514d44a7e28b0d41c641b0c25\`, are archived byte-exact: Git blobs \`eaba5c37f240d7aeb333e6e6c9a15465c9938814\` and \`06634e2c2e567e144aa9f59af7c1c84cc82a2c89\`. 13/13 symbolic checks and 4/4 source locks passed; \`FULL_PHYSICS_GO=False\`. The repeated prior 17/17 F3/causal-onset JSON and log are bit-for-bit duplicates of previously archived r2 files; no rearchive was needed.

**Scope:** the following equations are exact within the previously established original *restricted* GE05/GE06+NL0B longitudinal scalar action and assumed Einstein comoving constraint. Not a proof of unreduced covariant 3+1, actual primordial mode, full scalar Ward propagation or observable lensing.

## 1. Transform the source-locked reduced field system once, without dust or small-c expansion

Let \`X=chi/Q\`, \`E=E_A\`, \`S_A=K_B E+C Q X\`, \`C=2-K_B\`, \`R_A=QK_Q/3\`, \`c=c_a²=K_Q/(QK_QQ)\`, and \`\dot Q=-3HcQ\`. From the original equations
\`\`\`math
\dot X=E+cF,\quad
\dot E=-HE+\frac{Q}{K_B}
\bigl([K_Q-C(H+Q-3Hc)]X-CcF-\frac{\eta}{4}B_\chi\bigr),
\quad
F=\Delta_A+\frac{k²}{3a²R_A}S_A,
\`\`\`
differentiate \`S_A\` without applying any initial conditions. The two separate \`CcQF\` terms cancel **exactly**:
\`\`\`math
\dot S_A=(C Q-K_BH)E+Q[K_Q-C(H+Q)]X-\frac{\eta Q}{4}B_\chi.
\`\`\`
Eliminate \`E=(S_A-CQX)/K_B\`, use \`C+K_B=2\`:
\`\`\`math
\boxed{\dot X=-\frac{CQ}{K_B}X+
\left(\frac{1}{K_B}+\frac{k²}{a²Q²K_{QQ}}\right)S_A+c\Delta_A,}\tag{1}
\`\`\`
\`\`\`math
\boxed{\dot S_A=\left(\frac{CQ}{K_B}-H\right)S_A+
Q\left(K_Q-\frac{2CQ}{K_B}\right)X-\frac{\eta Q}{4}B_\chi.}\tag{2}
\`\`\`
These **two variables are coupled to the causal bath** \`B_\chi=W_b QX-(a/k)\sum_j\omega_j\sqrt{w_j}q_j\`; (1)–(2) are **not** a closed physical two-variable Einstein–Boltzmann cosmology without bath initial history, ordinary species evolution and the original scalar/AeST dictionary. But their exact form exposes the real source channels.

The density-only drive \`c\Delta_A\` enters \`X\`; the combination \`S_A\` receives it only through dynamic evolution of \`X\`. The gradient factor \`k²/(a²Q²K_{QQ})\` is finite in the pinned Exp positive branch, so the tiny scalar sound speed does **not** automatically suppress a physical \`S_A\` mode.

## 2. Stress-null mode is not an algebraic gauge freedom

At one finite regular time, consider the already identified same-instant stress-null *variation*
\`\`\`math
\delta\chi=\epsilon,\qquad \delta E=-\frac C{K_B}\epsilon,\qquad
\delta\varphi=\delta(\delta Q)=\delta q_j=0.
\`\`\`
Then \`\delta X=\epsilon/Q\` and \`\delta S_A=0\`. At equal metric/ordinary stress and bath coordinate values, Eq. (2) gives the **next time derivative difference**
\`\`\`math
\boxed{\delta\dot S_A(t_i)
=\epsilon\left[K_Q-\frac{2CQ}{K_B}-\frac{\eta QW_b}{4}\right]_{t_i}.}\tag{3}
\`\`\`
For generic background parameters this is **nonzero**, even though the instantaneous stress difference vanishes. Hence equality of instantaneous Einstein stress does not imply equality of the next state: the hidden longitudinal mode can become dynamically visible.

**Important:** This does *not* prove that arbitrary \`\epsilon\` is an admissible regular growing primordial mode. A mode that is stress-null at one Cauchy instant may be excluded by regularity or the full action/multiplier/Ward conditions. Conversely, it is not valid to set \`\epsilon=0\` merely because instantaneous stress or spatial scalar current is nonzero.

## 3. Local Ward/current-to-stress identity and the quarter/half normalization

The original reduced scalar Noether current derived by LW33 has at the same initial variation (with equal \`q_j\`)
\`\`\`math
\frac{\delta J_\phi^x}{ika\epsilon}
=2\frac{K_Q}{Q}-\frac{4C}{K_B}-\frac{\eta W_b}{2}.
\`\`\`
Comparing with (3) gives the **exact local bridge**
\`\`\`math
\boxed{\delta\dot S_A=\frac{Q}{2ika}\,\delta J_\phi^x,}\tag{4}
\`\`\`
**for this specific stress-null variation and the original quarter-normalized E force**. This is *not* the full off-shell covariant Noether identity; the temporal scalar-charge derivative and multiplier/aether/Einstein terms are still required.

More generally write the aether E force as \`-\gamma\eta Q B_\chi/K_B\`. The same algebra gives
\`\`\`math
\boxed{\delta\dot S_{A,\gamma}
-\frac{Q}{2ika}\delta J_\phi^x
=(1/4-\gamma)\eta QW_b\epsilon.}\tag{5}
\`\`\`
Therefore \`\gamma=1/4\` is uniquely compatible with this original-action local bridge for generic nonzero \`\eta,W_b,Q,\epsilon\`, while the historical \`\gamma=1/2\` has a residual \`-\eta QW_b\epsilon/4\`. This is an independent *local* manifestation of the already archived LW33 whole scalar-current mismatch; **do not count it as an independent full Ward closure.**

## 4. Zero-state onset and the physical primordial obstruction

Under **additional assumed** finite-time boundary data \`X_i=S_{A,i}=q_{j,i}=\dot q_{j,i}=0\`, Eqs. (1)–(2) imply:
\`\`\`math
\dot X_i=c_i\Delta_{A,i},\qquad \dot S_{A,i}=0,
\`\`\`
\`\`\`math
\boxed{\ddot S_{A,i}
=Q_ic_i\Delta_{A,i}
\left[K_{Q,i}-\frac{2C Q_i}{K_B}
-\frac{\eta Q_iW_b}{4}\right].}\tag{6}
\`\`\`
This is a **local conditional** result. In deriving the second equation, the initial selected oscillator acceleration/velocity vanishes and \`\dot B_{\chi,i}=W_bQ_i c_i\Delta_{A,i}\`. It explains the staggered onset in physical proper time: \`X\` is sourced at first derivative, \`S_A\` at second derivative, and the separately retarded auxiliary response begins still later (\`B_{\mathrm{delayed}}\sim h^3\`). It neither establishes a physical nonzero \`\eta\` mode nor determines \`W\`.

The real no-independent-free-bath retarded branch is defined by transport of the **entire earlier history**, not by setting \`q_j=\dot q_j=0\` at an arbitrary finite saved CLASS checkpoint.

## 5. Scientific decision

**New proven reduced-system fact:** the original quarter-normalized action gives a specific dynamical stress/current bridge, and generic instantaneous stress-null initial data are lifted into a nonzero stress derivative. The missing full physical datum is the **initial pair** \`X_i,S_{A,i}\` together with the complete Einstein–matter–aether–auxiliary/multiplier constraints and original scalar Noether propagation. This is precisely where the real regular adiabatic/decaying/isocurvature Frobenius selection must operate. The 42/42 dustlike mixed Einstein–Boltzmann source constrains \`\Delta_A\`, but does not fix this pair.

**Do not:** infer a detected gravity-memory mode; identify the half-source historical CLASS W1 with the quarter-source physical model; set the stress-null amplitude to zero by assumption; tune \`\eta\` or sweep \`k,z\` to amplify the small historical delayed W1; or treat 17 symbolic identities as 17 independent physics tests.

The next required work is to derive the full action-consistent finite-\`k\` Frobenius initial eigenvector from the coupled scalar/multiplier/Einstein/Boltzmann equations, and test the complete Ward and Hamiltonian propagation. If these fail, retain the bounded reduced-theory dynamical memory result as a legitimate partial publication target.

**FULL_PHYSICS_GO = FALSE. DES_detection = FALSE.**

## Reproducibility

[Source-locked 17-gate symbolic X–S/current-bridge proof](../ge19/physics_gate/exact_X_S_stress_lift_scalar_current_bridge_20261122.py), commit \`905bd0c\`. All 17 algebraic identities were checked independently with local SymPy before the repo commit; researcher WSL source-locked run pending.
