# GE19 — Exact Einstein-constraint Weyl identity and the delayed-memory cancellation condition

15 November 2026. Physics-first continuation of the frozen GE05/GE06 scalar-action and all-species source documents. No CLASS, DES, parameter sweep, observational significance, or new numerical experiment.

**Classification: EXACT_CONSTRAINT_TO_WEYL_ALGEBRA / RESTRICTED_AEST_ELECTRIC_TO_METRIC_COEFFICIENT_EXHIBITED / NONZERO_FULL_PHYSICAL_DELAYED_RESPONSE_NOT_PROVED / PHYSICS_BLOCK.**

## 1. Assumptions and equations

Use cosmic time, fixed Fourier mode k>0, background a>0 and H, scalar Newtonian gauge metric (Phi,Psi), and the *same fixed normalization as the existing GE19/CLASS source documents*. Let D_tot be the sum of the original AeST effective stress density and all distinct ordinary species' densities; let T_tot be their sum of momentum-divergence stress terms; let S_shear be the *full* normalized anisotropic stress including photons and free-streaming neutrinos, not an AeST-only assumption. No double-counting of the repurposed CLASS CDM slot.

Assume the **exact** linear Einstein constraint equations for this physical total stress,
\`\`\`math
\frac{k^2}{a^2}\Phi+3H(\dot\Phi+H\Psi)+\frac32D_{\rm tot}=0,
\qquad
\dot\Phi+H\Psi=\frac{3a}{2k^2}T_{\rm tot},
\qquad
\Phi-\Psi=\frac{9a^2}{2k^2}S_{\rm shear}.
\`\`\`
The first constraint is a full-action *hypothesis* in a multi-species setting, although it is derived for the restricted original AeST-only action and the latter two are source-level CLASS compatible. This distinction is essential.

The GE06 reduced original-action fluid dictionary (conditionally valid on the physical action-to-fluid constraint surface) is
\`\`\`math
D_A=\frac13\left[QK_{QQ}\delta Q-\frac{k^2}{a^2}(K_BE_A+C\chi)\right],
\quad
T_A=\frac{K_Qk^2}{3a}\varphi,\quad
\chi=\varphi+Q\alpha_A,\quad C=2-K_B.
\`\`\`
Write D_tot=D_A+D_o, T_tot=T_A+T_o. The original restricted bath stress has zero *direct* linear metric stress about the relaxed background, but can affect all these stresses indirectly through evolution. The background a,H is held fixed when taking the eta derivative.

## 2. Constraint-elimination theorem

**Claim:** with W=(Phi+Psi)/2 in the model's Newtonian-gauge Bardeen convention,
\`\`\`math
\boxed{W=-\frac{3a^2}{2k^2}\left(D_{\rm tot}+\frac{3aH}{k^2}T_{\rm tot}\right)
-\frac{9a^2}{4k^2}S_{\rm shear}.}
\tag{1}
\`\`\`
Substitution of the fixed original-action AeST fluid dictionary gives
\`\`\`math
\boxed{\begin{aligned}
W={}&\frac{K_B}{2}E_A+\frac C2\chi
-\frac{a^2QK_{QQ}}{2k^2}\delta Q
-\frac{3a^2HK_Q}{2k^2}\varphi\\
&-\frac{3a^2}{2k^2}\left(D_o+\frac{3aH}{k^2}T_o\right)
-\frac{9a^2}{4k^2}S_{\rm shear}.
\end{aligned}}\tag{2}
\`\`\`
**Proof:** replace dotPhi+H Psi in the Hamiltonian constraint with the momentum constraint, solve algebraically for Phi. By the shear equation, Psi=Phi-9a² S_shear/(2k²), so W=Phi-9a² S_shear/(4k²), proving (1). Insert D_A and T_A, collect coefficients; the term -3a²/(2k²)*[-k² K_B E_A/(3a²)] equals **+K_B E_A/2** exactly. QED.

The fact that the Einstein-constraint representation has a nonzero coefficient +K_B/2 of E_A (K_B>0) establishes a **structural electric-to-metric entry** in this particular representation. It does NOT imply a nonzero physical response on the complete dynamical constraint submanifold: deltaQ, chi, varphi, standard-species feedback and shear can cancel it exactly. No claim is made that E_A can be perturbed independently while preserving every Euler equation.

## 3. Exact history-only Weyl cancellation criterion

Assume a full physical constrained linear eta-tangent has been established and define the **source-decomposition difference** \`delta_h X = X_{1,retarded}-X_{1,instantaneous}\`, with identical eta=0 physical background, eta=0 trajectory, initial tangent, physical equation/operator, gauge fixing and observer. This decomposition remains conditional until the actual full action and initial conditions determine the physical tangent.

Linearity of (2), with background held fixed, gives
\`\`\`math
\boxed{\begin{aligned}
\delta_h W={}&\frac{K_B}{2}\delta_h E_A+\frac C2\delta_h\chi
-\frac{a^2QK_{QQ}}{2k^2}\delta_h(\delta Q)
-\frac{3a^2HK_Q}{2k^2}\delta_h\varphi\\
&-\frac{3a^2}{2k^2}\left(\delta_h D_o+\frac{3aH}{k^2}\delta_h T_o\right)
-\frac{9a^2}{4k^2}\delta_h S_{\rm shear}.
\end{aligned}}\tag{3}
\`\`\`
All variations in (3) are *eta-tangent history-only differences*, not differences of cosmological background histories. A nonzero history-only electric response proves a nonzero history-only Weyl output at an observation time **if and only if** the sum of the remaining terms fails to equal \`-K_B delta_h E_A/2\` there. This is a usable **exact cancellation condition**, not a nonvanishing proof.

Equivalent total-source statement:
\`\`\`math
\delta_h W= -\frac{3a^2}{2k^2}
\left(\delta_h D_{\rm tot}+\frac{3aH}{k^2}\delta_h T_{\rm tot}
+\frac32\delta_h S_{\rm shear}\right).\tag{4}
\`\`\`
Equation (4) is the observable constraint closure test: a physical nonzero delayed Weyl response requires a nonvanishing *specific comoving total-stress-plus-shear combination*, not merely q_j != 0 or E_A != 0.

## 4. Relation to the already proved retarded overlap theorem

The 15 November previous document gave the conditional nested Green convolution for \`delta_h W(T)\`. Equations (3)–(4) specify the Weyl projector **on a constrained state**, rather than leaving it wholly abstract. They do not supply the full A0, projected b_E, physical initial eigenvector, or resulting transfer. In the exact full constrained formulation (3) must equal the double-Volterra output for every allowed history and physical initial condition. This yields a demanding, independently derived **identity check** for future operator closure.

In particular, the reduced early-time fourth-order electric onset from the 14 November proof is NOT automatically a fourth-order gravitational onset. No assumption that ordinary species, deltaQ, varphi, or chi have zero delayed response is presently physically certified.

## 5. Decision and next irreducible physics step

**Proved algebraically under the stated Einstein/dictionary constraints:** (1)–(4), including the +K_B/2 electric entry and the exact cancellation condition.

**Not proved:** full covariant Einstein–AeST–NL0B action operator equivalence; complete constraint-preserving eta-dependent growing adiabatic eigenvector; nonzero delayed projected physical Weyl response; new propagating free mode; detectable lensing signal.

The next necessary action is to derive and close the *full coupled temporal scalar/aether Euler and linear all-species physical perturbation system* against equations (3)–(4), using the exact initial adiabatic condition delta_A/(1+w_A)=3 delta_gamma/4 and correct gauge transport. If the full dynamical equations imply cancellation, record it as a physical obstruction. If they give a nonzero signed overlap, establish its nonvanishing with an analytic leading coefficient or a validated bound **before** new CLASS/DES work.

This document is not a PHYSICS_GO certificate. No historical v019j half coefficient was modified.

## References (existing frozen project sources)
- [Prior constrained delayed-overlap theorem](ge19_20261115_constrained_delayed_weyl_transfer_proof_gate.md)
- [All-species Einstein constraint source, pressureful AeST IC issue](ge19_20261111_all_species_Einstein_operator_and_adiabatic_IC_block.md)
- [Original reduced action-to-CLASS stress/phase mapping](ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md)
- [LW30 lapse/shift constraints](ge19_lw30_original_gr_aest_adm_scalar_constraints_class_bridge_2026-11-10.md)
- [LW31 traceless spatial equation](ge19_lw31_original_action_spatial_traceless_Einstein_shear_2026-11-10.md)
- [13–14 November retarded action/Noether proof](ge19_20261114_noether_constraint_and_eta0_retarded_branch_theorems.md)
