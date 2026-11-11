# GE19 — the missing linear scalar **spatial Einstein trace** from the ORIGINAL GE06 action

**11 November 2026. Analytical physics-only result, not a new LW campaign.**  
**Classification:** \`GE19_ORIGINAL_REDUCED_ACTION_ALL_FOUR_SCALAR_EINSTEIN_ROWS_SUPPORTED / FULL_CLASS_PHYSICS_GO_OPEN\`.

This calculation extends the already archived **LW30 Hamiltonian/momentum** and **LW31 traceless spatial** equations by deriving the **spatial trace**, from exactly the same frozen GR+AeST+NL0B plane-symmetric scalar action. The algebra was independently evaluated with SymPy 1.14 in the model's isolated calculation runtime, using the original GE06/GE05 formulae transcribed from the source; it has **not** been independently rerun as a source-locked researcher WSL package. No CLASS, new eta runs, H4/Z21, DES data, or parameter adjustment.

**Important boundary:** the equation below is action-derived for the reduced *linear scalar sector* and the AeST-only FLRW background. It is **not** a proof of the full cosmological all-species source-to-CLASS operator or numerical constraint propagation.

## 1. Original Lagrangian and independent variations before gauge fixing

The original fixed source \`ge06/analytic_aest_directional_source_generator.py\`, original Git blob \`a7afe0035054a9dca55d74a6497c081422114b4c\`, defines
\[
ds^2=-N^2dt^2+L^2(dx+b\,dt)^2+R^2(dy^2+dz^2),
\]
\[
k_L=\frac{\dot L-bL_x-Lb_x}{NL},\quad
k_R=\frac{\dot R-bR_x}{NR},\quad
\mathcal L_{\rm GR}=NLR^2(-4k_Lk_R-2k_R^2)+\frac{2NR_x^2}{L}+\frac{4N_xRR_x}{L},
\]
\[
\mathcal L_A=NLR^2[K_BE^2+2CEX-CX^2+2K(Q_{\rm inv})],\qquad C=2-K_B.
\]
The original \`ge05/memory_directional_source_generator.py\`, Git blob \`40837d77f89028da30c28899e2d0530a4401844e\`, supplies the normalized positive per-mode bath
\[
\mathcal L_{\rm bath}=\frac{\eta NLR^2}{4}[(Aq)^2-(\omega q-\sqrt w X)^2].
\]
All three densities share the same overall gravitational normalization. On relaxed homogeneous FLRW, \(X=E=q=0\). The bath therefore has no **direct first-order spatial Einstein** source, though it changes metric dynamics indirectly through scalar and aether perturbations.

Crucially, compute **both** independent Euler equations *before* imposing \(L=R\) and \(b=0\):
\[
\mathcal E_L=\partial_L\mathcal L-\partial_t\partial_{\dot L}\mathcal L-
\partial_x\partial_{L_x}\mathcal L,
\quad
\mathcal E_R=\partial_R\mathcal L-\partial_t\partial_{\dot R}\mathcal L-
\partial_x\partial_{R_x}\mathcal L.
\]
Because \(R\) carries **both** transverse \(y,z\) metric directions, the scalar spatial **trace** is proportional to
\[
\boxed{\mathcal T=a(\mathcal E_L^{(1)}+\mathcal E_R^{(1)})}
\]
where superscript \((1)\) means first perturbative coefficient. The complementary traceless projection \(a(\mathcal E_L^{(1)}-\tfrac12\mathcal E_R^{(1)})\) reproduces LW31, namely \(2ak^2(\Phi-\Psi)\). The exact first-order \(L/R\) variations retain lapse, shift and both independent spatial directions.

For the Newtonian-gauge *evaluation after variation* use
\[
N=1+\Psi,\qquad L=R=a(1-\Phi),\qquad b=0,\qquad
u=ik\alpha/a,\quad \phi=\bar\phi+\varphi,
\]
and \(H=\dot a/a\), \(\delta Q=\dot\varphi-Q\Psi\).
The \(\Phi,\Psi\) amplitudes need not obey the background equations during the Euler variation.

## 2. Exact action-derived Euler coefficients before background specialization

Let \(K_0=K(Q)\), \(K_Q=\partial K/\partial Q\). The calculated background **spatial** equations are
\[
\mathcal E_{L,0}^{\rm GR}=2a^2(3H^2+2\dot H),\quad
\mathcal E_{R,0}^{\rm GR}=4a^2(3H^2+2\dot H),
\]
\[
\mathcal E_{L,0}^{A}=2a^2 K_0,\quad
\mathcal E_{R,0}^{A}=4a^2 K_0,\quad
\mathcal E_{L,0}^{\rm bath}=\mathcal E_{R,0}^{\rm bath}=0.
\]
Define the *unimposed* background pressure residual
\[
\mathcal B_P\equiv3H^2+2\dot H+K_0.
\]
An independently assembled pair of spatial Euler variations gives the **complete off-background-shell first-order identity**
\[
\boxed{\begin{aligned}
\mathcal T={}&-12a^3\bigg[
\ddot\Phi+H(3\dot\Phi+\dot\Psi)
+(3H^2+2\dot H)\Psi\\
&\quad+\frac{k^2}{3a^2}(\Phi-\Psi)-\frac{K_Q}{2}(\dot\varphi-Q\Psi)
\bigg]\\
&-6a^3(2\Phi-\Psi)\mathcal B_P.
\end{aligned}}\tag{T}
\]
It is algebraically exact under the above fixed GE06/GE05 first-jet action and convention: the difference between the independently assembled Euler expression and the right-hand side factorizes to **zero**. It was obtained without assuming \(K_Q Q=-2\dot H\), or replacing the background pressure equation prematurely. All terms involving \(\Phi\), \(\Psi\), \(\dot\Phi\), \(\dot\Psi\), \(\ddot\Phi\), \(H,\dot H\), \(k^2\) and \(\dot\varphi\) were retained until the identity was checked.

Specifically, the independent ingredients in (T) are
\[
\mathcal T_{\rm GR}
=-2a\Big[
a^2(18H^2\Phi+9H^2\Psi+18H\dot\Phi+6H\dot\Psi
+12\dot H\Phi+6\dot H\Psi+6\ddot\Phi)+2k^2(\Phi-\Psi)
\Big],
\]
\[
\mathcal T_A=-6a^3[2K_0\Phi-K_0\Psi+K_Q Q\Psi-K_Q\dot\varphi],
\qquad \mathcal T_{\rm bath}=0.
\]
These sum to (T) identically. An optional background-covariant weighting \(L\mathcal E_L+(R\mathcal E_R)\) differs by terms proportional to the **same** background residual \(\mathcal B_P\), hence it agrees on the intended physical background.

## 3. On the original AeST-only FLRW background: exact CLASS-form pressure equation

Set only the originally derived background spatial Euler equation \(\mathcal B_P=0\), and impose \(\mathcal T=0\). The original **action** pressure perturbation in the same state dictionary is
\[
P_A^{\rm action}=\frac13K_Q\delta Q.
\]
Then the complete scalar spatial Einstein trace equation is
\[
\boxed{
\ddot\Phi+H(3\dot\Phi+\dot\Psi)+(3H^2+2\dot H)\Psi
+\frac{k^2}{3a^2}(\Phi-\Psi)=\frac32P_A^{\rm action}.
}\tag{P}
\]
This has the expected Newtonian-gauge cosmological **Einstein pressure/trace form** in the original scalar normalization and \(k\) convention, *without postulating a bath metric pressure source or tuning the scalar E coefficient*. The LW31 **traceless** result implies \(\Phi-\Psi=0\) only for the **restricted AeST-only** scalar model without other anisotropic stress; do not silently use this equality once photons or neutrinos are included.

Adding separately minimally coupled species in the *full* cosmology produces their ordinary pressure and shear sources, and changes the homogeneous background pressure equation. That full all-species coupled projection has **not** been independently performed here, so Eq. (P) is **not yet a CLASS production certification**.

## 4. Actual advance and what remains before PHYSICS_GO

Within this one fixed reduced linear scalar action:

| Einstein scalar row | Status |
|---|---|
| Hamiltonian (lapse) | **Action-derived LW30** |
| Momentum (shift) | **Action-derived LW30** |
| Traceless spatial/shear | **Action-derived LW31** |
| **Spatial trace / pressure** | **Action-derived here**; exact off-background-shell (T) |

The **full restricted metric scalar block is now accounted for**. Coupled with LW32 regular multiplier elimination and LW33's exact off-shell scalar-charge identity, the quarter source is the unique choice compatible with the **fixed original reduced action/dictionary** for generic nonzero eta and bath force. This is a stronger theory result than the small unconverged finite-eta native CLASS W difference, and it is independent of DES data.

**Not yet established:** the full **unreduced** covariant action's all-species and all-branch projection into CLASS \((D_A,T_A,\alpha_A,E_A,\Phi,\Psi)\) and auxiliary states; exact initial-condition/gauge continuity and independently confirmed physical constraint propagation of that **implemented** system; physically normalized retarded matter–Weyl cross transfer. Note that code-level fluid conservation and Einstein constraint propagation alone are **not** discriminating for an arbitrarily injected E-source (LW15); the **full scalar Euler and aether source rows** must agree with the action. Thus the production \`PHYSICS_GO\` is still **BLOCK**, and the observed DES Y3 gamma_t likelihood has not been run.

The original frozen \`v019j\` CLASS half source is not silently changed, and the separate quarter-source candidate remains a source-level exploratory build with exact eta=0 equivalence but unresolved finite-eta numerical signed shape. No new numerical calculation or WSL command is needed for this theory result.

## Reproducibility / scope of the reported algebra

One independent isolated SymPy 1.14 evaluation recreated the *exact* public original GE06/GE05 scalar longitudinal action first jets, performed the independent \(L\), \(R\), \(L_t\), \(R_t\), \(L_x\), \(R_x\) Euler differentiations, substituted the Newtonian-mode fields **after variation**, and compared the resulting expression to (T) by exact symbolic factorization. The original canonical full LW31 source snippet \`ge19/lw31_action_spatial_traceless_shear_20261110.py\` supplied the *same* field-jet dictionary for cross-check. This is an independent analytic continuation of that logic, but **no separate new source-locked WSL original output has been claimed**.

No arbitrary precision target, eta sweep, numerical CLASS job, synthetic data, empirical detection or blind preregistration was used.

Original sources and prior evidence:
- \`ge06/analytic_aest_directional_source_generator.py\` (Git blob \`a7afe0035054a9dca55d74a6497c081422114b4c\`)
- \`ge05/memory_directional_source_generator.py\` (Git blob \`40837d77f89028da30c28899e2d0530a4401844e\`)
- [LW30](ge19_lw30_original_gr_aest_adm_scalar_constraints_class_bridge_2026-11-10.md)
- [LW31](ge19_lw31_original_action_spatial_traceless_Einstein_shear_2026-11-10.md)
- [LW32](ge19_lw32_covariant_unit_aether_auxiliary_multiplier_exact_elimination_2026-11-10.md)
- [LW33](ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md)
- [11 November joint Noether/scalar source decision](ge19_20261111_physics_first_noether_scalar_source_closure_decision.md).
