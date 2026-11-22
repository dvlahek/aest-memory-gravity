# GE19 — Exact finite Einstein-constrained Exp scalar source: pressureless limit versus true physical regularity

**2026-11-22 | Physics-first after verified 42/42 mixed Einstein–Boltzmann proxy and corrected 17/17 causal-onset proof.** No new CLASS, simulations, DES or tuning. A new original-source-locked 13-identity symbolic proof is provided. This note concerns **necessary constrained initial-data conditions**; it is **not** the missing full primordial eigenvector.

## 1. Researcher checkpoint and version integrity

The original [corrected source-locked 17/17 WSL JSON](../results/ge19_corrected_f3_causal_onset_20261121_r2.json) and [log](../results/ge19_corrected_f3_causal_onset_20261121_r2.log) are archived with byte-exact Git blobs \`afb73b906ead7f89868e28fbf6898158b277f389\` and \`c7baca547552d378642590af3e55ba8b187b720d\`; the original SHA-256 hashes are \`327cf250929236744d9f9ab46a27ca40d82afae67f6d2db2b359daa88e314e69\` and \`d62842a23c560003a94ba4b76b26c2d0ccbd48e3d371457ba9329a939bf8af02\`. The first r1 source-lock error was a wrong Git blob string, not a physical failure; the old log remains immutable. The reuploaded 42/42 original mixed-\`y_m(k\tau)^2\` JSON/log are byte-identical to prior Git archives. Neither result claims \`FULL_PHYSICS_GO\` or DES detection.

The repaired F3 test checks the correct nontrivial \`k^3\` coefficient and absent/wrong-sign negative controls. The 17-gate causal-onset theorem is conditional on **zero auxiliary and longitudinal state at one selected finite initial time**, not on a proven physical primordial mode. Never equate a finite checkpoint reset with no independent free-bath oscillations from primordial history.

## 2. The previously underappreciated exact ratio that decides the dust-limit argument

The original reduced action and Exp background dictionary have
\`\`\`math
R_A=\rho_A+p_A=\frac{QK_Q}{3},\qquad
c\equiv c_a^2=\frac{K_Q}{QK_{QQ}},\qquad
C=2-K_B,\quad S_A=K_BE_A+CQX .
\`\`\`
The constrained AeST scalar forcing, using **the total comoving Einstein constraint** and the ordinary-species sum \`\Omega_s\`, is
\`\`\`math
F=\Delta_A+\frac{k^2}{3a^2R_A}S_A
=-\frac{\Omega_s}{R_A}+\frac{k^2}{3a^2R_A}(S_A-2\Phi)
=\frac{\mathcal N}{R_A},
\qquad
\mathcal N=-\Omega_s+\frac{k^2}{3a^2}(S_A-2\Phi).
\`\`\`
Therefore the \`\dot X\` and \`\dot E_A\` source appears as **the exact ratio**
\`\`\`math
\boxed{
\frac{c_a^2}{R_A}=\frac{3}{Q^2K_{QQ}},\qquad
c_a^2 F=\frac{-3\Omega_s+\frac{k^2}{a^2}(S_A-2\Phi)}
{Q^2K_{QQ}}.
}\tag{1}
\`\`\`
This is an exact algebraic identity of the previously derived action/Einstein-constrained reduced system. It is not an extra perturbative approximation and involves **no division by the small \`K_Q\`** after cancellation.

For positive Exp \`Z>0\`,
\`\`\`math
Q=Q_0+Z_0Z,\qquad K_{QQ}=4K_2e^{Z^2}(1+2Z^2).
\`\`\`
With the actual pinned \`Q_0=10^{-4}\`, \`K_2=9500\`, both factors have positive global lower bounds:
\`\`\`math
\boxed{
0<\frac{c_a^2}{R_A}
=\frac{3}{4K_2(Q_0+Z_0Z)^2e^{Z^2}(1+2Z^2)}
<\frac{3}{4K_2Q_0^2}
=7894.736842105263 .
}\tag{2}
\`\`\`
In project-normalized stress units, this **dimensionful / convention-dependent coefficient is not a directly measured fractional effect**. It demonstrates why one cannot simply replace \`c_a² F\` by a negligible source based solely on the earlier upper bound \`c_a²<3.54e−14\`, without controlling \`F\`, \`R_A\`, and action initial-state regularity.

## 3. A singular versus regular dust-limit distinction, not permission to amplify by tuning

Consider the formal family \`Z_0=\varepsilon\to0^+\` at *fixed* \`Z>0,Q_0,K_2\`. Exactly
\`\`\`math
c_a^2=\frac{\varepsilon Z}{(Q_0+\varepsilon Z)(1+2Z^2)}
\longrightarrow0,\qquad
R_A=\frac{4K_2}{3}(Q_0+\varepsilon Z)
\varepsilon Z e^{Z^2}\longrightarrow0,
\`\`\`
\`\`\`math
\boxed{
\frac{c_a^2}{R_A}
\longrightarrow\frac{3}{4K_2Q_0^2e^{Z^2}(1+2Z^2)}>0 .
}\tag{3}
\`\`\`
**Important:** This is an algebraic path through the original Exp family at fixed \`Z\`; it is **not** the calibrated cosmology where \`K_Q=I_0/a^3\` fixes an epoch-dependent \`Z\` as parameters change. It must not be interpreted as a cosmological limit or a specific numerical gain.

The Einstein constraint states
\`\`\`math
R_A\Delta_A+\Omega_s=-\frac{2k^2}{3a^2}\Phi.
\`\`\`
Substituting this *actual* constraint into the complete source gives
\`\`\`math
\boxed{\mathcal N=R_A\Delta_A+\frac{k^2}{3a^2}S_A,\qquad
c_a^2F=c_a^2\Delta_A+
\frac{k^2}{a^2Q^2K_{QQ}}S_A.}\tag{4}
\`\`\`
This distinguishes two physically different questions:

- If \`\Delta_A\` stays bounded in a formal limit \`R_A\to0\`, its **matter-only** forcing \`c_a^2\Delta_A\` vanishes with \`c_a^2\`.
- **Nothing about bounded \`\Delta_A\` alone bounds the aether stress \`S_A\`**, so the *full* \`c_a^2F\` need not vanish. If the physical primordial mode additionally implies \`S_A=O(R_A)\`, the gradient contribution also vanishes; if \`S_A\` remains finite, it can survive. Whether either branch satisfies the complete action, regularity and Ward is still unproved.

It would be *incorrect* to identify \`\Delta_A=\mathcal N/R_A\` while discarding \`S_A\`, or to hold a nonzero \`\mathcal N\` fixed and infer a physical effect without evaluating both constituent terms. The actual dustlike Einstein–Boltzmann proxy determines \`\Delta_A\`, **not** the AeST scalar/aether stress required by the original covariant theory. This missing stress is exactly the next primordial selection problem.

## 4. Stress-null kernel remains invisible to instantaneous Einstein constraints

Even after \`S_A\` is identified, initial metric stress does not determine all the scalar/aether states. The known instantaneous stress-null displacement
\`\`\`math
\delta\chi=\epsilon,\qquad
\delta E_A=-\frac{C}{K_B}\epsilon,\qquad
\delta\varphi=\delta(\delta Q)=0
\`\`\`
leaves \`\delta S_A=K_B\delta E_A+C\delta\chi=0\` and the leading AeST metric stress unchanged. At fixed \`k\ne0\`, the original scalar spatial Noether current changes by
\`\`\`math
\boxed{\frac{\delta J_\phi^x}{ika\epsilon}
=2\frac{K_Q}{Q}-\frac{4C}{K_B}-\frac{\eta W_b}{2}.}
\`\`\`
The Ward equation requires **current divergence to vanish**, not the spatial current separately. It therefore does not algebraically eliminate this initial stress-null direction. Only **the joint dynamical finite-\`k\` regularity/Frobenius analysis** of metric, standard species, AeST, scalar, aether, auxiliary and multipliers can decide whether the direction is a valid independent primordial mode, a decaying/isocurvature mode, or excluded by regular growing-mode selection.

## 5. Scientific decision and one next physical acceptance criterion

The pressureless mixed \`42/42\` Einstein–Boltzmann source is closed **within its scope**, and the \`17/17\` corrected bath onset is closed **given its finite-time zero-state hypothesis**. This new exact ratio sharpens the remaining P0 issue:

**Construct \`S_A(t_i)=K_B E_i+(2-K_B)Q_iX_i\` from the original action, not by hand; determine whether it scales as \`R_A\`, remains independent or is forbidden by regular growing/adiabatic selection. Simultaneously verify full scalar Noether residual plus Einstein constraint propagation.** Only then can the historical delayed Weyl tangent be physically reinterpreted.

No additional \`k,\eta,z\` scans, no retuning based on DES. \`FULL_PHYSICS_GO=false\`, \`DES_detection=false\`.

## Reproducibility

New [source-locked 13-identity executable](../ge19/physics_gate/Exp_constraint_normalized_regular_source_20261122.py). It verifies (1)–(3), regular source substitutions and stress-null current relations with SymPy. A local SymPy prototype of the identity family passed 13/13. Researcher WSL source-locked execution pending.
