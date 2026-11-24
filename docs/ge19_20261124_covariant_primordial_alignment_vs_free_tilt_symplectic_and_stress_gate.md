# GE19 — Primordial scalar–aether alignment as a covariant state condition; why regular action and symplectic flux cannot force it

**24 November 2026 — decisive physics-first boundary assessment.** This is a derivation from the source-locked original **longitudinal reduced** AeST action plus the established strict positive-Exp radiation asymptotics, **not** a new CLASS/DES numerical campaign, a proof of full 3+1 gauge/ADM equivalence, or a detection. It supplements the [original-action aether tilt and momentum analysis](ge19_20261123_original_action_aether_tilt_canonical_momentum_strict_exp_nofree_boundary.md), rather than overwriting the historical evidence.

**Direct source anchors inspected in this continuation:**
- [LW30 original ADM lapse/shift Hamiltonian and momentum](../ge19/lw30_exact_adm_hamiltonian_momentum_constraints_20261110.py), Git blob `b9d2751c1a858cd00d3ef44816e7f7300113f600`;
- [LW31 original aether coframe/action/shear](../ge19/lw31_action_spatial_traceless_shear_20261110.py), Git blob `6e41aebf8fdd4f1bc3339e92b9183fecb1503ed3`, with `Q_i=\cosh(u)\sigma+\sinh(u)p_x/L`, `Xi=\sinh(u)\sigma+\cosh(u)p_x/L`, `u=ik\alpha_A/a`, and `AE=NL R²[K_BE²+2CE Xi-C Xi²+2K(Q_i)]`;
- [LW32 covariant unit-aether and auxiliary-multiplier algebra](../ge19/lw32_covariant_aether_auxiliary_multiplier_elimination_20261110.py), Git blob `b10c7c74e3fd31ed902bc76cd09878c99332cd60`;
- [original quarter-action k² X/S hierarchy](../ge19/physics_gate/primordial_k2_XS_retarded_bath_hierarchy_20261122.py), Git blob `a7fa9069fb2670a0231ed8374d09ebd0b684d192`;
- [strict Exp early two-mode classification](ge19_20261123_original_action_aether_tilt_canonical_momentum_strict_exp_nofree_boundary.md), previous verified Git blob `8594a60456c49f295b35148588b87c0980864bfe`.

## I. One covariantly interpretable primordial condition removes BOTH free reduced modes

The original covariant action distinguishes the aether-parallel scalar gradient `Q=A^\mu\nabla_\mu\phi` from the aether-orthogonal scalar gradient `U_\mu=h_\mu{}^\nu\nabla_\nu\phi`, `h_\mu{}^\nu=\delta_\mu{}^\nu+A_\mu A^\nu`. Along a longitudinal Fourier direction, the original LW31 `Xi` is the signed orthogonal gradient, and the original field identity `chi=varphi+Q alpha_A=QX` gives **exactly at linear order**

```math
\boxed{\frac{\Xi}{Q}=\frac{ik\,\chi}{aQ}=\frac{ik}{a}X.}\tag{1}
```

Thus `\Xi/Q` is the signed relative scalar-clock/aether tilt *to linear order* (a physical scalar-plane perturbation, independent of the separately gauge-dependent `alpha_A`).

On the selected analytic branch `X=k²X_2+O(k⁴)`, and at strict positive-Exp radiation `a=A_r\sqrt{t}[1+o(1)]`, the two homogeneous scalar/aether modes, for identical Einstein/species data, have:

```math
\begin{array}{lll}
H_1:& X_{2,h1}\longrightarrow A_*,&
\Xi_{h1}/Q \sim ik³ A_*/(A_r\sqrt t)\to\infty\quad (A_*\ne0),\\
H_2:& X_{2,h2}\sim 2P_*\sqrt t/(A_rK_B),&
\Xi_{h2}/Q\longrightarrow
i\,2k³P_*/(A_r²K_B)\quad(P_*\ne0).
\end{array}\tag{2}
```

The physically past-forced no-free particular solution from the earlier **conditional** strict Exp theorem has `X_{2,\mathrm{nf}}=Dt²/[6\ln(t_\star/t)](1+o(1))`, so

```math
\boxed{
(\Xi/Q)_{\rm nf}\sim
\frac{i k³D}{6A_r}\frac{t^{3/2}}{\ln(t_\star/t)}
\longrightarrow0 .}\tag{3}
```

Hence the following **single, geometrically grounded primordial-state prescription**

```math
\boxed{
\lim_{t\to0^+} \frac{h_\mu{}^\nu\nabla_\nu\phi}
{A^\lambda\nabla_\lambda\phi}=0
\quad\text{(equivalently }\lim_{t\to0^+}\Xi/Q=0
\text{ along each fixed Fourier direction)}}
\tag{4}
```

**removes both H₁ and H₂** and retains the conditional physically forced no-free branch. In words: in the primordial past, the scalar clock and unit aether become **aligned**, and any later relative aether–scalar strain comes from actual Einstein/matter forcing. This is an intelligible **single-clock initial-state hypothesis** for gravitational elasticity with memory.

**Scientific status of Eq. (4):** it is **not** an equation of motion or a theorem forced by LW30–LW33, and is not known to be the uniquely required inflationary vacuum state of the full Einstein–AeST–NL0B theory. It defines a declared model variant (**PRIMORDIAL_ALIGNED_NOFREE**), which can be studied without tuning the free aether amplitude against DES. For fixed finite Fourier `k`, it is an asymptotic boundary condition. A uniform-in-`k` primordial CLASS initialization would require a separate proof that the `t\to0` and `k\to0` limits commute.

## II. Why the normal variational boundary term does NOT force P* = 0

The original local longitudinal action's momentum conjugate to aether tilt `alpha_A` (up to Fourier/overall normalization) is

```math
\pi_\alpha \propto 2a k²(K_BE_A+C\chi)
=2a k² S_A=2k^4P_2,\qquad P_2=aS_2.
```

For a **regular H₂ variation**, `\delta X_{2,h2}=O(\sqrt t)` while `\delta P_{2,h2}\to\delta P_*` stays finite. Since `\delta\alpha_A=k²\delta X_2` at fixed common scalar phase/metric to this order, the primordial surface term is

```math
\boxed{
\pi_\alpha\,\delta\alpha_A\ \propto\
2k^6 P_2\,\delta X_2 = O(\sqrt t)\longrightarrow0,
\quad \text{for arbitrary finite }P_* .
}\tag{5}
```

Thus simply requiring **vanishing local variational endpoint term** does **not** force `P_*=0`, because the admissible H₂ coordinate variation already vanishes as `t\to0`. It would be incorrect to derive the no-free-aether condition by claiming “free boundary variations imply P(0)=0” without specifying the physical variation space and action boundary counterterms.

This is the **isolated longitudinal** boundary term, not the full Einstein+scalar+aether ADM-reduced symplectic potential. Full constrained cross-terms may change the conclusion; none has been proved to enforce `P_*=0`.

## III. The reduced symplectic flux also leaves the H₂ amplitude free

At `eta=0+`, the original k² homogeneous `(X_2,P_2=aS_2)` flow is a 2-D time-dependent linear Hamiltonian system with zero matrix trace. Its equal-time canonical Wronskian is exactly conserved,

```math
\boxed{
W(\delta_1,\delta_2)=
\delta_1X_2\,\delta_2P_2-
\delta_1P_2\,\delta_2X_2,
\qquad \dot W=0 .}\tag{6}
```

For the two normalized early homogeneous branches, \(X_{h1}\to A_*\), \(P_{h1}=O(L^{3/2})\), \(X_{h2}\sim 2P_*\sqrt t/(A_rK_B)\), \(P_{h2}\to P_*\), \(L=\ln(t_\star/t)\). Their cross flux is

```math
W(H_1,H_2)
=A_*P_*+O(\sqrt t\,L^{3/2})\longrightarrow A_*P_*,
\tag{7}
```

and must equal the same finite value at every later regular time. After imposing bounded **relative** aether tilt, H₁ is removed; the remaining one-dimensional H₂ branch is **isotropic**:

```math
\boxed{W(H_2(P_1),H_2(P_2))=0\quad
\text{for all }P_1,P_2.}\tag{8}
```

Therefore a “vanishing symplectic flux at the singular past” condition, **within this reduced canonical sector**, also cannot decide whether `P_*=0` or `P_*\ne0`. That is an independent primordial state choice. Equation (8) is not a complete full-covariant phase-space flux calculation.

## IV. Independent Einstein density regularity does NOT remove H₂

The original reduced action has *direct* spatial-gradient density `D_A^{S}=-k² S_A/(3a²)`. On an H₂ homogeneous variation `S_A=k² P_*/a`, this term is

```math
\boxed{\Delta D_{A,4}^{S}=-\frac{k^4P_*}{3a³}[1+o(1)] .}\tag{9}
```

On the strictly positive Exp background the exact homogeneous AeST density is `\rho_A=(QK_Q-K)/3` with `K_Q=I_0/a³`. Therefore the **exact fractional direct-stress expression** is

```math
\frac{\Delta D_{A,4}^{S}}{\rho_A}
=-\frac{k^4P_*}{I_0 Q-a³K}
=-\frac{k^4P_*}{
I_0\bigl[Q_0+Z_0Z-\frac{Z_0}{2Z}(1-e^{-Z²})\bigr]}
\longrightarrow0
\quad (Z\to\infty).
\tag{10}
```

Relative to the total radiation density `\rho_r=\rho_{r0}/a⁴`,

```math
\boxed{
\frac{\Delta D_{A,4}^{S}}{\rho_r}
=-\frac{k^4P_*\,a}{3\rho_{r0}}
\longrightarrow0 .}\tag{11}
```

The direct aether-gradient density is therefore **fractionally negligible for H₂ in both the AeST and radiation sectors** as the strict positive Exp background is approached. This makes the H₂ mode difficult to exclude by *leading* gravitational-stress regularity alone. It does NOT prove the **full induced** k⁴ Einstein/phase/ordinary-fluid perturbation is finite or that H₂ satisfies all original 3+1 constraints, since `\delta Q_4,\delta\varphi_4,\Phi_4` and their backreaction must also be solved.

**Contrast H₁:** its `P_{h1}\sim-\frac{2I_0Z_0A_*}{3A_r²}\sqrt{3/2}\,L^{3/2}` produces `\Delta D^{S}_{A,4}/\rho_A\sim+2k^4 A_* L/(3A_r²)`, unbounded, consistent with rejecting H₁ by uniform perturbativity. Both branches can have vanishing *radiation-relative* direct gradient density because `aP_{h1}\to0`; relative to total radiation alone is not a sufficient selection criterion.

## V. The local action itself does NOT supply a hidden finite-energy selection

The LW31 original quadratic longitudinal aether sector contains

```math
L^{(2)}_{AE,long}\sim a³\left[
K_B\left(\frac{k}{a}E_A\right)^2
+2C\left(\frac{k}{a}E_A\right)\Xi
-C\Xi²\right].
```

For H₂, `E_{A,h2}\sim k²P_*/(A_rK_B\sqrt t)`, so the original **orthonormal electric amplitude** `(k/a)E_A\sim t^{-1}` diverges in absolute units, but normalized by the divergent background \(H\sim1/(2t)\) it has a finite limit:

```math
\boxed{
\lim_{t\to0}
\frac{(k/a)E_{A,h2}}{H}
=\frac{2k³P_*}{A_r²K_B}.
}\tag{12}
```

The orthogonal scalar invariant `\Xi\sim Q\Xi/Q\sim\sqrt L` also diverges *absolutely*, but relative to the background scalar temporal gradient `Q\sim\sqrt L` is finite. Requiring *absolute* boundedness of either field at the big-bang singularity would reject H₂, but is a **strictly stronger hypothesis** than bounded *fractional* perturbations around a singular background. The latter is the relevant comparison for linear cosmological perturbation theory.

For H₂ the isolated local electric quadratic action behaves like `a³[(k/a)E_A]^2=O(t^{-1/2})`, and the mixed `E\Xi` and `\Xi²` pieces are even less singular, so the **isolated action integral near the strict endpoint converges**. H₁ has an isolated electric integrand of order `t^{-1/2}L³`, also integrable despite its unbounded relative tilt. Thus **finite isolated longitudinal quadratic action does not eliminate either mode**. No full constrained Hamiltonian positivity or all-species action energy norm is established by this statement.

## VI. Decision and minimal next step, avoiding more numerical audit loops

**What is now genuinely established within the original reduced longitudinal action + Exp asymptotics:**

- The scalar–aether relative tilt `\Xi/Q` is a source-derived covariantly interpretable linear field ratio, not a made-up numerical mode selector.
- Demanding **only bounded relative tilt**, finite reduced action, finite relative direct density stress, vanishing reduced canonical endpoint term, or vanishing reduced symplectic flux **does not eliminate H₂**.
- **Declaring primordial scalar–aether alignment** `\Xi/Q\to0` eliminates both homogeneous reduced modes and selects the previously defined no-free Volterra solution provided its existence assumptions hold.
- The full covariant original action **has not** been shown to force this alignment; H₂ may be a legitimate additional primordial aether isocurvature degree of freedom until the full metric/scalar/aether k⁴ constraints and boundary conditions are solved.
- If H₂ is physically allowed, a unique memory prediction requires specifying its primordial amplitude \(P_*(k)\) independently of DES. If alignment is physically chosen, \(P_*(k)=0\) is an **explicit, falsifiable modeling assumption**, not a posterior observational fit.

**Decision:** name the research branch **PRIMORDIAL_ALIGNED_NOFREE (conditional)** and retain **PRIMORDIAL_FREE_TILT (unresolved full-covariant admissibility)** as its controlled alternative. Do not modify CLASS initial conditions, fit DES or claim observational detection from either without a full original-action matter–Weyl transfer.

**Status:** `COVARIANTLY_INTERPRETABLE_PRIMORDIAL_ALIGNMENT_BC_EXPLICIT / REDUCED_H2_NOT_EXCLUDED_BY_STANDARD_LOCAL_REGULARITY / FULL_COVARIANT_H2_ADMISSIBILITY_OPEN / FULL_PHYSICS_GO=false / DES_detection=false`.
