# GE19 LW14 — reconcile previous NL0B Ward PASS with LW13's total-stress constraint gap

**Date:** 2026-11-09. **Classification:** \`GE19_LW14_REDUCED_LINEAR_BATH_SCALAR_AETHER_WARD_PASS_TOTAL_ACTION_CLOSURE_OPEN\`.

**Bottom line:** the frozen NL0B analysis had **already** derived the scalar/aether redundancy and declared its eight-identity analytic completion PASS. LW13 did **not** discover that the memory bath lacks covariance. LW13 asks a **different, stronger verification**: do the **specific implemented** linear CLASS effective density, momentum, Einstein stress and all relevant scalar/aether equations faithfully realize the **complete coupled action's** on-shell total conservation identities? The present work rechecks the reduced quadratic memory source algebra, supplies a negative control, and specifies this remaining implementation/action dictionary. It does not rerun CLASS, change source parameters, or retroactively reclassify previously frozen results.

## 1. Source history and genuinely existing prior proof

The frozen initial action was preregistered in [NL0B predata](nl0b_predata_covariant_memory_completion.md) (Git blob \`9b1c013153faeddbd2add3d80eb29f673bc7748f\`). The [NL0B analytic result](nl0b_covariant_memory_completion_result.md) (blob \`d005b1c135fead856510aa76b6174fb9051fa552\`) explicitly records **Identity 6 PASS** (the bath has no *direct first-order* Einstein stress about FLRW) and **Identity 7 PASS** (bath scalar and aether perturbation sources are linearly related; no new independent scalar constraint in the original frozen model). The [canonical action](gravitational_elasticity_canonical_nl0b_interpretation.md), blob \`d4a774074ad6c69142bb6f00f5426949e98ca67b\`, uses original fields \`g,A,phi\`, \`X_mu=h_mu^nu nabla_nu phi\`, positive projected auxiliary \`U_j\`, and local completed-square potential, not a newly introduced linear-model parameter.

The separate original [H4F1 longitudinal bath spatial Ward](ge19_h4f1_longitudinal_bath_ward_valid_freeze.md) and [G2B off-shell spatial action covariance](ge19_g2b_direct_action_offshell_spatial_noether_2026-11-08.md) were also completed in their restricted action/geometry scopes. They are NOT substitutes for a full time-and-space perturbed CLASS scalar Einstein/AeST Noether proof, and H4/Z21 remains uncertified.

LW13, [conditional Hamiltonian propagation](ge19_lw13_conditional_hamiltonian_propagation_and_memory_ward_gap_2026-11-09.md), separately established
\[
C_H'+\mathcal H C_H
=\frac32a^2 J_D+\frac92\frac{a^2\mathcal H}{k^2}J_T
\]
**assuming** the exact standard total fluid stress conservation laws with residuals \`J_D,J_T\` and the original flat FLRW/CLASS equations. It did NOT independently compute the full-action \`J_D,J_T\` of the specific frozen source-code implementation.

## 2. Re-audit of the exact rank-one quadratic source

This one-mode algebra uses the already frozen **linear scalar** reduction of the completed-square action. At fixed background time, let \(\kappa=k/a>0\), \(Q=\dot{\bar\phi}\), \(w_j>0\), and let \(\varphi\), \(\alpha\), and \(q_j\) be the frozen original normalized scalar, spatial-aether potential and physical-eta-regularized bath coordinate.

The gauge-invariant source combination is
\[
\chi=\varphi+Q\alpha,\qquad X_L=\kappa\chi.
\]

For a single positive mode, the normalized reduced potential contribution is
\[
\mathcal L_{\rm pot}^{(2)}
=-\frac\eta4\left[
\omega q-\sqrt{w}\,\kappa(\varphi+Q\alpha)
\right]^2 .
\]
The kinetic term of the bath does not introduce any **new** \(\varphi\)- or \(\alpha\)-dependence in this fixed-background one-mode reduced potential variation.

Set
\[
B_\chi=w\chi-\frac{\omega\sqrt w}{\kappa}q.
\]
Then the original action variation gives
\[
\boxed{
\frac{\partial\mathcal L_{\rm pot}^{(2)}}{\partial\varphi}
=-\frac{\eta\kappa^2}{2}B_\chi,\qquad
\frac{\partial\mathcal L_{\rm pot}^{(2)}}{\partial\alpha}
=Q\,\frac{\partial\mathcal L_{\rm pot}^{(2)}}{\partial\varphi}.}
\]
In this reduced Fourier-mode normalization, the first derivatives of the potential correspond to the **unprojected** scalar and spatial-aether potential Euler sources. The CLASS E_rhs scalar-potential source first removes the original spatial-gradient and field-equation normalization; it is \(-\eta Q B_{\chi,\rm raw}/2\) in the frozen CLASS closure, **not** the unprojected \(-\eta Q\kappa^2 B_\chi/2\). Any comparison must retain the original projection and prefactors.

At fixed \(q\), the Hessian with respect to \((\varphi,\alpha)\) is
\[
\boxed{
H_{\varphi,\alpha}=-\frac{\eta w\kappa^2}{2}
\begin{pmatrix}1&Q\\Q&Q^2\end{pmatrix}.}
\]

It has **rank one** for nonzero positive \(\eta,w,\kappa\) and kills \((-Q,1)^T\) exactly. Accordingly,
\[
\boxed{\mathcal E_\alpha^{\rm bath}-Q\,\mathcal E_\varphi^{\rm bath}=0}
\]
within the **original reduced spatial scalar** Euler source normalization. The two sources are not independent constraints. This is a formula-level reconstruction of **previous NL0B Identity 7**. It is not a newly discovered symmetry. The degenerate Hessian direction follows from dependence on \(\chi\) only and does not indicate an additional propagating physical massless mode.

**Negative control:** if one writes the aether bath source but incorrectly omits its scalar partner in the **unreduced action field equations**, the difference \(\mathcal E_\alpha-Q(0)\) is nonzero for a generic \(q,\chi\). Thus such an intentionally incomplete original-action equation set violates the restricted Ward relation. This does **not** demonstrate that the actual CLASS effective-fluid implementation makes this mistake: its scalar Euler equation may be encoded by the transformed density and velocity equations and the original AeST constraints, as claimed by NL0B. That **mapping** requires explicit verification rather than inference from a search for an \`E_phi\` assignment in C code.

## 3. Metric stress: retain the prior result at its proper order

Because the homogeneous relaxed FLRW background has \(X_\mu^{(0)}=0\) and \(U_{j\mu}^{(0)}=0\), the original NL0B quadratic covariant action has neither background memory stress nor a **direct memory stress tensor linear in perturbation amplitude**. This is the already frozen **NL0B Identity 6** and has not been re-derived from a fresh complete metric variation in this phase. The \(\eta\)-dependent response of \(\delta_A,\theta_A\), and the **induced** first-order Einstein fluid stress are a different, indirect contribution through the original AeST field equations and cannot be dropped.

The local field action is diffeomorphism invariant with the aether normalization and \(A\cdot U=0\) constraints. The general Noether identity for such a constrained multi-field system relates the full metric, scalar, aether, auxiliary and multiplier Euler derivatives. It is satisfied on shell if every Euler equation is correctly implemented. The mere fact of formal covariance does not establish that an **independently approximated source-code fluid representation** is identical to those Euler equations at every approximation switch and redshift.

## 4. Where LW13's physical J_D,J_T gate actually remains

The original \`v019/apply_patch_v019.py\` uses total effective AeST stress in the CLASS density, momentum and pressure sources, and evolves \`delta_A\` and \`theta_A\` in fluid conservation form. The original \`v019j/apply_memory_patch.py\` adds the bath correction \`E_rhs_aest -= 0.5*Q_aest*Bchi_aest\` to the aether closure equation.

That construction is **compatible** with a conserved total effective fluid if the frozen field-to-fluid dictionary is exact. But conserved-looking equations are **not independently action variation**. The current LW14 algebra alone cannot decide whether:
- the physical scalar Euler partner is **implicitly reproduced** by those effective fluid rows, using the correct original AeST field redefinitions, or
- an omitted action term would generate a nonzero physical source residual \(J_D\) or \(J_T\) in the full first-order momentum/energy Bianchi identity.

The older NL0B analytic audit *argues* for the first option and classifies its eight analytical obligations PASS. In the LW13/LW14 **implementation-level evidence standard**, the missing proof is an **explicit equation-by-equation mapping from the complete first-order action Euler variations to the actual CLASS fluid \(D,T\) source rows**, with consistent bath scalar/aether factors, unit-aether/auxiliary constraints, and source-normalization conventions. A new proof must not simply assert "Noether implies zero" or set \(J_D=J_T=0\) because the code's equations look conservative.

Thus the correct reconciliation is:
- **Previous NL0B theoretical minimal covariant completion: PASS in its frozen analytic audit scope (unchanged).**
- **LW14 reduced source rank-one Ward: independently rechecked, PASS (existing identity).**
- **LW13 conditional total constraint propagation: PASS given total conservation.**
- **Actual full modified CLASS field-to-fluid action identity/physical J_D,J_T: OPEN.**
- **Physical two-history Weyl observer and sky detection: OPEN.**

## 5. Reproducibility

LW14 was formula-locked first in \`ge19/lw14_linear_covariant_bath_scalar_aether_ward_predata_20261109.json\` (commit \`f30c322eff1fa3e0c242fedfac28bea0cc02d830\`, Git blob \`b81c6399ae18ef609a40043fcd946a4b101e9826\`). It explicitly acknowledged the earlier NL0B Identity 7 PASS, and its central formula was therefore not blindly unknown before registration. Source-checking and exact SymPy gate implementation: \`ge19/lw14_linear_covariant_bath_scalar_aether_ward_20261109.py\` (commit \`335b9636123c9212d2e45eecf22736f89ab411bd\`). An independent small local SymPy 1.14.0 computation verified the exact force variation, rank-one Hessian, null vector, source proportionality and missing-partner negative control. It did **not** run the Git source-check script in the researcher's WSL. Machine-readable frozen reduced result: \`results/ge19_lw14_reduced_bath_scalar_aether_ward_symbolic_replay_20261109.json\` (commit \`42bc42476ce6489fbe39ac8ef9c90e634a301f27\`). No numerical CLASS solve, H4 or observed DES residuals was used.

### Optional exact local source-check reproduction (no CLASS)

~~~bash
set +e
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
python3 -u -m ge19.lw14_linear_covariant_bath_scalar_aether_ward_20261109 --self-test
python3 -u -m ge19.lw14_linear_covariant_bath_scalar_aether_ward_20261109
~~~

Run only if independently verifying the committed script; its algebraic result is already recorded. The only new scientific gate worth pursuing is **LW15: explicitly map the original AeST scalar/aether Euler system with the actual bath into effective fluid conservation \(D,T\) and check the Hamiltonian/Bianchi source residual**, without additional source-grid sweeps or observational refits.

**Preserve original limitations:** LW01 native Weyl source tangent PASS, LW03 radial quadrature FAIL, LW05 full cosmic-shear LOS BLOCK, LW06 native matter–Weyl cross PASS, LW07b DES n(z) mass supports candidates only, LW08 differential Weyl-vs-density response unresolved, LW09 bath history theorem PASS but physical pair OPEN, LW10 source pathway PASS, LW11 local Green only conditional, LW12 direct 5×5 Jacobian PASS full A_eff OPEN, LW13 conserved-total-stress Hamiltonian identity conditional PASS, H4/Z21 uncertified, no astronomical gravitational-memory detection.
