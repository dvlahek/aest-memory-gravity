# GE19 — Forced primordial asymptotic versus homogeneous modes: retarded memory is history-selected, not stress-selected

**22 November 2026. Physics-first conditional asymptotic calculation, no new CLASS or numerical survey.** This note extends the researcher-verified [17/17 X₂ indicial screen](../results/ge19_primordial_X2_indicial_20261122_r1.json) and its [4/4 source-locked log](../results/ge19_primordial_X2_indicial_20261122_r1.log), archived **byte-exact** (original Git blobs \`946959fe23a5645e8ea9cf809f131c6b35e8f3b0\` and \`41a9b986620eaf8864a436802b3a600a278f9f43\`; SHA-256 \`28f1d6463c1a1e62430a3070ef1e02f40788b15048674f36af444a99e40fba37\` and \`ab6100350a50eedcfbdc9b189f05f2da7a27cb5140241737da684ff3aea0fa7b\`). Repeat 17/17 X–S uploads already match prior archive. The original script correctly distinguishes the two reference homogeneous exponents 0 and 1/2 and maintains \`FULL_PHYSICS_GO=false\`.

**Goal of this calculation:** demonstrate what an *externally source-selected particular* early solution would do, not postulate it is the unique covariant AeST growing mode. The full physical source \`\Delta_2(t)\` and unreduced action/Noether regularity remain unproved.

## 1. Strict Exp background and its domain

In proper cosmic time, assume a radiation-dominated background
\`\`\`math
a(t)=A\,t^{1/2}[1+o(1)],\quad H(t)=\frac{1+o(1)}{2t},\quad
\frac{\rho_A}{\rho_r}=o(1),\quad t\to0^+ .
\`\`\`
In the exact *positive branch* of the pinned Exp scalar background,
\`\`\`math
K_Q=I_0/a^3=4K_2Z_0Z e^{Z^2},\quad
Q=Q_0+Z_0Z,\quad c_a^2=\frac{Z_0Z}{Q(1+2Z^2)}.
\`\`\`
Set \`L(t)=ln(t_*/t)>0\` with arbitrary fixed reference \`t_*\`. Taking the **formal strict** \`t\to0^+\` limit at fixed positive \`Q_0,Z_0,K_2,I_0\`,
\`\`\`math
Z^2=\frac32L+O(\ln L),\quad
Q\sim Z_0\sqrt{\tfrac32L},\quad
c_a^2\sim\frac{1}{3L},\quad
K_Q\sim \frac{I_0}{A^3t^{3/2}}.
\`\`\`
For the actual tiny frozen \`Z_0=10^{-17}\`, the formal \`Z_0 Z\gg Q_0\` regime lies extraordinarily far into the mathematical past. Do **not** apply these coefficients quantitatively at the finite initial epoch of any old CLASS run. This limit is used only to check asymptotic *mode selection logic*. Treat the full Einstein background and \`a\sim A\sqrt t\` as hypotheses requiring joint regularity proof.

## 2. Distinguish source-selected particular from the two unselected homogeneous branches

The exact original-action reduced leading-k² system from the prior verified proofs is
\`\`\`math
\dot X_2=-\frac{CQ}{K_B}X_2+\frac{S_2}{K_B}+f(t),\quad
\dot S_2=\left(\frac{CQ}{K_B}-H\right)S_2+
Q\left(K_Q-\frac{2CQ}{K_B}\right)X_2-\frac{\eta Q}{4}B_2,\quad
f(t)=c_a^2(t)\Delta_2(t).
\`\`\`
The researcher-confirmed second-order elimination reads
\`\`\`math
\ddot X_2+H\dot X_2+
\left[\frac{Q(CQ-K_Q)}{K_B}+\frac{CQH}{K_B}(1-3c_a^2)\right]X_2
=\dot f+(H-CQ/K_B)f-\frac{\eta Q}{4K_B}B_2.
\`\`\`

**Explicit additional physical hypothesis for the next asymptotic:** the *actual* comoving AeST source is regular and has
\`\`\`math
\Delta_2(t)=D\,t[1+o(1)],\qquad D\neq0.
\`\`\`
This is suggested, **but not established for full original AeST**, by the **dustlike Einstein–Boltzmann proxy** \`\Delta_2^{proxy}=-[(15+4R_\nu)/40]\Psi_0\tau^2[1-y_m/5]\` with \`\tau\sim 2\sqrt t/A\`, giving \`D_{proxy}=-(15+4R_\nu)\Psi_0/(10A^2)\`. The actual D must be derived together with the original scalar/aether action and all species, not fitted to observation.

Then the exact Exp asymptotic has \`f(t)\sim D t/(3L)\`. **Only on the particular branch with zero independent homogeneous X₂/S₂ amplitudes and no free oscillator q₃/p₃ modes continued from earlier history**, the leading first equation is \`\dot X_2\sim f(t)\`. Hence:
\`\`\`math
\boxed{
X_2^{\rm part}(t)\sim\int_0^t f(s)\,ds
\sim\frac{D\,t^2}{6L(t)}.
}\tag{A}
\`\`\`
This is *not* the p=0 or p=1/2 homogeneous branch. The latter two can dominate (A) if their amplitudes are allowed, so a density source alone does not pick the physical primordial solution.

## 3. Consequence for the initial stress and causal bath

Assume \`0<K_B<2\`, finitely many oscillator modes with fixed \`omega_j,w_j>0\`, finite spectral moments \`W_b=\sum w_j\`, \`M_2=\sum w_j\omega_j^2\`, no independent homogeneous q_j modes, and finite \`eta\`. The leading second equation is
\`\`\`math
\dot S_2+\frac{1}{2t}S_2\sim QK_Q X_2
\sim\frac{D Z_0 I_0}{6A^3}\sqrt{\frac32}\,
\frac{t^{1/2}}{\sqrt L}.
\`\`\`
Therefore the *particular* stress has
\`\`\`math
\boxed{
S_2^{\rm part}(t)\sim
\frac{D Z_0 I_0}{12A^3}\sqrt{\frac32}\,
\frac{t^{3/2}}{\sqrt L}.
}\tag{B}
\`\`\`
The first-order feedback \`S_2/K_B\` is smaller than \`f\` as \`t\to0\`, and the \`-CQX_2/K_B\` term is smaller still; the assumed asymptotic is self-consistent. Similarly the retarded oscillator source is
\`\`\`math
\frac{\omega_j\sqrt{w_j}QX_2}{a}
\sim \frac{\omega_j\sqrt{w_j}D Z_0}{6A}\sqrt{\frac32}
\frac{t^{3/2}}{\sqrt L}.
\`\`\`
Since \`3H\sim 3/(2t)\`, the two inertial/friction terms acting on \`t^{7/2}\` add with coefficient \`(7/2)(4)=14\`, while \`\omega_j^2q_{3j}\` is subleading. Thus
\`\`\`math
q_{3j}^{\rm part}(t)\sim
\frac{\omega_j\sqrt{w_j} D Z_0}{84A}\sqrt{\frac32}
\frac{t^{7/2}}{\sqrt L},
\`\`\`
\`\`\`math
B_{2,\mathrm{instant}}\sim
\frac{W_b D Z_0}{6}\sqrt{\frac32}
\frac{t^2}{\sqrt L},\quad
B_{2,\mathrm{delayed}}\sim
-\frac{M_2 D Z_0}{84}\sqrt{\frac32}
\frac{t^4}{\sqrt L}.
\`\`\`
Consequently,
\`\`\`math
\boxed{
\frac{B_{2,\mathrm{delayed}}}{B_{2,\mathrm{instant}}}
\sim-\frac{M_2}{14W_b}t^2.
}\tag{C}
\`\`\`
This universal leading *proper-time* ratio applies only to the **new sourced p=2 (with log) branch and the specified radiation/Exp hypotheses**. It does **not** conflict with the earlier \`-M_2(t-t_i)^2/(6W_b)\` local finite-time zero-state onset: that earlier calculation started with \`X(t_i)=0\` but \`\dot X(t_i)\ne0\` at a **regular finite** \`t_i\`, whereas here \`X_2\sim t^2/L\` and the background is asymptotically singular at \`t=0\`. Both show a truly retarded, initially oppositely signed auxiliary source. Neither gives a physical Weyl transfer or late-time sign.

## 4. Why this still does not finish primordial selection

Eq. (A) exists only *after setting both independent homogeneous amplitudes to zero*. The original reduced action does not itself impose that selection; actual full Einstein+AeST+NL0B scalar/aether/auxiliary/multiplier and matter Euler/Noether/adiabatic constraints might retain one homogeneous mode or exclude this particular ansatz. The small \`c_a^2\` cannot simply be used as an overall suppression of the full mode, and no quantitative DES prediction follows from (C).

The **scientifically meaningful decision** is therefore sharpened: prove or disprove that a full covariant, regular, growing **adiabatic** solution actually has \`X_2(t)=o(t^{1/2})\`, with no independent stress-null homogeneous amplitude and with a no-free-mode retarded bath transported from its physical past. The condition \`X_2=o(t^{1/2})\` would eliminate both *reference* homogeneous amplitudes, **if independently justified from the action and full adiabaticity**; it is NOT currently proven, nor should it be imposed merely to obtain small memory.

**Current classification: CONDITIONAL_EARLY_SOURCE_SELECTED_RETARDED_ASYMPTOTIC_DERIVED / PHYSICAL_PRIMORDIAL_SELECTION_AND_WARD_OPEN. FULL_PHYSICS_GO=false; DES_detection=false.** The next serious work must be the unreduced 3+1 mode/Noether proof, rather than another small symbolic-gate iteration.
