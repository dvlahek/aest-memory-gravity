# GE19 — Action-derived nonadiabatic pressure and superhorizon curvature gate

19 November 2026. Physics-first continuation of the original frozen GE05/GE06 reduced action and GE19 11–19 November documents. No numerical integration, CLASS, H4/Z21, DES, source tuning, or new fitting.

**Classification: REDUCED_ACTION_NONADIABATIC_PRESSURE_IDENTITY_PROVED / CONDITIONAL_SUPERHORIZON_CURVATURE_CONSERVATION_PROVED / FULL_PHYSICAL_WEYL_NONZERO_NOT_PROVED / PHYSICS_BLOCK.**

## 1. Frozen action stress and background

At fixed Fourier k>0, use the original effective AeST stress dictionary on a flat FLRW background:
\`\`\`math
D_A=\frac13\left[QK_{QQ}\,\delta Q-\frac{k^2}{a^2}(K_B E_A+C\chi)\right],
\quad P_A=\frac13K_Q\,\delta Q,\quad
R_A=\rho_A+p_A=\frac{QK_Q}{3},
\quad c_a^2=\frac{\dot p_A}{\dot\rho_A}=\frac{K_Q}{QK_{QQ}},
\quad C=2-K_B.
\`\`\`
The kinetic variable \`delta Q=dot varphi-Q Psi\` and longitudinal physical variables \`chi=varphi+Q alpha_A\`, \`E_A=dot alpha_A+Psi\`, and \`theta_A=k² varphi/(aQ)\` follow from the same reduced original action phase dictionary. Assume \`R_A != 0\`, \`Q != 0\` and other denominators regular. The identity below is purely algebraic once the action stress dictionary holds; it does **not** independently certify its preservation by CLASS.

## 2. Exact reduced-action nonadiabatic-pressure identity

Define the AeST intrinsic nonadiabatic pressure at linear order \`delta P_nad,A := P_A-c_a² D_A\`. Then
\`\`\`math
\boxed{\delta P_{\mathrm{nad},A}
=\frac{c_a^2 k^2}{3a^2}(K_BE_A+C\chi).}\tag{1}
\`\`\`
**Proof:** use \`c_a² Q K_QQ=K_Q\` so that the \`delta Q\` terms cancel exactly in \`P_A-c_a² D_A\`; the remaining gradient term yields (1). No bath forcing coefficient, numerical value, observational data, or assumption about direct bath shear is needed. QED.

This gradient-suppressed nonadiabatic pressure is a direct statement about the **AeST effective stress tensor**, not necessarily the entropy perturbation of the complete multi-fluid cosmology. It does not claim the bracket is uniformly bounded at k->0 unless this is imposed separately.

## 3. Derivation of the AeST curvature equation

Assume the **independent full action scalar Euler and aether equations** actually enforce separate AeST effective stress continuity, rather than merely the internally constructed CLASS density row. Write the linear continuity equation in Newtonian gauge and cosmic time with theta_A the CLASS comoving velocity divergence:
\`\`\`math
\dot D_A+3H(D_A+P_A)-3R_A\dot\Phi+\frac{R_A}{a}\theta_A=0.
\tag{2}
\`\`\`
Together with background \`dot rho_A=-3H R_A\`, \`dot p_A=c_a² dot rho_A\`, define gauge-invariant uniform-AeST-density curvature \`zeta_A=-Phi-H D_A/dot rho_A=-Phi+D_A/(3R_A)\`. Direct differentiation, using \`dot R_A=-3H(1+c_a²)R_A\`, gives
\`\`\`math
\boxed{\dot\zeta_A=-\frac{H}{R_A}(P_A-c_a^2D_A)-\frac{\theta_A}{3a}.}\tag{3}
\`\`\`
Insert the original action (1) and \`theta_A=k² varphi/(aQ)\`:
\`\`\`math
\boxed{\dot\zeta_A=-\frac{k^2}{3a^2}
\left[\frac{Hc_a^2}{R_A}(K_BE_A+C\chi)+\frac{\varphi}{Q}\right].}\tag{4}
\`\`\`
This identity is **conditional on** separate physical AeST stress continuity (2) and the action dictionary. It is NOT proof that the current patched CLASS evolution lies on that full scalar-charge constraint surface. QED.

If \`varphi/Q\`, \`E_A\`, \`chi\`, \`Hc_a²/R_A\` and their relevant parameter variations are uniformly bounded as k->0 on a finite interval, then \`dot zeta_A=O(k²)\`. Hence at k=0 the leading uniform-AeST-density curvature is constant in time. More carefully, this is a regular-long-wavelength limit, not an assertion that the unnormalized longitudinal aether variables remain bounded for every gauge, any singular background, or every initial-state branch.

For the history-only eta-tangent difference \`delta_h\`, with fixed background and identical initial tangent and with both diagnostic sources obeying the **same physically consistent density conservation**, linearity yields
\`\`\`math
\boxed{\frac{d}{dt}\delta_h\zeta_A
=-\frac{k^2}{3a^2}\left[
\frac{Hc_a^2}{R_A}(K_B\delta_h E_A+C\delta_h\chi)
+\frac{\delta_h\varphi}{Q}\right].}\tag{5}
\`\`\`
The exact distinction between the two source decompositions remains formal: the instant-only comparator is a first-order mathematical diagnostic, not a second physical covariant action. If its state fails the independent continuity or scalar Ward equation, (5) cannot be applied to that diagnostic by fiat.

If initial \`delta_h zeta_A(t_i)=0\` and the bracket is uniformly bounded in k and integrable in t, then
\`\`\`math
|\delta_h\zeta_A(T)|\le \frac{k²}{3}\int_{t_i}^T\frac{dt}{a(t)^2}\left[\frac{|Hc_a²|}{|R_A|}(|K_B|\,|\delta_h E_A|+|C|\,|\delta_h\chi|)+\left|\frac{\delta_h\varphi}{Q}\right|\right].
\tag{6}
\`\`\`
The bound is **conditional** and does not provide a numeric sensitivity, Weyl lower bound or observed detection. It also does not prove that physical Weyl memory is \`O(k²)\`: the Einstein constraints explicitly involve \`1/k²\` factors, and ordinary-species shear/velocity contributions and initial-state choices matter.

## 4. Physical consequences and limitation

- The original stress-pressure action dictionary establishes a nontrivial \`k²\` suppression of the *AeST intrinsic nonadiabatic pressure* independent of how the positive bath kernel is discretized.
- For regular physical long-wavelength perturbations on the full separate-conservation constraint surface, uniform-AeST-density curvature is conserved to order k^0. This is consistent with, but does not derive, the entire coupled primordial adiabatic growing eigenmode.
- A finite-k driven memory response remains allowed and has not been proved to vanish. No conclusion on nonzero Weyl output follows without the full dynamical Einstein–AeST–NL0B projection and initial state.
- The precise action-derived background/pressure/phase dictionary must be retained; do not use the inherited dust CDM initial density relation for pressureful AeST.
- For a genuinely retarded physical memory perturbation, equation (4) is an exact conditional curvature-propagation checkpoint. It is a stronger *physical consistency requirement* than another numerical PASS stage.

**Decision:** Keep PHYSICS_BLOCK, no CLASS or DES runs. The next irreducible step is to derive the full time-dependent scalar/aether Euler system and physical radiation-era finite-k growing mode, verify AeST continuity and the original scalar Ward identity, then compute the delayed-only Weyl adjoint overlap. The curvature identity (4) and the existing Weyl cancellation identity provide two independent constraints on that one physical operator.

## Primary frozen repo sources
- [Action stress, phase, pressure identities](ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md)
- [Primordial adiabatic and all species gate](ge19_20261111_all_species_Einstein_operator_and_adiabatic_IC_block.md)
- [Nov 15 exact Weyl cancellation identity](ge19_20261115_constraint_eliminated_weyl_memory_cancellation_identity.md)
- [Nov 19 gauge-null / adjoint memory criterion](ge19_20261119_gauge_null_and_adjoint_delayed_weyl_proof_gate.md)
- [P0 physics gate](https://github.com/dvlahek/aest-memory-gravity/issues/2)
