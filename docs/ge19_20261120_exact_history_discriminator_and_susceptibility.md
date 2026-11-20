# GE19 — Exact causal history discrimination from the original NL0B oscillator

20 November 2026. **Direct demonstration that the original reduced gravity-sector NL0B bath remembers excitation history**, with one exact analytic controlled-input example and a stationary spectral diagnostic. This is **not** an Einstein-constrained physical primordial/Weyl solution, cosmological detection, or Christodoulou/Bondi permanent gravitational-wave memory.

**Classification: ORIGINAL_REDUCED_POSITIVE_BATH_HISTORY_DISCRIMINATION_EXACT / SELECTED_RETARDED_BRANCH / PHYSICAL_WEYL_TRANSFER_BLOCK.**

## 1. The original one-oscillator action and force

Take one original positive auxiliary mode with \`w>0, omega>0, eta>0\`, Fourier scalar momentum \`k>0\`, in a controlled background \`a=1, H=0\`. This is **not** claimed to be a complete self-gravitating cosmological solution; \`chi(t)\` is prescribed as an external forcing history specifically to test nonlocality of the source map.

The original quadratic Lagrangian and normalized E source are
\`\`\`math
L_{\rm bath}^{(2)}=\frac{\eta}{4}
[\dot q^2-(\omega q-\sqrt w\,k\chi)^2],\quad
\ddot q+\omega^2q=\omega\sqrt w\,k\chi,\quad
B_\chi=w\chi-\frac{\omega\sqrt w}{k}q,
\quad(\dot E_A)_{\eta\,\mathrm{source}}=-\frac{\eta Q}{4K_B}B_\chi.
\`\`\`
Use the *selected no-free-bath* initial conditions \`q(0)=dot q(0)=0\`. The eta=0 normalized q branch is understood as the one-sided eta->0+ continuation, **not** a unique Euler-Lagrange solution of a singular eta=0 auxiliary action.

## 2. Two controlled histories with exactly equal current excitation

Define history H1: \`chi_1(t)=0\` identically. Define history H2:
\`\`\`math
\chi_2(t)=\chi_0\sin^2(\pi t/T),\qquad
0\le t\le T,\quad \omega=\pi/T
\`\`\`
and \`chi_2(t)=0\` for \`t>T\`. Both histories have \`chi(T)=dot chi(T)=0\`. They need not share the rest of the self-gravitating state, and no complete physical Cauchy solution is asserted.

The exact *retarded* solution for H2 during the forcing interval is
\`\`\`math
q_2(t)=\frac{k\sqrt w\,\chi_0}{6\omega}
[3+\cos(2\omega t)-4\cos(\omega t)]
\`\`\`
and
\`\`\`math
\boxed{B_{\chi,2}(t)=\frac23w\chi_0[
\cos(\omega t)-\cos(2\omega t)] .}
\`\`\`
Substitution into the original forced auxiliary ODE is **identically exact**, satisfying both initial conditions. At the common endpoint:
\`\`\`math
\chi_1(T)=\chi_2(T)=0,\quad
\dot\chi_1(T)=\dot\chi_2(T)=0,\quad
q_2(T)=\frac{4k\sqrt w\,\chi_0T}{3\pi},
\quad \dot q_2(T)=0,
\`\`\`
\`\`\`math
\boxed{B_{\chi,1}(T)=0,\qquad
B_{\chi,2}(T)=-\frac43w\chi_0\ne0.}\tag{H}
\`\`\`
**Interpretation:** No local constitutive law depending only on \`chi(T),dot chi(T)\` can reproduce both bath forces. The additional state \`q(T)\` stores the preceding excitation history. This is a genuine causal memory mechanism in the **reduced source map**, not by itself a measurable distinction in the full metric or Weyl potential.

The original quarter action source changes correspondingly at the common endpoint:
\`\`\`math
\Delta[(\dot E_A)_{\eta\,source}](T)
=-\frac{\eta Q}{4K_B}\Delta B_\chi(T)
=+\frac{\eta Q w\chi_0}{3K_B}.
\`\`\`
This is a difference in the *source term* evaluated for the two externally prescribed histories, **not** an assertion that two fully evolved cosmologies possess identical metric/aether states at T.

## 3. Stored energy and post-pulse persistence

The original positive bath Hamiltonian energy in the static background is
\`\`\`math
\mathcal E_{\rm bath}(t)=\frac{\eta}{4}
[\dot q^2+(\omega q-\sqrt w\,k\chi)^2]\ge0.
\`\`\`
At the end of H2,
\`\`\`math
\boxed{\mathcal E_{\rm bath}(T)=\frac49\eta w k^2\chi_0^2>0.}
\`\`\`
For \`t>T\`, with chi=0, the exact free evolution is
\`\`\`math
q(t)=\frac{4k\sqrt w\,\chi_0}{3\omega}\cos[\omega(t-T)],\qquad
\boxed{B_\chi(t)=-\frac43w\chi_0\cos[\omega(t-T)].}
\`\`\`
The source retains information about history **after the external scalar forcing is zero**. Because this idealized oscillator has **no damping**, its memory is oscillatory and is **not a permanent offset**. An expanding background (\`3H dot q\`) and a distribution of bath frequencies change decay/dephasing; neither case is quantified by this static illustrative exact solution.

## 4. The exact stationary susceptibility and its consequence for observability

For a harmonic forcing \`chi~exp(-i Omega t)\` in a stationary background with a **selected retarded steady response** (adiabatic switch-on, causal \`i0^+\`), eliminate q to obtain for one oscillator:
\`\`\`math
\boxed{
\mathcal K_{\rm bath}(\Omega):=\frac{\widehat B_\chi}{\widehat\chi}
=w\left(1-\frac{\omega^2}{\omega^2-(\Omega+i0^+)^2}\right)
=-\frac{w(\Omega+i0^+)^2}{\omega^2-(\Omega+i0^+)^2}.}
\`\`\`
For multiple positive bath modes, add over j. In the real-frequency off-resonance limit:
\`\`\`math
\mathcal K_{\rm bath}(\Omega)\simeq
-w\frac{\Omega^2}{\omega^2}\quad (|\Omega|\ll\omega),\qquad
\mathcal K_{\rm bath}(\Omega)\to w\quad (|\Omega|\gg\omega).
\`\`\`
At exactly quasi-static *equilibrated* forcing \`Omega=0\`, the induced q cancels the instantaneous \`w chi\` stiffness: \`mathcal K_bath(0)=0\`. At near-resonance the finite undamped susceptibility has a pole. Causality does **not** license assigning a finite observable resonance gain without Hubble friction, bath spectral regularization, backreaction and a controlled physical observer.

This is a **useful falsifiable discriminator**: the material memory acts primarily on the *history and rate of change* of the gravitational-sector excitation, whereas a truly instantaneous extra stiffness would retain its static response. The historical small one-point CLASS Weyl tangent cannot be equated to this frequency factor: it derives from a different, uncertified full-CLASS implementation with a known one-half versus one-quarter source mismatch, pressureful primordial IC still open, and an unseparated instantaneous+delayed bath force.

## 5. What the required *physical* Weyl test is and is not

The full selected eta tangent, **if and only if** the original action-to-all-species Einstein+AeST+NL0B Ward and correct finite-k adiabatic background/initial mode are established, has the source decomposition already proved independently in the existing Noether note:
\`\`\`math
W_1=W_{1,\mathrm{IC}}+W_{1,\mathrm{inst}}+W_{1,\mathrm{delayed}}.
\`\`\`
The delayed component is projected with the same full \`eta=0\` propagator and the source \`+(a^2Q)/(4K_B k)\sum_j \omega_j\sqrt{w_j}\,q_{j,0}\`. This is **one linearized original theory**, not independently tuned \`W_retarded\` and \`W_instantaneous\` cosmologies. In a physical comparison, the instantaneous and delayed terms must be reported *separately*, as must any eta-dependent initial-state contribution. Neither sign nor magnitude of the late-time \`W_{1,delayed}\` has yet been computed in a certified Einstein-constraint-compatible cosmology.

**Decision:** The original gravitational-sector reduced action has unambiguous mathematical causal memory, independently of an observation. But the headline “GRAVITY HAS OBSERVED MEMORY” is not justified. The next acceptance should be **one** action/Ward-consistent full background and finite-k primordial state, followed by a split *physical* Weyl eta tangent. Predeclare the DES Y3 MagLim4 x Source4 Asimov observer only after the physics gate. No new local h5/h6 Taylor sweeps or parameter tuning.

## Executable, source-locked analytic check

\`ge19/physics_gate/exact_causal_history_discriminator_20261120.py\` performs 18 exact SymPy identities covering the pulse, current-jet equality, original q ODE, nonzero history force, positive energy, post-pulse oscillator, low/high frequency response and source-normalized quarter coefficient. Independent SymPy 18/18 PASS; researcher WSL source-locked execution pending. No CLASS, no data, no DES.

\`\`\`bash
cd ~/aest-memory-gravity
git switch physics-first-gravitational-elasticity
git pull --ff-only origin physics-first-gravitational-elasticity
source .venv/bin/activate
python -u ge19/physics_gate/exact_causal_history_discriminator_20261120.py \
  --out results/ge19_exact_causal_history_discriminator_20261120_r1.json \
  2>&1 | tee results/ge19_exact_causal_history_discriminator_20261120_r1.log
\`\`\`

## Locked theory sources
- [Original NL0B reduced-action and Noether analysis](ge19_20261114_noether_constraint_and_eta0_retarded_branch_theorems.md)
- [Exact off-shell scalar charge and original quarter-normalization](ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md)
- [No arbitrary finite-time bath reset](ge19_20261119_retarded_history_transport_no_finite_reset.md)
- [New exact controlled-history script](../ge19/physics_gate/exact_causal_history_discriminator_20261120.py)
