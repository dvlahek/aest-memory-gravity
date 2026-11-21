# GE19 — Physical meaning of the first nonzero memory drive: corrected F3 audit and exact cubic retarded onset

**2026-11-21 — physics-first correction / original reduced action, no CLASS runs.**

## Accepted research inputs

The researcher's [source-locked finite-k NLO radiation report](../results/ge19_radiation_finite_k_NLO_20261121_r1.json) and [log](../results/ge19_radiation_finite_k_NLO_20261121_r1.log) were archived byte-exact, Git blobs \`9b549510f83b20429f77f86993a229c71aa8aedb\` and \`3ab00c254c2e9834072ad342b2c94c814404c0c5\`, respectively. \`37/37\` original symbolic gates passed, with source locks \`3/3\`. The repeated 31-gate leading baryon/Exp JSON and log were byte-exact duplicates of the previously archived result; nothing was overwritten.

**Scientific integrity correction:** One original 37-gate test, \`neutrino_octupole_F3_evolution_k4\`, projected the Boltzmann octupole equation onto an identically absent \`k^4\` power. Consequently **that specific gate was vacuous** and should not be described as a nontrivial octupole evolution test. The archived original result is unchanged. The new standalone code [corrected_octupole_and_causal_memory_onset_20261121.py](../ge19/physics_gate/corrected_octupole_and_causal_memory_onset_20261121.py) tests the actual leading \`k^3\` residual and verifies that setting \`F_{nu3}=0\` or reversing its sign makes the \`k^3\` residual **nonzero**:
\`\`\`math
F_{\nu3}=\frac{2\Psi_0}{105}(k\tau)^3,\qquad
[F_{\nu3}'-\tfrac67 k\sigma_\nu]_{k^3}=0.
\`\`\`
The octupole's remaining uncomputed term is \`O(k^5)\`, as expected. This fixes the test design, not the verified NLO coefficients \`\Delta_A=-(15+4R_\nu)\Psi_0(k\tau)^2/40\` and the leading \`\Phi_2,\Psi_2,\sigma_{\nu4}\` identities.

## Exact original-action source-onset theorem at a *finite regular initial time*

The selected normalized NL0B auxiliary equations of the restricted original quadratic action are, in **proper cosmic time** \`t\`:
\`\`\`math
\dot X=E_A+c_a^2 F,\quad
\dot E_A=-H E_A+\frac{Q}{K_B}
\big([K_Q-C(H+Q-3Hc_a^2)]X-Cc_a^2F-\frac{\eta}{4}B_\chi\big),
\quad
F=\Delta_A+\frac{k^2}{3a^2R_A}(K_B E_A+C QX),
\`\`\`
\`\`\`math
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\frac{\omega_j\sqrt{w_j}kQX}{a},\quad
B_{\rm inst}=W_bQX,\quad
B_{\rm delayed}=-\frac{a}{k}\sum_j\omega_j\sqrt{w_j}\,q_j,
\quad W_b=\sum_jw_j>0.
\`\`\`
Assume a chosen **finite** regular time \`t_i\`, differentiable coefficients, \`k,a_i,Q_i,K_B\neq0\`, and the prescribed (not independently Ward-certified) source \`\Delta_A(t_i)=D_i\`. For an explicit **zero-state boundary condition** \`X_i=E_i=q_{j,i}=\dot q_{j,i}=0\`:
\`\`\`math
\boxed{\dot X_i=c_i D_i,\qquad
\dot E_{A,i}=-\frac{C Q_i c_i}{K_B}D_i,\qquad
\ddot q_{j,i}=0,\quad
q^{(3)}_{j,i}=\frac{\omega_j\sqrt{w_j} k Q_i c_i D_i}{a_i}.}
\`\`\`
The first two relations are exact instantaneous original-action flow statements; the last follows by differentiating the original oscillator once. Because \`q_i=\dot q_i=\ddot q_i=0\`, derivatives of \`a(t),H(t),Q(t)\` multiplying these zero values **drop out** of the jerk.

Define the strictly positive second frequency moment \`M_2=\sum_j w_j\omega_j^2\`. Let \`h=t-t_i\to0^+\` in proper time. Taylor's theorem gives
\`\`\`math
\boxed{
B_{\rm inst}(t_i+h)=W_b Q_i c_iD_i\,h+O(h^2),\quad
B_{\rm delayed}(t_i+h)
=-\frac{Q_i c_iD_iM_2}{6}\,h^3+O(h^4).
}
\`\`\`
When \`c_iD_i\neq0\`, the local signed ratio is
\`\`\`math
\boxed{
\frac{B_{\rm delayed}}{B_{\rm inst}}
=-\frac{M_2}{6W_b}h^2+O(h^3).
}
\`\`\`
**This is a robust, original-action constitutive result:** after an exactly zero selected finite-time bath state, the delayed source first appears two powers of proper time after the instantaneous source. Because \`M_2,W_b>0\`, it initially **opposes** the instantaneous source independently of the sign of \`D_i\`. This cannot by itself fix the sign of the **Weyl** response after propagation by the full Einstein/AeST Green operator.

For a split eta tangent in the *same* source-only linear propagator with zero eta-derivative initial data, the direct delayed forcing of the E equation is
\`\`\`math
(\dot E_{A,1})_{\rm delayed-source}
=-\frac{Q_i}{4K_B}B_{\rm delayed}+O(h^4),
\quad
\boxed{
E_{A,1}^{\rm delayed-source}(t_i+h)
=\frac{Q_i^2 c_i D_i M_2}{96K_B}\,h^4+O(h^5).}
\`\`\`
This \`h^4\` onset is a **local direct-source decomposition**. It is not a prediction for a finite-\`k\` physical metric response without the complete propagator, and it assumes no eta-dependent initial derivative.

The source from the separate **radiation-only test-fluid NLO** limit is \`D_i=-(15+4R_\nu)\Psi_0(k\tau_i)^2/40+\cdots\`. Substitution is a *conditional seed*, not a proof the full mixed \`O(y_A(k\tau)^2)\` primordial eigenmode has that coefficient or that the actual Exp theory selects zero initial \`X_i,E_i\`.

## A crucial caveat for the previous 141,494-row historical CLASS split

The physical *no independent free-bath-mode* / retarded boundary condition is a **history selection**, not a universal assertion that \`q_j(t_i)=\dot q_j(t_i)=0\` at **any** finite time \`t_i\`. If a nonzero \`X(t)\` existed before the first stored CLASS sample, the retarded integral generally has nonzero \`q_j(t_i)\` and \`\dot q_j(t_i)\`. This is precisely why the source-reconstruction report labels its zero first-saved-state assumption **not independently certified**. The new cubic-onset theorem does **not** retrospectively certify that historical split.

Likewise \`c_a^2=0\` is a potentially singular idealized limit of the Exp scalar action, not a universal physical no-memory theorem. In the pinned Exp background \`0<c_a^2\le3.5355\times10^{-14}\`, but coefficients with \`1/R_A\`, primordial mode selection and finite-\`k\` growth prevent turning that alone into a reliable upper bound on \`W_{1,\rm delayed}/W_0\`.

**Decision:** We have a true constitutive source-history mechanism and a provisional, nonzero numerical historical Weyl response, but still lack a **single, action-normalized, Ward-compatible finite-\`k\` adiabatic eigenmode**. Prioritize the combined Einstein–AeST–photon–baryon–neutrino \`O(y_m(k\tau)^2)\` expansion and physical choice of longitudinal scalar initial state, **not another CLASS/eta/k scan**. \`FULL_PHYSICS_GO=false\`, \`DES_detection=false\`.

## Reproducibility

New original-source-locked [symbolic finite-time onset script](../ge19/physics_gate/corrected_octupole_and_causal_memory_onset_20261121.py). An independent local SymPy prototype verified q jerk, 4 delayed-source jets and the corrected F3 k^3 residual, with nonzero absent-/wrong-sign controls. Researcher WSL source-locked execution pending.
