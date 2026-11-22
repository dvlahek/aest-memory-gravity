# GE19 — From causal NL0B forcing to an actual Einstein Weyl response: exact projector cancellation and first nonzero local transfer

**22 November 2026 | physics-first, no CLASS scan, no observed DES residuals, no invented gamma_t template.**

This is a substantive new conditional source-to-metric result, not a full cosmological memory detection. Starting with the *original quarter-normalized reduced action*, the *all-species* source-projected Einstein equations and the standard matter no-direct-bath-stress rule, derive an **exact constrained Weyl projector** and the first nonzero **retarded-only** local Weyl coefficient. The result isolates why a large instantaneous electric response need not imply a comparable gravitational signal. Original reference scripts: [finite-k X/S bath](../ge19/physics_gate/primordial_k2_XS_retarded_bath_hierarchy_20261122.py), [all-species joint Einstein constraints](../ge19/physics_gate/constraint_projected_joint_operator_20261112.py), [Weyl stress cancellation](ge19_20261115_constraint_eliminated_weyl_memory_cancellation_identity.md), [separate pressureful fluid/Einstein control](ge19_20261120_joint_primordial_fluid_einstein_constraint_decision.md). Companion compact source-locked [exact proof](../ge19/physics_gate/conditional_local_delayed_weyl_onset_20261122.py).

## 1. Exact source-to-Einstein equations, with bath already in a nonsingular causal coordinate

Use *proper cosmic time* and original GE19 normalization, finite k>0. Let C=2-K_B, X=chi/Q, S=K_B E_A+C QX, R_A=QK_Q/3, c=K_Q/(QK_QQ), W_b=sum w_j and \`r_j=(a omega_j sqrt(w_j)/k)q_j\` for active bath oscillators. As independently verified in the previous causal coordinate proof, the **time-dependent reduced equations** are:

\`\`\`math
\boxed{
\begin{aligned}
\dot X&=-\frac{CQ}{K_B}X+\frac{S}{K_B}+cF,\\
\dot S&=\left(\frac{CQ}{K_B}-H\right)S
+Q\left(K_Q-\frac{2CQ}{K_B}\right)X
-\frac{\eta Q}{4}\left(W_b QX-\sum_jr_j\right),\\
\dot\varphi&=Q\Psi-3Hc\varphi+QcF,\\
\dot\Phi&=\frac{K_Q}{2}\varphi+\frac{3a}{2k^2}T_o-H\Psi,\\
\ddot r_j&+H\dot r_j+(\omega_j^2-2H^2-\dot H)r_j
=\omega_j^2w_j QX .
\end{aligned}}\tag{1}
\`\`\`
All ordinary species enter **through their independently conserved density, momentum and shear** \`D_o,T_o,S_o\`, including pressure, tight-coupling/streaming and neutrino hierarchy. For these sources the Einstein constraint and shear relations *fix*:

\`\`\`math
\boxed{
\Psi=\Phi-\frac{9a^2}{2k^2}S_o,\quad
\Omega_o=D_o+\frac{3aH}{k^2}T_o,\quad
F=-\frac{\Omega_o+2k^2\Phi/(3a^2)}{R_A}
+\frac{k^2S}{a^2QK_Q}.}\tag{2}
\`\`\`

**This is an explicit reduced *coupled* source-to-ODE layout, not yet a closed full-physics solver:** (i) ordinary species dynamics must be appended with exact units/conventions; (ii) original action equivalence including all constraint multipliers and physical primordial mode selection remains unproven; (iii) time-varying \`a,H,Q,K_Q,c\` must come from the *same* expanding background; and (iv) true \`eta\` derivative of the physical initial state must be included or justified.

Most crucially, in the one-sided eta-tangent around eta=0+, **there is exactly one direct bath feedback input in the reduced dynamical subsystem**, in the \`S\` row:
\`\`\`math
\boxed{
\bigl(\partial_\eta\dot S\bigr)_{\mathrm{direct}}
=-\frac{Q}{4}\left(W_b QX_0-\sum_jr_{j,0}\right).}\tag{3}
\`\`\`
All other \`eta\` dependence in the metric and matter comes from the ensuing **coupled evolution**, unless the full action introduces an omitted companion term; this is precisely the still-open covariance/equivalence gate. Crucially, the bath contributes **no direct first-order Einstein stress** about relaxed \`U_j^{(0)}=0\`.

## 2. Exact cancellation of the apparent direct electric-field Weyl entry

The previously derived exact Einstein constraint, expressed through *original action stress*, is

\`\`\`math
W=\frac S2-\frac{a^2QK_{QQ}}{2k^2}\delta Q
-\frac{3a^2HK_Q}{2k^2}\varphi
-\frac{3a^2}{2k^2}\Omega_o
-\frac{9a^2}{4k^2}S_o,\qquad
\delta Q=\dot\varphi-Q\Psi .\tag{4}
\`\`\`

Using \`delta Q=-3Hc varphi+QcF\`, \`cQK_QQ=K_Q\` and the **complete** constrained \`F\` from Eq. (2), direct substitution gives the exact identity

\`\`\`math
\boxed{W=\Phi-\frac{9a^2}{4k^2}S_o
=\frac{\Phi+\Psi}{2}.}\tag{5}
\`\`\`

This is **not** independent Einstein evolution (indeed it is algebraically equivalent to the constrained metric shear definition); its interpretive importance is that the apparent \`+K_B E_A/2\` electric-field term in the stress representation **cancels exactly** against the scalar-density/phase and combined Einstein-source terms. Thus **do not convert an electric response directly into an observable Weyl response**. The Weyl observer is sensitive to *dynamically propagated* \`Phi\` and genuine ordinary-species shear, with all compensations enforced.

Equation (5) is independently checked symbolically in the companion proof, with no ad hoc assumption that the standard species shear vanishes.

## 3. The first nonzero *history-only* Weyl coefficient at finite regular time

Fix a finite regular initial time \`t_i\`, set \`h=t-t_i>0\`, and consider the **mathematical history-source difference** \`delta_h z_1=z_{1,retarded}-z_{1,instant-only}\` of one-sided \`eta\` tangents under the **same** eta=0 background, same full source-projected operator, same common initial eta derivative and same ordinary species. The instant-only comparator is an analysis device, not a second covariant theory.

**Explicit additional initial assumptions:** baseline \`chi_0(t_i)=E_{A,0}(t_i)=r_{j,0}(t_i)=dot r_{j,0}(t_i)=0\`, and \`D_i:=Q_i c_i\Delta_{A,i}\ne0\`. At this finite time \`dot chi_0(t_i)=D_i\`. Assume smooth bounded background and ordinary matter governed by its conserved metric-driven hierarchy without independent eta forcing; the direct *linear* NL0B stress is zero.

From the original oscillator forcing (or exact regular r_j equation), at earliest order,
\`\`\`math
\sum_jr_{j,0}(t_i+h)=\frac{M_2D_i}{6}h^3+O(h^4),
\qquad M_2:=\sum_jw_j\omega_j^2>0.
\`\`\`
The delayed-only \`S\`-row forcing is \`+(Q_i/4)\sum r_{j,0}\` at first order in eta. Because at leading order \`S_{1,h}=K_BE_{A,1,h}+O(h^5)\`, the original quarter coefficient leads to
\`\`\`math
\boxed{
\delta_h E_{A,1}(t_i+h)=\frac{Q_i D_i M_2}{96K_B}h^4+O(h^5).}\tag{6}
\`\`\`

There is NO direct bath metric stress. Full combined Einstein-source constraints then imply at successive leading powers:
\`\`\`math
\boxed{
\begin{aligned}
\delta_h\varphi_1&=\frac{c_i k^2 Q_i D_i M_2}{480a_i^2K_{Q,i}}h^5+O(h^6),\\
\delta_h\Phi_1=\delta_h W_1
&=\frac{c_i k^2 Q_i D_i M_2}{5760a_i^2}h^6+O(h^7).
\end{aligned}}\tag{7}
\`\`\`

Why are these powers legitimate? Before \`h^6\`, the ordinary-species density, momentum and shear corrections are driven **only by the induced metric**, so they enter at \`O(h^6),O(h^7),O(h^8)\` respectively under the assumed smooth hierarchy with no independent tangent initial data. The \`Phi\` metric source from \`phi_1\` enters at \`h^5\` and integrates to \`h^6\`; neutrino-shear corrections cannot modify that leading coefficient.

This is also corroborated by the **independent spatial Einstein pressure trace**, not simply the momentum equation. The leading action pressure \`P_{A,1}=K_Q\delta Q_1/3\` is

\`\`\`math
\boxed{
\delta_h P_{A,1}=\frac{c_i k^2 Q_iD_i M_2}{288a_i^2}h^4+O(h^5),
\quad \ddot{\delta_h\Phi}_1=
\frac32\delta_hP_{A,1}+O(h^5),}\tag{8}
\`\`\`
which reproduces exactly the coefficient \`1/5760\` in Eq. (7).

The AeST density perturbation responds **one time-power earlier than Weyl**:
\`\`\`math
\boxed{
\delta_h D_{A,1}=-\frac{H_i c_i k^2 Q_iD_i M_2}{480a_i^2}h^5+O(h^6),\quad
\delta_h D_{A,1}+H_iK_{Q,i}\delta_h\varphi_1=O(h^6).}\tag{9}
\`\`\`
The \`h^5\` density and momentum pieces cancel in the *comoving* constraint, which is essential for the \`h^6\` metric delay. Leading AeST continuity \`dot D_A+3H P_A=0+O(h^5)\` is satisfied independently, using (8)–(9). Thus the leading local **matter–Weyl** response is **not** inferable from Weyl alone: the AeST-effective-density channel may enter one power earlier, depending on how the actual galaxy-tracer matter transfer is constructed.

By \`D_i=Q_i c_i\Delta_{A,i}\`, (7) is equivalently
\`\`\`math
\boxed{\delta_h W_1(t_i+h)=\frac{k^2Q_i^2c_i^2M_2\Delta_{A,i}}{5760a_i^2}h^6+O(h^7).}\tag{10}
\`\`\`
Within these stated reduced-system hypotheses, a nonzero \`Delta_A_i\` and positive original coefficients imply a **nonzero signed leading local delayed-only Weyl perturbation** at sufficiently small nonzero h. It is **not** a complete physical retarded cosmological Weyl mode or a proof of observable DES signal. The result applies at a *finite regular* starting time with all imposed initially relaxed fields, and says nothing uniform about the singular \`t_i\to0\` Exp limit.

If the **additional unproven** finite-k adiabatic branch has \`\Delta_{A,i}=O(k^2)\`, then Eq. (10) has conditional \`O(k^4 h^6)\` fixed-time scaling. This is not an established suppression of actual DES \`gamma_t\`: at finite lens wavenumbers it requires the full evolving background, integrated history and angular projection.

## 4. Critical scientific implication for the next actual DES test

Our completed DES Y3 26-row covariance preflight found that only a **noise-weighted** shape change orthogonal to amplitude nuisances could be distinguished. A 3-sigma-equivalent Asimov distance corresponds to a projected-shape norm of **9.84% of the frozen GR reference C^-1 norm** in this *restricted two-amplitude model*. Eq. (10) is NOT such a forecast and cannot be directly compared to this number. It instead tells us the **physical response has at least three independent structures that must be retained** in an actual solver:

1. A causal oscillator history \`r_j(k,t)\` driven by \`X(k,t)\`, with no fabricated finite-time bath reset.
2. A constrained source-to-metric channel in which the raw \`E\` contribution is exactly canceled in the stress-only Weyl identity, and actual \`Phi,S_o\` evolve.
3. A *coupled matter response* \`D_A,\delta_b,\ldots\` that generally cannot be reconstructed by multiplying \`T_W\` by one constant.

The required **single future physical product** is \`(T_{\delta,1}^{delayed}(k,z),T_{W,1}^{delayed}(k,z))\` on the fixed DES lens-support domain, with the original quarter source, same expanding background, complete species hierarchy, physical finite-k adiabatic mode including its eta derivative, and full multiplier/Ward verification. The signed matter–Weyl cross-power must include **both** terms:
\`\`\`math
\partial_\eta P_{\delta W}
=P_{\cal R}\left[
T_{\delta,1}T_{W,0}+T_{\delta,0}T_{W,1}
\right]
\`\`\`
(for real coherent transfer functions and with correct cross-power conventions). Do NOT fit the observed DES residuals or substitute a historical one-k CLASS Weyl tangent. Compute and independently check the evolving constrained operator once; if the physical model excludes the imposed relaxed finite-time state, the local theorem is a negative control only and **must not be promoted to a physical detection**.

**Scientific status:** **REDUCED_ACTION_CONDITIONAL_NONZERO_LOCAL_DELAYED_WEYL_H6 / EXACT_W_STRESS_CANCELLATION / MATTER_RESPONSE_H5 / FULL_FINITE_K_PRIMORDIAL_PHYSICS_OPEN / PHYSICAL_GGL_TEMPLATE_OPEN / DES_DETECTION_FALSE**. No additional parameter or observational tuning, no full CLASS or DES runs.
